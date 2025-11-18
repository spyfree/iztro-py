iztro-py 文档
=============

欢迎使用 iztro-py！这是一个纯 Python 实现的紫微斗数库。

.. toctree::
   :maxdepth: 2
   :caption: 内容目录:

   installation
   quickstart
   api/index
   examples
   changelog

功能特性
--------

* ✅ 纯 Python 实现，无 JavaScript 依赖
* ✅ 类型安全，使用 Pydantic 数据验证
* ✅ 流畅的 API 设计，支持方法链式调用
* ✅ 完整的多语言支持（6种语言）
* ✅ 与原版 iztro (JavaScript) 算法对齐
* ✅ 完整的测试覆盖

快速开始
--------

安装::

    pip install iztro-py

基本使用::

    from iztro_py import by_solar

    # 通过阳历日期获取星盘
    chart = by_solar('2000-8-16', 6, '男')

    # 获取命宫
    soul_palace = chart.get_soul_palace()
    print(soul_palace)

    # 查询紫微星
    ziwei = chart.star('紫微')
    if ziwei:
        print(f"紫微星在 {ziwei.palace().name}")

链接
----

* `GitHub 仓库 <https://github.com/spyfree/iztro-py>`_
* `PyPI 页面 <https://pypi.org/project/iztro-py/>`_
* `问题追踪 <https://github.com/spyfree/iztro-py/issues>`_

索引和表格
==========

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
