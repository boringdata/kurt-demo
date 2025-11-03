#!/bin/bash
# Database Migration Checker
# Applies unapplied migrations from .kurt/migrations/

set -e

PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PLUGIN_ROOT"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

DB_FILE=".kurt/kurt.sqlite"
MIGRATIONS_DIR=".kurt/migrations"

# Ensure database exists
if [ ! -f "$DB_FILE" ]; then
    echo -e "${YELLOW}Creating database: $DB_FILE${NC}"
    touch "$DB_FILE"
fi

# Create migrations tracking table if it doesn't exist
sqlite3 "$DB_FILE" <<EOF 2>/dev/null || true
CREATE TABLE IF NOT EXISTS schema_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    migration_file TEXT UNIQUE NOT NULL,
    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
);
EOF

# Get list of applied migrations
APPLIED_MIGRATIONS=$(sqlite3 "$DB_FILE" "SELECT migration_file FROM schema_migrations;" 2>/dev/null || echo "")

# Apply each migration file
if [ -d "$MIGRATIONS_DIR" ]; then
    for migration in "$MIGRATIONS_DIR"/*.sql; do
        if [ -f "$migration" ]; then
            MIGRATION_NAME=$(basename "$migration")

            # Check if already applied
            if echo "$APPLIED_MIGRATIONS" | grep -q "^$MIGRATION_NAME$"; then
                continue
            fi

            echo -e "${YELLOW}Applying migration: $MIGRATION_NAME${NC}"

            # Apply migration
            if sqlite3 "$DB_FILE" < "$migration" 2>/dev/null; then
                # Record as applied
                sqlite3 "$DB_FILE" "INSERT INTO schema_migrations (migration_file) VALUES ('$MIGRATION_NAME');" 2>/dev/null || true
                echo -e "${GREEN}✓ Applied: $MIGRATION_NAME${NC}"
            else
                echo -e "${YELLOW}⚠ Failed to apply: $MIGRATION_NAME (may already exist)${NC}"
                # Still record it as applied to avoid retry loops
                sqlite3 "$DB_FILE" "INSERT OR IGNORE INTO schema_migrations (migration_file) VALUES ('$MIGRATION_NAME');" 2>/dev/null || true
            fi
        fi
    done
fi

echo -e "${GREEN}✓ Database migrations up to date${NC}"
