"""
Star positioning algorithms for iztro-py

Contains core algorithms for calculating positions of major stars,
especially Ziwei (紫微) and Tianfu (天府).
"""

from typing import Dict, Tuple
from datetime import date, timedelta
from iztro_py.data.types import FiveElementsClass, HeavenlyStemName, EarthlyBranchName, GenderName
from iztro_py.data.constants import HEAVENLY_STEMS, EARTHLY_BRANCHES, PALACES, fix_index
from iztro_py.utils.calendar import (
    parse_solar_date,
    solar_to_lunar,
    get_heavenly_stem_and_earthly_branch_date,
)
from iztro_py.utils.helpers import fix_earthly_branch_index, fix_lunar_month_index, fix_lunar_day_index


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

    # 起始宫位索引（以寅宫为 0）
    start_positions = {
        2: fix_earthly_branch_index("youEarthly"),  # 水二局：酉宫
        3: fix_earthly_branch_index("wuEarthly"),  # 木三局：午宫
        4: fix_earthly_branch_index("haiEarthly"),  # 金四局：亥宫
        5: fix_earthly_branch_index("chenEarthly"),  # 土五局：辰宫
        6: fix_earthly_branch_index("chouEarthly"),  # 火六局：丑宫
    }

    start_pos = start_positions[class_value]

    # 计算紫微星位置
    # 算法：(农历日期 - 1) // 五行局数值 = 循环次数
    # 每个循环移动一个宫位
    cycles = (lunar_day - 1) // class_value
    # 与原版 iztro 不完全一致的简化算法，已被 get_start_indices 替代
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


# Backward-compat helper to satisfy existing tests/imports
def get_star_indices(five_elements_class: FiveElementsClass, lunar_day: int) -> Tuple[int, int]:
    """
    兼容旧接口：根据五行局与农历日返回紫微与天府索引

    注意：该算法为简化版，生产使用请改用 get_start_indices。
    """
    ziwei_index = get_ziwei_index(five_elements_class, lunar_day)
    tianfu_index = get_tianfu_index(ziwei_index)
    return ziwei_index, tianfu_index


def get_start_indices(
    solar_date_str: str,
    time_index: int,
    fix_leap: bool,
    heavenly_stem_of_soul: HeavenlyStemName,
    earthly_branch_of_soul: EarthlyBranchName,
) -> Tuple[int, int]:
    """
    计算紫微与天府起始索引（与原生 iztro 对齐）

    对应 iztro/lib/star/location.getStartIndex 的 Python 实现。

    规则要点：
    - “六五四三二，酉午亥辰丑；局数除日数，商数宫前走；若见数无余，便要起虎口，日数小于局，还直宫中守。”
    - 晚子时（time_index==12）按次日处理（跨月则顺延到下一月初一）
    - 五行局按命宫干支起局

    Returns:
        (紫微索引, 天府索引)
    """
    # 解析阳历日期并获取当日农历
    year, month, day = parse_solar_date(solar_date_str)

    # 晚子时按次日计算农历日
    if time_index == 12:
        d = date(year, month, day) + timedelta(days=1)
        lunar = solar_to_lunar(d.year, d.month, d.day, fix_leap)
        lunar_day = lunar.day
    else:
        lunar = solar_to_lunar(year, month, day, fix_leap)
        lunar_day = lunar.day

    # 五行局数值
    # 直接使用传入的命宫干支计算的五行局数值
    # 复用已有查表逻辑
    from iztro_py.utils.helpers import get_five_elements_class

    five_cls = get_five_elements_class(heavenly_stem_of_soul, earthly_branch_of_soul)
    class_value: int = five_cls.value

    # 寻找最小 offset 使 (lunar_day + offset) 能被 class_value 整除
    offset = -1
    remainder = -1
    while remainder != 0:
        offset += 1
        divisor = lunar_day + offset
        remainder = divisor % class_value
        quotient = divisor // class_value

    # 商对 12 取模（以寅为0的坐标系）
    quotient %= 12

    # 起始紫微索引（寅为0坐标系）
    node_ziwei_index = quotient - 1

    # 循环次数为偶数：逆时针加 offset；奇数：顺时针减 offset
    if offset % 2 == 0:
        node_ziwei_index += offset
    else:
        node_ziwei_index -= offset
    node_ziwei_index = fix_index(node_ziwei_index)

    tianfu_index = fix_index(12 - node_ziwei_index)
    return node_ziwei_index, tianfu_index


def get_major_star_positions(ziwei_index: int, tianfu_index: int) -> Dict[str, int]:
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
    return fix_index(fix_earthly_branch_index("chenEarthly") + lunar_month - 1)


def get_minor_star_position_youbi(lunar_month: int) -> int:
    """
    计算右弼星位置（按农历月）

    口诀：正月起戌宫，逆行十二宫

    Args:
        lunar_month: 农历月 (1-12)

    Returns:
        右弼星宫位索引
    """
    return fix_index(fix_earthly_branch_index("xuEarthly") - (lunar_month - 1))


def get_minor_star_position_wenchang(time_index: int) -> int:
    """
    计算文昌星位置（按时辰）

    口诀：子时起戌宫，逆行十二宫

    Args:
        time_index: 时辰索引 (0-12)

    Returns:
        文昌星宫位索引
    """
    return fix_index(fix_earthly_branch_index("xuEarthly") - fix_index(time_index))


def get_minor_star_position_wenqu(time_index: int) -> int:
    """
    计算文曲星位置（按时辰）

    口诀：子时起辰宫，顺行十二宫

    Args:
        time_index: 时辰索引 (0-12)

    Returns:
        文曲星宫位索引
    """
    return fix_index(fix_earthly_branch_index("chenEarthly") + fix_index(time_index))


def get_minor_star_positions_kuiyue(year_stem_index: int) -> Tuple[int, int]:
    """
    计算天魁天钺星位置（按年干）

    Args:
        year_stem_index: 年干索引 (0-9)

    Returns:
        (天魁星索引, 天钺星索引) 元组
    """
    kuai_positions = [
        fix_earthly_branch_index("chouEarthly"),
        fix_earthly_branch_index("ziEarthly"),
        fix_earthly_branch_index("haiEarthly"),
        fix_earthly_branch_index("haiEarthly"),
        fix_earthly_branch_index("chouEarthly"),
        fix_earthly_branch_index("ziEarthly"),
        fix_earthly_branch_index("chouEarthly"),
        fix_earthly_branch_index("wuEarthly"),
        fix_earthly_branch_index("maoEarthly"),
        fix_earthly_branch_index("maoEarthly"),
    ]
    yue_positions = [
        fix_earthly_branch_index("weiEarthly"),
        fix_earthly_branch_index("shenEarthly"),
        fix_earthly_branch_index("youEarthly"),
        fix_earthly_branch_index("youEarthly"),
        fix_earthly_branch_index("weiEarthly"),
        fix_earthly_branch_index("shenEarthly"),
        fix_earthly_branch_index("weiEarthly"),
        fix_earthly_branch_index("yinEarthly"),
        fix_earthly_branch_index("siEarthly"),
        fix_earthly_branch_index("siEarthly"),
    ]

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
    fixed_time_index = fix_index(time_index)

    if year_branch_index in [2, 6, 10]:  # 寅午戌
        huo_base = fix_earthly_branch_index("chouEarthly")
        ling_base = fix_earthly_branch_index("maoEarthly")
    elif year_branch_index in [8, 0, 4]:  # 申子辰
        huo_base = fix_earthly_branch_index("yinEarthly")
        ling_base = fix_earthly_branch_index("xuEarthly")
    elif year_branch_index in [5, 9, 1]:  # 巳酉丑
        huo_base = fix_earthly_branch_index("maoEarthly")
        ling_base = fix_earthly_branch_index("xuEarthly")
    else:  # 亥卯未 [11, 3, 7]
        huo_base = fix_earthly_branch_index("youEarthly")
        ling_base = fix_earthly_branch_index("xuEarthly")

    return fix_index(huo_base + fixed_time_index), fix_index(ling_base + fixed_time_index)


def get_minor_star_positions_kongjie(time_index: int) -> Tuple[int, int]:
    """
    计算地空地劫星位置（按时辰）

    Args:
        time_index: 时辰索引 (0-12)

    Returns:
        (地空索引, 地劫索引) 元组
    """
    fixed_time_index = fix_index(time_index)
    hai_index = fix_earthly_branch_index("haiEarthly")
    return fix_index(hai_index - fixed_time_index), fix_index(hai_index + fixed_time_index)


def get_minor_star_positions_lucun_yangtuo_tianma(
    year_stem_index: int, year_branch_index: int
) -> Tuple[int, int, int, int]:
    """
    计算禄存、擎羊、陀罗、天马星位置（按年干支）

    Args:
        year_stem_index: 年干索引 (0-9)
        year_branch_index: 年支索引 (0-11)

    Returns:
        (禄存索引, 擎羊索引, 陀罗索引, 天马索引) 元组
    """
    lucun_positions = [
        fix_earthly_branch_index("yinEarthly"),
        fix_earthly_branch_index("maoEarthly"),
        fix_earthly_branch_index("siEarthly"),
        fix_earthly_branch_index("wuEarthly"),
        fix_earthly_branch_index("siEarthly"),
        fix_earthly_branch_index("wuEarthly"),
        fix_earthly_branch_index("shenEarthly"),
        fix_earthly_branch_index("youEarthly"),
        fix_earthly_branch_index("haiEarthly"),
        fix_earthly_branch_index("ziEarthly"),
    ]

    lucun_index = lucun_positions[year_stem_index]

    # 擎羊：禄存的下一宫
    yang_index = fix_index(lucun_index + 1)

    # 陀罗：禄存的上一宫
    tuo_index = fix_index(lucun_index - 1)

    # 天马位置（按年支）
    # 寅午戌年在申、申子辰年在寅、巳酉丑年在亥、亥卯未年在巳
    if year_branch_index in [2, 6, 10]:  # 寅午戌
        tianma_index = fix_earthly_branch_index("shenEarthly")
    elif year_branch_index in [8, 0, 4]:  # 申子辰
        tianma_index = fix_earthly_branch_index("yinEarthly")
    elif year_branch_index in [5, 9, 1]:  # 巳酉丑
        tianma_index = fix_earthly_branch_index("haiEarthly")
    else:  # 亥卯未
        tianma_index = fix_earthly_branch_index("siEarthly")

    return lucun_index, yang_index, tuo_index, tianma_index


def get_daily_star_indices(solar_date_str: str, time_index: int, fix_leap: bool) -> Dict[str, int]:
    """获取日系杂曜索引。"""
    lunar_day = solar_to_lunar(*parse_solar_date(solar_date_str)).day
    month_index = fix_lunar_month_index(solar_date_str, time_index, fix_leap)
    zuofu_index = get_minor_star_position_zuofu(month_index + 1)
    youbi_index = get_minor_star_position_youbi(month_index + 1)
    wenchang_index = get_minor_star_position_wenchang(time_index)
    wenqu_index = get_minor_star_position_wenqu(time_index)
    day_index = fix_lunar_day_index(lunar_day, time_index)
    return {
        "santai_index": fix_index(zuofu_index + day_index),
        "bazuo_index": fix_index(youbi_index - day_index),
        "enguang_index": fix_index(wenchang_index + day_index - 1),
        "tiangui_index": fix_index(wenqu_index + day_index - 1),
    }


def get_timely_star_indices(time_index: int) -> Dict[str, int]:
    """获取时系杂曜索引。"""
    fixed_time_index = fix_index(time_index)
    return {
        "taifu_index": fix_index(fix_earthly_branch_index("wuEarthly") + fixed_time_index),
        "fenggao_index": fix_index(fix_earthly_branch_index("yinEarthly") + fixed_time_index),
    }


def get_luan_xi_indices(year_branch: EarthlyBranchName) -> Dict[str, int]:
    """获取红鸾、天喜索引。"""
    year_branch_index = EARTHLY_BRANCHES.index(year_branch)
    hongluan_index = fix_index(fix_earthly_branch_index("maoEarthly") - year_branch_index)
    return {
        "hongluan_index": hongluan_index,
        "tianxi_index": fix_index(hongluan_index + 6),
    }


def get_huagai_xianchi_indices(year_branch: EarthlyBranchName) -> Dict[str, int]:
    """获取华盖、咸池索引。"""
    if year_branch in ["yinEarthly", "wuEarthly", "xuEarthly"]:
        huagai_branch, xianchi_branch = "xuEarthly", "maoEarthly"
    elif year_branch in ["shenEarthly", "ziEarthly", "chenEarthly"]:
        huagai_branch, xianchi_branch = "chenEarthly", "youEarthly"
    elif year_branch in ["siEarthly", "youEarthly", "chouEarthly"]:
        huagai_branch, xianchi_branch = "chouEarthly", "wuEarthly"
    else:
        huagai_branch, xianchi_branch = "weiEarthly", "ziEarthly"
    return {
        "huagai_index": fix_earthly_branch_index(huagai_branch),
        "xianchi_index": fix_earthly_branch_index(xianchi_branch),
    }


def get_guchen_guasu_indices(year_branch: EarthlyBranchName) -> Dict[str, int]:
    """获取孤辰、寡宿索引。"""
    if year_branch in ["yinEarthly", "maoEarthly", "chenEarthly"]:
        guchen_branch, guasu_branch = "siEarthly", "chouEarthly"
    elif year_branch in ["siEarthly", "wuEarthly", "weiEarthly"]:
        guchen_branch, guasu_branch = "shenEarthly", "chenEarthly"
    elif year_branch in ["shenEarthly", "youEarthly", "xuEarthly"]:
        guchen_branch, guasu_branch = "haiEarthly", "weiEarthly"
    else:
        guchen_branch, guasu_branch = "yinEarthly", "xuEarthly"
    return {
        "guchen_index": fix_earthly_branch_index(guchen_branch),
        "guasu_index": fix_earthly_branch_index(guasu_branch),
    }


def get_jiesha_adj_index(year_branch: EarthlyBranchName) -> int:
    """获取劫煞索引。"""
    if year_branch in ["shenEarthly", "ziEarthly", "chenEarthly"]:
        return 3
    if year_branch in ["haiEarthly", "maoEarthly", "weiEarthly"]:
        return 6
    if year_branch in ["yinEarthly", "wuEarthly", "xuEarthly"]:
        return 9
    return 0


def get_dahao_index(year_branch: EarthlyBranchName) -> int:
    """获取大耗索引。"""
    matched = [
        "weiEarthly",
        "wuEarthly",
        "youEarthly",
        "shenEarthly",
        "haiEarthly",
        "xuEarthly",
        "chouEarthly",
        "ziEarthly",
        "maoEarthly",
        "yinEarthly",
        "siEarthly",
        "chenEarthly",
    ][EARTHLY_BRANCHES.index(year_branch)]
    return fix_index(EARTHLY_BRANCHES.index(matched) - EARTHLY_BRANCHES.index("yinEarthly"))


def get_tianshi_tianshang_indices(
    gender: GenderName,
    year_branch: EarthlyBranchName,
    soul_index: int,
) -> Dict[str, int]:
    """获取天使、天伤索引。当前仅实现 JS 默认流派。"""
    _ = gender, year_branch
    return {
        "tianshang_index": fix_index(PALACES.index("friendsPalace") + soul_index),
        "tianshi_index": fix_index(PALACES.index("healthPalace") + soul_index),
    }


def get_nianjie_index(year_branch: EarthlyBranchName) -> int:
    """获取年解索引。"""
    return fix_earthly_branch_index(
        [
            "xuEarthly",
            "youEarthly",
            "shenEarthly",
            "weiEarthly",
            "wuEarthly",
            "siEarthly",
            "chenEarthly",
            "maoEarthly",
            "yinEarthly",
            "chouEarthly",
            "ziEarthly",
            "haiEarthly",
        ][EARTHLY_BRANCHES.index(year_branch)]
    )


def get_monthly_star_indices(solar_date: str, time_index: int, fix_leap: bool) -> Dict[str, int]:
    """获取月系杂曜索引。"""
    month_index = fix_lunar_month_index(solar_date, time_index, fix_leap)
    return {
        "yuejie_index": fix_earthly_branch_index(
            ["shenEarthly", "xuEarthly", "ziEarthly", "yinEarthly", "chenEarthly", "wuEarthly"][
                month_index // 2
            ]
        ),
        "tianyao_index": fix_index(fix_earthly_branch_index("chouEarthly") + month_index),
        "tianxing_index": fix_index(fix_earthly_branch_index("youEarthly") + month_index),
        "yinsha_index": fix_earthly_branch_index(
            [
                "yinEarthly",
                "ziEarthly",
                "xuEarthly",
                "shenEarthly",
                "wuEarthly",
                "chenEarthly",
            ][month_index % 6]
        ),
        "tianyue_index": fix_earthly_branch_index(
            [
                "xuEarthly",
                "siEarthly",
                "chenEarthly",
                "yinEarthly",
                "weiEarthly",
                "maoEarthly",
                "haiEarthly",
                "weiEarthly",
                "yinEarthly",
                "wuEarthly",
                "xuEarthly",
                "yinEarthly",
            ][month_index]
        ),
        "tianwu_index": fix_earthly_branch_index(
            ["siEarthly", "shenEarthly", "yinEarthly", "haiEarthly"][month_index % 4]
        ),
    }


def get_yearly_star_indices(
    solar_date: str,
    time_index: int,
    gender: GenderName,
    fix_leap: bool,
    soul_index: int,
    body_index: int,
) -> Dict[str, int]:
    """获取年系杂曜索引。"""
    stems_and_branches = get_heavenly_stem_and_earthly_branch_date(
        *parse_solar_date(solar_date),
        time_index,
    )
    year_stem = stems_and_branches.year_stem
    year_branch = stems_and_branches.year_branch
    year_stem_index = HEAVENLY_STEMS.index(year_stem)
    year_branch_index = EARTHLY_BRANCHES.index(year_branch)

    huagai_xianchi = get_huagai_xianchi_indices(year_branch)
    guchen_guasu = get_guchen_guasu_indices(year_branch)
    tianshi_tianshang = get_tianshi_tianshang_indices(gender, year_branch, soul_index)

    xunkong_index = fix_index(
        fix_earthly_branch_index(year_branch)
        + HEAVENLY_STEMS.index("guiHeavenly")
        - year_stem_index
        + 1
    )
    if (year_branch_index % 2) != (xunkong_index % 2):
        xunkong_index = fix_index(xunkong_index + 1)

    return {
        "xianchi_index": huagai_xianchi["xianchi_index"],
        "huagai_index": huagai_xianchi["huagai_index"],
        "guchen_index": guchen_guasu["guchen_index"],
        "guasu_index": guchen_guasu["guasu_index"],
        "tiancai_index": fix_index(soul_index + year_branch_index),
        "tianshou_index": fix_index(body_index + year_branch_index),
        "tianchu_index": fix_earthly_branch_index(
            [
                "siEarthly",
                "wuEarthly",
                "ziEarthly",
                "siEarthly",
                "wuEarthly",
                "shenEarthly",
                "yinEarthly",
                "wuEarthly",
                "youEarthly",
                "haiEarthly",
            ][year_stem_index]
        ),
        "posui_index": fix_earthly_branch_index(
            ["siEarthly", "chouEarthly", "youEarthly"][year_branch_index % 3]
        ),
        "feilian_index": fix_earthly_branch_index(
            [
                "shenEarthly",
                "youEarthly",
                "xuEarthly",
                "siEarthly",
                "wuEarthly",
                "weiEarthly",
                "yinEarthly",
                "maoEarthly",
                "chenEarthly",
                "haiEarthly",
                "ziEarthly",
                "chouEarthly",
            ][year_branch_index]
        ),
        "longchi_index": fix_index(fix_earthly_branch_index("chenEarthly") + year_branch_index),
        "fengge_index": fix_index(fix_earthly_branch_index("xuEarthly") - year_branch_index),
        "tianku_index": fix_index(fix_earthly_branch_index("wuEarthly") - year_branch_index),
        "tianxu_index": fix_index(fix_earthly_branch_index("wuEarthly") + year_branch_index),
        "tianguan_index": fix_earthly_branch_index(
            [
                "weiEarthly",
                "chenEarthly",
                "siEarthly",
                "yinEarthly",
                "maoEarthly",
                "youEarthly",
                "haiEarthly",
                "youEarthly",
                "xuEarthly",
                "wuEarthly",
            ][year_stem_index]
        ),
        "tianfu_index": fix_earthly_branch_index(
            [
                "youEarthly",
                "shenEarthly",
                "ziEarthly",
                "haiEarthly",
                "maoEarthly",
                "yinEarthly",
                "wuEarthly",
                "siEarthly",
                "wuEarthly",
                "siEarthly",
            ][year_stem_index]
        ),
        "tiande_index": fix_index(fix_earthly_branch_index("youEarthly") + year_branch_index),
        "yuede_index": fix_index(fix_earthly_branch_index("siEarthly") + year_branch_index),
        "tiankong_index": fix_index(fix_earthly_branch_index(year_branch) + 1),
        "jielu_index": fix_earthly_branch_index(
            ["shenEarthly", "wuEarthly", "chenEarthly", "yinEarthly", "ziEarthly"][
                year_stem_index % 5
            ]
        ),
        "kongwang_index": fix_earthly_branch_index(
            ["youEarthly", "weiEarthly", "siEarthly", "maoEarthly", "chouEarthly"][
                year_stem_index % 5
            ]
        ),
        "xunkong_index": xunkong_index,
        "tianshang_index": tianshi_tianshang["tianshang_index"],
        "tianshi_index": tianshi_tianshang["tianshi_index"],
        "jiesha_adj_index": get_jiesha_adj_index(year_branch),
        "nianjie_index": get_nianjie_index(year_branch),
        "dahao_adj_index": get_dahao_index(year_branch),
    }
