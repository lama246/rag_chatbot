import asyncio
import json
import trafilatura

from crawl4ai import AsyncWebCrawler

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from progress import crawl_progress
class Crawl4AICrawler:

    def __init__(self, start_url, max_pages=30):
        
        self.start_url = start_url
        self.max_pages = max_pages

        self.visited = set()
        self.scraped_data = []

        self.base_domain = (
            urlparse(start_url).netloc
        )
        self.base_path = urlparse(start_url).path

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

            parsed = urlparse(full_url)

            # must be same domain
            if parsed.netloc != self.base_domain:
                continue

            # must stay in same section (IMPORTANT FIX)
            if not parsed.path.startswith(self.base_path):
                continue

            links.add(full_url)

        return links

    async def crawl(self):

        queue = [self.start_url]

        async with AsyncWebCrawler() as crawler:
            
            
            crawl_progress["current"] = 0
            crawl_progress["total"] = self.max_pages
            while (
                queue and
                len(self.visited)
                < self.max_pages
            ):

                current_url = (
                    queue.pop(0)
                )
                crawl_progress["current"] += 1
            
                
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
                crawl_progress["current"] = len(
                        self.visited
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
                    print("\n" + "=" * 50)
                    print("URL:", current_url)
                    if content:
                        print(content[:500])
                        print("\nCONTENT LENGTH:", len(content))
                    else:
                        print("NO CONTENT EXTRACTED")

                    print("=" * 50)
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
                        len(content.strip()) > 100
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

                        if link not in self.visited:

                            queue.append(link)

                except Exception as e:

                    print(
                        "ERROR:",
                        e
                    )
            # Crawl finished
            crawl_progress["current"] = len(self.visited)
            crawl_progress["total"] = max(
                len(self.visited),
                1)
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
async def crawl_site(url):

                crawler = Crawl4AICrawler(
                            start_url=url,
                            max_pages=30
                        )

                return await crawler.crawl()


def crawl_website(url):

                return asyncio.run(
                            crawl_site(url)
                        )
        