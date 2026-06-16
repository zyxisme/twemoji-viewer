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
- `EMOJI_NAMES`: 679 entries with English/Chinese names for search (object in index.html)
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
- Generation script: See `docs/superpowers/plans/2026-06-16-emoji-category-filter.md`
- 11 categories: Smileys & Emotion, People & Body, Animals & Nature, Food & Drink, Activities, Travel & Places, Objects, Symbols, Flags, Component, Other
- 323 emojis fall into "Other" (not in unicode-emoji-json source)
