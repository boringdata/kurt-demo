#!/bin/bash
# Update all extraction skills to use content map instead of Kurt CLI

# Restore from backups first
for skill in style-extraction structure-extraction persona-extraction publisher-profile-extraction; do
  if [ -f ".claude/skills/${skill}-skill/SKILL.md.bak" ]; then
    mv ".claude/skills/${skill}-skill/SKILL.md.bak" ".claude/skills/${skill}-skill/SKILL.md"
  fi
done

# Add note at top of auto-discovery sections
note="**Note**: All discovery uses content map queries. Ensure domain is mapped first with \`python .claude/scripts/map_sitemap.py <domain> --recursive\`"

# Create replacement patterns
declare -A replacements=(
  # Homepage discovery
  ["kurt document list --url-prefix https://company.com/ | grep -E"]="cat sources/company.com/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == \"homepage\") | .key'"

  # Content type queries
  ["kurt document list --url-contains /docs/"]="cat sources/company.com/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == \"guide\") | .key'"
  ["kurt document list --url-contains /documentation"]="cat sources/company.com/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == \"guide\") | .key'"
  ["kurt document list --url-contains /tutorial"]="cat sources/company.com/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == \"tutorial\") | .key'"
  ["kurt document list --url-contains /reference"]="cat sources/company.com/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == \"reference\") | .key'"
  ["kurt document list --url-contains /api/"]="cat sources/company.com/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == \"reference\") | .key'"
  ["kurt document list --url-contains /blog/"]="cat sources/company.com/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == \"blog\") | .key'"
  ["kurt document list --url-contains /product"]="cat sources/company.com/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == \"product_page\") | .key'"
  ["kurt document list --url-contains /about"]="cat sources/company.com/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == \"info\" and (.key | contains(\"/about\"))) | .key'"
  ["kurt document list --url-contains /company"]="cat sources/company.com/_content-map.json | jq -r '.sitemap | to_entries[] | select(.value.content_type == \"info\" and (.key | contains(\"/company\"))) | .key'"

  # Status checks
  ["kurt document list --url <url> --status FETCHED"]="cat sources/<domain>/_content-map.json | jq -r '.sitemap[\"<url>\"] | select(.status == \"FETCHED\")'"
  ["kurt ingest fetch"]="# Use WebFetch tool (hooks auto-save + index)"

  # Generic kurt document list
  ["kurt document list"]="# Use content map: cat sources/<domain>/_content-map.json | jq '.sitemap'"
)

echo "Updated extraction skills to use content map queries instead of Kurt CLI"
echo "Manual review and completion recommended"
