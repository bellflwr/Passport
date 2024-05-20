import math

from flask import Blueprint, render_template

from .accounts import load_accounts
from .settings import (
    BONUS_POINTS,
    DAY,
    DAYS,
    MAX_POINTS,
    MIN_TICKETS,
    TICKETS_PER_RAFFLE,
)

bp = Blueprint("home", __name__, url_prefix="/")


@bp.route("/")
def home():
    return render_template("home.html", day=DAY)


def total_points(account: dict):
    total: int = 0

    for k, v in account.items():
        total += v

        if int(k) < DAYS and MAX_POINTS[int(k - 1)]:
            total += BONUS_POINTS

    return total


@bp.route("/raffle")
def raffle():
    accounts = load_accounts()
    updated_data = {}

    for name, account in accounts.items():

        if total_points(account) >= MIN_TICKETS:
            raffle_tickets = (
                math.floor((total_points(account) - MIN_TICKETS) / TICKETS_PER_RAFFLE)
                + 1
            )
            updated_data[name] = raffle_tickets

    return render_template("raffle.html", accounts=updated_data)
