from application import app
from flask import Response, request, url_for
import json
import logging
import requests
from jsonschema import validate

@app.route('/', methods=["GET"])
def index():
	return Response(status=200)

@app.route('/register', methods=["POST"])
def register():
	if request.headers['Content-Type'] != "application/json":
		return Response(status=415)  # 415 (Unsupported Media Type)

	json_data = request.get_json(force=True)

	schema = {
		"type" : "object",
		"properties" : {
			"keynumber" : {"type" : "string"},
			"ref" : {"type" : "string"},
			"date" : {"type" : "string"},
			"forename" : {"type" : "string"},
			"surname" : {"type" : "string"},
		},
	}
	validate (json_data,schema)

	url = 'http://10.0.2.2:5002/register'

	headers = {'Content-Type': 'application/json'}

	response = requests.post(url, data=json.dumps(json_data), headers=headers)

	if response.status_code == 200:
		data = {
			"message": "Register complete"
		}
		return Response(json.dumps(data), status=200, mimetype='application/json')
	else:
		logging.error("Received " + response.status_code)
		return Response(response.status_code)




