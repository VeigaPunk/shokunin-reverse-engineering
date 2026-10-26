# R40W2C1SuffixAudit — every path-matching site in `c1-counter.py`, its false positive and false negative

**Verdict: DEFECTS FOUND.** I attacked the L1's reading that L2's failing clause `nonregular_unpublished_ok`
is a path-suffix false positive. The reading is **CONFIRMED** with the exact mechanism and reproduced
from frozen bytes (`same_rel('firmware.bin_extract/usr/bin/busy', 'bin/busy') == True`). But the same
one-line rule is *also* load-bearing in three other clauses where its looseness is an **acceptance hole**,
not a rejection: it lets a gap on a regular file satisfy the required gap of a symlink (`gap_check`), lets
an oracle row be satisfied by a deeper copy at the wrong path (`oracle_hits`), and — through `rel_suffix`
— lets a receipt with **no chunk-extract root at all** project identically to the honest run. So the
smallest safe correction is not "ignore the L2 hit": the rule must be replaced by root-anchored exact
matching. The replacement is verified to keep all four carriers at 100 % (697/8/7/6 oracle rows, zero
non-regular violations, zero unresolved gaps) while flipping ten of twelve new pinning cases.

Seat `R40W2C1SuffixAudit` (critic, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, tip at
dispatch `4d62ee5a86b4692a13f682b29ed7975e8d7e5326`. Nothing frozen was modified, nothing committed, no
VCS mutation was run. Artifacts: `.ufo/waves/round-40/w2/artifacts/R40W2C1SuffixAudit/`. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40W2C1SuffixAudit` removed after the artifacts were copied.

Cross-domain evidence: none read. No R40-C2 path (`SKILL.md`, its interpreter/generator, held-out data) was
opened; the two claims stay separable.

## Axes named (Godspeed)

| axis | what this seat moves |
|---|---|
| **coverage** | all six path-matching sites (`same_rel`, `oracle_hits`, `nonregular_published`, `gap_check`, `rel_suffix`, the projection's path keys) plus the two adjacent path predicates, each with a built construction on the round-40 carriers or a minimal fixture — 12 pinned cases, 10 of which the frozen rule decides wrong. |
| **depth** | one executable rule the round-40 corpus does not hold: *a receipt path is only attributable when it names the receipt's single chunk extract root as a whole component; the comparison is then `==` on the remainder*. Measured on the four carriers, not argued. |
| **calibration** | the frozen predicate's own wording ("same relative-path suffix") is the defect — the tool is faithful to it. A round-41 fix that only patches the tool leaves a claim whose text still licenses the bug, and the freeze-integrity rule makes the text as frozen as the code. |

## 1. The live failure, decoded

`corpus/evidence/round-40/c1/L2/nonregular.tsv` (frozen table, 10 rows) contains

```
bin	dir	
bin/busy	symlink	/usr/bin/busy
```

and `corpus/evidence/round-40/c1/L2/oracle.tsv` contains the regular file `usr/bin/busy`
(`e28f81fc…`, 40 000 bytes). REA publishes that regular file at
`firmware.bin_extract/usr/bin/busy`. The counter's rule (`tools/round-40/c1-counter.py:606`)

```python
def same_rel(candidate, rel):
    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))
```

matches `.../usr/bin/busy` against the **symlink** `bin/busy`, so `nonregular_published` returns
`['firmware.bin_extract/usr/bin/busy']` and `nonregular_unpublished_ok` is false
(`.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`, L2 record; every other L2 clause true,
`carriers_matched: 3`, `exit_code: 1`).

This is not a one-off, and it is not the carrier's fault: it fires whenever a symlink's own path is a
proper component-suffix of *its target path* and that target is also published as a regular file. The
canonical instance is a basename-preserving absolute link, which is exactly what L2 carries
(`bin/busy → /usr/bin/busy`). V1 escaped **by luck of naming**, not by structure: V1 has **29 absolute
symlinks, 9 of whose targets are also oracle regular files** (`lib/libber.so → /lib/libber.so.0.4.2`,
`lib/libruli.so → /lib/libruli.so.4`, `usr/sbin/cefdk → /usr/sbin/upgradebox`, …) — all 9 escape only
because AVM's versioned library links change the basename. L1 escaped because its single absolute link
target (`/proc/mounts`) is not a published file. Any round-41 carrier with a same-basename absolute link
whose target exists reproduces the L2 false positive one-for-one.

## 2. Site audit

Notation: *FP* = the rule accepts/sees something that is not true; *FN* = the rule rejects or misses
something that is true. Every construction below was run against the frozen module (import, read-only):
`artifacts/R40W2C1SuffixAudit/probe-current-sites.txt`, `pinning-cases.txt`, `projection-hazards.txt`.

| # | site (`c1-counter.py`) | false positive | false negative | construction / evidence |
|---|---|---|---|---|
| 1 | `same_rel` `:606` | any path that ends with `rel` at a component boundary matches, regardless of where it sits | a path *shallower* than `rel` never matches; a trailing slash never matches | `same_rel('firmware.bin_extract/usr/bin/busy','bin/busy')` → `True` (live, §1); `same_rel('bin/busy/','bin/busy')` → `False` |
| 2 | `oracle_hits` `:635` | `sha == fs and same_rel(...)`: a **deeper copy** satisfies an oracle row for a shallower path, and for an empty file the digest is vacuous, so any empty file whose path ends with the oracle's rel counts | — (conjunctive, suffix is permissive) | oracle `usr/bin/busy`, only published file `firmware.bin_extract/mnt/usr/bin/busy` → still `1/1`; oracle `zero` (empty digest) satisfied by `firmware.bin_extract/tmp/zero` → `1` |
| 3 | `nonregular_published` `:643` | the live L2 case: a regular file at a symlink's target counts as "the symlink was published" | a candidate carrying a trailing slash (`bin/busy/`) is not seen; a *directory* published at a symlink path is in `files[]` and would be caught, but a path reported as a prefix (`bin/busy/x`) is not | `['firmware.bin_extract/usr/bin/busy']` vs frozen L2 table |
| 4 | `gap_check` path-resolved branch `:682` | a gap reported on the **regular file** `firmware.bin_extract/usr/bin/busy` resolves to the symlink `bin/busy` and satisfies `required[symlink]`, while the real symlink's gap is absent — the run "accounts for" a gap it never produced | `len(hits) != 1` rejects a correct gap when two frozen non-regular rels are nested | `gap_check(gaps=[depth-limited, gap on usr/bin/busy, gap on usr/bin/ls], L2, rule)` → `(True, '3 gaps (1 structural)…')` — same verdict as the honest gap set. Ambiguity: frozen V1 table has 4 nested pairs (`lib` / `lib/modules/2.6.39.4/kernel/lib`, `usr/bin`/`bin`, `usr/lib`/`lib`, `usr/sbin`/`sbin`), L1 has 1 (`usr/lib`/`lib`); all happen to be dirs, so no gap path reaches them **today** |
| 5 | `gap_check` required/missing branch `:697`–`:702` | satisfied by a gap that resolution (site 4) mis-attributed, or by a gap on a *different* entry with the same kind | a gap whose `relative_path` is the chunk root, or carries a trailing slash, is `0 hits` → whole clause red | same construction as site 4 |
| 6 | `rel_suffix` `:745` | erases *any* first `*_extract` component, so two different trees collapse (`a_extract/x` and `b_extract/x` → both `x`); a `..` component survives into the projection (`$output/a_extract/../../etc/passwd` → `../../etc/passwd`) | the **root itself** is *not* erased (`rel_suffix('firmware.bin_extract')` → `'firmware.bin_extract'`): an entry or derivation at the root stays name-dependent, so an honest rerun under a different root name would be red | all four behaviours reproduced in `projection-hazards.txt` and `probe-current-sites.txt` |
| 7 | `projection` files row / `hashes` key `:797`, `:808`, `:812` | — | the `plus-mime` and `plus-content` columns are **constant `null`** on every round-40 receipt: `normalized_result.files[].mime_type` is null (0/697 on V1, 0/6 on L2 and on a fresh rerun) and the HashReport map is keyed by `rel_suffix(task.path)`, an **absolute task path** (`fast/scratch/…/firmware.bin_extract`), a key space disjoint from the entry suffixes the rows look up → every row gets `[None, None]` | `projection(env,'plus-extractor')['files'][0]` → `["etc/hosts", "081ef9…", 20, null, null, null]`; task keys printed in `projection-hazards.txt` |
| 8 | `provenance_ok` `:596` (adjacent) | substring test only: any absolute path containing `/kaidoku-r40/` passes — `provenance_ok('/tmp/kaidoku-r40/x')` → `True`; two carriers may claim the same output directory | a legitimate run under a different `HYAKU_SCRATCH` base passes too — the predicate is a shape check, not an identity check | `probe`: `provenance_ok('/tmp/kaidoku-r40/x')` → `True`, `provenance_ok('/fast/scratch/hyaku/kaidoku-r40/run-L2/extract')` → `True` |

### 2.1 The `rel_suffix` premise is measurably false

The docstring (`:750`) and `rehost` (`:1380`) both rest on "the staged input name … differs between the
round run and the counter's rerun". I ran the counter's own rerun shape once, on committed L2 bytes:

```
cd "$S/rr" && cp …/c1/L2/carrier.sqsh ./carrier.bin
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob TMPDIR="$S/rr" \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
      --max-depth 1 --max-output-files 10000 --max-output-bytes 100000000 \
      carrier.bin "$S/rr/out"            # exit 0
```

Input named `carrier.bin`, subject `carrier.bin` — and the chunk extract root came back
**`firmware.bin_extract`**, exactly as in the committed receipt, with the same files and gaps. The root
name is derived from the handler/REA staging constant, not from the input name. So for `squashfs_v4_be`
under the pinned `rea-agents@6.5.0` the root is **stable**, the erasure buys nothing for these carriers,
and it costs items 6–8. (Inference, not measurement: this holds for the one handler and the one
rea-agents pin exercised here; a round-41 carrier through another handler must re-measure before relying
on it.)

## 3. Blast radius of the proposed rule

`artifacts/R40W2C1SuffixAudit/verify-carriers.txt` — the root-anchored rule of §4 re-scored against the
four committed receipts and frozen tables:

| carrier | root found | oracle (exact) | non-regular published | unresolved gaps | required gaps missing |
|---|---|---|---|---|---|
| V1 | `firmware.bin_extract` | 697/697 | `[]` | `[]` | 0 |
| V2 | `firmware.bin_extract` | 8/8 | `[]` | `[]` | 0 |
| L1 | `firmware.bin_extract` | 7/7 | `[]` | `[]` | 0 |
| L2 | `firmware.bin_extract` | 6/6 | `[]` (was `[…]usr/bin/busy`) | `[]` | 0 |

Zero oracle rows in any carrier are satisfied *only* by a suffix match
(`root-relative-coverage.txt`: `suffix_only_hits=0` for all four), so the strict rule loses nothing on
round-40 data. Under the same rule, L2 committed vs the fresh rerun still project equal (below the root),
the rootless receipt no longer equals the honest one, and a receipt whose root is renamed is equal
below-root and unequal with the root compared — both directions measured:
`below-root only: committed==fresh True | renamed==committed True`, `with root name: True | False`.

## 4. Exact replacement rule for a round-41 refreeze

```python
def path_parts(path):
    """Components of a receipt path; every leading '$output/' stripped, ''/'.' dropped."""
    if not isinstance(path, str):
        return None
    while path.startswith('$output/'):
        path = path[len('$output/'):]
    return [p for p in path.split('/') if p not in ('', '.')]


def chunk_root(env):
    """(root, why): the single chunk extract directory the receipt names.

    A depth-1 derivation child (`$output/<stem>_extract`) is authoritative; when
    a receipt carries none (unit fixtures, older shapes) the unique first
    component ending in `_extract` across entry paths is used. Anything other
    than exactly one is not attributable."""
    nr = env.get('normalized_result') or {}
    roots = []
    for d in nr.get('derivations') or []:
        if not isinstance(d, dict):
            continue
        ps = path_parts(d.get('child_path'))
        if ps and len(ps) == 1 and ps[0].endswith('_extract'):
            roots.append(ps[0])
    if not roots:
        cand = set()
        for key in ('files', 'extraction_gaps', 'unpublished_entries'):
            for e in nr.get(key) or []:
                ps = path_parts((e or {}).get('relative_path'))
                if ps and ps[0].endswith('_extract'):
                    cand.add(ps[0])
        roots = sorted(cand)
    roots = sorted(set(roots))
    if len(roots) != 1:
        return None, ('no_root' if not roots else 'mult_root:%r' % (roots,))
    return roots[0], None


def entry_rel(path, root):
    """Path relative to the receipt's single chunk extract root, or None.

    The root must appear as a whole component (first for `relative_path`,
    anywhere for an absolute `path`/`input_path`). `..` anywhere means outside.
    The root itself maps to '' so an entry at the root is name-independent."""
    ps = path_parts(path)
    if not ps or root is None or '..' in ps:
        return None
    if ps[0] == root:
        payload = ps[1:]
    else:
        try:
            i = ps.index(root)
        except ValueError:
            return None
        payload = ps[i + 1:]
    return '/'.join(payload)


def same_entry(path, rel, root):
    return rel is not None and entry_rel(path, root) == rel
```

Wiring, in this order:

1. `measure` computes `root, why = chunk_root(env)` once per carrier; `why` is recorded as
   `root_error` and makes every path clause red with that reason (not `unevaluable`, so the receipt —
   not the environment — is blamed).
2. `oracle_hits(oracle, files, root)`, `nonregular_published(files, nonreg, root)` and both branches of
   `gap_check(..., root)` replace every `same_rel` call with `same_entry`. `len(hits) != 1` becomes
   unreachable by construction (exact match is injective, and `parse_nonregular` already rejects
   duplicate rows); keep the guard as an assertion, not as a scoring branch.
3. `rel_suffix` is deleted and `projection` uses `entry_rel(x, root)` for all five path fields
   (`files`, `extraction_gaps`, `unpublished_entries`, `derivations` parent/child, and the
   `hashes` key). The `hashes` key must then come from the **entry** path
   (`files[].path`), which is the only place a per-file path exists; `raw_result.report[].task.path`
   gives a task path, not an entry path, and attaching on it is the silent no-op of site 7.
4. Because three components of `plus-extractor` carry no information on this schema (mime null,
   md5/sha1 null), the round-41 profile should either drop them or replace them; `carriers.json`
   currently selects a profile whose stated strength the data does not support. (`plus-extractor` is
   still satisfied — the columns are null on both sides — so no round-40 verdict moves; the review
   ledger's description of what the profile binds is what is overstated.)
5. Recommended strictness, costed: add `chunk_root` to `PROJECTION_KEYS_BY_PROFILE['plus-extractor']`.
   Measured safe under `rea-agents@6.5.0` + unblob 26.6.4 (`committed == fresh: True` with the root
   compared, §3), and it closes the "extracted into a differently named root" gap that erasure opened.
   This is the one item in this section that is a tradeoff rather than a defect: it couples the
   projection to handler/staging naming, so it must be re-measured the moment either version changes.

Predicate and input changes the same refreeze needs (the tool alone is not enough):

- `plans/round-40-claims.md` P40-C1 says "publishes every regular file of the frozen independent oracle
  (**same relative-path suffix**, same sha256)" and "carries extraction gaps only as the frozen gap rule
  allows (one `unpublished-entry` per symlink …)". Both sentences must become "the same path relative to
  the single chunk extract root named by the receipt" — otherwise the frozen text still licenses the
  defect and `frozen_drift` would reject a counter that fixed it.
- `tools/round-40/mk_env` fixture builder emits `derivations: []` (`:1304`), so every fixture exercises
  the fallback path and none exercises the authoritative one; the refreeze must emit the real derivation
  and add one fixture that omits it.
- `FROZEN_PATHS` gains nothing and loses nothing: `c1-counter.py` is already frozen, which is why this is
  a round-41 item and not a round-40 repair.

## 5. Selftest cases that pin it

Twelve cases, all run against the frozen module vs the §4 rule (`pinning-cases.txt`); `want` is the
proposed verdict. Ten of twelve are decided differently by the frozen rule — i.e. ten currently-uncaught
mutants.

| case | construction | frozen rule | §4 rule | want |
|---|---|---|---|---|
| `suffix-deep-regular-vs-symlink` | published regular `usr/bin/busy`; nonreg symlink `bin/busy` | `['…usr/bin/busy']` (**red**) | `[]` | `[]` |
| `suffix-deep-copy-satisfies-oracle` | oracle `usr/bin/busy`; only built file `mnt/usr/bin/busy`, same sha | `1/1` (**green**) | `0/1` | `0` |
| `suffix-empty-digest-elsewhere` | oracle `zero` (empty digest); built `tmp/zero`, empty | `1` (**green**) | `0` | `0` |
| `gap-on-regular-satisfies-symlink` | gaps on `usr/bin/busy`, `usr/bin/ls`, `depth-limited`; symlink `bin/busy` | `True` (**green**) | `False` | `False` |
| `gap-nested-nonreg-ambiguity` | nonreg `bin`(dir), `bin/busy`(symlink), `busy`(symlink); honest gaps | `False`, `matches 2 non-regular entries` (**red**) | `True` | `True` |
| `gap-trailing-slash` | gap path `bin/busy/` | unmatched (**red**) | `bin/busy` | `bin/busy` |
| `gap-absolute-path` | `…/firmware.bin_extract/bin/busy` | `bin/busy` | `bin/busy` | `bin/busy` (no change; pins absolute forms) |
| `in-image-extract-dir-preserved` | `firmware.bin_extract/opt/x_extract/y` | `opt/x_extract/y` | `opt/x_extract/y` | `opt/x_extract/y` (no change; pins that the root is matched by name, not by `*_extract`) |
| `entry-at-root` | path `firmware.bin_extract` | `'firmware.bin_extract'` (**unstable**) | `''` | `''` |
| `rootless-path` | `usr/bin/busy` with root `firmware.bin_extract` | `'usr/bin/busy'` (**accepted**) | `None` | `None` |
| `dotdot-escape` | `$output/a_extract/../../etc/passwd` | `'../../etc/passwd'` (**accepted**) | `None` | `None` |
| `two-roots` | receipt with derivations to `firmware.bin_extract` and `other_extract` | accepted | `mult_root:['firmware.bin_extract','other_extract']` | that string |

Case 1 replaces the fixture that currently covers this class (`escaping symlink published as a regular
file`, `:1783`) — that case uses an **exact** path and therefore stays green under both rules; it does
not cover the suffix direction, which is the one that fired. Case 4 is the sharpest: it is an
*acceptance*, so the frozen suite has no red case that can catch it, and no control in
`.ufo/waves/round-40/controls/` exercises it.

## 6. Consequence for the landing (calibration)

- The L1's diagnosis is right and now mechanised: L2's `nonregular_unpublished_ok` is a false positive,
  so P40-C1's *data* is 4/4 in substance.
- The L1's **honest stop still stands as a scoring fact** and my finding does not make it reversible: the
  counter is a frozen path, the predicate's text says "relative-path suffix", and a post-freeze repair
  would be `frozen_path_changed` (exit 2), never `met_target`. What should not be recorded is the reading
  "L2's extraction fails" — the correct record is "the frozen path rule is defective; L2 is correct data".
- Because the same rule is permissive in `oracle_hits`, `gap_check` and the projection, the round-40
  score of `3/4` and the round-41 target of `4/4` are not on the same scale: the round-41 refreeze must
  fix the rule *and* re-score all four carriers under it (which is exactly the table in §3 — no carrier
  loses a row).

## 7. Disclosed limits

- The handler-stability measurement (§2.1) is one run of one handler on one carrier; it is stated as
  measured, and its generalisation is marked inference. I did not run V1/V2 (vendor cache rebuild), so
  the "29 absolute symlinks / 9 same-target" V1 figures are read from the frozen tables, not from a rerun.
- The frozen rule's *ambiguity* FN is latent on round-40 data: the four nested V1/L1 pairs are `dir`/`dir`
  or `dir`/parent and no gap path reaches them. It is proved as a rule property (case 5), not as a
  round-40 failure.
- `provenance_ok` is adjacent to the six named sites and is reported with a direct construction only
  (`probe`), not through a re-scored receipt. My §4 rule does not touch it, so the two existing red cases
  at `:1791` and `:1795` keep their verdicts; a stricter provenance form (require the
  `<HYAKU_SCRATCH>/kaidoku-r40/<session>/` prefix and a directory that did not pre-exist) is a separate
  round-41 item and was not run.
- Nothing was installed or upgraded. Tooling used as found: `npx -y rea-agents@6.5.0` (package already
  present at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6`), `unblob 26.6.4` at `~/.local/bin/unblob`,
  python3 from the host. `pacman` untouched, `~/.local/bin` untouched.

## 8. Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r40/R40W2C1SuffixAudit
python3 -I -B tools/round-40/c1-counter.py --selftest \
        --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
# {"selftest": "c1-counter", "cases": 70, "green_ok": 5, "red_ok": 65, "failures": []}

python3 -I -B "$A/probe.py"    # frozen rule on every site   -> probe-current-sites.txt
python3 -I -B "$A/proj.py"     # projection path hazards     -> projection-hazards.txt
python3 -I -B "$A/exact.py"    # root-relative re-score      -> root-relative-coverage.txt
python3 -I -B "$A/cases.py"    # 12 pinning cases            -> pinning-cases.txt
python3 -I -B "$A/verify.py"   # 4 carriers + projection     -> verify-carriers.txt
```

`$A` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-40/w2/artifacts/R40W2C1SuffixAudit`.
