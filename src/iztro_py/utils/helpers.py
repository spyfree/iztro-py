"""
Helper utilities for iztro-py

Common utility functions used throughout the library.
"""

from typing import Optional, Tuple
from iztro_py.data.types import HeavenlyStemName, EarthlyBranchName, FiveElementsClass
from iztro_py.data.constants import (
    HEAVENLY_STEMS,
    EARTHLY_BRANCHES,
    FIVE_ELEMENTS_CLASS_LOOKUP,
    fix_index,
)


def get_five_elements_class(
    heavenly_stem: HeavenlyStemName, earthly_branch: EarthlyBranchName
) -> FiveElementsClass:
    """
    根据命宫天干地支获取五行局

    Args:
        heavenly_stem: 命宫天干
        earthly_branch: 命宫地支

    Returns:
        五行局枚举值
    """
    stem_index = HEAVENLY_STEMS.index(heavenly_stem)
    branch_index = EARTHLY_BRANCHES.index(earthly_branch)

    class_value = FIVE_ELEMENTS_CLASS_LOOKUP[stem_index][branch_index]

    # 转换为枚举
    if class_value == 2:
        return FiveElementsClass.WATER_2
    elif class_value == 3:
        return FiveElementsClass.WOOD_3
    elif class_value == 4:
        return FiveElementsClass.METAL_4
    elif class_value == 5:
        return FiveElementsClass.EARTH_5
    elif class_value == 6:
        return FiveElementsClass.FIRE_6
    else:
        raise ValueError(f"Invalid five elements class value: {class_value}")


def get_five_elements_class_name(five_elements_class: FiveElementsClass) -> str:
    """
    获取五行局的中文名称

    Args:
        five_elements_class: 五行局枚举

    Returns:
        中文名称，如 "水二局"
    """
    names = {
        FiveElementsClass.WATER_2: "水二局",
        FiveElementsClass.WOOD_3: "木三局",
        FiveElementsClass.METAL_4: "金四局",
        FiveElementsClass.EARTH_5: "土五局",
        FiveElementsClass.FIRE_6: "火六局",
    }
    return names[five_elements_class]


def get_time_range(time_index: int) -> str:
    """
    获取时辰的时间范围

    Args:
        time_index: 时辰索引 (0-12)

    Returns:
        时间范围字符串，如 "11:00~13:00"
    """
    time_ranges = [
        "00:00~01:00",  # 早子时
        "01:00~03:00",  # 丑时
        "03:00~05:00",  # 寅时
        "05:00~07:00",  # 卯时
        "07:00~09:00",  # 辰时
        "09:00~11:00",  # 巳时
        "11:00~13:00",  # 午时
        "13:00~15:00",  # 未时
        "15:00~17:00",  # 申时
        "17:00~19:00",  # 酉时
        "19:00~21:00",  # 戌时
        "21:00~23:00",  # 亥时
        "23:00~00:00",  # 晚子时
    ]

    if 0 <= time_index < len(time_ranges):
        return time_ranges[time_index]
    else:
        raise ValueError(f"Invalid time index: {time_index}. Must be 0-12.")


def get_time_name(time_index: int) -> str:
    """
    获取时辰的中文名称

    Args:
        time_index: 时辰索引 (0-12)

    Returns:
        时辰中文名称，如 "午时"
    """
    time_names = [
        "子时",  # 0 早子时
        "丑时",  # 1
        "寅时",  # 2
        "卯时",  # 3
        "辰时",  # 4
        "巳时",  # 5
        "午时",  # 6
        "未时",  # 7
        "申时",  # 8
        "酉时",  # 9
        "戌时",  # 10
        "亥时",  # 11
        "子时",  # 12 晚子时
    ]

    if 0 <= time_index < len(time_names):
        return time_names[time_index]
    else:
        raise ValueError(f"Invalid time index: {time_index}. Must be 0-12.")


def hour_to_time_index(hour: int) -> int:
    """
    将 24 小时制的小时数 (0-23) 映射为时辰索引 (0-12)

    规则与 iztro 保持一致：
    - 子时分早子时(0)与晚子时(12)：23点对应晚子时(12)，0点对应早子时(0)
    - 其他小时按每两小时一个时辰：(hour + 1) // 2

    Args:
        hour: 小时 (0-23)

    Returns:
        时辰索引 (0-12)
    """
    if not (0 <= hour <= 23):
        raise ValueError(f"hour must be in 0..23, got {hour}")

    if hour == 23:
        return 12  # 晚子时
    return (hour + 1) // 2


def calculate_nominal_age(birth_year: int, target_year: int, age_divide: str = "normal") -> int:
    """
    计算虚岁

    Args:
        birth_year: 出生年份
        target_year: 目标年份
        age_divide: 年龄划分方式
            - 'normal': 按自然年计算
            - 'birthday': 按生日计算（需要完整日期，此处简化处理）

    Returns:
        虚岁
    """
    # 虚岁 = 当前年份 - 出生年份 + 1
    return target_year - birth_year + 1


def get_palace_index_by_name(palace_name: str) -> Optional[int]:
    """
    根据宫位名称获取索引

    Args:
        palace_name: 宫位名称（中文或英文key）

    Returns:
        宫位索引 (0-11)，如果未找到返回None
    """
    # 中文名称映射
    chinese_names = {
        "命宫": 0,
        "父母宫": 1,
        "福德宫": 2,
        "田宅宫": 3,
        "官禄宫": 4,
        "奴仆宫": 5,
        "交友宫": 5,  # 奴仆宫别名
        "迁移宫": 6,
        "疾厄宫": 7,
        "财帛宫": 8,
        "子女宫": 9,
        "夫妻宫": 10,
        "兄弟宫": 11,
        # 简化别名（不带"宫"）
        "命": 0,
        "父母": 1,
        "福德": 2,
        "田宅": 3,
        "官禄": 4,
        "事业": 4,  # 官禄宫别名
        "奴仆": 5,
        "交友": 5,
        "迁移": 6,
        "疾厄": 7,
        "财帛": 8,
        "子女": 9,
        "夫妻": 10,
        "兄弟": 11,
    }

    # 英文key映射
    english_keys = {
        "soulPalace": 0,
        "parentsPalace": 1,
        "spiritPalace": 2,
        "propertyPalace": 3,
        "careerPalace": 4,
        "friendsPalace": 5,
        "surfacePalace": 6,
        "healthPalace": 7,
        "wealthPalace": 8,
        "childrenPalace": 9,
        "spousePalace": 10,
        "siblingsPalace": 11,
        # 简化别名（不带"Palace"）
        "soul": 0,
        "parents": 1,
        "spirit": 2,
        "property": 3,
        "career": 4,
        "friends": 5,
        "surface": 6,
        "health": 7,
        "wealth": 8,
        "children": 9,
        "spouse": 10,
        "siblings": 11,
    }

    # 先尝试中文
    if palace_name in chinese_names:
        return chinese_names[palace_name]

    # 再尝试英文
    if palace_name in english_keys:
        return english_keys[palace_name]

    return None


def get_decadal_range(
    five_elements_class: FiveElementsClass,
    palace_index: int,
    gender: str,
    soul_palace_index: int = 0,
    year_branch_yin_yang: str = "阳",
) -> Tuple[int, int]:
    """
    计算大限年龄范围

    大限从命宫开始，每个宫位管10年
    男命阳年生人、女命阴年生人：顺行
    男命阴年生人、女命阳年生人：逆行

    Args:
        five_elements_class: 五行局
        palace_index: 宫位索引 (0-11)
        gender: 性别 ('男' 或 '女')
        soul_palace_index: 命宫索引（默认0）
        year_branch_yin_yang: 年支阴阳（默认'阳'）

    Returns:
        (起始年龄, 截止年龄) 元组
    """
    # 五行局决定起始年龄
    start_age = five_elements_class.value

    # 判断顺逆行
    # 男阳女阴顺行，男阴女阳逆行
    is_forward = (gender == "男" and year_branch_yin_yang == "阳") or (
        gender == "女" and year_branch_yin_yang == "阴"
    )

    # 计算此宫位是第几个大限（从0开始）
    if is_forward:
        # 顺行：从命宫开始往后数
        decadal_order = (palace_index - soul_palace_index) % 12
    else:
        # 逆行：从命宫开始往前数
        decadal_order = (soul_palace_index - palace_index) % 12

    # 起始年龄
    range_start = start_age + decadal_order * 10
    range_end = range_start + 9

    return (range_start, range_end)


def get_decadal_palace_index(
    age: int,
    five_elements_class: FiveElementsClass,
    soul_palace_index: int,
    gender: str,
    year_branch_yin_yang: str = "阳",
) -> int:
    """
    根据年龄获取大限所在的宫位索引

    Args:
        age: 虚岁
        five_elements_class: 五行局
        soul_palace_index: 命宫索引
        gender: 性别
        year_branch_yin_yang: 年支阴阳

    Returns:
        大限宫位索引
    """
    start_age = five_elements_class.value

    # 判断顺逆行
    # 男阳女阴顺行，男阴女阳逆行
    is_forward = (gender == "男" and year_branch_yin_yang == "阳") or (
        gender == "女" and year_branch_yin_yang == "阴"
    )

    # 计算从命宫开始的第几个大限（从0开始）
    decadal_order = (age - start_age) // 10

    if is_forward:
        # 顺行
        palace_index = fix_index(soul_palace_index + decadal_order)
    else:
        # 逆行
        palace_index = fix_index(soul_palace_index - decadal_order)

    return palace_index
