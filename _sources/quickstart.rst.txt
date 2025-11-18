快速开始
========

这个快速指南将帮助你在几分钟内开始使用 iztro-py。

基本概念
--------

iztro-py 用于计算紫微斗数星盘，需要以下信息：

* 出生日期（阳历或农历）
* 出生时辰（0-12，其中0为早子时，12为晚子时）
* 性别（'男' 或 '女'）

创建星盘
--------

使用阳历日期
~~~~~~~~~~~~

.. code-block:: python

    from iztro_py import by_solar

    # 创建星盘：2000年8月16日 午时 男命
    chart = by_solar('2000-8-16', 6, '男')

使用农历日期
~~~~~~~~~~~~

.. code-block:: python

    from iztro_py import by_lunar

    # 创建星盘：农历2000年7月17日 午时 男命
    chart = by_lunar('2000-7-17', 6, '男')

查询星盘信息
-----------

获取基本信息
~~~~~~~~~~~~

.. code-block:: python

    print(f"性别: {chart.gender}")
    print(f"阳历: {chart.solar_date}")
    print(f"农历: {chart.lunar_date}")
    print(f"生肖: {chart.zodiac}")
    print(f"星座: {chart.sign}")
    print(f"五行局: {chart.five_elements_class}")

获取宫位信息
~~~~~~~~~~~~

.. code-block:: python

    # 获取命宫
    soul_palace = chart.get_soul_palace()
    print(f"命宫: {soul_palace.name}")

    # 获取其他宫位
    wealth_palace = chart.palace('财帛宫')
    career_palace = chart.palace('官禄宫')

查询星曜
~~~~~~~~

.. code-block:: python

    # 查询紫微星
    ziwei = chart.star('紫微')
    if ziwei:
        palace = ziwei.palace()
        print(f"紫微星在 {palace.name}")
        print(f"亮度: {ziwei.brightness}")
        print(f"四化: {ziwei.mutagen}")

宫位星曜查询
~~~~~~~~~~~~

.. code-block:: python

    # 获取命宫的所有主星
    soul_palace = chart.get_soul_palace()
    for star in soul_palace.major_stars:
        print(f"{star.name} - 亮度:{star.brightness}")

    # 检查宫位是否包含特定星曜
    if soul_palace.has('紫微'):
        print("命宫有紫微星")

    # 检查宫位是否有四化
    if soul_palace.has_mutagen('禄'):
        print("命宫有化禄星")

三方四正查询
~~~~~~~~~~~~

.. code-block:: python

    # 获取命宫的三方四正
    surpalaces = chart.get_soul_palace().surrounded_palaces()

    print(f"对宫: {surpalaces.opposite.name}")
    print(f"财帛位: {surpalaces.wealth.name}")
    print(f"官禄位: {surpalaces.career.name}")

    # 检查三方四正是否有某星
    if surpalaces.have('天马'):
        print("三方四正有天马星")

运限查询
--------

.. code-block:: python

    # 获取某个年龄的运限
    horoscope = chart.horoscope(25)

    print(f"大限: {horoscope.decadal.name}")
    print(f"流年: {horoscope.yearly.name}")
    print(f"流月: {horoscope.monthly.name}")

多语言支持
----------

.. code-block:: python

    # 设置语言
    chart.set_language('en-US')  # 英文
    chart.set_language('zh-TW')  # 繁体中文
    chart.set_language('ja-JP')  # 日文
    chart.set_language('ko-KR')  # 韩文
    chart.set_language('vi-VN')  # 越南文

链式调用
--------

iztro-py 支持链式调用，让代码更简洁：

.. code-block:: python

    # 检查紫微星的三方四正是否有化忌
    if chart.star('紫微').surrounded_palaces().have_mutagen('忌'):
        print("紫微星三方四正有化忌")

    # 检查命宫主星的亮度
    soul_palace = chart.get_soul_palace()
    for star in soul_palace.major_stars:
        if star.with_brightness(['庙', '旺']):
            print(f"{star.name} 庙旺")

下一步
------

* 查看 :doc:`api/index` 了解完整的API文档
* 查看 :doc:`examples` 了解更多使用示例
