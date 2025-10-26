#!/usr/bin/env python3
"""
Publish draft content to CMS.

Creates draft in CMS from markdown file (does not auto-publish).
User must review and publish from CMS interface.

Usage:
    python cms_publish.py --cms sanity --file draft.md --document-id abc-123
    python cms_publish.py --cms sanity --file draft.md --create-new --content-type article
"""

import argparse
import sys
import yaml
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


def parse_markdown_file(file_path: Path) -> tuple[dict, str]:
    """
    Parse markdown file with YAML frontmatter.

    Returns:
        Tuple of (frontmatter_dict, markdown_content)
    """
    with open(file_path, 'r') as f:
        content = f.read()

    frontmatter = {}
    markdown_content = content

    if content.startswith('---'):
        try:
            _, frontmatter_str, markdown_content = content.split('---', 2)
            frontmatter = yaml.safe_load(frontmatter_str) or {}
            markdown_content = markdown_content.strip()
        except (ValueError, yaml.YAMLError) as e:
            print(f"Warning: Could not parse frontmatter: {e}", file=sys.stderr)

    return frontmatter, markdown_content


def extract_metadata(frontmatter: dict, args) -> dict:
    """Extract CMS metadata from frontmatter and CLI args."""
    metadata = {}

    # Slug
    if 'slug' in frontmatter:
        metadata['slug'] = frontmatter['slug']
    elif hasattr(args, 'slug') and args.slug:
        metadata['slug'] = args.slug

    # Author
    if 'author_id' in frontmatter:
        metadata['author'] = frontmatter['author_id']
    elif hasattr(args, 'author') and args.author:
        metadata['author'] = args.author

    # Categories
    if 'category_ids' in frontmatter:
        metadata['categories'] = frontmatter['category_ids']
    elif hasattr(args, 'categories') and args.categories:
        metadata['categories'] = args.categories

    # Tags
    if 'tags' in frontmatter:
        metadata['tags'] = frontmatter['tags']
    elif hasattr(args, 'tags') and args.tags:
        metadata['tags'] = args.tags

    # SEO
    if 'seo' in frontmatter:
        metadata['seo'] = frontmatter['seo']

    return metadata


def main():
    parser = argparse.ArgumentParser(
        description='Publish draft content to CMS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update existing document as draft
  python cms_publish.py \\
    --cms sanity \\
    --file projects/my-project/targets/article-draft.md \\
    --document-id abc-123

  # Create new document as draft
  python cms_publish.py \\
    --cms sanity \\
    --file projects/my-project/targets/new-article.md \\
    --create-new \\
    --content-type article \\
    --slug "new-article-slug"

  # Update with metadata
  python cms_publish.py \\
    --cms sanity \\
    --file draft.md \\
    --document-id abc-123 \\
    --tags "tutorial,guide,quickstart"

Note: This creates DRAFTS only. User must review and publish from CMS.
        """
    )

    parser.add_argument(
        '--cms',
        required=True,
        choices=['sanity', 'contentful', 'wordpress'],
        help='CMS to publish to'
    )

    parser.add_argument(
        '--file',
        type=Path,
        required=True,
        help='Markdown file to publish'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--document-id',
        help='CMS document ID to update'
    )

    group.add_argument(
        '--create-new',
        action='store_true',
        help='Create new document'
    )

    parser.add_argument(
        '--content-type',
        help='CMS content type (required when creating new)'
    )

    parser.add_argument(
        '--slug',
        help='Document slug (optional)'
    )

    parser.add_argument(
        '--author',
        help='Author reference ID (optional)'
    )

    parser.add_argument(
        '--categories',
        help='Comma-separated category IDs (optional)'
    )

    parser.add_argument(
        '--tags',
        help='Comma-separated tags (optional)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be published without actually doing it'
    )

    args = parser.parse_args()

    # Validate
    if args.create_new and not args.content_type:
        print("Error: --content-type required when using --create-new", file=sys.stderr)
        sys.exit(1)

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Parse markdown file
    print(f"Reading: {args.file}", file=sys.stderr)
    frontmatter, markdown_content = parse_markdown_file(args.file)

    # Extract title
    title = frontmatter.get('title')
    if not title:
        # Try to extract from first heading
        for line in markdown_content.split('\n'):
            if line.startswith('# '):
                title = line[2:].strip()
                break

    if not title:
        print("Error: Could not determine title (add 'title' to frontmatter or use # heading)", file=sys.stderr)
        sys.exit(1)

    # Get content type
    if args.create_new:
        content_type = args.content_type
    else:
        content_type = frontmatter.get('cms_type', 'article')

    # Extract metadata
    metadata = extract_metadata(frontmatter, args)

    # Parse categories and tags from CLI
    if args.categories:
        metadata['categories'] = [c.strip() for c in args.categories.split(',')]
    if args.tags:
        metadata['tags'] = [t.strip() for t in args.tags.split(',')]

    if args.dry_run:
        print("\nDry run - would publish:", file=sys.stderr)
        print(f"  CMS: {args.cms}", file=sys.stderr)
        print(f"  Title: {title}", file=sys.stderr)
        print(f"  Content Type: {content_type}", file=sys.stderr)
        if args.document_id:
            print(f"  Update Document: {args.document_id}", file=sys.stderr)
        else:
            print(f"  Create New: Yes", file=sys.stderr)
        print(f"  Metadata: {metadata}", file=sys.stderr)
        print(f"  Content Length: {len(markdown_content)} chars", file=sys.stderr)
        sys.exit(0)

    # Load configuration
    config = load_config(args.cms)

    # Initialize adapter
    try:
        adapter = get_adapter(args.cms, config)
    except Exception as e:
        print(f"Error initializing {args.cms} adapter: {e}", file=sys.stderr)
        sys.exit(1)

    # Create draft
    try:
        print(f"\nPublishing to {args.cms}...", file=sys.stderr)

        result = adapter.create_draft(
            content=markdown_content,
            title=title,
            content_type=content_type,
            metadata=metadata,
            document_id=args.document_id
        )

        print("\n✓ Draft created successfully!")
        print(f"\nDraft ID: {result['draft_id']}")
        print(f"Draft URL: {result['draft_url']}")
        print("\nIMPORTANT: Review and publish from CMS interface")

    except Exception as e:
        print(f"\nError creating draft: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    # Need json for config loading
    import json
    main()
