"""
Core type definitions for iztro-py

This module defines all the type aliases, enums, and data structures used throughout the library.
Based on the original TypeScript definitions from iztro.
"""

from enum import Enum
from typing import Any, Dict, Literal, Optional, List, Tuple, Union
from pydantic import BaseModel, Field, ConfigDict


def _translate_name(key: str, lang: Optional[str] = None) -> str:
    """
    翻译名称的辅助函数
    延迟导入 i18n 模块以避免循环依赖
    """
    from iztro_py.i18n import t

    # 尝试多个可能的键
    # 1. 直接作为星曜名称
    if key in [
        "ziweiMaj",
        "tianjiMaj",
        "taiyangMaj",
        "wuquMaj",
        "tiantongMaj",
        "lianzhenMaj",
        "tianfuMaj",
        "taiyinMaj",
        "tanlangMaj",
        "jumenMaj",
        "tianxiangMaj",
        "tianliangMaj",
        "qishaMaj",
        "pojunMaj",
    ]:
        return t(f"stars.major.{key}", lang)

    if key in [
        "zuofuMin",
        "youbiMin",
        "wenchangMin",
        "wenquMin",
        "tiankuiMin",
        "tianyueMin",
        "huoxingMin",
        "lingxingMin",
        "dikongMin",
        "dijieMin",
        "lucunMin",
        "qingyangMin",
        "tuoluoMin",
        "tianmaMin",
    ]:
        return t(f"stars.minor.{key}", lang)

    # 2. 作为宫位名称
    if key in [
        "soulPalace",
        "parentsPalace",
        "spiritPalace",
        "propertyPalace",
        "careerPalace",
        "friendsPalace",
        "surfacePalace",
        "healthPalace",
        "wealthPalace",
        "childrenPalace",
        "spousePalace",
        "siblingsPalace",
    ]:
        return t(f"palaces.{key}", lang)

    # 3. 作为天干
    if "Heavenly" in key:
        return t(f"heavenlyStem.{key}", lang)

    # 4. 作为地支
    if "Earthly" in key:
        return t(f"earthlyBranch.{key}", lang)

    # 5. 作为时辰
    if "Hour" in key:
        return t(f"time.{key}", lang)

    # 默认返回原值
    return t(key, lang)


# ============================================================================
# Basic Type Aliases
# ============================================================================

Language = Literal["en-US", "ja-JP", "ko-KR", "zh-CN", "zh-TW", "vi-VN"]
YinYang = Literal["阴", "阳"]
FiveElements = Literal["木", "金", "水", "火", "土"]
GenderName = Literal["男", "女"]
Mutagen = Literal["禄", "权", "科", "忌"]
Brightness = Literal["庙", "旺", "得", "利", "平", "不", "陷"]
Scope = Literal["origin", "decadal", "yearly", "monthly", "daily", "hourly"]
StarType = Literal["major", "soft", "tough", "adjective", "flower", "helper", "lucun", "tianma"]


# ============================================================================
# Chinese Time (时辰)
# ============================================================================

ChineseTime = Literal[
    "earlyRatHour",  # 早子时 00:00~01:00
    "oxHour",  # 丑时 01:00~03:00
    "tigerHour",  # 寅时 03:00~05:00
    "rabbitHour",  # 卯时 05:00~07:00
    "dragonHour",  # 辰时 07:00~09:00
    "snakeHour",  # 巳时 09:00~11:00
    "horseHour",  # 午时 11:00~13:00
    "goatHour",  # 未时 13:00~15:00
    "monkeyHour",  # 申时 15:00~17:00
    "roosterHour",  # 酉时 17:00~19:00
    "dogHour",  # 戌时 19:00~21:00
    "pigHour",  # 亥时 21:00~23:00
    "lateRatHour",  # 晚子时 23:00~00:00
]


# ============================================================================
# Heavenly Stems (天干)
# ============================================================================

HeavenlyStemName = Literal[
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
# Earthly Branches (地支)
# ============================================================================

EarthlyBranchName = Literal[
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
# Palace Names (宫位名称)
# ============================================================================

PalaceName = Literal[
    "soulPalace",  # 命宫
    "parentsPalace",  # 父母宫
    "spiritPalace",  # 福德宫
    "propertyPalace",  # 田宅宫
    "careerPalace",  # 官禄宫
    "friendsPalace",  # 奴仆宫（交友宫）
    "surfacePalace",  # 迁移宫
    "healthPalace",  # 疾厄宫
    "wealthPalace",  # 财帛宫
    "childrenPalace",  # 子女宫
    "spousePalace",  # 夫妻宫
    "siblingsPalace",  # 兄弟宫
]


# ============================================================================
# Star Names (星曜名称)
# ============================================================================

# Major stars (14 main stars)
MajorStarName = Literal[
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

# Minor stars (auxiliary stars)
MinorStarName = Literal[
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

# Adjective stars (杂耀)
AdjectiveStarName = Literal[
    # 长生12神
    "changsheng12",
    # 博士12神
    "boshi12",
    # 流年将前12神
    "jiangqian12",
    # 流年岁前12神
    "suiqian12",
    # 其他杂耀
    "huagaiAdj",  # 华盖
    "xianchiAdj",  # 咸池
    "guchenAdj",  # 孤辰
    "guasuAdj",  # 寡宿
    "tiancaiAdj",  # 天才
    "tianshouAdj",  # 天寿
    "hongluan",  # 红鸾
    "tianxi",  # 天喜
    "tianxing",  # 天刑
    "tianyao",  # 天姚
    "jieshen",  # 解神
    "yinsha",  # 阴煞
    "tianguan",  # 天官
    "tianfu2",  # 天福
    "tianku",  # 天哭
    "tianxu",  # 天虚
    "longchi",  # 龙池
    "fengge",  # 凤阁
    "hongluan",  # 红鸾
    "tianxi",  # 天喜
    "guchen",  # 孤辰
    "guasu",  # 寡宿
    "feilian",  # 蜚廉
    "posui",  # 破碎
    "tianchu",  # 天厨
]

# All star names
StarName = Union[MajorStarName, MinorStarName, AdjectiveStarName]


# ============================================================================
# Five Elements Class (五行局)
# ============================================================================


class FiveElementsClass(Enum):
    """五行局枚举"""

    WATER_2 = 2  # 水二局
    WOOD_3 = 3  # 木三局
    METAL_4 = 4  # 金四局
    EARTH_5 = 5  # 土五局
    FIRE_6 = 6  # 火六局


# ============================================================================
# Data Models
# ============================================================================


class Star(BaseModel):
    """星耀数据结构"""

    name: StarName
    type: StarType
    scope: Scope
    brightness: Optional[Brightness] = None
    mutagen: Optional[Mutagen] = None

    model_config = ConfigDict(frozen=False)  # Allow modification for mutagen/brightness

    def translate_name(self, lang: Optional[str] = None) -> str:
        """
        翻译星曜名称

        Args:
            lang: 目标语言代码，如不指定则使用当前语言

        Returns:
            翻译后的星曜名称
        """
        return _translate_name(self.name, lang)

    def translate_brightness(self, lang: Optional[str] = None) -> Optional[str]:
        """
        翻译亮度

        Args:
            lang: 目标语言代码

        Returns:
            翻译后的亮度，如无亮度则返回 None
        """
        if not self.brightness:
            return None
        from iztro_py.i18n import t

        # 亮度直接就是中文，需要映射到英文键
        brightness_map = {
            "庙": "miao",
            "旺": "wang",
            "得": "de",
            "利": "li",
            "平": "ping",
            "不": "bu",
            "陷": "xian",
        }
        key = brightness_map.get(self.brightness, self.brightness)
        return t(f"brightness.{key}", lang)


class Decadal(BaseModel):
    """大限数据结构"""

    range: Tuple[int, int]  # [起始年龄, 截止年龄]
    heavenly_stem: HeavenlyStemName
    earthly_branch: EarthlyBranchName


class Palace(BaseModel):
    """宫位数据结构"""

    index: int = Field(..., ge=0, le=11)  # 宫位索引 0-11
    name: PalaceName
    is_body_palace: bool = False
    is_original_palace: bool = False
    heavenly_stem: HeavenlyStemName
    earthly_branch: EarthlyBranchName
    major_stars: List[Star] = Field(default_factory=list)
    minor_stars: List[Star] = Field(default_factory=list)
    adjective_stars: List[Star] = Field(default_factory=list)
    changsheng12: Optional[StarName] = None
    boshi12: Optional[StarName] = None
    jiangqian12: Optional[StarName] = None
    suiqian12: Optional[StarName] = None
    decadal: Optional[Decadal] = None
    ages: List[int] = Field(default_factory=list)  # 小限年龄数组

    model_config = ConfigDict(frozen=False)

    def translate_name(self, lang: Optional[str] = None) -> str:
        """
        翻译宫位名称

        Args:
            lang: 目标语言代码

        Returns:
            翻译后的宫位名称
        """
        return _translate_name(self.name, lang)

    def translate_heavenly_stem(self, lang: Optional[str] = None) -> str:
        """翻译天干"""
        return _translate_name(self.heavenly_stem, lang)

    def translate_earthly_branch(self, lang: Optional[str] = None) -> str:
        """翻译地支"""
        return _translate_name(self.earthly_branch, lang)


class SoulAndBody(BaseModel):
    """命身宫定位数据"""

    soul_index: int = Field(..., ge=0, le=11)  # 命宫索引
    body_index: int = Field(..., ge=0, le=11)  # 身宫索引
    heavenly_stem_of_soul: HeavenlyStemName
    earthly_branch_of_soul: EarthlyBranchName


class LunarDate(BaseModel):
    """农历日期"""

    year: int
    month: int
    day: int
    is_leap_month: bool = False


class HeavenlyStemAndEarthlyBranchDate(BaseModel):
    """干支日期（四柱）"""

    year_stem: HeavenlyStemName
    year_branch: EarthlyBranchName
    month_stem: HeavenlyStemName
    month_branch: EarthlyBranchName
    day_stem: HeavenlyStemName
    day_branch: EarthlyBranchName
    time_stem: HeavenlyStemName
    time_branch: EarthlyBranchName


class Astrolabe(BaseModel):
    """星盘数据结构（基础版，不含方法）"""

    gender: GenderName
    solar_date: str  # YYYY-MM-DD
    lunar_date: str  # 农历日期字符串
    chinese_date: str  # 干支日期字符串
    time: str  # 时辰中文名
    time_range: str  # 时间范围 如 '11:00~13:00'
    sign: str  # 星座
    zodiac: str  # 生肖
    earthly_branch_of_soul_palace: EarthlyBranchName
    earthly_branch_of_body_palace: EarthlyBranchName
    soul: StarName  # 命主
    body: StarName  # 身主
    five_elements_class: str  # 五行局
    palaces: List[Palace]

    # Language setting
    language: Language = "zh-CN"

    # Raw dates for internal use
    raw_lunar_date: Optional[LunarDate] = None
    raw_chinese_date: Optional[HeavenlyStemAndEarthlyBranchDate] = None

    model_config = ConfigDict(frozen=False)

    def set_language(self, lang: Language) -> None:
        """
        设置星盘语言

        Args:
            lang: 目标语言代码
        """
        from iztro_py.i18n import set_language

        self.language = lang
        set_language(lang)


class SurroundedPalaces(BaseModel):
    """三方四正宫位（本宫、对宫、财帛、官禄）"""

    target: Palace  # 本宫
    opposite: Palace  # 对宫
    wealth: Palace  # 财帛位（相隔8宫）
    career: Palace  # 官禄位（相隔4宫）

    model_config = ConfigDict(frozen=False)


class HoroscopeItem(BaseModel):
    """运限项"""

    index: int = Field(..., ge=0, le=11)
    name: str
    heavenly_stem: HeavenlyStemName
    earthly_branch: EarthlyBranchName
    palace_names: List[PalaceName]
    mutagen: List[StarName]
    stars: Optional[List[List[Star]]] = None  # 流耀


class Horoscope(BaseModel):
    """运限数据结构"""

    solar_date: str
    lunar_date: str
    decadal: HoroscopeItem  # 大限
    age: HoroscopeItem  # 小限 (包含nominal_age)
    yearly: HoroscopeItem  # 流年
    monthly: HoroscopeItem  # 流月
    daily: HoroscopeItem  # 流日
    hourly: HoroscopeItem  # 流时
    nominal_age: int  # 虚岁


# ============================================================================
# Configuration Types
# ============================================================================


class Config(BaseModel):
    """全局配置"""

    mutagens: Optional[Dict[str, Any]] = None  # 四化配置
    brightness: Optional[Dict[str, Any]] = None  # 亮度配置
    year_divide: Literal["normal", "exact"] = "normal"  # 年分割点
    horoscope_divide: Literal["normal", "exact"] = "normal"  # 运限分割点
    age_divide: Literal["normal", "birthday"] = "normal"  # 小限分割点
    day_divide: Literal["current", "forward"] = "current"  # 晚子时分割
    algorithm: Literal["default", "zhongzhou"] = "default"  # 安星算法


class AstrolabeOptions(BaseModel):
    """星盘生成选项"""

    type: Literal["solar", "lunar"]
    date_str: str
    time_index: int = Field(..., ge=0, le=12)
    gender: GenderName
    is_leap_month: bool = False
    fix_leap: bool = True
    language: Language = "zh-CN"
    config: Optional[Config] = None
