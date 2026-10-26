# R39C2ReconClean — R39-C2 development recon: four outcome classes, feature stability, grammar expressiveness

**Verdict: DONE — all four development classes are stable across two independent trees each and
pairwise distinct under the R39-C2 grammar, but the recon found three defects in the draft
contract that must be settled before the freeze: the symlink rule is not "resolves inside the
root" (absolute targets are reinterpreted root-relative and kept), a carrier with one link of
each kind is `unclassified` under a 7-row table, and the `-be in child argv` cell is inert on
all four classes (it is only observable when the BE extractor actually fails).**

Seat: leaf executor `R39C2ReconClean`. Lane `kaidoku-shokunin`, base `a2f64e1da78afcf8cc39287106604dbcc270844c`.
Nothing outside `.ufo/waves/round-39/w1/` was written; no VCS mutation; no K5/K6 carrier was built,
copied or run through REA; no held-out carrier was built or run.

---

## 1. What was run (exact commands, exit codes)

All REA runs are **after-arm** (both `sasquatch` and `sasquatch-v4be` reachable in `~/.local/bin`),
on **development carriers I built in scratch from trees I authored**. Scratch
`S=/fast/scratch/hyaku/kaidoku-r39/R39C2ReconClean`; every REA call was `cd "$S"` first so
`unblob.log` lands there.

```
# 1. trees + images (deterministic writer, round-37)
sh .ufo/waves/round-39/w1/artifacts/R39C2ReconClean/build-dev-carriers.sh "$S"
  -> exit 0; wrote a1 a2 b1 b2 c1 c2 d1 d2 e1 f1 f2 c2-twolevel .sqsh
python3 .ufo/waves/round-39/w1/artifacts/R39C2ReconClean/make-damaged.py "$S/carriers/a1.sqsh" "$S/carriers"
  -> exit 0; wrote be-body-damaged.sqsh be-meta-damaged.sqsh

# 2. after-arm REA, one fresh outdir per run (15 invocations over 15 image builds; 14 kept)
REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob" \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
  "$S/carriers/<C>.sqsh" "$S/out/<C>" > "$S/env/<C>.json" 2>"$S/env/<C>.err"
  -> exit 0 for all 15 invocations (see §1.1 for the two superseded runs)

# 3. features + grammar probe
python3 .../featurize.py "$S"/env/*.json "$S"/known/*.json          -> exit 0
python3 .../sqfs-triage-ref.py --selftest                            -> exit 0 (0 failures)
python3 .../sqfs-triage-ref.py --table .../candidate-table-fragment.md --label <envelopes>
  -> exit 0, 20/21 labelled, `e1` unclassified (by design, §5 F2)
python3 .../sqfs-triage-ref.py --table .../candidate-table-mixed-fragment.md --label <envelopes>
  -> exit 0, 21/21 labelled
python3 .../sqfs-triage-ref.py --table $LANE/SKILL.md --label "$S/env/a1.json"
  -> exit 2, `unevaluable: no triage-table marker in the craft section`
```

### 1.1 Run accounting (honest)

15 REA invocations, 14 kept envelopes, 1 discarded:

* `c2` was run twice. The first tree used `deep/inner/link-out -> ../../outside/x.txt`, which I
  had wrongly assumed escaped; from `deep/inner`, two `..` land on the image root, so unblob kept
  it (kept envelope `c2-twolevel`, subject sha `c21973c9…`). The class-(c) tree was rebuilt with
  `../../../outside/x.txt` and re-run (`c2`, subject sha `9e4464e1…`). Both envelopes and both
  images are in the artifacts; the first one is now the primary evidence for finding F1.
* `be-body-damaged` was run twice. The first corruption (bytes 200..207) did not disturb
  extraction, so the image was rebuilt with a stronger corruption (bytes 96..175) and re-run; the
  first envelope was overwritten. Both images differ in sha; only the current one is claimed.

## 2. Tooling

Nothing installed, upgraded or removed this wave; no pacman transaction was attempted.

| tool | version | how resolved | role |
|---|---|---|---|
| `rea-agents` | 6.5.0 | `npx -y rea-agents@6.5.0` (existing `_npx` cache) | envelope producer |
| `unblob` | 26.6.4 | `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` (absolute) | provider |
| `sasquatch` | 4.5.1 (onekey-sec) | `~/.local/bin` on the child `PATH` | LE extractor |
| `sasquatch-v4be` | 4.5.1 (onekey-sec) | `~/.local/bin` on the child `PATH` | BE extractor |
| `gen-squashfs.py` | round-37, unmodified | `tools/round-37/gen-squashfs.py` | image writer |

`--full-output` envelopes are 8.5–16.4 KB, so none were gzipped.

## 3. The four classes — stability across two trees, distinctness

Each class was built from two freshly authored trees (different file sets, different depths,
different link spellings). Features are computed exactly per the grammar (H, G, D, BE, SR, P).

| class | tree 1 | tree 2 | H | G | D | BE | SR | P |
|---|---|---|---|---|---|---|---|---|
| (a) clean BE gzip, no symlinks | `a1` | `a2` | `{squashfs_v4_be}` | `∅` | `∅` | `n/a` | `no` | 4 / 3 |
| (b) clean LE gzip, no symlinks | `b1` | `b2` | `{squashfs_v4_le}` | `∅` | `∅` | `n/a` | `no` | 3 / 3 |
| (c) BE, only an escaping relative symlink | `c1` | `c2` | `{squashfs_v4_be}` | `∅` | `∅` | `n/a` | **`yes`** | 2 / 2 |
| (d) BE, only an in-tree relative symlink | `d1` | `d2` | `{squashfs_v4_be}` | **`{unpublished-entry}`** | `∅` | `n/a` | `no` | 2 / 2 |

**Stable.** Within each class the two trees agree on all six features. P differs in value (4 vs 3)
but not in the cell it feeds (`>0`), so the class is stable *under the grammar*, which is what the
interpreter sees.

**Pairwise distinct.** (a)/(b) differ in H. (a)/(c) differ in SR. (a)/(d) differ in G.
(c)/(d) differ in both SR and G. (b) differs from (c) and (d) in H. No two classes share a feature
vector, so a 4-row table separates them without any `*` in a condition cell.

Five independent non-class envelopes reproduce the same shapes and are included in the artifacts:
round-38 `K3/after`, `K4/after` (class a), `K1/after` and the round-38 probe `rea-k1-orig`
(class c), `K2/after` (class d). The lane's own K1–K4 receipts therefore corroborate the
development recon rather than contradict it.

## 4. Feature table per run

Columns are exactly the fields the item asks for. `unpublished` is
`normalized_result.unpublished_entries[].kind`; `diagnostics` is
`normalized_result.diagnostics[].report.__typename__`; `command` is
`normalized_result.diagnostics[].report.command`. `P` = `len(normalized_result.files)`.
Rows `k3-after` … `avm-k1` are **read-only copies of pre-existing envelopes** (round-38 receipts
and the round-38 AVM probe), not new runs.

| run | handler | extraction_failed | gap kinds | dependencies | BE | SR | unpublished | P | published_bytes | coverage | diagnostics | command |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `a1` | `squashfs_v4_be` | false | none | none | n/a | no | none | 4 | 244 | complete | - | - |
| `a2` | `squashfs_v4_be` | false | none | none | n/a | no | none | 3 | 6039 | complete | - | - |
| `b1` | `squashfs_v4_le` | false | none | none | n/a | no | none | 3 | 57 | complete | - | - |
| `b2` | `squashfs_v4_le` | false | none | none | n/a | no | none | 3 | 3031 | complete | - | - |
| `c1` | `squashfs_v4_be` | false | none | none | n/a | yes | none | 2 | 28 | partial | MaliciousSymlinkRemoved | - |
| `c2` | `squashfs_v4_be` | false | none | none | n/a | yes | none | 2 | 21 | partial | MaliciousSymlinkRemoved | - |
| `d1` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | no | `symlink` | 2 | 19 | partial | - | - |
| `d2` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | no | `symlink` | 2 | 19 | partial | - | - |
| `c2-twolevel` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | no | `symlink` | 2 | 21 | partial | - | - |
| `e1` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | yes | `symlink` | 2 | 18 | partial | MaliciousSymlinkRemoved | - |
| `f1` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | no | `symlink` | 2 | 19 | partial | - | - |
| `f2` | `squashfs_v4_be` | false | none | none | n/a | yes | none | 1 | 10 | partial | MaliciousSymlinkRemoved | - |
| `be-body-damaged` | `squashfs_v4_be` | false | none | none | n/a | no | none | 4 | 244 | complete | - | - |
| `be-meta-damaged` | `squashfs_v4_be` | true | `extractor-failure` | none | **yes** | no | none | 0 | 0 | partial | ExtractCommandFailedReport | `sasquatch-v4be -be -no-exit-code -f -d <out> <in>` |
| `k3-after` | `squashfs_v4_be` | false | none | none | n/a | no | none | 4 | 28 | complete | - | - |
| `k4-after` | `squashfs_v4_be` | false | none | none | n/a | no | none | 4 | 28 | complete | - | - |
| `k1-after` | `squashfs_v4_be` | false | none | none | n/a | yes | none | 5 | 9656 | partial | MaliciousSymlinkRemoved | - |
| `orig-k1` | `squashfs_v4_be` | false | none | none | n/a | yes | none | 5 | 9656 | partial | MaliciousSymlinkRemoved | - |
| `k2-after` | `squashfs_v4_be` | false | `unpublished-entry` | none | n/a | no | `symlink` | 3 | 10283 | partial | - | - |
| `k1-before` | `squashfs_v4_be` | true | `missing-extractor-dependency` | `sasquatch-v4be` | n/a | no | none | 0 | 0 | partial | ExtractorDependencyNotFoundReport | - |
| `avm-k1` | `squashfs_v4_be` | true | `extractor-failure` | none | **no** | no | none | 0 | 0 | partial | ExtractCommandFailedReport | `sasquatch-v4be -no-exit-code -f -d <out> <in>` |

`ok` is `true` on all 14 new envelopes and on the two full-envelope probes (`avm-k1`,
`orig-k1`); the round-38 receipts are bare `data` objects and carry no `ok` key (`-`).

### 4.1 Envelope identity (subject digest == carrier bytes)

| run | evidence_id | subject sha256 | carrier |
|---|---|---|---|
| `a1` | `ev_3438fad69cce0ba986744359c147be8512817dd83d9ee92e7adfd7f08ca3d954` | `a7addcc839818d0e3c7dd8c1352cac8155f1916c60f1e1c6647c70ea002ea569` | `a1.sqsh` |
| `a2` | `ev_c738706ed26c920c891b046dc435eb5e71ca32aa16fefa50476db9ecef329d07` | `0cd9c65a5a302f22a84027a57e7b5eb9db72690eb173e61f0a36b99ee5ed8fb4` | `a2.sqsh` |
| `b1` | `ev_ac25612f0a73330850c24c7ed0342b6fa82c21f745ec76b3f28254da5db27183` | `0c844f2919e945eb74626a4b0fd8cd0a52313489c04b3a0c48a272cec201f9a1` | `b1.sqsh` |
| `b2` | `ev_2730f6b948eaa4ebf0e2967a303f6b294f64bb5dfcfff017a325a19b497f1d97` | `f2bc60c5267d78ed3b8bed8df035de4d4212b7180056ca0c045634c32b7fd0b6` | `b2.sqsh` |
| `c1` | `ev_4b49218e045a3af258461f2b9d59ba53c0ee7e8c9a680b72ca23c9c4d944c015` | `9f519693c9d199561e69e76339be6870d4bb1ddd0ceb09932699c6890352f516` | `c1.sqsh` |
| `c2` | `ev_76ad2e7493db85a02ba1a09c20b47f575e3ba6f094ab0d5255f1688b4a20b68c` | `9e4464e1969bdd592104e0e29f7e782d1fe82da6dc4b2e34a1b60e61e8c38295` | `c2.sqsh` |
| `d1` | `ev_c68d28c8c9fc5e821eec36bb55d667f0580723015395808548881f944101642c` | `a5dd999dd4dd8847f562290410bc266c72bd9d8e9e94f479e0e3b31c83189958` | `d1.sqsh` |
| `d2` | `ev_308d1d17cdca3a505014ac762ffe0a48f48f67e6e42698d24f304153a1d154f2` | `fc1d08c2522ac3c31a389499cbc3b6014ffe67ebfae724e660b12e8f6faf1a13` | `d2.sqsh` |
| `c2-twolevel` | `ev_dff71945febae5ffa763ece62b0ad94048ab6c18812f4b81bacd34cf77880942` | `c21973c9174f7819a0559892363dac0cdc536a17b50ad8f87d76cfd2f6c8f615` | `c2-twolevel.sqsh` |
| `e1` | `ev_155910ba60c78504d8b5862ef5882ce39513b3c519a142d0a3e2926cd826fb19` | `c67f8e83d46d8f69faeeac9e812957425b3017632af2842732b397dd9b65239e` | `e1.sqsh` |
| `f1` | `ev_8f6387aca57936ea0c147ce7beeec1e16c545f9d627545641bd470b4f0ce35fa` | `598ae140abd0459e298558b3e9f340043d4a01eb949314b2b840f476f7e80856` | `f1.sqsh` |
| `f2` | `ev_0cac189ae9a0edd3bdfd0ab88ae671be00c726a6a93e90cd2c27860f13eb0659` | `c093c76bb76053a21a956d7681dba65cba9e8344534f713c5dc1e272454be9ef` | `f2.sqsh` |
| `be-body-damaged` | `ev_e2c1b7ada4efd52b8ca90fbaeef573dbd4ce455057ad321f2d9fdcf1424cfb96` | `1e715d56083c317edd67fc20850f6e39dce014fbea74c77c2f132d1e62a9dad7` | `be-body-damaged.sqsh` |
| `be-meta-damaged` | `ev_95133832f8e5f2e5bd1148079e11b2f3d49499508c59be4b09bf72be76fd8523` | `f3afc97b3814968c0cc3aa120dbc6fb334da1af87341f04c5e5a382d79a0e9a6` | `be-meta-damaged.sqsh` |

Every row's subject digest equals the sha256 of the carrier in `carriers/` — checked for all 14
by recomputing the file digest, not copied from the envelope.

**Determinism.** All 14 carriers reproduce byte-identically from the two recorded scripts, checked
twice into fresh scratch directories (`repro2`, `repro3`): `cmp` IDENTICAL for every file. The
round-37 writer embeds a fixed `mkfs_time` and sorts its walk, so seed-driven regeneration is
mechanically plausible — but see limit L6: *seed* is not a generator input today.

## 5. Findings that must be settled before the freeze

### F1 (material, C1 + C2) — the symlink rule is not "resolves inside the extraction root"

The draft rule ("a symlink whose target resolves inside the extraction root is kept … a symlink
that escapes is removed") is right for relative targets and **wrong for absolute targets**.
unblob 26.6.4 `extractor.py:52-89` strips a leading `/` from an absolute target and then tests it
**root-relative**; `file_utils.py:34-39` (`is_safe_path`) resolves `outdir.joinpath(path)` and asks
whether it is under `outdir`.

Evidence (both after-arm, BE, gzip):

| probe | link | observed |
|---|---|---|
| `f1` | `abs-out -> /etc/passwd`, `abs-in -> /plain.txt` | **kept**: two `unpublished-entry` gaps, `unpublished_entries[].link_target` = `etc/passwd` and `plain.txt`, **no** `MaliciousSymlinkRemoved`, 2 files published |
| `f2` | `abs-dotdot -> /../../outside.txt` | **removed**: `MaliciousSymlinkRemoved` with `target` `../../outside.txt`, no gap, 1 file published |

So the exact rule to freeze is:

1. absolute target → drop the leading `/` and interpret the remainder **relative to the image
   root**; inside → kept (rewritten), one `unpublished-entry` gap; outside → removed
   (`MaliciousSymlinkRemoved`), no gap;
2. relative target → resolve against the link's own directory; inside → kept, one gap; outside →
   removed, no gap.

Two consequences:

* **C1's frozen `symlinks.tsv` `in-tree | escaping` classification must use rule (1)/(2), not
  POSIX resolution of the raw target.** A POSIX-resolved `/etc/passwd` is *outside* the root, so a
  POSIX-only oracle would label it `escaping` while unblob keeps it — the predicate would then
  demand "no gap" for a carrier that has one. No K1–K4 carrier has an absolute link (K1/K2 `src/`
  trees carry only relative links; K3/K4 after-receipts carry no `unpublished-entry` at all), so
  this is a K5/K6 freeze risk, not an existing defect.
* **`unpublished_entries[].link_target` in the envelope is the *sanitised* target**, not the
  image's stored bytes: `/plain.txt` arrives as `plain.txt`, and an escaping link's
  `diagnostics[].report.target` is the rewritten relative path (`../../outside.txt` for
  `/../../outside.txt`). An oracle that compares link targets verbatim will mismatch on absolute
  links. Compare `relative_path` only, or normalise both sides.

Also confirmed (K2's own source tree): `K2/src/var/lib/run-link -> ../../a/run.sh` is **in-tree**.
Two `..` from `var/lib` land on the root. A `..`-counting or "target starts with `..`" rule would
misclassify the lane's own K2 carrier. The rule is resolution, full stop.

### F2 (material, C2) — a carrier with one link of each kind is `unclassified`

`e1` (BE, one in-tree link `alias.txt -> plain.txt` **and** one escaping link
`esc.txt -> ../../outside/x.txt`) produces `G = {unpublished-entry}`, `SR = yes`, `P = 2`. Under
the 7-row table that matches neither `escaping-symlink-removed` (needs `G = none`) nor
`in-tree-symlink-metadata` (needs `SR = no`) → `unclassified` (verified, `labels-7row.tsv`).

Either the frozen `heldout-gen.py` must guarantee **at most one symlink kind per carrier** (which
is what the class names imply — "only an escaping", "only an in-tree"), or the table needs one
extra row. A row that fixes it, scoring 21/21 including `e1`:

```
| mixed-symlink-outcomes | squashfs_v4* | unpublished-entry | none | n/a | yes | >0 | … | … |
```

I did **not** put this row in the 7-row candidate; both variants are in the artifacts so the L1
can pick with the numbers in hand (`labels-7row.tsv` 20/21, `labels-8row.tsv` 21/21).

### F3 (material, C2) — `-be in child argv` is inert on all four classes

BE is `n/a` in 8 of 8 class runs, and in every clean/symlink envelope I looked at: a
`sasquatch`-naming `command` only exists in `diagnostics[].report` when a **stage report** exists,
and a clean extraction emits none. BE is therefore `yes`/`no` only on extractor-failure envelopes:

* `be-meta-damaged` (inode table corrupted) → `sasquatch-v4be -be -no-exit-code …`,
  gap `extractor-failure`, `P = 0` → **BE = yes**;
* `avm-k1` (round-38 marker probe) → `sasquatch-v4be -no-exit-code …`, gap `extractor-failure`,
  `P = 0` → **BE = no**.

That pair is exactly the `body-extractor-failure` vs `avm-marker-be-dropped` separation the claims
ask for, and it is the *only* job the BE cell can do. Consequences for the table:

* **Never** use the BE cell to separate BE from LE — use `handler` (`squashfs_v4_be` vs
  `squashfs_v4_le`). A row with `-be = yes` and `gap kinds = none` can never match anything.
* BE=yes is reachable only with a real BE extractor failure, so any class that depends on it must
  actually fail extraction. A held-out "body damage" carrier that sasquatch still extracts will
  label `clean` (see F4).

### F4 (design limit, C2) — the table cannot see byte damage when the extractor succeeds

`be-body-damaged` (bytes 96..175 of a clean BE image overwritten with `0xAA`) **still extracts 4
files**, `coverage complete`, no gap, no diagnostic → grammar-identical to `clean`. The round-37
writer stores blocks raw when compression does not shrink them, so corrupting small-file data
neither fails the extractor nor changes the file count. `body-extractor-failure` must therefore be
defined as *the extractor exited non-zero* (gap `extractor-failure`), and byte-content damage must
be caught by oracle `sha256` comparison, never by this table. A held-out "damaged" carrier must be
built to fail the extractor (e.g. damage the inode/directory table, as `be-meta-damaged` does).

### F5 (spec ambiguity) — `*` in the `-be` / `symlink removed` cells

The contract states "`*` matches anything" for condition cells generally, then gives
`-be`/`symlink removed`: `yes`/`no`/`n/a` with no `*`. Both readings are defensible. My reference
interpreter accepts `*` everywhere (documented in-code) **and** both candidate tables use explicit
values in those two columns, so they score identically under either reading. Recommendation: the
frozen interpreter should reject `*` in those two cells (a narrower grammar cannot silently
mis-match), and the frozen table should never need it.

Related trap: `symlink removed` can **never** be `n/a`. SR is defined as `yes`/`no` only, so an
`n/a` cell in that column matches nothing at all. Only the BE column has a reachable `n/a`.

### F6 (expressiveness limit) — the grammar collapses gap multiplicity

`G` is a *set of kinds*, so `f1` (two in-tree links, two gaps) and `d1` (one) are the same feature
vector. Any class distinguished only by the *number* of gaps is inexpressible. This is fine for
C2 (classes differ by kind) and irrelevant to C1 (which counts gaps per oracle row), but the
held-out generator must not create a class whose only signal is a count.

### F7 (grammar consequence, not a defect) — `clean` merges BE and LE

Classes (a) and (b) both label `clean`; the label says nothing about endianness. If the frozen
class list wants a BE/LE split it must be two labels (`clean-be`, `clean-le`) with
`handler = squashfs_v4_be` / `squashfs_v4_le`. The draft class list has a single `clean`, which is
consistent with the evidence.

### F8 (C1 corroboration) — the escaping-symlink outcome carries no gap, but `coverage` is `partial`

`c1`/`c2`/`f2`/`k1-after` all publish files, record `MaliciousSymlinkRemoved`, and carry **zero**
gaps, yet `coverage` is `partial`. So `coverage` is not a gap proxy and must never be used as one
(it is also not a grammar feature). This matches the draft C1 predicate's "gaps of kind
`unpublished-entry` exactly on the in-tree symlinks and no other gap".

## 6. Grammar feasibility probe (what the frozen interpreter can express)

`sqfs-triage-ref.py` implements the contract literally — marker-in-section table discovery, exact
header order, backtick/space stripping, `none` vs `a+b` **set equality**, `handler` via
`fnmatchcase` against at least one element of H, `0`/`>0`/`*` on `P`, first-match-wins,
`unclassified` on no match, **exit 2 on any malformed cell** — and reads both a bare `data`
object and a full `{ok,data,meta}` envelope.

* `--selftest`: 0 failures across 18 cases (10 accepting: bare data, full envelope, `-be` from a
  string command, `-be` from an argv-list command, dependency **superset is a non-match**, two-name
  set, `MaliciousSymlinkRemoved` recovered from `raw_result.report`, …; plus 8 malformed-table
  cases).
* On the real `SKILL.md` (no marker yet) it exits **2** — the "unmoved at base" behaviour the C2
  counter needs.
* 7-row candidate: 20/21 envelopes labelled, `e1` unclassified (F2). 8-row candidate: 21/21.
* Two independent feature implementations (`featurize.py` and the interpreter's own `features()`)
  agree on H/G/D/BE/SR/P for all 21 envelopes.

The candidate rows I would hand the L1 (condition cells only; cause→action and source are in
`candidate-table-fragment.md`, each row carrying a file:line or receipt citation):

```
avm-marker-be-dropped   | squashfs_v4_be | extractor-failure           | none            | no  | no  | 0
body-extractor-failure  | squashfs_v4_be | extractor-failure           | none            | yes | no  | 0
dep-missing-be          | squashfs_v4_be | missing-extractor-dependency| sasquatch-v4be  | n/a | no  | 0
dep-missing-le          | squashfs_v4_le | missing-extractor-dependency| sasquatch       | n/a | no  | 0
escaping-symlink-removed| squashfs_v4*   | none                        | none            | n/a | yes | >0
in-tree-symlink-metadata| squashfs_v4*   | unpublished-entry           | none            | n/a | no  | >0
clean                   | squashfs_v4*   | none                        | none            | n/a | no  | >0
```

`dep-missing-le` is the one row **not exercised by my runs** (I ran no before-arm, per the item);
its shape is the round-38 `K1/before` receipt with `handler`/`dependencies` swapped, i.e.
`D = {sasquatch}` for the LE path, read from `FirmwarePublication.js:208-215` plus unblob's
`EXECUTABLE`/`V4BE_EXECUTABLE` split. [INFERENCE] on the LE dependency name; the L1 should confirm
it in a before-arm on a dev LE carrier before freezing that row.

## 7. Limits and non-claims

* **L1.** No K5/K6 carrier was built, copied, or run through REA; no held-out carrier was built or
  run. The only non-development envelopes touched are read-only copies of round-38 receipts and
  the round-38 AVM probe.
* **L2.** All runs are after-arm. `dep-missing-le` (and the LE half of the dependency rule) is
  inferred, not measured, here.
* **L3.** Class (c)/(d) trees each carry exactly one link. Multi-link carriers are covered only by
  `e1` (mixed) and `f1` (two in-tree) probes.
* **L4.** No absolute or mixed-link behaviour is claimed for *vendored* images; my probes are
  round-37-writer images, whose symlink inode layout is the writer's, not a vendor's.
* **L5.** `is_safe_path` resolves with the kernel, so a relative target whose *intermediate*
  component is itself a symlink is resolved through it. No dev tree or K1–K4 carrier has such a
  link; the lexical-vs-kernel distinction is unexercised. [INFERENCE] that lexical POSIX
  resolution agrees with unblob for all realistic symlink tables.
* **L6.** "Regenerates byte-identically from the seed" is not demonstrated: the round-37 writer has
  no seed parameter. What I showed is that the writer is deterministic given a tree (14/14
  `cmp`-identical across two fresh rebuilds). A `heldout-gen.py` seeded by the freeze commit hash
  must derive *tree contents* from the seed and then call the writer; the writer itself cannot be
  the seed consumer. This is a freeze-design constraint for the L1, not a defect in my evidence.
* **L7.** No claim about AVM-BE bodies beyond the round-38 probe envelope: `avm-k1` is quoted, not
  re-run.
* **L8.** Scratch was removed; every cited envelope, image and script is copied into the artifacts
  directory.

## 8. Artifacts (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-39/w1/artifacts/R39C2ReconClean/`)

| file | contents |
|---|---|
| `build-dev-carriers.sh` | authors the 12 trees and builds 12 images with the round-37 writer |
| `make-damaged.py` | derives `be-body-damaged.sqsh` and `be-meta-damaged.sqsh` from `a1.sqsh` |
| `run-rea-dev.sh` | the exact after-arm REA invocation for every carrier |
| `featurize.py` | grammar feature extractor + per-run detail (independent of the interpreter) |
| `sqfs-triage-ref.py` | reference implementation of the triage grammar + 18-case selftest |
| `candidate-table-fragment.md` | 7-row candidate table in the contract's exact shape |
| `candidate-table-mixed-fragment.md` | 8-row variant adding `mixed-symlink-outcomes` |
| `env/*.json` | 14 kept after-arm envelopes (full `{ok,data,meta}`) |
| `known/*.json` | 7 read-only copies of pre-existing envelopes (round-38 receipts + AVM probe) |
| `carriers/*.sqsh` | 14 images, byte-identical to a fresh rebuild |
| `carrier-sha256.txt` | sha256 of every carrier |
| `feature-table.md` | the §4 table, machine-generated |
| `features-all.json` | H/G/D/BE/SR/P + detail for all 21 envelopes |
| `labels-7row.tsv`, `labels-8row.tsv` | interpreter output for both candidate tables |
| `selftest.txt` | `--selftest` transcript and exit code |

Report: .ufo/waves/round-39/w1/R39C2ReconClean.md
