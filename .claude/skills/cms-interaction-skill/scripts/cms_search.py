#!/usr/bin/env python3
"""
Search CMS content.

Usage:
    python cms_search.py --cms sanity --query "tutorial"
    python cms_search.py --cms sanity --content-type article --limit 20
    python cms_search.py --cms sanity --output json > results.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

# Add adapters to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'adapters'))

from base import CMSAdapter


def load_config(cms_name: str) -> dict:
    """Load CMS configuration from cms-config.json."""
    config_path = Path.home() / 'code' / 'kurt-demo' / '.claude' / 'scripts' / 'cms-config.json'

    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}", file=sys.stderr)
        print("\nCreate configuration file:", file=sys.stderr)
        print(f"  cp .claude/skills/cms-interaction-skill/adapters/{cms_name}/config.json.example \\", file=sys.stderr)
        print(f"     .claude/scripts/cms-config.json", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    if cms_name not in config:
        print(f"Error: No configuration found for CMS '{cms_name}'", file=sys.stderr)
        print(f"\nAvailable CMSs in config: {', '.join(config.keys())}", file=sys.stderr)
        sys.exit(1)

    return config[cms_name]


def get_adapter(cms_name: str, config: dict) -> CMSAdapter:
    """Load and initialize CMS adapter."""
    if cms_name == 'sanity':
        from sanity.adapter import SanityAdapter
        return SanityAdapter(config)
    elif cms_name == 'contentful':
        from contentful.adapter import ContentfulAdapter
        return ContentfulAdapter(config)
    elif cms_name == 'wordpress':
        from wordpress.adapter import WordPressAdapter
        return WordPressAdapter(config)
    else:
        print(f"Error: Unknown CMS '{cms_name}'", file=sys.stderr)
        print("Supported CMSs: sanity, contentful, wordpress", file=sys.stderr)
        sys.exit(1)


def parse_filters(filter_args: Optional[list]) -> dict:
    """Parse filter arguments into dict."""
    if not filter_args:
        return {}

    filters = {}
    for arg in filter_args:
        if '=' not in arg:
            print(f"Warning: Invalid filter format '{arg}' (expected key=value)", file=sys.stderr)
            continue

        key, value = arg.split('=', 1)

        # Parse lists
        if value.startswith('[') and value.endswith(']'):
            value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]

        filters[key] = value

    return filters


def main():
    parser = argparse.ArgumentParser(
        description='Search CMS content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search by keyword
  python cms_search.py --cms sanity --query "quickstart"

  # Filter by content type
  python cms_search.py --cms sanity --content-type article --limit 50

  # Complex filters
  python cms_search.py --cms sanity \\
    --filter "tags=[tutorial,guide]" \\
    --filter "publishedAt=>2024-01-01"

  # JSON output
  python cms_search.py --cms sanity --query "tutorial" --output json > results.json
        """
    )

    parser.add_argument(
        '--cms',
        required=True,
        choices=['sanity', 'contentful', 'wordpress'],
        help='CMS to search'
    )

    parser.add_argument(
        '--query',
        help='Text search query'
    )

    parser.add_argument(
        '--content-type',
        help='Filter by content type'
    )

    parser.add_argument(
        '--filter',
        action='append',
        help='Additional filters (key=value format, can be used multiple times)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Maximum number of results (default: 100)'
    )

    parser.add_argument(
        '--output',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--test-connection',
        action='store_true',
        help='Test CMS connection and exit'
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.cms)

    # Initialize adapter
    try:
        adapter = get_adapter(args.cms, config)
    except Exception as e:
        print(f"Error initializing {args.cms} adapter: {e}", file=sys.stderr)
        sys.exit(1)

    # Test connection if requested
    if args.test_connection:
        print(f"Testing connection to {args.cms}...")
        if adapter.test_connection():
            print("✓ Connection successful")
            sys.exit(0)
        else:
            print("✗ Connection failed")
            sys.exit(1)

    # Parse filters
    filters = parse_filters(args.filter)

    # Perform search
    try:
        print(f"Searching {args.cms}...", file=sys.stderr)
        results = adapter.search(
            query=args.query,
            filters=filters,
            content_type=args.content_type,
            limit=args.limit
        )

        if args.output == 'json':
            # JSON output
            output = [doc.to_dict() for doc in results]
            print(json.dumps(output, indent=2))
        else:
            # Human-readable output
            print(f"\n✓ Found {len(results)} documents\n", file=sys.stderr)

            for doc in results:
                print(f"ID: {doc.id}")
                print(f"Title: {doc.title}")
                print(f"Type: {doc.content_type}")
                print(f"Status: {doc.status}")
                if doc.url:
                    print(f"URL: {doc.url}")
                if doc.author:
                    print(f"Author: {doc.author}")
                if doc.published_date:
                    print(f"Published: {doc.published_date}")
                if doc.last_modified:
                    print(f"Modified: {doc.last_modified}")

                # Show metadata summary
                if doc.metadata:
                    if doc.metadata.get('tags'):
                        print(f"Tags: {', '.join(doc.metadata['tags'])}")
                    if doc.metadata.get('categories'):
                        print(f"Categories: {', '.join(doc.metadata['categories'])}")

                print()

    except Exception as e:
        print(f"Error during search: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
