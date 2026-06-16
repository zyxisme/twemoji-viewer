#!/usr/bin/env python3
"""Validate flag search name generation results"""
import json
import re


def validate():
    """Validate generation results"""

    # 1. Read EMOJI_NAMES
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ index.html not found")
        return False

    match = re.search(r"const EMOJI_NAMES\s*=\s*\{(.*?)\n    \};", content, re.DOTALL)
    if not match:
        print("❌ Could not find EMOJI_NAMES")
        return False

    names_str = match.group(1)

    # 2. Extract flag entries
    flag_pattern = r"'(1f1e[6-9a-f]-1f1e[6-9a-f]|1f1f[0-9a-f]-1f1e[6-9a-f]|1f1e[6-9a-f]-1f1f[0-9a-f]|1f1f[0-9a-f]-1f1f[0-9a-f])':\s*\{([^}]+)\}"
    flags = re.findall(flag_pattern, names_str)

    print(f"📊 Statistics:")
    print(f"  - Flag search names count: {len(flags)}")

    if len(flags) == 0:
        print("⚠️  No flag search names found")
        return False

    # 3. Validate each flag
    errors = []
    for codepoints, names_str in flags:
        # Check English name
        en_match = re.search(r"en:\s*'([^']+)'", names_str)
        if not en_match:
            errors.append(f"❌ {codepoints}: Missing English name")
            continue

        en_name = en_match.group(1)
        if not en_name.startswith('flag '):
            errors.append(f"❌ {codepoints}: English name format error: {en_name}")

        # Check Chinese name
        zh_match = re.search(r"zh:\s*'([^']+)'", names_str)
        if not zh_match:
            errors.append(f"❌ {codepoints}: Missing Chinese name")
            continue

        zh_name = zh_match.group(1)
        if not zh_name:
            errors.append(f"❌ {codepoints}: Chinese name is empty")

    if errors:
        print(f"\n❌ Found {len(errors)} errors:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("✅ All flag search names format correct")
        return True


if __name__ == '__main__':
    success = validate()
    exit(0 if success else 1)
