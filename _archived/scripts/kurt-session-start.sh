#!/bin/bash
# Kurt Session Start Hook
# Checks Kurt project status and provides context to Claude

# Check if this is a Kurt project (has .kurt/ directory or kurt.config)
if [[ ! -f "kurt.config" ]] && [[ ! -d ".kurt" ]]; then
  # Not a Kurt project at all
  exit 0
fi

# If .kurt/ exists but no kurt.config, prompt to initialize
if [[ -d ".kurt" ]] && [[ ! -f "kurt.config" ]]; then
  cat <<EOF
{
  "systemMessage": $(echo -e "⚠ **Kurt project not initialized**\n\nYou have Kurt configuration files but haven't run initialization.\n\nRun \`kurt init\` to set up your project." | jq -Rs .),
  "additionalContext": $(echo -e "Kurt project detected (.kurt/ directory exists) but kurt.config missing. User should run 'kurt init'." | jq -Rs .)
}
EOF
  exit 0
fi

# Initialize status variables
KURT_INITIALIZED=false
DB_EXISTS=false
DOCUMENT_COUNT=0
CLUSTER_COUNT=0
HAS_PROJECTS=false

# Output buffer for structured context
OUTPUT=""

# Check if Kurt is initialized
if [[ -f ".kurt/kurt.sqlite" ]]; then
  KURT_INITIALIZED=true
  DB_EXISTS=true
fi

# Add header
OUTPUT+="# Kurt Project Status\n\n"

# Check initialization status
if [[ "$KURT_INITIALIZED" == true ]]; then
  OUTPUT+="✓ **Kurt project initialized**\n"
  OUTPUT+="- Config: \`kurt.config\` found\n"
  OUTPUT+="- Database: \`.kurt/kurt.sqlite\` exists\n\n"
else
  OUTPUT+="⚠ **Kurt project not fully initialized**\n"
  OUTPUT+="- Config exists but database missing\n"
  OUTPUT+="- Run \`kurt init\` to complete setup\n\n"
  # Output and exit early if not initialized
  cat <<EOF
{
  "systemMessage": $(echo -e "$OUTPUT" | jq -Rs .),
  "additionalContext": $(echo -e "$OUTPUT" | jq -Rs .)
}
EOF
  exit 0
fi

# Check for documents
if command -v kurt &> /dev/null; then
  # Get total document count
  DOC_LIST=$(kurt content list 2>/dev/null)
  if [[ "$DOC_LIST" != "No documents found" ]]; then
    DOCUMENT_COUNT=$(echo "$DOC_LIST" | wc -l | tr -d ' ')

    OUTPUT+="## Documents\n"
    OUTPUT+="**Total documents ingested: $DOCUMENT_COUNT**\n\n"

    # Get document counts by domain (extract domain from URLs)
    DOMAINS=$(kurt content list --format json 2>/dev/null | grep -o '"url":"https\?://[^/"]*' | cut -d'"' -f4 | sort | uniq -c | sort -rn)
    if [[ -n "$DOMAINS" ]]; then
      OUTPUT+="Documents by source:\n"
      while IFS= read -r line; do
        count=$(echo "$line" | awk '{print $1}')
        domain=$(echo "$line" | awk '{print $2}')
        OUTPUT+="- \`$domain\`: $count documents\n"
      done <<< "$DOMAINS"
      OUTPUT+="\n"
    fi
  else
    OUTPUT+="## Documents\n"
    OUTPUT+="⚠ **No documents ingested yet**\n"
    OUTPUT+="- Run the \`user-onboarding\` skill to map and ingest content\n"
    OUTPUT+="- Or use: \`kurct content map <url>\` to discover content\n\n"
  fi

  # Check for clusters
  CLUSTER_LIST=$(kurt cluster list 2>/dev/null)
  if [[ "$CLUSTER_LIST" != *"No clusters found"* ]] && [[ -n "$CLUSTER_LIST" ]]; then
    CLUSTER_COUNT=$(echo "$CLUSTER_LIST" | grep -c "^" || echo "0")
    OUTPUT+="## Topic Clusters\n"
    OUTPUT+="**$CLUSTER_COUNT topic clusters computed**\n"
    OUTPUT+="- View with: \`kurt cluster list\`\n\n"
  else
    if [[ "$DOCUMENT_COUNT" -gt 0 ]]; then
      OUTPUT+="## Topic Clusters\n"
      OUTPUT+="⚠ **No clusters computed yet**\n"
      OUTPUT+="- Run: \`kurt cluster compute --url-contains \"\"\` to analyze content\n\n"
    fi
  fi
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
  OUTPUT+="**Content ingested and analyzed.** Consider:\n"
  OUTPUT+="- Use \`/create-project\` to create a project based on your content\n"
  OUTPUT+="- Explore documents with the \`document-management\` skill\n"
elif [[ "$DOCUMENT_COUNT" -gt 0 ]]; then
  OUTPUT+="**Content ingested but not analyzed.** Next:\n"
  OUTPUT+="- Run: \`kurt cluster compute --url-contains \"\"\` to discover topics\n"
  OUTPUT+="- Then use \`/create-project\` to organize your work\n"
else
  OUTPUT+="**Ready to start!** Choose an approach:\n"
  OUTPUT+="- Use \`/create-project\` for quick project setup\n"
  OUTPUT+="- Run the \`user-onboarding\` skill for comprehensive guided setup\n"
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
