# R44W2C1Controls — CTL-C1-1 and CTL-C1-4 re-scored: both red as recorded, two stated reasons false

**Seat** R44W2C1Controls · lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · measured
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac` · freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`
· base `c29360e3ba5381a5ab69e372d0d9577970f85018` · dispatch tip `c86ea508` (lane HEAD observed
at dispatch: `8bb1090af3fef64477c4337855e4347472db2701`).

**Answer.** Both arms reproduce the committed verdicts exactly — counter exit `1`,
`carriers_matched 0`, `met_target false`, `frozen_path_changed []`, and a failing-binding vector
identical to `.ufo/waves/round-44/controls/{c1,c4}/counter.json`, from an independently rebuilt
control tree whose 10 files hash to the frozen blobs. CTL-C1-4's red is genuinely load-bearing on
`run_provenance_ok`, and for `v1le` that is the *only* clause that fires. **But two of the three
bindings the record names as the reason for these reds do not fire at all**: `layout_ok` is `true`
in CTL-C1-1 (the superblock is a property of the carrier bytes, which the arm never touches), and
`evidence_id_ok` is `true` in CTL-C1-4 (the id is recomputed from the envelope's own bytes, so a
byte-identical pre-freeze envelope is self-consistent). Neither error changes an exit code, the
C1 honest-stop verdict, the `summary.json` verdicts, or the kill rule; both are record /
tool-description defects for round 45. I changed no claim, counter, rubric, frozen byte or
production doc.

---

## 1. Method

One clone, one work tree, absolute paths, everything disposable under
`/fast/scratch/hyaku/kaidoku-r44/R44W2C1Controls/` (deleted before yield).

```bash
S=/fast/scratch/hyaku/kaidoku-r44/R44W2C1Controls
mkdir -p "$S"
git clone --shared --quiet --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel        # -> $S/lane
git -C "$S/lane" archive 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac | tar -x -C "$S/lane"
```

The clone's object store is shared with the lane (read-only); its work tree is materialised from
the admissible measured revision, so the c4 arm's `os.walk` over the heldout envelope set and every
`git show <freeze>:<path>` read the 55bcce69 content. No git mutation touched the lane; the only
commits written were the two arms' own `git clone --shared` sandboxes that `c1-controls.py` creates
under its `--work` (each asserted `rev-parse --show-toplevel == sandbox` by the tool, identity
`r44-c1-controls <controls@r44.invalid>`).

Fixed inputs, verified by hash:

| object | value |
|---|---|
| `tools/round-44/c1-counter.py` | `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993` — **identical** at freeze, at 55bcce69 and at lane tip |
| `tools/round-44/c1-controls.py` | `b8c55f9b9d8af47e56f6bc8c11b21018b7fb1997c4fd399355c045a16aafa402` — identical at freeze and 55bcce69 |
| `--pkg65` | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `package.json` version `6.5.0` |
| python | `/usr/bin/python3` 3.14.8 |
| control fixtures | `c1` and `c4` trees unchanged at `c48f8a4`, `55bcce69` and HEAD (`c86ea508` touched only `c3/` and `pos/`) |

The two runs are the same detector the freeze score used: `c1-controls.py --controls c1,c4` builds
each planted tree, commits it as a descendant of the freeze, then invokes the frozen counter with
the frozen argv. I ran it twice — once rebuilding every fixture from source (`planted_from_committed_fixtures:
false`, the mode the recorded receipts used) and once planting the committed fixture bytes
(`--from-fixtures`). Both are recorded below.

## 2. What the record claims

| source | claim about these arms |
|---|---|
| `plans/round-44-claims.md:168-169` | CTL-C1-1 → "non-zero (**subject/handler/superblock fail**)" |
| `plans/round-44-claims.md:174-175` | CTL-C1-4 → "non-zero because the frozen **provenance/evidence-id** bindings reject their `/kaidoku-r42/` paths" |
| `plans/round-44-claims.md:140-141` | "A pre-freeze envelope relabelled into a round-44 receipt path is rejected by **provenance and evidence-id** bindings" |
| `tools/round-44/c1-controls.py:29`, `:640`, `:675` | "subject digest, handler and superblock all disagree" / "three independent disagreements" |
| `tools/round-44/c1-controls.py:795-797` | c4 note: "the provenance binding refuses an output_directory outside `corpus/evidence/round-44/c1`, and **the evidence id was minted over the old path**" |
| `.ufo/waves/round-44/controls/summary.json` | both arms `as_expected`, `exit_code 1`, `kill_rule_fires false`, `failures []` |

## 3. Reproduction — both arms behave as recorded

Command (exit `0`; driver stdout sha256 `12606cd7…`; wall **16.81 s**; stdout
`{"controls": 2, "failures": [], "kill_rule_fires": false, "unevaluated": []}`):

```bash
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-controls.py \
  --root "$S/lane" --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 \
  --counter tools/round-44/c1-counter.py \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work "$S/work" --out "$S/out" --fixtures-root "$S/fixtures" \
  --controls c1,c4 --json-out "$S/summary.json"
```

| | CTL-C1-1 | CTL-C1-4 |
|---|---|---|
| counter exit | **1** | **1** |
| `carriers_matched` / `met_target` | `0` / `false` | `0` / `false` |
| `frozen_path_changed` | `[]` | `[]` |
| driver verdict | `as_expected` | `as_expected` |
| counter stdout sha256 | `10f16cc73abc1943c1b6f9da5725e0862915757221dd3f129285797a82a1e115` | `bf21013794eb1cb98a57883f9433d635f20813150acf039d56d0998b6c090383` |
| counter wall | 6.770 s | 7.055 s |
| failing (bare) | `gaps_ok, handler_ok, nonregular_unpublished_ok, oracle_hits_ok, projection_ok, run_provenance_ok, subject_pin_ok` (all 4 carriers) | `chunks_ok, gaps_ok, nonregular_unpublished_ok, oracle_hits_ok, projection_ok, run_provenance_ok` |

Semantic equality with the committed receipts (`exit_code`, `carriers_matched`, `met_target`,
`frozen_path_changed`, the bare failing-clause set and the full per-carrier vector):
**c1 `True`, c4 `True`**. Byte equality of `stdout` is *not* expected and does not occur: the
counter's stdout payload carries `revision`, the planted commit id, which differs per sandbox.
`--from-fixtures` reproduces the same semantics again (driver exit `0`, wall 17.14 s, c1 stdout
`ca2df9e22c6d6008…` exit 1, c4 stdout `603ddfbc9e3c328d…` exit 1), so the committed fixture trees
are self-sufficient inputs.

Rebuilt control tree vs frozen blobs — **10/10 files MATCH** at `c48f8a4`, at `55bcce69`, and in
the worktree (`artifacts/R44W2C1Controls/fixture-hashes.txt`). The committed transcript trees
`.ufo/waves/round-44/controls/{c1,c4}/tree/` are byte-identical to those fixtures (`diff -rq`
reports only the fixtures' extra `manifest.json`), so transcript, frozen input and rebuild are the
same bytes. The arms are content-addressed honestly; nothing about their red is a fixture artefact.

## 4. Attribution — what actually fired

Per-carrier clause values read from the counter's own `carriers` map
(`artifacts/R44W2C1Controls/rerun-c1-counter.json`, `…-c4-counter.json`):

### CTL-C1-1 — round-42 v3 receipts at the round-44 paths

| carrier | `subject_pin_ok` | `handler_ok` | `layout_ok` | `chunks_ok` | `run_provenance_ok` | `evidence_id_ok` | `projection_ok` |
|---|---|---|---|---|---|---|---|
| v1le | **false** | **false** | **true** | true | **false** | true | **false** |
| v1be | **false** | **false** | **true** | true | **false** | true | **false** |
| v2le | **false** | **false** | **true** | true | **false** | true | **false** |
| v2be | **false** | **false** | **true** | true | **false** | true | **false** |

The source receipts are genuinely v3 (`squashfs_v3_ddwrt` for `DW-FONERA`/`DW-MEGA`,
`squashfs_v3` for `OW-A8092`/`OW-X86FS`, subject digests `02199832…`, `5d37063e…`, `35f777eb…`,
`12a2fd58…`, all ≠ the v1/v2 pins). Two predicted clauses fire (subject, handler) with five more
(`gaps_ok`, `nonregular_unpublished_ok`, `oracle_hits_ok`, `projection_ok`, `run_provenance_ok`).
**The superblock clause does not fire**: `layout_ok` is `true` on all four carriers.

Cause, read from the frozen counter: `layout_ok` is computed as
`layout_probe(raw, c)` where `raw = git show <rev>:<carrier path>` (`c1-counter.py:2038,2043`; the
docstring at `:123-128` defines it as "the v1/v2 superblock reads the frozen magic…"). The arm
plants only `corpus/evidence/round-44/c1/*/after.json`, never the carrier bytes, so this clause is
unreachable by construction. `--selftest` does exercise it (7 `want_fail='…:layout_ok'` cases; run
below, all green) — the binding is live, it simply is not what this arm tests.

### CTL-C1-4 — pre-freeze committed envelopes relabelled (D1)

| carrier | source envelope (at 55bcce69) | `output_directory` in the envelope | `run_provenance_ok` | `evidence_id_ok` | `subject_pin_ok` | `chunks_ok` | `projection_ok` |
|---|---|---|---|---|---|---|---|
| v1le | `corpus/evidence/round-42/c2/heldout/H41/envelope.json` | `/fast/scratch/hyaku/kaidoku-r42/l1-data/gen/r42-heldout-pu06iz5w/rea-H41/out` | **false** | **true** | true | true | true |
| v1be | `…/H43/envelope.json` | `…/rea-H43/out` | **false** | **true** | true | **false** | **false** |
| v2be | `…/H44/envelope.json` | `…/rea-H44/out` | **false** | **true** | true | **false** | **false** |
| v2le | `…/H45/envelope.json` | `…/rea-H45/out` | **false** | **true** | true | **false** | **false** |

`run_provenance_ok` fires on all four — the `/kaidoku-r42/` path is not the `/kaidoku-r44/` segment
(`c1-counter.py:258` `PROV_SEGMENT`, `:1180`). For **`v1le` this is the only failing clause**, a
clean single-binding attribution. `evidence_id_ok` is **`true` on all four**.

Cause: `evidence_ids()` recomputes the id by running the frozen `xpin-attribute.mjs` over the
envelope's *own* contents (`c1-counter.py:596-640`, applied at `:2128`; docstring `:158-159`:
"stored evidence id == the id recomputed under the frozen rea-agents 6.5.0 rule"). A byte-identical
pre-freeze envelope is self-consistent by definition, so this binding detects tampering, not
provenance. It is exactly the R44-CL3 caveat, now measured on the arm that was supposed to close
it.

## 5. Mutation probes — is each arm load-bearing on the clause it names?

Same detector, same arms, with the smallest behaviour-bearing edit in a **disposable scratch copy**
of the counter. Lane counter sha256 re-checked after both probes:
`9f2cc140…ffea993` (unchanged).

| probe | edit (`artifacts/…/m1.diff`, `m2.diff`) | scored on | counter exit | `carriers_matched` | driver verdict |
|---|---|---|---|---|---|
| **M1** | `d['subject_pin_ok']=True; d['handler_ok']=True` before the match loop | CTL-C1-1 | **1** | **0** | **misbehaved** (driver exit 1) |
| **M2** | `d['run_provenance_ok']=True` before the match loop | CTL-C1-4 | **1** | **1** | **misbehaved** (driver exit 1) |

M1 detail: with both clauses neutered the arm still returns `exit 1`, `carriers_matched 0`,
`met_target false` — the claim's exit-code class is satisfied by `gaps_ok`/`nonregular_unpublished_ok`/
`oracle_hits_ok`/`projection_ok`/`run_provenance_ok` alone. The driver's `failing_any` assertion is
what catches it ("none of ['subject_pin_ok','handler_ok','layout_ok'] fired"). So the arm has
fitness for subject/handler *only through the driver's clause assertion*, never through its exit
code.

M2 detail: neutering `run_provenance_ok` makes `v1le` fully `matched` (`carriers_matched 1`) and
flips the driver to `misbehaved` — proof that the provenance clause is the load-bearing one for the
one carrier that is otherwise clean, and the strongest positive result in this report.

## 6. Numbered defects for L1

**D-1 — CTL-C1-1's stated reason names a clause the arm cannot make false.**
Path:line `plans/round-44-claims.md:169` ("non-zero (subject/handler/superblock fail)"), repeated
at `tools/round-44/c1-controls.py:29`, `:640`, `:675`. Command: §3 CMD-A (c1 arm); also the same
arm's `counter.json`. Exit code `1` (as expected). Observed value: `layout_ok == true` on `v1le`,
`v1be`, `v2le`, `v2be`; `layout_ok` absent from `failing`/`failing_clauses`. Fix for round 45:
correct the sentence to "subject/handler" and drop `layout_ok` from the arm's `expect.failing_any`
(it is a dead alternative), or attribute the superblock witness to CTL-C1-5 / `--selftest` where it
is actually exercised. Not a claim-verdict change.

**D-2 — CTL-C1-4's stated reason names a binding that passes on every carrier.**
Path:line `plans/round-44-claims.md:175` and `:140-141` ("rejected by provenance and evidence-id
bindings"), and `tools/round-44/c1-controls.py:796-797` ("the evidence id was minted over the old
path"). Command: §3 CMD-A (c4 arm). Exit code `1`. Observed value: `evidence_id_ok == true` for
`v1le`, `v1be`, `v2be`, `v2le`; `evidence_id_ok` absent from `failing_clauses`. The D1 mitigation
itself still holds (provenance rejects all four, and alone for `v1le`); what does not exist is the
second mechanism the text asserts. Fix: restate the D1 guarantee as "rejected by the provenance
binding" and record that `evidence_id_ok` validates self-consistency only (fold into R44-CL3).

**D-3 — the c4 arm's note names the wrong provenance predicate.**
Path:line `tools/round-44/c1-controls.py:795-796` ("the provenance binding refuses an
output_directory outside `corpus/evidence/round-44/c1`"). Command: §3 CMD-A (c4 arm). Exit code
`1`. Observed value: the binding that fires is `c1-counter.py:1180`, which requires the literal
`/kaidoku-r44/` segment; `provenance_ok` never inspects any `corpus/` path. This is R44-CL2's
unsatisfiability restated inside a frozen tool's comment — same defect class, second location.
Frozen this round; route to round 45 with D-2.

**D-4 — control fitness: CTL-C1-1's exit code does not test the clauses it is credited with.**
Path:line `plans/round-44-claims.md:169` (the arm's stated purpose) against
`tools/round-44/c1-controls.py:1015-1080` (`failing_any` is the only clause guard). Command: §5
M1. Exit code `1` from the counter, `1` from the driver. Observed value: `carriers_matched 0`
with `subject_pin_ok`/`handler_ok` forced true — i.e. the arm is red for five other reasons and
would not notice a dead subject/handler binding on exit code alone. The driver's `failing_any`
does catch it, so nothing is unsound; but a per-binding fitness case (mutate one binding, expect
that bound name) is the shape the C2 rubric already requires and C1 lacks. Recommendation only.

**O-1 (observation, not a defect) — `per_carrier_failing` mixes clause failures with aggregates.**
`tools/round-44/c1-controls.py:598-602` collects every boolean `false` in the counter's per-carrier
map, so `matched` (the aggregate) and `extract_root_confirmed` (a detail flag) appear beside real
clause names. It does not affect any verdict; it does make `v1le` read as `['matched',
'run_provenance_ok']` where the single clause failure is `run_provenance_ok`.

## 7. What survives — positive confirmations

- Both arms are **red for the reason the record's exit-code contract names**, and neither reaches
  the target: `carriers_matched 0`, `met_target false`, `frozen_path_changed []`.
- The four predicted warts are absent: no control reds via `could-not-evaluate` (exit 2), no
  `frozen_path_changed`, no unexpected `bindings` flip (`bindings_false` identical to the
  committed receipts), and `kill_rule_fires false`.
- CTL-C1-4 does what D1 needed: provenance rejects all four relabelled envelopes, and for `v1le`
  that is provably the sole reason (M2).
- The committed control inputs are honest: 10/10 rebuilt files hash to the frozen blobs, and
  `--from-fixtures` reproduces the same semantics.
- The frozen counter's own `--selftest` is green: exit `0`, `cases 47`, `red_ok 46`, `green_ok 1`,
  `failures []` (wall 6.72 s) — including 7 `layout_ok` mutations and 1 `evidence_id_ok` mutation,
  so D-1/D-2 are misdescriptions, not dead bindings.
- **C1's honest-stop verdict is untouched.** Nothing here bears on the `parameters.output_directory`
  contradiction (R44-CL2) or on the 4/4 publication; the stop remains the reading these arms
  support.

## 8. Hygiene, scope, tooling

- Wrote only `…/w2/R44W2C1Controls.md` and `…/w2/artifacts/R44W2C1Controls/` (plus scratch). No
  claim, counter, rubric, frozen byte, fixture, rubric or production doc was modified; no lane
  path was written. Read-only git only in the lane (`rev-parse`, `log`, `show`, `diff`, `ls-tree`,
  `status`); fixture commits existed solely inside `c1-controls.py`'s own `--work` sandboxes and my
  clone.
- Scratch discipline: one `git clone --shared`, `TMPDIR`/`--work` passed explicitly, everything
  under `/fast/scratch/hyaku/kaidoku-r44/R44W2C1Controls/`, deleted before yield. No `/tmp`
  evidence is cited.
- Tool installs/upgrades: **none** (no pacman, no `uv`, no PATH changes). python 3.14.8,
  `rea-agents 6.5.0` and `/usr/bin/unsquashfs` 4.7.5 were already present.

## 9. Receipts

| id | command (seat R44W2C1Controls) | exit | stdout sha256 | wall |
|---|---|---|---|---|
| A | `c1-controls.py … --controls c1,c4` (§3) | **0** | `12606cd714dff1a19f2f71df785a2a4a18d82d268902d459f0fda7f67285ac99` (driver) | 16.81 s |
| A-c1 | frozen counter, CTL-C1-1 arm | **1** | `10f16cc73abc1943c1b6f9da5725e0862915757221dd3f129285797a82a1e115` | 6.770 s |
| A-c4 | frozen counter, CTL-C1-4 arm | **1** | `bf21013794eb1cb98a57883f9433d635f20813150acf039d56d0998b6c090383` | 7.055 s |
| B | same, `--from-fixtures` | **0** | `12606cd714dff1a19f2f71df785a2a4a18d82d268902d459f0fda7f67285ac99` (driver) | 17.14 s |
| C | M1 mutant on CTL-C1-1 | **1** (driver detects) | `6a10784f2b017402fedef87ec41e734f698df6d954b06acb4fbcf17da0d4a824` | 7.376 s |
| D | M2 mutant on CTL-C1-4 | **1** (driver detects) | `f77714439be15f9fac6dcc8e55e72f0ed19e1204d3476e8cc87b055acbdf025b` | 7.238 s |
| E | `c1-counter.py --selftest` | **0** | `fbe23fefc21c12358232a8146947a3da39e96fc1d359fa9f61ec36178310da1c` (artifact sha) | 6.72 s |

Artifacts: `artifacts/R44W2C1Controls/` — `rerun-{summary,c1-receipt,c1-counter,c4-receipt,c4-counter}.json`,
`ff-*`, `m1-*`, `m2-*`, `selftest.json`, `fixture-hashes.txt`, driver stdout/stderr, and
`SHA256SUMS.txt` over the lot.

Probe verdicts in UFO terms: **M1 survived** (neutering subject/handler leaves exit 1 /
`carriers_matched 0`; only the driver's clause assertion kills it) — a coverage finding about the
arm's exit-code class, not permission to change the contract. **M2 killed** (neutering provenance
lets `v1le` match, so the clause is load-bearing). Pristine bytes restored: lane counter
`9f2cc140…` before and after; the mutated copies were throwaway.
