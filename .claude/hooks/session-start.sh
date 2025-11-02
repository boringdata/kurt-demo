#!/bin/bash
# Session start hook for Kurt analytics auto-sync
#
# This hook checks if analytics data is stale and prompts user to sync.
# Runs automatically when Claude Code session starts.

# Check if analytics is configured
ANALYTICS_DOMAINS=$(kurt analytics list --format json 2>/dev/null)

if [ -z "$ANALYTICS_DOMAINS" ] || [ "$ANALYTICS_DOMAINS" = "[]" ]; then
  # No analytics configured, skip silently
  exit 0
fi

# Check for stale analytics data (>7 days since last sync)
STALE_DOMAINS=$(echo "$ANALYTICS_DOMAINS" | jq -r '.[] | select(.days_since_sync > 7) | .domain' 2>/dev/null)

if [ -z "$STALE_DOMAINS" ]; then
  # All domains are up to date
  exit 0
fi

# Count stale domains
STALE_COUNT=$(echo "$STALE_DOMAINS" | wc -l | tr -d ' ')

if [ "$STALE_COUNT" -eq 0 ]; then
  exit 0
fi

# Show stale analytics warning
echo ""
echo "📊 Analytics data is stale for $STALE_COUNT domain(s):"
echo ""

# List stale domains with days
echo "$ANALYTICS_DOMAINS" | jq -r '.[] | select(.days_since_sync > 7) | "  - \(.domain) (\(.days_since_sync) days old)"' 2>/dev/null

echo ""
echo "Sync now? (recommended for accurate content prioritization)"
echo ""
echo "a) Yes, sync all stale domains"
echo "b) Skip for now"
echo ""

# Note: In Claude Code, this will be handled by Claude's question/answer flow
# The hook output will be shown to the user via Claude
# For now, we just show the info and let Claude handle the interaction

exit 0
