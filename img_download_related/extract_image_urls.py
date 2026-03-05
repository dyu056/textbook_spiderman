#!/usr/bin/env python3
"""
Step 1: 扫描所有清洗后的JSON文件，提取图片URL
"""
import json
from pathlib import Path
from collections import defaultdict
import re

# 配置
RESULT_DIR = Path('clean_output_1/result_0204')
OUTPUT_FILE = Path('image_download_list.txt')
OUTPUT_JSON = Path('image_mapping.json')

def extract_images_from_flow(flow):
    """从flow数组中提取图片URL"""
    images = []
    for item in flow:
        if isinstance(item, dict) and item.get('render') == 'image':
            images.append(item.get('value', ''))
    return images

def extract_images_from_html(html):
    """从HTML中提取img标签的src"""
    if not html:
        return []
    pattern = r'<img[^>]+src="([^"]+)"'
    return re.findall(pattern, html, re.IGNORECASE)

def scan_json_files():
    """扫描所有JSON文件，提取图片URL"""
    image_urls = set()
    file_image_map = {}  # 记录每个文件包含的图片

    # 遍历所有书籍文件夹
    for book_dir in RESULT_DIR.iterdir():
        if not book_dir.is_dir():
            continue

        answers_dir = book_dir / 'answers'
        if not answers_dir.exists():
            continue

        print(f"扫描: {book_dir.name}")
        count = 0

        # 遍历所有答案文件
        for json_file in answers_dir.glob('*.json'):
            try:
                with json_file.open('r', encoding='utf-8') as f:
                    data = json.load(f)

                file_images = []

                # 提取AnswerContent中的图片
                for answer in data.get('AnswerContent', []):
                    solution = answer.get('solution', {})
                    parts = solution.get('parts', [])

                    for part in parts:
                        # 从result中提取
                        for result_block in part.get('result', []):
                            flow = result_block.get('flow', [])
                            images = extract_images_from_flow(flow)
                            for img in images:
                                if img and img.startswith('/solutions/attachments/'):
                                    image_urls.add(img)
                                    file_images.append(img)

                        # 从steps中提取
                        for step in part.get('steps', []):
                            flow = step.get('flow', [])
                            images = extract_images_from_flow(flow)
                            for img in images:
                                if img and img.startswith('/solutions/attachments/'):
                                    image_urls.add(img)
                                    file_images.append(img)

                            # 从HTML中提取img标签
                            for item in flow:
                                if isinstance(item, dict) and item.get('render') == 'html':
                                    html_images = extract_images_from_html(item.get('value', ''))
                                    for img in html_images:
                                        if img and img.startswith('/solutions/attachments/'):
                                            image_urls.add(img)
                                            file_images.append(img)

                if file_images:
                    file_image_map[str(json_file.relative_to(RESULT_DIR))] = file_images
                    count += len(file_images)

            except Exception as e:
                print(f"  错误: {json_file.name} - {e}")

        print(f"  找到 {count} 个图片引用")

    return image_urls, file_image_map

def main():
    print("=" * 60)
    print("提取图片URL")
    print("=" * 60)

    image_urls, file_image_map = scan_json_files()

    print(f"\n总共找到 {len(image_urls)} 个唯一图片URL")

    # 保存URL列表
    with OUTPUT_FILE.open('w', encoding='utf-8') as f:
        for url in sorted(image_urls):
            f.write(f"https://www.coursehero.com{url}\n")

    print(f"\n✓ 图片URL列表已保存到: {OUTPUT_FILE}")

    # 保存映射关系
    with OUTPUT_JSON.open('w', encoding='utf-8') as f:
        json.dump({
            'total_images': len(image_urls),
            'image_urls': sorted(list(image_urls)),
            'file_mapping': file_image_map
        }, f, ensure_ascii=False, indent=2)

    print(f"✓ 图片映射关系已保存到: {OUTPUT_JSON}")

    # 显示前10个URL作为示例
    print("\n前10个图片URL示例:")
    for i, url in enumerate(sorted(list(image_urls))[:10], 1):
        print(f"{i}. https://www.coursehero.com{url}")

if __name__ == '__main__':
    main()
