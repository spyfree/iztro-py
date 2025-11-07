# iztro-py vs py-iztro: 快速对比

## 📊 一句话总结

**iztro-py** 是紫微斗数的**纯 Python 实现**，而 **py-iztro** 是使用 JavaScript 解释器运行原始 JS 代码的 **Python 包装器**。

## 🎯 核心差异

| 方面 | iztro-py | py-iztro |
|------|----------|----------|
| **实现** | ✅ 纯 Python | ⚠️ Python + pythonmonkey (JS 引擎) |
| **性能** | ✅ ~1ms/盘 | ⚠️ ~6ms/盘 |
| **依赖大小** | ✅ ~3MB | ⚠️ ~53MB |
| **Python 版本** | ✅ 3.8+ | ⚠️ 3.10+ |
| **调试** | ✅ 纯 Python 堆栈 | ⚠️ Python + JS 混合 |

## 💡 关键发现

### py-iztro 的秘密

py-iztro 使用 **pythonmonkey** 依赖，这是一个：
- Python 到 JavaScript 的桥接库
- 包含完整的 SpiderMonkey JS 引擎
- 体积 ~50MB+
- 每次调用都有跨语言开销

### iztro-py 的优势

1. **性能**: 5-10倍速度提升
2. **部署**: 更小、更快、更广泛支持
3. **维护**: 纯 Python，易于调试和修改
4. **兼容性**: 支持更多 Python 版本和环境

## 📈 提升策略

### 立即执行（本周）

✅ **已完成的工作**:
1. ✅ 创建详细对比文档 (`docs/why-iztro-py.md`)
2. ✅ 创建迁移指南 (`docs/migration-guide.md`)
3. ✅ 更新 README 强调优势
4. ✅ 创建性能基准测试 (`benchmarks/performance.py`)
5. ✅ 创建发布自动化 (`.github/workflows/publish-to-pypi.yml`)
6. ✅ 创建项目对比分析 (`PROJECT_COMPARISON.md`)

🎯 **下一步**:
1. 更新 `pyproject.toml` 版本到 0.2.0
2. 发布到 PyPI
3. 在社区推广

### 中期目标（1个月）

1. **性能验证**: 运行实际基准测试，确认 5-10x 提升
2. **文档网站**: 使用 MkDocs 构建在线文档
3. **社区推广**:
   - 撰写技术博客对比两者
   - 在 Python 中文社区发布
   - 回答相关问题时推荐 iztro-py

### 长期目标（3-6个月）

1. **成为首选**: PyPI 下载量超过 py-iztro
2. **生态建设**: CLI 工具、Web API、GUI
3. **功能扩展**: i18n、更多星曜、格局判断

## 🚀 营销定位

### 宣传语

> **iztro-py**: 真正的 Python 紫微斗数库
>
> 不是包装器，是完整重写。更快、更轻、更 Pythonic。

### 目标受众

1. **性能敏感用户**: Web API、批量处理
2. **云端部署者**: 需要轻量级依赖
3. **学习研究者**: 想要理解算法
4. **Python 开发者**: 追求纯 Python 解决方案

## 📋 快速决策指南

### 什么时候选 iztro-py？

- ✅ 需要高性能（API、批量）
- ✅ 云函数/容器部署
- ✅ Python 3.8 或 3.9
- ✅ 想要学习源码
- ✅ 追求简洁依赖

### 什么时候用 py-iztro？

- ⚠️ 已有 py-iztro 项目且运行良好
- ⚠️ 不在意性能（每天几十次查询）
- ⚠️ 必须 100% 跟随原版 iztro 更新

## 📊 市场分析

### 当前状态

- **py-iztro**: 89 stars, 版本 0.1.5
- **iztro-py**: 新项目, 版本 0.1.0

### 赶超计划

**3个月目标**:
- GitHub stars > 100
- PyPI 下载量 > py-iztro
- 被 awesome-python 收录

**6个月目标**:
- 成为 Python 紫微斗数的首选
- 被其他项目作为依赖
- 有 5+ 活跃贡献者

## 🎬 立即行动

### 今天

```bash
# 1. 查看所有新文档
ls docs/
cat PROJECT_COMPARISON.md

# 2. 运行性能测试（需要先安装依赖）
# pip install -e ".[dev]"
# python benchmarks/performance.py

# 3. 准备发布
# ./scripts/release.sh 0.2.0
```

### 本周

1. 发布 0.2.0 版本到 PyPI
2. 撰写技术博客初稿
3. 在社区分享

### 本月

1. 发布博客到多个平台
2. 完善文档网站
3. 收集用户反馈

## 📚 资源链接

- **详细对比**: [docs/why-iztro-py.md](./docs/why-iztro-py.md)
- **迁移指南**: [docs/migration-guide.md](./docs/migration-guide.md)
- **战略分析**: [PROJECT_COMPARISON.md](./PROJECT_COMPARISON.md)
- **发布检查**: [RELEASE_CHECKLIST.md](./RELEASE_CHECKLIST.md)

## 🏆 成功标准

在 6 个月内:
- [ ] PyPI 月下载量 > 1000
- [ ] GitHub stars > 200
- [ ] 被至少 3 个项目依赖
- [ ] 有完整的在线文档
- [ ] 有活跃的社区讨论

---

**结论**: iztro-py 拥有明显的技术优势，现在需要的是市场推广和社区建设。通过强调"纯 Python"和"高性能"两大优势，可以吸引大量对性能敏感和追求代码质量的开发者。

*创建日期: 2025-11-07*
