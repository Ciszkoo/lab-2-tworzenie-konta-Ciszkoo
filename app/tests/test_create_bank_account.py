import unittest
from parameterized import parameterized
from ..Account import Account


class TestCreateBankAccount(unittest.TestCase):
    name = "Dariusz"
    surname = "Januszewski"
    pesel = "12325678912"  # 12.2012r.
    wrong_pesel_info = "Niepoprawny PESEL!"

    def test_create_account(self):
        first_account = Account(self.name, self.surname, self.pesel)

        self.assertEqual(first_account.name, self.name,
                         "Imie nie zostało zapisane!")
        self.assertEqual(
            first_account.surname, self.surname, "Nazwisko nie zostało zapisane!"
        )
        self.assertEqual(first_account.balance, 0, "Saldo nie jest zerowe!")

        # tutaj proszę dodawać nowe testy

        self.assertEqual(first_account.pesel, self.pesel,
                         "PESEL nie zostal zapisany!")

    @parameterized.expand([
        ("123", "PESEL jest zbyt krótki!"),
        ("123456789123456789", "PESEL jest zbyt długi!"),
    ])
    def test_pesel_incorrect_length(self, pesel, message):
        account = Account(self.name, self.surname, pesel)
        self.assertEqual(
            account.pesel, self.wrong_pesel_info, message
        )

    @parameterized.expand([
        ("12325678912", "PROM-XYZ", 50, "Bonusowe srodki nie zostaly dodane!"),
        ("12325678912", "DARMOWE_5_DYSZEK", 0,
         "Bonusowe srodki zostaly dodane mimo zlego kodu!"),
        ("99811234567", "PROM-XYZ", 0, "Bonusowe srodki zostaly przyznane seniorowi!"),
        ("60011234567", "PROM-XYZ", 0, "Bonusowe srodki zostaly przyznane seniorowi!"),
    ])
    def test_account_promo_code(self, pesel, promo_code, expected_balance, message):
        bonus_srodki = 50
        account = Account(self.name, self.surname,
                          pesel, promo_code)

        self.assertEqual(
            account.balance, expected_balance, message
        )
