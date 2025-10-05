# Aphorisms Refactoring Summary

## Problem
The aphorisms in `/src/content/aphorisms` were duplicated in two places:
1. In the frontmatter `description` field
2. In the markdown body (with a duplicate h1 heading)

This duplication was unnecessary and made editing harder.

## Solution

### 1. Updated Content Schema
Modified `/src/content.config.ts` to make the `description` field optional:
- Changed `description: z.string()` to `description: z.string().optional()`
- The description field can now be omitted, and if present, will only be used for SEO meta descriptions

### 2. Updated Template to Use Body Content
Modified `/src/pages/aphorisms/[slug].astro` to:
- Render the markdown body content instead of the description field
- Use `marked.parse(currentAphorism.body)` to convert markdown to HTML
- Fall back to the body content for meta descriptions if no explicit description is provided
- Pass aphorism data through props as plain objects (since Content Collection entries can't be serialized with their `render()` method)

### 3. Cleaned Up All Aphorism Files
Created `/scripts/fix_aphorisms.py` to:
- Remove the `description` field from frontmatter
- Remove duplicate h1 headings from the body
- Process all 26 aphorism files automatically

## Result
Now aphorism files only need the content written once in the body:

```markdown
---
title: "Why, then what, then how"
order: 1
icon: "💡"
references:
  - title: "Start with Why"
    url: "https://example.com"
---

Context in organizations is hard: people know their local priorities...
```

## Tools
- `/scripts/fix_aphorisms.py` - Script to clean up aphorism files (can be used for future batch edits)

## Benefits
1. **No duplication** - Content only exists in one place
2. **Easier editing** - Just edit the markdown body
3. **Cleaner frontmatter** - Only essential metadata
4. **Backward compatible** - Description field still works if present (used for SEO meta description)
