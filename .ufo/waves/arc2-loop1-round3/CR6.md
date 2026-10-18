# CR6 (critic) — separability attack: does C2's knowledge entry (if held) move C1's census denominator or C3's pinned table?

Seat CR6, wave `arc2-loop1-round3`, 2026-10-18. Read-only on every repo and home
file; **the only write is this report**. No git mutations in the repo (all
commits below were made in a throwaway clone `/tmp/arc2-l3r3-CR6-clone`, a fresh
`git clone` of this repo at `679af5d`), no config edits, no installs, no network.
Scratch: `/tmp/arc2-l3r3-CR6-{clone,gate.py,contract-amend.json,*}` only.
Pre-pair receipt verified before my leg: **5/5 OK, rc=0**.

## 1. Verdict

**SEPARABLE AT THE TEST LEVEL — but NOT at the edit level, and one direction is
live: C2's landing *does* move C3's pinned table (measured, gate rc=1), while
C1's census denominator does not move for any landing shape C2 can choose. Two
further defects found: (a) the round's own recommended landing form (E8 FORM 2,
line-neutral amend) is REJECTED by the round's own gate as currently pinned —
the gate must be re-pinned to the amend envelope before use; (b) C3's proposed
r4-16 errata text re-introduces a `config.toml:1284-1292` token and *increases*
the round-3 dead-pointer count 7 → 8 under E20's own census instrument.**

1. **C2 → C1 (denominator): NO COUPLING.** C1's census scoped set is
   `SCORECARD.md:265-275` + the two knowledge files (round-3 seat line; E4 §2.5,
   E20 §1.5). C2's new entry file is not in that set, and its own text carries
   **0** `config.toml:<N>` tokens (measured). C1's denominators (7 dead tokens in
   the scoped set under E20's instrument) are unchanged whether C2 holds or not.
2. **C2 → C3 (pinned table): LIVE COUPLING, measured.** C3's gate pins
   `readme-90/138/160/177` at their base line numbers and `readme-shape` with
   `inserts: [68, 153]`. A row-insert landing (the shape C3 rehearsed) shifts
   four pinned pointers: gate **VERDICT failed, rc=1** with six FINDINGs. The
   line-neutral amend form (E8 FORM 2, `+2/−2`, 187→187 lines) keeps all four
   pointers resolving — but is itself rejected by the pinned shape envelope
   (`FINDING readme-shape … hunk @@ -22,1 outside envelope []`), rc=1. With the
   envelope re-pinned to `allow: [[22,22],[117,117]], max_del: 2`, the amend form
   passes clean, rc=0.
3. **C1 → C3: clean.** C1's fix alone (the `:270` reword) passes C3's gate
   **VERDICT clean, rc=0** — one `+1/−1` hunk inside the pinned `[270,270]`
   envelope. No C3 dependency.
4. **The combined amend-form landing is command-A neutral and gate-clean**
   (`80/80, 10/10, 10.0/10.0`; rc=0 under the re-pinned contract) — but only if
   C3's §5.3 second errata block is dropped or rewritten, because its quoted
   `config.toml:1284-1292` token re-adds a dead locus under E20's census (§4).
5. **The seat line's named hazard is real in the C2→C3 direction and absent in
   the C2→C1 direction.** The separating mechanism is *line-shape*, not shared
   test inputs: C3's pinned table is a line-number table, so any C2 landing that
   changes README line counts moves it; C1's census is content-class scoped, so
   it is immune to where C2's row lands.

## 2. Evidence — commands run THIS session with observed output

All from repo root unless noted; stamps `date -u` → `2026-10-18T18:10:25Z`,
`18:14Z`, `18:20Z`. Repo HEAD `679af5d749f2fd48b9d543e3c99d348d5458f90f`;
`git status --porcelain` → `?? .ufo/waves/arc2-loop1-round3/` only.

### 2.1 Pre-pair receipt and base state

```console
$ tail -n +2 .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
$ wc -l PROVINCE.md SCORECARD.md SKILL.md corpus/README.md LOG.md
  162 PROVINCE.md   766 SCORECARD.md   336 SKILL.md   187 corpus/README.md  1065 LOG.md
$ python3 - "679af5d..." <<'PY'   # command A verbatim (SCORECARD.md:92-123)
{"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "679af5d...", "rule_blocks": 10}
```

### 2.2 C1's scoped set — content census at HEAD (E20's instrument, verbatim)

Instrument patterns read from `.ufo/waves/arc2-loop1-round3/E20.md:356-357`:
`config\.toml:(\d+)(?:-(\d+))?` and `config\.toml`?\s+lines?\s+(\d+)(?:\s*-\s*(\d+))?`.

```console
$ python3 -   # scoped files: SCORECARD.md, mcp-registrations.md, r4-16-frontier-rescan.md
BASE 679af5d: config.toml tokens=7 dead=7
   DEAD SCORECARD.md:59  'config.toml:2940'
   DEAD SCORECARD.md:291 'config.toml:1478'
   DEAD SCORECARD.md:698 'config.toml:2940'
   DEAD corpus/knowledge/2026-10-13-mcp-registrations.md:11  'config.toml lines 1285-1292'
   DEAD corpus/knowledge/2026-10-13-mcp-registrations.md:18  'config.toml line 1288'
   DEAD corpus/knowledge/2026-10-13-mcp-registrations.md:88  'config.toml:1284'
   DEAD corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43 'config.toml:1284-1292'
```

(The "dead" test used the live stanza range `:3296-3303`, read this session:
`[mcp_servers.rea]` at `:3296`, pin `:3298`, `startup_timeout_sec` `:3299`,
config 3322 lines, sha `bd5a78d1…` = the pre-pair receipt hash.)

### 2.3 C2's landing forms — the two shapes in play, both from round-3 seat text

- **Insert form** (C3 §5.4: map row after base `:68`, Knowledge row after base
  `:153`): measured `+2/−0`, README 187→189, last map row `:68`→`:69`.
- **Amend form** (E8 Block B, "FORM 2 — recommended"): the two exact replacement
  rows are E8.md lines 205 and 211. Cells verified against base rows:
  B1 rest-of-row == README:22 rest-of-row (**True**); B2 differs from README:117
  only in cells 0 and 3 (entry list + date `2026-10-13 + 2026-10-18`).
  Measured `+2/−2`, README 187→187, last map row stays `:68`.

### 2.4 C3's gate, extracted from its report and re-run here

Extraction from `C3.md:414-950` (fenced `python` block) → 535 lines;
`sha256 0a3e74801114e866a0515bca8297de0eca332431238e12a38aa88ec24834ebbe`
= the hash C3's §4 reports. Its own selftest, my run:

```console
$ python3 /tmp/arc2-l3r3-CR6-gate.py --selftest
C1..C10 ok    selftest PASS 10/10    rc=0
```

Baseline, in my clone at `679af5d`: `VERDICT clean, rc=0`.

### 2.5 The three landing experiments (isolated clone, one commit each)

```console
# (a) C1's fix alone — C3 §5.1 reword of SCORECARD.md:270
$ git diff --numstat 679af5d HEAD      → 1  1  SCORECARD.md
$ python3 gate.py --repo . --pin 679af5d
OK scorecard-shape: SCORECARD.md: +1 -1 hunks=1
OK readme-shape: corpus/README.md untouched
VERDICT clean    rc=0

# (b) C2 amend form (E8 FORM 2) + new entry file
$ git diff --numstat 679af5d HEAD      → 2  2  corpus/README.md ; 1 0 corpus/knowledge/…-retry.md
$ python3 gate.py --repo . --pin 679af5d
FINDING readme-shape  corpus/README.md: hunk @@ -22,1 outside envelope []; hunk @@ -117,1 outside
                      envelope []; deletions 2 > 0
VERDICT failed    rc=1
$ python3 gate.py --repo . --pin 679af5d --contract /tmp/arc2-l3r3-CR6-contract-amend.json
    (readme-shape: allow=[[22,22],[117,117]], inserts=[], max_del=2)
OK readme-shape: corpus/README.md: +2 -2 hunks=2
VERDICT clean    rc=0

# (c) C2 insert form (map row after :68 + Knowledge row after :153)
$ git diff --numstat 679af5d HEAD      → 2  0  corpus/README.md ; 1 0 corpus/knowledge/…-retry.md
$ python3 gate.py --repo . --pin 679af5d
FINDING readme-90-safety   corpus/README.md:90 lacks 'r2-jq-shadow-verdict.*benign'; identical line now at :91
FINDING readme-160-safety  corpus/README.md:160 lacks '2026-10-13-round-2.*benign'; identical line now at :162
FINDING readme-177-frontier corpus/README.md:177 lacks 'Runtime-obs depth'; identical line now at :179
FINDING readme-138-r13row  corpus/README.md:138 lacks 'round-13-distillation'; identical line now at :139
VERDICT failed    rc=1
```

**This is the coupling, measured**: the insert shape moves C3's four pinned
pointers; the amend shape does not, but the gate as pinned rejects the amend
shape. The two round-3 seat drafts disagree about the shape; C3 §5.2 assumes
insert (`+1`/`+2` shifts), E8 Block B recommends amend ("**Do not add rows**").

### 2.6 The combined landing (amend form + C1 reword + both errata appends)

```console
$ git diff --numstat 679af5d HEAD
1  1  SCORECARD.md
2  2  corpus/README.md
10 0  corpus/knowledge/2026-10-13-mcp-registrations.md
8  0  corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md
1  0  corpus/knowledge/2026-10-18-a2r3-01-godot-arm64-scale-retry.md
$ python3 gate.py --repo . --pin 679af5d --contract contract-amend.json | tail
OK readme-shape: corpus/README.md: +2 -2 hunks=2
VERDICT clean    rc=0
$ python3 - "HEAD" <<'PY'   # command A at the combined commit
{"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 80, "mapped": 80, "missing": [], "revision": "HEAD", "rule_blocks": 10}
```

### 2.7 The C1×C3 defect: C3's errata text increases C1's dead count

Under E20's census instrument over the three scoped files:

```console
BASE 679af5d: config.toml tokens=7 dead=7
COMBINED landing (with C3 §5.3 errata as drafted): config.toml tokens=8 dead=8
   … new: DEAD corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:940 'config.toml:1284-1292'
new entry file config.toml tokens: 0
```

C3's §5.3 second block quotes the superseded pointer
(`- The `:43` citation of `~/.kimi-code/config.toml:1284-1292` is superseded:`),
and the quoted token is scanned by E20's instrument as a live dead locus. If C1's
after-value is measured with the round-3 landing in place, C3's own errata makes
N go 7 → 8. The first errata block is clean (no `config.toml:<N>` token).

### 2.8 C2 → C1 denominator check

```console
scoped files: 3 (C2's new file NOT in the scoped set)
new entry file config.toml tokens: 0
```

C1's census denominator is the scoped-file set (3 files) and the token count
within it (7). C2's entry lands at `corpus/knowledge/2026-10-18-…-retry.md`,
outside the set, and contributes no tokens. **No coupling.**

### 2.9 C1's `:270` fix text, checked for the same class

```console
BASE    : SCORECARD.md:270 token '`:157`' -> '| entry | round | gist |' (dead)
          SCORECARD.md:270 token '`:160`' -> Lessons round-2 row (dead reading)
COMBINED: SCORECARD.md:270 token '`:177`' -> '- Runtime-obs depth — … held, not frontier' (resolves)
```

C3 §5.1's replacement (`:177 in HEAD; :160 was stale at write`) is content-correct
under my read; the `:157` token remains in the line as the historical reading,
which is the intended record. Note the reword keeps the sentence's own claim
"recorded as named debt, not silently fixed" although `SCORECARD.md:68-72` now
reads "Closed; kept as a record" — C2's round-3 report calls this a content-stale
sentence; the reword does not address it.

## 3. Separability matrix (this seat's measurements)

| Pair | Does the first claim's landing change the second's test input? | Verdict |
|---|---|---|
| C2 → C1 | No — entry outside C1's scoped set; 0 `config.toml:<N>` tokens in the entry; C1's token census 7/7 dead identical before and after | **independent** |
| C2 → C3 | **Yes** — insert form shifts `readme-90/138/160/177` (4 FINDINGs) and moves the map/Knowledge insert points; amend form moves none but violates the pinned shape envelope as currently written | **coupled (line-shape)** |
| C1 → C3 | No — the `:270` reword is a `+1/−1` same-line repair inside `[270,270]`; gate clean rc=0 | **independent** |
| C1 → C2 | No — C2's tests read README `:90/:160` cells and the new entry; C1 writes only SCORECARD/knowledge files | **independent** |
| C3 → C1 | **Yes, adverse** — C3's §5.3 r4-16 errata adds a scanned `config.toml:1284-1292` token at `:940`, raising C1's dead count 7 → 8 | **coupled (adverse)** |

Strict sense (each claim verifiable at a revision where only it is landed):
C1 ✔ (2.5a), C2 ✔ (2.5b with the correct envelope; 80/80), C3 ✔ (baseline
clean). Weak sense (one combined landing): holds **only** if the shape decision
is made first and C3's errata text is rewritten token-free.

## 4. Text for the parent to land VERBATIM

### Block A — the shape decision (choose one; do not mix)

```text
Round-3 landing shape (CR6 measurement, 2026-10-18). Two shapes are in the
round's own drafts and they are not interchangeable:

INSERT (C3 §5.4): map row after base corpus/README.md:68 + Knowledge row after
base :153. Measured: +2/-0, README 187->189; last map row :68->:69; C3's pinned
pointers readme-90/138/160/177 all drift (gate rc=1, four FINDINGs with the
"identical line now at :N" locator). If chosen, land C3 §5.2's re-points in the
SAME commit and re-pin the gate's pointer table and shape envelope.

AMEND (E8 FORM 2, "recommended"; E8.md:144-151): replace the two existing
r4-12 rows in place (corpus/README.md:22 and :117, cells 0 and — for :117 —
also the date cell). Measured: +2/-2, README stays 187 lines, every tracked
pointer unmoved, command A 80/80, 10.0/10.0. This is the shape the round's own
simulation measured at 80/80 with zero shifts.

Decision rule: if the round wants its landing to be pointer-neutral, AMEND; the
gate's readme-shape envelope must then be re-pinned to
allow=[[22,22],[117,117]], inserts=[], max_del=2 (measured: rc=0 with that
contract, rc=1 with the as-written contract). Do not land the amend form under
the insert-shaped contract, and do not land the insert form without the
re-points.
```

### Block B — C3's errata text must not quote the dead pointer

```text
The r4-16 errata block drafted at .ufo/waves/arc2-loop1-round3/C3.md:355-364
quotes `config.toml:1284-1292` inside its explanatory sentence. Under the
round-3 dead-pointer census (E20.md:355-357 instrument: every
config.toml:<line> token in the scoped files, resolved against the live stanza
:3296-3303), that quoted token is scanned as a locus and counts dead — measured:
the combined landing carries 8 dead tokens, not 7; the extra is this line
(r4-16-frontier-rescan.md:940). Rewrite the errata without the token, e.g.:

- The `:43` citation of the kimi stanza's config line range is superseded: the
  config file is rewritten in place by its owner and the stanza has moved
  several times since (four rewrites on 2026-10-18 alone). Read the stanza by
  its header `[mcp_servers.rea]`, whose pin line stayed byte-identical.

(measured: this form adds no scanned token; the census stays 7 dead before and
after the landing.)
```

### Block C — the separability statement for the round record

```text
Separability (CR6, arc2-loop1-round3). Measured in an isolated clone at
679af5d with C3's own gate (sha256 0a3e7480…, selftest 10/10): C1's fix alone
passes clean (rc=0); C2's amend-form landing keeps every pinned pointer
resolving but fails the as-written shape envelope (rc=1) and passes with the
envelope re-pinned to the amend ranges (rc=0); C2's insert-form landing breaks
four pinned README pointers (rc=1, four FINDINGs). C1's census denominator is
unchanged by any C2 landing: the entry file is outside C1's scoped set and
carries no config.toml line token. One adverse coupling exists in the other
direction: C3's drafted r4-16 errata re-introduces a scanned dead token,
raising the round's dead-pointer count 7 -> 8; rewrite it token-free. The
three claims are acceptance-test independent; the round is only landable as
one commit if the shape decision (Block A) and the errata rewrite (Block B)
precede it.
```

## 5. Conclusions, labeled

**Observations** (ran or read this session at `679af5d`):

- Pre-pair receipt 5/5 OK, rc=0; `config.toml` sha `bd5a78d1…`, 3322 lines,
  stanza `:3296`, pin `:3298`.
- Command A at base: 79/79, 10/10, 10.0/10.0.
- C3's gate extracted from its report runs and passes selftest 10/10 here; its
  sha256 matches C3's own reported hash.
- Gate verdicts, three landings: C1-alone clean rc=0; C2 amend failed rc=1
  (shape) and clean rc=0 with the re-pinned envelope; C2 insert failed rc=1 with
  four pointer FINDINGs (`:91`, `:162`, `:179`, `:139` locators).
- E8's Block B rows match the base rows' remaining cells (B1 exact; B2 cells 0
  and 3 changed); measured `+2/−2`, 187→187.
- Combined landing (amend + C1 + errata): gate clean rc=0 under the re-pinned
  contract; command A 80/80, 10/10, 10.0/10.0.
- E20-instrument census: 7 dead config.toml tokens at base; 8 after the combined
  landing with C3's drafted errata; the extra locus is
  `r4-16-frontier-rescan.md:940`.
- C2's entry file contains 0 config.toml line tokens; C1's scoped set contains 3
  files, none of them C2's.
- `scripts/` and `.ufo/gates/` do not exist (gate home is the parent's call);
  `SKILL.md` registry table is `:334-336`, one row.

**Inferences**:

1. C2 → C1 is genuinely separable because C1's census is content-scoped, not
   line-scoped; no C2 landing shape can move it. The seat line's hypothesis is
   answered **no** for the denominator direction.
2. C2 → C3 is a real line-shape coupling: C3's pinned table is a line-number
   table, so it is downstream of C2's shape choice. The remedy is mechanical
   (pick amend, or land the re-points in the same commit), not architectural.
3. The round's drafts are internally inconsistent about the shape (C3 assumes
   insert; E8 recommends amend and says "do not add rows"). Landing either
   without the other's adjustment fails the round's own gate.
4. C3's errata quoting the dead pointer is the same defect class the gate exists
   to catch, one level up: the fix text itself becomes a census locus.
5. Command A cannot see any of this: it reads no README line citations, so the
   insert form would still read 10.0/10.0 while breaking four pinned pointers.

**Unknowns**:

1. Which shape the parent picks (amend vs insert) — the re-point list and the
   gate contract depend on it. E8's own text recommends amend; C3's rehearsals
   and §5.2 assume insert.
2. Whether the parent re-pins C3's gate contract at landing time or lands the
   insert form with re-points; both are self-consistent, neither is done yet.
3. Whether `SCORECARD.md:270`'s "recorded as named debt, not silently fixed"
   clause is also to be corrected (the `:68-72` bullet now reads "Closed; kept
   as a record"); C3's §5.1 reword does not address it, C2's round-3 report
   flags it.
4. Whether C2's claim will hold (the BATTERY leg's outcome is E11's to record;
   E8/E20 both observed a live `AnalyzeHeadless` with `-Xmx8G` still running at
   their read time). If C2's leg refuses/times out, the entry lands as a
   recorded negative and Block A/B still apply to the README rows.
5. Whether the round-3 receipts land in the same commit — the gate's `--pin`
   guard is unaffected, but the staged-set expectation grows.

## 6. Scope compliance / residue

- Repo writes: this report only. `git status --porcelain` before and after →
  `?? .ufo/waves/arc2-loop1-round3/` only; HEAD unchanged at `679af5d`.
- All experiment commits live in `/tmp/arc2-l3r3-CR6-clone` (4 commits over the
  base). Scratch: `/tmp/arc2-l3r3-CR6-{gate.py,contract-amend.json,clone,
  readme22.txt,readme117.txt,E8rows.txt,gate-raw.txt}`.
- One clone-local file `arc2-l3r3-CR6-gate.py` sits in the clone worktree (my
  scratch copy; not in the repo).
- No network, no installs, no config edits, no git mutation in the repo, no
  other seat's namespace touched. No runaway processes to kill.

## 7. Reproduction commands

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
git rev-parse HEAD; git status --porcelain
tail -n +2 .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt | sha256sum -c -

# extract C3's gate from its report (C3.md:414-950), then:
python3 /tmp/arc2-l3r3-CR6-gate.py --selftest                       # PASS 10/10

# clone + three landing experiments
rm -rf /tmp/arc2-l3r3-CR6-clone && git clone -q . /tmp/arc2-l3r3-CR6-clone
cd /tmp/arc2-l3r3-CR6-clone && git checkout -q 679af5d
# (a) C1 fix: edit SCORECARD.md:270 per C3 §5.1; commit; gate → clean rc=0
# (b) amend form: replace corpus/README.md:22 with E8.md:205 and :117 with
#     E8.md:211; add the entry file; commit; gate → failed rc=1 (shape);
#     gate --contract /tmp/arc2-l3r3-CR6-contract-amend.json → clean rc=0
# (c) insert form: insert map row after :68 + Knowledge row after :153;
#     commit; gate → failed rc=1 (four pointer FINDINGs)

# census (E20.md:356-357 patterns) over the three scoped files at base vs combined
```
