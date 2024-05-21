import orjson

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from .logger import logger
from .settings import DATA_FOLDER, DAY, DAYS, MAX_POINTS
from .settings import (
    BONUS_POINTS,
    DAY,
    DAYS,
    MAX_POINTS,
    MIN_TICKETS,
    TICKETS_PER_RAFFLE,
)

bp = Blueprint("accounts", __name__, url_prefix="/accounts")


accounts_file = DATA_FOLDER / "accounts.json"


DATA_FOLDER.mkdir(exist_ok=True, parents=True)

if not accounts_file.exists():
    accounts_file.write_text("{}", "utf-8")


class AccountDoesntExist(Exception):
    pass


class AccountAlreadyExists(Exception):
    pass


def _load_accounts() -> dict[str, dict]:
    with accounts_file.open("rb") as f:
        return orjson.loads(f.read())


def load_accounts() -> dict[str, dict]:
    accounts = getattr(g, "_accounts", None)
    if accounts is None:
        accounts = g._accounts = _load_accounts()
    return accounts


def mark_dirty() -> None:
    g._dirty = True


def write_accounts(accounts: dict) -> None:
    with accounts_file.open("wb") as f:
        f.write(orjson.dumps(accounts))


def load_account(name: str) -> dict | None:
    accounts = load_accounts()
    return accounts.get(name, None)

def total_points(account: dict):
    total: int = 0

    for k, v in account.items():
        total += v

        if int(k) < DAYS and MAX_POINTS[int(k) - 1] == v:
            total += BONUS_POINTS

    return total


def write_account(name: str, val: dict) -> None:
    accounts = load_accounts()
    accounts[name] = val
    mark_dirty()


def create_account(name: str) -> None:
    accounts = load_accounts()

    if name in accounts:
        raise AccountAlreadyExists(f'Account "{name}" already exists in the database')

    account = {}

    for i in range(1, DAYS + 1):
        account[str(i)] = 0

    write_account(name, account)


def delete_account(name: str) -> None:
    accounts = load_accounts()

    if name not in accounts:
        raise AccountDoesntExist(f'Name "{name}" not found in database')

    del accounts[name]
    mark_dirty()


@bp.route("/", methods=["GET", "POST"])
def accounts():
    accounts = load_accounts()

    if request.method == "POST":
        name = request.form["name"]

        try:
            create_account(name)
            flash(f'Account "{name}" created!')
            logger.info('User "%s" was created', name)
        except AccountAlreadyExists:
            flash(f'Account with name "{name}" already exists!', "error")
    updatedAccounts = {}
    for name, account in accounts.items():
        print(name)
        print(account)
        updatedAccounts[name] = total_points(account)

    return render_template("accounts.html", accounts=updatedAccounts)


@bp.route("/delete/<name>", methods=["POST"])
def delete_account_route(name):
    if request.method == "POST":
        try:
            delete_account(name)
            flash(f'Account "{name}" deleted!')
            logger.info('User "%s" was deleted', name)
        except AccountDoesntExist:
            flash(f'Account with name "{name}" doesn\'t exist!', "error")

    return redirect(url_for("accounts.accounts"))


@bp.route("/add", methods=["GET", "POST"])
def add():
    names = list(load_accounts().keys())
    
    if request.method == "POST":
        name = request.form["name"]
        worth = int(request.form["worth"])

        account = load_account(name)
        if account is None:
            flash(f'Account with name "{name}" doesn\'t exist!', "error")
            return render_template("add.html", names=names)
        day = str(DAY)
        max_points = MAX_POINTS[int(day) - 1]

        account[day] += worth
        if account[day] > max_points:
            account[day] = max_points

        write_account(name, account)

        logger.info('Added %s points to account "%s"', worth, name)

    return render_template("add.html", names=names)
