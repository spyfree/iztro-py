"""
Star positioning algorithms for iztro-py

Contains core algorithms for calculating positions of major stars,
especially Ziwei (紫微) and Tianfu (天府).
"""

from typing import Tuple
from iztro_py.data.types import FiveElementsClass
from iztro_py.data.constants import fix_index, ZIWEI_START_POSITIONS


def get_ziwei_index(five_elements_class: FiveElementsClass, lunar_day: int) -> int:
    """
    计算紫微星所在宫位索引

    口诀：六五四三二，酉午亥辰丑

    算法：
    1. 根据五行局确定起始宫位
       - 水二局：从酉宫(9)起
       - 木三局：从午宫(6)起
       - 金四局：从亥宫(11)起
       - 土五局：从辰宫(4)起
       - 火六局：从丑宫(1)起

    2. 从起始宫位开始，按照五行局数值为一个循环
       每个循环对应一定天数的农历日期

    3. 循环计算直到找到包含农历日的范围

    Args:
        five_elements_class: 五行局
        lunar_day: 农历日 (1-30)

    Returns:
        紫微星所在宫位索引 (0-11)
    """
    # 五行局数值
    class_value = five_elements_class.value  # 2, 3, 4, 5, or 6

    # 起始宫位索引
    # 水2->酉9, 木3->午6, 金4->亥11, 土5->辰4, 火6->丑1
    start_positions = {
        2: 9,   # 水二局：酉宫
        3: 6,   # 木三局：午宫
        4: 11,  # 金四局：亥宫
        5: 4,   # 土五局：辰宫
        6: 1    # 火六局：丑宫
    }

    start_pos = start_positions[class_value]

    # 计算紫微星位置
    # 算法：(农历日期 - 1) // 五行局数值 = 循环次数
    # 每个循环移动一个宫位
    cycles = (lunar_day - 1) // class_value
    remainder = (lunar_day - 1) % class_value

    # 从起始宫位开始，顺行cycles个宫位
    ziwei_index = fix_index(start_pos + cycles)

    return ziwei_index


def get_tianfu_index(ziwei_index: int) -> int:
    """
    根据紫微星位置计算天府星位置

    天府星与紫微星的关系：
    紫微在寅，天府在申（相对）
    规律：天府索引 = 对宫 = (紫微索引 + 6) % 12

    实际上天府的计算是：
    寅宫(紫微) -> 申宫(天府)
    如果紫微在寅(2)，天府在子(0): 12 - 2 = 10, 不对

    正确规律：
    紫微寅(2) -> 天府子(0)
    紫微卯(3) -> 天府亥(11)
    紫微辰(4) -> 天府戌(10)
    ...

    实际公式：天府索引 = (12 - 紫微索引) % 12

    Args:
        ziwei_index: 紫微星宫位索引

    Returns:
        天府星宫位索引
    """
    # 修正后的公式
    tianfu_index = fix_index(12 - ziwei_index)

    return tianfu_index


def get_star_indices(
    five_elements_class: FiveElementsClass,
    lunar_day: int
) -> Tuple[int, int]:
    """
    获取紫微星和天府星的位置

    Args:
        five_elements_class: 五行局
        lunar_day: 农历日

    Returns:
        (紫微星索引, 天府星索引) 元组
    """
    ziwei_index = get_ziwei_index(five_elements_class, lunar_day)
    tianfu_index = get_tianfu_index(ziwei_index)

    return ziwei_index, tianfu_index


def get_major_star_positions(
    ziwei_index: int,
    tianfu_index: int
) -> dict[str, int]:
    """
    根据紫微和天府星位置，计算其他主星位置

    紫微星系（逆行）：紫微、天机、太阳、武曲、天同、廉贞
    天府星系（顺行）：天府、太阴、贪狼、巨门、天相、天梁、七杀、破军

    Args:
        ziwei_index: 紫微星宫位索引
        tianfu_index: 天府星宫位索引

    Returns:
        星曜名称到宫位索引的映射字典
    """
    from iztro_py.data.constants import ZIWEI_GROUP, TIANFU_GROUP

    positions = {}

    # 紫微星系（逆行）
    # 紫微、天机、(空)、太阳、武曲、天同、(空)、(空)、廉贞
    for offset, star_name in enumerate(ZIWEI_GROUP):
        if star_name:  # 跳过空位
            # 逆行：索引递减
            star_index = fix_index(ziwei_index - offset)
            positions[star_name] = star_index

    # 天府星系（顺行）
    # 天府、太阴、贪狼、巨门、天相、天梁、七杀、(空)、(空)、(空)、破军
    for offset, star_name in enumerate(TIANFU_GROUP):
        if star_name:  # 跳过空位
            # 顺行：索引递增
            star_index = fix_index(tianfu_index + offset)
            positions[star_name] = star_index

    return positions


def get_minor_star_position_zuofu(lunar_month: int) -> int:
    """
    计算左辅星位置（按农历月）

    口诀：正月起辰宫，顺行十二宫

    Args:
        lunar_month: 农历月 (1-12)

    Returns:
        左辅星宫位索引
    """
    # 正月在辰宫(4)
    return fix_index(4 + lunar_month - 1)


def get_minor_star_position_youbi(lunar_month: int) -> int:
    """
    计算右弼星位置（按农历月）

    口诀：正月起戌宫，逆行十二宫

    Args:
        lunar_month: 农历月 (1-12)

    Returns:
        右弼星宫位索引
    """
    # 正月在戌宫(10)
    return fix_index(10 - (lunar_month - 1))


def get_minor_star_position_wenchang(time_index: int) -> int:
    """
    计算文昌星位置（按时辰）

    口诀：子时起戌宫，逆行十二宫

    Args:
        time_index: 时辰索引 (0-12)

    Returns:
        文昌星宫位索引
    """
    # 处理早子时和晚子时
    actual_time_index = 0 if time_index == 12 else time_index

    # 子时在戌宫(10)，逆行
    return fix_index(10 - actual_time_index)


def get_minor_star_position_wenqu(time_index: int) -> int:
    """
    计算文曲星位置（按时辰）

    口诀：子时起辰宫，顺行十二宫

    Args:
        time_index: 时辰索引 (0-12)

    Returns:
        文曲星宫位索引
    """
    # 处理早子时和晚子时
    actual_time_index = 0 if time_index == 12 else time_index

    # 子时在辰宫(4)，顺行
    return fix_index(4 + actual_time_index)


def get_minor_star_positions_kuiyue(year_stem_index: int) -> Tuple[int, int]:
    """
    计算天魁天钺星位置（按年干）

    Args:
        year_stem_index: 年干索引 (0-9)

    Returns:
        (天魁星索引, 天钺星索引) 元组
    """
    # 天魁位置（按年干）
    # 甲戊庚在丑寅, 乙己在子申, 丙丁在亥酉, 辛在午寅, 壬在卯巳, 癸在卯巳
    kuai_positions = [1, 0, 11, 11, 1, 0, 6, 6, 3, 3]  # 索引对应甲-癸

    # 天钺位置（按年干）
    yue_positions = [7, 8, 9, 9, 7, 8, 2, 2, 5, 5]  # 索引对应甲-癸

    return kuai_positions[year_stem_index], yue_positions[year_stem_index]


def get_minor_star_positions_huoling(year_branch_index: int, time_index: int) -> Tuple[int, int]:
    """
    计算火星铃星位置（按年支和时辰）

    Args:
        year_branch_index: 年支索引 (0-11)
        time_index: 时辰索引 (0-12)

    Returns:
        (火星索引, 铃星索引) 元组
    """
    # 处理早子时和晚子时
    actual_time_index = 0 if time_index == 12 else time_index

    # 火星位置（寅午戌年起寅，申子辰年起申，巳酉丑年起亥，亥卯未年起巳）
    # 年支分组
    if year_branch_index in [2, 6, 10]:  # 寅午戌
        huo_base = 2  # 寅
    elif year_branch_index in [8, 0, 4]:  # 申子辰
        huo_base = 8  # 申
    elif year_branch_index in [5, 9, 1]:  # 巳酉丑
        huo_base = 11  # 亥
    else:  # 亥卯未 [11, 3, 7]
        huo_base = 5  # 巳

    huo_index = fix_index(huo_base + actual_time_index)

    # 铃星位置（卯酉年起卯，寅午戌年起寅...）
    if year_branch_index in [3, 9]:  # 卯酉
        ling_base = 3  # 卯
    elif year_branch_index in [2, 6, 10]:  # 寅午戌
        ling_base = 2  # 寅
    elif year_branch_index in [8, 0, 4]:  # 申子辰
        ling_base = 8  # 申
    else:  # 巳酉丑、亥卯未
        ling_base = 5  # 巳

    ling_index = fix_index(ling_base + actual_time_index)

    return huo_index, ling_index


def get_minor_star_positions_kongjie(time_index: int) -> Tuple[int, int]:
    """
    计算地空地劫星位置（按时辰）

    Args:
        time_index: 时辰索引 (0-12)

    Returns:
        (地空索引, 地劫索引) 元组
    """
    # 处理早子时和晚子时
    actual_time_index = 0 if time_index == 12 else time_index

    # 地空：子时在亥，逆行
    kong_index = fix_index(11 - actual_time_index)

    # 地劫：子时在亥，顺行
    jie_index = fix_index(11 + actual_time_index)

    return kong_index, jie_index


def get_minor_star_positions_lucun_yangtuo_tianma(
    year_stem_index: int,
    year_branch_index: int
) -> Tuple[int, int, int, int]:
    """
    计算禄存、擎羊、陀罗、天马星位置（按年干支）

    Args:
        year_stem_index: 年干索引 (0-9)
        year_branch_index: 年支索引 (0-11)

    Returns:
        (禄存索引, 擎羊索引, 陀罗索引, 天马索引) 元组
    """
    # 禄存位置（按年干，对应地支）
    # 甲禄在寅、乙禄在卯、丙戊禄在巳、丁己禄在午、庚禄在申、辛禄在酉、壬禄在亥、癸禄在子
    lucun_positions = [2, 3, 5, 6, 5, 6, 8, 9, 11, 0]

    lucun_index = lucun_positions[year_stem_index]

    # 擎羊：禄存的下一宫
    yang_index = fix_index(lucun_index + 1)

    # 陀罗：禄存的上一宫
    tuo_index = fix_index(lucun_index - 1)

    # 天马位置（按年支）
    # 寅午戌年在申、申子辰年在寅、巳酉丑年在亥、亥卯未年在巳
    if year_branch_index in [2, 6, 10]:  # 寅午戌
        tianma_index = 8  # 申
    elif year_branch_index in [8, 0, 4]:  # 申子辰
        tianma_index = 2  # 寅
    elif year_branch_index in [5, 9, 1]:  # 巳酉丑
        tianma_index = 11  # 亥
    else:  # 亥卯未
        tianma_index = 5  # 巳

    return lucun_index, yang_index, tuo_index, tianma_index
