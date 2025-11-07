"""检查时辰索引"""

from iztro_py.utils.calendar import get_time_index

# 用户提供的信息：
# 四柱：己巳年甲戌月己未日 庚午时
# 时辰：午时
# 时间段：11:00~13:00

# 午时对应的 hour 参数
hour_11 = get_time_index(11)
hour_12 = get_time_index(12)
hour_13 = get_time_index(13)

print("11点对应的时辰索引:", hour_11)
print("12点对应的时辰索引:", hour_12)
print("13点对应的时辰索引:", hour_13)

# 测试不同时辰的排盘
from iztro_py import by_solar

for hour in [11, 12, 13]:
    result = by_solar('1989-10-17', hour, '男', True, 'zh-CN')
    time_idx = get_time_index(hour)
    print(f"\nhour={hour} (时辰索引={time_idx}):")
    print(f"  命宫地支: {result.earthly_branch_of_soul_palace}")
    print(f"  身宫地支: {result.earthly_branch_of_body_palace}")
    print(f"  五行局: {result.five_elements_class}")
    print(f"  命宫: {result.get_soul_palace()}")
