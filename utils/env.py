import logging
import os

from dotenv import load_dotenv

log = logging.getLogger(__name__)


def load_env():
    from features.environment import PROJECT_ROOT

    env_path = PROJECT_ROOT / ".env"
    load_dotenv(dotenv_path=env_path)
    log.debug("Environment loaded")


def get_from_env(name: str, required: bool = True):
    value = os.getenv(name)
    if required and not value:
        raise RuntimeError(f"No {name} environment variable found.")
    return value


def get_window_size():
    window_size = get_from_env("WINDOW_SIZE").split("x")
    if not len(window_size) == 2:
        raise RuntimeError("Invalid window size")
    return window_size


def is_truthy(bool_as_string: str):
    return bool_as_string.lower() == "true"
