#!/usr/bin/env python3
"""
Sitemap Mapping Script
Fetches and parses sitemaps, classifies URLs by content type, and updates content map.
"""

import sys
import json
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, urljoin
from pathlib import Path


def fetch_sitemap(url: str) -> str:
    """Fetch sitemap XML from URL."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching sitemap: {e}", file=sys.stderr)
        sys.exit(1)


def parse_sitemap_xml(xml_content: str) -> List[Dict]:
    """Parse sitemap XML and extract URLs with metadata."""
    urls = []

    try:
        root = ET.fromstring(xml_content)

        # Handle namespace (sitemaps use xmlns)
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Check if this is a sitemap index
        sitemap_elements = root.findall('ns:sitemap', ns)
        if sitemap_elements:
            # This is a sitemap index - return sitemap URLs
            for sitemap in sitemap_elements:
                loc = sitemap.find('ns:loc', ns)
                if loc is not None and loc.text:
                    urls.append({
                        'url': loc.text.strip(),
                        'is_sitemap': True
                    })
        else:
            # This is a regular sitemap - extract URLs
            url_elements = root.findall('ns:url', ns)
            for url_elem in url_elements:
                loc = url_elem.find('ns:loc', ns)
                lastmod = url_elem.find('ns:lastmod', ns)

                if loc is not None and loc.text:
                    url_data = {
                        'url': loc.text.strip(),
                        'is_sitemap': False
                    }

                    if lastmod is not None and lastmod.text:
                        url_data['lastmod'] = lastmod.text.strip()

                    urls.append(url_data)

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}", file=sys.stderr)
        sys.exit(1)

    return urls


def extract_date_from_url(url: str) -> Optional[str]:
    """Extract date from URL patterns like /2024/01/15/ or /blog/2024-01-15-title."""
    # Pattern: YYYY/MM/DD
    match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', url)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

    # Pattern: YYYY-MM-DD
    match = re.search(r'/(\d{4}-\d{2}-\d{2})', url)
    if match:
        return match.group(1)

    # Pattern: YYYY/MM
    match = re.search(r'/(\d{4})/(\d{2})/', url)
    if match:
        return f"{match.group(1)}-{match.group(2)}-01"

    return None


def classify_url(url: str) -> str:
    """
    Classify URL into content type based on path patterns.

    Content types match kurt-core ContentType enum:
    - reference: API docs, technical references
    - tutorial: Step-by-step tutorials, quickstarts
    - guide: Documentation, how-to guides
    - blog: Blog posts, articles, news
    - product_page: Product/feature pages
    - solution_page: Solutions, use cases
    - homepage: Site homepage
    - case_study: Customer stories, case studies
    - event: Events, webinars
    - info: About, support, FAQ, changelog
    - landing_page: Marketing landing pages, pricing
    - other: Everything else
    """
    path = urlparse(url).path.lower()

    # Homepage (check first, most specific)
    if path in ['', '/']:
        return 'homepage'

    # API Reference (before general docs)
    if any(pattern in path for pattern in ['/api/', '/api-reference/', '/api-docs/']):
        return 'reference'

    # Tutorial/Quickstart (before general guide)
    if any(pattern in path for pattern in ['/tutorial', '/quickstart', '/getting-started']):
        return 'tutorial'

    # Guide/Documentation (use specific patterns to avoid false matches)
    if any(pattern in path for pattern in ['/docs/', '/documentation/', '/guide/']):
        return 'guide'

    # Blog
    if any(pattern in path for pattern in ['/blog/', '/article/', '/post/', '/news/']):
        return 'blog'

    # Case Study
    if any(pattern in path for pattern in ['/case-study', '/case-studies', '/customer-stories', '/customers/']):
        return 'case_study'

    # Event
    if any(pattern in path for pattern in ['/event', '/webinar', '/conference']):
        return 'event'

    # Solution Page (before product page)
    if any(pattern in path for pattern in ['/solutions/', '/use-case']):
        return 'solution_page'

    # Product Page
    if any(pattern in path for pattern in ['/product/', '/features/']):
        return 'product_page'

    # Landing Page (pricing, contact, etc.)
    if any(pattern in path for pattern in ['/pricing', '/contact', '/demo', '/signup', '/get-started']):
        return 'landing_page'

    # Info (about, support, changelog, etc.)
    if any(pattern in path for pattern in ['/about', '/company', '/team', '/support/', '/help/', '/faq', '/changelog', '/release', '/updates/']):
        return 'info'

    # Default
    return 'other'


def get_content_map_path(domain: str) -> str:
    """Get path to content map for domain."""
    return f"sources/{domain}/_content-map.json"


def load_content_map(map_path: str) -> Dict:
    """Load existing content map or create new structure."""
    if Path(map_path).exists():
        with open(map_path, 'r') as f:
            return json.load(f)

    # Extract domain from path
    domain = map_path.split('/')[1]

    return {
        "domain": domain,
        "last_updated": datetime.now().isoformat(),
        "sitemap": {},
        "clusters": [],
        "topics": {}
    }


def update_content_map_with_urls(content_map: Dict, urls: List[Dict]) -> Tuple[int, int]:
    """
    Update content map with discovered URLs.
    Returns: (new_count, existing_count)
    """
    new_count = 0
    existing_count = 0

    for url_data in urls:
        url = url_data['url']

        # Skip if already FETCHED (don't overwrite)
        if url in content_map['sitemap']:
            existing_entry = content_map['sitemap'][url]
            if existing_entry.get('status') == 'FETCHED':
                existing_count += 1
                continue

        # Add or update with DISCOVERED status
        content_type = classify_url(url)
        published_date = url_data.get('lastmod') or extract_date_from_url(url)

        content_map['sitemap'][url] = {
            'status': 'DISCOVERED',
            'file_path': None,
            'title': None,
            'author': None,
            'published_date': published_date,
            'content_type': content_type,
            'source': 'sitemap',
            'discovered_at': datetime.now().isoformat()
        }

        new_count += 1

    content_map['last_updated'] = datetime.now().isoformat()

    return new_count, existing_count


def save_content_map(map_path: str, content_map: Dict):
    """Save content map to file."""
    # Ensure directory exists
    Path(map_path).parent.mkdir(parents=True, exist_ok=True)

    with open(map_path, 'w') as f:
        json.dump(content_map, f, indent=2)


def discover_sitemap_url(domain_or_url: str) -> str:
    """Discover sitemap URL from domain or URL."""
    parsed = urlparse(domain_or_url)

    # If no scheme, add https://
    if not parsed.scheme:
        domain_or_url = f"https://{domain_or_url}"
        parsed = urlparse(domain_or_url)

    base_url = f"{parsed.scheme}://{parsed.netloc}"

    # Common sitemap locations to try
    sitemap_paths = [
        '/sitemap.xml',
        '/sitemap_index.xml',
        '/sitemap-index.xml',
        '/sitemaps/sitemap.xml'
    ]

    for path in sitemap_paths:
        sitemap_url = urljoin(base_url, path)
        try:
            response = requests.head(sitemap_url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                return sitemap_url
        except requests.RequestException:
            continue

    # Default to /sitemap.xml
    return urljoin(base_url, '/sitemap.xml')


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python map_sitemap.py <domain_or_sitemap_url> [--recursive]", file=sys.stderr)
        sys.exit(1)

    input_url = sys.argv[1]
    recursive = '--recursive' in sys.argv

    # Discover sitemap URL
    if 'sitemap' in input_url.lower():
        sitemap_url = input_url
    else:
        sitemap_url = discover_sitemap_url(input_url)
        print(f"Discovered sitemap: {sitemap_url}", file=sys.stderr)

    # Extract domain for content map
    parsed = urlparse(sitemap_url)
    domain = parsed.netloc

    # Fetch and parse sitemap
    print(f"Fetching sitemap from {sitemap_url}...", file=sys.stderr)
    xml_content = fetch_sitemap(sitemap_url)
    urls = parse_sitemap_xml(xml_content)

    # Handle sitemap indexes (recursive)
    if urls and urls[0].get('is_sitemap') and recursive:
        print(f"Found sitemap index with {len(urls)} sitemaps", file=sys.stderr)
        all_urls = []

        for sitemap_entry in urls:
            sitemap_child_url = sitemap_entry['url']
            print(f"  Fetching {sitemap_child_url}...", file=sys.stderr)
            child_xml = fetch_sitemap(sitemap_child_url)
            child_urls = parse_sitemap_xml(child_xml)
            all_urls.extend([u for u in child_urls if not u.get('is_sitemap')])

        urls = all_urls

    # Filter out sitemap entries (keep only actual URLs)
    urls = [u for u in urls if not u.get('is_sitemap')]

    print(f"Found {len(urls)} URLs", file=sys.stderr)

    # Load content map
    map_path = get_content_map_path(domain)
    content_map = load_content_map(map_path)

    # Update content map
    new_count, existing_count = update_content_map_with_urls(content_map, urls)

    # Save content map
    save_content_map(map_path, content_map)

    # Output summary as JSON
    result = {
        'domain': domain,
        'sitemap_url': sitemap_url,
        'total_urls': len(urls),
        'new_urls': new_count,
        'existing_urls': existing_count,
        'content_map_path': map_path,
        'content_types': {}
    }

    # Count by content type
    for url_entry in content_map['sitemap'].values():
        content_type = url_entry.get('content_type', 'unknown')
        result['content_types'][content_type] = result['content_types'].get(content_type, 0) + 1

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
