# -*- coding: utf-8 -*-
"""
iztro-py 完整多语言支持示例

展示所有支持的6种语言：
- 简体中文 (zh-CN)
- 繁體中文 (zh-TW)
- English (en-US)
- 日本語 (ja-JP)
- 한국어 (ko-KR)
- Tiếng Việt (vi-VN)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from iztro_py import astro

# 所有支持的语言
LANGUAGES = [
    ('zh-CN', '简体中文', 'Simplified Chinese'),
    ('zh-TW', '繁體中文', 'Traditional Chinese'),
    ('en-US', 'English', 'English'),
    ('ja-JP', '日本語', 'Japanese'),
    ('ko-KR', '한국어', 'Korean'),
    ('vi-VN', 'Tiếng Việt', 'Vietnamese')
]

print("=" * 80)
print("iztro-py 多语言支持演示")
print("Multilingual Support Demo")
print("=" * 80)
print()

# 示例 1: 显示命宫信息（所有语言）
print("示例 1: 命宫信息 (Soul Palace Information)")
print("-" * 80)

for lang_code, lang_native, lang_english in LANGUAGES:
    chart = astro.by_solar('2000-8-16', 6, '男', language=lang_code)
    soul = chart.get_soul_palace()
    
    palace_name = soul.translate_name(lang_code)
    stem = soul.translate_heavenly_stem(lang_code)
    branch = soul.translate_earthly_branch(lang_code)
    
    stars = []
    if soul.major_stars:
        for star in soul.major_stars[:2]:  # 只显示前2颗主星
            star_name = star.translate_name(lang_code)
            brightness = star.translate_brightness(lang_code) or '-'
            stars.append(f"{star_name}({brightness})")
    
    stars_str = ', '.join(stars) if stars else '-'
    
    print(f"{lang_native:15s} ({lang_code}): {palace_name:15s} {stem}{branch}  [{stars_str}]")

print()

# 示例 2: 显示所有宫位名称（选择3种语言对比）
print("示例 2: 十二宫位对比 (12 Palaces Comparison)")
print("-" * 80)

# 选择简体中文、英文、越南语进行对比
compare_langs = [
    ('zh-CN', '简体中文'),
    ('en-US', 'English'),
    ('vi-VN', 'Tiếng Việt')
]

chart = astro.by_solar('2000-8-16', 6, '男')

print(f"{'宫位':4s}  {'简体中文':15s}  {'English':20s}  {'Tiếng Việt':20s}")
print("-" * 80)

for i in range(12):
    palace = chart.palace(i)
    if palace:
        names = []
        for lang_code, _ in compare_langs:
            names.append(palace.translate_name(lang_code))
        
        marker = ""
        if palace.is_original_palace:
            marker = "●命"
        elif palace.is_body_palace:
            marker = "○身"
        
        print(f"{i:2d}{marker:4s}  {names[0]:15s}  {names[1]:20s}  {names[2]:20s}")

print()

# 示例 3: 主星名称对比（14主星）
print("示例 3: 十四主星名称对比 (14 Major Stars Comparison)")
print("-" * 80)

major_star_keys = [
    'ziweiMaj', 'tianjiMaj', 'taiyangMaj', 'wuquMaj',
    'tiantongMaj', 'lianzhenMaj', 'tianfuMaj', 'taiyinMaj',
    'tanlangMaj', 'jumenMaj', 'tianxiangMaj', 'tianliangMaj',
    'qishaMaj', 'pojunMaj'
]

print(f"{'序号':4s}  {'简体中文':10s}  {'繁體中文':10s}  {'日本語':10s}  {'한국어':10s}")
print("-" * 80)

from iztro_py.i18n import t

for idx, star_key in enumerate(major_star_keys, 1):
    zh_cn = t(f'stars.major.{star_key}', 'zh-CN')
    zh_tw = t(f'stars.major.{star_key}', 'zh-TW')
    ja_jp = t(f'stars.major.{star_key}', 'ja-JP')
    ko_kr = t(f'stars.major.{star_key}', 'ko-KR')
    
    print(f"{idx:2d}.   {zh_cn:10s}  {zh_tw:10s}  {ja_jp:10s}  {ko_kr:10s}")

print()

# 示例 4: 天干地支对比
print("示例 4: 天干地支对比 (Heavenly Stems & Earthly Branches)")
print("-" * 80)

heavenly_stems = ['jiaHeavenly', 'yiHeavenly', 'bingHeavenly', 'dingHeavenly', 
                   'wuHeavenly', 'jiHeavenly', 'gengHeavenly', 'xinHeavenly',
                   'renHeavenly', 'guiHeavenly']

earthly_branches = ['ziEarthly', 'chouEarthly', 'yinEarthly', 'maoEarthly',
                     'chenEarthly', 'siEarthly', 'wuEarthly', 'weiEarthly',
                     'shenEarthly', 'youEarthly', 'xuEarthly', 'haiEarthly']

print("天干 (Heavenly Stems):")
stems_zh = [t(f'heavenlyStem.{s}', 'zh-CN') for s in heavenly_stems]
stems_vi = [t(f'heavenlyStem.{s}', 'vi-VN') for s in heavenly_stems]
print(f"  中文: {' '.join(stems_zh)}")
print(f"  Việt: {' '.join(stems_vi)}")

print()
print("地支 (Earthly Branches):")
branches_zh = [t(f'earthlyBranch.{b}', 'zh-CN') for b in earthly_branches]
branches_ko = [t(f'earthlyBranch.{b}', 'ko-KR') for b in earthly_branches]
print(f"  中文: {' '.join(branches_zh)}")
print(f"  한국: {' '.join(branches_ko)}")

print()
print("=" * 80)
print("演示完成！All demos completed!")
print("=" * 80)
