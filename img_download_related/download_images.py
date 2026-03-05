#!/usr/bin/env python3
"""
Step 2: 下载图片到本地
使用方法：
1. 在浏览器中登录 CourseHero
2. 打开开发者工具 (F12)
3. 进入 Network 标签
4. 访问任意 coursehero.com 页面
5. 找到一个请求，右键 -> Copy -> Copy as cURL
6. 从cURL命令中复制 Cookie 字符串，粘贴到下面的 COOKIE 变量中
"""
import json
import requests
from pathlib import Path
import time
import re

# ====== 配置区域 ======
# 请在这里填入您的 Cookie（从浏览器复制）
COOKIE = """
_ga=GA1.1.1292413847.1769310908; OTGPPConsent=DBABLA~BVQqAAAAAAKA.QA; _fbp=fb.1.1769311179015.1149686072; _gtmeec=eyJleHRlcm5hbF9pZCI6IjEwMDAwMDkwMzQxNjI2NyJ9; __ssid=83ba7000-787f-4bec-87f5-284fe92ea5a3; _gcl_gs=2.1.k1$i1769495356$u132009117; _gcl_aw=GCL.1769495380.Cj0KCQiAvtzLBhCPARIsALwhxdohefM3EZ-slF51FF6-VpTbuD3IquT-ULHJUxQiw5QMay_kr8ultJEaAqioEALw_wcB; supportEmail=yunnananna358%40gmail.com; OptanonAlertBoxClosed=2026-02-04T08:53:51.695Z; ab.storage.deviceId.e00c83ea-b6ed-4d7d-84ba-974600395aaf=g%3A1ecf718b-c9c0-7f33-c0dd-802c1a5724b9%7Ce%3Aundefined%7Cc%3A1769329215581%7Cl%3A1770263590083; ab.storage.userId.e00c83ea-b6ed-4d7d-84ba-974600395aaf=g%3Ac13071f1-d3db-4b4e-a474-bb2e6d0d2563%7Ce%3Aundefined%7Cc%3A1769329215578%7Cl%3A1770263590083; ab.storage.sessionId.e00c83ea-b6ed-4d7d-84ba-974600395aaf=g%3A5581e41b-51e3-f6bb-87b0-47198f7a794b%7Ce%3A1770263590083%7Cl%3A1770263628252; __cf_bm=GFiZvIqhAN6Ct8xFCRcwjT0lWkmJo1afMxJG6zRG24w-1770265279-1.0.1.1-9Mrs0e.GaHmLO6BR5j1MdEiPCwgt6n.TlDPMhZsRmv0cM7FrhaO307WnsJ3Nc7vmtQHRtDexxOKGG0WMUiTyUWYKG7S5O144_e1tkNaQPLo; cf_clearance=jak0.pFD4ceeF5rjy090blDEKzC6p3boHgECbkA5SSQ-1770265507-1.2.1.1-ApO.51Kw_0NENjayVeBNsQHmcNcGPMLHkhYiNoB_X77coB0DE5vWI.y_uLXXvy5AIWu1J7e53_MToZSy0Srr2m3OZ8Y8T_wvmYMgtKmBmIqG0w18eoZKAZZsp9wJ4Q1iQ8zrKv22_xtMZfyEM5k_IOLU6qocMEX1VYoRHz7U7CjTswsJDGsr_PpGR4VO5gl4z5asqZUrevLxwCNE5FtN0uEvNAGkRTbFh97OaAQfZBg; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Feb+05+2026+12%3A27%3A29+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202512.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&GPPCookiesCount=1&gppSid=7&groups=C0001%3A1%2CC0003%3A1%2CSSPD_BG%3A1%2CC0004%3A1%2CC0002%3A1&AwaitingReconsent=false&geolocation=US%3BNJ; AMP_3a41cfadba=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIyNzFmYTViODJiNTQ3ODFiNjhjZDcwZWZlNTg3YmE5MmFkMjBjYzgyJTIyJTJDJTIydXNlcklkJTIyJTNBJTIyMTAwMDAwOTAzNDE2MjY3JTIyJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTc3MDI2MjIyNCUyQyUyMm9wdE91dCUyMiUzQWZhbHNlJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE3NzAyNjU2NTA0MzElMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTE2NCUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBMCU3RA==; _ga_HR7CRKGJMD=GS2.1.s1770265505$o4$g1$t1770266154$j60$l0$h755372034
"""

# 其他配置
IMAGE_LIST_FILE = Path('image_mapping.json')
OUTPUT_DIR = Path('clean_output_1/result_0204/images')
DELAY_SECONDS = 5  # 请求之间的延迟，避免被限制

# 测试模式：只下载前几张图片
TEST_MODE = True
TEST_DOWNLOAD_COUNT = 3  # 测试时只下载3张

# ====== 配置区域结束 ======

def get_attachment_id(url):
    """从URL中提取attachment ID"""
    match = re.search(r'/attachments/(\d+)', url)
    return match.group(1) if match else None

def download_image(url, output_path, headers):
    """下载单个图片"""
    try:
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()

        # 从Content-Type推测文件扩展名
        content_type = response.headers.get('Content-Type', '')
        ext = '.jpg'  # 默认
        if 'png' in content_type:
            ext = '.png'
        elif 'gif' in content_type:
            ext = '.gif'
        elif 'svg' in content_type:
            ext = '.svg'
        elif 'webp' in content_type:
            ext = '.webp'

        # 如果文件名没有扩展名，添加上
        if not output_path.suffix:
            output_path = output_path.with_suffix(ext)

        # 保存文件
        with output_path.open('wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True, output_path, len(response.content)

    except Exception as e:
        return False, output_path, str(e)

def main():
    print("=" * 60)
    print("下载图片")
    print("=" * 60)

    # 检查Cookie
    if '请将您的Cookie粘贴在这里' in COOKIE or len(COOKIE.strip()) < 50:
        print("\n❌ 错误: 请先在脚本中填入您的 Cookie!")
        print("\n获取Cookie的步骤:")
        print("1. 在浏览器中登录 CourseHero")
        print("2. 按F12打开开发者工具")
        print("3. 进入 Network 标签")
        print("4. 访问任意 coursehero.com 页面")
        print("5. 找到一个请求，查看 Request Headers 中的 Cookie")
        print("6. 复制完整的 Cookie 字符串到脚本的 COOKIE 变量中")
        return

    # 加载图片列表
    if not IMAGE_LIST_FILE.exists():
        print(f"\n❌ 错误: 找不到 {IMAGE_LIST_FILE}")
        print("请先运行 extract_image_urls.py")
        return

    with IMAGE_LIST_FILE.open('r', encoding='utf-8') as f:
        data = json.load(f)

    image_urls = data['image_urls']

    # 测试模式：只下载前几张
    if TEST_MODE:
        image_urls = image_urls[:TEST_DOWNLOAD_COUNT]
        print(f"\n⚠️  测试模式：只下载前 {len(image_urls)} 张图片")
    else:
        print(f"\n总共需要下载 {len(image_urls)} 个图片")

    # 创建输出目录
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 设置请求头
    headers = {
        'Cookie': COOKIE.strip(),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://www.coursehero.com/',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
    }

    # 下载统计
    success_count = 0
    fail_count = 0
    total_size = 0
    failed_urls = []

    # 开始下载
    print("\n开始下载...")
    for i, url_path in enumerate(image_urls, 1):
        full_url = f"https://www.coursehero.com{url_path}"
        attachment_id = get_attachment_id(url_path)

        if not attachment_id:
            print(f"[{i}/{len(image_urls)}] ⚠️  跳过（无法提取ID）: {url_path}")
            fail_count += 1
            failed_urls.append((url_path, "无法提取ID"))
            continue

        output_path = OUTPUT_DIR / attachment_id

        # 如果已存在，跳过
        if any(output_path.with_suffix(ext).exists() for ext in ['.jpg', '.png', '.gif', '.svg', '.webp']):
            print(f"[{i}/{len(image_urls)}] ⏭️  跳过（已存在）: {attachment_id}")
            success_count += 1
            continue

        print(f"[{i}/{len(image_urls)}] 下载中: {attachment_id} ... ", end='', flush=True)

        success, saved_path, result = download_image(full_url, output_path, headers)

        if success:
            print(f"✓ ({result} bytes) -> {saved_path.name}")
            success_count += 1
            total_size += result
        else:
            print(f"✗ {result}")
            fail_count += 1
            failed_urls.append((url_path, result))

        # 延迟
        time.sleep(DELAY_SECONDS)

    # 输出统计
    print("\n" + "=" * 60)
    print("下载完成!")
    print(f"✓ 成功: {success_count}")
    print(f"✗ 失败: {fail_count}")
    print(f"📦 总大小: {total_size / 1024 / 1024:.2f} MB")
    print(f"📁 保存位置: {OUTPUT_DIR}")

    # 保存失败列表
    if failed_urls:
        fail_file = Path('failed_downloads.txt')
        with fail_file.open('w', encoding='utf-8') as f:
            for url, reason in failed_urls:
                f.write(f"{url}\t{reason}\n")
        print(f"\n⚠️  失败的URL已保存到: {fail_file}")

if __name__ == '__main__':
    main()
