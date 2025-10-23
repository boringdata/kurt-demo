-- Kurt Document SQL Query Examples
-- Database: .kurt/kurt.sqlite

-- List all documents
SELECT id, title, ingestion_status, source_url
FROM documents ORDER BY created_at DESC;

-- Count by status
SELECT ingestion_status, COUNT(*) as count
FROM documents GROUP BY ingestion_status;

-- Find by title
SELECT id, title FROM documents
WHERE title LIKE '%Python%';

-- Filter by URL prefix (specific domain)
SELECT id, title, source_url FROM documents
WHERE source_url LIKE 'https://example.com%'
ORDER BY created_at DESC;

-- Filter by URL substring (e.g., blog posts)
SELECT id, title, source_url FROM documents
WHERE source_url LIKE '%/blog/%'
ORDER BY created_at DESC;

-- Combine URL filters (e.g., blog posts from example.com)
SELECT id, title, source_url FROM documents
WHERE source_url LIKE 'https://example.com%'
  AND source_url LIKE '%/blog/%'
ORDER BY created_at DESC;

-- Count documents by domain
SELECT
    CASE
        WHEN source_url LIKE 'https://example.com%' THEN 'example.com'
        WHEN source_url LIKE 'https://docs.example.com%' THEN 'docs.example.com'
        ELSE 'other'
    END as domain,
    COUNT(*) as count
FROM documents
GROUP BY domain;

-- Documents with authors (JSON field)
SELECT title, json_extract(author, '$[0]') as first_author
FROM documents WHERE author IS NOT NULL;

-- Documents with specific category
SELECT title, json_extract(categories, '$') as categories
FROM documents
WHERE json_extract(categories, '$') LIKE '%Python%';

-- Find duplicates by content hash
SELECT content_hash, COUNT(*) as count, GROUP_CONCAT(title, ' | ') as titles
FROM documents WHERE content_hash IS NOT NULL
GROUP BY content_hash HAVING COUNT(*) > 1;

-- Recent documents (last 7 days)
SELECT id, title, created_at FROM documents
WHERE created_at > datetime('now', '-7 days')
ORDER BY created_at DESC;

-- Update document title
UPDATE documents
SET title = 'New Title', updated_at = datetime('now')
WHERE id = '44ea066ecac74b1eafe2a90cee69cb8e';

-- Delete document
DELETE FROM documents WHERE id = '44ea066ecac74b1eafe2a90cee69cb8e';

-- Export to CSV
.mode csv
.output /tmp/documents.csv
SELECT id, title, ingestion_status, source_url FROM documents;
.output stdout
