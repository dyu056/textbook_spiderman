#!/usr/bin/env python3
"""
Inspect HAR files and print a concise summary of entries.

Usage:
  python har_inspect.py path/to/file.har
  python har_inspect.py path/to/dir --limit 20 --show-headers
"""
from __future__ import annotations

import argparse
import base64
import html
import re
import json
import os
from typing import Any, Dict, Iterable, List, Tuple


def iter_har_files(path: str) -> Iterable[str]:
    if os.path.isdir(path):
        for name in sorted(os.listdir(path)):
            if name.lower().endswith(".har"):
                yield os.path.join(path, name)
    else:
        yield path


def load_har(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_get(d: Dict[str, Any], key: str, default: Any = "") -> Any:
    return d.get(key, default)


def summarize_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    req = safe_get(entry, "request", {})
    resp = safe_get(entry, "response", {})
    timings = safe_get(entry, "timings", {})
    content = safe_get(resp, "content", {})

    method = safe_get(req, "method", "")
    url = safe_get(req, "url", "")
    status = safe_get(resp, "status", "")
    status_text = safe_get(resp, "statusText", "")
    mime = safe_get(content, "mimeType", "")
    size = safe_get(resp, "bodySize", "")
    t_wait = safe_get(timings, "wait", "")
    t_receive = safe_get(timings, "receive", "")

    return {
        "method": method,
        "url": url,
        "status": status,
        "statusText": status_text,
        "mime": mime,
        "bodySize": size,
        "wait_ms": t_wait,
        "receive_ms": t_receive,
        "requestHeaders": safe_get(req, "headers", []),
        "responseHeaders": safe_get(resp, "headers", []),
    }


def format_headers(headers: List[Dict[str, Any]], limit: int) -> List[str]:
    lines = []
    for h in headers[:limit]:
        name = safe_get(h, "name", "")
        value = safe_get(h, "value", "")
        lines.append(f"{name}: {value}")
    if len(headers) > limit:
        lines.append(f"... ({len(headers) - limit} more)")
    return lines


def decode_content_text(content: Dict[str, Any]) -> Tuple[str, str]:
    text = safe_get(content, "text", "")
    encoding = safe_get(content, "encoding", "")
    if not text:
        return "", encoding
    if encoding == "base64":
        try:
            raw = base64.b64decode(text)
            return raw.decode("utf-8", errors="replace"), encoding
        except Exception:
            return "", encoding
    return text, encoding


def truncate_text(text: str, limit: int) -> str:
    if limit <= 0 or len(text) <= limit:
        return text
    return text[:limit] + "... [truncated]"


def html_to_text(value: str) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = value.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    value = value.replace("</li>", "\n").replace("<li>", "- ")
    value = re.sub(r"<[^>]+>", "", value)
    return value.strip()


def extract_widget_texts(widgets: List[Dict[str, Any]]) -> List[str]:
    texts: List[str] = []
    for w in widgets:
        text = safe_get(w, "text", "")
        if text:
            texts.append(text)
    return texts


def extract_explanations(explanations: List[Dict[str, Any]]) -> List[str]:
    items: List[str] = []
    for exp in explanations:
        widgets = safe_get(exp, "widgets", [])
        if isinstance(widgets, list):
            items.extend(extract_widget_texts(widgets))
        nested = safe_get(exp, "explanations", [])
        if isinstance(nested, list):
            items.extend(extract_explanations(nested))
    return items


def parse_solution_title(canonical_url: str, source_id: str) -> str:
    if canonical_url:
        m = re.search(r"/Chapter-(\\d+)-Problem-(\\d+)-(\\d+)/", canonical_url)
        if m:
            chapter, problem, exercise_id = m.groups()
            return f"Chapter {chapter}, Problem {problem} (exercise {exercise_id}) sourceId={source_id}"
    if source_id:
        return f"sourceId={source_id}"
    return "unknown"


def extract_solutions(
    entries: List[Dict[str, Any]],
    strip_html: bool,
    solution_limit: int,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for entry in entries:
        content = safe_get(entry.get("response", {}), "content", {})
        body_text, _encoding = decode_content_text(content)
        if not body_text or "questionsAndSolutions" not in body_text:
            continue
        try:
            payload = json.loads(body_text)
        except json.JSONDecodeError:
            continue
        qs = payload.get("questionsAndSolutions", [])
        canonical_url = payload.get("canonicalUrl", "")
        if not isinstance(qs, list):
            continue
        for item in qs:
            solution = safe_get(item, "solution", {})
            solution_content = safe_get(solution, "solutionContent", {})
            hints = safe_get(solution_content, "hints", [])
            answers = safe_get(solution_content, "answers", [])
            explanations = []
            if isinstance(answers, list):
                for ans in answers:
                    exp = safe_get(ans, "explanations", [])
                    if isinstance(exp, list):
                        explanations.extend(extract_explanations(exp))
            verified = []
            if isinstance(answers, list):
                for ans in answers:
                    if ans.get("isSampleResponse") is True:
                        continue
                    widgets = safe_get(ans, "widgets", [])
                    if isinstance(widgets, list):
                        verified.extend(extract_widget_texts(widgets))
            item_out = {
                "title": parse_solution_title(canonical_url, safe_get(solution, "sourceId", "")),
                "tip": hints,
                "explanation": explanations,
                "verified_answer": verified,
                "canonical_url": canonical_url,
            }
            if strip_html:
                item_out["tip"] = [html_to_text(t) for t in item_out["tip"]]
                item_out["explanation"] = [html_to_text(t) for t in item_out["explanation"]]
                item_out["verified_answer"] = [
                    html_to_text(t) for t in item_out["verified_answer"]
                ]
            results.append(item_out)
            if solution_limit and len(results) >= solution_limit:
                return results
    return results


def print_summary(
    path: str,
    entries: List[Dict[str, Any]],
    limit: int,
    show_headers: bool,
    header_limit: int,
    show_body: bool,
    body_limit: int,
) -> None:
    print(f"\n== {os.path.basename(path)} ==")
    print(f"entries: {len(entries)}")
    for i, entry in enumerate(entries[:limit], start=1):
        s = summarize_entry(entry)
        status = f"{s['status']} {s['statusText']}".strip()
        size = s["bodySize"]
        wait_ms = s["wait_ms"]
        recv_ms = s["receive_ms"]
        print(f"{i:>3}. {s['method']} {s['url']}")
        print(f"     -> {status} | {s['mime']} | size={size} | wait={wait_ms}ms recv={recv_ms}ms")
        if show_headers:
            req_headers = format_headers(s["requestHeaders"], header_limit)
            resp_headers = format_headers(s["responseHeaders"], header_limit)
            if req_headers:
                print("     request headers:")
                for line in req_headers:
                    print(f"       {line}")
            if resp_headers:
                print("     response headers:")
                for line in resp_headers:
                    print(f"       {line}")
        if show_body:
            content = safe_get(entry.get("response", {}), "content", {})
            body_text, encoding = decode_content_text(content)
            if body_text:
                preview = truncate_text(body_text, body_limit)
                enc_note = f" (encoding={encoding})" if encoding else ""
                print(f"     response body{enc_note}:")
                for line in preview.splitlines()[:50]:
                    print(f"       {line}")
            else:
                print("     response body: <empty or unavailable>")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect HAR files.")
    parser.add_argument("path", help="HAR file or directory containing HAR files.")
    parser.add_argument("--limit", type=int, default=20, help="Max entries to show per HAR.")
    parser.add_argument(
        "--show-headers",
        action="store_true",
        help="Show request/response headers for each entry.",
    )
    parser.add_argument("--header-limit", type=int, default=10, help="Max headers to show.")
    parser.add_argument(
        "--show-body",
        action="store_true",
        help="Show response body text if present.",
    )
    parser.add_argument(
        "--body-limit",
        type=int,
        default=2000,
        help="Max characters of body text to show per entry.",
    )
    parser.add_argument(
        "--extract-solutions",
        action="store_true",
        help="Extract tips/explanations/verified answers from solution payloads.",
    )
    parser.add_argument(
        "--strip-html",
        action="store_true",
        help="Strip HTML tags from extracted text.",
    )
    parser.add_argument(
        "--solution-limit",
        type=int,
        default=0,
        help="Max solutions to show per HAR (0 = no limit).",
    )
    args = parser.parse_args()

    for har_path in iter_har_files(args.path):
        data = load_har(har_path)
        log = data.get("log", {})
        entries = log.get("entries", [])
        if not isinstance(entries, list):
            entries = []
        if args.extract_solutions:
            print(f"\n== {os.path.basename(har_path)} ==")
            items = extract_solutions(
                entries,
                strip_html=args.strip_html,
                solution_limit=max(0, args.solution_limit),
            )
            for i, item in enumerate(items, start=1):
                print(f"{i:>3}. {item['title']}")
                print(f"     url: {item['canonical_url']}")
                if item["tip"]:
                    print("     here is a tip:")
                    for t in item["tip"]:
                        for line in t.splitlines():
                            print(f"       {line}")
                if item["explanation"]:
                    print("     explanation:")
                    for t in item["explanation"]:
                        for line in t.splitlines():
                            print(f"       {line}")
                if item["verified_answer"]:
                    print("     verified answer:")
                    for t in item["verified_answer"]:
                        for line in t.splitlines():
                            print(f"       {line}")
            if not items:
                print("     <no solution payloads found>")
        else:
            print_summary(
                har_path,
                entries,
                limit=max(0, args.limit),
                show_headers=args.show_headers,
                header_limit=max(0, args.header_limit),
                show_body=args.show_body,
                body_limit=max(0, args.body_limit),
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
