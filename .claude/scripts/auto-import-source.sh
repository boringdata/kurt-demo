#!/bin/bash
# Auto-Import Source Files to Kurt Database
# Triggered by PostToolUse hook when Write tool creates markdown files in sources/

set -euo pipefail

# Log file for debugging
LOG_FILE=".claude/logs/auto-import.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Function to log messages
log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

# Function to convert file path to URL
# sources/docs.getdbt.com/path/file.md → https://docs.getdbt.com/path/file
path_to_url() {
  local file_path="$1"

  # Remove sources/ prefix
  local path_without_sources="${file_path#sources/}"

  # Extract domain (first path component)
  local domain=$(echo "$path_without_sources" | cut -d'/' -f1)

  # Extract path after domain
  local url_path=$(echo "$path_without_sources" | cut -d'/' -f2- | sed 's/\.md$//')

  # Construct URL
  echo "https://$domain/$url_path"
}

# Function to find ERROR record by URL
find_error_record() {
  local url="$1"

  # Query Kurt database for ERROR record matching this URL
  local doc_id=$(kurt document list --url-prefix "$url" 2>/dev/null | \
    grep -i "ERROR" | \
    head -1 | \
    awk '{print $1}' | \
    tr -d '…')

  echo "$doc_id"
}

# Function to retry command with exponential backoff
retry_command() {
  local max_attempts=3
  local delay=2
  local attempt=1
  local command="$*"

  while [ $attempt -le $max_attempts ]; do
    log "Attempt $attempt/$max_attempts: $command"

    if eval "$command" 2>> "$LOG_FILE"; then
      return 0
    fi

    if [ $attempt -lt $max_attempts ]; then
      log "Failed, retrying in ${delay}s..."
      sleep $delay
      delay=$((delay * 2))
    fi

    attempt=$((attempt + 1))
  done

  log "Command failed after $max_attempts attempts"
  return 1
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

  # Only process files in sources/ or projects/*/sources/
  if [[ ! "$file_path" =~ ^sources/ ]] && [[ ! "$file_path" =~ ^projects/.*/sources/ ]]; then
    log "Not in sources directory, skipping"
    exit 0
  fi

  # Check if Kurt is installed
  if ! command -v kurt &> /dev/null; then
    log "ERROR: Kurt CLI not found"
    echo "⚠️  Kurt CLI not installed - skipping auto-import" >&2
    exit 0  # Non-blocking error
  fi

  # Wait briefly for file to be fully written
  sleep 0.5

  # Verify file exists
  if [ ! -f "$file_path" ]; then
    log "ERROR: File not found: $file_path"
    exit 0
  fi

  # Convert path to URL
  local url
  url=$(path_to_url "$file_path")
  log "Mapped to URL: $url"

  # Find ERROR record for this URL
  local doc_id
  doc_id=$(find_error_record "$url")

  if [ -z "$doc_id" ]; then
    log "No ERROR record found for URL: $url (this is OK, might be new file)"
    exit 0
  fi

  log "Found ERROR record: $doc_id"

  # Run Python import script with retry
  if ! retry_command "python .claude/scripts/import_markdown.py --document-id '$doc_id' --file-path '$file_path'"; then
    log "ERROR: Failed to import after retries"
    echo "⚠️  Auto-import failed for $(basename "$file_path") - see .claude/logs/auto-import.log" >&2
    exit 0  # Non-blocking
  fi

  log "Successfully updated database record"

  # Extract metadata with retry
  if ! retry_command "kurt index '$doc_id' > /dev/null 2>&1"; then
    log "WARNING: Metadata extraction failed (non-fatal)"
    echo "✓ Auto-imported: $(basename "$file_path") → Kurt DB (metadata extraction pending)" >&2
    exit 0
  fi

  log "Successfully extracted metadata"

  # Success message
  local filename
  filename=$(basename "$file_path")
  echo "✓ Auto-imported: $filename → Kurt DB" >&2

  exit 0
}

# Run main function
main

