#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

# Count question types in Math HAR files.
# We count per questionsAndSolutions entry using solutionContent.type.

def iter_responses():
    for p in Path('spider_data/Math').glob('*.har'):
        with p.open('r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception:
                continue
        entries = data.get('log', {}).get('entries', [])
        for e in entries:
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
            if 'questionsAndSolutions' in obj:
                yield obj


def main():
    counter = Counter()
    total = 0

    for obj in iter_responses():
        qas = obj.get('questionsAndSolutions') or []
        for qa in qas:
            sol = qa.get('solution') or {}
            sc = sol.get('solutionContent') or {}
            qtype = sc.get('type')
            if qtype:
                counter[qtype] += 1
                total += 1

    if total == 0:
        print('No questions found.')
        return

    # Output sorted by count desc
    print('type\tcount\tpercent')
    for qtype, count in counter.most_common():
        pct = count / total * 100
        print(f'{qtype}\t{count}\t{pct:.2f}%')
    print(f'TOTAL\t{total}\t100.00%')


if __name__ == '__main__':
    main()
