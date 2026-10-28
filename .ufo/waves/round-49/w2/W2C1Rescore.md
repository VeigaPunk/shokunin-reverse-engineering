# W2C1Rescore — wave 2 (post-landing), attack on the R49-C1 before→after numbers

Verdict: **reproduced.** At the landing revision `29883d4ec35a31a8393c4ffb220888c44c0bb022` the frozen
C1 counter exits 0 with `carriers_matched 4`, `failing []`, `bindings_false []`, `frozen_path_changed []`,
as the plan states. At the freeze `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d` it exits 1 with
`carriers_matched 0`. Field by field, the L1 receipt `.ufo/waves/round-49/l1/scores/c1-at-landing.json`
differs from my landing score in three fields only: `argv`, `counter` (lane worktree path vs my clone path),
and `revision`. The L1 receipt was scored at `b58f9b192aba548b99d250bb896bbc42c654632c`, not at the landing
revision `29883d4e` (one commit later, the S145-restore). No binding, carrier, failing clause or digest
differs. No counter defect changes a number. The findings are a plan/counter prose disagreement, a latent
binding gap in the REA rerun, and provenance observations. None is a miss in the score.

## Setup (receipts in this directory)

- Clean clone: `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/c`, then
  `git -C $S/c checkout -q --detach 29883d4ec35a31a8393c4ffb220888c44c0bb022`; `rev-parse --show-toplevel`
  printed `$S/c`. No commits in any repo. `$S=/fast/scratch/hyaku/kaidoku-r49/W2C1Rescore`.
- Env for every counter run: `TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku GIT_NO_REPLACE_OBJECTS=1`.
- Counter bytes: `git show decc5697…:tools/round-49/c1-counter.py | sha256sum` and the same at `29883d4e…`
  both give `ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f` (= L1 `counter_sha256`).
- Tools: none installed or upgraded. Existing: unblob 26.6.4 (`unblob --version`), sasquatch (banner
  `unsquashfs version 4.5.1`), `/usr/bin/unsquashfs` 4.7.5 (sha256 `461e1fd9…1677c`, equal to the frozen value).

## Scores (counting command, `--root $S/c`, `--pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`)

| # | rev (role) | exit | carriers_matched | failing | bindings_false | frozen_path_changed | stdout sha256 | json file sha256 |
|---|---|---|---|---|---|---|---|---|
| S1 | `29883d4e` (landing) | **0** | **4** | 0 | none | none | `ae830b210a799c2b5ec6a67dd629562f0b170e46574f3b70646003f6b6b64657` | `7a900ce74f84a616d73344680607cc8e6ef614b6ece39e8d01c35f76098cc583` (`c1-land.json`) |
| S2 | `decc5697` (freeze, before) | **1** | **0** | 56 (14 per carrier) | `province_core_section, province_core_row, frontier_note, entry_present, sourced, coverage_map_row` | none | `976af57f9395202fe82a70d5d0e632d4cc3776d74034c2711b3e3e2eeacfa17c` | `a01f996f86feb276356f724bccaf4247a2719fc876afa0e4825a22ffb21cd782` (`c1-freeze.json`) |
| S3 | `4aabb0b4` (data-run commit) | 1 | 4 | 0 | the same six documentation bindings | none | `73186d0a89f512ebd2c1dfd9a9a594bde42ceabe8a0ba2ac3eb77f108cd6293f` | `cf4b6848613604c2a1f21d325ab9e891a2eaaaf02826b5c09208d69e52a79ad8` (`c1-4aabb0b4bf716fb564c8406509c40b0a67457800.json`) |
| S4 | `3847f393` (landing commit 1) | 0 | 4 | 0 | none | none | `8755165df0c19b27f40b9e6e30e6036a8be203c416a0eb5591f11774b0ced2dd` | `1ac2d446eda0e42f3a853097d76096e0dbde10d7f22a5c24deae442d11e70318` (`c1-3847f393.json`) |

Decomposition the numbers support: **carrier coverage 0→4 is caused by the data-run commit** (S2→S3:
`carriers_matched` 0→4 with the six bindings still false); **the six documentation bindings turn true in the
landing commit** (S3→S4: exit 1→0). S4 and S1 differ only in `argv` and `revision` (walked field by field), so
the three later landing revisions (`188ddeea`, `b58f9b19`, `29883d4e`), which changed only S145/S147/S148 and
the lesson text, did not change any C1 field.

## L1 receipt vs my landing score (`c1-at-landing.json` vs `c1-land.json`)

Walked field by field (both JSON trees). Three differing fields:

| field | L1 | W2 |
|---|---|---|
| `argv` | `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev b58f9b19… --work …/kaidoku-r49/l1/cwork3` | `--root $S/c --rev 29883d4e… --work $S/work-land` |
| `counter` | lane worktree path | `$S/c/tools/round-49/c1-counter.py` |
| `revision` | `b58f9b192aba548b99d250bb896bbc42c654632c` | `29883d4ec35a31a8393c4ffb220888c44c0bb022` |

Equal in every other field, including `carriers` (all four), `evidence_digests` (`7b9da824…`, `8a2e8386…`,
`f7afd909…`, `b925ff90…`), `bindings`, `failing`, `counter_sha256`, `exit_code 0`, `frozen_path_changed []`.

## Findings (each names what it attacks)

| ID | Attacks | Finding | Evidence (command → result) | Severity |
|---|---|---|---|---|
| F0 | C1 landing numbers | Reproduced: exit 0, 4 carriers, every binding true, `failing []`, `frozen_path_changed []`. | `python3 -I -B $S/c/tools/round-49/c1-counter.py --root $S/c --rev 29883d4e… --freeze decc5697… --pkg65 …/rea-agents --work $S/work-land --json-out $S/c1-land.json` → exit 0; stdout sha `ae830b21…` | pass |
| F0b | C1 freeze numbers | Reproduced: exit 1, 0 carriers; 56 failing clauses (4×14); six documentation bindings false. | same command with `--rev decc5697…` → exit 1; stdout sha `976af57f…` | pass |
| F1 | L1 receipt `c1-at-landing.json` | Labelled "at landing" but scored at `b58f9b19`, not `29883d4e`. Numbers identical; the provenance label is wrong. The L1 should re-measure at its final revision and name it. | field `revision` = `b58f9b19…` in the L1 file; three differing fields (table above) | low (label) |
| F2 | Decomposition of the before→after | Confirmed: data-run commit `4aabb0b4` moves carriers 0→4 with exit 1 (bindings false); landing commit `3847f393` makes exit 0. | S2, S3, S4 rows | pass |
| F3 | Freeze integrity (C1 walk) | Confirmed: no frozen C1 path changed between freeze and landing. `git -C $R diff --name-only decc5697… 29883d4e… -- plans/round-49-claims.md tools/round-49 tools/round-42/fixtures.json tools/round-42/c1-counter.py tools/round-42/prior-pins.json tools/round-42/rea-pkg.json tools/round-39/gen-squashfs.py tools/round-27/xpin-attribute.mjs corpus/evidence/round-44/oracle corpus/evidence/round-44/carriers corpus/evidence/round-42/c2/fixtures` → empty output. | empty output | pass |
| F4 | Carrier freeze binding (plan prose vs counter) | **Plan prose names the wrong directory.** Plan lines 53–54 say C1 freezes "the committed carriers under `corpus/evidence/round-44/carriers/`". Those two files are the **v2.1** carriers, which C1 does not use. The four C1 carriers live under `corpus/evidence/round-42/c2/fixtures/` (`carriers.json` `carrier_path`), and the plan's "Frozen paths" list (lines 200–207) omits them too. The counter does bind the four carriers, through the carrier paths in the frozen `carriers.json`. Fixture (one commit after the freeze, appending `X` to `v1-le--squashfs_v1.0_le.bin`, fixture commit `0837cb08…`) → `exit 2`, `frozen_path_changed ["corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1.0_le.bin"]`. Round-44 v2.1 files are not bound, which is correct for C1. | `python3 -I -B $S/c/tools/round-49/c1-counter.py --root $D --rev 0837cb08… --freeze decc5697… --pkg65 …` → exit 2; stdout sha `bdd3988d…` | low (plan prose; the counter is stricter and correct) |
| F5 | REA rerun binding | **Latent gap.** The rerun executes `npx -y rea-agents@6.5.0 extract-firmware …` (`make_real_runner`), not the `--pkg65` path. `--pkg65` is bound for the evidence-id/xpin step and the frozen `rea-pkg.json` digests: a bogus package with `package.json` version 6.5.1 → `exit 2`, `rea package does not match the freeze: package.json sha256 d56ac4d1… != frozen a500302…`. The rerun binary is whatever npx resolves for the spec. Today that resolves to `~/.npm/_npx/ad9a3fdbcad992c6`, which equals `--pkg65` and is the only `rea-agents` install under `~/.npm/_npx/*`. The claim "REA 6.5.0 rerun" therefore holds by spec and cache state, not by the counter checking the executed bytes. | `strace -f -qq -e trace=execve` on the landing score (`strace-land.txt`): the `npx -y rea-agents@6.5.0` execs resolve to `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/.bin/rea`. `grep -l '"name": *"rea-agents"' ~/.npm/_npx/*/node_modules/rea-agents/package.json` → one file, `version 6.5.0`. | medium-low (latent; numbers correct today). Not run: a substituted npx cache (needs writes under `~/.npm` or PATH, forbidden) |
| F6 | The rerun is real | Confirmed by strace on the landing score: per carrier one `npx` → `rea` → `node` → `unblob --process-num 1 … --extract-dir` → `sasquatch` (`-le` for LE, `-be` for BE). Counts: npx 4, rea 4, unblob extract 4, sasquatch 4. The rerun dirs were removed after use (`work-land/` is empty). | `grep -E 'execve\(.*npx".*rea-agents@6.5.0' strace-land.txt \| grep -vc ENOENT` → 4 | pass |
| F7 | Committed receipts vs round-44 (disclosed limit 1) | Not a byte copy. Leaf-walk of `corpus/evidence/round-44/c1/<id>/after.json` vs `round-49`: v1be 41, v1le 41, v2be 48, v2le 48 differing leaves. All are paths (`probe-R44C1Run`→`probe-R49C1Run`), pids/mkdtemp names, blob ids (`1344682:1`→`1044454:1`), `evidence_id`, and command strings. No sha, size, handler, layout or projection field differs. Consistent with a fresh run of the same inputs; does not prove who or when (the plan says so). | `git show 29883d4e:corpus/evidence/round-44/c1/<id>/after.json` and `…round-49/…` → sha256 r44 `facc57d9…`/`eb44f3db…`/`18839471…`/`162e69b2…` vs r49 `7b9da824…`/`8a2e8386…`/`f7afd909…`/`b925ff90…` | pass with the plan's limit |
| F8 | Provenance paths named by the receipts | The receipts' `output_directory` is `/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/c1-run.<id>.1044367/rea-out`. At review time `/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/` exists and is **empty**: the cited rea-out trees are gone; the committed `corpus/evidence/round-49/c1/<id>/firmware.bin_extract` is the only copy. The counter's prefix test passes (plan-consistent). The directory name says "probe" for a data run (cosmetic; from `SCRATCH_PREFIX` in `c1-run.py`). | `ls -la /fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run` → only `.` and `..` | low (plan-consistent; non-retrievable provenance, the same as disclosed limit 1) |
| F9 | Oracle and tool versions in the rerun environment | Match the claims: unblob 26.6.4; sasquatch 4.5.1; `unsquashfs` 4.7.5 with the frozen sha. The committed `run.json` `child_path` equals FIXED_PATH. | `unblob --version` → 26.6.4; `sasquatch -version` → `unsquashfs version 4.5.1 (2022/03/17)`; `sha256sum /usr/bin/unsquashfs` → `461e1fd9…1677c` | pass |

## Not run

- `--selftest`, the CTL-C1-* controls and the in-counter mutation battery (outside "before→after numbers";
  other seats own them). No data run was started (`c1-run.sh --data-run` is forbidden here).
- A cache-substitution test for F5 (needs writes under `~/.npm` or PATH; forbidden by the host guard).

## Residual risk

- The data receipts cannot be re-audited from their cited scratch paths (F8). The only evidence that the REA
  runs happened as recorded is the counter's own rerun, which F6 shows is real, plus the committed trees.
- F5: "REA 6.5.0" is enforced by the npx spec and by cache state, not by the counter's bytes check. A future
  npx cache change could make the rerun and `--pkg65` disagree without a counter red.

## Artifacts (`.ufo/waves/round-49/w2/W2C1Rescore/`)

`summary.json` (all rows, full sha256s), `c1-land.{json,stdout,stderr}`, `c1-freeze.{json,stdout,stderr}`,
`c1-4aabb0b4bf716fb564c8406509c40b0a67457800.{json,stdout}`, `c1-3847f393.{json,stdout}`, `c1-f1.{json,stdout,err}`
(fixture F4), `strace-land.txt` (full execve trace of the landing score), `strace-land-rea-execs.txt`.
