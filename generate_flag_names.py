#!/usr/bin/env python3
"""Generate flag search names for Twemoji Viewer"""
import json
import re


def extract_flag_data(emoji_data):
    """Extract flag data from unicode-emoji-json

    Args:
        emoji_data: Dictionary from unicode-emoji-json/data-by-emoji.json

    Returns:
        Dictionary mapping country code to flag data
    """
    flags = {}
    for emoji_char, data in emoji_data.items():
        if data.get('group') == 'Flags':
            # Extract country/region code
            # Flag emojis consist of two regional indicators
            # e.g., 🇨🇳 = U+1F1E8 U+1F1F3 → codepoints: 1f1e8, 1f1f3
            codepoints = []
            for char in emoji_char:
                cp = hex(ord(char))[2:]
                codepoints.append(cp)

            if len(codepoints) == 2:
                # Verify both codepoints are regional indicators (U+1F1E6..U+1F1FF)
                values = [int(cp, 16) for cp in codepoints]
                if not all(0x1F1E6 <= v <= 0x1F1FF for v in values):
                    continue
                # This is a country/region flag
                country_code = ''.join(
                    chr(v - 0x1F1E6 + ord('A'))
                    for v in values
                )
                flags[country_code] = {
                    'emoji': emoji_char,
                    'name': data['name'],
                    'codepoints': '-'.join(codepoints)
                }
    return flags


def match_flags_to_emoji_list(flags, emoji_list):
    """Match flags to EMOJI_LIST

    Args:
        flags: Dictionary from extract_flag_data
        emoji_list: List of emoji codepoints from EMOJI_LIST

    Returns:
        Dictionary mapping codepoints to matched flag data
    """
    matched = {}
    for country_code, flag_data in flags.items():
        codepoints = flag_data['codepoints']
        if codepoints in emoji_list:
            matched[codepoints] = {
                'country_code': country_code,
                'name': flag_data['name']
            }
    return matched


def generate_search_names(matched_flags, country_names_cn):
    """Generate search names for flags

    Args:
        matched_flags: Dictionary from match_flags_to_emoji_list
        country_names_cn: Dictionary mapping country code to Chinese name

    Returns:
        Dictionary mapping codepoints to search name dict with 'en' and 'zh'
    """
    names = {}
    for codepoints, flag_info in matched_flags.items():
        country_code = flag_info['country_code']
        english_name = flag_info['name']

        # Extract country name (remove "flag " prefix if present)
        if english_name.startswith('flag '):
            country_name = english_name[5:]
        else:
            country_name = english_name

        # Generate English search name
        en_name = f"flag {country_name} {country_code}"

        # Generate Chinese search name (fallback to English name)
        zh_name = country_names_cn.get(country_code, english_name)

        names[codepoints] = {
            'en': en_name,
            'zh': zh_name
        }
    return names


def merge_emoji_names(existing_names, new_names):
    """Merge new names into existing EMOJI_NAMES

    Args:
        existing_names: Current EMOJI_NAMES dictionary
        new_names: New names to merge in

    Returns:
        Merged dictionary
    """
    merged = existing_names.copy()
    merged.update(new_names)
    return merged


def update_index_html(index_path, new_names):
    """Update EMOJI_NAMES in index.html

    Args:
        index_path: Path to index.html
        new_names: Dictionary of new names to add

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {index_path}")
        return False

    # Find EMOJI_NAMES object
    pattern = r"const EMOJI_NAMES\s*=\s*\{(.+)\}\s*;"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print("❌ Could not find EMOJI_NAMES in index.html")
        return False

    # Generate new EMOJI_NAMES string
    names_str = match.group(1)

    # Add new flag names
    additions = []
    for codepoints, names in sorted(new_names.items()):
        additions.append(
            f"      '{codepoints}': {{ en: '{names['en']}', zh: '{names['zh']}' }}"
        )

    # Append to EMOJI_NAMES object
    if additions:
        # Find the last entry
        last_entry_pattern = r"('[0-9a-f]+(?:-[0-9a-f]+)*':\s*\{[^}]+\})"
        last_match = re.search(last_entry_pattern + r"(?![\s\S]*\1)", names_str)
        if last_match:
            insert_pos = last_match.end()
            new_additions = ",\n" + ",\n".join(additions)
            names_str = names_str[:insert_pos] + new_additions + names_str[insert_pos:]

    # Replace EMOJI_NAMES object
    new_content = content[:match.start()] + f"const EMOJI_NAMES = {{{names_str}}};" + content[match.end():]

    try:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"❌ Failed to write file: {e}")
        return False


def read_json_file(file_path):
    """Safely read JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON format error: {file_path}")
        print(f"   Error message: {e}")
        return None


def read_emoji_list_from_html(index_path):
    """Read EMOJI_LIST from index.html"""
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {index_path}")
        return None

    match = re.search(r"const EMOJI_LIST\s*=\s*\[(.*?)\];", content, re.DOTALL)
    if not match:
        print("❌ Could not find EMOJI_LIST in index.html")
        return None

    emoji_list_str = match.group(1)
    return [m.group(1) for m in re.finditer(r'"([0-9a-f]+(?:-[0-9a-f]+)*)"', emoji_list_str)]


def main():
    """Main execution function"""
    print("🚀 Starting flag search name generation...\n")

    # 1. Read unicode-emoji-json data
    print("📖 Reading unicode-emoji-json data...")
    emoji_data = read_json_file('unicode-emoji-json/data-by-emoji.json')
    if not emoji_data:
        return False

    # 2. Extract flag data
    flags = extract_flag_data(emoji_data)
    print(f"✅ Found {len(flags)} flag emojis\n")

    # 3. Read EMOJI_LIST
    print("📖 Reading EMOJI_LIST...")
    emoji_list = read_emoji_list_from_html('index.html')
    if not emoji_list:
        return False

    flag_count = sum(1 for e in emoji_list if e.startswith('1f1e') or e.startswith('1f1f'))
    print(f"✅ Found {flag_count} flag codepoints\n")

    # 4. Match flags to EMOJI_LIST
    print("🔗 Matching flags...")
    matched = match_flags_to_emoji_list(flags, emoji_list)
    print(f"✅ Successfully matched {len(matched)} flags")

    # Find unmatched
    unmatched_in_list = [
        e for e in emoji_list
        if (e.startswith('1f1e') or e.startswith('1f1f')) and e not in matched
    ]
    if unmatched_in_list:
        print(f"⚠️  {len(unmatched_in_list)} flags in EMOJI_LIST unmatched")
    print()

    # 5. Read Chinese names
    print("📖 Reading country/region Chinese names...")
    country_names_cn = read_json_file('country_names_cn.json')
    if not country_names_cn:
        return False
    print(f"✅ Loaded {len(country_names_cn)} Chinese names\n")

    # 6. Generate search names
    print("✏️  Generating search names...")
    new_names = generate_search_names(matched, country_names_cn)
    print(f"✅ Generated {len(new_names)} flag search names\n")

    # 7. Update index.html
    print("📝 Updating index.html...")
    success = update_index_html('index.html', new_names)
    if not success:
        return False
    print("✅ Successfully updated EMOJI_NAMES\n")

    # Summary
    print("=" * 50)
    print("📊 Generation Report:")
    print(f"✅ Successfully generated {len(new_names)} flag search names")
    if unmatched_in_list:
        print(f"⚠️  {len(unmatched_in_list)} flags unmatched")
    print("=" * 50)

    return True


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
