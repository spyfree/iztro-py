"""简化版验证脚本"""

print("=" * 80)
print("使用 py-iztro 排盘（JavaScript 实现）")
print("=" * 80)

from py_iztro import Astro

py_astro = Astro()
py_result = py_astro.by_solar('1989-10-17', 11, 'male', True, 'zh-CN')

print(f"\n五行局: {py_result.five_elements_class}")
print(f"命宫地支: {py_result.earthly_branch_of_soul_palace}")
print(f"身宫地支: {py_result.earthly_branch_of_body_palace}")

print("\n各宫主星分布:")
for palace_data in py_result.palaces:
    major_stars = [s.name for s in palace_data.major_stars] if palace_data.major_stars else []
    stars_str = "、".join(major_stars) if major_stars else "无主星"
    palace_name = palace_data.name
    branch = palace_data.earthly_branch
    print(f"  {palace_name}({branch}): {stars_str}")

print("\n" + "=" * 80)
print("使用 iztro-py 排盘（纯 Python 实现）")
print("=" * 80)

from iztro_py import by_solar

result = by_solar('1989-10-17', 11, '男', True, 'zh-CN')

print(f"\n五行局: {result.five_elements_class}")
print(f"命宫: {result.get_soul_palace()}")
print(f"身宫: {result.get_body_palace()}")

print("\n各宫主星分布:")
for palace in result.palaces:
    major_stars = [s.name for s in palace.major_stars]
    stars_str = "、".join(major_stars) if major_stars else "无主星"
    branch = palace.earthly_branch
    print(f"  {palace.name}({branch}): {stars_str}")
