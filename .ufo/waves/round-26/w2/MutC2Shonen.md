# Wave 2 seat MutC2Shonen — K6 mutants on the repaired SHONEN line

Target: R26-C2 item K6 of the frozen claims at `.ufo/waves/round-26/claims.json`
(read 2026-10-22; tracked file, sha256 `1137c312d9d1a4aa83ec4f7b167bcd03423de955d89ede1e53f3c6bf6bfbcb5f`,
unchanged since the freeze commit `c27f445e`; the freeze rules bind).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read-only. Base revision
judged: `fe3eb4edf410244eff46151a148c8f754be1ce80` (lane HEAD at the time of the run).
All mutation happened in the sandbox clone
`/fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC2Shonen/clone` (clone of the lane).

## Subject under test

`SHONEN.md` line 11 is the box line `- [~] No cross-domain bleed (PROVINCE.md still accurate)`;
line 12 is the asserted-boundary line that K6 reads. `PROVINCE.md` has 303 lines at the base
revision; its sections are `## Core` (38), `## Frontier` (73), `## Adjacent` (95).

## Detector

`python3 -I -B tools/round-26/c2-calibration.py --root . --rev <REV>` run inside the clone,
one call at a time, against Git objects at `<REV>` only. Verdict read from the JSON:
`mismatches`, `exit`, and the `K6` item result and note. No REA call was needed:
K6 is a text-and-line-count rule over committed bytes.
Baseline on pristine bytes at `fe3eb4ed`: `exit 0`, `mismatches 0`, K6 `pass`, note
"the asserted boundary line is clean and inside PROVINCE.md".
`SHONEN.md` sha256 pristine = `c4ce10ff4d24ddd9e10d54781b65773652d1af8c855b1f18c239a380bbb6a964`.
UTC 2026-10-22T12:58:39Z (baseline), 2026-10-22T12:59:03Z (mutant sweep).

## Mutant table

| id | mutation on the SHONEN line | mutant rev | exit | mismatches | K6 | detector note | verdict |
|---|---|---|---|---|---|---|---|
| M1 | insert the word `contested` on the line after the box line | `072dda72` | 1 | 1 | mismatch | "the line after the box line contains the word 'contested'" | killed |
| M2 | replace the boundary pointer with `PROVINCE.md:400` | `bc7d9ec3` | 1 | 1 | mismatch | "a PROVINCE.md pointer is outside PROVINCE.md's line count" | killed |
| M3 | change the box mark from `- [~]` to `- [x]` | `9997dd54` | 0 | 0 | pass | "the asserted boundary line is clean and inside PROVINCE.md" | survived (false accept) |
| M4 | replace the boundary pointer with one into the PROVINCE `## Core` tables (`PROVINCE.md:38-72`) | `119ed614` | 0 | 0 | pass | "the asserted boundary line is clean and inside PROVINCE.md" | survived (false accept) |
| M5 | state a false pin `rea-agents@6.4.0` instead of `6.5.0` for the round carrier runs | `cba8c5bb` | 0 | 0 | pass | "the asserted boundary line is clean and inside PROVINCE.md" | survived (false accept) |

Mutant file sha256 (sha256 of `SHONEN.md` at the mutant commit): M1 `f5c564364ddfc752…`,
M2 `1f65509776a6ea3b…`, M3 `5ffd8d0149a1dd55…`, M4 `ea19e8c00e0bfecf…`, M5 `3e9ea55018683610…`.
Pristine sha256 for all five: `c4ce10ff4d24ddd9…`.

## False accepts the frozen K6 rule allows (the coverage finding)

K6 as frozen checks exactly three things: the word `contested` is absent from the line
after the box line, at least one `PROVINCE.md:A-B` or `PROVINCE.md:A` pointer is present on
that line, and every such pointer is inside PROVINCE.md's line count. Three of the five
mutants pass the detector while making the SHONEN line materially untrue:

1. M3 — the box mark. The rule accepts both `- [~]` and `- [x]` as the box line, so a
   mutant that claims the cross-domain bleed check is complete (`[x]`) is accepted. The
   repaired line's `- [~]` means "boundary asserted, not verified"; a flipped `[x]` claims
   more than the rule can distinguish, and K6 cannot see the difference.
2. M4 — the pointer target. Only the pointer's numeric range is checked against PROVINCE.md's
   line count, never what is at those lines. Pointing the boundary at `## Core` tables
   (`PROVINCE.md:38-72`) instead of the `## Adjacent` refusal list (`PROVINCE.md:95-116`)
   keeps every pointer in range and passes.
3. M5 — the stated pins. The line asserts `rea-agents@6.7.0` and `rea-agents@6.5.0` pins;
   K6 reads no pin value, so a false pin `rea-agents@6.4.0` passes unchanged.

What K6 does catch: the word `contested` (M1) and a pointer beyond PROVINCE.md's 303 lines
(M2). Both were killed with exit 1 and one mismatch.

Inferred from the instrument source only, not run (labelled inference): the `contested`
test is a case-sensitive substring test applied to the single line immediately after the
box line, so a differently cased spelling, or the word placed on the next line, would
evade it; and the pointer test only recognises the `PROVINCE.md:<digits>` colon form.

## Restoration evidence

After every mutant the clone was hard-reset to `fe3eb4ed`; `SHONEN.md` sha256 was
`c4ce10ff4d24ddd9…` again each time and `git status --porcelain` in the clone was empty
(`clone_status_after_reset` = "" for all five rows in `out/summary.json`).
A final detector run on the restored bytes gave `exit 0`, `mismatches 0`, K6 `pass`, and its
stdout file `out/restored.json` is byte-identical to `out/baseline.json`
(both sha256 `c7781731360a1efee1c25b6fff9b400fe4049752eb2e2e8df95f65aa5bab6f0c`). The lane was never written: lane `SHONEN.md` sha256 is still
`c4ce10ff4d24ddd9e10d54781b65773652d1af8c855b1f18c239a380bbb6a964`, lane `PROVINCE.md`
`73df22ffba7735cef880e3c3797f25c4a967dc617cf4132fd3e810cd17b79408`, lane HEAD still
`fe3eb4edf410244eff46151a148c8f754be1ce80`, and lane `git status --porcelain` over
SHONEN.md, PROVINCE.md and SCORECARD.md is empty.

## Artifacts (all under the seat scratch directory)

- `mutate.py` — driver; sha256 `96807f7f5d8762b71c475d5b658e01b9aafd2be2cb0e543d7913aa424fd82a85`
- `out/summary.json` — sha256 `32ccc50866a5ddc3886d08aaf596df21c9a08bec0c26494a005caf97cd88c37a`
- `out/baseline.json` and `out/restored.json` — sha256 `c7781731360a1efee1c25b6fff9b400fe4049752eb2e2e8df95f65aa5bab6f0c` (both)
- `out/M1_contested_word.json` — sha256 `4d0ee29b03e1dc248b513c020c1ab216759bf5caacf99e3baec962b9f1ac3cbb`
- `out/M2_pointer_province_400.json` — sha256 `8dbd804f36f7fb1168ef23ff6b009ed65b127856e537453b8c35604d7e5e3e8e`
- `out/M3_box_mark_checked.json` — sha256 `eade434ef72341659e4e47e85fc2ed5bc2d365cbfaab6e288f98955ae3355653`
- `out/M4_pointer_into_province_core.json` — sha256 `0243017841f598f7856e63cb05b26ea57dfebaf9a7af1357ca0b92bff607cd86`
- `out/M5_false_pin_rea_6_4_0.json` — sha256 `b48fea6ffe078a31807a4362a40495afd18295292996f57ec3b38d3b1416ac5a`
- `out_run.log` — sha256 `fbca516dcb75daa4a92d7950f8992bf8f98344564902a2109c85a2686e4dab25`; `out/*.err` all empty (sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`)

## Conclusion

Verdict: partially holds. The K6 rule kills the two mutations it was written for
(contested wording, out-of-range pointer) and falsely accepts the box-mark flip, the
pointer-retarget into the PROVINCE `## Core` tables, and the false `rea-agents@6.4.0`
pin. Those three survivors are a coverage finding about the frozen K6 rule; they are not
grounds to change the rule, and no lane file was changed here.
