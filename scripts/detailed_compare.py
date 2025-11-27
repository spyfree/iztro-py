"""详细对比两个库的计算结果"""

from py_iztro import Astro
from iztro_py import by_solar

print("=" * 80)
print("对比 1989-10-17 午时的排盘")
print("=" * 80)

# py-iztro
py_astro = Astro()
py_result = py_astro.by_solar('1989-10-17', 11, 'male', True, 'zh-CN')

# iztro-py
iz_result = by_solar('1989-10-17', 11, '男', True, 'zh-CN')

print("\n基本信息对比:")
print(f"{'项目':<20} {'py-iztro':<20} {'iztro-py':<20}")
print("-" * 60)
print(f"{'五行局':<20} {py_result.five_elements_class:<20} {iz_result.five_elements_class:<20}")
print(f"{'命宫地支':<20} {py_result.earthly_branch_of_soul_palace:<20} {iz_result.earthly_branch_of_soul_palace:<20}")
print(f"{'身宫地支':<20} {py_result.earthly_branch_of_body_palace:<20} {iz_result.earthly_branch_of_body_palace:<20}")

# 找到命宫
py_soul = None
for p in py_result.palaces:
    if p.earthly_branch == py_result.earthly_branch_of_soul_palace:
        py_soul = p
        break

iz_soul = None
for p in iz_result.palaces:
    if p.is_original_palace:
        iz_soul = p
        break

print(f"\n命宫详情:")
if py_soul:
    print(f"  py-iztro:")
    print(f"    宫位: {py_soul.name}")
    print(f"    地支: {py_soul.earthly_branch}")
    print(f"    天干: {py_soul.heavenly_stem}")

if iz_soul:
    print(f"  iztro-py:")
    print(f"    宫位: {iz_soul.name}")
    print(f"    地支: {iz_soul.earthly_branch}")
    print(f"    天干: {iz_soul.heavenly_stem}")

# 找到父母宫
print(f"\n父母宫详情:")
py_parent = None
for p in py_result.palaces:
    if p.name == '父母':
        py_parent = p
        break

if py_parent:
    stars = [s.name for s in py_parent.major_stars] if py_parent.major_stars else []
    print(f"  py-iztro:")
    print(f"    地支: {py_parent.earthly_branch}")
    print(f"    天干: {py_parent.heavenly_stem}")
    print(f"    主星: {stars if stars else '无主星'}")

iz_parent = iz_result.palace('父母宫')
if iz_parent:
    stars = [s.name for s in iz_parent.major_stars]
    print(f"  iztro-py:")
    print(f"    地支: {iz_parent.earthly_branch}")
    print(f"    天干: {iz_parent.heavenly_stem}")
    print(f"    主星: {stars if stars else '无主星'}")

print(f"\n所有宫位对比:")
print(f"{'py-iztro':<40} {'iztro-py':<40}")
print("-" * 80)

for py_p, iz_p in zip(py_result.palaces, iz_result.palaces):
    py_stars = [s.name for s in py_p.major_stars] if py_p.major_stars else []
    py_str = f"{py_p.name}({py_p.earthly_branch}): {', '.join(py_stars) if py_stars else '无'}"

    iz_stars = [s.name for s in iz_p.major_stars]
    iz_str = f"{iz_p.name}({iz_p.earthly_branch}): {', '.join(iz_stars) if iz_stars else '无'}"

    match = "✓" if py_p.earthly_branch == iz_p.earthly_branch else "✗"
    print(f"{py_str:<40} {iz_str:<40} {match}")
