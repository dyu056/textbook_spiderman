#!/usr/bin/env python3
"""
Step 3: 更新JSON文件中的图片路径，从远程URL改为本地路径
"""
import json
from pathlib import Path
import re
import shutil

# 配置
RESULT_DIR = Path('clean_output_1/result_0204')
IMAGE_DIR = Path('clean_output_1/result_0204/images')
BACKUP_SUFFIX = '.backup'

# 如果为True，会先备份原JSON文件
CREATE_BACKUP = True

def get_attachment_id(url):
    """从URL中提取attachment ID"""
    match = re.search(r'/attachments/(\d+)', url)
    return match.group(1) if match else None

def find_local_image(attachment_id):
    """查找本地图片文件（可能有不同的扩展名）"""
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']:
        image_path = IMAGE_DIR / f"{attachment_id}{ext}"
        if image_path.exists():
            return image_path
    return None

def update_flow_images(flow, book_slug):
    """更新flow数组中的图片路径"""
    updated = False
    for item in flow:
        if isinstance(item, dict) and item.get('render') == 'image':
            old_url = item.get('value', '')
            if old_url and old_url.startswith('/solutions/attachments/'):
                attachment_id = get_attachment_id(old_url)
                if attachment_id:
                    local_image = find_local_image(attachment_id)
                    if local_image:
                        # 使用相对路径：从书籍目录到images目录
                        new_path = f"../../images/{local_image.name}"
                        item['value'] = new_path
                        updated = True
    return updated

def update_html_images(html, book_slug):
    """更新HTML中的img标签的src属性"""
    if not html:
        return html, False

    updated = False

    def replace_src(match):
        nonlocal updated
        old_url = match.group(1)
        if old_url.startswith('/solutions/attachments/'):
            attachment_id = get_attachment_id(old_url)
            if attachment_id:
                local_image = find_local_image(attachment_id)
                if local_image:
                    new_path = f"../../images/{local_image.name}"
                    updated = True
                    return f'<img src="{new_path}"'
        return match.group(0)

    new_html = re.sub(r'<img[^>]+src="([^"]+)"', replace_src, html, flags=re.IGNORECASE)
    return new_html, updated

def update_json_file(json_path, book_slug):
    """更新单个JSON文件"""
    try:
        with json_path.open('r', encoding='utf-8') as f:
            data = json.load(f)

        total_updated = 0

        # 更新AnswerContent中的图片
        for answer in data.get('AnswerContent', []):
            solution = answer.get('solution', {})
            parts = solution.get('parts', [])

            for part in parts:
                # 更新result中的flow
                for result_block in part.get('result', []):
                    flow = result_block.get('flow', [])
                    if update_flow_images(flow, book_slug):
                        total_updated += 1

                # 更新steps中的flow
                for step in part.get('steps', []):
                    flow = step.get('flow', [])
                    if update_flow_images(flow, book_slug):
                        total_updated += 1

                    # 更新HTML中的img标签
                    for item in flow:
                        if isinstance(item, dict) and item.get('render') == 'html':
                            old_html = item.get('value', '')
                            new_html, updated = update_html_images(old_html, book_slug)
                            if updated:
                                item['value'] = new_html
                                total_updated += 1

        if total_updated > 0:
            # 备份原文件
            if CREATE_BACKUP:
                backup_path = json_path.with_suffix(json_path.suffix + BACKUP_SUFFIX)
                if not backup_path.exists():  # 只备份一次
                    shutil.copy2(json_path, backup_path)

            # 保存更新后的文件
            with json_path.open('w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True, total_updated
        else:
            return False, 0

    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("更新JSON文件中的图片路径")
    print("=" * 60)

    # 检查images目录
    if not IMAGE_DIR.exists():
        print(f"\n❌ 错误: 找不到图片目录 {IMAGE_DIR}")
        print("请先运行 download_images.py 下载图片")
        return

    # 统计images目录中的文件
    image_files = list(IMAGE_DIR.glob('*'))
    image_count = len([f for f in image_files if f.is_file()])
    print(f"\n图片目录: {IMAGE_DIR}")
    print(f"本地图片数量: {image_count}")

    if image_count == 0:
        print("\n❌ 错误: 图片目录为空")
        print("请先运行 download_images.py 下载图片")
        return

    # 处理统计
    total_files = 0
    updated_files = 0
    total_images = 0

    # 遍历所有书籍文件夹
    for book_dir in RESULT_DIR.iterdir():
        if not book_dir.is_dir() or book_dir.name == 'images':
            continue

        answers_dir = book_dir / 'answers'
        if not answers_dir.exists():
            continue

        print(f"\n处理: {book_dir.name}")
        book_updated = 0
        book_images = 0

        # 遍历所有答案文件
        for json_file in answers_dir.glob('*.json'):
            total_files += 1
            success, count = update_json_file(json_file, book_dir.name)

            if success:
                if count > 0:
                    updated_files += 1
                    book_updated += 1
                    total_images += count
                    book_images += count
            elif isinstance(count, str):
                print(f"  ✗ 错误: {json_file.name} - {count}")

        if book_updated > 0:
            print(f"  ✓ 更新了 {book_updated} 个文件，{book_images} 处图片引用")

    # 输出统计
    print("\n" + "=" * 60)
    print("更新完成!")
    print(f"📁 扫描文件: {total_files}")
    print(f"✓ 更新文件: {updated_files}")
    print(f"🖼️  图片引用: {total_images}")

    if CREATE_BACKUP and updated_files > 0:
        print(f"\n💾 原文件已备份（扩展名: {BACKUP_SUFFIX}）")
        print("如需恢复，可删除更新后的文件，并将备份文件重命名")

if __name__ == '__main__':
    main()
