"""调试五行局计算"""

from iztro_py.data.constants import HEAVENLY_STEMS, EARTHLY_BRANCHES, FIVE_ELEMENTS_CLASS_LOOKUP
from iztro_py.utils.helpers import get_five_elements_class

# 测试：命宫在亥，天干是乙
heavenly_stem = 'yiHeavenly'  # 乙
earthly_branch = 'haiEarthly'  # 亥

stem_index = HEAVENLY_STEMS.index(heavenly_stem)
branch_index = EARTHLY_BRANCHES.index(earthly_branch)

print(f"命宫天干: {heavenly_stem} (索引: {stem_index})")
print(f"命宫地支: {earthly_branch} (索引: {branch_index})")
print(f"查表值: {FIVE_ELEMENTS_CLASS_LOOKUP[stem_index][branch_index]}")

five_elements_class = get_five_elements_class(heavenly_stem, earthly_branch)
print(f"五行局: {five_elements_class}")

# 打印查表的完整信息
print("\n完整的五行局查找表 (天干 x 地支):")
print("    ", "  ".join([f"{i:2d}" for i in range(12)]))
print("    ", "  ".join([EARTHLY_BRANCHES[i][:2] for i in range(12)]))
for i, stem in enumerate(HEAVENLY_STEMS):
    values = FIVE_ELEMENTS_CLASS_LOOKUP[i]
    print(f"{stem[:2]}: {', '.join([str(v) for v in values])}")

# 验证：根据 py-iztro 的结果，命宫在亥，天干是乙，应该是火六局
print(f"\n根据 py-iztro：命宫在亥，天干是乙，应该是火六局")
print(f"iztro-py 计算结果：{five_elements_class}")
