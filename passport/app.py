from flask import Flask, render_template, request, redirect, url_for
from . import data
from . import accounts as accountutil
import pathlib
import math

app = Flask(__name__)

data_folder = pathlib.Path("./data/")

data_folder.mkdir(exist_ok=True, parents=True)

if not (data_folder / "accounts.json").exists():
    data.post_file({}, "accounts")

if not (data_folder / "deleted.json").exists():
    data.post_file({}, "deleted")

if not (data_folder / "settings.toml").exists():
    data.make_settings()

settings = data.load_settings()

DAYS = 4
BONUS_POINTS = 5


@app.route("/")
def home():
    day = settings["day"]
    return render_template("home.html", day=day)


@app.route("/accounts", methods=["GET", "POST"])
def accounts():
    accounts = data.load_file("accounts")

    if request.method == "POST":
        name = request.form["name"]

        if name not in accounts:
            accountutil.create_account(name)

    accounts = data.load_file("accounts")

    return render_template("accounts.html", accounts=data.order(accounts))


@app.route("/delete/<name>", methods=["POST"])
def delete_account(name):
    accounts = data.load_file("accounts")

    if request.method == "POST":
        deleted = data.load_file("deleted")

        deleted[name] = accounts[name]
        del accounts[name]

        data.post_file(deleted, "deleted")
        data.post_file(accounts, "accounts")

    return redirect(url_for("accounts"))


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        worth = int(request.form["worth"])

        account = accountutil.load_account(name)

        day = settings["day"] - 1
        day_data = account["days"][day]

        day_data["points"] += worth
        if day_data["points"] > settings["max_points"][day]:
            day_data["points"] = settings["max_points"][day]

        account["days"][day] = day_data

        accountutil.write_account(name, account)
        data.post_file(accounts, "accounts")

    return render_template("add.html")


def total_points(account: dict):
    total: int = 0

    for i, day in enumerate(account["days"]):
        total += day["points"]

        if i + 1 < DAYS and settings["max_points"][i]:
            total += BONUS_POINTS

    return total


@app.route("/raffle")
def raffle():
    accounts = data.load_file("accounts")
    updated_data = {}

    min_tickets = settings["minimumTickets"]
    tickets_per_raffle = settings["ticketsPerRaffle"]

    for name in accounts.keys():
        print(total_points(accounts, name))
        print(accounts[name])

        if total_points(accounts, name) >= min_tickets:
            raffle_tickets = (
                math.floor(
                    (total_points(accounts, name) - min_tickets) / tickets_per_raffle
                )
                + 1
            )
            updated_data[name] = raffle_tickets

    return render_template("raffle.html", accounts=updated_data)


if __name__ == "__main__":
    app.run("localhost", 8000, debug=True)
