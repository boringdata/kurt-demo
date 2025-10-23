"""Export documents to JSON."""

from kurt.document import list_documents
import json

# Get all documents
docs = list_documents()

# Export to file
with open('/tmp/documents_export.json', 'w') as f:
    json.dump(docs, f, indent=2, default=str)

print(f"✓ Exported {len(docs)} documents to /tmp/documents_export.json")
