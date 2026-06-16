#!/usr/bin/env python3
"""Generate EMOJI_CATEGORY_MAP from unicode-emoji-json data and EMOJI_LIST."""
import json
import re

# Read EMOJI_LIST from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r"const EMOJI_LIST\s*=\s*\[(.*?)\];", content, re.DOTALL)
if not match:
    print("Error: Could not find EMOJI_LIST in index.html")
    exit(1)

emoji_list_str = match.group(1)
EMOJI_LIST = [m.group(1) for m in re.finditer(r'"([0-9a-f]+(?:-[0-9a-f]+)*)"', emoji_list_str)]

print(f"EMOJI_LIST count: {len(EMOJI_LIST)}")

# Load unicode-emoji-json data
with open('unicode-emoji-json/data-by-emoji.json', 'r', encoding='utf-8') as f:
    emoji_data = json.load(f)

# Build lookup: codepoint -> category
# Try different variations to find a match
SKIN_TONES = {'1f3fb', '1f3fc', '1f3fd', '1f3fe', '1f3ff'}

def find_category(codepoint):
    # Direct lookup
    parts = codepoint.split('-')
    emoji = ''.join(chr(int(p, 16)) for p in parts)
    if emoji in emoji_data:
        cat = emoji_data[emoji].get('group', '')
        if cat:
            return cat

    # Try without FE0F
    if 'fe0f' in parts:
        alt = '-'.join(p for p in parts if p != 'fe0f')
        alt_emoji = ''.join(chr(int(p, 16)) for p in alt.split('-'))
        if alt_emoji in emoji_data:
            cat = emoji_data[alt_emoji].get('group', '')
            if cat:
                return cat

    # Try with FE0F added (single emoji)
    if len(parts) == 1 and 'fe0f' not in parts:
        emoji_with_fe0f = emoji + chr(0xfe0f)
        if emoji_with_fe0f in emoji_data:
            cat = emoji_data[emoji_with_fe0f].get('group', '')
            if cat:
                return cat

    # Try without skin tone modifiers
    if any(p in SKIN_TONES for p in parts):
        alt_parts = [p for p in parts if p not in SKIN_TONES]
        alt_emoji = ''.join(chr(int(p, 16)) for p in alt_parts)
        if alt_emoji in emoji_data:
            cat = emoji_data[alt_emoji].get('group', '')
            if cat:
                return cat
        # Also try with FE0F added
        alt_with_fe0f = alt_emoji + chr(0xfe0f)
        if alt_with_fe0f in emoji_data:
            cat = emoji_data[alt_with_fe0f].get('group', '')
            if cat:
                return cat

    # Try base emoji only (first codepoint for ZWJ sequences)
    if len(parts) > 1 and '200d' in parts:
        base = parts[0]
        base_emoji = chr(int(base, 16))
        if base_emoji in emoji_data:
            cat = emoji_data[base_emoji].get('group', '')
            if cat:
                return cat

    return None

# Manual overrides for known categories
MANUAL_OVERRIDES = {
    # Regional indicators (single) are components
    '1f1e6': 'Component', '1f1e7': 'Component', '1f1e8': 'Component',
    '1f1e9': 'Component', '1f1ea': 'Component', '1f1eb': 'Component',
    '1f1ec': 'Component', '1f1ed': 'Component', '1f1ee': 'Component',
    '1f1ef': 'Component', '1f1f0': 'Component', '1f1f1': 'Component',
    '1f1f2': 'Component', '1f1f3': 'Component', '1f1f4': 'Component',
    '1f1f5': 'Component', '1f1f6': 'Component', '1f1f7': 'Component',
    '1f1f8': 'Component', '1f1f9': 'Component', '1f1fa': 'Component',
    '1f1fb': 'Component', '1f1fc': 'Component', '1f1fd': 'Component',
    '1f1fe': 'Component', '1f1ff': 'Component',
    # Skin tones
    '1f3fb': 'Component', '1f3fc': 'Component', '1f3fd': 'Component',
    '1f3fe': 'Component', '1f3ff': 'Component',
    # ZWJ and other components
    '200d': 'Component', 'fe0f': 'Component', '20e3': 'Component',
    'e50a': 'Component',
    # Hair components
    '1f9b0': 'Component', '1f9b1': 'Component', '1f9b2': 'Component',
    '1f9b3': 'Component',
    # Keycap components
    '23-20e3': 'Symbols', '2a-20e3': 'Symbols',
    '30-20e3': 'Symbols', '31-20e3': 'Symbols', '32-20e3': 'Symbols',
    '33-20e3': 'Symbols', '34-20e3': 'Symbols', '35-20e3': 'Symbols',
    '36-20e3': 'Symbols', '37-20e3': 'Symbols', '38-20e3': 'Symbols',
    '39-20e3': 'Symbols',
}

# Generate mapping
category_map = {}
unmatched = []

for codepoint in EMOJI_LIST:
    if codepoint in MANUAL_OVERRIDES:
        category_map[codepoint] = MANUAL_OVERRIDES[codepoint]
        continue

    cat = find_category(codepoint)
    if cat:
        category_map[codepoint] = cat
    else:
        # Heuristic: if contains 200d, it's a ZWJ sequence
        if '200d' in codepoint:
            # Try to determine from first emoji
            base = codepoint.split('-')[0]
            base_cat = MANUAL_OVERRIDES.get(base) or find_category(base)
            if base_cat:
                category_map[codepoint] = base_cat
            else:
                category_map[codepoint] = 'Other'
                unmatched.append(codepoint)
        else:
            category_map[codepoint] = 'Other'
            unmatched.append(codepoint)

print(f"Total mapped: {len(category_map)}")
print(f"Unmatched: {len(unmatched)}")
if unmatched[:5]:
    print(f"Sample unmatched: {unmatched[:5]}")

# Save
with open('emoji_category_map.json', 'w', encoding='utf-8') as f:
    json.dump(category_map, f, indent=2, ensure_ascii=False)

# Print stats
from collections import Counter
counts = Counter(category_map.values())
print("\nCategory distribution:")
for cat, count in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}")
