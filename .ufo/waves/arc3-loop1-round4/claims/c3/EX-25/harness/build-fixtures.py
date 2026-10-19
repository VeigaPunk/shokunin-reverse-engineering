#!/usr/bin/env python3
"""EX-25 (c3, arc3-loop1-round4) fixture builder.

Builds the coverage-gate vectors used by coverage-after.md.  Fixtures are
generated from the tool's OWN renderer (imported from the BEFORE revision), so
every stanza is tool-produced rather than hand-fabricated; only the *padding*
is synthetic (repeating a stanza the tool itself emitted).

Scratch only: /var/tmp/ex25-r4/.  Custody paths are read-only (capture =
sha256+stat, no write).
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
import time
from pathlib import Path

ROOT = Path("/var/tmp/ex25-r4")
TOOL = ROOT / "tools" / "before" / "custody-pair.py"
FIX = ROOT / "fixtures"
CUSTODY_FIVE = (
    "~/.config/devin/mcp_config.json",
    "~/.omp/agent/mcp.json",
    "~/.kimi-code/config.toml",
    "~/.bashrc",
    "~/.profile",
)


def load_tool(path: Path):
    spec = importlib.util.spec_from_file_location("cp_ex25", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def stanza_block(rendered: str, path: str) -> str:
    """Extract the `PATH: ...` stanza block for `path` from a rendered receipt."""
    marker = "PATH: %s\n" % path
    i = rendered.index(marker)
    j = rendered.index("\n\nPATH: ", i) if "\n\nPATH: " in rendered[i:] else len(rendered)
    if j != len(rendered):
        j += 1  # keep the separating newline owned by the next block
    return rendered[i:j].rstrip("\n")


def header(rendered: str, n_paths: int, present: int) -> str:
    out = []
    for line in rendered.splitlines():
        if line.startswith("PATH: "):
            break
        if line.startswith("# paths: "):
            line = "# paths: %d  present: %d" % (n_paths, present)
        out.append(line)
    return "\n".join(out).rstrip("\n")


def write(p: Path, text: str) -> None:
    p.write_text(text, encoding="utf-8")
    print("FIXTURE %-34s %6d B  sha256=%s" % (p.name, len(text.encode()), sha256_file(p)))


def main() -> int:
    FIX.mkdir(parents=True, exist_ok=True)
    cp = load_tool(TOOL)
    now = time.time()

    # ---- scratch payloads ------------------------------------------------
    sc = FIX / "scratch"
    sc.mkdir(exist_ok=True)
    distinct_files = []
    for i in range(5):
        f = sc / ("distinct-%d.conf" % (i + 1))
        f.write_text("ex25 control payload %d\n" % (i + 1), encoding="utf-8")
        os.utime(f, (1700000000, 1700000000))
        distinct_files.append(f)

    real = sc / "aliased-real.conf"
    real.write_text("ex25 alias target\n", encoding="utf-8")
    a1 = sc / "alias-1.conf"
    a2 = sc / "alias-2.conf"
    for a in (a1, a2):
        if a.exists() or a.is_symlink():
            a.unlink()
        a.symlink_to(real)

    # ---- tool-rendered references ---------------------------------------
    # 5 real custody paths, one stanza each (read-only capture)
    c5 = [Path(p).expanduser() for p in CUSTODY_FIVE]
    sec5 = [cp.capture_path(p) for p in c5]
    r5 = cp.render_receipt(sec5, "EX-25 custody5 (read-only capture)", now)

    # 5 distinct scratch paths, one stanza each (control, no custody path)
    s5sec = [cp.capture_path(p) for p in distinct_files]
    s5 = cp.render_receipt(s5sec, "EX-25 distinct5 control", now)

    # 1 custody path (selftest-case-16 shape)
    one = cp.capture_path(c5[0])
    r1 = cp.render_receipt([one], "EX-25 one-path reference", now)

    # ---- padding vectors -------------------------------------------------
    blk0 = stanza_block(r5, str(c5[0]))
    write(FIX / "custody5-distinct-pre.txt", r5)
    write(FIX / "scratch5-distinct-pre.txt", s5)
    write(FIX / "one-pre.txt", r1)

    # 5 stanzas / 1 distinct path — header keeps the honest "paths: 5 present: 5"
    dupe = header(r5, 5, 5) + "\n\n" + "\n\n".join([blk0] * 5) + "\n"
    write(FIX / "dupe5-one-path-pre.txt", dupe)

    # 5 stanzas / 4 distinct paths (stanza 1 padded) — 4 real custody stanzas + 1 dupe
    blocks = [stanza_block(r5, str(p)) for p in c5]
    four_plus = header(r5, 5, 5) + "\n\n" + "\n\n".join(blocks[:4] + [blocks[0]]) + "\n"
    write(FIX / "dupe4plus1-pre.txt", four_plus)

    # v1 sums shape: 5 rows, 1 path / 5 rows, 5 distinct paths
    v1d = "\n".join("%s  %s" % (s["sha256"], s["path"]) for s in s5sec) + "\n"
    write(FIX / "v1-distinct5-pre.txt", v1d)
    v1p = "\n".join("%s  %s" % (s5sec[0]["sha256"], s5sec[0]["path"]) for _ in range(5)) + "\n"
    write(FIX / "v1-dupe5-one-path-pre.txt", v1p)

    # symlink-alias boundary: 5 stanzas, two of which resolve to one file (4 distinct)
    alias_secs = [cp.capture_path(p) for p in (a1, a2, distinct_files[0], distinct_files[1], distinct_files[2])]
    alias = cp.render_receipt(alias_secs, "EX-25 symlink-alias boundary", now)
    write(FIX / "symlink-alias-5stanzas-pre.txt", alias)

    print("\n# rendered header of dupe5-one-path-pre.txt:")
    for line in dupe.splitlines()[:11]:
        print("   " + line)
    print("\n# paths in each fixture (distinct resolved):")
    for f in sorted(FIX.glob("*.txt")):
        try:
            fmt, secs = cp.parse_receipt(f)
        except ValueError as exc:
            print("   %-34s UNPARSABLE %s" % (f.name, exc))
            continue
        have = {str(Path(s["path"]).expanduser().resolve()) for s in secs}
        print("   %-34s fmt=%-9s stanzas=%d distinct_resolved=%d" % (f.name, fmt, len(secs), len(have)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
