"""
iztro-py 基本使用示例

演示如何使用 iztro-py 库创建和查询紫微斗数星盘。
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from iztro_py import astro

# ============================================================
# 示例 1：创建星盘（使用阳历日期）
# ============================================================
print("=" * 60)
print("示例 1：创建星盘（使用阳历日期）")
print("=" * 60)

# 创建星盘：2000年8月16日午时出生的男命
chart = astro.by_solar('2000-8-16', 6, '男')

# 查看基本信息
print(f"性别: {chart.gender}")
print(f"阳历: {chart.solar_date}")
print(f"农历: {chart.lunar_date}")
print(f"四柱: {chart.chinese_date}")
print(f"生肖: {chart.zodiac}")
print(f"星座: {chart.sign}")
print(f"五行局: {chart.five_elements_class}")
print()


# ============================================================
# 示例 2：查询命宫和身宫
# ============================================================
print("=" * 60)
print("示例 2：查询命宫和身宫")
print("=" * 60)

# 获取命宫
soul_palace = chart.get_soul_palace()
print(f"命宫: {soul_palace.name}")
print(f"  天干地支: {soul_palace.heavenly_stem} {soul_palace.earthly_branch}")
print(f"  主星: {', '.join(s.name for s in soul_palace.major_stars) or '空宫'}")

# 获取身宫
body_palace = chart.get_body_palace()
print(f"\n身宫: {body_palace.name}")
print()


# ============================================================
# 示例 3：查询指定宫位
# ============================================================
print("=" * 60)
print("示例 3：查询指定宫位")
print("=" * 60)

# 通过索引查询
palace_0 = chart.palace(0)
print(f"索引 0 的宫位: {palace_0.name}")

# 通过中文名称查询
wealth_palace = chart.palace('财帛')
print(f"财帛宫: {wealth_palace.name}")
print(f"  主星: {', '.join(s.name for s in wealth_palace.major_stars) or '空宫'}")

# 通过英文名称查询
career_palace = chart.palace('career')
print(f"事业宫: {career_palace.name}")
print(f"  主星: {', '.join(s.name for s in career_palace.major_stars) or '空宫'}")
print()


# ============================================================
# 示例 4：查询星曜
# ============================================================
print("=" * 60)
print("示例 4：查询星曜")
print("=" * 60)

# 查找紫微星（使用星曜的英文名称）
ziwei = chart.star('ziweiMaj')
if ziwei:
    print(f"紫微星:")
    print(f"  亮度: {ziwei.brightness}")
    print(f"  四化: {ziwei.mutagen or '无'}")

    # 查看所在宫位
    palace = ziwei.palace()
    if palace:
        print(f"  所在宫位: {palace.name}")

    # 查看是否庙旺
    print(f"  是否庙旺: {ziwei.is_bright()}")
else:
    print("未找到紫微星")

# 查找天机星
tianji = chart.star('tianjiMaj')
if tianji:
    print(f"\n天机星:")
    print(f"  亮度: {tianji.brightness}")
    print(f"  四化: {tianji.mutagen or '无'}")
    palace = tianji.palace()
    if palace:
        print(f"  所在宫位: {palace.name}")
print()


# ============================================================
# 示例 5：宫位星曜查询
# ============================================================
print("=" * 60)
print("示例 5：宫位星曜查询")
print("=" * 60)

# 检查命宫是否包含特定星曜
soul = chart.get_soul_palace()
print(f"命宫包含天机星: {soul.has(['tianjiMaj'])}")
print(f"命宫包含紫微星: {soul.has(['ziweiMaj'])}")

# 检查是否有化禄星
print(f"命宫有化禄: {soul.has_mutagen('禄')}")

# 检查是否为空宫
print(f"命宫是否空宫: {soul.is_empty()}")
print()


# ============================================================
# 示例 6：三方四正查询
# ============================================================
print("=" * 60)
print("示例 6：三方四正查询")
print("=" * 60)

# 获取命宫的三方四正
soul = chart.get_soul_palace()
surpalaces = chart.surrounded_palaces(soul.index)

if surpalaces:
    print(f"命宫三方四正:")
    for p in surpalaces.all_palaces():
        major = ', '.join(s.name for s in p.major_stars) or '空'
        print(f"  {p.name}: {major}")

    # 检查三方四正是否有特定星曜
    print(f"\n三方四正是否有紫微: {surpalaces.have(['ziweiMaj'])}")
    print(f"三方四正是否有化禄: {surpalaces.have_mutagen('禄')}")
print()


# ============================================================
# 示例 7：遍历所有宫位
# ============================================================
print("=" * 60)
print("示例 7：遍历所有宫位")
print("=" * 60)

for i in range(12):
    palace = chart.palace(i)
    if palace:
        # 标记命宫和身宫
        markers = []
        if palace.is_original_palace:
            markers.append("命")
        if palace.is_body_palace:
            markers.append("身")
        marker = f"[{'/'.join(markers)}]" if markers else ""

        # 获取主星
        major = ', '.join(s.name for s in palace.major_stars) or '空'

        # 获取四化星
        mutagen_stars = [
            f"{s.name}化{s.mutagen}"
            for s in palace.major_stars + palace.minor_stars
            if s.mutagen
        ]
        mutagen_str = ', '.join(mutagen_stars) if mutagen_stars else ''

        print(f"{i:2d}. {palace.name:15s}{marker:8s} {major:25s} {mutagen_str}")
print()


# ============================================================
# 示例 8：使用农历日期
# ============================================================
print("=" * 60)
print("示例 8：使用农历日期")
print("=" * 60)

# 使用农历日期创建星盘
chart2 = astro.by_lunar('2000-7-17', 6, '男')
print(f"阳历: {chart2.solar_date}")
print(f"农历: {chart2.lunar_date}")
print(f"生肖: {chart2.zodiac}")
print()


# ============================================================
# 示例 9：便捷函数
# ============================================================
print("=" * 60)
print("示例 9：便捷函数")
print("=" * 60)

# 直接获取生肖
zodiac = astro.get_zodiac_by_solar_date('2000-8-16')
print(f"2000-8-16 的生肖: {zodiac}")

# 直接获取星座
sign = astro.get_sign_by_solar_date('2000-8-16')
print(f"2000-8-16 的星座: {sign}")
print()


print("=" * 60)
print("示例完成！")
print("=" * 60)
