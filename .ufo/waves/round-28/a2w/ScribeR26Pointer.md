# ScribeR26Pointer — routed defect 1 of `corpus/lessons/round-27-verifier-spotcheck.md:150-152`

Role: scribe. Lane read-only; no lane writes except this report. Finished 2026-10-22T18:40Z.

## Behavior

Defect 1 asks for two drafts: a round-27 pointer appended to
`corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md` (naming the
`analyze`/`inspect` table rows and `## Use`), and a QUALITY row superseding row 37 — both
saying the `analyze`/`inspect` content-keyed id holds only when both paths map to the same
Ghidra snapshot suffix (S083; round-27 entry
`corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md`).

## Finding — the defect is already fixed on the lane (observation)

Lane HEAD moved during this seat's run and is now `071270b5` (main). Both items exist:

- `git show 071270b5:corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md`
  lines 137-146 hold `## Pointer appended in round 28 (routed defect 1 of
  `corpus/lessons/round-27-verifier-spotcheck.md:152`)`. Its text names table rows
  `analyze`/`inspect` (`:32-33`) and `## Use`, and states the id is the same across two paths
  only when both map to the same snapshot suffix (`target-<sha256[0:12]><suffix>`; suffix is
  the extension if it matches `^\.[A-Za-z0-9]{1,12}$`, else `.bin`), citing the round-27 entry
  and S083. Committed by `2832c5b3` (15:26:30-03:00, "hygiene for r27 routed defects 1,4-7").
- `git show 071270b5:corpus/QUALITY.md` line 51 holds row 41: `Supersedes row 37's class list
  for `analyze` and `inspect`...` with why cell
  `corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md`;
  `corpus/lessons/round-27-verifier-spotcheck.md:112` and `:152` (routed defect 1); S083 |
  `supersedes 37 for `analyze` and `inspect``. Committed by `9db24c9e` (15:23:33-03:00).

Verdict on acceptance: holds. The committed pointer names the rows and `## Use` and carries
the suffix condition; row 41 supersedes 37 with that condition and cites the round-27 entry
plus spot-check :112 ("Knowledge sweep", naming rows :32-33, `## Use`, row 37) and :152.

Verbatim conflict for the judge: the assignment says the row should cite "the round-27
lesson"; the committed row 41 does not cite `corpus/lessons/round-27.md` — my draft below
adds it. Inserting my row would also duplicate row number 41 (rows 41-44 occupy :51-54), so
the drafts are reference text, not a second insertion. If the L1 wants the extra citation,
QUALITY's rule (never rewrite a criterion) suggests a new superseding row or a citation-cell
amendment, at the L1's choice.

## Draft (a) — appended pointer block

Insertion point: end of file, after line 135 (the last line at lane commit a2673116; at
observed main 071270b5 the committed equivalent occupies :137-146 — adopt only if the
committed block is judged insufficient).

```markdown
## Round-27 pointer (appended; filed text above unchanged)

The `analyze` and `inspect` table rows above (:32-33, verdict `content-keyed`) and the
`## Use` section describe these two ids only as content-keyed across directories. Round 27
narrowed that: at `rea-agents@6.5.0` the `analyze`/`inspect` id stays the same across two
paths only when both paths map to the same Ghidra snapshot suffix. The snapshot name is
`target-<sha256[0:12]><suffix>` and the suffix is the target path's extension when it matches
`^\.[A-Za-z0-9]{1,12}$`, else `.bin` (S083). A same-bytes copy in another directory or under
another file name keeps the id while the mapped suffix is equal; a copy with a different
extension gets a different id, and `subject.digest.sha256` is the content key to compare. See
`corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md` (evidence
`corpus/evidence/round-27/c1/table.tsv`) and QUALITY row 41, which supersedes row 37 for
`analyze` and `inspect`. The six other table rows are not affected: the five address verbs
stay content-keyed and `inspect-binary-layout` stays path-sensitive on the full path string.
```

## Draft (b) — QUALITY row 41 (one table line)

Insertion point: admission table, after row 40 (line 50 of the pre-round-28 file; at observed
main 071270b5 line 51 is already the committed row 41 — see conflict above).

```markdown
| 41 | Supersedes row 37's class list for `analyze` and `inspect`. At `rea-agents@6.5.0` an evidence-id identity claim for `analyze` or `inspect` is admitted only when it names the Ghidra snapshot suffix of every path compared and the suffixes are equal: the snapshot name is `target-<sha256[0:12]><suffix>` and the suffix is the target path's extension when it matches `^\.[A-Za-z0-9]{1,12}$`, else `.bin` (S083). A same-bytes copy in another directory or under another file name keeps the id while the mapped suffix is the same; a different extension changes it, and the claim must then compare `subject.digest.sha256` instead. Fails when a claim calls `analyze` or `inspect` content-keyed across paths without saying the mapped suffixes were equal. Row 37 stays in force for the six other verbs and for same-suffix copies. | `corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md` (table `corpus/evidence/round-27/c1/table.tsv`; mechanism S083); `corpus/lessons/round-27.md`; `corpus/lessons/round-27-verifier-spotcheck.md:112` and `:152` (routed defect 1) | 37 (for `analyze` and `inspect`) |
```

## Evidence

All read-only; lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, 2026-10-22, 18:31-18:40Z.

- `git log --oneline -4` — exit 0 — HEAD `071270b5`; `2832c5b3` ("r26 entry pointer"),
  `9db24c9e` ("QUALITY rows 41-43").
- `git show HEAD:.../r26...md | sed -n '137,146p'` and `'32,33p;108p'` — exit 0 — pointer
  block, `analyze` row :32, `inspect` row :33, `## Use` :108 (excerpts above).
- `git show HEAD:corpus/QUALITY.md | sed -n '51p'` — exit 0 — committed row 41 (above).
- `sed -n '112p;150,152p' corpus/lessons/round-27-verifier-spotcheck.md` — exit 0 — :112 names
  rows :32-33, `## Use`, row 37; :152 is defect 1's text.
- `git status --porcelain` — exit 0 — lane files mid-integration by the L1 during this run; no seat writes.

## Out of scope

No lane writes; no REA or network calls; the suffix rule was not re-verified (drafting route only). Routed defects 2-8 belong to other seats.

## Artifacts

- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/ScribeR26Pointer/drafts.md`
  sha256 `c19492e2d89f2f339da4b3631b8d6c97184ebb8d2d8974556fadfa75a7450b04`
- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/ScribeR26Pointer/evidence.txt`
  sha256 `c99971624c247e26381f3170a56922739ba3c633403eae445db68cd55b21b8d4`

No installs or upgrades.

Report: .ufo/waves/round-28/a2w/ScribeR26Pointer.md
