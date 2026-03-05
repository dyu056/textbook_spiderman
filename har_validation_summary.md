# HAR文件验证汇总报告

验证时间: 2026-02-04
验证工具: validate_har_data.py
验证标准:
- 占位符率 < 5%
- 章节连续完整
- 习题覆盖率 > 80%（支持多小节）

## 验证结果总览

| 状态 | 数量 | 占比 |
|------|------|------|
| ✓ 可用 | 11 | 61% |
| ❌ 不可用 | 7 | 39% |
| **总计** | **18** | **100%** |

---

## ✓ 可用文件 (11个)

### 1. Calculus.har
- **书籍**: Calculus 8th Edition (9781285740621)
- **题数**: 11,790题
- **章节**: 19章
- **占位符率**: 0%
- **连续性**: 100%
- **评价**: ✓ 优秀

### 2. College Algebra  An Early Functions Approach.har
- **书籍**: College Algebra 2nd Edition (9780077836344)
- **题数**: 6,615题
- **章节**: 9章
- **占位符率**: 0%
- **连续性**: 100%
- **评价**: ✓ 优秀

### 3. College Algebra(10th Edition).har
- **书籍**: College Algebra 10th Edition (9780321999412)
- **题数**: 8,372题
- **章节**: 12章
- **占位符率**: 0%
- **连续性**: 100%
- **评价**: ✓ 优秀

### 4. College Algebra.har
- **书籍**: College Algebra 7th Edition (9780134469164)
- **题数**: 8,087题
- **章节**: 9章
- **占位符率**: 0%
- **连续性**: 100%
- **评价**: ✓ 优秀

### 5. Essential Calculus Early Transcendentals.har
- **书籍**: Essential Calculus Early Transcendentals 2nd Edition (9781133112280)
- **题数**: 1,776题
- **章节**: 15章
- **占位符率**: 0%
- **连续性**: 96.7%
- **评价**: ✓ 优秀

### 6. Essential Calculus.har
- **书籍**: Essential Calculus 2nd Edition (9781133112297)
- **题数**: 2,024题
- **章节**: 13章
- **占位符率**: 0%
- **连续性**: 97.7%
- **评价**: ✓ 优秀

### 7. Multivariable Calculus.har
- **书籍**: Calculus 8th Edition (9781285740621)
- **题数**: 3,714题
- **章节**: 11章
- **占位符率**: 0%
- **连续性**: 100%
- **评价**: ✓ 优秀

### 8. Prealgebra & Introductory Algebra.har
- **书籍**: Prealgebra Introductory Algebra 1st Edition (9780073512952)
- **题数**: 7,476题
- **章节**: 17章
- **占位符率**: 0%
- **连续性**: 100%
- **评价**: ✓ 优秀

### 9. Prealgebra(2nd Edition).har
- **书籍**: Prealgebra 2nd Edition (9780073384474)
- **题数**: 8,401题
- **章节**: 10章
- **占位符率**: 0%
- **连续性**: 100%
- **评价**: ✓ 优秀

### 10. Single Variable Calculus Early Transcendentals.har
- **书籍**: Single Variable Calculus Early Transcendentals 8th Edition (9781305270336)
- **题数**: 823题
- **章节**: 7章
- **占位符率**: 0%
- **连续性**: 98.6%
- **评价**: ✓ 优秀

### 11. Single Variable Essential Calculus.har
包含2本书：
- **Calculus 8th Edition**: 3,538题, 0%占位符, 97.5%连续性 ✓
- **Single Variable Essential Calculus 2nd Edition**: 1,793题, 0%占位符, 97.8%连续性 ✓

---

## ❌ 不可用文件 (7个)

### 1. Algebra and Trigonometry.har
- **原因**: 占位符过多 (92.96%)
- **书籍**: Algebra and Trigonometry 6th Edition
- **题数**: 152题
- **问题**: 原始数据包含大量Lorem Ipsum占位符文本

### 2. Calculus  Early Transcendentals.har
- **原因**: 占位符过多 (72.59%)
- **书籍**: Calculus Early Transcendentals 8th Edition
- **题数**: 803题
- **问题**: 原始数据包含大量Lorem Ipsum占位符文本

### 3. Calculus Early Transcendentals.har
- **原因**: 占位符过多 (91.63%)
- **书籍**: Calculus 3rd Edition / Calculus Early Transcendentals 3rd Edition
- **题数**: 9,760题
- **问题**: 原始数据包含大量Lorem Ipsum占位符文本

### 4. Calculus, Multivariable.har
- **原因**: 占位符过多 (94.59%)
- **书籍**: Calculus 3rd Edition
- **题数**: 6,393题
- **问题**: 原始数据包含大量Lorem Ipsum占位符文本

### 5. Calculus, Single Variable Early Transcendentals.har
- **原因**: 占位符过多 (95.75%)
- **书籍**: Calculus 3rd Edition
- **题数**: 5,954题
- **问题**: 原始数据包含大量Lorem Ipsum占位符文本

### 6. Precalculus.har
- **原因**: 占位符过多 (91.37%)
- **书籍**: College Algebra 2nd Edition / Precalculus 6th Edition等
- **题数**: 11,803题
- **问题**: 原始数据包含大量Lorem Ipsum占位符文本

### 7. Single Variable Calculus.har
- **原因**: 习题不连续
- **书籍**: Single Variable Calculus 8th Edition
- **题数**: 560题
- **章节**: 13章
- **问题**: 多个章节缺失大量习题，平均连续性仅64.2%

---

## 推荐使用的数据

基于验证结果，推荐使用以下3本教材的数据（无占位符，章节完整，习题连续）：

1. **College Algebra 10th Edition** (9780321999412)
   - 来源: College Algebra(10th Edition).har
   - 6,303题，12章，质量优秀

2. **Prealgebra 2nd Edition** (9780073384474)
   - 来源: Prealgebra(2nd Edition).har
   - 8,396题，10章，质量优秀

3. **Prealgebra Introductory Algebra 1st Edition** (9780073512952)
   - 来源: Prealgebra & Introductory Algebra.har
   - 7,454题，17章，质量优秀

**总计: 22,153道高质量题目**

这3本教材的数据已清洗到 `clean_output_1/` 目录。

---

## 占位符问题分析

### 受影响的书籍

| 书籍 | 占位符率 | 状态 |
|------|----------|------|
| Calculus 3rd Edition | 95-96% | 严重 |
| Algebra and Trigonometry 6th Edition | 93% | 严重 |
| Calculus Early Transcendentals 3rd/8th Edition | 72-92% | 严重 |
| College Algebra 2nd Edition (部分) | 91% | 严重 |
| Precalculus 6th Edition (部分) | 91% | 严重 |

### 占位符特征

原始数据中的占位符包含以下Lorem Ipsum文本：
- "lorem ipsum dolor sit amet"
- "consectetur adipiscing elit"
- "pellentesque dapibus efficitur"
- "facilisis mauris sit amet"
- "laoreet ac dictum vitae"

这些占位符表明CourseHero数据库中的原始内容未完成或被测试数据覆盖。

---

## 使用建议

### 数据清洗流程

```bash
# 1. 验证HAR文件
python3 validate_har_data.py spider_data/Math/*.har

# 2. 仅清洗可用的数据
python3 clean_valid_math_data.py

# 3. 输出目录
# clean_output_1/ - 高质量数据（3本书，22,153题）
```

### 质量标准

推荐使用符合以下标准的数据：
- ✓ 占位符率 < 1%
- ✓ 章节完整连续
- ✓ 习题覆盖率 > 95%
- ✓ 无大段缺失（最大连续缺失 < 5个）

---

生成时间: 2026-02-04
验证工具版本: validate_har_data.py v1.0
