source: `corpus/evidence/round-26/c1/table.tsv` (24 committed REA 6.5.0 envelopes in `corpus/evidence/round-26/c1/envelopes/`, call records in `corpus/evidence/round-26/c1/runs.tsv`); S079 installed `rea-agents@6.5.0` Evidence-ID minting and projection source (opened 2026-10-22); S080 npm registry record for `rea-agents@6.5.0` (opened 2026-10-22)

verified-at: 2026-10-22, round 26; 24 CLI calls 12:11:50Z–12:15:45Z, package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/` (version 6.5.0)

recheck: `python3 -I -B tools/round-26/c1-id-identity.py --root <LANE> --rev <REV>` re-derives each verdict from the committed envelopes (offline). A live recheck copies `/usr/bin/jq` to a second directory with the same file name, checks both sha256 values equal `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`, and runs the argv in `.ufo/waves/round-26/claims.json` `verbs_argv` with `TMPDIR` set to a private scratch directory, never `/tmp`. Run it from the host login shell: the verbs need `GHIDRA_INSTALL_DIR` and the `REA_*` provider variables that `~/.bashrc` exports; without them they return `provider_unavailable` with `ok: false` and no id (seat reports `.ufo/waves/round-26/w1/ReplayA.md`, `ReplayB.md`).

# Evidence-ID identity of the eight native reader verbs at REA 6.5.0 — seven content-keyed, `inspect-binary-layout` path-sensitive

Coverage-map ground: evidence-ID identity per verb at the lane's carrier pin. Before this
entry the lane held a family-wide statement (`corpus/README.md` Known gaps, evidence-ID bullet)
backed by two-path controls at 6.4.0 (`analyze`/`inspect` in r5-01, `function` in r9-02) and
at 6.7.0 for four `inspect-*` verbs outside this set. No two-path control existed at 6.5.0 for
any of the eight verbs below, and five of them (`decompile`, `xrefs`, `read-bytes`,
`instructions`, `inspect-binary-layout`) had none at any pin.

## Observation

Carrier: `/usr/bin/jq`, 30,800 bytes, sha256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`,
and a byte-identical copy at `/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq` (same file
name, different directory). Address-taking verbs used `0x103fa0`, a function start (file
address `0x3fa0`; Ghidra image base `0x100000`; two direct callers in `main`; REA names it
`FUN_00103fa0` because the file is stripped, and only the host's separate debug information names
it `process`; seat report `.ufo/waves/round-26/w1/AddressCheck.md`). Each verb ran three times with the
frozen argv: base and same-path repeat on `/usr/bin/jq`, then the copy. All 24 calls exited 0
with `ok: true`, and every envelope's `.data.subject.digest.sha256` equals the carrier sha256.

| verb | operation id equality | verdict |
|---|---|---|
| `analyze` | base = repeat = copy, `ev_14f9d92f…b3d328` | content-keyed |
| `inspect` | base = repeat = copy, `ev_14f9d92f…b3d328` (the same id as `analyze`) | content-keyed |
| `decompile` | base = repeat = copy, `ev_03d78618…6014df` | content-keyed |
| `xrefs` | base = repeat = copy, `ev_d591ef8c…96b27c` | content-keyed |
| `read-bytes` | base = repeat = copy, `ev_99b0c6e1…47500c` | content-keyed |
| `function` | base = repeat = copy, `ev_b2b7e9e4…0488b5` | content-keyed |
| `instructions` | base = repeat = copy, `ev_b20a0f25…1125f8b` | content-keyed |
| `inspect-binary-layout` | base = repeat `ev_294a449c…0a71bd`; copy `ev_52da4b3d…dccd161` | path-sensitive |

Full ids are in `corpus/evidence/round-26/c1/table.tsv`. Base and repeat envelopes differ only
in `.meta.duration`; base and copy additionally differ in `.data.subject.local_path` (and, for
`inspect-binary-layout`, in the three path fields named below). So the envelope file sha256 is
not reproducible run to run while the evidence id is. Two independent replays in other sessions
(seat reports `.ufo/waves/round-26/w1/ReplayA.md` and `ReplayB.md`) reproduced the base ids, gave
the content-keyed verbs the same id at a third directory, gave `inspect-binary-layout` a third
distinct id at that third directory, and kept the id after only the file's modification time changed.

`analyze` and `inspect` return the same id because both CLI verbs call one operation,
`binary_overview`, with empty parameters (seat report `.ufo/waves/round-26/w1/IdentityClaimsMap.md`,
citing `dist/cli-runtime/cli.js` in the 6.5.0 package). An id alone therefore does not tell
which of the two verbs produced it; `.meta.command` does.

## Why — the minting rule in the installed source (S079)

`dist/domain/evidence.js:182` mints `ev_` plus the SHA-256 of a canonical-JSON semantic
projection (`:156-180`). The projection keeps the subject's `digest`, `format` and
`architecture` but not its local path or display name; among the other kept fields are
`parameters`, the raw and normalized results, limitations, `locations`, the analysis profile and
the provider. A verb is path-sensitive exactly when it writes the path
into one of those kept fields. `inspect-binary-layout` does: its service writes the run path
into `parameters.path`, `normalized_result.artifact.path` and an `artifact-path` location
(`dist/application/binaryDiagnostics/BinaryLayoutService.js:61-67`). The other seven verbs (five
answered by the Ghidra provider, `analyze` and `inspect` by the `rea-workflow` provider, per the
envelopes) put no path in those fields; the Ghidra runs analyse a private content-named byte
copy. A blind prediction written
from the source before the run outputs were read matched all eight verdicts (seat report
`.ufo/waves/round-26/w1/PredictionCritic.md`, predictions at 12:16:14Z).

No cache served the repeats. The 6.5.0 caches are content-keyed and none is reached by the frozen
argv: the in-memory analysis snapshot lives for one process (and a cached in-session replay adds a
hashed limitation, which would change the id), the snapshot file is read only with `--snapshot`,
and each Ghidra run imports a content-named copy into a fresh private project that is deleted
after the run (seat report `.ufo/waves/round-26/w1/CacheConfound.md`, citing
`dist/application/binary/AnalysisSnapshotCache.js`, `dist/ghidra/GhidraTargetSnapshot.js:14` and
`dist/process/PrivateRuntimeRoot.js:38`). Equal ids across the three runs are therefore provider
determinism, not a stored answer.

An independent standard-library recompute of the projection and digest,
`python3 -I -B tools/round-26/recompute-ids.py corpus/evidence/round-26/c1/envelopes/*.json`,
reproduces all 24 ids (`corpus/evidence/round-26/c1/recompute-ids.txt`: "24 match of 24 total").
Changing `subject.local_path` in an envelope leaves the recomputed id unchanged; changing
`parameters.path` or `normalized_result.artifact.path` changes it (seat report
`.ufo/waves/round-26/w1/RecomputeIds.md`).

## Pin dependence — the verdicts transfer across pins, the id values do not

The id values in the table are 6.5.0 values. Diffing the installed 6.5.0 and 6.7.0 packages
(seat report `.ufo/waves/round-26/w1/PinSourceDiff.md`) found two causes of different ids for the
same bytes and request: 6.7.0's projection always emits `relationship_coverage`, which 6.5.0
omits when it is null (`dist/domain/evidence.js:175-178` in each package), and 6.7.0's
`function` result carries changed `analysis_profile.parameters` names. Live pairs on
`/usr/bin/jq` confirm it: `inspect-binary-layout` 6.5.0 `ev_294a449c…` versus 6.7.0
`ev_d1256a96…`, `function` `ev_b2b7e9e4…` versus `ev_177586c6…`. The lane's stored 6.7.0
envelopes (arc3 rounds 7, 10, 11, 12) recompute exactly under the 6.7.0 rule and never under the
6.5.0 rule. So compare ids only within one pin. The relations themselves were measured here at
6.5.0 only; the two 6.7.0 calls above are single base runs and test no relation. That the same
eight relations hold at 6.7.0 is inference from the shared projection rule, not a measurement.

## Use

- To show two envelopes from these seven verbs came from the same bytes and request, compare ids;
  for `inspect-binary-layout`, compare `.data.subject.digest.sha256` and the parameters instead,
  because the same bytes at another path get another id.
- An equal id between `analyze` and `inspect` is expected and is not evidence that two verbs agree.
- Equal ids do not authenticate the subject path or module name: those fields are outside the
  projection (this agrees with `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-169`).

## Limits

One carrier, one pin (`rea-agents@6.5.0`), one address for the five address-taking verbs,
default parameters otherwise, and three runs per verb. The copy kept the file name `jq`, so the
table shows directory-insensitivity at an identical file name; sensitivity to a different file
name or extension was not tested. No claim is made for other pins, other carriers, other
parameter values, error envelopes, MCP sessions, or other verbs. The envelopes do not record
the package version; the pin rests on the call records and the resolved package root.
