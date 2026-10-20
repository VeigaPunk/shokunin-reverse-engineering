# R18 closure residuals — routed or unrouted (R19 W1 scout)

Seat `KaidokuR19.R18ClosureResiduals`, read-only. Anchors: `SPOT` = `corpus/lessons/round-18-verifier-spotcheck.md`;
`L18` = `corpus/lessons/round-18.md`. Baseline B = `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. The lane's
`refs/heads/main` was at `85589ac757f9ca3cb25efcd702d0963e25c9c4df` when read (integration in flight); the residual
block is byte-identical at B and at that tip (sha256 of lines 97–101: `8e4cbebc…f8210` at both). No tools installed
or updated; nothing written except this report. All checks are Git-object reads, no lane tool executed.

## Answer

Three of the four residual bullets are subsumed by routed defects; the fourth (r17 `SHA256SUMS`) is **unrouted**.
It also survives only as a *disclosure* attached to the already-closed `R17-SUMS-RUNLOG`, and the disclosure
compresses a three-state history into "edited in place".

| Residual (`SPOT`) | Text | Routed defect | Round-19 seat / counter rule | Verdict |
|---|---|---|---|---|
| :98 | `validator-sha256-pinned` gate check is format-only | **R18-VALIDATOR-DIGEST**, clause 1 (`SPOT:194`) | seat `ValidatorDigestGuard` (`gen-wave1.py:79-85`); counter rule (`gen-wave1.py:53-56`) mutates a wrong digest and requires R17-VALIDATE16 to open | routed, fully specified |
| :99 | VALIDATE16 remapped inputs carry no digest of the `/tmp` copies; tie rests on label set + 341 count | **R18-VALIDATOR-DIGEST**, clause 2 — `SPOT:194` says "Also retain the digest of each remapped receipt copy in `validate16/summary.json`" | seat `Validate16RemapDigests` (`gen-wave1.py:86-93`); counter requires `W19/evidence/validate16-remap/digests.json` with one sha256 per copy, copies retained and re-hashing equal (`gen-wave1.py:55-56`) | routed, with a depth caveat (§C) |
| :100 | `pins` and `go-buildinfo-probe` "Pinned values" cells name no path | **R18-REGISTRY-PINNED** (`SPOT:198`) | scribe `SkillRegistryDraft` (`gen-wave1.py:377-380`), applied by the L1; counter rule: path that exists at REV **or** the literal `probe; no persisted baseline` (`gen-wave1.py:65-66`) | routed, with a calibration caveat (§B) |
| :101 | the frozen r17 `SHA256SUMS` was edited in place (disclosed) | **none** — not among `SPOT:193-199`; only `L18:57`, the named correction of the already-closed `R17-SUMS-RUNLOG` | no executor, scout, reviewer or counter in the W1 roster touches r17 prediction evidence (`gen-wave1.py:43-171`); `SpotcheckAnchors` verifies only `SPOT:191-199` and `:201-206` (`gen-wave1.py:267-270`) | **unrouted** |

Observation: `claims.json` C1 counts exactly seven defects (`7 at 8a8da7e -> 0`), so residual :101 is outside the
round's falsifiable statement as written. Inference: if C1 closes 7/7, the SUMS residual remains live with no owner.

## Evidence for the three routed mappings

- `R18-VALIDATOR-DIGEST` clause 1 is exactly :98. At B the check is `routed-defects.py:463-467`: it tests
  `isinstance(vs, str) and len(vs)==64 and hex`, and its own detail string says `(format only; see limits)`.
  The committed value is correct today — own check: `git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py |
  sha256sum` = `618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f`, equal to
  `summary.json:82`. So the defect is about the guard, not a wrong value; the seat's expected post-fix result
  (`gen-wave1.py:84-85`) matches.
- Clause 2 is exactly :99. `summary.json:68-79` holds `from`/`to` (`/tmp/r17-validate16.MWZBce`)/`tree`/
  `scope` ("16 occurrences per receipt")/`live_paths_left_unremapped` and **no digest field**; the eight
  receipt entries carry only `label`, `kind`, `exit`, `checks_performed: 341`, `findings`, `stdout_sha256`.
  The 341 count is uniform (own: `grep -c '"checks_performed": 341'` → 8), and the eight `stdout_sha256` values
  are hash-bound to retained stdout by the existing `summary-stdout-bound` check (`routed-defects.py:468-485`).
  That is the "label set + 341-count consistency" the residual names.
- `R18-REGISTRY-PINNED` is exactly :100. At B, `SKILL.md:542` (`pins`) reads `Pinned values: none (no expected
  digests; each entry records sha256, size and mtime_ns at the instant read)` — i.e. it already *states* there is
  no baseline but names no path; `SKILL.md:545` (`go-buildinfo-probe`) reads `Pinned values: the build-info magic
  and header constants of go1.25.0 debug/buildinfo (…, S024)` — a source identity, no lane path. The gate only
  requires the token `Pinned values:` (`routed-defects.py:660-661`), which both rows satisfy.

## The unrouted residual — r17 `SHA256SUMS`

Observation (own, `git show`/`git cat-file`/`cmp`):

| Revision | Lines | Size | sha256 | Content delta |
|---|---|---|---|---|
| `2711674` (r17 freeze) | 17 | 1847 | `d89e6de808fbba17b5dc5e3f88c83c102eadb956e797b1e35a8c0748637b9b26` | frozen manifest, includes `8ac38afe… carriers.tsv` |
| `95e34db` (r17 w2) | 17 | 1862 | `1b46b3edf114d98d93c39b92397cea5dcbe2c5699703f17a0abc7a3fd97ab42e` | **drops** the `carriers.tsv` line, **adds** `f5ce3d6… replicate-expectations.json` |
| `b2aad08` (r18) and B `8a8da7e` | 18 | 1953 | `b4ed972f568f2b0b3ae78d6947898c906851a6c10e0a5a141a563bb287399a11` | restores `carriers.tsv`, keeps the appended line |

The 2711674 blob is a byte **prefix** of the B blob (`cmp` of `2711674` against the first 17 lines of `8a8da7e` →
exit 0). So the frozen bytes were never rewritten; one line was appended after the r17 run.

Observation (this is the part the spotcheck does not record): the round-17 verification pin matches the
**intermediate** state, not the freeze and not the current file. `.ufo/waves/round-17/verification.json:1796-1800`
(`pins_pre`) and `:1972-1976` (`pins_post`) both record `sha256 1b46b3ed…ab42e`, `size 1862` — the `95e34db`
blob. `L18:57` says "the restore makes the SHA256SUMS digest pinned in round-17 verification.json stale by
design"; that is true, but the pin was already off the frozen blob *before* round 18 (it binds the r17 w2 edit).
A later auditor re-deriving r17 freeze evidence from the pin alone will mismatch and has only prose to explain
it; the residual's phrase "edited in place" names one state where three exist and one pin.

Observation (existing guard, and its blind spot): the only check touching this file is `R17-SUMS-RUNLOG`'s
substance branch (`routed-defects.py:590-607`): `rev_lines = set(...)`, then every 2711674 line must be *present*.
Set membership catches loss, is blind to additions and reordering by construction — exactly the residual — and the
`sums-covers-carriers-tsv` named check (`:563-585`) covers only the restored `carriers.tsv` digest. Neither the
round-19 counter (`gen-wave1.py:45-71` counts only the seven R18 defects) nor `measure.py`/`verify.py`
(`gen-wave1.py:155-164`) asserts prefix-only growth or the pin's staleness.

**Proposal: the round should address it now — as a correction plus retained evidence, not as an eighth defect.**

- Keep `claims.json` C1 at seven. Its falsifiable wording is `7 at 8a8da7e -> 0`; adding an eighth item
  mid-round would rewrite the stated before/after rather than strengthen it, and the L1 owns claims. The
  residual is a custody disclosure, not a broken check.
- Required, cheap (append-only text, no r17 byte edit — honours `claims.json` non_goals):
  1. One correction line `- R18-SUMS-INPLACE: …` in `corpus/lessons/round-19.md` (the skeleton already reserves
     `- R18-<ID>:` lines, `gen-wave1.py:353-357`) stating the three blob states above, the pin binding
     `95e34db`, and that B's file is a strict prefix-append of `2711674`.
  2. A carried entry in that lesson's `## Open` list, because the current Open list (`L18:86-92`) does not
     mention the SUMS at all.
  3. Retained census evidence (6 lines, no new tool) under `W19/evidence/r17-sums/`: the `cmp` prefix check, the
     per-rev sha256/size table, and re-hash of all 18 lines against blobs at B. Command template is in §Commands
     (`A2`, `A3`-adjacent loop). This is what makes the claim reproducible instead of prose.
- Optional, only if the L1 is willing to amend claims: an eighth counter rule asserting
  `git show 2711674:…SHA256SUMS` is a byte prefix of `git show REV:…SHA256SUMS` and that any growth line is
  `predictions/replicate-expectations.json`. Cost is small, but it changes the frozen `7 -> 0` and duplicates a
  property `routed-defects.py:590-607` already half-guards. Not recommended this round.

Rationale for "address": this is the only residual that mutates a *frozen* artifact — the property round-18's C3
and the quality axis rest on. Leaving it inside a lesson's "Residuals" bullet with no counter means round 19 can
show 7/7 routed defects closed while the one freeze-custody residual stays invisible to every round-19 surface.

## Advisory calibration notes for the L1

**B. The REGISTRY-PINNED counter literal is narrower than the defect it encodes.** `gen-wave1.py:65-66` accepts a
path that exists at REV **or** the exact string `probe; no persisted baseline`; `SPOT:198` says "name the path or
state that the row is a probe with no persisted baseline". For `pins` (`SKILL.md:542`) the literal is truthful and
matches the existing "none (no expected digests…)". For `go-buildinfo-probe` (`SKILL.md:545`) the row pins
constants tied to go1.25.0 `debug/buildinfo` (S024), so `probe; no persisted baseline` would pass the counter while
discarding provenance the row already carries; the truthful path form is the tool blob
`.ufo/waves/round-17/tools/buildinfo-probe.py` (exists at B). Scribe should use path-for-buildinfo, literal-for-pins,
or name both. Inference: a token-only pass here would repeat the class of defect (`format-only`) that :98 already
names.

**C. The remap re-creation binds *new* copies, not the r18 originals.** `summary.json` retains no copy digest
(`:68-79`) and the r18 evidence retains only per-label `exit`/`stdout_sha256`. The round-19 seat re-creates the
copies (`gen-wave1.py:86-93`) and the counter checks the new files re-hash (`:55-56`), so the residual's "tie to
`da64646`" becomes: copy-equivalence for validator purposes is evidenced by reproduced exit 0 and `stdout_sha256`
per label, not by byte-identity with what the r18 run read. The named correction should say that — otherwise :99
is over-claimed as "the original input is now digested". This is a limit, not a blocker: `stdout_sha256` matching
is a real behavioural binding, and the seat is told to report any divergence honestly (`gen-wave1.py:92-93`).

## Commands (observed, with exits)

```text
$ git show 8a8da7e:corpus/lessons/round-18-verifier-spotcheck.md | awk 'NR>=97 && NR<=101'
- **Residuals.** No fabrication survives, and none reopens a defect:
  - The `validator-sha256-pinned` gate check is format-only.
(remaining bullets :99-101 omitted here; :99-101 quoted verbatim in §Mapping / §The unrouted residual)
exit=0   (full 5-line block read; :97-101)

$ git show 2711674:.ufo/waves/round-17/predictions/SHA256SUMS | cmp - <(git show 8a8da7e:.ufo/waves/round-17/predictions/SHA256SUMS | head -17)
(no output)
exit=0   -> 2711674 blob is a byte prefix of the first 17 lines at B

$ git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum
618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f  -
exit=0   -> equals summary.json:82 validator_sha256

$ git show 8a8da7e:.ufo/waves/round-18/evidence/validate16/summary.json | grep -c '"checks_performed": 341'
8
exit=0

$ for r in 2711674 95e34db b2aad08 8a8da7e; do printf "%s " $r; git show $r:.ufo/waves/round-17/predictions/SHA256SUMS | sha256sum; done
2711674 d89e6de808fbba17b5dc5e3f88c83c102eadb956e797b1e35a8c0748637b9b26  -
95e34db 1b46b3edf114d98d93c39b92397cea5dcbe2c5699703f17a0abc7a3fd97ab42e  -
b2aad08 b4ed972f568f2b0b3ae78d6947898c906851a6c10e0a5a141a563bb287399a11  -
8a8da7e b4ed972f568f2b0b3ae78d6947898c906851a6c10e0a5a141a563bb287399a11  -
exit=0

$ git show 8a8da7e:.ufo/waves/round-17/verification.json | awk 'NR>=1796 && NR<=1800'
      ".../round-17/predictions/SHA256SUMS": {
        "mtime_ns": 1792506450355219266,
        "sha256": "1b46b3edf114d98d93c39b92397cea5dcbe2c5699703f17a0abc7a3fd97ab42e",
        "size": 1862
      },
exit=0   (same entry at :1972-1976, pins_post)

$ git diff 2711674 95e34db -- .ufo/waves/round-17/predictions/SHA256SUMS   (excerpt; header/context omitted)
-8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv
+f5ce3d6ba0da04749a65f63295540f82610e13adfe931fb39c67be75b7cb72d5  predictions/replicate-expectations.json
exit=0

$ git diff 95e34db b2aad08 -- .ufo/waves/round-17/predictions/SHA256SUMS   (excerpt; header/context omitted)
+8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv
exit=0

$ git show 8a8da7e:corpus/lessons/round-18-verifier-spotcheck.md | awk 'NR>=191&&NR<=206'
(seven routed defects :193-199 and carried items :201-206; none names the SUMS)
exit=0

$ grep -n '^add("' .ufo/waves/round-19/gen-wave1.py   (excerpt of 70+ hits)
43 RoutedR18Tool, 72 MidmapListStep, 79 ValidatorDigestGuard, 86 Validate16RemapDigests, ...
(no seat named for r17 SUMS / round-17 prediction evidence)
exit=0

$ git rev-parse refs/heads/main ; git status --porcelain
85589ac757f9ca3cb25efcd702d0963e25c9c4df
?? .ufo/waves/round-19/w1/
exit=0
```

## Remaining unknowns

- Whether the L1 elects to amend claims to eight items. My recommendation is no (§The unrouted residual), and the
  correction+evidence route needs no claims change.
- Whether the r17 knowledge entry (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`) or `SCORECARD`
  should also carry the pin-vs-freeze note. Inference: the lesson line is sufficient for a later auditor who
  starts from `L18:57`; a SCORECARD append would need an owner I do not have.
- The `95e34db` SUMS edit (drop `carriers.tsv`, add `replicate-expectations.json`) is a round-17 w2 act, outside
  this round's routed set and outside `SPOT:97-101`; I did not attribute an owner to it beyond the blob history.
