#!/usr/bin/env python3
"""
Interactive CMS onboarding script.

Discovers content types and guides user through field mapping configuration.

Usage:
    python cms_onboard.py --cms sanity
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add adapters to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'adapters'))

from base import CMSAdapter


def load_config(cms_name: str) -> dict:
    """Load CMS configuration."""
    config_path = Path.home() / 'code' / 'kurt-demo' / '.claude' / 'scripts' / 'cms-config.json'

    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}", file=sys.stderr)
        print("\nCreate basic configuration first:", file=sys.stderr)
        print(f"  cp .claude/skills/cms-interaction-skill/adapters/{cms_name}/config.json.example \\", file=sys.stderr)
        print(f"     .claude/scripts/cms-config.json", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    if cms_name not in config:
        print(f"Error: No configuration found for CMS '{cms_name}'", file=sys.stderr)
        sys.exit(1)

    return config, config_path


def save_config(config: dict, config_path: Path):
    """Save updated configuration."""
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"\n✓ Configuration saved to: {config_path}")


def get_adapter(cms_name: str, config: dict) -> CMSAdapter:
    """Load and initialize CMS adapter."""
    if cms_name == 'sanity':
        from sanity.adapter import SanityAdapter
        return SanityAdapter(config)
    else:
        print(f"Error: Onboarding not yet implemented for '{cms_name}'", file=sys.stderr)
        sys.exit(1)


def print_header(text: str):
    """Print section header."""
    print(f"\n{'='*60}")
    print(text)
    print('='*60)


def print_dict(data: dict, indent: int = 0):
    """Pretty print dictionary."""
    spacing = "  " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"{spacing}{key}:")
            print_dict(value, indent + 1)
        elif isinstance(value, list):
            print(f"{spacing}{key}: {value}")
        else:
            print(f"{spacing}{key}: {value}")


def select_content_types(adapter: CMSAdapter) -> List[str]:
    """Interactive content type selection."""
    print_header("Content Type Discovery")

    print("Discovering content types...")
    types = adapter.get_content_types()

    print(f"\nFound {len(types)} content types:\n")
    print(f"{'ID':>4}  {'Type':<20} {'Documents':>10}")
    print(f"{'--':>4}  {'----':<20} {'---------':>10}")

    for idx, type_info in enumerate(types, 1):
        print(f"{idx:>4}  {type_info['name']:<20} {type_info['count']:>10}")

    while True:
        print("\nWhich content types contain content you want to work with?")
        print("Options:")
        print("  - Enter numbers (comma-separated): 1,2,5")
        print("  - Type 'preview X' to see example of type X")
        print("  - Type 'all' to select all types")
        print("  - Type 'quit' to exit")

        selection = input("\nYour selection: ").strip()

        if selection.lower() == 'quit':
            sys.exit(0)

        if selection.lower() == 'all':
            return [t['name'] for t in types]

        if selection.lower().startswith('preview '):
            try:
                idx = int(selection.split()[1])
                if 1 <= idx <= len(types):
                    preview_content_type(adapter, types[idx - 1]['name'])
                else:
                    print(f"Invalid index: {idx}")
            except (ValueError, IndexError):
                print("Invalid preview command. Use: preview X")
            continue

        # Parse selection
        try:
            indices = [int(x.strip()) for x in selection.split(',')]
            if all(1 <= idx <= len(types) for idx in indices):
                selected_types = [types[idx - 1]['name'] for idx in indices]
                print(f"\n✓ Selected {len(selected_types)} types: {', '.join(selected_types)}")
                return selected_types
            else:
                print("Invalid selection. Numbers must be in range.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")


def preview_content_type(adapter: CMSAdapter, content_type: str):
    """Show example document for content type."""
    print_header(f"Preview: {content_type}")

    try:
        example = adapter.get_example_document(content_type)
        print("\nExample document structure:")
        print(json.dumps(example, indent=2))
    except Exception as e:
        print(f"Error fetching example: {e}")


def configure_content_type(adapter: CMSAdapter, content_type: str) -> Dict[str, Any]:
    """Interactive configuration for a content type."""
    print_header(f"Configuring: {content_type}")

    # Get example document
    try:
        example = adapter.get_example_document(content_type)
    except Exception as e:
        print(f"Warning: Could not fetch example: {e}")
        example = {}

    print("\nExample document:")
    print(json.dumps(example, indent=2, default=str)[:1000] + "...\n")

    config = {"enabled": True}

    # Content field
    print("1. CONTENT FIELD")
    print("   Which field contains the main content to extract?")
    default_content = "body"
    content_field = input(f"   Content field [{default_content}]: ").strip() or default_content
    config['content_field'] = content_field

    # Title field
    print("\n2. TITLE FIELD")
    print("   Which field should be used as the document title?")
    default_title = "title"
    title_field = input(f"   Title field [{default_title}]: ").strip() or default_title
    config['title_field'] = title_field

    # Slug field
    print("\n3. SLUG FIELD")
    print("   Which field contains the URL slug?")
    default_slug = "slug.current"
    slug_field = input(f"   Slug field [{default_slug}]: ").strip() or default_slug
    config['slug_field'] = slug_field

    # Metadata fields
    print("\n4. METADATA FIELDS")
    print("   Enter field names to include as metadata (comma-separated).")
    print("   Common fields: author, publishedAt, _updatedAt, tags, categories")
    print("   Or type 'none' to skip metadata")

    metadata_input = input("\n   Metadata fields: ").strip()

    if metadata_input.lower() != 'none' and metadata_input:
        metadata_fields = {}
        fields = [f.strip() for f in metadata_input.split(',')]

        for field in fields:
            # Ask about reference resolution if field looks like a reference
            if 'author' in field.lower() or 'category' in field.lower() or 'categories' in field.lower():
                print(f"\n   How should '{field}' be resolved?")
                print(f"     a) Use as-is: {field}")
                print(f"     b) Resolve reference: {field}->name")
                print(f"     c) Resolve reference: {field}->title")
                print(f"     d) Custom path")

                choice = input(f"   Choice [a]: ").strip().lower() or 'a'

                if choice == 'b':
                    field_path = f"{field}->name"
                elif choice == 'c':
                    field_path = f"{field}->title"
                elif choice == 'd':
                    field_path = input(f"   Custom path: ").strip()
                else:
                    field_path = field

                # Map to standard metadata names
                if 'author' in field.lower():
                    metadata_fields['author'] = field_path
                elif 'published' in field.lower() or 'date' in field.lower():
                    metadata_fields['published_date'] = field_path
                elif 'updated' in field.lower() or 'modified' in field.lower():
                    metadata_fields['last_modified'] = field_path
                elif 'tag' in field.lower():
                    metadata_fields['tags'] = f"{field}[]" if not field.endswith('[]') else field
                elif 'categor' in field.lower():
                    metadata_fields['categories'] = field_path
                    # Add array notation if missing
                    if not '[]' in metadata_fields['categories']:
                        metadata_fields['categories'] = metadata_fields['categories'].replace(field, f"{field}[]")
                else:
                    # Use field name as-is
                    metadata_fields[field] = field
            else:
                # Simple field
                metadata_fields[field] = field

        config['metadata_fields'] = metadata_fields

    print("\n✓ Configuration complete!")
    print("\nSummary:")
    print_dict(config, indent=1)

    return config


def validate_configuration(adapter: CMSAdapter, mappings: Dict[str, Any]) -> bool:
    """Validate configuration with real data."""
    print_header("Validating Configuration")

    all_valid = True

    for content_type, config in mappings.items():
        if not config.get('enabled', True):
            continue

        print(f"\nValidating: {content_type}")

        try:
            # Fetch sample document
            example = adapter.get_example_document(content_type)

            # Check content field
            content_field = config.get('content_field', 'body')
            if not check_field_exists(example, content_field):
                print(f"  ✗ Content field '{content_field}' not found")
                all_valid = False
            else:
                print(f"  ✓ Content field '{content_field}' exists")

            # Check title field
            title_field = config.get('title_field', 'title')
            if not check_field_exists(example, title_field):
                print(f"  ⚠ Title field '{title_field}' not found")
            else:
                print(f"  ✓ Title field '{title_field}' exists")

            # Check slug field
            slug_field = config.get('slug_field', 'slug')
            if not check_field_exists(example, slug_field):
                print(f"  ⚠ Slug field '{slug_field}' not found or null")
            else:
                print(f"  ✓ Slug field '{slug_field}' exists")

            # Check metadata fields
            metadata_fields = config.get('metadata_fields', {})
            for key, field_path in metadata_fields.items():
                # Simplified check (doesn't resolve references)
                base_field = field_path.split('->')[0].split('.')[0].replace('[]', '')
                if not check_field_exists(example, base_field):
                    print(f"  ⚠ Metadata field '{field_path}' may not exist")
                else:
                    print(f"  ✓ Metadata field '{field_path}' accessible")

        except Exception as e:
            print(f"  ✗ Validation error: {e}")
            all_valid = False

    return all_valid


def check_field_exists(data: dict, field_path: str) -> bool:
    """Check if a field path exists in data."""
    # Remove reference syntax and array syntax for basic check
    field_path = field_path.split('->')[0].replace('[]', '')

    parts = field_path.split('.')
    current = data

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False

    return current is not None


def main():
    parser = argparse.ArgumentParser(
        description='Interactive CMS onboarding',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run interactive onboarding
  python cms_onboard.py --cms sanity

  # Validate existing configuration
  python cms_onboard.py --cms sanity --validate-only
        """
    )

    parser.add_argument(
        '--cms',
        required=True,
        choices=['sanity'],
        help='CMS to configure'
    )

    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate existing configuration'
    )

    args = parser.parse_args()

    # Load configuration
    config, config_path = load_config(args.cms)

    # Initialize adapter
    try:
        adapter = get_adapter(args.cms, config[args.cms])
    except Exception as e:
        print(f"Error initializing {args.cms} adapter: {e}", file=sys.stderr)
        sys.exit(1)

    # Test connection
    print("Testing connection...")
    if not adapter.test_connection():
        print("✗ Connection failed", file=sys.stderr)
        sys.exit(1)
    print("✓ Connection successful")

    # Validate-only mode
    if args.validate_only:
        mappings = config[args.cms].get('content_type_mappings', {})
        if not mappings:
            print("No content type mappings found in configuration")
            sys.exit(1)

        valid = validate_configuration(adapter, mappings)
        if valid:
            print("\n✓ All validations passed")
            sys.exit(0)
        else:
            print("\n✗ Some validations failed")
            sys.exit(1)

    # Interactive onboarding
    print("\nWelcome to CMS Onboarding!")
    print("This will help you configure content types and field mappings.\n")

    # Get existing mappings
    existing_mappings = config[args.cms].get('content_type_mappings', {})

    # Select content types
    selected_types = select_content_types(adapter)

    if not selected_types:
        print("No content types selected. Exiting.")
        sys.exit(0)

    # Configure each type
    new_mappings = {}

    for content_type in selected_types:
        # Use existing config if available
        if content_type in existing_mappings:
            print(f"\n'{content_type}' already configured.")
            print("Existing configuration:")
            print_dict(existing_mappings[content_type], indent=1)

            reconfigure = input("\nReconfigure? (y/n) [n]: ").strip().lower()
            if reconfigure != 'y':
                new_mappings[content_type] = existing_mappings[content_type]
                continue

        # Configure type
        new_mappings[content_type] = configure_content_type(adapter, content_type)

    # Preserve disabled types from existing config
    for content_type, mapping in existing_mappings.items():
        if content_type not in new_mappings and not mapping.get('enabled', True):
            new_mappings[content_type] = mapping

    # Validate configuration
    print("\n")
    valid = validate_configuration(adapter, new_mappings)

    if not valid:
        print("\n⚠ Some validations failed. Configuration may not work correctly.")
        proceed = input("Save configuration anyway? (y/n) [y]: ").strip().lower()
        if proceed == 'n':
            print("Configuration not saved.")
            sys.exit(1)

    # Save configuration
    config[args.cms]['content_type_mappings'] = new_mappings
    save_config(config, config_path)

    # Summary
    print_header("Onboarding Complete")
    print(f"\nConfigured {len([m for m in new_mappings.values() if m.get('enabled', True)])} content types:")
    for content_type, mapping in new_mappings.items():
        if mapping.get('enabled', True):
            print(f"  ✓ {content_type}")

    print("\nYou can now use:")
    print("  - cms-search-skill (searches configured types)")
    print("  - cms-fetch-skill (extracts using field mappings)")
    print("  - cms-import-skill (imports with mapped metadata)")
    print("  - cms-publish-skill (publishes to mapped fields)")

    print("\nTo reconfigure or add content types, run this script again.")


if __name__ == '__main__':
    main()
