#!/bin/bash
# Extract Metadata Hook
# Automatically extracts metadata from newly added files in /sources/
# Triggered by PostToolUse hook when Write tool creates/modifies files

set -euo pipefail

# Log file for debugging
LOG_FILE=".claude/logs/metadata-extraction.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Function to log messages
log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

# Function to convert file path to URL
path_to_url() {
  local file_path="$1"

  # Remove sources/ prefix
  local path_without_sources="${file_path#sources/}"

  # Extract domain (first path component)
  local domain=$(echo "$path_without_sources" | cut -d'/' -f1)

  # Extract path after domain, remove .md extension
  local url_path=$(echo "$path_without_sources" | cut -d'/' -f2- | sed 's/\.md$//')

  # Construct URL
  echo "https://$domain/$url_path"
}

# Function to get content map path for a file
get_content_map_path() {
  local file_path="$1"
  local parts=$(echo "$file_path" | cut -d'/' -f1-2)
  echo "$parts/_content-map.json"
}

# Function to check if URL exists in content map
url_in_content_map() {
  local url="$1"
  local content_map_path="$2"

  if [ ! -f "$content_map_path" ]; then
    return 1  # No content map = not in it
  fi

  # Check if URL exists in sitemap
  if jq -e ".sitemap[\"$url\"]" "$content_map_path" > /dev/null 2>&1; then
    return 0  # Found
  else
    return 1  # Not found
  fi
}

# Main logic
main() {
  # Read JSON from stdin (PostToolUse provides tool_input)
  local input
  input=$(cat)

  # Extract file_path from tool_input using jq
  local file_path
  file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")

  # If no file_path, exit silently
  if [ -z "$file_path" ]; then
    log "No file_path in tool_input, skipping"
    exit 0
  fi

  log "Processing file: $file_path"

  # Only process markdown files
  if [[ ! "$file_path" =~ \.md$ ]]; then
    log "Not a markdown file, skipping"
    exit 0
  fi

  # Only process files in sources/
  if [[ ! "$file_path" =~ ^sources/ ]]; then
    log "Not in sources directory, skipping"
    exit 0
  fi

  # Skip content map files themselves
  if [[ "$file_path" =~ _content-map\.json$ ]]; then
    log "Skipping content map file"
    exit 0
  fi

  # Wait briefly for file to be fully written
  sleep 0.3

  # Verify file exists
  if [ ! -f "$file_path" ]; then
    log "ERROR: File not found: $file_path"
    exit 0
  fi

  # Convert path to URL
  local url
  url=$(path_to_url "$file_path")
  log "Mapped to URL: $url"

  # Get content map path
  local content_map_path
  content_map_path=$(get_content_map_path "$file_path")
  log "Content map: $content_map_path"

  # Check if URL already in content map
  if url_in_content_map "$url" "$content_map_path"; then
    log "URL already indexed, skipping: $url"
    echo "  Skipped (already indexed): $(basename "$file_path")" >&2
    exit 0
  fi

  log "New URL detected, extracting metadata: $url"

  # Extract metadata using Python script
  local metadata_json
  if ! metadata_json=$(python3 .claude/scripts/extract_metadata.py "$file_path" 2>> "$LOG_FILE"); then
    log "ERROR: Metadata extraction failed for $file_path"
    echo "⚠️  Metadata extraction failed: $(basename "$file_path")" >&2
    exit 0  # Non-blocking
  fi

  log "Metadata extracted successfully"

  # Update content map using Python script
  local update_result
  if ! update_result=$(echo "$metadata_json" | python3 .claude/scripts/update_content_map.py - 2>> "$LOG_FILE"); then
    log "ERROR: Content map update failed for $file_path"
    echo "⚠️  Content map update failed: $(basename "$file_path")" >&2
    exit 0  # Non-blocking
  fi

  log "Content map updated successfully"

  # Extract topics and cluster from result
  local topics=$(echo "$update_result" | jq -r '.topics | join(", ")' 2>/dev/null || echo "unknown")
  local cluster=$(echo "$update_result" | jq -r '.cluster' 2>/dev/null || echo "unknown")

  # Success message
  local filename=$(basename "$file_path")
  echo "  ✓ Indexed: $filename → topics: $topics, cluster: $cluster" >&2
  log "Successfully indexed: $url → topics: $topics, cluster: $cluster"

  exit 0
}

# Run main function
main
