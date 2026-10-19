# CN-2 — arc3-loop1-round7 verdict and reconciliation

Seat: CN-2 · verdict/reconciliation · 2026-10-19 · `kaidoku-shokunin`.

## Ruling

- **C1 — REPRODUCED; PL-2 is the better-scoped patch text.** The blind spot is real. In isolated scratch, the PL-2 candidate passes on the current source copy and fails on a dead-pointer seed while preserving the receipt anchor. RV-2 independently demonstrates the same current-pointer bug and seeded catch, but registers only the full `:3546` locator; PL-2 also registers the frozen claim’s shorthand receipt `:3298`.
- **C2 — REPRODUCED for the bounded Vyper K8 characterization; landing/axis exit PENDING.** Four of the six C2 artifacts propose the Vyper `--no-optimize` / `-O codesize` Unknown (EX-4, EX-5, CR-1, CR-2); EX-3 and EX-6 pursue the `ev_` ID domain. CN-2 freshly recompiled and reprobed the Vyper cases. However, the corpus entry and map token remain drafts: Command A is still 85/85, and no post-landing 86/86 measurement exists. Do not report the coverage axis complete yet.
- **C3 — REPRODUCED; adjudicate, no corpus edit.** CN-2 measured 1,350 current archive paths, 206 below the dated 1,556 receipt. This is mutable inventory, not a capability invariant. Four C3 artifacts select the no-edit adjudication (SC-2, EX-8, EX-9, SC-1); EX-7 and RV-3 propose an append-only erratum. Preserve the dated source receipt, but flag the current-sounding `PROVINCE.md:50` statement as a separate residual.

Frozen work commit: `2fba56fe7d54cfb94ca9332c11cea81667b3b289`. Records HEAD at inspection: `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804`.

## C1 — pointer-check blind spot

The frozen claim at `claims-frozen.md:14-38` says that pointers in a pin-bearing clause must be evaluated, the receipt-stamped current pointer must remain current-by-design, a dead re-key must fail, and the G21/counter surface must be retained. At HEAD, `.ufo/gates/c1-census-v10.py:511-514` only gathers `PTR` matches inside `if not occ`; pins/bare versions in the same unit suppress pointer collection. The regex at `:311` requires a full path plus line number. `PROVINCE.md:18` now carries the current full path `~/.kimi-code/config.toml:3546`, along with the dated/shorthand receipt `:3298` (and older `:2940`, `:3227`). Direct baseline `ptr_check` calls for both 3298 and 3546 return `stale` because those lines do not themselves hold the REA pin. Baseline gate still passes: `PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; G21 is 14 rows with no errors.

I independently applied the PL-2 patch logic to a copy of the gate and the three scoped source documents under `/var/tmp/cn2-r7-c1/`; no repository gate/source file was edited. Candidate SHA-256: `7a5c2123e8ecd7aa595a262f322ada98239aef3af855aebb408eda9b801d8ab7`.

- Clean scratch candidate: exit 0, `PASS`; both `:3546` and receipt `:3298` report `current-ok` only through the exact stamped/pin/live-anchor receipt binding. G21: 14 rows, no errors; G2 true.
- Seeded copy: changed only the full current locator `:3546` to `:999999`. Candidate exit 1, `FAIL`; `:999999` is `UNRESOLVED` (`line 999999 beyond EOF (4150 lines)`), and the now-missing registered `:3546` anchor is also unresolved. The distinct `:3298` receipt remains receipt-anchored/current-ok.
- Baseline and clean-candidate JSON each have the same 19 keys; `counts` (the files’ line/locus counts) are unchanged. G21/G2 are intact. The expected `current_ok_per_file` values rise from Province 17→21, Scorecard 14→16, Skill 3→3 as formerly suppressed pointers become detections; in the seeded tree Province is 20, Scorecard 16, Skill 3. Thus the output surface and unrelated counts remain, while the pointer-derived positive counter changes. If “every counter intact” was meant to require identical numeric `current_ok_per_file` values, that stricter reading is not met by either candidate that actually exposes new current pointers.

PL-2’s exact-locus receipt registration matches the frozen `:3298` blind spot more fully than RV-2’s `:3546`-only receipt table. Neither patch was applied; C1 asked for patch text and scratch fault evidence, not a landed gate change.

## C2 — Vyper optimizer dispatcher forms

The selected motion is the r4 Vyper Unknown named at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`, bounded to the K8 synthetic source, Vyper `0.4.3+commit.bff19ea2`, and the two frozen options. CN-2 rebuilt from the read-only K8 source into `/var/tmp/cn2-r7-vyper/` and ran REA 6.4.0 on the newly emitted runtimes.

- `--no-optimize`: 617 bytes; decoded-runtime SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`. REA returned 8 functions and the eight selectors `2ae1431c, 364605a1, 9adbf691, 9b7c2962, bf3724af, cf35f823, d7531d91, d7b7913b`. Independent opcode-boundary walk found eight `PUSH4` selector literals, each followed by `DUP2; EQ; ISZERO; PUSH2; JUMPI`.
- `-O codesize`: 360 bytes; decoded-runtime SHA-256 `bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5`. REA returned the same 8 selectors. Byte walk found no opcode-boundary `PUSH4`, `CODECOPY` at PCs 12 and 45, and a 61-byte table tail at `0x12b` containing the selector/target records. These observations support two distinct dispatcher forms on this fixture; selector/ABI interpretation is still analyzer/compiler-derived, not runtime-execution evidence.
- Offset caveat: noopt’s eight offsets are `PUSH4_pc + 12` and point at `CALLVALUE` (`0x34`); codesize reports the same offset 65 (`DUP1`, `0x80`) for every function. Neither offset set establishes individual handler identity.

The peer Vyper artifacts agree on the byte hashes and bounded forms. EX-3 and EX-6’s ID-domain work is also substantive, not rejected as false: CN-2 independently recomputed all eight EX-3 envelope IDs from the package-described canonical semantic projection; all eight matched. The 6.4.0/6.7.0 package `evidence.js` and 6.7.0 `canonicalDigest.js` hashes also matched the supplied hashes. Separately, six fresh 6.7.0 EX-6-shape calls on identical 1,517-byte carrier copies (SHA-256 `2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a`) reproduced the relation: same resolved path/repeat, changed TMPDIR, and relative spelling of the same path retained one ID; renamed basename and changed parent path changed the ID while all 15-function/bytecode payloads stayed constant. These are bounded ID observations; they do not generalize beyond the tested operation/request/package cases. The Vyper motion is selected because it has four convergent C2 artifacts and directly closes the specifically named byte-characterization gap; the two ID-domain explorations remain useful residual knowledge.

Command A was re-run from `SCORECARD.md:88-124` against both the frozen work commit and records HEAD:

```text
2fba56fe7d54cfb94ca9332c11cea81667b3b289: knowledge_files=85 mapped=85 missing=[] dangling=[] citation_resolved_rules=15/15 coverage=10.0 depth=10.0
ebdcc8eb1cf01134e9ed01f2402fe97736a8b804 (HEAD): knowledge_files=85 mapped=85 missing=[] dangling=[] citation_resolved_rules=15/15 coverage=10.0 depth=10.0
```

The second line abbreviates the records HEAD above (`ebdcc8eb1cf01134e9ed01f2402fe97736a8b804`). `corpus/README.md:38` remains unchanged and contains no arc3-r7 Vyper token. EX-4, EX-5, CR-1 and CR-2 propose conflicting token/entry stems (`...dispatch-shapes`, `...optimizer-forms`, `...optimizer-variants`). Integrator must choose/merge one bounded entry, append exactly one map token, then rerun Command A at the actual landing commit. No 86/86 result is asserted here.

Scope limits: this does not generalize to other K values, Vyper releases, source programs, EVM targets or deployed contracts; `-O none` was not a separate compile in the selected paired experiment. No contract was executed, and no deployment identity was established.

## C3 — pacman package-cache inventory

Independent current measurements by CN-2:

```text
Python pathlib direct-child regular *.pkg.tar.zst files: 1350; non-files: 0
Bash nullglob *.pkg.tar.zst paths: 1350
Historical receipt: corpus/knowledge/2026-10-13-pacman-packages.md:21-25 = 1556 (verified-at 2026-10-13)
Delta: 1350 - 1556 = -206
```

This reproduces the cache drift, not a signature audit, archive-integrity test, or byte-size measurement. I adopt disposition (b) from `claims-frozen.md:55-69`: leave the dated corpus fact intact; the live cache count changes through retention/eviction and is not a capability claim. This resolves the C3 disposition split (four no-edit artifacts, two erratum proposals) without substituting a transient current value for the dated source observation. Residual: `PROVINCE.md:50` repeats 1,556 without an explicit as-of qualifier, so it is misleading if read as a live count; this verdict does not alter it.

## Custody and limits

CN-2 wrote only this verdict file in the repository. All candidate gates, compiler outputs and REA envelopes used for CN-2 reprobes were under `/var/tmp/cn2-r7-*`; repository gate, corpus, map, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, and other seats were left untouched. The pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md` and the pre-existing untracked arc3 wave were not touched. The project `AGENTS.md` normally asks for a LOG entry, but the seat’s explicit write fence excludes `LOG.md`; no LOG edit was made.
