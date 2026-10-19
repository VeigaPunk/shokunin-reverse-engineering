#!/usr/bin/env python3
"""CN-2 (arc3-loop1-round4) merge assembler — v1.

Extracts the literal blocks from the chains' landed records drafts, splices the
C1/C2/C3 bullets byte-faithfully (placeholder convention normalized to
`[[FILL: …]]`), and composes the merged SCORECARD section + LOG entry with this
seat's connector text. Writes to claims/cross/CN-2/ and prints source/segment
shas. A missing chain draft fails loudly (named gap), never a silent skip.

Chain draft conventions (r3 precedent, r4 expected):
  C1: claims/c1/records-drafts/records-drafts.md       (one block: LOG then SCORECARD)
  C2: claims/c2/records-drafts/scorecard-section-draft.md + LOG-entry-draft.md
  C3: claims/c3/records-drafts/scorecard-section-draft.md + log-entry-draft.md
Also accepts an r4 variant where each chain ships a single `records-drafts.md`
holding both blocks (detected by the presence of both markers).
"""
import hashlib, os, pathlib, re, sys

W = pathlib.Path(os.environ.get(
    "CN2_WAVE",
    "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4"))
OUT = W / "claims/cross/CN-2"
SCRATCH = pathlib.Path("/dev/shm/cn2r4/blocks")
SCRATCH.mkdir(parents=True, exist_ok=True)

R3 = W.parent / "arc3-loop1-round3"


def read(p):
    return p.read_text(encoding="utf-8")


def literal(path):
    txt = read(path)
    m = re.search(r"<!-- BEGIN LITERAL [A-Z ]+ -->\n(.*?)<!-- END LITERAL [A-Z ]+ -->", txt, re.S)
    if not m:
        sys.exit("no literal block in %s" % path)
    return m.group(1)


def norm_placeholders(s):
    s = re.sub(r"⟨(N ≥ \d+|\d+)⟩", r"[[FILL: \1]]", s)
    for _ in range(10):
        prev = s
        s = re.sub(r"⟨((?:PARENT-)?FILL|PARENT)(?::\s*|\s+|$)([^⟨]*?)⟩",
                   lambda m: "[[FILL: %s]]" % (m.group(2).strip() or "…"), s, flags=re.S)
        s = re.sub(r"⟨(?:PARENT-)?FILL⟩", "[[FILL: …]]", s)
        if s == prev:
            break
    leftover = re.findall(r"⟨[^⟩]*⟩", s)
    if leftover:
        sys.exit("un-normalized placeholder(s): %r" % leftover)
    return s


def bullet_block(block, start_prefix, stop_prefixes):
    lines = block.splitlines(keepends=True)
    out, inside = [], False
    for ln in lines:
        if not inside and ln.startswith(start_prefix):
            inside = True
        if inside:
            if out and any(ln.startswith(p) for p in stop_prefixes):
                break
            out.append(ln)
    if not out:
        sys.exit("bullet not found: %r" % start_prefix)
    return "".join(out).rstrip("\n")


def seg(name, text):
    (SCRATCH / (name + ".seg")).write_text(text, encoding="utf-8")
    print("segment %s: %d lines sha256=%s" % (
        name, len(text.splitlines()), hashlib.sha256(text.encode()).hexdigest()[:16]))


def find_chain_drafts(chain, allow_gaps):
    """Locate (scorecard_src, log_src) for a chain; either half may be None."""
    d = W / ("claims/%s/records-drafts" % chain)
    cands = sorted(d.glob("*.md")) if d.is_dir() else []
    if not cands:
        if allow_gaps:
            print("GAP: no records-drafts for chain %s under %s (stubbed)" % (chain, d))
            return None, None
        sys.exit("GAP: no records-drafts for chain %s under %s" % (chain, d))
    sc = [p for p in cands if "scorecard" in p.name.lower()]
    lg = [p for p in cands if "log" in p.name.lower()]
    if sc or lg:
        return (sc[0] if sc else None), (lg[0] if lg else None)
    # single-file variant: one block holding both
    for p in cands:
        t = read(p)
        if t.count("<!-- BEGIN LITERAL") >= 1 and re.search(r"\n## arc3-loop1-round4", t):
            return p, p
    if allow_gaps:
        print("GAP: cannot classify drafts for chain %s: %s (stubbed)" % (
            chain, [p.name for p in cands]))
        return None, None
    sys.exit("GAP: cannot classify drafts for chain %s: %s" % (chain, [p.name for p in cands]))


def split_single(block, chain_label):
    """Single-block variant: split at the SCORECARD heading."""
    m = re.search(r"\n## arc3-loop1-round4", block)
    if not m:
        sys.exit("GAP: single block for %s holds no SCORECARD heading" % chain_label)
    return block[:m.start()], block[m.start() + 1:]


def extract_learn(block, chain):
    """Pull a chain's learning-trend sentence, tolerating wrapped lines and a
    leading ownership placeholder. Stops at the chain's own next marker."""
    m = re.search(r"Learning trends: (.*?)(?=\nPlanned:|\n\n|\Z)", block, re.S)
    if not m:
        return "[[FILL: %s learning sentence]]" % chain
    learn = m.group(1).strip()
    learn = re.sub(r"^⟨[^⟩]*⟩\s*", "", learn)
    # a wrapped sentence joins its continuation lines
    learn = re.sub(r"\s*\n\s*", " ", learn)
    learn = re.sub(r"\s+", " ", learn).strip()
    # a chain draft may inline its own planned/carried/retired lines: cut them
    learn = re.split(r"\s*Planned:|\s*Carried debt|\s*Retired:", learn)[0].strip()
    # cross-chain splice markers are satisfied by the splice itself
    learn = re.sub(r"\s*\[\[FILL: [^\]]*(?:one-liners|sentences)[^\]]*\]\]\s*", " ", learn)
    learn = re.sub(r"\s+", " ", learn).strip()
    learn = norm_placeholders(learn)
    return learn


print("== CN-2 r4 fold ==")
ALLOW_GAPS = os.environ.get("CN2_ALLOW_GAPS") == "1"
# --- C1 -------------------------------------------------------------------
c1_src = W / "claims/c1/records-drafts/records-drafts.md"
if not c1_src.is_file():
    if not ALLOW_GAPS:
        sys.exit("GAP: C1 draft absent: %s" % c1_src)
    print("GAP: C1 draft absent (stubbed)")
    c1_block = None
else:
    c1_block = literal(c1_src)
if c1_block is not None:
    print("source c1: %d lines sha256=%s" % (
        len(c1_block.splitlines()), hashlib.sha256(c1_block.encode()).hexdigest()[:16]))
    if re.search(r"\n## arc3-loop1-round4", c1_block):
        c1_log_block, c1_sec_block = split_single(c1_block, "c1")
    else:
        sys.exit("GAP: C1 block carries no SCORECARD section heading")
    c1_sec_bullet = norm_placeholders(bullet_block(c1_sec_block, "- C1 coverage (owned)",
                                                   ["- C2 ", "- C3 ", "- Custody", "- Measured"]))
    c1_log_bullet = norm_placeholders(bullet_block(c1_log_block, "- C1 coverage (owned)",
                                                   ["- C2 ", "- C3 ", "- Custody", "- Measured"]))
    seg("c1-sec-bullet", c1_sec_bullet)
    seg("c1-log-bullet", c1_log_bullet)

    m = re.search(r"\n\| coverage(?: \(owned\))? — C1 \| (.*?) \| (improved[^|]*) \|", c1_sec_block, re.S)
    if not m:
        sys.exit("GAP: C1 verdict row not found")
    c1_row = "| coverage (owned) — C1 | " + norm_placeholders(m.group(1).strip()) + " | " + m.group(2).strip() + " |"
    c1_learn = extract_learn(c1_sec_block, "C1")
else:
    c1_sec_bullet = "- C1 coverage (owned) — [[FILL: C1's records draft had not landed at fold time; re-fold when it does]]"
    c1_log_bullet = "- C1 coverage — [[FILL: C1's records draft had not landed at fold time; re-fold when it does]]"
    c1_row = "| coverage (owned) — C1 | [[FILL: C1 verdict row]] | [[FILL]] |"
    c1_learn = "[[FILL: C1 learning sentence]]"

# --- C2 / C3 --------------------------------------------------------------
sources = {}
for name, chain in [("c2", "c2"), ("c3", "c3")]:
    sc, lg = find_chain_drafts(chain, ALLOW_GAPS)
    for half, src in (("sec", sc), ("log", lg)):
        key = name + "-" + half
        if src is None:
            sources[key] = None
            continue
        b = literal(src)
        sources[key] = b
        print("source %s: %d lines sha256=%s (%s)" % (
            key, len(b.splitlines()), hashlib.sha256(b.encode()).hexdigest()[:16], src.name))

def chain_or_stub(chain, key, prefix, stops):
    b = sources.get(key)
    if b is None:
        return "%s [[FILL: %s's records draft had not landed at fold time; re-fold when it does]]" % (prefix, chain)
    return norm_placeholders(bullet_block(b, prefix, stops))

c2_sec_bullet = chain_or_stub("C2", "c2-sec", "- C2 ", ["- C3 ", "- Custody", "- Measured"])
c3_sec_bullet = chain_or_stub("C3", "c3-sec", "- C3 ", ["- Custody", "- Measured"])
c2_log_bullet = chain_or_stub("C2", "c2-log", "- C2 ", ["- C3 ", "- Custody", "- Measured"])
c3_log_bullet = chain_or_stub("C3", "c3-log", "- C3 ", ["- Custody", "- Measured"])
seg("c2-sec-bullet", c2_sec_bullet)
seg("c3-sec-bullet", c3_sec_bullet)
seg("c2-log-bullet", c2_log_bullet)
seg("c3-log-bullet", c3_log_bullet)

def row_and_learn(chain, key, label, rowpat, fallback_row):
    b = sources.get(key)
    if b is None:
        return fallback_row, "[[FILL: %s learning sentence]]" % chain
    m = re.search(rowpat, b, re.S)
    row = ("| " + label + " | " + norm_placeholders(m.group(1).strip()) + " | " + m.group(2).strip() + " |") if m else fallback_row
    return row, extract_learn(b, chain)

c2_row, c2_learn = row_and_learn(
    "C2", "c2-sec", "freshness (fleet) — C2",
    r"\n\| (?:operability \(fleet\) — C2|C2 — operability|freshness \(fleet\) — C2|C2 — freshness|freshness — C2) \| (.*?) \| (improved[^|]*) \|",
    "| freshness (fleet) — C2 | [[FILL: C2 verdict row]] | [[FILL]] |")
c3_row, c3_learn = row_and_learn(
    "C3", "c3-sec", "operability (fleet) — C3",
    r"\n\| (?:freshness \(fleet\) — C3|C3 — freshness|operability \(fleet\) — C3|C3 — operability|operability — C3) \| (.*?) \| (improved[^|]*) \|",
    "| operability (fleet) — C3 | [[FILL: C3 verdict row]] | [[FILL]] |")

# --- connector text -------------------------------------------------------
OPENING = """Round 4 of arc 3 (loop 1; 4/10). Axis set: **coverage (owned)**,
freshness (fleet), operability (fleet); all three owned proxies stay tied at
10.0 with none retired, so the owned claim is selected by the standing
most-falsifiable-next-claim tie-break. The claims are causally separable — the
corpus knowledge surface (the Vyper leg), the province surface text, and the
custody tool share no edit target. Roster frozen PRE-DISPATCH (mechanically
enumerated, 16+14+14+4 = 48, every name exactly once; the items-array assertion
held at dispatch). Lane note: the wave was declared on the hyper lane
(`hyper/deepseek-v4.1-flash`) and re-dispatched on the devin lane
(`devin/deepseek-v4-1-flash-max`) after the hyper lane returned 402
out-of-credits on all 48 seats — the schedule's declared fallback, recorded
with cause, not a lane signal."""

WAVE_BULLET = """- Wave: 48 seats; reports `.ufo/waves/arc3-loop1-round4/`; round report
  `.ufo/reports/arc3-loop1-round4/kaidoku.md`. Delivered [[FILL: N/48 per the
  roster reconciliation, never the declared count]]. Landed at [[FILL: work /
  wave-artifacts / records commits]]."""

MEASURED_BULLET = """- Measured at the records commit: [[FILL: command A at the settled tree;
  probe selftest + findings both modes; census PASS 0/0/0/0; custody pair]].
  The connector's own pre-landing measurements: the records text appended to
  scratch copies of the scoped files reads census PASS 0/0/0/0 with an
  injected-pin control FAILing (`undeclared=1`), the PIN-FREE checker reads
  CLEAN on both literal bodies, and the chains' patch texts projected in place
  (with the section appended) also read PASS."""

TRENDS = "Learning trends: %s %s %s" % (c1_learn, c2_learn, c3_learn)

CARRIED = """Carried debt (named): [[FILL: per the chains' own carried-debt
clauses — C1's Vyper Unknowns, C2's adjudicated NO-CHANGE bullets, C3's
custody residuals (d) and the standing hazards]]. Standing: the host `/tmp`
quota exhaustion (recipes must carry a disk-backed scratch); the pre-existing
dirty `.ufo/waves/arc2-loop1-round10/C3.md` (not this round's). Retired:
[[FILL: none / list]]."""

section = """## arc3-loop1-round4 — coverage + freshness + operability: [[FILL: verdict phrase per the parent's admission]], 2026-10-19

%s

%s
%s
%s
%s
%s

| Axis | Before → after | Verdict |
|---|---|---|
%s
%s
%s
| depth | [[FILL: unchanged, with the measurement recipe at the records commit]] | unchanged |
| calibration | [[FILL: unchanged, with the measurement recipe at the records commit]] | unchanged |

%s
Planned: [[FILL: round 5 per schedule]].
%s
""" % (OPENING, WAVE_BULLET, c1_sec_bullet, c2_sec_bullet, c3_sec_bullet, MEASURED_BULLET,
       c1_row, c2_row, c3_row, TRENDS, CARRIED)

merged_sec = ("# merged records text — arc3-loop1-round4 (seat CN-2, cross connector)\n\n"
 "Assembled 2026-10-19 by seat CN-2 from the chains' literal drafts (C1/C2/C3 —\n"
 "spliced verbatim, placeholder-normalized; sources + shas in the outline's\n"
 "merge-delta table). **Pasteable text only** — nothing here is applied; the\n"
 "parent lands R1/R2. The section is PIN-FREE by construction and measured\n"
 "(outline §6.4); identity of this file: receipts/identity.txt (rule #14 — not\n"
 "inlined).\n\n"
 "## Literal SCORECARD section (append at EOF after the round-3 section)\n\n"
 "<!-- BEGIN LITERAL SECTION TEXT -->\n" + section +
 "<!-- END LITERAL SECTION TEXT -->\n")
(OUT / "merged-SCORECARD-section.md").write_text(merged_sec, encoding="utf-8")

log_body = """### arc3-loop1-round4 — coverage: [[FILL: C1 short phrase]] + freshness: [[FILL: C2 short phrase]] + operability: [[FILL: C3 short phrase]] (2026-10-19)

- Dispatch: 48 seats frozen PRE-DISPATCH (roster enumerated mechanically —
  16+14+14+4, every name exactly once; the items-array assertion held at
  dispatch). Declared on the hyper lane; re-dispatched on the devin lane after
  the hyper lane returned 402 out-of-credits on all 48 seats (the schedule's
  declared fallback; recorded with cause, not a lane signal). Delivered
  [[FILL: N]]/48 per the roster reconciliation (count the items array, never
  the intent).
%s
%s
%s
- Custody: [[FILL per CU-1 / the C3 landing: pre-pair capture time + 5/5,
  post-pair capture time + 5/5, the in-window drift comparison; any
  operator-side churn recorded verbatim, not repaired; custody paths read-only
  for every seat]].
- Scope: kaidoku repo only; no pushes (standing rule); no installs beyond C1's
  authorized vyper venv into the wave tree; custody paths read-only; scratch
  under `/var/tmp` or `/dev/shm` (the host `/tmp` quota exhaustion is standing).
""" % (c1_log_bullet, c2_log_bullet, c3_log_bullet)

merged_log = ("# merged records text — arc3-loop1-round4 LOG entry (seat CN-2, cross connector)\n\n"
 "Assembled 2026-10-19 by seat CN-2 from the chains' literal drafts — literal\n"
 "blocks spliced verbatim, placeholder-normalized. **Pasteable text only**; the\n"
 "parent lands R1. LOG.md is not census-scanned, but the entry keeps the same\n"
 "pin-free voice (one voice across both records). Identity:\n"
 "receipts/identity.txt.\n\n"
 "## Literal LOG entry (append at EOF after the round-3 entry)\n\n"
 "<!-- BEGIN LITERAL ENTRY TEXT -->\n" + log_body +
 "<!-- END LITERAL ENTRY TEXT -->\n")
(OUT / "merged-LOG-entry.md").write_text(merged_log, encoding="utf-8")

print("wrote", OUT / "merged-SCORECARD-section.md")
for f in ["merged-SCORECARD-section.md", "merged-LOG-entry.md"]:
    t = (OUT / f).read_text(encoding="utf-8")
    print("%s: %d lines sha256=%s" % (f, len(t.splitlines()), hashlib.sha256(t.encode()).hexdigest()))
