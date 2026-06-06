import os

from utils.cache import (
    get_db_path
)


def index_exists(url):

    db_path = get_db_path(url)

    return os.path.exists(db_path)