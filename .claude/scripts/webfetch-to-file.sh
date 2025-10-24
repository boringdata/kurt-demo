#!/bin/bash
# WebFetch to File Hook
# Automatically saves WebFetch content to /sources/ with frontmatter
# Triggered by PostToolUse hook when WebFetch tool is used

set -euo pipefail

# Log file for debugging
LOG_FILE=".claude/logs/webfetch-save.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Function to log messages
log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

# Function to convert URL to file path
# https://docs.getdbt.com/docs/build/incremental → sources/docs.getdbt.com/docs/build/incremental.md
url_to_path() {
  local url="$1"

  # Remove protocol
  local without_protocol="${url#https://}"
  without_protocol="${without_protocol#http://}"

  # Extract domain (everything before first /)
  local domain=$(echo "$without_protocol" | cut -d'/' -f1)

  # Extract path (everything after first /)
  local path=$(echo "$without_protocol" | cut -d'/' -f2-)

  # If path is empty or just domain, use index
  if [ -z "$path" ] || [ "$path" = "$domain" ]; then
    path="index"
  fi

  # Remove trailing slashes and query params
  path="${path%/}"
  path="${path%%\?*}"
  path="${path%%#*}"

  # Construct file path
  echo "sources/$domain/$path.md"
}

# Function to extract title from content
# Looks for first H1 (# Title) or falls back to domain
extract_title() {
  local content="$1"
  local url="$2"

  # Try to find first H1 heading
  local title=$(echo "$content" | grep -m 1 '^# ' | sed 's/^# //' | head -1 || echo "")

  # If no H1, try HTML title tag
  if [ -z "$title" ]; then
    title=$(echo "$content" | grep -o '<title>[^<]*</title>' | sed 's/<title>//;s/<\/title>//' | head -1 || echo "")
  fi

  # If still empty, extract from URL
  if [ -z "$title" ]; then
    # Get last path component and convert dashes/underscores to spaces
    title=$(echo "$url" | sed 's|.*/||;s|[-_]| |g' | sed 's/\.html$//')
  fi

  echo "$title"
}

# Function to extract hostname from URL
extract_hostname() {
  local url="$1"
  echo "$url" | sed -E 's|https?://||;s|/.*||'
}

# Function to extract domain (for sitename)
extract_domain() {
  local url="$1"
  local hostname=$(extract_hostname "$url")
  echo "$hostname"
}

# Main logic
main() {
  # Read JSON from stdin (PostToolUse provides tool output)
  local input
  input=$(cat)

  # Extract URL and content from tool_output using jq
  local url
  local content

  url=$(echo "$input" | jq -r '.tool_output.url // empty' 2>/dev/null || echo "")

  # Content might be in different fields depending on WebFetch output
  content=$(echo "$input" | jq -r '.tool_output.content // .tool_output.text // .tool_output.markdown // empty' 2>/dev/null || echo "")

  # If no URL or content, exit silently
  if [ -z "$url" ] || [ -z "$content" ]; then
    log "No URL or content in tool_output, skipping"
    exit 0
  fi

  log "Processing WebFetch: $url"

  # Skip if URL is obviously not content (images, etc.)
  if [[ "$url" =~ \.(jpg|jpeg|png|gif|svg|ico|pdf|zip|tar|gz)$ ]]; then
    log "Skipping non-content URL: $url"
    exit 0
  fi

  # Convert URL to file path
  local file_path
  file_path=$(url_to_path "$url")

  log "Target file path: $file_path"

  # Create directory if needed
  local dir_path=$(dirname "$file_path")
  mkdir -p "$dir_path"

  # Extract metadata
  local title=$(extract_title "$content" "$url")
  local hostname=$(extract_hostname "$url")
  local domain=$(extract_domain "$url")
  local date=$(date +'%Y-%m-%d')

  # Construct frontmatter
  local frontmatter="---
title: $title
url: $url
hostname: $hostname
sitename: $domain
date: $date
---

"

  # Check if content already has frontmatter
  if [[ "$content" =~ ^---.*---.*$ ]]; then
    # Content already has frontmatter, use as-is
    echo "$content" > "$file_path"
    log "Saved (with existing frontmatter): $file_path"
  else
    # Add our frontmatter
    echo "${frontmatter}${content}" > "$file_path"
    log "Saved (with generated frontmatter): $file_path"
  fi

  # Log success
  local filename=$(basename "$file_path")
  echo "✓ Saved: $filename → $file_path" >&2
  log "Successfully saved: $url → $file_path"

  exit 0
}

# Run main function
main
