from unittest import mock
from application.routes import app
import requests
from tests import test_data
import json


class FakeResponse(requests.Response):
    def __init__(self, content='', status_code=200):
        super(FakeResponse, self).__init__()
        self._content = content
        self._content_consumed = True
        self.status_code = status_code
        self.reason = 'TEST'


my_reg_data = test_data.addr_withheld


class TestB2BApi:
    def setup_method(self, method):
        self.app = app.test_client()

    def test_health_check(self):
        response = self.app.get("/")
        assert response.status_code == 200

    def test_not_found(self):
        response = self.app.get("/doesnt_exist")
        assert response.status_code == 404

    # test for successful registration where debtor has 1 residence
    fake_success = FakeResponse('{"new_regs": [50001]}'.encode(), 200)
    fake_failure = FakeResponse('', 404)
    fake_healthcheck = FakeResponse('{"dependencies": {"an-app": "200 OK"} }'.encode(), 200)

    @mock.patch('requests.post', return_value=fake_success)
    def test_register(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.residence_1, headers=headers)
        assert response.status_code == 202
        assert ('complete' in response.data.decode())

    # test where the residence_withheld flag is set on - pass
    @mock.patch('requests.post', return_value=fake_success)
    def test_witheld_flag(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.addr_withheld, headers=headers)
        assert response.status_code == 202
        assert ('complete' in response.data.decode())

    # test where the residence_withheld flag is set off but no residence exists - fail
    @mock.patch('requests.post', return_value=fake_success)
    def test_witheld_flag_fail(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.withheld_flag_fail, headers=headers)
        assert response.status_code == 400
        assert ('No residence included for the debtor' in response.data.decode())

    # test for the debtor with 3 residence - pass
    @mock.patch('requests.post', return_value=fake_success)
    def test_residence_3(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.residence_3_pass, headers=headers)
        assert response.status_code == 202
        assert ('complete' in response.data.decode())

    # test for the debtor with 3 residence but 1 missing a postcode - fail
    @mock.patch('requests.post', return_value=fake_success)
    def test_residence_3_fail(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.residence_3_fail, headers=headers)
        assert response.status_code == 400

    # test for no key number being passed - fail
    @mock.patch('requests.post', return_value=fake_success)
    def test_no_key_no(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.no_key_no, headers=headers)
        assert response.status_code == 400

    # test for no reference being passed - fail
    @mock.patch('requests.post', return_value=fake_success)
    def test_no_ref(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.no_ref, headers=headers)
        assert response.status_code == 400

    # test for no date being passed - fail
    @mock.patch('requests.post', return_value=fake_success)
    def test_no_date(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.no_date, headers=headers)
        assert response.status_code == 400

    # test for no debtor name being passed - fail
    @mock.patch('requests.post', return_value=fake_success)
    def test_no_debtor(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.no_debtor_name, headers=headers)
        assert response.status_code == 400

    # test for debtor forename being passed - fail
    @mock.patch('requests.post', return_value=fake_success)
    def test_forename(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.no_forename, headers=headers)
        assert response.status_code == 400

    # test for no surname being passed - fail
    @mock.patch('requests.post', return_value=fake_success)
    def test_no_surname(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.no_surname, headers=headers)
        assert response.status_code == 400

    # test for no withheld flag being passed - fail
    @mock.patch('requests.post', return_value=fake_success)
    def test_withheld_flag(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.no_withheld_flag, headers=headers)
        assert response.status_code == 400

    # test for the debtor with 2 forenames and an alternative name - pass
    @mock.patch('requests.post', return_value=fake_success)
    def test_forename_2_altname(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.forename_2_alt_name, headers=headers)
        assert response.status_code == 202
        assert ('complete' in response.data.decode())

    # test for the debtor with 4 forenames - pass
    @mock.patch('requests.post', return_value=fake_success)
    def test_forename4(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.forename_4, headers=headers)
        assert response.status_code == 202
        assert ('complete' in response.data.decode())

    # test for occupation supplied - pass
    @mock.patch('requests.post', return_value=fake_success)
    def test_no_occupation(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.no_occupation, headers=headers)
        assert response.status_code == 202
        assert ('complete' in response.data.decode())

    # test for no trading name being supplied - pass
    @mock.patch('requests.post', return_value=fake_success)
    def test_no_trade_name(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.no_trading_name, headers=headers)
        assert response.status_code == 202
        assert ('complete' in response.data.decode())

    # test for all fields being supplied - pass
    @mock.patch('requests.post', return_value=fake_success)
    def test_all_fields(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.all_fields, headers=headers)
        assert response.status_code == 202
        assert ('complete' in response.data.decode())

    # test for incorrect data type in schema
    @mock.patch('requests.post', return_value=fake_success)
    def test_schema_fail(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        reg_error = '{"keynumber": 222222,"ref": "myref","date": "16/06/2015","forename": "John","surname": "Watson"}'
        response = self.app.post('/register', data=reg_error, headers=headers)
        assert response.status_code == 400

    # test that call to b2b processor failed
    @mock.patch('requests.post', return_value=fake_failure)
    def test_register_fail(self, mock_post):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/register', data=test_data.residence_1, headers=headers)
        assert response.status_code != 202

    # test for incorrect header type
    @mock.patch('requests.post', return_value=fake_success)
    def test_content_fail(self, mock_post):
        headers = {'Content-Type': 'text'}
        response = self.app.post('/register', data=test_data.residence_1, headers=headers)
        assert response.status_code == 415

    @mock.patch('requests.get', return_value=fake_healthcheck)
    def test_healthcheck(self, mock_get):
        response = self.app.get('/health')
        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert data['dependencies']['an-app'] == '200 OK'
