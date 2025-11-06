"""
iztro-py 运势系统使用示例

演示如何使用运势系统查询大限、流年、流月、流日、流时等信息。
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from iztro_py import astro

# ============================================================
# 示例 1：查询完整运势信息
# ============================================================
print("=" * 60)
print("示例 1：查询完整运势信息")
print("=" * 60)

# 创建星盘：2000年8月16日午时出生的男命
chart = astro.by_solar('2000-8-16', 6, '男')

print(f"出生日期: {chart.solar_date}")
print(f"性别: {chart.gender}")
print(f"生肖: {chart.zodiac}")
print(f"五行局: {chart.five_elements_class}")
print()

# 查询2024年1月1日午时的运势
horoscope = chart.horoscope('2024-1-1', 6)

print(f"查询日期: {horoscope.solar_date} ({horoscope.lunar_date})")
print(f"虚岁: {horoscope.nominal_age}")
print()

# 大限（10年一运）
print(f"【大限】{horoscope.decadal.name}")
print(f"  所在宫位: {', '.join(horoscope.decadal.palace_names)}")
print(f"  天干地支: {horoscope.decadal.heavenly_stem} {horoscope.decadal.earthly_branch}")
decadal_palace = chart.palace(horoscope.decadal.index)
if decadal_palace:
    stars = ', '.join(s.name for s in decadal_palace.major_stars) or '空宫'
    print(f"  宫内主星: {stars}")
print()

# 小限（1年一运）
print(f"【小限】{horoscope.age.name}")
print(f"  所在宫位: {', '.join(horoscope.age.palace_names)}")
age_palace = chart.palace(horoscope.age.index)
if age_palace:
    stars = ', '.join(s.name for s in age_palace.major_stars) or '空宫'
    print(f"  宫内主星: {stars}")
print()

# 流年
print(f"【流年】{horoscope.yearly.name}")
print(f"  流年命宫在本命: {', '.join(horoscope.yearly.palace_names)}")
yearly_palace = chart.palace(horoscope.yearly.index)
if yearly_palace:
    stars = ', '.join(s.name for s in yearly_palace.major_stars) or '空宫'
    print(f"  宫内主星: {stars}")
    print(f"  流年四化: {', '.join(horoscope.yearly.mutagen[:4])}")
print()

# 流月
print(f"【流月】{horoscope.monthly.name}")
print(f"  流月命宫在本命: {', '.join(horoscope.monthly.palace_names)}")
print()

# 流日
print(f"【流日】{horoscope.daily.name}")
print(f"  流日命宫在本命: {', '.join(horoscope.daily.palace_names)}")
print()

# 流时
print(f"【流时】{horoscope.hourly.name}")
print(f"  流时命宫在本命: {', '.join(horoscope.hourly.palace_names)}")
print()


# ============================================================
# 示例 2：追踪一年中的运势变化
# ============================================================
print("=" * 60)
print("示例 2：追踪一年中的运势变化")
print("=" * 60)

chart = astro.by_solar('1990-1-1', 0, '女')

# 查看2024年1、4、7、10月的运势
months = ['2024-1-1', '2024-4-1', '2024-7-1', '2024-10-1']

for date_str in months:
    h = chart.horoscope(date_str, 0)
    print(f"{date_str}")
    print(f"  流月: {h.monthly.name}, 宫位: {h.monthly.palace_names[0]}")
    monthly_palace = chart.palace(h.monthly.index)
    if monthly_palace:
        stars = ', '.join(s.name for s in monthly_palace.major_stars) or '空'
        print(f"  主星: {stars}")
    print()


# ============================================================
# 示例 3：大限分析（每10年的运程）
# ============================================================
print("=" * 60)
print("示例 3：大限分析（每10年的运程）")
print("=" * 60)

chart = astro.by_solar('2000-8-16', 6, '男')

print(f"出生: {chart.solar_date}, {chart.gender}, {chart.five_elements_class}")
print()

# 分析从10岁到50岁的大限
ages = [10, 20, 30, 40, 50]

for age in ages:
    # 假设查询该年龄的1月1日
    birth_year = 2000
    query_year = birth_year + age - 1  # 虚岁
    h = chart.horoscope(f'{query_year}-1-1', 6)

    print(f"{age}岁 ({query_year}年)")
    print(f"  大限: {h.decadal.name}")
    decadal_palace = chart.palace(h.decadal.index)
    if decadal_palace:
        print(f"  宫位: {decadal_palace.name}")
        stars = ', '.join(s.name for s in decadal_palace.major_stars) or '空宫'
        print(f"  主星: {stars}")
    print()


# ============================================================
# 示例 4：结合三方四正分析流年
# ============================================================
print("=" * 60)
print("示例 4：结合三方四正分析流年")
print("=" * 60)

chart = astro.by_solar('2000-8-16', 6, '男')
horoscope = chart.horoscope('2024-6-15', 6)

print(f"查询日期: 2024-6-15")
print(f"流年: {horoscope.yearly.name}")
print()

# 获取流年命宫
yearly_palace = chart.palace(horoscope.yearly.index)
if yearly_palace:
    print(f"流年命宫在本命: {yearly_palace.name}")
    stars = ', '.join(s.name for s in yearly_palace.major_stars) or '空'
    print(f"  主星: {stars}")
    print()

    # 查看流年命宫的三方四正
    surpalaces = chart.surrounded_palaces(horoscope.yearly.index)
    if surpalaces:
        print("流年命宫三方四正:")
        for p in surpalaces.all_palaces():
            stars_list = ', '.join(s.name for s in p.major_stars) or '空'
            # 显示四化星
            mutagen_stars = [f"{s.name}化{s.mutagen}" for s in p.major_stars if s.mutagen]
            mutagen_str = f" ({', '.join(mutagen_stars)})" if mutagen_stars else ""
            print(f"  {p.name:15s}: {stars_list}{mutagen_str}")
        print()

        # 分析三方四正的吉凶
        print("三方四正分析:")
        has_lu = surpalaces.have_mutagen('禄')
        has_ji = surpalaces.have_mutagen('忌')
        print(f"  有化禄: {'是' if has_lu else '否'}")
        print(f"  有化忌: {'是' if has_ji else '否'}")
        print()


# ============================================================
# 示例 5：男女命大限对比
# ============================================================
print("=" * 60)
print("示例 5：男女命大限对比（同日同时）")
print("=" * 60)

# 同一天同一时辰出生的男女命
chart_male = astro.by_solar('2000-8-16', 6, '男')
chart_female = astro.by_solar('2000-8-16', 6, '女')

query_date = '2024-1-1'
h_male = chart_male.horoscope(query_date, 6)
h_female = chart_female.horoscope(query_date, 6)

print(f"出生: 2000-8-16 午时")
print(f"查询: {query_date}")
print()

print("男命:")
print(f"  大限: {h_male.decadal.name}, 宫位: {h_male.decadal.palace_names[0]}")
decadal_male = chart_male.palace(h_male.decadal.index)
if decadal_male:
    stars = ', '.join(s.name for s in decadal_male.major_stars) or '空'
    print(f"  主星: {stars}")
print()

print("女命:")
print(f"  大限: {h_female.decadal.name}, 宫位: {h_female.decadal.palace_names[0]}")
decadal_female = chart_female.palace(h_female.decadal.index)
if decadal_female:
    stars = ', '.join(s.name for s in decadal_female.major_stars) or '空'
    print(f"  主星: {stars}")
print()

print("注: 男女命大限顺逆行不同，因此相同年龄的大限宫位也不同")
print()


print("=" * 60)
print("示例完成！")
print("=" * 60)
