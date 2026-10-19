# EX-46 — interplay: census PASS with the landed table; command A unchanged; the digest pin matches the landed table bytes

Seat EX-46 · chain c3 · role executor · wave `arc3-loop1-round3` · 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`.
The artifact pair was **read-only** for this seat; every mutation ran on marked copies in a
scratch clone under `/var/tmp/ex46/clone` (never `/tmp`). No git mutation in the repo.

Task (seat line): after EX-41 lands the arc3-era pointer-table extension
(`.ufo/gates/citation-drift/pointer-table.json` + `expected.json`), verify the interplay:
**census PASS with the landed table; command A unchanged; the digest pin matches the landed
table bytes.**

## 0. Verdict — all three legs CONFIRMED on the landed bytes

| leg | pre-landing (T0 13:07Z) | landed (T1 13:13Z) | verdict |
|---|---|---|---|
| census v10 (`c1-census-v10.py`, `d0772ce8…`) | PASS `stale=0 ambiguous=0 undeclared=0 unresolved=0`, exit 0 | PASS, output **byte-identical** (sha256 `c8d97713…` both sides) | PASS with the landed table |
| command A (SCORECARD.md:92-124, `REV`-labeled) | `{"mapped":82,"knowledge_files":82,"missing":[],"dangling":[],"citation_resolved_rules":14,"rule_blocks":14,"coverage_score":10.0,"depth_score":10.0}` | identical modulo the `revision` label — at HEAD, in an isolation clone owning **only** C3's pair, and re-measured at 13:15Z after C2's landing | unchanged |
| digest pin (expected.json `pointer_table.sha256`) | `738b3a56…` == table sha256 (MATCH) | table `bfc42f1b…` == pin `bfc42f1b…` (MATCH; the pin moved with the table) | matches the landed bytes |

Supporting, on the landed bytes: probe `reported findings=0 exit=0` (default) and
`clean findings=0 exit=0` (`--strict`); selftest `cases=13 passed=13 failed=0 exit=0`;
expected.json's `frozen_run.revision`, `snapshots` and 13-case selftest list unchanged —
only the pin field moved (mechanical diff, §4).

## 1. Why the three legs are structurally independent (read-sets, cited)

- **Census read-set** = its declared `SCOPE` table (`c1-census-v10.py:215-237`: PROVINCE.md,
  SKILL.md, SCORECARD.md) — `files = sorted({s[0] for s in SCOPE})` (`:509`), plus the three
  live client configs for anchor re-derivation (`CLIENTS` `:204-206`, `live_pins` `:253`). The
  census never walks the tree and never reads `.ufo/`.
- **Command A read-set** = immutable Git objects only: `git ls-tree … corpus/knowledge`,
  `corpus/README.md` (`## Coverage map`), `SKILL.md` (`## Queue-drain craft`)
  (SCORECARD.md:88-124).
- **C3's landing write-set** = `.ufo/gates/citation-drift/pointer-table.json` +
  `expected.json` — disjoint from both. The invariance is therefore structural, and it is
  measured, not assumed (§3, §5).

## 2. Pre-landing baseline (T0, 13:06-13:08Z) — `baseline/`

- Table 14,694 B sha256 `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`
  (31 entries / 4 quoted / 3 exempt); expected.json `ff47bfd6…` pins that digest;
  probe `e2665074…`; census `d0772ce8…` (`baseline/sha256-baseline.txt`).
- `pin-check.py` → `PIN_CHECK: VERDICT MATCH`, rc 0 (`baseline/pin-check.txt`).
- Census PASS, exit 0 (`baseline/census-default.txt`, sha256 `9f383bc0…` including the
  appended `census_exit=0` line; marker-stripped form sha256 `c8d97713…`).
- Command A at `c07af80` (`baseline/commandA-HEAD.txt`); re-run pinned to `HEAD`
  (`baseline/commandA-HEAD-recheck.txt`) — equal modulo the label.
- Probe default/strict both `findings=0 exit=0`; selftest 13/13 (`baseline/probe-*.txt`,
  `baseline/selftest.txt`). All runs with disk-backed `TMPDIR=/var/tmp/ex46`.

## 3. Rehearsal in a scratch clone (T0.5) — `scratch/`

Before EX-41 landed, the landing was rehearsed so the post-landing battery would not be the
first measurement: `sim-landing.py` appended 3 candidate-shaped arc3 entries (31 → 34) and
re-pinned expected.json (`738b3a56…` → `8907bb48…`) in the clone
(`/var/tmp/ex46/clone`, commit `e970440`).

- probe default/strict over the re-pinned pair → `findings=0 exit=0` (`sim-probe-default.txt`,
  `sim-probe-strict.txt`).
- **Stale-pin drill**: same table, old pin supplied via `--expected` → `pointer_table_tampered
  … exit=2` (`sim-probe-stalepin.txt`) — the pin is load-bearing, not decorative.
- **One-byte drill**: table mutated by one byte with the correct pin → `pointer_table_tampered
  … exit=2`; restored → `findings=0 exit=0` (`sim-onebyte-tamper.txt`).
- **Census over the sim landing** → byte-identical to baseline (diff empty; both sha256
  `c8d97713…`, `sim-census.txt`).
- **Command A over the sim commit** → equal modulo the revision field
  (`sim-commandA.json`; `COMMAND_A_EQUAL_MODULO_REVISION: True`).

## 4. The landed pair (T1, 13:13Z) — `post/landed-identity.txt`

EX-41 wrote both files 13:12-13:13Z (mtimes 1792415557 / 1792415608; its own FINAL capture
`claims/c3/EX-41/05-identity-and-diff.txt` 13:13:38Z).

| object | pre | landed | delta |
|---|---|---|---|
| `pointer-table.json` | 14,694 B `738b3a56…`; 31 entries / 4 quoted / 3 exempt | **30,348 B `bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7`; 57 entries / 4 quoted / 8 exempt** | +26 entries, +5 exempt, 0 other movement |
| `expected.json` | `ff47bfd6…`, pin `738b3a56…` | `d97dd60a942eaf53771c8224e84a9e8cdaf976dc66c3a543a450b1f1fa3827e2`, pin `bfc42f1b…` | pin only |
| probe / census | `e2665074…` / `d0772ce8…` | identical | instruments unchanged |

Independently re-derived (not trusted from EX-41): entries 0..30 **prefix-equal** to the
committed table (`git show HEAD:…`), 0 duplicate ids, `quoted` equal, `exempt` prefix-equal,
`_doc` prefix preserved (`post/new-entries.json` holds the 26 new objects). The expected.json
delta enumerated key-by-key: the **only** changed node is `/pointer_table/sha256`;
`frozen_run.revision` (`679af5d749f2…`), `snapshots` and the 13-case selftest list are
byte-equal.

## 5. Interplay measurements on the landed bytes — `post/`

- **Digest pin**: `pin-check.py` → `VERDICT MATCH` rc 0 (13:13:48Z, re-derived 13:15:11Z,
  re-derived again 13:15:34Z after C2's landing, saved 13:16:40Z — digests unmoved across the
  settle window; `post/pin-check-post.txt`, `post/final-pin-check.txt`). The pin now names the
  landed bytes and no longer the T0 bytes:
  the F3 coupling held inside the pair.
- **Census at HEAD, landed table on disk**: `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
  unresolved=0)` exit 0; `diff` against the T0 output empty →
  `CENSUS_BYTE_IDENTICAL_ACROSS_LANDING` (`post/census-diff.txt`, `post/census-post.txt`,
  `post/final-census.txt` — the final run re-measured after C2's custody landing).
- **Command A**: at HEAD equal modulo `revision` (`post/commandA-compare.txt`); in the
  isolation clone at commit `4b1917f` (c07af80 + **only** C3's landed pair) equal modulo
  `revision` (`post/clone-commandA.txt`, `ISOLATED_COMMAND_A_EQUAL_MODULO_REVISION: True`) —
  the pair alone moves nothing; the round's eventual 83/83 lives in C1's corpus landing, not
  here. Clone census also byte-identical (`post/clone-census.txt`); clone probe `clean
  findings=0 exit=0`.
- **Probe on the landed table at HEAD**: default `findings=0 exit=0`, `--strict` `clean
  findings=0 exit=0` (`post/probe-post-*.txt`); selftest remains 13/13
  (`post/selftest-post.txt`).
- **Teeth (the landed entries are load-bearing)**: in the clone, two cited sources were
  corrupted (QUALITY.md:21 `parsed-and-empty` → `parsed-and-blank`; custody README precedence
  line reworded) → `citation_dead entry=arc3r1-entry-quality-11` and `citation_dead
  entry=custody-readme-precedence`; default `reported findings=2 exit=0`, strict `failed
  findings=2 exit=1` (`post/teeth-default.txt`, `post/teeth-strict.txt`); clone reset to
  `4b1917f` and re-verified `clean findings=0 exit=0`.
- **Cross-chain landing during my window**: C2's EX-21 rewrote
  `.ufo/gates/custody-pair/{README.md,custody-pair.py}` (13:14Z; README sha moved
  `039993ed…` → `f30df42e…` by 13:15Z). None of it enters the census/command-A/pin read-sets;
  the final battery above was re-run at 13:15:34Z with those files modified on disk and every
  leg held. (The landed table's custody-README anchors are checked at `--rev HEAD` against the
  *committed* README; EX-41's `10-cross-seat-check.txt` additionally greps the *worktree*
  rewrite and finds each needle present — a parent-integration re-probe will read the
  committed rewrite.)

## 6. Attacks / refutations attempted (with verdicts)

| # | attack | result |
|---|---|---|
| A1 | "table changed without re-pin → silent clean" — stale pin supplied | REFUTED: `pointer_table_tampered`, exit 2 |
| A2 | "pin is decorative" — one-byte table edit with correct pin | REFUTED: tampered, exit 2 |
| A3 | "extension perturbs the census" | REFUTED: byte-identical outputs (sim + landed + post-C2) |
| A4 | "extension perturbs command A" | REFUTED: equal modulo the `revision` label; isolation clone narrows the counterfactual to C3's pair only |
| A5 | "the landed entries are dead weight / entries the probe cannot see" | REFUTED: needle corruption in two distinct cited files fires both new anchors, strict exit 1 |
| A6 | "EX-41's additive claim is a restatement" | REFUTED as trust-dependency: prefix equality, dup-id count, quoted equality, `_doc` prefix independently re-derived from `git show HEAD:…` |
| A7 | "the pin matched only because the pair was captured once" | REFUTED as one-shot: MATCH re-derived at 13:13:48, 13:15:11, 13:15:34Z; digests unmoved |
| A8 | "sibling C2 landing voids the interplay measurements" | REFUTED: read-sets disjoint, final battery re-run on the mutated tree holds |

## 7. Identity discipline (rule #14)

Every digest above is re-derived from the file bytes at capture time by
`claims/c3/EX-46/pin-check.py` (table ↔ pin) and `sha256sum` (instruments, evidence).
`post/landed-identity.txt` and the final re-derivations at 13:15:34Z agree; the manifest
`claims/c3/EX-46/manifest.sha256` pins this claim directory's evidence files, generated after
this document was final; no identity is cited from an earlier revision.

## 8. Blockers / gaps

- None blocking. The parent's **work commit** does not exist yet at seat time; command A at
  the work commit is the parent's integration measurement (expected delta: C1's corpus
  landing only — 82 → 83 knowledge files, map row, rule counts; C3's pair contributes none
  of it, per §5).
- The landed table's custody-README anchors will next be read at the *committed* rewritten
  README once C2's landing is committed; EX-41's worktree grep covers the interim state.