"""调试主星位置计算"""

from iztro_py.data.types import FiveElementsClass
from iztro_py.star.location import get_star_indices, get_major_star_positions
from iztro_py.data.constants import EARTHLY_BRANCHES

# 1989-10-17 午时的参数
five_elements_class = FiveElementsClass.WOOD_3
lunar_day = 18  # 农历九月十八

print("=" * 80)
print("调试主星位置计算")
print("=" * 80)

print(f"\n输入参数:")
print(f"  五行局: {five_elements_class}")
print(f"  农历日: {lunar_day}")

# 计算紫微和天府的位置
ziwei_index, tianfu_index = get_star_indices(five_elements_class, lunar_day)

print(f"\n紫微星和天府星位置:")
print(f"  紫微星索引: {ziwei_index}, 地支: {EARTHLY_BRANCHES[ziwei_index]}")
print(f"  天府星索引: {tianfu_index}, 地支: {EARTHLY_BRANCHES[tianfu_index]}")

# 获取所有主星位置
star_positions = get_major_star_positions(ziwei_index, tianfu_index)

print(f"\n所有主星位置:")
for star_name, palace_index in sorted(star_positions.items(), key=lambda x: x[1]):
    branch = EARTHLY_BRANCHES[palace_index]
    print(f"  {star_name}: 索引{palace_index}, 地支{branch}")

# 检查父母宫（索引1，即命宫+1）的主星
# 命宫在索引0（辰），父母宫在索引1（巳）
print(f"\n父母宫（索引1，巳）的主星:")
parents_palace_stars = [name for name, idx in star_positions.items() if idx == 1]
if parents_palace_stars:
    print(f"  {', '.join(parents_palace_stars)}")
else:
    print(f"  无主星")

# 注意：宫位索引和地支索引是两回事
# 宫位索引：0=命宫, 1=父母宫, 2=福德宫...
# 地支索引：0=子, 1=丑, 2=寅, 3=卯, 4=辰, 5=巳...
#
# 如果命宫在辰（地支索引4），那么：
# - 宫位索引0 = 地支索引4（辰）- 命宫
# - 宫位索引1 = 地支索引5（巳）- 父母宫
# - ...
