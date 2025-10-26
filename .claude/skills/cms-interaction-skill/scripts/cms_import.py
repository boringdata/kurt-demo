#!/usr/bin/env python3
"""
Import CMS content into Kurt database.

Maps markdown files from CMS fetch to Kurt document records,
then runs metadata extraction.

Usage:
    python cms_import.py --cms sanity --source-dir sources/cms/sanity/
    python cms_import.py --cms sanity --file sources/cms/sanity/article/quickstart.md
"""

import argparse
import subprocess
import sys
import yaml
from pathlib import Path
from typing import List, Optional


def parse_frontmatter(file_path: Path) -> dict:
    """Extract YAML frontmatter from markdown file."""
    with open(file_path, 'r') as f:
        content = f.read()

    if not content.startswith('---'):
        return {}

    # Find end of frontmatter
    try:
        _, frontmatter_str, _ = content.split('---', 2)
        return yaml.safe_load(frontmatter_str)
    except (ValueError, yaml.YAMLError) as e:
        print(f"Warning: Could not parse frontmatter in {file_path}: {e}", file=sys.stderr)
        return {}


def import_to_kurt(
    file_path: Path,
    cms_name: str,
    create_document: bool = True
) -> Optional[str]:
    """
    Import markdown file to Kurt database.

    Args:
        file_path: Path to markdown file
        cms_name: CMS name (for URL construction)
        create_document: If True, creates new Kurt document record

    Returns:
        Kurt document ID if successful, None otherwise
    """
    # Parse frontmatter to get CMS metadata
    frontmatter = parse_frontmatter(file_path)

    if not frontmatter:
        print(f"Warning: No frontmatter found in {file_path}", file=sys.stderr)
        return None

    cms_id = frontmatter.get('cms_id')
    cms_url = frontmatter.get('cms_url') or frontmatter.get('url')

    if not cms_url:
        # Construct URL from CMS name and ID
        cms_url = f"{cms_name}://{cms_id}"

    # Check if document already exists in Kurt
    try:
        result = subprocess.run(
            ['kurt', 'document', 'list', '--url-contains', cms_url],
            capture_output=True,
            text=True,
            timeout=10
        )

        existing_docs = [line for line in result.stdout.split('\n') if cms_url in line]

        if existing_docs and not create_document:
            # Document exists, get its ID
            # Parse ID from output (format: "ID: <id> | URL: <url> | ...")
            for line in existing_docs:
                if 'ID:' in line:
                    doc_id = line.split('ID:')[1].split('|')[0].strip()
                    print(f"Found existing document: {doc_id}")
                    break
            else:
                print(f"Warning: Could not extract document ID from Kurt output", file=sys.stderr)
                return None
        else:
            # Create new document record
            print(f"Creating Kurt document for: {cms_url}")
            result = subprocess.run(
                ['kurt', 'ingest', 'add', cms_url],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                print(f"Error creating document: {result.stderr}", file=sys.stderr)
                return None

            # Extract document ID from output
            # Output format: "✓ Added: <id>"
            output = result.stdout.strip()
            if 'ID:' in output:
                doc_id = output.split('ID:')[1].split('|')[0].strip()
            else:
                print(f"Warning: Could not extract document ID from: {output}", file=sys.stderr)
                # Try to fetch it
                result = subprocess.run(
                    ['kurt', 'document', 'list', '--url-contains', cms_url],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                for line in result.stdout.split('\n'):
                    if 'ID:' in line and cms_url in line:
                        doc_id = line.split('ID:')[1].split('|')[0].strip()
                        break
                else:
                    return None

        # Import content using import_markdown.py
        import_script = Path(__file__).parent.parent.parent.parent / 'scripts' / 'import_markdown.py'

        if not import_script.exists():
            print(f"Error: import_markdown.py not found at {import_script}", file=sys.stderr)
            return None

        print(f"Importing content to document {doc_id}...")
        result = subprocess.run(
            ['python', str(import_script), '--document-id', doc_id, '--file-path', str(file_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"Error importing content: {result.stderr}", file=sys.stderr)
            return None

        print(result.stdout)

        # Run metadata extraction
        print(f"Extracting metadata...")
        result = subprocess.run(
            ['kurt', 'index', doc_id],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"Warning: Metadata extraction failed: {result.stderr}", file=sys.stderr)
        else:
            print("✓ Metadata extracted")

        return doc_id

    except subprocess.TimeoutExpired:
        print(f"Error: Command timed out", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None


def find_markdown_files(directory: Path) -> List[Path]:
    """Find all markdown files in directory."""
    return list(directory.rglob('*.md'))


def main():
    parser = argparse.ArgumentParser(
        description='Import CMS content to Kurt database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import all files from CMS directory
  python cms_import.py --cms sanity --source-dir sources/cms/sanity/

  # Import specific file
  python cms_import.py --cms sanity --file sources/cms/sanity/article/quickstart.md

  # Import without creating new documents (only update existing)
  python cms_import.py --cms sanity --source-dir sources/cms/sanity/ --no-create
        """
    )

    parser.add_argument(
        '--cms',
        required=True,
        help='CMS name (used for URL construction)'
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--source-dir',
        type=Path,
        help='Directory containing markdown files to import'
    )

    group.add_argument(
        '--file',
        type=Path,
        help='Single file to import'
    )

    parser.add_argument(
        '--no-create',
        action='store_true',
        help='Only update existing documents (do not create new ones)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be imported without actually doing it'
    )

    args = parser.parse_args()

    # Collect files to import
    if args.source_dir:
        if not args.source_dir.exists():
            print(f"Error: Directory not found: {args.source_dir}", file=sys.stderr)
            sys.exit(1)

        files = find_markdown_files(args.source_dir)
        if not files:
            print(f"No markdown files found in {args.source_dir}", file=sys.stderr)
            sys.exit(1)
    else:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        files = [args.file]

    print(f"Found {len(files)} file(s) to import", file=sys.stderr)

    if args.dry_run:
        print("\nDry run - would import:", file=sys.stderr)
        for file_path in files:
            frontmatter = parse_frontmatter(file_path)
            title = frontmatter.get('title', file_path.name)
            cms_id = frontmatter.get('cms_id', 'unknown')
            print(f"  - {title} (CMS ID: {cms_id})", file=sys.stderr)
        sys.exit(0)

    # Import files
    success_count = 0
    error_count = 0

    for file_path in files:
        print(f"\n{'='*60}")
        print(f"Importing: {file_path}")
        print('='*60)

        doc_id = import_to_kurt(
            file_path,
            args.cms,
            create_document=not args.no_create
        )

        if doc_id:
            success_count += 1
            print(f"✓ Success: {doc_id}\n")
        else:
            error_count += 1
            print(f"✗ Failed\n")

    # Summary
    print(f"\n{'='*60}")
    print("Import Summary")
    print('='*60)
    print(f"Total files: {len(files)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {error_count}")

    if error_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
