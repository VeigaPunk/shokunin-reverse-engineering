# CriticClaim — attack on R64-C1 (kaidoku round-64, w1, attempt 1)

Read-only critic seat. Nothing in the frozen instrument, claims file or inputs was edited or
re-predicted. All 9 frozen pins re-verified on disk this session; freeze chain verified.

## Verified before attacking

- Instrument sha256 `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb` — matches F1
  (`sha256sum tools/round-64/jsc-route-matrix.py`).
- Inputs: probe `a86f6ea0…d710`, typora `6a0cb7b3…2dfe9` (sha256sum, both match PINS); typora size 388080 (F5);
  mkcache.js `f052eafb…ff11` (F4).
- Binaries: D1 `bc70d3c0…`, D2 `4060ff2e…`, D3 `c240ffae…`, D1-snapshot `b5c418dc…`, D1-icudtl `c5da2fc3…`,
  view8.py `b3123e4a…` — all match PINS.
- Freeze chain: instrument committed at `3fd8468c1a8c5b90a440b3aabe99cb6f139c892b` (2026-11-03 19:40:51),
  claims.json landed at `a35e514105234515e266440aa33a578536b0007b` (19:41:12) — matches the declaration pointer.
- Live selftest of the frozen instrument: `SELFTEST CLEAN cases=22 failures=0` (F2 holds now, not only at freeze).
- Do-nothing control receipt `.ufo/waves/round-64/l1/c1-before-donothing.json`: `"exit": 1`, every cell
  `"observed": "not-run"` — 0/18, matches the declared control.

## Findings

| id | attack | class | severity | evidence (path · command · output) |
|---|---|---|---|---|
| CC-1 | Check stage is unpinned and one-directional: `PINS` (tool lines 48–57) has 8 keys and no `node`; `classify_check` maps ANY nonzero rc to `node-fail` (selftest `check-fail PASS`); both dump-ok cells predict `node-fail`, so an always-failing `--node /bin/false` reaches 18/18 exit 0; the receipt dict records no check rc/stderr (only `dump_rc`, `dump_bytes`, `view8_out_bytes`, `label`), so substitution leaves no trace. Empirics: `node --check probe-view8.js` → rc 1 with `SyntaxError: Unexpected token ':'` (line 3); `/bin/false --check probe-view8.js` → rc 1 — identical label. | evidence-soundness gap (evasion route, not falsehood — declared counting command hardcodes `--node node`) | non-blocking | tools/round-64/jsc-route-matrix.py:48-57,133-135,317-319; `node --check …/prefreeze-probe/probe-view8.js; /bin/false --check …` → `REAL_NODE_EXIT=1`, `FALSE_NODE_EXIT=1`; fake-node matrix receipt: `w1/CriticClaim/receipt-false-node.json` (exit 0, 18/18) |
| CC-2 | Two of the four claimed pre-freeze observations are not recountable from committed receipts: probe×D3 "exit 139" — `dump-probe-x7.txt` is 0 bytes with NO `.err` companion and no recorded rc anywhere in `l1/` (`grep -rn '139' l1/` hits only *predicted* labels in c1-before-donothing.json); and probe×D1's "node --check fails" — `probe-view8.js` (213 B) is receipted but no check rc/log is. Narrative-only observations. | provenance gap in pre-freeze receipts | non-blocking (matrix re-observes both under receipts; scratch demo reproduced SIGSEGV `Received signal 11 SEGV_ACCERR` on probe×D3) | `wc -c .ufo/waves/round-64/l1/prefreeze-probe/dump-probe-x7.txt` → `0`; `grep -rn '139' .ufo/waves/round-64/l1/` → predicted-only |
| CC-3 | `dump-probe-ctrl.txt` (2880 B) records no producing binary; `diff dump-probe.txt dump-probe-ctrl.txt` shows ONLY heap-address drift (`0x311d…` vs `0x0381…`, same SFI/BytecodeArray[43] structure) — a second probe dump that cannot be attributed to D1 or D2 post-hoc. If it was D2, the plan's "Two were not run before the freeze" mis-states provenance. | plan-wording / provenance risk | non-blocking | `diff` output: lines 3-5, 12, 14-15, 38-57 … all address-only substitutions |
| CC-4 | Unpinned components beyond node: D2/D3 `snapshot_blob.bin`+`icudtl.dat` exist in their dirs but are unpinned (only D1's are); View8 `Parser/` tree unpinned (only `view8.py`); `--python` unpinned and the pre-freeze venv (`…/kaidoku-r64/lead/venv-r64`, visible as RuntimeWarning in view8-probe.log) differs from the counting command's `~/.local/share/kaidoku-jsc/venv` (both parse 1.22.4). Fake `--python /bin/true` IS caught (view8-empty ≠ view8-ok). So the predicate's "every input and binary sha256 equal to its pin" is scoped to the PINS table, which is narrower than the executed set. | pin-coverage boundary — disclose in lesson | non-blocking | glob `~/.local/share/kaidoku-jsc/d8-14.8.178.1/*`, `d8-14.7.173/*` → snapshot+icudtl present; `view8-probe.log:1-2` venv warning; `venv/bin/python -c …` → `3.15.0 parse 1.22.4` |
| CC-5 | Sourced claim (f): SUPPORTED. README at 01fc264d contains the exact CLI contract and the matching-d8 requirement: line 139 `./d8 -e "loadjsc('path/to/xxx.jsc')" > xxx.txt`; line 128 `### 1. Get the matching d8`; line 199 "Always use a **matching** d8 build"; line 121 "builtin helper `loadjsc()` that loads and prints `.jsc` bytecode"; line 122 View8 → "approximate JavaScript reconstruction" (the plan's measured correction "not parseable" refines, does not contradict). Stale cosmetic: the frozen tool docstring (line 3) still says "S125 README" — the renumbering to S264 happened at freeze; frozen, left unedited. | sourced-claim grounding | none — confirmed | `git -C ~/.local/share/kaidoku-jsc/jsc2js-src show 01fc264d…:README.md \| grep -n -i 'd8\|matching'` → lines 12,13,31,35,121,122,128,139,143,199 |
| CC-6 | (a) Falsifiability: holds. `verdict()` requires exact label equality for all 18; `not-run` counts as mismatch; partial/failed runs exit 1; pins pre-checked before any run (exit 2); no code path emits green without 18 exact matches. Controls re-verified live (selftest 22/0) and in the committed do-nothing receipt. | falsifiability | none — holds | selftest output `verdict-do-nothing-exit got=1`, `verdict-one-mismatch-count got=17`, `verdict-fake-green-count got=0`; c1-before-donothing.json `"exit": 1` |
| CC-7 | (d) "The route never runs the application": TRUE of the command set. The loadjsc patches register a d8 builtin containing NO `Execution::Call`, `->Run(`, `Script::Run` or `Compile(` (`grep` over `patches/` → zero matches); README: "loads and prints .jsc bytecode"; View8 is offline text processing; `node --check` parses only. The only executed code is the disclosed 2-line probe generator (mkcache.js, pinned). The Typora abort is a libc++ hardening OOB inside the loader (`vector.h:416: vector[] index out of bounds` → `Received signal 6`), an artifact-level outcome, not a version banner. | claim-statement truth | none — holds | `grep -rn 'Execution::Call\|->Run(\|Script::Run\|Compile(' ~/.local/share/kaidoku-jsc/jsc2js-src/patches` → no matches; `dump-match.err:1-2` |
| CC-8 | (c) Corroboration from a scratch run (CriticClaim's own, NOT the official receipt — L1 owns the landing run): 17/18 cells executed to frozen outcome classes under load before a deadline kill — probe×D1 and probe×D2 dump-ok with 212/213 B reconstructions (the unobserved probe×D2 prediction corroborated), probe×D3 dump 0 B + 646 B stderr with `Received signal 11 SEGV_ACCERR`, typora×D1 and typora×D2 aborts, 4.7 KB stderr with the same libc++ OOB (unobserved typora×D2 corroborated). Real-node SyntaxError on the receipted View8 output also reproduced. | prediction plausibility | corroborating, not verification | `ls /fast/scratch/hyaku/kaidoku-r64/CriticClaim/fake/matrix` (since deleted; classes quoted here); receipt copy: `w1/CriticClaim/receipt-false-node.json` |
| CC-9 | (e) Not-claimed list completeness: covers Typora-crash attribution, semantic-reconstruction, Typora code mapping, other V8 versions, Typora runtime. Missing three wordings for the lesson, not the claim: (i) `node-fail` means "node rejected (rc≠0)", not specifically a syntax-level rejection; (ii) reproducibility is single-host — ASLR-address drift is visible across repetitions (reconstruction 212 vs 213 B, ctrl-vs-main dump), which is why labels are class-equality, not byte-equality; (iii) unpinned auxiliaries (node, python, D2/D3 snapshot/icu, View8 Parser/) are outside the predicate's pin scope. | wording additions for the lesson | non-blocking | plans/round-64-claims.md "Not claimed:" section; reconstruction sizes 212/213 B across reps in CC-8 cells |

## Strongest counter-argument and what would falsify it

**CC-1.** The matrix's third stage cannot distinguish an honest SyntaxError rejection from any failing
`--node`, node carries no pin, and the receipt records no check rc/stderr — so 18/18 green evidences
"the reconstruction does not parse as JavaScript" only if the runner used the real host node. This is
the one route by which a green receipt overstates the evidence. What would falsify the critique: a
receipt that records the check rc/stderr plus a pinned node — impossible within the frozen instrument;
the honest mitigations are the lesson disclosure (CC-9-i) and the independently receipted 213 B
`probe-view8.js` whose SyntaxError is directly observable.

## Verdict

claim-survives — no blocking defect; disclose CC-1, CC-2, CC-3, CC-4, CC-9 in the round-64 lesson.
