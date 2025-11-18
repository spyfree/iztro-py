安装
====

要求
----

* Python 3.8 或更高版本
* pip (Python 包管理器)

使用 pip 安装
-------------

从 PyPI 安装（推荐）::

    pip install iztro-py

从源码安装
----------

克隆仓库::

    git clone https://github.com/spyfree/iztro-py.git
    cd iztro-py

安装开发模式::

    pip install -e ".[dev]"

验证安装
--------

验证安装是否成功::

    python -c "from iztro_py import by_solar; print('安装成功！')"

依赖项
------

核心依赖：

* ``pydantic >= 2.0.0`` - 数据验证
* ``python-dateutil >= 2.8.0`` - 日期处理
* ``lunarcalendar >= 0.0.9`` - 农历转换

开发依赖（可选）：

* ``pytest >= 7.0.0`` - 测试框架
* ``pytest-cov >= 4.0.0`` - 覆盖率报告
* ``black >= 23.0.0`` - 代码格式化
* ``mypy >= 1.0.0`` - 类型检查
* ``ruff >= 0.1.0`` - 代码检查
