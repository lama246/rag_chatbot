from urllib.parse import urlparse
import os

def get_domain(url):

    domain = (
        urlparse(url)
        .netloc
        .replace("www.", "")
        .replace(".", "_")
    )

    return domain


def get_db_path(url):

    domain = get_domain(url)

    return f"indexes/{domain}"


def get_metadata_path(url):

    domain = get_domain(url)

    return f"metadata/{domain}.json"