#!/usr/bin/env python3
"""Unit tests for generate_flag_names.py"""
import unittest
import sys
import os

# Add parent directory to path to import generate_flag_names
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_flag_names import (
    extract_flag_data,
    match_flags_to_emoji_list,
    generate_search_names,
    merge_emoji_names,
    update_index_html
)
import tempfile


class TestExtractFlagData(unittest.TestCase):
    """Test extract_flag_data function"""

    def test_extract_basic_flags(self):
        """Test extracting basic country flags"""
        emoji_data = {
            '🇨🇳': {'name': 'flag China', 'group': 'Flags'},
            '🇺🇸': {'name': 'flag United States', 'group': 'Flags'},
            '🇯🇵': {'name': 'flag Japan', 'group': 'Flags'}
        }

        result = extract_flag_data(emoji_data)

        self.assertEqual(len(result), 3)
        self.assertIn('CN', result)
        self.assertIn('US', result)
        self.assertIn('JP', result)

    def test_extract_flag_name(self):
        """Test that flag names are correctly extracted"""
        emoji_data = {
            '🇨🇳': {'name': 'flag China', 'group': 'Flags'}
        }

        result = extract_flag_data(emoji_data)

        self.assertEqual(result['CN']['name'], 'flag China')

    def test_extract_flag_codepoints(self):
        """Test that codepoints are correctly generated"""
        emoji_data = {
            '🇨🇳': {'name': 'flag China', 'group': 'Flags'}
        }

        result = extract_flag_data(emoji_data)

        # CN = U+1F1E8 U+1F1F3
        self.assertEqual(result['CN']['codepoints'], '1f1e8-1f1f3')

    def test_skip_non_flags(self):
        """Test that non-flag emojis are skipped"""
        emoji_data = {
            '🇨🇳': {'name': 'flag China', 'group': 'Flags'},
            '😀': {'name': 'grinning face', 'group': 'Smileys & Emotion'}
        }

        result = extract_flag_data(emoji_data)

        self.assertEqual(len(result), 1)
        self.assertIn('CN', result)

    def test_skip_single_regional_indicators(self):
        """Test that single regional indicators are skipped"""
        emoji_data = {
            '🇨': {'name': 'regional indicator C', 'group': 'Flags'}
        }

        result = extract_flag_data(emoji_data)

        self.assertEqual(len(result), 0)


class TestMatchFlagsToEmojiList(unittest.TestCase):
    """Test match_flags_to_emoji_list function"""

    def test_match_basic_flags(self):
        """Test matching flags to EMOJI_LIST"""
        flags = {
            'CN': {'codepoints': '1f1e8-1f1f3', 'name': 'flag China'},
            'US': {'codepoints': '1f1fa-1f1f8', 'name': 'flag United States'}
        }
        emoji_list = ['1f1e8-1f1f3', '1f1fa-1f1f8', '1f1ef-1f1f5']

        result = match_flags_to_emoji_list(flags, emoji_list)

        self.assertEqual(len(result), 2)
        self.assertIn('1f1e8-1f1f3', result)
        self.assertIn('1f1fa-1f1f8', result)

    def test_match_preserves_country_code(self):
        """Test that country code is preserved in match"""
        flags = {
            'CN': {'codepoints': '1f1e8-1f1f3', 'name': 'flag China'}
        }
        emoji_list = ['1f1e8-1f1f3']

        result = match_flags_to_emoji_list(flags, emoji_list)

        self.assertEqual(result['1f1e8-1f1f3']['country_code'], 'CN')

    def test_match_preserves_name(self):
        """Test that flag name is preserved in match"""
        flags = {
            'CN': {'codepoints': '1f1e8-1f1f3', 'name': 'flag China'}
        }
        emoji_list = ['1f1e8-1f1f3']

        result = match_flags_to_emoji_list(flags, emoji_list)

        self.assertEqual(result['1f1e8-1f1f3']['name'], 'flag China')

    def test_skip_unmatched_flags(self):
        """Test that flags not in EMOJI_LIST are skipped"""
        flags = {
            'CN': {'codepoints': '1f1e8-1f1f3', 'name': 'flag China'},
            'XX': {'codepoints': '1f1e8-1f1f4', 'name': 'flag Unknown'}
        }
        emoji_list = ['1f1e8-1f1f3']

        result = match_flags_to_emoji_list(flags, emoji_list)

        self.assertEqual(len(result), 1)
        self.assertIn('1f1e8-1f1f3', result)
        self.assertNotIn('1f1e8-1f1f4', result)

    def test_empty_emoji_list(self):
        """Test matching with empty EMOJI_LIST"""
        flags = {
            'CN': {'codepoints': '1f1e8-1f1f3', 'name': 'flag China'}
        }
        emoji_list = []

        result = match_flags_to_emoji_list(flags, emoji_list)

        self.assertEqual(len(result), 0)

    def test_empty_flags(self):
        """Test matching with empty flags dictionary"""
        flags = {}
        emoji_list = ['1f1e8-1f1f3']

        result = match_flags_to_emoji_list(flags, emoji_list)

        self.assertEqual(len(result), 0)


class TestGenerateSearchNames(unittest.TestCase):
    """Test generate_search_names function"""

    def test_generate_english_name(self):
        """Test English name generation"""
        matched_flags = {
            '1f1e8-1f1f3': {'country_code': 'CN', 'name': 'flag China'}
        }
        country_names_cn = {'CN': '中国'}

        result = generate_search_names(matched_flags, country_names_cn)

        self.assertEqual(result['1f1e8-1f1f3']['en'], 'flag China CN')

    def test_generate_chinese_name(self):
        """Test Chinese name generation"""
        matched_flags = {
            '1f1e8-1f1f3': {'country_code': 'CN', 'name': 'flag China'}
        }
        country_names_cn = {'CN': '中国'}

        result = generate_search_names(matched_flags, country_names_cn)

        self.assertEqual(result['1f1e8-1f1f3']['zh'], '中国')

    def test_generate_multiple_flags(self):
        """Test generating names for multiple flags"""
        matched_flags = {
            '1f1e8-1f1f3': {'country_code': 'CN', 'name': 'flag China'},
            '1f1fa-1f1f8': {'country_code': 'US', 'name': 'flag United States'}
        }
        country_names_cn = {'CN': '中国', 'US': '美国'}

        result = generate_search_names(matched_flags, country_names_cn)

        self.assertEqual(len(result), 2)
        self.assertEqual(result['1f1e8-1f1f3']['en'], 'flag China CN')
        self.assertEqual(result['1f1fa-1f1f8']['en'], 'flag United States US')

    def test_fallback_to_english_name(self):
        """Test fallback when Chinese name is missing"""
        matched_flags = {
            '1f1e8-1f1f3': {'country_code': 'CN', 'name': 'flag China'}
        }
        country_names_cn = {}  # Empty mapping

        result = generate_search_names(matched_flags, country_names_cn)

        # Should use English name as fallback
        self.assertEqual(result['1f1e8-1f1f3']['zh'], 'flag China')

    def test_handle_flag_prefix(self):
        """Test that 'flag ' prefix is handled correctly"""
        matched_flags = {
            '1f1e8-1f1f3': {'country_code': 'CN', 'name': 'flag China'}
        }
        country_names_cn = {'CN': '中国'}

        result = generate_search_names(matched_flags, country_names_cn)

        # Should be "flag China CN", not "flag flag China CN"
        self.assertEqual(result['1f1e8-1f1f3']['en'], 'flag China CN')

    def test_handle_name_without_prefix(self):
        """Test handling name without 'flag ' prefix"""
        matched_flags = {
            '1f1e8-1f1f3': {'country_code': 'CN', 'name': 'China'}
        }
        country_names_cn = {'CN': '中国'}

        result = generate_search_names(matched_flags, country_names_cn)

        # Should be "flag China CN"
        self.assertEqual(result['1f1e8-1f1f3']['en'], 'flag China CN')


class TestMergeEmojiNames(unittest.TestCase):
    """Test merge_emoji_names function"""

    def test_merge_basic(self):
        """Test basic merge operation"""
        existing = {
            '1f446': {'en': 'point up', 'zh': '手指向上 指'}
        }
        new_names = {
            '1f1e8-1f1f3': {'en': 'flag China CN', 'zh': '中国'}
        }

        result = merge_emoji_names(existing, new_names)

        self.assertEqual(len(result), 2)
        self.assertIn('1f446', result)
        self.assertIn('1f1e8-1f1f3', result)

    def test_merge_preserves_existing(self):
        """Test that existing entries are preserved"""
        existing = {
            '1f446': {'en': 'point up', 'zh': '手指向上 指'}
        }
        new_names = {
            '1f1e8-1f1f3': {'en': 'flag China CN', 'zh': '中国'}
        }

        result = merge_emoji_names(existing, new_names)

        self.assertEqual(result['1f446']['en'], 'point up')
        self.assertEqual(result['1f446']['zh'], '手指向上 指')

    def test_merge_adds_new(self):
        """Test that new entries are added"""
        existing = {
            '1f446': {'en': 'point up', 'zh': '手指向上 指'}
        }
        new_names = {
            '1f1e8-1f1f3': {'en': 'flag China CN', 'zh': '中国'}
        }

        result = merge_emoji_names(existing, new_names)

        self.assertEqual(result['1f1e8-1f1f3']['en'], 'flag China CN')
        self.assertEqual(result['1f1e8-1f1f3']['zh'], '中国')

    def test_merge_overwrites_duplicate(self):
        """Test that duplicate keys are overwritten"""
        existing = {
            '1f1e8-1f1f3': {'en': 'old name', 'zh': '旧名称'}
        }
        new_names = {
            '1f1e8-1f1f3': {'en': 'flag China CN', 'zh': '中国'}
        }

        result = merge_emoji_names(existing, new_names)

        self.assertEqual(result['1f1e8-1f1f3']['en'], 'flag China CN')
        self.assertEqual(result['1f1e8-1f1f3']['zh'], '中国')

    def test_merge_empty_existing(self):
        """Test merging with empty existing dictionary"""
        existing = {}
        new_names = {
            '1f1e8-1f1f3': {'en': 'flag China CN', 'zh': '中国'}
        }

        result = merge_emoji_names(existing, new_names)

        self.assertEqual(len(result), 1)
        self.assertIn('1f1e8-1f1f3', result)

    def test_merge_empty_new(self):
        """Test merging with empty new names"""
        existing = {
            '1f446': {'en': 'point up', 'zh': '手指向上 指'}
        }
        new_names = {}

        result = merge_emoji_names(existing, new_names)

        self.assertEqual(len(result), 1)
        self.assertIn('1f446', result)


class TestUpdateIndexHtml(unittest.TestCase):
    """Test update_index_html function"""

    def setUp(self):
        """Create temporary index.html for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.index_path = os.path.join(self.test_dir, 'index.html')

        # Create minimal index.html with EMOJI_NAMES
        with open(self.index_path, 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html>
<body>
<script>
    const EMOJI_LIST = ["1f446", "1f1e8-1f1f3"];
    const EMOJI_NAMES = {
      '1f446': { en: 'point up', zh: '手指向上 指' }
    };
</script>
</body>
</html>''')

    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.test_dir)

    def test_update_adds_flag(self):
        """Test that update adds flag names"""
        new_names = {
            '1f1e8-1f1f3': {'en': 'flag China CN', 'zh': '中国'}
        }

        result = update_index_html(self.index_path, new_names)

        self.assertTrue(result)

        # Verify the update
        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('flag China CN', content)
        self.assertIn('中国', content)

    def test_update_preserves_existing(self):
        """Test that update preserves existing entries"""
        new_names = {
            '1f1e8-1f1f3': {'en': 'flag China CN', 'zh': '中国'}
        }

        update_index_html(self.index_path, new_names)

        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('point up', content)
        self.assertIn('手指向上 指', content)

    def test_update_returns_true_on_success(self):
        """Test that function returns True on success"""
        new_names = {
            '1f1e8-1f1f3': {'en': 'flag China CN', 'zh': '中国'}
        }

        result = update_index_html(self.index_path, new_names)

        self.assertTrue(result)

    def test_update_returns_false_on_missing_file(self):
        """Test that function returns False when file doesn't exist"""
        new_names = {
            '1f1e8-1f1f3': {'en': 'flag China CN', 'zh': '中国'}
        }

        result = update_index_html('/nonexistent/path.html', new_names)

        self.assertFalse(result)

    def test_update_returns_false_on_invalid_format(self):
        """Test that function returns False when EMOJI_NAMES not found"""
        # Create file without EMOJI_NAMES
        with open(self.index_path, 'w', encoding='utf-8') as f:
            f.write('<html><body></body></html>')

        new_names = {
            '1f1e8-1f1f3': {'en': 'flag China CN', 'zh': '中国'}
        }

        result = update_index_html(self.index_path, new_names)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
