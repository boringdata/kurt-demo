#!/usr/bin/env python3
"""
Fetch content from CMS and save as markdown files.

Usage:
    python cms_fetch.py --cms sanity --document-id abc-123
    python cms_fetch.py --cms sanity --document-ids abc-123,def-456,ghi-789
    python cms_fetch.py --cms sanity --from-stdin < search-results.json
    python cms_fetch.py --cms sanity --document-id abc-123 --output sources/cms/
"""

import argparse
import json
import sys
import yaml
from pathlib import Path
from typing import List

# Add adapters to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'adapters'))

from base import CMSAdapter, CMSDocument


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
        sys.exit(1)


def save_document(doc: CMSDocument, output_dir: Path, cms_name: str):
    """Save document as markdown file with YAML frontmatter."""
    # Build file path: output_dir/cms-name/content-type/slug-or-id.md
    content_type_dir = output_dir / cms_name / doc.content_type
    content_type_dir.mkdir(parents=True, exist_ok=True)

    # Use slug if available, otherwise use ID
    slug = doc.metadata.get('slug') if doc.metadata else None
    filename = f"{slug}.md" if slug else f"{doc.id}.md"
    filepath = content_type_dir / filename

    # Build YAML frontmatter
    frontmatter = doc.to_frontmatter()
    frontmatter['fetched_from'] = cms_name
    frontmatter['cms_url'] = doc.url if doc.url else f"{cms_name}://{doc.id}"

    # Write file
    with open(filepath, 'w') as f:
        f.write('---\n')
        yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
        f.write('---\n\n')
        f.write(doc.content)

    return filepath


def main():
    parser = argparse.ArgumentParser(
        description='Fetch content from CMS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch single document
  python cms_fetch.py --cms sanity --document-id abc-123

  # Fetch multiple documents
  python cms_fetch.py --cms sanity --document-ids abc-123,def-456,ghi-789

  # Fetch from search results (JSON)
  python cms_search.py --cms sanity --query "tutorial" --output json | \\
    python cms_fetch.py --cms sanity --from-stdin

  # Custom output directory
  python cms_fetch.py --cms sanity --document-id abc-123 --output sources/cms/
        """
    )

    parser.add_argument(
        '--cms',
        required=True,
        choices=['sanity', 'contentful', 'wordpress'],
        help='CMS to fetch from'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--document-id',
        help='Single document ID to fetch'
    )

    group.add_argument(
        '--document-ids',
        help='Comma-separated document IDs to fetch'
    )

    group.add_argument(
        '--from-stdin',
        action='store_true',
        help='Read document IDs or search results from stdin (JSON)'
    )

    parser.add_argument(
        '--output',
        default='sources/cms',
        help='Output directory (default: sources/cms)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be fetched without saving'
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

    # Collect document IDs
    document_ids: List[str] = []

    if args.document_id:
        document_ids = [args.document_id]
    elif args.document_ids:
        document_ids = [id.strip() for id in args.document_ids.split(',')]
    elif args.from_stdin:
        # Read from stdin (could be JSON search results or plain IDs)
        stdin_data = sys.stdin.read().strip()
        try:
            # Try parsing as JSON (from search results)
            data = json.loads(stdin_data)
            if isinstance(data, list):
                document_ids = [item['id'] if isinstance(item, dict) else item for item in data]
            elif isinstance(data, dict) and 'id' in data:
                document_ids = [data['id']]
        except json.JSONDecodeError:
            # Plain text - one ID per line
            document_ids = [line.strip() for line in stdin_data.split('\n') if line.strip()]

    if not document_ids:
        print("Error: No document IDs provided", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching {len(document_ids)} document(s) from {args.cms}...", file=sys.stderr)

    # Fetch documents
    try:
        if len(document_ids) == 1:
            documents = [adapter.fetch(document_ids[0])]
        else:
            documents = adapter.fetch_batch(document_ids)

        if args.dry_run:
            print("\nDry run - would fetch:", file=sys.stderr)
            for doc in documents:
                print(f"  - {doc.title} ({doc.id})", file=sys.stderr)
            sys.exit(0)

        # Save documents
        output_dir = Path(args.output)
        saved_files = []

        for doc in documents:
            filepath = save_document(doc, output_dir, args.cms)
            saved_files.append(filepath)
            print(f"✓ Saved: {filepath}")

        print(f"\n✓ Fetched {len(documents)} document(s)", file=sys.stderr)
        print(f"  Output: {output_dir}/{args.cms}/", file=sys.stderr)

    except Exception as e:
        print(f"Error during fetch: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
