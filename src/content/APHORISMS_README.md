# Aphorisms Management

This directory contains the aphorisms displayed on the website's wisdom cards section.

## Remaining todos
1. Incorporate all my aphorisms from https://docs.google.com/document/d/1TWSuSfHaunXeJk2G5bzJC24G0Ljmndlr3K7tInsKX6w/edit?tab=t.0

## Completed Features
- ✅ **URL-based navigation**: Each aphorism card is referenceable by a unique URL
  - Format: `/aphorisms/{order-padded}-{title-slug}`
  - Example: `/aphorisms/01-who-should-do-what-differently-be-specific`
  - Base URL `/aphorisms` redirects to the first aphorism
  - URLs are shareable and bookmarkable
  - Browser back/forward navigation works seamlessly


## Adding New Aphorisms

1. Create a new `.md` file in this directory
2. Use the naming convention: `##-descriptive-name.md` (e.g., `06-new-aphorism.md`)
3. Include the required frontmatter:

```markdown
---
title: "Your Aphorism Title"
order: 6
icon: "🎯"
description: "A paragraph explaining the aphorism in detail. This will appear below the title on the card."
references:
  - title: "Book or Article Title"
    url: "https://example.com/reference"
    author: "Author Name"
  - title: "Another Reference"
    url: "https://example.com/another-reference"
    author: "Another Author"
---

# Your Aphorism Title

A paragraph explaining the aphorism in detail. This will appear below the title on the card.
```

## Frontmatter Fields

- `title`: The main aphorism text (displayed prominently on the card)
- `order`: Number for ordering (determines display sequence)
- `icon`: Emoji or symbol to display above the title (optional, defaults to 💡)
- `description`: Detailed explanation of the aphorism
- `references`: Array of reference objects (optional)
  - `title`: Title of the reference
  - `url`: URL to the reference
  - `author`: Author name (optional)

## Reordering Aphorisms

To change the order of aphorisms, simply update the `order` field in the frontmatter. The cards will automatically be sorted by this number.

## Current Aphorisms

1. Who Should Do What Differently (Be Specific)
2. Perfect is the Enemy of Good
3. Complexity is the Enemy of Security
4. Trust, but Verify
5. The Best Defense is a Good Offense

## Features

- Swipe left/right on mobile
- Arrow key navigation on desktop
- Click navigation buttons
- Click dots for direct navigation
- Automatic card counter (1/5, 2/5, etc.)
- Responsive design for mobile and desktop
- **References support**: Add clickable book icon with overlay for citations
- **External links**: References open in new tabs
