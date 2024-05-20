from flask import Flask, g

from .accounts import write_accounts
from .logger import logger
from .settings import SECRET_KEY


def create_app() -> Flask:
    logger.info("CF Passport")

    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    @app.teardown_appcontext
    def teardown_accounts(exception):
        accounts = g.pop("_accounts", None)
        dirty = g.pop("_dirty", False)

        if dirty and accounts is not None:
            write_accounts(accounts)

    with app.app_context():
        from . import accounts, home

        app.register_blueprint(home.bp)
        app.register_blueprint(accounts.bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run("localhost", 8000, debug=True)
