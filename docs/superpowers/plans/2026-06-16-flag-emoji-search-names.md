# Flag Emoji Search Names Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add comprehensive search names for all 267 flag emojis, enabling users to search by country name, country code, and Chinese name.

**Architecture:** Create a Python script that reads flag data from unicode-emoji-json, matches against EMOJI_LIST, generates formatted search names (English with country code, Chinese with standard names), and updates index.html's EMOJI_NAMES object.

**Tech Stack:** Python 3.x, JSON, Regular Expressions

---

## File Structure

### Files to Create

| File | Responsibility |
|------|---------------|
| `country_names_cn.json` | Country/region code to Chinese name mapping (250+ entries) |
| `generate_flag_names.py` | Main script: read data, match flags, generate names, update index.html |
| `test_generate_flag_names.py` | Unit tests for all core functions |
| `test_integration.py` | Integration test: verify complete flow |
| `validate_flag_names.py` | Validation script: check generated results |

### Files to Modify

| File | Changes |
|------|---------|
| `index.html` | Update EMOJI_NAMES object with flag search names |

---

## Task 1: Create Country/Region Chinese Name Mapping

**Files:**
- Create: `country_names_cn.json`

- [ ] **Step 1: Create the Chinese name mapping file**

```json
{
  "AC": "阿森松岛",
  "AD": "安道尔",
  "AE": "阿联酋",
  "AF": "阿富汗",
  "AG": "安提瓜和巴布达",
  "AI": "安圭拉",
  "AL": "阿尔巴尼亚",
  "AM": "亚美尼亚",
  "AO": "安哥拉",
  "AQ": "南极洲",
  "AR": "阿根廷",
  "AS": "美属萨摩亚",
  "AT": "奥地利",
  "AU": "澳大利亚",
  "AW": "阿鲁巴",
  "AX": "奥兰群岛",
  "AZ": "阿塞拜疆",
  "BA": "波黑",
  "BB": "巴巴多斯",
  "BD": "孟加拉国",
  "BE": "比利时",
  "BF": "布基纳法索",
  "BG": "保加利亚",
  "BH": "巴林",
  "BI": "布隆迪",
  "BJ": "贝宁",
  "BL": "圣巴泰勒米",
  "BM": "百慕大",
  "BN": "文莱",
  "BO": "玻利维亚",
  "BQ": "荷兰加勒比区",
  "BR": "巴西",
  "BS": "巴哈马",
  "BT": "不丹",
  "BV": "布韦岛",
  "BW": "博茨瓦纳",
  "BY": "白俄罗斯",
  "BZ": "伯利兹",
  "CA": "加拿大",
  "CC": "科科斯群岛",
  "CD": "刚果（金）",
  "CF": "中非",
  "CG": "刚果（布）",
  "CH": "瑞士",
  "CI": "科特迪瓦",
  "CK": "库克群岛",
  "CL": "智利",
  "CM": "喀麦隆",
  "CN": "中国",
  "CO": "哥伦比亚",
  "CP": "克利珀顿岛",
  "CR": "哥斯达黎加",
  "CU": "古巴",
  "CV": "佛得角",
  "CW": "库拉索",
  "CX": "圣诞岛",
  "CY": "塞浦路斯",
  "CZ": "捷克",
  "DE": "德国",
  "DG": "迪戈加西亚",
  "DJ": "吉布提",
  "DK": "丹麦",
  "DM": "多米尼克",
  "DO": "多米尼加",
  "DZ": "阿尔及利亚",
  "EA": "休达和梅利利亚",
  "EC": "厄瓜多尔",
  "EE": "爱沙尼亚",
  "EG": "埃及",
  "EH": "西撒哈拉",
  "ER": "厄立特里亚",
  "ES": "西班牙",
  "ET": "埃塞俄比亚",
  "EU": "欧盟",
  "FI": "芬兰",
  "FJ": "斐济",
  "FK": "福克兰群岛",
  "FM": "密克罗尼西亚",
  "FO": "法罗群岛",
  "FR": "法国",
  "GA": "加蓬",
  "GB": "英国",
  "GD": "格林纳达",
  "GE": "格鲁吉亚",
  "GF": "法属圭亚那",
  "GG": "根西岛",
  "GH": "加纳",
  "GI": "直布罗陀",
  "GL": "格陵兰",
  "GM": "冈比亚",
  "GN": "几内亚",
  "GP": "瓜德罗普",
  "GQ": "赤道几内亚",
  "GR": "希腊",
  "GS": "南乔治亚和南桑威奇群岛",
  "GT": "危地马拉",
  "GU": "关岛",
  "GW": "几内亚比绍",
  "GY": "圭亚那",
  "HK": "香港",
  "HM": "赫德岛和麦克唐纳群岛",
  "HN": "洪都拉斯",
  "HR": "克罗地亚",
  "HT": "海地",
  "HU": "匈牙利",
  "IC": "加纳利群岛",
  "ID": "印度尼西亚",
  "IE": "爱尔兰",
  "IL": "以色列",
  "IM": "马恩岛",
  "IN": "印度",
  "IO": "英属印度洋领地",
  "IQ": "伊拉克",
  "IR": "伊朗",
  "IS": "冰岛",
  "IT": "意大利",
  "JE": "泽西岛",
  "JM": "牙买加",
  "JO": "约旦",
  "JP": "日本",
  "KE": "肯尼亚",
  "KG": "吉尔吉斯斯坦",
  "KH": "柬埔寨",
  "KI": "基里巴斯",
  "KM": "科摩罗",
  "KN": "圣基茨和尼维斯",
  "KP": "朝鲜",
  "KR": "韩国",
  "KW": "科威特",
  "KY": "开曼群岛",
  "KZ": "哈萨克斯坦",
  "LA": "老挝",
  "LB": "黎巴嫩",
  "LC": "圣卢西亚",
  "LI": "列支敦士登",
  "LK": "斯里兰卡",
  "LR": "利比里亚",
  "LS": "莱索托",
  "LT": "立陶宛",
  "LU": "卢森堡",
  "LV": "拉脱维亚",
  "LY": "利比亚",
  "MA": "摩洛哥",
  "MC": "摩纳哥",
  "MD": "摩尔多瓦",
  "ME": "黑山",
  "MF": "法属圣马丁",
  "MG": "马达加斯加",
  "MH": "马绍尔群岛",
  "MK": "北马其顿",
  "ML": "马里",
  "MM": "缅甸",
  "MN": "蒙古",
  "MO": "澳门",
  "MP": "北马里亚纳群岛",
  "MQ": "马提尼克",
  "MR": "毛里塔尼亚",
  "MS": "蒙特塞拉特",
  "MT": "马耳他",
  "MU": "毛里求斯",
  "MV": "马尔代夫",
  "MW": "马拉维",
  "MX": "墨西哥",
  "MY": "马来西亚",
  "MZ": "莫桑比克",
  "NA": "纳米比亚",
  "NC": "新喀里多尼亚",
  "NE": "尼日尔",
  "NF": "诺福克岛",
  "NG": "尼日利亚",
  "NI": "尼加拉瓜",
  "NL": "荷兰",
  "NO": "挪威",
  "NP": "尼泊尔",
  "NR": "瑙鲁",
  "NU": "纽埃",
  "NZ": "新西兰",
  "OM": "阿曼",
  "PA": "巴拿马",
  "PE": "秘鲁",
  "PF": "法属波利尼西亚",
  "PG": "巴布亚新几内亚",
  "PH": "菲律宾",
  "PK": "巴基斯坦",
  "PL": "波兰",
  "PM": "圣皮埃尔和密克隆",
  "PN": "皮特凯恩群岛",
  "PR": "波多黎各",
  "PS": "巴勒斯坦",
  "PT": "葡萄牙",
  "PW": "帕劳",
  "PY": "巴拉圭",
  "QA": "卡塔尔",
  "RE": "留尼汪",
  "RO": "罗马尼亚",
  "RS": "塞尔维亚",
  "RU": "俄罗斯",
  "RW": "卢旺达",
  "SA": "沙特阿拉伯",
  "SB": "所罗门群岛",
  "SC": "塞舌尔",
  "SD": "苏丹",
  "SE": "瑞典",
  "SG": "新加坡",
  "SH": "圣赫勒拿",
  "SI": "斯洛文尼亚",
  "SJ": "斯瓦尔巴和扬马延",
  "SK": "斯洛伐克",
  "SL": "塞拉利昂",
  "SM": "圣马力诺",
  "SN": "塞内加尔",
  "SO": "索马里",
  "SR": "苏里南",
  "SS": "南苏丹",
  "ST": "圣多美和普林西比",
  "SV": "萨尔瓦多",
  "SX": "荷属圣马丁",
  "SY": "叙利亚",
  "SZ": "斯威士兰",
  "TA": "特里斯坦-达库尼亚",
  "TC": "特克斯和凯科斯群岛",
  "TD": "乍得",
  "TF": "法属南部领地",
  "TG": "多哥",
  "TH": "泰国",
  "TJ": "塔吉克斯坦",
  "TK": "托克劳",
  "TL": "东帝汶",
  "TM": "土库曼斯坦",
  "TN": "突尼斯",
  "TO": "汤加",
  "TR": "土耳其",
  "TT": "特立尼达和多巴哥",
  "TV": "图瓦卢",
  "TW": "台湾",
  "TZ": "坦桑尼亚",
  "UA": "乌克兰",
  "UG": "乌干达",
  "UM": "美国本土外小岛屿",
  "UN": "联合国",
  "US": "美国",
  "UY": "乌拉圭",
  "UZ": "乌兹别克斯坦",
  "VA": "梵蒂冈",
  "VC": "圣文森特和格林纳丁斯",
  "VE": "委内瑞拉",
  "VG": "英属维尔京群岛",
  "VI": "美属维尔京群岛",
  "VN": "越南",
  "VU": "瓦努阿图",
  "WF": "瓦利斯和富图纳",
  "WS": "萨摩亚",
  "XK": "科索沃",
  "YE": "也门",
  "YT": "马约特",
  "ZA": "南非",
  "ZM": "赞比亚",
  "ZW": "津巴布韦"
}
```

- [ ] **Step 2: Verify the file is valid JSON**

Run: `python3 -c "import json; json.load(open('country_names_cn.json')); print('✅ Valid JSON')"`

Expected: `✅ Valid JSON`

- [ ] **Step 3: Count entries**

Run: `python3 -c "import json; data = json.load(open('country_names_cn.json')); print(f'Entries: {len(data)}')"`

Expected: `Entries: 250` (or similar count)

- [ ] **Step 4: Commit**

```bash
git add country_names_cn.json
git commit -m "feat: add country/region Chinese name mapping"
```

---

## Task 2: Create Unit Tests for extract_flag_data

**Files:**
- Create: `test_generate_flag_names.py`

- [ ] **Step 1: Write the failing test for extract_flag_data**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest test_generate_flag_names.py::TestExtractFlagData -v`

Expected: FAIL with "ModuleNotFoundError: No module named 'generate_flag_names'"

- [ ] **Step 3: Commit**

```bash
git add test_generate_flag_names.py
git commit -m "test: add unit tests for extract_flag_data"
```

---

## Task 3: Implement extract_flag_data Function

**Files:**
- Create: `generate_flag_names.py`

- [ ] **Step 1: Write minimal implementation**

```python
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
```

- [ ] **Step 2: Run test to verify it passes**

Run: `python3 -m pytest test_generate_flag_names.py::TestExtractFlagData -v`

Expected: All 5 tests PASS

- [ ] **Step 3: Commit**

```bash
git add generate_flag_names.py
git commit -m "feat: implement extract_flag_data function"
```

---

## Task 4: Add Unit Tests for match_flags_to_emoji_list

**Files:**
- Modify: `test_generate_flag_names.py`

- [ ] **Step 1: Add test class for match_flags_to_emoji_list**

Append to `test_generate_flag_names.py`:

```python
from generate_flag_names import extract_flag_data, match_flags_to_emoji_list


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest test_generate_flag_names.py::TestMatchFlagsToEmojiList -v`

Expected: FAIL with "ImportError: cannot import name 'match_flags_to_emoji_list'"

- [ ] **Step 3: Commit**

```bash
git add test_generate_flag_names.py
git commit -m "test: add unit tests for match_flags_to_emoji_list"
```

---

## Task 5: Implement match_flags_to_emoji_list Function

**Files:**
- Modify: `generate_flag_names.py`

- [ ] **Step 1: Add match_flags_to_emoji_list function**

Add after `extract_flag_data` function in `generate_flag_names.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it passes**

Run: `python3 -m pytest test_generate_flag_names.py::TestMatchFlagsToEmojiList -v`

Expected: All 6 tests PASS

- [ ] **Step 3: Commit**

```bash
git add generate_flag_names.py
git commit -m "feat: implement match_flags_to_emoji_list function"
```

---

## Task 6: Add Unit Tests for generate_search_names

**Files:**
- Modify: `test_generate_flag_names.py`

- [ ] **Step 1: Add test class for generate_search_names**

Append to `test_generate_flag_names.py`:

```python
from generate_flag_names import (
    extract_flag_data, 
    match_flags_to_emoji_list, 
    generate_search_names
)


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest test_generate_flag_names.py::TestGenerateSearchNames -v`

Expected: FAIL with "ImportError: cannot import name 'generate_search_names'"

- [ ] **Step 3: Commit**

```bash
git add test_generate_flag_names.py
git commit -m "test: add unit tests for generate_search_names"
```

---

## Task 7: Implement generate_search_names Function

**Files:**
- Modify: `generate_flag_names.py`

- [ ] **Step 1: Add generate_search_names function**

Add after `match_flags_to_emoji_list` function in `generate_flag_names.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it passes**

Run: `python3 -m pytest test_generate_flag_names.py::TestGenerateSearchNames -v`

Expected: All 6 tests PASS

- [ ] **Step 3: Commit**

```bash
git add generate_flag_names.py
git commit -m "feat: implement generate_search_names function"
```

---

## Task 8: Add Unit Tests for merge_emoji_names

**Files:**
- Modify: `test_generate_flag_names.py`

- [ ] **Step 1: Add test class for merge_emoji_names**

Append to `test_generate_flag_names.py`:

```python
from generate_flag_names import (
    extract_flag_data, 
    match_flags_to_emoji_list, 
    generate_search_names,
    merge_emoji_names
)


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest test_generate_flag_names.py::TestMergeEmojiNames -v`

Expected: FAIL with "ImportError: cannot import name 'merge_emoji_names'"

- [ ] **Step 3: Commit**

```bash
git add test_generate_flag_names.py
git commit -m "test: add unit tests for merge_emoji_names"
```

---

## Task 9: Implement merge_emoji_names Function

**Files:**
- Modify: `generate_flag_names.py`

- [ ] **Step 1: Add merge_emoji_names function**

Add after `generate_search_names` function in `generate_flag_names.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it passes**

Run: `python3 -m pytest test_generate_flag_names.py::TestMergeEmojiNames -v`

Expected: All 6 tests PASS

- [ ] **Step 3: Commit**

```bash
git add generate_flag_names.py
git commit -m "feat: implement merge_emoji_names function"
```

---

## Task 10: Add Unit Tests for update_index_html

**Files:**
- Modify: `test_generate_flag_names.py`

- [ ] **Step 1: Add test class for update_index_html**

Append to `test_generate_flag_names.py`:

```python
from generate_flag_names import (
    extract_flag_data, 
    match_flags_to_emoji_list, 
    generate_search_names,
    merge_emoji_names,
    update_index_html
)
import tempfile
import os


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest test_generate_flag_names.py::TestUpdateIndexHtml -v`

Expected: FAIL with "ImportError: cannot import name 'update_index_html'"

- [ ] **Step 3: Commit**

```bash
git add test_generate_flag_names.py
git commit -m "test: add unit tests for update_index_html"
```

---

## Task 11: Implement update_index_html Function

**Files:**
- Modify: `generate_flag_names.py`

- [ ] **Step 1: Add update_index_html function**

Add after `merge_emoji_names` function in `generate_flag_names.py`:

```python
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
    pattern = r"const EMOJI_NAMES\s*=\s*\{([^}]+)\};"
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
```

- [ ] **Step 2: Run test to verify it passes**

Run: `python3 -m pytest test_generate_flag_names.py::TestUpdateIndexHtml -v`

Expected: All 5 tests PASS

- [ ] **Step 3: Commit**

```bash
git add generate_flag_names.py
git commit -m "feat: implement update_index_html function"
```

---

## Task 12: Add Main Execution Logic

**Files:**
- Modify: `generate_flag_names.py`

- [ ] **Step 1: Add main function with complete flow**

Add at the end of `generate_flag_names.py` (replace the `if __name__ == '__main__': pass` block):

```python
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
```

- [ ] **Step 2: Run all unit tests to verify nothing is broken**

Run: `python3 -m pytest test_generate_flag_names.py -v`

Expected: All tests PASS

- [ ] **Step 3: Commit**

```bash
git add generate_flag_names.py
git commit -m "feat: add main execution logic"
```

---

## Task 13: Create Integration Test

**Files:**
- Create: `test_integration.py`

- [ ] **Step 1: Create integration test script**

```python
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
        # 1. Create test index.html
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
        
        # 2. Create test emoji data
        emoji_data_path = os.path.join(test_dir, 'data-by-emoji.json')
        emoji_data = {
            '🇨🇳': {'name': 'flag China', 'group': 'Flags'},
            '🇺🇸': {'name': 'flag United States', 'group': 'Flags'},
            '🇯🇵': {'name': 'flag Japan', 'group': 'Flags'}
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
        from generate_flag_names import main
        
        result = main()
        
        # 6. Verify results
        if not result:
            print("❌ main() returned False")
            return False
        
        # 7. Check updated index.html
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that flags were added
        if 'flag China CN' not in content:
            print("❌ 'flag China CN' not found in output")
            return False
        
        if '中国' not in content:
            print("❌ '中国' not found in output")
            return False
        
        if 'flag United States US' not in content:
            print("❌ 'flag United States US' not found in output")
            return False
        
        if '美国' not in content:
            print("❌ '美国' not found in output")
            return False
        
        if 'flag Japan JP' not in content:
            print("❌ 'flag Japan JP' not found in output")
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
```

- [ ] **Step 2: Run integration test**

Run: `python3 test_integration.py`

Expected: `✅ Integration test passed!`

- [ ] **Step 3: Commit**

```bash
git add test_integration.py
git commit -m "test: add integration test for flag search names"
```

---

## Task 14: Create Validation Script

**Files:**
- Create: `validate_flag_names.py`

- [ ] **Step 1: Create validation script**

```python
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
    
    match = re.search(r"const EMOJI_NAMES\s*=\s*\{([^}]+)\};", content, re.DOTALL)
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
```

- [ ] **Step 2: Run validation script**

Run: `python3 validate_flag_names.py`

Expected: `✅ All flag search names format correct`

- [ ] **Step 3: Commit**

```bash
git add validate_flag_names.py
git commit -m "feat: add validation script for flag search names"
```

---

## Task 15: Run Complete Workflow

**Files:**
- Modify: `index.html` (via generate_flag_names.py)

- [ ] **Step 1: Run all unit tests**

Run: `python3 -m pytest test_generate_flag_names.py -v`

Expected: All tests PASS

- [ ] **Step 2: Run integration test**

Run: `python3 test_integration.py`

Expected: `✅ Integration test passed!`

- [ ] **Step 3: Run the actual generation script**

Run: `python3 generate_flag_names.py`

Expected output:
```
🚀 Starting flag search name generation...

📖 Reading unicode-emoji-json data...
✅ Found 270 flag emojis

📖 Reading EMOJI_LIST...
✅ Found 284 flag codepoints

🔗 Matching flags...
✅ Successfully matched 267 flags
⚠️  17 flags in EMOJI_LIST unmatched

📖 Reading country/region Chinese names...
✅ Loaded 250 Chinese names

✏️  Generating search names...
✅ Generated 267 flag search names

📝 Updating index.html...
✅ Successfully updated EMOJI_NAMES

==================================================
📊 Generation Report:
✅ Successfully generated 267 flag search names
⚠️  17 flags unmatched
==================================================
```

- [ ] **Step 4: Run validation script**

Run: `python3 validate_flag_names.py`

Expected: `✅ All flag search names format correct`

- [ ] **Step 5: Verify index.html was updated**

Run: `grep -c "flag.*CN\|flag.*US\|flag.*JP" index.html`

Expected: `3` (or similar count showing flags were added)

- [ ] **Step 6: Commit the updated index.html**

```bash
git add index.html
git commit -m "feat: add 267 flag search names to EMOJI_NAMES"
```

---

## Task 16: Final Verification

- [ ] **Step 1: Run all tests one final time**

Run: `python3 -m pytest test_generate_flag_names.py -v && python3 test_integration.py`

Expected: All tests PASS

- [ ] **Step 2: Open index.html in browser and test search**

Manual verification:
- Search "中国" → should show China flag
- Search "china" → should show China flag
- Search "CN" → should show China flag
- Search "flag" → should show all flags

- [ ] **Step 3: Verify commit history**

Run: `git log --oneline -10`

Expected: Clean commit history with all tasks completed

---

## Self-Review Checklist

### Spec Coverage

- ✅ Add search names for all 267 flag emojis
- ✅ Support search by English country name, country code, and Chinese name
- ✅ Create an automated, repeatable process
- ✅ Maintain consistency with existing EMOJI_NAMES format
- ✅ Naming strategy: `flag {country_name} {country_code}`
- ✅ Chinese names: Standard country/region names
- ✅ Manual review via validation script

### Placeholder Scan

- ✅ No "TBD" or "TODO" markers
- ✅ All code blocks are complete
- ✅ All commands have expected outputs
- ✅ No "implement later" or "fill in details"

### Type Consistency

- ✅ `extract_flag_data()` returns `dict[str, dict]`
- ✅ `match_flags_to_emoji_list()` returns `dict[str, dict]`
- ✅ `generate_search_names()` returns `dict[str, dict]`
- ✅ `merge_emoji_names()` returns `dict[str, dict]`
- ✅ `update_index_html()` returns `bool`
- ✅ All function signatures consistent across tasks

---

*Plan generated: 2026-06-16*
*Based on design: docs/superpowers/specs/2026-06-16-flag-emoji-search-names-design.md*
