# R36W2MutantC1Landed — mutation test of the landed C1 evidence (wave 2)

Seat: R36W2MutantC1Landed (leaf, wave 2). Lane: `kaidoku-shokunin`. Target of attack: the landed
C1 evidence bytes at `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95` (C1 + assimilation landing), scored
with the frozen c1-counter. Detector: `tools/round-36/c1-counter.py` as frozen at
`790561d4e3aca732a434081aa9573ec2fa5fd7d0`. Date: 2026-10-26.

**Verdict: 5 of 7 mutants killed, 2 survived.** Both survivors hit the same binding — the
`sourced` provenance check is existential, so partial provenance rot on the landed C1 chain is
invisible to the score.

## Method

Fixture repo built exactly per bounds, then scored with the frozen counter bytes:

```
S=/fast/scratch/hyaku/kaidoku-r36/R36W2MutantC1Landed
mkdir -p "$S"; export TMPDIR="$S" HYAKU_SCRATCH="$S/hs"
D=$(mktemp -d "$S/fx.XXXX")            # -> $S/fx.cXJK
git -C "$D" init -q
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin archive ffc813417d3bceeeb7b028b12ce0be8a5dc33d95 | tar -x -C "$D"
git -C "$D" rev-parse --show-toplevel  # == $D, verified before first commit
git -C "$D" add -A && git -C "$D" -c user.name=r36w2-mut -c user.email=mut@scratch commit -q -m base-ffc8134-tree
git -C "$D" fetch -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin main   # real freeze + ffc8134 objects, fixture-only
```

- Tree equality proof: fixture base tree `0197338a6a114979fb448ed84503fc5c330850ea` ==
  `git rev-parse ffc8134^{tree}` in the fixture. `git merge-base --is-ancestor 790561d4 ffc8134` →
  true in the lane, so the real freeze object resolves in the fixture and `--freeze 790561d4…` is the
  genuine frozen reference (needed because `after.json`/`after-run.json` gained lines between the
  freeze and the landing — a synthesized freeze would not have been equivalent).
- Frozen-detector proof: counter blob `654c3cd0ec2ec0152cdc420cdd5d8e6799c2951c` identical at
  `790561d4` and at tip `01a44dbf`; `git status --porcelain -- tools/round-36/c1-counter.py` empty,
  so the worktree file executed is the frozen bytes. No counter/carrier/oracle bytes were changed.
- Environment sanity: `--selftest` → `{"selftest": "c1-counter", "cases": 14, "green_ok": 1,
  "red_ok": 13, "failures": []}`, exit 0. node v24.21.0; `--pkg65
  /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` present.
- Per mutant: `git -C "$D" checkout -q -B mut ffc8134…` → single edit → commit →
  `python3 -I -B tools/round-36/c1-counter.py --root "$D" --rev <mut-sha> --freeze 790561d4… --pkg65 <pkg> --json-out $S/receipts/<name>.json`; exit code recorded. Mutants are commits parented on the
  real `ffc8134`; each is exactly one changed file.

## Baseline (unmutated ffc8134)

Exit 0, `met_target: true` — detector is green on the landed state before any mutation:

```
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107", "S108", "S109"],
"opened_source_rows": ["S107", "S108", "S109"], "province_core_row": true, "province_core_section": true,
"sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true,
"revision": "ffc813417d3bceeeb7b028b12ce0be8a5dc33d95"}
```

## Mutants and verdicts

| id | mutation (single file) | before blob → after blob | mutant commit | exit | decisive counter fields | verdict |
|---|---|---|---|---|---|---|
| M1 | `corpus/evidence/round-36/c1/K1/after.json`: published `files[2].sha256` of `payload.bin` flipped `…fe11824f`→`…fe11824e` (`reported_sha256` and the raw_result HashReport left true) | `0595e242` → `b5d65893` | `d65bc269` | 1 | `carriers_matched 3`; K1 `after_oracle_hits 2/3`, `after_evidence_id_ok false` | **killed** |
| M2 | `corpus/evidence/round-36/c1/K1/oracle.tsv`: row `README.txt 88dc952a… 59` deleted at the rev | `edd39fab` → `4706b629` | `14473b10` | 1 | `carriers_matched 3`; K1 `oracle_frozen false` | **killed** |
| M3 | `PROVINCE.md:368`: heading `## Round-36 additions to Core` → `## Round-36 additions to Core (moved from Frontier)` | `fbeeaee9` → `cdcd59ae` | `6a72733d` | 1 | `province_core_section false`, `province_core_row false` (carriers still 4/4) | **killed** |
| M4 | entry `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`: the whole `source: S107 — …not any carrier` line removed (one of three `source:` lines) | `26758b59` → `7c8ad5e1` | `3216c72d` | **0** | `entry_source_ids [S108,S109]`, `sourced true`, `met_target true` | **SURVIVED** |
| M5 | `corpus/SOURCES.md:113` (S107 row): used-by cell `…r36-sasquatch-squashfs-recursion.md` → `…2026-10-26-unblob-sasquatch-dependency.md` | `c1b5ec4a` → `c82f61d3` | `7a92273d` | **0** | `opened_source_rows [S108,S109]`, `sourced true`, `met_target true` | **SURVIVED** |
| M6 | `corpus/README.md:89` (Coverage map row): stem typo `…squashfs-recursion` → `…squashfs-recusion` | `e36597da` → `a0b07d4f` | `befdcebc` | 1 | `coverage_map_row false` | **killed** |
| M7 | `corpus/evidence/round-36/c1/carriers.json`: whitespace only (indent 2→3 spaces on line 2) | `99e34e84` → `ce563ead` | `0299c7ee` | 1 | `carriers_unchanged false` | **killed** |

Full blob shas: before `0595e242fb8f2b53fb78895eefa25492c35f59f1`, `edd39fabbb74f9c4b3d000bfc20f2ed1a3034c73`, `fbeeaee92b4e48d812be05774ee9ce33835d65ae`, `26758b599f4d5f4fb468be987a53d6b97b4426dd`, `c1b5ec4aaf0186e05adb13f4282eaf35bc1999dc`, `e36597da6b41468421278045f1d2ad17338f28a1`, `99e34e84467756a1b65d3250252dbeab36b4c322`; after `b5d658936e39430803a8249d427b8d3f47cab908`, `4706b6294ae233bb73c243efbc4d39c1fbdbffe7`, `cdcd59ae6cee2d981f2294484c17c4df6bde012d`, `7c8ad5e168c85c57aeeb2fc656e879dd7a111ddb`, `c82f61d3de214de31bec3bcf39d7e76fc9968cce`, `a0b07d4ff1c811aa274a342b6933933d75474903`, `ce563ead76175ed7c6136ac70ae729bf37aacffe`.

Counter stdout for the two survivors:

```
M4: {"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S108", "S109"],
     "opened_source_rows": ["S108", "S109"], "province_core_row": true, "province_core_section": true,
     "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true,
     "revision": "3216c72deb0cb90458bbb28141defe30e5d0f6a3"}   exit 0
M5: {"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107", "S108", "S109"],
     "opened_source_rows": ["S108", "S109"], "province_core_row": true, "province_core_section": true,
     "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true,
     "revision": "7a92273d8ef19ee23db377c026bb4fc6c20dbbb0"}   exit 0
```

## Survivor analysis — one weakness, two entry points

Root cause, `tools/round-36/c1-counter.py:213-225` (frozen bytes):

```python
ok_ids = []
    ...
    if c[0] in src_ids and c[8] == OPENED and ENTRY in used:
        ok_ids.append(c[0])
b['opened_source_rows'] = sorted(ok_ids)
b['sourced'] = bool(ok_ids)
```

`sourced` is true when **at least one** cited source row is opened 2026-10-26 with the entry in its
used-by. There is no completeness check that every id on the entry's `source:` lines has an ok row,
and no check that any particular row stays cited.

- **M4** (entry loses its `source: S107` line): the counter re-derives a smaller but internally
  consistent provenance set (`[S108, S109]`) and scores `met_target true`. The round's headline
  provenance row — S107, the sasquatch release that grounds the install provenance — becomes
  silently uncited while the claim stays green.
- **M5** (S107's used-by stops listing the entry): `entry_source_ids` still names S107 but
  `opened_source_rows` drops it; the entry↔registry inconsistency the predicate is about is
  invisible while any other cited row remains consistent.

Calibration of the finding: the frozen predicate wording (`plans/round-36-claims.md:28`) is itself
existential — "which cites a SOURCES.md row opened 2026-10-26 whose used-by lists that entry" — so
the counter implements the frozen predicate faithfully; **[INFERENCE]** the weakness is the
predicate's strength, not a counter/predicate divergence, and the predicate is frozen and must not
be edited. It is a landed-state weakness: the C1 score cannot distinguish a fully-cited chain from
a partially-rotted one. This is the same counting shape the round itself named for C2 (lesson
M36-3, class A3 "first match only" / partial-match counting) — it also holds on C1's `sourced`
binding. Boundary, from code not probed (the seven assigned mutations were the mandate):
`[INFERENCE]` if all cited rows fail or the entry cites nothing, `ok_ids` is empty and `sourced`
goes false — total provenance loss is caught, only partial rot is not.

## What the killed mutants confirm

The landed evidence's load-bearing parts are individually detectable: receipt content (M1 — both
oracle-hit matching and 6.5.0 evidence-id recomputation catch a flipped published sha), oracle
frozenness at the rev (M2), exact Core heading + row presence (M3), the Coverage map row's stem
(M6 — the map row at `README.md:89` is the only Coverage-map row carrying the stem; the other stem
occurrences at `README.md:195,233` are outside the `## Coverage map` section), and the carrier
freeze (M7 — byte-level, so even whitespace is caught).

## Restoration evidence

After each mutant's scoring, `git -C "$D" checkout -q -B mut ffc8134…` restored the tree; the
restored blob matched the before blob in every case (restored values in the table order above:
`0595e242…`, `edd39fab…`, `fbeeaee9…`, `26758b59…`, `c1b5ec4a…`, `e36597da…`, `99e34e84…`).
Final state: `git -C "$D" diff --stat ffc8134 mut` → empty (0 lines); `git rev-parse mut^{tree}`
== `ffc8134^{tree}` == `0197338a6a114979fb448ed84503fc5c330850ea`. The lane's VCS was never
mutated (no add/commit/checkout/reset in the lane; the only lane write is this report file).
Pre-existing concurrent dirt observed in `git status --porcelain` (`.ufo/waves/round-36/after/
c1-final.json`, `c2-final.json` modified; sibling w2 reports untracked) is other seats' work —
not touched.

## Tooling record

No tools installed or upgraded (operator authorization 2026-10-19 noted; nothing was needed:
system `python3`, `node` v24.21.0, `git`; no pacman transactions; no REA runs — the counter's
evidence-id recomputation used the pre-existing pkg65 npx cache). Scratch
`/fast/scratch/hyaku/kaidoku-r36/R36W2MutantC1Landed` (incl. fixture `fx.cXJK` and receipts
`baseline.json`, `m1…m7*.json`) removed after this report was written; all cited outputs are
embedded above.
