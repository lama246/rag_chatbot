from crawler.crawler import WebsiteCrawler
import json

url = input("Enter Website URL: ")

crawler = WebsiteCrawler(
    start_url=url,
    max_pages=15
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