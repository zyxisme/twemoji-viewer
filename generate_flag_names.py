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
                # This is a country/region flag
                country_code = ''.join(
                    chr(int(cp, 16) - 0x1F1E6 + ord('A'))
                    for cp in codepoints
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


if __name__ == '__main__':
    # Main execution will be added in later tasks
    pass
