# PROVINCE.md repair — Frontier bullet "Recorded crashes >32 MiB": the cap-raising knob EXISTS

Authored by SEAT RV-5 (chain c2, reviewer), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — seats never write `PROVINCE.md`; the parent applies.

## Stale item (census-checked, falsified first-hand)

`PROVINCE.md` Frontier bullet `Recorded crashes >32 MiB`, current bytes:

> mechanism held (Core); all 3 organic cores exceed the cap (waybar 434MB). Needs
> a cap-raising knob or partial-core intake — neither exists.

Both halves are falsified on this host, 2026-10-19:

1. **"all 3 organic cores exceed the cap"** — falsified by EX-13 first-hand (an
   organic 17.6 MB `chrome_crashpad_handler` core inspects, exit 0,
   `ev_1c1cd827…`); re-derived by this seat: the same core dumps to
   17,608,704 B and inspects to `ev_913e9789eb657cb6bba29431a9e74e498bd08e02dbc9b05197a6f58e09fa2a81`,
   `format elf-core`, 53 segments.
2. **"Needs a cap-raising knob … neither exists"** — **falsified by this seat**
   (the chain's census read this row `current`). The knob exists:
   `REA_PWNTOOLS_MAX_INPUT_BYTES`. Measured on a real 36,360,192-byte core
   (`coredumpctl dump 1214442`, git SIGBUS, 2026-10-19 09:05 −03):

   | leg | command | result |
   |---|---|---|
   | A | 6.7.0, no knob | **refused** `invalid_request`/`out_of_range` "exceeds 33554432 bytes" |
   | B | 6.7.0, `REA_PWNTOOLS_MAX_INPUT_BYTES=40000000` | **exit 0**, `ev_367c6cb419b75675348d7fb16f8673f743133e15d547fadf86a78f5eae56057e`, `elf-core`, 49 segments, 1 thread |
   | C | 6.5.0, no knob | refused (same class) |
   | D | 6.5.0, knob set | **exit 0**, `ev_0ed48c73e94bf032f9214b6b5183f5df7438b6d8d77585726f66c4059bebfe9d`, 49 segments |
   | E | 6.4.0, knob set | refused — the key is **absent** in 6.4.0's dist (0 files carry it; 6.5.0 and 6.7.0 carry it in 4 files each) |

   Transcript: `evidence/f2b-knob-measurement.txt`.

**What survives, correctly scoped.** The r2 sentence the census cited is about
the **verb schema**, and it still holds: `inspect-recorded-crash --schema`
exposes only `path` + `debuggerContext` — no size/limit option
(`evidence/f2b-knob-measurement.txt` §G). So the true statement is "the verb
schema exposes no cap flag; the cap is raised by the
`REA_PWNTOOLS_MAX_INPUT_BYTES` env key on 6.5.0/6.7.0" — not "neither exists".

**Also superseded:** EX-13's `province-frontier-recorded-crashes-organic.patch.md`
repairs the first half correctly but **carries the same false existential clause
forward** verbatim ("No cap-raising knob or partial-core intake."). Landing that
patch alone leaves the falsified claim in a scoped file. This patch supersedes it
on both halves.

## Change (same-line replacement, line count held at 3)

`PROVINCE.md`

```diff
# file: PROVINCE.md
-- **Recorded crashes >32 MiB** — mechanism held (Core); all 3 organic cores
-  exceed the cap (waybar 434MB). Needs a cap-raising knob or partial-core
-  intake — neither exists. Retention decays oldest-first.
+- **Recorded crashes >32 MiB** — mechanism held (Core); the oversize class
+  refuses by default (`out_of_range`), and an organic 17.6MB core inspects
+  (arc3-r4). `REA_PWNTOOLS_MAX_INPUT_BYTES` raises the cap. Retention decays oldest-first.
```

## Census conformance

- **Line-neutral**: 3 search lines → 3 replacement lines; `PROVINCE.md` stays at
  162 lines, so the DATED marker at line 119 (`verified 2026-10-13`) does not
  shift (EX-14's arm 8 measured the line-count-change failure mode:
  `SCOPE-ERRORS ["PROVINCE.md:119 marker … absent"]`, FAIL exit 1).
- **Needle-free**: the replacement carries no `rea-agents@x.y.z`, no bare
  `6.x.y`, and no `~`/`/`-absolute `path:line`. `REA_PWNTOOLS_MAX_INPUT_BYTES`
  does not trip the instrument's `REA_GATE` (`\brea\b` fails inside
  `REA_PWNTOOLS…` because `_` is a word character) — **measured**, not reasoned:
  see `evidence/patch-apply-and-census.txt`, where the census on the patched tree
  reads `undeclared=0`.
- Search text is verbatim and unique in `PROVINCE.md` (apply transcript:
  `evidence/patch-apply-and-census.txt`).
