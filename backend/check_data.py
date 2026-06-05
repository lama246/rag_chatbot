import json

with open(
    "data/scraped_content.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)

print("Total pages:", len(data))