"""
Constants and reference data for iztro-py

This module contains all constant values, lookup tables, and reference data
used for Zi Wei Dou Shu calculations.
"""

from typing import List, Dict
from iztro_py.data.types import (
    HeavenlyStemName,
    EarthlyBranchName,
    PalaceName,
    ChineseTime,
    StarName,
    FiveElementsClass,
)


# ============================================================================
# Time Constants
# ============================================================================

# 时辰列表（13个，包括早子时和晚子时）
CHINESE_TIME: List[ChineseTime] = [
    "earlyRatHour",  # 0  子时 00:00~01:00
    "oxHour",  # 1  丑时 01:00~03:00
    "tigerHour",  # 2  寅时 03:00~05:00
    "rabbitHour",  # 3  卯时 05:00~07:00
    "dragonHour",  # 4  辰时 07:00~09:00
    "snakeHour",  # 5  巳时 09:00~11:00
    "horseHour",  # 6  午时 11:00~13:00
    "goatHour",  # 7  未时 13:00~15:00
    "monkeyHour",  # 8  申时 15:00~17:00
    "roosterHour",  # 9  酉时 17:00~19:00
    "dogHour",  # 10 戌时 19:00~21:00
    "pigHour",  # 11 亥时 21:00~23:00
    "lateRatHour",  # 12 子时 23:00~00:00
]

# 时间范围
TIME_RANGE: List[str] = [
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


# ============================================================================
# Heavenly Stems (十天干)
# ============================================================================

HEAVENLY_STEMS: List[HeavenlyStemName] = [
    "jiaHeavenly",  # 甲
    "yiHeavenly",  # 乙
    "bingHeavenly",  # 丙
    "dingHeavenly",  # 丁
    "wuHeavenly",  # 戊
    "jiHeavenly",  # 己
    "gengHeavenly",  # 庚
    "xinHeavenly",  # 辛
    "renHeavenly",  # 壬
    "guiHeavenly",  # 癸
]


# ============================================================================
# Earthly Branches (十二地支)
# ============================================================================

EARTHLY_BRANCHES: List[EarthlyBranchName] = [
    "ziEarthly",  # 子
    "chouEarthly",  # 丑
    "yinEarthly",  # 寅
    "maoEarthly",  # 卯
    "chenEarthly",  # 辰
    "siEarthly",  # 巳
    "wuEarthly",  # 午
    "weiEarthly",  # 未
    "shenEarthly",  # 申
    "youEarthly",  # 酉
    "xuEarthly",  # 戌
    "haiEarthly",  # 亥
]


# ============================================================================
# Palaces (十二宫位)
# ============================================================================

PALACES: List[PalaceName] = [
    "soulPalace",  # 0 - 命宫
    "parentsPalace",  # 1 - 父母宫
    "spiritPalace",  # 2 - 福德宫
    "propertyPalace",  # 3 - 田宅宫
    "careerPalace",  # 4 - 官禄宫
    "friendsPalace",  # 5 - 奴仆宫（交友宫）
    "surfacePalace",  # 6 - 迁移宫
    "healthPalace",  # 7 - 疾厄宫
    "wealthPalace",  # 8 - 财帛宫
    "childrenPalace",  # 9 - 子女宫
    "spousePalace",  # 10 - 夫妻宫
    "siblingsPalace",  # 11 - 兄弟宫
]


# ============================================================================
# Major Stars (14主星)
# ============================================================================

MAJOR_STARS: List[StarName] = [
    "ziweiMaj",  # 紫微
    "tianjiMaj",  # 天机
    "taiyangMaj",  # 太阳
    "wuquMaj",  # 武曲
    "tiantongMaj",  # 天同
    "lianzhenMaj",  # 廉贞
    "tianfuMaj",  # 天府
    "taiyinMaj",  # 太阴
    "tanlangMaj",  # 贪狼
    "jumenMaj",  # 巨门
    "tianxiangMaj",  # 天相
    "tianliangMaj",  # 天梁
    "qishaMaj",  # 七杀
    "pojunMaj",  # 破军
]


# ============================================================================
# Minor Stars (14辅星)
# ============================================================================

MINOR_STARS: List[StarName] = [
    "zuofuMin",  # 左辅
    "youbiMin",  # 右弼
    "wenchangMin",  # 文昌
    "wenquMin",  # 文曲
    "tiankuiMin",  # 天魁
    "tianyueMin",  # 天钺
    "huoxingMin",  # 火星
    "lingxingMin",  # 铃星
    "dikongMin",  # 地空
    "dijieMin",  # 地劫
    "lucunMin",  # 禄存
    "qingyangMin",  # 擎羊
    "tuoluoMin",  # 陀罗
    "tianmaMin",  # 天马
]


# ============================================================================
# Mutagenesis (四化)
# ============================================================================

MUTAGEN: List[str] = ["禄", "权", "科", "忌"]


# ============================================================================
# Star Groups (星群)
# ============================================================================

# 紫微星系（逆行）
ZIWEI_GROUP: List[str] = [
    "ziweiMaj",  # 0 紫微
    "tianjiMaj",  # 1 天机
    "",  # 2 空
    "taiyangMaj",  # 3 太阳
    "wuquMaj",  # 4 武曲
    "tiantongMaj",  # 5 天同
    "",  # 6 空
    "",  # 7 空
    "lianzhenMaj",  # 8 廉贞
]

# 天府星系（顺行）
TIANFU_GROUP: List[str] = [
    "tianfuMaj",  # 0 天府
    "taiyinMaj",  # 1 太阴
    "tanlangMaj",  # 2 贪狼
    "jumenMaj",  # 3 巨门
    "tianxiangMaj",  # 4 天相
    "tianliangMaj",  # 5 天梁
    "qishaMaj",  # 6 七杀
    "",  # 7 空
    "",  # 8 空
    "",  # 9 空
    "pojunMaj",  # 10 破军
]


# ============================================================================
# Five Tiger Rule (五虎遁)
# ============================================================================
# 年上起月法：甲己之年丙作首

TIGER_RULE: Dict[HeavenlyStemName, HeavenlyStemName] = {
    "jiaHeavenly": "bingHeavenly",  # 甲己之年丙作首
    "jiHeavenly": "bingHeavenly",
    "yiHeavenly": "wuHeavenly",  # 乙庚之岁戊为头
    "gengHeavenly": "wuHeavenly",
    "bingHeavenly": "gengHeavenly",  # 丙辛之岁庚寅上
    "xinHeavenly": "gengHeavenly",
    "dingHeavenly": "renHeavenly",  # 丁壬壬寅顺水流
    "renHeavenly": "renHeavenly",
    "wuHeavenly": "jiaHeavenly",  # 戊癸甲寅为岁首
    "guiHeavenly": "jiaHeavenly",
}


# ============================================================================
# Five Rat Rule (五鼠遁)
# ============================================================================
# 日上起时法：甲己还加甲

RAT_RULE: Dict[HeavenlyStemName, HeavenlyStemName] = {
    "jiaHeavenly": "jiaHeavenly",  # 甲己还加甲
    "jiHeavenly": "jiaHeavenly",
    "yiHeavenly": "bingHeavenly",  # 乙庚丙作初
    "gengHeavenly": "bingHeavenly",
    "bingHeavenly": "wuHeavenly",  # 丙辛从戊起
    "xinHeavenly": "wuHeavenly",
    "dingHeavenly": "gengHeavenly",  # 丁壬庚子居
    "renHeavenly": "gengHeavenly",
    "wuHeavenly": "renHeavenly",  # 戊癸何方发？壬子是真途
    "guiHeavenly": "renHeavenly",
}


# ============================================================================
# Five Elements Class Lookup Table (五行局)
# ============================================================================
# 根据命宫纳音五行确定五行局
# 索引：[命宫天干索引][命宫地支索引]

FIVE_ELEMENTS_CLASS_LOOKUP: List[List[int]] = [
    # 地支：子   丑   寅   卯   辰   巳   午   未   申   酉   戌   亥
    [4, 5, 3, 3, 4, 5, 3, 3, 5, 2, 6, 6],  # 甲
    [5, 5, 6, 6, 5, 5, 6, 6, 2, 2, 3, 3],  # 乙
    [6, 6, 4, 4, 2, 2, 5, 5, 4, 4, 2, 2],  # 丙
    [2, 2, 4, 4, 2, 2, 5, 5, 3, 3, 5, 5],  # 丁
    [6, 6, 4, 4, 3, 3, 6, 6, 4, 4, 3, 3],  # 戊
    [3, 3, 5, 5, 3, 3, 6, 6, 2, 2, 6, 6],  # 己
    [2, 2, 3, 3, 5, 5, 2, 2, 3, 3, 5, 5],  # 庚
    [3, 3, 3, 3, 5, 5, 2, 2, 4, 4, 2, 2],  # 辛
    [3, 3, 4, 4, 2, 2, 3, 3, 4, 4, 2, 2],  # 壬
    [4, 4, 2, 2, 6, 6, 4, 4, 2, 2, 6, 6],  # 癸
]


# ============================================================================
# Ziwei Star Position Algorithm Constants (紫微星定位算法常量)
# ============================================================================

# 紫微星定位口诀：六五四三二，酉午亥辰丑
ZIWEI_START_POSITIONS = [9, 6, 11, 4, 1]  # 对应五行局 2,3,4,5,6 的起始宫位


# ============================================================================
# Star Brightness (星耀亮度)
# ============================================================================
# 按地支顺序：寅卯辰巳午未申酉戌亥子丑

BRIGHTNESS_ORDER = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]

# Mapping brightness keywords
BRIGHTNESS_MAPPING = {
    "庙": "miao",
    "旺": "wang",
    "得": "de",
    "利": "li",
    "平": "ping",
    "不": "bu",
    "陷": "xian",
}


# ============================================================================
# Helper Functions
# ============================================================================


def fix_index(index: int, total: int = 12) -> int:
    """
    修正索引到 0-11 范围内

    Args:
        index: 原始索引
        total: 总数，默认12

    Returns:
        修正后的索引 (0 到 total-1)
    """
    return index % total


def get_opposite_index(index: int) -> int:
    """
    获取对宫索引

    Args:
        index: 当前宫位索引 (0-11)

    Returns:
        对宫索引 (0-11)
    """
    return fix_index(index + 6)


def get_surrounded_indices(index: int) -> Dict[str, int]:
    """
    获取三方四正的索引

    Args:
        index: 当前宫位索引 (0-11)

    Returns:
        包含 target, opposite, wealth, career 的字典
    """
    return {
        "target": index,
        "opposite": fix_index(index + 6),  # 对宫
        "wealth": fix_index(index + 8),  # 财帛位
        "career": fix_index(index + 4),  # 官禄位
    }
