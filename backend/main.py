from crawler.crawler import WebsiteCrawler
import json
if __name__ == "__main__":

    url = input("Enter Website URL: ")

    crawler = WebsiteCrawler(
        start_url=url,
        max_pages=30
    )

    data = crawler.crawl()

    with open(
        "data/scraped_content.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("Saved Successfully")
    print("WRITING JSON")