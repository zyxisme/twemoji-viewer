# Twemoji Viewer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-page HTML application displaying all 3689 twemoji icons with copy functionality, case-sensitive copying, multi-language search, and Vercel-style design.

**Architecture:** Single HTML file with embedded CSS and JavaScript. Uses CSS Grid for emoji layout, localStorage for preferences, and Clipboard API for copying. Emoji data hardcoded from twemoji repository.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Twemoji CDN

---

## File Structure

```
twemoji-viewer/
├── index.html          # Main application file (HTML + CSS + JS)
└── docs/
    ├── DESIGN.md       # Vercel design reference (already exists)
    └── superpowers/
        ├── specs/      # Design spec
        └── plans/      # This plan
```

**Single file approach:** All HTML, CSS, and JavaScript in `index.html` for simplicity and portability.

---

### Task 1: HTML Structure and Base Styles

**Files:**
- Create: `index.html`

- [ ] **Step 1: Create HTML skeleton with Vercel-style CSS**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Twemoji Viewer</title>
  <style>
    :root {
      --primary: #171717;
      --on-primary: #ffffff;
      --canvas: #ffffff;
      --canvas-soft: #fafafa;
      --hairline: #ebebeb;
      --link: #0070f3;
      --success: #0070f3;
      --mute: #888888;
      --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: var(--font-family);
      background: var(--canvas);
      color: var(--primary);
      min-height: 100vh;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }

    /* Header */
    .header {
      text-align: center;
      margin-bottom: 24px;
    }

    .header h1 {
      font-size: 24px;
      font-weight: 600;
      margin-bottom: 8px;
    }

    .header p {
      color: var(--mute);
      font-size: 14px;
    }

    /* Control Bar */
    .control-bar {
      display: flex;
      gap: 12px;
      align-items: center;
      padding: 12px 16px;
      background: var(--canvas-soft);
      border: 1px solid var(--hairline);
      border-radius: 8px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }

    .search-group {
      display: flex;
      gap: 8px;
      flex: 1;
      min-width: 200px;
    }

    .search-input {
      flex: 1;
      padding: 8px 12px;
      border: none;
      background: transparent;
      font-size: 14px;
      outline: none;
    }

    .search-input::placeholder {
      color: var(--mute);
    }

    .search-btn {
      padding: 8px 16px;
      background: var(--primary);
      color: var(--on-primary);
      border: none;
      border-radius: 4px;
      font-size: 14px;
      cursor: pointer;
      transition: opacity 0.2s;
    }

    .search-btn:hover {
      opacity: 0.9;
    }

    .control-group {
      display: flex;
      gap: 8px;
      align-items: center;
    }

    .control-label {
      font-size: 13px;
      color: var(--mute);
    }

    .page-size-select {
      padding: 8px 12px;
      border: 1px solid var(--hairline);
      border-radius: 4px;
      background: var(--canvas);
      font-size: 14px;
      cursor: pointer;
    }

    .case-toggle {
      padding: 8px 12px;
      background: var(--canvas);
      border: 1px solid var(--hairline);
      border-radius: 4px;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .case-toggle.active {
      background: var(--primary);
      color: var(--on-primary);
      border-color: var(--primary);
    }

    /* Emoji Grid */
    .emoji-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
      gap: 4px;
      margin-bottom: 24px;
    }

    .emoji-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 60px;
      height: 60px;
      background: var(--canvas);
      border: 1px solid var(--hairline);
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s ease-out;
      user-select: none;
    }

    .emoji-card:hover {
      border-color: var(--link);
    }

    .emoji-card.copied {
      transform: scale(1.2);
      border-color: var(--success);
    }

    .emoji-icon {
      width: 36px;
      height: 36px;
      object-fit: contain;
    }

    .emoji-label {
      font-size: 10px;
      color: var(--mute);
      margin-top: 2px;
      text-align: center;
      width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    /* Pagination */
    .pagination {
      display: flex;
      justify-content: center;
      gap: 4px;
      flex-wrap: wrap;
    }

    .page-btn {
      padding: 8px 12px;
      background: transparent;
      border: 1px solid var(--hairline);
      border-radius: 4px;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s;
      min-width: 40px;
      text-align: center;
    }

    .page-btn:hover {
      background: var(--canvas-soft);
    }

    .page-btn.active {
      background: var(--primary);
      color: var(--on-primary);
      border-color: var(--primary);
    }

    .page-btn.disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    /* Empty State */
    .empty-state {
      text-align: center;
      padding: 40px;
      color: var(--mute);
    }

    /* Responsive */
    @media (max-width: 600px) {
      .control-bar {
        flex-direction: column;
      }

      .search-group {
        width: 100%;
      }

      .control-group {
        width: 100%;
        justify-content: space-between;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Twemoji Viewer</h1>
      <p>点击表情复制编号，支持多语种搜索</p>
    </div>

    <div class="control-bar">
      <div class="search-group">
        <input type="text" class="search-input" placeholder="搜索emoji... (如: smile / 微笑)">
        <button class="search-btn" id="searchBtn">搜索</button>
      </div>
      <div class="control-group">
        <span class="control-label">每页:</span>
        <select class="page-size-select" id="pageSizeSelect">
          <option value="20">20</option>
          <option value="50" selected>50</option>
          <option value="100">100</option>
          <option value="200">200</option>
        </select>
      </div>
      <div class="control-group">
        <button class="case-toggle" id="caseToggle">A/a</button>
      </div>
    </div>

    <div class="emoji-grid" id="emojiGrid"></div>

    <div class="pagination" id="pagination"></div>
  </div>

  <script>
    // JavaScript will be added in next task
  </script>
</body>
</html>
```

- [ ] **Step 2: Verify HTML structure**

Open `index.html` in browser and verify:
- Page loads without errors
- Header displays correctly
- Control bar is visible with all elements
- Grid area is empty (no emojis yet)

- [ ] **Step 3: Commit HTML structure**

```bash
git add index.html
git commit -m "feat: add HTML structure with Vercel-style CSS"
```

---

### Task 2: Emoji Data and Initialization

**Files:**
- Modify: `index.html:200-250`

- [ ] **Step 1: Add emoji data array**

Add this JavaScript before `</script>`:

```javascript
// Twemoji CDN base URL
const TWEMOJI_CDN = 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/';

// Complete list of twemoji codepoints (3689 total)
const EMOJI_LIST = [
  '1f004', '1f0cf', '1f170', '1f171', '1f17e', '1f17f', '1f18e',
  '1f191', '1f192', '1f193', '1f194', '1f195', '1f196', '1f197',
  '1f198', '1f199', '1f19a', '1f1e6-1f1e8', '1f1e6-1f1e9',
  // ... (full list will be generated from twemoji repository)
];

// State
let currentPage = 1;
let pageSize = 50;
let isUpperCase = false;
let filteredEmojis = [...EMOJI_LIST];
```

- [ ] **Step 2: Generate complete emoji list from twemoji**

Run this command to generate the full emoji list:

```bash
cd twemoji/assets/svg && ls *.svg | sed 's/\.svg$//' | sort > /tmp/emoji_list.txt
```

Then read the file and format as JavaScript array:

```bash
cat /tmp/emoji_list.txt | awk 'BEGIN{printf "const EMOJI_LIST = [\n"} {printf "  \"%s\",\n", $0} END{printf "];\n"}' > /tmp/emoji_array.txt
```

- [ ] **Step 3: Add emoji names for multi-language search**

Add emoji names mapping (sample - full list will be extensive):

```javascript
// Emoji names mapping (English and Chinese)
const EMOJI_NAMES = {
  '1f600': { en: 'grinning face', zh: '笑脸' },
  '1f601': { en: 'grinning face with smiling eyes', zh: '笑眼' },
  '1f602': { en: 'face with tears of joy', zh: '笑哭' },
  // ... (full mapping needed for search)
};
```

- [ ] **Step 4: Add initialization function**

```javascript
// Initialize application
function init() {
  // Load preferences from localStorage
  const savedCase = localStorage.getItem('twemoji-case');
  const savedPageSize = localStorage.getItem('twemoji-page-size');

  if (savedCase === 'upper') {
    isUpperCase = true;
    document.getElementById('caseToggle').classList.add('active');
  }

  if (savedPageSize) {
    pageSize = parseInt(savedPageSize);
    document.getElementById('pageSizeSelect').value = pageSize;
  }

  // Render initial grid
  renderGrid();
  renderPagination();
}

// Get emoji image URL
function getEmojiUrl(codepoint) {
  return `${TWEMOJI_CDN}${codepoint}.svg`;
}

// Format shortcode based on case setting
function formatShortcode(codepoint) {
  return isUpperCase ? codepoint.toUpperCase() : codepoint.toLowerCase();
}
```

- [ ] **Step 5: Call init on page load**

Add before `</script>`:

```javascript
// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);
```

- [ ] **Step 6: Commit emoji data**

```bash
git add index.html
git commit -m "feat: add emoji data and initialization logic"
```

---

### Task 3: Render Emoji Grid

**Files:**
- Modify: `index.html:250-300`

- [ ] **Step 1: Add renderGrid function**

```javascript
// Render emoji grid for current page
function renderGrid() {
  const grid = document.getElementById('emojiGrid');
  grid.innerHTML = '';

  const start = (currentPage - 1) * pageSize;
  const end = start + pageSize;
  const pageEmojis = filteredEmojis.slice(start, end);

  if (pageEmojis.length === 0) {
    grid.innerHTML = '<div class="empty-state">未找到匹配的emoji</div>';
    return;
  }

  pageEmojis.forEach(codepoint => {
    const card = document.createElement('div');
    card.className = 'emoji-card';
    card.dataset.codepoint = codepoint;

    const img = document.createElement('img');
    img.className = 'emoji-icon';
    img.src = getEmojiUrl(codepoint);
    img.alt = codepoint;
    img.loading = 'lazy';

    const label = document.createElement('div');
    label.className = 'emoji-label';
    label.textContent = formatShortcode(codepoint);

    card.appendChild(img);
    card.appendChild(label);

    // Click to copy
    card.addEventListener('click', () => copyToClipboard(codepoint, card));

    grid.appendChild(card);
  });
}
```

- [ ] **Step 2: Add copyToClipboard function**

```javascript
// Copy shortcode to clipboard
async function copyToClipboard(codepoint, card) {
  const shortcode = formatShortcode(codepoint);

  try {
    await navigator.clipboard.writeText(shortcode);

    // Visual feedback
    card.classList.add('copied');
    setTimeout(() => {
      card.classList.remove('copied');
    }, 300);
  } catch (err) {
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = shortcode;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);

    // Visual feedback
    card.classList.add('copied');
    setTimeout(() => {
      card.classList.remove('copied');
    }, 300);
  }
}
```

- [ ] **Step 3: Test grid rendering**

Open `index.html` in browser:
- Verify emojis are displayed
- Click an emoji and verify it's copied to clipboard
- Check that copy animation works

- [ ] **Step 4: Commit grid rendering**

```bash
git add index.html
git commit -m "feat: add emoji grid rendering and copy functionality"
```

---

### Task 4: Pagination

**Files:**
- Modify: `index.html:300-350`

- [ ] **Step 1: Add renderPagination function**

```javascript
// Render pagination controls
function renderPagination() {
  const pagination = document.getElementById('pagination');
  pagination.innerHTML = '';

  const totalPages = Math.ceil(filteredEmojis.length / pageSize);

  if (totalPages <= 1) {
    return;
  }

  // Previous button
  const prevBtn = createPageButton('←', currentPage > 1 ? currentPage - 1 : null);
  if (currentPage <= 1) {
    prevBtn.classList.add('disabled');
  }
  pagination.appendChild(prevBtn);

  // Page numbers
  const maxVisiblePages = 7;
  let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
  let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

  if (endPage - startPage + 1 < maxVisiblePages) {
    startPage = Math.max(1, endPage - maxVisiblePages + 1);
  }

  // First page
  if (startPage > 1) {
    pagination.appendChild(createPageButton(1, 1));
    if (startPage > 2) {
      const ellipsis = document.createElement('span');
      ellipsis.textContent = '...';
      ellipsis.style.padding = '8px 4px';
      ellipsis.style.color = 'var(--mute)';
      pagination.appendChild(ellipsis);
    }
  }

  // Page numbers
  for (let i = startPage; i <= endPage; i++) {
    const btn = createPageButton(i, i);
    if (i === currentPage) {
      btn.classList.add('active');
    }
    pagination.appendChild(btn);
  }

  // Last page
  if (endPage < totalPages) {
    if (endPage < totalPages - 1) {
      const ellipsis = document.createElement('span');
      ellipsis.textContent = '...';
      ellipsis.style.padding = '8px 4px';
      ellipsis.style.color = 'var(--mute)';
      pagination.appendChild(ellipsis);
    }
    pagination.appendChild(createPageButton(totalPages, totalPages));
  }

  // Next button
  const nextBtn = createPageButton('→', currentPage < totalPages ? currentPage + 1 : null);
  if (currentPage >= totalPages) {
    nextBtn.classList.add('disabled');
  }
  pagination.appendChild(nextBtn);
}

// Create page button
function createPageButton(text, page) {
  const btn = document.createElement('button');
  btn.className = 'page-btn';
  btn.textContent = text;

  if (page !== null) {
    btn.addEventListener('click', () => {
      currentPage = page;
      renderGrid();
      renderPagination();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  return btn;
}
```

- [ ] **Step 2: Test pagination**

Open `index.html` in browser:
- Verify pagination controls appear
- Click different pages and verify grid updates
- Check that "←" and "→" buttons work correctly

- [ ] **Step 3: Commit pagination**

```bash
git add index.html
git commit -m "feat: add pagination controls"
```

---

### Task 5: Search Functionality

**Files:**
- Modify: `index.html:350-400`

- [ ] **Step 1: Add search function**

```javascript
// Search emojis
function searchEmojis(query) {
  if (!query.trim()) {
    filteredEmojis = [...EMOJI_LIST];
  } else {
    const lowerQuery = query.toLowerCase().trim();
    filteredEmojis = EMOJI_LIST.filter(codepoint => {
      // Search by shortcode
      if (codepoint.includes(lowerQuery)) {
        return true;
      }

      // Search by name (if available)
      const names = EMOJI_NAMES[codepoint];
      if (names) {
        if (names.en && names.en.toLowerCase().includes(lowerQuery)) {
          return true;
        }
        if (names.zh && names.zh.includes(lowerQuery)) {
          return true;
        }
      }

      return false;
    });
  }

  currentPage = 1;
  renderGrid();
  renderPagination();
}
```

- [ ] **Step 2: Add event listeners for search**

Add after `init()` function:

```javascript
// Search button click
document.getElementById('searchBtn').addEventListener('click', () => {
  const query = document.querySelector('.search-input').value;
  searchEmojis(query);
});

// Enter key in search input
document.querySelector('.search-input').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    const query = e.target.value;
    searchEmojis(query);
  }
});
```

- [ ] **Step 3: Test search functionality**

Open `index.html` in browser:
- Type "smile" and click search
- Verify filtered results
- Clear search and verify all emojis return
- Test Chinese search if names are available

- [ ] **Step 4: Commit search functionality**

```bash
git add index.html
git commit -m "feat: add search functionality with multi-language support"
```

---

### Task 6: Preferences and Controls

**Files:**
- Modify: `index.html:400-450`

- [ ] **Step 1: Add page size change handler**

```javascript
// Page size change
document.getElementById('pageSizeSelect').addEventListener('change', (e) => {
  pageSize = parseInt(e.target.value);
  localStorage.setItem('twemoji-page-size', pageSize.toString());
  currentPage = 1;
  renderGrid();
  renderPagination();
});
```

- [ ] **Step 2: Add case toggle handler**

```javascript
// Case toggle
document.getElementById('caseToggle').addEventListener('click', () => {
  isUpperCase = !isUpperCase;
  localStorage.setItem('twemoji-case', isUpperCase ? 'upper' : 'lower');
  document.getElementById('caseToggle').classList.toggle('active');
  renderGrid();
});
```

- [ ] **Step 3: Test preferences persistence**

Open `index.html` in browser:
- Change page size to 100
- Toggle case to uppercase
- Refresh page
- Verify preferences are preserved

- [ ] **Step 4: Commit preferences**

```bash
git add index.html
git commit -m "feat: add preferences with localStorage persistence"
```

---

### Task 7: Generate Complete Emoji List

**Files:**
- Modify: `index.html:10-50`

- [ ] **Step 1: Generate full emoji list from twemoji repository**

```bash
cd twemoji/assets/svg
ls *.svg | sed 's/\.svg$//' | sort > /tmp/full_emoji_list.txt
```

- [ ] **Step 2: Format as JavaScript array**

```bash
awk 'BEGIN{printf "const EMOJI_LIST = [\n"} {printf "  \"%s\",\n", $0} END{printf "];\n"}' /tmp/full_emoji_list.txt > /tmp/emoji_array.js
```

- [ ] **Step 3: Update index.html with complete list**

Replace the `EMOJI_LIST` array in `index.html` with the generated array from `/tmp/emoji_array.js`.

- [ ] **Step 4: Verify complete list**

Open `index.html` in browser:
- Verify all 3689 emojis are available
- Check pagination shows correct total pages
- Test scrolling through multiple pages

- [ ] **Step 5: Commit complete emoji list**

```bash
git add index.html
git commit -m "feat: add complete twemoji list (3689 emojis)"
```

---

### Task 8: Emoji Names for Search

**Files:**
- Modify: `index.html:50-100`

- [ ] **Step 1: Generate emoji names mapping**

Use Unicode CLDR data or create a comprehensive mapping:

```bash
# This would require processing Unicode CLDR data
# For now, create a sample mapping for common emojis
```

- [ ] **Step 2: Add emoji names to index.html**

Add the `EMOJI_NAMES` object with English and Chinese names for common emojis.

- [ ] **Step 3: Test multi-language search**

Open `index.html` in browser:
- Search "smile" - should find 😄
- Search "微笑" - should find 😄
- Search "heart" - should find ❤️
- Search "心" - should find ❤️

- [ ] **Step 4: Commit emoji names**

```bash
git add index.html
git commit -m "feat: add emoji names for multi-language search"
```

---

### Task 9: Final Testing and Polish

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Test all features end-to-end**

Open `index.html` in browser and test:
1. ✅ All emojis load correctly
2. ✅ Pagination works (click through all pages)
3. ✅ Search works (English and Chinese)
4. ✅ Copy works (click emoji, check clipboard)
5. ✅ Case toggle works (switch between upper/lower)
6. ✅ Page size change works
7. ✅ Preferences persist after refresh
8. ✅ Animations work smoothly
9. ✅ Responsive design works on mobile

- [ ] **Step 2: Performance optimization**

If needed, add:
- Lazy loading for images
- Debounce for search input
- Virtual scrolling for very large lists

- [ ] **Step 3: Final commit**

```bash
git add index.html
git commit -m "feat: complete twemoji viewer with all features"
```

---

## Summary

**Total Tasks:** 9
**Estimated Time:** 2-3 hours
**Files Created:** 1 (`index.html`)
**Files Modified:** 0

**Key Features:**
- ✅ Display all 3689 twemoji icons
- ✅ Copy shortcode with case-sensitive option
- ✅ Multi-language fuzzy search
- ✅ Configurable pagination
- ✅ localStorage persistence
- ✅ Vercel-style design
- ✅ Responsive layout

**Next Steps:**
1. Execute this plan using subagent-driven-development or executing-plans
2. Test thoroughly
3. Deploy as single HTML file
