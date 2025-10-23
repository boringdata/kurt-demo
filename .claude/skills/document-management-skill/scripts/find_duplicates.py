"""Find duplicate documents by content hash."""

from kurt.database import get_session
from kurt.models.models import Document
from sqlmodel import select
from collections import defaultdict

session = get_session()
stmt = select(Document).where(Document.content_hash.isnot(None))
docs = session.exec(stmt).all()

# Group by content hash
hash_groups = defaultdict(list)
for doc in docs:
    hash_groups[doc.content_hash].append(doc)

# Find duplicates (more than one doc with same hash)
duplicates = {h: docs for h, docs in hash_groups.items() if len(docs) > 1}

if duplicates:
    print(f"Found {len(duplicates)} duplicate groups:\n")
    for content_hash, docs in duplicates.items():
        print(f"Hash: {content_hash[:16]}... ({len(docs)} documents)")
        for doc in docs:
            print(f"  - {doc.title[:50]}")
            print(f"    ID: {str(doc.id)[:8]}... URL: {doc.source_url}")
else:
    print("No duplicates found")
