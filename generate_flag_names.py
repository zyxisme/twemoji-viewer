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


if __name__ == '__main__':
    # Main execution will be added in later tasks
    pass
