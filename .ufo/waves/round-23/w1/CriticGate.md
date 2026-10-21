# CriticGate — R23-C1 cumulative reuse architecture

Seat: `KaidokuR23.CriticGate` (critic, read-only, leaf). Author-side critique, not verification.
Subject: the BuildCounter design in `.ufo/waves/round-23/gen-wave1.py:18` (wrapper loads pinned R22
`count-c1.py`, calls `measure` twice with R22/R23 `EVIDENCE_PREFIX`, unions by verb, S058+ gate for new
witnesses, frozen `--selftest`). No BuildCounter draft existed at review time
(`ls .ufo/waves/round-23/worktrees/` → only `AppImageLibraries`), so attacks target the specified design
plus the legacy code it must execute.

Axes attacked: count soundness (no inflation / no inherited loss), provenance identity, single
measurement snapshot, control independence. Frozen claim read:
`claims.json` sha256 `249811d9d103960811025d5305422e97271877bec1f470c1601cadc1f40d1906`.

## Findings

### F1 — Legacy `measure` cannot express the R23 new-witness gate (design defect, blocks as specified)
Observation:
- `.ufo/waves/round-22/tools/count-c1.py:129` hard-codes eligibility `int(id) >= 51 and tier A/B and mined
  and opened == "2026-10-21"`; `source_rows` is a local, not returned.
- `:142` eligibility is keyed by entry **text** (`eligible.add(text)`), not path.
- `:162` a witness is `[evidence_id, path]` — no entry path, no source id. `:167` truncates to
  `witnesses[:5]`.
- At a3c92eb the S051+ eligible set is exactly S051–S057 (13-cell parse of `git show a3c92eb:corpus/SOURCES.md`,
  57 rows, max S057). The R22 entry `corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md:1`
  cites S054/S055, i.e. legacy-eligible.

Counterexample: an R22-era entry (or any new entry whose first `source:` line cites S051–S057 and is
listed in that row's used-by) that names `decode-signal-recording` and cites a round-23 envelope with its
`ev_` id. The round-23-prefix `measure` call reports `exercised:true` with witness `[ev, path]`. The
wrapper has no field to tell this witness came from a non-S058 entry, so "newly counted witness must cite
mined S058+ with matching used-by" is unenforceable from `measure` output. To enforce it the wrapper must
re-scan entries and SOURCES itself, which is a second eligibility authority — contradicting "never
duplicate binding policy".

Impacted axes: count soundness, single authority.
Smallest safe correction: keep `measure` only for the **historical** R22 root. For the R23 root, the
wrapper owns one eligibility scan that emits explicit tuples
`(entry_path, source_id ≥ S058, evidence_path, evidence_id)`. It calls the legacy `bind_cli` (the
binding policy, reused, not copied) per tuple. Report every tuple, not `[:5]`. Then the round-23
`measure` call is redundant and should be dropped. Binding stays single-authority (`bind_cli`), and
eligibility is a new, explicitly R23-owned rule rather than a hidden filter over legacy output.

### F2 — Citation regex credits absolute, sandbox and foreign paths to the lane file (absolute-reference hole)
Observation: the R20 helper at aa1450b (sha256 `cfbf1880…f26f`, the pinned bytes) was executed in memory
with `CITED` rebuilt exactly as `count-c1.py:110` does for `.ufo/waves/round-23/evidence/c1/`.
`cited_prefixes` returned `['.ufo/waves/round-23/evidence/c1/inv.envelope.json']` for each of:
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/evidence/c1/inv.envelope.json`
- `…/round-23/worktrees/BuildSigrok/.ufo/waves/round-23/evidence/c1/inv.envelope.json` (sandbox copy)
- `/tmp/elsewhere/x.ufo/waves/round-23/evidence/c1/inv.envelope.json` (unrelated location)

The regex is unanchored (`verb-coverage.py:124` pattern, rebuilt at `count-c1.py:110`). `worktrees/` is
gitignored (`.ufo/waves/round-23/.gitignore:2`), so a sandbox citation names bytes that never exist at
REV, yet it is silently resolved to whatever L1 later commits under the lane path.

Counterexample: an entry drafted against a sandbox envelope cites the sandbox absolute path. L1 then
copies a different (re-run or edited) envelope to the lane path. The count binds the lane file as if it
were the cited artifact, as long as the `ev_` id appears in both.

Impacted axes: provenance identity.
Smallest safe correction: in the wrapper's R23 eligibility scan (F1), accept only lane-relative citations
preceded by a non-path character (start, whitespace, backtick, `(`). Refuse, rather than count, any
citation whose match is preceded by `/` or path characters. Keep the legacy regex untouched for the R22
root (no-harm). Add an "absolute/sandbox citation" control expecting no count.

### F3 — Two scans equal up to five independent revision resolutions (mutation between scans)
Observation:
- `count-c1.py:102` resolves `rev` and extracts helpers at that OID.
- `round-21/tools/verb-coverage.py:121` resolves again inside `_measure`.
- `count-c1.py:116` reads blobs at `result['rev']`, the second resolution.
- Two `measure` calls give four resolutions; the wrapper's own SOURCES/entry scan is a fifth.
- The lane is jj-colocated (`.jj` present), so Git `HEAD` is moved by jj operations.

[INFERENCE] concurrent L1 jj activity can move `HEAD` mid-run. Not exercised: I did not run jj, because
that would snapshot the production repo.

Counterexample: `--rev HEAD`. The historical scan reads commit A and the new scan reads commit B, or,
within one call, helpers come from A and the tree from B. The union mixes snapshots, and inherited
identify can be lost or gained without any single commit justifying it. Even the legacy counter alone has
this split when given a symbolic ref.

Impacted axes: single measurement snapshot, inherited-identify preservation.
Smallest safe correction: the wrapper resolves `--rev` exactly once (`rev-parse --verify --end-of-options
<rev>^{commit}`, require `[0-9a-f]{40,64}`). It passes only that OID to every call and scan. It asserts
each returned `rev` equals it, else exit 2. It emits `requested_rev` and `resolved_rev`.

### F4 — Calling `measure` directly bypasses the legacy environment guard (executing measured helpers)
Observation: `GIT_*` clearing and `GIT_NO_REPLACE_OBJECTS=1` live only in legacy `main()`
(`count-c1.py:190-193`). R20 `git()` (`round-20/tools/verb-coverage.py:65-66`) and the R22 `subprocess.run`
calls (`count-c1.py:56,102,116`) pass no `env`, so they inherit the caller's environment. A wrapper that
imports the module and calls `measure` gets no guard unless it re-implements one. `python3 -I` does not
clear `GIT_*`. No `refs/replace` exist today (`git for-each-ref refs/replace` → empty).

Counterexample: `GIT_DIR` or `GIT_OBJECT_DIRECTORY` inherited from a sandbox shell redirects both scans to
the sandbox clone while `--root` names the lane.

Smallest safe correction: the wrapper performs the same clear-and-set as the first statement of its own
`main()`, before loading anything. A selftest control runs the wrapper as a subprocess with a poisoned
`GIT_DIR`/replace ref and expects an unchanged count. R22 fixtures already run the counter via subprocess
(`counter-fixtures.py:260`), and the R23 fixtures must too.

### F5 — Pin the legacy counter and retained catalog by bytes read at the OID, and execute those bytes, not an in-place file
Observation:
- The legacy `count-c1.py` blob is `c925918f…9b1879` at both aa1450b and a3c92eb (`git show … | sha256sum`).
- The retained catalog `.ufo/waves/round-20/verify/round20/verb-coverage.json` is `7c0d57d7…c515` at a3c92eb.
  It is pinned only in the R22 *selftest* manifest (`frozen/expected-v2.json:8`), not in measurement
  (`round-21/tools/verb-coverage.py:125` reads it unpinned).
- `load()` (`count-c1.py:43-47`) uses `spec_from_file_location` → `SourceLoader.get_code`, which prefers
  `__pycache__` bytecode validated by source mtime+size, not by content hash (CPython 3.14.8 source
  inspected). `-B` only suppresses writing.
- `.ufo/waves/round-22/tools/__pycache__/count-c1.cpython-314.pyc` exists (10:15:18, source mtime
  10:41:02, so currently stale and not exploitable).

Counterexample: a wrapper that hashes `<root>/.ufo/waves/round-22/tools/count-c1.py` and then imports it
in place executes a mtime/size-matching pyc rather than the hashed bytes. Separately, a REV that edits the
catalog changes `catalog_total`/mention counts (the 153 denominator ConnectCounters relies on) without any
refusal.

Smallest safe correction: read legacy `count-c1.py` via `git show OID:path`, verify `c925918f…`, then
`exec(compile(bytes, …))` into a fresh module, or write to a tempdir as the legacy helper loader already
does (`count-c1.py:54-64`). Verify the catalog blob equals `7c0d57d7…` at OID, else exit 2. Record the
wrapper's own `sha256(__file__)` and, when present, require it to equal
`git show OID:.ufo/waves/round-23/tools/count-c1.py`. The claims `counting_command` path is relative to
cwd, not `--root`, so otherwise a different working-tree wrapper measures REV.

### F6 — Historical root is not frozen; new files under the R22 prefix count as "inherited"
Observation: the `.ufo/waves/round-22/evidence/c1` tree OID is `b83fc459dca64a8356480b1ebc8309b4de65de71`
at both aa1450b and a3c92eb. Legacy eligibility admits S058+ rows (≥51, same date `2026-10-21`). The claim
says new evidence goes "only under round-23/evidence/c1", but nothing enforces it.

Counterexample: a new envelope added (not modified, so "pre-round files unchanged" still holds) under
`round-22/evidence/c1/`, cited by a new S058 entry. The historical scan counts it, so a new verb enters
through the "inherited" root and bypasses every R23-specific gate (F1, F2).

Smallest safe correction: require `git rev-parse OID:.ufo/waves/round-22/evidence/c1` ==
`b83fc459…`, else exit 2. Require the historical result to be exactly `{identify-flutter-build}`, matching
`before:1`. If it changes, exit 2 ("inherited identify lost/gained"); do not union it silently.

### F7 — Frozen controls: what R22 actually froze, and gaps the R23 selftest must close
Observation:
- `frozen/expected-v2.json` holds only `expected_finding: counter_controls_clean`. Per-case exit/count
  live in code (`counter-fixtures.py:152-153,210-211`), frozen only transitively via that file's digest.
- The manifest `inputs` do not include the counter under test, and the selftest output records no
  counter digest (`count-c1.py:221-223`).
- Inputs are hashed from the **working tree** (`count-c1.py:213`, `root/rel`), not from REV. The fixture
  module is loaded in place (`:219`, same pyc path as F5).

Counterexample: selftest passes for working-tree wrapper X, measurement at REV runs committed wrapper Y.
Nothing in either output binds them. A "separately authored expected file" that again carries only a
finding name would let a fixture-code edit change expectations while the digests merely move.

Smallest safe correction:
- The R23 expected file lists every case id with expected exit, count, and the `t1_exercised` set.
- The wrapper embeds that file's digest.
- Selftest output records the wrapper's sha256 and the legacy pin.
- Fixtures load from bytes (F5).

Mandatory added controls beyond the assigned list:
- symbolic-ref race (F3)
- absolute/sandbox citation (F2)
- new file under R22 prefix (F6)
- R22-era-source entry citing R23 evidence (F1)
- more than five witnesses (truncation, F1)
- inherited `GIT_DIR` (F4)
- edited catalog blob (F5)
- working-tree-only legacy edit must still count (proves OID loading), mirroring R22 `helper_drift`

### F8 — Original-envelope identity stays outside the counter (tradeoff, retain as explicit limit)
Observation: the legacy docstring (`count-c1.py:15-16`) states that the envelope is not compared with
`run.stdout`. For Saber, `run.stdout` bytes == envelope bytes (sha256 `143af76e…904b`), and the run record
carries `artifact_sha256 de4813f9…` and `artifact_url`. The target path is ephemeral and absolute
(`/tmp/kd22probe/saber.apk`), and Godot evidence cites `/home/vgpnk/.local/share/godot/…`.

Counterexample: an L1 copy that drops a refused sibling or re-pretty-prints the envelope still binds. The
counter cannot detect "copy erases parent refusal" when the refusal lived outside the copied JSON.

Disposition: this is a tradeoff, not a wrapper defect. Either the wrapper checks, for each R23 witness, a
sibling `*.run.json` whose `stdout` bytes equal the envelope and which carries `artifact_sha256`, or the
output `limit` must state that this is unchecked. It must not be presented as covering the "copy erases
parent refusal" falsifier.

### Non-findings (bounded)
- Union by verb set prevents same-verb double count, provided it is computed over verb keys, not witness
  lists.
- `bind_cli` nested-refusal traversal (`count-c1.py:84-94`) plus R21 `records` ancestry
  (`round-21/tools/verb-coverage.py:58-74`) cover nested/list refusals inside the retained envelope.
- No `refs/replace` exist at review time.

## Produced files
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/CriticGate.md` (this report; sha256 in seat hand-off, a file cannot contain its own digest).

## Installs
None.

## Open risks
- [INFERENCE] The legacy date gate `opened == "2026-10-21"` (`count-c1.py:129`) excludes any S058+ row
  dated 2026-10-22. Host local time is −03:00 and the claim timestamp is UTC, so a late-wave source could
  be silently ineligible under any `measure`-based path. F1's own scan must state its date rule explicitly.
- F3 race is argued from code and jj colocation, not reproduced.
- No BuildCounter draft existed. Findings must be re-checked against the actual `output/count-c1.py`
  once it exists.
- No commands besides read-only `git show/rev-parse/ls-tree/check-ignore/for-each-ref`, `stat`, and
  in-memory Python were run. No builds, tests, REA, jj, or devices.
