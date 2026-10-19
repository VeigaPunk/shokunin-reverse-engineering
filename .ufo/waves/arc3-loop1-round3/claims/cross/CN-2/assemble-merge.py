#!/usr/bin/env python3
"""CN-2 (arc3-loop1-round3) merge assembler — v3, C1 folded.

Extracts the literal blocks from the landed chain drafts (C1: one block holding
the LOG entry then the SCORECARD section; C2/C3: separate files), splices the
C1/C2/C3 bullets byte-faithfully (placeholder convention normalized), and
composes the merged SCORECARD section + LOG entry with this seat's connector
text. Writes to claims/cross/CN-2/ and prints source/segment shas.
"""
import hashlib, pathlib, re, sys

W = pathlib.Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3")
OUT = W / "claims/cross/CN-2"
SCRATCH = pathlib.Path("/dev/shm/cn2r3/blocks")
SCRATCH.mkdir(parents=True, exist_ok=True)

def read(p):
    return p.read_text(encoding="utf-8")

def literal(path):
    txt = read(path)
    m = re.search(r"<!-- BEGIN LITERAL [A-Z ]+ -->\n(.*?)<!-- END LITERAL [A-Z ]+ -->", txt, re.S)
    if not m:
        sys.exit("no literal block in %s" % path)
    return m.group(1)

def norm_placeholders(s):
    s = re.sub(r"⟨(N ≥ 17)⟩", r"[[FILL: \1]]", s)
    s = re.sub(r"⟨(N)⟩", r"[[FILL: \1]]", s)
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
    print("segment %s: %d lines sha256=%s" % (name, len(text.splitlines()), hashlib.sha256(text.encode()).hexdigest()[:16]))

c1_src = W / "claims/c1/records-drafts/records-drafts.md"
c2_src = W / "claims/c2/records-drafts/scorecard-section-draft.md"
c2_log_src = W / "claims/c2/records-drafts/LOG-entry-draft.md"
c3_src = W / "claims/c3/records-drafts/scorecard-section-draft.md"
c3_log_src = W / "claims/c3/records-drafts/log-entry-draft.md"

# --- C1: one literal block holding LOG entry then SCORECARD section ---------
c1_block = literal(c1_src)
(SCRATCH / "c1.block").write_text(c1_block, encoding="utf-8")
print("source c1: %d lines sha256=%s" % (len(c1_block.splitlines()), hashlib.sha256(c1_block.encode()).hexdigest()[:16]))
cut = c1_block.index("\n## arc3-loop1-round3")
c1_log_block, c1_sec_block = c1_block[:cut], c1_block[cut + 1:]
c1_sec_bullet = norm_placeholders(bullet_block(c1_sec_block, "- C1 coverage (owned)", ["- C2 operability (fleet)"]))
c1_log_bullet = norm_placeholders(bullet_block(c1_log_block, "- C1 coverage (owned)", ["- C2 operability (fleet)"]))
seg("c1-sec-bullet", c1_sec_bullet)
seg("c1-log-bullet", c1_log_bullet)

m = re.search(r"\n\| coverage — C1 \| (.*?) \| improved ⟨FILL: parent confirm⟩ \|", c1_sec_block, re.S)
c1_row = "| coverage (owned) — C1 | " + m.group(1).strip() + " | improved [[FILL: parent confirm]] |"
m = re.search(r"Learning trends: (coverage — .*?no formula claimed\)\.)", c1_sec_block, re.S)
c1_learn = m.group(1).strip()

# --- C2 / C3 ---------------------------------------------------------------
sources = {}
for name, p in [("c2-sec", c2_src), ("c2-log", c2_log_src), ("c3-sec", c3_src), ("c3-log", c3_log_src)]:
    b = literal(p)
    (SCRATCH / (name + ".block")).write_text(b, encoding="utf-8")
    sources[name] = b
    print("source %s: %d lines sha256=%s" % (name, len(b.splitlines()), hashlib.sha256(b.encode()).hexdigest()[:16]))

c2_sec_bullet = norm_placeholders(bullet_block(sources["c2-sec"], "- C2 operability (fleet)", ["- Measured at the records commit", "- Custody"]))
c3_sec_bullet = norm_placeholders(bullet_block(sources["c3-sec"], "- C3 freshness (fleet)", ["- Measured at the records commit", "- Custody"]))
c2_log_bullet = norm_placeholders(bullet_block(sources["c2-log"], "- C2 operability —", ["- Custody", "- Measured"]))
c3_log_bullet = norm_placeholders(bullet_block(sources["c3-log"], "- C3 freshness (fleet)", ["- Custody", "- Measured"]))
seg("c2-sec-bullet", c2_sec_bullet)
seg("c3-sec-bullet", c3_sec_bullet)
seg("c2-log-bullet", c2_log_bullet)
seg("c3-log-bullet", c3_log_bullet)

c2_txt = read(c2_src)
c2_row_m = re.search(r"\n\| operability \(fleet\) — C2 \| (.*?) \| improved \|\n", c2_txt, re.S)
c2_row = "| operability (fleet) — C2 | " + c2_row_m.group(1).strip() + " | improved |"
c2_row = re.sub(r"⟨[^⟩]*⟩", "[[FILL: …]]", c2_row)
c2_learn = re.search(r"C2's:⟩ (.*?)Planned:", c2_txt, re.S).group(1).strip()
c3_txt = read(c3_src)
c3_row = "| freshness (fleet) — C3 | 31 entries, no arc3-era coverage → [[FILL: N]] entries with every pinnable arc3 citation table-covered or adjudicated NO-ENTRY; digest re-pinned in the expected-values file in the same commit; findings 0 in both modes at the work commit; selftest 13/13 unchanged | improved |"
c3_learn = re.search(r"C3's:⟩ (.*?)Planned:", c3_txt, re.S).group(1).strip()

OPENING = """Round 3 of arc 3 (loop 1; 3/10). Axis set: **coverage (owned)**,
operability (fleet), freshness (fleet); all three owned proxies stay tied at
10.0 with none retired, so the owned claim is selected by the standing
most-falsifiable-next-claim tie-break. The claims are causally separable — the
corpus knowledge surface, the custody tool and the probe's pointer table share
no edit target. Roster frozen PRE-DISPATCH (mechanically enumerated, 24+24+12+4
= 64, every name exactly once; the items-array assertion held at dispatch);
the wave rides the token-plan lane per the operator's deepseek-v4.1-flash swarm
directive (recorded in the round-2 records)."""

WAVE_BULLET = """- Wave: 64 seats; `alibaba-token-plan/deepseek-v4.1-flash` (token-plan key 1 of
  3); reports `.ufo/waves/arc3-loop1-round3/`; round report
  `.ufo/reports/arc3-loop1-round3/kaidoku.md`. Delivered [[FILL: N/64 per the
  roster reconciliation (VZ-4), never the declared count]]. Landed at [[FILL:
  work / wave-artifacts / records commits]]."""

MEASURED_BULLET = """- Measured at the records commit: [[FILL: command A at the settled tree;
  probe selftest + findings both modes; census PASS 0/0/0/0; custody post-pair
  MATCH 5/5]]. The connector's own pre-landing measurements: the records text
  appended to scratch copies of the scoped files reads census PASS 0/0/0/0 with
  an injected-pin control FAILing (`undeclared=1`), the PIN-FREE checker reads
  CLEAN on both literal bodies, and the C2 registry-row patch text projected
  in place (with the section appended) also reads PASS."""

TRENDS = "Learning trends: %s %s\n%s" % (c1_learn, c2_learn, c3_learn)

CARRIED = """Carried debt (named): the stale province EVM frontier bullet (doubly stale
across two real-compiler rounds — candidate one-line refresh, protected file,
not landed); optimizer runs values other than 200 / the `viaIR` pipeline /
vyper (Unknowns); the sealed-id domain measured only as path-sensitive. C2
keeps named: D1 (capture TOCTOU — misclassification, not an undetected
tamper), D4 (receipt self-authentication — the sidecar is not an anchor for a
tampered receipt), D5 (out-of-band/root class: the tool is a tripwire for
attribution, not an integrity control against an actor sharing its trust
domain), and D7 (write-guard hardlink evasion — named as precision, not
severity). C3 adds [[FILL: the adjudicated NO-ENTRY items that stay named debt,
with causes]]. Standing: the host `/tmp` quota exhaustion (the EVM rechecks
fail EDQUOT under a `/tmp`-defaulted run — a disk-backed scratch is a recipe
requirement, not advice); the pre-existing dirty
`.ufo/waves/arc2-loop1-round10/C3.md` (not this round's). Retired: [[FILL: none
/ list]]."""

section = """## arc3-loop1-round3 — coverage + operability + freshness: [[FILL: verdict phrase per the parent's admission]], 2026-10-19

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
Planned: [[FILL: round 4 per schedule; token-plan key 2 of 3]].
%s
""" % (OPENING, WAVE_BULLET, c1_sec_bullet, c2_sec_bullet, c3_sec_bullet, MEASURED_BULLET,
       c1_row, c2_row, c3_row, TRENDS, CARRIED)

merged_sec = ("# merged records text — arc3-loop1-round3 (seat CN-2, cross connector)\n\n"
 "Assembled 2026-10-19 by seat CN-2 from the chains' literal drafts (C1 = SC-2\n"
 "`records-drafts.md`; C2 = SC-4; C3 = SC-5 — all spliced verbatim,\n"
 "placeholder-normalized; sources + shas in the outline's merge-delta table).\n"
 "**Pasteable text only** — nothing here is applied; the parent lands R1/R2.\n"
 "The section is PIN-FREE by construction and measured (outline §6.4); identity\n"
 "of this file: receipts/identity.txt (rule #14 — not inlined).\n\n"
 "## Literal SCORECARD section (append at EOF after the round-2 section)\n\n"
 "<!-- BEGIN LITERAL SECTION TEXT -->\n" + section +
 "<!-- END LITERAL SECTION TEXT -->\n")
(OUT / "merged-SCORECARD-section.md").write_text(merged_sec, encoding="utf-8")

log_body = """### arc3-loop1-round3 — coverage: EVM optimizer-enabled dispatch shapes + operability: custody-pair hardening + freshness: citation-drift table extension (2026-10-19)

- Dispatch: 64 seats frozen PRE-DISPATCH (roster enumerated mechanically —
  24+24+12+4, every name exactly once; the items-array assertion held at
  dispatch, the counting lesson's wire-it gate); `alibaba-token-plan/
  deepseek-v4.1-flash` (token-plan key 1 of 3 — operator directive: the
  deepseek-v4.1-flash swarm waves ride the token-plan lanes). Delivered
  [[FILL: N]]/64 per the roster reconciliation (count the items array, never
  the intent).
%s
%s
%s
- Custody: [[FILL per CU-1 / the C2 landing: pre-pair capture time + 5/5, post-pair
  capture time + 5/5, the in-window drift comparison; any operator-side churn
  recorded verbatim, not repaired; the connector independently reproduced the
  four before-injections against the committed revision and their declared
  after-classes against the in-window revision on scratch fixtures]].
- Scope: kaidoku repo only; no pushes (standing rule); no installs (C1 reuses
  the round-1 receipted compiler prefix; receipt re-verified); custody paths
  read-only; scratch under `/var/tmp` or `/dev/shm` (the host `/tmp` quota
  exhaustion is standing — no recipe in this round uses `/tmp`).
""" % (c1_log_bullet, c2_log_bullet, c3_log_bullet)

merged_log = ("# merged records text — arc3-loop1-round3 LOG entry (seat CN-2, cross connector)\n\n"
 "Assembled 2026-10-19 by seat CN-2 from `claims/c1/records-drafts/records-drafts.md`\n"
 "(LOG part), `claims/c2/records-drafts/LOG-entry-draft.md` and\n"
 "`claims/c3/records-drafts/log-entry-draft.md` — literal blocks spliced verbatim,\n"
 "placeholder-normalized. **Pasteable text only**; the parent lands R1. LOG.md is\n"
 "not census-scanned, but the entry keeps the same pin-free voice (one voice\n"
 "across both records). Identity: receipts/identity.txt.\n\n"
 "## Literal LOG entry (append at EOF after the round-2 entry)\n\n"
 "<!-- BEGIN LITERAL ENTRY TEXT -->\n" + log_body +
 "<!-- END LITERAL ENTRY TEXT -->\n")
(OUT / "merged-LOG-entry.md").write_text(merged_log, encoding="utf-8")

print("wrote", OUT / "merged-SCORECARD-section.md")
for f in ["merged-SCORECARD-section.md", "merged-LOG-entry.md"]:
    t = (OUT / f).read_text(encoding="utf-8")
    print("%s: %d lines sha256=%s" % (f, len(t.splitlines()), hashlib.sha256(t.encode()).hexdigest()))