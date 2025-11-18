使用示例
========

完整示例
--------

创建和分析星盘
~~~~~~~~~~~~~~

.. code-block:: python

    from iztro_py import by_solar

    # 创建星盘
    chart = by_solar('2000-8-16', 6, '男')

    # 打印基本信息
    print(f"=== 基本信息 ===")
    print(f"性别: {chart.gender}")
    print(f"阳历: {chart.solar_date}")
    print(f"农历: {chart.lunar_date}")
    print(f"四柱: {chart.chinese_date}")
    print(f"生肖: {chart.zodiac} | 星座: {chart.sign}")
    print(f"五行局: {chart.five_elements_class}")

    # 命宫信息
    print(f"\n=== 命宫信息 ===")
    soul_palace = chart.get_soul_palace()
    print(f"命宫: {soul_palace.name}")
    print(f"天干地支: {soul_palace.heavenly_stem} {soul_palace.earthly_branch}")

    print("\n主星:")
    for star in soul_palace.major_stars:
        print(f"  {star.name} - 亮度:{star.brightness} 四化:{star.mutagen or '无'}")

    print("\n辅星:")
    for star in soul_palace.minor_stars:
        print(f"  {star.name}")

分析星曜组合
~~~~~~~~~~~~

.. code-block:: python

    from iztro_py import by_solar

    chart = by_solar('2000-8-16', 6, '男')

    # 查找特定星曜
    ziwei = chart.star('紫微')
    if ziwei:
        palace = ziwei.palace()
        print(f"紫微星在 {palace.name} 宫")

        # 检查星曜亮度
        if ziwei.with_brightness(['庙', '旺']):
            print("紫微星庙旺，力量强大")

        # 检查三方四正
        surp = ziwei.surrounded_palaces()
        if surp.have('天府'):
            print("紫微与天府相对，为最佳格局")

批量处理
--------

批量生成星盘
~~~~~~~~~~~~

.. code-block:: python

    from iztro_py import by_solar

    birth_data = [
        ('2000-8-16', 6, '男'),
        ('1995-3-15', 3, '女'),
        ('1988-12-1', 10, '男'),
    ]

    charts = []
    for date, time_idx, gender in birth_data:
        chart = by_solar(date, time_idx, gender)
        charts.append(chart)
        print(f"{date} {gender}命 - 五行局: {chart.five_elements_class}")

运限分析
--------

分析大限流年
~~~~~~~~~~~~

.. code-block:: python

    from iztro_py import by_solar

    chart = by_solar('2000-8-16', 6, '男')

    # 分析25岁的运限
    age = 25
    horoscope = chart.horoscope(age)

    print(f"=== {age}岁运限 ===")
    print(f"大限宫位: {horoscope.decadal.name}")
    print(f"流年宫位: {horoscope.yearly.name}")
    print(f"流月宫位: {horoscope.monthly.name}")

    # 查看流年四化
    print(f"\n流年四化:")
    for star_name in horoscope.yearly.mutagen:
        print(f"  {star_name}")

多语言输出
----------

切换语言
~~~~~~~~

.. code-block:: python

    from iztro_py import by_solar

    chart = by_solar('2000-8-16', 6, '男')

    # 中文（默认）
    print(f"中文: {chart.zodiac}")

    # 英文
    chart.set_language('en-US')
    print(f"English: {chart.zodiac}")

    # 日文
    chart.set_language('ja-JP')
    print(f"日本語: {chart.zodiac}")

    # 繁体中文
    chart.set_language('zh-TW')
    print(f"繁體: {chart.zodiac}")

高级用法
--------

自定义查询
~~~~~~~~~~

.. code-block:: python

    from iztro_py import by_solar

    chart = by_solar('2000-8-16', 6, '男')

    # 查找所有庙旺的主星
    print("=== 庙旺主星 ===")
    for palace in chart.palaces:
        for star in palace.major_stars:
            if star.with_brightness(['庙', '旺']):
                print(f"{star.name} 在 {palace.name} - {star.brightness}")

    # 查找所有化禄星
    print("\n=== 化禄星 ===")
    for palace in chart.palaces:
        for star in palace.major_stars + palace.minor_stars:
            if star.with_mutagen('禄'):
                print(f"{star.name} 在 {palace.name}")

空宫检查
~~~~~~~~

.. code-block:: python

    from iztro_py import by_solar

    chart = by_solar('2000-8-16', 6, '男')

    # 查找空宫
    print("=== 空宫 ===")
    empty_palaces = chart.get_empty_palaces()
    for palace in empty_palaces:
        print(f"{palace.name} 是空宫")

    # 检查特定宫位是否为空
    if chart.palace('财帛宫').is_empty():
        print("财帛宫为空宫")

错误处理
--------

日期验证
~~~~~~~~

.. code-block:: python

    from iztro_py import by_solar

    try:
        # 无效日期
        chart = by_solar('2000-13-32', 6, '男')
    except ValueError as e:
        print(f"日期错误: {e}")

    try:
        # 无效时辰
        chart = by_solar('2000-8-16', 15, '男')
    except Exception as e:
        print(f"时辰错误: {e}")

更多示例
--------

更多详细示例请查看项目的 ``examples/`` 目录：

* ``basic_usage.py`` - 基础用法
* ``horoscope_usage.py`` - 运限分析
* ``i18n_usage.py`` - 多语言使用
* ``multilang_demo.py`` - 多语言演示
