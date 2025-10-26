# Sanity CMS Adapter

Integration with Sanity.io CMS using GROQ queries and the Sanity Python client.

## Setup

### 1. Install Dependencies

```bash
pip install sanity pyyaml
```

### 2. Get Sanity Credentials

From your Sanity project dashboard:

1. **Project ID**: Found in project settings
2. **Dataset**: Usually `production`
3. **Read Token**:
   - Go to API settings
   - Create new token with `Viewer` role
   - Copy token (shown once)
4. **Write Token** (for drafts):
   - Create another token with `Editor` role
   - Copy token

### 3. Configure

Copy the example config:

```bash
cp .claude/skills/cms-interaction-skill/adapters/sanity/config.json.example \
   .claude/scripts/cms-config.json
```

Edit `.claude/scripts/cms-config.json`:

```json
{
  "sanity": {
    "project_id": "abc12345",
    "dataset": "production",
    "token": "sk...xyz",
    "write_token": "sk...abc",
    "use_cdn": false,
    "base_url": "https://yoursite.com"
  }
}
```

**Important**: Add `cms-config.json` to `.gitignore`!

```bash
echo ".claude/scripts/cms-config.json" >> .gitignore
```

### 4. Test Connection

```bash
python .claude/skills/cms-interaction-skill/scripts/cms_search.py \
  --cms sanity \
  --test-connection
```

## Features

### GROQ Query Support

The adapter uses Sanity's GROQ query language for powerful searches:

```bash
# Text search
python cms_search.py --cms sanity --query "quickstart"

# Filter by content type
python cms_search.py --cms sanity --content-type article

# Complex filters
python cms_search.py --cms sanity \
  --filter "tags=[tutorial,guide]" \
  --filter "publishedAt=>2024-01-01"
```

### Portable Text Conversion

The adapter converts Sanity's Portable Text format to/from markdown:

**Supported features:**
- Headings (h1-h4)
- Paragraphs
- Bold, italic, code inline formatting
- Code blocks with language
- Blockquotes
- Images (basic support)

**Limitations:**
- Complex nested structures may need manual adjustment
- Custom marks/annotations not fully supported
- For production, consider using a dedicated portable text library

### Draft System

Sanity's draft system is fully supported:

- Creating drafts: `drafts.{document-id}` format
- Updating drafts: Updates existing draft version
- Searching drafts: Included in results with `status: draft`

## Content Types

List available content types in your Sanity dataset:

```bash
# This will query your schema
python cms_search.py --cms sanity --content-type <type-name> --limit 1
```

Common Sanity content types:
- `post` - Blog posts
- `page` - Static pages
- `article` - Articles
- `product` - Products

## URL Construction

The adapter constructs document URLs using:

1. `base_url` from config
2. Document `slug` field

Example:
- Base URL: `https://yoursite.com`
- Slug: `blog/my-post`
- Result: `https://yoursite.com/blog/my-post`

If no slug exists, uses CMS ID: `sanity://abc-123`

## Troubleshooting

### "sanity-python package not installed"

```bash
pip install sanity
```

### "Connection test failed"

- Check `project_id` and `dataset` are correct
- Verify token has proper permissions
- Check network/firewall settings

### "No configuration found for CMS 'sanity'"

- Ensure `cms-config.json` exists at `.claude/scripts/cms-config.json`
- Check JSON syntax is valid
- Verify `sanity` key exists in config

### GROQ Query Errors

If GROQ queries fail:
- Validate filter syntax in Sanity Studio's Vision tool
- Check field names match your schema
- Ensure referenced fields exist

### Draft Creation Fails

- Verify `write_token` has `Editor` role
- Check content type exists in schema
- Ensure required fields are provided

## Advanced Usage

### Custom GROQ Queries

For advanced queries, modify `sanity/adapter.py` or use Sanity Vision tool to test queries first.

### Schema Introspection

Sanity doesn't provide schema introspection via API. To get available fields:

1. Use Sanity Studio's Schema view
2. Check your schema files (`schemas/*.js`)
3. Use Vision tool to test field availability

### Webhooks

For real-time sync, set up Sanity webhooks:

1. Go to API settings in Sanity dashboard
2. Create webhook for document changes
3. Point to your sync endpoint

## References

- [Sanity Python Client](https://github.com/sanity-io/sanity-python)
- [GROQ Query Language](https://www.sanity.io/docs/groq)
- [Portable Text](https://www.sanity.io/docs/presenting-block-text)
- [Sanity API Docs](https://www.sanity.io/docs/http-api)
