"""检查戊+辰的五行局"""

from iztro_py.data.constants import HEAVENLY_STEMS, EARTHLY_BRANCHES, FIVE_ELEMENTS_CLASS_LOOKUP
from iztro_py.utils.helpers import get_five_elements_class, get_five_elements_class_name

# 命宫天干：戊
# 命宫地支：辰

stem = 'wuHeavenly'  # 戊
branch = 'chenEarthly'  # 辰

stem_idx = HEAVENLY_STEMS.index(stem)
branch_idx = EARTHLY_BRANCHES.index(branch)

print(f"命宫天干: {stem} (索引: {stem_idx})")
print(f"命宫地支: {branch} (索引: {branch_idx})")
print(f"\n查找表:")
print(f"FIVE_ELEMENTS_CLASS_LOOKUP[{stem_idx}][{branch_idx}] = {FIVE_ELEMENTS_CLASS_LOOKUP[stem_idx][branch_idx]}")

five_class = get_five_elements_class(stem, branch)
class_name = get_five_elements_class_name(five_class)

print(f"\n五行局: {class_name}")
print(f"五行局枚举: {five_class}")

# 打印戊那一行
print(f"\n天干戊的完整五行局表:")
print("地支:  ", " ".join([f"{EARTHLY_BRANCHES[i][:2]:>3}" for i in range(12)]))
print("      ", " ".join([f"{i:>3}" for i in range(12)]))
print(f"戊({stem_idx}):  ", " ".join([f"{v:>3}" for v in FIVE_ELEMENTS_CLASS_LOOKUP[stem_idx]]))

# 根据用户数据，应该是木三局
print(f"\n用户数据显示应该是: 木三局")
print(f"iztro-py计算结果: {class_name}")
print(f"是否匹配: {'✓' if class_name == '木三局' else '✗'}")
