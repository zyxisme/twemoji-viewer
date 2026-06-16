#!/usr/bin/env python3
"""Unit tests for generate_flag_names.py"""
import unittest
import sys
import os

# Add parent directory to path to import generate_flag_names
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_flag_names import extract_flag_data


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


if __name__ == '__main__':
    unittest.main()
