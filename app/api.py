from flask import Flask, request, jsonify
from app.AccountsRegister import AccountsRegister
from app.Account import Account

app = Flask(__name__)


@app.route("/account/create_account", methods=["POST"])
def create_account():
    data = request.get_json()
    isUsed = AccountsRegister.find_account(data["pesel"])
    if isUsed is not None:
        return jsonify("Account with provided pesel already exists!"), 400
    print(f"Received data - creating account: {data}")
    account = Account(data["name"], data["surname"], data["pesel"])
    AccountsRegister.add_account(account)
    return jsonify("Account created!"), 201


@app.route("/account/number_of_accounts", methods=["GET"])
def number_of_accounts():
    return jsonify(AccountsRegister.number_of_accounts()), 200


@app.route("/account/find_account/<pesel>", methods=["GET"])
def find_account(pesel: str):
    account = AccountsRegister.find_account(pesel)
    if account:
        return jsonify(account.__dict__), 200
    return jsonify("Account not found!"), 404

@app.route("/account/update_account/<pesel>", methods=["PUT"])
def update_account(pesel: str):
    data = request.get_json()
    account = AccountsRegister.find_account(pesel)
    if account:
        if "name" in data:
            account.name = data["name"]
        if "surname" in data:
            account.surname = data["surname"]
        if "balance" in data:
            account.balance = data["balance"]
        return jsonify("Account updated!"), 200
    return jsonify("Account not found!"), 404
    
@app.route("/account/delete_account/<pesel>", methods=["DELETE"])
def delete_account(pesel: str):
    account = AccountsRegister.find_account(pesel)
    if account:
        AccountsRegister.accounts.remove(account)
        return jsonify("Account deleted!"), 200
    return jsonify("Account not found!"), 404
