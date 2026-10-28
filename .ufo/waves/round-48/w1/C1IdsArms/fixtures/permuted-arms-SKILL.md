# SKILL

intro

## Queue-drain craft (test) 

- **1. Plain rule 1.** body text
- **2. Plain rule 2.** body text
- **3. Plain rule 3.** body text
- **4. Plain rule 4.** body text
- **5. Plain rule 5.** body text
- **6. Plain rule 6.** body text
- **7. Plain rule 7.** body text
- **8. Plain rule 8.** body text
- **9. Plain rule 9.** body text
- **10. Plain rule 10.** body text
- **11. Plain rule 11.** body text
- **12. Plain rule 12.** body text
- **13. Plain rule 13.** body text
- **14. Plain rule 14.** body text
- **15. Plain rule 15.** body text
- **16. Plain rule 16.** body text
- **17. Plain rule 17.** body text
- **18. Plain rule 18.** body text
- **19. Plain rule 19.** body text
- **20. Plain rule 20.** body text
- **21. Plain rule 21.** body text
- **22. Plain rule 22.** body text
- **23. Plain rule 23.** body text
- **24. Plain rule 24.** body text
- **25. A verdict map binds meanings, and a denominator is a floor.** <!-- verdict-meaning-table v1 --> `tools/round-48/meanings.py` interpreter_sha256:74b8da35b4c47c7732bc2cb5a69a3c048e8e1f22ccf93b506cba9a71cd90816d mutations_sha256:25ce025f8b2be63a5122583191cbf7588db7dc2894c869fac2ab075a84f5c1ea names gold-meaning, swapped-meaning, duplicate-meaning, permuted-arm.

| trigger | v1 hole | v2 arm | exit |
|---|---|---|---|
| R46-CL7 | `0=banana; 1=nope; 2=whatever` scores met | floor | 1 |
| R47-CL10 | four rows name the wrong arm and still pass | meaning | 1 |

  Refs: `corpus/lessons/round-47.md:30-50`, `corpus/lessons/round-46.md:57-66`, `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`, `plans/round-48-claims.md:20`, `plans/round-48-claims.md:40`

## Instrument registry

intro

<!-- instrument-registry v2 -->

| tool | gate or probe - purpose | verdict map (exit codes) | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|
| `tools/round-48/meanings.py` | gate — test | 0=met, the target holds; 1=not met, a clause is false; 2=could-not-evaluate, the revision or a frozen file is unusable | none | none | none | kaidoku |

<!-- /instrument-registry -->

## Next section

tail
