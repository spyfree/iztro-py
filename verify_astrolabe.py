"""验证脚本：对比 py-iztro 和 iztro-py 的排盘结果"""

import json
from datetime import datetime

# 使用 py-iztro (JavaScript wrapper)
try:
    from py_iztro import Astro

    print("=" * 80)
    print("使用 py-iztro 排盘（JavaScript 实现）")
    print("=" * 80)

    # 1989-10-17 午时
    py_astro = Astro()
    py_result = py_astro.by_solar(
        '1989-10-17',
        11,  # 午时
        'male',
        True,
        'zh-CN'
    )

    print(f"\n命宫: {py_result.palace.name[0]}")
    print(f"身宫: {py_result.palace.name[1]}")
    print(f"五行局: {py_result.five_elements_class}")

    print("\n各宫主星分布:")
    for palace_name, palace_data in py_result.palaces.items():
        major_stars = [s.name for s in palace_data.major_stars]
        stars_str = "、".join(major_stars) if major_stars else "无主星"
        print(f"  {palace_name}: {stars_str}")

    print("\n父母宫详情:")
    parents_palace = py_result.palaces['父母']
    print(f"  地支: {parents_palace.earthly_branch}")
    print(f"  天干: {parents_palace.heavenly_stem}")
    major_stars = [s.name for s in parents_palace.major_stars]
    print(f"  主星: {major_stars if major_stars else '无主星'}")

except Exception as e:
    print(f"py-iztro 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("使用 iztro-py 排盘（纯 Python 实现）")
print("=" * 80)

# 使用 iztro-py (纯 Python)
try:
    from iztro_py import by_solar

    result = by_solar('1989-10-17', 11, '男', True, 'zh-CN')

    print(f"\n命宫: {result.get_soul_palace()}")
    print(f"身宫: {result.get_body_palace()}")
    print(f"五行局: {result.astrolabe.five_elements_class}")

    print("\n各宫主星分布:")
    for palace in result.astrolabe.palaces:
        major_stars = [s.name for s in palace.major_stars]
        stars_str = "、".join(major_stars) if major_stars else "无主星"
        print(f"  {palace.name}: {stars_str}")

    print("\n父母宫详情:")
    parents_palace = result.palace('父母宫')
    if parents_palace:
        print(f"  地支: {parents_palace.earthly_branch}")
        print(f"  天干: {parents_palace.heavenly_stem}")
        major_stars = [s.name for s in parents_palace.major_stars]
        print(f"  主星: {major_stars if major_stars else '无主星'}")

except Exception as e:
    print(f"iztro-py 错误: {e}")
    import traceback
    traceback.print_exc()
