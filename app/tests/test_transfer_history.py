from datetime import date
import unittest
from unittest.mock import patch, Mock, MagicMock

from app.SMTPConnection import SMTPConnection

from ..BusinessAccount import BusinessAccount
from ..Account import Account


class TestTransferHistory(unittest.TestCase):
    name = "Johny"
    surname = "Krasinski"
    pesel = "01212567891"
    company_name = "Januszex sp. z o.o."
    nip = "8461627563"

    def _mock_response(self, status):
        return Mock(status_code=status)

    def test_history_new_normal_account(self):
        account = Account(self.name, self.surname, self.pesel)
        self.assertListEqual(
            account.transfer_history,
            [],
            "Historia transakcji dla nowego konta prywatnego nie jest pusta!",
        )

    def test_history_incoming_transfer_normal_account(self):
        account = Account(self.name, self.surname, self.pesel)
        account.incoming_transfer(100)
        self.assertListEqual(
            account.transfer_history,
            [100],
            "Przelew przychodzacy nie zostal wpisany do historii!",
        )

    def test_history_outgoing_transfer_normal_account(self):
        account = Account(self.name, self.surname, self.pesel)
        account.balance = 100
        account.outgoing_transfer(50)
        self.assertListEqual(
            account.transfer_history,
            [-50],
            "Przelew wychodzacy nie zostal wpisany do historii!",
        )

    def test_history_express_transfer_normal_account(self):
        account = Account(self.name, self.surname, self.pesel)
        account.balance = 100
        account.express_transfer(50)
        self.assertListEqual(
            account.transfer_history,
            [-50, -1],
            "Przelew ekspresowy nie zostal wpisany do historii!",
        )

    def test_history_multiple_transfers_normal_account(self):
        account = Account(self.name, self.surname, self.pesel)
        account.incoming_transfer(1000)
        account.express_transfer(200)
        account.outgoing_transfer(100)
        self.assertListEqual(
            account.transfer_history,
            [1000, -200, -1, -100],
            "Historia przelewow nie jest poprawna!",
        )

    # Business account

    @patch('requests.get')
    def test_history_new_business_account(self, mock_get):
        mock_response = self._mock_response(200)
        mock_get.return_value = mock_response
        account = BusinessAccount(self.company_name, self.nip)
        self.assertListEqual(
            account.transfer_history,
            [],
            "Historia transakcji dla nowego konta biznesowego nie jest pusta!",
        )

    @patch('requests.get')
    def test_history_incoming_transfer_business_account(self, mock_get):
        mock_response = self._mock_response(200)
        mock_get.return_value = mock_response
        account = BusinessAccount(self.company_name, self.nip)
        account.incoming_transfer(100)
        self.assertListEqual(
            account.transfer_history,
            [100],
            "Przelew przychodzacy nie zostal wpisany do historii!",
        )

    @patch('requests.get')
    def test_history_outgoing_transfer_business_account(self, mock_get):
        mock_response = self._mock_response(200)
        mock_get.return_value = mock_response
        account = BusinessAccount(self.company_name, self.nip)
        account.balance = 100
        account.outgoing_transfer(50)
        self.assertListEqual(
            account.transfer_history,
            [-50],
            "Przelew wychodzacy nie zostal wpisany do historii!",
        )

    @patch('requests.get')
    def test_history_express_transfer_business_account(self, mock_get):
        mock_response = self._mock_response(200)
        mock_get.return_value = mock_response
        account = BusinessAccount(self.company_name, self.nip)
        account.balance = 100
        account.express_transfer(50)
        self.assertListEqual(
            account.transfer_history,
            [-50, -5],
            "Przelew ekspresowy nie zostal wpisany do historii!",
        )

    @patch('requests.get')
    def test_history_multiple_transfers_business_account(self, mock_get):
        mock_response = self._mock_response(200)
        mock_get.return_value = mock_response
        account = BusinessAccount(self.company_name, self.nip)
        account.incoming_transfer(1000)
        account.express_transfer(200)
        account.outgoing_transfer(100)
        self.assertListEqual(
            account.transfer_history,
            [1000, -200, -5, -100],
            "Historia przelewow nie jest poprawna!",
        )

    # Sending mail history

    def test_send_mail_history_normal_account(self):
        title = f"Wyciąg z dnia {date.today()}"
        content = "Twoja historia konta to: [-100]"
        mail = "pawel@gmail.com"
        account = Account(self.name, self.surname, self.pesel)
        account.balance = 1000
        account.outgoing_transfer(100)
        smtp_connector = SMTPConnection()
        smtp_connector.send_mail = MagicMock(return_value=True)
        status = account.send_mail_history("pawel@gmail.com", smtp_connector)
        self.assertTrue(
            status, "Wysylanie historii przelewow nie powiodlo sie!")
        smtp_connector.send_mail.assert_called_once_with(title, content, mail)

    def test_send_mail_history_normal_account_failed(self):
        title = f"Wyciąg z dnia {date.today()}"
        content = "Twoja historia konta to: [-100]"
        mail = "pawel@gmail.com"
        account = Account(self.name, self.surname, self.pesel)
        account.balance = 1000
        account.outgoing_transfer(100)
        smtp_connector = SMTPConnection()
        smtp_connector.send_mail = MagicMock(return_value=False)
        status = account.send_mail_history(mail, smtp_connector)
        self.assertFalse(status, "Wysylanie historii przelewow powiodlo sie!")
        smtp_connector.send_mail.assert_called_once_with(title, content, mail)

    @patch('requests.get')
    def test_send_mail_history_business_account(self, mock_get):
        title = f"Wyciąg z dnia {date.today()}"
        content = "Historia konta Twojej firmy to: [-100]"
        mail = "pawel@gmail.com"
        mock_response = self._mock_response(200)
        mock_get.return_value = mock_response
        account = BusinessAccount(self.company_name, self.nip)
        account.balance = 1000
        account.outgoing_transfer(100)
        smtp_connector = SMTPConnection()
        smtp_connector.send_mail = MagicMock(return_value=True)
        status = account.send_mail_history("pawel@gmail.com", smtp_connector)
        self.assertTrue(
            status, "Wysylanie historii przelewow nie powiodlo sie!")
        smtp_connector.send_mail.assert_called_once_with(title, content, mail)

    @patch('requests.get')
    def test_send_mail_history_business_account_failed(self, mock_get):
        title = f"Wyciąg z dnia {date.today()}"
        content = "Historia konta Twojej firmy to: [-100]"
        mail = "pawel@gmail.com"
        mock_response = self._mock_response(200)
        mock_get.return_value = mock_response
        account = BusinessAccount(self.company_name, self.nip)
        account.balance = 1000
        account.outgoing_transfer(100)
        smtp_connector = SMTPConnection()
        smtp_connector.send_mail = MagicMock(return_value=False)
        status = account.send_mail_history("pawel@gmail.com", smtp_connector)
        self.assertFalse(status, "Wysylanie historii przelewow powiodlo sie!")
        smtp_connector.send_mail.assert_called_once_with(title, content, mail)
