from . import data

DAYS = 4


def load_accounts() -> dict[str, dict]:
    return data.load_file("accounts")


def write_accounts(accounts: dict) -> None:
    data.post_file(accounts, "accounts")


def load_account(name: str) -> dict | None:
    accounts = load_accounts()
    return accounts.get(name, None)


def write_account(name: str, val: dict) -> None:
    accounts = load_accounts()
    accounts[name] = val
    write_accounts


def create_account(name: str) -> None:
    accounts = load_accounts()

    account = {}

    account["days"] = []

    for _ in range(1, DAYS + 1):
        account["days"].append({"points": 0})

    accounts[name] = account

    write_accounts()
