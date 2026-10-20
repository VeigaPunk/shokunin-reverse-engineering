#!/usr/bin/env python3
"""routed-defects.py — count the six routed round-17 defects still open at a rev.

Reads Git objects at REV only (`git show REV:path`); the working tree is never
consulted, so the result is reproducible for any commit. The six defects are
defined in corpus/lessons/round-17-verifier-spotcheck.md:137-147; closure
criteria live in .ufo/waves/round-18/contract.md section C1 as amended by the
L1 (2026-10-20): each defect carries a `named` check set (the token checks —
naming the routed id/anchor) and a `substance` check set (the claim itself —
anchors, code, retained evidence). A defect is closed only when BOTH sets
pass; tokens alone cannot close it.

Output: {rev, defects: [{id, open, named_open, substance_open, checks:
[{set, name, ok, detail}]}], named_open_count, substance_open_count,
open_count} where open_count counts defects failing either set.

A path absent at REV makes its checks fail (the defect stays open) — exit 2
is reserved for an unresolvable rev or a git failure, never for missing
remediation content. Historical pins use abbreviations (2711674, da64646)
so the fixture repo can satisfy them with tags.

Python 3 stdlib only. Runnable as `python3 -I -B routed-defects.py ...`.
Exit codes: 0 reported, 1 reported with --strict and open_count > 0,
2 could-not-evaluate.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize

_HEX40 = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{40}(?![0-9a-fA-F])")
_HEX64 = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])")
_SUMS_LINE = re.compile(rb"^([0-9a-fA-F]{64}) [ *]predictions/carriers\.tsv\s*$")
_RUNLOG_START = re.compile(r"^== \S+ start\b")
_BACKTICK_PATH = re.compile(r"`([^`]+)`")

KNOWLEDGE = "corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md"
LESSONS18 = "corpus/lessons/round-18.md"
SUMMARY16 = ".ufo/waves/round-18/evidence/validate16/summary.json"
S032_DIGESTS = ".ufo/waves/round-18/evidence/s032-digests.json"
RUNS18 = ".ufo/waves/round-18/runs"
RUNS17 = ".ufo/waves/round-17/runs"
SUMS = ".ufo/waves/round-17/predictions/SHA256SUMS"
CARRIERS_TSV = ".ufo/waves/round-17/predictions/carriers.tsv"
CARRIER_RUN = ".ufo/waves/round-17/tools/carrier-run.py"
RECEIPT_VALIDATE = ".ufo/waves/round-17/tools/receipt-validate.py"
VALIDATE16_REV = "da64646adcb19c1ede7537b799b8c7d283fe43da"
RUNLOG_REV = "da64646"          # abbrev: resolvable in the real lane and fixtures
HIST_SUMS_REV = "2711674"       # rev whose SHA256SUMS must be restored
PRODUCER_REVS = ("271167473d87ef710f07ecdd98caf0ce12091686",
                 "95e34db62f2693c455d7ee4dfef24b8f3ebc007d")
REGISTRY_SCOPED = ("go-route-compare", "receipt-validate", "pins",
                   "go-buildinfo-probe")
PINMAP_ANCHORS = {KNOWLEDGE: "2026-10-20-r17-go-carrier-diagnostics.md:30-32",
                  "SCORECARD.md": "SCORECARD.md:2374"}


class EvalError(Exception):
    """The rev or repo itself could not be evaluated (exit 2)."""


def _git(root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", root, *args],
                          capture_output=True, text=False, timeout=60)


def _resolve_rev(root: str, rev: str) -> str:
    proc = _git(root, "rev-parse", "--verify", f"{rev}^{{commit}}")
    if proc.returncode != 0:
        raise EvalError(f"cannot resolve {rev!r}: "
                        f"{proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout.decode("ascii", "replace").strip()


def _show(root: str, rev: str, path: str) -> bytes | None:
    """Blob bytes at REV:path, or None when the path is absent/unreadable.

    REV is verified before any _show call, so a failure here means the path
    is absent (or a non-blob) at that rev — a failing check, not exit 2.
    """
    proc = _git(root, "show", f"{rev}:{path}")
    if proc.returncode != 0:
        return None
    return proc.stdout


def _exists(root: str, rev: str, path: str) -> bool:
    return _git(root, "cat-file", "-e", f"{rev}:{path}").returncode == 0


def _ls_trees(root: str, rev: str, dirpath: str) -> list[str] | None:
    """Immediate subdirectory names of DIRPATH at REV, or None if absent."""
    proc = _git(root, "ls-tree", f"{rev}:{dirpath}")
    if proc.returncode != 0:
        return None
    names = []
    for line in proc.stdout.decode("utf-8", "replace").splitlines():
        meta, _, name = line.partition("\t")
        parts = meta.split()
        if len(parts) >= 2 and parts[1] == "tree":
            names.append(name)
    return names


def _is_ancestor(root: str, sha: str, rev: str) -> bool:
    """True iff SHA is a commit ancestor of REV. An absent object fails —
    ancestry cannot be verified, so the substance check stays open."""
    return _git(root, "merge-base", "--is-ancestor",
              sha, rev).returncode == 0


def _text(blob: bytes | None) -> str | None:
    if blob is None:
        return None
    return blob.decode("utf-8", "replace")


def _check(check_set: str, name: str, ok: bool, detail: str) -> dict:
    return {"set": check_set, "name": name, "ok": bool(ok), "detail": detail}


def _line_with(text: str | None, path: str,
               *needles: str) -> tuple[bool, str]:
    if text is None:
        return False, f"{path} absent at rev"
    for line in text.splitlines():
        if all(n in line for n in needles):
            return True, line.strip()[:200]
    return False, f"{path}: no line containing {' + '.join(repr(n) for n in needles)}"


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _section_lines(text: str, heading: str) -> list[str]:
    """Lines of the `## <heading>` section up to the next `## ` heading."""
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            if inside:
                break
            inside = line[3:].strip() == heading
            continue
        if inside:
            out.append(line)
    return out


def _code_text(src: str) -> str | None:
    """Python source minus comments and statement-leading (docstring) strings.

    A STRING token is dropped when it starts a statement (previous kept token
    was NEWLINE/INDENT/DEDENT/`;` or start-of-file); NL/COMMENT tokens are
    ignored. Returns None when the source cannot be tokenized.
    """
    parts = []
    boundary = True
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            t, s = tok.type, tok.string
            if t in (tokenize.COMMENT, tokenize.NL, tokenize.ENCODING,
                     tokenize.ENDMARKER):
                continue
            if t == tokenize.STRING and boundary:
                boundary = False
                continue
            parts.append(s)
            boundary = (t in (tokenize.NEWLINE, tokenize.INDENT,
                              tokenize.DEDENT)
                        or (t == tokenize.OP and s == ";"))
        return " ".join(parts)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return None


def _defect(defect_id: str, checks: list[dict]) -> dict:
    named_open = any(c["set"] == "named" and not c["ok"] for c in checks)
    substance_open = any(c["set"] == "substance" and not c["ok"]
                         for c in checks)
    return {"id": defect_id,
            "open": named_open or substance_open,
            "named_open": named_open,
            "substance_open": substance_open,
            "checks": checks}


# ---------------------------------------------------------------------------
# R17-PINMAP
# ---------------------------------------------------------------------------

def _d_pinmap(root: str, rev: str) -> dict:
    checks = []
    # named: correction lines name the routed defect
    for path in (KNOWLEDGE, "SCORECARD.md"):
        label = "knowledge" if path == KNOWLEDGE else "scorecard"
        ok, detail = _line_with(_text(_show(root, rev, path)), path,
                                "R17-PINMAP", "comparator verdict")
        checks.append(_check("named", f"{label}-names-correction", ok, detail))
    quality = _text(_show(root, rev, "corpus/QUALITY.md"))
    if quality is None:
        checks.append(_check("named", "quality-admission-row", False,
                             "corpus/QUALITY.md absent at rev"))
    else:
        hit = None
        for line in _section_lines(quality, "Admission criteria"):
            if not line.startswith("|"):
                continue
            cells = _cells(line)
            if len(cells) < 3 or cells[0] == "#" or set(cells[0]) <= {"-"}:
                continue
            why = cells[2]
            if "round-17-verifier-spotcheck.md" in why and "R17-PINMAP" in why:
                hit = f"row {cells[0]}: {why[:160]}"
                break
        checks.append(_check("named", "quality-admission-row", hit is not None,
                             hit or "no admission-table data row whose "
                                    "why-cell names round-17-verifier-"
                                    "spotcheck.md and R17-PINMAP"))
    src = _text(_show(root, rev, CARRIER_RUN))
    checks.append(_check("named", "carrier-run-retains-map",
                         src is not None and "map_sha256" in src,
                         f"{CARRIER_RUN} absent at rev" if src is None else
                         (f"{CARRIER_RUN} contains literal 'map_sha256'"
                          if "map_sha256" in src else
                          f"{CARRIER_RUN} lacks literal 'map_sha256'")))

    # substance: the correction is anchored, the code retains mid maps, a
    # validator finds drift, and a round-18 receipt carries hashed mid maps
    for path, anchor in PINMAP_ANCHORS.items():
        label = "knowledge" if path == KNOWLEDGE else "scorecard"
        ok, detail = _line_with(_text(_show(root, rev, path)), path,
                                "R17-PINMAP", anchor, "not the map")
        checks.append(_check("substance", f"{label}-correction-anchored",
                             ok, detail))

    lessons = _text(_show(root, rev, LESSONS18))
    if lessons is None:
        checks.append(_check("substance", "lessons18-mistakes-row", False,
                             f"{LESSONS18} absent at rev"))
    else:
        hit = next((ln.strip()[:160] for ln in
                    _section_lines(lessons, "Mistakes")
                    if "R17-PINMAP" in ln), None)
        checks.append(_check("substance", "lessons18-mistakes-row",
                             hit is not None,
                             hit or "no '## Mistakes' row containing "
                                    "R17-PINMAP"))

    if src is None:
        checks.append(_check("substance", "carrier-run-map-code", False,
                             f"{CARRIER_RUN} absent at rev"))
    else:
        code = _code_text(src)
        ok = code is not None and "map_sha256" in code
        checks.append(_check("substance", "carrier-run-map-code", ok,
                             "'map_sha256' in non-comment code"
                             if ok else ("cannot tokenize" if code is None else
                                         "'map_sha256' only in comments/"
                                         "docstrings or absent")))

    rsrc = _text(_show(root, rev, RECEIPT_VALIDATE))
    if rsrc is None:
        checks.append(_check("substance", "receipt-validate-mid-finding",
                             False, f"{RECEIPT_VALIDATE} absent at rev"))
    else:
        code = _code_text(rsrc)
        ok = code is not None and "mid_map_mismatch" in code
        checks.append(_check("substance", "receipt-validate-mid-finding", ok,
                             "'mid_map_mismatch' in non-comment code"
                             if ok else ("cannot tokenize" if code is None else
                                         "'mid_map_mismatch' only in comments/"
                                         "docstrings or absent")))

    checks.append(_pinmaps_retained_check(root, rev))
    return _defect("R17-PINMAP", checks)


def _map_candidates(map_path: str, receipt_dir: str) -> list[str]:
    """Lane-relative candidate paths for a recorded map_path."""
    out = []
    if map_path.startswith("/"):
        idx = map_path.find(".ufo/")
        if idx >= 0:
            out.append(map_path[idx:])
        out.append(map_path.lstrip("/"))
    else:
        out.append(map_path)
        out.append(f"{receipt_dir}/{map_path}")
    seen, dedup = set(), []
    for c in out:
        if c and c not in seen:
            seen.add(c)
            dedup.append(c)
    return dedup


def _pin_checks_of(doc: dict) -> list | None:
    steps = doc.get("steps")
    if not isinstance(steps, dict):
        return None
    for step in steps.values():
        if isinstance(step, dict) and isinstance(step.get("pin_checks"), list):
            return step["pin_checks"]
    return None


def _pinmaps_retained_check(root: str, rev: str) -> dict:
    name = "r18-receipt-pinmaps"
    runs = _ls_trees(root, rev, RUNS18)
    if runs is None:
        return _check("substance", name, False,
                      f"{RUNS18}/ absent at rev")
    failures = []
    for run_dir in runs:
        receipt_path = f"{RUNS18}/{run_dir}/receipt.json"
        blob = _show(root, rev, receipt_path)
        if blob is None:
            continue
        try:
            doc = json.loads(blob.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            failures.append(f"{run_dir}: receipt.json unparseable")
            continue
        checks_list = _pin_checks_of(doc)
        if not checks_list:
            failures.append(f"{run_dir}: no steps.*.pin_checks list")
            continue
        bad = []
        for i, pc in enumerate(checks_list):
            if not isinstance(pc, dict):
                bad.append(f"pin_checks[{i}] not an object")
                continue
            mp, ms = pc.get("map_path"), pc.get("map_sha256")
            if not isinstance(mp, str) or not isinstance(ms, str):
                bad.append(f"pin_checks[{i}] lacks map_path/map_sha256")
                continue
            resolved = None
            for cand in _map_candidates(mp, f"{RUNS18}/{run_dir}"):
                blob2 = _show(root, rev, cand)
                if blob2 is not None:
                    resolved = (cand, blob2)
                    break
            if resolved is None:
                bad.append(f"pin_checks[{i}] map_path {mp!r} resolves to no "
                           "lane-relative blob")
            elif hashlib.sha256(resolved[1]).hexdigest() != ms:
                bad.append(f"pin_checks[{i}] blob at {resolved[0]} sha256 "
                           f"!= map_sha256 {ms[:16]}…")
        if not bad:
            return _check("substance", name, True,
                          f"{receipt_path}: {len(checks_list)} pin_checks "
                          "each carry map_path + verified map_sha256")
        failures.append(f"{run_dir}: {'; '.join(bad[:3])}")
    return _check("substance", name, False,
                  ("no qualifying receipt; " + " | ".join(failures[:4]))
                  if failures else "no receipt.json under runs dirs")


# ---------------------------------------------------------------------------
# R17-VALIDATE16
# ---------------------------------------------------------------------------

def _summary_labels(doc: dict) -> list[str] | None:
    labels = doc.get("labels")
    if isinstance(labels, list) and all(isinstance(x, str) for x in labels):
        return list(labels)
    receipts = doc.get("receipts")
    if isinstance(receipts, list):
        got = [r["label"] for r in receipts
               if isinstance(r, dict) and isinstance(r.get("label"), str)]
        if got and len(got) == len(receipts):
            return got
    return None


def _d_validate16(root: str, rev: str) -> dict:
    checks = []
    blob = _show(root, rev, SUMMARY16)
    doc = None
    if blob is None:
        checks.append(_check("named", "validate16-summary", False,
                             f"{SUMMARY16} absent at rev"))
    else:
        try:
            doc = json.loads(blob.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            checks.append(_check("named", "validate16-summary", False,
                                 f"{SUMMARY16} does not parse: {exc}"))
        else:
            problems = []
            if not isinstance(doc, dict):
                problems.append("top level is not an object")
            else:
                if doc.get("rev") != VALIDATE16_REV:
                    problems.append(f"rev is {doc.get('rev')!r}, "
                                    f"expected {VALIDATE16_REV}")
                receipts = doc.get("receipts")
                if not isinstance(receipts, list) or len(receipts) != 8:
                    n = len(receipts) if isinstance(receipts, list) \
                        else "non-list"
                    problems.append(f"receipts has {n} entries, expected 8")
                else:
                    for i, entry in enumerate(receipts):
                        if not isinstance(entry, dict) or \
                                not isinstance(entry.get("exit"), int) or \
                                isinstance(entry.get("exit"), bool):
                            problems.append(
                                f"receipts[{i}] lacks an int 'exit'")
            checks.append(_check("named", "validate16-summary",
                                 not problems,
                                 "; ".join(problems) if problems else
                                 f"rev={VALIDATE16_REV}, 8 receipts each "
                                 "with int exit"))
    for path, label in (("SCORECARD.md", "scorecard"), ("LOG.md", "log")):
        ok, detail = _line_with(_text(_show(root, rev, path)), path,
                                "R17-VALIDATE16")
        checks.append(_check("named", f"{label}-names-defect", ok, detail))

    # substance: summary labels are the receipt-bearing run dirs at da64646,
    # a validator digest is pinned, and the reported k/8 is the true count
    zero_exits = None
    if isinstance(doc, dict):
        receipts = doc.get("receipts")
        if isinstance(receipts, list):
            zero_exits = sum(1 for r in receipts
                             if isinstance(r, dict) and r.get("exit") == 0)
    dirs = _ls_trees(root, RUNLOG_REV, RUNS17)
    if isinstance(doc, dict) and dirs is not None:
        with_receipt = sorted(d for d in dirs
                              if _exists(root, RUNLOG_REV,
                                         f"{RUNS17}/{d}/receipt.json"))
        labels = _summary_labels(doc)
        if labels is None:
            checks.append(_check("substance", "summary-labels-are-run-dirs",
                                 False, "summary has no labels list and no "
                                        "per-receipt label fields"))
        else:
            checks.append(_check(
                "substance", "summary-labels-are-run-dirs",
                sorted(labels) == with_receipt,
                f"labels {sorted(labels)!r} vs run dirs {with_receipt!r}"))
        vs = doc.get("validator_sha256")
        ok = isinstance(vs, str) and len(vs) == 64 and all(
            c in "0123456789abcdefABCDEF" for c in vs)
        checks.append(_check("substance", "validator-sha256-pinned", ok,
                             f"validator_sha256={vs!r}"))
    else:
        reason = ("summary absent/unparseable" if not isinstance(doc, dict)
                  else f"no run dirs at {RUNLOG_REV}:{RUNS17}/")
        checks.append(_check("substance", "summary-labels-are-run-dirs",
                             False, reason))
        checks.append(_check("substance", "validator-sha256-pinned", False,
                             reason))

    if zero_exits is None:
        for path, label in (("SCORECARD.md", "scorecard"),
                            ("LOG.md", "log")):
            checks.append(_check("substance", f"{label}-states-true-count",
                                 False, "cannot count exit-0 receipts"))
    else:
        fraction = f"{zero_exits}/8"
        for path, label in (("SCORECARD.md", "scorecard"),
                            ("LOG.md", "log")):
            ok, detail = _line_with(_text(_show(root, rev, path)), path,
                                    "R17-VALIDATE16", fraction)
            checks.append(_check("substance", f"{label}-states-true-count",
                                 ok, detail))
    return _defect("R17-VALIDATE16", checks)


# ---------------------------------------------------------------------------
# R17-PRODUCER-REV
# ---------------------------------------------------------------------------

def _line_with_two_hashes(text: str | None, path: str) -> tuple[bool, str]:
    if text is None:
        return False, f"{path} absent at rev"
    for line in text.splitlines():
        if "R17-PRODUCER-REV" not in line:
            continue
        hashes = set(_HEX40.findall(line))
        if len(hashes) >= 2:
            return True, line.strip()[:200]
    return False, (f"{path}: no line containing 'R17-PRODUCER-REV' and two "
                   "distinct 40-hex hashes")


def _d_producer_rev(root: str, rev: str) -> dict:
    checks = []
    for path, label in (("SCORECARD.md", "scorecard"),
                        (KNOWLEDGE, "knowledge")):
        ok, detail = _line_with_two_hashes(_text(_show(root, rev, path)), path)
        checks.append(_check("named", f"{label}-names-producing-revs",
                             ok, detail))

    # substance: the named lines carry BOTH pinned producer hashes and each
    # hash is a real ancestor of REV; LOG.md carries such a line too
    for path, label in (("SCORECARD.md", "scorecard"),
                        (KNOWLEDGE, "knowledge"), ("LOG.md", "log")):
        ok, detail = _line_with(_text(_show(root, rev, path)), path,
                                "R17-PRODUCER-REV", *PRODUCER_REVS)
        checks.append(_check("substance", f"{label}-names-pinned-revs",
                             ok, detail))
    not_anc = [h for h in PRODUCER_REVS if not _is_ancestor(root, h, rev)]
    checks.append(_check("substance", "producer-revs-are-ancestors",
                         not not_anc,
                         "both pinned producer revs are ancestors of REV"
                         if not not_anc else
                         f"not ancestors of REV (or absent objects): "
                         f"{not_anc}"))
    return _defect("R17-PRODUCER-REV", checks)


# ---------------------------------------------------------------------------
# R17-SUMS-RUNLOG
# ---------------------------------------------------------------------------

def _d_sums_runlog(root: str, rev: str) -> dict:
    checks = []
    sums_blob = _show(root, rev, SUMS)
    carriers = _show(root, rev, CARRIERS_TSV)
    if sums_blob is None:
        checks.append(_check("named", "sums-covers-carriers-tsv", False,
                             f"{SUMS} absent at rev"))
    elif carriers is None:
        checks.append(_check("named", "sums-covers-carriers-tsv", False,
                             f"{CARRIERS_TSV} absent at rev"))
    else:
        want = hashlib.sha256(carriers).hexdigest().encode()
        recorded = [m.group(1).lower() for line in sums_blob.splitlines()
                    if (m := _SUMS_LINE.match(line))]
        if want in recorded:
            detail = f"SHA256SUMS records {want.decode()} for carriers.tsv"
            ok = True
        elif recorded:
            detail = (f"carriers.tsv line records {[r.decode() for r in recorded]}"
                      f" but blob sha256 is {want.decode()}")
            ok = False
        else:
            detail = "no 'predictions/carriers.tsv' line in SHA256SUMS"
            ok = False
        checks.append(_check("named", "sums-covers-carriers-tsv", ok, detail))
    ok, detail = _line_with(_text(_show(root, rev, "LOG.md")),
                            "LOG.md", "R17-SUMS-RUNLOG", "7/8")
    checks.append(_check("named", "log-names-runlog-gap", ok, detail))

    # substance: REV's manifest contains every historical line byte-exact,
    # carriers.tsv is the same blob as at 2711674, and the stated fraction
    # equals (start lines at da64646)/(labels in carriers.tsv)
    hist = _show(root, HIST_SUMS_REV, SUMS)
    if sums_blob is None or hist is None:
        checks.append(_check("substance", "sums-restored-from-2711674", False,
                             f"{SUMS} absent at REV" if sums_blob is None else
                             f"{SUMS} unreadable at {HIST_SUMS_REV}"))
    else:
        rev_lines = set(sums_blob.split(b"\n"))
        missing = [ln for ln in hist.split(b"\n")
                   if ln and ln not in rev_lines]
        checks.append(_check("substance", "sums-restored-from-2711674",
                             not missing,
                             "every 2711674 SHA256SUMS line present "
                             "byte-exact" if not missing else
                             f"{len(missing)} historical line(s) missing: "
                             f"{missing[0][:100]!r}"))
    hist_tsv = _show(root, HIST_SUMS_REV, CARRIERS_TSV)
    if carriers is None or hist_tsv is None:
        checks.append(_check("substance", "carriers-tsv-identical", False,
                             f"{CARRIERS_TSV} absent at REV or {HIST_SUMS_REV}"))
    else:
        checks.append(_check("substance", "carriers-tsv-identical",
                             carriers == hist_tsv,
                             "carriers.tsv blob identical to 2711674"
                             if carriers == hist_tsv else
                             "carriers.tsv differs from 2711674 blob"))

    runlog = _text(_show(root, RUNLOG_REV, f"{RUNS17}/run-log.txt"))
    if runlog is None or carriers is None:
        checks.append(_check("substance", "log-fraction-true", False,
                             f"run-log.txt unreadable at {RUNLOG_REV}"
                             if runlog is None else
                             f"{CARRIERS_TSV} absent at rev"))
    else:
        starts = sum(1 for ln in runlog.splitlines()
                     if _RUNLOG_START.match(ln))
        labels = sum(1 for ln in _text(carriers).splitlines()
                     if ln.strip() and not ln.startswith("label"))
        frac = f"{starts}/{labels}"
        ok, detail = _line_with(_text(_show(root, rev, "LOG.md")),
                                "LOG.md", "R17-SUMS-RUNLOG", RUNLOG_REV, frac)
        checks.append(_check("substance", "log-fraction-true", ok,
                             detail if not ok else
                             f"LOG line states the true fraction {frac} "
                             f"({starts} start lines / {labels} labels)"))
    return _defect("R17-SUMS-RUNLOG", checks)


# ---------------------------------------------------------------------------
# R17-REGISTRY
# ---------------------------------------------------------------------------

def _registry_rows(text: str, first_cell: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = _cells(line)
        if cells and cells[0] == first_cell:
            rows.append(cells)
    return rows


def _scope_cell_ok(root: str, rev: str, cell: str) -> tuple[bool, str]:
    """'Write scope:' followed by >=3 words; backticked .ufo//corpus/ tokens
    must exist at REV."""
    idx = cell.find("Write scope:")
    if idx < 0:
        return False, "no 'Write scope:' in 5th cell"
    tail = cell[idx + len("Write scope:"):]
    words = tail.split()
    if len(words) < 3:
        return False, f"'Write scope:' followed by {len(words)} word(s), need 3"
    missing = []
    for tok in _BACKTICK_PATH.findall(cell):
        t = tok.strip().rstrip("/")
        if t.startswith(".ufo/") or t.startswith("corpus/"):
            if not _exists(root, rev, t):
                missing.append(t)
    if missing:
        return False, f"scoped paths absent at rev: {missing}"
    return True, f"'Write scope:' + {len(words)} words; scoped paths exist"


def _d_registry(root: str, rev: str) -> dict:
    skill = _text(_show(root, rev, "SKILL.md"))
    checks = []
    if skill is None:
        for name in REGISTRY_SCOPED:
            checks.append(_check("named", f"skill-row-{name}", False,
                                 "SKILL.md absent at rev"))
            checks.append(_check("substance", f"skill-scope-{name}", False,
                                 "SKILL.md absent at rev"))
        checks.append(_check("named", "skill-row-citation-drift", False,
                             "SKILL.md absent at rev"))
        return _defect("R17-REGISTRY", checks)
    for name in REGISTRY_SCOPED:
        rows = _registry_rows(skill, name)
        if not rows:
            checks.append(_check("named", f"skill-row-{name}", False,
                                 f"no SKILL.md table row with first cell "
                                 f"{name!r}"))
            checks.append(_check("substance", f"skill-scope-{name}", False,
                                 "row absent"))
            continue
        bad = [f"5th cell is {r[4][:80]!r}" if len(r) > 4 else
               f"row has {len(r)} cells" for r in rows
               if len(r) <= 4 or "Write scope:" not in r[4]]
        checks.append(_check("named", f"skill-row-{name}", not bad,
                             "; ".join(bad) if bad else
                             f"{name} 5th cell names 'Write scope:'"))
        scope_bad = []
        for r in rows:
            if len(r) <= 4:
                scope_bad.append(f"row has {len(r)} cells")
                continue
            ok, why = _scope_cell_ok(root, rev, r[4])
            if not ok:
                scope_bad.append(why)
        checks.append(_check("substance", f"skill-scope-{name}",
                             not scope_bad,
                             "; ".join(scope_bad) if scope_bad else
                             f"{name} scope cell verified"))
    rows = _registry_rows(skill, "citation-drift")
    if not rows:
        checks.append(_check("named", "skill-row-citation-drift", False,
                             "no SKILL.md table row with first cell "
                             "'citation-drift'"))
    else:
        bad = [f"2nd cell is {r[1][:80]!r}" for r in rows
               if len(r) < 2 or not r[1].startswith("gate")]
        checks.append(_check("named", "skill-row-citation-drift", not bad,
                             "; ".join(bad) if bad else
                             "citation-drift 2nd cell starts with 'gate'"))
    return _defect("R17-REGISTRY", checks)


# ---------------------------------------------------------------------------
# R17-S032-DIGEST
# ---------------------------------------------------------------------------

def _s032_superseding_rows(sources: str) -> list[list[str]]:
    out = []
    for line in sources.splitlines():
        if not line.startswith("|"):
            continue
        cells = _cells(line)
        if (len(cells) == 11 and cells[6].startswith("supersedes S032 —")
                and "fetch-time" in cells[5]):
            out.append(cells)
    return out


def _hex64s_in(obj) -> set[str]:
    found = set()
    if isinstance(obj, str):
        found.update(m.lower() for m in _HEX64.findall(obj))
    elif isinstance(obj, list):
        for x in obj:
            found.update(_hex64s_in(x))
    elif isinstance(obj, dict):
        for x in obj.values():
            found.update(_hex64s_in(x))
    return found


def _d_s032_digest(root: str, rev: str) -> dict:
    checks = []
    sources = _text(_show(root, rev, "corpus/SOURCES.md"))
    if sources is None:
        checks.append(_check("named", "superseding-row", False,
                             "corpus/SOURCES.md absent at rev"))
        checks.append(_check("substance", "s033-anchor-commit", False,
                             "corpus/SOURCES.md absent at rev"))
    else:
        rows = _s032_superseding_rows(sources)
        if rows:
            checks.append(_check("named", "superseding-row", True,
                                 f"row {rows[0][0]}: teaches="
                                 f"{rows[0][6][:120]!r}"))
            anchored = [r for r in rows if _HEX40.search(r[5])]
            checks.append(_check("substance", "s033-anchor-commit",
                                 bool(anchored),
                                 f"row {anchored[0][0]} anchor pins a "
                                 "40-hex commit" if anchored else
                                 "superseding row's anchor cell has no "
                                 "40-hex commit"))
        else:
            checks.append(_check("named", "superseding-row", False,
                                 "no 11-column registry row whose teaches "
                                 "cell starts with 'supersedes S032 —' and "
                                 "whose anchor cell contains 'fetch-time'"))
            checks.append(_check("substance", "s033-anchor-commit", False,
                                 "no superseding row"))

    blob = _show(root, rev, S032_DIGESTS)
    if blob is None:
        checks.append(_check("substance", "s032-digests-evidence", False,
                             f"{S032_DIGESTS} absent at rev"))
    else:
        try:
            doc = json.loads(blob.decode("utf-8"))
            digests = _hex64s_in(doc)
        except (UnicodeDecodeError, ValueError) as exc:
            digests = None
            checks.append(_check("substance", "s032-digests-evidence", False,
                                 f"{S032_DIGESTS} does not parse: {exc}"))
        if digests is not None:
            checks.append(_check("substance", "s032-digests-evidence",
                                 len(digests) >= 2,
                                 f"{len(digests)} distinct 64-hex page "
                                 "digests" if len(digests) >= 2 else
                                 f"only {len(digests)} distinct 64-hex page "
                                 "digest(s), need >=2"))
    return _defect("R17-S032-DIGEST", checks)


def evaluate(root: str, rev: str) -> dict:
    """Evaluate all six routed defects at REV; raises EvalError (exit 2)."""
    resolved = _resolve_rev(root, rev)
    defects = [_d_pinmap(root, resolved),
               _d_validate16(root, resolved),
               _d_producer_rev(root, resolved),
               _d_sums_runlog(root, resolved),
               _d_registry(root, resolved),
               _d_s032_digest(root, resolved)]
    return {"rev": resolved,
            "defects": defects,
            "named_open_count": sum(1 for d in defects if d["named_open"]),
            "substance_open_count": sum(
                1 for d in defects if d["substance_open"]),
            "open_count": sum(1 for d in defects if d["open"])}


def _emit(doc: dict) -> None:
    json.dump(doc, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")


# --------------------------------------------------------------------------
# selftest — fixture repo under tempfile.mkdtemp(), outside LANE
# --------------------------------------------------------------------------

_LABELS = ["calib-shfmt", "calib-esbuild-0.25.12", "pro-notesmd-cli",
           "pro-aether", "pro-esbuild-0.21.5", "pro-containerd-shim",
           "pro-esbuild-0.27.7", "pro-op"]
_CARRIERS_TSV = ("label\tpath\tkind\n" +
                 "".join(f"{l}\t/usr/bin/{l}\ttest\n" for l in _LABELS))
_RUNLOG_7 = "".join(f"== {l} start 2026-10-20T10:00:00Z\n"
                    f"== {l} end carrier-run=0 compare=0\n"
                    for l in _LABELS[1:])  # 7 starts, calib-shfmt missing

H1 = "a" * 40
H2 = "b" * 40
_PRODUCER_LINE = ("- R17-PRODUCER-REV: pass produced by "
                  f"{PRODUCER_REVS[0]} {{extra1}}, verified at "
                  f"{PRODUCER_REVS[1]} {{extra2}} "
                  "(producing vs verifying revision)\n")


def _hist_files() -> dict[str, str]:
    """Files living at the 2711674/da64646-tagged history commit."""
    files = {CARRIERS_TSV: _CARRIERS_TSV,
             f"{RUNS17}/run-log.txt": _RUNLOG_7}
    carriers_sha = hashlib.sha256(_CARRIERS_TSV.encode()).hexdigest()
    files[SUMS] = ("aa" * 32 + "  predictions/replicate-expectations.json\n"
                   + carriers_sha + "  predictions/carriers.tsv\n")
    for label in _LABELS:
        files[f"{RUNS17}/{label}/receipt.json"] = json.dumps(
            {"label": label, "exit": 0})
    return files


def _open_files() -> dict[str, str]:
    """All six defects open: named checks fail everywhere."""
    return {
        "SCORECARD.md": "# scorecard\nno routed notes\n",
        "LOG.md": "# log\nnothing routed\n",
        KNOWLEDGE: "# diagnostics\npin map claim text\n",
        "corpus/QUALITY.md": "# bar\n\n## Admission criteria\n\n"
                             "| # | criterion | why (lesson) | supersedes |\n"
                             "|---|---|---|---|\n"
                             "| 1 | cite | a lesson | — |\n",
        CARRIER_RUN: "# mid-run pin keeps verdict only\npin_checks = {}\n",
        RECEIPT_VALIDATE: "# validator without mid finding\n",
        "SKILL.md": "# skill\n\n| name | kind | cmd | selftest | note |\n"
                    "|---|---|---|---|---|\n"
                    "| go-route-compare | probe / k | `c` | `s` | note |\n"
                    "| receipt-validate | gate / k | `c` | `s` | note |\n"
                    "| pins | tool / k | `c` | `s` | note |\n"
                    "| go-buildinfo-probe | probe / k | `c` | `s` | note |\n"
                    "| citation-drift | probe / kaidoku | `c` | `s` | note |\n",
        "corpus/SOURCES.md": "# src\n\n| id | source | kind | tier | scope | "
                            "anchor | teaches | status | opened | recheck | "
                            "used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
                            "| S032 | PR 9348 | community | B | scope | "
                            "sha256 `436c0f63` | names the misread | mined | "
                            "2026-10-20 | 90d | lessons |\n",
        SUMS: "deadbeef" * 8 + "  predictions/other.tsv\n",
        CARRIERS_TSV: "label\tpath\n",
    }


def _closed_files(fixture_revs: tuple[str, str] | None = None) -> dict[str, str]:
    """Every named and substance check satisfied. fixture_revs are two real
    ancestor commits used so an in-process evaluate with a patched
    PRODUCER_REVS can fully close R17-PRODUCER-REV; the file text also names
    the literal contract hashes so only the ancestor check is unclosable
    from the CLI."""
    extra1, extra2 = fixture_revs or (H1, H2)
    producer = _PRODUCER_LINE.format(extra1=extra1, extra2=extra2)
    map_body = b'{"a":1}\n'
    map_sha = hashlib.sha256(map_body).hexdigest()
    carriers_sha = hashlib.sha256(_CARRIERS_TSV.encode()).hexdigest()
    files = {
        "SCORECARD.md": (
            "# scorecard\n"
            "- R17-PINMAP correction at SCORECARD.md:2374: mid-run instants "
            "retain the comparator verdict against the retained pre map, "
            "not the map\n"
            "- R17-VALIDATE16: 8/8 receipts validate (8 committed plus 8 "
            "validated from git objects)\n"
            + producer),
        "LOG.md": (
            "# log\n"
            "- R17-VALIDATE16 validated the da64646 receipts: 8/8\n"
            "- R17-SUMS-RUNLOG: pass-1 run-log at da64646 listed 7/8 "
            "carriers, no final exit line\n"
            + producer),
        KNOWLEDGE: (
            "# diagnostics\n"
            "- R17-PINMAP correction at "
            "2026-10-20-r17-go-carrier-diagnostics.md:30-32: mid-run "
            "instants retain the comparator verdict against the retained "
            "pre map, not the map\n"
            + producer),
        LESSONS18: ("# round 18\n\n## Mistakes\n\n"
                    "| mistake | fix |\n|---|---|\n"
                    "| r17 claimed pin maps retained | routed R17-PINMAP |\n"),
        "corpus/QUALITY.md": (
            "# bar\n\n## Admission criteria\n\n"
            "| # | criterion | why (lesson) | supersedes |\n"
            "|---|---|---|---|\n"
            "| 21 | pin claims | lesson corpus/lessons/"
            "round-17-verifier-spotcheck.md R17-PINMAP | — |\n"),
        CARRIER_RUN: ("def check():\n"
                      "    entry = {}\n"
                      "    entry[\"map_sha256\"] = digest\n"
                      "    return entry\n"),
        RECEIPT_VALIDATE: ("FINDING = \"mid_map_mismatch\"\n"
                           "def validate():\n"
                           "    return FINDING\n"),
        "SKILL.md": (
            "# skill\n\n| name | kind | cmd | selftest | scope | note |\n"
            "|---|---|---|---|---|---|\n"
            "| go-route-compare | probe / k | `c` | `s` | Write scope: "
            "`.ufo/waves/round-18/runs/` receipt files only | n |\n"
            "| receipt-validate | gate / k | `c` | `s` | Write scope: "
            "`.ufo/waves/round-18/runs/` receipt files only | n |\n"
            "| pins | tool / k | `c` | `s` | Write scope: `corpus/` pin "
            "snapshot files only | n |\n"
            "| go-buildinfo-probe | probe / k | `c` | `s` | Write scope: "
            "`.ufo/waves/round-18/runs/` receipt files only | n |\n"
            "| citation-drift | gate / kaidoku | `c` | `s` | Write scope: "
            "`.ufo/waves/round-18/runs/` receipt files only | n |\n"),
        "corpus/SOURCES.md": (
            "# src\n\n| id | source | kind | tier | scope | anchor | "
            "teaches | status | opened | recheck | used-by |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|\n"
            "| S032 | PR 9348 | community | B | scope | sha256 `436c0f63` "
            "| names the misread | mined | 2026-10-20 | 90d | lessons |\n"
            f"| S033 | new anchor | docs | A | scope | fetch-time sha256, "
            f"title+state at commit {H1} | supersedes S032 — digest was "
            "fetch-time only | mined | 2026-10-20 | 90d | lessons |\n"),
        SUMS: ("aa" * 32 + "  predictions/replicate-expectations.json\n"
               + carriers_sha + "  predictions/carriers.tsv\n"),
        CARRIERS_TSV: _CARRIERS_TSV,
        SUMMARY16: json.dumps(
            {"rev": VALIDATE16_REV,
             "labels": list(_LABELS),
             "validator_sha256": "f" * 64,
             "receipts": [{"label": l, "exit": 0} for l in _LABELS]}),
        S032_DIGESTS: json.dumps(
            {"page_digests": ["1" * 64, "2" * 64]}),
        "corpus/pins-note.txt": "x\n",
        f"{RUNS18}/pro-aether/receipt.json": json.dumps(
            {"label": "pro-aether",
             "steps": {"analyze": {"pin_checks": [
                 {"map_path": "/fixture/root/.ufo/waves/round-18/runs/"
                              "pro-aether/pins/mid-1.json",
                  "map_sha256": map_sha},
                 {"map_path": "pins/mid-2.json",
                  "map_sha256": hashlib.sha256(b'{"b":2}\n').hexdigest()}]}}}),
        f"{RUNS18}/pro-aether/pins/mid-1.json": map_body.decode(),
        f"{RUNS18}/pro-aether/pins/mid-2.json": '{"b":2}\n',
    }
    return files


def _selftest() -> int:
    failures: list[str] = []
    cases = 0

    def check(ok: bool, name: str, detail: str = "") -> None:
        if not ok:
            failures.append(f"{name}: {detail}")

    root = tempfile.mkdtemp(prefix="routed-defects-selftest-")
    try:
        env = dict(os.environ,
                   GIT_AUTHOR_NAME="selftest", GIT_AUTHOR_EMAIL="s@t",
                   GIT_COMMITTER_NAME="selftest", GIT_COMMITTER_EMAIL="s@t")

        def git(*args: str) -> str:
            proc = subprocess.run(["git", "-C", root, *args],
                                  capture_output=True, env=env, timeout=60)
            if proc.returncode != 0:
                raise RuntimeError(f"git {' '.join(args)}: "
                                   f"{proc.stderr.decode('utf-8', 'replace')}")
            return proc.stdout.decode().strip()

        def commit(files: dict[str, str | None], message: str) -> str:
            for path, content in files.items():
                full = os.path.join(root, path)
                if content is None:      # None = delete the path at this commit
                    if os.path.exists(full):
                        os.unlink(full)
                    continue
                parent = os.path.dirname(full)
                if parent:
                    os.makedirs(parent, exist_ok=True)
                with open(full, "w", encoding="utf-8") as fh:
                    fh.write(content)
            git("add", "-A")
            git("-c", "commit.gpgsign=false", "commit", "-q", "-m", message)
            return git("rev-parse", "HEAD")

        def run_tool(*argv: str) -> subprocess.CompletedProcess:
            return subprocess.run(
                [sys.executable, "-I", "-B", os.path.abspath(__file__), *argv],
                capture_output=True, text=True, timeout=60)

        git("init", "-q")
        hist_rev = commit(_hist_files(), "historical r17 pins")
        git("tag", HIST_SUMS_REV, hist_rev)
        git("tag", RUNLOG_REV, hist_rev)
        git("-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty",
            "-m", "producer pass two")
        producer2 = git("rev-parse", "HEAD")
        fixture_producers = (hist_rev, producer2)

        open_rev = commit(_open_files(), "all six routed defects open")
        closed_rev = commit(_closed_files(fixture_producers),
                            "all six routed defects closed")

        # case 1: open fixture, default exit 0, open_count 6
        cases += 1
        r = run_tool("--root", root, "--rev", open_rev)
        doc = json.loads(r.stdout) if r.stdout.strip() else {}
        check(r.returncode == 0 and doc.get("open_count") == 6
              and all(d["open"] and d["named_open"] and d["substance_open"]
                      for d in doc.get("defects", [])),
              "open-fixture",
              f"rc={r.returncode} open_count={doc.get('open_count')}")

        # case 2 (required red): same fixture under --strict exits 1
        cases += 1
        r = run_tool("--root", root, "--rev", open_rev, "--strict")
        check(r.returncode == 1, "open-fixture-strict",
              f"rc={r.returncode} (expected 1: open defects under --strict)")

        # case 3: closed fixture via CLI. The two literal 40-hex producer
        # hashes can never be objects in a fixture (git ignores 40-hex
        # refnames), so only producer-revs-are-ancestors stays open.
        cases += 1
        r = run_tool("--root", root, "--rev", closed_rev)
        doc = json.loads(r.stdout) if r.stdout.strip() else {}
        opened = [d["id"] for d in doc.get("defects", []) if d["open"]]
        broken = [c["name"] for d in doc.get("defects", [])
                  for c in d["checks"] if not c["ok"]]
        check(r.returncode == 0 and opened == ["R17-PRODUCER-REV"]
              and broken == ["producer-revs-are-ancestors"],
              "closed-fixture-cli",
              f"rc={r.returncode} opened={opened} broken={broken}")

        # case 4: closed fixture in-process with fixture producer revs —
        # every check of every defect passes, open_count 0.
        cases += 1
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "routed_defects_st", os.path.abspath(__file__))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.PRODUCER_REVS = fixture_producers
        doc2 = mod.evaluate(root, closed_rev)
        check(doc2["open_count"] == 0
              and doc2["named_open_count"] == 0
              and doc2["substance_open_count"] == 0,
              "closed-fixture-inprocess",
              f"open_count={doc2['open_count']} "
              f"broken={[c['name'] for d in doc2['defects'] for c in d['checks'] if not c['ok']]}")

        # one case per defect: exactly one named check broken -> defect open
        named_variants = [
            ("R17-PINMAP", {
                CARRIER_RUN: "# no mid map retention\npin_checks = {}\n"},
             "carrier-run-retains-map"),
            ("R17-VALIDATE16", {
                "LOG.md": ("# log\n"
                           "- R17-SUMS-RUNLOG: pass-1 run-log at da64646 "
                           "listed 7/8 carriers\n")},
             "log-names-defect"),
            ("R17-PRODUCER-REV", {
                "SCORECARD.md": (
                    "# scorecard\n"
                    "- R17-PINMAP correction at SCORECARD.md:2374: mid-run "
                    "instants retain the comparator verdict against the "
                    "retained pre map, not the map\n"
                    "- R17-VALIDATE16: 8/8 receipts validate\n"
                    f"- R17-PRODUCER-REV: produced by {H1} alone\n")},
             "scorecard-names-producing-revs"),
            ("R17-SUMS-RUNLOG", {
                SUMS: ("0" * 64) + "  predictions/carriers.tsv\n"},
             "sums-covers-carriers-tsv"),
            ("R17-REGISTRY", {
                "SKILL.md": (
                    "# skill\n\n| name | kind | cmd | selftest | scope | "
                    "note |\n|---|---|---|---|---|---|\n"
                    "| go-route-compare | probe / k | `c` | `s` | Write "
                    "scope: `.ufo/waves/round-18/runs/` receipt files only "
                    "| n |\n"
                    "| receipt-validate | gate / k | `c` | `s` | Write "
                    "scope: `.ufo/waves/round-18/runs/` receipt files only "
                    "| n |\n"
                    "| pins | tool / k | `c` | `s` | Write scope: `corpus/` "
                    "pin snapshot files only | n |\n"
                    "| go-buildinfo-probe | probe / k | `c` | `s` | Write "
                    "scope: `.ufo/waves/round-18/runs/` receipt files only "
                    "| n |\n"
                    "| citation-drift | probe / kaidoku | `c` | `s` | Write "
                    "scope: `.ufo/waves/round-18/runs/` receipt files only "
                    "| n |\n")},
             "skill-row-citation-drift"),
            ("R17-S032-DIGEST", {
                "corpus/SOURCES.md": (
                    "# src\n\n| id | source | kind | tier | scope | anchor "
                    "| teaches | status | opened | recheck | used-by |\n"
                    "|---|---|---|---|---|---|---|---|---|---|---|\n"
                    "| S033 | new anchor | docs | A | scope | page title + "
                    "state | supersedes S032 — digest dropped | mined | "
                    "2026-10-20 | 90d | lessons |\n")},
             "superseding-row"),
        ]
        for defect_id, overrides, broken_check in named_variants:
            cases += 1
            files = _closed_files(fixture_producers)
            files.update(overrides)
            variant_rev = commit(files, f"one named check broken: {defect_id}")
            r = run_tool("--root", root, "--rev", variant_rev)
            doc = json.loads(r.stdout) if r.stdout.strip() else {}
            target = next(d for d in doc.get("defects", [])
                          if d["id"] == defect_id)
            named_broken = [c["name"] for c in target["checks"]
                            if c["set"] == "named" and not c["ok"]]
            others_named = [d["id"] for d in doc.get("defects", [])
                            if d["id"] != defect_id and d["named_open"]]
            check(r.returncode == 0 and broken_check in named_broken
                  and not others_named,
                  f"named-variant-{defect_id}",
                  f"rc={r.returncode} named_broken={named_broken} "
                  f"others_named={others_named}")

        # one case per defect: named checks all pass, substance absent —
        # the defect must stay open (the circularity guard).
        token_only = [
            ("R17-PINMAP", {
                # map_sha256 survives only inside a comment; no r18 runs,
                # no lessons file, no anchored correction
                CARRIER_RUN: ("# entry[\"map_sha256\"] = digest\n"
                              "pin_checks = {}\n"),
                RECEIPT_VALIDATE: ("# finding mid_map_mismatch\n"
                                   "def validate():\n"
                                   "    return 0\n"),
                "SCORECARD.md": (
                    "# scorecard\n"
                    "- R17-PINMAP correction: mid-run instants retain the "
                    "comparator verdict, unanchored\n"
                    "- R17-VALIDATE16: 8/8 receipts validate\n"
                    + _PRODUCER_LINE.format(extra1=fixture_producers[0],
                                            extra2=fixture_producers[1])),
                KNOWLEDGE: (
                    "# diagnostics\n"
                    "- R17-PINMAP correction: mid-run instants retain the "
                    "comparator verdict, unanchored\n"
                    + _PRODUCER_LINE.format(extra1=fixture_producers[0],
                                            extra2=fixture_producers[1])),
            }),
            ("R17-VALIDATE16", {
                SUMMARY16: json.dumps(
                    {"rev": VALIDATE16_REV,
                     "labels": ["wrong-label"] * 8,
                     "validator_sha256": "not-a-sha",
                     "receipts": [{"label": l, "exit": 0}
                                  for l in _LABELS]}),
            }),
            ("R17-PRODUCER-REV", {
                # distinct 40-hex tokens, but never the pinned producer revs
                "SCORECARD.md": (
                    "# scorecard\n"
                    "- R17-PINMAP correction at SCORECARD.md:2374: mid-run "
                    "instants retain the comparator verdict against the "
                    "retained pre map, not the map\n"
                    "- R17-VALIDATE16: 8/8 receipts validate\n"
                    f"- R17-PRODUCER-REV: produced by {H1}, "
                    f"verified at {H2}\n"),
                KNOWLEDGE: (
                    "# diagnostics\n"
                    "- R17-PINMAP correction at "
                    "2026-10-20-r17-go-carrier-diagnostics.md:30-32: "
                    "mid-run instants retain the comparator verdict "
                    "against the retained pre map, not the map\n"
                    f"- R17-PRODUCER-REV: produced by {H1}, "
                    f"verified at {H2}\n"),
                "LOG.md": (
                    "# log\n"
                    "- R17-VALIDATE16 validated the da64646 receipts: 8/8\n"
                    "- R17-SUMS-RUNLOG: pass-1 run-log at da64646 listed "
                    "7/8 carriers\n"
                    f"- R17-PRODUCER-REV: produced by {H1}, "
                    f"verified at {H2}\n"),
            }),
            ("R17-SUMS-RUNLOG", {
                # carriers.tsv line present and matching REV's blob, but
                # the tsv differs from the 2711674 blob
                CARRIERS_TSV: "label\tpath\tkind\nchanged\t/x\tt\n",
                SUMS: ("aa" * 32 + "  predictions/replicate-expectations.json\n"
                       + hashlib.sha256(
                           b"label\tpath\tkind\nchanged\t/x\tt\n").hexdigest()
                       + "  predictions/carriers.tsv\n"),
            }),
            ("R17-REGISTRY", {
                "SKILL.md": (
                    "# skill\n\n| name | kind | cmd | selftest | scope | "
                    "note |\n|---|---|---|---|---|---|\n"
                    "| go-route-compare | probe / k | `c` | `s` | Write "
                    "scope: none here | n |\n"
                    "| receipt-validate | gate / k | `c` | `s` | Write "
                    "scope: `corpus/no-such-dir/` receipt files only | n |\n"
                    "| pins | tool / k | `c` | `s` | Write scope: `corpus/` "
                    "pin snapshot files only | n |\n"
                    "| go-buildinfo-probe | probe / k | `c` | `s` | Write "
                    "scope: `.ufo/waves/round-18/runs/` receipt files only "
                    "| n |\n"
                    "| citation-drift | gate / kaidoku | `c` | `s` | Write "
                    "scope: `.ufo/waves/round-18/runs/` receipt files only "
                    "| n |\n"),
            }),
            ("R17-S032-DIGEST", {
                S032_DIGESTS: None,  # path removed: evidence absent
            }),
        ]
        for defect_id, overrides in token_only:
            cases += 1
            files = _closed_files(fixture_producers)
            for path, content in overrides.items():
                files[path] = content   # None = delete that path at this commit
            variant_rev = commit(files, f"tokens only: {defect_id}")
            r = run_tool("--root", root, "--rev", variant_rev)
            doc = json.loads(r.stdout) if r.stdout.strip() else {}
            target = next(d for d in doc.get("defects", [])
                          if d["id"] == defect_id)
            extra = [d["id"] for d in doc.get("defects", [])
                     if d["open"] and d["id"] not in
                     (defect_id, "R17-PRODUCER-REV")]
            check(r.returncode == 0 and target["open"]
                  and not target["named_open"] and target["substance_open"]
                  and not extra,
                  f"token-only-{defect_id}",
                  f"rc={r.returncode} target={target['open'], target['named_open'], target['substance_open']} extra_open={extra}")

        # case: could-not-evaluate (bad rev) -> exit 2
        cases += 1
        r = run_tool("--root", root, "--rev", "no-such-rev")
        check(r.returncode == 2, "bad-rev", f"rc={r.returncode}")
    except Exception as exc:  # noqa: BLE001 — selftest reports, never crashes
        failures.append(f"setup: {type(exc).__name__}: {exc}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    if failures:
        print("SELFTEST: FAILED " + "; ".join(failures))
        return 1
    print(f"SELFTEST: CLEAN cases={cases}")
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        return _selftest()
    ap = argparse.ArgumentParser(
        prog="routed-defects.py",
        description="Count the six routed round-17 defects still open at REV "
                    "(Git objects only, never the working tree).",
        epilog="Closed requires every named AND substance check; absent "
               "paths keep a defect open.")
    ap.add_argument("--root", required=True, metavar="DIR",
                    help="lane repository root (read-only git)")
    ap.add_argument("--rev", required=True, metavar="REV",
                    help="revision to evaluate (pin the branch tip, never HEAD)")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when open_count > 0")
    args = ap.parse_args(argv)
    try:
        doc = evaluate(args.root, args.rev)
    except EvalError as exc:
        _emit({"error": str(exc), "rev": args.rev})
        return 2
    except (OSError, subprocess.SubprocessError) as exc:
        _emit({"error": f"{type(exc).__name__}: {exc}", "rev": args.rev})
        return 2
    _emit(doc)
    if args.strict and doc["open_count"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
