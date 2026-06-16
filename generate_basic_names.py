#!/usr/bin/env python3
"""
Generate basic emoji names from unicode-emoji-json for missing emojis.
Focuses on Flags category first (smallest category).
"""

import json
import re
from collections import defaultdict


def emoji_to_codepoint(emoji_char):
    """Convert emoji character to codepoint format."""
    codepoints = []
    for char in emoji_char:
        cp = hex(ord(char))[2:]  # Remove '0x' prefix
        codepoints.append(cp)
    return '-'.join(codepoints)


def load_unicode_emoji_data(emoji_data_file):
    """Load unicode emoji data and create codepoint-to-name mapping."""
    with open(emoji_data_file, 'r', encoding='utf-8') as f:
        emoji_data = json.load(f)

    # Create mapping from codepoint to name
    codepoint_to_name = {}
    for emoji_char, data in emoji_data.items():
        codepoint = emoji_to_codepoint(emoji_char)
        codepoint_to_name[codepoint] = data['name']

    return codepoint_to_name


def load_missing_emojis(missing_file):
    """Load missing emojis from JSON file."""
    with open(missing_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_basic_names(category_emojis, codepoint_to_name, category):
    """Generate basic names for a category of emojis."""
    basic_names = {}

    for codepoint in category_emojis:
        # Get name from unicode-emoji-json
        name = codepoint_to_name.get(codepoint, '')

        if not name:
            # If no name found, create a generic one
            name = f"emoji {codepoint}"

        # For flags, we need special handling
        if category == 'Flags':
            # Extract country code from codepoint
            # Flag emojis are typically two regional indicators
            parts = codepoint.split('-')
            if len(parts) == 2:
                # Convert regional indicators to country code
                country_code = ''
                for part in parts:
                    # Regional indicators are 1f1e6-1f1ff
                    # Convert to letter: 1f1e6 -> A, 1f1e7 -> B, etc.
                    if part.startswith('1f1e') and len(part) == 5:
                        letter_index = int(part[3:], 16) - int('e6', 16)
                        if 0 <= letter_index < 26:
                            country_code += chr(65 + letter_index)  # A-Z
                if country_code:
                    name = f"flag {country_code}"

        # Create basic entry
        basic_names[codepoint] = {
            'en': name,
            'zh': '',  # Will be filled later
            'category': category
        }

    return basic_names


def main():
    # File paths
    missing_file = 'missing_emojis.json'
    emoji_data_file = 'unicode-emoji-json/data-by-emoji.json'

    # Load data
    print("Loading missing emojis...")
    missing_data = load_missing_emojis(missing_file)

    print("Loading unicode emoji data...")
    codepoint_to_name = load_unicode_emoji_data(emoji_data_file)
    print(f"Loaded {len(codepoint_to_name)} emoji names")

    # Process Flags category first
    category = 'Flags'
    if category not in missing_data['categories']:
        print(f"No missing emojis in {category} category")
        return

    category_emojis = missing_data['categories'][category]
    print(f"\nProcessing {category} category: {len(category_emojis)} emojis")

    # Generate basic names
    basic_names = generate_basic_names(category_emojis, codepoint_to_name, category)

    # Print summary
    print(f"Generated basic names for {len(basic_names)} emojis:")
    for codepoint, name_data in list(basic_names.items())[:5]:  # Show first 5
        print(f"  {codepoint}: {name_data['en']}")
    if len(basic_names) > 5:
        print(f"  ... and {len(basic_names) - 5} more")

    # Save to file
    output_file = f'basic_names_{category.lower().replace(" ", "_")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(basic_names, f, indent=2, ensure_ascii=False)

    print(f"\nSaved basic names to {output_file}")


if __name__ == '__main__':
    main()
