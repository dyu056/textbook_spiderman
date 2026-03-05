# Textbook Spiderman - 教材习题数据清洗工具

从CourseHero HAR文件中提取和清洗数学教材习题数据的工具集。

## 功能特性

- 🕷️ 从HAR文件提取CourseHero习题数据
- 🧹 清洗和标准化数据格式
- 📊 自动检测和过滤占位符数据
- 🔢 全局连续编号系统
- ✅ 数据质量验证

## 目录结构

```
textbook_spiderman/
├── spider_data/           # 原始HAR数据（不上传）
│   ├── Math/             # 数学类HAR文件
│   ├── complete_data/    # 完整教材数据文件夹
│   └── incomplete_data/  # 不完整教材数据文件夹
├── clean_output/         # 清洗后的数据（不上传）
├── clean_output_1/       # 高质量数据输出（不上传）
├── clean_math_data.py    # 清洗所有书籍
├── clean_complete_math_data.py  # 清洗完整书籍
├── clean_valid_math_data.py     # 清洗无占位符书籍
├── validate_har_data.py  # HAR数据验证工具
├── count_math_types.py   # 统计题型分布
└── doc/                  # 文档
    ├── math_data_schema.md
    ├── math_question_types_samples.md
    └── math_ui_data_structure.md
```

## 快速开始

### 1. 验证HAR文件质量

验证单个文件：
```bash
python3 validate_har_data.py spider_data/Math/Calculus.har
```

批量验证所有HAR文件：
```bash
python3 validate_har_data.py spider_data/Math/*.har
```

**验证标准：**
- ✅ 无Lorem Ipsum占位符（< 5%）
- ✅ 章节连续完整
- ✅ 每章习题基本连续（覆盖率 > 80%，支持多小节）

### 2. 清洗数据

清洗所有书籍：
```bash
python3 clean_math_data.py
# 输出到 clean_output/
```

清洗完整书籍（基于book_chapter_summary.txt标注）：
```bash
python3 clean_complete_math_data.py
# 输出到 clean_output/
```

清洗高质量书籍（无占位符）：
```bash
python3 clean_valid_math_data.py
# 输出到 clean_output_1/
```

### 3. 统计题型

```bash
python3 count_math_types.py
```

## 数据格式

### 输出结构

```
clean_output_1/
└── College-Algebra-10th-Edition-9780321999412-6/
    ├── catalog.json                    # 书籍目录
    └── answers/
        ├── 1-ch-r-problem-1.json      # 习题答案
        ├── 2-ch-r-problem-2.json
        └── ...
```

### catalog.json

```json
{
  "bookSlug": "College-Algebra-10th-Edition-9780321999412-6",
  "bookTitle": "College Algebra 10th Edition",
  "bookIsbn": "9780321999412",
  "bookEdition": "10th-Edition",
  "chapters": [
    {
      "nodeId": "ch-r",
      "label": "Chapter R",
      "exercises": [
        {"pageId": "1-ch-r-problem-1", "label": "Exercise 1"},
        {"pageId": "2-ch-r-problem-2", "label": "Exercise 2"}
      ]
    }
  ]
}
```

### 答案文件格式

```json
{
  "AnswerContent": [
    {
      "solution": {
        "contentId": 1,
        "type": "calc",
        "parts": [
          {
            "result": [
              {
                "title": "The Answer",
                "flow": [
                  {"render": "html", "value": "<p>答案内容...</p>"}
                ]
              }
            ],
            "steps": [
              {
                "stepId": 1,
                "title": "Step 1",
                "flow": [
                  {"render": "html", "value": "<p>解题步骤...</p>"}
                ]
              }
            ]
          }
        ]
      },
      "tips": [],
      "meta": {
        "solutionId": 123456,
        "sourceType": "tbq",
        "authoredDate": "2020-01-01 00:00:00"
      }
    }
  ],
  "nav": {
    "prevId": "1-ch-r-problem-1",
    "nextId": "3-ch-r-problem-3"
  },
  "pageId": "2-ch-r-problem-2",
  "problemId": "2",
  "bookSlug": "College-Algebra-10th-Edition-9780321999412-6",
  "chapterTag": "r",
  "problemNo": "2"
}
```

## 数据质量

### 高质量教材（clean_output_1）

| 教材 | ISBN | 题数 | 占位符率 |
|------|------|------|----------|
| College Algebra 10th Edition | 9780321999412 | 6,303 | 0% |
| Prealgebra 2nd Edition | 9780073384474 | 8,396 | 0% |
| Prealgebra Introductory Algebra 1st Edition | 9780073512952 | 7,454 | 0% |

**总计：3本教材，22,153道题目**

### 题型分布

支持13种题型：
- `calc` - 计算题
- `mcq` - 单选题
- `ms` - 多选题
- `sa` - 简答题
- `fib` - 填空题
- `mat` - 匹配题
- `gr` - 图形题
- `tcq` - 判断题
- `ord` - 排序题
- `cl` - 分类题
- `es` - 论述题
- `drw` - 绘图题
- `tutor_answer` - 辅导答案

## 清洗逻辑

### 数据提取流程

1. **HAR文件解析**
   - 从HAR文件的response中提取JSON数据
   - 解析canonicalUrl获取书籍/章节/题号信息

2. **去重与排序**
   - 按canonicalUrl去重（同一题目可能出现在多个HAR文件）
   - 按origid（CourseHero内部ID）排序，保证正确顺序

3. **数据转换**
   ```
   原始数据                        清洗后
   ─────────────────────────────────────
   answer.widgets        →    result.flow
   answer.explanations   →    steps
   hints                 →    tips
   widget.text           →    flow.value (原样保留)
   ```

4. **全局编号**
   - 为所有题目分配连续的全局ID（1, 2, 3...）
   - pageId格式：`{全局ID}-ch-{章节}-problem-{题号}`

### 占位符检测

检测以下Lorem Ipsum特征：
- lorem ipsum
- consectetur adipiscing
- pellentesque dapibus
- facilisis
- laoreet
- donec aliquet

## 开发

### 依赖

```bash
# Python 3.7+
# 无第三方依赖，仅使用标准库
```

### 运行测试

```bash
# 验证所有HAR文件
python3 validate_har_data.py spider_data/Math/*.har

# 清洗测试
python3 clean_valid_math_data.py

# 检查输出
ls -lh clean_output_1/
```

## 数据来源

数据通过Chrome DevTools抓取CourseHero网站的HAR文件获得。

**注意：** 原始HAR文件和清洗后的数据由于文件较大，已在`.gitignore`中排除，不上传到Git仓库。

## License

MIT

## 作者

- 数据清洗工具：Co-Authored-By Claude Sonnet 4.5
- 项目维护：dyu056
