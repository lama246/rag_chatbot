import hashlib
from urllib.parse import urlparse


def get_domain(url):

    parsed = urlparse(url)

    domain = (
        parsed.netloc
        .replace("www.", "")
        .replace(".", "_")
    )

    url_hash = hashlib.md5(
        url.encode()
    ).hexdigest()[:8]

    return f"{domain}_{url_hash}"


def get_db_path(url):

    domain = get_domain(url)

    return f"indexes/{domain}"


def get_metadata_path(url):

    domain = get_domain(url)

    return f"metadata/{domain}.json"