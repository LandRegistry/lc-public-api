import pytest
from unittest import mock
from application.routes import app
import requests

class FakeResponse(requests.Response):
    def __init__(self, content='', status_code=200):
        super(FakeResponse, self).__init__()
        self._content = content
        self._content_consumed = True
        self.status_code = status_code

reg_data = '{"keynumber": "222222", "ref": "myref", "date": "16/06/2015", "forename": "John", "surname": "Watson"}'
class TestB2BApi:
    def setup_method(self, method):
        self.app = app.test_client()

    def test_reality(self):
        assert 1 + 2 == 3

    def test_healthcheck(self):
        response = self.app.get("/")
        assert response.status_code == 200

    def test_notfound(self):
        response = self.app.get("/doesnt_exist")
        assert response.status_code == 404

    #test for successful registration
    fake_success = FakeResponse('stuff',200)
    @mock.patch('requests.post', return_value=fake_success)
    def test_register(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data= reg_data, headers=headers)
        assert response.status_code == 200
        assert('complete' in response.data.decode())

    #test for incorrect data type in schema
    fake_success = FakeResponse('stuff',200)
    @mock.patch('requests.post', return_value=fake_success)
    def test_schemafail(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        reg_error = '{"keynumber": 222222, "ref": "myref", "date": "16/06/2015", "forename": "John", "surname": "Watson"}'
        response = self.app.post('/register', data= reg_error, headers=headers)
        assert response.status_code == 500

    #test that call to b2b processor failed
    fake_success = FakeResponse('stuff',400)
    @mock.patch('requests.post', return_value=fake_success)
    def test_registerfail(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data= reg_data, headers=headers)
        assert response.status_code != 200

    #test for incorrect header type
    fake_success = FakeResponse('stuff',200)
    @mock.patch('requests.post', return_value=fake_success)
    def test_contentfail(self, mock_post):
        headers = {'Content-Type': 'text'}
        response = self.app.post('/register', data= reg_data, headers=headers)
        assert response.status_code == 415

