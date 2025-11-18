"""
Heavenly Stems (天干) data and properties

Contains detailed information about the ten heavenly stems including
yin-yang, five elements, clashes, and mutagen (四化) configurations.
"""

from typing import Dict, List, Optional
from iztro_py.data.types import HeavenlyStemName, YinYang, FiveElements, StarName, Mutagen


class HeavenlyStem:
    """天干数据类"""

    def __init__(
        self,
        yin_yang: YinYang,
        five_elements: FiveElements,
        crash: HeavenlyStemName,
        mutagen: List[StarName],
    ):
        self.yin_yang = yin_yang
        self.five_elements = five_elements
        self.crash = crash  # 相冲的天干
        self.mutagen = mutagen  # 四化：禄、权、科、忌


# ============================================================================
# Heavenly Stems Configuration
# ============================================================================

HEAVENLY_STEMS_CONFIG: Dict[HeavenlyStemName, HeavenlyStem] = {
    # 甲天干
    "jiaHeavenly": HeavenlyStem(
        yin_yang="阳",
        five_elements="木",
        crash="gengHeavenly",
        mutagen=["lianzhenMaj", "pojunMaj", "wuquMaj", "taiyangMaj"],  # 廉禄、破权、武科、阳忌
    ),
    # 乙天干
    "yiHeavenly": HeavenlyStem(
        yin_yang="阴",
        five_elements="木",
        crash="xinHeavenly",
        mutagen=["tianjiMaj", "tianliangMaj", "ziweiMaj", "taiyinMaj"],  # 机禄、梁权、紫科、月忌
    ),
    # 丙天干
    "bingHeavenly": HeavenlyStem(
        yin_yang="阳",
        five_elements="火",
        crash="renHeavenly",
        mutagen=[
            "tiantongMaj",
            "tianjiMaj",
            "wenchangMin",
            "lianzhenMaj",
        ],  # 同禄、机权、昌科、廉忌
    ),
    # 丁天干
    "dingHeavenly": HeavenlyStem(
        yin_yang="阴",
        five_elements="火",
        crash="guiHeavenly",
        mutagen=["taiyinMaj", "tiantongMaj", "tianjiMaj", "jumenMaj"],  # 阴禄、同权、机科、巨忌
    ),
    # 戊天干
    "wuHeavenly": HeavenlyStem(
        yin_yang="阳",
        five_elements="土",
        crash="jiaHeavenly",
        mutagen=["tanlangMaj", "taiyinMaj", "youbiMin", "tianjiMaj"],  # 贪禄、月权、弼科、机忌
    ),
    # 己天干
    "jiHeavenly": HeavenlyStem(
        yin_yang="阴",
        five_elements="土",
        crash="yiHeavenly",
        mutagen=["wuquMaj", "tanlangMaj", "tianliangMaj", "wenquMin"],  # 武禄、贪权、梁科、曲忌
    ),
    # 庚天干
    "gengHeavenly": HeavenlyStem(
        yin_yang="阳",
        five_elements="金",
        crash="jiaHeavenly",
        mutagen=["taiyangMaj", "wuquMaj", "taiyinMaj", "tiantongMaj"],  # 阳禄、武权、阴科、同忌
    ),
    # 辛天干
    "xinHeavenly": HeavenlyStem(
        yin_yang="阴",
        five_elements="金",
        crash="yiHeavenly",
        mutagen=["jumenMaj", "taiyangMaj", "wenquMin", "wenchangMin"],  # 巨禄、阳权、曲科、昌忌
    ),
    # 壬天干
    "renHeavenly": HeavenlyStem(
        yin_yang="阳",
        five_elements="水",
        crash="bingHeavenly",
        mutagen=["tianliangMaj", "ziweiMaj", "zuofuMin", "wuquMaj"],  # 梁禄、紫权、左科、武忌
    ),
    # 癸天干
    "guiHeavenly": HeavenlyStem(
        yin_yang="阴",
        five_elements="水",
        crash="dingHeavenly",
        mutagen=["pojunMaj", "jumenMaj", "taiyinMaj", "tanlangMaj"],  # 破禄、巨权、阴科、贪忌
    ),
}


# ============================================================================
# Helper Functions
# ============================================================================


def get_mutagen(heavenly_stem: HeavenlyStemName) -> List[StarName]:
    """
    获取指定天干的四化星

    Args:
        heavenly_stem: 天干名称

    Returns:
        四化星列表 [禄, 权, 科, 忌]
    """
    return HEAVENLY_STEMS_CONFIG[heavenly_stem].mutagen


def get_mutagen_type(heavenly_stem: HeavenlyStemName, star_name: StarName) -> Optional[Mutagen]:
    """
    获取指定星耀在指定天干下的四化类型

    Args:
        heavenly_stem: 天干名称
        star_name: 星耀名称

    Returns:
        四化类型：'禄'、'权'、'科'、'忌'，如果不是四化星则返回 None
    """
    mutagen_stars = HEAVENLY_STEMS_CONFIG[heavenly_stem].mutagen
    mutagen_types: List[Mutagen] = ["禄", "权", "科", "忌"]

    if star_name in mutagen_stars:
        index = mutagen_stars.index(star_name)
        return mutagen_types[index]

    return None


def get_yin_yang(heavenly_stem: HeavenlyStemName) -> YinYang:
    """
    获取天干的阴阳属性

    Args:
        heavenly_stem: 天干名称

    Returns:
        阴阳属性
    """
    return HEAVENLY_STEMS_CONFIG[heavenly_stem].yin_yang


def get_five_elements(heavenly_stem: HeavenlyStemName) -> FiveElements:
    """
    获取天干的五行属性

    Args:
        heavenly_stem: 天干名称

    Returns:
        五行属性
    """
    return HEAVENLY_STEMS_CONFIG[heavenly_stem].five_elements


def get_crash(heavenly_stem: HeavenlyStemName) -> HeavenlyStemName:
    """
    获取相冲的天干

    Args:
        heavenly_stem: 天干名称

    Returns:
        相冲的天干名称
    """
    return HEAVENLY_STEMS_CONFIG[heavenly_stem].crash
