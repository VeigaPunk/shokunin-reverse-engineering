**Verdict: CONFIRMED** — every committed R39-C2 held-out envelope H01–H05 re-executes to the same payload, the same triage features and the same frozen-interpreter label; the carriers, tree oracles and manifest entries regenerate byte-identically from the freeze seed `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`, and each `evidence_id` re-derives from its own content, so the artefacts carry live provenance rather than transcribed numbers.

# Seat R39W2HeldReproA — provenance attack on committed held-out envelopes H01–H05

Scope: only `corpus/evidence/round-39/c2/heldout/H01..H05` (the two `clean-be`, the two `clean-le`, one `escaping-symlink-removed` carrier). No lane file outside my report/artifacts was written; no VCS mutation; scratch `/fast/scratch/hyaku/kaidoku-r39/R39W2HeldReproA` removed at exit.

## 1. Result table

| id | class | label (manifest) | fresh label | payload match |
|---|---|---|---|---|
| H01 | clean-be | clean | clean | yes — 7/7 files, 1/1 dir, sha256+size identical |
| H02 | clean-be | clean | clean | yes — 5/5 files, 2/2 dirs identical |
| H03 | clean-le | clean | clean | yes — 5/5 files, 2/2 dirs identical |
| H04 | clean-le | clean | clean | yes — 5/5 files, 1/1 dir identical |
| H05 | escaping-symlink-removed | escaping-symlink-removed | escaping-symlink-removed | yes — 3/3 files, 3/3 dirs identical; the escaping link `b5q0u3of -> ../xx7gcbx` is recorded in `tree.json` and **absent** from the extraction, exactly as the class requires |

All five are `arm: after` (default PATH, `$HOME/.local/bin` present), exit 0, `ok: true`. Carrier sha256 verified against `manifest.json` before every run (`carrier-sha256.txt`).

## 2. Envelope feature comparison (committed vs fresh)

Normalization: output-directory prefix → `$OUT`, `.../rea-firmware-<id>/...` and `.../r39-heldout-<id>/rea-<ID>/out` → `$RUN`, and REA blob ids (`provider_id`, `provider_blob_id`) excluded — those are per-run allocation ids and legitimately differ, so their difference is itself proof the committed envelopes were produced by a separate execution, not copied from mine.

| id | chunk handler / extraction_failed | gap kinds | deps | diagnostics `__typename__` | sasquatch command | symlink removed | files | coverage | equal |
|---|---|---|---|---|---|---|---|---|---|
| H01 | squashfs_v4_be / false | — | — | — | none | no | 7 | complete | yes |
| H02 | squashfs_v4_be / false | — | — | — | none | no | 5 | complete | yes |
| H03 | squashfs_v4_le / false | — | — | — | none | no | 5 | complete | yes |
| H04 | squashfs_v4_le / false | — | — | — | none | no | 5 | complete | yes |
| H05 | squashfs_v4_be / false | — | — | MaliciousSymlinkRemoved (WARNING) | none | yes | 3 | partial | yes |

Whole-`normalized_result` deep diff (committed vs fresh), after path+blob-id normalization: **0 semantic differences for all five** (`cmp2.py` in artifacts). The only raw diffs were the blob ids and the scratch run-directory prefixes. The H05 diagnostic also matches byte-for-byte after prefix normalization, including `link` = `.../firmware.bin_extract/b5q0u3of` and `target` = `.../extracted/xx7gcbx`.

Committed `run.json` claims also hold against my runs: `handlers ["squashfs_v4_be"]` / `["squashfs_v4_le"]`, `gap_kinds []`, `diagnostics []` / `["MaliciousSymlinkRemoved"]`, `files 7/5/5/5/3`, `exit_code 0`, `subject_sha256` equal to the carrier digest.

## 3. Labels from the frozen interpreter

`python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md [--json] <envelope>` on committed and on fresh envelopes produced identical `label` **and identical feature vectors** (`H/G/D/BE/SR/P/commands`) for every id:

```
H01 clean-be                  committed=clean                    fresh=clean
H02 clean-be                  committed=clean                    fresh=clean
H03 clean-le                  committed=clean                    fresh=clean
H04 clean-le                  committed=clean                    fresh=clean
H05 escaping-symlink-removed  committed=escaping-symlink-removed fresh=escaping-symlink-removed
features (all ids): BE="n/a", commands=[], D=[], G=[], H=<handler>, SR=no|yes, P=7/5/5/5/3
```

Rule hit: H01–H04 → rule 8 (`clean`, row `squashfs_v4_*`), H05 → rule 6 (`escaping-symlink-removed`). The interpreter is byte-identical to the freeze commit (`ef4a8a8b…`), and the craft triage table after `<!-- sqfs-triage-table v1 -->` is byte-identical between the freeze `SKILL.md` and HEAD (`f69c0991…`, 3089 bytes), so the post-freeze SKILL edits (round-35/37/38/39 registry section) did not move any label.

## 4. The `-be` question

The committed envelopes record **no** sasquatch command for H01–H05 (`commands: []`, `BE="n/a"`). That is correct behaviour, not missing evidence: unblob 26.6.4's `Command` extractor emits `ExtractCommandFailedReport` (with `command`) only on failure, so a successful extraction leaves no argv in the envelope.

I established the actual child argv independently, by instrumenting the tool (pass-through shim first on PATH + `strace -f -e trace=execve`), both on unblob directly and through the full REA CLI:

| id | child argv (argv[1:]) |
|---|---|
| H01 | `sasquatch-v4be -be -no-exit-code -f -d <outdir> <inpath>` |
| H02 | `sasquatch-v4be -be -no-exit-code -f -d <outdir> <inpath>` |
| H05 | `sasquatch-v4be -be -no-exit-code -f -d <outdir> <inpath>` |
| H03 | `sasquatch -le -no-exit-code -f -d <outdir> <inpath>` |
| H04 | `sasquatch -le -no-exit-code -f -d <outdir> <inpath>` |

So `-be` **is** present for the three BE carriers and the LE carriers correctly take `-le`. This matches the handler logic (`SquashFSExtractor.extract`: BE+4 → `sasquatch-v4be`, `-be` appended unless `bytes_used == mkfs_time`, the AVM marker). I parsed each superblock: all five are v4.0 with `mkfs_time = 1700000000` and `bytes_used` ≠ `mkfs_time`, i.e. `is_avm = False`, so `-be` is required and was appended. Control experiment: the same carriers fail with `sasquatch-v4be` **without** `-be` (`read_id_table: failed to read id table block`, `FATAL ERROR: File system corruption detected`) and succeed with `-be` (7 files listed for H01, matching the oracle), and `sasquatch-v4be -be -ll H05.sqsh` also shows the escaped symlink `b5q0u3of -> ../xx7gcbx`, confirming the carrier really contains it.

Consequence for the frozen table [INFERENCE]: `-be in child argv` can only ever be resolved as `n/a` from a successful clean envelope; a reader cannot distinguish "BE extracted with `-be`" from "AVM marker dropped `-be`" from the envelope alone — that distinction only becomes observable through `extraction_failed`/gap diagnostics (the `avm-marker-be-dropped` and `version-minor-mismatch` classes, H11/H12/H19/H20, outside my seat).

## 5. Tamper evidence: `evidence_id` re-derives from content

REA computes `evidence_id = "ev_" + sha256(canonical(semanticProjection(evidence)))` (`canonicalize`-style: JSON primitives, object keys sorted, arrays in order; `evidence_id` itself and `subject.name/local_path/path` are outside the projection). I re-implemented that encoder (`evid.py`) and first validated it on my own fresh REA output (H01, H05: both matched), then applied it to the committed files:

```
H01 stored=ev_dda74322…b1f668  recomputed=ev_dda74322…b1f668  match=True
H02 stored=ev_ac7afa3d…8037f6  recomputed=ev_ac7afa3d…8037f6  match=True
H03 stored=ev_8b663367…1ce669  recomputed=ev_8b663367…1ce669  match=True
H04 stored=ev_8340453c…4cf81c  recomputed=ev_8340453c…4cf81c  match=True
H05 stored=ev_86e5d480…f8ea83  recomputed=ev_86e5d480…f8ea83  match=True
```

`corpus/.../H0*/envelope.json` is exactly `rea-full.json["data"]` (`==` true, `ok: true`), and every recomputation matches, so the envelope bodies are internally self-consistent REA output rather than hand-assembled JSON. The only fields outside the digest are the subject path/name aliases, and those point at the in-corpus `carrier.sqsh` whose sha256 equals `manifest.json`.

## 6. Generator / freeze provenance: carriers regenerate byte-identically

```
python3 -I -B tools/round-39/heldout-gen.py \
        --seed 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b \
        --out $S/regen --classes clean-be,clean-le,escaping-symlink-removed      # exit 0, no --run
```

| id | committed carrier.sha256 | regenerated | tree.json |
|---|---|---|---|
| H01 | 67839b52…54c1b26 | identical | byte-identical |
| H02 | 0225f2bb…aaabe01 | identical | byte-identical |
| H03 | 67a373ac…33916a | identical | byte-identical |
| H04 | 8c7d04c0…1e71298 | identical | byte-identical |
| H05 | ae6d2f11…3f6cc8 | identical | byte-identical |

Regenerated `manifest.json` has the same `seed`, the same `generator` block, and carrier entries H01–H06 equal to the committed ones. Hash binding of the tool chain: `heldout-gen.py` at the freeze commit and at HEAD = `8b3eddf8225cfb1092726f2cabd78040f5ad765c5b4248c690a2d5bfad3cf5fc` = `manifest.generator.sha256`; `tools/round-37/gen-squashfs.py` = `1c7c5e88324d64ad5935e81f205a609a8361466e5aea9ba461575f4e01ba8dd5` = `manifest.generator.writer.sha256`; `tools/round-39/sqfs-triage.py` unchanged since freeze (`ef4a8a8b…`). Carrier identity is therefore a pure function of the freeze hash, as the claims file asserts.

Carrier classes are structurally honest: H01/H02 magic `sqsh` (BE), H03/H04 magic `hsqs` (LE), H05 magic `sqsh` (BE) with compression 1 = gzip (tree says gzip) while the others are compression 4 = xz (tree says xz); the five oracle file sets are pairwise distinct (no carrier reuse).

## 7. Determinism

H01 and H02 were re-run a second time and H01 a third time through REA (the third one under `strace`); each re-run's `normalized_result` equals both the committed envelope and the first fresh run after path normalization (0 diffs), including all file sha256/size, chunk ranges, coverage and diagnostics. Provider blob ids differed every run, as expected for fresh REA allocations.

## 8. Commands used (evidence)

```
# per carrier, scratch copy
cp corpus/evidence/round-39/c2/heldout/H0N/carrier.sqsh $S/carriers/H0N.sqsh   # sha256 verified
cd "$S" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
  "$S/carriers/H0N.sqsh" "$S/fresh/H0N-out" > "$S/fresh/H0N-full.json"        # exit 0, arm "after"
python3 -I -B <lane>/tools/round-39/sqfs-triage.py --skill <lane>/SKILL.md --json <env>
python3 $S/cmp2.py H01 H02 H03 H04 H05      # semantic diff, 0
python3 $S/payload.py H01 H02 H03 H04 H05   # oracle vs on-disk extraction
python3 $S/evid.py <envelope|rea-full>      # evidence_id recomputation
python3 -I -B <lane>/tools/round-39/heldout-gen.py --seed <freeze> --out $S/regen --classes clean-be,clean-le,escaping-symlink-removed
strace -f -qq -e trace=execve -o exec-H0N.txt <unblob ...>    # and once around the REA CLI for H01
```

Environment: unblob 26.6.4 (`executable_sha256 0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` in both committed and fresh engine blocks), REA `rea-agents@6.5.0`, `sasquatch`/`sasquatch-v4be` untouched in `~/.local/bin`. No tool installs or upgrades were needed (nothing recorded).

## 9. Observations, limits, non-findings

* The escaping symlink in H05 exists in `tree.json` (`symlinks[0] = {path: b5q0u3of, target: ../xx7gcbx, kind: escaping}`) but must not exist in an extraction; the files/dirs/sha checks pass and the absence of the link is the class semantics, so "payload match" is true in the intended sense, not a mismatch.
* `manifest.json` `label` for the two `clean-le` carriers is `clean` (shared label), which the frozen table produces for both handlers `squashfs_v4_le` and `squashfs_v4_be` via the `squashfs_v4_*` row — consistent, no drift.
* `coverage: partial` on H05 comes from the removed symlink; the table row for `escaping-symlink-removed` requires `SR=yes` with no gap, which is what both envelopes carry.
* No counter, carrier, oracle, table or predicate was modified; nothing outside my seat's paths was written. Attacks that could still hide beyond this seat: H06–H20 (in particular the two `before`-arm dependency classes and the two failure-message classes), which I did not run.

## Files changed

Only this report and the artifacts directory:

```
.ufo/waves/round-39/w2/R39W2HeldReproA.md
.ufo/waves/round-39/w2/artifacts/R39W2HeldReproA/
  carrier-sha256.txt  feature-table.txt  labels.txt  payload-check.txt
  evidence-id.txt  regeneration.txt  tool-provenance.txt
  sasquatch-argv-per-id.txt  rea-strace.txt
  cmp2.py  payload.py  evid.py
```
