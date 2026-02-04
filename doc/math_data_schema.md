# Math 数据结构接口（前端渲染用）

本文档基于 `spider_data/Math/*.har` 中 `https://www.coursehero.com/api/v1/textbooks/exercises/*/content/` 响应抽样总结。
响应核心为 `questionsAndSolutions`，题干未出现在该接口中，仅包含解答与渲染素材。

## 顶层结构
```json
{
  "questionsAndSolutions": [ ... ],
  "canonicalUrl": "string",
  "isThinContent": true,
  "noindex": true
}
```

- `questionsAndSolutions`：题目+解答集合（本接口中只有解答）。
- `canonicalUrl`：教材解答页面的规范 URL。
- `isThinContent`：内容是否被标记为“内容较少/薄内容”。
- `noindex`：是否建议搜索引擎不收录。

## questionsAndSolutions[]
```json
{
  "questionId": 12345,
  "solution": { ... }
}
```

- `questionId`：题目唯一 ID。
- `solution`：解答对象。

## solution
```json
{
  "solutionId": 12345,
  "sourceType": "tbq",
  "sourceId": "001001",
  "userId": "100000000000000",
  "version": 2,
  "authoredDate": "2019-11-25 09:39:52 -0600 CST",
  "solutionContent": { ... }
}
```

- `solutionId`：解答 ID。
- `sourceType`：来源类型（如 `tbq`）。
- `sourceId`：来源标识。
- `userId`：作者/用户 ID。
- `version`：版本号。
- `authoredDate`：解答时间（字符串）。
- `solutionContent`：解答内容（含题型）。

## solutionContent
```json
{
  "type": "calc",
  "answers": [ ... ],
  "hints": [],
  "hasSameExplanationForAllAnswers": false,
  "externalLink": "https://...",
  "format": "string",
  "state": "string",
  "tutor": { ... },
  "locked": false,
  "isScorable": true,
  "takedownUrl": "https://..."
}
```

- `type`：题型编码（见“题型枚举”）。
- `answers`：答案数组（与 `type` 同步）。
- `hints`：提示数组（常为空）。
- `hasSameExplanationForAllAnswers`：是否所有答案共享同一解释。
- `externalLink`：外部链接（如视频）。
- `format`：格式标记（偶发）。
- `state`：状态字段（偶发）。
- `tutor`：导师/作者相关信息（偶发）。
- `locked`：是否锁定（偶发）。
- `isScorable`：是否可评分（偶发）。
- `takedownUrl`：下架链接（偶发）。

> 备注：`solutionContent` 字段为“并集”，具体响应中可能缺失。

## 题型枚举（Math 实际出现）
`calc`, `cl`, `drw`, `es`, `fib`, `gr`, `mat`, `mcq`, `ms`, `ord`, `sa`, `tcq`, `tutor_answer`

建议中文映射：
- `mcq`：单选题
- `ms`：多选题
- `tcq`：判断题
- `fib`：填空题
- `sa`：简答题
- `es`：论述/问答题
- `calc`：计算题
- `gr`：作图题
- `drw`：绘图题
- `ord`：排序题
- `mat`：匹配题
- `cl`：分类/分组题
- `tutor_answer`：教师/助教解答

## answers[]（按题型）
所有题型的 `answers[].type` 与 `solutionContent.type` 一致。

### 通用子结构：widgets[]
```json
{
  "type": "text",
  "text": "<p>...</p>",
  "source": "..." 
}
```

- `type`：`text` 或 `graph`。
- `text`：HTML 片段（含 `<formula>`）。
- `source`：当 `type=graph` 时，通常为 JSXGraph 脚本。

### 通用子结构：explanations[]
```json
{
  "type": "text",
  "widgets": [ ... ]
}
```
或
```json
{
  "type": "step_by_step",
  "explanations": [ {"type":"text","widgets":[...]} ]
}
```

- `type`：`text` 或 `step_by_step`。
- `widgets`：用于渲染文本/公式。
- `explanations`：分步骤说明。

### calc
```json
{
  "type": "calc",
  "widgets": [ ... ],
  "explanations": [ ... ],
  "isSampleResponse": false
}
```

### cl（分类/分组题）
```json
{
  "type": "cl",
  "groupName": "string",
  "options": ["string", "string"],
  "explanations": [ ... ]
}
```

### drw（绘图）
```json
{
  "type": "drw",
  "widgets": [ ... ],
  "explanations": [ ... ],
  "isSampleResponse": false
}
```

### es（问答/论述）
```json
{
  "type": "es",
  "widgets": [ ... ],
  "explanations": [ ... ],
  "isSampleResponse": false
}
```

### fib（填空）
```json
{
  "type": "fib",
  "widgets": [ ... ],
  "explanations": [ ... ]
}
```

### gr（作图）
```json
{
  "type": "gr",
  "widgets": [ ... ],
  "explanations": [ ... ],
  "isSampleResponse": false
}
```

### mat（匹配）
```json
{
  "type": "mat",
  "answerIdentifier": "string",
  "explanations": [ ... ]
}
```

### mcq（单选）
```json
{
  "type": "mcq",
  "answerIdentifier": "string",
  "explanations": [ ... ],
  "isCorrect": true
}
```

### ms（多选）
```json
{
  "type": "ms",
  "answerIdentifier": "string",
  "explanations": [ ... ],
  "isCorrect": true
}
```

### ord（排序）
```json
{
  "type": "ord",
  "answerIdentifier": "string",
  "explanations": [ ... ]
}
```

### sa（简答）
```json
{
  "type": "sa",
  "widgets": [ ... ],
  "explanations": [ ... ],
  "isSampleResponse": false,
  "isExplanationRequired": true
}
```

### tcq（判断）
```json
{
  "type": "tcq",
  "answerIdentifier": "string",
  "explanations": [ ... ],
  "isCorrect": true
}
```

### tutor_answer（教师/助教解答）
```json
{
  "type": "tutor_answer",
  "widgets": [ ... ],
  "explanations": [ ... ],
  "attachments": [ ... ]
}
```

## 渲染建议
- `widgets[].text` 直接作为 HTML 片段渲染；包含 `<formula>` 标记，需要前端公式渲染组件解析。
- `widgets[].type=graph` 时，使用 `source` 作为作图脚本（JSXGraph）。
- `explanations` 可能为空或仅包含文字说明，需容错。

## 合并大JSON（带注释）
> 说明：这是 JSONC（带 `//` 注释）的示意结构，用于说明字段含义，非严格 JSON。

```jsonc
{
  "canonicalUrl": "string", // 教材解答页面规范 URL
  "isThinContent": true, // 是否薄内容
  "noindex": true, // 是否建议搜索引擎不收录
  "questionsAndSolutions": [
    {
      "questionId": 12345, // 题目 ID
      "solution": {
        "solutionId": 12345, // 解答 ID
        "sourceType": "tbq", // 来源类型
        "sourceId": "001001", // 来源标识
        "userId": "100000000000000", // 作者/用户 ID
        "version": 2, // 解答版本
        "authoredDate": "2019-11-25 09:39:52 -0600 CST", // 解答时间
        "solutionContent": {
          "type": "calc", // 题型编码
          "answers": [
            {
              "type": "calc", // 题型编码
              "widgets": [
                {
                  "type": "text", // 渲染类型（出现题型：calc/计算题, drw/绘图题, es/论述/问答题, fib/填空题, gr/作图题, sa/简答题, tutor_answer/教师/助教解答）
                  "text": "<p>...</p>", // HTML 片段（出现题型：calc/计算题, drw/绘图题, es/论述/问答题, fib/填空题, gr/作图题, sa/简答题, tutor_answer/教师/助教解答）
                  "source": "..." // 图形脚本（出现题型：calc/计算题, gr/作图题, sa/简答题）
                }
              ],
              "explanations": [
                {
                  "type": "text", // 解释类型
                  "widgets": [
                    {
                      "type": "text", // 渲染类型
                      "text": "<p>...</p>",
                      "source": "..."
                    }
                  ]
                },
                {
                  "type": "step_by_step", // 分步解释
                  "explanations": [
                    {
                      "type": "text",
                      "widgets": [
                        {"type": "text", "text": "<p>...</p>"}
                      ]
                    }
                  ]
                }
              ],
              "isSampleResponse": false, // 是否示例回答（出现题型：calc/计算题, drw/绘图题, es/论述/问答题, gr/作图题, sa/简答题）
              "isExplanationRequired": true, // 是否要求解释（出现题型：sa/简答题）
              "answerIdentifier": "A", // 选项/匹配/排序标识（出现题型：mat/匹配题, mcq/单选题, ms/多选题, ord/排序题, tcq/判断题）
              "isCorrect": true, // 是否正确（出现题型：mcq/单选题, ms/多选题, tcq/判断题）
              "groupName": "Group 1", // 分组名（出现题型：cl/分类/分组题）
              "options": ["opt1", "opt2"], // 选项数组（出现题型：cl/分类/分组题）
              "attachments": [ /* ... */ ] // 附件（出现题型：tutor_answer/教师/助教解答）
            }
          ],
          "hints": [], // 提示数组（出现题型：calc/计算题, cl/分类/分组题, drw/绘图题, es/论述/问答题, fib/填空题, gr/作图题, mat/匹配题, mcq/单选题, ms/多选题, ord/排序题, sa/简答题, tcq/判断题）
          "hasSameExplanationForAllAnswers": false, // 是否共用同一解释（出现题型：calc/计算题, cl/分类/分组题, drw/绘图题, es/论述/问答题, fib/填空题, gr/作图题, mat/匹配题, mcq/单选题, ms/多选题, ord/排序题, sa/简答题, tcq/判断题）
          "externalLink": "https://...", // 外部链接（出现题型：calc/计算题, cl/分类/分组题, drw/绘图题, es/论述/问答题, fib/填空题, gr/作图题, mat/匹配题, mcq/单选题, ms/多选题, sa/简答题, tcq/判断题）
          "format": "string", // 格式标记（出现题型：tutor_answer/教师/助教解答）
          "state": "string", // 状态字段（出现题型：tutor_answer/教师/助教解答）
          "tutor": { /* ... */ }, // 导师信息（出现题型：tutor_answer/教师/助教解答）
          "locked": false, // 是否锁定（出现题型：calc/计算题, cl/分类/分组题, drw/绘图题, es/论述/问答题, fib/填空题, gr/作图题, mat/匹配题, mcq/单选题, ms/多选题, sa/简答题, tcq/判断题, tutor_answer/教师/助教解答）
          "isScorable": true, // 是否可评分（出现题型：calc/计算题, cl/分类/分组题, drw/绘图题, es/论述/问答题, fib/填空题, gr/作图题, mat/匹配题, mcq/单选题, ms/多选题, sa/简答题, tcq/判断题, tutor_answer/教师/助教解答）
          "takedownUrl": "https://..." // 下架链接（出现题型：tutor_answer/教师/助教解答）
        }
      }
    }
  ]
}
```

## 字段出现题型
以下为“字段 -> 出现题型”的统计（英文缩写 + 中文）。

**solutionContent 字段**
- `answers`: calc(计算题), cl(分类/分组题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), mat(匹配题), mcq(单选题), ms(多选题), ord(排序题), sa(简答题), tcq(判断题), tutor_answer(教师/助教解答)
- `externalLink`: calc(计算题), cl(分类/分组题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), mat(匹配题), mcq(单选题), ms(多选题), sa(简答题), tcq(判断题)
- `format`: tutor_answer(教师/助教解答)
- `hasSameExplanationForAllAnswers`: calc(计算题), cl(分类/分组题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), mat(匹配题), mcq(单选题), ms(多选题), ord(排序题), sa(简答题), tcq(判断题)
- `hints`: calc(计算题), cl(分类/分组题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), mat(匹配题), mcq(单选题), ms(多选题), ord(排序题), sa(简答题), tcq(判断题)
- `isScorable`: calc(计算题), cl(分类/分组题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), mat(匹配题), mcq(单选题), ms(多选题), sa(简答题), tcq(判断题), tutor_answer(教师/助教解答)
- `locked`: calc(计算题), cl(分类/分组题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), mat(匹配题), mcq(单选题), ms(多选题), sa(简答题), tcq(判断题), tutor_answer(教师/助教解答)
- `state`: tutor_answer(教师/助教解答)
- `takedownUrl`: tutor_answer(教师/助教解答)
- `tutor`: tutor_answer(教师/助教解答)
- `type`: calc(计算题), cl(分类/分组题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), mat(匹配题), mcq(单选题), ms(多选题), ord(排序题), sa(简答题), tcq(判断题), tutor_answer(教师/助教解答)

**answers 字段**
- `answerIdentifier`: mat(匹配题), mcq(单选题), ms(多选题), ord(排序题), tcq(判断题)
- `attachments`: tutor_answer(教师/助教解答)
- `explanations`: calc(计算题), cl(分类/分组题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), mat(匹配题), mcq(单选题), ms(多选题), ord(排序题), sa(简答题), tcq(判断题), tutor_answer(教师/助教解答)
- `groupName`: cl(分类/分组题)
- `isCorrect`: mcq(单选题), ms(多选题), tcq(判断题)
- `isExplanationRequired`: sa(简答题)
- `isSampleResponse`: calc(计算题), drw(绘图题), es(论述/问答题), gr(作图题), sa(简答题)
- `options`: cl(分类/分组题)
- `type`: calc(计算题), cl(分类/分组题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), mat(匹配题), mcq(单选题), ms(多选题), ord(排序题), sa(简答题), tcq(判断题), tutor_answer(教师/助教解答)
- `widgets`: calc(计算题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), sa(简答题), tutor_answer(教师/助教解答)

**widgets 字段（answers.widgets[]）**
- `source`: calc(计算题), gr(作图题), sa(简答题)
- `text`: calc(计算题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), sa(简答题), tutor_answer(教师/助教解答)
- `type`: calc(计算题), drw(绘图题), es(论述/问答题), fib(填空题), gr(作图题), sa(简答题), tutor_answer(教师/助教解答)
