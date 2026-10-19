# EX-02 (c1, executor) — dry-run of EX-01's rule #14 patch on a scratch tree

Seat EX-02 · chain c1 · wave arc3-loop1-round2 · 2026-10-19.
Task: build a scratch tree (`git archive` of `corpus/knowledge` + `corpus/README.md`
+ `SKILL.md` under `/var/tmp`), apply EX-01's rule patch, run command A
(recipe `SCORECARD.md:92-124`) — expect rules 14, 14/14 resolved, prior-13 craft
rules byte-identical. **Result: the claim verifies.** All commands below ran
under `/var/tmp/ex02-dryrun` (host `/tmp` is quota-exhausted, standing hazard).

## 1. Pre-image and scratch tree

| Item | Value |
|---|---|
| HEAD | `14b1682b1128d2e41085ebc79c9addeb8786d420` |
| SKILL.md (pre-image) | 371 lines, sha256 `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb` |
| corpus/README.md | sha256 `6ac43e838bca7d08cc7ac3c24cff60042cb174d92b08363db0798fa844163577` |
| scratch tree | `git archive HEAD corpus/knowledge corpus/README.md SKILL.md \| tar -x -C /var/tmp/ex02-dryrun/tree` — 82 knowledge `.md` + `.gitkeep` + README + SKILL, 85 files |
| craft section (command A's split) | 161 lines, sha256 `5dff0b655cd4300fc613a1b88b8f33dfbb1b86b370f641d069ddf50eeefbcb87` (`craft-before-canonical.txt`) |

Command A is written against `git show REV:path`, so a scratch-tree run needs a
translation. `commandA-scratch.py` replaces only the two read paths
(`get(path)` → file read; `git ls-tree` → `rglob`) — the section splits, the
citation regex and the resolution loop are byte-for-byte the recipe.

**Fidelity control (run before any patch existed):** stock command A at `REV=HEAD`
in the lane repo and the scratch variant on the unpatched tree produced the same
JSON (only the `revision` label differs):

```
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [],
 "rule_blocks": 13}                      # commandA-pre.json (stock run: CR-1/command-a-head.txt, SC-1/command-A-before.txt)
```

## 2. The patch under test

`.ufo/waves/arc3-loop1-round2/claims/c1/EX-01/rule14.patch.md` — 8,833 bytes,
sha256 `7cd9e950d227b4fa496a3cde1db6b84167d9fbce6b2088dbe94c2d6d6c340b7c`.
Re-checked at 12:10Z after EX-01's `identity-final.txt` landed: **unchanged**, so
this dry-run exercised the current revision (rule #14's own failure mode — a
revision after the identity was recorded — did not occur here).

- payload (lines strictly between EX-01's `payload-begin`/`payload-end` markers):
  **896 bytes**, sha256 `a47dc38d1e12856bb34b3f1310af7109d65c649f8eef17a5feb3c00781623b80`
  — matches the patch's own claim exactly (`ex01-payload.txt`).
- EX-01's predicted post-image: 385 lines, sha256 `19057c131038352ba1bee1aec007401de774cc88a9ef42cde2cc09dcbe6f4e90`.

## 3. Application — two independent recipes, both reproduce EX-01's hash

| Recipe | Result |
|---|---|
| EX-01 §2 anchor form (insert after the unique `kernel-OOM-killed (…:23-37`).` line) | 385 lines, sha256 `19057c131038352ba1bee1aec007401de774cc88a9ef42cde2cc09dcbe6f4e90` |
| EX-01 §2 unified diff, `patch -p1` (dry-run rc 0, apply rc 0; 13 added, 0 removed) | 385 lines, **same sha256** |

EX-01's predicted post-image identity is confirmed byte-exactly by two
mechanically independent applications (`ex01.diff`, sha256 `f581c2d88de91e2436855c4cf6288551d6965143e3a388330dfd68457c437b16`).

## 4. Command A after the patch — the claim's core numbers

```
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [],
 "rule_blocks": 14}                       # commandA-post.json, anchor form
```

Identical for the diff-form tree. **rules 13 → 14, 14/14 resolved, 82/82 mapped,
coverage 10.0, depth 10.0** — no other counter moved.

The counted citation is `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7`
(33-line file; line 7 is the `recheck:` line, i.e. the line the incident turned
on). All five cited ranges resolve and carry the clauses they support
(`citation-range-check.txt`):

| Citation in the payload | Resolves | Line content carries |
|---|---|---|
| `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7` | yes | the entry's `recheck:` line (the revised line) |
| `.ufo/waves/arc3-loop1-round1/seats/CR-2.md:86-89` | yes | F2: `8,316 B / f95c5a05…` stale vs `8,598 B / d8d85949…` |
| `.ufo/waves/arc3-loop1-round1/seats/VZ-1.md:115` | yes | D9 table row: re-apply `9,513 B ≠ claimed 8,316 B` SUSTAINED |
| `SCORECARD.md:1366-1368` | yes | fresh identity `10,225 B, sha256 dd986f56…` recorded at landing |
| `LOG.md:1411-1412` | yes | landed identity `(10,225 B, sha256 dd986f56…)` |

## 5. Prior-13 byte-identity — verified, with one honest nuance

- `cmp` of SKILL.md lines 1-239 (pre) vs 1-239 (post): **byte-identical, rc 0**.
  Every byte at or before the insertion point is untouched.
- `cmp` of the pre tail (line 240→) against the post tail (line 254→):
  **byte-identical, rc 0**. The insertion is pure — nothing removed or reordered.
- Rule-block extraction (split on `^- \*\*`, as command A reads the section):
  12 of 13 blocks byte-identical; **rule 13's block differs only in trailing
  separator newlines (2 → 1)** because rule #14 now follows it directly, and the
  blank separator line that used to precede `## Config custody` now follows
  rule #14. Rule 13's content is byte-identical after `rstrip` (sha256
  `430dc4e42ff4e5d3…`) — see `rule-block-compare.txt`, `separator-analysis.txt`.

**Strict reading:** 12/13 blocks byte-identical; rule 13's *text* is identical,
its trailing separator byte is not. The claim's wording ("prior 13 craft rules
byte-identical") is true at the rule-content level and true for every byte of
the pre-image; it is not true if "rule block" means "including the separator
whitespace between the last pre-existing rule and the next section". EX-01's own
checker (`EX-01/evidence/rule-bytes.txt`) reports the same `DIFF rule 13`, so
this is a shared, understood property, not a defect discovered only here.

Markdown well-formedness holds: rules 1-10 and 12 already follow each other with
a single newline; rule #14 continues that convention. Post-patch
`## Config custody` moves 242 → 256.

## 6. Independent instrument reproductions (instrument pinned by sha256)

C2's EX-16 is editing the live worktree census this round, so the census was
pinned to the HEAD blob — `census-v10-HEAD.py`, sha256
`6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` (the same
digest EX-01's patch cites; the live worktree copy is `c95a5cf3…`, not mine to
touch).

| Check | Result |
|---|---|
| census on complete HEAD archive, pre-append | `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, rc 0 — sha256 `d3da75092dfeba0b7eb587818cda42e0e71df9e7c35a97061e2c2fcd60d7c304` |
| census on complete archive, post-append | `VERDICT: PASS (…)`, rc 0 — sha256 `bbe55bc1d92cb4d7bb500daf341de4b339e3cfc179fc34449d220560acfa289b` |
| full-output diff pre vs post | **exactly one line**: `SKILL.md lines=371 loci=2` → `SKILL.md lines=385 loci=2` |
| census token scan over the 896 payload bytes (census's own PIN/VER/PTR/CACHE/REA_GATE patterns, `.ufo/gates/c1-census-v10.py:230-234`) | `0 / 0 / 0 / 0 / 0` — E21 form confirmed |
| citation-drift probe at `REV=HEAD` (read-only) | `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`; `--strict` → `clean findings=0 exit=0` |
| SHONEN.md:6 needle emulation | needle `A mitigation claim carries its natural control` at line 233 in **both** trees, inside the pinned range `81-243` → the probe's range needle stays resolvable; the range end and the `13/13` count go stale post-append (EX-01 §4.3 drafts the same-line refresh) |

EX-01's own census receipts (`EX-01/evidence/census-before.txt` `d3da7509…`,
`census-after.txt` `bbe55bc1…`) are **byte-identical** to these two independent
runs.

**Shape caveat.** "PASS on both scratch copies" holds for a *complete* archive.
On the narrower tree this seat was told to build (knowledge + README + SKILL
only), both pre- and post-patch runs read
`VERDICT: FAIL (stale=0 ambiguous=0 undeclared=0 unresolved=0)` with 13
`SCOPE-ERRORS … marker uncheckable (file unreadable)` — an artefact of the
absent scoped files, identical on both sides, not of the patch. The verdict
statement should name the archive shape.

## 7. Attacks attempted

1. **Metric form-fork (pre-registered, `prediction-prereg.md`, written before the
   patch existed).** Measured with the parser itself: a wave-tree-only rule text
   scores 13/14 → depth 9.29; a text carrying one resolvable `corpus/knowledge`
   reference scores 14/14; a decoration-only control also scores 14/14. EX-01's
   landed text is the citation-bearing branch → 14/14 as predicted. **Verdict:**
   the count is not evidence of craft (decoration passes it); the verdict must
   rest on the cited content, which this seat checked line-by-line (§4).
2. **Stale-twin attack (rule #14's own failure mode).** Doctored the payload's
   size claim (`8,316 B` → `999 B`; doctored payload sha256 `8a6f1458…`) and
   re-ran the instruments on a complete tree: command A still reads 14/14, and
   the census output is **byte-identical** to the true-payload run
   (`census-full-doctored.out` sha256 `bbe55bc1…` = post-patch run). **Verdict
   (unfavourable, reported):** no committed instrument enforces rule #14 — the
   discipline is procedural (seat re-derivation + the integrator recording the
   fresh identity at landing). The rule text should not be read as
   instrument-enforced.
3. **Prior-13 claim read strictly.** See §5 — the block-level comparator flags
   rule 13; investigated to the byte, shown to be separator whitespace with
   identical content. **Verdict:** claim holds for content and for every
   pre-existing byte; the stricter block-extraction reading is false and is
   recorded rather than smoothed over.
4. **Patch-revision drift (rule #14 against its own artifact).** Re-hashed
   `rule14.patch.md` after EX-01's `identity-final.txt` landed: unchanged
   (`7cd9e950…`). EX-01's identity file re-derives artifact / payload / patched
   SKILL.md identities; all three were independently reproduced here. **Verdict:**
   no stale self-identity on this artifact.

## 8. Boundary of this dry-run

- The **work commit does not exist yet**; every measurement here is against a
  scratch tree built from HEAD `14b1682`. The frozen claim's "at the work commit"
  still requires the parent's command A run after landing (EX-01 §4.1 states the
  same expectation: rules 14/14).
- Nothing outside `/var/tmp/ex02-dryrun` and this seat's claim directory was
  written; custody paths were not touched; no git mutation ran.

## 9. Files in this directory

| File | sha256 | What |
|---|---|---|
| `dryrun.md` | recorded in `identity-final.txt` (a hash inside the file it describes is stale by construction — rule #14) | the dry-run record |
| `prediction-prereg.md` | `8f3b1c70a692961d45c388bab48039f244172c3660b182a21da209d3e44e2c45` | pre-registered fork, written before the patch existed |
| `commandA-scratch.py` | `37bffa2774b9dedb99d3a55aaa0cf4901047c31d95cbeac2fde65b139807a463` | command A translated to a scratch tree |
| `rule-resolution-probe.py` | `fe40376bef3be504472e807101ae161db02cdf7408f294cce610edf4907d24b3` | candidate-form metric probe |
| `verify-rules.py` | `de94637d048870e40de4750aa5d5988d40e46172390fc997760ace3d737f6c67` | rule-block comparator |
| `commandA-pre.json` | `ae4a9ee5e483592623128a981d2d40ef420559e7a2fcab04269545271b769b22` | command A, unpatched tree |
| `commandA-post.json` | `2f4535844f9f515c360582ef8d5873251a97ec8da08a45dc2a9ca7e124d331b8` | command A, patched tree |
| `craft-before-canonical.txt` | `5dff0b655cd4300fc613a1b88b8f33dfbb1b86b370f641d069ddf50eeefbcb87` | craft section, command A's split |
| `ex01-payload.txt` | `a47dc38d1e12856bb34b3f1310af7109d65c649f8eef17a5feb3c00781623b80` | EX-01 payload, extracted verbatim |
| `ex01.diff` | `f581c2d88de91e2436855c4cf6288551d6965143e3a388330dfd68457c437b16` | EX-01 unified diff, extracted verbatim |
| `rule-block-compare.txt` | `1faba3c6f3fb7170f2657ecb8e67c36159d097315ae34c11938baf6fb8203254` | per-block comparison output |
| `separator-analysis.txt` | `ad36ce4c2cde42e284e5d5f92109e0e1e0351dd9a22a828a3ddac6a1cb776b24` | rule 13 separator bytes |
| `citation-range-check.txt` | `6d7d05e51b98bd1d91c7e9f7c7f3beeb53fe0d7ddc261fe5a6db9c4e82c03077` | every cited range, verbatim |
| `census-full-pre.out` / `-post.out` / `-doctored.out` | `d3da7509…` / `bbe55bc1…` / `bbe55bc1…` | census on complete archive (pre / post / stale-twin) |
