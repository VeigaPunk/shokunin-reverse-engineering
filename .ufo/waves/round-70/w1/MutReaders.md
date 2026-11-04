# MutReaders

Detailed battery: [MutReaders/battery.md](MutReaders/battery.md). Actual detector evidence: [MutReaders/evidence.json](MutReaders/evidence.json). Nine receipt fixtures are preserved alongside them.

Seven independent frozen-reader mutations: registry pin, ratio recomputation, packed ceiling comparison, revision binding, carrier-id multiset binding, DECLARED_ORIG binding, producer hash binding. All seven are DEAD: six accept their dedicated false input; the ceiling inversion removes its dedicated rejection clause while retaining other rejections (the assigned clause-shrink kill criterion).

135 bounded CLI executions: 9 pristine, 63 mutated, 63 restored. Pristine rejects all seven dedicated negative shapes and the unmodified round-69 receipt; the explicitly synthetic structural control passes. Every restored output matches pristine byte-for-byte. Before/restored SHA-256: `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`. Individual mutant hashes/diffs are recorded in the battery and evidence. No syntax-error kills or unevaluable runs; no survivors to route.

Scratch removed after receipts were preserved. Frozen files untouched. No installs, git mutations, host service changes, or PATH writes. Scope is reader mutation sensitivity, not real-carrier execution or an overall judgment on the three claims. Recommend registering these seven reader-specific false-input cases at the next freeze, beyond the existing five arm mutants.

VERDICT: met — 7/7 new reader mutants killed; exact-byte restoration and identical restored detector outputs confirmed; scratch removed.
