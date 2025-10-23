"""Read document content from filesystem."""

from pathlib import Path
from kurt.document import get_document
from kurt.config import load_config

# Example 1: Using config to get absolute path (RECOMMENDED)
print("=" * 60)
print("Example 1: Read content using config (recommended)")
print("=" * 60)

doc_id = "44ea066e"  # Replace with actual document ID
doc = get_document(doc_id)

# Get configured source directory
config = load_config()
source_base = config.get_absolute_source_path()

print(f"Document: {doc['title']}")
print(f"Content path (relative): {doc['content_path']}")
print(f"Source base: {source_base}")

# Build full path
content_file = source_base / doc['content_path']
print(f"Full path: {content_file}")

# Read content
if content_file.exists():
    content = content_file.read_text()
    print(f"\nContent length: {len(content)} characters")
    print(f"First 200 chars:\n{content[:200]}...")
else:
    print(f"ERROR: Content file not found at {content_file}")

print("\n")

# Example 2: Quick method (assumes ./sources/ from project root)
print("=" * 60)
print("Example 2: Quick method (if in project root)")
print("=" * 60)

doc = get_document(doc_id)
content_file = Path(f"./sources/{doc['content_path']}")

print(f"Reading from: {content_file}")
if content_file.exists():
    content = content_file.read_text()
    print(f"Success! Content length: {len(content)} characters")
else:
    print(f"ERROR: File not found (are you in the project root?)")

print("\n")

# Example 3: Find content files using pattern matching
print("=" * 60)
print("Example 3: Find files by pattern")
print("=" * 60)

# Find all markdown files in sources directory
config = load_config()
source_base = config.get_absolute_source_path()

# Example: Find all files from juhache.substack.com
pattern = "**/juhache.substack.com/**/*.md"
files = list(source_base.glob(pattern))

print(f"Found {len(files)} files matching '{pattern}':")
for f in files[:5]:  # Show first 5
    relative = f.relative_to(source_base)
    print(f"  - {relative}")

if len(files) > 5:
    print(f"  ... and {len(files) - 5} more")

print("\n")

# Example 4: Batch read multiple documents
print("=" * 60)
print("Example 4: Batch read multiple documents")
print("=" * 60)

from kurt.document import list_documents

docs = list_documents(url_prefix="https://juhache.substack.com", limit=3)

config = load_config()
source_base = config.get_absolute_source_path()

for doc in docs:
    content_file = source_base / doc['content_path']

    if content_file.exists():
        content = content_file.read_text()
        print(f"✓ {doc['title'][:50]}")
        print(f"  Path: {doc['content_path']}")
        print(f"  Size: {len(content)} chars")
    else:
        print(f"✗ {doc['title'][:50]}")
        print(f"  Missing: {content_file}")
    print()
