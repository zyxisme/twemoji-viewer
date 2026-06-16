# Emoji Category Filter Design

## Overview

Add category filtering functionality to the Twemoji Viewer app, allowing users to filter emojis by Unicode standard categories.

## Data Structure

### Category Mapping

- Source: `unicode-emoji-json` repository (muan/unicode-emoji-json)
- Mapping: 3689 Twemoji codepoints → 10 categories
- File: `emoji_category_map.json`

### Category Distribution

| Category | Count | Icon |
|----------|-------|------|
| People & Body | 2130 | 👋 |
| Flags | 295 | 🏁 |
| Objects | 256 | 💡 |
| Symbols | 232 | 🔣 |
| Travel & Places | 218 | 🚗 |
| Smileys & Emotion | 153 | 😊 |
| Animals & Nature | 149 | 🐻 |
| Food & Drink | 126 | 🍎 |
| Activities | 120 | ⚽ |
| Component | 9 | 🏷️ |

### Implementation

1. Generate `emoji_category_map.json` from unicode-emoji-json
2. Embed mapping data inline in index.html
3. Add category lookup function

## UI Design

### Dropdown Menu Location

Add category dropdown in control-bar, right of search box:

```
[🔍 搜索emoji...]  [搜索]  [分类: 全部 ▼]  [每页: 50]  [A/a]
```

### HTML Structure

```html
<div class="control-group">
  <span class="control-label">分类:</span>
  <select class="category-select" id="categorySelect">
    <option value="all">全部 (3689)</option>
    <option value="Smileys & Emotion">😊 表情与情感 (153)</option>
    <option value="People & Body">👋 人物与身体 (2130)</option>
    <option value="Animals & Nature">🐻 动物与自然 (149)</option>
    <option value="Food & Drink">🍎 食物与饮品 (126)</option>
    <option value="Activities">⚽ 活动 (120)</option>
    <option value="Travel & Places">🚗 旅行与地点 (218)</option>
    <option value="Objects">💡 物品 (256)</option>
    <option value="Symbols">🔣 符号 (232)</option>
    <option value="Flags">🏁 旗帜 (295)</option>
  </select>
</div>
```

### CSS Styling

```css
.category-select {
  padding: 8px 12px;
  border: 1px solid var(--hairline);
  border-radius: 4px;
  background: var(--canvas);
  font-size: 14px;
  cursor: pointer;
  min-width: 150px;
}
```

## Interaction Logic

### Filter Priority

1. Category filter applied first
2. Search query filters within selected category

### State Management

- `currentCategory`: Currently selected category ('all' or category name)
- `filteredEmojis`: Result of category + search filtering

### Event Handlers

```javascript
// Category change
document.getElementById('categorySelect').addEventListener('change', function() {
  currentCategory = this.value;
  filterEmojis();
});

// Combined filter function
function filterEmojis() {
  let result = EMOJI_LIST;

  // Filter by category
  if (currentCategory !== 'all') {
    result = result.filter(cp => getEmojiCategory(cp) === currentCategory);
  }

  // Filter by search query
  const query = document.querySelector('.search-input').value.trim();
  if (query) {
    const q = query.toLowerCase();
    result = result.filter(cp => {
      if (cp.toLowerCase().includes(q)) return true;
      const names = EMOJI_NAMES[cp];
      if (names) {
        if (names.en && names.en.toLowerCase().includes(q)) return true;
        if (names.zh && names.zh.toLowerCase().includes(q)) return true;
      }
      return false;
    });
  }

  filteredEmojis = result;
  currentPage = 1;
  renderGrid();
  renderPagination();
}
```

## localStorage

- Key: `twemoji-category`
- Values: 'all' or category name
- Load on init, save on change

## Success Criteria

1. User can select category from dropdown
2. Emojis filter immediately on selection
3. Search works within selected category
4. Category preference persists in localStorage
5. Page resets to 1 on category change
6. Emoji count displays correctly in dropdown options
