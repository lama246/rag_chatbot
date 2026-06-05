import asyncio
import json
import trafilatura

from crawl4ai import AsyncWebCrawler

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class Crawl4AICrawler:

    def __init__(self, start_url, max_pages=100):

        self.start_url = start_url
        self.max_pages = max_pages

        self.visited = set()
        self.scraped_data = []

        self.base_domain = (
            urlparse(start_url).netloc
        )

    async def extract_links(
        self,
        html,
        current_url
    ):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        links = set()

        for a in soup.find_all(
            "a",
            href=True
        ):

            full_url = urljoin(
                current_url,
                a["href"]
            )

            parsed = urlparse(
                full_url
            )

            if parsed.netloc == self.base_domain:

                links.add(
                    full_url
                )

        return links

    async def crawl(self):

        queue = [self.start_url]

        async with AsyncWebCrawler() as crawler:

            while (
                queue and
                len(self.visited)
                < self.max_pages
            ):

                current_url = (
                    queue.pop(0)
                )

                if (
                    current_url
                    in self.visited
                ):
                    continue

                print(
                    "Scraping:",
                    current_url
                )

                self.visited.add(
                    current_url
                )

                try:

                    result = await (
                        crawler.arun(
                            url=current_url
                        )
                    )

                    html = result.html

                    content = trafilatura.extract(
                        html,
                        include_comments=False,
                        include_tables=True
                    )
                    if content:

                        junk_phrases = [

                            "You are logged in",

                            "Loading...",

                            "Subscribe now",

                            "Account Settings",

                            "Need help with your subscription",

                            "Additional Subscription Benefits"

                        ]

                        for phrase in junk_phrases:

                            content = content.replace(
                                phrase,
                                ""
                            )

                    if (
                            content and
                            len(content)
                            > 2000
                        ):

                        title = ""

                        soup = BeautifulSoup(
                            html,
                            "html.parser"
                        )

                        if soup.title:
                            title = (
                                soup.title
                                .get_text(
                                    strip=True
                                )
                            )

                        self.scraped_data.append(
                            {
                                "url":
                                current_url,

                                "title":
                                title,

                                "content":
                                content
                            }
                        )

                    links = await (
                        self.extract_links(
                            html,
                            current_url
                        )
                    )

                    for link in links:

                        # Only crawl article pages

                        if (
                            "/article" in link
                            and
                            link not in self.visited
                        ):

                            queue.append(link)

                except Exception as e:

                    print(
                        "ERROR:",
                        e
                    )

        return self.scraped_data

    async def save_json(
        self,
        output_file
    ):

        data = await self.crawl()

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Saved {len(data)} pages"
        )