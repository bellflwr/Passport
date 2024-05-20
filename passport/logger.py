import logging

g_logger = logging.getLogger("gunicorn.error")

logger = logging.getLogger()
logger.setLevel("DEBUG")

formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
)

logger.handlers.extend(g_logger.handlers)
