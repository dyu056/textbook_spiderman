#!/usr/bin/env python3
"""
HAR数据验证脚本
验证标准：
1. 没有Lorem Ipsum占位符
2. 每个chapter连续
3. 每一章的习题几乎是连续的（允许少量缺失）
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict, OrderedDict

# 占位符文本的特征
PLACEHOLDER_MARKERS = [
    'lorem ipsum',
    'consectetur adipiscing',
    'pellentesque dapibus',
    'facilisis',
    'laoreet',
    'donec aliquet',
    'ultrices ac magna',
    'lorem',
]

CANON_RE = re.compile(
    r'/textbook-solutions/(?P<book>[^/]+)/Chapter-(?P<chapter>[^/]+)-Problem-(?P<problem>[^/]+)-(?P<origid>\d+)/?$',
    re.IGNORECASE,
)


def parse_canonical(url: str):
    """解析canonical URL"""
    if not url:
        return None
    m = CANON_RE.search(url)
    if not m:
        return None
    return m.groupdict()


def check_for_placeholders(text):
    """检查文本中是否包含占位符"""
    if not text:
        return False
    text_lower = text.lower()
    for marker in PLACEHOLDER_MARKERS:
        if marker in text_lower:
            return True
    return False


def extract_text_from_widgets(widgets):
    """从widgets中提取所有文本"""
    texts = []
    for widget in widgets or []:
        if isinstance(widget, dict) and widget.get('type') == 'text':
            texts.append(widget.get('text', ''))
    return ' '.join(texts)


def validate_har_file(har_path: Path):
    """验证单个HAR文件"""
    print(f"\n{'='*80}")
    print(f"验证文件: {har_path.name}")
    print(f"{'='*80}\n")

    # 读取HAR文件
    try:
        with har_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 无法读取HAR文件: {e}")
        return False

    # 收集所有数据
    problems_by_book = defaultdict(list)
    total_problems = 0

    for entry in data.get('log', {}).get('entries', []):
        text = entry.get('response', {}).get('content', {}).get('text', '')
        if not text.strip().startswith('{'):
            continue

        try:
            obj = json.loads(text)
        except:
            continue

        canon = obj.get('canonicalUrl', '')
        parsed = parse_canonical(canon)
        if not parsed:
            continue

        qas = obj.get('questionsAndSolutions', [])
        if not qas:
            continue

        # 提取问题数据
        for qa in qas:
            sol = qa.get('solution', {})
            sc = sol.get('solutionContent', {})
            answers = sc.get('answers', [])

            problem_data = {
                'chapter': parsed['chapter'],
                'problem': parsed['problem'],
                'origid': int(parsed['origid']),
                'canonical': canon,
                'answers': answers,
            }

            problems_by_book[parsed['book']].append(problem_data)
            total_problems += 1

    if not problems_by_book:
        print("❌ 未找到任何有效数据")
        return False

    print(f"✓ 找到 {len(problems_by_book)} 本书，共 {total_problems} 道题\n")

    # 验证每本书
    all_books_valid = True
    for book_slug, problems in sorted(problems_by_book.items()):
        print(f"\n{'─'*80}")
        print(f"书籍: {book_slug}")
        print(f"{'─'*80}")

        is_valid = validate_book(book_slug, problems)
        if not is_valid:
            all_books_valid = False

    return all_books_valid


def validate_book(book_slug: str, problems: list):
    """验证单本书的数据质量"""

    # 1. 检查占位符
    print("\n[1] 检查占位符...")
    placeholder_count = 0

    for prob in problems:
        has_placeholder = False

        for ans in prob['answers']:
            if has_placeholder:
                break

            # 检查答案widgets
            widgets_text = extract_text_from_widgets(ans.get('widgets', []))
            if check_for_placeholders(widgets_text):
                has_placeholder = True
                break

            # 检查解释explanations
            for exp in ans.get('explanations', []):
                if has_placeholder:
                    break
                if exp.get('type') == 'step_by_step':
                    for inner in exp.get('explanations', []):
                        inner_text = extract_text_from_widgets(inner.get('widgets', []))
                        if check_for_placeholders(inner_text):
                            has_placeholder = True
                            break

        if has_placeholder:
            placeholder_count += 1

    placeholder_rate = (placeholder_count / len(problems)) * 100 if problems else 0

    if placeholder_count == 0:
        print(f"  ✓ 无占位符 (0/{len(problems)})")
    elif placeholder_rate < 5:
        print(f"  ⚠️  少量占位符: {placeholder_count}/{len(problems)} ({placeholder_rate:.2f}%)")
    else:
        print(f"  ❌ 大量占位符: {placeholder_count}/{len(problems)} ({placeholder_rate:.2f}%)")
        return False

    # 2. 按章节分组
    print("\n[2] 检查章节连续性...")
    chapters = defaultdict(list)
    for prob in problems:
        chapters[prob['chapter']].append(prob)

    # 对章节排序
    def chapter_sort_key(ch_str):
        ch_upper = ch_str.upper()
        if ch_upper.isdigit():
            return (0, int(ch_upper))
        elif ch_upper == 'R':
            return (-1, 0)
        elif ch_upper.startswith('CH'):
            return (0.5, ch_upper)
        else:
            return (1, ch_upper)

    sorted_chapters = sorted(chapters.keys(), key=chapter_sort_key)

    print(f"  ✓ 找到 {len(sorted_chapters)} 个章节: {', '.join(sorted_chapters)}")

    # 3. 检查每章习题连续性
    print("\n[3] 检查习题连续性...")

    chapter_stats = []
    all_continuous = True

    for chapter in sorted_chapters:
        chapter_problems = chapters[chapter]

        # 提取习题号（尝试转换为数字）
        problem_numbers = []
        for prob in chapter_problems:
            prob_str = prob['problem']
            # 尝试提取数字
            match = re.match(r'^(\d+)', prob_str)
            if match:
                problem_numbers.append(int(match.group(1)))
            else:
                # 非数字习题号（如A, B），用字符串处理
                problem_numbers.append(prob_str)

        # 如果都是数字，检查连续性（考虑多小节情况）
        if all(isinstance(x, int) for x in problem_numbers):
            # 检测是否有多个section（习题号重复表明有多个section）
            problem_count_map = {}
            for num in problem_numbers:
                problem_count_map[num] = problem_count_map.get(num, 0) + 1

            has_multiple_sections = any(count > 1 for count in problem_count_map.values())
            unique_numbers = sorted(set(problem_numbers))
            min_num = min(unique_numbers)
            max_num = max(unique_numbers)

            if has_multiple_sections:
                # 多小节：只检查是否有大的空缺
                full_range = set(range(min_num, max_num + 1))
                present = set(unique_numbers)
                missing = sorted(full_range - present)

                # 检查最大连续缺失
                max_gap = 0
                if missing:
                    gaps = []
                    for i in range(len(missing)):
                        if i == 0 or missing[i] != missing[i-1] + 1:
                            gaps.append(1)
                        else:
                            gaps[-1] += 1
                    max_gap = max(gaps) if gaps else 0

                # 宽松标准：最大连续缺失不超过10个
                coverage = len(present) / len(full_range) * 100

                if max_gap <= 5 or coverage >= 90:
                    status = "✓"
                    continuity_rate = 100
                elif max_gap <= 10 or coverage >= 75:
                    status = "⚠️"
                    continuity_rate = 90
                    all_continuous = False
                else:
                    status = "❌"
                    continuity_rate = coverage
                    all_continuous = False

                section_info = f"(多小节, 覆盖率{coverage:.0f}%)"
                missing_str = f", 最大缺失{max_gap}个" if max_gap > 0 else ""
                print(f"  {status} Chapter {chapter}: {len(problem_numbers)}题, 范围[{min_num}-{max_num}] {section_info}{missing_str}")
            else:
                # 单小节：检查连续性
                expected_count = max_num - min_num + 1
                actual_count = len(unique_numbers)
                continuity_rate = (actual_count / expected_count) * 100 if expected_count > 0 else 0

                full_range = set(range(min_num, max_num + 1))
                missing = sorted(full_range - unique_numbers)

                if continuity_rate >= 95:
                    status = "✓"
                elif continuity_rate >= 80:
                    status = "⚠️"
                    all_continuous = False
                else:
                    status = "❌"
                    all_continuous = False

                missing_str = f", 缺失: {missing[:5]}..." if missing else ""
                print(f"  {status} Chapter {chapter}: {actual_count}题, 范围[{min_num}-{max_num}], 连续性{continuity_rate:.1f}%{missing_str}")

            chapter_stats.append({
                'chapter': chapter,
                'count': len(problem_numbers),
                'range': f'{min_num}-{max_num}',
                'continuity': continuity_rate,
                'missing': []
            })
        else:
            # 非数字习题号
            print(f"  ✓ Chapter {chapter}: {len(problem_numbers)}题 (非数字习题号)")
            chapter_stats.append({
                'chapter': chapter,
                'count': len(problem_numbers),
                'range': 'N/A',
                'continuity': 100,
                'missing': []
            })

    # 4. 生成总结
    print(f"\n[总结]")
    print(f"  书籍: {book_slug}")
    print(f"  总题数: {len(problems)}")
    print(f"  章节数: {len(sorted_chapters)}")
    print(f"  占位符率: {placeholder_rate:.2f}%")

    avg_continuity = sum(s['continuity'] for s in chapter_stats) / len(chapter_stats) if chapter_stats else 0
    print(f"  平均连续性: {avg_continuity:.1f}%")

    # 判断是否可用
    is_valid = (
        placeholder_rate < 5 and  # 占位符少于5%
        avg_continuity >= 80       # 平均连续性高于80%
    )

    if is_valid:
        print(f"\n  ✓ 数据质量: 优秀，可以使用")
    elif placeholder_rate >= 5:
        print(f"\n  ❌ 数据质量: 不可用 (占位符过多)")
    elif avg_continuity < 80:
        print(f"\n  ❌ 数据质量: 不可用 (习题不连续)")
    else:
        print(f"\n  ⚠️  数据质量: 一般，建议检查")

    return is_valid


def validate_har_folder(folder_path: Path):
    """验证文件夹中的所有HAR文件（合并验证）"""
    print(f"\n{'='*80}")
    print(f"验证文件夹: {folder_path.name}")
    print(f"{'='*80}\n")

    # 收集文件夹中的所有HAR文件
    har_files = sorted(folder_path.glob('*.har'))
    if not har_files:
        print(f"❌ 文件夹中未找到HAR文件")
        return False

    print(f"✓ 找到 {len(har_files)} 个HAR文件，将合并验证")
    for hf in har_files:
        print(f"  - {hf.name}")
    print()

    # 合并所有HAR文件的数据
    problems_by_book = defaultdict(list)
    total_problems = 0

    for har_file in har_files:
        try:
            with har_file.open('r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"⚠️  无法读取 {har_file.name}: {e}")
            continue

        for entry in data.get('log', {}).get('entries', []):
            text = entry.get('response', {}).get('content', {}).get('text', '')
            if not text.strip().startswith('{'):
                continue

            try:
                obj = json.loads(text)
            except:
                continue

            canon = obj.get('canonicalUrl', '')
            parsed = parse_canonical(canon)
            if not parsed:
                continue

            qas = obj.get('questionsAndSolutions', [])
            if not qas:
                continue

            # 提取问题数据
            for qa in qas:
                sol = qa.get('solution', {})
                sc = sol.get('solutionContent', {})
                answers = sc.get('answers', [])

                problem_data = {
                    'chapter': parsed['chapter'],
                    'problem': parsed['problem'],
                    'origid': int(parsed['origid']),
                    'canonical': canon,
                    'answers': answers,
                }

                problems_by_book[parsed['book']].append(problem_data)
                total_problems += 1

    if not problems_by_book:
        print("❌ 未找到任何有效数据")
        return False

    print(f"✓ 合并后找到 {len(problems_by_book)} 本书，共 {total_problems} 道题\n")

    # 验证每本书
    all_books_valid = True
    for book_slug, problems in sorted(problems_by_book.items()):
        print(f"\n{'─'*80}")
        print(f"书籍: {book_slug}")
        print(f"{'─'*80}")

        is_valid = validate_book(book_slug, problems)
        if not is_valid:
            all_books_valid = False

    return all_books_valid


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_har_data.py <har_file_or_folder_path>")
        print("\n示例:")
        print("  python validate_har_data.py spider_data/Math/Calculus.har")
        print("  python validate_har_data.py spider_data/Math/*.har  # 验证所有HAR文件")
        print("  python validate_har_data.py 'math_spider/第二期/Algebra and Trigonometry (10th Edition)'  # 验证文件夹")
        sys.exit(1)

    har_files = []
    har_folders = []

    for path_str in sys.argv[1:]:
        path = Path(path_str)
        if path.is_dir():
            # 如果是文件夹，添加到文件夹列表
            har_folders.append(path)
        elif path.is_file() and path.suffix == '.har':
            har_files.append(path)
        elif '*' in path_str:
            # 处理通配符
            parent = path.parent
            pattern = path.name
            har_files.extend(parent.glob(pattern))

    if not har_files and not har_folders:
        print("❌ 未找到HAR文件或文件夹")
        sys.exit(1)

    results = {}

    # 先验证文件夹（合并验证）
    if har_folders:
        print(f"准备验证 {len(har_folders)} 个文件夹\n")
        for folder in sorted(har_folders):
            is_valid = validate_har_folder(folder)
            results[folder.name] = is_valid

    # 再验证单个文件
    if har_files:
        print(f"\n准备验证 {len(har_files)} 个单独HAR文件\n")
        for har_file in sorted(har_files):
            is_valid = validate_har_file(har_file)
            results[har_file.name] = is_valid

    # 最终总结
    print(f"\n\n{'='*80}")
    print("最终验证结果")
    print(f"{'='*80}\n")

    valid_files = [name for name, valid in results.items() if valid]
    invalid_files = [name for name, valid in results.items() if not valid]

    if valid_files:
        print("✓ 可用文件:")
        for name in valid_files:
            print(f"  - {name}")

    if invalid_files:
        print("\n❌ 不可用文件:")
        for name in invalid_files:
            print(f"  - {name}")

    print(f"\n总计: {len(valid_files)}/{len(results)} 个文件可用")


if __name__ == '__main__':
    main()
