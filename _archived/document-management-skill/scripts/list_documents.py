"""List documents with filtering."""

from kurt.document import list_documents
from kurt.models.models import IngestionStatus

# Example 1: List fetched documents with limit
print("=" * 60)
print("Example 1: List fetched documents")
print("=" * 60)
docs = list_documents(status=IngestionStatus.FETCHED, limit=10)

for doc in docs:
    print(f"{doc['id'][:8]}... {doc['title'][:50]}")
    if doc.get('author'):
        print(f"  Author: {', '.join(doc['author'])}")
    if doc.get('categories'):
        print(f"  Categories: {', '.join(doc['categories'][:3])}")
    print()

# Example 2: Filter by URL prefix (specific domain)
print("\n" + "=" * 60)
print("Example 2: Documents from a specific domain")
print("=" * 60)
docs = list_documents(url_prefix="https://example.com", limit=10)
for doc in docs:
    print(f"{doc['id'][:8]}... {doc['title'][:50]}")
    print(f"  URL: {doc['source_url']}")
    print()

# Example 3: Filter by URL substring (find blog posts)
print("\n" + "=" * 60)
print("Example 3: Documents with 'blog' in URL")
print("=" * 60)
docs = list_documents(url_contains="blog", limit=10)
for doc in docs:
    print(f"{doc['id'][:8]}... {doc['title'][:50]}")
    print(f"  URL: {doc['source_url']}")
    print()

# Example 4: Combine multiple filters
print("\n" + "=" * 60)
print("Example 4: Fetched articles from example.com")
print("=" * 60)
docs = list_documents(
    status=IngestionStatus.FETCHED,
    url_prefix="https://example.com",
    url_contains="article",
    limit=10
)
for doc in docs:
    print(f"{doc['id'][:8]}... {doc['title'][:50]}")
    print(f"  URL: {doc['source_url']}")
    print(f"  Status: {doc['ingestion_status']}")
    print()
