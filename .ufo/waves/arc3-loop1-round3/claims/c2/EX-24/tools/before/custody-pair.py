#!/usr/bin/env python3
"""custody-pair gate (v2, seat EX-31, wave arc3-loop1-round2).

A committed, re-runnable instrument that captures and verifies the custody of the
five operator-owned paths this province treats as frozen:

    ~/.config/devin/mcp_config.json
    ~/.omp/agent/mcp.json
    ~/.kimi-code/config.toml
    ~/.bashrc
    ~/.profile

The instrument is READ-ONLY over every path it inspects: it opens files for
reading only (sha256), never for writing, never renames, never touches mtime.

WHY v2. Two defects were measured against the round-1 canonical receipt
(arc3-loop1-round1, cross seats; receipts still in the round-1 tree):

  1. LABEL DEFECT. The v1 receipt printed the path's local (-03) mtime string
     under an `MTIME_UTC` label (EX-01 A4: epoch 1792011200 = 2026-10-14T20:53:20Z
     = 2026-10-14 17:53:20 -03; the receipt printed "2026-10-14 17:53:20" as
     MTIME_UTC — off by 3 h). Digests were unaffected, the label was wrong.
     v2 renders UTC strictly from the epoch via `time.gmtime()` into
     `MTIME_UTC_RENDER`, and records the local render separately under
     `MTIME_LOCAL_RENDER`. The UTC render is TZ-independent by construction.

  2. SHA-ONLY BLINDNESS. sha256-only custody cannot see a same-content rewrite
     (attack 3, measured in round 1): rewrite the bytes, restore them, and the
     digest is unchanged. v2 adds identification fields that move on any write:
     `INODE`, `CTIME_EPOCH`/`CTIME_NS`, `MTIME_NS`. ctime is the robust pin — a
     user can set mtime back with `os.utime`, but ctime cannot be set.

atime is deliberately NOT captured: reading a file (including this instrument's
own sha256 pass on a relatime mount) can move atime, so an atime field would make
the instrument non-idempotent over its own use.

RECEIPT FORMAT (v2), one stanza per path:

    # receipt-version: 2
    ...
    PATH: /home/vgpnk/.bashrc
    EXISTS: yes
    TYPE: file
    SIZE: 3601
    SHA256: <64 hex>
    MTIME_EPOCH: 1792168396
    MTIME_NS: 1792168396272618342
    MTIME_UTC_RENDER: 2026-10-16T16:33:16Z
    MTIME_LOCAL_RENDER: 2026-10-16T13:33:16-03:00
    CTIME_EPOCH: 1792168396
    CTIME_NS: 1792168396272618342
    CTIME_UTC_RENDER: 2026-10-16T16:33:16Z
    CTIME_LOCAL_RENDER: 2026-10-16T13:33:16-03:00
    INODE: 25991953
    MODE: 644
    UID: 1000
    GID: 1000

EXIT CODES (declared; verify -> worst finding wins):

    0   MATCH             every compared path agrees on every comparable field
    10  CONTENT-DRIFT     sha256 differs on >=1 path
    11  REWRITE-DRIFT     sha256 equal but inode/ctime/mtime moved on >=1 path
                          (the same-content-rewrite class, round-1 attack 3)
    12  METADATA-DRIFT    sha256 + identification times equal but mode/uid/gid/
                          size/type differ, or the candidate side carries a path
                          the reference does not (EXTRA-PATH), or a receipt's own
                          epoch/render pair is inconsistent, or a v1 label defect
                          is reproduced (LABEL-DEFECT)
    13  ABSENT            >=1 reference path missing on the candidate side
    2   USAGE             bad arguments, unreadable/unparsable receipt, refused
                          or failed write
    3   SELFTEST-FAIL     a selftest case failed

    capture exits 0 when every requested path is present (5/5 for the default
    set) and 13 when >=1 requested path is absent; the receipt is still written.

SEVERITY PRECEDENCE (verify): CONTENT-DRIFT > ABSENT > REWRITE-DRIFT >
METADATA-DRIFT > MATCH.

v1 COMPATIBILITY. Three v1 receipt shapes are parsed and compared on the fields
they actually carry (sha256 is the contract):
    stanza-v1  `PATH:/EXISTS:/SIZE:/MTIME_UTC:/MODE: .. UID: .. GID:/SHA256:`
    sums-v1    `sha256sum` output (`<64 hex>  <path>`)
    pipe-v1    `path | inode | ctime | mtime | size | blocks | sha256`
A v1 comparison prints the per-path class `MATCH-V1-PARTIAL` (severity MATCH) and
reports how many fields were comparable; a sha256 mismatch is still
CONTENT-DRIFT. When a v1 time string is present next to a live/receipt epoch, the
instrument renders the epoch both ways and reports `LABEL-DEFECT` if the v1
string matches the local render and not the UTC render.
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import os
import platform
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

RECEIPT_VERSION = 2
TOOL_PATH = Path(__file__).resolve()
SELF = sys.argv[0]

CUSTODY_PATHS = (
    "~/.config/devin/mcp_config.json",
    "~/.omp/agent/mcp.json",
    "~/.kimi-code/config.toml",
    "~/.bashrc",
    "~/.profile",
)

EXIT_MATCH = 0
EXIT_CONTENT_DRIFT = 10
EXIT_REWRITE_DRIFT = 11
EXIT_METADATA_DRIFT = 12
EXIT_ABSENT = 13
EXIT_USAGE = 2
EXIT_SELFTEST_FAIL = 3

SEVERITY = {
    "MATCH": 0,
    "MATCH-V1-PARTIAL": 0,
    "METADATA-DRIFT": 1,
    "REWRITE-DRIFT": 2,
    "ABSENT": 3,
    "CONTENT-DRIFT": 4,
}
EXIT_FOR = {
    "MATCH": EXIT_MATCH,
    "MATCH-V1-PARTIAL": EXIT_MATCH,
    "METADATA-DRIFT": EXIT_METADATA_DRIFT,
    "REWRITE-DRIFT": EXIT_REWRITE_DRIFT,
    "ABSENT": EXIT_ABSENT,
    "CONTENT-DRIFT": EXIT_CONTENT_DRIFT,
}

# Fields compared by verify. Named after the receipt keys.
COMPARE_KEYS = (
    "sha256",
    "size",
    "mtime_epoch",
    "mtime_ns",
    "inode",
    "ctime_epoch",
    "ctime_ns",
    "mode",
    "uid",
    "gid",
    "type",
)

HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


# --------------------------------------------------------------------------- #
# stat + hash (read-only)
# --------------------------------------------------------------------------- #

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render_utc(epoch: float) -> str:
    """UTC render derived from the epoch only — TZ-independent (the v1 label fix)."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch))


def render_local(epoch: float) -> str:
    tm = time.localtime(epoch)
    off = getattr(tm, "tm_gmtoff", None)
    if off is None:  # pragma: no cover - Linux always exposes tm_gmtoff
        off = -time.timezone if not tm.tm_isdst else -time.altzone
    sign = "+" if off >= 0 else "-"
    off = abs(int(off))
    return "%s%s%02d:%02d" % (time.strftime("%Y-%m-%dT%H:%M:%S", tm), sign, off // 3600, (off % 3600) // 60)


def capture_path(path: Path) -> dict:
    """Read-only stat + hash of one path. Never opens a file for writing."""
    fields: dict = {"path": str(path)}
    try:
        st = os.lstat(path)  # lstat: a symlink swap is itself a custody event
    except FileNotFoundError:
        fields["exists"] = "no"
        return fields
    except OSError as exc:
        fields["exists"] = "no"
        fields["stat_error"] = "%s" % exc
        return fields

    fields["exists"] = "yes"
    fields["size"] = st.st_size
    fields["mode"] = "%o" % (st.st_mode & 0o7777)
    fields["uid"] = st.st_uid
    fields["gid"] = st.st_gid
    fields["inode"] = st.st_ino
    fields["mtime_epoch"] = int(st.st_mtime)
    fields["mtime_ns"] = int(st.st_mtime_ns)
    fields["ctime_epoch"] = int(st.st_ctime)
    fields["ctime_ns"] = int(st.st_ctime_ns)
    if os.path.islink(path):
        fields["type"] = "symlink"
        target = os.readlink(path)
        fields["symlink_target"] = target
        fields["sha256"] = hashlib.sha256(target.encode()).hexdigest()
    elif os.path.isfile(path):
        fields["type"] = "file"
        fields["sha256"] = sha256_file(path)
    else:
        fields["type"] = "other"
    return fields


# --------------------------------------------------------------------------- #
# receipt rendering
# --------------------------------------------------------------------------- #

def repo_head(cwd: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(cwd), capture_output=True, text=True, timeout=10,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:
        pass
    return "(none)"


def render_receipt(sections, label: str, now: float) -> str:
    tool_sha = sha256_file(TOOL_PATH) if TOOL_PATH.exists() else "(unavailable)"
    present = sum(1 for s in sections if s.get("exists") == "yes")
    lines = [
        "# custody-pair receipt v%d — READ-ONLY capture (sha256 + stat); no bytes written" % RECEIPT_VERSION,
        "# receipt-version: %d" % RECEIPT_VERSION,
        "# tool: %s  sha256 %s" % (TOOL_PATH.name, tool_sha),
        "# captured-utc: %s" % render_utc(now),
        "# captured-local: %s" % render_local(now),
        "# capture-label: %s" % (label or "(none)"),
        "# host: %s  user: %s  kernel: %s" % (socket.gethostname(), getpass.getuser(), platform.release()),
        "# cwd: %s" % os.getcwd(),
        "# repo-HEAD: %s" % repo_head(Path.cwd()),
        "# paths: %d  present: %d" % (len(sections), present),
        "# label-contract: MTIME_UTC_RENDER/CTIME_UTC_RENDER = gmtime(epoch) renders ('Z');",
        "#                 local renders are recorded separately under *_LOCAL_RENDER.",
        "#                 (v1 printed local time under an MTIME_UTC label — round-1 defect.)",
        "# compare-contract: sha256 = content identity; inode+ctime(+ns) = rewrite identity;",
        "#                   atime deliberately not captured (self-mutating on read).",
    ]
    for sec in sections:
        lines.append("")
        lines.append("PATH: %s" % sec["path"])
        lines.append("EXISTS: %s" % sec.get("exists", "no"))
        if sec.get("stat_error"):
            lines.append("STAT-ERROR: %s" % sec["stat_error"])
        if sec.get("exists") != "yes":
            continue
        lines.append("TYPE: %s" % sec.get("type", "other"))
        lines.append("SIZE: %s" % sec.get("size", ""))
        if "sha256" in sec:
            lines.append("SHA256: %s" % sec["sha256"])
        if "symlink_target" in sec:
            lines.append("SYMLINK-TARGET: %s" % sec["symlink_target"])
        lines.append("MTIME_EPOCH: %s" % sec["mtime_epoch"])
        lines.append("MTIME_NS: %s" % sec["mtime_ns"])
        lines.append("MTIME_UTC_RENDER: %s" % render_utc(sec["mtime_epoch"]))
        lines.append("MTIME_LOCAL_RENDER: %s" % render_local(sec["mtime_epoch"]))
        lines.append("CTIME_EPOCH: %s" % sec["ctime_epoch"])
        lines.append("CTIME_NS: %s" % sec["ctime_ns"])
        lines.append("CTIME_UTC_RENDER: %s" % render_utc(sec["ctime_epoch"]))
        lines.append("CTIME_LOCAL_RENDER: %s" % render_local(sec["ctime_epoch"]))
        lines.append("INODE: %s" % sec["inode"])
        lines.append("MODE: %s" % sec["mode"])
        lines.append("UID: %s" % sec["uid"])
        lines.append("GID: %s" % sec["gid"])
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# receipt parsing (v2 + three v1 shapes)
# --------------------------------------------------------------------------- #

_KEY_PATTERNS = {
    "exists": re.compile(r"^EXISTS:\s*(yes|no)\s*$", re.M),
    "type": re.compile(r"^TYPE:\s*(\w+)\s*$", re.M),
    "size": re.compile(r"^SIZE:\s*(\d+)\s*$", re.M),
    "sha256": re.compile(r"^SHA256:\s*([0-9a-fA-F]{64})\s*$", re.M),
    "mtime_epoch": re.compile(r"^MTIME_EPOCH:\s*(\d+)\s*$", re.M),
    "mtime_ns": re.compile(r"^MTIME_NS:\s*(\d+)\s*$", re.M),
    "mtime_utc_render": re.compile(r"^MTIME_UTC_RENDER:\s*(\S+)\s*$", re.M),
    "mtime_utc_v1": re.compile(r"^MTIME_UTC:\s*(.+?)\s*$", re.M),
    "ctime_epoch": re.compile(r"^CTIME_EPOCH:\s*(\d+)\s*$", re.M),
    "ctime_ns": re.compile(r"^CTIME_NS:\s*(\d+)\s*$", re.M),
    "ctime_utc_v1": re.compile(r"^CTIME_UTC:\s*(.+?)\s*$", re.M),
    "inode": re.compile(r"^INODE:\s*(\d+)\s*$", re.M),
    "mode": re.compile(r"^MODE:\s*(\d+)\s+UID:\s*(\d+)\s+GID:\s*(\d+)\s*$", re.M),
    "mode_only": re.compile(r"^MODE:\s*(\d+)\s*$", re.M),
    "uid_only": re.compile(r"^UID:\s*(\d+)\s*$", re.M),
    "gid_only": re.compile(r"^GID:\s*(\d+)\s*$", re.M),
}


def _parse_section(text: str) -> dict:
    sec: dict = {}
    for key in ("type", "size", "sha256", "mtime_epoch", "mtime_ns", "mtime_utc_render",
                "mtime_utc_v1", "ctime_epoch", "ctime_ns", "ctime_utc_v1", "inode"):
        m = _KEY_PATTERNS[key].search(text)
        if m:
            val = m.group(1)
            if key in ("size", "mtime_epoch", "mtime_ns", "ctime_epoch", "ctime_ns", "inode"):
                val = int(val)
            sec[key] = val
    m = _KEY_PATTERNS["mode"].search(text)
    if m:
        sec["mode"], sec["uid"], sec["gid"] = m.group(1), int(m.group(2)), int(m.group(3))
    else:
        for key, out in (("mode_only", "mode"), ("uid_only", "uid"), ("gid_only", "gid")):
            mm = _KEY_PATTERNS[key].search(text)
            if mm:
                sec[out] = mm.group(1) if out == "mode" else int(mm.group(1))
    m = _KEY_PATTERNS["exists"].search(text)
    sec["exists"] = m.group(1) if m else ("yes" if "sha256" in sec else "no")
    return sec


def parse_receipt(path: Path) -> tuple[str, list[dict]]:
    """Return (format-tag, sections). Raises ValueError on an unparsable receipt."""
    text = path.read_text(encoding="utf-8", errors="replace")
    version = 1
    m = re.search(r"^#\s*receipt-version:\s*(\d+)\s*$", text, re.M)
    if m:
        version = int(m.group(1))

    if re.search(r"^PATH:\s", text, re.M):
        sections = []
        parts = re.split(r"^PATH:\s*", text, flags=re.M)[1:]
        for part in parts:
            body = part.split("\n", 1)
            sec_path = body[0].strip()
            rest = body[1] if len(body) > 1 else ""
            sec = _parse_section(rest)
            sec["path"] = sec_path
            sections.append(sec)
        if not sections:
            raise ValueError("no stanzas parsed from %s" % path)
        fmt = "v2" if any("mtime_epoch" in s for s in sections) else "v1-stanza"
        return fmt, sections

    sections = []
    pipe_lines = 0
    for line in text.splitlines():
        raw = line.rstrip()
        if not raw or raw.lstrip().startswith("#"):
            continue
        parts = [p.strip() for p in raw.split("|")]
        if len(parts) >= 7 and HEX64.match(parts[-1]):
            sections.append({
                "path": parts[0],
                "inode": int(parts[1]) if parts[1].isdigit() else None,
                "ctime_utc_v1": parts[2],
                "mtime_utc_v1": parts[3],
                "size": int(parts[4]) if parts[4].isdigit() else None,
                "sha256": parts[-1].lower(),
                "exists": "yes",
            })
            pipe_lines += 1
            continue
        m = re.match(r"^([0-9a-fA-F]{64})\s\s?(.+?)\s*$", raw)
        if m:
            sections.append({"path": m.group(2), "sha256": m.group(1).lower(), "exists": "yes"})
    if sections:
        return ("pipe-v1" if pipe_lines else "sums-v1"), sections
    raise ValueError("unparsable receipt (no PATH stanzas, sums, or pipe rows): %s" % path)


# --------------------------------------------------------------------------- #
# comparison
# --------------------------------------------------------------------------- #

def _label_audit(ref: dict, cand: dict, notes: list) -> list:
    """Reproduce the v1 label defect when a v1 time string meets an epoch."""
    findings = []
    for v1_key, label, clock in (("mtime_utc_v1", "MTIME_UTC", "mtime"), ("ctime_utc_v1", "CTIME_UTC", "ctime")):
        v1 = ref.get(v1_key) or cand.get(v1_key)
        epoch = cand.get(clock + "_epoch", ref.get(clock + "_epoch"))  # same clock only, never crossed
        if not v1 or epoch is None:
            continue
        loose = re.sub(r"T", " ", v1).replace("Z", "").strip()
        utc_loose = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(epoch))
        local_loose = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(epoch))
        if loose == local_loose and loose != utc_loose:
            findings.append(
                "LABEL-DEFECT: %s says '%s' = localtime(epoch %d); gmtime(epoch) is '%s'"
                % (label, v1.strip(), epoch, utc_loose)
            )
        elif loose != utc_loose:
            notes.append("%s '%s' matches neither gmtime nor localtime(epoch %d)" % (label, v1.strip(), epoch))
    for side_name, sec in (("ref", ref), ("cand", cand)):
        if "mtime_epoch" in sec and "mtime_utc_render" in sec:
            if render_utc(sec["mtime_epoch"]) != sec["mtime_utc_render"]:
                findings.append(
                    "LABEL-INCONSISTENT(%s): epoch %d renders %s, receipt says %s"
                    % (side_name, sec["mtime_epoch"], render_utc(sec["mtime_epoch"]), sec["mtime_utc_render"])
                )
    return findings


def compare_section(ref: dict, cand: dict) -> dict:
    """Classify one path. Returns {finding, moved, compared, comparable, notes, label_findings}."""
    notes: list = []
    label_findings = _label_audit(ref, cand, notes)

    ref_exists = ref.get("exists", "no") == "yes" or "sha256" in ref
    cand_exists = cand.get("exists", "no") == "yes" or "sha256" in cand
    comparable = sum(1 for k in COMPARE_KEYS if k in ref and k in cand)
    if not ref_exists and not cand_exists:
        return {"finding": "MATCH", "moved": [], "compared": 0, "comparable": 0,
                "notes": notes, "label_findings": label_findings}
    if ref_exists and not cand_exists:
        return {"finding": "ABSENT", "moved": ["exists"], "compared": 0, "comparable": comparable,
                "notes": notes, "label_findings": label_findings}
    if cand_exists and not ref_exists:
        return {"finding": "ABSENT", "moved": ["exists"], "compared": 0, "comparable": comparable,
                "notes": notes, "label_findings": label_findings}

    compared = 0
    diffs: list = []
    if "sha256" in ref and "sha256" in cand:
        compared += 1
    for key in ("size", "mtime_epoch", "mtime_ns", "inode", "ctime_epoch", "ctime_ns",
                "mode", "uid", "gid", "type"):
        if key in ref and key in cand:
            compared += 1

    if "sha256" in ref and "sha256" in cand and ref["sha256"] != cand["sha256"]:
        return {"finding": "CONTENT-DRIFT", "moved": ["sha256"], "compared": compared,
                "comparable": comparable, "notes": notes, "label_findings": label_findings}

    for key in ("inode", "mtime_ns", "mtime_epoch"):
        if key in ref and key in cand and ref[key] != cand[key]:
            diffs.append(key)
    if diffs:
        finding = "REWRITE-DRIFT"
    else:
        meta = [k for k in ("mode", "uid", "gid", "size", "type")
                if k in ref and k in cand and ref[k] != cand[k]]
        ctime = [k for k in ("ctime_ns", "ctime_epoch")
                 if k in ref and k in cand and ref[k] != cand[k]]
        if meta:
            finding, diffs = "METADATA-DRIFT", meta + ctime
        elif ctime:
            finding, diffs = "REWRITE-DRIFT", ctime
        else:
            finding = "MATCH"

    if finding == "MATCH" and compared < len(COMPARE_KEYS):
        finding = "MATCH-V1-PARTIAL"
    if label_findings and finding in ("MATCH", "MATCH-V1-PARTIAL"):
        finding = "METADATA-DRIFT"
    return {"finding": finding, "moved": diffs, "compared": compared, "comparable": comparable,
            "notes": notes, "label_findings": label_findings}


def verify_sets(ref_sections, cand_sections, a_name, b_name):
    ref_by = {s["path"]: s for s in ref_sections}
    cand_by = {s["path"]: s for s in cand_sections}
    rows = []
    for path in list(ref_by) + [p for p in cand_by if p not in ref_by]:
        ref = ref_by.get(path)
        cand = cand_by.get(path)
        if ref is None:
            rows.append({"path": path, "finding": "METADATA-DRIFT", "moved": ["EXTRA-PATH"],
                         "compared": 0, "comparable": 0, "notes": ["path present only on candidate side"],
                         "label_findings": [], "sha_agree": None})
            continue
        if cand is None:
            rows.append({"path": path, "finding": "ABSENT", "moved": ["missing"], "compared": 0,
                         "comparable": 0, "notes": ["path present only in reference"],
                         "label_findings": [], "sha_agree": None})
            continue
        row = compare_section(ref, cand)
        row["path"] = path
        row["sha_agree"] = (ref["sha256"] == cand["sha256"]) if ("sha256" in ref and "sha256" in cand) else None
        rows.append(row)

    worst = max(rows, key=lambda r: SEVERITY[r["finding"]])["finding"] if rows else "MATCH"
    exit_code = EXIT_FOR[worst]
    print("CUSTODY-PAIR VERIFY (v%d instrument)" % RECEIPT_VERSION)
    print("A (reference): %s  stanzas=%d" % (a_name, len(ref_sections)))
    print("B (candidate): %s  stanzas=%d" % (b_name, len(cand_sections)))
    counts: dict = {}
    for row in rows:
        counts[row["finding"]] = counts.get(row["finding"], 0) + 1
        detail = "compared=%d/%d" % (row["compared"], len(COMPARE_KEYS))
        if row["moved"]:
            detail += " moved=%s" % ",".join(row["moved"])
        print("PATH %s: %s  %s" % (row["path"], row["finding"], detail))
        for note in row["notes"]:
            print("    note: %s" % note)
        for lf in row["label_findings"]:
            print("    %s" % lf)
    sha_pairs = [r for r in rows if r["sha_agree"] is not None]
    sha_agree = sum(1 for r in sha_pairs if r["sha_agree"])
    print("SHA256-CONTRACT: %d/%d paths agree on sha256 (v1/v2 receipts compare on this field)"
          % (sha_agree, len(sha_pairs)))
    summary = " ".join("%s=%d" % (k, counts[k]) for k in sorted(counts))
    print("VERDICT: %s  paths=%d  %s  exit=%d" % (worst, len(rows), summary or "none", exit_code))
    print("CUSTODY_PAIR_VERIFY: %s paths=%d/%d drift=%d exit=%d"
          % (worst, sum(1 for r in rows if SEVERITY[r["finding"]] == 0), len(rows),
             sum(1 for r in rows if SEVERITY[r["finding"]] > 0), exit_code))
    return exit_code


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #

def default_scratch() -> Path:
    for cand in (os.environ.get("CUSTODY_PAIR_SCRATCH"), "/dev/shm", "/var/tmp"):
        if not cand:
            continue
        p = Path(cand)
        if p.is_dir() and os.access(p, os.W_OK):
            return p
    raise SystemExit("USAGE: no writable scratch dir (/dev/shm, /var/tmp); /tmp is excluded (EDQUOT hazard)")


def warn_if_tmp(path: Path) -> None:
    if str(path).startswith("/tmp"):
        print("WARN: /tmp is quota-exhausted on this host (EDQUOT); prefer /dev/shm or /var/tmp", file=sys.stderr)


def cmd_paths(_args) -> int:
    for p in CUSTODY_PATHS:
        print(p)
    return EXIT_MATCH


def cmd_capture(args) -> int:
    paths = [Path(p).expanduser() for p in (args.paths or CUSTODY_PATHS)]
    sections = [capture_path(p) for p in paths]
    now = time.time()
    text = render_receipt(sections, args.label, now)
    present = sum(1 for s in sections if s.get("exists") == "yes")
    exit_code = EXIT_MATCH if present == len(sections) else EXIT_ABSENT

    if args.out == "-":
        sys.stdout.write(text)
    else:
        out = Path(args.out).expanduser()
        warn_if_tmp(out)
        if out.resolve() in {Path(p).expanduser().resolve() for p in CUSTODY_PATHS}:
            print("USAGE: refusing to write a receipt over a custody path: %s" % out, file=sys.stderr)
            return EXIT_USAGE
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            out.write_text(text, encoding="utf-8")
            digest = sha256_file(out)
            sidecar = out.with_name(out.name + ".sha256")
            sidecar.write_text("%s  %s\n" % (digest, out.name), encoding="utf-8")
        except OSError as exc:
            print("USAGE: write failed (%s): %s" % (exc, out), file=sys.stderr)
            return EXIT_USAGE
        print("RECEIPT: %s  sha256=%s" % (out, digest))
        print("SIDECAR: %s" % sidecar)
    print("CUSTODY_PAIR_CAPTURE: %s paths=%d/%d label=%s exit=%d"
          % ("OK" if exit_code == EXIT_MATCH else "PARTIAL", present, len(sections),
             args.label or "(none)", exit_code))
    return exit_code


def cmd_verify(args) -> int:
    try:
        a_fmt, a_sections = parse_receipt(Path(args.receipt_a).expanduser())
    except (OSError, ValueError) as exc:
        print("USAGE: %s" % exc, file=sys.stderr)
        return EXIT_USAGE

    if args.live:
        b_fmt, b_name = "live", "live filesystem"
        b_sections = [capture_path(Path(s["path"]).expanduser()) for s in a_sections]
    else:
        if not args.receipt_b:
            print("USAGE: verify needs RECEIPT_B or --live", file=sys.stderr)
            return EXIT_USAGE
        try:
            b_fmt, b_sections = parse_receipt(Path(args.receipt_b).expanduser())
            b_name = str(args.receipt_b)
        except (OSError, ValueError) as exc:
            print("USAGE: %s" % exc, file=sys.stderr)
            return EXIT_USAGE

    print("A format: %s   B format: %s" % (a_fmt, b_fmt))
    return verify_sets(a_sections, b_sections, str(args.receipt_a), b_name)


# --------------------------------------------------------------------------- #
# selftest (fixtures only — never touches a custody path)
# --------------------------------------------------------------------------- #

def run_case(cases: list, name: str, fn) -> None:
    try:
        fn()
        cases.append((name, True, ""))
    except AssertionError as exc:
        cases.append((name, False, str(exc) or "assertion failed"))
    except Exception as exc:  # pragma: no cover - defensive
        cases.append((name, False, "%s: %s" % (type(exc).__name__, exc)))


def cmd_selftest(args) -> int:
    import tempfile

    base = Path(args.scratch).expanduser() if args.scratch else default_scratch()
    if str(base).startswith("/tmp") and not args.scratch:
        print("USAGE: /tmp is excluded scratch (EDQUOT hazard)", file=sys.stderr)
        return EXIT_USAGE
    root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))

    def capture_to(out_name: str, paths, label="selftest"):
        out = root / out_name
        rc = cmd_capture(argparse.Namespace(out=str(out), paths=[str(p) for p in paths],
                                            label=label))
        return out, rc

    fixture = root / "fixture.conf"
    payload = b"custody-pair selftest fixture\n"
    fixture.write_bytes(payload)
    os.utime(fixture, (1000000000, 1000000000))
    pre, rc_pre = capture_to("pre.txt", [fixture])

    cases: list = []

    run_case(cases, "capture-ok-exit-0", lambda: (
        None if rc_pre == EXIT_MATCH else (_ for _ in ()).throw(AssertionError("capture exit %d" % rc_pre))))
    run_case(cases, "receipt-shape-v2-fields", lambda: (
        None if all(k in pre.read_text() for k in
                    ("PATH:", "SHA256:", "MTIME_EPOCH:", "MTIME_UTC_RENDER:", "CTIME_EPOCH:",
                     "CTIME_UTC_RENDER:", "INODE:", "MTIME_NS:", "CTIME_NS:"))
        else (_ for _ in ()).throw(AssertionError("missing v2 field"))))
    run_case(cases, "sidecar-self-hash", lambda: (
        None if pre.with_name("pre.txt.sha256").read_text().split()[0] == sha256_file(pre)
        else (_ for _ in ()).throw(AssertionError("sidecar digest mismatch"))))

    # 1. self-verify is idempotent
    def case_self():
        out = root / "self-verify.out"
        rc = _run_verify([str(pre), "--live"], out)
        assert rc == EXIT_MATCH, "expected MATCH exit 0, got %d" % rc
        assert "VERDICT: MATCH" in out.read_text(), "no MATCH verdict"
    run_case(cases, "verify-receipt-vs-live-clean", case_self)

    # 2. same-content rewrite, in place, mtime restored -> only ctime moves
    def case_ctime_only():
        before = capture_path(fixture)
        fixture.write_bytes(payload)
        os.utime(fixture, ns=(before["mtime_ns"] * 0 + 1000000000 * 10 ** 9,
                              before["mtime_ns"]))
        after = capture_path(fixture)
        assert before["inode"] == after["inode"], "in-place write changed the inode (fixture setup)"
        assert before["mtime_ns"] == after["mtime_ns"], "mtime not restored (fixture setup)"
        assert before["ctime_ns"] != after["ctime_ns"], "ctime did not move (instrument blind spot)"
        out = root / "ctime-only.out"
        rc = _run_verify([str(pre), "--live"], out)
        assert rc == EXIT_REWRITE_DRIFT, "expected REWRITE-DRIFT exit %d, got %d" % (EXIT_REWRITE_DRIFT, rc)
        assert "REWRITE-DRIFT" in out.read_text(), "no REWRITE-DRIFT class printed"
    run_case(cases, "same-content-rewrite-inplace-ctime-pin", case_ctime_only)

    # 3. same-content rewrite via temp+rename -> inode moves
    def case_rename():
        tmp = root / "fixture.conf.new"
        tmp.write_bytes(payload)
        os.utime(tmp, ns=(1000000000 * 10 ** 9, 1000000000 * 10 ** 9))
        os.replace(tmp, fixture)
        os.utime(fixture, ns=(1000000000 * 10 ** 9, 1000000000 * 10 ** 9))
        out = root / "rename.out"
        rc = _run_verify([str(pre), "--live"], out)
        assert rc == EXIT_REWRITE_DRIFT, "expected REWRITE-DRIFT exit %d, got %d" % (EXIT_REWRITE_DRIFT, rc)
    run_case(cases, "same-content-rewrite-rename-inode-pin", case_rename)

    # 4. content drift
    def case_content():
        fixture.write_bytes(payload + b"tampered\n")
        out = root / "content.out"
        rc = _run_verify([str(pre), "--live"], out)
        assert rc == EXIT_CONTENT_DRIFT, "expected CONTENT-DRIFT exit %d, got %d" % (EXIT_CONTENT_DRIFT, rc)
    run_case(cases, "content-drift-detected", case_content)

    # 5. absent path
    def case_absent():
        gone = root / "fixture-gone.conf"
        gone.write_bytes(b"x")
        out_rec, rc = capture_to("gone-pre.txt", [gone])
        assert rc == EXIT_MATCH, "reference capture exit %d" % rc
        gone.unlink()
        out = root / "absent.out"
        rc = _run_verify([str(out_rec), "--live"], out)
        assert rc == EXIT_ABSENT, "expected ABSENT exit %d, got %d" % (EXIT_ABSENT, rc)
    run_case(cases, "absent-path-detected", case_absent)

    # 6. metadata drift (mode change; content + mtime untouched)
    def case_mode():
        other = root / "fixture-mode.conf"
        other.write_bytes(payload)
        os.utime(other, (1000000000, 1000000000))
        rec, rc = capture_to("mode-pre.txt", [other])
        assert rc == EXIT_MATCH, "reference capture exit %d" % rc
        os.chmod(other, 0o600)
        out = root / "mode.out"
        rc = _run_verify([str(rec), "--live"], out)
        assert rc == EXIT_METADATA_DRIFT, "expected METADATA-DRIFT exit %d, got %d" % (EXIT_METADATA_DRIFT, rc)
    run_case(cases, "metadata-drift-detected", case_mode)

    # 7. label correctness + TZ independence (the v1 defect regression)
    fixture2 = root / "fixture-label.conf"
    fixture2.write_bytes(b"label fixture\n")
    epoch = 1792011200  # 2026-10-14T20:53:20Z, the round-1 defect epoch
    os.utime(fixture2, (epoch, epoch))

    def case_label():
        src = (Path(__file__).resolve().parent / "custody-pair.py")
        env = dict(os.environ)
        renders = {}
        for tz in ("UTC", "UTC-3", "UTC+5"):
            env["TZ"] = tz
            out = subprocess.run([sys.executable, str(src), "capture", "--out", "-",
                                  "--paths", str(fixture2)],
                                 capture_output=True, text=True, env=env)
            assert out.returncode == 0, "capture failed under TZ=%s: %s" % (tz, out.stderr)
            line = [l for l in out.stdout.splitlines() if l.startswith("MTIME_UTC_RENDER:")]
            assert line, "no MTIME_UTC_RENDER under TZ=%s" % tz
            renders[tz] = line[0].split(":", 1)[1].strip()
            if tz == "UTC+5":
                local_line = [l for l in out.stdout.splitlines() if l.startswith("MTIME_LOCAL_RENDER:")]
                assert local_line, "no MTIME_LOCAL_RENDER"
                assert local_line[0].split(":", 1)[1].strip() != renders["UTC"], \
                    "local render equals UTC render under TZ=UTC+5 (fixture setup)"
        assert len(set(renders.values())) == 1, "MTIME_UTC_RENDER is TZ-dependent: %s" % renders
        assert renders["UTC"] == "2026-10-14T20:53:20Z", "UTC render != gmtime(epoch): %s" % renders["UTC"]
    run_case(cases, "label-utc-render-tz-independent", case_label)

    # 8. v1 stanza compat (+ mutation detection)
    def case_v1stanza():
        sec = capture_path(fixture2)
        v1 = root / "v1-stanza.txt"
        v1.write_text(
            "# v1-shaped receipt (fixture)\n"
            "PATH: %s\nEXISTS: yes\nSIZE: %d\n"
            "MTIME_UTC: %s\nMODE: %s  UID: %d  GID: %d\nSHA256: %s\n" % (
                sec["path"], sec["size"],
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sec["mtime_epoch"])),
                sec["mode"], sec["uid"], sec["gid"], sec["sha256"]),
            encoding="utf-8")
        out = root / "v1-stanza.out"
        rc = _run_verify([str(v1), "--live"], out)
        assert rc == EXIT_METADATA_DRIFT, "expected METADATA-DRIFT (LABEL-DEFECT) exit %d, got %d" % (
            EXIT_METADATA_DRIFT, rc)
        text = out.read_text()
        assert "LABEL-DEFECT" in text, "v1 label defect not reported"
        assert "MATCH-V1-PARTIAL" not in text or "LABEL-DEFECT" in text, "class precedence wrong"
        mutated = root / "v1-stanza-mutated.txt"
        bad = sec["sha256"][:-1] + ("0" if sec["sha256"][-1] != "0" else "1")
        mutated.write_text(v1.read_text().replace(sec["sha256"], bad), encoding="utf-8")
        out2 = root / "v1-stanza-mutated.out"
        rc2 = _run_verify([str(mutated), "--live"], out2)
        assert rc2 == EXIT_CONTENT_DRIFT, "expected CONTENT-DRIFT exit %d, got %d" % (EXIT_CONTENT_DRIFT, rc2)
    run_case(cases, "v1-stanza-compat-and-mutation", case_v1stanza)

    # 9. sums-v1 compat
    def case_sums():
        sec = capture_path(fixture2)
        sums = root / "v1-sums.txt"
        sums.write_text("%s  %s\n" % (sec["sha256"], sec["path"]), encoding="utf-8")
        out = root / "v1-sums.out"
        rc = _run_verify([str(sums), "--live"], out)
        assert rc == EXIT_MATCH, "expected MATCH exit 0 on sums-v1, got %d" % rc
        assert "MATCH-V1-PARTIAL" in out.read_text(), "v1-partial class not printed"
    run_case(cases, "sums-v1-compat", case_sums)

    # 10. pipe-v1 compat
    def case_pipe():
        sec = capture_path(fixture2)
        pipe = root / "v1-pipe.txt"
        pipe.write_text("%s | %d | %s | %s | %d | 8 | %s\n" % (
            sec["path"], sec["inode"],
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sec["ctime_epoch"])),
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sec["mtime_epoch"])),
            sec["size"], sec["sha256"]), encoding="utf-8")
        out = root / "v1-pipe.out"
        rc = _run_verify([str(pipe), "--live"], out)
        assert rc in (EXIT_MATCH, EXIT_METADATA_DRIFT), "unexpected exit %d" % rc
        assert "pipe-v1" in out.read_text(), "pipe format not detected"
    run_case(cases, "pipe-v1-compat", case_pipe)

    # 11. unparsable receipt -> usage exit 2, not a silent pass
    def case_unparsable():
        junk = root / "junk.txt"
        junk.write_text("not a receipt at all\n", encoding="utf-8")
        out = root / "junk.out"
        rc = _run_verify([str(junk), "--live"], out)
        assert rc == EXIT_USAGE, "expected USAGE exit 2 for unparsable receipt, got %d" % rc
    run_case(cases, "unparsable-receipt-usage-exit", case_unparsable)

    # 12. read-only guard: refuse to write a receipt over a custody path
    def case_guard():
        target = Path(CUSTODY_PATHS[3]).expanduser()
        before = capture_path(target)
        rc = cmd_capture(argparse.Namespace(out=str(target), paths=list(CUSTODY_PATHS), label="guard"))
        after = capture_path(target)
        assert rc == EXIT_USAGE, "expected USAGE exit 2, got %d" % rc
        assert before == after, "custody path changed during the guard case"
    run_case(cases, "refuses-to-write-over-custody-path", case_guard)

    passed = sum(1 for _, ok, _ in cases if ok)
    for name, ok, why in cases:
        print("case %-42s %s%s" % (name, "PASS" if ok else "FAIL", ("  (%s)" % why) if why else ""))
    failed = len(cases) - passed
    print("scratch: %s" % root)
    print("CUSTODY_PAIR_SELFTEST: %s cases=%d passed=%d failed=%d exit=%d"
          % ("CLEAN" if failed == 0 else "DIRTY", len(cases), passed, failed,
             EXIT_MATCH if failed == 0 else EXIT_SELFTEST_FAIL))
    return EXIT_MATCH if failed == 0 else EXIT_SELFTEST_FAIL


def _run_verify(argv, out_path: Path) -> int:
    """Run the verify path in-process, capturing stdout to out_path."""
    import io
    import contextlib
    ns = argparse.Namespace(receipt_a=argv[0], receipt_b=None, live=False)
    for item in argv[1:]:
        if item == "--live":
            ns.live = True
        else:
            ns.receipt_b = item
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = cmd_verify(ns)
    text = buf.getvalue()
    out_path.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return rc


# --------------------------------------------------------------------------- #

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="custody-pair.py",
        description="v2 custody receipt instrument (capture/verify/selftest) for the 5 frozen paths.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_cap = sub.add_parser("capture", help="write a v2 receipt (read-only over the paths)")
    p_cap.add_argument("--out", required=True, help="receipt path, or '-' for stdout")
    p_cap.add_argument("--label", default="", help="capture label recorded in the header")
    p_cap.add_argument("--paths", nargs="*", default=None, help="override paths (default: the 5 custody paths)")
    p_cap.set_defaults(func=cmd_capture)

    p_ver = sub.add_parser("verify", help="compare two receipts, or a receipt against the live filesystem")
    p_ver.add_argument("receipt_a", help="reference receipt")
    p_ver.add_argument("receipt_b", nargs="?", default=None, help="candidate receipt")
    p_ver.add_argument("--live", action="store_true", help="compare receipt_a against the live filesystem")
    p_ver.set_defaults(func=cmd_verify)

    p_self = sub.add_parser("selftest", help="fixture-based selftest (never touches a custody path)")
    p_self.add_argument("--scratch", default=None, help="fixture root (default: $CUSTODY_PAIR_SCRATCH, /dev/shm, /var/tmp)")
    p_self.set_defaults(func=cmd_selftest)

    p_paths = sub.add_parser("paths", help="print the 5 canonical custody paths")
    p_paths.set_defaults(func=cmd_paths)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
