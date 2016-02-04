from application import app
from flask import Response, request
import json
import logging
import requests
import traceback
import kombu
import re
from jsonschema import Draft4Validator


name_schema = {
    "type": "object",
    "properties": {
        "forenames": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
        },
        "surname": {"type": "string"}
    },
    "required": ["forenames", "surname"]
}

address_schema = {
    "type": "object",
    "properties": {
        "address_lines": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1
        },
        "county": {"type": "string"},
        "postcode": {"type": "string"}
    },
    "required": ["address_lines", "postcode", "county"]
}

date_schema = {
    "type": "string",
    "pattern": "^([0-9]{4}-[0-9]{2}-[0-9]{2})$"
}

full_schema = {
    "type": "object",
    "properties": {
        "key_number": {
            "type": "string",
            "pattern": "^\d+$"
        },
        "application_type": {
            "type": "string",
            "enum": ["PA(B)", "WO(B)"]
        },
        "application_ref": {"type": "string"},
        "application_date": date_schema,
        "debtor_names": {
            "type": "array",
            "minItems": 1,
            "items": name_schema
        },
        "gender": {"type": "string"},
        "occupation": {"type": "string"},
        "trading_name": {"type": "string"},
        "residence": {
            "type": "array",
            "items": address_schema
        },
        "residence_withheld": {"type": "boolean"},
        "business_address": {
            "type": "array",
            "items": address_schema
        },
        "date_of_birth": date_schema,
        "investment_property": {
            "type": "array",
            "items": address_schema
        }
    },
    "required": ["key_number", "application_type", "application_ref", "application_date", "debtor_names",
                 "residence_withheld"]
}


def check_processor_health():
    return requests.get(app.config['B2B_PROCESSOR_URL'] + '/health')


application_dependencies = [
    {
        "name": "b2b-processor",
        "check": check_processor_health
    }
]


@app.route('/', methods=["GET"])
def index():
    return Response(status=200)


@app.route('/health', methods=['GET'])
def health():
    result = {
        'status': 'OK',
        'dependencies': {}
    }

    status = 200
    for dependency in application_dependencies:
        response = dependency["check"]()
        if response.status_code != 200:
            status = 500

        result['dependencies'][dependency['name']] = str(response.status_code) + ' ' + response.reason
        data = json.loads(response.content.decode('utf-8'))
        for key in data['dependencies']:
            result['dependencies'][key] = data['dependencies'][key]

    return Response(json.dumps(result), status=status, mimetype='application/json')


@app.errorhandler(Exception)
def error_handler(err):
    logging.error('Unhandled exception: ' + str(err))
    call_stack = traceback.format_exc()

    lines = call_stack.split("\n")
    for line in lines:
        logging.error(line)

    error = {
        "type": "F",
        "message": str(err),
        "stack": call_stack
    }
    raise_error(error)
    return Response(json.dumps(error), status=500)


@app.before_request
def before_request():
    logging.info("BEGIN %s %s [%s] (%s)",
                 request.method, request.url, request.remote_addr, request.__hash__())


@app.after_request
def after_request(response):
    logging.info('END %s %s [%s] (%s) -- %s',
                 request.method, request.url, request.remote_addr, request.__hash__(),
                 response.status)
    return response


@app.route('/bankruptcies', methods=["POST"])
def register():
    if request.headers['Content-Type'] != "application/json":
        logging.info("Invalid Content-Type - rejecting")
        return Response(status=415)  # 415 (Unsupported Media Type)

    request_text = request.data.decode('utf-8')
    logging.info("Data received: %s", re.sub(r"\r?\n", "", request_text))
    json_data = request.get_json(force=True)
    val = Draft4Validator(full_schema)
    errors = []
    for error in val.iter_errors(json_data):
        # Should be able to express the error location using JSONPath:
        path = "$"
        while len(error.path) > 0:
            item = error.path.popleft()
            if isinstance(item, int):  # This is an assumption!
                path += "[" + str(item) + "]"
            else:
                path += "." + item
        if path == '$':
            path = '$.'
        errors.append({
            "location": path,
            "error_message": error.message
        })

    if 'residence_withheld' in json_data and \
            json_data['residence_withheld'] is False \
            and not json_data['residence']:
        message = "'residence' is a required property when 'address_withheld' is false"
        errors.append({
            'location': '',
            'error_message': message
        })

    if 'residence_withheld' in json_data and json_data['residence_withheld'] is True \
            and 'residence' in json_data and len(json_data['residence']) > 0:
        errors.append({
            'location': '',
            'error_message': "'residence' may not be supplied when 'address_withheld' is true"
        })

    if len(errors) > 0:
        data = {
            'errors': errors,
        }
        if 'application_ref' in json_data:
            data['application_ref'] = json_data['application_ref']
        else:
            data['application_ref'] = ''

        body = json.dumps(data)
        logging.info("Invalid submission: {}".format(body))
        return Response(body, status=400, mimetype='application/json')

    url = app.config['B2B_PROCESSOR_URL'] + '/bankruptcies'
    headers = {'Content-Type': 'application/json'}

    json_data['original_request'] = request_text
    json_data['customer_name'] = '[INS PLACEHOLDER HERE! FIXME]'
    json_data['customer_address'] = '[INS PLACEHOLDER HERE! FIXME]'
    response = requests.post(url, data=json.dumps(json_data), headers=headers)

    if response.status_code == 200:
        response_text = response.content.decode('utf-8')
        logging.info('POST {} -- {}'.format(url, response.status_code))
        logging.info("Successful registration: {}".format(response_text))
        data = {
            "new_registrations": json.loads(response_text)['new_registrations'],
            'application_type': json_data['application_type'],
            'application_ref': json_data['application_ref']
        }

        return Response(json.dumps(data), status=201, mimetype='application/json')
    else:
        raise RuntimeError("Unexpected response from {} -- {}".format(url, response.status_code))


def raise_error(error):
    hostname = "amqp://{}:{}@{}:{}".format(app.config['MQ_USERNAME'], app.config['MQ_PASSWORD'],
                                           app.config['MQ_HOSTNAME'], app.config['MQ_PORT'])
    connection = kombu.Connection(hostname=hostname)
    producer = connection.SimpleQueue('errors')
    producer.put(error)
    logging.warning('Error successfully raised.')
