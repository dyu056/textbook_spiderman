# 数学解答页面数据结构（左侧目录 + 右侧解答）

目标：左侧书本与章节目录保持稳定；切换题目时只刷新右侧解答区域。
所有字段名均为**新命名**（不与原始数据字段名完全一致）。

## 顶层结构
```json
{
  "volume": { ... },
  "catalog": { ... },
  "selection": { ... },
  "content": { ... }
}
```

- `volume`：左侧顶部的书本信息。
- `catalog`：左侧章节/小节/习题树。
- `selection`：当前选中的题目 + 前后题导航。
- `content`：右侧解答内容。

---

## volume（左侧书本信息）
```json
{
  "bookKey": "math-college-algebra-10e",
  "name": "College Algebra",
  "editionLabel": "10th Edition",
  "authors": ["Sullivan"],
  "isbn13": "9780321999412",
  "coverImage": {
    "kind": "image",
    "path": "/covers/college-algebra-10e.jpg"
  },
  "buyLink": "https://..."
}
```

---

## catalog（左侧目录树）
```json
{
  "chapters": [
    {
      "nodeId": "ch-5",
      "title": "Chapter 5",
      "sections": [
        {
          "nodeId": "sec-5-1",
          "title": "Section 5.1: Polynomial Functions and Models",
          "groups": [
            {
              "label": "ASSESS YOUR UNDERSTANDING",
              "items": [
                {"itemId": "ex-5-1-1", "label": "Exercise 1"},
                {"itemId": "ex-5-1-2", "label": "Exercise 2"}
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

- `nodeId` / `itemId`：用于前端选中与定位的稳定 ID。
- `groups`：可选，用于“Assess Your Understanding”等分组显示。

---

## selection（当前题目 + 导航）
```json
{
  "activeItemId": "ex-5-3-65",
  "activePath": {
    "chapterId": "ch-5",
    "sectionId": "sec-5-3",
    "itemId": "ex-5-3-65"
  },
  "labels": {
    "chapter": "Chapter 5",
    "section": "Section 5.3",
    "exercise": "Exercise 65",
    "pageHint": "Page 367"
  },
  "neighbors": {
    "prevId": "ex-5-3-64",
    "nextId": "ex-5-3-66"
  },
  "pageUrl": "https://.../Chapter-5-Section-5.3-Exercise-65"
}
```

---

## content（右侧解答内容）
```json
{
  "itemId": "ex-5-3-65",
  "answer": {
    "kind": "sa",
    "parts": [
      {
        "partId": "p1",
        "result": [
          {"fragType": "html", "html": "<p>...</p>"}
        ],
        "steps": [
          {
            "title": "Explanation",
            "flow": [
              {"fragType": "html", "html": "<p>...</p>"}
            ]
          }
        ]
      }
    ],
    "assets": [
      {
        "assetId": "a1",
        "assetType": "image",
        "path": "/solutions/attachments/98/",
        "filename": "image.png"
      },
      {
        "assetId": "a2",
        "assetType": "graph",
        "script": "var board = ..."
      }
    ],
    "links": [
      {"label": "Video", "url": "https://..."}
    ]
  },
  "meta": {
    "sourceKey": "tbq",
    "sourceRef": "001001",
    "ownerId": "100000000000000",
    "rev": 2,
    "authoredAt": "2019-11-25 09:39:52 -0600 CST"
  },
  "quality": {
    "thin": true,
    "noIndex": true
  }
}
```

---

## 字段含义（关键说明）
- `answer.kind`：题型编码（对应原始类型）。
- `parts[]`：同一题可以拆成多个子解答，按顺序渲染。
- `result`：最终答案区域，`fragType` 可为 `html` 或 `graph` 引用。
- `steps`：解释/步骤内容，每块可带标题与富文本/图形片段。
- `assets`：媒体资源/图形脚本（不含二进制）。
- `quality.thin` / `quality.noIndex`：质量/SEO 标记。

---

## 为什么适配你的页面
- 左侧只依赖 `volume` + `catalog`，切题时不变。
- 右侧只刷新 `selection` + `content`。
- 目录和解答分离，便于缓存与增量加载。
- 字段名全部新命名，避免与原始字段冲突。
