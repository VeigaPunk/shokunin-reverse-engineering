# kaidoku round 36: verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Session `CloseKaidokuR36`, 2026-10-26. Range `cab59f221fe19726b5692bfa4d9a9679e96b8a73..018ae62889cb0717be5a02a8bb74de055bd104cf`.
Report `.ufo/reports/round-36/kaidoku.md` (fleet commit `db0aacfe9fc0c609901418fa727d7a9db781402d`, author `kaidoku-shokunin`, 02:23:36 -03).
Claims read: **R36-C1** (coverage: sasquatch SquashFS recursion from Frontier to Core) and **R36-C2** (calibration:
self-assessment surfaces against observed repo state, 3 → 0). Frozen in `790561d4` (`plans/round-36-claims.md`).

No seat was dispatched. Every re-check below ran inline in this session. No lane counter, gate or selftest was executed
(PROTOCOL §Gate standard, Closure consequence). `c1-counter.py` and `c2-counter.py` were neither run nor imported; their
committed evidence was read instead. What I did run: git/jq/python over committed bytes; the lane's documented
**command A** measurement recipe (`SCORECARD.md` `## Measurement recipes`; it prints counts and returns no verdict, so
it is not a gate); `/usr/bin/unsquashfs` 4.7.5; and the domain tool itself, `npx -y rea-agents@6.5.0 extract-firmware`,
which I called directly and not through `tools/round-36/c1-run.sh`. The lane-side commands were `jj-lane.sh state`
(pure git) and the helper commit of this file. All scratch was under `/fast/scratch/hyaku/closure-kaidoku-r36`, and I
removed it after use. Nothing was installed or updated.

Driver digest (`.ufo/watchdog.log`, mutable):

```
2026-10-26T01:05:47-03:00 launch kaidoku round=36 pgid=25605 driver=hyaku-inline attempt=1
2026-10-26T02:24:03-03:00 complete kaidoku round=36; hyaku-inline attempt=1
```

## Step-1 conformance

| check | observed | result |
|---|---|---|
| report author | `git log --format='%an %H' -- .ufo/reports/round-36/kaidoku.md` → `kaidoku-shokunin db0aacfe…` | pass |
| `SHONEN` heading | `## SHONEN` present with 4 `[~]` lines; lane `SHONEN.md` has 4 boxes (`grep -nE '^\s*- \[.\]' SHONEN.md` → lines 5, 7, 9, 11) | pass |
| real report, not a marker | 11 landed commits, a LOG entry (`LOG.md:3116` `## 2026-10-26 — round 36 …`), receipts and wave reports | pass (status `ok`) |
| cited hashes exist and are ancestors of `main` | all 12 (`790561d4 6a870b92 3310d8fa d2e46ef5 ffc81341 01a44dbf 6f2ba761 38c1a8be 2618cf07 a6c433b5 018ae628` plus base `cab59f22`): `cat-file -t` → `commit` and `merge-base --is-ancestor <h> main` → 0 for each | pass |
| filed after its tip | lane tip `018ae628` committed at 02:23:10 -03, report committed at 02:23:36 -03 | pass |
| pushed | `jj-lane.sh state` → `branch=main local=018ae628… remote=018ae628… ahead=0 behind=0 head=detached tracked=0 untracked=1`; `ls-remote origin refs/heads/main` → `018ae628…` | pass |
| leftovers | `git status --porcelain` → `?? .ufo/waves/round-36/w2.ready.dispatched`. This is a 20-byte dispatch stamp (`2026-10-26T02:03:47`). Its wave-1 sibling `w1.ready.dispatched` is committed | defect R36-CL1 (status-neutral) |
| prompt contract | `.ufo/prompts/kaidoku-round-36.md` (fleet `c5f53253`, author `kaidoku-shokunin`) up to `## 6. Campaign addendum` equals the literal substitution render of `templates/round-prompt.md`. I applied `{{LANE}}`, `{{ROUND}}`, `{{AXES}}` from `shokunin.conf`, `{{FLEET_ROOT}}`, `{{LANE_REPO}}` and the legacy `<{{LANE}}-repo>` literal, and `difflib` reported 0 diff lines. §6 hyaku addendum and §7 scratch discipline follow. The prompt quotes no L2 route map, so the MISSION bucket check does not apply | pass |
| scratch | `/fast/scratch/hyaku/kaidoku-r36` absent (`ls -d` → no such file) | pass |
| seat accounting | `w1-results.json` seats 43 / results 43, `w2-results.json` 36 / 36; 43 + 36 `.md` reports (plus one `swarm-registry.json` per wave) | pass |

## Per-claim re-check

### R36-C1 (coverage): improved (re-measured; counter verdict evidence-verified)

**1. Receipts compared with the frozen oracle, from committed bytes at `018ae628`.** I read each
`corpus/evidence/round-36/c1/K*/{oracle.tsv,after.json,before.json}` with `git show` and matched each oracle row against
`normalized_result.files[]`: the `relative_path` must end with `/<oracle path>` and the `sha256` must be equal.

| carrier | oracle rows | after files / hits | after gaps | before files / hits | before gaps | subject sha256 (after = before) |
|---|---|---|---|---|---|---|
| K1 | 3 | 3 / 3 | none | 0 / 0 | `missing-extractor-dependency` `[sasquatch]` | `93802938486d…` |
| K2 | 4 | 4 / 4 | `unpublished-entry` (symlink) | 0 / 0 | same | `ce5bf60e765e…` |
| K3 | 2130 | 2147 / 2130 | `unpublished-entry` ×2 | 2 / 0 | same | `b644d034746a…` |
| K4 | 2130 | 2147 / 2130 | `unpublished-entry` ×2 | 2 / 0 | same | `8efcec73cea1…` |

**2. The oracle, re-derived independently.** K1 and K2 were taken from committed fixture bytes (`git show 018ae628:…/k1-le-xz.sqsh`
and `…/k2-le-gzip.sqsh`). K3 and K4 were downloaded fresh from the `carriers.json` URLs. `sha256sum` gave all four exactly
as `carriers.json` lists them: `93802938…a589`, `ce5bf60e…084f`, `b644d034…29fb`, `8efcec73…e1c2`. I computed the offset
myself from the ELF header (`e_shoff + e_shnum*e_shentsize`): 0, 0, 944632 and 936456. I then ran
`/usr/bin/unsquashfs -no-progress -o <off> -d <dir>` and hashed every regular non-symlink file. Regular files found:
3, 4, 2130, 2130. The `{path: sha256}` map is **identical** to the committed `oracle.tsv` for all four carriers.

**3. An outside reproduction of the receipts.** This answers QUALITY 78 and wave-1 F1, which showed that receipt integrity
alone is not provenance. I ran `REA_UNBLOB_COMMAND=~/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json <carrier> <out>`
as follows:

- K1 with sasquatch on PATH: exit 0. 3 files, 3/3 oracle hits, no gaps, handler `squashfs_v4_le`, unblob 26.6.4.
- K3 with sasquatch on PATH: exit 0. 2147 files, 2130/2130 hits, gaps `unpublished-entry` ×2, handlers `elf64`, `padding` and `squashfs_v4_le`.
- K1 with every sasquatch directory removed from PATH (`command -v sasquatch` → none): exit 0. 0 files, gap `missing-extractor-dependency` `[sasquatch]`.

My published `(relative_path, sha256)` sets equal the committed `K1/after.json` set (3 = 3) and the committed
`K3/after.json` set (2147 = 2147). So the committed receipts are reproducible from outside the lane, and they are not
re-hashed fabrications.

**4. Installed tool provenance.** `sha256sum ~/.local/bin/sasquatch` → `ad02d27a3d84…4754` and
`~/.local/bin/sasquatch-v4be` → `fac88740f49b…14c6`. Both equal the deb member digests recorded in S107. I re-opened the
GitHub API for `sasquatch-v4.5.1-6`: published `2026-01-27T11:57:51Z`, 6 assets, `sasquatch_1.0_amd64.deb` 187244 bytes,
`sha256:efbc92bd…ade95`, matching the S107 row.

**5. The bindings, read from committed bytes.**

- **PROVINCE before and after.** At base, `PROVINCE.md:149` holds the Frontier bullet `**sasquatch** — … (AUR-only)`. At
  tip, that bullet sits at `:156` and carries `[2026-10-26: superseded for LE SquashFS v4 — see `## Round-36 additions to Core`; …]`.
  Tip `## Round-36 additions to Core` (`:368`) adds row `:372`, `sasquatch squashfs recursion`, citing
  `corpus/evidence/round-36/c1/`. The Frontier note is at `:374`.
- **The entry.** `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` opens with `source:` S107/S108/S109,
  then `verified-at:` and `recheck:`.
- **The SOURCES rows.** S107–S109 are `mined` and opened 2026-10-26.
- **Census.** `sources-census.sh validate` gave exit 0 (below).
- **Coverage-map rows.** `corpus/README.md` adds both new stems, and command A shows them mapped (C2 §2).

**6. The counter's committed evidence (not executed).** C1 counter bytes are unchanged from the freeze to the tip:
`git diff --stat 790561d4 018ae628 -- tools/round-36/ …/carriers.json …/K*/oracle.tsv …/K1/before.json …/K3/before.json`
is empty, and `git log -- tools/round-36/c1-counter.py` → only `790561d4`. Selftest `{"cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}`
appears in `w1/R36ExecRecountC1.md:27`, `w1/R36MutantC1.md:31` and `w2/R36W2ExecC1Final.md:69`. The frozen run is
`.ufo/waves/round-36/after/c1-final.json`: `--rev a6c433b5…`, all bindings true. `.ufo/waves/round-36/after/c1-at-ffc81341.json`
is the same at `ffc81341`. `a6c433b5..018ae628` touches only `after/c{1,2}-final.json`, `w2-results.json` and `w2/*.md`,
so no measured surface moved after the final receipt. The controls are in `controls/ctl-c1-{0,1,2}-*.json`, all exit 1,
and they were committed in `6a870b92` (01:22:29) before the after receipts in `3310d8fa` (01:22:59).

Verdict: **improved**. The surface moved from Frontier to Core, backed by receipts that I reproduced and re-derived myself.
The counter's known blind spots (F1, mutants alive 2/10, skip controls left green) do not carry this verdict, because
steps 1–4 do not use the counter.

### R36-C2 (calibration): improved (re-measured with a stricter independent resolver; counter evidence-verified)

**1. My own pointer resolver.** I wrote it for this closure; it does not import or read `c2-counter.py`. Units: every
`## Owned axes` table row, every row of the first `## Capabilities` table, and every SHONEN box (the box line plus its
indented continuation). Checked: every backticked token that is a repo path (contains `/` or has a file extension, is not
a command, and is not absolute or `~`). Each must exist in `git ls-tree -r <rev>` as a file or a directory, and any
`:a-b` range must lie inside the file.

- At base `cab59f22`: 15 units, 36 pointers, **4 unresolved**. These are `result.json` (calibration row, bare basename),
  `receipts-B/` (capability "pre-registered two-lane live battery"), `config-post-pair.txt` (capability "config custody",
  bare basename) and `ScoutSkillPlacement.md` (SHONEN box 4). The frozen counter counts only the two that its predicate
  enumerates; the other two are stricter catches of mine. The lane repaired all four in place.
- At tip `018ae628`: 16 units (+1 new capability row), 43 pointers, **0 unresolved**.

**2. Counts via command A**, run from the `SCORECARD.md` recipe over git objects.

| rev | mapped | files | missing | dangling | rules resolved |
|---|---|---|---|---|---|
| `cab59f22` | 122 | 122 | [] | [] | 17/17 |
| `d2e46ef5` | 122 | 122 | [] | [] | 17/17 |
| `018ae628` | 124 | 124 | [] | [] | 17/17 |

The coverage row now states `124/124 … (122/122 at cab59f22 …)`. At base it stated `116/116` against an observed 122/122,
which was the third base mismatch. The depth row's `17/17` matches. The command B jq returns `aligned 0/9 → 9/9`, which
matches the calibration row, and `git diff --stat cab59f22 018ae628 -- evidence/` is empty.

**3. Section ranges.** The tip `SKILL.md` `## Queue-drain craft` section runs from heading 81 to last non-blank line 314,
matching `SKILL.md:81-314` in the depth row and in SHONEN box 1. The tip `PROVINCE.md` `## Adjacent` refusal list runs
from 97 to 125, the last non-blank line before `### Round-4 additions to Core` at `:128`. This matches SHONEN box 4's `PROVINCE.md:97-125`.

**4. No shadow units (QUALITY 77 blind spot).** `git diff cab59f22 018ae628 -- SCORECARD.md SHONEN.md` edits the three
owned-axis rows, two capability rows and SHONEN box 4 in place. It appends one capability row and the round-36 section,
and deletes nothing else (`--numstat`: SCORECARD 19/4, SHONEN 1/1). Raw counts are unchanged base → tip: rows starting
`| coverage |`, `| depth |` or `| calibration |` 110 → 110; SHONEN boxes 4 → 4; the "pre-registered two-lane" capability
row appears once, at `:619`.

**5. The counter's committed evidence (not executed).** Selftest 13/13 (`{"green_ok": 1, "red_ok": 12}`) appears in
`w1/R36ExecRecountC2.md:35` and `w2/R36W2ExecC2Final.md:76`. Frozen runs: `c2/after-at-d2e46ef5.json` (0 mismatches,
`guards_ok`, measured before C1's entry existed), `after/c2-at-ffc81341.json` and `after/c2-final.json` (`--rev a6c433b5`,
0 mismatches, `base_unresolved` = the two enumerated pointers, `unrepaired` []). The controls are `controls/ctl-c2-{0..3}-*.json`,
all exit 1.

Verdict: **improved**. My stricter re-derivation agrees with the counter: 4 pointer misses plus 1 count miss at base,
0 and 0 at tip.

### Axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | improved | R36-C1 re-measured (§C1 1–5). Command A 122/122 → 124/124; capability row added |
| depth | unchanged | not claimed. Command A rules 17/17 → 17/17, and the craft range 81-314 is unchanged. SKILL gains a decision table outside the craft section |
| calibration | improved | R36-C2 re-measured (§C2 1–4) |
| operability | unchanged | not claimed. `c1-run.sh` and the reproduction order were added; I did not grade them |
| freshness | unchanged | not claimed. The r4u-03 sasquatch clause was re-verified by a supersession note appended to the entry |
| adjacency | unchanged | not claimed. A dated tooling bullet was added to PROVINCE `## Adjacent`, and no sibling ground was absorbed |

No axis harmed: the `SCORECARD.md` diff only restates or appends rows, and owned scores stay 10 → 10.

## Discernment spot-check (`corpus/lessons/round-36.md` `## Gate`)

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S107 onekey-sec/sasquatch `sasquatch-v4.5.1-6` | admit (tier A, code) | GitHub API `repos/onekey-sec/sasquatch/releases/tags/sasquatch-v4.5.1-6` | agree | `published_at 2026-01-27T11:57:51Z`; the six asset names, sizes and amd64 digest `efbc92bd…ade95` equal the row. The body line 4 reads `* fix: remove unnecessary magic checks by @jstucke in https://github.com/onekey-sec/sasquatch/pull/34`, and the 9-word Gate quote is its rendered form (`#34`). The installed binaries equal the row's member digests |
| S110 unblob README @26.6.4 (assimilated, renumbered from staged S106) | admit | `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md` | agree | sha256 `6544d60f…3716` and 235 lines equal the row and the entry. Line 49 reads verbatim `For SquashFS support, also install [sasquatch](https://github.com/onekey-sec/sasquatch):`. The quote is 9 words (≤25) at the stated location |
| S111 devttys0 sasquatch README | admit (tier B) | `https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md` | agree | sha256 `f09961ee…1fef` and 30 lines equal the row. Line 12 reads `Very beta.`. Tier B is right for a self-description |
| AppImage Specification as authority for the offset rule | reject | `https://raw.githubusercontent.com/AppImage/AppImageSpec/master/draft.md` (280 lines) | agree | Type 2 says only "**MUST** have appended to it a filesystem that the ELF part can mount" (`:130`), with no offset formula. The real rule is in type2-runtime `src/runtime/runtime.c@8f39b89e:527`: "The offset at which a filesystem image is expected = end of this ELF". It reproduces the ELF-end offset 944632 on K3, and the lane cited it without appending a row |
| Decision 2: refuse `sasquatch-prebuilt-package-inventory` | refuse | GitHub API `releases/tags/sasquatch-v1.0` | agree | `sasquatch-v1.0` (2022-02-26) carries only `sasquatch_1.0_amd64.deb` and its dbgsym, so the staged "a Debian package per architecture" is false for that release |

Newly written `corpus/SOURCES.md` rows re-opened: S107, S110 and S111 (above). Their quotes and anchors hold.
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
→ 9 × W04 (the pre-existing duplicate-URL warnings S033, S047, S054, S062, S069, S083, S090, S092, S102),
`kaidoku ok`, **exit 0**. There are 111 rows (`grep -cE '^\| *S[0-9]{3,} *\|'` at `018ae628`), matching the report's census end.

Result: all 5 gate decisions agree (3 admits, 2 rejects).

## Trend verdicts

- **expansion: improved.** Two admitted entries cover ground the coverage map held as blocked (README Firmware row:
  "recursion blocked by missing sasquatch"). Each entry's `source:` cites mined rows opened in-round (S107–S109;
  S110–S111). One Frontier area is entered, and one capability row was added after a demonstration I reproduced.
- **quality: improved.** Stale statements are superseded by a measured entry with dated pointers: the r4u-03 entry has an
  appended `## Supersession`, `PROVINCE.md:157`, the README Firmware row, and the README Frontier note. The r34b entry
  gains an appended provenance trio. The assimilated entry was corrected before admission. No admitted entry failed my
  re-check.
- **discernment: improved.** The outside spot-check agrees with the gate on admits and on rejects (5/5). New criteria
  QUALITY 77 and 78 each cite a lesson (`corpus/lessons/round-36.md` M36-3 and M36-4) plus the wave findings behind them.

## Routed defects (the lane fixes these next round)

- **R36-CL1.** `.ufo/waves/round-36/w2.ready.dispatched` is left untracked in the lane (its w1 sibling is committed).
  Commit it or declare it ignored.
- **R36-CL2.** The dated pointer on the Frontier bullet at `PROVINCE.md:157` names `## Round-36 additions to Core` but not
  the entry path or stem. The `:374` note cites only the dependency entry (`w2/R36W2ExecC1Strict.md` S2a/S2b, still open
  at tip). Add the r36 entry stem.
- **R36-CL3.** The frozen counters have known blind spots:
  - C1 accepts a re-hashed envelope copied from the oracle (`w1/R36CriticC1Shortcut.md` F1).
  - C2 admits shadow rows and decoys (`w1/R36CriticC2Shortcut.md` A1–A6).
  - Mutants survive: C1 2/10, C2 7/14.
  - 12 of 17 extra skip controls stay green (`w2/R36W2CriticDoNothing.md`).

  The round-37 successor counters must implement QUALITY 77 and 78 before any data. This closure's verdicts rest on
  re-measurement, not on those counters.
- **R36-CL4.** The round-36 freeze has no map, so the lane's freeze-integrity gate cannot evaluate it (exit 2: no commit
  adds `.ufo/waves/round-36/claims.json`; `w1/R36ReviewerQualityBar.md` row 66). The next freeze ships its instrument map.
- **R36-CL5.** The instruments still do not meet the lane's own QUALITY rows 33, 39, 45, 58, 60 and 68
  (`w1/R36ReviewerQualityBar.md`, lane-disclosed).
- **R36-CL6 (minor).** The committed envelopes' `subject.local_path` and `parameters.*` point into deleted scratch. SKILL
  limit 4 already records this. Keep `subject.digest.sha256` as the identity, and name that rule wherever a receipt is cited.

## Operator note (promotion is operator-owned)

SHONEN boxes 2 ("end-to-end domain task executed and logged") and 3 ("instructions executable by an agent without oral
context") now look checkable by a non-author. This closure reproduced the REA `extract-firmware` task on K1 and K3, with
and without sasquatch, from the committed carriers, the entry's recheck line and the SKILL reproduction order, with no
oral context, and the results matched the committed receipts byte-for-set. Boxes 1 and 4 remain the lane's assertions.
Nothing was promoted.
