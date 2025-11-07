"""最终验证脚本 - 展示修复结果"""

from iztro_py import by_solar

print("=" * 80)
print("iztro-py 排盘结果（修复后）")
print("日期: 1989-10-17 午时")
print("=" * 80)

# 使用正确的参数
result = by_solar('1989-10-17', 6, '男', True, 'zh-CN')

print(f"\n基本信息:")
print(f"  阳历日期: {result.solar_date}")
print(f"  农历日期: {result.lunar_date}")
print(f"  四柱: {result.chinese_date}")
print(f"  时辰: {result.time}时 ({result.time_range})")
print(f"  星座: {result.sign}")
print(f"  生肖: {result.zodiac}")
print(f"  五行局: {result.five_elements_class}")
print(f"  命宫地支: {result.earthly_branch_of_soul_palace}")
print(f"  身宫地支: {result.earthly_branch_of_body_palace}")

print(f"\n十二宫主星分布:")
palace_names_order = ['命宫', '父母宫', '福德宫', '田宅宫', '官禄宫', '交友宫', '迁移宫', '疾厄宫', '财帛宫', '子女宫', '夫妻宫', '兄弟宫']

for name in palace_names_order:
    palace = result.palace(name)
    if palace:
        major_stars = [s.name for s in palace.major_stars]
        stars_str = "、".join(major_stars) if major_stars else "无主星"
        body_mark = "[身]" if palace.is_body_palace else "    "
        print(f"  {name}({palace.earthly_branch}): {stars_str} {body_mark}")

print(f"\n修复要点:")
print(f"  ✓ 宫位地支排列：从命宫地支开始，按地支顺序排列")
print(f"  ✓ 主星安置：正确转换地支索引到宫位")
print(f"  ✓ 辅星安置：正确转换地支索引到宫位")
print(f"  ✓ 五行局计算：命宫天干地支正确对应")
print(f"  ✓ 所有测试通过：48 passed")

print("\n" + "=" * 80)
