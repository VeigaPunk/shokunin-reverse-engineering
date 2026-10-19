# CN-1 — arc3-loop1-round9 verdict and convergence

Seat: `CN-1` · verdicts/convergence · measured base `947091d6b6f52684faf9ca53adf94ff8a0f6b006` · verified-at `2026-10-19`.

## Disposition

**Integration HOLD.** The three frozen claims are adjudicated separately; this is not a scalar or a combined pass. C1's live inventory and candidate patch are supported, but its required gate-PASS condition is disproved. C2's selected Unknown is reproduced within a bounded fixture, but its corpus entry/map token and the 88/88 after-count are not landed. C3's pointer behavior is reproduced, but no authorized canonical receipt/corpus update was made. No source or custody change is proposed by this verdict.

## C1 — freshness: live inventory corrected in proposal; gate condition discrepant

`PROVINCE.md:50` still says `1556 signed archives` without a row-local as-of date. My direct count and two-way filename pairing were:

```text
archives=1350
.sig sidecars=1350
missing sidecars=[]
orphan sidecars=[]
delta_vs_1556=-206
wc -l PROVINCE.md -> 162
```

The current count is file/sidecar presence only, not cryptographic verification of all signatures. The `1,556` is retained as the dated 2026-10-13 snapshot; the extant erratum identifies that snapshot and the delta at `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`.

The other volatile row statements were censused:

- `available:true` in a live session is session-scoped and **UNVERIFIABLE as current** here; the containing Core table dates its recorded verification to 2026-10-13 (`PROVINCE.md:40`). The replacement dates it as historical and says it was not re-probed.
- Installed `jq` byte identity was **VERIFIED as of 2026-10-19**: `pacman -Q jq` → `jq 1.8.2-1`; `pacman -Qkk jq` → `jq: 25 total files, 0 altered files`; installed `/usr/bin/jq` and the cached archive member both hash to `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`.
- `.MTREE` per-file SHA-256, `pacman -Qkk verify`, and `binary_session {}` are respectively a format/property, a procedure, and a probe name—not other live counts. No current REA session was available to probe the `available:true` assertion.

Proposed **same-line replacement text only** for `PROVINCE.md:50`:

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` recorded in the 2026-10-13 live session; not re-probed); pacman `.pkg.tar.zst` corpus 1,556 signed archives (2026-10-13 snapshot; live re-count 2026-10-19: 1,350 archive files and 1,350 matching `.sig` sidecars, delta −206 vs snapshot; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` 1.8.2-1 byte-identical to its cached archive member (reverified 2026-10-19; SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`) |
```

I applied exactly this row to a `/var/tmp` copy, not to the source:

```text
patch_occurrences=1 original_lines=162 patched_lines=162
scratch census gate: VERDICT: FAIL (stale=0 ambiguous=0 undeclared=1 unresolved=0)
scratch_gate_exit=1
```

The live gate identity is SHA-256 `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`. Both live and scratch runs identify the same separate blocker: `SCORECARD.md` block `1833-1839`, line `1834`, an out-of-scope `6.7.0` pin with no client token; the declared SCORECARD range ends at line `1813` (`.ufo/gates/c1-census-v10.py:276`). The PROVINCE pointer at line 18 is `current-ok`; the whole gate is not PASS. Thus C1 is **CORRECTED as a measurement/proposal, DISCREPANCY against the frozen PASS condition, and not landed**. The PROVINCE row and gate were not edited.

## C2 — coverage: select EX-8's explicit R6 fallback Unknown

I select **one** candidate: EX-8's bounded investigation of the still-open R6 question, “the SUB-leg/fall-through interaction with a real fallback” (`corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`). I prefer it over the competing CR-1 / EX-11 Evidence-ID proposals and Vyper optimizer drafts because it maps directly to this explicitly named R6 Unknown and its corpus draft has `source:`, `verified-at:`, and `recheck:` fields (`claims/c2/EX-8/evidence/draft-corpus-entry.md:1-3`). EX-6 is a related measurement, but its draft does not carry the required `recheck:` field. This is CN-1's single-candidate ruling, not unanimous peer selection: CN-2 recommends EX-11, CN-3 CR-1, VZ-1 a Vyper residual, and VZ-3 EX-8 (`claims/verdicts/CN-2.md:71-96`, `CN-3.md:17-25`, `VZ-1.md:44-68`, `VZ-3.md:36-48`). Do not land multiple entries for this one frozen C2 move.

I did **not** execute EX-8's `rederive.sh`: inspection showed it redirects generated files into the peer's evidence directory. Instead I invoked its read-only `compile.js` with output directed to a fresh `/var/tmp` tree, probed those fresh runtimes using the cached local REA CLI, and ran its byte-walk against the temporary outputs. The initial compile invocation with a relative solc prefix failed before compilation (`MODULE_NOT_FOUND`); using the absolute prefix succeeded. All scratch was removed on exit; no peer file was written.

First-hand results:

```text
solc: 0.8.37+commit.f401782d.Emscripten.clang
soljson.js sha256: 221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c
settings: viaIR=true, optimizer.enabled=true, runs=200
no-fallback source sha256: f53911672f2e33eaabaeff85e75c2565bb2899638d194fb3ffe6747abe80cbbe
payable-fallback source sha256: 9c5c2d461bc2a3142984c6adb0f2082d3d3fd8ec3753105d3342bef812b51e6d
no-fallback runtime: 1517 bytes; sha256=2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a; repeat compile identical
payable-fallback runtime: 1525 bytes; sha256=a064b8de5b7d0aa924980f21df768e9338d41678d9e04bb0acebe8dcd029968d; repeat compile identical
REA, each runtime: raw=15, normalized=15, compiler selector set match=True, decoded SHA match=True
```

The opcode-boundary walk independently found 14 `EQ` legs and a final `SUB` leg for selector `ee02438e` in both runtimes. Both mismatch branches target PC `0x0e`. In the no-fallback bytes the nonempty miss reaches a revert path; with the payable fallback it reaches a path containing `CALLVALUE`, `SLOAD` slot 2, and `SSTORE` slot 2. This is a static bytecode/source inference, **not** an executed call. REA reports `confidence=inferred` and `runtime_execution=not-performed`; no deployment behavior is claimed. Proposed landing: `corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-miss.md`, EVM map token `2026-10-19-arc3-r9-viair-fallback-miss` (`claims/c2/EX-8/evidence/draft-corpus-entry.md:5`).

Command A, re-run from immutable HEAD per `SCORECARD.md:88-124`, returned:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":87,"mapped":87,"missing":[],"revision":"947091d6b6f52684faf9ca53adf94ff8a0f6b006","rule_blocks":15}
```

No corpus entry or map token was landed, so 88/88 remains **UNVERIFIABLE**, not a measured after-state. C2 is **REPRODUCED within the named fixture/compiler/settings boundary; integration remains pending**.

## C3 — calibration: line pointer is positional and perishable

A fresh search of `/home/vgpnk/.kimi-code/config.toml` found exactly one `rea-agents@` occurrence:

```text
/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
match count=1
```

Available dated config snapshots carry the same pin text at varying physical lines: `20261018-085645.bak:2915`, `20261018-114557.bak:2932`, `20261018-143236.bak:2940`, `20261018-145016.bak:3227`, `20261018-150133.bak:3298`, `20261018-161746.bak:3298`, `20261018-201656.bak:3157`; live is `:4126`. This confirms movement among the inspected snapshots, including non-monotone movement; it does not identify the cause of each shift or establish every intermediate edit.

The current gate grades `PROVINCE.md:18`'s `~/.kimi-code/config.toml:4126` pointer `current-ok (pins 6.7.0)`. I re-ran the gate's scratch-only `ptr_check()` experiment (`claims/c3/SC-2/evidence/rederive_drift.py`), which reads the live config and writes only a temporary copy under `/var/tmp`:

```text
source_occurrences=1 source_pin_line=4126 source_pin=args = [ "-y", "rea-agents@6.7.0", "mcp" ]
baseline live_kimi=6.7.0 ptr_check@4126=('ok', 'pins 6.7.0')
one-line-insertion occurrences=1 new_pin_line=4127 new_live_kimi=6.7.0
old_pointer@4126=('stale', "line holds no rea-agents pin: '# SC-2 hypothetical one-line config edit'")
reanchored_pointer@4127=('ok', 'pins 6.7.0')
```

The mechanism is positional: the gate's `live_pins()` takes the first version match (`.ufo/gates/c1-census-v10.py:324-334`), while `ptr_check()` dereferences the stated file and line and compares the pin version (`:466-482`). An insertion before the target moves the pin but not the stored line reference. The experiment did not edit the real config. This is **REPRODUCED** for one current match, the targeted `current-ok` result, and the controlled insertion/re-anchor behavior; uniqueness is only a current observation, not an invariant.

The full census remains **DISCREPANCY / FAIL** on the unrelated SCORECARD line 1834 described under C1. The frozen request to preserve the characterization in a canonical receipt/corpus entry is also not landed: the write fence forbids those paths, so this artifact is the only authorized record from CN-1 and canonical integration remains pending.

## Peer state and boundary

At this inventory snapshot, all eleven peer verdicts were present: `CN-2`–`CN-4`, `CR-5`–`CR-8`, and `VZ-1`–`VZ-4`; no verdict peer was absent. C2 preferences diverge: EX-8 (`CN-1`, `VZ-3`, `CR-7`), EX-6 (`CN-4`), EX-10 (`CR-5`, `CR-6`, `VZ-4`), EX-11 (`CN-2`), CR-1 (`CN-3`), the narrower Vyper creation-bytecode result (`VZ-1`, `CR-8`), and EX-5 (`VZ-2`). This is an adjudication, not a consensus: CN-1 retains EX-8 for its direct mapping to R6's explicit `SUB`/real-fallback Unknown, required recheck fields, and independent reproduction. Do not land multiple entries for this one frozen C2 move.

CN-1 wrote only `.ufo/waves/arc3-loop1-round9/claims/verdicts/CN-1.md`. Git remained read-only; the pre-existing `.ufo/waves/arc2-loop1-round10/C3.md` modification was left untouched. Scratch was confined to `/var/tmp` and cleaned. Protected paths (`PROVINCE.md`, corpus, gate, `SKILL.md`, `SCORECARD.md`, and `LOG.md`) were not changed.