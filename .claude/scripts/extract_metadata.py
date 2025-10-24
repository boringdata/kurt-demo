#!/usr/bin/env python3
"""
Extract metadata from markdown content using Claude API.

This script analyzes a markdown file and extracts:
- Topics (3-5 keywords)
- Entities (companies, products, people)
- Summary (1-2 sentences)
- Content type (blog, docs, tutorial, etc.)

No Kurt CLI dependency - uses Claude API directly.
"""

import sys
import json
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional, List
import anthropic


def parse_frontmatter(content: str) -> tuple[Optional[Dict[str, Any]], str]:
    """
    Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter_dict, content_without_frontmatter)
    """
    if not content.startswith('---'):
        return None, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    # Simple YAML parsing (handles common cases)
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')

            # Handle lists
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]

            frontmatter[key] = value

    return frontmatter, body


def extract_url_from_path(file_path: str) -> str:
    """
    Convert file path to original URL.

    Examples:
        /sources/docs.getdbt.com/docs/build/incremental-models.md
        -> https://docs.getdbt.com/docs/build/incremental-models
    """
    path = Path(file_path)

    # Find sources directory
    parts = path.parts
    sources_idx = parts.index('sources') if 'sources' in parts else -1

    if sources_idx == -1 or sources_idx + 1 >= len(parts):
        return ""

    # Domain is the first directory after sources
    domain = parts[sources_idx + 1]

    # Path is everything after domain, without .md extension
    path_parts = parts[sources_idx + 2:]
    url_path = '/'.join(path_parts)

    # Remove .md extension
    if url_path.endswith('.md'):
        url_path = url_path[:-3]

    return f"https://{domain}/{url_path}"


def extract_metadata_with_claude(content: str, file_path: str) -> Dict[str, Any]:
    """
    Use Claude API to extract metadata from content.

    Returns dict with:
        - topics: List[str]
        - entities: List[str]
        - summary: str
        - content_type: str
    """
    # Get API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    # Truncate content if too long (keep first 4000 chars)
    if len(content) > 4000:
        content = content[:4000] + "\n\n[Content truncated for analysis...]"

    prompt = f"""Analyze this markdown content and extract metadata in JSON format.

File path: {file_path}

Content:
{content}

Extract the following metadata:

1. **topics**: 3-5 main topic keywords that describe what this content is about
2. **entities**: 2-5 important entities mentioned (companies, products, technologies, people)
3. **summary**: 1-2 sentence summary of the content
4. **content_type**: One of: blog, docs, tutorial, guide, api-reference, landing-page, case-study, or other

Return ONLY valid JSON with this structure:
{{
  "topics": ["keyword1", "keyword2", "keyword3"],
  "entities": ["entity1", "entity2"],
  "summary": "Brief summary here.",
  "content_type": "docs"
}}"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    # Extract JSON from response
    response_text = message.content[0].text.strip()

    # Remove markdown code blocks if present
    if response_text.startswith('```'):
        response_text = re.sub(r'^```(?:json)?\n', '', response_text)
        response_text = re.sub(r'\n```$', '', response_text)

    try:
        metadata = json.loads(response_text)
        return metadata
    except json.JSONDecodeError as e:
        print(f"Error parsing Claude response as JSON: {e}", file=sys.stderr)
        print(f"Response was: {response_text}", file=sys.stderr)
        # Return empty metadata as fallback
        return {
            "topics": [],
            "entities": [],
            "summary": "",
            "content_type": "other"
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_metadata.py <file_path>", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]

    # Verify file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)

    # Extract URL from path
    url = extract_url_from_path(file_path)

    # Extract metadata using Claude
    extracted = extract_metadata_with_claude(body, file_path)

    # Combine with frontmatter
    result = {
        "file_path": file_path,
        "url": url,
        "frontmatter": frontmatter or {},
        "extracted": extracted,
        "metadata_level": "basic",
        "extracted_at": None  # Will be set by update_content_map.py
    }

    # Output as JSON
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
