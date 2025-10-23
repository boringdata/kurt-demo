"""Get document details by ID."""

from kurt.document import get_document

# Get by partial UUID (minimum 8 chars)
doc = get_document("44ea066e")

print(f"ID: {doc['id']}")
print(f"Title: {doc['title']}")
print(f"Status: {doc['ingestion_status']}")
print(f"URL: {doc['source_url']}")

if doc.get('description'):
    print(f"Description: {doc['description'][:100]}...")

if doc.get('author'):
    print(f"Authors: {', '.join(doc['author'])}")

if doc.get('categories'):
    print(f"Categories: {', '.join(doc['categories'])}")
