"""正确的验证脚本 - 使用正确的时辰索引"""

from py_iztro import Astro
from iztro_py import by_solar

print("=" * 80)
print("对比 1989-10-17 午时(时辰索引=6)的排盘")
print("=" * 80)

# py-iztro
# 注意：py-iztro 的 by_solar 第二个参数是小时数，不是时辰索引
py_astro = Astro()
py_result = py_astro.by_solar('1989-10-17', 12, 'male', True, 'zh-CN')  # 12点是午时中间

# iztro-py
# iztro-py 的 by_solar 第二个参数是时辰索引
# 午时索引 = 6
iz_result = by_solar('1989-10-17', 6, '男', True, 'zh-CN')

print("\n基本信息对比:")
print(f"{'项目':<20} {'py-iztro':<30} {'iztro-py':<30}")
print("-" * 80)
print(f"{'五行局':<20} {py_result.five_elements_class:<30} {iz_result.five_elements_class:<30}")
print(f"{'命宫地支':<20} {py_result.earthly_branch_of_soul_palace:<30} {iz_result.earthly_branch_of_soul_palace:<30}")
print(f"{'身宫地支':<20} {py_result.earthly_branch_of_body_palace:<30} {iz_result.earthly_branch_of_body_palace:<30}")

# 找到命宫
py_soul = None
for p in py_result.palaces:
    if p.earthly_branch == py_result.earthly_branch_of_soul_palace:
        py_soul = p
        break

iz_soul = iz_result.palace('命宫')

print(f"\n命宫详情:")
if py_soul:
    print(f"  py-iztro:")
    print(f"    地支: {py_soul.earthly_branch}")
    print(f"    天干: {py_soul.heavenly_stem}")

if iz_soul:
    print(f"  iztro-py:")
    print(f"    地支: {iz_soul.earthly_branch}")
    print(f"    天干: {iz_soul.heavenly_stem}")

# 父母宫
py_parent = None
for p in py_result.palaces:
    if p.name == '父母':
        py_parent = p
        break

iz_parent = iz_result.palace('父母宫')

print(f"\n父母宫详情:")
if py_parent:
    stars = [s.name for s in py_parent.major_stars] if py_parent.major_stars else []
    print(f"  py-iztro:")
    print(f"    地支: {py_parent.earthly_branch}")
    print(f"    天干: {py_parent.heavenly_stem}")
    print(f"    主星: {stars if stars else '无主星'}")

if iz_parent:
    stars = [s.name for s in iz_parent.major_stars]
    print(f"  iztro-py:")
    print(f"    地支: {iz_parent.earthly_branch}")
    print(f"    天干: {iz_parent.heavenly_stem}")
    print(f"    主星: {stars if stars else '无主星'}")

print(f"\n所有宫位主星对比:")
print(f"{'宫位':<15} {'py-iztro':<35} {'iztro-py':<35} {'匹配':<5}")
print("-" * 90)

palace_names = ['命宫', '父母宫', '福德宫', '田宅宫', '官禄宫', '仆役宫', '迁移宫', '疾厄宫', '财帛宫', '子女宫', '夫妻宫', '兄弟宫']
py_palace_map = {p.name: p for p in py_result.palaces}

for name in palace_names:
    py_p = py_palace_map.get(name.replace('宫', ''))
    iz_name = name if name != '仆役宫' else '交友宫'
    iz_p = iz_result.palace(iz_name)

    if py_p and iz_p:
        py_stars = [s.name for s in py_p.major_stars] if py_p.major_stars else []
        iz_stars = [s.name for s in iz_p.major_stars]

        py_str = f"{py_p.earthly_branch}: {', '.join(py_stars) if py_stars else '无'}"
        iz_str = f"{iz_p.earthly_branch}: {', '.join(iz_stars) if iz_stars else '无'}"

        # 简单对比地支是否相同（去掉后缀）
        py_branch = py_p.earthly_branch
        iz_branch_simple = iz_p.earthly_branch.replace('Earthly', '')

        match = "✓" if len(py_stars) == len(iz_stars) else "✗"
        print(f"{name:<15} {py_str:<35} {iz_str:<35} {match:<5}")
