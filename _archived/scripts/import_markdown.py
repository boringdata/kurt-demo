#!/usr/bin/env python3
"""
Import existing markdown file into Kurt database.
Updates ERROR records to FETCHED status and links content files.
Extracts and populates metadata from YAML frontmatter if present.
"""

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import yaml
except ImportError:
    yaml = None


def calculate_content_hash(file_path: str) -> str:
    """Calculate SHA256 hash of file content."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_relative_content_path(file_path: str) -> str:
    """
    Convert absolute or project-relative path to content_path format.

    Examples:
      sources/docs.getdbt.com/guides/fusion.md
        → docs.getdbt.com/guides/fusion.md

      projects/my-project/sources/internal-spec.md
        → projects/my-project/sources/internal-spec.md
    """
    # Remove leading sources/ if present
    if file_path.startswith('sources/'):
        return file_path[8:]  # Remove "sources/" prefix

    # Keep full path for project-specific sources
    return file_path


def parse_frontmatter(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Parse YAML frontmatter from markdown file.

    Returns:
        Dictionary of metadata fields, or None if no frontmatter found
    """
    if yaml is None:
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for YAML frontmatter (--- at start and end)
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(frontmatter_pattern, content, re.DOTALL)

        if not match:
            return None

        # Parse YAML
        frontmatter_text = match.group(1)
        metadata = yaml.safe_load(frontmatter_text)

        return metadata if isinstance(metadata, dict) else None

    except Exception as e:
        print(f"Warning: Failed to parse frontmatter: {e}", file=sys.stderr)
        return None


def extract_metadata_for_db(frontmatter: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract and format metadata fields for Kurt database.

    Args:
        frontmatter: Parsed YAML frontmatter dictionary

    Returns:
        Dictionary with database field names and values
    """
    if not frontmatter:
        return {}

    db_metadata = {}

    # Title
    if 'title' in frontmatter:
        db_metadata['title'] = frontmatter['title']

    # Description
    if 'description' in frontmatter:
        db_metadata['description'] = frontmatter['description']

    # Author (store as JSON array)
    if 'author' in frontmatter:
        author = frontmatter['author']
        if isinstance(author, str):
            db_metadata['author'] = json.dumps([author])
        elif isinstance(author, list):
            db_metadata['author'] = json.dumps(author)

    # Published date
    # Try: published_date, published, date, last_modified
    for date_field in ['published_date', 'published', 'date', 'last_modified']:
        if date_field in frontmatter:
            date_val = frontmatter[date_field]
            if date_val:
                db_metadata['published_date'] = str(date_val)
                break

    return db_metadata


def import_markdown_to_kurt(document_id: str, file_path: str) -> bool:
    """
    Update Kurt database record for existing markdown file.
    Extracts and populates metadata from YAML frontmatter if present.

    Args:
        document_id: Kurt document ID (full or partial UUID)
        file_path: Path to markdown file (relative to project root)

    Returns:
        True if successful, False otherwise
    """
    # Verify file exists
    if not Path(file_path).exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return False

    # Calculate content hash
    try:
        content_hash = calculate_content_hash(file_path)
    except Exception as e:
        print(f"ERROR: Failed to read file: {e}", file=sys.stderr)
        return False

    # Get relative content path
    content_path = get_relative_content_path(file_path)

    # Parse frontmatter for metadata
    frontmatter = parse_frontmatter(file_path)
    metadata = extract_metadata_for_db(frontmatter)

    # Connect to Kurt database
    db_path = ".kurt/kurt.sqlite"
    if not Path(db_path).exists():
        print(f"ERROR: Kurt database not found: {db_path}", file=sys.stderr)
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Find document by ID (support partial UUID)
        cursor.execute(
            "SELECT id, source_url, ingestion_status FROM documents WHERE id LIKE ? || '%'",
            (document_id,)
        )
        result = cursor.fetchone()

        if not result:
            print(f"ERROR: Document not found: {document_id}", file=sys.stderr)
            conn.close()
            return False

        full_id, source_url, current_status = result

        # Build UPDATE query dynamically based on available metadata
        update_fields = [
            "ingestion_status = 'FETCHED'",
            "content_path = ?",
            "content_hash = ?",
            "updated_at = CURRENT_TIMESTAMP"
        ]
        update_values = [content_path, content_hash]

        # Add metadata fields if present
        if 'title' in metadata:
            update_fields.append("title = ?")
            update_values.append(metadata['title'])

        if 'description' in metadata:
            update_fields.append("description = ?")
            update_values.append(metadata['description'])

        if 'author' in metadata:
            update_fields.append("author = ?")
            update_values.append(metadata['author'])

        if 'published_date' in metadata:
            update_fields.append("published_date = ?")
            update_values.append(metadata['published_date'])

        # Add document ID at the end for WHERE clause
        update_values.append(full_id)

        # Execute UPDATE
        query = f"""
            UPDATE documents
            SET {', '.join(update_fields)}
            WHERE id = ?
        """
        cursor.execute(query, update_values)

        conn.commit()
        conn.close()

        # Print results
        print(f"✓ Updated document {document_id[:8]}...")
        print(f"  Status: {current_status} → FETCHED")
        print(f"  Path: {content_path}")
        print(f"  Hash: {content_hash[:16]}...")

        if metadata:
            print(f"  Metadata extracted from frontmatter:")
            if 'title' in metadata:
                print(f"    Title: {metadata['title']}")
            if 'author' in metadata:
                authors = json.loads(metadata['author'])
                print(f"    Author: {', '.join(authors)}")
            if 'published_date' in metadata:
                print(f"    Date: {metadata['published_date']}")
            if 'description' in metadata:
                desc_preview = metadata['description'][:60] + '...' if len(metadata['description']) > 60 else metadata['description']
                print(f"    Description: {desc_preview}")

        return True

    except sqlite3.Error as e:
        print(f"ERROR: Database error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Import markdown file into Kurt database"
    )
    parser.add_argument(
        "--document-id",
        required=True,
        help="Kurt document ID (full or partial UUID)"
    )
    parser.add_argument(
        "--file-path",
        required=True,
        help="Path to markdown file (relative to project root)"
    )

    args = parser.parse_args()

    success = import_markdown_to_kurt(args.document_id, args.file_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
