# R38W2ReproK4 artifacts — independent K4 C1 receipt reproduction

Self-contained evidence for `.ufo/waves/round-38/w2/R38W2ReproK4.md`.
Produced by a non-author leaf seat, wave 2, round 38 attempt 2.

## Files

| file | sha256 | what it is |
|---|---|---|
| `env_before.json` | `a3a009bf00ce84217a28a15e2bcc364b53a287616fdb5a99a98ed7c5e1eb9597` | my before-arm REA envelope (`$HOME/.local/bin` stripped from PATH) |
| `env_after.json` | `69b52f508007b578959260a57aad24267669bb3e6dd24d2d6e36d94e220aee56` | my after-arm REA envelope (default PATH) |
| `env_after2.json` | `ffa61392009e901d391e70f78910dce22ca650f7ba60a706f6dcd04b55461f18` | second after-arm run (determinism control) |
| `env_v4be_only.json` | `f635f263b22ceea484a99fd6202c2be87219edcc93445b6d720c54240ce538ac` | PATH = stripped + `sasquatch-v4be` only |
| `env_sasquatch_only.json` | `d170b0f15d67cc6891db4904672aab2c0d08875b9362f53aa8463018bc027669` | PATH = stripped + `sasquatch` (v1–4) only |
| `compare.py` | — | reproduces the semantic-payload/oracle comparison from these artifacts |
| `compare.out` | — | its output (0 semantic diffs both arms, 4/4 oracle matches) |
| `checkid.mjs` | `a5b2ca2543d10244e3d4991c32d2f4b5ade8b2c79070cbdb958820810cf439b4` | vendor `parseEvidence` replay over these envelopes + the committed receipts |

`compare.py` and `checkid.mjs` take absolute paths, so they run from any cwd.
`checkid.mjs` needs `P=<rea-agents 6.5.0 package root>` in the environment
(`P=$HOME/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents node checkid.mjs …`).

## Carrier and oracle pins (recomputed from git objects at `3b960fe5`, not from the manifest)

| item | pin |
|---|---|
| `corpus/evidence/round-37/c1/K4/carrier.bin` | sha256 `a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed`, 307 bytes |
| `.ufo/waves/round-38/c1/carriers.json` K4 pin | `a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed` — **identical** |
| `corpus/evidence/round-37/c1/K4/oracle.tsv` | sha256 `638a6f75579ae1ff508d3152723b1b9b279a90090e180cc63a2a6a758a477d23` (4 rows) |
| committed `K4/before.json` | sha256 `000adcfb928a2032395bc47fbab175d1a1e356277db28eb26022f4d5012131e5`, blob `d42a0929…` |
| committed `K4/after.json` | sha256 `d26830916167ff1cee8ddd089605e6e4024f7b77ad56cf4e86907bda1622e28d`, blob `93079cfc…` |

## PATH attribution matrix (2×2 control)

| PATH state | `sasquatch-v4be` reachable | `sasquatch` (v1–4) reachable | coverage | files published | extraction gap |
|---|---|---|---|---|---|
| `$HOME/.local/bin` stripped | no | no | `partial` | 0 | `missing-extractor-dependency` deps `["sasquatch-v4be"]` |
| stripped + only `sasquatch-v4be` | **yes** | no | `complete` | 4, all oracle-matching | none |
| stripped + only `sasquatch` | no | yes | `partial` | 0 | `missing-extractor-dependency` deps `["sasquatch-v4be"]` |
| default PATH (both) | yes | yes | `complete` | 4, all oracle-matching | none |

The before→after delta is attributable to `sasquatch-v4be` reachability alone; the older
`sasquatch` (v1–4) binary does not satisfy the dependency.

## Binary pins seen inside the envelopes

| binary | version | sha256 |
|---|---|---|
| unblob (via `~/.local/bin/unblob` → uv tool) | 26.6.4 | `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` |
| `sasquatch-v4be` | 4.5.1 | `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6` |
| `sasquatch` | 4.5.1 | `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` |

The `executable_sha256` recorded in my envelopes and in the committed receipts is the same
`0ce7b624…`, i.e. the receipts came from this exact stock unblob binary.

## Evidence ids (vendor-authenticated, not hand-trusted)

`checkid.mjs` calls the package's own `parseEvidence` (`dist/domain/evidence.js`, which
`superRefine`s `computeEvidenceId(withoutId) === evidence_id`):

```
env_before.json:    PASS id=ev_854527ec55fbb4dfeae033e9f8c3400c101acde2ab9debaeb1f43e732c4f0056
env_after.json:     PASS id=ev_071c77df9b5fe712c8f9df7d077e550f0c3616ce6e9afcb12ede7f195b8d187f
K4/before.json:     PASS id=ev_c4444070ecf5d3832fb8607464c85cdb6c6ff6cb2a71f1a85f9464d13c0bf8a1
K4/after.json:      PASS id=ev_4348dcafae0806d8c098b00b18eef0765aa074fe1c1712f45ff0d5a49bfbae2e
```

## Landing-integrity cross-checks (read-only, lane artifacts)

- committed `K4/after.json` vs wave-1 author artifact
  `.ufo/waves/round-38/w1/artifacts/R38ExecAfterK4/after.json` (sha256 `ca329ef3…`):
  full envelope equal after canonicalizing output paths/blob ids/id; **sole differing
  parameter is `output_directory`** (`R38ExecAfterK4/out-lane` → `l1-receipts/K4-after`).
  So L1 regenerated rather than hand-edited the receipt.
- committed `K4/before.json` vs both wave-1 before-arm envelopes
  (`envelopes/h-K4-stripped.json`, `envelopes/direct-K4-stripped.json`): full-envelope equal.
- my `env_before.json` / `env_after.json` vs the committed receipts: **0 semantic diffs**
  (see `compare.out`).
