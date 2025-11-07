"""检查父母宫的主星问题"""

from iztro_py import by_solar

# 1989-10-17 午时
result = by_solar('1989-10-17', 6, '男', True, 'zh-CN')

print("=" * 80)
print("1989-10-17 午时 排盘详情")
print("=" * 80)

print(f"\n基本信息:")
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
        print(f"  {name}({palace.earthly_branch}): {stars_str}")

print(f"\n父母宫详情:")
parents_palace = result.palace('父母宫')
if parents_palace:
    print(f"  地支: {parents_palace.earthly_branch}")
    print(f"  天干: {parents_palace.heavenly_stem}")
    print(f"  主星:")
    for star in parents_palace.major_stars:
        print(f"    - {star.name} (类型: {star.type}, 亮度: {star.brightness})")

# 根据紫微斗数理论，检查天府星的位置
print(f"\n天府星位置检查:")
tianfu_palace = result.star('天府')
if tianfu_palace:
    print(f"  天府星所在宫位: {tianfu_palace.palaces}")
