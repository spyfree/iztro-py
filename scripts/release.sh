#!/bin/bash
# release.sh - 半自动化发布脚本
# Usage: ./scripts/release.sh <version>

set -e  # Exit on error

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "❌ Error: Version number required"
    echo "Usage: ./scripts/release.sh <version>"
    echo "Example: ./scripts/release.sh 0.2.0"
    exit 1
fi

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Releasing iztro-py version $VERSION${NC}\n"

# 检查工作目录是否干净
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  Warning: Working directory is not clean${NC}"
    echo "Uncommitted changes:"
    git status --short
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 1. 运行测试
echo -e "${GREEN}📝 Running tests...${NC}"
pytest || {
    echo -e "${RED}❌ Tests failed!${NC}"
    exit 1
}
echo -e "${GREEN}✅ Tests passed${NC}\n"

# 2. 格式化代码
echo -e "${GREEN}🎨 Formatting code...${NC}"
black src tests
echo -e "${GREEN}✅ Code formatted${NC}\n"

# 3. 类型检查
echo -e "${GREEN}🔍 Type checking...${NC}"
mypy src || {
    echo -e "${YELLOW}⚠️  Type checking has warnings${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
}
echo -e "${GREEN}✅ Type check complete${NC}\n"

# 4. 清理旧构建
echo -e "${GREEN}🧹 Cleaning old builds...${NC}"
rm -rf dist/ build/ *.egg-info src/*.egg-info
echo -e "${GREEN}✅ Cleaned${NC}\n"

# 5. 构建包
echo -e "${GREEN}📦 Building package...${NC}"
python -m build || {
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
}
echo -e "${GREEN}✅ Package built${NC}\n"

# 6. 检查包
echo -e "${GREEN}🔍 Checking package...${NC}"
twine check dist/* || {
    echo -e "${RED}❌ Package check failed!${NC}"
    exit 1
}
echo -e "${GREEN}✅ Package validated${NC}\n"

# 7. 本地测试安装
echo -e "${GREEN}🧪 Testing local installation...${NC}"
python -m venv /tmp/test_iztro_py_$$
source /tmp/test_iztro_py_$$/bin/activate
pip install -q dist/*.whl
python -c "from iztro_py import astro; chart = astro.by_solar('2000-8-16', 6, '男'); print(f'✅ Test: {chart.sign} {chart.zodiac}')" || {
    echo -e "${RED}❌ Installation test failed!${NC}"
    deactivate
    rm -rf /tmp/test_iztro_py_$$
    exit 1
}
deactivate
rm -rf /tmp/test_iztro_py_$$
echo -e "${GREEN}✅ Installation test passed${NC}\n"

# 8. 性能基准测试（可选）
echo -e "${GREEN}⚡ Running performance benchmarks (optional)...${NC}"
read -p "Run benchmarks? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python benchmarks/performance.py | head -50
fi

# 显示总结
echo -e "\n${GREEN}✅ Pre-release checks complete!${NC}\n"
echo "📋 Next steps:"
echo "1. Review CHANGELOG.md for version $VERSION"
echo "2. Update version in pyproject.toml to $VERSION"
echo "3. Commit all changes:"
echo "   git add ."
echo "   git commit -m 'Release version $VERSION'"
echo "4. Create git tag:"
echo "   git tag -a v$VERSION -m 'Release version $VERSION'"
echo "5. Push to GitHub:"
echo "   git push origin claude/compare-iztro-projects-011CUsm9nG3cDC9sgneVcqkU"
echo "   git push origin v$VERSION"
echo "6. Upload to PyPI:"
echo "   twine upload dist/*"
echo ""
echo "Or upload to TestPyPI first:"
echo "   twine upload --repository testpypi dist/*"
echo ""
echo -e "${YELLOW}⚠️  Don't forget to create a GitHub Release after pushing the tag!${NC}"
