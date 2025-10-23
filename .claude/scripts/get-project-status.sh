#!/bin/bash
# Get Project Status Helper
# Scans projects/ directory and extracts metadata from project.md files

# Check if projects directory exists
if [[ ! -d "projects" ]]; then
  exit 0
fi

# Function to extract content between markdown headers
extract_section() {
  local file="$1"
  local header="$2"
  local content=""

  # Use awk to extract content between the specified header and the next header
  content=$(awk -v header="^## $header" '
    $0 ~ header {found=1; next}
    found && /^##/ {found=0}
    found && NF {print; exit}
  ' "$file")

  echo "$content"
}

# Iterate through project directories
for project_dir in projects/*/; do
  # Skip if not a directory
  [[ ! -d "$project_dir" ]] && continue

  project_name=$(basename "$project_dir")
  project_md="$project_dir/project.md"

  # Check if project.md exists
  if [[ -f "$project_md" ]]; then
    # Extract project title from first H1
    title=$(grep -m 1 "^# " "$project_md" | sed 's/^# //')

    # Extract goal
    goal=$(extract_section "$project_md" "Goal")

    # Extract intent category
    intent=$(extract_section "$project_md" "Intent Category")

    # Format output
    echo "### \`$project_name\`"
    if [[ -n "$title" ]]; then
      echo "**$title**"
    fi
    if [[ -n "$goal" ]]; then
      echo "- Goal: $goal"
    fi
    if [[ -n "$intent" ]]; then
      echo "- Intent: $intent"
    fi
    echo ""
  else
    # No project.md, just show directory name
    echo "### \`$project_name\`"
    echo "- No project.md found"
    echo ""
  fi
done

exit 0
