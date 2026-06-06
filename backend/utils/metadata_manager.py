import json
import os
from datetime import datetime

from utils.cache import (
    get_metadata_path
)


def save_metadata(url, pages):

    metadata = {
        "url": url,
        "pages": pages,
        "last_indexed":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
    }

    path = get_metadata_path(url)

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )


def load_metadata(url):

    path = get_metadata_path(url)

    if not os.path.exists(path):
        return None

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)