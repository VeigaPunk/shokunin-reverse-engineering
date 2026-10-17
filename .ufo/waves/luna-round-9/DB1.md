# DB1 — derivability, round-9 items 1-2

## CLAIM
Every drafted clause in the current item-1 text (RB1) and item-2 text (RB2) is evidenced at HEAD `a280e07`; two inline-citation completeness notes only, no unevidenced clause found.

## METHOD
Read at HEAD `a280e07` (read-only; only write is this file): `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:750-754,875-925`; `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:97-120`; `.ufo/waves/luna-round-5/X1.md:12,32-34`; `.ufo/waves/luna-round-5/CB4.md:9-11`; `.ufo/reports/luna-round-4/kaidoku.md:43-46`; `.ufo/reports/luna-round-5/kaidoku.md:50-56,63-67`; `SCORECARD.md:407-410,453-460`; RB1/RB2/GB6/QB1. Re-ran two checks: comma-needle repro `python3 -c "import re;n=lambda s:re.sub(r'[^a-z0-9]+',' ',s.lower());print('29,367,752' in n('x = 29,367,752'))"` → `False`; F18 predicate from `C04.md:36-49` over git objects at `0772d548`/`6a71cd5` → `6a71cd5 ns=1 stale=False repl=False`, `0772d548 ns=1 stale=True repl=False`. `git show 7125dd4^:corpus/README.md | sed -n 163p` → `Runtime-obs extended…`.

## FINDINGS
- **Item 1 (RB1), five clauses all reproduce:** `:751-752` names exactly two sites (`files[].path`, `chunks[].provider_id`); r12-01 `:99-104` = four sites, `:110-120` = round-5 freshness erratum, `:115-118` = “numeral attributed… /tmp receipts are gone”; text does not imply r12-01 supersedes r4-16 (A3's caution honored). Tail placement verified: r4-16 ends `:925` LF, last heading `:875`.
- **Item 2 (RB2), all clauses evidenced:** SIZES clause → X1:12/:32 + CB4:11 + my repro; “correct `29,367,752` / `84,258,816`” → CB4:9 hex↔dec; F18 clause → my re-execution (count=1, stale absent, failing conjunct = replacement pair `v42;Kimi`) matches “replacement-pair/refuted-encoding test”; opener clause → r5 `:63-64` + `7125dd4^:163` = “Runtime-obs extended” + X1:33-34 rejects it; bounds clause → B3:9-10 / SCORECARD:453-460.
- Both item-2 wording variants (RB2 refined; GB6's Z2 wording + Status line) are separately derivable — parent must pick exactly one (QB1).

## THREATS
- RB2's inline cites don't carry two quoted specifics: opener name “Runtime-obs extended” (trace: X1:33-34, `7125dd4^:163`) and F18 mechanism refinement (trace: VB2's and my re-execution; r4 report's `z=1 line-count` parenthetical itself does not reproduce — count=1). Clause content is evidenced; consider augmenting cites at landing.
- “7 values” remains not re-derivable (receipts gone); draft correctly attributes it.
- RB1 heading lacks lane id/leading blank (FB1/YB1) — mechanics, not derivability.
- Wave live; audited texts are the RB1 22:01 / RB2 22:01 snapshots.

## VERDICT
CLEAN — every drafted clause in the current item-1 and item-2 texts is evidenced at `a280e07`.
