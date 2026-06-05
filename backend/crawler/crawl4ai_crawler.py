import asyncio
import trafilatura

from crawl4ai import AsyncWebCrawler


async def scrape_page(url):

    async with AsyncWebCrawler() as crawler:

        result = await crawler.arun(url=url)

        clean_text = trafilatura.extract(
            result.html
        )

        return {
            "url": url,
            "content": clean_text
        }


url = input("URL: ")

data = asyncio.run(
    scrape_page(url)
)

print(data["content"][:5000])