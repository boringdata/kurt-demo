# Style Guidelines

This directory contains shared style guides used across all projects.

## Purpose

Style guides define:
- **Voice & Tone**: How your content sounds (technical, conversational, authoritative, etc.)
- **Terminology**: Preferred terms and phrases
- **Formatting**: Code blocks, headings, lists, emphasis
- **Examples**: Reference documents that exemplify the style

## Organization

```
style/
├── README.md (this file)
├── technical-style.md          # For docs, tutorials, guides
├── blog-conversational-style.md # For blog posts, newsletters
└── examples/                    # Reference documents
    ├── example-tutorial.md
    └── example-blog-post.md
```

## Usage

Projects reference style guides in their `project.md`:

```markdown
## Style Guidelines
- Technical style: `/style/technical-style.md`
- Examples: `/style/examples/`
```

## Future Features

- **Style extraction**: Automatically analyze documents to create style guides
- **Style validation**: Check draft content against style guidelines
- **Multiple styles**: Support for different content types and audiences
