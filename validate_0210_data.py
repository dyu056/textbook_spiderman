#!/usr/bin/env python3
"""
验证 0210_data 文件夹中的数据质量
检查项：
1. Lorem Ipsum 占位符检测
2. 多书混杂检测（一个文件/文件夹只应包含一本书）
3. 书名与文件名匹配度
4. 章节连续性
5. 习题编号连续性/覆盖率（按小节拆分显示）
"""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

SOURCE_DIR = Path('math_spider/0210_data')
OUTPUT_FILE = SOURCE_DIR / '0210_validation_report.txt'

CANON_RE = re.compile(
    r'/textbook-solutions/(?P<book>[^/]+)/Chapter-(?P<chapter>[^/]+)-Problem-(?P<problem>[^/]+)-(?P<origid>\d+)/?$',
    re.IGNORECASE,
)

# Lorem Ipsum 占位符标记
LOREM_MARKERS = [
    'lorem ipsum',
    'consectetur adipiscing',
    'pellentesque dapibus',
    'facilisis',
    'laoreet',
    'donec aliquet',
    'ultrices ac magna',
]

# 通用占位符
GENERIC_PLACEHOLDERS = [
    r'\[placeholder\]',
    r'\[image\]',
    r'\[formula\]',
    r'Coming soon',
    r'Under construction',
]


class TeeOutput:
    """同时输出到终端和文件"""
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.file = open(filepath, 'w', encoding='utf-8')

    def write(self, msg):
        self.terminal.write(msg)
        self.file.write(msg)

    def flush(self):
        self.terminal.flush()
        self.file.flush()

    def close(self):
        self.file.close()


def check_lorem(text):
    if not text:
        return False
    text_lower = text.lower()
    for marker in LOREM_MARKERS:
        if marker in text_lower:
            return True
    return False


def check_generic_placeholder(text):
    if not text:
        return []
    found = []
    for pattern in GENERIC_PLACEHOLDERS:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(pattern)
    return found


def extract_text_from_widgets(widgets):
    texts = []
    for widget in widgets or []:
        if isinstance(widget, dict):
            if widget.get('type') == 'text':
                texts.append(widget.get('text', ''))
            elif widget.get('type') == 'html':
                texts.append(widget.get('html', ''))
    return ' '.join(texts)


def normalize_name(name):
    name = re.sub(r'-\d+$', '', name)
    name = re.sub(r'\s*\(?\d+(?:st|nd|rd|th)\s+Edition\)?', '', name, flags=re.IGNORECASE)
    name = re.sub(r'97[89]\d{10}', '', name)
    name = re.sub(r'-\d+$', '', name)
    name = re.sub(r'[^\w\s]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip().lower()
    return name


def slug_to_name(slug):
    parts = slug.split('-')
    name_parts = []
    for part in parts:
        if re.match(r'97[89]\d{10}', part):
            break
        if re.match(r'\d+(?:st|nd|rd|th)', part, re.IGNORECASE):
            break
        if part.isdigit() and len(part) <= 3:
            continue
        name_parts.append(part.lower())
    return ' '.join(name_parts)


def calc_name_similarity(slug, filename):
    slug_name = slug_to_name(slug)
    file_name = normalize_name(filename)
    slug_words = set(slug_name.split())
    file_words = set(file_name.split())
    if not slug_words or not file_words:
        return 0.0
    common = slug_words & file_words
    return len(common) / max(len(slug_words), len(file_words))


def chapter_sort_key(ch_str):
    ch_upper = ch_str.upper()
    if ch_upper.isdigit():
        return (0, int(ch_upper), '')
    elif ch_upper == 'R':
        return (-1, 0, '')
    elif ch_upper == 'P':
        return (-0.5, 0, '')
    else:
        return (1, 0, ch_upper)


def parse_har_file(har_path):
    problems_by_book = defaultdict(list)
    try:
        with har_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ❌ 无法读取 {har_path.name}: {e}")
        return problems_by_book

    for entry in data.get('log', {}).get('entries', []):
        text = entry.get('response', {}).get('content', {}).get('text', '')
        if not text or not text.strip().startswith('{'):
            continue
        try:
            obj = json.loads(text)
        except:
            continue

        canon = obj.get('canonicalUrl', '')
        m = CANON_RE.search(canon)
        if not m:
            continue
        qas = obj.get('questionsAndSolutions', [])
        if not qas:
            continue

        book_slug = m.group('book')
        chapter = m.group('chapter')
        problem = m.group('problem')
        origid = int(m.group('origid'))

        for qa in qas:
            sol = qa.get('solution', {})
            sc = sol.get('solutionContent', {})
            answers = sc.get('answers', [])
            problems_by_book[book_slug].append({
                'chapter': chapter,
                'problem': problem,
                'origid': origid,
                'canonical': canon,
                'answers': answers,
            })
    return problems_by_book


def check_book_placeholders(problems):
    lorem_count = 0
    generic_count = 0
    for prob in problems:
        has_lorem = False
        has_generic = False
        for ans in prob['answers']:
            if has_lorem and has_generic:
                break
            widgets_text = extract_text_from_widgets(ans.get('widgets', []))
            if not has_lorem and check_lorem(widgets_text):
                has_lorem = True
            if not has_generic and check_generic_placeholder(widgets_text):
                has_generic = True
            for exp in ans.get('explanations', []):
                if has_lorem and has_generic:
                    break
                if exp.get('type') == 'step_by_step':
                    for inner in exp.get('explanations', []):
                        inner_text = extract_text_from_widgets(inner.get('widgets', []))
                        if not has_lorem and check_lorem(inner_text):
                            has_lorem = True
                        if not has_generic and check_generic_placeholder(inner_text):
                            has_generic = True
        if has_lorem:
            lorem_count += 1
        if has_generic:
            generic_count += 1
    return lorem_count, generic_count


def detect_sections(chapter_problems):
    """
    按 origid 排序，检测小节边界（题号大幅回落时为新小节）。
    返回 list of sections，每个 section 是 [int, int, ...] 题号列表。
    """
    # 提取 (origid, problem_number) 对
    items = []
    non_numeric_count = 0
    for prob in chapter_problems:
        match = re.match(r'^(\d+)', prob['problem'])
        if match:
            items.append((prob['origid'], int(match.group(1))))
        else:
            non_numeric_count += 1

    if not items:
        return [], non_numeric_count

    # 按 origid 排序（还原抓取/网页上的自然顺序）
    items.sort(key=lambda x: x[0])

    sections = []
    current_section = [items[0][1]]
    current_max = items[0][1]

    for i in range(1, len(items)):
        num = items[i][1]
        # 题号大幅回落 → 新小节
        # 判定：当前题号 < 当前小节最大题号的 40%，且最大题号 > 5
        if current_max > 5 and num < current_max * 0.4:
            sections.append(current_section)
            current_section = [num]
            current_max = num
        else:
            current_section.append(num)
            if num > current_max:
                current_max = num

    if current_section:
        sections.append(current_section)

    return sections, non_numeric_count


def analyze_section(nums):
    """分析单个小节的题号覆盖情况"""
    unique = sorted(set(nums))
    min_n = min(unique)
    max_n = max(unique)
    full = set(range(min_n, max_n + 1))
    present = set(unique)
    missing = sorted(full - present)
    coverage = len(present) / len(full) * 100 if full else 100

    max_gap = 0
    if missing:
        gaps = []
        for i, m in enumerate(missing):
            if i == 0 or m != missing[i - 1] + 1:
                gaps.append(1)
            else:
                gaps[-1] += 1
        max_gap = max(gaps) if gaps else 0

    return {
        'count': len(nums),
        'unique': len(unique),
        'min': min_n,
        'max': max_n,
        'coverage': coverage,
        'max_gap': max_gap,
        'missing_count': len(missing),
        'missing': missing,
    }


def check_continuity(problems):
    """检查章节连续性和习题覆盖率，按小节拆分"""
    chapters = defaultdict(list)
    for prob in problems:
        chapters[prob['chapter']].append(prob)

    sorted_chapters = sorted(chapters.keys(), key=chapter_sort_key)

    chapter_results = []
    for chapter in sorted_chapters:
        chapter_problems = chapters[chapter]
        sections, non_numeric = detect_sections(chapter_problems)

        if not sections:
            # 全部非数字题号
            chapter_results.append({
                'chapter': chapter,
                'total_count': len(chapter_problems),
                'sections': [],
                'is_numeric': False,
                'non_numeric': non_numeric,
                'avg_coverage': 100,
            })
            continue

        section_details = []
        for sec_nums in sections:
            info = analyze_section(sec_nums)
            section_details.append(info)

        # 计算整章的平均覆盖率（按小节加权）
        total_unique = sum(s['unique'] for s in section_details)
        total_full = sum(s['max'] - s['min'] + 1 for s in section_details)
        overall_coverage = (total_unique / total_full * 100) if total_full > 0 else 100

        chapter_results.append({
            'chapter': chapter,
            'total_count': sum(s['count'] for s in section_details) + non_numeric,
            'sections': section_details,
            'is_numeric': True,
            'non_numeric': non_numeric,
            'avg_coverage': overall_coverage,
        })

    return sorted_chapters, chapter_results


def validate_unit(unit_name, har_files):
    print(f"\n{'=' * 80}")
    print(f"验证: {unit_name}")
    print(f"{'=' * 80}")

    if len(har_files) > 1:
        print(f"  包含 {len(har_files)} 个HAR文件:")
        for hf in har_files:
            print(f"    - {hf.name}")

    all_problems = defaultdict(list)
    for hf in har_files:
        book_data = parse_har_file(hf)
        for slug, probs in book_data.items():
            all_problems[slug].extend(probs)

    total_problems = sum(len(p) for p in all_problems.values())
    num_books = len(all_problems)

    result = {
        'unit_name': unit_name,
        'num_books': num_books,
        'total_problems': total_problems,
        'books': {},
        'issues': [],
    }

    if not all_problems:
        print("  ❌ 未找到有效数据")
        result['issues'].append('无有效数据')
        return result

    print(f"\n  找到 {num_books} 本书，共 {total_problems} 道题")

    # ---- 检查1: 多书混杂 ----
    if num_books > 1:
        print(f"\n  ⚠️  [多书检测] 发现 {num_books} 本不同的书!")
        for slug, probs in sorted(all_problems.items()):
            print(f"    - {slug} ({len(probs)} 题)")
        result['issues'].append(f'包含{num_books}本不同的书')

    # ---- 检查2: 书名与文件名匹配 ----
    print(f"\n  [书名匹配]")
    for slug in sorted(all_problems.keys()):
        similarity = calc_name_similarity(slug, unit_name)
        if similarity >= 0.5:
            print(f"    ✓ {slug}")
            print(f"      相似度: {similarity:.2f}")
        else:
            print(f"    ⚠️  {slug}")
            print(f"      与文件名「{unit_name}」相似度仅 {similarity:.2f}")
            result['issues'].append(f'书名不匹配: slug={slug}, 文件={unit_name}, 相似度={similarity:.2f}')

    # ---- 逐本书详细验证 ----
    for slug in sorted(all_problems.keys()):
        problems = all_problems[slug]
        print(f"\n  {'─' * 70}")
        print(f"  书籍: {slug} ({len(problems)} 题)")
        print(f"  {'─' * 70}")

        book_result = {'slug': slug, 'count': len(problems)}

        # 检查3: Lorem Ipsum
        lorem_count, generic_count = check_book_placeholders(problems)
        lorem_rate = (lorem_count / len(problems)) * 100 if problems else 0

        if lorem_count == 0:
            print(f"    [Lorem检测] ✓ 无占位符 (0/{len(problems)})")
        elif lorem_rate < 5:
            print(f"    [Lorem检测] ⚠️  少量占位符: {lorem_count}/{len(problems)} ({lorem_rate:.1f}%)")
        else:
            print(f"    [Lorem检测] ❌ 大量占位符: {lorem_count}/{len(problems)} ({lorem_rate:.1f}%)")
            result['issues'].append(f'{slug}: Lorem占位符过多 ({lorem_rate:.1f}%)')

        if generic_count > 0:
            print(f"    [通用占位符] ⚠️  {generic_count} 处")

        book_result['lorem_count'] = lorem_count
        book_result['lorem_rate'] = lorem_rate

        # 检查4+5: 章节和习题连续性（按小节展示）
        sorted_chapters, chapter_results = check_continuity(problems)
        print(f"    [章节] 共 {len(sorted_chapters)} 章: {', '.join(sorted_chapters)}")

        print(f"    [习题连续性]")
        for cr in chapter_results:
            ch = cr['chapter']

            if not cr['is_numeric']:
                print(f"      ✓ Ch {ch}: {cr['total_count']}题 (非数字习题号)")
                continue

            sections = cr['sections']
            avg_cov = cr['avg_coverage']
            non_num = cr['non_numeric']

            if avg_cov >= 90:
                status = "✓"
            elif avg_cov >= 75:
                status = "⚠️"
            else:
                status = "❌"

            num_sections = len(sections)
            total_count = cr['total_count']
            non_num_str = f" + {non_num}个非数字题号" if non_num > 0 else ""

            # 构建小节范围字符串
            sec_ranges = []
            for s in sections:
                r = f"[{s['min']}-{s['max']}]({s['unique']}题)"
                sec_ranges.append(r)

            # 主行：章节概要
            print(f"      {status} Ch {ch}: {total_count}题, {num_sections}个小节, 整章覆盖{avg_cov:.0f}%{non_num_str}")

            # 子行：每个小节详情
            for idx, (s, rng_str) in enumerate(zip(sections, sec_ranges), 1):
                gap_str = f", 缺{s['missing_count']}个(最大连续缺{s['max_gap']})" if s['missing_count'] > 0 else ""
                cov_str = f"{s['coverage']:.0f}%"
                print(f"          小节{idx}: [{s['min']}-{s['max']}] {s['unique']}题, 覆盖{cov_str}{gap_str}")
                if s['missing']:
                    # 将缺失题号压缩为连续区间显示，如 [3-5, 8, 12-15]
                    ranges = []
                    start = s['missing'][0]
                    end = start
                    for m in s['missing'][1:]:
                        if m == end + 1:
                            end = m
                        else:
                            ranges.append(f"{start}" if start == end else f"{start}-{end}")
                            start = end = m
                    ranges.append(f"{start}" if start == end else f"{start}-{end}")
                    print(f"                   缺失: {', '.join(ranges)}")

        # 整书平均覆盖率
        coverages = [cr['avg_coverage'] for cr in chapter_results]
        avg_coverage = sum(coverages) / len(coverages) if coverages else 0
        book_result['chapters'] = len(sorted_chapters)
        book_result['avg_coverage'] = avg_coverage

        if avg_coverage < 80:
            result['issues'].append(f'{slug}: 平均覆盖率低 ({avg_coverage:.1f}%)')

        # 综合判定
        is_good = lorem_rate < 5 and avg_coverage >= 80
        if is_good:
            print(f"    [结论] ✓ 数据质量优秀，可以使用 (覆盖率{avg_coverage:.1f}%)")
        else:
            reasons = []
            if lorem_rate >= 5:
                reasons.append(f"占位符{lorem_rate:.1f}%")
            if avg_coverage < 80:
                reasons.append(f"覆盖率{avg_coverage:.1f}%")
            print(f"    [结论] ❌ 数据质量不达标: {', '.join(reasons)}")

        result['books'][slug] = book_result

    return result


def main():
    # 同时输出到终端和文件
    tee = TeeOutput(OUTPUT_FILE)
    sys.stdout = tee

    print("=" * 80)
    print("  0210_data 数据验证报告")
    print("=" * 80)

    # 收集验证单元（扫描 valid_data 和 invalid_data）
    def collect_units(folder):
        """从文件夹中收集验证单元"""
        units = []
        if not folder.exists():
            return units
        for item in sorted(folder.iterdir()):
            if item.name.startswith('.') or item.suffix == '.md':
                continue
            if item.is_file() and item.suffix == '.har':
                units.append((item.stem, [item]))
            elif item.is_dir():
                har_files = sorted(item.glob('*.har'))
                if har_files:
                    units.append((item.name, har_files))
        return units

    valid_dir = SOURCE_DIR / 'valid_data'
    invalid_dir = SOURCE_DIR / 'invalid_data'

    # 如果已分类，从子文件夹收集；否则从根目录收集
    if valid_dir.exists() or invalid_dir.exists():
        valid_units_list = collect_units(valid_dir)
        invalid_units_list = collect_units(invalid_dir)
        # 也扫描根目录下残余的HAR文件
        root_units = collect_units(SOURCE_DIR)
        # 过滤掉 valid_data/invalid_data 目录本身
        root_units = [(n, f) for n, f in root_units
                      if not any(str(ff).startswith(str(valid_dir)) or str(ff).startswith(str(invalid_dir))
                                 for ff in f)]
        units = root_units + valid_units_list + invalid_units_list
    else:
        units = collect_units(SOURCE_DIR)

    print(f"\n共发现 {len(units)} 个验证单元:")
    for name, files in units:
        # 标注来源
        src = ""
        if files and str(files[0]).startswith(str(valid_dir)):
            src = " [valid_data]"
        elif files and str(files[0]).startswith(str(invalid_dir)):
            src = " [invalid_data]"
        print(f"  - {name} ({len(files)} 个HAR文件){src}")

    # 逐个验证
    all_results = []
    for name, files in units:
        result = validate_unit(name, files)
        all_results.append(result)

    # ==================== 全局汇总 ====================
    print(f"\n\n{'=' * 80}")
    print("  全局验证汇总")
    print(f"{'=' * 80}")

    total_books_count = 0
    total_problems_count = 0
    valid_units = []
    problematic_units = []

    for r in all_results:
        total_books_count += r['num_books']
        total_problems_count += r['total_problems']
        if r['issues']:
            problematic_units.append(r)
        else:
            valid_units.append(r)

    print(f"\n  总验证单元: {len(all_results)}")
    print(f"  总书籍数: {total_books_count}")
    print(f"  总题目数: {total_problems_count:,}")

    # 多书混杂
    multi_book = [r for r in all_results if r['num_books'] > 1]
    print(f"\n  [多书混杂检测]")
    if multi_book:
        print(f"  ⚠️  {len(multi_book)} 个单元包含多本书:")
        for r in multi_book:
            print(f"    - {r['unit_name']}: {list(r['books'].keys())}")
    else:
        print(f"  ✓ 无多书混杂")

    # 书名匹配
    name_mismatch = [r for r in all_results
                     if any('书名不匹配' in iss for iss in r['issues'])]
    print(f"\n  [书名匹配检测]")
    if name_mismatch:
        print(f"  ⚠️  {len(name_mismatch)} 个单元书名不匹配:")
        for r in name_mismatch:
            for iss in r['issues']:
                if '书名不匹配' in iss:
                    print(f"    - {iss}")
    else:
        print(f"  ✓ 所有书名匹配")

    # Lorem 占位符
    lorem_issues = [r for r in all_results
                    if any('Lorem' in iss for iss in r['issues'])]
    print(f"\n  [Lorem占位符检测]")
    if lorem_issues:
        print(f"  ⚠️  {len(lorem_issues)} 个单元有占位符问题:")
        for r in lorem_issues:
            for iss in r['issues']:
                if 'Lorem' in iss:
                    print(f"    - {iss}")
    else:
        print(f"  ✓ 无Lorem占位符")

    # 总结
    print(f"\n  {'─' * 60}")
    if problematic_units:
        print(f"\n  ⚠️  有问题的单元 ({len(problematic_units)}):")
        for r in problematic_units:
            print(f"    - {r['unit_name']}:")
            for iss in r['issues']:
                print(f"      • {iss}")

    if valid_units:
        print(f"\n  ✓ 正常的单元 ({len(valid_units)}):")
        for r in valid_units:
            print(f"    - {r['unit_name']} ({r['total_problems']:,} 题)")

    print(f"\n{'=' * 80}")
    print(f"  验证完成! {len(valid_units)}/{len(all_results)} 个单元通过验证")
    print(f"{'=' * 80}")

    sys.stdout = tee.terminal
    tee.close()
    print(f"\n报告已保存到: {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
