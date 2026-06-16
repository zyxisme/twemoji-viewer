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

### Functions (index.html)
- `init()` — Load preferences from localStorage, set `filteredEmojis = [...EMOJI_LIST]`, render
- `renderGrid()` — Display current page of emojis using `filteredEmojis`
- `renderPagination()` — Page buttons with ellipsis logic
- `searchEmojis(query)` — Filter by codepoint, English name, Chinese name
- `copyToClipboard(codepoint, card)` — Clipboard API with fallback
- `formatShortcode(codepoint)` — Apply uppercase/lowercase setting

### State Variables
- `currentPage` — Current page number
- `pageSize` — Items per page (20/50/100/200)
- `isUpperCase` — Case toggle for shortcode format
- `filteredEmojis` — Currently displayed emoji list (filtered or full)

### localStorage Keys
- `twemoji-case` — Case preference ('upper' or 'lower')
- `twemoji-page-size` — Page size preference

### Design
- Vercel-style: black/white primary, `#0070f3` accent blue
- CSS Grid: `auto-fill, minmax(60px, 1fr)`
- Responsive: mobile-friendly with stacked controls

## Known Fixes Applied
1. **Init bug**: `init()` must set `filteredEmojis = [...EMOJI_LIST]` before rendering
2. **Search bug**: EMOJI_NAMES expanded from 127 to 679 entries for better coverage
