"""
Integration test - Complete astrolabe generation
完整的星盘生成集成测试
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from iztro_py.utils.calendar import (
    parse_solar_date,
    solar_to_lunar,
    get_heavenly_stem_and_earthly_branch_date,
    get_zodiac,
    get_sign,
    format_lunar_date,
    format_chinese_date,
)
from iztro_py.utils.helpers import (
    get_five_elements_class,
    get_five_elements_class_name,
    get_time_name,
    get_time_range,
)
from iztro_py.astro.palace import get_soul_and_body, initialize_palaces
from iztro_py.star.major_star import place_major_stars
from iztro_py.star.minor_star import place_minor_stars
from iztro_py.star.mutagen import apply_mutagen_to_palaces
from iztro_py.data.brightness import apply_brightness_to_palaces
from iztro_py.data.earthly_branches import get_soul_star, get_body_star


def generate_astrolabe(solar_date_str: str, time_index: int, gender: str):
    """
    生成完整的星盘

    Args:
        solar_date_str: 阳历日期字符串 'YYYY-M-D'
        time_index: 时辰索引 (0-12)
        gender: 性别 ('男' 或 '女')

    Returns:
        包含完整信息的星盘字典
    """
    print("=" * 80)
    print(f"开始生成星盘：{solar_date_str} {get_time_name(time_index)} {gender}命")
    print("=" * 80)

    # 1. 解析日期
    year, month, day = parse_solar_date(solar_date_str)

    # 2. 阳历转农历
    lunar_date = solar_to_lunar(year, month, day)
    print(f"\n📅 日期信息:")
    print(f"  阳历: {year}年{month}月{day}日")
    print(f"  农历: {format_lunar_date(lunar_date)}")

    # 3. 计算四柱
    chinese_date = get_heavenly_stem_and_earthly_branch_date(
        year, month, day, time_index, lunar_date.month
    )
    print(f"  四柱: {format_chinese_date(chinese_date)}")

    # 4. 生肖星座
    zodiac = get_zodiac(chinese_date.year_branch)
    sign = get_sign(month, day)
    print(f"  生肖: {zodiac}")
    print(f"  星座: {sign}")
    print(f"  时辰: {get_time_name(time_index)} ({get_time_range(time_index)})")

    # 5. 计算命宫身宫
    soul_and_body = get_soul_and_body(lunar_date.month, time_index, chinese_date.year_stem)

    print(f"\n🏠 命身宫信息:")
    print(f"  命宫: 索引 {soul_and_body.soul_index}")
    print(
        f"  命宫干支: {soul_and_body.heavenly_stem_of_soul} {soul_and_body.earthly_branch_of_soul}"
    )
    print(f"  身宫: 索引 {soul_and_body.body_index}")

    # 6. 计算五行局
    five_class = get_five_elements_class(
        soul_and_body.heavenly_stem_of_soul, soul_and_body.earthly_branch_of_soul
    )
    print(f"  五行局: {get_five_elements_class_name(five_class)}")

    # 7. 命主身主
    soul_star = get_soul_star(soul_and_body.earthly_branch_of_soul)
    body_star = get_body_star(chinese_date.year_branch)
    print(f"  命主: {soul_star}")
    print(f"  身主: {body_star}")

    # 8. 初始化十二宫
    palaces = initialize_palaces(soul_and_body)

    # 9. 安置主星
    place_major_stars(palaces, five_class, lunar_date.day)

    # 10. 安置辅星
    place_minor_stars(
        palaces, lunar_date.month, time_index, chinese_date.year_stem, chinese_date.year_branch
    )

    # 11. 应用四化
    apply_mutagen_to_palaces(palaces, chinese_date.year_stem)

    # 12. 应用亮度
    apply_brightness_to_palaces(palaces)

    # 13. 打印十二宫信息
    print(f"\n⭐ 十二宫星曜配置:")
    print("=" * 80)

    for palace in palaces:
        # 宫位基本信息
        palace_marker = ""
        if palace["is_original_palace"]:
            palace_marker += " [命]"
        if palace["is_body_palace"]:
            palace_marker += " [身]"

        print(f"\n【{palace['name']}{palace_marker}】")
        print(f"  索引: {palace['index']}")
        print(f"  干支: {palace['heavenly_stem']} {palace['earthly_branch']}")

        # 主星
        if palace["major_stars"]:
            print(f"  主星:", end="")
            for star in palace["major_stars"]:
                star_info = f" {star.name}"
                if star.brightness:
                    star_info += f"({star.brightness})"
                if star.mutagen:
                    star_info += f"[化{star.mutagen}]"
                print(star_info, end="")
            print()

        # 辅星
        if palace["minor_stars"]:
            print(f"  辅星:", end="")
            for star in palace["minor_stars"]:
                star_info = f" {star.name}"
                if star.mutagen:
                    star_info += f"[化{star.mutagen}]"
                print(star_info, end="")
            print()

    # 统计信息
    total_major = sum(len(p["major_stars"]) for p in palaces)
    total_minor = sum(len(p["minor_stars"]) for p in palaces)
    total_mutagen = sum(
        len([s for s in p["major_stars"] + p["minor_stars"] if s.mutagen]) for p in palaces
    )

    print("\n" + "=" * 80)
    print(f"✓ 星盘生成完成！")
    print(f"  主星: {total_major}颗")
    print(f"  辅星: {total_minor}颗")
    print(f"  四化: {total_mutagen}颗")
    print("=" * 80)

    return {
        "solar_date": solar_date_str,
        "lunar_date": lunar_date,
        "chinese_date": chinese_date,
        "gender": gender,
        "zodiac": zodiac,
        "sign": sign,
        "time_index": time_index,
        "soul_and_body": soul_and_body,
        "five_elements_class": five_class,
        "soul_star": soul_star,
        "body_star": body_star,
        "palaces": palaces,
    }
