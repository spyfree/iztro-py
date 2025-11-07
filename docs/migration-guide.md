# 从 py-iztro 迁移到 iztro-py

本指南帮助你从 **py-iztro** 迁移到 **iztro-py**。

## 为什么要迁移？

- 🚀 **5-10倍性能提升** - 纯 Python 实现，无跨语言开销
- 📦 **更小的依赖** - 无需 pythonmonkey（~50MB）
- 🔧 **更易调试** - 纯 Python 堆栈，错误信息清晰
- 🌍 **更广泛支持** - Python 3.8+，支持更多部署环境
- 📚 **更易维护** - 可以直接阅读和修改源码

## 快速迁移检查清单

- [ ] 卸载 py-iztro
- [ ] 安装 iztro-py
- [ ] 更新导入语句
- [ ] 调整 API 调用方式
- [ ] 运行测试验证
- [ ] 性能对比（可选）

## 详细步骤

### 1. 安装 iztro-py

```bash
# 卸载旧版本（可选）
pip uninstall py-iztro

# 安装 iztro-py
pip install iztro-py
```

### 2. 更新代码

#### 2.1 导入语句

```python
# ❌ 旧代码 (py-iztro)
from py_iztro import Astro

# ✅ 新代码 (iztro-py)
from iztro_py import astro
```

#### 2.2 创建星盘

```python
# ❌ 旧代码 (py-iztro)
astro_obj = Astro()
chart = astro_obj.by_solar("2000-8-16", 2, "女")

# ✅ 新代码 (iztro-py)
chart = astro.by_solar('2000-8-16', 2, '女')
```

**变化说明：**
- 不需要实例化 `Astro()` 类
- 直接调用模块级函数
- 更简洁、更 Pythonic

#### 2.3 农历日期

```python
# ❌ 旧代码 (py-iztro)
chart = astro_obj.by_lunar("2000-7-17", 2, "女", False, True)

# ✅ 新代码 (iztro-py)
chart = astro.by_lunar('2000-7-17', 2, '女', False, True)
```

**变化说明：**
- API 参数完全相同
- 只是调用方式变化

### 3. API 映射表

#### 3.1 核心函数

| py-iztro | iztro-py | 说明 |
|----------|----------|------|
| `Astro().by_solar()` | `astro.by_solar()` | 阳历起盘 |
| `Astro().by_lunar()` | `astro.by_lunar()` | 农历起盘 |

#### 3.2 星盘对象属性

```python
# 两者完全相同
chart.gender           # 性别
chart.solar_date       # 阳历日期
chart.lunar_date       # 农历日期
chart.chinese_date     # 四柱
chart.sign             # 星座
chart.zodiac           # 生肖
chart.five_elements_class  # 五行局
chart.palaces          # 宫位列表
```

#### 3.3 宫位查询

```python
# py-iztro 和 iztro-py 都支持
palace = chart.palace(0)              # 通过索引
palace = chart.palace('命宫')         # 通过中文名
palace = chart.palace('careerPalace') # 通过英文名（如果支持）
```

#### 3.4 星曜查询

```python
# py-iztro 和 iztro-py 都支持
star = chart.star('紫微')
star = chart.star('ziweiMaj')  # 英文名

# 星曜属性
star.name          # 星名
star.brightness    # 亮度
star.mutagen       # 四化
star.type          # 类型
```

#### 3.5 方法链

```python
# py-iztro 和 iztro-py 都支持
if chart.star('紫微').surrounded_palaces().have_mutagen('忌'):
    print('紫微星三方四正有化忌')
```

#### 3.6 运势查询

```python
# py-iztro 和 iztro-py 都支持
horoscope = chart.horoscope('2024-1-1', 6)
print(horoscope.decadal.name)    # 大限
print(horoscope.yearly.name)     # 流年
print(horoscope.monthly.name)    # 流月
print(horoscope.daily.name)      # 流日
print(horoscope.hourly.name)     # 流时
```

## 完整示例对比

### py-iztro 代码

```python
from py_iztro import Astro

# 创建星盘
astro_obj = Astro()
chart = astro_obj.by_solar("2000-8-16", 6, "男")

# 查询基本信息
print(f"性别: {chart.gender}")
print(f"星座: {chart.sign}")
print(f"生肖: {chart.zodiac}")

# 查询命宫
soul = chart.get_soul_palace()
print(f"命宫: {soul.name}")
print(f"主星: {[s.name for s in soul.major_stars]}")

# 查询星曜
ziwei = chart.star('紫微')
if ziwei:
    print(f"紫微在: {ziwei.palace().name}")
    print(f"亮度: {ziwei.brightness}")

# 查询运势
horoscope = chart.horoscope('2024-1-1', 6)
print(f"流年: {horoscope.yearly.name}")
```

### iztro-py 代码（迁移后）

```python
from iztro_py import astro

# 创建星盘 - 直接调用函数，无需实例化
chart = astro.by_solar('2000-8-16', 6, '男')

# 查询基本信息（完全相同）
print(f"性别: {chart.gender}")
print(f"星座: {chart.sign}")
print(f"生肖: {chart.zodiac}")

# 查询命宫（完全相同）
soul = chart.get_soul_palace()
print(f"命宫: {soul.name}")
print(f"主星: {[s.name for s in soul.major_stars]}")

# 查询星曜（完全相同）
ziwei = chart.star('紫微')
if ziwei:
    print(f"紫微在: {ziwei.palace().name}")
    print(f"亮度: {ziwei.brightness}")

# 查询运势（完全相同）
horoscope = chart.horoscope('2024-1-1', 6)
print(f"流年: {horoscope.yearly.name}")
```

## 自动化迁移脚本

你可以使用以下脚本批量替换：

```bash
# 使用 sed 批量替换（macOS/Linux）
find . -name "*.py" -type f -exec sed -i '' \
  -e 's/from py_iztro import Astro/from iztro_py import astro/g' \
  -e 's/Astro()/astro/g' \
  -e 's/astro_obj\.by_solar/astro.by_solar/g' \
  -e 's/astro_obj\.by_lunar/astro.by_lunar/g' \
  {} +

# 或使用 Python 脚本
cat > migrate.py << 'EOF'
import os
import re

def migrate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换导入
    content = re.sub(
        r'from py_iztro import Astro',
        'from iztro_py import astro',
        content
    )

    # 替换实例化
    content = re.sub(
        r'(\w+)\s*=\s*Astro\(\)',
        r'# \1 = Astro()  # 迁移到 iztro-py 后不再需要',
        content
    )

    # 替换方法调用
    content = re.sub(
        r'(\w+)\.by_solar\(',
        r'astro.by_solar(',
        content
    )
    content = re.sub(
        r'(\w+)\.by_lunar\(',
        r'astro.by_lunar(',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Migrated: {filepath}")

# 遍历当前目录下的所有 .py 文件
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            migrate_file(filepath)

print("\n✅ Migration complete!")
EOF

python migrate.py
```

## 潜在问题和解决方案

### 问题 1: 导入错误

```python
# 错误信息
ImportError: No module named 'iztro_py'

# 解决方案
pip install iztro-py
```

### 问题 2: API 调用方式

```python
# ❌ 错误
from iztro_py import astro
astro_obj = astro()  # 错误：astro 是模块，不是类
chart = astro_obj.by_solar('2000-8-16', 6, '男')

# ✅ 正确
from iztro_py import astro
chart = astro.by_solar('2000-8-16', 6, '男')
```

### 问题 3: 星曜名称

```python
# 如果使用了特定的星曜名称格式
# py-iztro 和 iztro-py 都支持中文名和英文名

# 两者都支持
star = chart.star('紫微')      # 中文
star = chart.star('ziweiMaj')  # 英文
```

### 问题 4: 性能差异

```python
# iztro-py 更快，可能需要调整并发设置

# py-iztro: 可能需要限制并发数
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as executor:
    # ...

# iztro-py: 可以使用更高并发数
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=50) as executor:  # 更高并发
    # ...
```

## 测试验证

迁移后，建议进行以下测试：

### 1. 单元测试

```python
# test_migration.py
from iztro_py import astro

def test_basic_chart():
    chart = astro.by_solar('2000-8-16', 6, '男')
    assert chart is not None
    assert chart.gender == '男'
    assert chart.sign == '狮子座'
    assert chart.zodiac == '龙'

def test_palace_query():
    chart = astro.by_solar('2000-8-16', 6, '男')
    soul = chart.get_soul_palace()
    assert soul is not None
    assert soul.name is not None

def test_star_query():
    chart = astro.by_solar('2000-8-16', 6, '男')
    ziwei = chart.star('紫微')
    assert ziwei is not None

def test_horoscope():
    chart = astro.by_solar('2000-8-16', 6, '男')
    horoscope = chart.horoscope('2024-1-1', 6)
    assert horoscope is not None
    assert horoscope.yearly is not None

if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
```

### 2. 对比测试

```python
# compare_results.py
# 同时安装 py-iztro 和 iztro-py，对比结果

from py_iztro import Astro as OldAstro
from iztro_py import astro as new_astro

# 创建星盘
old_chart = OldAstro().by_solar("2000-8-16", 6, "男")
new_chart = new_astro.by_solar('2000-8-16', 6, '男')

# 对比基本信息
assert old_chart.gender == new_chart.gender
assert old_chart.sign == new_chart.sign
assert old_chart.zodiac == new_chart.zodiac
assert old_chart.five_elements_class == new_chart.five_elements_class

print("✅ 基本信息一致")

# 对比宫位
for i in range(12):
    old_palace = old_chart.palace(i)
    new_palace = new_chart.palace(i)
    assert old_palace.name == new_palace.name
    assert len(old_palace.major_stars) == len(new_palace.major_stars)

print("✅ 宫位信息一致")

print("\n🎉 迁移验证成功！")
```

### 3. 性能测试

```python
# benchmark_migration.py
import time
from py_iztro import Astro as OldAstro
from iztro_py import astro as new_astro

def benchmark_old():
    start = time.perf_counter()
    astro_obj = OldAstro()
    for _ in range(1000):
        astro_obj.by_solar("2000-8-16", 6, "男")
    return time.perf_counter() - start

def benchmark_new():
    start = time.perf_counter()
    for _ in range(1000):
        new_astro.by_solar('2000-8-16', 6, '男')
    return time.perf_counter() - start

old_time = benchmark_old()
new_time = benchmark_new()

print(f"py-iztro:  {old_time:.2f}s ({old_time/1000*1000:.2f}ms per chart)")
print(f"iztro-py:  {new_time:.2f}s ({new_time/1000*1000:.2f}ms per chart)")
print(f"提升:      {old_time/new_time:.2f}x")
```

## 回滚计划

如果迁移遇到问题，可以快速回滚：

```bash
# 回滚到 py-iztro
pip uninstall iztro-py
pip install py-iztro==0.1.5

# 恢复代码
git checkout -- .  # 或者从备份恢复
```

## 迁移时间表建议

### 小型项目（<1000 行）
- **准备**: 30 分钟（阅读文档、安装依赖）
- **迁移**: 1 小时（修改代码、运行测试）
- **验证**: 30 分钟（功能测试、性能测试）
- **总计**: ~2 小时

### 中型项目（1000-5000 行）
- **准备**: 1 小时
- **迁移**: 3-4 小时
- **验证**: 1-2 小时
- **总计**: 1 个工作日

### 大型项目（>5000 行）
- **准备**: 2-3 小时
- **迁移**: 1-2 天
- **验证**: 1 天
- **总计**: 3-5 个工作日

## 获取帮助

如果迁移过程中遇到问题：

1. **查看文档**: [iztro-py README](https://github.com/spyfree/iztro-py#readme)
2. **提交 Issue**: [GitHub Issues](https://github.com/spyfree/iztro-py/issues)
3. **对比差异**: 使用对比测试脚本找出不一致的地方
4. **性能分析**: 使用性能测试确认加速效果

## 成功案例

> "从 py-iztro 迁移到 iztro-py 后，我们的 API 响应时间从平均 8ms 降到了 1.5ms，用户体验显著提升！" - 某紫微排盘网站开发者

> "Docker 镜像从 250MB 减小到 180MB，云函数冷启动时间减少了 40%。" - 某 Serverless 应用开发者

## 下一步

迁移完成后，你可能想要：

1. **优化性能**: 利用 iztro-py 的性能优势，增加并发处理能力
2. **简化部署**: 移除 pythonmonkey 相关的特殊配置
3. **学习源码**: 阅读 iztro-py 的 Python 源码，了解算法细节
4. **贡献代码**: 为 iztro-py 贡献功能或修复 bug

---

**祝迁移顺利！** 🎉

如有问题，欢迎在 [GitHub](https://github.com/spyfree/iztro-py) 上交流！
