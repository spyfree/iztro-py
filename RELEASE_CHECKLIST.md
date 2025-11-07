# Release Checklist

使用此清单确保每次发布都顺利完成。

## Pre-release (发布前)

### 1. 代码质量检查
- [ ] 所有测试通过: `pytest`
- [ ] 测试覆盖率 ≥85%: `pytest --cov=src/iztro_py --cov-report=term`
- [ ] 代码格式化: `black src tests`
- [ ] 类型检查通过: `mypy src`
- [ ] Linting 通过: `ruff check src tests`
- [ ] 无明显的 TODO 或 FIXME 标记

### 2. 文档更新
- [ ] 更新 `CHANGELOG.md` 添加新版本的变更
- [ ] 更新 `README.md` 如有必要
- [ ] 检查所有示例代码可运行
- [ ] 更新 API 文档（如有变更）
- [ ] 检查 `pyproject.toml` 中的版本号

### 3. 版本号更新
- [ ] 更新 `pyproject.toml` 中的版本号
- [ ] 遵循语义化版本规则:
  - MAJOR.MINOR.PATCH
  - MAJOR: 不兼容的 API 变更
  - MINOR: 向后兼容的新功能
  - PATCH: 向后兼容的错误修复

### 4. 依赖检查
- [ ] 检查所有依赖是否为最新稳定版本
- [ ] 验证最小 Python 版本要求
- [ ] 测试在不同 Python 版本上运行 (3.8, 3.9, 3.10, 3.11, 3.12)

### 5. 性能测试
- [ ] 运行性能基准测试: `python benchmarks/performance.py`
- [ ] 确认性能没有明显退化
- [ ] 记录性能数据到发布说明

## Release (发布)

### 6. 构建包
```bash
# 清理旧的构建文件
rm -rf dist/ build/ *.egg-info

# 构建新包
python -m build
```

- [ ] 检查构建产物: `ls dist/`
- [ ] 应该有 `.whl` 和 `.tar.gz` 文件

### 7. 本地验证
```bash
# 在虚拟环境中测试安装
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate
pip install dist/iztro_py-*.whl

# 测试导入
python -c "from iztro_py import astro; chart = astro.by_solar('2000-8-16', 6, '男'); print(chart.sign)"
```

- [ ] 包可以成功安装
- [ ] 基本功能可以使用
- [ ] 无导入错误

### 8. 检查包元数据
```bash
# 检查包的元数据
twine check dist/*
```

- [ ] 无错误或警告
- [ ] 描述正确显示

### 9. 发布到 TestPyPI (可选但推荐)
```bash
# 发布到 TestPyPI
twine upload --repository testpypi dist/*

# 从 TestPyPI 安装测试
pip install --index-url https://test.pypi.org/simple/ iztro-py
```

- [ ] 可以从 TestPyPI 安装
- [ ] 功能正常

### 10. 发布到 PyPI
```bash
# 发布到 PyPI
twine upload dist/*
```

- [ ] 发布成功
- [ ] 在 PyPI 上可见: https://pypi.org/project/iztro-py/
- [ ] 版本号正确

### 11. Git 标签和发布
```bash
# 创建 Git 标签
git tag -a v0.x.x -m "Release version 0.x.x"

# 推送标签
git push origin v0.x.x

# 或推送所有标签
git push --tags
```

- [ ] Git 标签已创建
- [ ] 标签已推送到远程仓库

### 12. GitHub Release
- [ ] 在 GitHub 上创建 Release
- [ ] 填写发布说明（从 CHANGELOG 复制）
- [ ] 上传构建产物（可选）
- [ ] 标记为 Latest Release

## Post-release (发布后)

### 13. 验证发布
```bash
# 在新的虚拟环境中测试
python -m venv verify_env
source verify_env/bin/activate
pip install iztro-py

# 运行快速测试
python -c "from iztro_py import astro; chart = astro.by_solar('2000-8-16', 6, '男'); print(chart.sign)"
```

- [ ] 可以从 PyPI 安装最新版本
- [ ] 基本功能正常
- [ ] 版本号正确: `pip show iztro-py`

### 14. 更新文档网站
- [ ] 更新在线文档（如果有）
- [ ] 更新示例代码
- [ ] 更新 changelog

### 15. 社区通知
- [ ] 在 GitHub Discussions 发布公告
- [ ] 在相关论坛/社区发布更新通知
- [ ] 更新项目主页（如果有）
- [ ] 发送邮件通知（如果有邮件列表）

### 16. 准备下一个版本
- [ ] 在 `pyproject.toml` 中更新版本号为下一个开发版本
- [ ] 在 `CHANGELOG.md` 中创建 `[Unreleased]` 部分
- [ ] 提交版本号更新: `git commit -m "Bump version to X.Y.Z-dev"`

## 回滚计划

如果发布后发现严重问题:

### 紧急回滚步骤
1. **不要删除 PyPI 上的版本**（PyPI 不允许）
2. **发布修复版本**:
   ```bash
   # 修复问题
   # 更新版本号（patch version +1）
   # 发布新版本
   ```

3. **或发布 yank 标记**（不推荐作为第一选择）:
   - 在 PyPI 项目页面标记版本为 "yanked"
   - 不会从 PyPI 删除，但不会被默认安装

### 问题处理流程
1. 在 GitHub Issues 创建紧急问题
2. 评估严重程度
3. 决定是否需要紧急修复版本
4. 如需修复，快速通道发布
5. 通知用户升级

## 常见问题

### Q: 如何选择版本号？
A: 遵循语义化版本 (SemVer):
- 0.1.0 → 0.1.1: Bug 修复
- 0.1.0 → 0.2.0: 新功能（向后兼容）
- 0.1.0 → 1.0.0: 稳定版本或重大变更

### Q: TestPyPI 是必需的吗？
A: 不是必需的，但强烈推荐用于验证包的上传和安装流程。

### Q: 发布后发现小问题怎么办？
A: 评估严重程度：
- 严重 bug: 立即发布 patch 版本
- 小问题: 记录到下一个版本的计划中

### Q: 如何撤回已发布的版本？
A: PyPI 不允许删除版本，只能标记为 "yanked"。最好是发布修复版本。

## 自动化脚本

### 发布助手脚本
```bash
#!/bin/bash
# release.sh - 半自动化发布脚本

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh <version>"
    exit 1
fi

echo "🚀 Releasing version $VERSION"

# 运行测试
echo "📝 Running tests..."
pytest || exit 1

# 格式化代码
echo "🎨 Formatting code..."
black src tests

# 构建包
echo "📦 Building package..."
rm -rf dist/
python -m build

# 检查包
echo "🔍 Checking package..."
twine check dist/*

echo "✅ Pre-release checks complete!"
echo "Next steps:"
echo "1. Review CHANGELOG.md"
echo "2. Commit all changes"
echo "3. Run: git tag -a v$VERSION -m 'Release version $VERSION'"
echo "4. Run: twine upload dist/*"
echo "5. Push tags: git push --tags"
```

保存为 `scripts/release.sh` 并添加执行权限: `chmod +x scripts/release.sh`

## 版本发布时间表建议

- **Patch 版本** (0.1.x): 按需发布（bug 修复）
- **Minor 版本** (0.x.0): 每 1-2 个月
- **Major 版本** (x.0.0): 稳定后或重大变更

---

**最后更新**: 2025-11-07
