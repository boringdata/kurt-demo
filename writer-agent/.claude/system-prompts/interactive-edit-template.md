---
# Interactive Edit Template Metadata
template_type: interactive_edit
version: 1.0
created_date: 2025-09-25
last_updated: 2025-09-25
compatible_commands:
  - edit-content
generates_output_at: projects/[project-name]/assets/
metadata_includes:
  - original_file
  - edit_instructions
  - edit_command
  - edit_session_id
---

# Interactive Edit Template

Use this template structure when conducting interactive inline editing sessions. This guides the step-by-step change presentation and user interaction flow.

---

## Change Group Presentation Format

### Group [X] of [Total]: [Category Name]
**Priority:** [High/Medium/Low]
**Location:** [Line numbers or section name]
**Issue Type:** [Style/Clarity/Flow/Technical/Content Quality]
**Estimated Impact:** [Specific improvement expected]

---

### Current Text:
```
[Line numbers for reference]
[X]: [Original text line 1]
[X]: [Original text line 2]
[X]: [Original text line 3]
```

### Suggested Revision:
```
[Same line numbers]
[X]: [Revised text line 1] ← [Brief change note]
[X]: [Revised text line 2] ← [Brief change note]
[X]: [Revised text line 3] ← [Brief change note]
```

### Changes Explanation:
**What Changed:**
- [Change 1: Specific modification made]
- [Change 2: Specific modification made]
- [Change 3: Specific modification made]

**Why This Improves Content:**
- [Benefit 1: How this serves the target audience better]
- [Benefit 2: How this aligns with style guide/brand voice]
- [Benefit 3: How this improves engagement/clarity/conversion]

**Style Guide Alignment:**
- [Reference to specific style guide requirements this addresses]
- [Persona consideration this change reflects]

---

### User Choice Presentation:
```
Choose your action:

A) ACCEPT - Apply this change group
   → Changes will be made to lines [X-Y]
   → Continue to next group

B) MODIFY - Let me refine this suggestion
   → I'll adjust based on your feedback
   → Present alternative version

C) REJECT - Skip this change group
   → Keep original text unchanged
   → Move to next improvement opportunity

D) EXPLAIN - Tell me more about this change
   → Detailed rationale for suggestions
   → Style guide references and examples
   → Expected impact metrics

E) BATCH MODE - Show me all remaining changes
   → Preview all suggested improvements
   → Apply multiple groups at once

F) SAVE PROGRESS - Pause and resume later
   → Save current changes made
   → Generate session resume point

Your choice (A/B/C/D/E/F):
```

---

## Progress Tracking Display

### Session Progress:
```
📊 **Edit Session Status**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Groups Complete: ████████░░ 8/10 (80%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Applied: [X] groups
⏭️ Skipped: [X] groups
📝 Modified: [X] groups
🔄 Remaining: [X] groups

📈 **Quality Improvements:**
• Readability Score: [X] → [Y] (+[Z] points)
• Brand Alignment: [X]% → [Y]% (+[Z]%)
• Word Count: [original] → [current] ([+/-X] words)
• Estimated Engagement: +[X]%
```

---

## Change Category Templates

### Style & Brand Voice Changes
```
**Issue:** [Brand voice inconsistency/tone mismatch/style guide violation]
**Root Cause:** [Why current text doesn't align with guidelines]
**Fix Applied:** [How revision addresses the issue]
**Brand Alignment:** [How this reflects company personality/values]
**Audience Fit:** [How this better serves target persona]
```

### Clarity & Readability Changes
```
**Issue:** [Confusing sentence/unclear message/complex language]
**Readability Impact:** [How current text hinders comprehension]
**Simplification Strategy:** [Approach used to improve clarity]
**Persona Consideration:** [How this matches audience knowledge level]
**Engagement Benefit:** [Why clearer text improves user experience]
```

### Content Quality & Value Changes
```
**Issue:** [Weak value proposition/missing proof point/generic content]
**Content Gap:** [What value or insight was missing]
**Enhancement Added:** [Specific improvement made]
**Audience Benefit:** [How this better serves reader needs]
**Differentiation:** [How this strengthens unique positioning]
```

### Technical & SEO Changes
```
**Issue:** [SEO opportunity/broken link/weak CTA/formatting problem]
**Technical Problem:** [Specific issue affecting performance]
**Optimization Applied:** [How revision improves technical quality]
**Performance Impact:** [Expected improvement in metrics]
**User Experience:** [How this enhances reader journey]
```

---

## Batch Mode Preview Template

### Complete Change Summary:
```
📋 **All Suggested Changes Overview**

**High Priority Changes (Recommended):**
│
├─ Group 1: Opening Hook Improvement
│  └─ Impact: +25% engagement, stronger value prop
│
├─ Group 3: CTA Optimization
│  └─ Impact: +30% conversion, clearer action
│
└─ Group 5: Brand Voice Alignment
   └─ Impact: +20% brand consistency

**Medium Priority Changes (Beneficial):**
│
├─ Group 2: Technical Language Simplification
│  └─ Impact: +15% comprehension for target audience
│
└─ Group 4: Internal Link Optimization
   └─ Impact: +10% time on site, better navigation

**Low Priority Changes (Optional):**
│
└─ Group 6: Minor Grammar & Style Cleanup
   └─ Impact: +5% professional polish

**Batch Options:**
A) Apply ALL changes (Groups 1-6)
B) Apply HIGH priority only (Groups 1,3,5)
C) Apply HIGH + MEDIUM priority (Groups 1-5)
D) Custom selection - choose specific groups
E) Return to individual review
```

---

## Modification Request Handling

### When User Selects "MODIFY":
```
🔧 **Refine This Change**

Current suggestion doesn't quite fit? Let me adjust it.

**What would you like me to modify?**

A) TONE - Make it more/less [formal/casual/technical/friendly]
B) LENGTH - Make it shorter/longer/more concise
C) FOCUS - Emphasize different aspect [specify which]
D) STYLE - Different approach to same improvement
E) SCOPE - Change fewer/more elements in this group
F) CUSTOM - Specific feedback on what to adjust

**Or provide specific guidance:**
"I'd prefer if this section was more [specific direction]"
"Keep the original [specific element] but change [other element]"
"Make it sound more like [reference or example]"

Your preference:
```

---

## Session Completion Template

### Final Summary Display:
```
🎉 **Interactive Editing Session Complete!**

**📊 Session Results:**
• Duration: [X] minutes
• Groups Reviewed: [X]
• Changes Applied: [X]
• Changes Skipped: [X]
• Words Modified: [X]

**📈 Quality Improvements:**
• Overall Score: [before] → [after] (+[X]%)
• Readability: [improvement description]
• Brand Alignment: [improvement description]
• Audience Value: [improvement description]

**🔍 Key Enhancements:**
• [Enhancement 1: Most impactful change made]
• [Enhancement 2: Second most impactful change]
• [Enhancement 3: Third most impactful change]

**📝 Content Status:**
✅ Ready for: [Final review/Publishing/Stakeholder approval]
⚠️ Consider: [Any remaining recommendations]

**💾 Files Updated:**
• Content: [path to updated content file]
• Edit Log: [path to session documentation]
• Change Report: [path to detailed change summary]
```

---
*Template for interactive editing sessions*
*Supports: Accept/Reject workflow, Batch operations, Progress tracking*
*Optimized for: User control, Clear feedback, Efficient iteration*
