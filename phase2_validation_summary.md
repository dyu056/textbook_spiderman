# 第二期数据验证结果

验证时间: 2026-02-04
数据位置: math_spider/第二期/
验证方法: validate_har_data.py（支持文件夹合并验证）

## 总体结果

| 状态 | 数量 | 说明 |
|------|------|------|
| ✓ 可用 | **0** | 无占位符，数据完整 |
| ❌ 不可用 | **25** | 占位符率 74-94% |
| **总计** | **25** | 包含19个数据源（7个文件夹+12个文件） |

## ⚠️ 严重问题：全部数据不可用

**所有25本书都包含大量Lorem Ipsum占位符（74-94%），无法使用。**

---

## 详细检测结果

### 占位符率排行（从高到低）

| 排名 | 书籍 | 占位符率 | 题数 |
|------|------|----------|------|
| 1 | Linear Algebra and Its Applications 5th Edition | **94.13%** | 2,776 |
| 2 | Calculus 3rd Edition | **93.08%** | 10,241 |
| 3 | College Algebra Enhanced with Graphing Utilities 7th Edition | **92.41%** | 1,515 |
| 4 | Thomas' Calculus Early Transcendentals 14th Edition | **91.20%** | 5,739 |
| 5 | Precalculus 6th Edition | **91.19%** | 4,667 |
| 6 | Precalculus Enhanced with Graphing Utilities 7th Edition | **90.76%** | 4,849 |
| 7 | College Algebra with Modeling & Visualization 6th Edition | **90.66%** | 9,557 |
| 8 | College Algebra 7th Edition | **90.39%** | 8,520 |
| 9 | College Algebra 10th Edition (多个来源) | **88-90%** | 多份数据 |
| 10 | College Algebra 2nd Edition | **89.33%** | 11,285 |
| 11 | Trigonometry A Unit Circle Approach 11th Edition | **89.29%** | 5,025 |
| 12 | Algebra and Trigonometry 10th Edition | **88.79%** | 3,540 |
| 13 | Thomas' Calculus Single Variable 14th Edition | **88.36%** | 3,488 |
| 14 | Algebra and Trigonometry Enhanced 7th Edition | **85.19%** | 1,141 |
| 15 | Using & Understanding Mathematics 7th Edition | **83.41%** | 4,322 |
| 16 | Intermediate Algebra 7th Edition | **83.23%** | 10,799 |
| 17 | Thinking Mathematically 7th Edition | **80.83%** | 9,872 |
| 18 | Mathematical Ideas 14th Edition | **77.63%** | 7,125 |
| 19 | Beginning and Intermediate Algebra 5th Edition | **75.35%** | 12,637 |
| 20 | Mathematics with Applications 12th Edition | **75.00%** | 7,965 |
| 21 | A Survey of Mathematics with Applications 10th Edition | **74.39%** | 8,204 |

---

## 数据源分类

### 文件夹（包含多个HAR文件）- 7个

| 文件夹名称 | HAR文件数 | 检测到的书籍 | 占位符率 |
|------------|-----------|--------------|----------|
| A Survey of Mathematics with Applications (10th Edition) | 2 | 1本 | 74.39% |
| Algebra and Trigonometry (10th Edition) | 2 | 2本 | 88-89% |
| Beginning and Intermediate Algebra(5th Edition) | 3 | 1本 | 75.35% |
| College Algebra with Modeling & Visualization (6th Edition) | 2 | 1本 | 90.66% |
| Intermediate Algebra (7th Edition) | 2 | 1本 | 83.23% |
| Precalculus(6th Edition) | 2 | 3本 | 89-91% |
| Trigonometry A Unit Circle Approach(11th Edition) | 2 | 1本 | 89.29% |

### 独立HAR文件 - 12个

| 文件名 | 书籍 | 占位符率 |
|--------|------|----------|
| Algebra and Trigonometry Enhanced with Graphing Utilities (7th Edition).har | 1本 | 85.19% |
| Calculus, Single Variable (3rd Edition).har | 1本 | 93.08% |
| College Algebra (2nd Edition).har | 1本 | 89.33% |
| College Algebra Enhanced with Graphing Utilities (7th Edition).har | 1本 | 92.41% |
| Linear Algebra and Its Applications (5th Edition).har | 1本 | 94.13% |
| Mathematical Ideas (14th Edition).har | 1本 | 77.63% |
| Mathematics with Applications (12th Edition).har | 1本 | 75.00% |
| Precalculus Enhanced with Graphing Utilities (7th Edition).har | 1本 | 90.76% |
| Thinking Mathematically (7th Edition).har | 1本 | 80.83% |
| Thomas' Calculus Early Transcendentals (14th Edition).har | 1本 | 91.20% |
| Thomas' Calculus Single Variable (14th Edition).har | 1本 | 88.36% |
| Using & Understanding Mathematics (7th Edition).har | 1本 | 83.41% |

---

## 占位符示例

第二期数据中的典型占位符内容：

```html
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
<p>Pellentesque dapibus efficitur laoreet.</p>
<p>Donec aliquet. Sed facilisis mauris sit amet est.</p>
```

这些都是标准的Lorem Ipsum测试文本，不是真实的数学内容。

---

## 对比：第一期 vs 第二期

### 第一期数据（spider_data/Math）

| 状态 | 数量 | 占比 |
|------|------|------|
| ✓ 可用 | 11 | 61% |
| ❌ 不可用 | 7 | 39% |

**高质量书籍（3本）：**
- College Algebra 10th Edition - 6,303题，0%占位符
- Prealgebra 2nd Edition - 8,396题，0%占位符
- Prealgebra Introductory Algebra 1st Edition - 7,454题，0%占位符

### 第二期数据（math_spider/第二期）

| 状态 | 数量 | 占比 |
|------|------|------|
| ✓ 可用 | 0 | 0% |
| ❌ 不可用 | 25 | 100% |

**问题：全部数据包含74-94%的占位符**

---

## 结论与建议

### 结论

**第二期数据全部不可用，原因：**

1. **占位符率极高**：所有书籍占位符率都在74-94%之间
2. **数据质量差**：原始数据中就是Lorem Ipsum测试文本
3. **无真实内容**：缺少实际的数学解答内容

### 建议

1. **不建议清洗第二期数据**
   - 即使清洗也只会得到占位符文本
   - 没有实际教学价值

2. **继续使用第一期高质量数据**
   - College Algebra 10th Edition
   - Prealgebra 2nd Edition
   - Prealgebra Introductory Algebra 1st Edition
   - 共22,153道高质量题目

3. **寻找新的数据源**
   - 第二期数据可能是CourseHero上未完成的内容
   - 需要找到包含真实解答的数据源

---

## 验证脚本功能

本次验证使用了升级后的 `validate_har_data.py`，新增功能：

✓ **支持文件夹合并验证**
- 可以验证包含多个HAR文件的文件夹
- 自动合并同一文件夹中的所有HAR数据
- 适用于分片下载的教材数据

**使用方法：**
```bash
# 验证单个文件夹（合并其中的多个HAR文件）
python3 validate_har_data.py "math_spider/第二期/Algebra and Trigonometry (10th Edition)"

# 批量验证所有文件夹和文件
python3 validate_har_data.py "math_spider/第二期"/*/ "math_spider/第二期"/*.har
```

---

生成时间: 2026-02-04
验证工具: validate_har_data.py v1.1（支持文件夹合并）
