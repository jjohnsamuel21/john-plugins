#!/usr/bin/env python3
"""Blueprint approval gate and document status report.

Reads the YAML-style header at the top of each Blueprint document and reports
status, version, and staleness. Standard library only; works on Python 3.8+
on Windows, macOS, and Linux. Output is plain ASCII.

Usage:
  python check_approved.py                       gate check on docs/
  python check_approved.py --docs path\\to\\docs   use another docs folder
  python check_approved.py --require prd,ux      gate only on these documents
  python check_approved.py --file docs\\features\\x.md   gate on one document
  python check_approved.py --all --json          full status of every document, as JSON

Exit codes: 0 gate passed, 1 gate failed, 2 usage error.
"""
import argparse
import glob
import json
import os
import re
import sys

# Dependency order. A document is built on the ones before it.
FLOW = ["prd", "ux", "hld", "lld", "testplan"]
EXTRA = ["discovery", "tasks", "codebase-map"]
VALID_STATUS = ("draft", "in-review", "approved", "ready")


def read_header(path):
    """Return the header of a document as a dict, or None if it has none."""
    try:
        with open(path, encoding="utf-8-sig") as handle:
            lines = handle.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    if not lines or lines[0].strip() != "---":
        return None
    header = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return header
        match = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if match:
            value = re.sub(r"\s+#.*$", "", match.group(2)).strip()
            header[match.group(1)] = value
    return None  # header never closed


def parse_based_on(value):
    """'[prd@0.3, ux@0.1]' -> {'prd': '0.3', 'ux': '0.1'}"""
    result = {}
    for name, version in re.findall(r"([a-z][a-z0-9-]*)@([\w.\-]+)", value or ""):
        result[name] = version
    return result


def load_document(name, path):
    info = {
        "name": name,
        "path": path.replace("\\", "/"),
        "exists": os.path.isfile(path),
        "status": None,
        "version": None,
        "updated": None,
        "based_on": {},
        "problems": [],
    }
    if not info["exists"]:
        return info
    header = read_header(path)
    if header is None:
        info["problems"].append("no valid header (the file must start with a --- block)")
        return info
    status = header.get("status", "").lower()
    info["status"] = status or None
    info["version"] = header.get("version") or None
    info["updated"] = header.get("updated") or None
    info["based_on"] = parse_based_on(header.get("based_on", ""))
    if status not in VALID_STATUS:
        info["problems"].append("status is '%s', expected draft, in-review, or approved" % status)
    if not info["version"]:
        info["problems"].append("header has no version")
    return info


def add_staleness(documents):
    """Flag documents built on an older version of an upstream document."""
    by_name = {doc["name"]: doc for doc in documents}
    for doc in documents:
        if not doc["exists"]:
            continue
        for upstream, version in doc["based_on"].items():
            other = by_name.get(upstream)
            if other is None or not other["exists"]:
                doc["problems"].append("built on %s@%s but %s is missing" % (upstream, version, upstream))
            elif other["version"] != version:
                doc["problems"].append(
                    "STALE: built on %s@%s but %s is now %s" % (upstream, version, upstream, other["version"])
                )
            elif (doc["status"] == "approved" and other["name"] in FLOW
                  and other["status"] != "approved"):
                doc["problems"].append("approved, but upstream %s is %s" % (upstream, other["status"]))


def gate_problems(documents, required):
    problems = []
    for doc in documents:
        if doc["name"] not in required:
            continue
        if not doc["exists"]:
            problems.append("%s: document is missing" % doc["name"])
            continue
        if doc["status"] != "approved":
            problems.append("%s: status is %s, not approved" % (doc["name"], doc["status"]))
        for text in doc["problems"]:
            problems.append("%s: %s" % (doc["name"], text))
    return problems


def print_table(documents, title):
    print(title)
    print("  %-14s %-10s %-8s %s" % ("document", "status", "version", "notes"))
    for doc in documents:
        if not doc["exists"]:
            print("  %-14s %-10s %-8s %s" % (doc["name"], "-", "-", "missing"))
            continue
        notes = "; ".join(doc["problems"])
        print("  %-14s %-10s %-8s %s" % (doc["name"], doc["status"] or "?", doc["version"] or "?", notes))


def main():
    parser = argparse.ArgumentParser(description="Blueprint approval gate and document status report.")
    parser.add_argument("--docs", default="docs", help="docs folder (default: docs)")
    parser.add_argument("--require", default=",".join(FLOW),
                        help="comma-separated documents the gate requires (default: %s)" % ",".join(FLOW))
    parser.add_argument("--file", help="gate on a single document, for example a lite feature file")
    parser.add_argument("--all", action="store_true",
                        help="also report discovery, tasks, codebase-map, and docs/features/*.md (informational)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    args = parser.parse_args()

    # Single-file mode (lite features).
    if args.file:
        name = os.path.splitext(os.path.basename(args.file))[0]
        doc = load_document(name, args.file)
        problems = []
        if not doc["exists"]:
            problems.append("%s: file not found" % args.file)
        else:
            if doc["status"] != "approved":
                problems.append("%s: status is %s, not approved" % (name, doc["status"]))
            problems.extend("%s: %s" % (name, text) for text in doc["problems"])
        result = {"gate": "fail" if problems else "pass", "documents": [doc], "problems": problems}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_table([doc], "Blueprint gate for %s" % args.file)
            print("GATE PASSED" if not problems else "GATE FAILED: %d problem(s)" % len(problems))
        return 1 if problems else 0

    required = [item.strip() for item in args.require.split(",") if item.strip()]
    unknown = [item for item in required if item not in FLOW + EXTRA]
    if unknown:
        parser.error("unknown document name(s): %s" % ", ".join(unknown))

    # Always load every known document so staleness can be checked against
    # upstream documents; only show the gated ones unless --all is given.
    documents = [load_document(name, os.path.join(args.docs, name + ".md")) for name in FLOW + EXTRA]
    add_staleness(documents)
    shown = [doc for doc in documents if args.all or doc["name"] in FLOW]
    if args.all:
        for path in sorted(glob.glob(os.path.join(args.docs, "features", "*.md"))):
            shown.append(load_document("feature:" + os.path.splitext(os.path.basename(path))[0], path))

    problems = []
    if not os.path.isdir(args.docs):
        problems.append("docs folder '%s' not found" % args.docs)
    problems.extend(gate_problems(documents, required))
    result = {"gate": "fail" if problems else "pass", "documents": shown, "problems": problems}

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_table(shown, "Blueprint gate: %s (requires: %s)" % (args.docs, ", ".join(required)))
        print("GATE PASSED" if not problems else "GATE FAILED: %d problem(s)" % len(problems))
        for text in problems:
            print("  - " + text)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
