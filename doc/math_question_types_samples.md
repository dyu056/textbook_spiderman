# Math 题型样例（每题型一条完整数据）

基于 spider_data/Math/*.har 抽样；每个题型提供一条完整 questionsAndSolutions 片段（含 solution），并包含 canonicalUrl/isThinContent/noindex。

## fib
- 中文题型: 填空题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/7693/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/College-Algebra-10th-Edition-9780321999412-6/Chapter-R-Problem-1-7693/",
  "isThinContent": false,
  "noindex": true,
  "questionsAndSolutions": [
    {
      "questionId": 2302,
      "solution": {
        "solutionId": 7190,
        "sourceType": "tbq",
        "sourceId": "001001",
        "userId": "100000763022653",
        "solutionContent": {
          "type": "fib",
          "hints": [],
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "fib",
              "widgets": [
                {
                  "type": "text",
                  "text": "<p>Rational Numbers <formula data-display=\"inline\">\\mathbb{Q}</formula></p>"
                }
              ],
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>Rational Numbers <formula data-display=\"inline\">\\mathbb{Q}</formula> are numbers that can be written as a fraction of two integers.</p>"
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 8,
        "authoredDate": "2020-01-22 13:12:16 -0600 CST"
      }
    }
  ]
}
```

## mcq
- 中文题型: 单选题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/7697/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/College-Algebra-10th-Edition-9780321999412-6/Chapter-R-Problem-5-7697/",
  "isThinContent": true,
  "noindex": false,
  "questionsAndSolutions": [
    {
      "questionId": 2328,
      "solution": {
        "solutionId": 7222,
        "sourceType": "tbq",
        "sourceId": "001005",
        "userId": "100000786194527",
        "solutionContent": {
          "type": "mcq",
          "hints": [],
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "mcq",
              "answerIdentifier": "a",
              "isCorrect": true,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>The intersection of two sets is denoted as <formula data-display=\"inline\">A \\cap B</formula>.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "mcq",
              "answerIdentifier": "b",
              "isCorrect": false,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p><formula data-display=\"inline\">A \\cup B</formula> denotes the union of two sets, also defined as \"A and/or B\".</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "mcq",
              "answerIdentifier": "c",
              "isCorrect": false,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p><formula data-display=\"inline\">A \\subseteq B</formula> states that <formula data-display=\"inline\">A</formula> is a subset of <formula data-display=\"inline\">B</formula>. This means every element of <formula data-display=\"inline\">A</formula> is included in <formula data-display=\"inline\">B</formula>. For example: Integers <formula data-display=\"inline\">\\mathbb{Z}</formula> are a subset of the real numbers <formula data-display=\"inline\">\\mathbb{R}</formula>.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "mcq",
              "answerIdentifier": "d",
              "isCorrect": false,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p><formula data-display=\"inline\">\\varnothing</formula> is not used to define a relationship between two sets, but rather expresses a characteristic of a set without any elements.</p>"
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 1,
        "authoredDate": "2019-08-28 13:28:17 -0500 CDT"
      }
    }
  ]
}
```

## tcq
- 中文题型: 判断题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/7699/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/College-Algebra-10th-Edition-9780321999412-6/Chapter-R-Problem-7-7699/",
  "isThinContent": true,
  "noindex": false,
  "questionsAndSolutions": [
    {
      "questionId": 2577,
      "solution": {
        "solutionId": 7492,
        "sourceType": "tbq",
        "sourceId": "001007",
        "userId": "100000786194527",
        "solutionContent": {
          "type": "tcq",
          "hints": [],
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "tcq",
              "answerIdentifier": "True",
              "isCorrect": true,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>Rational numbers are defined as numbers that can be written as <formula data-display=\"inline\">\\frac{p}{q}</formula> where <formula data-display=\"inline\">p, q \\in \\mathbb{Z}</formula>, which means that <formula data-display=\"inline\">p</formula> and <formula data-display=\"inline\">q</formula> are integers and <formula data-display=\"inline\">q \\neq 0</formula>. Therefore, nonterminating decimals with non-repeating digits would not be included, which includes <formula data-display=\"inline\">\\sqrt{2}</formula> and <formula data-display=\"inline\">\\pi</formula>.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "tcq",
              "answerIdentifier": "False",
              "isCorrect": false,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>Rational numbers are defined as numbers that can be written as <formula data-display=\"inline\">\\frac{p}{q}</formula> where <formula data-display=\"inline\">p, q \\in \\mathbb{Z}</formula>, which means that <formula data-display=\"inline\">p</formula> and <formula data-display=\"inline\">q</formula> are integers and <formula data-display=\"inline\">q \\neq 0</formula>. Therefore, nonterminating decimals with non-repeating digits would not be included, which includes <formula data-display=\"inline\">\\sqrt{2}</formula> and <formula data-display=\"inline\">\\pi</formula>.</p>"
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 1,
        "authoredDate": "2019-08-28 16:03:26 -0500 CDT"
      }
    }
  ]
}
```

## calc
- 中文题型: 计算题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/7703/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/College-Algebra-10th-Edition-9780321999412-6/Chapter-R-Problem-11-7703/",
  "isThinContent": true,
  "noindex": false,
  "questionsAndSolutions": [
    {
      "questionId": 2585,
      "solution": {
        "solutionId": 7500,
        "sourceType": "tbq",
        "sourceId": "00100B",
        "userId": "100000786194527",
        "solutionContent": {
          "type": "calc",
          "hints": [],
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "calc",
              "widgets": [
                {
                  "type": "text",
                  "text": "<p><formula data-display=\"inline\">A \\cup B = \\{1,2,3,4,5,6,7,8,9\\}</formula></p>"
                }
              ],
              "explanations": [
                {
                  "type": "step_by_step",
                  "explanations": [
                    {
                      "type": "text",
                      "widgets": [
                        {
                          "type": "text",
                          "text": "<p>Take all elements from set <formula data-display=\"inline\">A</formula> and set <formula data-display=\"inline\">B</formula>.</p>"
                        }
                      ]
                    },
                    {
                      "type": "text",
                      "widgets": [
                        {
                          "type": "text",
                          "text": "<p><formula data-display=\"inline\">A + B = \\{1,3,4,5,9\\} + \\{2,4,6,7,8\\} \\\\ \\{1,2,3,4,4,5,6,7,8,9\\}</formula></p>"
                        }
                      ]
                    }
                  ]
                },
                {
                  "type": "step_by_step",
                  "explanations": [
                    {
                      "type": "text",
                      "widgets": [
                        {
                          "type": "text",
                          "text": "<p><formula data-display=\"inline\">A \\cup B</formula> is defined as <formula data-display=\"inline\">A</formula> + <formula data-display=\"inline\">B - \\lparen A \\cap B\\rparen</formula>. We need to make sure to eliminate the duplicate elements defined in the intersection <formula data-display=\"inline\">A \\cap B</formula>.</p>"
                        }
                      ]
                    },
                    {
                      "type": "text",
                      "widgets": [
                        {
                          "type": "text",
                          "text": "<p><formula data-display=\"inline\">\\{1,2,3,4,4,5,6,7,8,9\\} - \\{4\\} \\\\ \\{1,2,3,4,5,6,7,8,9\\}</formula></p>"
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 1,
        "authoredDate": "2019-08-28 16:08:29 -0500 CDT"
      }
    }
  ]
}
```

## sa
- 中文题型: 简答题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/7715/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/College-Algebra-10th-Edition-9780321999412-6/Chapter-R-Problem-23-7715/",
  "isThinContent": false,
  "noindex": true,
  "questionsAndSolutions": [
    {
      "questionId": 2625,
      "solution": {
        "solutionId": 7540,
        "sourceType": "tbq",
        "sourceId": "00100N",
        "userId": "100000786194527",
        "solutionContent": {
          "type": "sa",
          "hints": [],
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "sa",
              "widgets": [
                {
                  "type": "text",
                  "text": "<p><formula data-display=\"inline\">2,5</formula></p>"
                }
              ],
              "isSampleResponse": false,
              "isExplanationRequired": true,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>The natural numbers <formula data-display=\"inline\">\\mathbb{N}</formula> are defined as the positive whole numbers.</p>"
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 1,
        "authoredDate": "2019-08-28 16:25:50 -0500 CDT"
      }
    }
  ]
}
```

## gr
- 中文题型: 作图题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/7820/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/College-Algebra-10th-Edition-9780321999412-6/Chapter-R-Problem-13-7820/",
  "isThinContent": true,
  "noindex": true,
  "questionsAndSolutions": [
    {
      "questionId": 5743,
      "solution": {
        "solutionId": 8681,
        "sourceType": "tbq",
        "sourceId": "001048",
        "userId": "100000793732068",
        "solutionContent": {
          "type": "gr",
          "hints": [
            "<p>Use the fractions decimal equivalent to determine where they lie on the real number line.</p>"
          ],
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "gr",
              "widgets": [
                {
                  "type": "graph",
                  "text": "<img src=\"/solutions/attachments/98/\">",
                  "source": "var board = JXG.JSXGraph.initBoard('jxgboxa', {\nshowCopyright: false,\nshowNavigation: false,\nregisterEvents: false\n});\nvar axisx = board.create('axis', [[0,0], [1,0]],\n{\nfirstArrow: true,\nlastArrow: true,\nticks: {\ndrawZero: true,\nticksDistance: 1,\nmajorHeight: 30,\ntickEndings: [1,1],\nminorTicks: 0\n}\n});\nboard.setBoundingBox([-5, 0.5, 5, -0.1]);\nboard.create('point', [-2.5, 0], {size:4, name:'-2.5', label: {offset:[-10,20]}});\nboard.create('point', [-1, 0], {size:4, withLabel:false});\nboard.create('point', [0, 0], {size:4, withLabel:false});\nboard.create('point', [.25, 0], {size:4, name:'0.25', label: {offset:[-10,20]}});\nboard.create('point', [.75, 0], {size:4, name:'3/4', label: {offset:[-10,20]}});\nboard.create('point', [1, 0], {size:4, withLabel:false});\nboard.create('point', [2.5, 0], {size:4, name:'5/2', label: {offset:[-10,20]}});"
                }
              ],
              "isSampleResponse": false,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>Here are the points <formula data-display=\"inline\">0, 1, -1, \\frac{5}{2} ,-2.5, \\frac{3}{4}</formula>, and <formula data-display=\"inline\">0.25</formula> on the real number line.</p>"
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 2,
        "authoredDate": "2019-11-04 14:45:02 -0600 CST"
      }
    }
  ]
}
```

## ms
- 中文题型: 多选题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/12884/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/College-Algebra-10th-Edition-9780321999412-6/Chapter-2-Problem-131-12884/",
  "isThinContent": true,
  "noindex": true,
  "questionsAndSolutions": [
    {
      "questionId": 18901,
      "solution": {
        "solutionId": 21504,
        "sourceType": "tbq",
        "sourceId": "0011LI",
        "userId": "100000793732053",
        "solutionContent": {
          "type": "ms",
          "hints": [
            "<p>Y-intercepts above the x-axis will be positive.</p>"
          ],
          "externalLink": "https://youtu.be/6_9xNMtwnfs",
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "ms",
              "answerIdentifier": "a",
              "isCorrect": false,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p> This equation has a negative slope <formula data-display=\"inline\">m = -\\frac{2}{3}</formula>.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "ms",
              "answerIdentifier": "b",
              "isCorrect": true,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>This equation has a positive slope <formula data-display=\"inline\">m = \\frac{2}{3}</formula> and positive y-intercept <formula data-display=\"inline\">b = 2</formula>.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "ms",
              "answerIdentifier": "c",
              "isCorrect": true,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>This equation has a positive slope <formula data-display=\"inline\">m = \\frac{3}{4}</formula> and positive y-intercept <formula data-display=\"inline\">b = 3</formula>.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "ms",
              "answerIdentifier": "d",
              "isCorrect": false,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>This equation has a negative y-intercept <formula data-display=\"inline\">b = -1</formula>.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "ms",
              "answerIdentifier": "e",
              "isCorrect": true,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>This equation has a positive slope <formula data-display=\"inline\">m = 1</formula> and positive y-intercept <formula data-display=\"inline\">b = 1</formula>.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "ms",
              "answerIdentifier": "f",
              "isCorrect": false,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p> This equation has a negative y-intercept <formula data-display=\"inline\">b = -5</formula>.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "ms",
              "answerIdentifier": "g",
              "isCorrect": true,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>This equation has a positive slope <formula data-display=\"inline\">m = 2</formula> and positive y-intercept <formula data-display=\"inline\">b = 3</formula>.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "ms",
              "answerIdentifier": "h",
              "isCorrect": false,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p> This equation has a negative slope <formula data-display=\"inline\">m = -3</formula>.</p>"
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 2,
        "authoredDate": "2019-11-13 17:13:52 -0600 CST"
      }
    }
  ]
}
```

## mat
- 中文题型: 匹配题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/12947/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/College-Algebra-10th-Edition-9780321999412-6/Chapter-2-Problem-45-48-12947/",
  "isThinContent": false,
  "noindex": true,
  "questionsAndSolutions": [
    {
      "questionId": 28853,
      "solution": {
        "solutionId": 31774,
        "sourceType": "tbq",
        "sourceId": "0011O1",
        "userId": "100000793732053",
        "solutionContent": {
          "type": "mat",
          "hints": [
            "<p>Use the center of the circle to determine what the equation in standard form would resemble.</p>"
          ],
          "externalLink": "https://youtu.be/JvDpYlyKkNU",
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "mat",
              "answerIdentifier": "c",
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>Use the standard form for the equation of a circle to determine a center to match the image.</p><p> </p><p><formula data-display=\"inline\">\\begin{aligned}\\text{Radius} &amp;= 2 \\\\ \\text{Center} &amp;= (1,-2) \\\\ (x-h)^2 + (y-k)^2 &amp;=r^2 \\\\ (x-1)^2 + (y+2)^2 &amp;= 4 \\\\ &amp;(c) ~\\checkmark \\end{aligned}</formula></p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "mat",
              "answerIdentifier": "d",
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p> Use the standard form for the equation of a circle to determine a center to match the image.</p><p> </p><p><formula data-display=\"inline\">\\begin{aligned}\\text{Radius} &amp;= 3 \\\\ \\text{Center} &amp;= (-3,3) \\\\ (x-h)^2 + (y-k)^2 &amp;=r^2\\\\ (x+3)^2 + (y-3)^2 &amp;= 9 \\\\ &amp;(d) ~\\checkmark \\end{aligned}</formula></p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "mat",
              "answerIdentifier": "b",
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>Use the standard form for the equation of a circle to determine a center to match the image.</p><p> </p><p> <formula data-display=\"inline\">\\begin{aligned}\\text{Radius} &amp;= 2 \\\\ \\text{Center} &amp;= (-1,2) \\\\ (x-h)^2 + (y-k)^2 &amp;=r^2\\\\ (x+1)^2 + (y-2)^2 &amp;= 4 \\\\ &amp;(b) ~\\checkmark \\end{aligned}</formula></p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "mat",
              "answerIdentifier": "a",
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>  Use the standard form for the equation of a circle to determine a center to match the image.</p><p> </p><p> <formula data-display=\"inline\">\\begin{aligned}\\text{Radius} &amp;= 3 \\\\ \\text{Center} &amp;= (3,-3) \\\\ (x-h)^2 + (y-k)^2 &amp;=r^2\\\\ (x-3)^2 + (y+3)^2 &amp;= 9 \\\\ &amp;(a) ~\\checkmark \\end{aligned}</formula></p>"
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 3,
        "authoredDate": "2019-11-14 16:57:49 -0600 CST"
      }
    }
  ]
}
```

## drw
- 中文题型: 绘图题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/13853/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/College-Algebra-10th-Edition-9780321999412-6/Chapter-4-Problem-25-13853/",
  "isThinContent": true,
  "noindex": true,
  "questionsAndSolutions": [
    {
      "questionId": 18405,
      "solution": {
        "solutionId": 21007,
        "sourceType": "tbq",
        "sourceId": "00132M",
        "userId": "100000790801547",
        "solutionContent": {
          "type": "drw",
          "hints": [],
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "drw",
              "widgets": [
                {
                  "type": "text",
                  "text": "<img src=\"/solutions/attachments/4115/\">"
                }
              ],
              "isSampleResponse": false,
              "explanations": [
                {
                  "type": "step_by_step",
                  "explanations": [
                    {
                      "type": "text",
                      "widgets": [
                        {
                          "type": "text",
                          "text": "<p>Set the graphing utility into Statistics mode. Place all x-values under the first list and the y-values under the second list.</p>"
                        }
                      ]
                    }
                  ]
                },
                {
                  "type": "step_by_step",
                  "explanations": [
                    {
                      "type": "text",
                      "widgets": [
                        {
                          "type": "text",
                          "text": "<p>Draw a scatter plot using the built in statistics plot. Adjust the viewing window by setting Xmin=0, Xmax=100, Ymin=0, and Ymax=60,000.</p>"
                        }
                      ]
                    }
                  ]
                },
                {
                  "type": "step_by_step",
                  "explanations": [
                    {
                      "type": "text",
                      "widgets": [
                        {
                          "type": "text",
                          "text": "<p>Execute the built in quadratic regression function to find the quadratic function of best fit <formula data-display=\"inline\">y=ax^2+bx+c</formula>. Store the regression equation into one of the y equations of the graphing utility.</p>"
                        }
                      ]
                    }
                  ]
                },
                {
                  "type": "step_by_step",
                  "explanations": [
                    {
                      "type": "text",
                      "widgets": [
                        {
                          "type": "text",
                          "text": "<p>Hit GRAPH key to display the scatter plot and the quadratic of best fit.</p>"
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 2,
        "authoredDate": "2019-11-14 19:22:57 -0600 CST"
      }
    }
  ]
}
```

## es
- 中文题型: 论述/问答题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/33619/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/College-Algebra-10th-Edition-9780321999412-6/Chapter-5-Problem-65-33619/",
  "isThinContent": false,
  "noindex": true,
  "questionsAndSolutions": [
    {
      "questionId": 24519,
      "solution": {
        "solutionId": 27119,
        "sourceType": "tbq",
        "sourceId": "0013KX",
        "userId": "100000793738159",
        "solutionContent": {
          "type": "es",
          "hints": [],
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "es",
              "widgets": [
                {
                  "type": "text",
                  "text": "<p>In graphing a rational function, start with finding the domain of the function. Factor the numerator and the denominator, if possible, and reduce it to lowest terms for ease in identifying all the necessary data to graph the function. Zeros of the denominator which are canceled out give rise to a hole in the graph if it yields a different result upon evaluating the function in lowest terms. To determine the points of the graph,  set <formula data-display=\"inline\">x=0</formula> to find the <formula data-display=\"inline\">y</formula>-intercept by and set the numerator equal to zero to find the <formula data-display=\"inline\">x</formula>-intercepts. Plot the points and use the concept of multiplicity to find the behavior of the graph at each <formula data-display=\"inline\">x</formula>-intercept. To find the vertical asymptotes, set the denominator of the function equal to zero. For the horizontal asymptote, compare the degree of the numerator and the denominator and identify the asymptote accordingly: for proper rational functions, the horizontal asymptote is given by <formula data-display=\"inline\">y=0</formula>; for improper rational functions with equal degrees, divide the leading coefficient of the numerator by the leading coefficient of the denominator; for improper rational functions with numerator having 1 degree greater than the denominator, divide the numerator of the function by its denominator; for improper rational functions with numerator having 2 or more degrees greater than the denominator, there is no horizontal or oblique asymptote. Create a table of intervals using the zeros of the numerator and the denominator and determine whether the graph is below or above the <formula data-display=\"inline\">x</formula>-axis.</p>"
                }
              ],
              "isSampleResponse": true,
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>Identifying the domain of the function is so important in analyzing the graph of a rational function since the domain determines whether what zeros of the function will make the function undefined and thus can either give rise to a hole or a vertical asymptote in the graph. The graph of a rational function can have a hole if the zero of the denominator can give a different result upon evaluating the function in lowest terms. The multiplicity of the <formula data-display=\"inline\">x</formula>-intercepts can be used to determine whether the graph touches or crosses the <formula data-display=\"inline\">x</formula>-axis. The vertical asymptote of the rational function serves as a barrier that the graph will never touch the asymptote.</p>"
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 3,
        "authoredDate": "2019-11-08 09:14:16 -0600 CST"
      }
    }
  ]
}
```

## tutor_answer
- 中文题型: 教师/助教解答
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/298740/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/Calculus-8th-Edition-9781285740621-40/Chapter-2-Problem-3-20434/",
  "isThinContent": false,
  "noindex": true,
  "questionsAndSolutions": [
    {
      "questionId": 404285,
      "solution": {
        "sourceType": "tbq",
        "solutionContent": {
          "type": "tutor_answer",
          "state": "answered",
          "tutor": {
            "displayName": "dcdennice",
            "profileUrl": "/profile/dcdennice/",
            "profilePictureUrl": "/api/v1/users/photo/100000791884520/"
          },
          "takedownUrl": "/tutors-problems/Calculus/34683097-a-Find-the-slope-of-the-tangent-line-to-the-parabola-y-4-x-/",
          "format": "ckeditor",
          "answers": [
            {
              "type": "tutor_answer",
              "widgets": [
                {
                  "type": "text",
                  "text": "<p style=\"margin-left:0px;\"><strong>From the information in the question above, we can analyze the scenario and solve the problem given as done below.</strong></p><p><br /> </p>"
                }
              ],
              "attachments": [
                {
                  "question_attachment_id": 23414356,
                  "qa_thread_id": 91259287,
                  "users_filename": "image.png",
                  "filehash": "172bd98782d69d9068a0886d2daeea83b5f4beb1",
                  "type": "png",
                  "on_s3": 1,
                  "inline": true
                }
              ],
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p><strong>SOLUTION</strong></p><p>From the information in the question above, we can analyze the scenario and solve the problem given as follows.</p><p>To begin with;</p><p> </p><figure class=\"image\"><img src=\"/qa/attachment/23414356/\" alt=\"23414356\" /></figure><p> </p><p> </p><p> </p><p> </p><p> </p><p> </p><p><strong>*Please like. Thanks.</strong></p>"
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    }
  ]
}
```

## cl
- 中文题型: 分类/分组题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/309890/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/Essential-Calculus-Early-Transcendentals-2nd-Edition-9781133112280-47/Chapter-10-Problem-19-309890/",
  "isThinContent": false,
  "noindex": true,
  "questionsAndSolutions": [
    {
      "questionId": 418849,
      "solution": {
        "solutionId": 183457,
        "sourceType": "tbq",
        "sourceId": "01848N",
        "userId": "100000799650108",
        "solutionContent": {
          "type": "cl",
          "hints": [
            "<p><strong>The dot product of two vectors <formula data-display=\"inline\">a=&lt;a_1,a_2,a_3&gt;</formula> and <formula data-display=\"inline\">b=&lt;b_1,b_2,b_3&gt;</formula> is <formula data-display=\"inline\">a\\cdot b=a_1 b_1+a_2 b_2+a_3 b_3</formula>.</strong></p>"
          ],
          "externalLink": "https://www.youtube.com/watch?v=kK_pGcJZavQ",
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "cl",
              "groupName": "Orthogonal, Parallel, Neither",
              "options": [
                "Neither"
              ],
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p><strong>Two vectors are orthogonal if the dot product of the vectors is equal to zero. The dot product <formula data-display=\"inline\">a\\cdot b</formula> is   </strong></p><p><strong><formula data-display=\"inline\">\\begin{aligned} a\\cdot b&amp;=&lt;-5,\\ 3,\\ 7&gt;\\cdot&lt;6,\\ -8,\\ 2&gt;\\\\&amp;=-5(6)+3(-8)+7(2)\\\\&amp;=-40\\end{aligned}</formula></strong></p><p> </p><p><strong>Two vectors <formula data-display=\"inline\">a</formula> and <formula data-display=\"inline\">b</formula> are parallel if the angle <formula data-display=\"inline\">\\theta</formula> between them is <formula data-display=\"inline\">\\pi</formula> or <formula data-display=\"inline\">0</formula>. If <formula data-display=\"inline\">\\theta</formula> is the angle between two nonzero vectors <formula data-display=\"inline\">a</formula> and <formula data-display=\"inline\">b</formula> then  <formula data-display=\"inline\">\\cos\\theta=\\frac{a \\cdot b}{\\left | a \\right |\\left | b \\right |}</formula>.</strong></p><p> </p><p><strong><formula data-display=\"inline\">\\begin{aligned} \\cos\\theta&amp;=\\frac{-40}{\\sqrt{(-5)^2+3^2+7^2}\\cdot{\\sqrt{6^2+(-8)^2+2^2}}}\\\\\\cos\\theta&amp;=\\frac{-40}{\\sqrt{83}\\cdot\\sqrt{104}}\\\\\\cos\\theta&amp;=-0.43\\\\ \\theta&amp;=\\cos^{-1}\\left ( 0.43 \\right )\\\\&amp;=115.47^{\\circ}\\end{aligned}</formula></strong></p><p><strong> </strong></p><p><strong>The angle between <formula data-display=\"inline\">a</formula> and <formula data-display=\"inline\">b</formula> is neither <formula data-display=\"inline\">0</formula> nor <formula data-display=\"inline\">\\pi</formula>. </strong></p><p> </p><p><strong>Therefore, the vectors <formula data-display=\"inline\">a</formula> and <formula data-display=\"inline\">b</formula> are neither orthogonal nor parallel.</strong></p>"
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 4,
        "authoredDate": "2020-05-01 10:37:40 -0500 CDT"
      }
    }
  ]
}
```

## ord
- 中文题型: 排序题
- source_url: https://www.coursehero.com/api/v1/textbooks/exercises/270038/content/
```json
{
  "canonicalUrl": "https://www.coursehero.com/textbook-solutions/Prealgebra-2nd-Edition-9780073384474-9/Chapter-2-Problem-95-270038/",
  "isThinContent": false,
  "noindex": true,
  "questionsAndSolutions": [
    {
      "questionId": 368335,
      "solution": {
        "solutionId": 629782,
        "sourceType": "tbq",
        "sourceId": "03L0UX",
        "userId": "100000797467134",
        "solutionContent": {
          "type": "ord",
          "hints": [
            "<p>Use the definitions of absolute value and opposites.</p>"
          ],
          "hasSameExplanationForAllAnswers": false,
          "answers": [
            {
              "type": "ord",
              "answerIdentifier": "-60",
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>Since negative numbers lie to the left of 0 on the number line, the integer <formula data-display=\"inline\">-60</formula> lies at the leftmost position on the number line among the given five integers.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "ord",
              "answerIdentifier": "-|-46|",
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<ul><li>The absolute value <formula data-display=\"inline\">|a|</formula> is the distance between <formula data-display=\"inline\">a</formula> and 0. The absolute value of a negative as well as a positive integer is always positive. </li><li>The value <formula data-display=\"inline\">-|-46|</formula> represents the opposite of <formula data-display=\"inline\">|-46|</formula>. Since <formula data-display=\"inline\">|-46|=46</formula> and the opposite of 46 is <formula data-display=\"inline\">-46</formula>, <formula data-display=\"inline\">-|-46|</formula> lies 46 units to the left of 0 on the number line, which is the second most left position on the number line among the given five integers.</li></ul>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "ord",
              "answerIdentifier": "|-12|",
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>The absolute value <formula data-display=\"inline\">|a|</formula> is the distance between <formula data-display=\"inline\">a</formula> and 0. The absolute value of a negative as well as a positive integer is always positive. So, <formula data-display=\"inline\">|-12|</formula> lies 12 units to the right of 0 on the number line.</p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "ord",
              "answerIdentifier": "-(-24)",
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p>The opposite of a negative integer is always a positive integer. So, <formula data-display=\"inline\">-(-24)=24</formula>.</p><p> <formula data-display=\"inline\">-(-24)</formula> lies 24 units to the right of 0 on the number line. </p>"
                    }
                  ]
                }
              ]
            },
            {
              "type": "ord",
              "answerIdentifier": "5²",
              "explanations": [
                {
                  "type": "text",
                  "widgets": [
                    {
                      "type": "text",
                      "text": "<p><formula data-display=\"block\">\\begin{aligned}5^2&amp;=5\\cdot5\\\\&amp;=25\\end{aligned}</formula></p><p>The integer 25 lies 25 units to the right of 0 since positive numbers lie on the right side of the number line.</p>"
                    }
                  ]
                }
              ]
            }
          ]
        },
        "version": 10,
        "authoredDate": "2020-12-01 23:52:50 -0600 CST"
      }
    }
  ]
}
```
