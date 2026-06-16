# Twemoji Viewer

Single-page HTML app displaying all Twemoji icons with copy-to-clipboard functionality.

## Project Structure

- `index.html` — Main application (single file, all CSS/JS inline)
- `twemoji/` — Cloned twemoji repository (SVG source files)
- `docs/` — Documentation and planning files
- `DESIGN.md` — Design specifications

## Key Technical Details

### Twemoji CDN
```
https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{codepoint}.svg
```

### Data
- `EMOJI_LIST`: 3689 twemoji codepoints (array in index.html)
- `EMOJI_NAMES`: 937 entries with English/Chinese names for search (object in index.html), including 258 flag names
- `EMOJI_CATEGORY_MAP`: 3689 codepoint-to-category mappings (generated from unicode-emoji-json)
- `CATEGORIES`: Category display info with name/icon for 12 categories

### Functions (index.html)
- `init()` — Load preferences from localStorage, set `filteredEmojis = [...EMOJI_LIST]`, render
- `renderGrid()` — Display current page of emojis using `filteredEmojis`
- `renderPagination()` — Page buttons with ellipsis logic
- `filterEmojis()` — Filter by category and search query (replaces searchEmojis)
- `getEmojiCategory(codepoint)` — Returns category for a codepoint
- `copyToClipboard(codepoint, card)` — Clipboard API with fallback
- `formatShortcode(codepoint)` — Apply uppercase/lowercase setting

### State Variables
- `currentPage` — Current page number
- `pageSize` — Items per page (20/50/100/200)
- `isUpperCase` — Case toggle for shortcode format
- `filteredEmojis` — Currently displayed emoji list (filtered or full)
- `currentCategory` — Selected category filter ('all' or category name)

### localStorage Keys
- `twemoji-case` — Case preference ('upper' or 'lower')
- `twemoji-page-size` — Page size preference
- `twemoji-category` — Category preference

### Design
- Vercel-style: black/white primary, `#0070f3` accent blue
- CSS Grid: `auto-fill, minmax(60px, 1fr)`
- Responsive: mobile-friendly with stacked controls

## Known Fixes Applied
1. **Init bug**: `init()` must set `filteredEmojis = [...EMOJI_LIST]` before rendering
2. **Search bug**: EMOJI_NAMES expanded from 127 to 679 entries for better coverage

## Emoji Category Data
- Source: `unicode-emoji-json` repository (cloned to project root)
- Generation script: `generate_emoji_categories.py` (run to regenerate `emoji_category_map.json`)
- 11 categories: Smileys & Emotion, People & Body, Animals & Nature, Food & Drink, Activities, Travel & Places, Objects, Symbols, Flags, Component
- 100% coverage: all 3689 codepoints mapped (no "Other" category)
- unicode-emoji-json uses `group` field (not `category`)
- Variant handling: FE0F, skin tones (1f3fb-1f3ff), ZWJ sequences
- Single regional indicators (1f1e6-1f1ff) = Component, not Flags
