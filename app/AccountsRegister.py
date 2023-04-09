from app.Account import Account


class AccountsRegister():
    accounts = []

    @classmethod
    def add_account(cls, account: Account) -> None:
        cls.accounts.append(account)

    @classmethod
    def number_of_accounts(cls) -> int:
        return len(cls.accounts)

    @classmethod
    def find_account(cls, pesel: str) -> Account | None:
        for account in cls.accounts:
            if account.pesel == pesel:
                return account
        return None
