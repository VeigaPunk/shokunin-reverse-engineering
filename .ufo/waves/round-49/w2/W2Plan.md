# W2Plan — round 49 wave 2: plan vs frozen bytes (post-landing)

Seat: W2Plan (leaf, read-only on the lane). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
FREEZE `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`; REV (landing) `29883d4ec35a31a8393c4ffb220888c44c0bb022`.
Receipts and the falsification driver: `.ufo/waves/round-49/w2/W2Plan/` (`sha256sums.txt` lists every hash below).

## Verdict

**Both counters reproduce the plan's expected results at REV and at FREEZE, and the frozen tools measure what their
code says they measure for the R49-C1 carrier clauses and the R49-C2 atoms A1–A6, A9 and the battery.** The plan is
not clean against its own text: **2 P49-C2 sentences disagree with the code** (A8 "exactly one round-48 entry"; A7
"no other status for EX_USAGE"), each shown by an in-process test in which a planted defect leaves the atom green while the
counter still exits 0. **1 P49-C1 freeze sentence disagrees** (the round-44 carriers path is named as frozen and is not),
and **1 P49-C1 predicate sentence is not bound by the code** (the counter-time REA rerun is not tied to `--pkg65`).
None of these changes a REV result (C1 4/4 exit 0; C2 mismatches 0, exit 0). Wave-1 amendment record (8 rows): 5 TRUE
outright (rows 1, 2, 3, 4, 6); 3 TRUE only with a qualification recorded as a finding (row 5: F7/F8; row 7: F2; row 8: F9).
No counter bytes were patched; nothing was committed.

## Findings (ordered by weight to the claims)

| # | claim | severity | disposition vs plan | what | exact evidence |
|---|---|---|---|---|---|
| F1 | R49-C2 A8 | medium (calibration) | **disagrees** | The plan says `## Search log` "carries exactly one round-48 entry (marked late entry)". The counter filters to entries containing `late entry` *before* counting (`ent = [l for l in ent if 'late entry' in l]`), so a second, non-late round-48 entry is never counted. An extra round-48 entry passes all nine atoms. | `frz/tools/round-49/c2-mismatch.py:514–519` (filter at 516). Test `falsify_c2.py` T1: REV `corpus/SOURCES.md` + duplicate of the round-48 line with ` (late entry, written in round 49)` removed → `red []`, exit would be 0. Output `falsify_c2.out` line 1. |
| F2 | R49-C2 A7 | low (calibration) | **disagrees (narrow)** | Amendment record and P49-C2 say A7 requires "`EX_USAGE is 64` and no other status". The counter rejects only `EX_USAGE is <non-64>` (regex `EX_USAGE is (?!64\b)\S`). `EX_USAGE = 2` or `EX_USAGE 2` in the S148 teaches cell is accepted. | `c2-mismatch.py:493`. Test T2: REV S148 teaches `EX_USAGE is 64` + appended ` and EX_USAGE = 2 in this lane` → `red []`. Sanity T3 (`EX_USAGE is 2`) → red A7, so the regex does work for the form it checks. |
| F3 | R49-C1 P49-C1 predicate "counter-time REA rerun" + `--pkg65` in counting command | medium (binding) | **unbound (code-read)** | `--pkg65` feeds only `evidence_ids()` (the id recompute, sha-checked against the frozen `rea-pkg.json`). The rerun is `npx -y rea-agents@6.5.0 extract-firmware …` with `env = dict(os.environ)` (only PATH and `REA_UNBLOB_COMMAND` overwritten). So the package the rerun executes is whatever npx resolves from the inherited environment (e.g. `npm_config_cache`), not the package whose sha256 was checked. Today both resolve to `…/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (path equality checked against `rea-pkg.json` `package_root`); the code does not enforce it. [INFERENCE] on exploitability: not exercised. | `frz/tools/round-49/c1-counter.py:1893–1897` (env, argv), `:604–636` (`evidence_ids` takes pkg65), `make_real_runner(work, unblob, timeout)` signature at ~1874 has no package parameter. |
| F4 | R49-C1 freeze rule | low (plan-internal) | **disagrees (no score effect)** | Freeze paragraph: "C1 additionally freezes … the committed carriers under `corpus/evidence/round-44/carriers/`". The counter freezes the four carrier paths named in `carriers.json` (`corpus/evidence/round-42/c2/fixtures/…`, via `_frozen_paths`) and `corpus/evidence/round-44/oracle/` by prefix; `round-44/carriers/` is in neither `FROZEN_PATHS` (c1-counter.py:280–293) nor `FROZEN_PREFIXES` (:294). The two files there (`squashfs_v2.1_{le,be}.bin`) are v2.1, which the claim says stays unbound, so editing them cannot move the score. The plan's own "Frozen paths" list omits the directory too. | `git ls-tree -r decc5697… -- corpus/evidence/round-44/carriers` → 2 blobs. |
| F5 | R49-C1 predicate "regular file at the freeze and at the measured revision" | low | **unchecked explicitly; agrees by implication** | `carrier_present` checks `blob_mode(root, rev, path) == '100644'` at REV only (`c1-counter.py:2050–2053`). Freeze-time regularity is not tested. It is implied because `frozen_drift` treats any `M` in `git log --name-status` (mode change included) on a frozen carrier path as drift, and the freeze tree shows the four carriers as 100644. | `git ls-tree decc5697… -- corpus/evidence/round-42/c2/fixtures/` (100644 ×4 carriers, verified). |
| F6 | R49-C1 predicate "no extra regular file" | low | **narrower than text** | The oracle clause counts extra files only under the chunk root: `extra_published` → `published_rels` → `extract_rel` (`c1-counter.py:1455–1472`). A regular file published outside the root is not counted by `oracle_hits_ok`. It is still rejected in practice by `evidence_id_ok` (the id covers the envelope) and by `projection_ok` (the committed file list must equal the rerun's). | code-read; not separately tested. |
| F7 | R49-C1 runner "write scope" (amendment row 5) | low | **guard wider than the row says** | `allowed_roots` includes the whole scratch base (`/fast/scratch/hyaku`), so `--evidence-root /fast/scratch/hyaku` passes the write-scope guard (`c1-run.py:838–848`). `--force` then `shutil.rmtree`s `<evidence-root>/<carrier-id>` (`clear_outdir` 514–527, `outdir = join(evidence_root, cid)` at 338). Deletion is limited to dirs named exactly `v1le|v1be|v2le|v2be`, but it is outside `kaidoku-r49/`. | code-read; the runner is not a counter and not run here (no `--data-run`, as instructed). |
| F8 | R49-C1 runner "copy failure fatal" (amendment row 5) | low | **partial** | The REA-tree verbatim copy is fatal (`c1-run.py:602`). The unblob log tee copy is not: `cp -- "$log" "$C1_LOG_COPY" || echo … >&2` (`:152`), and a missing `unblob.log` is silently omitted (`:638–641`, `unblob_log` path None). Not a counter clause; the committed `unblob.log` files exist for all four carriers. | `c1-run.py:152, 638`. |
| F9 | R49-C2 "every round-48 input read at the base" (amendment row 7) | none (effect) | **partial, agrees in effect** | A1 reads the stale lesson header at REV (`c2-mismatch.py:291`). Line 310 requires `sha(REV lesson) == sha(base lesson)`, which forces REV == base. No effect; wording differs. | code-read. |
| F10 | R49-C1 P49-C1 toolchain sentence "sasquatch 4.5.1 on the child PATH" | info | **unchecked by counter** | The counter checks unblob through `engine` in the projection (`plus-extractor`), not sasquatch. Host `~/.local/bin/sasquatch` reports `unsquashfs version 4.5.1` on `-v`; `unblob --version` is 26.6.4. Sasquatch version is not compared anywhere. | `c1-counter.py:1849–1871` (PROJECTION_KEYS), `:1722–1845` (projection). |

## Wave-1 amendment record — frozen-byte check (one row per table row)

| row | disposition as stated | frozen bytes at `decc5697` | verdict |
|---|---|---|---|
| 1 provenance | `provenance_ok` is prefix test `/fast/scratch/hyaku/kaidoku-r49/`; claim re-scoped; relabel + oracle fabrication disclosed | `provenance_ok` `:1184–1191` (isabs, no `..`, `startswith(PROV_BASE)`); selftest cases `:3148–3174` (`/tmp`, lane-path segment, `..`, `/kaidoku-r42/`) | TRUE |
| 2 quiet rule / freeze walk / clauses named / target | `nonregular_unpublished_ok` quiet rule; added file under `tools/round-49/` counts; extra clauses in docstring; `TARGET = 4` | quiet `:1980–1981`; `FROZEN_PREFIXES` `:294`, add-branch `:1664–1675`; docstring names `carrier_size_ok`, `carve_ok`, `oracle_ok`, `carrier_fresh_ok`, `receipt_fresh`, `frozen_tables_valid`; `TARGET = 4` `:259` | TRUE |
| 3 controls | CTL-C1-5 retired; CTL-C1-4 plants round-44 receipts verbatim | `c1-controls.py` lines 45 (retired), 758–778 (verbatim copy); controls receipts `.ufo/waves/round-49/controls/c4/counter.json`: red only on `run_provenance_ok` | TRUE |
| 4 selftest | six cases: quiet-carrier gap, unpublished row, provenance under `/tmp`, provenance with lane-path segment, added file under frozen dir (+1 unnamed) | cases at `:3137, 3141, 3148, 3152, 3227`; `--selftest` run here: 52 cases, `failures []`, exit 0 | TRUE |
| 5 runner | id regex; evidence-root write scope; `--fake-rea` never committed; copy failure fatal; `outdir_mode` default `scratch` | id regex `c1-run.py:240` (fullmatch `[a-z0-9]{2,8}`); scope `:838–848`; fake `:849–851`; REA-tree copy fatal `:602`; default `scratch` `:332, :801–805` | TRUE except copy-fatal on the log tee (F8) and scope wider than stated (F7) |
| 6 docs bindings | presence checks, disclosed | `bindings` in `measure()` `:2200–2240`; REV `PROVINCE.md:438` has the Round-49 frontier note | TRUE (disclosed) |
| 7 C2 reads / A3 sets / duplicates / A7 / A8 / word counts / battery / freeze | as listed | A3 sets `:~100–101, :339–360` (`LOG_KEYS` incl. c093e798, `UNNAMED` incl. 7fe11332); duplicates → mismatch via `ctx_for` and `sections()` length checks; A8 fields `:520–531`; word counts `_check_quotes` `:~455–466`; battery 16 `N_MUT` `:107`, `:654–677`; `counter_not_frozen` `:690–700` | TRUE for A3, duplicates, A8, word counts, battery, `counter_not_frozen`; PARTIAL for A7 (F2); A1 read-at-REV (F9) |
| 8 scope note "every round-48 input read at base" | (merged into 7) | see F9 | PARTIAL (agrees in effect) |

Summary: 8 rows checked: 5 TRUE (rows 1, 2, 3, 4, 6), 3 with qualification (row 5: F7/F8; row 7: F2; row 8: F9).

## Sentence trace (P49-C1 and P49-C2 → counter code, once more at `decc5697`)

Legend: AGREES / DISAGREES / UNCHECKED. Line numbers are `frz/tools/round-49/c1-counter.py` unless marked `c2:`. A number written `~N` is approximate (±10 lines, read from `sed -n` windows); the function name is the authoritative anchor.

### P49-C1

| # | plan sentence (paraphrase, cited) | code | status |
|---|---|---|---|
| C1.1 | after-receipt is a committed REA 6.5.0 extract-firmware receipt first added in a commit descending from the freeze | `receipt_fresh` `:2099–2101` (`first_add` = oldest `A` commit `:1583`), `is_ancestor` `:1591` | AGREES |
| C1.2 | names the carrier's frozen `squashfs_v1`/`squashfs_v2` handler | `handler_ok` `:1953–1957` (squashfs handler list == `[handler]`) | AGREES |
| C1.3 | no failed chunk | `chunks_ok` `:1958` (`chunk_failed` `:1428`) | AGREES |
| C1.4 | publishes every regular oracle file at exact relative path under the chunk root with same sha256 and size | `oracle_hits` `:1439`, `oracle_hits_ok` `:1974` | AGREES |
| C1.5 | "and no extra regular file" | `extra_published` `:1467` under root only | DISAGREES-narrow (F6) |
| C1.6 | accounts for non-regular oracle rows by the frozen gap rule; structural allowance 0 | `disposition_check` `:1499–1581`; `GAP_RULE` `:~345–365` | AGREES |
| C1.7 | `gaps == []` and `unpublished_entries == []` (all four oracles hold no non-regular member) | `quiet_ok` `:1980–1981`, `gaps_ok` `:1960s` | AGREES (quiet rule applies because `nonreg` is empty for all four; verified in `carriers.json`) |
| C1.8 | subject digest equals carrier pin | `subject_pin_ok` (evaluate_carrier) | AGREES |
| C1.9 | recomputes its evidence id under the rea-agents 6.5.0 rule | `evidence_ids` `:604`; `rea_package_problems` `:569` (pkg65 sha-checked vs frozen `rea-pkg.json`) | AGREES |
| C1.10 | carrier bytes hash to the pin | `carrier_pin_ok` `:2056` | AGREES |
| C1.11 | carrier a regular file at the freeze and at REV | REV only `:2050–2053` | UNCHECKED explicitly (F5, agrees by implication) |
| C1.12 | superblock reads frozen magic, s_major, s_minor, endianness, observed compression class | `layout_probe` `:1078–1183` | AGREES |
| C1.13 | committed `__output__` tree (S138) reproduces census rows and frozen digest | `tree_check` `:2273–2302`; `output_tree_binding` `:828–871` | AGREES |
| C1.14 | counter-time REA rerun of the same bytes has the same semantic projection | `projection_ok` `:2120–2131`, `projection` `:1722`, `projection_diff` `:1849` | AGREES for the committed-vs-rerun comparison; rerun *identity* not bound (F3) → PARTIAL |
| C1.15 | `parameters.output_directory` absolute, starts with `/fast/scratch/hyaku/kaidoku-r49/`, no `..` | `provenance_ok` `:1184–1191`; committed values checked: `/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/c1-run.<id>.<pid>/rea-out` ×4 | AGREES |
| C1.16 | PROVINCE `## Round-49 additions to Core` row names squashfs_v1/v2 and cites the entry | `province_core_row` `:~2180–2195` (presence) | AGREES (presence only — disclosed) |
| C1.17 | one line carries `Round-49 frontier note`, stem, SquashFS v1/v2 token | `frontier_note` (presence) | AGREES (presence only — disclosed); the word "supersedes" in the counter docstring is not tested |
| C1.18 | entry exists; `source:` lines cite S138 and S139; both rows `opened` 2026-10-28 with entry in `used-by` | `entry_present`, `sourced`, `opened_source_rows` `:~2196–2215`; SOURCES header is `id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by` so index 8 = opened, 10 = used-by | AGREES |
| C1.19 | `corpus/README.md ## Coverage map` maps the stem | `coverage_map_row` (presence) | AGREES (presence only — disclosed) |
| C1.20 | no frozen C1 path changed after freeze | `frozen_drift` `:1638–1701` (merge-aware `git log -m --diff-merges=first-parent`, blob equality) | AGREES |
| C1.21 | target `carriers_matched == 4`, every binding true, exit 0 | `TARGET = 4` `:259`; `met_target` `:2233–2239` | AGREES (REV: 4, all bindings true) |
| C1.22 | freeze rule: C1 freezes committed carriers under `corpus/evidence/round-44/carriers/` | not frozen; `FROZEN_PATHS` `:280–293`, `FROZEN_PREFIXES` `:294` | DISAGREES (F4) |
| C1.23 | kill rule: CTL-C1-0 or CTL-C1-4 at 4/4 with bindings true, or do-nothing green → stop | controls at FREEZE: c0 exit 1, matched 0; c4 exit 1, red only `run_provenance_ok`; not re-scored here | AGREES (receipts at REV, not re-run) |
| C1.24 | `frozen_tables_valid` = carriers.json parses at freeze | `:2014`, `:2228` (docstring line 182 matches) | AGREES |

### P49-C2

| # | plan sentence | code (`c2:` = `frz/tools/round-49/c2-mismatch.py`) | status |
|---|---|---|---|
| C2.1 | A1: SCORECARD `## Round 48` declared freeze; LOG names it final; closure names 8-hex; lesson header names another; correction line names both; `round-48.md` byte-identical to base | `a1` `c2:~281–316`; identity `:310` (reads REV, see F9) | AGREES |
| C2.2 | A2: closure quotes dead hash; dead is not a commit; real is a commit, ancestor of REV, shares 8-hex | `a2` `c2:~320–337` | AGREES |
| C2.3 | A3: full LOG line-number sets for three pointers; unnamed exactly three; LOG append-only | `a3` `c2:~339–360`; `LOG_KEYS` `:103–105` and `UNNAMED` `:106` | AGREES |
| C2.4 | A4: seats, seats with non-empty `.md` (at `w1/<seat>.md` or `w1/<seat>/`), missing | `a4` `c2:~362–378` | AGREES |
| C2.5 | A5: raw and newline-stripped sha256 of both receipts; closure quotes the stripped 8-hex | `a5` `c2:~380–398` | AGREES |
| C2.6 | A6: S147 `supersedes S145 —`, locator = heading above quote in pinned snapshot, quote ≤25 words, stated count real, quote present, lesson in used-by, S145 byte-identical | `a6` + `_snapshot_row` `c2:~400–470` | AGREES |
| C2.7 | A7: S148 `supersedes S146 —` on sysexits page; quote and count; snapshot carries `EX_USAGE 64`; teaches states `EX_USAGE is 64` and no other status | `a7` `c2:~486–497` | PARTIAL → DISAGREES on "no other status" (F2) |
| C2.8 | A8: exactly one round-48 entry (marked `late entry`) and exactly one round-49 entry; identified/screened/included/excluded and `rows B -> A`; `where searched:`, `stop:`, `exclusion:` (when excluded > 0); screened = included + excluded; identified ≥ screened | `a8` `c2:506–531` | round-49 AGREES; round-48 "exactly one" DISAGREES (F1); fields AGREE |
| C2.9 | A9: exactly one `## Record corrections — round 49` heading with exactly one `- A9 verdict=rejected-harmed …` line; closure states `Admission: **rejected-harmed**` and `| calibration | harmed |` | `a9` `c2:~545–559` | AGREES |
| C2.10 | freeze rule: REV descends from FREEZE; no commit in FREEZE..REV touches `tools/round-49` or plan; blob equality; exit 2 `frozen_path_changed` | `freeze_check` `c2:~575–586`, `touched` `:~150` (merge-aware, `core.quotePath=false`) | AGREES |
| C2.11 | counter refuses if its own bytes differ from FREEZE | `main` `c2:~690–700` (`counter_not_frozen`) | AGREES |
| C2.12 | battery: sixteen single-mutation overlays, each turning exactly its atom red, none a no-op | `mutations` `c2:~598–652`, `battery` `c2:654–677`; `N_MUT = 16` `:107` | AGREES (REV: 16/16 ok) |
| C2.13 | do-nothing overlay (every path changed since FREEZE restored) turns all nine red | `battery` do-nothing `c2:~669–676` | AGREES (REV: 102 paths, nine red) |
| C2.14 | at FREEZE without battery: `mismatches 9`, exit 1 | `main` | AGREES (observed) |
| C2.15 | predicate at REV: `atoms_total 9`, `mismatches 0`, `battery.failing []`, exit 0 | `main` | AGREES (observed) |

## Counting commands run (all exit codes semantic; GIT_NO_REPLACE_OBJECTS=1; HYAKU_SCRATCH=/fast/scratch/hyaku)

Counters were executed from a byte-identical copy of the frozen tools (sha256 equal to `git show <REV>:tools/round-49/<file>` and to `git show <FREEZE>:…`), not from the worktree. `--root` is the lane; `--pkg65` is `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (rea-pkg.json package_root; `package_json_sha256 a500…050a6`).

| run | command (abridged) | exit | stdout sha256 | JSON sha256 | result |
|---|---|---|---|---|---|
| C1 @REV | `python3 -I -B <frozen>/c1-counter.py --root LANE --rev 29883d4e… --freeze decc5697… --pkg65 <pkg> --work <S>/w-rev --json-out <S>/c1-rev.json` | 0 | ae830b210a799c2b5ec6a67dd629562f0b170e46574f3b70646003f6b6b64657 | e904db78d635aa214c2098a3b012024afd3cb88f49c1bb39d85b2e2ee1c42340 | `carriers_matched 4`, `met_target true`, `frozen_path_changed []`, `bindings_false []`; per carrier all 22 clauses True; `projection_diff []` ×4; `evidence_digests` v1le 8a2e8386…, v1be 7b9da824…, v2le b925ff90…, v2be f7afd909… |
| C1 @FREEZE | same, `--rev decc5697…` | 1 | 976af57f9395202fe82a70d5d0e632d4cc3776d74034c2711b3e3e2eeacfa17c | 7abcfdf930aadf6a4059f6ed45ae42fa917ef00d49d0b4b8db0bfa8c6e8d3e46 | `carriers_matched 0`; false bindings: `province_core_section`, `province_core_row`, `frontier_note`, `entry_present`, `sourced`, `coverage_map_row` |
| C2 @REV battery | `python3 -I -B <frozen>/c2-mismatch.py --root LANE --rev 29883d4e… --freeze decc5697… --battery --json-out …` | 0 | 0cad6d5cfb525227be6af09d6cd6b6115818cee4436180a902a8d1847f490f86 | 0cad6d5c… (same) | `atoms_total 9`, `mismatches 0`, `battery.failing []`, 16/16 mutations ok, do-nothing red = A1..A9, 102 changed paths |
| C2 @REV | same without `--battery` | 0 | 5f403b7479a9ee5a657c550079b5fbf54d53fe59c6d63d9e311dbaaec785be6c | 5f403b74… | `mismatches 0` |
| C2 @FREEZE | `--rev decc5697…` | 1 | 7aa900e1f004d3f13117264e85b68a51b9116dab2590da7a00a66c584b2e37f4 | 7aa900e1… | `mismatches 9` |
| C1 selftest | `python3 -I -B <frozen>/c1-counter.py --selftest --pkg65 <pkg> --work <S>/w-self` | 0 | 5e248ebf1ac2867953a1817b802f2da278a1b6dde153a975cfc93f6921182f91 | — | 52 cases, `failures []` |
| F1/F2 falsification | `python3 -I -B falsify_c2.py` (imports frozen `c2-mismatch.py`, `score(Overlay(REV, {SOURCES: mutated}))`) | 0 (script) | 071218c973d5e356379d7f65a82baa284ff28a5f4f8c6c0607023450675cef3b | script sha 62b47b2e8bd3b9d50b912180f409f5c0a28bf59e864506d5333d4f2fafec4ab7 | T1 `red []`, T2 `red []` (should be red); T3 red A7, T4 red A8 (sanity) |

Controls at FREEZE (receipts committed at REV under `.ufo/waves/round-49/controls/`, not re-run): c0 exit 1 matched 0; c1 exit 1 matched 0 (red on v1be/v1le/… `gaps_ok`, `handler_ok`, `projection_ok`, `run_provenance_ok`); c2 exit 1 matched 0 (red only `projection_ok` ×4); c3 exit 1 matched 0; c4 exit 1 matched 0 (red only `run_provenance_ok` ×4); pos exit 0 matched 4. `controls/summary.json` present at REV (blob 74bbda4a…).

## Unchecked / not run

- Runner behaviour (F7, F8) is code-read only; no `c1-run.sh` invocation was made (`--data-run` never run against the evidence root, per contract).
- F3 is code-read; no fake npx cache was constructed to exercise the rerun identity.
- Counter-only: `identified` (A8) and prose are not derivable (disclosed by the claim); A6/A7 bind snapshots, not live pages (disclosed).
- The controls were not re-scored; only their committed receipts were read.

## Tooling record

No tools installed or updated. Read `/home/vgpnk/.omp/agent/RULES.md`; pacman not used. Observed toolchain (versions only): `unblob 26.6.4` (`~/.local/bin/unblob --version`), `sasquatch 4.5.1` (`~/.local/bin/sasquatch -v`), `unsquashfs 4.7.5` (`/usr/bin/unsquashfs`), `npx` under fnm `v24.21.0`, python 3.14.8. `disk-guard.sh status`: /fast/scratch/hyaku 40% used before the run.

## Git

Read-only only (`show`, `ls-tree`, `cat-file`, `rev-parse`, `merge-base`, `log`, `diff`). No commit, stage, stash, or edit in the lane or fleet repo. Scratch `/fast/scratch/hyaku/kaidoku-r49/W2Plan` removed after copying receipts here.
