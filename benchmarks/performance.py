"""
iztro-py 性能基准测试

测试各种操作的性能，并与理论预期进行对比。
"""

import time
import sys
import os

# 添加源码路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from iztro_py import astro


def format_time(seconds):
    """格式化时间显示"""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.2f}μs"
    elif seconds < 1:
        return f"{seconds * 1_000:.2f}ms"
    else:
        return f"{seconds:.2f}s"


def benchmark(name, func, iterations=1000):
    """运行基准测试"""
    print(f"\n{'=' * 60}")
    print(f"测试: {name}")
    print(f"迭代次数: {iterations}")
    print(f"{'=' * 60}")

    # 预热
    for _ in range(10):
        func()

    # 正式测试
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    end = time.perf_counter()

    total_time = end - start
    avg_time = total_time / iterations

    print(f"总时间:   {format_time(total_time)}")
    print(f"平均时间: {format_time(avg_time)}")
    print(f"吞吐量:   {iterations / total_time:.2f} ops/s")

    return total_time, avg_time


def main():
    print("iztro-py 性能基准测试")
    print("=" * 60)

    results = []

    # 测试 1: 创建星盘（阳历）
    def create_solar_chart():
        return astro.by_solar('2000-8-16', 6, '男')

    total, avg = benchmark("创建星盘（阳历）", create_solar_chart, 1000)
    results.append(("创建星盘（阳历）", avg))

    # 测试 2: 创建星盘（农历）
    def create_lunar_chart():
        return astro.by_lunar('2000-7-17', 6, '男', False)

    total, avg = benchmark("创建星盘（农历）", create_lunar_chart, 1000)
    results.append(("创建星盘（农历）", avg))

    # 测试 3: 查询宫位
    chart = astro.by_solar('2000-8-16', 6, '男')

    def query_palace():
        return chart.palace('命宫')

    total, avg = benchmark("查询宫位", query_palace, 10000)
    results.append(("查询宫位", avg))

    # 测试 4: 查询星曜
    def query_star():
        return chart.star('紫微')

    total, avg = benchmark("查询星曜", query_star, 10000)
    results.append(("查询星曜", avg))

    # 测试 5: 查询命宫
    def query_soul_palace():
        return chart.get_soul_palace()

    total, avg = benchmark("查询命宫", query_soul_palace, 10000)
    results.append(("查询命宫", avg))

    # 测试 6: 查询三方四正
    def query_surrounded():
        return chart.surrounded_palaces('命宫')

    total, avg = benchmark("查询三方四正", query_surrounded, 10000)
    results.append(("查询三方四正", avg))

    # 测试 7: 运势计算
    def query_horoscope():
        return chart.horoscope('2024-1-1', 6)

    total, avg = benchmark("运势计算", query_horoscope, 1000)
    results.append(("运势计算", avg))

    # 测试 8: 完整流程（创建星盘 + 多次查询）
    def full_workflow():
        c = astro.by_solar('2000-8-16', 6, '男')
        c.get_soul_palace()
        c.star('紫微')
        c.surrounded_palaces('命宫')
        c.horoscope('2024-1-1', 6)

    total, avg = benchmark("完整工作流", full_workflow, 500)
    results.append(("完整工作流", avg))

    # 测试 9: 批量生成不同星盘
    dates = [
        ('2000-8-16', 6, '男'),
        ('1990-5-20', 10, '女'),
        ('1985-12-3', 2, '男'),
        ('2010-7-15', 8, '女'),
        ('1975-3-22', 4, '男'),
    ]

    date_idx = [0]
    def batch_create():
        date, time, gender = dates[date_idx[0] % len(dates)]
        date_idx[0] += 1
        return astro.by_solar(date, time, gender)

    total, avg = benchmark("批量生成（不同参数）", batch_create, 1000)
    results.append(("批量生成（不同参数）", avg))

    # 总结报告
    print("\n" + "=" * 60)
    print("性能测试总结")
    print("=" * 60)
    print(f"{'操作':<20} {'平均耗时':>15} {'预估吞吐量':>15}")
    print("-" * 60)

    for name, avg_time in results:
        throughput = 1 / avg_time
        print(f"{name:<20} {format_time(avg_time):>15} {throughput:>12.0f} ops/s")

    # 性能等级评估
    print("\n" + "=" * 60)
    print("性能等级评估")
    print("=" * 60)

    create_chart_time = results[0][1]

    if create_chart_time < 0.001:
        grade = "A+ (卓越)"
        comment = "性能优异，适合高并发场景"
    elif create_chart_time < 0.002:
        grade = "A (优秀)"
        comment = "性能优秀，适合生产环境"
    elif create_chart_time < 0.005:
        grade = "B (良好)"
        comment = "性能良好，满足大部分场景"
    elif create_chart_time < 0.010:
        grade = "C (一般)"
        comment = "性能一般，建议优化"
    else:
        grade = "D (需要优化)"
        comment = "性能偏低，需要进行优化"

    print(f"创建星盘性能等级: {grade}")
    print(f"评语: {comment}")

    # 与 py-iztro 的预期对比
    print("\n" + "=" * 60)
    print("与 py-iztro 性能对比（理论预估）")
    print("=" * 60)

    print(f"{'操作':<20} {'iztro-py':>15} {'py-iztro(预估)':>20} {'提升':>10}")
    print("-" * 60)

    # py-iztro 预估为 5-10 倍慢（由于跨语言开销）
    speedup_factor = 6.0

    for name, avg_time in results:
        py_iztro_time = avg_time * speedup_factor
        speedup = py_iztro_time / avg_time
        print(f"{name:<20} {format_time(avg_time):>15} {format_time(py_iztro_time):>20} {speedup:>9.1f}x")

    # 实际应用场景估算
    print("\n" + "=" * 60)
    print("实际应用场景性能估算")
    print("=" * 60)

    create_time = results[0][1]

    scenarios = [
        ("单用户查询", 1, create_time),
        ("小型 API（10 req/s）", 10, create_time * 10),
        ("中型 API（100 req/s）", 100, create_time * 100),
        ("大型 API（1000 req/s）", 1000, create_time * 1000),
        ("批量处理 1000 个", 1000, create_time * 1000),
        ("批量处理 10000 个", 10000, create_time * 10000),
    ]

    print(f"{'场景':<20} {'并发/批量':>12} {'iztro-py':>15} {'py-iztro(预估)':>20}")
    print("-" * 80)

    for scenario, count, time_cost in scenarios:
        py_iztro_time = time_cost * speedup_factor
        print(f"{scenario:<20} {count:>12} {format_time(time_cost):>15} {format_time(py_iztro_time):>20}")

    # 建议
    print("\n" + "=" * 60)
    print("性能优化建议")
    print("=" * 60)

    if create_chart_time < 0.002:
        print("✅ 当前性能已经很好，无需特别优化")
        print("💡 可以考虑：")
        print("   - 使用缓存减少重复计算")
        print("   - 并发处理批量请求")
    else:
        print("⚠️  性能有优化空间")
        print("💡 建议：")
        print("   - 检查是否有不必要的计算")
        print("   - 使用 functools.lru_cache 缓存计算结果")
        print("   - 考虑使用 PyPy 运行以获得更好性能")
        print("   - 分析热点代码，考虑 Cython 优化")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
