import asyncio

from crawler.crawl4ai_recursive import (
    Crawl4AICrawler
)
if __name__ == "__main__":

    url = input(
        "Enter Website URL: "
    )

    crawler = Crawl4AICrawler(

        start_url=url,

        max_pages=30
    )

    asyncio.run(

        crawler.save_json(

            "data/scraped_content.json"
        )
    )
