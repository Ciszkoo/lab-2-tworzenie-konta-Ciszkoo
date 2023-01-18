import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized

from ..BusinessAccount import BusinessAccount


class TestCreateBusinessAccount(unittest.TestCase):
    company_name = "Januszex sp. z o.o."
    correct_nip = "8461627563"
    wrong_nip_info = "Niepoprawny NIP!"

    def _mock_response(self, status):
        return Mock(status_code=status)

    @patch('requests.get')
    def test_create_business_account(self, mock_get):
        mock_response = self._mock_response(200)
        mock_get.return_value = mock_response
        account = BusinessAccount(self.company_name, self.correct_nip)

        self.assertEqual(
            account.company_name,
            self.company_name,
            "nazwa firmy nie zostala ustawiona!",
        )
        self.assertEqual(
            account.nip, self.correct_nip, "Nip firmy nie zostal ustawiony"
        )
        self.assertEqual(account.balance, 0, "Saldo konta nie wynosi zero!")

    @patch('requests.get')
    def test_create_business_account_nip_does_not_exist(self, mock_get):
        mock_response = self._mock_response(400)
        mock_get.return_value = mock_response
        account = BusinessAccount(self.company_name, self.correct_nip)

        self.assertEqual(account.nip, "Pranie!")

    @parameterized.expand([
        ("11234567891", "Komunikat o niepoprawnym nipie nie zostal nadany!"),
        ("112345678", "Komunikat o niepoprawnym nipie nie zostal nadany!")
    ])
    def test_create_business_account_nip_incorrect_length(self, incorrect_length_nip, message):
        account = BusinessAccount(self.company_name, incorrect_length_nip)

        self.assertEqual(
            account.nip,
            self.wrong_nip_info,
            message,
        )
