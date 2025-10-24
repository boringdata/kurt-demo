#!/usr/bin/env python3
"""
Update content map JSON file with extracted metadata.

This script:
1. Reads existing content map (or creates new one)
2. Adds/updates entry for a document
3. Attempts simple cluster matching
4. Writes back to JSON

Content maps are stored per-domain in: /sources/{domain}/_content-map.json
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


def get_content_map_path(file_path: str) -> str:
    """
    Determine content map path for a given source file.

    Examples:
        /sources/docs.getdbt.com/docs/build/file.md
        -> /sources/docs.getdbt.com/_content-map.json
    """
    path = Path(file_path)
    parts = path.parts

    sources_idx = parts.index('sources') if 'sources' in parts else -1
    if sources_idx == -1 or sources_idx + 1 >= len(parts):
        raise ValueError(f"File path {file_path} is not in /sources/ directory")

    # Domain directory is first after sources
    domain_dir = Path(*parts[:sources_idx + 2])

    return str(domain_dir / '_content-map.json')


def load_content_map(map_path: str) -> Dict[str, Any]:
    """
    Load existing content map or create new structure.

    Returns dict with:
        - domain: str
        - last_updated: str (ISO timestamp)
        - sitemap: Dict[url, metadata]
        - clusters: List[cluster objects]
        - topics: Dict[topic, count]
    """
    if os.path.exists(map_path):
        with open(map_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Extract domain from path
    domain = Path(map_path).parent.name

    # Create new content map structure
    return {
        "domain": domain,
        "last_updated": datetime.now().isoformat(),
        "sitemap": {},
        "clusters": [],
        "topics": {}
    }


def find_matching_cluster(
    topics: List[str],
    existing_clusters: List[Dict[str, Any]]
) -> Optional[str]:
    """
    Find best matching cluster based on topic overlap.

    Simple matching: if 2+ topics match, consider it same cluster.
    Returns cluster name or None if no good match.
    """
    if not topics or not existing_clusters:
        return None

    best_cluster = None
    best_overlap = 0

    for cluster in existing_clusters:
        cluster_name = cluster.get('name', '')
        cluster_topics = cluster.get('topics', [])

        # Count topic overlap
        overlap = len(set(topics) & set(cluster_topics))

        if overlap > best_overlap and overlap >= 2:
            best_overlap = overlap
            best_cluster = cluster_name

    return best_cluster


def add_to_cluster(
    cluster_name: str,
    url: str,
    topics: List[str],
    clusters: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Add URL to existing cluster or create new cluster.
    """
    # Find existing cluster
    for cluster in clusters:
        if cluster['name'] == cluster_name:
            # Add URL if not already there
            if url not in cluster.get('urls', []):
                cluster.setdefault('urls', []).append(url)
            # Merge topics
            cluster_topics = set(cluster.get('topics', []))
            cluster_topics.update(topics)
            cluster['topics'] = sorted(list(cluster_topics))
            return clusters

    # Create new cluster
    clusters.append({
        "name": cluster_name,
        "description": f"Content related to {', '.join(topics[:3])}",
        "urls": [url],
        "topics": topics
    })

    return clusters


def update_topic_counts(topics: List[str], topic_counts: Dict[str, int]) -> Dict[str, int]:
    """
    Update global topic counts.
    """
    for topic in topics:
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
    return topic_counts


def main():
    if len(sys.argv) < 2:
        print("Usage: python update_content_map.py <extracted_metadata_json>", file=sys.stderr)
        print("", file=sys.stderr)
        print("Input should be JSON output from extract_metadata.py", file=sys.stderr)
        sys.exit(1)

    # Read extracted metadata from stdin or arg
    if sys.argv[1] == '-':
        metadata_json = sys.stdin.read()
    else:
        metadata_json = sys.argv[1]

    try:
        metadata = json.loads(metadata_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing input JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract fields
    file_path = metadata.get('file_path')
    url = metadata.get('url')
    frontmatter = metadata.get('frontmatter', {})
    extracted = metadata.get('extracted', {})

    if not file_path or not url:
        print("Error: metadata must include file_path and url", file=sys.stderr)
        sys.exit(1)

    # Get content map path
    try:
        map_path = get_content_map_path(file_path)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Load or create content map
    content_map = load_content_map(map_path)

    # Prepare entry
    topics = extracted.get('topics', [])
    entities = extracted.get('entities', [])
    summary = extracted.get('summary', '')
    content_type = extracted.get('content_type', 'other')

    # Find matching cluster
    cluster = find_matching_cluster(topics, content_map['clusters'])
    if not cluster:
        # Create cluster name from first topic
        cluster = topics[0] if topics else 'unclustered'

    # Add to cluster
    content_map['clusters'] = add_to_cluster(
        cluster,
        url,
        topics,
        content_map['clusters']
    )

    # Update topic counts
    content_map['topics'] = update_topic_counts(topics, content_map.get('topics', {}))

    # Create sitemap entry
    sitemap_entry = {
        "status": "FETCHED",
        "file_path": file_path,
        "title": frontmatter.get('title', extracted.get('title', '')),
        "author": frontmatter.get('author'),
        "published_date": frontmatter.get('published_date'),
        "topics": topics,
        "entities": entities,
        "summary": summary,
        "content_type": content_type,
        "cluster": cluster,
        "metadata_level": "basic",
        "source": "dynamic_fetch",
        "indexed_at": datetime.now().isoformat()
    }

    # Update sitemap
    content_map['sitemap'][url] = sitemap_entry
    content_map['last_updated'] = datetime.now().isoformat()

    # Write back to file
    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump(content_map, f, indent=2, ensure_ascii=False)

    # Output summary
    result = {
        "status": "success",
        "content_map_path": map_path,
        "url": url,
        "title": sitemap_entry['title'],
        "topics": topics,
        "cluster": cluster,
        "metadata_level": "basic"
    }

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
