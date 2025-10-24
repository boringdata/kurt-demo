#!/bin/bash
# Kurt Session Start Hook
# Checks Kurt project status and provides context to Claude

# Exit early if kurt.config doesn't exist (not a Kurt project)
if [[ ! -f "kurt.config" ]]; then
  exit 0
fi

# Initialize status variables
KURT_INITIALIZED=false
HAS_CONTENT_MAPS=false
DOCUMENT_COUNT=0
CLUSTER_COUNT=0
HAS_PROJECTS=false

# Output buffer for structured context
OUTPUT=""

# Check if sources directory exists with content maps
if [[ -d "sources" ]]; then
  CONTENT_MAP_COUNT=$(find sources -name "_content-map.json" 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$CONTENT_MAP_COUNT" -gt 0 ]]; then
    KURT_INITIALIZED=true
    HAS_CONTENT_MAPS=true
  fi
fi

# Add header
OUTPUT+="# Kurt Project Status\n\n"

# Check initialization status
if [[ "$KURT_INITIALIZED" == true ]]; then
  OUTPUT+="✓ **Kurt project initialized (file-based)**\n"
  OUTPUT+="- Config: \`kurt.config\` found\n"
  OUTPUT+="- Content maps: $CONTENT_MAP_COUNT domain(s) mapped\n\n"
else
  OUTPUT+="⚠ **No content mapped yet**\n"
  OUTPUT+="- Run \`python .claude/scripts/map_sitemap.py <domain> --recursive\` to discover content\n"
  OUTPUT+="- Or use \`/create-project\` to start with guided setup\n\n"
  # Output and exit early if not initialized
  cat <<EOF
{
  "systemMessage": $(echo -e "$OUTPUT" | jq -Rs .),
  "additionalContext": $(echo -e "$OUTPUT" | jq -Rs .)
}
EOF
  exit 0
fi

# Check for documents in content maps
if [[ "$HAS_CONTENT_MAPS" == true ]]; then
  OUTPUT+="## Content Maps\n"

  # Count documents across all content maps
  TOTAL_DISCOVERED=0
  TOTAL_FETCHED=0
  TOTAL_CLUSTERS=0

  for content_map in sources/*/_content-map.json; do
    if [[ -f "$content_map" ]]; then
      domain=$(dirname "$content_map" | xargs basename)

      # Count discovered and fetched URLs
      discovered=$(jq '[.sitemap[] | select(.status == "DISCOVERED")] | length' "$content_map" 2>/dev/null || echo "0")
      fetched=$(jq '[.sitemap[] | select(.status == "FETCHED")] | length' "$content_map" 2>/dev/null || echo "0")
      clusters=$(jq '.clusters | length' "$content_map" 2>/dev/null || echo "0")

      TOTAL_DISCOVERED=$((TOTAL_DISCOVERED + discovered))
      TOTAL_FETCHED=$((TOTAL_FETCHED + fetched))
      TOTAL_CLUSTERS=$((TOTAL_CLUSTERS + clusters))

      OUTPUT+="**\`$domain\`:**\n"
      OUTPUT+="- Discovered: $discovered URLs\n"
      OUTPUT+="- Fetched: $fetched URLs (files in /sources/)\n"
      OUTPUT+="- Clusters: $clusters topic clusters\n\n"
    fi
  done

  DOCUMENT_COUNT=$TOTAL_FETCHED
  CLUSTER_COUNT=$TOTAL_CLUSTERS

  OUTPUT+="**Totals:**\n"
  OUTPUT+="- $TOTAL_DISCOVERED URLs discovered from sitemaps\n"
  OUTPUT+="- $TOTAL_FETCHED URLs fetched with metadata\n"
  OUTPUT+="- $TOTAL_CLUSTERS topic clusters\n\n"

  if [[ "$TOTAL_FETCHED" -eq 0 ]]; then
    OUTPUT+="💡 **Tip:** Use WebFetch to fetch specific pages. Hooks automatically save files and extract metadata.\n\n"
  fi
else
  OUTPUT+="## Content Maps\n"
  OUTPUT+="⚠ **No content mapped yet**\n"
  OUTPUT+="- Map a domain: \`python .claude/scripts/map_sitemap.py <domain> --recursive\`\n"
  OUTPUT+="- Or use \`/create-project\` for guided setup\n\n"
fi

# Check for existing projects
OUTPUT+="## Projects\n"
if [[ -d "projects" ]]; then
  PROJECT_COUNT=$(find projects -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$PROJECT_COUNT" -gt 0 ]]; then
    HAS_PROJECTS=true
    OUTPUT+="**Found $PROJECT_COUNT project(s):**\n\n"

    # Call helper script to get project details
    if [[ -f ".claude/scripts/get-project-status.sh" ]]; then
      PROJECT_DETAILS=$(bash .claude/scripts/get-project-status.sh 2>/dev/null)
      OUTPUT+="$PROJECT_DETAILS\n"
    else
      # Fallback: just list project directories
      for project_dir in projects/*/; do
        project_name=$(basename "$project_dir")
        OUTPUT+="- \`$project_name\`\n"
      done
      OUTPUT+="\n"
    fi
  else
    OUTPUT+="⚠ **No projects created yet**\n"
    OUTPUT+="- Create a project with: \`/create-project\`\n"
    OUTPUT+="- Or run the \`user-onboarding\` skill for guided setup\n\n"
  fi
else
  OUTPUT+="⚠ **No projects created yet**\n"
  OUTPUT+="- Create a project with: \`/create-project\`\n"
  OUTPUT+="- Or run the \`user-onboarding\` skill for guided setup\n\n"
fi

# Add contextual recommendations
OUTPUT+="---\n\n"
OUTPUT+="## Recommended Next Steps\n\n"

if [[ "$HAS_PROJECTS" == true ]]; then
  OUTPUT+="**You have existing projects.** Would you like to:\n"
  OUTPUT+="- Use \`/resume-project\` to continue working on a project\n"
  OUTPUT+="- Use \`/create-project\` to start a new project\n"
elif [[ "$DOCUMENT_COUNT" -gt 0 ]] && [[ "$CLUSTER_COUNT" -gt 0 ]]; then
  OUTPUT+="**Content mapped and fetched.** Consider:\n"
  OUTPUT+="- Use \`/create-project\` to create a project based on your content\n"
  OUTPUT+="- Query content maps to explore available content\n"
elif [[ "$DOCUMENT_COUNT" -gt 0 ]]; then
  OUTPUT+="**Content fetched with metadata.** Next:\n"
  OUTPUT+="- Use \`/create-project\` to organize your work\n"
  OUTPUT+="- Or continue fetching more content with WebFetch\n"
elif [[ "$HAS_CONTENT_MAPS" == true ]]; then
  OUTPUT+="**Content mapped but not fetched.** Next:\n"
  OUTPUT+="- Use WebFetch to fetch specific pages (hooks auto-index)\n"
  OUTPUT+="- Or use \`/create-project\` to start working\n"
else
  OUTPUT+="**Ready to start!** Choose an approach:\n"
  OUTPUT+="- Use \`/create-project\` for guided project setup\n"
  OUTPUT+="- Map a domain: \`python .claude/scripts/map_sitemap.py <domain> --recursive\`\n"
fi

# Output the complete context as JSON for visibility
# systemMessage shows to user, additionalContext goes to Claude
cat <<EOF
{
  "systemMessage": $(echo -e "$OUTPUT" | jq -Rs .),
  "additionalContext": $(echo -e "$OUTPUT" | jq -Rs .)
}
EOF

exit 0
