"""
Palace positioning algorithms for iztro-py

Contains functions for calculating palace positions, especially
the soul palace (命宫) and body palace (身宫).
"""

from typing import Any, Dict, List, Union
from iztro_py.data.types import (
    SoulAndBody,
    HeavenlyStemName,
    EarthlyBranchName,
    FiveElementsClass,
    GenderName,
    Decadal,
)
from iztro_py.data.constants import HEAVENLY_STEMS, EARTHLY_BRANCHES, TIGER_RULE, fix_index
from iztro_py.data.earthly_branches import get_yin_yang as get_branch_yin_yang
from iztro_py.utils.calendar import (
    get_heavenly_stem_and_earthly_branch_date,
)
from iztro_py.utils.helpers import fix_lunar_month_index, get_age_index


def get_soul_and_body(
    lunar_month: Union[int, str],
    time_index: int,
    year_stem: HeavenlyStemName = "jiaHeavenly",
    fix_leap: bool = True,
) -> SoulAndBody:
    """
    计算命宫和身宫的位置

    算法：
    1. 命宫：寅起正月，顺数至生月，再逆数生时
    2. 身宫：从生月宫位顺数生时

    Args:
        lunar_month: 农历月份(兼容旧接口)或阳历日期字符串
        time_index: 时辰索引 (0-12)
        year_stem: 年干（旧接口使用）
        fix_leap: 是否修正闰月（仅阳历接口使用）

    Returns:
        SoulAndBody对象，包含命宫和身宫的索引及天干地支
    """
    if isinstance(lunar_month, str):
        solar_date = lunar_month
        month_index = fix_lunar_month_index(solar_date, time_index, fix_leap)
        stems_and_branches = get_heavenly_stem_and_earthly_branch_date(
            *[int(part) for part in solar_date.split("-")],
            time_index,
        )
        heavenly_stem_of_year = stems_and_branches.year_stem
        earthly_branch_of_time = stems_and_branches.time_branch
    else:
        month_index = fix_index(int(lunar_month) - 1)
        heavenly_stem_of_year = year_stem
        earthly_branch_of_time = EARTHLY_BRANCHES[fix_index(time_index)]

    # 以寅宫为 0 的坐标系，与 iztro 保持一致。
    soul_index = fix_index(month_index - EARTHLY_BRANCHES.index(earthly_branch_of_time))
    body_index = fix_index(month_index + EARTHLY_BRANCHES.index(earthly_branch_of_time))

    yin_month_stem = TIGER_RULE[heavenly_stem_of_year]
    heavenly_stem_of_soul_index = fix_index(HEAVENLY_STEMS.index(yin_month_stem) + soul_index, 10)
    heavenly_stem_of_soul = HEAVENLY_STEMS[heavenly_stem_of_soul_index]
    earthly_branch_of_soul = EARTHLY_BRANCHES[fix_index(soul_index + EARTHLY_BRANCHES.index("yinEarthly"))]

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
    target_stem_index = fix_index(soul_stem_index - soul_palace_index + palace_index, 10)
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
    return EARTHLY_BRANCHES[fix_index(EARTHLY_BRANCHES.index("yinEarthly") + palace_index)]


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


def initialize_palaces(
    soul_and_body: SoulAndBody, year_stem: HeavenlyStemName = "jiaHeavenly"
) -> List[Dict[str, Any]]:
    """
    初始化十二宫位的基础信息

    Args:
        soul_and_body: 命身宫位置信息

    Returns:
        包含12个宫位基础信息的列表
    """
    from iztro_py.data.constants import PALACES

    palaces = []

    # 与 iztro 一致：palaces 数组始终以寅宫为 index 0。
    soul_index = soul_and_body.soul_index
    body_index = soul_and_body.body_index
    first_palace_branch_index = EARTHLY_BRANCHES.index("yinEarthly")

    for i in range(12):
        earthly_branch_index = fix_index(first_palace_branch_index + i)
        earthly_branch = EARTHLY_BRANCHES[earthly_branch_index]
        heavenly_stem = get_palace_heavenly_stem(
            i, soul_and_body.soul_index, soul_and_body.heavenly_stem_of_soul
        )

        palace: Dict[str, Any] = {
            "index": i,
            "name": PALACES[fix_index(i - soul_index)],
            "is_body_palace": body_index == i,
            "is_original_palace": earthly_branch not in ["ziEarthly", "chouEarthly"]
            and heavenly_stem == year_stem,
            "earthly_branch": earthly_branch,
            "heavenly_stem": heavenly_stem,
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


def populate_decadal_and_ages(
    palaces: List[Dict[str, Any]],
    soul_index: int,
    five_elements_class: FiveElementsClass,
    gender: GenderName,
    year_stem: HeavenlyStemName,
    year_branch: EarthlyBranchName,
) -> None:
    """
    按 iztro 的 birth-chart 规则填充每个宫位的大限和小限锚点。
    """
    start_heavenly_stem = TIGER_RULE[year_stem]
    same_yin_yang = (
        gender == "男" and get_branch_yin_yang(year_branch) == "阳"
    ) or (
        gender == "女" and get_branch_yin_yang(year_branch) == "阴"
    )

    for i in range(12):
        palace_index = fix_index(soul_index + i) if same_yin_yang else fix_index(soul_index - i)
        start_age = five_elements_class.value + 10 * i
        heavenly_stem_index = fix_index(HEAVENLY_STEMS.index(start_heavenly_stem) + palace_index, 10)
        earthly_branch_index = fix_index(EARTHLY_BRANCHES.index("yinEarthly") + palace_index)
        palaces[palace_index]["decadal"] = Decadal(
            range=(start_age, start_age + 9),
            heavenly_stem=HEAVENLY_STEMS[heavenly_stem_index],
            earthly_branch=EARTHLY_BRANCHES[earthly_branch_index],
        )

    age_index = get_age_index(year_branch)
    for i in range(12):
        ages = [12 * j + i + 1 for j in range(10)]
        palace_index = fix_index(age_index + i) if gender == "男" else fix_index(age_index - i)
        palaces[palace_index]["ages"] = ages
