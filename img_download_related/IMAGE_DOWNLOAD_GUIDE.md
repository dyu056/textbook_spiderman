# 图片下载与路径更新指南

这套脚本帮助您将CourseHero的远程图片下载到本地，并更新JSON文件中的图片路径。

## 使用步骤

### Step 1: 提取图片URL列表

运行第一个脚本，扫描所有JSON文件并提取图片URL：

```bash
python3 extract_image_urls.py
```

**输出文件：**
- `image_download_list.txt` - 所有图片的完整URL列表
- `image_mapping.json` - 图片URL和文件的映射关系

### Step 2: 获取Cookie并下载图片

#### 2.1 获取Cookie

1. 在浏览器中访问并登录 https://www.coursehero.com
2. 按 `F12` 打开浏览器开发者工具
3. 切换到 **Network（网络）** 标签
4. 刷新页面或访问任意CourseHero页面
5. 在请求列表中找到任意一个对 `coursehero.com` 的请求
6. 点击该请求，在右侧找到 **Request Headers（请求头）**
7. 找到 `Cookie:` 字段，复制完整的Cookie字符串

**Cookie示例：**
```
PHPSESSID=abc123...; _ga=GA1.2.123...; user_token=xyz789...
```

#### 2.2 配置下载脚本

打开 `download_images.py` 文件，找到这一行：

```python
COOKIE = """
请将您的Cookie粘贴在这里
例如：PHPSESSID=xxxxx; _ga=xxxxx; ...
"""
```

将复制的Cookie粘贴进去：

```python
COOKIE = """
PHPSESSID=abc123...; _ga=GA1.2.123...; user_token=xyz789...
"""
```

#### 2.3 运行下载脚本

```bash
python3 download_images.py
```

脚本会：
- 自动创建 `clean_output_1/result_0204/images/` 目录
- 依次下载所有图片
- 显示下载进度和状态
- 保存失败的URL到 `failed_downloads.txt`

**下载进度示例：**
```
[1/150] 下载中: 3920 ... ✓ (45231 bytes) -> 3920.jpg
[2/150] 下载中: 3921 ... ✓ (32145 bytes) -> 3921.png
[3/150] 跳过（已存在）: 3922
```

**注意事项：**
- 下载过程中请保持网络连接
- 已存在的图片会自动跳过
- 如果部分下载失败，可以稍后重新运行脚本（会跳过已下载的）
- 默认每个请求间隔0.5秒，避免频率限制

### Step 3: 更新JSON文件路径

下载完成后，运行更新脚本，将JSON文件中的远程路径改为本地路径：

```bash
python3 update_image_paths.py
```

脚本会：
- 扫描所有JSON文件
- 将 `/solutions/attachments/3920/` 改为 `../../images/3920.jpg`
- 自动备份原文件（添加 `.backup` 后缀）
- 显示更新统计

**路径更新示例：**

更新前：
```json
{
  "render": "image",
  "value": "/solutions/attachments/3920/"
}
```

更新后：
```json
{
  "render": "image",
  "value": "../../images/3920.jpg"
}
```

HTML中的img标签也会被更新：
```html
<!-- 更新前 -->
<img src="/solutions/attachments/3920/">

<!-- 更新后 -->
<img src="../../images/3920.jpg">
```

## 完整流程示例

```bash
# 1. 提取图片URL
python3 extract_image_urls.py
# 输出: 找到 150 个唯一图片URL

# 2. 编辑 download_images.py，填入Cookie

# 3. 下载图片
python3 download_images.py
# 输出: ✓ 成功: 148, ✗ 失败: 2

# 4. 更新JSON路径
python3 update_image_paths.py
# 输出: ✓ 更新文件: 350, 🖼️ 图片引用: 148
```

## 目录结构

下载完成后的目录结构：

```
clean_output_1/result_0204/
├── images/                          # 所有图片统一存放
│   ├── 3920.jpg
│   ├── 3921.png
│   ├── 3922.gif
│   └── ...
├── Calculus-8th-Edition-.../
│   ├── catalog.json
│   └── answers/
│       ├── 22243-ch-1-problem-59.json
│       ├── 22243-ch-1-problem-59.json.backup  # 备份文件
│       └── ...
└── Thomas-Calculus-.../
    ├── catalog.json
    └── answers/
        └── ...
```

## 常见问题

### Q: Cookie过期怎么办？
A: 重新登录CourseHero，按照Step 2.1重新获取Cookie，更新脚本后重新运行。

### Q: 下载失败的图片怎么处理？
A: 查看 `failed_downloads.txt` 文件，手动访问这些URL检查原因。然后重新运行下载脚本。

### Q: 如何恢复原始JSON文件？
A: 删除更新后的JSON文件，将 `.backup` 文件重命名即可：
```bash
cd clean_output_1/result_0204/Calculus-8th-Edition-.../answers/
rm *.json
rename 's/.json.backup/.json/' *.backup
```

### Q: 可以只下载部分图片吗？
A: 可以，编辑 `image_download_list.txt`，删除不需要的URL，然后修改 `download_images.py` 让它从txt文件读取。

### Q: 图片会占用多少空间？
A: 取决于图片数量和大小，通常每张图片10-100KB，150张大约5-15MB。

## 安全提示

- Cookie是敏感信息，不要分享或提交到git仓库
- 建议在 `.gitignore` 中添加：
  ```
  download_images.py  # 如果包含Cookie
  image_download_list.txt
  image_mapping.json
  failed_downloads.txt
  ```

## 依赖安装

如果遇到 `requests` 模块未安装的错误：

```bash
pip3 install requests
```
