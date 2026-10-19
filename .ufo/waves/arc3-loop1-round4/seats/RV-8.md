# Seat RV-8 — chain c3 — reviewer — wave arc3-loop1-round4

Task as frozen: review the registry-row + README patch texts for the revised
tool (new sha, case count, new classes) against the landed bytes.

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; HEAD `015e1bab…` (no
seat commits); no git mutations; no write to any real target by this seat
(scratch `/var/tmp/rv8r4`, never `/tmp`; custody paths read-only — hash/stat and
the tool's own read-only captures only). Review protocol pre-registered before
the target existed: `claims/c3/RV-8/prereg.md`.

**Reviewed revision (pinned).** Tool `.ufo/gates/custody-pair/custody-pair.py`
sha256 `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf`
(1343 lines, 65,902 B); gate README sha256
`9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a` (272 lines,
15,293 B) — the final bytes after EX-21's attribution edit (an earlier
`125e7e02…`/267-line revision was also read; all README-side checks were re-run
on the final bytes). Registry row patch text:
`claims/c3/EX-21/patch/proposed-skill-registry-row.patch.md` +
`patch/skill-registry-row.patched.md`. The tool did not move between first read
and final read (3×20 s stability samples, then re-derived at close).

## 1. Work performed (evidence pointers)

All under `claims/c3/RV-8/`:

- `prereg.md` — 10-check protocol, written before the target existed.
- `evidence/class-map.sh` + `evidence/class-map-BEFORE.out` (sha
  `00b3253c…`) and `evidence/class-map-AFTER.out` (sha `81bc39ab…`) — every
  declared exit class plus all four residual vectors, run on the r3 bytes and on
  the landed bytes.
- `evidence/selftest-AFTER-28cases.out` (sha `1cb2f94b…`) — `CLEAN cases=28
  passed=28 failed=0 exit=0`; all 28 case names present in the bytes.
- `evidence/anchor-grader.py` + `evidence/anchors-head.out` — the probe's
  anchor/exact grading replicated over file bytes (no git write).
- `evidence/commandA-head.json` — verbatim SCORECARD recipe at `015e1ba`:
  `83/83, missing [], dangling [], 14/14, 10.0/10.0`.
- Tooling calibrated on the r3 pair before use: extracted `registry-row.diff`
  (8 lines `7c4a7a68…`) and `readme.diff` (122 lines `e61f0a2f…`), applied to the
  `c07af80` blobs → `03832723…`/390 lines and `42b07ee5…`/188 lines — every
  digest EX-30 claimed reproduced exactly.

**Identity re-derivation (rule #14), first-hand at review time:**

| object | claimed | re-derived |
|---|---|---|
| base row (`git show HEAD:SKILL.md`, the `| custody-pair |` line) | `a94e79d9…` | `a94e79d9a4d34795cf7db985ebb58cf46e416dcdb3e38144fc7e5828fc91db89` ✓ |
| patched SKILL file | `8e56f3d9…`, 390 lines | `8e56f3d9ce21d16b2c46a398ad52aa2723c295008a76145b928265bdc88a68bf`, 390 ✓ |
| patched row | `8f8e5408…` | `8f8e5408648c7aacfb0c161eee54c86514f35570f3a8e332526ca5fec136fa0e` ✓ |
| only-line-changed | one row | `diff` = exactly 2 diff lines (`390c390`), nothing else ✓ |
| `r3-to-r4.diff` applied to r3 tool | landed tool | `patch -p1` → `29bb45ae…`, byte-identical to the landed tool ✓ |
| `readme-r3-to-r4.diff` applied to r3 README | landed README | → `125e7e02…` — the **superseded** revision, not the final `9d9400da…` (finding 1) |

## 2. Proposed changes

No write to any real target (reviewer seat). One correction text: none needed
for the landed files — the single finding is an evidence-artifact staleness, not
a file defect. Correction text for it, if the parent wants it recorded in the
wave tree: re-emit `claims/c3/EX-21/tools/readme-r3-to-r4.diff` against the
final README, or append a note to EX-21's `sha256s.txt` naming the delta. This
seat supplies no patch text of its own (the artifact is EX-21's).

## 3. Before → after measurement (chain c3 claim)

First-hand, same harness both sides; before = `7cd19c3c…` (r3), after =
`29bb45ae…` (landed).

| # | residual (claim (a)-(d)) | before (measured) | after (measured) |
|---|---|---|---|
| a | sidecar scope | `--paths X.sha256 --out X` → rc 0, measured file replaced by the 68 B sidecar; `--out X.sha256 --paths X` → rc 0, neighbour replaced by the 1318 B receipt | both spellings → **rc 2** `USAGE: refusing to write a receipt or its derived sidecar over a path it measures, a custody path, or the sidecar-shaped neighbour of one…`; measured file intact (5 B), neighbour never created. Sidecar **inode arm** verified: sidecar path hardlinked to a measured path → rc 2, target intact |
| b | mkdir outside try | `<regular-file>/sub/r.txt` → rc 1 `NotADirectoryError` traceback; read-only parent → rc 1 `PermissionError` traceback | rc 2 `USAGE: cannot create the receipt directory (…)`, **no traceback**; ELOOP parent → rc 2; `--out ''`/`'.'` → rc 2 `USAGE: --out carries no usable name…`; fresh parent chain still created (rc 0) |
| c | coverage gate basis | 5× duplicate stanzas `--require-paths 5` → rc 0, `MATCH paths=1/1`, zero coverage lines (4/5 custody paths unexamined) | rc 2 `USAGE: reference covers 1 of the required 5 distinct paths` + `REFERENCE-COVERAGE: 1/5 … unaccounted: …`; v1 sums dupe 5× → rc 2 as well; five **distinct** paths → rc 0 `MATCH 5/5` (no false positive) |
| d | both-absent semantics | rc 0 `MATCH` `compared=0/11` (undeclared) | rc 0 `MATCH` with the new per-path annotation `both sides record the path absent — the MATCH is an agreement on absence…`; error-carrying on either side → `UNEVALUABLE 14` (re-verified in all four mixed configurations) |
| — | selftest | `CLEAN cases=22` | `CLEAN cases=28 passed=28 failed=0 exit=0`; six new closures named in the bytes and in the README |
| — | live pair (landed tool, scratch receipts) | — | `MATCH 5/5 exit=0` plain and `--require-paths 5`; both receipts self-pin `29bb45ae…`; sidecars equal their receipts' digests; EX-21's committed pair verifies `MATCH 5/5`; r3 receipt vs r4 post receipt → `MATCH 5/5` (cross-revision) |
| — | no-harm instruments (HEAD `015e1ba`) | 83/83, 14/14, 10.0/10.0; probe 0/0 + 13/13; census PASS | unchanged: command A `83/83, missing [], dangling [], 14/14, 10.0/10.0`; probe `reported findings=0` / `clean findings=0`, selftest 13/13; census `PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` |
| — | anchors | 6/6 green at HEAD | 6/6 green against the landed README and the patched SKILL (`skill-registry-custody-pair-row`, `skill-registry-row`, four `custody-readme-*`) |

### Clause-by-clause verdicts (landed README + patched row vs measured behavior)

Every clause of the README's Round-4 hardening section and the row's new
clauses was located in the bytes **and** fired by command. Verdict: **EXISTS**
for all of the following, except the one noted.

| clause | verdict |
|---|---|
| row: "two cleanly-absent stanzas compare MATCH (ruling: only error-carrying stanzas are UNEVALUABLE)" | EXISTS (measured, incl. the annotation line) |
| row/README: `--require-paths N` counts **distinct resolved paths** | EXISTS (dupe → 2, distinct → 0, v1 sums too) |
| row/README: USAGE covers receipt/sidecar/neighbour scope + uncreatable receipt dir | EXISTS (all four vectors fired) |
| row: write-guard cell names derived sidecar + sidecar-shaped neighbour, by resolved path or inode | EXISTS (incl. the hardlink-alias inode arm on the sidecar path) |
| row/README: selftest 22 → 28 with the six closures named | EXISTS (28/28 CLEAN; names match) |
| README: exit-map rows cover tool constants | EXISTS (rows `0 2 3 10 11 12 13 14` ⊇ constants; nothing missing) |
| README: v1 shapes — sums `MATCH-V1-PARTIAL exit 0` clean-control, label-defect `METADATA-DRIFT/LABEL-DEFECT 12` | EXISTS with the standing operator-side drift caveat: live `~/.kimi-code/config.toml` drifted pre-wave (`8cbacd48…`→`bc66d543…`), so the r1 examples read `CONTENT-DRIFT 10` today; clean control (drifted path removed) `MATCH-V1-PARTIAL 4/4 exit 0` — same as r3 |
| README: ruling "adopted here by seat EX-21 with one clause corrected" | EXISTS and **correct**: EX-26's proposed closing sentence ("the coverage gate is a *stanza* gate") is falsified by (c)'s own closure; the landed text states the distinct-path basis and credits EX-26. Cross-patch collision handled, disclosed in both files |
| row/README: no line-pinned citation into an operator-mutable file (rule #11) | EXISTS: no `file:N` token into a mutable file in either; `--paths`/flags/classes named, never tool line numbers |
| README usage block: `selftest [--scratch /dev/shm]` line | NUANCE (not a defect): the tool requires an **existing** scratch base; the Usage example uses `/dev/shm` (exists on this host) and the paragraph below states the requirement explicitly. Same phrasing as r3 |

## 4. Attacks / refutations attempted

- **A1 claim-existence.** Every behavioral clause of the row + README Round-4
  section mapped to code and fired by command (table above). No clause found
  without implementing code. Verdict: **all stand**.
- **A2 apply-integrity.** `r3-to-r4.diff` applied to the r3 tool blob →
  byte-identical to the landed tool (`29bb45ae…`). `readme-r3-to-r4.diff`
  applied to the r3 README → `125e7e02…`, **not** the final `9d9400da…`.
  Verdict: **tool diff intact; README diff stale** (finding 1 below).
- **A3 anchor collision.** The row rewrite rewrites strings the pointer-table
  anchors grade. Re-ran the probe's anchor semantics over the patched SKILL and
  the final README: 6/6 green; probe at HEAD (and against the landed tree,
  table `1b3ab955…` pinned in expected.json) `findings=0` in both modes.
  Verdict: **no collision**.
- **A4 stale tokens.** Scanned landed README + patched row for the superseded
  digests/counts (`7cd19c3c`, `f30df42e`, `cases=22`, "15 cases"): none.
  Verdict: **clean**.
- **A5 compound (c)+(d).** Reproduced first-hand on the r3 bytes: a 5-absent
  reference passed gate + verify (`MATCH 5/5`, `SHA256-CONTRACT: 0/0`). On the
  landed bytes the gate now counts distinct paths and the ruling documents the
  weak-witness reading — the compound case is *adjudicated and documented*,
  which is what the claim requires ((d) is a ruling, not a class change).
  Verdict: **handled as declared**.
- **A6 EX-21's own (d) probe leg.** Its `after-probes.out` "both-absent
  receipt-vs-receipt" leg reads `ABSENT 13`, not `MATCH`. Traced to probe
  construction: its reference was captured **while the file existed** (then the
  file was deleted), so `ABSENT` is the correct class for that fixture. My own
  same-spelling pair and the selftest's `both-sides-absent-is-agreement-match`
  both read `MATCH` with the annotation. Verdict: **probe-leg artifact, not a
  behavior gap** — worth a note in EX-21's matrix but no fix required.
- **A7 live-pair self-pin.** Both receipts' `# tool:` lines equal an
  independently re-derived `sha256sum` of the landed tool. Verdict: **holds**.
- **A8 no-harm.** command A, probe (both modes + selftest), census at the
  settled tree: all unchanged. Verdict: **holds**.

### Finding 1 (evidence artifact, not a file defect)

`claims/c3/EX-21/tools/readme-r3-to-r4.diff` (sha `c1325834a56c…`, 188 lines)
reproduces the **superseded** README `125e7e02…` (267 lines). The final landed
README `9d9400da…` (272 lines) differs by the 5-line attribution note EX-21
added after first landing (the "adopted here by seat EX-26 with one clause
corrected" paragraph). EX-21's report says README-side checks were re-run on the
final bytes, and every claim about the final bytes is true; but the emitted diff
artifact was not re-emitted after the edit, so the diff no longer regenerates
the landed README. Impact: the README itself and every behavioral claim are
correct; only the diff artifact's regeneration claim is stale. Landing does not
depend on this diff (the README is written in place by EX-21, the one authorized
writer). Recommendation for the parent: record the delta (or have the artifact
re-emitted) when the wave tree is committed — no code change needed.

## 5. Blockers

None. Residual notes: (i) the tool+README were written by EX-21 during this
seat's window; the reviewed pin is the final `29bb45ae…`/`9d9400da…` pair, and
the parent must re-derive both at the work commit (rule #14); (ii) the live
custody drift at `~/.kimi-code/config.toml` is operator-side and predates the
wave — any record quoting v1-live classes must read it against that drift.

## Self-identity (rule #14)

- `prereg.md` `2d3aa62eea9c8de2a5f5521ab8ba441d0089216bf9c27a9c664636668a6f8a21`
- `evidence/class-map-BEFORE.out` `00b3253c509e52a80d9a0db013d89f6fd1711a6751007be5363f333aa2d44628`
- `evidence/class-map-AFTER.out` `81bc39ab3ff8ba992f30aa37a6a5e7037dc3d9cd910f3a46a5af34106b91070e`
- `evidence/selftest-AFTER-28cases.out` `1cb2f94bb8cf2a4111a4fa739f0703fa5d7defd12462287d4ce79d121b520055`
- `evidence/commandA-head.json` `2155c2d48bc4aaa0a41c377e0365bef7a007c82eb927e82edae248d1b734c379`
- instrument reviewed: `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` (1343 lines)
- README reviewed: `9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a` (272 lines)
- patched SKILL reviewed: `8e56f3d9ce21d16b2c46a398ad52aa2723c295008a76145b928265bdc88a68bf` (390 lines)
