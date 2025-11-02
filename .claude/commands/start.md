# Start Command

**Purpose:** One-time team onboarding and setup
**Invokes:** onboarding-skill
**Output:** `.kurt/profile.md` + foundation rules

---

## Usage

```bash
/start              # Full interactive onboarding
/start --continue   # Resume incomplete onboarding
/start --minimal    # Skip optional steps
/start --update     # Update existing profile
```

---

## What This Command Does

The `/start` command guides you through Kurt's initial setup:

1. **Capture team context** - Company, goals, content types, personas
2. **Map content sources** - Your website, docs, research sources
3. **Extract foundation rules** - Company profile, style guide, personas
4. **Create team profile** - Centralized setup in `.kurt/profile.md`
5. **Suggest next steps** - Personalized based on your setup

**Time:** 10-15 minutes for full setup

**Adaptive:** You can skip any question - Kurt adapts to what you know

---

## When to Use This Command

**First time using Kurt:**
- Run `/start` to set up your team profile and foundation

**Already have a profile:**
- Run `/start --update` to refresh your profile
- Run `/start --continue` if you have an incomplete setup

**Quick setup without rules extraction:**
- Run `/start --minimal` to create profile only

---

## What Gets Created

After running `/start`, you'll have:

**Profile:**
- `.kurt/profile.md` - Your team's setup and configuration

**Foundation Rules:**
- `rules/publisher/publisher-profile.md` - Your company context
- `rules/style/*.md` - Your writing style guides
- `rules/personas/*.md` - Your target audience profiles

**Indexed Content:**
- Content from your website/sources mapped and indexed
- Ready for analysis and rule extraction

---

## Next Steps After `/start`

Once setup is complete, you can:

1. **Define workflows** - Codify recurring project patterns
   ```
   workflow-skill add
   ```

2. **Create projects** - Start your first content project
   ```
   /create-project
   ```

3. **Extract more rules** - Add structure templates, custom rule types
   ```
   writing-rules-skill structure --type tutorial --auto-discover
   ```

---

## Integration

This command invokes the onboarding-skill, which:
- Guides you through interactive questionnaire
- Calls `kurt map` and `kurt fetch` for content
- Calls `writing-rules-skill` for rule extraction
- Creates and maintains `.kurt/profile.md`

---

Invoke: onboarding-skill
