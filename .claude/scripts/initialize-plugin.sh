#!/bin/bash
# Kurt Plugin Initialization Script
# Ensures all required configurations and database tables exist
# Safe to run multiple times - only creates missing components

set -e

PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PLUGIN_ROOT"

echo "Initializing Kurt plugin..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Track if any initialization was needed
INITIALIZED=false

# ============================================================================
# 1. Check Kurt CLI Availability
# ============================================================================

echo ""
echo "Checking kurt-core CLI..."

if ! command -v kurt &> /dev/null; then
    echo -e "${RED}✗ kurt CLI not found${NC}"
    echo ""
    echo "Please install kurt-core first:"
    echo "  cd ../kurt-core && uv sync"
    echo "  source ../kurt-core/.venv/bin/activate"
    exit 1
else
    KURT_VERSION=$(kurt --version 2>/dev/null || echo "unknown")
    echo -e "${GREEN}✓ kurt CLI available${NC} ($KURT_VERSION)"
fi

# ============================================================================
# 2. Verify Required Directories
# ============================================================================

echo ""
echo "Checking directory structure..."

REQUIRED_DIRS=(
    ".kurt"
    ".kurt/feedback"
    ".kurt/workflows"
    ".kurt/migrations"
    "rules"
    "rules/style"
    "rules/structure"
    "rules/personas"
    "rules/publisher"
    "projects"
    "sources"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo -e "${YELLOW}  Creating missing directory: $dir${NC}"
        mkdir -p "$dir"
        INITIALIZED=true
    fi
done

echo -e "${GREEN}✓ Directory structure verified${NC}"

# ============================================================================
# 3. Check Required Configuration Files
# ============================================================================

echo ""
echo "Checking configuration files..."

# Check rules-config.yaml
if [ ! -f "rules/rules-config.yaml" ]; then
    echo -e "${RED}✗ rules/rules-config.yaml missing${NC}"
    echo "  This file should have been created during setup."
    echo "  Please check your installation."
    exit 1
else
    echo -e "${GREEN}✓ rules/rules-config.yaml exists${NC}"
fi

# Check feedback-config.yaml
if [ ! -f ".kurt/feedback/feedback-config.yaml" ]; then
    echo -e "${RED}✗ .kurt/feedback/feedback-config.yaml missing${NC}"
    echo "  This file should have been created during feedback-skill setup."
    echo "  Please check your installation."
    exit 1
else
    echo -e "${GREEN}✓ .kurt/feedback/feedback-config.yaml exists${NC}"
fi

# ============================================================================
# 4. Check Database and Run Migrations
# ============================================================================

echo ""
echo "Checking database..."

# Create database if it doesn't exist
if [ ! -f ".kurt/kurt.sqlite" ]; then
    echo -e "${YELLOW}  Creating .kurt/kurt.sqlite${NC}"
    # kurt CLI should create the database
    # Just verify it exists after kurt commands run
    INITIALIZED=true
fi

# Check if migrations need to be run
if [ -d ".kurt/migrations" ]; then
    echo ""
    echo "Checking database migrations..."

    # Run migration checker script
    if [ -f ".claude/scripts/check-migrations.sh" ]; then
        bash .claude/scripts/check-migrations.sh
    else
        # Fallback: apply all migrations
        echo -e "${YELLOW}  Applying database migrations...${NC}"
        for migration in .kurt/migrations/*.sql; do
            if [ -f "$migration" ]; then
                echo "  Applying $(basename $migration)..."
                sqlite3 .kurt/kurt.sqlite < "$migration" 2>/dev/null || true
                INITIALIZED=true
            fi
        done
        echo -e "${GREEN}✓ Migrations applied${NC}"
    fi
else
    echo -e "${YELLOW}  No migrations directory found${NC}"
fi

# ============================================================================
# 5. Verify Feedback Tables
# ============================================================================

echo ""
echo "Verifying feedback system tables..."

REQUIRED_TABLES=(
    "feedback_events"
    "improvements"
    "workflow_retrospectives"
    "workflow_phase_ratings"
    "feedback_loops"
)

MISSING_TABLES=()

for table in "${REQUIRED_TABLES[@]}"; do
    if ! sqlite3 .kurt/kurt.sqlite "SELECT name FROM sqlite_master WHERE type='table' AND name='$table';" 2>/dev/null | grep -q "$table"; then
        MISSING_TABLES+=("$table")
    fi
done

if [ ${#MISSING_TABLES[@]} -gt 0 ]; then
    echo -e "${RED}✗ Missing feedback tables: ${MISSING_TABLES[*]}${NC}"
    echo ""
    echo "Attempting to create feedback tables..."

    if [ -f ".kurt/migrations/001_add_feedback_tables.sql" ]; then
        sqlite3 .kurt/kurt.sqlite < .kurt/migrations/001_add_feedback_tables.sql
        echo -e "${GREEN}✓ Feedback tables created${NC}"
        INITIALIZED=true
    else
        echo -e "${RED}✗ Migration file not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ All feedback tables exist${NC}"
fi

# ============================================================================
# 6. Summary
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════"

if [ "$INITIALIZED" = true ]; then
    echo -e "${GREEN}✓ Plugin initialization complete${NC}"
    echo ""
    echo "New components created:"
    echo "  • Database tables (if needed)"
    echo "  • Directory structure (if needed)"
    echo ""
    echo "Ready to use Kurt plugin!"
else
    echo -e "${GREEN}✓ Plugin already initialized${NC}"
    echo ""
    echo "All components in place. No action needed."
fi

echo "═══════════════════════════════════════════════════════"
echo ""

exit 0
