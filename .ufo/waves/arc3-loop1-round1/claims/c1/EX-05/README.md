# EX-05 — c1 probe-leg artifacts (arc3-loop1-round1, 2026-10-19)

Seat line: `run rea inspect-evm-interface <compiled.bin> raw on EX-04's
bytecode; capture the full JSON output; record evidence id if sealed.`

**EX-04 landed (late) — seat command executed on its bytecode.** EX-04's
`claims/c1/EX-04/` appeared at 2026-10-19T10:09Z (found at check 13 of the
25-min background poll `bash-vo5t528p`; absent at every manual check through
10:06Z). Its artifacts are compiled KdxToken carriers — `token.runtime.bin`
(1789 B, sha256 `9c40940e…580e`), `token.creation.bin`, `token.abi`,
`KdxToken.sol`, `solc-input.json`, `solc-out.cleaned.json` — plus its own
self-check probe `ex04-selfcheck-probe-raw.json` (ev `ev_7a343fa7…`, real repo
path). The literal seat command was then run on EX-04's `token.runtime.bin`
(via a byte-identical copy, per the wave's copy-only rule for non-owner seats):
**exit 0, K=6/6, ev `ev_ce4d9f7e…`** → `ex04-token.raw.json`.

**Plan-vs-execution note (recorded, not silently resolved):** PL-1's plan
assigned EX-04 step S5 = independent selector derivation →
`keccak-receipt.txt` (`claims/c1/PL-1/plan.md:207-219,310`) and assigned the S6
probe legs to EX-05/EX-06 (`plan.md:221-236,311-312`). EX-04 in fact landed
compile carriers (S4-class work). The K-table independence S5 owed is covered
by RV-1's from-spec keccak + js-sha3 cross-check (`seats/RV-1.md:47-49`).

**Pre-landing reproduction (kept as an independent twin):** before EX-04
landed, the wave's canonical real bytecode (EX-06's `KdxToken.sol`, solc
0.8.37) was recompiled here with the wave's own solc-prefix (`compile-kdx.js`)
→ `kdx-runtime.bin` — **byte-identical to EX-06's recorded subject digest**
(`9c40940e…580e`) and, once EX-04 landed, **byte-identical on all four files**
(`cmp` on runtime/creation/abi/source). So every probe here is on the same
subject bytes EX-04 shipped.

## Artifact index

| file | what |
|---|---|
| `ex04-token.raw.json` | **PRIMARY** — literal seat command on EX-04's `token.runtime.bin` (copy); ev `ev_ce4d9f7e…`; K=6/6 |
| `kdx.raw.json` | same command on the pre-landing reproduction (`kdx-runtime.bin`, same bytes); ev `ev_4dd5ea20…`; K=6/6 |
| `kdx.raw.rerun.json` | determinism twin (same path): identical envelope except `meta.duration` (150ms vs 113ms); same ev id |
| `kdx.raw.renamed.json` | path-sensitivity twin (same bytes, renamed file): same bytecode sha, different ev id `ev_b29370…` |
| `kdx.hex.json` | `hex` leg on the same contract (ASCII-hex carrier); ev `ev_2a79dd25…`; K=6/6; same decoded bytecode sha |
| `kdx-creation.raw.json` | attack: `raw` on the *creation* blob (1817 B); 0 functions, `kind:"unknown"` |
| `kdx.hex-on-bin.json` | attack: `hex` on the binary → typed refusal `invalid_request` ("Hex carrier must be valid UTF-8."), exit 1 |
| `rv2.raw.json` / `rv2.hex.json` | secondary real contract (RV-2's Rv2Token runtime, K=5): raw ev `ev_0636c55d…`, hex ev `ev_1a60d32c…`, both 5/5 |
| `rv2.hex-on-bin.json` | same refusal class on the second contract |
| `rv2.640.raw.json` | cross-version twin: rea-agents@6.4.0 on the same bytes → identical selectors/offsets/inference |
| `recon.out.json` / `recon.640.json` | 5-byte synthetic carrier @6.7.0 / @6.4.0: identical decoded bytecode sha `b20db086…` (r3-07 carrier-1 value) |
| `kdx-runtime.bin` / `kdx-creation.bin` / `kdx-runtime.hex` | the pre-landing reproduction of EX-04's subject (byte-identical; sha256s in `probe-subject.txt`) |
| `kdx-abi.json` | ABI of the compiled contract (selector ground truth cross-check) |
| `compile-kdx.js` | reproduction script (node + wave solc-prefix) |
| `ex07-crosscheck.txt` | EX-07's independent extractor (M1 disassembler, M2 pure-python keccak) on `kdx-runtime.bin`: 6/6, 6/6 |
| `evidence-ids.txt` | every envelope's ok/ev-id/subject-digest in one table |
| `versions.txt` | version receipts (rea 6.7.0 default, 6.4.0 twin; node v26.12.0) |
| `probe-subject.txt` | subject provenance + sha256s + verbatim commands |

## Probe commands (verbatim, environment-forced TMPDIR)

```bash
# PRIMARY — literal seat command on EX-04's bytecode (byte-identical copy; copy-only rule)
TMPDIR=/dev/shm/ex05 npx -y rea-agents@6.7.0 inspect-evm-interface \
  /dev/shm/ex05/ex04-runtime.bin raw --format json --full-output > ex04-token.raw.json   # exit 0
# pre-landing reproduction of the same bytes
TMPDIR=/dev/shm/ex05 npx -y rea-agents@6.7.0 inspect-evm-interface \
  /dev/shm/ex05/kdx-runtime.bin raw --format json --full-output > kdx.raw.json           # exit 0
TMPDIR=/dev/shm/ex05 npx -y rea-agents@6.7.0 inspect-evm-interface \
  /dev/shm/ex05/kdx-runtime.hex hex --format json --full-output > kdx.hex.json           # exit 0
```

`TMPDIR` deviation: /tmp is a 16G tmpfs with `usrquota`; the 64-seat wave
exhausted the per-user quota (EDQUOT on 10-byte writes; EX-15's census lists
`/tmp/ex05-work/recon.*` as 0-byte casualties). All probes ran with
`TMPDIR=/dev/shm/ex05` (separate tmpfs, ample headroom); scratch was removed
after capture. Same failure class EX-06 hit when `TMPDIR` was unset
(`seats/RV-1.md:168`).

Subject provenance: EX-04's `token.runtime.bin` sha256
`9c40940ef88c0e82349af0b0bebb31fabf0b71bf68f5117478ac07d7e44e580e`; the
pre-landing `kdx-runtime.bin` is byte-identical (compiled 10:02Z from
`claims/c1/EX-06/evidence/KdxToken.sol` sha256 `c2980385…ccba` with the wave
solc-prefix; `cmp`-verified against EX-04's four files). Evidence ids are
path-sensitive for this verb — the same bytes probed at five different paths
yielded five ids (`ev_ce4d9f7e…`, `ev_4dd5ea20…`, `ev_b29370…`,
`ev_9259f412…`, `ev_7a343fa7…`); use `subject.digest.sha256` for identity.
