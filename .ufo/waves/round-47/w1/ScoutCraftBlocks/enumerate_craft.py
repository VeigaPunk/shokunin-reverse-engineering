#!/usr/bin/env python3
"""Enumerate ## Queue-drain craft rule blocks at the round-47 freeze.

Scout resolver (written here, not imported from exact.py / record.py):

A citation is a repo-relative path token, optional line selector, found in
the block text. Prefixes: corpus/, plans/, tools/, .ufo/, or a root file
SCORECARD.md, LOG.md, PROVINCE.md, SKILL.md. A selector is :N or :N-M with
hyphen or en/em dash. The path is stripped of a trailing sentence dot.

Resolves at REV when git cat-file -t REV:path is 'blob' and, if a selector
is present, 1 <= start <= end <= len(splitlines()). No selector + blob
exists counts as resolved, and is flagged no_line_selector. A block with
zero citations is vacuous, not a pass.

Command-A comparison (record.py depth_pair rule, duplicated here so this
file does not import the frozen counter): a block is command-A-resolved
iff HARD_REF finds at least one corpus|plans|tools path and every such
ref's range (defaulting a missing selector to line 1) falls inside the blob.
Paths outside that prefix are invisible to command A.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "5017e1f7299c3a812e87e7950148f54313dd279e"
S = Path("/fast/scratch/hyaku/kaidoku-r47/ScoutCraftBlocks")
CRAFT = "## Queue-drain craft "
MARKER_V3 = "<!-- exactness-table v3 -->"
HARD_REF = re.compile(
    r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?"
)
CITE_RE = re.compile(
    r"(?P<path>(?:\.ufo/|(?:corpus|plans|tools)/)[A-Za-z0-9._/-]+"
    r"|(?:SCORECARD|LOG|PROVINCE|SKILL)\.md)"
    r"(?::(?P<start>\d+)(?P<dash>[-–—])(?P<end>\d+)|:(?P<only>\d+))?"
)
HTML_COMMENT = re.compile(r"<!--(.*?)-->", re.S)
INDENTED_BOLD = re.compile(r"(?m)^[ \t]+- \*\*")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Git:
    def __init__(self) -> None:
        self.receipts = []

    def run(self, args: list[str], label: str) -> subprocess.CompletedProcess:
        cmd = ["git", "-C", ROOT, *args]
        started = utc_now()
        proc = subprocess.run(cmd, capture_output=True)
        rec = {
            "label": label,
            "command": " ".join(cmd),
            "exit": proc.returncode,
            "stdout_sha256": sha256(proc.stdout),
            "stderr_sha256": sha256(proc.stderr),
            "stdout_bytes": len(proc.stdout),
            "stderr_bytes": len(proc.stderr),
            "utc": started,
        }
        if proc.stderr and proc.returncode != 0:
            rec["stderr_prefix"] = proc.stderr[:400].decode("utf-8", "replace")
        self.receipts.append(rec)
        return proc


GIT = Git()
BLOB_CACHE: dict[str, dict] = {}


def git_bytes(spec: str) -> tuple[int, bytes, bytes]:
    proc = GIT.run(["cat-file", "blob", spec], f"cat-file blob {spec}")
    return proc.returncode, proc.stdout, proc.stderr


def blob_info(path: str) -> dict:
    if path in BLOB_CACHE:
        return BLOB_CACHE[path]
    spec = f"{REV}:{path}"
    kind = GIT.run(["cat-file", "-t", spec], f"cat-file -t {path}")
    k = kind.stdout.decode().strip() if kind.returncode == 0 else None
    info = {"path": path, "type": k, "exists": kind.returncode == 0, "lines": None}
    if k == "blob":
        rc, raw, _ = git_bytes(spec)
        info["bytes"] = len(raw)
        info["sha256"] = sha256(raw)
        info["lines"] = len(raw.decode("utf-8", "replace").splitlines()) if rc == 0 else None
    BLOB_CACHE[path] = info
    return info


def craft_section(skill: str) -> str:
    if CRAFT not in skill:
        raise SystemExit("no craft heading with trailing space")
    return skill.split(CRAFT, 1)[1].split("\n## ", 1)[0]


def blocks_of(skill: str) -> list[str]:
    return re.split(r"(?m)^- \*\*", craft_section(skill))[1:]


def line_of(skill: str, idx: int) -> int:
    return skill.count("\n", 0, idx) + 1


def normalize_path(path: str) -> str:
    return path.rstrip(".")


def scout_cites(text: str) -> list[dict]:
    out = []
    for m in CITE_RE.finditer(text):
        raw_path = m.group("path")
        path = normalize_path(raw_path)
        if path != raw_path:
            # trailing sentence dot belonged to prose, not the path
            pass
        start = m.group("start") or m.group("only")
        end = m.group("end") or m.group("only")
        dash = m.group("dash")
        ctx_lo = max(0, m.start() - 30)
        ctx = text[ctx_lo:m.end() + 20].replace("\n", " ")
        item = {
            "raw": text[m.start():m.end()],
            "path": path,
            "stripped_dot": path != raw_path.rstrip("\n"),
            "start": int(start) if start else None,
            "end": int(end) if end else None,
            "dash": dash,
            "context": ctx,
        }
        info = blob_info(path)
        if not info["exists"]:
            item["status"] = "unresolved"
            item["reason"] = "absent"
        elif info["type"] == "tree" and start is None:
            item["status"] = "resolved"
            item["reason"] = "tree_no_selector"
            show = show_text(path)
            item["show_lines"] = None if show is None else len(show.splitlines())
            item["show_exit"] = 0 if show is not None else 1
        elif info["type"] != "blob":
            item["status"] = "unresolved"
            item["reason"] = f"type {info['type']}"
        elif start is None:
            item["status"] = "resolved"
            item["reason"] = "no_line_selector"
            item["file_lines"] = info["lines"]
        else:
            a, b = int(start), int(end)
            n = info["lines"]
            item["file_lines"] = n
            if dash and dash != "-":
                item["dash_note"] = "non-hyphen range separator"
            if not (1 <= a <= b <= n):
                item["status"] = "unresolved"
                item["reason"] = f"range {a}-{b} outside 1..{n}"
            else:
                item["status"] = "resolved"
                item["reason"] = "in_range"
        out.append(item)
    return out


SHOW_CACHE: dict[str, str | None] = {}


def show_text(path: str) -> str | None:
    """gate.show semantics: git show REV:path stdout, or None when exit != 0."""
    if path in SHOW_CACHE:
        return SHOW_CACHE[path]
    proc = GIT.run(["show", f"{REV}:{path}"], f"show {path}")
    text = proc.stdout.decode("utf-8", "replace") if proc.returncode == 0 else None
    SHOW_CACHE[path] = text
    return text


def command_a(block: str) -> dict:
    """record.py depth_pair, via git show rather than cat-file -t.

    A missing selector defaults to line 1. git show of a tree exits 0 and
    prints a listing, so a directory citation with no selector passes when
    that listing has at least one line.
    """
    refs = []
    for name, first, last in HARD_REF.findall(block):
        text = show_text(name)
        start = int(first or 1)
        end = int(last or first or 1)
        if text is None:
            ok, reason, n = False, "git show failed", None
        else:
            n = len(text.splitlines())
            if not (1 <= start <= end <= n):
                ok, reason = False, f"range {start}-{end} outside 1..{n}"
            else:
                ok = True
                reason = "in_range" if first else "defaulted_to_line_1"
        refs.append({
            "path": name, "start": start, "end": end,
            "selector": bool(first), "ok": ok, "reason": reason, "show_lines": n,
        })
    if not refs:
        return {"refs": 0, "resolved_block": False, "reason": "no HARD_REF", "failures": []}
    failures = [r for r in refs if not r["ok"]]
    return {
        "refs": len(refs),
        "resolved_block": not failures,
        "reason": "all HARD_REF in range" if not failures else "HARD_REF miss",
        "failures": failures,
    }


def title_of(block: str) -> str:
    end = block.find("**")
    raw = block if end < 0 else block[:end]
    return re.sub(r"\s+", " ", raw).strip()


def analyze(skill: str, label: str) -> dict:
    prefix_count = skill.count(CRAFT)
    malformed_heading = "\n## Queue-drain craft\n" in ("\n" + skill)
    craft_at = skill.find(CRAFT)
    next_rel = skill.find("\n## ", craft_at + len(CRAFT))
    next_heading = None
    next_line = None
    if next_rel >= 0:
        next_heading = skill[next_rel + 1:].split("\n", 1)[0]
        next_line = line_of(skill, next_rel + 1)
    section = craft_section(skill)
    blocks = blocks_of(skill)
    intro = re.split(r"(?m)^- \*\*", section)[0]
    rows = []
    pos = 0
    for i, block in enumerate(blocks, 1):
        first = block.split("\n", 1)[0]
        needle = "- **" + first
        idx = skill.find(needle, pos)
        if idx < 0:
            idx = skill.find(needle)
        pos = idx + len(needle) if idx >= 0 else pos
        title = title_of(block)
        num = re.match(r"(\d+)\.\s+", title)
        markers = [re.sub(r"\s+", " ", c).strip() for c in HTML_COMMENT.findall(block)]
        cites = scout_cites(block)
        unresolved = [c for c in cites if c["status"] != "resolved"]
        if not cites:
            verdict = "vacuous"
        elif unresolved:
            verdict = "no"
        else:
            verdict = "yes"
        rows.append({
            "ordinal": i,
            "line": line_of(skill, idx) if idx >= 0 else None,
            "titled_number": int(num.group(1)) if num else None,
            "title": title,
            "title_closed": end_closed(block),
            "markers": markers,
            "has_v3_marker": MARKER_V3 in block,
            "citation_count": len(cites),
            "unresolved_count": len(unresolved),
            "no_selector_count": sum(1 for c in cites if c["reason"] == "no_line_selector"),
            "all_citations_resolve": verdict,
            "citations": cites,
            "command_a": command_a(block),
        })
    cust_lines = []
    for m in re.finditer(r"(?m)^## Config custody.*$", skill):
        cust_lines.append({"line": line_of(skill, m.start()), "text": m.group(0)})
    return {
        "label": label,
        "craft_prefix_occurrences": prefix_count,
        "craft_heading_line": line_of(skill, craft_at) if craft_at >= 0 else None,
        "craft_heading": skill[craft_at:].split("\n", 1)[0] if craft_at >= 0 else None,
        "next_heading": next_heading,
        "next_heading_line": next_line,
        "config_custody_headings": cust_lines,
        "intro_markers": HTML_COMMENT.findall(intro),
        "intro_citations": len(scout_cites(intro)),
        "indented_bold_items": len(INDENTED_BOLD.findall(section)),
        "v3_marker_occurrences_file": skill.count(MARKER_V3),
        "rule_blocks": len(blocks),
        "blocks": rows,
    }


def end_closed(block: str) -> bool:
    return "**" in block


def simulate(skill: str) -> dict:
    """In-memory only. Shows which existing blocks follow a fake block 24."""
    craft_at = skill.find(CRAFT)
    next_rel = skill.find("\n## ", craft_at + len(CRAFT))
    fake = "\n- **24. Simulated exactness block.** " + MARKER_V3 + "\n"
    appended = skill[:next_rel] + fake + skill[next_rel:]
    app_blocks = blocks_of(appended)
    last = app_blocks[-1]
    # insert immediately before the current last bold item
    section_start_in_skill = craft_at + len(CRAFT)
    # find last '- **' in the original craft section
    section = craft_section(skill)
    last_rel = None
    for m in re.finditer(r"(?m)^- \*\*", section):
        last_rel = m.start()
    insert_at = section_start_in_skill + last_rel
    inserted = skill[:insert_at] + fake + skill[insert_at:]
    ins_blocks = blocks_of(inserted)
    marked = [i for i, b in enumerate(ins_blocks) if MARKER_V3 in b]

    def followers(blocks, marked_indexes):
        if len(marked_indexes) != 1:
            return {"marked_indexes": marked_indexes}
        mi = marked_indexes[0]
        return {
            "marked_index_ordinal": mi + 1,
            "block_is_last": mi == len(blocks) - 1,
            "followers": [
                {"ordinal": i + 1, "title": title_of(b)[:120]}
                for i, b in enumerate(blocks) if i > mi
            ],
        }

    app_marked = [i for i, b in enumerate(app_blocks) if MARKER_V3 in b]
    return {
        "append_before_next_heading": followers(app_blocks, app_marked),
        "insert_before_current_last": followers(ins_blocks, marked),
        "append_last_title": title_of(last)[:160],
        "append_rule_blocks": len(app_blocks),
    }


def main() -> int:
    top = GIT.run(["rev-parse", "--show-toplevel"], "toplevel")
    top_s = top.stdout.decode().strip()
    if top.returncode != 0 or top_s != ROOT:
        print(json.dumps({"error": "toplevel", "got": top_s, "exit": top.returncode}))
        return 2
    ident = GIT.run(["rev-parse", f"{REV}:SKILL.md"], "skill blob")
    raw_rc, raw, _ = git_bytes(f"{REV}:SKILL.md")
    if raw_rc != 0:
        print("cat-file skill failed")
        return 2
    skill = raw.decode("utf-8")
    freeze = analyze(skill, "freeze")
    sims = simulate(skill)
    wt_path = Path(ROOT) / "SKILL.md"
    wt_raw = wt_path.read_bytes()
    work = analyze(wt_raw.decode("utf-8"), "worktree")
    status = GIT.run(["status", "--porcelain", "--", "SKILL.md"], "status SKILL.md")
    diff_stat = GIT.run(
        ["diff", "--stat", REV, "HEAD", "--", "SKILL.md"],
        "diff stat freeze..HEAD SKILL.md",
    )
    # which freeze blocks are not byte-identical to the same ordinal in the worktree
    drift = []
    fb = blocks_of(skill)
    wb = blocks_of(wt_raw.decode("utf-8"))
    for i, (a, b) in enumerate(zip(fb, wb), 1):
        if a != b:
            drift.append(i)
    if len(fb) != len(wb):
        drift.append(f"count freeze {len(fb)} worktree {len(wb)}")

    payload = {
        "rev": REV,
        "skill_git_blob": ident.stdout.decode().strip(),
        "skill_sha256": sha256(raw),
        "skill_bytes": len(raw),
        "worktree_skill_sha256": sha256(wt_raw),
        "worktree_status": status.stdout.decode(),
        "freeze_to_head_diff_stat": diff_stat.stdout.decode(),
        "ordinals_whose_text_differs_from_worktree": drift,
        "freeze": freeze,
        "simulations": sims,
        "worktree": {
            "rule_blocks": work["rule_blocks"],
            "v3_marker_occurrences_file": work["v3_marker_occurrences_file"],
            "next_heading": work["next_heading"],
            "next_heading_line": work["next_heading_line"],
            "config_custody_headings": work["config_custody_headings"],
            "blocks_tail": [
                {
                    "ordinal": b["ordinal"],
                    "line": b["line"],
                    "titled_number": b["titled_number"],
                    "title": b["title"][:180],
                    "markers": b["markers"],
                    "has_v3_marker": b["has_v3_marker"],
                    "all_citations_resolve": b["all_citations_resolve"],
                    "unresolved": [
                        {"raw": c["raw"], "reason": c["reason"]}
                        for c in b["citations"] if c["status"] != "resolved"
                    ],
                }
                for b in work["blocks"]
            ],
        },
        "git_receipts": GIT.receipts,
    }
    out = S / "blocks.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    print(f"skill_blob {payload['skill_git_blob']} sha256 {payload['skill_sha256']}")
    print(f"rule_blocks {freeze['rule_blocks']} v3_file {freeze['v3_marker_occurrences_file']}")
    print(f"craft_heading L{freeze['craft_heading_line']}: {freeze['craft_heading']}")
    print(f"next_heading L{freeze['next_heading_line']}: {freeze['next_heading']}")
    print(f"config_custody {freeze['config_custody_headings']}")
    print(f"indented_bold {freeze['indented_bold_items']} intro_cites {freeze['intro_citations']}")
    print("--- blocks ---")
    for b in freeze["blocks"]:
        bad = [c["raw"] + " :: " + c["reason"] for c in b["citations"] if c["status"] != "resolved"]
        print(
            f"{b['ordinal']:02d}\tL{b['line']}\ttitled={b['titled_number']}\t"
            f"markers={b['markers'] or '-'}\t"
            f"cites={b['citation_count']}\tunresolved={b['unresolved_count']}\t"
            f"nosel={b['no_selector_count']}\tresolve={b['all_citations_resolve']}\t"
            f"cmdA={b['command_a']['resolved_block']}:{b['command_a']['refs']}\t"
            f"{b['title'][:110]}"
        )
        for item in bad:
            print(f"    UNRESOLVED {item}")
        for c in b["citations"]:
            if c["reason"] in ("no_line_selector", "tree_no_selector") or (c.get("dash") and c["dash"] != "-"):
                print(f"    NOTE {c['raw']} :: {c['reason']} dash={c.get('dash')} show_lines={c.get('show_lines')} file_lines={c.get('file_lines')}")
    yes = sum(1 for b in freeze["blocks"] if b["all_citations_resolve"] == "yes")
    cmd_yes = sum(1 for b in freeze["blocks"] if b["command_a"]["resolved_block"])
    print(f"scout_blocks_all_resolve {yes}/{len(freeze['blocks'])}")
    print(f"command_A_blocks_resolved {cmd_yes}/{len(freeze['blocks'])}")
    print("--- titles ---")
    for b in freeze["blocks"]:
        print(f"{b['ordinal']}\tL{b['line']}\t{b['titled_number']}\t{b['title']}")
    print("--- citations ---")
    for b in freeze["blocks"]:
        for c in b["citations"]:
            print(f"{b['ordinal']}\t{c['status']}\t{c['reason']}\t{c.get('start')}\t{c.get('end')}\t{c.get('file_lines')}\t{c['raw']}")
    print("--- command A failures (even if scout resolved) ---")
    for b in freeze["blocks"]:
        fails = b["command_a"]["failures"]
        if fails or not b["command_a"]["resolved_block"]:
            print(f"  block {b['ordinal']} cmdA {b['command_a']['reason']} fails={fails}")
    print("--- simulations ---")
    print(json.dumps(sims, indent=2))
    print("--- worktree tail ---")
    print(
        f"wt blocks {work['rule_blocks']} v3 {work['v3_marker_occurrences_file']} "
        f"next L{work['next_heading_line']} {work['next_heading']}"
    )
    for b in work["blocks"][-3:]:
        print(f"  {b['ordinal']} L{b['line']} titled={b['titled_number']} v3={b['has_v3_marker']} {b['title'][:100]}")
    print(f"drift {drift}")
    print(f"status {status.stdout.decode()!r} diffstat {diff_stat.stdout.decode()!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
