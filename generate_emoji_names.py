#!/usr/bin/env python3
"""
Extract missing emojis from EMOJI_LIST that are not in EMOJI_NAMES.
Groups missing emojis by category using emoji_category_map.json.
"""

import json
import re
from collections import defaultdict


def extract_emoji_list_from_html(html_file):
    """Extract EMOJI_LIST from index.html."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find EMOJI_LIST array
    pattern = r'const EMOJI_LIST = \[(.*?)\];'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ValueError("Could not find EMOJI_LIST in HTML file")

    # Extract codepoints
    list_content = match.group(1)
    codepoints = re.findall(r'"([0-9a-fA-F-]+)"', list_content)
    return codepoints


def extract_emoji_names_from_html(html_file):
    """Extract EMOJI_NAMES keys from index.html."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find EMOJI_NAMES object
    pattern = r'const EMOJI_NAMES = \{(.*?)\};'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ValueError("Could not find EMOJI_NAMES in HTML file")

    # Extract keys
    names_content = match.group(1)
    keys = re.findall(r"'([0-9a-fA-F-]+)':", names_content)
    return set(keys)


def load_category_map(category_file):
    """Load emoji category mapping."""
    with open(category_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    # File paths
    html_file = 'index.html'
    category_file = 'emoji_category_map.json'

    # Extract data
    print("Extracting EMOJI_LIST from index.html...")
    emoji_list = extract_emoji_list_from_html(html_file)
    print(f"Found {len(emoji_list)} emojis in EMOJI_LIST")

    print("Extracting EMOJI_NAMES keys from index.html...")
    emoji_names_keys = extract_emoji_names_from_html(html_file)
    print(f"Found {len(emoji_names_keys)} emojis in EMOJI_NAMES")

    print("Loading category map...")
    category_map = load_category_map(category_file)
    print(f"Loaded {len(category_map)} category mappings")

    # Find missing emojis
    missing_emojis = []
    for codepoint in emoji_list:
        if codepoint not in emoji_names_keys:
            missing_emojis.append(codepoint)

    print(f"Found {len(missing_emojis)} missing emojis")

    # Group by category
    category_groups = defaultdict(list)
    for codepoint in missing_emojis:
        category = category_map.get(codepoint, 'Unknown')
        category_groups[category].append(codepoint)

    # Print summary
    print("\nMissing emojis by category:")
    for category, emojis in sorted(category_groups.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {category}: {len(emojis)} emojis")

    # Save to file
    output = {
        'total_missing': len(missing_emojis),
        'categories': dict(category_groups)
    }

    with open('missing_emojis.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSaved missing emojis to missing_emojis.json")


if __name__ == '__main__':
    main()
