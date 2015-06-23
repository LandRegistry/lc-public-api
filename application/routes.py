from application import app
from flask import Response, request
import json
import logging
import requests
from jsonschema import validate
from jsonschema.exceptions import ValidationError


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
        "postcode": {"type": "string"}
    },
    "required": ["address_lines", "postcode"]
}

date_schema = {
    "type": "string",
    "pattern": "^([0-9]{4}-[0-9]{2}-[0-9]{2})$"
}

full_schema = {
    "type": "object",
    "properties": {
        "key_number": {"type": "string"},
        "application_ref": {"type": "string"},
        "date": date_schema,
        "debtor_name": name_schema,
        "debtor_alternative_name": {
            "type": "array",
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
        "business_address": address_schema,
        "date_of_birth": date_schema,
        "investment_property": {
            "type": "array",
            "items": address_schema
        }
    },
    "required": ["key_number", "application_ref", "date", "debtor_name", "residence_withheld"]
}


@app.route('/', methods=["GET"])
def index():
    return Response(status=200)


@app.route('/register', methods=["POST"])
def register():
    if request.headers['Content-Type'] != "application/json":
        return Response(status=415)  # 415 (Unsupported Media Type)

    json_data = request.get_json(force=True)
    try:
        validate(json_data, full_schema)
    except ValidationError as error:
        message = "{}\n{}".format(error.message, error.path)
        return Response(message, status=400)

    if json_data['residence_withheld'] is False and not json_data['residence']:
        message = "No residence included for the debtor. Residence required unless withheld."
        return Response(message, status=400)

    url = 'http://10.0.2.2:5002/register'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(json_data), headers=headers)

    if response.status_code == 200:
        data = {
            "message": "Register complete"
        }
        return Response(json.dumps(data), status=202, mimetype='application/json')
    else:
        logging.error("Received " + str(response.status_code))
        return Response(response.status_code)