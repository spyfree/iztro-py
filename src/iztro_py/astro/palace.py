"""
Palace positioning algorithms for iztro-py

Contains functions for calculating palace positions, especially
the soul palace (命宫) and body palace (身宫).
"""

from typing import Any, Dict, List
from iztro_py.data.types import SoulAndBody, HeavenlyStemName, EarthlyBranchName
from iztro_py.data.constants import HEAVENLY_STEMS, EARTHLY_BRANCHES, TIGER_RULE, fix_index


def get_soul_and_body(
    lunar_month: int, time_index: int, year_stem: HeavenlyStemName
) -> SoulAndBody:
    """
    计算命宫和身宫的位置

    算法：
    1. 命宫：寅起正月，顺数至生月，再逆数生时
    2. 身宫：从生月宫位顺数生时

    Args:
        lunar_month: 农历月份 (1-12)
        time_index: 时辰索引 (0-12)
        year_stem: 年干（用于计算命宫天干）

    Returns:
        SoulAndBody对象，包含命宫和身宫的索引及天干地支
    """
    # 1. 寅起正月，顺数至生月
    # 寅 = 索引2，正月 = lunar_month 1
    # 生月宫位索引 = (2 + lunar_month - 1) % 12
    birth_month_palace_index = fix_index(2 + lunar_month - 1)

    # 2. 从生月宫位逆数生时，得到命宫
    # 时辰索引转换：0(早子时)和12(晚子时)都对应子时，其他时辰直接对应
    actual_time_index = 0 if time_index == 12 else time_index

    # 逆数：减去时辰数
    soul_index = fix_index(birth_month_palace_index - actual_time_index)

    # 3. 从生月宫位顺数生时，得到身宫
    body_index = fix_index(birth_month_palace_index + actual_time_index)

    # 4. 计算命宫地支
    earthly_branch_of_soul = EARTHLY_BRANCHES[soul_index]

    # 5. 计算命宫天干（使用五虎遁）
    # 先找到寅宫的天干
    # 五虎遁：根据年干确定寅月（正月）的天干
    yin_month_stem = TIGER_RULE[year_stem]
    yin_month_stem_index = HEAVENLY_STEMS.index(yin_month_stem)

    # 寅宫索引是2，命宫索引是soul_index
    # 计算从寅宫到命宫的天干偏移
    # 地支顺序：子丑寅卯辰巳午未申酉戌亥
    # 从寅(2)到命宫的距离
    if soul_index >= 2:
        offset = soul_index - 2
    else:
        offset = soul_index + 12 - 2

    # 命宫天干
    heavenly_stem_of_soul_index = fix_index(yin_month_stem_index + offset, 10)
    heavenly_stem_of_soul = HEAVENLY_STEMS[heavenly_stem_of_soul_index]

    return SoulAndBody(
        soul_index=soul_index,
        body_index=body_index,
        heavenly_stem_of_soul=heavenly_stem_of_soul,
        earthly_branch_of_soul=earthly_branch_of_soul,
    )


def get_palace_heavenly_stem(
    palace_index: int, soul_palace_index: int, soul_palace_stem: HeavenlyStemName
) -> HeavenlyStemName:
    """
    根据命宫天干推算其他宫位的天干

    Args:
        palace_index: 目标宫位索引
        soul_palace_index: 命宫索引
        soul_palace_stem: 命宫天干

    Returns:
        目标宫位的天干
    """
    soul_stem_index = HEAVENLY_STEMS.index(soul_palace_stem)

    # 计算从命宫到目标宫位的距离
    if palace_index >= soul_palace_index:
        offset = palace_index - soul_palace_index
    else:
        offset = palace_index + 12 - soul_palace_index

    # 目标宫位天干索引
    target_stem_index = fix_index(soul_stem_index + offset, 10)

    return HEAVENLY_STEMS[target_stem_index]


def get_palace_earthly_branch(palace_index: int) -> EarthlyBranchName:
    """
    根据宫位索引获取地支

    宫位地支固定：
    0(命宫) - 根据命宫定位算法确定
    其他宫位按地支顺序排列

    Args:
        palace_index: 宫位索引 (0-11)

    Returns:
        地支名称
    """
    return EARTHLY_BRANCHES[palace_index]


def get_body_palace_index(soul_index: int, body_index: int) -> int:
    """
    确定身宫所在的宫位

    身宫会落在某个宫位上，该宫位标记为身宫

    Args:
        soul_index: 命宫索引
        body_index: 身宫索引（通过算法计算出的地支位置）

    Returns:
        身宫所在的宫位索引
    """
    # 身宫的索引就是其地支位置相对于命宫的偏移
    # 因为十二宫固定从命宫开始：命宫(0)、父母(1)、福德(2)...
    # 而身宫的地支位置是通过"从生月顺数生时"得到的

    # 直接返回body_index，因为宫位是从命宫开始按地支顺序排列的
    return body_index


def calculate_palace_ages(
    palace_index: int, soul_palace_index: int, five_elements_class_value: int, is_forward: bool
) -> List[int]:
    """
    计算宫位的小限年龄数组

    小限从命宫开始，每年走一宫
    顺逆根据性别和年支阴阳决定

    Args:
        palace_index: 宫位索引
        soul_palace_index: 命宫索引
        five_elements_class_value: 五行局数值 (2-6)
        is_forward: 是否顺行

    Returns:
        该宫位对应的年龄列表
    """
    ages = []

    # 小限从命宫开始，起始年龄 = 五行局数值
    start_age = five_elements_class_value

    # 计算当前宫位是从命宫数起的第几个宫位
    if is_forward:
        # 顺行
        offset = (palace_index - soul_palace_index) % 12
    else:
        # 逆行
        offset = (soul_palace_index - palace_index) % 12

    # 该宫位对应的年龄：起始年龄 + 偏移，然后每隔12年一次
    first_age = start_age + offset

    # 生成年龄列表（通常到120岁）
    for age in range(first_age, 121, 12):
        ages.append(age)

    return ages


def initialize_palaces(soul_and_body: SoulAndBody) -> List[Dict[str, Any]]:
    """
    初始化十二宫位的基础信息

    Args:
        soul_and_body: 命身宫位置信息

    Returns:
        包含12个宫位基础信息的列表
    """
    from iztro_py.data.constants import PALACES

    palaces = []

    # 重要：宫位地支是从命宫的地支开始，按地支顺序排列
    # 例如：命宫在亥 -> 父母宫在子 -> 福德宫在丑 -> ...
    soul_index = soul_and_body.soul_index
    body_index = soul_and_body.body_index

    # 计算身宫在宫位序列中的相对索引（以命宫所在宫位为0）
    body_palace_rel_index = fix_index(body_index - soul_index)

    for i in range(12):
        # 计算这个宫位对应的地支索引
        # 从命宫开始，i=0是命宫，i=1是父母宫等
        earthly_branch_index = fix_index(soul_index + i)

        # 判断该宫位是否为身宫（相对命宫的序列位置等于身宫相对索引）
        is_body = i == body_palace_rel_index

        palace: Dict[str, Any] = {
            "index": i,
            "name": PALACES[i],
            "is_body_palace": is_body,
            "is_original_palace": (i == 0),  # 第0个宫位总是命宫
            "earthly_branch": EARTHLY_BRANCHES[earthly_branch_index],
            "heavenly_stem": get_palace_heavenly_stem(
                earthly_branch_index, soul_and_body.soul_index, soul_and_body.heavenly_stem_of_soul
            ),
            "major_stars": [],
            "minor_stars": [],
            "adjective_stars": [],
            "changsheng12": None,
            "boshi12": None,
            "jiangqian12": None,
            "suiqian12": None,
            "decadal": None,
            "ages": [],
        }

        palaces.append(palace)

    return palaces
