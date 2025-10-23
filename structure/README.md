# Structure Templates

This directory contains shared document templates and structural patterns used across all projects.

## Purpose

Structure templates define:
- **Document Patterns**: Common section ordering (H1 > Prerequisites > Steps > Next Steps)
- **Templates**: Reusable outlines for different content types
- **Sections**: Required vs optional sections for each content type

## Organization

```
structure/
├── README.md (this file)
├── templates/
│   ├── tutorial-template.md      # Step-by-step guides
│   ├── api-reference-template.md # API documentation
│   ├── blog-post-template.md     # Blog content
│   └── guide-template.md         # Conceptual guides
└── patterns/
    └── analysis-notes.md         # Notes from pattern analysis
```

## Usage

Projects reference templates in their `project.md`:

```markdown
## Structure Templates
- Tutorial template: `/structure/templates/tutorial-template.md`
- Based on analysis of 12 existing tutorials
```

## Future Features

- **Structure extraction**: Analyze multiple documents to find common patterns
- **Template generation**: Create reusable templates from patterns
- **Structure validation**: Check if draft content follows template structure
