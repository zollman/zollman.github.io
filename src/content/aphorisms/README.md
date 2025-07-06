# Aphorisms Management

This directory contains the aphorisms displayed on the website's wisdom cards section.

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
---

# Your Aphorism Title

A paragraph explaining the aphorism in detail. This will appear below the title on the card.
```

## Frontmatter Fields

- `title`: The main aphorism text (displayed prominently on the card)
- `order`: Number for ordering (determines display sequence)
- `icon`: Emoji or symbol to display above the title (optional, defaults to 💡)
- `description`: Detailed explanation of the aphorism

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
