from application import app
from flask import Response, request
import json
import logging
import requests
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


@app.route('/bankruptcies', methods=["POST"])
def register():
    if request.headers['Content-Type'] != "application/json":
        return Response(status=415)  # 415 (Unsupported Media Type)

    json_data = request.get_json(force=True)
    val = Draft4Validator(full_schema)
    errors = []
    for error in val.iter_errors(json_data):
        # Should be able to express the error location using JSONPath:
        path = "$"
        while len(error.path) > 0:
            item = error.path.popleft()
            if isinstance(item, int): # This is an assumption!
                path += "[" + str(item) + "]"
            else:
                path += "." + item
        if path == '$':
            path = '$.'
        errors.append({
            "location": path,
            "error_message": error.message
        })

    if json_data['residence_withheld'] is False and not json_data['residence']:
        message = "'residence' is a required property when 'address_withheld' is false"
        errors.append({
            'location': '',
            'error_message': message
        })

    if json_data['residence_withheld'] is True \
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
        return Response(json.dumps(data), status=400, mimetype='application/json')

    url = app.config['B2B_PROCESSOR_URL'] + '/bankruptcies'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(json_data), headers=headers)

    if response.status_code == 200:
        print(response.content)
        data = {
            "new_registrations": json.loads(response.content.decode('utf-8'))['new_registrations'],
            'application_type': json_data['application_type'],
            'application_ref': json_data['application_ref']
        }

        return Response(json.dumps(data), status=202, mimetype='application/json')
    else:
        logging.error("Received " + str(response.status_code))
        return Response(status=response.status_code)
