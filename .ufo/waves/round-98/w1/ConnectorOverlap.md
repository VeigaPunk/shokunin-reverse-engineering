# ConnectorOverlap — round 98 w1 — overlap and supersession scan (read-only)

Seat ConnectorOverlap-34, 2026-11-05. Scope: (1) packed-PE frontier clauses in
`corpus/README.md` vs R98-C1, (2) sibling-lane UPX-PE knowledge, (3) M97-j-class
allow-lists in `tools/`. Read-only throughout; no tools installed; scratch
`/fast/scratch/hyaku/kaidoku-r98/ConnectorOverlap` created and deleted. Lane state:
HEAD `9cb930014a57c9b29d830739e0c4229f6e7e7016`, tracked tree clean (only untracked
`.ufo/waves/round-98/` wave files, `git status --porcelain`). Line numbers below are
the working tree at that HEAD; F/L states checked by read-only `git show`.

## 1. Frontier lines naming packed PE inputs (corpus/README.md)

| line | note | clause | vs R98-C1 |
|---|---|---|---|
| 341 | r68 | "packed PE/Mach-O" | open — not named by the r98 note |
| 343 | r87 | "packed PE/Mach-O" | open — not named by the r98 note |
| 374 | r70 | "packed PE/Mach-O" | open — not named by the r98 note |
| 376 | r72 | "packed PE/Mach-O" | open — not named by the r98 note |
| 379 | r73 | "packed PE/Mach-O" | open — not named by the r98 note |
| 381 | r76 | "packed PE/Mach-O" | PE half superseded (note names r76) |
| 383 | r77 | "packed PE/Mach-O" | PE half superseded (note names r77) |
| 395 | r92 | "PE and Mach-O packed inputs" | primary surface (plan F:393): PE half superseded, Mach-O half open |
| 397 | r98 | the superseding note itself | — |

- R98-C1 supersedes exactly the "packed PE" half of the r92 clause (395) and the
  "packed PE/Mach-O" halves of r76/77 (381/383), "for this class only" (note 397):
  six pinned carriers, UPX 5.2.0 `--best`, win32/pe + win64/pep, magic/names/both.
- Must stay open per note 397's Still-Frontier list: Mach-O, ARM64 PE, PE DLLs and
  .NET, other UPX modes/versions, PackHeader offsets other than 992, `UPX2`-named
  third sections, PackHeader-field/stub-code tampers, whether a repaired PE runs —
  plus everything outside the class under the five un-named notes (341/343/374/376/379).
- Map/knowledge rows 134 and 279 name UPX-packed PE (records, not frontier clauses);
  rows 21/22/176/177/191 hold PE capability ground (Ghidra e2e, ARM64 wall) that
  R98-C1 does not touch.

## 2. Sibling-lane scan (`/home/vgpnk/Projects/shokunin/*-shokunin/corpus`)

- Case-sensitive `UPX`: 31 files — all kaidoku except
  `chousa-shokunin/corpus/captures/e84bfe97808591d23fe3266f.raw:35`, the substring
  "JDUPXurk" inside base64 JPEG thumbnail data — false positive, not knowledge.
- Precision pattern `UPX-packed|anti-UPX|packed PE|upx -d|upx -t|upx --best`:
  29 files, all kaidoku except
  `revenger-shokunin/corpus/live/runs/round-56/header-review.md:4` — an independent
  PE32+ header/resource-directory review of synthetic fixtures (struct-parsed bytes,
  no packer, no anti-unpack content). No overlap with R98-C1, no contradiction.
- Verdict: **zero sibling lanes hold UPX-PE or anti-UPX-PE knowledge** — no overlap,
  no contradiction (consistent with round-90 ConnectorOverlap and round-87
  ConnectorR87 sibling scans, both empty).

## 3. Allow-list census (the M97-j class: list vs emitting verdict)

`grep 'COUNT_KEYS'` hits exactly three files; rounds 91/92/93 batteries have none
(`grep 'KEYS|counts-extra'` → no matches; they compare printed labels to `--expect`).

- `tools/round-96/stop-boundary-repair-battery-v6.py:57-58` — **nine keys** — same
  defect class as v7 (gates v3.score's fourteen-key verdicts); retired instrument,
  no live producer path since v7 (round 97). Do not reuse as a template.
- `tools/round-97/stop-boundary-repair-battery-v7.py:55-56` — **nine keys** — the
  M97-j defect, retained intentionally as the failing C2 control (must exit 1).
- `tools/round-98/stop-boundary-repair-battery-v8.py:62-64` — **fourteen keys**.

Producer ground truth (read-only; batteries not run — they pack real carriers):
- `tools/round-93/stop-boundary-repair-battery-v3.py:288-303`, `counts = {...}` emits
  exactly scored, repaired, wrong, unsafe, refused, silent, intact, far, far_refused,
  fresh_scored, fresh_repaired, fresh_roundtrip, fresh_far, fresh_far_refused (14).
- The committed verdict receipt `.ufo/waves/round-97/l1/public/v6-public.json`
  (`verdict_counter`: v3) carries exactly those 14 count keys.
- Equality: **v8 == producer emission** (14 = 14); v7/v6 (9) do not — the five dropped
  keys answer `counts-extra-key` on every honest run, which is R98-C2's routed defect.
- Cosmetic coupling: the nine-key tuple is duplicated at
  `allowlist-check.py:37-38` (`NINE`, stub9 leg) and `v8:65-66` (`NINE_LABEL_KEYS`);
  the L1 receipt `.ufo/waves/round-98/l1/scores/c2-at-7234689….json` shows the pair
  behaving: `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1`, met true, exit 0.

Remaining `KEYS = (` hits (43 files) — none in the M97-j class: multi-spelling input
selectors (PATH_KEYS/COMMAND_KEYS/ENTRY_LIST_KEYS/ARGV_KEYS/FEATURE_KEYS/PROJECTION_KEYS…,
deliberately widen acceptance), child-env contracts (CHILD_ENV_KEYS/ENV_KEYS =
HOME/LANG/PATH/TMPDIR, equal to what the producers set), pin categories (PIN_KEYS),
receipt-id pins (round-49 LOG_KEYS), and round-66 `RECIPE_A_KEYS:73-75`, which its own
docstring derives from "the committed SCORECARD block (lines 96-122). Same inputs,
same arithmetic, same keys" — record-derived, not label-derived. Clear.

## 4. Proposed move (record-level; owner = round record step)

Finding: the r98 note (397) names 3 of the 8 clause-bearing lines (395, 381, 383) and
leaves 5 un-named — 341 (r68), 343 (r87), 374 (r70), 376 (r72), 379 (r73). The r87
precedent (343) enumerated every note its class superseded with exact line refs
(324, 355, 357, 360, 362, 364); the r98 note does not, and no text says why.
Un-named clauses risk a future reader treating r68/70/72/73/87 as live blockers on
the next packed-PE class.

Move: when the round-98 record is finalized, extend the supersession sentence to
"…and the 'packed PE' half of 'packed PE/Mach-O' in the round-68/70/72/73/87 notes",
keeping "for this class only"; or add one sentence that dated notes are historical
snapshots, not live clauses. Improves record consistency; harms none — the claim
boundary is unchanged (note 397's Still-Frontier list already carries everything
outside the class). Rejected alternative: superseding whole clauses — that would
wrongly core packed PE generally while ARM64 PE, PE DLLs/.NET stay frontier.

Line drift note: the plan cites `corpus/README.md:393` for the r92 clause, correct at
F and at L (`git show` of both pins the clause at 393); in the working tree it sits at
395 — shifted +2 by the r98 coverage row (134) and knowledge row (279), committed after
L. Any future line-pinned pointer to that clause should cite 395 at HEAD `9cb9300…`.

## 5. Verification log

- `git -C <lane> rev-parse HEAD` → `9cb930014a57c9b29d830739e0c4229f6e7e7016`; status
  → untracked wave files only. `git show 69c581c…:corpus/README.md | grep -n 'PE and
  Mach-O packed inputs'` → 393; same at `72346895…` → 393; `grep -n 'packed PE/Mach-O'`
  at F → lines 339/341/372/374/377/379/381 (F offsets, −2 vs tree).
- `grep -c`-equivalent counts: `UPX` case-true across `*-shokunin/corpus` = 31 files;
  precision pattern = 29 files; `COUNT_KEYS` in `tools/` = 3 files; `KEYS = (` = 43 files.
- Files read verbatim: `README.md:395:raw`, `README.md:397:raw`,
  `tools/round-98/allowlist-check.py`, `v8:62-66`, `v7:55-56`, `v6:57-58`,
  `v3.py:280-310`, `v6-public.json` (14 keys), `round-66/coverage-selfcheck.py:55-115`,
  `revenger-shokunin/.../header-review.md`.
- Not run: v7/v8 batteries and the C1 battery (they pack real PE/ELF carriers — not
  cheap; the read-only question needed only the emission code and committed receipts).
