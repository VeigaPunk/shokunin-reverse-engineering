# PL-1 — seat report (chain c1, arc3-loop1-round4, 2026-10-19)

Seat: **PL-1** · chain **c1** · role **planner** · artifact
`claims/c1/PL-1/plan.md`.

Planner seat. Per the freeze, planners produce a plan artifact and a seat report;
no corpus/README/PROVINCE/SKILL/LOG writes, no git mutations, scratch under
`/var/tmp` only. All measurements below were run first-hand by this seat; every
identity is re-derived at the path cited (rule #14) and no peer receipt is
trusted as identity.

## 1. Work performed (evidence pointers)

**1.1 Venv / python-compatibility pre-check** (the seat line's first ask).
Built four scratch venvs (3.11.17, 3.12.15, 3.13.16, 3.14.7 — all bootstrap
`venv` + `ensurepip` cleanly) and ran `pip install --dry-run vyper` in each,
with and without `--only-binary=:all:`. Result table and the silent-downgrade
trap (3.14 → vyper **0.4.1** wheel-only, because `immutables 0.21` has no cp314
wheel) are in `plan.md` §1.1. Scratch reports: `/var/tmp/pl1-r4/report-{bin,any}-*.json`.
Cross-checked PyPI metadata live (`vyper 0.4.3`, `requires_python <4,>=3.10`,
7 runtime deps; wheel sha256 `3b967172…`).
Re-derived the landed venv's identity myself rather than citing EX-02's receipt:
`vyper --version` → `0.4.3+commit.bff19ea2`; `bin/vyper` sha256 `615f792c…`;
`bin/vyper-json` `c64126b9…`; `bin/python` `d78f9cf7…`; `vyper/*.py` tree digest
`526cf63b…`; `dist-info/RECORD` `8bc98248…`; `pip list` shows
`vyper==0.4.3` (not 0.4.1) — `plan.md` §1.2.

**1.2 Carrier design + compile.** Wrote a second, structurally independent Vyper
carrier (`evidence/src/CarrierW.vy`, sha256 `5e66c85d…`) exercising all four
mutability classes, a payable `__default__`, a constructor *with* an argument,
and canonicalization-probing parameter types (`String[32]`, `Bytes[32]`,
`uint256[2]`, `bool`). Compiled with the wave venv
(`-f abi|method_identifiers|bytecode_runtime|bytecode`); runtime 829 B,
`evidence/CarrierW.runtime.hex` file sha256 `406e45ea…`, decoded-bytes sha256
`67d1d88f…`.

**1.3 Probe pre-measurement (eight envelopes, this seat's own runs).**
`evidence/probe/`: `Smoke-6.4.0-hex`, `CarrierW-{6.4.0,6.7.0}-hex`,
`CarrierV-{6.4.0-hex,6.4.0-raw,6.7.0-hex}`, `EX03-6.4.0-hex`,
`EX04creation-6.4.0-hex`. Pins `rea-agents@6.4.0`/`6.7.0`, provider
`evmole-interface evmole@0.9.3`, disk-backed TMPDIR on every invocation.

**1.4 Independent K/K verification.** `evidence/verify.txt` — for each carrier,
the probe's selector set compared against a set derived **by this seat** with
`EX-08/recon.py`'s pure-Python keccak over the *compiled ABI* (not the source
text, not the probe), plus decoded-digest binding and offset-landing census.
Also validated five available keccak oracles against standard vectors before
using any of them (node `keccak-256`, `js-sha3@0.8.0` from the r1 receipted
prefix, `EX-08/recon.py keccak-test`, `EX-10/keccak.py vectors`,
`EX-05/keccak_ref.py`), and cross-checked `pycryptodome` (in the same venv as
the compiler) against vyper's own `method_identifiers` 10/10 on CarrierW.

**1.5 Structural analysis.** Jump-table decode and offset-semantics census by
hand-written disassembly of the three runtime carriers; `__default__` phantom
byte-presence test; leading-zero normalization test; creation-vs-runtime
embedding test; envelope-delta diff across pins. All in `plan.md` §3–§4.

## 2. Proposed changes

**Patch-text proposals: none from this seat.** The plan specifies the *content*
and the acceptance shape of the two landing artifacts, but the freeze assigns
the patch texts to the chain's scribe/records seats, and PL-1 writing them would
collide with those seats' identity claims. Concretely, `plan.md` §6 gives:

- §6.1 the entry skeleton and the required observation list (each item with its
  envelope pointer), plus the QUALITY row mapping and the rule #11 citation form;
- §6.2 the README map-token patch, with the **verified before-text** quoted
  verbatim from `corpus/README.md` (one physical line; README 190 lines at HEAD
  `015e1bab…`) and a line-neutral after-text adding exactly one token
  (`2026-10-19-arc3-r4-evm-vyper-leg`);
- §6.3 the command-A before/after recipe (overlay mode, prior-83 manifest).

Entry stem and map token must agree; the token regex `2026-10-\d{2}-[a-z0-9-]+`
matches the proposed name.

## 3. Before → after measurement for the chain's claim

The claim has two arms; **both are measured, and the first is green**.

| measurement | before | after (measured by this seat) |
|---|---|---|
| command A (knowledge files) | 83 at HEAD `015e1bab…` (VZ-1 baseline re-derived, `missing [] dangling [] 14/14 10.0/10.0`) | 84 **not measured** — seats cannot commit; the overlay rehearsal is specified in §6.3, the authoritative read is the parent's at landing |
| Vyper K/K recovery | no Vyper carrier had ever been probed (r1/r3 Unknown) | **K/K on four carriers, zero extras**: Smoke 4/4, CarrierW 9/9, CarrierV 15/15, StewardToken 22/22; decoded `bytecode.sha256` = carrier sha256 on every leg; hex ≡ raw; set-equal across 6.4.0 and 6.7.0 |
| planted-vs-probe agreement | n/a | probe set == this seat's ABI-derived keccak set, `missing=[] extra=[]`, on all four |
| offset semantics | r1/r3 rule: reported offsets land on `JUMPDEST` | **refuted for Vyper**: 0/46 land on `0x5b`; 46/46 are preceded by `JUMPI` (`plan.md` §4.1a) |

So the claim's first arm is pre-measured satisfiable, and the honest-stop
branches in §5 are insurance rather than the expected path. **The one thing this
seat cannot measure is the 83 → 84 line itself** — that belongs to the parent's
landing measurement, and the plan says so explicitly rather than projecting it.

## 4. Attacks / refutations attempted, with verdicts

1. **Naive planted set from `method_identifiers` — REFUTED as a methodology.**
   Vyper emits an entry for the fallback (`__default__() -> 0x89402a72`) which
   the ABI carries as `{"type":"fallback"}`, not a named function. Measured:
   the 4-byte value **does not occur anywhere in the runtime bytes** on CarrierV
   or StewardToken. A planted set built from those keys is K+1 with a phantom.
   Rule landed in `plan.md` §3.2: planted set = ABI `type=="function"` entries only.
2. **Naive string compare against `method_identifiers` — REFUTED.**
   Vyper strips leading zero nibbles (`0xc751377` = `0x0c751377`,
   `0x776076f` = `0x0776076f`). Unnormalized, this reads as two missing
   selectors, i.e. a false "partial recovery". `zfill(8)` required; EX-05
   measured the same independently. `plan.md` §3.3.
3. **Source-spelling signatures — REFUTED.** `tag(String[32],Bytes[32],…)` hashes
   to `9d51c97e`, the canonical `tag(string,bytes,uint256[2],bool)` to
   `7425570b` (the value vyper itself emits). The planted set must be derived
   from compiled ABI types, never from the `.vy` text. `plan.md` §3.1.
4. **The r1/r3 offset-semantics rule, attacked against Vyper — REFUTED.**
   "Every reported offset lands on a JUMPDEST" is false for Vyper (0/46); the
   reported value is the handler's fall-through address after each compare
   `JUMPI` (46/46). Independently reached by RV-2
   (`RV-2/evidence/vyper-dispatch-shape.txt`). `plan.md` §4.1a.
5. **"The dispatch is a compare tree" (solc-shaped assumption) — REFUTED.**
   Vyper emits a **computed jump table**: `bucket = selector % K`, entry =
   big-endian `uint16` at `table + 2*bucket`, with `0x5e7` as the empty-bucket
   sentinel when K exceeds the bucket count (CarrierV K=15, 13 buckets, sentinel
   ×3). Decoded by hand from the prologue bytes; all 13 table entries are
   JUMPDESTs. Vyper also compares via `XOR` (15 `DUP2-XOR` sites in CarrierV)
   rather than `EQ` (4 byte occurrences) — an `EQ`-keyed extractor sees nothing
   here. `plan.md` §4.1.
6. **"Creation blobs are empty because the runtime isn't in them" — REFUTED.**
   EX-04's Vyper creation blob (1,637 B) embeds the runtime at byte 20, jump
   table included; the probe still reports 0 functions. The solc control
   (VaultB.opt200, runtime at byte 34) behaves the same. Verdict: **parsed-and-
   empty**, not an inventory exclusion (QUALITY row 11) — and the plan says so
   rather than repeating the r1 erratum's wording. `plan.md` §4.2.
7. **Venv pre-check as a formality — REFUTED (it earns its place).** On 3.14 the
   same `pip install vyper` that succeeds on 3.11–3.13 resolves **0.4.1** under
   `--only-binary`, with no error and a nominally-in-range `requires_python`.
   A receipt recording only "vyper installed" is insufficient there. EX-02's
   landed path (source-build `immutables` on 3.14) is valid and yields the
   non-downgraded 0.4.3 — verified first-hand, not assumed. `plan.md` §1.
8. **Re-measuring peer claims instead of trusting them — DONE.** All four K/K
   results, the `__default__` phantom, the zfill hazard, and the offset census
   were reproduced by this seat from the carriers' own bytes; agreement with
   EX-03/EX-04/EX-05/RV-2 is stated as corroboration, with the derivations kept
   separate in `evidence/verify.txt`.

## 5. Blockers

- **None for this seat's task.** The plan and all pre-measurements landed.
- **Named gap for the chain (not this seat's to fill):** `claims/c1/EX-06/` was
  still empty at this writing, i.e. the *executor's* probe legs for the claim
  carriers had not landed. The envelopes this seat produced are **planner
  pre-measurements** and must not be presented as EX-06's legs; if EX-06 does
  not land, the chain must either cite PL-1's envelopes *as planner
  pre-measurements* with that provenance stated, or take the honest-stop form.
- **Observation, not a blocker:** `git status` shows
  `.ufo/gates/custody-pair/{custody-pair.py,README.md}` modified during this
  window. That is C3's EX-21 (the round's designated implementer) writing the
  real custody target — authorized by the freeze. This seat wrote nothing there
  (hash/stat only) and ran no git mutation.
- Scratch is at `/var/tmp/pl1-r4/`; nothing was written to `/tmp`.
