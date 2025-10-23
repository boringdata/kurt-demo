"""
Advanced URL Discovery using Trafilatura Focused Crawler

Use when you need fine-grained control over crawling:
- Filter by URL patterns
- Depth limits
- Language filtering
- Custom crawl parameters

Trafilatura Documentation:
- Crawls: https://trafilatura.readthedocs.io/en/latest/crawls.html
- Focused Crawler API: https://trafilatura.readthedocs.io/en/latest/crawls.html#focused-crawler
- Language-aware crawling: https://trafilatura.readthedocs.io/en/latest/crawls.html#language-aware-crawling
"""

from trafilatura.spider import focused_crawler
from kurt.source import add_document

# 1. Discover URLs with custom parameters
to_visit, known_links = focused_crawler(
    homepage='https://example.com',
    max_seen_urls=200,          # Max URLs to discover
    max_known_urls=10000,       # Max URLs to track
    # language='en',            # Optional: language filter
)

# 2. Save to temporary file
with open('/tmp/discovered_urls.txt', 'w') as f:
    for url in to_visit:
        f.write(f"{url}\n")

print(f"Saved {len(to_visit)} URLs to /tmp/discovered_urls.txt")

# 3. Import into kurt database
with open('/tmp/discovered_urls.txt', 'r') as f:
    for line in f:
        url = line.strip()
        if url:
            doc_id = add_document(url)
            print(f"✓ {url}")
