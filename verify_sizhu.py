"""验证四柱计算的正确性"""

from iztro_py.utils.calendar import get_heavenly_stem_and_earthly_branch_date, solar_to_lunar

print("=" * 80)
print("验证 1989-10-17 的四柱")
print("=" * 80)

# 测试不同时辰
test_cases = [
    (11, "巳时 (9-11点)"),
    (12, "午时 (11-13点，正午)"),
    (13, "未时 (13-15点)"),
]

for hour, desc in test_cases:
    print(f"\n{desc} - hour={hour}")
    print("-" * 80)

    # 阳历转农历
    lunar = solar_to_lunar(1989, 10, 17, True)
    print(f"农历: {lunar.year}年{lunar.month}月{lunar.day}日")

    # 根据小时数计算时辰索引
    # 0: 早子时 00:00~01:00
    # 1: 丑时 01:00~03:00
    # ...
    # 6: 午时 11:00~13:00
    if hour == 0:
        time_index = 0  # 早子时
    elif hour == 23:
        time_index = 12  # 晚子时
    else:
        time_index = (hour + 1) // 2

    print(f"时辰索引: {time_index}")

    # 计算四柱
    sizhu = get_heavenly_stem_and_earthly_branch_date(
        1989, 10, 17, time_index, lunar.month
    )

    # 获取中文表示
    from iztro_py.i18n import t
    year_stem = t(sizhu.year_stem)
    year_branch = t(sizhu.year_branch)
    month_stem = t(sizhu.month_stem)
    month_branch = t(sizhu.month_branch)
    day_stem = t(sizhu.day_stem)
    day_branch = t(sizhu.day_branch)
    time_stem = t(sizhu.time_stem)
    time_branch = t(sizhu.time_branch)

    print(f"四柱: {year_stem}{year_branch}年 "
          f"{month_stem}{month_branch}月 "
          f"{day_stem}{day_branch}日 "
          f"{time_stem}{time_branch}时")

print("\n" + "=" * 80)
print("用户提供的四柱")
print("=" * 80)
print("己巳年 甲戌月 己未日 庚午时")
print("\n说明：如果午时（11-13点）计算出的四柱与用户数据匹配，则 iztro-py 是正确的")
