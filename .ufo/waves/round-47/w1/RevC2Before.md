# RevC2Before — R47-C2 before-state (scoped findings)

Full report: `.ufo/waves/round-47/w1/RevC2Before/report.md`; receipts:
`.ufo/waves/round-47/w1/RevC2Before/receipts/` (commands, exits, stdout sha256, UTC).
Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`; first freeze
`5017e1f7299c3a812e87e7950148f54313dd279e`; lane HEAD at close `09a9f912f4a639b91bce7dcd3711d8f391969d4f`.
Scratch removed. No installs. Lane tree untouched.

## Before-state replicates and each atom is independently confirmed

`record.py --rev 13a9e9e1` → exit 1, atoms 50, mismatches 4, stdout sha256 `53d81a3d…`
(2026-10-28T18:03:32Z), identical to `controls/ctl-c2-0-do-nothing.json` and identical under the
frozen and the landed counter bytes.

1. `seats/45`: dispatch `w1.spawn 40`, `w2.spawn 36`; the card's own cited
   `r45-w2-results.json` also says `seats: 36`. `32` is false against both.
2. `window/46`: placeholder → unverifiable, **and false**: `git log 0425224..13a9e9e --
   tools/round-46 plans/round-46-claims.md` shows `M attest.py`, `M gate.py` at `332f4884`.
3. `axes/coverage`: 138 knowledge files, 138 coverage-map tokens, intersection 138, dangling 0 → 138/138.
4. `axes/depth`: 23 craft blocks, 23 fully resolved → 23/23.

## Findings (severity order; every one has a fixture, a command and an exit code in the report)

- **F1 HIGH** the landed after-cell is false about its own receipt: card says `atoms 50` /
  `exempted 2`; `l1/scores/c2-at-A7.json` says **42 / 1**; the counter at `09a9f912` says **44 / 1**.
  No atom class reads the counter's output, so nothing fails.
- **F2 HIGH** one fenced line converts a detected false atom into exit 0 on the landed card:
  `Waves: 9 + 9 = 99 seats` → exit 1 (mismatch `seats/47`); the same sentence with a fenced
  `## note:` line after the `## Round 47` heading → exit 0, atoms 45 → 26. `sections()`/`collect()`
  are fence-blind; a fenced `## Round 99` heading also replaces a real section in the last-two window.
- **F3 HIGH** A1's premise ("unreachable by construction") is false: the **frozen** bytes reach
  exit 0 (`af666ce2…`, P4). And the clause A1 deleted was the only one that caught an unrelated-window
  exemption: same card → frozen exit 1 `window pair names no atom in scope`, landed exit 0.
- **F4 HIGH** the landed window correction is true but vacuous: `empty in 332f4884..58eb04b6` starts
  at the very commit that falsifies the atom (`332f4884` touched `tools/round-46/{attest,gate}.py`).
- **F5 HIGH** `record.py` has no `--freeze` arm and no self-pin (`SELF` unused); the claims' "a change
  makes **both** counters exit 2" is false for C2 (`exact.py` exits 2 at freeze `5017e1f`; `record.py`
  exits 0 at the same rev). Four post-freeze edits to `record.py` (A1, A3, A4, A5).
- **F6 MED-HIGH** `- corrects axes …` lines are unparsed (`CORR` excludes `axes`): the landed
  `24/24` changed to `99/99` still exits 0.
- **F7 MED** a zero-atom newest section is green (`## Round 47 — nothing measured` → exit 0).
- **F8 MED** the window class is the literal word `is empty`: rephrased to `was empty` + one true
  sentence → the false claim is invisible and the class check passes.
- **F9 MED** the `axes` atom is the first fraction in the row remainder (score cell included): a true
  `138/138` in the score cell flips coverage green while `133/133 knowledge files mapped` stays.
- **F10 MED** path atoms truncate at `{`: `.ufo/waves/round-46/{nope,nada}-results.json` is graded on
  the directory prefix and verifies.
- **F11 MED** the separability paragraph is false: `depth_pair` reads `SKILL.md`; block 24 moves the
  derived depth `23/23 → 24/24`, so C2's depth atom is coupled to C1's landing.
- **F12 MED** battery: 3 "forgeries" with `error: no corrections section` pass clause 6 for free at
  the base; `wrong_total` is a no-op without a seats correction; `non_empty` can be a no-op on a
  **true** correction (exit 1 with `mismatches []`).
- **F13 LOW** predicate names a `classes` field the receipt does not emit (`atoms_by_class`);
  `exempted` counts atoms, not corrections.
- **F14 LOW/MED** "every machine-checkable atom" overstates: the round-46 "declared freeze is
  `0425224`" is contradicted by `git log -1 -- plans/round-46-claims.md` → `31820472` and by
  `git show --stat 0425224` (only `tools/round-46/registry.py`); prose numbers and non-`.ufo` paths
  are ungraded.
- **F15 LOW** the frozen claims file carries amendment paragraphs for A1–A2 only; A3–A6 changed
  clauses/selftests with no ledger entry in the file.
