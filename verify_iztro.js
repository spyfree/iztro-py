// 使用原始 iztro JS 库验证
// npm install iztro

const { astro } = require('iztro');

console.log('=' .repeat(80));
console.log('原始 iztro (JavaScript) 排盘验证');
console.log('日期: 1989-10-17 午时');
console.log('=' .repeat(80));

// 测试不同的小时参数
const hours = [11, 12, 13];

hours.forEach(hour => {
    console.log(`\n${'='.repeat(80)}`);
    console.log(`使用 hour=${hour}`);
    console.log('='.repeat(80));

    const result = astro.bySolar('1989-10-17', hour, 'male', true, 'zh-CN');

    console.log(`\n基本信息:`);
    console.log(`  五行局: ${result.fiveElementsClass}`);
    console.log(`  命宫地支: ${result.earthlyBranchOfSoulPalace}`);
    console.log(`  身宫地支: ${result.earthlyBranchOfBodyPalace}`);
    console.log(`  农历: ${result.lunarDate}`);
    console.log(`  四柱: ${result.chineseDate}`);

    // 找父母宫
    const parentsPalace = result.palaces.find(p => p.name === '父母');
    if (parentsPalace) {
        const stars = parentsPalace.majorStars.map(s => s.name);
        console.log(`\n父母宫:`);
        console.log(`  地支: ${parentsPalace.earthlyBranch}`);
        console.log(`  天干: ${parentsPalace.heavenlyStem}`);
        console.log(`  主星: ${stars.length > 0 ? stars.join('、') : '无主星'}`);
    }

    console.log(`\n所有宫位主星:`);
    result.palaces.forEach(p => {
        const stars = p.majorStars.map(s => s.name);
        console.log(`  ${p.name}(${p.earthlyBranch}): ${stars.length > 0 ? stars.join('、') : '无'}`);
    });
});
