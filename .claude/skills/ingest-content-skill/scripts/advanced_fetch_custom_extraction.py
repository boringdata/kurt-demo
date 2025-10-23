"""
Advanced Content Fetching with Custom Trafilatura Settings

Use when you need custom extraction behavior:
- Include/exclude comments
- Favor precision vs recall
- Custom output formats
- Extraction timeouts

Trafilatura Documentation:
- Core Functions: https://trafilatura.readthedocs.io/en/latest/corefunctions.html
- Extract Function: https://trafilatura.readthedocs.io/en/latest/corefunctions.html#extract
- Extraction Settings: https://trafilatura.readthedocs.io/en/latest/corefunctions.html#extraction-settings
- Metadata Extraction: https://trafilatura.readthedocs.io/en/latest/corefunctions.html#extract-metadata
"""

import trafilatura
from pathlib import Path
import sqlite3
from urllib.parse import urlparse

# 1. Get NOT_FETCHED documents from database
conn = sqlite3.connect('.kurt/kurt.sqlite')
cursor = conn.cursor()
cursor.execute("""
    SELECT id, source_url
    FROM documents
    WHERE ingestion_status = 'NOT_FETCHED'
""")
docs = cursor.fetchall()

# 2. Custom trafilatura extraction
for doc_id, url in docs:
    try:
        # Download
        downloaded = trafilatura.fetch_url(url)

        # Extract with custom settings
        content = trafilatura.extract(
            downloaded,
            output_format='markdown',
            include_comments=False,     # Exclude comments
            include_tables=True,        # Include tables
            include_links=True,         # Preserve links
            favor_precision=True,       # Favor precision over recall
            favor_recall=False,
        )

        if not content:
            raise ValueError("No content extracted")

        # Get metadata
        metadata = trafilatura.extract_metadata(downloaded)
        title = metadata.title if metadata else url.split('/')[-1]

        # 3. Save to filesystem (same structure as kurt)
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path.strip('/') or 'index'
        if not path.endswith('.md'):
            path = path + '.md'

        filepath = Path(f"sources/{domain}/{path}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)

        # 4. Update database
        relative_path = f"{domain}/{path}"
        cursor.execute("""
            UPDATE documents
            SET title = ?,
                content_path = ?,
                ingestion_status = 'FETCHED',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (title, relative_path, doc_id))
        conn.commit()

        print(f"✓ {url} ({len(content)} chars)")

    except Exception as e:
        # Mark as ERROR
        cursor.execute("""
            UPDATE documents
            SET ingestion_status = 'ERROR',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (doc_id,))
        conn.commit()
        print(f"✗ {url}: {e}")

conn.close()
