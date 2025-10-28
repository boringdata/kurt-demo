# Iterative Source Gathering

This shared module provides an iterative, collaborative workflow for gathering sources with the user.

## Why Iterative?

Source gathering is exploratory and requires user validation:
- Users may not know exact URLs or search terms upfront
- Preview helps users decide if sources are relevant before fetching
- Review helps users evaluate if they need more/different sources
- Conversational exploration for research prevents wasted API calls

## Pattern: Two-Checkpoint Loop

```
┌─────────────────────────────────────────────────────┐
│ User describes what sources they need               │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ CHECKPOINT 1: Proposal & Preview                    │
│ - Parse description → specific actions              │
│ - Show what will be fetched                         │
│ - User approves/refines/cancels                     │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ EXECUTION                                           │
│ - Run approved actions                              │
│ - Show progress                                     │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ CHECKPOINT 2: Review & Iterate                      │
│ - Show what was fetched                             │
│ - Offer: Add more / Refine / Continue               │
└─────────────────────────────────────────────────────┘
                       ↓
              Loop back or continue
```

---

## Step 1: User Describes Sources

Ask the user to describe what sources they need:

```
**What sources would be helpful for this project?**

Available source types:

1. **Web Content (URLs/Websites)**
   - Individual URLs or entire websites
   - Example: "docs.example.com/features" or "blog.company.com"

2. **CMS Content**
   - Sanity (if configured)
   - Example: "existing tutorials about authentication"

3. **Local Content**
   - Files, transcripts, notes
   - Example: "conversation transcript from customer research"

4. **Research Content** (if available)
   - Perplexity, web search, etc.
   - Example: "research what Auth0 and Okta are doing for authentication"

Describe the sources you need:
```

**Wait for user's response.**

---

## Step 2: CHECKPOINT 1 - Proposal & Preview

Parse the user's description and propose specific actions **before executing**.

### 2.1: Identify Source Types

Analyze user's description:
- **URLs mentioned** → Web content
- **"from Sanity" / "CMS" / "existing content"** → CMS
- **"transcript" / "notes" / "paste"** → Local files
- **"research" / "what are competitors"** → Research

### 2.2: Propose Actions for Each Source Type

#### For Web Content (URLs/Websites)

**If user provided specific URLs:**
```
I'll fetch these URLs:
1. docs.example.com/features
2. docs.example.com/guides
3. blog.company.com/post-about-auth

Action:
- Map each URL to discover any linked pages
- Fetch content to /sources/
- Index for metadata extraction

Estimated: ~10-50 pages depending on site structure

Proceed with these URLs? Or refine?
```

**If user provided a domain:**
```
I'll map the entire domain: docs.example.com

Action:
- Discover all URLs via sitemap
- Show you what's found before fetching
- You select which sections to fetch

This is a discovery step only. No fetching yet.

Proceed with mapping? (Y/n)
```

#### For CMS Content

**Prerequisites check:**
```bash
test -f .kurt/cms-config.json && echo "✓ Sanity configured" || echo "✗ Need cms-interaction onboard first"
```

**If configured, propose search:**
```
I'll search your CMS for: [interpreted query]

Proposed search:
- Content type: article
- Query: "authentication"
- Filter: tags contains "tutorial"

This will show results for you to review before fetching.

Proceed with this search? Or refine query?
```

#### For Research Content

**Use conversational exploration** (most important for research):

```
You mentioned researching: "what Auth0 and Okta are doing for authentication"

Let's refine this together before using API calls:

**What aspects should I focus on?**
- Their authentication flows and features?
- Their documentation and explanation style?
- Their pricing and positioning?
- Their developer experience?

Please specify, or I can start broad and we'll narrow down.
```

**Continue conversation until query is refined:**

User: "Their documentation style"

```
Good! So I'll research their documentation writing patterns.

**Any specific aspects of documentation?**
- How they explain complex concepts?
- Their use of examples and tutorials?
- Tone and voice characteristics?
- Structure and organization patterns?

Or should I cover all of these?
```

User: "All of those, and compare the two"

```
Perfect! I'll research:

**Query**: "Auth0 vs Okta documentation writing patterns: concept explanation, examples, tone, and structure"

**Expected outcome**: Comparison of how both companies approach documentation, covering explanation style, tutorial structure, voice, and organization

This will use Perplexity API (~1 query).

Ready to execute this research? (Y/n)
```

**Wait for explicit approval before API call.**

#### For Local Content

```
You mentioned: [pasted content / file]

I'll save this to: projects/<project-name>/sources/<descriptive-name>.md

Suggested filename: customer-research-transcript.md

Approve filename, or provide different name:
```

### 2.3: Get User Approval/Refinement

For each proposed action, wait for user response:
- **Approve**: "Yes, proceed"
- **Refine**: User provides corrections/adjustments → loop back to proposal
- **Cancel**: Skip this source type

---

## Step 3: EXECUTION

Execute only the approved actions.

### For Web Content (URLs)

#### If specific URLs:
```bash
# Fetch approved URLs
for url in "${approved_urls[@]}"; do
  echo "Fetching: $url"
  kurt ingest map "$url" --discover-dates
  kurt ingest fetch --url "$url"
  kurt index --url "$url"
done
```

#### If domain mapping:
```bash
# Map domain to discover URLs
kurt ingest map https://docs.example.com --discover-dates

# Show discovered URLs
echo "Discovered URLs:"
kurt document list --url-prefix https://docs.example.com --status NOT_FETCHED | head -20

# Ask user which to fetch
echo "Found X URLs. Fetch all, or select specific paths?"
```

**Show progress:**
```
✓ Mapped docs.example.com (45 URLs discovered)
✓ Fetched 45 pages
✓ Indexed 45 pages
```

### For CMS Content

```bash
# Execute approved search
cms-interaction search --query "${approved_query}" --content-type ${content_type} --output json > search-results.json

# Show preview
echo "Search found X results:"
cat search-results.json | jq -r '.[] | "\(.title) (\(.published_date))"' | head -10

# Ask user which to fetch
echo "Fetch all X results, or select specific ones?"
```

If user approves all:
```bash
# Fetch from search results
cat search-results.json | cms-interaction fetch --from-stdin

# Import to Kurt
cms-interaction import --source-dir sources/cms/sanity/
```

**Show progress:**
```
✓ Searched CMS (12 results)
✓ Fetched 12 documents
✓ Imported to Kurt database
```

### For Research Content

```bash
# Execute approved research query
kurt research search "${approved_query}" --recency day --save
```

**Show progress:**
```
✓ Research complete
✓ Saved to: sources/research/2025-10-28-auth0-vs-okta-documentation.md
✓ Found 15 citations
```

### For Local Content

```bash
# Save to project sources
cat > "projects/<project-name>/sources/${approved_filename}.md" <<EOF
${user_content}
EOF

# Optionally import to Kurt
kurt ingest add "file://projects/<project-name>/sources/${approved_filename}.md"
python .claude/scripts/import_markdown.py --file-path "projects/<project-name>/sources/${approved_filename}.md"
kurt index "file://projects/<project-name>/sources/${approved_filename}.md"
```

**Show progress:**
```
✓ Saved to: projects/<project-name>/sources/customer-research.md
✓ Imported to Kurt database
```

---

## Step 4: CHECKPOINT 2 - Review & Iterate

After execution, show what was fetched and offer continuation options.

### 4.1: Show Summary

```
**Sources Fetched**

Web Content:
✓ docs.example.com (45 pages)
  - Topics: authentication, APIs, deployment
  - Date range: 2023-01 to 2024-10

CMS Content:
✓ Sanity articles (12 documents)
  - Content type: article
  - Tags: tutorial, authentication
  - Date range: 2024-06 to 2024-10

Research:
✓ Auth0 vs Okta documentation patterns
  - Saved: sources/research/2025-10-28-auth0-vs-okta-documentation.md
  - 15 citations from official docs and analysis articles

Local:
✓ Customer research transcript
  - Saved: projects/<project-name>/sources/customer-research.md

Total: 58 sources added to project
```

### 4.2: Offer Continuation Options

```
**What would you like to do next?**

a) **Add more sources** - Describe additional sources to fetch
b) **Refine existing sources** - Adjust what was fetched (re-fetch, filter, expand)
c) **Continue to next step** - Move on (extract rules or identify targets)

Choose (a/b/c):
```

**Wait for user response.**

### 4.3: Handle User Choice

**If (a) - Add more sources:**
- Return to Step 1 (user describes more sources)
- Follow same Proposal → Execution → Review loop

**If (b) - Refine existing sources:**
```
Which sources do you want to refine?

1. Web content (docs.example.com) - fetch more pages, or narrow scope?
2. CMS content (Sanity articles) - different search query or filters?
3. Research - follow-up query on specific aspect?
4. Local content - add more files?

Select number(s) or describe refinement:
```

Then return to Step 2 (Proposal & Preview) for refined actions.

**If (c) - Continue:**
- Update project.md with source list
- Continue to next phase (rule extraction or target identification)
- Remind user: "You can always add more sources later using project-management-skill"

---

## Integration with Commands

### In `/create-project` Step 3:

```markdown
## Step 3: Collect Ground Truth Sources (Skippable)

Ask if user has sources to add:
> Do you have ground truth sources (material you'll work FROM)?
> a) Add sources now
> b) Skip for now (add later)

**If (a) - Add sources now:**

Follow the complete iterative workflow in:
`.claude/commands/_shared/iterative-source-gathering.md`

This will guide through:
1. User describes sources
2. CHECKPOINT 1: Proposal & preview actions
3. Execute approved actions
4. CHECKPOINT 2: Review & iterate
5. Continue when user is satisfied

**If (b) - Skip:**
- Continue to Step 4
```

### In `/resume-project` (via project-management-skill):

When user wants to add sources to existing project, use same module.

---

## Error Handling

### URL not accessible
```
⚠️ Could not fetch: docs.example.com/page

Possible issues:
- URL not accessible
- Authentication required
- Network error

Try:
1. Check URL is correct
2. Verify network access
3. Skip this URL for now

Continue with remaining URLs? (Y/n)
```

### CMS search returns no results
```
⚠️ CMS search found 0 results

Query: "authentication tutorials"

Try:
1. Broaden search: "authentication"
2. Different content type
3. Check different tags/filters
4. Skip CMS sources for now

Refine search or skip? (refine/skip)
```

### Research API error
```
⚠️ Research API error

Possible issues:
- API rate limit
- Network error
- API key issue

Try:
1. Wait and retry
2. Use different research source
3. Skip research for now

What would you like to do?
```

---

## Key Design Principles

1. **Two checkpoints**: Proposal (before execution) + Review (after execution)
2. **Conversational for research**: Refine queries through dialogue before API calls
3. **Progressive disclosure**: Show only relevant options at each step
4. **Non-blocking**: User can skip any source type
5. **Explicit continuation**: User chooses when to stop iterating
6. **Visibility**: Always show what will happen before it happens
7. **Reversibility**: Can refine after seeing results

---

*This module is referenced by `/create-project` Step 3 and `project-management-skill` for adding sources to existing projects.*
