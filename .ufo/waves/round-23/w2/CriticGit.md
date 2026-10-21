# CriticGit — R23-C1 Git/loading/preservation falsification

Seat: `KaidokuR23.CriticGit` (source review only; not a Run* seat — no counter, selftest, verify, build or lint executed).
Candidate `C=2838351450ff1ee4baa620c962a1153450d53311` (tree `a02f35c79bba77c63173d44ee19038823621319d`), baseline `B=aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
All bytes read via `git show C:PATH`; copies under ignored `.ufo/waves/round-23/runtime/CriticGit/`.

Reviewed blobs (sha256 of `git show C:PATH`):

| path | sha256 |
|---|---|
| `.ufo/waves/round-23/tools/count-c1.py` | `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2` |
| `.ufo/waves/round-23/verify.py` | `59833006e860631b8d4d6f381056744595769308b377072ceacc116781a4a21a` |
| `.ufo/waves/round-23/tools/counter-fixtures.py` | `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f` |
| `.ufo/waves/round-23/frozen/expected-v2.json` | `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f` |
| `.ufo/waves/round-22/tools/count-c1.py` (legacy, = B) | `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` |
| `.ufo/waves/round-21/tools/verb-coverage.py` | `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b` |
| `.ufo/waves/round-20/tools/verb-coverage.py` | `cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f` |

## Verdict

None of the attacks I tried produces a false count of 4 at C. The checks on revision resolution, the old evidence root, the catalog and the old SOURCES rows all held. I found one real defect that could let a future revision count something it should not (F1), two provenance/binding gaps in how the count is attributed (F2, F3), one config-trust gap (F4), and several low-severity items. The count at C is **inferred** to be 4/6 from the unchanged read set; it was **not verified at C**, because every committed verify record is stamped `6615aea…`.

## Findings

### F1 — Symlink (mode 120000) blobs accepted as knowledge entries and as Evidence files (fixable defect; observed in source)
- `count-c1.py:94` lists entries with `ls-tree -r --name-only` and applies no mode filter. `count-c1.py:118` reads each cited path with `git show C:path`, whatever its mode.
- For a symlink entry, `git show rev:path` prints the stored link-target bytes. Git does not limit their size or content. So someone could commit a mode-120000 entry `.ufo/waves/round-23/evidence/c1/x.json` whose "target" is a complete `ok:true` envelope. The binder would accept it, even though the worktree has only a dangling link and no retained Evidence file. The same trick works for a `corpus/knowledge/*.md` symlink whose target text starts with `source: S0xx`.
- The legacy authority rejects both: `r20 verb-coverage.py:77-91` (`tree_entries` keeps only `blob` with mode `100644`/`100755`), which `r22 count-c1.py:131,153-154` uses through `path in paths`. R23 has dropped that restriction, so two authorities now disagree on what counts as a "retained file".
- At C this is not exploited (observed): `git ls-tree -r C -- corpus/knowledge .ufo/waves/round-2{2,3}/evidence` has no non-`100644` entries other than `connect-dart-symbols/preflight_dart_carrier.py` (100755), which is not JSON and not cited as Evidence.
- Axes: coverage (possible false held count at future revisions), provenance.
- Smallest correction: build the knowledge and evidence path sets from `r20.tree_entries(root, rev)`, as R22 does. Require `entry in regular_paths` and `evidence_path in regular_paths` before calling `git show`. That also fixes F6.

### F2 — The counting command's code is not bound to `--rev` (fixable defect; observed in source)
- The claims `counting_command` is `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <LANE> --rev <REV>`, which runs the counter from the worktree as it is at run time. `measure()` pins the legacy counter and the helpers to C's blobs (`count-c1.py:61-63`; `r22:59-61`), but never compares its own bytes with `git show REV:.ufo/waves/round-23/tools/count-c1.py`.
- The output JSON (`count-c1.py:127-133`) has no counter digest. So a result labelled `"rev": C` could come from any counter code.
- `verify.py` partly makes up for this: it runs the counter from a clone checkout of rev (`verify.py:55-59`) and writes `source-pins.json`. But it only records the pins and never compares them with blob digests.
- Observed: the committed pins equal C's blob digests for all six pinned files (count-c1 `f4b8d16a…`, fixtures `f2990b35…`, expected-v2 `458b30d5…`).
- Axes: provenance/identity.
- Smallest correction: emit `counter_sha256` (from `Path(__file__).read_bytes()`) and fail with exit 2 unless it equals `sha256(git show rev:<counter path>)`. Alternatively, add a pinned `COUNTER_SHA256` to the claims.

### F3 — No committed record at the named commit; census output carries a false `source_rev` (provenance gap; observed)
- Every file in `verify/initial/*.json` carries `source_rev = 6615aeae642aec36959180e7ea940b2794c7f1cb`, including `after-c1.json`, whose stdout `"rev"` is `6615aea…` with count 4. C itself adds those records plus changes to `LOG.md`, `SCORECARD.md` and `corpus/lessons/round-23.md`.
- `git diff --quiet 6615aea C -- corpus/knowledge corpus/SOURCES.md corpus/README.md .ufo/waves/round-2{0,1,2} .ufo/waves/round-23/{evidence,tools,frozen,verify.py}` exited 0. The counter's whole read set is therefore unchanged, so 4/6 at C is a deterministic **[INFERENCE]**, not a measurement. Under the goal's "count verified only at named commit" rule, C is unverified until a Run* seat runs it.
- `verify.py:110` runs `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` against the live worktree (stdout names `…/kaidoku-shokunin/corpus/SOURCES.md`), with no pinned `--today`. Yet `record()` (`verify.py:46`) stamps `'source_rev': rev` on that output. This is false provenance: the census measures the worktree on the day it runs, not rev.
- Observed now: the worktree HEAD is C, and `git diff --quiet C -- corpus/SOURCES.md` exited 0, so the census input currently matches C. That is incidental, not a binding.
- Axes: provenance, calibration.
- Smallest correction: run the census on `--file <clone>/corpus/SOURCES.md` from the rev clone with a pinned `--today`, or label its record `source: worktree`.

### F4 — The GIT_* scrub leaves global and system git config trusted (tradeoff/hardening; [INFERENCE] about the effect)
- `count-c1.py:150-153`, `verify.py:20-23` and `r22:190-193` all delete every `GIT_*` variable and then set `GIT_NO_REPLACE_OBJECTS=1`. This does neutralise replacement refs, including `core.useReplaceRefs` in local config.
- Grafts change parent links only, so they cannot change `rev:path` content. Alternates are content-addressed. `git show <blob>` applies neither textconv (only on an explicit `--textconv`) nor filters.
- The full-hex `BASELINE`/`rev` takes precedence over any same-named ref; git only prints an ambiguity warning.
- The read-only counter path is therefore sound. What remains exposed (`~/.gitconfig`/`/etc/gitconfig` honored; not read, per the contract against reading HOME config):
  - `core.hooksPath` would run `post-checkout` during `verify.py:56` and `counter-fixtures.py:32,35`, and `pre-commit`/`commit-msg` during `counter-fixtures.py:103`.
  - Global `core.attributesFile`, `filter.*` or `core.autocrlf` could make the checked-out code that `verify.py` executes (`verify.py:58-59,68-72`) differ from the reviewed blobs. C's tree has no `.gitattributes` (observed), so only global config could cause this.
  - `commit.gpgSign` could break the fixture commits, which fails closed.
- Axes: identity of executed code in `verify.py`; selftest determinism.
- Smallest correction: after the scrub, set `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`, and pass `-c core.hooksPath=/dev/null` to clone/checkout/commit. Alternatively, have `verify.py` assert that `sha256(checked-out file) == sha256(git show rev:file)` for every file it executes.

### F5 — Inherited R22 witnesses are measured only at B (design tradeoff; observed in source; not exploited at C)
- `count-c1.py:81-83,91-92` takes the historical identify witness from `r22.measure(root, BASELINE)`.
- At rev, only three things are checked: the old-root tree OID (`:66-68`, exact tree identity, strong), the catalog bytes (`:64-65`), and the SOURCES row prefix (`:69-73`). The knowledge entries that bind those witnesses are **not** checked at rev.
- Counterexample: a rev that deletes or rewrites `corpus/knowledge/2026-10-21-r22-flutter-*.md` would still count identify-flutter-build. That is the "inherited identify lost" falsifier in the opposite direction: the knowledge is lost but the credit is kept. The selftest's `inherited_lost` case only deletes an old-root evidence file (`counter-fixtures.py:95-96`), which the tree-OID check catches.
- At C: `git diff --name-status B C -- corpus/knowledge` shows only two `A` rows (r23 entries), with no D/M. `verify.py:68` also runs `r22-c1` at rev and expects 1. So C is safe, but only through an outside control.
- Smallest correction: in `measure`, require that `r22.measure(root, rev)` still binds each historical `[eid, path]`, or that every knowledge blob citing them is byte-identical between B and rev.

### F6 — `ls-tree` without `-z`/`--full-tree` (low; fails closed)
- `count-c1.py:94`: core.quotePath quoting of unusual names, or a gitlink, makes `git show` fail with `git_input_unreadable`, so the counter exits 2. That is denial of service, not a false count.
- If `--root` is a subdirectory of the repo, the pathspec is interpreted relative to the current directory while `rev:path` is resolved from the top of the tree. Fewer entries are counted, which gives only a false negative. F1's correction removes both issues.

### Attacks that failed (observed)
- **Single revision resolution:**
  - `count-c1.py:60` resolves once with `rev-parse --verify --end-of-options REV^{commit}`, and every later read uses that SHA or the literal 40-hex `BASELINE`.
  - The helpers re-resolve the same full SHA (`r20:69-74` enforces hex).
  - `verify.py:35` resolves once and passes the SHA to its children.
  - No `HEAD`- or worktree-relative read occurs in the count path.
- **Pyc versus reviewed code:**
  - `-B` only stops pyc writes. The R23 counter (`count-c1.py:36-40`), the selftest fixtures and `verify.py:74-75` all use `exec(compile(read_bytes))`, so no pyc is ever consulted.
  - The only pyc-capable loads are `importlib` `SourceFileLoader` in `r22:43-47` and `r21:104-109`. Both read helpers written into a fresh `mkdtemp` (0700, random name) under `tempfile.tempdir=<root>/.ufo/waves/round-23/runtime` (`count-c1.py:76`), so no `__pycache__` can exist beforehand. Modules are not entered into `sys.modules`, so the r20 globals that `r22.measure` patches do not leak into the second `revision_helpers` call.
  - C's tree contains no `__pycache__`/`.pyc` files, and `/runtime/` is gitignored (`.ufo/waves/round-23/.gitignore`).
- **Fixed catalog / old root / source rows:**
  - The catalog blob is byte-compared with B.
  - The old root is compared by tree OID, so injected or removed files fail.
  - The legacy counter at C equals B (`git diff --quiet B C -- .ufo/waves/round-2{0,1,2}` exited 0).
  - Old SOURCES rows are a prefix of the rows at C. Because the preservation regex and the 13-cell eligibility parser differ, a new row could be placed anywhere, but an old row cannot be altered without either breaking the prefix or raising `duplicate_source_id`.
  - LOG/SCORECARD/SKILL/PROVINCE are byte-prefix-preserved B→C (observed; byte lengths 169587→174342, 201535→204073, 89430→94184, 28387→29789).

### Low / hygiene
- Check-then-use races (TOCTOU) in two places. `selftest` hashes `counter-fixtures.py` (`count-c1.py:142-145`) and then re-reads it in `load`. `verify.py:90` hashes the counter after executing it. Hashing and executing the same in-memory bytes would close both.
- `corpus/README.md` is not prefix-preserved B→C. Besides inserting rows, C deletes the three blank lines after `## Knowledge`, `## Lessons` and `## Frontier`. No row changed and the counter does not read README, but README is in the claims `read_set`.
- `verify.py:55-56` uses `check=True` on clone/checkout without catching the error. A git failure would surface as a Python traceback with exit 1, not the documented exit 2.

## Produced files and hashes
- `.ufo/waves/round-23/w2/CriticGit.md`: this report (hash in the handoff).
- Scratch copies of blobs (ignored): `.ufo/waves/round-23/runtime/CriticGit/{count-c1.py,verify.py,counter-fixtures.py,r22-count-c1.py,r21-vc.py,r20-vc.py}`. Each is byte-identical to `git show C:…`; digests are in the table above.

## Installs
None.

## Open risks
- 4/6 at C is unverified until a Run* seat executes the counting command at C (F3).
- Hooks, filters or other global git config are unknown (not read); they affect only the `verify.py`/selftest clones (F4).
- F1, F2 and F5 would allow false or unattributable counts at future revisions, not at C.
