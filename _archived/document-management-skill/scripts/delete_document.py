"""Delete document from database."""

from kurt.document import delete_document, get_document

# Preview what will be deleted
doc = get_document("44ea066e")
print(f"About to delete: {doc['title']}")
print(f"URL: {doc['source_url']}")

# Delete (with optional content file deletion)
result = delete_document("44ea066e", delete_content=True)

print(f"\n✓ Deleted: {result['title']}")
print(f"  Content file deleted: {result['content_deleted']}")
