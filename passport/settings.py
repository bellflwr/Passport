import pathlib

import tomllib

from .logger import logger


def load_settings():
    with open("./cfsettings.toml", "rb") as f:
        return tomllib.load(f)


def make_settings():
    with open("./cfsettings.toml", "w") as f:
        f.write(
            """day = 1
days = 4

max_points = [10, 8, 5, 9]
bonus_points = 5

minimum_tickets = 0
tickets_per_raffle = 10

secret_key = \"\"
data_folder = \"./data/\""""
        )


settings_file = pathlib.Path("./cfsettings.toml")

if not settings_file.exists():
    make_settings()

settings = load_settings()

if "secret_key" not in settings:
    logger.critical("Secret key does not exist.")
    exit()
if not isinstance(settings["secret_key"], str):
    logger.critical("Secret key must be a string.")
    exit()
if not settings["secret_key"]:
    logger.critical("Secret key must not be an empty string.")
    exit()

SECRET_KEY = settings["secret_key"]
DAY = settings["day"]
DAYS = settings["days"]
MAX_POINTS = settings["max_points"]
MIN_TICKETS = settings["minimum_tickets"]
TICKETS_PER_RAFFLE = settings["tickets_per_raffle"]
BONUS_POINTS = settings["bonus_points"]
DATA_FOLDER = pathlib.Path(settings["data_folder"])
