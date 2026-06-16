# Emoji Category Filter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add category filtering dropdown to Twemoji Viewer, allowing users to filter emojis by Unicode standard categories.

**Architecture:** Single HTML file modification. Add category mapping data, dropdown UI, and filter logic. Category data sourced from unicode-emoji-json repository.

**Tech Stack:** Vanilla HTML/CSS/JavaScript, no dependencies

---

## File Structure

- Modify: `index.html` — Main application file (all changes in this file)
- Reference: `emoji_category_map.json` — Generated category mapping (to be embedded)

---

### Task 1: Generate Category Mapping Data

**Files:**
- Read: `unicode-emoji-json/data-by-emoji.json`
- Create: `emoji_category_map.json`

- [ ] **Step 1: Run mapping generation script**

```bash
cd /vol1/1000/tmj
python3 << 'EOF'
import json
import re

# Read emoji data
with open('unicode-emoji-json/data-by-emoji.json', 'r', encoding='utf-8') as f:
    emoji_data = json.load(f)

# Create mapping from emoji character to group
emoji_to_group = {}
for emoji_char, info in emoji_data.items():
    emoji_to_group[emoji_char] = info['group']

# Function to convert codepoint string to emoji
def codepoint_to_emoji(codepoint):
    parts = codepoint.split('-')
    chars = []
    for part in parts:
        chars.append(chr(int(part, 16)))
    return ''.join(chars)

# Manual mappings for unmapped emojis
manual_mappings = {
    '1f1e6': 'Flags', '1f1e7': 'Flags', '1f1e8': 'Flags', '1f1e9': 'Flags',
    '1f1ea': 'Flags', '1f1eb': 'Flags', '1f1ec': 'Flags', '1f1ed': 'Flags',
    '1f1ee': 'Flags', '1f1ef': 'Flags', '1f1f0': 'Flags', '1f1f1': 'Flags',
    '1f1f2': 'Flags', '1f1f3': 'Flags', '1f1f4': 'Flags', '1f1f5': 'Flags',
    '1f1f6': 'Flags', '1f1f7': 'Flags', '1f1f8': 'Flags', '1f1f9': 'Flags',
    '1f1fa': 'Flags', '1f1fb': 'Flags', '1f1fc': 'Flags', '1f1fd': 'Flags',
    '1f1fe': 'Flags', '1f1ff': 'Flags',
    '1f170': 'Symbols', '1f171': 'Symbols', '1f17e': 'Symbols', '1f17f': 'Symbols',
    '1f3fb': 'Component', '1f3fc': 'Component', '1f3fd': 'Component',
    '1f3fe': 'Component', '1f3ff': 'Component',
}

# Read EMOJI_LIST from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract EMOJI_LIST array
match = re.search(r'const EMOJI_LIST = \[(.*?)\];', content, re.DOTALL)
if match:
    emoji_list_str = match.group(1)
    codepoints = re.findall(r'"([0-9a-f-]+)"', emoji_list_str)

    # Map each codepoint to group
    cp_to_group = {}

    for cp in codepoints:
        base_cp = cp.split('-')[0]
        group = manual_mappings.get(base_cp)

        if not group:
            emoji = codepoint_to_emoji(cp)
            group = emoji_to_group.get(emoji)

        if not group:
            emoji = codepoint_to_emoji(base_cp)
            group = emoji_to_group.get(emoji)

        if not group:
            group = 'Other'

        cp_to_group[cp] = group

    # Save the mapping
    with open('emoji_category_map.json', 'w') as f:
        json.dump(cp_to_group, f, indent=2)

    print(f"Generated mapping for {len(cp_to_group)} codepoints")
EOF
```

Expected output: `Generated mapping for 3689 codepoints`

- [ ] **Step 2: Verify mapping file exists and has correct structure**

```bash
head -20 emoji_category_map.json
wc -l emoji_category_map.json
```

Expected: JSON object with 3689 entries

- [ ] **Step 3: Commit**

```bash
git add emoji_category_map.json
git commit -m "feat: generate emoji category mapping data"
```

---

### Task 2: Add Category Data to index.html

**Files:**
- Modify: `index.html:280-284` (after TWEMOJI_CDN constant)

- [ ] **Step 1: Add category constants after TWEMOJI_CDN**

Add the following code after line 281 (`const TWEMOJI_CDN = ...`):

```javascript
    // Emoji category mapping (from unicode-emoji-json)
    const EMOJI_CATEGORY_MAP = EMBEDDED_MAP_PLACEHOLDER;

    // Category display info
    const CATEGORIES = {
      'all': { name: '全部', icon: '📋' },
      'Smileys & Emotion': { name: '表情与情感', icon: '😊' },
      'People & Body': { name: '人物与身体', icon: '👋' },
      'Animals & Nature': { name: '动物与自然', icon: '🐻' },
      'Food & Drink': { name: '食物与饮品', icon: '🍎' },
      'Activities': { name: '活动', icon: '⚽' },
      'Travel & Places': { name: '旅行与地点', icon: '🚗' },
      'Objects': { name: '物品', icon: '💡' },
      'Symbols': { name: '符号', icon: '🔣' },
      'Flags': { name: '旗帜', icon: '🏁' },
      'Component': { name: '组件', icon: '🏷️' },
      'Other': { name: '其他', icon: '❓' }
    };

    // Get emoji category
    function getEmojiCategory(codepoint) {
      return EMOJI_CATEGORY_MAP[codepoint] || 'Other';
    }
```

- [ ] **Step 2: Generate and embed the actual category map**

Run this script to replace the placeholder with actual data:

```bash
cd /vol1/1000/tmj
python3 << 'EOF'
import json

# Read the mapping
with open('emoji_category_map.json', 'r') as f:
    category_map = json.load(f)

# Convert to compact JSON string
map_json = json.dumps(category_map, separators=(',', ':'))

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace placeholder
content = content.replace('EMBEDDED_MAP_PLACEHOLDER', map_json)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Embedded category map ({len(map_json)} chars)")
EOF
```

Expected output: `Embedded category map (~50000 chars)`

- [ ] **Step 3: Verify the data was embedded correctly**

```bash
grep -c "EMOJI_CATEGORY_MAP" index.html
grep "1f600" index.html | head -1
```

Expected: Should show the map contains entry for 1f600

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add emoji category mapping data to index.html"
```

---

### Task 3: Add Category Dropdown UI

**Files:**
- Modify: `index.html:57-67` (control-bar CSS)
- Modify: `index.html:255-272` (control-bar HTML)

- [ ] **Step 1: Add category-select CSS**

Add after line 138 (`.case-toggle.active` block):

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

- [ ] **Step 2: Add category dropdown HTML**

Add after line 259 (search button closing `</div>`), before the page-size control group:

```html
      <div class="control-group">
        <span class="control-label">分类:</span>
        <select class="category-select" id="categorySelect">
          <option value="all">📋 全部 (3689)</option>
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

- [ ] **Step 3: Verify HTML structure**

Open `index.html` in browser and verify dropdown appears in control bar.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add category dropdown UI"
```

---

### Task 4: Implement Category Filter Logic

**Files:**
- Modify: `index.html` (script section, around line 4830-4860)

- [ ] **Step 1: Add state variable**

Add after line where `filteredEmojis` is declared (around line 4830):

```javascript
    // Current category filter
    var currentCategory = 'all';
```

- [ ] **Step 2: Add combined filter function**

Replace the existing `searchEmojis` function with:

```javascript
    // Filter emojis by category and search query
    function filterEmojis() {
      var result = EMOJI_LIST;

      // Filter by category
      if (currentCategory !== 'all') {
        result = result.filter(function(cp) {
          return getEmojiCategory(cp) === currentCategory;
        });
      }

      // Filter by search query
      var query = document.querySelector('.search-input').value.trim();
      if (query) {
        var q = query.toLowerCase();
        result = result.filter(function(cp) {
          if (cp.toLowerCase().indexOf(q) !== -1) return true;
          var names = EMOJI_NAMES[cp];
          if (names) {
            if (names.en && names.en.toLowerCase().indexOf(q) !== -1) return true;
            if (names.zh && names.zh.toLowerCase().indexOf(q) !== -1) return true;
          }
          return false;
        });
      }

      filteredEmojis = result;
      currentPage = 1;
      renderGrid();
      renderPagination();
    }

    // Legacy search function (calls filterEmojis)
    function searchEmojis(query) {
      filterEmojis();
    }
```

- [ ] **Step 3: Add category change event listener**

Add after the existing event listeners (around line 4870):

```javascript
    // Category filter
    document.getElementById('categorySelect').addEventListener('change', function() {
      currentCategory = this.value;
      localStorage.setItem('twemoji-category', currentCategory);
      filterEmojis();
    });
```

- [ ] **Step 4: Update search event listeners**

Modify the search button and Enter key handlers to call `filterEmojis()`:

```javascript
    document.getElementById('searchBtn').addEventListener('click', function() {
      filterEmojis();
    });

    document.querySelector('.search-input').addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        filterEmojis();
      }
    });
```

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat: implement category filter logic"
```

---

### Task 5: Add localStorage Persistence

**Files:**
- Modify: `index.html` (init function)

- [ ] **Step 1: Load category preference in init function**

Add in the `init()` function, after loading other preferences:

```javascript
    // Load category preference
    var savedCategory = localStorage.getItem('twemoji-category');
    if (savedCategory && CATEGORIES[savedCategory]) {
      currentCategory = savedCategory;
      document.getElementById('categorySelect').value = currentCategory;
    }
```

- [ ] **Step 2: Apply category filter on init**

Modify init to call `filterEmojis()` instead of directly setting `filteredEmojis`:

```javascript
    function init() {
      // Load preferences
      var savedCase = localStorage.getItem('twemoji-case');
      if (savedCase === 'upper') {
        isUpperCase = true;
        document.getElementById('caseToggle').classList.add('active');
      }

      var savedPageSize = localStorage.getItem('twemoji-page-size');
      if (savedPageSize) {
        pageSize = parseInt(savedPageSize);
        document.getElementById('pageSizeSelect').value = pageSize;
      }

      var savedCategory = localStorage.getItem('twemoji-category');
      if (savedCategory && CATEGORIES[savedCategory]) {
        currentCategory = savedCategory;
        document.getElementById('categorySelect').value = currentCategory;
      }

      // Apply filters and render
      filterEmojis();
    }
```

- [ ] **Step 3: Verify persistence works**

1. Open page, select a category
2. Refresh page
3. Verify category is still selected

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: persist category preference in localStorage"
```

---

### Task 6: Final Testing and Cleanup

**Files:**
- Modify: `index.html` (if needed)

- [ ] **Step 1: Test category filtering**

1. Open `index.html` in browser
2. Select "表情与情感" category
3. Verify only smiley emojis appear
4. Verify count matches (153 emojis)

- [ ] **Step 2: Test combined filter**

1. Select "动物与自然" category
2. Type "cat" in search box
3. Verify results are animal emojis matching "cat"

- [ ] **Step 3: Test "全部" option**

1. Select "全部" category
2. Verify all 3689 emojis appear

- [ ] **Step 4: Test localStorage persistence**

1. Select a category
2. Refresh page
3. Verify category is preserved

- [ ] **Step 5: Final commit**

```bash
git add index.html
git commit -m "feat: complete emoji category filter feature"
```

---

## Summary

Total tasks: 6
Total commits: 6
Files modified: `index.html`
Files created: `emoji_category_map.json`
