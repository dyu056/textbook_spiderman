#!/usr/bin/env python3
import json
import re
from pathlib import Path
from collections import defaultdict, OrderedDict

SOURCE_DIR = Path('math_spider/0205_data/valid_data')
OUT_DIR = Path('clean_output_1/result_0205')
# Only process this specific file
TARGET_FILE = None  # Process all .har files in the directory

CANON_RE = re.compile(
    r'/textbook-solutions/(?P<book>[^/]+)/Chapter-(?P<chapter>[^/]+)-Problem-(?P<problem>[^/]+)-(?P<origid>\d+)/?$',
    re.IGNORECASE,
)
ISBN_RE = re.compile(r'(97[89]\d{10})')
EDITION_RE = re.compile(r'(\d+(?:st|nd|rd|th)-Edition)', re.IGNORECASE)

YOUTUBE_HOSTS = {'www.youtube.com', 'youtu.be'}

# Process all books (no filter)
VALID_BOOKS = None

# Starting global problem ID (set to continue from previous batch)
START_PROBLEM_ID = 35629


def parse_canonical(url: str):
    if not url:
        return None
    m = CANON_RE.search(url)
    if not m:
        return None
    return m.groupdict()


def slug_to_title(slug: str):
    # Remove edition, isbn, trailing numeric tokens
    parts = slug.split('-')
    cleaned = []
    for p in parts:
        if ISBN_RE.fullmatch(p):
            continue
        if EDITION_RE.fullmatch(p + ''):
            # edition is usually split, keep for bookEdition separately
            continue
        if p.isdigit():
            continue
        cleaned.append(p)
    # Title-case words, keep acronyms
    title = ' '.join(cleaned)
    return ' '.join(w.upper() if w.isupper() else w.capitalize() for w in title.split())


def slug_to_isbn(slug: str):
    m = ISBN_RE.search(slug)
    return m.group(1) if m else ''


def slug_to_edition(slug: str):
    m = EDITION_RE.search(slug)
    return m.group(1) if m else ''


def extract_img_sources(html: str):
    if not html:
        return [], html
    # find all img src
    srcs = re.findall(r'<img[^>]+src="([^"]+)"', html, flags=re.IGNORECASE)
    # remove img tags
    cleaned = re.sub(r'<img[^>]*>', '', html, flags=re.IGNORECASE).strip()
    return srcs, cleaned


def widget_to_flow_items(widget: dict):
    wtype = widget.get('type')
    if wtype == 'graph':
        return [{'render': 'graph', 'value': widget.get('source', '')}]
    if wtype == 'text':
        html = widget.get('text', '')
        img_srcs, cleaned_html = extract_img_sources(html)
        items = []
        for src in img_srcs:
            items.append({'render': 'image', 'value': src})
        if cleaned_html:
            items.append({'render': 'html', 'value': cleaned_html})
        if not items:
            items.append({'render': 'html', 'value': html})
        return items
    # fallback
    return [{'render': 'html', 'value': str(widget)}]


def widgets_to_flow(widgets):
    flow = []
    for w in widgets or []:
        if isinstance(w, dict):
            flow.extend(widget_to_flow_items(w))
    return flow


def build_steps(explanations):
    steps = []
    step_id = 1
    for exp in explanations or []:
        if not isinstance(exp, dict):
            continue
        etype = exp.get('type')
        if etype == 'text':
            flow = widgets_to_flow(exp.get('widgets'))
            if flow:
                steps.append({
                    'stepId': step_id,
                    'title': 'Explanation',
                    'flow': flow
                })
                step_id += 1
        elif etype == 'step_by_step':
            for inner in exp.get('explanations') or []:
                if not isinstance(inner, dict):
                    continue
                flow = widgets_to_flow(inner.get('widgets'))
                if flow:
                    steps.append({
                        'stepId': step_id,
                        'title': f'Step {step_id}',
                        'flow': flow
                    })
                    step_id += 1
    return steps


def link_label(url: str):
    if not url:
        return None
    host = re.sub(r'^https?://', '', url).split('/')[0]
    if host in YOUTUBE_HOSTS:
        return 'Video'
    return 'reference'


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # First, collect ALL data from ALL HAR files and group by canonical URL
    # This prevents data from being overwritten when the same book appears in multiple HAR files
    canonical_data = {}  # canon -> (parsed, obj, qas)

    print("Step 1: Collecting data from HAR files...")
    # Only process TARGET_FILE if specified, otherwise all .har files
    if TARGET_FILE:
        har_files = [SOURCE_DIR / TARGET_FILE]
    else:
        # Recursively find all .har files in subdirectories
        har_files = list(SOURCE_DIR.rglob('*.har'))

    for p in har_files:
        print(f"  Processing {p.name}...")
        with p.open('r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception:
                print(f"    ⚠️  Failed to parse JSON")
                continue

        count = 0
        for e in data.get('log', {}).get('entries', []):
            text = e.get('response', {}).get('content', {}).get('text')
            if not text:
                continue
            t = text.strip()
            if not t.startswith('{'):
                continue
            try:
                obj = json.loads(t)
            except Exception:
                continue
            canon = obj.get('canonicalUrl')
            parsed = parse_canonical(canon)
            if not parsed:
                continue

            # Process all books
            book_slug = parsed['book']

            qas = obj.get('questionsAndSolutions') or []
            if not qas:
                continue

            # Store by canonical URL to avoid duplicates
            if canon not in canonical_data:
                canonical_data[canon] = (parsed, obj, qas, canon)
                count += 1

        print(f"    ✓ Extracted {count} valid book problems")

    print(f"\nTotal unique problems collected: {len(canonical_data)}")

    # Convert to list and group by book
    pages = list(canonical_data.values())
    by_book = defaultdict(list)
    for parsed, obj, qas, canon in pages:
        by_book[parsed['book']].append((parsed, obj, qas, canon))

    print(f"Total valid books found: {len(by_book)}\n")

    # Sort books by slug for consistent processing order
    sorted_books = sorted(by_book.items())

    # Global problem ID counter (start from configured value)
    global_problem_id = START_PROBLEM_ID

    print("Step 2: Processing valid books...")
    for book_slug, items in sorted_books:
        print(f"\n  Processing: {book_slug}")
        # dedupe by canonicalUrl
        seen = set()
        deduped = []
        for parsed, obj, qas, canon in items:
            if canon in seen:
                continue
            seen.add(canon)
            deduped.append((parsed, obj, qas, canon))
        items = deduped

        # Sort by original ID from URL (the true sequential order)
        items.sort(key=lambda x: int(x[0]['origid']))
        print(f"    ✓ {len(items)} problems after dedup and sort")

        # assign new page ids with global numbering
        page_id_map = {}
        problem_id_map = {}
        for parsed, obj, qas, canon in items:
            ch = parsed['chapter']
            prob = parsed['problem']
            origid = parsed['origid']

            # New pageId format: {global_id}-ch-{chapter}-problem-{problem}
            new_page_id = f"{global_problem_id}-ch-{ch.lower()}-problem-{prob}"
            page_id_map[(ch, prob, origid)] = new_page_id
            problem_id_map[(ch, prob, origid)] = str(global_problem_id)
            global_problem_id += 1

        # build catalog
        chapter_map = OrderedDict()
        for parsed, obj, qas, canon in items:
            ch = parsed['chapter']
            prob = parsed['problem']
            origid = parsed['origid']
            chapter_key = ch

            if chapter_key not in chapter_map:
                chapter_map[chapter_key] = {
                    'nodeId': f'ch-{ch.lower()}',
                    'label': f'Chapter {ch}',
                    'exercises': []
                }

            new_page_id = page_id_map[(ch, prob, origid)]
            chapter_map[chapter_key]['exercises'].append({
                'pageId': new_page_id,
                'label': f'Exercise {prob}'
            })

        catalog = {
            'bookSlug': book_slug,
            'bookTitle': slug_to_title(book_slug),
            'bookIsbn': slug_to_isbn(book_slug),
            'bookEdition': slug_to_edition(book_slug),
            'chapters': list(chapter_map.values()),
            'coverImage': {
                'type': 'image',
                'path': ''
            }
        }

        # write book folder
        book_dir = OUT_DIR / book_slug
        (book_dir / 'answers').mkdir(parents=True, exist_ok=True)
        with (book_dir / 'catalog.json').open('w', encoding='utf-8') as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)

        # build answers pages
        for idx, (parsed, obj, qas, canon) in enumerate(items):
            ch = parsed['chapter']
            prob = parsed['problem']
            origid = parsed['origid']
            new_page_id = page_id_map[(ch, prob, origid)]
            new_problem_id = problem_id_map[(ch, prob, origid)]

            # nav
            prev_id = None
            next_id = None
            if idx > 0:
                p_prev = items[idx-1][0]
                prev_id = page_id_map[(p_prev['chapter'], p_prev['problem'], p_prev['origid'])]
            if idx < len(items)-1:
                p_next = items[idx+1][0]
                next_id = page_id_map[(p_next['chapter'], p_next['problem'], p_next['origid'])]

            # AnswerContent array
            answer_content = []
            debug_info = []
            for cidx, qa in enumerate(qas, start=1):
                sol = qa.get('solution') or {}
                sc = sol.get('solutionContent') or {}
                answers = sc.get('answers') or []

                parts = []
                for ans in answers:
                    # result from answer.widgets
                    result_flow = widgets_to_flow(ans.get('widgets'))
                    result_block = {
                        'title': 'The Answer',
                        'flow': result_flow
                    }

                    # steps from answer.explanations
                    steps = build_steps(ans.get('explanations'))

                    part = {
                        'result': [result_block],
                        'steps': steps
                    }
                    if 'answerIdentifier' in ans:
                        part['optionCharacter'] = ans.get('answerIdentifier')
                    if 'isCorrect' in ans:
                        part['isRight'] = ans.get('isCorrect')
                    if 'groupName' in ans:
                        part['groupTitle'] = ans.get('groupName')
                    if 'options' in ans:
                        part['groupContents'] = ans.get('options')
                    if 'attachments' in ans:
                        part['file_attached'] = ans.get('attachments')

                    parts.append(part)

                links = []
                ext = sc.get('externalLink')
                if ext:
                    links.append({'label': link_label(ext), 'url': ext})

                answer_content.append({
                    'solution': {
                        'contentId': cidx,
                        'type': sc.get('type'),
                        'parts': parts,
                        'links': links
                    },
                    'tips': sc.get('hints') or [],
                    'meta': {
                        'solutionId': sol.get('solutionId'),
                        'sourceType': sol.get('sourceType'),
                        'sourceId': sol.get('sourceId'),
                        'userId': sol.get('userId'),
                        'version': sol.get('version'),
                        'authoredDate': sol.get('authoredDate')
                    }
                })

                debug_info.append({
                    'canonical': obj.get('canonicalUrl'),
                    'questionId': qa.get('questionId'),
                    'pageId': f"ch-{ch.lower()}-problem-{prob}-{origid}"
                })

            # top-level page
            is_thin = obj.get('isThinContent')
            page = {
                'AnswerContent': answer_content,
                'nav': {'prevId': prev_id, 'nextId': next_id},
                'pageId': new_page_id,
                'bookSlug': book_slug,
                'chapterTag': ch,
                'problemNo': prob,
                'problemId': new_problem_id,
                'debugInfo': debug_info,
                'isRich': (not is_thin) if is_thin is not None else True,
                'noIndex': obj.get('noindex') if obj.get('noindex') is not None else False
            }

            out_path = book_dir / 'answers' / f'{new_page_id}.json'
            with out_path.open('w', encoding='utf-8') as f:
                json.dump(page, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Complete! Processed {global_problem_id - 1} total problems from {len(by_book)} valid books")


if __name__ == '__main__':
    main()
