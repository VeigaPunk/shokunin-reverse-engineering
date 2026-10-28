# R44W2SentEnvelope — path-handling attack on the frozen round-44 counters

Seat: `R44W2SentEnvelope` (wave 2, falsification). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`; admissible measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; base `c29360e3ba5381a5ab69e372d0d9577970f85018`; lane tip at
dispatch `8bb1090a`. Counter bytes are identical at freeze, measured revision and tip
(`c1-counter.py` sha256 `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993`,
`c2-counter.py` sha256 `085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277`).

Method: one `git clone --shared` of the lane into
`/fast/scratch/hyaku/kaidoku-r44/R44W2SentEnvelope/lane`, detached at 55bcce69
(`git -C` toplevel asserted before every mutation). The frozen counters were imported as
modules and driven through their own functions, and run end to end on clone commits that carry
only mutated receipts / manifests / fixtures. The lane was not written to; the clone commits are
clone-local and are deleted with the scratch tree. `repro.md` beside this file is the rebuild
recipe. No tool was installed or upgraded (nothing was needed).

## Verdict on the assigned attacks

| # | attack | result | binding that decides it |
|---|---|---|---|
| 1 | `output_directory` with `..` traversal that still contains the segment | **REJECTED** | `provenance_ok` (`c1-counter.py:1182`) rejects any exact `..` component; `path_shape_problem` (`:1209`) also rejects it for every normalised receipt path. Full counter at clone rev `84060c25`: exit 1, `carriers_matched 3`, `failing ['v1le:run_provenance_ok']`. |
| 2 | path that is a symlink out of the tree | **ACCEPTED** | `provenance_ok` is purely lexical (no `realpath`, no `lstat`, no existence test). A path under a symlink `kaidoku-r44 -> /etc` returns true; `os.path.realpath` = `/etc/shadow`. With the evidence id re-minted the whole carrier passes (D-2). |
| 3a | manifest entry pointing at an absolute path outside the evidence root | **NOT EVALUATED — unbound** | No clause in `c1-counter.py` opens `corpus/evidence/round-44/c1/manifest.json`, `provenance.json`, `run.json`, `extract-tree.tsv` or `stdout.log`. A clone commit that rewrites every manifest path to `/etc/passwd`, `/etc/shadow`, `/home/operator/...` produces a counter result identical to the baseline (D-4). |
| 3b | carrier-table path / oracle row pointing at an absolute path outside the tree | **REJECTED** (fails closed) | `parse_rel_path` (`:718`) rejects absolute and `..`; `carriers_spec` (`:865`) reports `carrier 'h1' path: absolute path '/etc/passwd'`; `oracle_rows`/`output_tree_binding` reject absolute roots; `git show`/`ls-tree` return empty. Exit is **1**, not 2 (D-6). |
| 4 | evidence id recomputed over a different path | **REJECTED when the id is minted over a different path; ACCEPTED when it is minted over the receipt's own (arbitrary) path** | The 6.5.0 `semanticProjection` includes `parameters` wholesale, so the id binds the exact string (`xpin-attribute.mjs` over `rea-agents@6.5.0`). Id minted over `/kaidoku-r44/a-different-run/out` while the receipt says `/kaidoku-r44/other-run/out`: clone rev `d950a586`, exit 1, `carriers_matched 3`, `failing ['v1le:evidence_id_ok']`. Id minted over the receipt's own `/etc/kaidoku-r44/<id>/out`: accepted (D-1). |

The round-43 routed weakness is **not closed**: the lexical `..` case is, but the
substring/symlink/no-realpath surface is intact, and it is the only thing the word
"provenance" in the predicate is backed by.

## Findings

### D-1 (P1, open) `run_provenance_ok` accepts any absolute path that contains `/kaidoku-r44/`

`tools/round-44/c1-counter.py:1176-1182`:

```python
def provenance_ok(output_directory):
    if not isinstance(output_directory, str) or not os.path.isabs(output_directory):
        return False
    if PROV_SEGMENT not in output_directory:      # PROV_SEGMENT = '/kaidoku-r44/'
        return False
    return '..' not in output_directory.split('/')
```

A substring test on an unvalidated string: it is not segment-bounded, does not canonicalise, and
does not require the path to be inside this round's scratch root (or to exist). `receipt_paths`
(`:1232-1264`) does not include `parameters.output_directory`, so `path_shape_ok` never sees it
(`:1967`, measured true for every accepted case below).

Exploit path (measured, not theoretical):

1. take any real REA envelope for the frozen carrier (the four committed receipts are real);
2. set `parameters.output_directory` to an arbitrary absolute string containing `/kaidoku-r44/` —
   `/etc/kaidoku-r44/<id>/out` is enough;
3. re-mint `evidence_id` with the frozen `tools/round-27/xpin-attribute.mjs` (the counter's own
   `evidence_ids()`, `:596`) — one line, no REA run;
4. commit under `corpus/evidence/round-44/c1/<id>/after.json` in a post-freeze commit.

Evidence:

- `/fast/scratch/.../out/c1-receipt-mutation.json` — full frozen counter at clone rev
  `7cebb772ed26273b4334fb4f21b6a9d161dda7ae`: `carriers_matched 4`, `failing []`,
  per carrier `output_directory = /etc/kaidoku-r44/<id>/out`, `run_provenance_ok true`,
  `evidence_id_ok true`, `projection_ok true`; exit 1 only because the three documentation
  bindings are false at 55bcce69 (`province_core_section`, `province_core_row`, `frontier_note`).
- `c1-devarm-accepted.json` — frozen counter `--dev-arm` over the same four envelopes: exit **0**,
  `dev_matched 4`, `scored 4`, `failing []`.
- `attack.json` (path matrix): `/etc/kaidoku-r44/out`, `/tmp/kaidoku-r44/x`, `/kaidoku-r44/x`,
  `//etc/kaidoku-r44/x` all `provenance_ok true`, `path_shape_problem null`.
- `attack.json` (`real_receipt_clauses`): the four committed receipts are already the scratch
  form, all `run_provenance_ok true`; the named tree
  `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/` **no longer exists** (`ls` exit 2), so the
  accepted provenance string names nothing on disk and the counter cannot tell.

Impact: `run_provenance_ok` is the clause the claim uses to say a receipt came from this round's
scratch run. It says only "the receipt's own string contains a segment". Combined with
`evidence_id_ok` (which binds the exact same string) the pair is internally consistent and
externally anchorless. At `4cc1ac11` the instrument reported `met_target true` with these
scratch-form receipts; the only thing that stopped the promotion was the claim text, not the
instrument. A future round that lands the row *and* a re-pathed receipt scores exit 0.

Smallest remediation: replace the substring test with segment-bounded containment
(`under_root`, `:1279`, already in the file) against the round's scratch root
(`$HYAKU_SCRATCH/kaidoku-r44/<seat>/<run>/`), require `os.path.realpath(output_directory)` to be
that directory and to exist as a directory, and derive `trusted_run_root` from the validated
root rather than `dirname` (D-2).

### D-2 (P2, open) provenance and the trusted root are lexical: a symlink escapes both

`tools/round-44/c1-counter.py:1176-1194`. Measured (`attack.json`):
`/fast/scratch/hyaku/kaidoku-r44/R44W2SentEnvelope/sym/kaidoku-r44/shadow` where
`sym/kaidoku-r44 -> /etc` gives `provenance_ok true`, `trusted_run_root` =
`…/sym/kaidoku-r44`, `realpath` = `/etc/shadow`. `trusted_run_root` also returns a parent for a
string that fails provenance: `output_directory = /fast/scratch/hyaku/kaidoku-r44` →
`trusted_run_root = /fast/scratch/hyaku` (the segment's parent). `diagnostic_rel` (`:1326`) then
calls `under_root(link, trusted)` lexically, so a removal diagnostic is trusted under an
arbitrary, unvalidated parent.

Impact today: `make_real_runner` (`:1859`) builds its own `outdir` and ignores
`parameters.output_directory`, so there is **no filesystem write sink in the counter**; this is a
provenance-integrity defect, not an arbitrary-write one. Escalation risk: any consumer that
honours the committed field (the `c1-run.sh` copy-back convention in the claims, a round-45
counter, an operator re-running from the receipt) inherits the traversal.

Smallest remediation: same change as D-1 — canonicalise and require containment; use
`os.path.realpath` equality on every component, and reject a `trusted_run_root` whose realpath
is not the validated run root.

### D-3 (P2, latent) `diagnostic_rel` accepts `..` inside a removal diagnostic's link

`tools/round-44/c1-counter.py:1326-1358`: the link is only required to be lexically under
`trusted_run_root`, then the root segment is searched from the end; the `..` component is never
rejected. Measured (`attack.json`, `diagnostic_rel`): link
`<trusted>/../firmware.bin_extract/link` resolves to rel `"link"`, identical to the in-tree
`<trusted>/firmware.bin_extract/link`.

Impact: for a carrier with non-regular members, a `MaliciousSymlinkRemoved` diagnostic that did
not occur inside the run's output tree satisfies the removal gate for the in-tree entry. The four
frozen carriers have zero non-regular members and `GAP_RULE` requires the rel to match a frozen
non-regular row, so no score this round is affected; it matters for the first v1/v2 carrier with
a symlink (the claim already discloses that no such carrier is exercised).

Smallest remediation: run `report.link` through `path_shape_problem` (`:1209`) and drop the
diagnostic when it returns a problem.

### D-4 (P2, open) the committed run manifest is not bound by any clause

`corpus/evidence/round-44/c1/manifest.json` records `command`, `exit_code`,
`output_directory`, `receipt`, `stdout_sha256`, `extract_tree`, `run_json` per carrier. No clause
reads it (`grep -n manifest tools/round-44/c1-counter.py` → no match; same for c2).

Measured: clone rev `8e23ba19896cb8fef60802ab46d73f18c0e58a37` rewrites every carrier's
`output_directory` → `/etc/passwd`, `outdir` → `/etc/kaidoku-r44/out`, `receipt` → `/etc/shadow`,
`fixture` → `/home/operator/fixtures/<id>.bin`. Counter output is identical to the 55bcce69
baseline: exit 1, `carriers_matched 4`, `failing []`, same three false documentation bindings
(`c1-manifest-mutation.json`). The answer to attack 3a is therefore "neither rejected nor
accepted — ignored": a manifest may assert any absolute path and the score does not move.

Impact: the manifest is the only committed artefact that claims *how* the run was made, and it is
decorative for the verdict. `receipt_identity_ok` (`--verify-receipt`) binds the counter file to
its own receipt, not the evidence manifest.

Smallest remediation: bind the manifest entry to its receipt (same `output_directory`, same
`receipt` path, same `stdout_sha256`; the receipt's `parameters.output_directory` must equal the
manifest's) and require every path field to pass `parse_rel_path`; or remove the manifest from
the evidence tree so it cannot be read as a binding.

### D-5 (P2, open) `oracle.tool` is an absolute path from the frozen table that the counter executes

`tools/round-44/c1-counter.py:2222-2253`: `detail['path'] = tool`; `file_sha256(tool)`;
`subprocess.run([tool, '-version'])`. The digest is only compared **if** the table carries
`sha256`/`tool_sha256` (`:2236-2240`), and the execution only happens if it carries `version`
(`:2243`).

Measured (`attack2.json`, `oracle_tool`): a frozen table
`{"oracle": {"tool": "<scratch>/evil-oracle.sh"}}` (no digest, no version) returns
`ok: true` with no execution; adding `"version": "evil version"` executes the binary
(marker file written, `version_line "evil version 9.9"`) and still returns `ok: true`; with a
digest pinned to other bytes it executes and returns `ok: false`.

Impact: carriers.json is the frozen trust anchor, so this is not remote code execution — but a
mistaken or hostile pre-freeze table turns every scoring run into execution of an arbitrary
absolute path, and the "no digest means advisory" default makes the binding vacuously true. The
same class of table error is what M44-2 shows the lane does commit.

Smallest remediation: require a 64-hex digest whenever `oracle.tool` is present (exit 2
otherwise), require the resolved path to be under `FIXED_PATH` (or one of the frozen
`toolchain.*` paths), and never execute a path the table did not also digest.

### D-6 (P3, open) a malformed frozen carrier table reds as exit 1, not exit 2

`tools/round-44/c1-counter.py:865-…` collects `carriers_spec_problems`; `:2190` turns them into
`carriers_spec_ok false`; `:2216` makes `met_target false`; `main` returns 1. Measured with a
hostile entry (`attack.json`, `carrier_table_absolute_path`): 44 problems including
`carrier 'h1' path: absolute path '/etc/passwd'`, while `frozen_tables_valid` stays true.

Impact: a freeze-time instrument error is recorded as "the claim failed" instead of "the claim
could not be evaluated". The round's exit-code discipline (0 met, 1 red, 2 could-not-evaluate; a
2 never counts toward a target) is what distinguishes these, and a caller that reads exit 1 will
count the round as a measured red rather than an unevaluable instrument.

Smallest remediation: raise `Unevaluable` (exit 2) on any non-empty `carriers_spec_problems`,
`gap_rule_problems` or `rule_probs`.

### D-7 (P3, open) c2 rubric path fields accept absolute and `..` spellings

`tools/round-44/c2-counter.py:425-445` (`add_frozen`) takes rubric-declared paths verbatim. Measured
(`attack2.json`, `c2_rubric_paths`): `parse_rubric` returns `malformed: null` for
`frozen_paths: ['/etc/passwd']`, `frozen_paths: ['../../outside']`,
`expected_edits: {'/etc/passwd': …}`, entry `expected_edit.file: '/etc/passwd'`, entry
`file: '/etc/passwd'` / `'../../etc/passwd'`, `script.path: '/etc/passwd'`, and
`frozen_dirs: ['/']` / `['../../etc']`.

Every subsequent read goes through git (`show`, `ls-tree`, `git archive`), so the reads fail
closed (measured: `show(root, rev, '/etc/passwd')` empty, `tree_entries` empty), and
`freeze_integrity` (`:595`) records an unknown path as `absent_at_freeze` rather than as a rubric
error. `check_script_paths` (`:865-884`) additionally does `path = token.lstrip('./')`, so an
absolute token is recorded as a repo-relative path.

Impact: no false pass observed this round, but the rubric is the C2 trust root and it will accept
a path that can never be checked, silently, instead of exit 2. It also means "the rubric cannot
be authored to name a wrong value" (claim B2) is enforced for the *asserted string*, not for the
*file* it names.

Smallest remediation: pass every rubric-declared path through the `parse_rel_path` rule and
return `rubric_malformed` on absolute/`..`/trailing-slash; drop the `lstrip`.

### D-8 (P2, open) `frozen-path-preflight.py` false-reds by default and its frozen set is caller-supplied

`tools/round-45/frozen-path-preflight.py:29-30` documents `--pathspec` as "Default: none (tree
backstop only)", but `:47-67` runs `git log --name-status` with no pathspec and counts **every**
status as a violation.

Measured (all in `artifacts/`, exit codes captured directly):

| rev | pathspec | exit | observed |
|---|---|---|---|
| `c48f8a4` (freeze) | `tools/round-44` | 0 | clean |
| `55bcce69` | `tools/round-44` | 0 | clean |
| `c86ea508` | `tools/round-44` | 1 | `touched 8`, `blob_changed 8`, exactly the counters' `frozen_path_changed` list |
| `8bb1090a` (tip) | `tools/round-44` | 1 | same 8 paths |
| `55bcce69` | none | **1** | `touched 110`, `blob_changed 0` → false red |
| `a16b3cfa` (post-freeze byte change to `plans/round-44-claims.md`) | `tools/round-44` | **0** | clean — the gate does not see the pinned claim file |
| `a16b3cfa` | `plans/round-44-claims.md` | 1 | red, status `M` |

It also catches a *post-freeze addition* under a frozen directory: a fixture repo
(`git init` at `/fast/scratch/.../fixture-preflight`, toplevel asserted) with a post-freeze
`tools/round-44/b.py` → exit 1, `touched [{status: 'A', path: 'tools/round-44/b.py'}]`.

So: "does the fix really catch M44-2?" — **yes, when invoked with the frozen pathspec**: it
reproduces the counters' 8-path list and exit 1, and it catches the added-file variant that the
counters' `A`-only-if-existed-at-freeze rule would not. "Does it close the class?" — **no**: the
freeze set is not derived from the claim, so a caller who passes the paths it happens to
remember gets a green for a post-freeze rewrite of the pinned claim file. This is the same
hard-coded-set defect recorded as R44-CL7 for the c2 counter, one tool over.

Smallest remediation: make `--pathspec` required (exit 2 when absent) or derive it from the
claim's freeze rule, and correct the help text so the default is not described as a tree-only
backstop.

## The claims and the record

### R44-C1 — verdict confirmed; the record says exactly it

Independent run of the frozen counter at `55bcce69` (`c1-at-55bcce69.json`, 7.53 s):

```
exit_code 1 · carriers_matched 4 · target 4 · met_target false · carriers_unchanged true
frozen_path_changed [] · failing [] · bindings_false
  ["province_core_section", "province_core_row", "frontier_note"]
per carrier: run_provenance_ok true, evidence_id_ok true, projection_ok true, matched true
```

So every carrier clause is true and the only false bindings are the three withdrawn documentation
bindings. That is exactly what `LOG.md:3201` and `SCORECARD.md:3525` state (same numbers, same
three names), and the lesson's `R44-CL2` qualifier (`corpus/lessons/round-44.md:66-78`) already
records that "its red at `55bcce69` is the three withdrawn documentation bindings, not
provenance; the score was withdrawn under the claim text rather than rejected by the counter".
Confirmed — the record is honest on the instrument, and the stop is the only admissible
reading *of the frozen claim text*: the receipts satisfy the scratch arm and cannot satisfy the
"committed `corpus/evidence/round-44/c1/` path" arm as an output directory inside the lane.

Two precision notes, neither changing the verdict:

- *(G-1, P3)* The record's "internally unsatisfiable on one field" is too strong as literal
  prose: one string can contain both literals.
  `/fast/scratch/hyaku/kaidoku-r44/x/corpus/evidence/round-44/c1/v1le` contains
  `/kaidoku-r44/` and `corpus/evidence/round-44/c1/`, and `provenance_ok` returns **true**
  (measured). The lesson's own next sentence ("a loophole, not a legitimate route") states the
  accurate version, so the record is not wrong overall — but the first sentence should not be
  quoted without the qualifier.
- *(G-2, P3)* The four committed receipts name
  `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.<id>.1342995/rea-out`; that directory
  is gone (`ls` exit 2). The counter accepts a non-existent provenance path (D-1), and neither
  the entry status line nor the LOG row says the named tree was reaped. R44-REAP is routed for
  scratch-path citations generally; the C1 provenance claim is the sharpest instance and is not
  tied to it.

### R44-C2 — verdict confirmed

Frozen counter at `55bcce69` (`c2-at-55bcce69.json`, 4.40 s): `exit_code 0`,
`entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, `met_target true`,
`claim_score true`, `rubric_sha256 e8cc0ded…`, counter sha unchanged from freeze. Matches
`LOG.md:3202` and `SCORECARD.md:3526`. Rubric path handling is D-7; `extract_tar`
(`c2-counter.py:751-786`) is **hardened**: over a real `git archive` of a fixture carrying
`/etc/passwd` and `../../outside` symlinks it skipped both, created the in-tree link, wrote one
regular file, and wrote nothing outside the destination.

### M44-2 — verdict confirmed, fix is real but partial

Both counters exit 2 at `8bb1090a` (measured: c1 `frozen_path_changed` = the 8
`tools/round-44/control-fixtures/` paths; c2 exits 2 with `entries_evaluated 0`), so the
admissible revision really is `55bcce69` and the round's choice to measure there is correct. The
preflight catches it with the right pathspec (D-8 table) and catches the added-file variant; its
default mode and its caller-supplied freeze set are the remaining gaps.

## What stayed closed (positive results)

- `..` traversal in `output_directory`, in every normalised receipt path, in oracle member rows
  and in `output_tree` roots: rejected (`provenance_ok`, `path_shape_problem`, `parse_rel_path`).
- Evidence id not minted over the receipt's own `output_directory`: rejected
  (`failing ['v1le:evidence_id_ok']`, exit 1).
- Carrier table absolute/dotdot paths: rejected (fail-closed through git and through
  `parse_rel_path`), though as exit 1 (D-6).
- c2 `extract_tar`: absolute and escaping symlinks and dotdot members skipped; no escape write.
- No filesystem write path from `parameters.output_directory` into the counter or the REA child
  (`make_real_runner` ignores the field and builds its own outdir under `--work`).

## Limits

- The four attacks are measured on the four frozen carriers and on receipt-shaped envelopes; no
  live adversarial REA run was attempted (the counter-time rerun compares the projection, and the
  projection is path-independent, so it neither detects nor is detected by these changes).
- The C2 counter was scored (80/80, exit 0) and its rubric/freeze/extract helpers were driven
  directly; the 80 individual check commands were not mutated, so vacuity/free-pass of the 80
  entries is left to the C2 seats.
- Clone revisions cited (`7cebb772`, `84060c25`, `d950a586`, `a16b3cfa`, `8e23ba19`) exist only in
  the deleted scratch clone; `repro.md` + the copied receipt bytes are the reproducible form.
- `unblob`, `npx rea-agents@6.5.0`, `node` and `/usr/bin/unsquashfs` were already present; no
  install or upgrade was performed (pacman is paused host-wide; nothing required it).

## Artifacts

`artifacts/R44W2SentEnvelope/` — `c1-at-55bcce69.{json,stdout}`,
`c1-manifest-mutation.json`, `c1-receipt-mutation.json`, `c1-traversal.json`,
`c1-idmismatch.json`, `c1-devarm-accepted.json`, `c1-tip.stdout`,
`c2-at-55bcce69.json`, `c2-tip.stdout`, `attack.json`, `attack2.json`,
`preflight-*.json`, `mutated-receipts/accepted_absolute_outside/`, `receipts.json` (per-run
command, exit code, stdout sha256, wall time), `repro.md`.
