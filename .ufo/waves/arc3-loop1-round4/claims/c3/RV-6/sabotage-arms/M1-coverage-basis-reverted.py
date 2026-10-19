#!/usr/bin/env python3
"""custody-pair gate (v2; seats EX-31 wave arc3-loop1-round2, EX-21 wave arc3-loop1-round3).

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

ROUND-3 HARDENING (seat EX-21, wave arc3-loop1-round3). Each hole below was
measured in round 2 (arc3-loop1-round2, chain c3); the round-2 tree carries the
measuring seats and the patch texts this revision applies:

  3. UNEVALUABLE (exit 14, round-2 debt D2). A path that exists but cannot be
     evaluated is recorded instead of crashing the capture: `EXISTS: yes` +
     `TYPE: file` + `READ-ERROR: ...` for an unreadable regular file, and
     `EXISTS: no` + `STAT-ERROR: ...` when even lstat fails (EACCES on a parent
     directory). The receipt is still written; capture exits 14. `verify`
     classifies such a stanza UNEVALUABLE *before* the both-absent MATCH branch
     — fail-closed, because the round-2 tool read an EACCES path as `MATCH
     exit 0` (the fail-open defect). `STAT-ERROR:`/`READ-ERROR:` are parsed
     from receipts, so receipt-vs-receipt comparison is fail-closed too.
  4. REFERENCE COVERAGE (round-2 debt D3). `verify --require-paths N` exits 2
     (USAGE class) with a `REFERENCE-COVERAGE: n/N paths present in reference;
     unaccounted: <list>` line when the reference carries fewer than N paths.
     A 1-of-5 receipt can no longer read exit 0 with the other four custody
     paths unexamined.
  5. WRITE-GUARD SCOPE (VZ-4 A11 + RV-11 D7). `capture` refuses `--out` when
     the output would resolve to — or share an inode with — any path being
     captured OR any of the five custody paths. `--paths X --out X` no longer
     clobbers the scoped file it measures, and a hardlink alias of a guarded
     path is refused through the inode arm. Scope statement: this remains a
     self-harm guard, not a security boundary (an actor able to create the
     alias can already write the file; TOCTOU is inherent and out of scope).
     Item 7 below (round 4) extends the same guard to the derived sidecar path
     and to sidecar-shaped neighbours of the measured paths.
  6. SCRATCH GUARD (round-2 debt D6). `selftest --scratch <dir>` on a
     missing or unusable directory is a declared USAGE exit 2 (with a message),
     not a raw `FileNotFoundError` traceback at exit 1.

ROUND-4 HARDENING (seat EX-21, wave arc3-loop1-round4). Three residuals named by
the round-3 verdict; each was re-measured on the round-3 landed revision before
this revision was written:

  7. SIDECAR / NEIGHBOUR WRITE-GUARD SCOPE (residual (a); RV-8's `capture --out
     X --paths X.sha256` probe). The guard now examines the receipt path AND its
     derived sidecar path (`out.name + ".sha256"`), each against the measured
     paths and the five custody paths by resolved path and by inode, and refuses
     a receipt/sidecar landing on the sidecar-shaped neighbour (`<measured> +
     ".sha256"`) of a measured path. Before this revision that probe exited 0
     and the sidecar write destroyed X.sha256 — the very file the same run had
     just measured. The sidecar name is derived inside the guarded region: an
     `--out` with no usable name (`''`, `'.'`) is a declared USAGE exit 2, not a
     `ValueError` traceback (CR-4 item 6's trap).
  8. RECEIPT-DIRECTORY FAILURES (residual (b); CR-3/CR-4's `capture --out
     <regular-file>/sub/r.txt` probe). `out.parent.mkdir(...)` now runs inside a
     guarded block: a non-directory component (NotADirectoryError), a symlink
     loop (ELOOP), or any other OSError is a declared USAGE exit 2 with a
     message, not a raw traceback at exit 1.
  9. COVERAGE-GATE BASIS (residual (c); EX-24's duplicate-stanza vector).
     `--require-paths N` counts DISTINCT RESOLVED PATHS, the same basis as its
     own `unaccounted:` list. Five duplicate stanzas for one path used to
     satisfy `--require-paths 5` silently (exit 0, no coverage line printed);
     they now read `REFERENCE-COVERAGE: 1/5 ...` and exit 2.

BOTH-SIDES-ABSENT RULING (residual (d), adjudicated in round 4). Two stanzas
that both record `EXISTS: no` and carry NO error line compare as MATCH: the
instrument's contract is agreement between the two sides on every comparable
field, and "absent" is a comparable state. This is the declared design — only
error-carrying stanzas (`STAT-ERROR`/`READ-ERROR`) are UNEVALUABLE, and those
are classified before this branch. Such a verdict is an agreement on absence,
not a verified presence: the row carries the note `both sides record the path
absent`, and the run still prints `SHA256-CONTRACT: 0/0` — a reader must not
read it as a satisfied content contract. Closing this with a flag was considered
and rejected: the round-3 evidence is that the fail-open lived in the
error-carrying form, which the UNEVALUABLE class already closes.

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

An unevaluable stanza carries `READ-ERROR: <errno message>` (exists but
unreadable) or `STAT-ERROR: <errno message>` (lstat failed) and omits SHA256.

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
    14  UNEVALUABLE       a path exists but could not be evaluated (EACCES on
                          open, or a stat error other than ENOENT); the receipt
                          is still written, carrying STAT-ERROR/READ-ERROR
    2   USAGE             bad arguments, unreadable/unparsable receipt, refused
                          or failed write (including a receipt or sidecar aimed
                          at a measured path, a custody path, or the
                          sidecar-shaped neighbour of a measured path, and a
                          receipt directory that cannot be created),
                          insufficient reference coverage under --require-paths,
                          unusable selftest scratch dir
    3   SELFTEST-FAIL     a selftest case failed

    capture exits 0 when every requested path is present (5/5 for the default
    set), 14 when >=1 path is present-but-unevaluable, else 13 when >=1
    requested path is absent; the receipt is still written.

SEVERITY PRECEDENCE (verify): CONTENT-DRIFT > UNEVALUABLE > ABSENT >
REWRITE-DRIFT > METADATA-DRIFT > MATCH.

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
EXIT_UNEVALUABLE = 14
EXIT_USAGE = 2
EXIT_SELFTEST_FAIL = 3

SEVERITY = {
    "MATCH": 0,
    "MATCH-V1-PARTIAL": 0,
    "METADATA-DRIFT": 1,
    "REWRITE-DRIFT": 2,
    "ABSENT": 3,
    "UNEVALUABLE": 4,
    "CONTENT-DRIFT": 5,
}
EXIT_FOR = {
    "MATCH": EXIT_MATCH,
    "MATCH-V1-PARTIAL": EXIT_MATCH,
    "METADATA-DRIFT": EXIT_METADATA_DRIFT,
    "REWRITE-DRIFT": EXIT_REWRITE_DRIFT,
    "ABSENT": EXIT_ABSENT,
    "UNEVALUABLE": EXIT_UNEVALUABLE,
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


def _same_file(a: Path, b: Path) -> bool:
    """True when both paths currently denote the same inode (os.stat follows symlinks)."""
    try:
        sa, sb = os.stat(a), os.stat(b)
    except OSError:
        return False
    return (sa.st_dev, sa.st_ino) == (sb.st_dev, sb.st_ino)


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
        try:
            fields["sha256"] = sha256_file(path)
        except OSError as exc:  # exists but not evaluable (e.g. EACCES)
            fields["read_error"] = "%s" % exc
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
        if sec.get("read_error"):
            lines.append("READ-ERROR: %s" % sec["read_error"])
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
    "stat_error": re.compile(r"^STAT-ERROR:\s*(.+?)\s*$", re.M),
    "read_error": re.compile(r"^READ-ERROR:\s*(.+?)\s*$", re.M),
    "mode": re.compile(r"^MODE:\s*(\d+)\s+UID:\s*(\d+)\s+GID:\s*(\d+)\s*$", re.M),
    "mode_only": re.compile(r"^MODE:\s*(\d+)\s*$", re.M),
    "uid_only": re.compile(r"^UID:\s*(\d+)\s*$", re.M),
    "gid_only": re.compile(r"^GID:\s*(\d+)\s*$", re.M),
}


def _parse_section(text: str) -> dict:
    sec: dict = {}
    for key in ("type", "size", "sha256", "mtime_epoch", "mtime_ns", "mtime_utc_render",
                "mtime_utc_v1", "ctime_epoch", "ctime_ns", "ctime_utc_v1", "inode",
                "stat_error", "read_error"):
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
        fmt = "v2" if (version >= 2 or any("mtime_epoch" in s for s in sections)) else "v1-stanza"
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
    ref_uneval = bool(ref.get("stat_error") or ref.get("read_error"))
    cand_uneval = bool(cand.get("stat_error") or cand.get("read_error"))
    if ref_uneval or cand_uneval:
        sides = "+".join(n for n, u in (("reference", ref_uneval), ("candidate", cand_uneval)) if u)
        return {"finding": "UNEVALUABLE", "moved": ["unevaluable"], "compared": 0,
                "comparable": comparable,
                "notes": notes + ["exists but not evaluable on %s side" % sides],
                "label_findings": label_findings}
    if not ref_exists and not cand_exists:
        return {"finding": "MATCH", "moved": [], "compared": 0, "comparable": 0,
                "notes": notes + ["both sides record the path absent — the MATCH is an agreement"
                                  " on absence, not a verified presence (declared ruling: only"
                                  " error-carrying stanzas are UNEVALUABLE)"],
                "label_findings": label_findings}
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


def distinct_paths(sections) -> set:
    """The coverage basis: distinct RESOLVED paths. A duplicate stanza adds none
    (round-3 residual (c) — the count and `unaccounted:` share this basis)."""
    return {Path(s["path"]).expanduser().resolve() for s in sections}


def reference_coverage(ref_sections, required: int) -> tuple[bool, str]:
    """--require-paths gate (round-2 debt D3; basis fixed in round 4): does the
    reference account for `required` DISTINCT resolved paths? Returns (ok, line);
    `unaccounted` lists the canonical custody paths absent from the reference."""
    have = distinct_paths(ref_sections)
    unaccounted = [p for p in CUSTODY_PATHS if Path(p).expanduser().resolve() not in have]
    line = ("REFERENCE-COVERAGE: %d/%d paths present in reference; unaccounted: %s"
            % (len(have), required, " ".join(unaccounted) if unaccounted else "(none)"))
    return len(ref_sections) >= required, line


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
    unevaluable = sum(1 for s in sections
                      if s.get("stat_error") or s.get("read_error")
                      or (s.get("exists") == "yes" and s.get("type") == "file" and "sha256" not in s))
    if unevaluable:
        exit_code = EXIT_UNEVALUABLE
    elif present == len(sections):
        exit_code = EXIT_MATCH
    else:
        exit_code = EXIT_ABSENT

    if args.out == "-":
        sys.stdout.write(text)
    else:
        out = Path(args.out).expanduser()
        warn_if_tmp(out)
        try:
            sidecar = out.with_name(out.name + ".sha256")
        except ValueError:
            print("USAGE: --out carries no usable name, so no sidecar path can be derived: %r"
                  % args.out, file=sys.stderr)
            return EXIT_USAGE
        guarded = [Path(p).expanduser() for p in CUSTODY_PATHS] + paths
        try:
            guarded_names = {g.resolve() for g in guarded}
            neighbours = {Path(str(g) + ".sha256").resolve() for g in guarded}
            candidates = ((out, out.resolve()), (sidecar, sidecar.resolve()))
        except OSError as exc:  # unresolvable --out or measured path: fail closed, USAGE
            print("USAGE: cannot resolve the receipt or a guarded path (%s): %s" % (exc, out),
                  file=sys.stderr)
            return EXIT_USAGE
        for cand, cand_res in candidates:
            if (cand_res in guarded_names or cand_res in neighbours
                    or any(_same_file(cand, g) for g in guarded)):
                print("USAGE: refusing to write a receipt or its derived sidecar over a path it"
                      " measures, a custody path, or the sidecar-shaped neighbour of one"
                      " (resolved path or inode): %s" % cand, file=sys.stderr)
                return EXIT_USAGE
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:  # e.g. a path component is a regular file, or ELOOP
            print("USAGE: cannot create the receipt directory (%s): %s" % (exc, out.parent),
                  file=sys.stderr)
            return EXIT_USAGE
        try:
            out.write_text(text, encoding="utf-8")
            digest = sha256_file(out)
            sidecar.write_text("%s  %s\n" % (digest, out.name), encoding="utf-8")
        except OSError as exc:
            print("USAGE: write failed (%s): %s" % (exc, out), file=sys.stderr)
            return EXIT_USAGE
        print("RECEIPT: %s  sha256=%s" % (out, digest))
        print("SIDECAR: %s" % sidecar)
    state = {EXIT_MATCH: "OK", EXIT_UNEVALUABLE: "UNEVALUABLE"}.get(exit_code, "PARTIAL")
    print("CUSTODY_PAIR_CAPTURE: %s paths=%d/%d label=%s exit=%d"
          % (state, present, len(sections), args.label or "(none)", exit_code))
    return exit_code


def cmd_verify(args) -> int:
    try:
        a_fmt, a_sections = parse_receipt(Path(args.receipt_a).expanduser())
    except (OSError, ValueError) as exc:
        print("USAGE: %s" % exc, file=sys.stderr)
        return EXIT_USAGE

    require = getattr(args, "require_paths", None)
    if require:  # falsy (None/0) = no gate — the declared default; opt-in by design
        ok, line = reference_coverage(a_sections, require)
        if not ok:
            print(line)
            print("USAGE: reference covers %d of the required %d distinct paths"
                  % (len(distinct_paths(a_sections)), require), file=sys.stderr)
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
    base_s = str(base)
    if base_s == "/tmp" or base_s.startswith("/tmp/"):
        print("USAGE: /tmp is excluded scratch (EDQUOT hazard)", file=sys.stderr)
        return EXIT_USAGE
    if not base.is_dir():
        print("USAGE: scratch base is not a directory: %s" % base, file=sys.stderr)
        return EXIT_USAGE
    try:
        root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))
    except OSError as exc:
        print("USAGE: cannot create a fixture root under %s (%s)" % (base, exc), file=sys.stderr)
        return EXIT_USAGE

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
        src = TOOL_PATH  # the running script, not a same-named neighbour (rule-#14 identity arm)
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

    # 13. exists-but-unreadable file: declared UNEVALUABLE, receipt kept, no crash
    def case_unreadable():
        if os.geteuid() == 0:
            return  # mode 000 does not block root; the case is not meaningful
        bad = root / "unreadable.conf"
        bad.write_bytes(b"x\n")
        os.chmod(bad, 0)
        try:
            out = root / "unreadable.txt"
            rc = cmd_capture(argparse.Namespace(out=str(out), paths=[str(bad)], label="selftest"))
            outv = root / "unreadable-verify.out"
            rc_ver = _run_verify([str(out), "--live"], outv)
        finally:
            os.chmod(bad, 0o644)
        assert rc == EXIT_UNEVALUABLE, "expected UNEVALUABLE exit %d, got %d" % (EXIT_UNEVALUABLE, rc)
        text = out.read_text()
        assert "READ-ERROR:" in text, "read error not recorded in the receipt"
        assert "EXISTS: yes" in text, "unevaluable path recorded as absent"
        assert rc_ver == EXIT_UNEVALUABLE, "expected verify UNEVALUABLE (fail-closed), got %d" % rc_ver
        assert "VERDICT: UNEVALUABLE" in outv.read_text(), "no UNEVALUABLE verdict printed"
    run_case(cases, "unreadable-path-is-unevaluable", case_unreadable)

    # 14. an unevaluable path must never verify as MATCH (the live fail-open class);
    #     the format tag stays honest on an all-unevaluable v2 receipt
    def case_unevaluable_not_match():
        if os.geteuid() == 0:
            return
        d = root / "blocked"
        d.mkdir()
        inner = d / "inner.conf"
        inner.write_bytes(b"y\n")
        os.chmod(d, 0)
        try:
            out = root / "blocked-receipt.txt"
            rc_cap = cmd_capture(argparse.Namespace(out=str(out), paths=[str(inner)], label="selftest"))
            outv = root / "blocked-verify.out"
            rc_ver = _run_verify([str(out), "--live"], outv)
        finally:
            os.chmod(d, 0o755)
        assert rc_cap == EXIT_UNEVALUABLE, "expected capture UNEVALUABLE, got %d" % rc_cap
        assert "STAT-ERROR:" in out.read_text(), "stat error not recorded in the receipt"
        assert parse_receipt(out)[0] == "v2", "unevaluable v2 receipt mislabeled v1"
        assert rc_ver == EXIT_UNEVALUABLE, "expected verify UNEVALUABLE (fail-closed), got %d" % rc_ver
        text = outv.read_text()
        assert "VERDICT: UNEVALUABLE" in text, "unevaluable path not classified UNEVALUABLE"
        assert "VERDICT: MATCH" not in text, "unevaluable path read as MATCH (fail-open)"
    run_case(cases, "unevaluable-never-matches", case_unevaluable_not_match)

    # 15. a PARSED receipt carrying an unreadable stanza must never verify MATCH:
    #     the parser must read READ-ERROR/STAT-ERROR, or the receipt-file path
    #     stays fail-open (EX-40's patch alone leaves this open — PL-2 §2.1)
    def case_parsed_unevaluable():
        if os.geteuid() == 0:
            return
        f = root / "parsed-uneval.conf"
        f.write_bytes(b"parsed unevaluable fixture\n")
        os.chmod(f, 0)
        try:
            hidden, rc_h = capture_to("parsed-hidden.txt", [f])
        finally:
            os.chmod(f, 0o644)
        assert rc_h == EXIT_UNEVALUABLE, "expected capture UNEVALUABLE, got %d" % rc_h
        assert "READ-ERROR:" in hidden.read_text(), "READ-ERROR not rendered into the receipt"
        opened, rc_o = capture_to("parsed-open.txt", [f])
        assert rc_o == EXIT_MATCH, "control capture exit %d" % rc_o
        out = root / "parsed-uneval.out"
        rc = _run_verify([str(hidden), str(opened)], out)
        assert rc == EXIT_UNEVALUABLE, "expected UNEVALUABLE exit %d on a parsed receipt, got %d" % (
            EXIT_UNEVALUABLE, rc)
        assert "VERDICT: MATCH" not in out.read_text(), "parsed unevaluable stanza read as MATCH (fail-open)"
        d = root / "blocked-pair"
        d.mkdir()
        inner = d / "inner.conf"
        inner.write_bytes(b"z\n")
        os.chmod(d, 0)
        try:
            pair = []
            for tag in ("a", "b"):
                outx = root / ("blocked-pair-%s.txt" % tag)
                rc_x = cmd_capture(argparse.Namespace(out=str(outx), paths=[str(inner)], label="selftest"))
                assert rc_x == EXIT_UNEVALUABLE, "expected capture UNEVALUABLE, got %d" % rc_x
                pair.append(str(outx))
            outv2 = root / "blocked-pair-verify.out"
            rc_ver2 = _run_verify(pair, outv2)
        finally:
            os.chmod(d, 0o755)
        assert rc_ver2 == EXIT_UNEVALUABLE, "expected receipt-vs-receipt UNEVALUABLE (fail-closed), got %d" % rc_ver2
    run_case(cases, "parsed-unevaluable-reference-never-matches", case_parsed_unevaluable)

    # 16. partial reference: declared gate --require-paths N (D3)
    def case_require_paths():
        single = root / "single.conf"
        single.write_bytes(payload)
        os.utime(single, (1000000000, 1000000000))
        rec, rc0 = capture_to("single-pre.txt", [single])
        assert rc0 == EXIT_MATCH, "reference capture exit %d" % rc0
        out_plain = root / "coverage-plain.out"
        rc_plain = _run_verify([str(rec), "--live"], out_plain)
        assert rc_plain == EXIT_MATCH, "declared default (no gate without the flag) broke: exit %d" % rc_plain
        out_gated = root / "coverage-gated.out"
        rc_gated = _run_verify([str(rec), "--live", "--require-paths", "5"], out_gated)
        assert rc_gated == EXIT_USAGE, "expected USAGE exit %d under --require-paths 5, got %d" % (
            EXIT_USAGE, rc_gated)
        text = out_gated.read_text()
        assert "REFERENCE-COVERAGE: 1/5" in text, "REFERENCE-COVERAGE line missing or wrong: %r" % text
        assert "unaccounted:" in text, "unaccounted list missing"
        out_pass = root / "coverage-pass.out"
        rc_pass = _run_verify([str(rec), "--live", "--require-paths", "1"], out_pass)
        assert rc_pass == EXIT_MATCH, "expected MATCH under --require-paths 1, got %d" % rc_pass
    run_case(cases, "partial-reference-require-paths-gate", case_require_paths)

    # 17. write guard covers the scoped paths it measures (the --paths X --out X clobber)
    def case_guard_scope():
        scoped = root / "scoped.conf"
        scoped.write_bytes(b"scoped fixture bytes\n")
        before = capture_path(scoped)
        rc = cmd_capture(argparse.Namespace(out=str(scoped), paths=[str(scoped)], label="guard-scope"))
        after = capture_path(scoped)
        assert rc == EXIT_USAGE, "expected USAGE refusing --out over a measured path, got %d" % rc
        assert before == after, "the scoped file was clobbered by the receipt it measured"
        assert scoped.read_text() == "scoped fixture bytes\n", "scoped file bytes changed"
    run_case(cases, "refuses-to-write-over-scoped-path", case_guard_scope)

    # 18. selftest scratch base must pre-exist; missing/file//tmp base is USAGE, not a
    #     traceback (D6). The subprocess arms never pass an existing scratch, so the
    #     child cannot recurse into this case; the in-process arm asserts the class too.
    def case_missing_scratch():
        tool = str(Path(__file__).resolve())
        for label, scratch in (("missing", root / "does-not-exist"),
                               ("file", root / "scratch-is-a-file"),
                               ("tmp", "/tmp/ex21-selftest-must-not-run")):
            if label == "file":
                Path(scratch).write_text("x", encoding="utf-8")
            p = subprocess.run([sys.executable, tool, "selftest", "--scratch", str(scratch)],
                               capture_output=True, text=True)
            assert p.returncode == EXIT_USAGE, "expected USAGE exit %d for %s scratch, got %d" % (
                EXIT_USAGE, label, p.returncode)
            assert "Traceback" not in p.stderr, "raw traceback for %s scratch: %s" % (label, p.stderr)
        rc = cmd_selftest(argparse.Namespace(scratch=str(root / "does-not-exist")))
        assert rc == EXIT_USAGE, "expected USAGE exit %d in-process for a missing base, got %d" % (EXIT_USAGE, rc)
    run_case(cases, "selftest-missing-scratch-usage-exit", case_missing_scratch)

    # 19. write guard must also refuse a hardlink alias of a measured path (D7/RV-11)
    def case_guard_hardlink():
        a = root / "guard-hardlink-a.conf"
        a.write_bytes(b"guard hardlink fixture\n")
        b = root / "guard-hardlink-alias.txt"
        os.link(a, b)
        before = capture_path(a)
        rc = cmd_capture(argparse.Namespace(out=str(b), paths=[str(a)], label="guard-inode"))
        after = capture_path(a)
        assert rc == EXIT_USAGE, "expected USAGE for a hardlink alias, got %d" % rc
        assert before == after, "hardlinked alias was written through the guard"
    run_case(cases, "refuses-write-through-hardlink-alias", case_guard_hardlink)

    # 20. coverage gate basis: DISTINCT RESOLVED PATHS, not stanzas (round-3
    #     residual (c); EX-24's measured vector). A duplicate-padded reference
    #     must not satisfy --require-paths 5.
    def case_coverage_duplicates():
        dup = root / "dupe-src.conf"
        dup.write_bytes(payload)
        os.utime(dup, (1000000000, 1000000000))
        rec, rc0 = capture_to("dupe-src.txt", [dup])
        assert rc0 == EXIT_MATCH, "reference capture exit %d" % rc0
        header, sep, stanza = rec.read_text().partition("PATH: ")
        assert sep and stanza, "no stanza rendered into the reference receipt"
        dup5 = root / "dupe-5x.txt"
        dup5.write_text(header + (sep + stanza) * 5, encoding="utf-8")
        assert dup5.read_text().count("PATH: ") == 5, "fixture is not 5 stanzas"
        out = root / "dupe-5x.out"
        rc = _run_verify([str(dup5), "--live", "--require-paths", "5"], out)
        text = out.read_text()
        assert rc == EXIT_USAGE, "expected USAGE exit %d on 5 duplicate stanzas, got %d" % (EXIT_USAGE, rc)
        assert "REFERENCE-COVERAGE: 1/5" in text, "coverage line does not count distinct paths: %r" % text
        assert "VERDICT: MATCH" not in text, "duplicate-padded reference read as MATCH (the residual)"
    run_case(cases, "coverage-gate-rejects-duplicate-stanzas", case_coverage_duplicates)

    # 21. the same gate's control: five DISTINCT paths still satisfy it
    def case_coverage_distinct():
        five = []
        for i in range(5):
            p = root / ("cov-%d.conf" % i)
            p.write_bytes(payload + bytes([48 + i]))
            os.utime(p, (1000000000, 1000000000))
            five.append(p)
        rec, rc0 = capture_to("cov-5.txt", five)
        assert rc0 == EXIT_MATCH, "reference capture exit %d" % rc0
        out = root / "cov-5.out"
        rc = _run_verify([str(rec), "--live", "--require-paths", "5"], out)
        assert rc == EXIT_MATCH, "five distinct paths must satisfy --require-paths 5, got %d" % rc
        assert "VERDICT: MATCH" in out.read_text(), "no MATCH verdict for the five-distinct control"
    run_case(cases, "coverage-gate-passes-distinct-five", case_coverage_distinct)

    # 22. write guard covers the DERIVED SIDECAR (round-3 residual (a), variant A:
    #     --paths X.sha256 --out X). Before: exit 0 and X.sha256 destroyed.
    def case_sidecar_scope():
        vic = root / "sidecar-vic.sha256"
        vic.write_bytes(b"measured file whose name ends in .sha256\n")
        before = capture_path(vic)
        rc = cmd_capture(argparse.Namespace(out=str(root / "sidecar-vic"),
                                            paths=[str(vic)], label="sidecar-scope"))
        after = capture_path(vic)
        assert rc == EXIT_USAGE, "expected USAGE refusing a sidecar over the measured file, got %d" % rc
        assert before == after, "the measured .sha256 file was clobbered by the receipt's sidecar"
        assert not (root / "sidecar-vic").exists(), "a refused run left the receipt behind"
    run_case(cases, "refuses-sidecar-over-measured-file", case_sidecar_scope)

    # 23. write guard covers the SIDECAR-SHAPED NEIGHBOUR (residual (a), variant B2:
    #     --paths X --out X.sha256, the neighbour already existing as a bystander)
    def case_neighbour_scope():
        meas = root / "neighbour-vic.conf"
        meas.write_bytes(b"measured file\n")
        neighbour = root / "neighbour-vic.conf.sha256"
        neighbour.write_bytes(b"bystander neighbour bytes\n")
        before_m = capture_path(meas)
        before_n = capture_path(neighbour)
        rc = cmd_capture(argparse.Namespace(out=str(neighbour), paths=[str(meas)],
                                            label="neighbour-scope"))
        assert rc == EXIT_USAGE, "expected USAGE for a receipt on a measured path's sidecar" \
            " neighbour, got %d" % rc
        assert capture_path(meas) == before_m, "the measured file changed"
        assert capture_path(neighbour) == before_n, "the sidecar-shaped neighbour was clobbered"
    run_case(cases, "refuses-receipt-over-sidecar-neighbour", case_neighbour_scope)

    # 24. a receipt directory that cannot be created is the declared USAGE class,
    #     not a raw traceback (round-3 residual (b); CR-3 §3 / CR-4 item 5).
    def case_out_parent_usage():
        blocker = root / "not-a-dir.txt"
        blocker.write_bytes(b"a regular file, not a directory\n")
        out = root / "not-a-dir.txt" / "sub" / "receipt.txt"
        tool = str(Path(__file__).resolve())  # the running script (rule-#14 identity arm)
        p = subprocess.run([sys.executable, tool, "capture", "--out", str(out),
                            "--paths", str(blocker), "--label", "out-parent"],
                           capture_output=True, text=True)
        assert p.returncode == EXIT_USAGE, "expected USAGE exit %d, got %d" % (EXIT_USAGE, p.returncode)
        assert "Traceback" not in p.stderr, "raw traceback for an uncreatable receipt dir: %s" % p.stderr
        assert not out.exists(), "a partial receipt was left behind"
        loop = root / "symlink-loop"
        if not loop.is_symlink():
            os.symlink(str(loop), str(loop))
        p2 = subprocess.run([sys.executable, tool, "capture", "--out", str(loop / "r.txt"),
                             "--paths", str(blocker), "--label", "out-parent-loop"],
                            capture_output=True, text=True)
        assert p2.returncode == EXIT_USAGE, "expected USAGE exit %d for ELOOP, got %d" % (
            EXIT_USAGE, p2.returncode)
        assert "Traceback" not in p2.stderr, "raw traceback for ELOOP: %s" % p2.stderr
    run_case(cases, "out-parent-not-a-directory-usage-exit", case_out_parent_usage)

    # 25. the both-sides-absent ruling (round-3 residual (d)): agreement on
    #     absence is MATCH by declared design, and the row says so; the
    #     error-carrying form is UNEVALUABLE (cases 13-15).
    def case_both_absent():
        ghost = root / "ghost.conf"
        ghost.write_bytes(b"ghost fixture\n")
        rec_a, rc_a = capture_to("ghost-a.txt", [ghost])
        assert rc_a == EXIT_MATCH, "reference capture exit %d" % rc_a
        ghost.unlink()
        rec_b, rc_b = capture_to("ghost-b.txt", [ghost])
        assert rc_b == EXIT_ABSENT, "expected ABSENT capture exit %d, got %d" % (EXIT_ABSENT, rc_b)
        out = root / "ghost-pair.out"
        rc = _run_verify([str(rec_a), str(rec_b)], out)
        assert rc == EXIT_ABSENT, "reference-present/candidate-absent must be ABSENT, got %d" % rc
        out2 = root / "ghost-both.out"
        rc2 = _run_verify([str(rec_b), str(rec_b)], out2)
        text2 = out2.read_text()
        assert rc2 == EXIT_MATCH, "both-absent must read MATCH by declared design, got %d" % rc2
        assert "agreement" in text2, "the both-absent MATCH is not annotated: %r" % text2
        assert "SHA256-CONTRACT: 0/0" in text2, "the vacuous contract line is not printed"
    run_case(cases, "both-sides-absent-is-agreement-match", case_both_absent)

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
    ns = argparse.Namespace(receipt_a=argv[0], receipt_b=None, live=False, require_paths=None)
    rest = [a for a in argv[1:] if a != "--live"]
    if any(a == "--live" for a in argv[1:]):
        ns.live = True
    if "--require-paths" in rest:
        i = rest.index("--require-paths")
        ns.require_paths = int(rest[i + 1])
        del rest[i:i + 2]
    if rest:
        ns.receipt_b = rest[0]
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
    p_ver.add_argument("--require-paths", type=int, default=None, metavar="N",
                       help="exit 2 (USAGE) when the reference carries fewer than N paths (D3 coverage gate)")
    p_ver.set_defaults(func=cmd_verify)

    p_self = sub.add_parser("selftest", help="fixture-based selftest (never touches a custody path)")
    p_self.add_argument("--scratch", default=None,
                        help="fixture root (default: $CUSTODY_PAIR_SCRATCH, /dev/shm, /var/tmp); "
                             "a missing / non-directory / `/tmp` base is a USAGE exit 2")
    p_self.set_defaults(func=cmd_selftest)

    p_paths = sub.add_parser("paths", help="print the 5 canonical custody paths")
    p_paths.set_defaults(func=cmd_paths)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
