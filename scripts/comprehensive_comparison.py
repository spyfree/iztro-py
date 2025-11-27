"""全面对比三个库的结果"""

print("=" * 80)
print("全面对比：原始 iztro (JS)、py-iztro、iztro-py")
print("日期: 1989-10-17 午时")
print("=" * 80)

# ============================================================================
# 1. iztro-py (纯 Python 实现)
# ============================================================================
from iztro_py import by_solar as py_by_solar

print("\n" + "=" * 80)
print("1. iztro-py (纯 Python 实现)")
print("=" * 80)

# 参数说明：
# - date: '1989-10-17' (阳历)
# - time_index: 6 (午时索引)
# - gender: '男'
# - fix_leap: True
# - language: 'zh-CN'
py_result = py_by_solar('1989-10-17', 6, '男', True, 'zh-CN')

print(f"\n输入参数:")
print(f"  date: '1989-10-17'")
print(f"  time_index: 6 (午时)")
print(f"  gender: '男'")
print(f"  fix_leap: True")
print(f"  language: 'zh-CN'")

print(f"\n基本信息:")
print(f"  五行局: {py_result.five_elements_class}")
print(f"  命宫地支: {py_result.earthly_branch_of_soul_palace}")
print(f"  身宫地支: {py_result.earthly_branch_of_body_palace}")

print(f"\n父母宫:")
parents = py_result.palace('父母宫')
if parents:
    stars = [s.name for s in parents.major_stars]
    print(f"  地支: {parents.earthly_branch}")
    print(f"  天干: {parents.heavenly_stem}")
    print(f"  主星: {stars if stars else '无主星'}")

print(f"\n所有宫位主星:")
for palace in py_result.palaces:
    stars = [s.name for s in palace.major_stars]
    print(f"  {palace.name}({palace.earthly_branch}): {stars if stars else '无'}")

# ============================================================================
# 2. py-iztro (JS wrapper)
# ============================================================================
print("\n" + "=" * 80)
print("2. py-iztro (JavaScript wrapper)")
print("=" * 80)

try:
    from py_iztro import Astro

    astro = Astro()
    # 参数说明：
    # - date: '1989-10-17' (阳历)
    # - hour: 12 (小时数，午时的中间时刻)
    # - gender: 'male'
    # - fix_leap: True
    # - language: 'zh-CN'
    js_result = astro.by_solar('1989-10-17', 12, 'male', True, 'zh-CN')

    print(f"\n输入参数:")
    print(f"  date: '1989-10-17'")
    print(f"  hour: 12 (午时，注意这是小时数不是时辰索引)")
    print(f"  gender: 'male'")
    print(f"  fix_leap: True")
    print(f"  language: 'zh-CN'")

    print(f"\n基本信息:")
    print(f"  五行局: {js_result.five_elements_class}")
    print(f"  命宫地支: {js_result.earthly_branch_of_soul_palace}")
    print(f"  身宫地支: {js_result.earthly_branch_of_body_palace}")

    print(f"\n父母宫:")
    for p in js_result.palaces:
        if p.name == '父母':
            stars = [s.name for s in p.major_stars] if p.major_stars else []
            print(f"  地支: {p.earthly_branch}")
            print(f"  天干: {p.heavenly_stem}")
            print(f"  主星: {stars if stars else '无主星'}")
            break

    print(f"\n所有宫位主星:")
    for p in js_result.palaces:
        stars = [s.name for s in p.major_stars] if p.major_stars else []
        print(f"  {p.name}({p.earthly_branch}): {stars if stars else '无'}")

except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# 3. 对比分析
# ============================================================================
print("\n" + "=" * 80)
print("3. 对比分析")
print("=" * 80)

print(f"\n关键参数差异:")
print(f"  iztro-py: time_index=6 (时辰索引), gender='男'")
print(f"  py-iztro: hour=12 (小时数), gender='male'")

print(f"\n说明:")
print(f"  - iztro-py 使用时辰索引 (0-12)，其中 6=午时")
print(f"  - py-iztro 使用小时数 (0-23)，午时可以用 11、12 或 13")
print(f"  - 两个库的性别参数格式不同：'男' vs 'male'")

# 检查命宫地支是否一致
if 'js_result' in locals():
    py_soul = py_result.earthly_branch_of_soul_palace
    js_soul = js_result.earthly_branch_of_soul_palace

    # 去掉后缀比较
    py_soul_simple = py_soul.replace('Earthly', '')

    print(f"\n命宫地支对比:")
    print(f"  iztro-py: {py_soul}")
    print(f"  py-iztro: {js_soul}")
    print(f"  是否一致: {'✓' if py_soul_simple == js_soul else '✗'}")
