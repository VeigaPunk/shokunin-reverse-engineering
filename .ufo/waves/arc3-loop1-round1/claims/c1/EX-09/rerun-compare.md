# EX-09 — rerun id-stability: byte-wise envelope compare (chain c1)

Seat EX-09 | wave `arc3-loop1-round1` | 2026-10-19 | HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
(`git rev-parse HEAD`, verified at 07:05 -03). Only repo writes: this artifact + `seats/EX-09.md`.
Scratch: `/var/tmp/ex09/` (deviation from the `/tmp` rule, cause in §6).

## 1. Verdict

**The evidence id IS stable across reruns of EX-05's exact invocation.** Four distinct runs
(EX-05 ×2, EX-09 ×2) of the identical command at the identical carrier path produced an
**envelope byte-identical** across all of them (9935 B, sha256
`729c48818d2eb776e9414ddb1ce775df8a6f8cecda78abe65294f2ec541d5129`), all sealing the same id:

```
ev_4dd5ea2051a41e8a952c571d068efde878e21a0f6296dd1ccecd91516b651a6a
```

The id was additionally **re-derived independently** from the envelope bytes (RFC 8785 canonical
JSON over the semantic projection, `subject.name`/`subject.local_path` excluded) — MATCH.
The only bytes that differ between runs anywhere in stdout are inside the `--full-output`
wrapper's `meta.duration` (150ms / 113ms / 146ms / 145ms), which is outside the envelope and
outside the id domain.

## 2. EX-05's exact invocation (the thing repeated)

EX-05's task (`SEAT LINE: SEAT EX-05 | CHAIN c1 | ROLE executor`): "run
`rea inspect-evm-interface <compiled.bin> raw` on EX-04's bytecode — encoding arg is POSITIONAL
per PROVINCE. Capture the full JSON output under claims/c1/EX-05/. Record evidence id if sealed."
EX-05's repo artifacts landed at 07:05 (`claims/c1/EX-05/`, 18 files).

Exact command as executed by EX-05 (recovered read-only from EX-05's live scratch dir
`/dev/shm/ex05/` and its session tool-call record — `agent-5` wire log — because EX-05's own
report had not landed when this seat started; the argv is corroborated by the envelope it
produced, whose `parameters`/`provider.version` pin path, encoding and provider version):

```
cd /dev/shm/ex05
TMPDIR=/dev/shm/ex05 npx -y rea-agents@6.7.0 inspect-evm-interface \
    /dev/shm/ex05/kdx-runtime.bin raw --format json --full-output > kdx.raw.json 2> kdx.raw.err
```

- carrier `kdx-runtime.bin` sha256 `9c40940ef88c0e82349af0b0bebb31fabf0b71bf68f5117478ac07d7e44e580e`, 1789 B
  (EX-04's compiled contract runtime; EX-04's own artifact dir had **not** landed at compare time —
  gap named in §6). EX-04's artifact dir does not exist, so this carrier is EX-05's own copy —
  the solc provenance is EX-05's claim, not verified by this seat.
- provider `evmole-interface` / "REA EVM interface adapter" / `evmole@0.9.3`; `dispatch:"abi"` for
  all 6 recovered selectors (`095ea7b3, 18160ddd, 23b872dd, 40c10f19, 70a08231, a9059cbb`).

## 3. The rerun (EX-09)

Same argv, same carrier path, same provider version; only the temp dir and cwd are EX-09's own
(both are proven outside the envelope in §5):

```
cd /var/tmp/ex09
TMPDIR=/var/tmp/ex09/tmpdir npx -y rea-agents@6.7.0 inspect-evm-interface \
    /dev/shm/ex05/kdx-runtime.bin raw --format json --full-output > kdx-rerun-1.json 2> kdx-rerun-1.err   # exit 0
TMPDIR=/var/tmp/ex09/tmpdir npx -y rea-agents@6.7.0 inspect-evm-interface \
    /dev/shm/ex05/kdx-runtime.bin raw --format json --full-output > kdx-rerun-2.json 2> kdx-rerun-2.err   # exit 0
```

Whole-stdout sha256: EX-05 `f8be246acb590213e7a7f45ef229bd6fa8a44dcde7e7643321a05c82ef772b39`,
rerun-1 `020e3800f66a89d58a277561b1da88b2648d48cbedcb34c7afa2b90b5db9309e`,
rerun-2 `7ec49625d08146f38872ac9cc848d965ca02861953a21aff9fc098a8aa18e023` — these differ **only**
in `meta.duration`; both stderr files 0 B.

## 4. Byte-wise envelope comparison (five samples — four distinct runs; rows 1–2 are the same run in two locations)

The envelope is extracted as the exact `"data":…,"meta":` substring of the raw stdout bytes
(no re-serialization, no key reordering).

| # | sample | source | envelope bytes | envelope sha256 (first 24) | evidence_id |
|---|--------|--------|---------------|----------------------------|-------------|
| 1 | EX-05 original (scratch, frozen copy) | `/var/tmp/ex09/kdx-backup/ex05-kdx.raw.json` | 9935 | `729c48818d2eb776e9414ddb` | `ev_4dd5ea20…` |
| 2 | EX-05 landed | `claims/c1/EX-05/kdx.raw.json` | 9935 | `729c48818d2eb776e9414ddb` | `ev_4dd5ea20…` |
| 3 | EX-05's own rerun | `claims/c1/EX-05/kdx.raw.rerun.json` | 9935 | `729c48818d2eb776e9414ddb` | `ev_4dd5ea20…` |
| 4 | EX-09 rerun-1 | `/var/tmp/ex09/kdx-rerun-1.json` | 9935 | `729c48818d2eb776e9414ddb` | `ev_4dd5ea20…` |
| 5 | EX-09 rerun-2 | `/var/tmp/ex09/kdx-rerun-2.json` | 9935 | `729c48818d2eb776e9414ddb` | `ev_4dd5ea20…` |

All five envelopes byte-identical → `cmp`-clean pairwise. Full envelope sha256:
`729c48818d2eb776e9414ddb1ce775df8a6f8cecda78abe65294f2ec541d5129`.

Whole-wrapper comparison: `{"ok":true,"data":<envelope>,"meta":{"command":"inspect-evm-interface","duration":"<ms>"}}`
— `meta.duration` observed 150ms (EX-05 original), 113ms (EX-05 rerun), 146ms / 145ms (EX-09) →
byte-difference confined to a field that is neither in the envelope nor in the hashed projection.

## 5. Independent id re-derivation and attacks (all run, with verdicts)

Tool: `/var/tmp/ex09/reid.py` — Python re-implementation of `dist/domain/evidence.js:159-183`
(`semanticProjection`) + `dist/domain/canonicalDigest.js` (RFC 8785: `Object.keys().sort()` in
UTF-16 code-unit order, `JSON.stringify` scalars, no whitespace, sha256), read from the pinned
`rea-agents@6.7.0` package cache. The tool auto-includes `relationship_coverage` when present in
the record (6.7.0-only field).

| # | attack | command / method | result | verdict |
|---|--------|------------------|--------|---------|
| A | Re-derive the id from the envelope | `python3 reid.py <envelope>` | `canonical_bytes: 9781`; derived == recorded `ev_4dd5ea20…` | MATCH — id function reproduced bit-exactly, not just observed twice |
| B | Display-field mutation (`subject.name`, `subject.local_path`) | mutate those two keys, re-derive | id unchanged (`ev_4dd5ea20…`) | CONFIRMED — the r10 statement "id domain excludes `subject.name`/`local_path`" is executable, not just read from source |
| C | Semantic mutation (a recovered selector) | set `functions[0].selector="0x00000000"`, re-derive | id changes to `ev_5e094edb72986625626274c70b1b62e81683f692e1f1fa94abeeaf84cdda84b5` | CONFIRMED — the id is content-keyed, so B is a real exclusion and not a broken canonicalizer |
| D | Carrier digest ↔ envelope consistency | `sha256(bytes.fromhex(bytecode.hex))` vs carrier file | both `9c40940e…`, 1789 B | CONFIRMED — the envelope's decoded bytecode is exactly the carrier that was probed |
| E | TMPDIR/cwd dependence | EX-05 ran with `TMPDIR=/dev/shm/ex05`, cwd `/dev/shm/ex05`; EX-09 with `TMPDIR=/var/tmp/ex09/tmpdir`, cwd `/var/tmp/ex09` | envelopes byte-identical | CONFIRMED — neither temp dir nor cwd reaches the envelope or the id |
| F | Path sensitivity (rerun at a *different* path) | EX-05's own `kdx.raw.renamed.json`: same bytes at `/dev/shm/ex05/kdx-runtime-renamed.bin` | id changes to `ev_b293709088888e4f1424e36252305b9a9fea58f0ad830d176bedfb42b0a8ed62` (re-derives MATCH) | CONFIRMED — the id is path-keyed via `parameters.path`, `normalized_result.artifact.path`, `locations[].path`; "rerun" must mean *same path*, else the comparison is measuring the path change |
| G | Version twin (is a differing id always instability?) | EX-05 ran the *same* command on the *same* `rv2-runtime.bin` under 6.7.0 and 6.4.0 | 6.7.0 id `ev_0636c55dc312eacbf…` vs 6.4.0 id `ev_76a1c1e347a394fa2…`; both re-derive MATCH under their own projections | REFUTED as instability — the envelopes genuinely differ (`bytecode.metadata` terminal-CBOR block + `relationship_coverage` exist only in 6.7.0), i.e. a schema/version difference, not a rerun effect. Reruns must pin the provider version |

## 6. Gaps / blockers (named, not absorbed)

- **EX-05's seat report had not landed at write time** (`seats/EX-05.md` absent; its 18 claim
  artifacts landed at 07:05). The comparison therefore rests on EX-05's **landed** artifacts
  (rows 2–3 of §4) plus its sha256-frozen scratch output (row 1), not on its prose.
- **EX-04's artifact dir does not exist** (`claims/c1/EX-04/` absent at 07:05) — the carrier
  `kdx-runtime.bin` is EX-05's own copy; its solc provenance is EX-05's claim, not verified here.
  If EX-05 later re-seals a different invocation (e.g. on EX-04's file at a different path), this
  verdict covers the `kdx-runtime.bin` invocation only.
- **`/tmp` is unusable for this user** (tmpfs 16G 80% + usrquota → `EDQUOT`/errno -122 on any
  write, reproduced: `printf` → "Disk quota exceeded"). The EVM worker writes through `TMPDIR`
  and **fails with `execution_failure` "Unknown system error -122"** unless `TMPDIR` is
  redirected — verified with both a relative and an absolute carrier path. Scratch moved to
  `/var/tmp/ex09/` (root fs, 703G free) as the closest equivalent; deviation recorded here.
  Durable copies of the rerun outputs and the re-derivation tool sit in this artifact's own dir:
  `claims/c1/EX-09/kdx-rerun-1.json` (sha256 `020e3800f66a89d58a277561b1da88b2648d48cbedcb34c7afa2b90b5db9309e`),
  `kdx-rerun-2.json` (`7ec49625d08146f38872ac9cc848d965ca02861953a21aff9fc098a8aa18e023`),
  `reid.py` (`879e09a187646238fbbadd91bf84a1974e4f3d058813daf4bd8067e19824fbdb`);
  bulk temp dirs removed.
- **Verdict scope**: id stability is confirmed for *this* invocation (EVM probe, raw encoding,
  evmole@0.9.3 inside rea-agents@6.7.0, one carrier, same path, 5 samples). It does not test other
  operations or other scale points; the r10 leg remains the only other measured point.
