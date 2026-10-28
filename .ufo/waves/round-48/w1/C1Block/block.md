- **25. A verdict map binds meanings, and a denominator is a floor.** <!-- verdict-meaning-table v1 --> `tools/round-48/meanings.py` interpreter_sha256:74b8da35b4c47c7732bc2cb5a69a3c048e8e1f22ccf93b506cba9a71cd90816d mutations_sha256:25ce025f8b2be63a5122583191cbf7588db7dc2894c869fac2ab075a84f5c1ea names gold-meaning, swapped-meaning, duplicate-meaning, permuted-arm.

| trigger | v1 hole | v2 arm | exit |
|---|---|---|---|
| R46-CL7 | Digits 0/1/2 can be relabelled arbitrarily while still scoring met. | meaning | 1 |
| R47-CL10 | Rows naming the wrong arm can pass without proving the predicate. | floor | 1 |

Verdict meanings are bound to the digit they claim: `0=met, the target holds; 1=not met, a clause is false; 2=could-not-evaluate, the revision or a frozen file is unusable`. The success, not-met, and unevaluable classes are distinct; a digit is not evidence unless its meaning agrees.

Refs: `corpus/lessons/round-47.md:30-50`, `corpus/lessons/round-46.md:57-66`, `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`, `plans/round-48-claims.md:20`, `plans/round-48-claims.md:40`
