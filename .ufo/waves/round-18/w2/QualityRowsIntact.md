PARTIAL

# QualityRowsIntact — QUALITY rows 1–20 byte-identity, row 21 shape and why-cell

Seat: KaidokuR18.QualityRowsIntact (w2 falsify, author-side advisory; not outside verification).
B = `9011581d84527ba34c675f9cf912e54d2e72d470`, REV = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. All anchors are `git show REV:path` unless marked B. Cwd for all commands: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

| sub-check | verdict | basis |
|---|---|---|
| Rows 1–20 byte-identical B→REV | **HOLDS** | [obs] C1–C4 |
| Row 21 has 4 cells | **HOLDS** | [obs] C5 |
| Row 21 why-cell resolvable | **PARTIAL** | [obs] locator 1 resolves and matches; locator 2 resolves to a row that has none of the facts attributed to it (F1) |

## Findings

### F1 (low, calibration). The why-cell credits three red-before facts to a row that does not contain them
- [obs] `corpus/QUALITY.md:31`, cell 3 cites: "`corpus/lessons/round-18.md`, Mistakes row R17-PINMAP (red-before: knowledge grep exit 1 at 9011581, 29/29 mid checks verdict-only, forged verdict-only check accepted by the 9011581 validator)".
- [obs] That row is `corpus/lessons/round-18.md:62`, Mistakes `#1`. Its "fix (shown able to fail)" column gives other facts: the REV `receipt-validate.py --require-mid-maps` gives `mid_map_missing` red 8/8 on r17 receipts and green 15/15 on r18 receipts, and a forged `entries` selftest gives `mid_entries_mismatch`. None of the three parenthetical facts appear in it (C12: grep exit 1).
- [obs] Elsewhere in `round-18.md`, only "29/29" appears (`:51`, the named-corrections section, not Mistakes). `:23` says "red-before below", but nothing below states RB-1 or RB-3.
- [obs] The three facts are **true**; I reproduced each one independently:
  - RB-1: the knowledge-entry grep exits 1 at B and 0 at REV (C13).
  - RB-2: 8 labels with 4+2+3+2+4+4+2+8 = 29 `pin_checks`, one uniform key set `{changed, entries, equal, missing, taken_at_utc}`, and 0 checks carry a map (C14). `runs/` is unchanged B→REV (C15).
  - RB-3: run in memory, the B validator returns `valid True, findings []` for both the original pro-aether receipt and a forged one (`entries` 7 vs 146 pinned, a 1970 instant, an extra bare `{"equal":true}`) (C16). Cause: B `.ufo/waves/round-17/tools/receipt-validate.py:187-191` tests only `chk.get("equal") is True`.
- [obs] Where the facts are actually retained at REV:
  - all three: `.ufo/waves/round-18/w1/CriticDiscernment.md:55-57` (table RB-1..RB-3), `:64-69`, `:75-79` (commands with exits);
  - two of them: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:204` ("each of the 29 second-pass") and `:205` ("a forged verdict-only entry with a wrong `entries` count was accepted").
- [obs] w1 asked for exactly this row content. `CriticDiscernment.md:58` (RB-4) says the Mistakes row R17-PINMAP "lists RB-1 to RB-3 with exits", and `:99-100` says "able-to-fail: RB-1 to RB-3 with exits. The why-cell of #21 must cite this row." The why-cell was written to that spec. The row was not.
- [inference] Smallest safe correction: put RB-1..RB-3 with their exits into `round-18.md:62`, or point that row at `w1 CriticDiscernment.md` §4–5. `round-18.md` is this round's own file. Do **not** rewrite QUALITY row 21: `corpus/QUALITY.md:4-5` makes rows append-only.
- [inference] The C1 counter cannot catch this. `.ufo/waves/round-18/tools/routed-defects.py:216-229` passes `quality-admission-row` when cell 3 contains the two substrings `round-17-verifier-spotcheck.md` and `R17-PINMAP`. That is a token test; it does not check that locators resolve.

## Observations behind the HOLDS rows
- [obs] The diff is one hunk, `@@ -28,6 +28,7 @@`, with one `+` line (`| 21 | …`) and zero `-` lines; blobs `e04b742..8eeab5c` (C1).
- [obs] `diff` gives exactly `30a31` (C3). REV lines 1–30 equal B lines 1–30, and REV lines 32–44 equal B lines 31–43, both by `cmp` exit 0. Rows 1–20 (`:11-30`) have the same sha256 `5cd40d5a…66b7f` at B and REV (C3).
- [obs] Data rows go from 20 to 21, numbered 1..N without gaps. CR count is 0 and both files end in LF (C5). Row 21 sits at `:31`, followed by a blank `:32` and `## Signals of weak material` at `:33`.
- [obs] Row 21 has exactly 5 `|`, 0 backslashes and 20 backticks (an even number, so code spans are balanced). That gives 4 cells under GFM splitting, matching the header `| # | criterion | why (lesson) | supersedes |` at `:9`. Cell 4 is `sharpens 19`, the same form rows 18–20 use (C6).
- [obs] Locator 1, `corpus/lessons/round-17-verifier-spotcheck.md`, resolves. Its blob `fa3058d6…` is identical at B and REV (C7, C8), so the anchors cannot have drifted.
  - `:108` has `{changed:[],entries:146,equal:true,missing:[],taken_at_utc}` ×3 and "partial disagree".
  - `:137` has "R17-PINMAP", `{taken_at_utc, equal, entries:int, changed, missing}` and "not per-path maps".
  - The quoted r17 phrase is at knowledge `:30`: "each pin map is retained with its UTC instant". That file is append-only B→REV (8 lines added, 0 removed, one hunk after `:198`), so `:30` is the same at REV (C18).

## Residual risk / gaps (not findings)
- [obs, pre-existing, out of scope] `corpus/QUALITY.md:23` (row 13) has an unescaped `|` inside the code span `` `grep -o … | wc -l` ``, giving 6 pipes and 5 cells under GFM. The line is identical at B, so this is not a round-18 regression. Repro: `git show REV:corpus/QUALITY.md | sed -n '23p'`, then count `|`.
- I did not exercise the REV validator against the forged receipt (the green side). Row 21 does not claim it; that check belongs to the receipt-validate reviewers.
- Post-REV state [obs]: `refs/heads/main` = REV; no commit after REV touches QUALITY.md; the worktree's QUALITY.md and round-18.md equal REV (C19).

## Commands (exit codes observed)
```text
C1  git diff 9011581d84527ba34c675f9cf912e54d2e72d470 b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- corpus/QUALITY.md        exit 0 (1 insertion, 0 deletions)
C2  git rev-parse <B> <REV>                                                         exit 0 ; git --no-optional-locks merge-base --is-ancestor <B> <REV>   exit 0
C3  diff <(git show B:corpus/QUALITY.md) <(git show REV:corpus/QUALITY.md)              exit 1, output "30a31 > | 21 | …"
    cmp <(git show B:corpus/QUALITY.md|sed -n '1,30p') <(git show REV:corpus/QUALITY.md|sed -n '1,30p')      exit 0
    cmp <(git show B:corpus/QUALITY.md|sed -n '31,$p') <(git show REV:corpus/QUALITY.md|sed -n '32,$p')      exit 0
    git show {B,REV}:corpus/QUALITY.md | sed -n '11,30p' | sha256sum  -> 5cd40d5a38d9ed04b70912f167a6357d3450d38adb16b948fdb0254cecd66b7f (both)
C4  python3 -I -B -c (difflib.SequenceMatcher over git show B/REV lines)                exit 0: 43 vs 44 lines; opcodes [('insert',30,30,30,31)]; rebuilt==baseline True
C5  python3 -I -B -c (admission rows, numbering, CR, EOF)                                exit 0: B 11301 B, 20 rows contiguous; REV 12318 B, 21 rows contiguous; CR 0; EOF LF
C6  python3 -I -B -c (row 21 split + counts)                                            exit 0: 4 cells; pipes 5, backslashes 0, backticks 20
C7  git ls-tree REV -- corpus/lessons/round-17-verifier-spotcheck.md corpus/lessons/round-18.md corpus/QUALITY.md   exit 0 (fa3058d6…, fde4d083…, 8eeab5c5…); same at B for spotcheck: fa3058d6…
C8  git diff --stat B REV -- corpus/lessons/round-17-verifier-spotcheck.md               exit 0, empty
C9  git show REV:corpus/lessons/round-17-verifier-spotcheck.md | cat -n | sed -n '100,150p'   exit 0
C10 git show B:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | cat -n | sed -n '26,34p'   exit 0 (:30 "each pin map is retained with its UTC instant")
C11 git show REV:corpus/lessons/round-18.md | cat -n                                      exit 0 (:23, :51, :58, :62)
C12 git show REV:corpus/lessons/round-18.md | sed -n '62p' | grep -o -E '9011581|29/29|29 |grep|accept[a-z]*|verdict-only'   grep exit 1
    git show REV:corpus/lessons/round-18.md | grep -n -o -E '29/29|accept[a-z]*|verdict-only|knowledge grep|red-before'      exit 0: 9,23 red-before; 51 29/29
C13 git show B:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | grep -n 'R17-PINMAP\|comparator verdict'     grep exit 1
    git show REV:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | grep -n 'R17-PINMAP\|comparator verdict'   grep exit 0 (:204, :205)
C14 python3 -I -B -c (json over git show B:.ufo/waves/round-17/runs/<8 labels>/receipt.json .steps.analyze.pin_checks)   exit 0: total 29, 1 keyset, checks_with_map 0
C15 git diff --stat B REV -- .ufo/waves/round-17/runs/ .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-17/tools/pins.py   exit 0: only receipt-validate.py (306+/5-)
C16 python3 -I -B -c (exec B pins.py + B receipt-validate.py from git objects into modules; validate_receipt(pro-aether), then forged copy)   exit 0
    -> ORIG valid True findings [] checks 344 ; FORGED valid True findings [] checks 345
C17 git show REV:.ufo/waves/round-18/tools/routed-defects.py | sed -n '199,236p'         exit 0
C18 git diff --numstat B REV -- corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md   exit 0 "8 0"; hunk "@@ -198,0 +199,8 @@"; REV :30 = "each pin map is retained with its UTC instant: …"
C19 git --no-optional-locks rev-parse refs/heads/main -> b2aad08… exit 0; git --no-optional-locks log --oneline REV..refs/heads/main -- corpus/QUALITY.md -> empty exit 0;
    git --no-optional-locks diff --stat REV -- corpus/QUALITY.md corpus/lessons/round-18.md -> empty exit 0
```

Safety: the only write was this report. C16 ran entirely in memory: no temp files, and no carrier or REA execution (it reads log and carrier bytes only to hash them). No jj, no git writes. Tools installed or updated: none.
