import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


class WebsiteCrawler:

    def __init__(self, start_url, max_pages=200):
        self.start_url = start_url
        self.max_pages = max_pages

        self.visited = set()
        self.scraped_data = []

    def get_text_content(self, url):

        try:

            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent":
                    "Mozilla/5.0"
                }
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            for tag in soup(
                [
                    "script",
                    "style",
                    "nav",
                    "footer",
                    "header",
                    "aside"
                ]
            ):
                tag.decompose()

            title = ""

            if soup.title:
                title = soup.title.get_text(
                    strip=True
                )

            text = soup.get_text(
                separator=" ",
                strip=True
            )

            return {
                "title": title,
                "content": text
            }

        except Exception as e:

            print("Error:", url, e)

            return {
                "title": "",
                "content": ""
            }

    def get_links(self, url):

        links = set()

        try:
            response = requests.get(url)

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            base_domain = urlparse(
                self.start_url
            ).netloc

            for a in soup.find_all(
                "a",
                href=True
            ):

                full_url = urljoin(
                    url,
                    a["href"]
                )

                parsed = urlparse(
                    full_url
                )

                if parsed.netloc == base_domain:
                    links.add(full_url)

        except:
            pass

        return links

    def crawl(self):

        queue = deque([self.start_url])

        while queue and len(self.visited) < self.max_pages:

            current_url = queue.popleft()

            if current_url in self.visited:
                continue

            print("Scraping:", current_url)

            self.visited.add(current_url)

            page_data = self.get_text_content(
    current_url
)

            if len(page_data["content"]) > 500:

                self.scraped_data.append({

                    "url": current_url,

                    "title":
                    page_data["title"],

                    "content":
                    page_data["content"]

                })

            links = self.get_links(
                current_url
            )

            for link in links:

                if link not in self.visited:
                    queue.append(link)

        return self.scraped_data