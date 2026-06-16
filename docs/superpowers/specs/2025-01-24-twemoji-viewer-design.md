# Twemoji Viewer Design Spec

## Overview

A single-page HTML application to display all Twitter emojis (twemoji) with the ability to copy their shortcode identifiers in `xxxxx-xxxxx` format. Supports case-sensitive copying and multi-language search.

## Goals

1. Display all 3689 twemoji SVG icons
2. Allow users to copy emoji shortcodes (e.g., `1f600` or `1F600`)
3. Support case-sensitive copy (uppercase/lowercase toggle)
4. Multi-language fuzzy search (e.g., "smile" or "微笑")
5. Client-side pagination with configurable page size
6. Persist user preferences in localStorage

## Design Reference

Based on Vercel design language (see `DESIGN.md` in project root).

### Color Palette

```css
:root {
  --primary: #171717;
  --on-primary: #ffffff;
  --canvas: #ffffff;
  --canvas-soft: #fafafa;
  --hairline: #ebebeb;
  --link: #0070f3;
  --success: #0070f3;
  --mute: #888888;
}
```

### Typography

- **Font Family**: Geist, Inter, system-ui, -apple-system, sans-serif
- **Emoji Label**: 10px, mute color
- **Body Text**: 14px, primary color

## UI Components

### 1. Top Control Bar

```
┌─────────────────────────────────────────────────────┐
│  🔍 搜索emoji...  [搜索]  每页: [50▼]  大写: [A/a] │
└─────────────────────────────────────────────────────┘
```

- **Background**: canvas-soft (#fafafa)
- **Border**: 1px hairline (#ebebeb)
- **Search Input**: No border, transparent background
- **Search Button**: primary background (#171717), white text
- **Page Size Select**: Options: 20, 50, 100, 200
- **Case Toggle**: Toggle button, persists to localStorage

### 2. Emoji Grid

```
┌─────────────────────────────────────────────────────┐
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐          │
│  │     │ │     │ │     │ │     │ │     │          │
│  │ 😀  │ │ 😁  │ │ 😂  │ │ 🤣  │ │ 😃  │  ...     │
│  │     │ │     │ │     │ │     │ │     │          │
│  │1f600│ │1f601│ │1f602│ │1f923│ │1f603│          │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘          │
└─────────────────────────────────────────────────────┘
```

- **Layout**: CSS Grid with auto-fill, minmax(60px, 1fr)
- **Gap**: 4px
- **Card Size**: 60px × 60px
- **Card Background**: canvas (#ffffff)
- **Card Border**: 1px hairline (#ebebeb)
- **Card Border Radius**: 4px
- **Emoji Size**: 36px × 36px
- **Label Font**: 10px, mute color

### 3. Pagination

```
┌─────────────────────────────────────────────────────┐
│              [←] [1] [2] [3] ... [74] [→]          │
└─────────────────────────────────────────────────────┘
```

- **Current Page**: primary background (#171717), white text
- **Other Pages**: transparent background, primary text
- **Hover**: canvas-soft background
- **Border Radius**: 4px

## Interactions

### Copy Action

1. **Click on emoji card**
2. **Visual Feedback**:
   - Emoji scales to 1.2x
   - Border changes to success color (#0070f3)
   - Duration: 0.3s with ease-out
3. **Clipboard**: Copies shortcode to clipboard
   - Lowercase: `1f600`
   - Uppercase: `1F600`
4. **Restore**: Returns to original state after animation

### Search

1. **Click search button** (not real-time)
2. **Fuzzy matching**: Partial string match
3. **Multi-language**: Supports English and Chinese emoji names
4. **Clear**: Empty search shows all emojis

### Case Toggle

1. **Toggle button**: A/a icon
2. **State**: Stored in localStorage
3. **Effect**: Changes all displayed shortcodes
4. **Default**: Lowercase

## Data

### Emoji Data Source

- **Source**: Twemoji SVG files (3689 total)
- **Format**: `{codepoint}.svg` (e.g., `1f600.svg`, `1f1e6-1f1e8.svg`)
- **CDN**: `https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/`

### Emoji Names

- **Source**: Unicode CLDR data
- **Languages**: English, Chinese (Simplified)
- **Storage**: Embedded in JavaScript as JSON

## Technical Implementation

### Single File Structure

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Twemoji Viewer</title>
  <style>
    /* CSS styles */
  </style>
</head>
<body>
  <!-- HTML structure -->
  <script>
    // JavaScript logic
  </script>
</body>
</html>
```

### Key Functions

1. **initEmojiData()**: Load emoji list and names
2. **renderGrid()**: Render emoji grid for current page
3. **copyToClipboard()**: Copy shortcode with case handling
4. **search()**: Fuzzy search implementation
5. **changePage()**: Pagination logic
6. **toggleCase()**: Case toggle with localStorage

### localStorage Keys

- `twemoji-case`: "upper" or "lower"
- `twemoji-page-size`: "20", "50", "100", or "200"

## Success Criteria

1. ✅ All 3689 emojis displayed correctly
2. ✅ Copy works with correct case
3. ✅ Search finds emojis by name (EN/CN)
4. ✅ Pagination smooth and responsive
5. ✅ Preferences persist across sessions
6. ✅ Vercel design style applied consistently

## Future Enhancements (Out of Scope)

- Category filtering
- Emoji preview on hover
- Export functionality
- Keyboard navigation
- Dark mode support
