#!/usr/bin/env python3
"""Integration test for flag search name generation"""
import json
import re
import tempfile
import shutil
import os
import sys


def test_integration():
    """Integration test: verify the entire flow"""

    # Create temporary directory
    test_dir = tempfile.mkdtemp()

    try:
        # 1. Create test index.html with flag codepoints in EMOJI_LIST
        index_path = os.path.join(test_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html>
<body>
<script>
    const EMOJI_LIST = ["1f1e8-1f1f3", "1f1fa-1f1f8", "1f1ef-1f1f5"];
    const EMOJI_NAMES = {
      '1f446': { en: 'point up', zh: '手指向上 指' }
    };
</script>
</body>
</html>''')

        # 2. Create test emoji data at the path main() expects
        emoji_data_dir = os.path.join(test_dir, 'unicode-emoji-json')
        os.makedirs(emoji_data_dir, exist_ok=True)
        emoji_data_path = os.path.join(emoji_data_dir, 'data-by-emoji.json')
        # Regional indicator codepoints for flags:
        # CN = U+1F1E8 U+1F1F3, US = U+1F1FA U+1F1F8, JP = U+1F1EF U+1F1F5
        emoji_data = {
            '\U0001f1e8\U0001f1f3': {'name': 'flag: China', 'group': 'Flags'},
            '\U0001f1fa\U0001f1f8': {'name': 'flag: United States', 'group': 'Flags'},
            '\U0001f1ef\U0001f1f5': {'name': 'flag: Japan', 'group': 'Flags'}
        }
        with open(emoji_data_path, 'w', encoding='utf-8') as f:
            json.dump(emoji_data, f)

        # 3. Create test country names
        country_names_path = os.path.join(test_dir, 'country_names_cn.json')
        country_names = {
            'CN': '中国',
            'US': '美国',
            'JP': '日本'
        }
        with open(country_names_path, 'w', encoding='utf-8') as f:
            json.dump(country_names, f)

        # 4. Change to test directory
        original_dir = os.getcwd()
        os.chdir(test_dir)

        # 5. Import and run the script
        sys.path.insert(0, original_dir)
        # Remove cached module if re-running
        if 'generate_flag_names' in sys.modules:
            del sys.modules['generate_flag_names']
        from generate_flag_names import main

        result = main()

        # 6. Verify results
        if not result:
            print("❌ main() returned False")
            return False

        # 7. Check updated index.html
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check that flags were added with correct format
        if 'flag: China CN' not in content:
            print("❌ 'flag: China CN' not found in output")
            return False

        if '中国' not in content:
            print("❌ '中国' not found in output")
            return False

        if 'flag: United States US' not in content:
            print("❌ 'flag: United States US' not found in output")
            return False

        if '美国' not in content:
            print("❌ '美国' not found in output")
            return False

        if 'flag: Japan JP' not in content:
            print("❌ 'flag: Japan JP' not found in output")
            return False

        if '日本' not in content:
            print("❌ '日本' not found in output")
            return False

        # Check that existing entries are preserved
        if 'point up' not in content:
            print("❌ Existing entry 'point up' was lost")
            return False

        print("✅ Integration test passed!")
        return True

    except Exception as e:
        print(f"❌ Integration test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Cleanup
        os.chdir(original_dir)
        shutil.rmtree(test_dir)


if __name__ == '__main__':
    success = test_integration()
    exit(0 if success else 1)
