import unittest
import requests


class TestAccountUsage(unittest.TestCase):
    body = {
        "name": "Dariusz",
        "surname": "Januszewski",
        "pesel": "12325678912"
    }

    newBody = {
        "name": "Janusz",
        "surname": "Dariusz",
    }

    url = "http://127.0.0.1:5000"

    def test_1_create_account(self):
        response = requests.post(
            self.url + "/account/create_account", json=self.body)
        self.assertEqual(response.status_code, 201)

    def test_2_create_account_with_existing_pesel(self):
        response = requests.post(
            self.url + "/account/create_account", json=self.body)
        self.assertEqual(response.status_code, 400)

    def test_3_find_account(self):
        response = requests.get(self.url + "/account/find_account/12325678912")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], self.body['name'])
        self.assertEqual(response.json()['surname'], self.body['surname'])
        self.assertEqual(response.json()['pesel'], self.body['pesel'])

    def test_4_update_account(self):
        response = requests.put(
            self.url + "/account/update_account/12325678912", json=self.newBody)
        self.assertEqual(response.status_code, 200)

    def test_5_find_account(self):
        response = requests.get(self.url + "/account/find_account/12325678912")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], self.newBody['name'])
        self.assertEqual(response.json()['surname'], self.newBody['surname'])

    def test_6_find_non_existing_account(self):
        response = requests.get(self.url + "/account/find_account/02325768910")
        self.assertEqual(response.status_code, 404)

    def test_7_delete_account(self):
        response = requests.delete(
            self.url + "/account/delete_account/12325678912")
        self.assertEqual(response.status_code, 200)
