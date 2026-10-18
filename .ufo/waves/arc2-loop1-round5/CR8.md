# CR8 (critic) — archive provenance attack

**VERDICT: ARCHIVE FIDELITY CONFIRMED for all 13 cited snapshots; PROVENANCE IS CONDITIONAL.** No path, blob, or executable-mode mismatch was found. The material risk is binding an archive-runner to the wrong root/revision or assuming an archive contains host inputs/history; `/var/tmp` had ample space during this audit, but storage exhaustion remains an unclosed operational failure mode.

**Axes:** temporary-space robustness; archive/tree fidelity; revision/root identity; external runtime inputs.

## Evidence — commands run and observed output

### 1. Capacity and exact committed-tree materialization

```console
$ git status --short && git rev-parse HEAD
?? .ufo/waves/arc2-loop1-round5/
0e8c96b48a8823e8c6964081cfc04e21f6adcf56
$ df -h /var/tmp /tmp                         # after my extraction/check
/dev/mapper/root  930G  147G  768G  17% /
tmpfs              16G   13G  3.1G  80% /tmp
```

I created only `/var/tmp/arc2-l5r5-CR8-archive-5YIdYH/`. The exact extraction form was `git -C "$ROOT" archive --format=tar "$rev" | tar -xf - -C "$SCRATCH/$rev"`, under `set -euo pipefail`, to a newly `mkdir`'d directory for each explicit cited revision. Revisions materialized: `4b806e1 58116aa df31bfb b3cd790 b21c0da 679af5d fd30b9c dbba2dd 158a966 1692acb 265e1aa fc8e53c 0e8c96b` (the listed short refs resolve to unique commits). `du -sh "$SCRATCH"` → `507M`.

The checker parsed `git ls-tree -r -z --full-tree REV`, enumerated extracted regular files and symlinks, compared path sets and Git blob SHA-1 (`sha1("blob " + size + NUL + bytes)`) plus Git executable/symlink modes. Exact summary:

```text
REDERIVE 4b806e1: tree=1181 extracted=1181 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE 58116aa: tree=1190 extracted=1190 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE df31bfb: tree=1254 extracted=1254 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE b3cd790: tree=1264 extracted=1264 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE b21c0da: tree=1324 extracted=1324 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE 679af5d: tree=1325 extracted=1325 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE fd30b9c: tree=1329 extracted=1329 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE dbba2dd: tree=1389 extracted=1389 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE 158a966: tree=1390 extracted=1390 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE 1692acb: tree=1394 extracted=1394 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE 265e1aa: tree=1399 extracted=1399 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE fc8e53c: tree=1457 extracted=1457 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
REDERIVE 0e8c96b: tree=1458 extracted=1458 missing=0 extra=0 blob_mismatch=0 mode_mismatch=0
```

Checker invocation was `python3 - "$ROOT" "$SCRATCH" <<'PY'` and used `git ls-tree -r -z --full-tree` plus the hash/mode comparison above (the inline checker was not saved as a separate file). Metadata checks: `git rev-parse --show-object-format` → `sha1`; `git ls-files -- '*gitattributes' '*gitmodules'` → no paths; `git ls-files -z | git check-attr -z --all --stdin | wc -c` → `0`; `git ls-tree -r --full-tree 0e8c96b | awk '$1 == "160000" {print}' | wc -l` → `0`; `.git` under the `265e1aa` archive → absent. Thus no active export-attribute or gitlink exception was observed in the tested state, and the audited archives were byte-/mode-identical to their source trees.

Space is not hypothetical: round-4 E15 recorded `git archive HEAD | tar -x` failing with `Disk quota exceeded` under `/tmp` and relocation to `/var/tmp` (`.ufo/waves/arc2-loop1-round4/E15.md:48-51`). Current `df` is only a point-in-time filesystem-capacity reading; it does not establish a future free-space or user/project-quota guarantee.

### 2. Provenance binding: reproducible wrong-root result

I replayed the archived v10 census twice:

```console
$ PYTHONDONTWRITEBYTECODE=1 python3 "$SCRATCH/265e1aa/.ufo/gates/c1-census-v10.py" --quiet
SCORECARD.md   lines=933  loci=9
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
$ PYTHONDONTWRITEBYTECODE=1 python3 "$SCRATCH/265e1aa/.ufo/gates/c1-census-v10.py" --root "$SCRATCH/265e1aa" --quiet
SCORECARD.md   lines=854  loci=9
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

This is an observed root-binding hazard, not evidence that a prior round made this mistake: v10 defaults `--root` to the live repository path at `.ufo/gates/c1-census-v10.py:370-374`, then opens each file under `args.root` at `:381-390`. The archived tool without `--root` therefore measured current HEAD (933 lines), not `265e1aa` (854 lines); both PASS, so a verdict-only transcript would conceal the misbinding. The round-4 scorecard says v10 passed at `265e1aa` (`SCORECARD.md:880-888`); my explicit-root replay independently confirms that cited tree's PASS.

Even with `--root`, this census is not self-contained in the archive: it reads live host configs under `$HOME` (`.ufo/gates/c1-census-v10.py:74-83,124-134`) and the current `$HOME/.npm/_npx` cache (`:218-234`); `--root` affects only the repository files read at `:383-390`. I observed the current anchor output on both runs as `{'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}`. A later replay can change if those host inputs drift; the archive alone cannot recreate them.

`git archive` also has no `.git` history/commit identity: I checked `.git` absent in the extracted tree. Round-4 CR6 explicitly materialized `HEAD`, then committed the scratch tree as synthetic `3de057b` before simulation (`.ufo/waves/arc2-loop1-round4/CR6.md:133-145`). Such a scratch `HEAD` is not the cited commit. Separately, round-4 E10 observed shared `HEAD` move from `158a966` to `1692acb` during the run (`.ufo/waves/arc2-loop1-round4/E10.md:34-38`); any `git archive HEAD` recipe in a concurrent wave can race unless it resolves and archives a full commit ID first. Round-3 C1 documents the good use case—dirty shared worktree, immutable `git archive 679af5d` before-state (`.ufo/waves/arc2-loop1-round3/C1.md:8-11,80-85`)—and its reproduction command (`:346-356`).

Control: `git archive --format=tar no-such-arc2-l5r5-revision | tar -tf - >/dev/null` returned `2`; the same pipeline with `set -o pipefail` also returned `2` (tar rejected empty input). This control did not demonstrate a masked bad-ref failure; `pipefail` is still prudent for producer failures, and no disk-full partial extraction was induced.

## Conclusions

- **OBSERVATION:** 13/13 cited commit archives had exact tracked path sets, blob bytes, and modes; the v10 PASS at `265e1aa` reproduced only when its `--root` was explicitly bound to that archive. This is snapshot-fidelity evidence, not an audit of every round claim's before/after metric.
- **OBSERVATION:** `/var/tmp` had 768G free after this 507M extraction. Prior `/tmp` quota failure is recorded at E15:48-51; this seat did not try to exhaust shared `/var/tmp`.
- **INFERENCE:** Archive provenance is safe for committed repository bytes only when the full revision, fresh extraction root, extractor success, and extracted-tree identity are recorded. Reusing a directory after an interrupted extraction risks stale/partial inputs; no such failure occurred in my fresh destinations.
- **INFERENCE:** Omitting `--root` is a concrete false-provenance path for v10, and using synthetic scratch `HEAD` or mutable `HEAD` can detach a measurement from its cited revision. These are hardening requirements; I found no evidence that they invalidate the recorded round results.
- **UNKNOWN:** Whether every historical archive replay used an immutable full SHA, explicit `--root`, and a tree-integrity check; whether future `/var/tmp` quota/free-space conditions will suffice; whether current home configs/cache equal the environment behind each historical measurement.

## Text parent may land VERBATIM

```text
Archive-based re-derivations must pin the full commit ID before extraction and use a new, empty, seat-owned scratch directory. Run `git archive "$REV" | tar -x` under `set -euo pipefail`; compare the extracted path/mode/blob manifest with `git ls-tree -r "$REV"` before measuring. Pass the extracted directory explicitly as `--root` and record both the source revision and root. `git archive` captures committed tree content, not `.git` history, untracked files, or host-state inputs; list and bind external config/cache anchors separately. A synthetic scratch commit is not the cited revision.
```
