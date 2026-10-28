# R44W2ScribeSources — round-44 Sources & Frontier annex

Seat `R44W2ScribeSources`. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Date 2026-10-28.
Method: committed bytes only (`git show`/`git diff`/`git log`/`git ls-tree`, read-only), plus the
fleet census validator in its documented read-only modes. No VCS mutation, no claim/counter/rubric/
frozen-byte/production-doc edit, no tool installed. Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2ScribeSources`
was removed after this file was written (§11). Artifacts:
`.ufo/waves/round-44/w2/artifacts/R44W2ScribeSources/` — `receipts.tsv` (sha256 `c64654e0…`, 44 rows),
one `.out` stdout capture per receipt (`R01.out`…`R44.out`), `extract_rows.py`, `census-validate*.txt`,
`census-freeze.txt`.

Axes walked (godspeed, cheap-parallel): **A1** row delta and revision identity; **A2** added-row
fields and line digests; **A3** existing-row immutability (`status`/`recheck`/`used-by`); **A4**
frontier advance; **A5** assimilation line + five-row quarantine + `considerthese/`; **A6** validator
state at base/freeze/measured/tip; **A7** instrument coverage of the frozen-claim SOURCES clause.

## 0. Answer block

| item | answer | evidence |
|---|---|---|
| registry rows before → after | **137 → 139** (139 at freeze, measured rev and tip) | R01, R02, R06 |
| rows added, by tier | **S138** (`dataset`, tier **A**) and **S139** (`docs`, tier **A**) — both `mined`, opened `2026-10-28` | R25, R11/R12 |
| `status`/`recheck`/`used-by` changed old→new | **none** (0 changed cells; 0 deletions; first 137 rows byte-identical) | R03, R04, R06, R25 |
| frontier rows advanced | **none advanced; v1/v2 remain Frontier** (no `## Round-44 additions to Core`; new round-44 note says "remain Frontier") | R31, R15, R30, R33 |
| assimilation | **`none`** — full five-row quarantine slice (`S150`, `S113`, `S117`, `S136`, `S147`) re-derived, sha256 `7383a90e…28e6a`; nothing adopted | R17, R44, claims:290-292, lesson:34-41 |
| `considerthese/` | **absent** in the lane (0 directories named `considerthese` at REV; `ls -d` fails at the worktree) | R16, lesson:41 |

Two numbered defects (§8) and three observations (§9) follow; neither defect changes a claim, a
counter, a rubric, or a frozen byte, and neither falsifies the registry delta above.

## 1. Revisions and the SOURCES blob

| role | revision |
|---|---|
| base | `c29360e3ba5381a5ab69e372d0d9577970f85018` |
| freeze | `c48f8a4bfd449300c975668e59aae5b5538b6a84` (parent `b2a1bd91`) |
| measured | `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac` |
| lane tip at write | `8bb1090af3fef64477c4337855e4347472db2701` |

`corpus/SOURCES.md` sha256 (R07): base `251ec4a72ee3dcf1f0f5e45debc001be2333c0340b661e616ebceaaedb62c68c`;
freeze = measured = tip = worktree `90a10fddc549777e841182986f4841d4736721ac05955d85bbf1d11641255dfd`.
`git diff --stat 55bcce69..8bb1090a -- corpus/SOURCES.md` is empty (R09), and exactly one commit in
`c29360e3..8bb1090a` touches the file — `b2a1bd91 round-44: freeze-reviewed claims and S138/S139 source rows`
(R08). No byte of the registry moved after the freeze.

**Citation anchor.** Every `file:line` in this annex names a committed blob, read with
`git show <rev>:<path>`: `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, `SCORECARD.md`
and `plans/round-44-claims.md` at `55bcce69` (the claims file is byte-frozen from `c48f8a4b`);
`corpus/lessons/round-44.md` at its only committed revision `8bb1090a` (it does not exist at
`55bcce69`). The worktree acquired concurrent uncommitted edits to `LOG.md`, `SCORECARD.md` and
`corpus/lessons/round-44.md` during this seat's run — not made by this seat — so no citation here
is taken from mutable worktree bytes. The single worktree-based check (the census validator, R10)
reads `corpus/SOURCES.md`, which is byte-identical to the committed blob (R07).

## 2. Registry census — 137 → 139 confirmed

`corpus/SOURCES.md` header `## Registry` at `:3`; the 11-column row schema at `:5-6`
(`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`, R32).
Row-detection regex on every revision, `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` (R01/R02):

| revision | rows |
|---|---|
| `c29360e3` (base) | 137 |
| `c48f8a4b` (freeze) | 139 |
| `55bcce69` (measured) | 139 |
| `8bb1090a` (tip) | 139 |
| worktree | 139 |

Validator census, same file bytes (`sources-census.sh census --file …`, R11/R12):

| metric | base | measured |
|---|---|---|
| rows | 137 | 139 |
| tier.A | 129 | **131** |
| tier.B | 7 | 7 |
| tier.C | 1 | 1 |
| status.mined | 132 | **134** |
| status.rejected | 5 | 5 |
| status.queued / invalid | 0 | 0 |

The delta is exactly two tier-A, `mined` rows; no tier moved and no row changed status. This matches
`corpus/lessons/round-44.md:44-45` ("`corpus/SOURCES.md` **137 → 139 rows**") and the claims'
frontier step (`plans/round-44-claims.md:285-289`). The 139 knowledge-file/.md count is a different
denominator (`corpus/knowledge/*.md` 137 base / 137 freeze / 138 measured, R22) and must not be
conflated with the 139 registry rows; `SCORECARD.md:3511`'s `137/137` is a knowledge-file count at
the freeze tree, not a registry-row count.

## 3. Rows added — S138 and S139

Line numbers at measured rev (= freeze = tip, same blob): `S138` at `corpus/SOURCES.md:144`,
`S139` at `:145`; 11 cells each (R25). `git diff c29360e3..55bcce69 -- corpus/SOURCES.md` is
`@@ -141,6 +141,9 @@` — two `+` rows and one `+` blank separator (R03/R05/R24), 3 insertions, 0 deletions.

| field | S138 (`:144`) | S139 (`:145`) |
|---|---|---|
| kind | `dataset` | `docs` |
| tier | `A` | `A` |
| status | `mined` | `mined` |
| opened | `2026-10-28` | `2026-10-28` |
| recheck | `180d` | `on-release` |
| used-by | `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | same path |
| source (canonical URL) | `https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs` | `https://github.com/plougher/squashfs-tools/releases` |
| line sha256 incl. terminating LF (R26) | `fbfb0186e09836b45d3baf9ea1a2358dfe78a4eb2536fa645c397a2056f8f2ba` | `56abb1deaa3f9aeb53d4d813d274105891cba217184eb9a74434ced0d5cd84d4` |
| same line without LF (peer canonicalization) | `0bd3e0990cea35c087833665aa65c5b7b16abf47e1473968e46a63d884474916` | `2f625005cb1087c586eeacdcd86b19b9250e249c90d5915f810b52752f67f924` |

The two digest pairs are the same bytes hashed with and without the trailing newline: the peer seat
`R44W2Sources` reported the no-LF forms and this annex reports the LF forms (R26); there is no
digest conflict. `S139`'s URL appears on exactly one registry line (its own, R27); `S138`'s canonical
URL is shared with `S130:136` (and `S113:119` carries a deeper subpath of it), which is the census
W04 described in §6 (R28).

The `used-by` cell points at the knowledge entry that `S138`/`S139` ground; the entry itself cites
them back at `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:12` (`source: S138`) and `:13`
(`source: S139`). The entry exists at the measured rev and is absent at the freeze (R36) — the
round-43 forward-reference pattern, with the consequence recorded as O-3.

## 4. Existing-row immutability (`status`/`recheck`/`used-by`)

Expectation in the seat spec and the lesson (`corpus/lessons/round-44.md:50-51`): none changed.
Verified four ways, all on committed blobs:

1. `git diff --numstat c29360e3..55bcce69 -- corpus/SOURCES.md` → `3	0	corpus/SOURCES.md` (R03).
2. Content deletions: `git diff … | grep -cE '^-([^-]|$)'` → `0` (exit 1 = no match, R04); total
   additions `3`, of which blank `1` (R05, R24), so the only changed rows are the two added rows.
3. First 137 registry rows of the rev are byte-identical to the base's 137 rows (`diff` → `IDENTICAL-137`, R06).
4. Structural cell diff over the row map: `base_rows 137 rev_rows 139 added ['S138','S139'] dropped []
   status_recheck_usedby_changed []` (R25); 139 unique ids, 0 duplicates (R20).

No cell of any pre-existing row changed, and no id was dropped.

## 5. Frontier — none advanced; v1/v2 remain Frontier

- **No Core promotion row exists.** `git show 55bcce69:PROVINCE.md | grep -c 'Round-44 additions to Core'`
  → `0` (R31); the C1 counter's `province_core_section`/`province_core_row` bindings are therefore
  false, consistent with the honest stop.
- `PROVINCE.md:416` — the round-42 frontier note that names `SquashFS v1/v2` as Frontier — is
  **unchanged**: base PROVINCE (422 lines) sha256 `e385f119…` equals rev's first 422 lines (R15);
  `git diff --numstat c29360e3..55bcce69 -- PROVINCE.md` is `8	0` (R30), i.e. append-only, 0 deletions.
- `PROVINCE.md:418` (round-43 note) sits inside the preserved prefix and is unchanged.
- `PROVINCE.md:430` — the new round-44 note: v1/v2 "were measured on four standard fixtures … but
  R44-C1 is not promoted … **remain Frontier** pending a new pre-data freeze that aligns the
  predicate and instrument."
- `corpus/README.md:104` — coverage-map row: `SquashFS v1/v2 through REA (round 44) … **Measured, not
  promoted** … the score is not admitted and v1/v2 remain Frontier`. `README.md:224` — knowledge row
  (`S112, S138, S139`; "no Core claim"). `README.md:275` — frontier bullet: "was measured … but
  **remains Frontier**". README diff is append-only `3	0` (R30, R33).
- Registry-side: no frontier marker is encoded in `SOURCES.md`; the registry records sources, and
  both new rows are `mined` sources that cite a measurement, not a promotion (R25).

## 6. Assimilation, quarantine slice, `considerthese/`

- Claim text: `plans/round-44-claims.md:290-292` — "`Assimilation: none` — the kaidoku package's full
  5-row quarantine slice was hand-checked in round 43 and re-derived this wave (R44Quarantine: no
  staged row adopted since); `considerthese/` does not exist."
- Lesson: `corpus/lessons/round-44.md:34-41` — Reject/no adoption; "the full five-row quarantine
  slice was re-derived byte-identically to round 43 (sha256 `7383a90e…28e6a`) and hand-checked live";
  `considerthese/`: absent at lane root.
- Measured here: `.ufo/waves/round-44/w1/artifacts/R44Quarantine/quarantine-slice` sha256
  `7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a` (R17), five lines with ids
  `S150`, `S113`, `S117`, `S136`, `S147` (file read; the same five ids at
  `w1/R44Quarantine.md:94-98`); no `S150` registry row exists at the measured rev (id scan R44 → `0`;
  peer R44W2Assim's `grep S150` exit 1).
- `considerthese/`: 0 directories with that name at REV (`git ls-tree -d --name-only`, R16); `ls -d
  considerthese` fails at the worktree. Lane-root top-level dirs at REV: `.ufo`, `corpus`, `evidence`,
  `kaidoku-r26`, `plans`, `tools`.
- Peer seat `R44W2Assim` independently reached **CONFIRMED** for the same line
  (`.ufo/waves/round-44/w2/R44W2Assim.md`, §4); this annex adds the registry-side measurements only
  (slice digest, absence, no S150 row) and does not re-claim its live reopens.

## 7. Validator state (base / freeze / measured / tip)

| tree | command | exit | W04 | E-codes | note |
|---|---|---|---|---|---|
| worktree = measured = tip | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | **0** | **14** | none; final line `kaidoku ok …/corpus/SOURCES.md` | R10, stdout sha256 `9f32a8a8…` |
| base (137 rows) | `… validate --file <SOURCES-base.md>` | 1 | **13** | many E11 (artifacts of `--file` mode: used-by resolution has no repo root) | R38 |
| freeze tree (`git archive c48f8a4b`) | `… validate <freeze-tree>` | **1** | 14 | **E11 ×2**: `S138`/`S139` `missing used-by corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | R19 |

The measured/tip state is clean with 14 duplicate-URL warnings; `S138` is the 14th
(`kaidoku	W04	S138 duplicate url github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs across scopes`,
R10). The 13→14 delta is exactly the new row's shared URL (R28: the path appears in `S113`, `S130`,
`S138`; the validator flags the later row only). Ids are unique (R20), and each added row parses to
11 cells (R25) so the contract's `NF=13` holds.

## 8. Numbered defects for the L1

### D-1 — the frozen claim's `corpus/SOURCES.md` byte-freeze clause has no instrument

- **Claim text:** `plans/round-44-claims.md:64-65` ("`SOURCES.md` IS byte-frozen, with S138 + S139
  landed in the freeze commit …"), `:146` ("no frozen C1 path changed after the freeze"), and
  `:274-275` ("Shared README/SOURCES landing edits MUST be exactly represented in the rubric's
  content-bound expected-edit set … any additional change to either file reds `frozen_path_changed`").
  `plans/round-44-claims.md:319` repeats that no later SOURCES edit is permitted by either claim.
- **Command / exit / observed (C1 instrument):**
  `python3 -I -B -c "…load tools/round-44/c1-counter.py…; m._frozen_paths(carriers.json)"` — exit 0.
  Observed: `n 18`; `SOURCES False`; `README False`; `PROVINCE False`;
  `prefixes ('tools/round-44/', 'corpus/evidence/round-44/oracle/')`; `SOURCES_prefix False` (R13).
  Code path: `tools/round-44/c1-counter.py:272-286` (`FROZEN_PATHS`, `FROZEN_PREFIXES`),
  `:1616-1626` (`_frozen_paths` adds only carrier paths + oracle roots), `:1629-1683`
  (`frozen_drift`; the endpoint blob loop `for path in sorted(frozen)` compares only that set), and
  `:2012-2015` (only `drift` raises `FrozenPathChanged`). `corpus/SOURCES.md` is in none of the sets,
  so a post-freeze rewrite of a pre-existing row cannot appear in `frozen_path_changed`.
- **Command / exit / observed (C2 instrument):**
  `python3 -I -B -c "json.load(tools/round-44/c2-rubric.json)"` — exit 0. Observed:
  `frozen_paths ["SCORECARD.md","SHONEN.md","SKILL.md"]`;
  `expected_edits ["SCORECARD.md"]`; `frozen_dirs ["tools/round-44"]` (R14). The rubric has no
  SOURCES (or README) entry, so the shared-landing binding the claim demands is absent there too.
- **Why it matters:** the SOURCES clause is currently true only because this seat diffed the bytes
  (R03/R06/R25), not because an instrument checks it — the same "rule stated, gate absent" class as
  M44-2. A future post-freeze edit to `S130`, `S135` or any other pre-existing row would leave both
  counters green while the registry silently drifted from the freeze.
- **No live violation:** SOURCES is byte-identical at freeze, measured and tip (R07), 3 insertions /
  0 deletions (R03), first 137 rows identical (R06), 0 changed `(status,recheck,used-by)` cells (R25).
- **Contrast showing the gap is closable without new code:**
  `python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4b… --rev 8bb1090a… --pathspec corpus/SOURCES.md`
  — exit **0**, `verdict clean`, `touched []`, `blob_changed []` (R40). The round-45 gate can enforce
  the clause when handed the pathspec, but nothing in the repo supplies it: the same gate with no
  `--pathspec` walks the whole range and reports `touched 557` (R42), i.e. it is only correct when
  fed an explicit list, and no committed list names `corpus/SOURCES.md`.
- **Suggested route (round 45, not done here):** add `corpus/SOURCES.md` to
  `c1-counter.py` `FROZEN_PATHS` (blob model, matching the claim's wording) or to
  `c2-rubric.json` `frozen_paths` **with** an `expected_edits` insert clause of exactly the two rows
  plus the blank separator; add `corpus/README.md` with the row-identity clause `:274-275` requires;
  and hand both paths to the round-45 preflight's pathspec list before the next freeze.

### D-2 — "landed in the freeze commit" is not the commit that landed the rows

- **Claim text:** `plans/round-44-claims.md:64-65`, `:99-100` ("S138/S139 land in the freeze
  commit"), `:286-287` ("Landed in the freeze commit with `used-by` = the C1 entry"), `:319`.
- **Command / exit / observed:**
  `git log --format='%h parents=%p %s' -1 c48f8a4b; … -1 b2a1bd91` — exit 0.
  Observed: `c48f8a4b parents=b2a1bd91 round-44: freeze C1/C2 claims, carriers, counters, and controls`;
  `b2a1bd91 parents=7ed97668 round-44: freeze-reviewed claims and S138/S139 source rows` (R35).
  `git show --stat --format='%h %s' c48f8a4b -- corpus/SOURCES.md` prints no file entry — the freeze
  commit does not touch SOURCES (R34). `git log --oneline c29360e3..8bb1090a -- corpus/SOURCES.md`
  returns only `b2a1bd91` (R08).
- **Why it matters:** a reader who diffs the freeze commit alone will not see the two rows; the
  provenance is one commit earlier. The rows are nevertheless present **at** the freeze tree, which
  is what the claim's actual rule binds (`plans/round-44-claims.md:44-45`: "each frozen regular-file
  blob at FREEZE equals the blob at REV"), and the C1 counter reads content only
  (`tools/round-44/c1-counter.py:2172-2185`, `git show <rev>:corpus/SOURCES.md`), so no predicate is
  false. Severity: record wording, not an unmet target.
- **Not a live violation:** freeze blob = measured blob = tip blob `90a10fdd…` (R07).

## 9. Observations (not defects of the registry)

- **O-1 — lesson wording on the 14th W04.** `corpus/lessons/round-44.md:47-48` says the S138 URL is
  "present at another row's evidence pointer". Observed: the identical canonical URL is `S130`'s
  **source** URL (`corpus/SOURCES.md:136`), and `S113:119` carries a deeper `/squashfs_v4_be/__input__`
  subpath that the validator does not flag (R28). The warning itself is correct; the sentence's
  classifier is not.
- **O-2 — the round-end census receipt is untracked.** `corpus/lessons/round-44.md:48-49` cites
  `.ufo/waves/round-44/l1/sources-census-end.txt`; `git ls-files --error-unmatch` on it fails and
  `git status` shows it as `??` at the tip (R39), so it is not in any commit. Its bytes are, however,
  byte-identical to this seat's independent re-run (`cmp` clean; both sha256 `9f32a8a8…`, R10/R39).
  It also records raw TSV stdout only (no exit code, no command, no sha256). Suggest committing it
  with a receipt header, or pointing the lesson at a committed artifact.
- **O-3 — the freeze tree is not census-clean by construction.** Validating the freeze tree exits
  **1** with `E11` for `S138`/`S139` because `used-by` names the knowledge entry that only lands at
  the measured rev (R19, entry absent at freeze R36). This is the intended round-43 forward reference
  and not a claim violation — the round's green census is at the measured rev (R10) — but if
  `sources-census.sh validate` is ever wired into the freeze gate alongside the new
  `frozen-path-preflight.py`, the forward reference will red the gate; the wiring needs either the
  entry pre-landed or an explicit forward-reference allowance.
- **C-1 — corroboration of the peer seat's S138 record defects.** Peer `R44W2Sources`
  (`.ufo/waves/round-44/w2/R44W2Sources.md`) reports that the S138 gate cell's "1 token" label and
  the cited `manifest.json` digest do not match the bytes. Independent check here:
  `git show 55bcce69:corpus/evidence/round-44/oracle/manifest.json | sha256sum` → exit 0, observed
  `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe`, 48,198 B, identical at the
  freeze (R37), while `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:12` cites
  `4bc53dbb…`. The **registry rows do not cite that digest** — `S138:144`'s anchor is the sorted tree
  digest `21cb3a6a…` — so the two rows stand and the defect stays in the entry/lesson, as the peer
  filed it. Not re-filed here.

## 10. Receipts

Every receipt below was produced by seat `R44W2ScribeSources` on 2026-10-28 with the exact command in
the last column, from cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. `stdout_sha256` is over
stdout+stderr bytes; `exit` is the command's own exit code (`R04` exits 1 because `grep -c` matched
nothing and printed `0`; `R19`/`R38`/`R41` exit 1 by design, `R39`'s second command fails on the
untracked path; `R44` ends `; true` so its recorded exit is the shell's and its stdout `0` is the
measurement). `/fast/scratch/…` paths appear only as the scratch inputs named in the command
strings; the tree was deleted (§11).

```tsv
receipt	exit	stdout_sha256	stdout_bytes	wall_ms	command
R01	0	67cf55e9845f01affd23aa248e7314a0aad876f2164e3d5d23acf4b69e92abd0	52	5	for r in c29360e3 c48f8a4b 55bcce69 8bb1090a; do printf "%s\t" "$r"; git show $r:corpus/SOURCES.md | grep -cE "^ {0,3}\|[[:space:]]*S[0-9]{3,}"; done
R02	0	690e07064753123c967bbac0180f32da6a753a5bd8b79a47644cef58e776d9f0	4	1	grep -cE "^ {0,3}\|[[:space:]]*S[0-9]{3,}" corpus/SOURCES.md
R03	0	b72ffe6172eae8ba3fae02619b24ecd6f597f6cdf0fa977e7c66ff9f7b05695a	22	2	git diff --numstat c29360e3..55bcce69 -- corpus/SOURCES.md
R04	1	9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa	2	2	git diff c29360e3..55bcce69 -- corpus/SOURCES.md | grep -cE '^-([^-]|$)'
R05	0	1121cfccd5913f0a63fec40a6ffd44ea64f9dc135c66634ba001d10bcf4302a2	2	2	git diff c29360e3..55bcce69 -- corpus/SOURCES.md | grep -cE '^\+([^+]|$)'
R06	0	f52bacb262bd2e35459b1cbaa706a61865c9daee4c8897f22382bbec3391a5d1	14	2	diff <(git show c29360e3:corpus/SOURCES.md | grep -E "^ {0,3}\|[[:space:]]*S[0-9]{3,}") <(git show 55bcce69:corpus/SOURCES.md | grep -E "^ {0,3}\|[[:space:]]*S[0-9]{3,}" | head -137) && echo IDENTICAL-137
R07	0	d7571a97a8027e98230e9e68751d72ef6288a2a3ad34c021ab0cd2ebd1da6e6d	392	6	for r in c29360e3 c48f8a4b 55bcce69 8bb1090a; do printf "%s " "$r"; git show $r:corpus/SOURCES.md | sha256sum; done; sha256sum corpus/SOURCES.md
R08	0	9052a99e0d0ea1514bc4f1e4b6e488ac535658a12635981548f2f2a8f6148a34	68	1	git log --oneline c29360e3..8bb1090a -- corpus/SOURCES.md
R09	0	e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855	0	1	git diff --stat 55bcce69..8bb1090a -- corpus/SOURCES.md
R10	0	9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19	1518	228	bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
R11	0	b8c45ea2d1d3339849aad0f4bd48e95e0a6b406f58585e0fdbc10daeb801d03f	294	12	bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file /fast/scratch/hyaku/kaidoku-r44/R44W2ScribeSources/SOURCES-base.md
R12	0	ba020d94b4465b66c14ce62ae99aef2fc2cc1c5cc638f967255f555f698c4920	294	13	bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file /fast/scratch/hyaku/kaidoku-r44/R44W2ScribeSources/SOURCES-rev.md
R13	0	29f61dfc461cfad3ae7c213f756b7d9366683f49c37aa0348dddf5de623a54ee	133	20	python3 -I -B -c "import importlib.util,json;s=importlib.util.spec_from_file_location('c1','tools/round-44/c1-counter.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);spec=json.load(open('tools/round-44/carriers.json'));fz=m._frozen_paths(spec);print('n',len(fz));print('SOURCES','corpus/SOURCES.md' in fz);print('README','corpus/README.md' in fz);print('PROVINCE','PROVINCE.md' in fz);print('prefixes',m.FROZEN_PREFIXES);print('SOURCES_prefix',any('corpus/SOURCES.md'.startswith(p) for p in m.FROZEN_PREFIXES))"
R14	0	c2f558e6d3d97aca061297645d9a9e442f9eae7ec26fe9efdd60e2b44a909051	118	13	python3 -I -B -c "import json;d=json.load(open('tools/round-44/c2-rubric.json'));print('frozen_paths',d['frozen_paths']);print('expected_edits',sorted(d['expected_edits']));print('frozen_dirs',d['frozen_dirs'])"
R15	0	8836a909f2060f87f5a9243e1a594b890d345ea77a18236bf8aed413a04eebde	163	3	a=$(git show c29360e3:PROVINCE.md | sha256sum | cut -d" " -f1); b=$(git show 55bcce69:PROVINCE.md | head -422 | sha256sum | cut -d" " -f1); echo "base=$a"; echo "rev_prefix=$b"; [ "$a" = "$b" ] && echo PREFIX-PRESERVED
R16	0	9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa	2	1	git ls-tree -d --name-only 55bcce69 | grep -c considerthese; true
R17	0	3fbeceb2a9e8066589a6db60081f2e96951df96502ee76b929c20face24bdc7b	130	1	sha256sum .ufo/waves/round-44/w1/artifacts/R44Quarantine/quarantine-slice
R18	0	6c111b8d38f9542687ff8ce62858774479eb0740bb0305d00fa4cb1bb8e54b90	68	1	git show 55bcce69:corpus/SOURCES.md | sed -n "144p;145p" | sha256sum
R19	1	6612e10dcfcb020ad64c809e05e2e6a50038e9449ab153cf12aaae776f39241a	1680	234	bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate /fast/scratch/hyaku/kaidoku-r44/R44W2ScribeSources/freeze-tree
R20	0	9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa	2	2	git show 55bcce69:corpus/SOURCES.md | awk -F"|" '/^ {0,3}\|[[:space:]]*S[0-9]{3,}/{gsub(/ /,"",$2); print $2}' | sort | uniq -d | wc -l
R21	0	1121cfccd5913f0a63fec40a6ffd44ea64f9dc135c66634ba001d10bcf4302a2	2	1	git show 55bcce69:corpus/SOURCES.md | grep -c "tests/integration/filesystem/squashfs"
R22	0	17a86f103eadf630664d720fa3957e10034964b0c3f12cfbae3012269935347f	52	4	for r in c29360e3 c48f8a4b 55bcce69 8bb1090a; do printf "%s " "$r"; git ls-tree -r --name-only $r corpus/knowledge/ | grep -c "\.md$"; done
R23	0	03d069924452653bbfd7b98d39b95011b2931891b9c907e02de7e02ebad1c110	70	2	for r in 55bcce69; do printf "%s " "$r"; git show $r:corpus/SOURCES.md | sed -n "144p" | cut -c1-60; done
R24	0	4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865	2	2	git diff c29360e3..55bcce69 -- corpus/SOURCES.md | grep -cE '^\+$'
R25	0	07ca4e4191b5f4ebed4688613776af40266755b4e3b152b0ff2040ec1b657568	391	18	python3 -I -B /fast/scratch/hyaku/kaidoku-r44/R44W2ScribeSources/extract_rows.py
R26	0	14843dfa6ec2dbad3d62f13e1c95d5eccbed0ffcbe7ece782967f8a8dc1baff4	136	3	git show 55bcce69:corpus/SOURCES.md | sed -n '144p' | sha256sum; git show 55bcce69:corpus/SOURCES.md | sed -n '145p' | sha256sum
R27	0	4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865	2	2	git show 55bcce69:corpus/SOURCES.md | grep -c 'plougher/squashfs-tools'
R28	0	13326fbfc0805298f915d352ede7c1f59b27ea8c6dbf64a17cc0a156b47ec61f	15	2	git show 55bcce69:corpus/SOURCES.md | awk -F'|' '/^ {0,3}\| *S[0-9]+ \|/ && /tests\/integration\/filesystem\/squashfs/{gsub(/ /,"",$2); print $2}'
R29	0	9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa	2	2	git show 55bcce69:corpus/SOURCES.md | grep -c 'SQUASHFS' ; true
R30	0	1c672d2000385ca3cf16a4f491bf1205e513ca6b8bef35432d5b3fe6d608e90f	37	2	git diff --numstat c29360e3..55bcce69 -- PROVINCE.md corpus/README.md
R31	0	9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa	2	1	git show 55bcce69:PROVINCE.md | grep -c 'Round-44 additions to Core'; true
R32	0	55bf2318588dfdce616bf848469f7c1a3eac7ad312e10492b88d16656d39b07f	156	1	git show 55bcce69:corpus/SOURCES.md | sed -n '3p;5p;6p' | cat -A | cut -c1-120
R33	0	cd9d450c3baf8142415f80da7f98b181b8992fa788dd394570c56405fbd7d2e2	245	1	git show 55bcce69:corpus/README.md | grep -n 'Measured, not promoted\|remains Frontier\|r44-squashfs-v1v2' | cut -c1-80
R34	0	29f3eaed00da6278ea51c7aa6dc50310ff2f8d990fae97bcf73d6849eb632e59	8	1	git show --stat --format='%h %s' c48f8a4b -- corpus/SOURCES.md | head -5; echo EXIT_OK
R35	0	dbb4316610761e81f1079486349e13d88604fb709ae5f8c38640f31fdb14485f	175	2	git log --format='%h parents=%p %s' -1 c48f8a4b; git log --format='%h parents=%p %s' -1 b2a1bd91
R36	0	451e0dc5a99e835668c80e80384365286f6f93a925ea1dc5efe4efb8b9c1f802	39	2	git cat-file -e 55bcce69:corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md && echo ENTRY-AT-REV-OK; git cat-file -e c48f8a4b:corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md 2>/dev/null && echo ENTRY-AT-FREEZE || echo ENTRY-ABSENT-AT-FREEZE
R37	0	d8e08ccf862e31338c4ca702ef3075df95123bfaad7350419e87a36a9bb58b07	142	4	git show 55bcce69:corpus/evidence/round-44/oracle/manifest.json | sha256sum; git show c48f8a4b:corpus/evidence/round-44/oracle/manifest.json | sha256sum; git show 55bcce69:corpus/evidence/round-44/oracle/manifest.json | wc -c
R38	1	e362381dab6b92731e6ccb84aea6dd5febd301b1d674ed55b93c9c490ff94a43	18487	212	bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kaidoku-r44/R44W2ScribeSources/SOURCES-base.md
R39	0	a1bf068731f3b3e785820326b809db110e098ed2f3ff1248769b2e1319090120	141	4	sha256sum .ufo/waves/round-44/l1/sources-census-end.txt; git ls-files --error-unmatch .ufo/waves/round-44/l1/sources-census-end.txt 2>&1 | tail -1
R40	0	26340615d1eef460e66e491cace2d78b3720e4afcb8aafd52b0ee82b1ba9cc37	229	32	python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev 8bb1090af3fef64477c4337855e4347472db2701 --pathspec corpus/SOURCES.md
R41	1	dae13b0acb4810b6e15e35a814011964bfb52d48f979171400ab81dcd696bb15	2093	87	python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev 8bb1090af3fef64477c4337855e4347472db2701 --pathspec tools/round-44/
R42	0	c683b39ed20f324b35ca4b69dc99833c11228e117d76c0cbaff810155f1a92d6	44	35	python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev 8bb1090af3fef64477c4337855e4347472db2701 | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["verdict"],"touched",len(d["touched"]),"pathspec",d["pathspec"])'
R43	0	0d8a4f42a2e53b34ba1a2928933a842d80b453ef82c93a57e269cd95604a2f91	674	0	python3 -c json summary of receipts/R41.out (n_touched + unique paths)
R44	0	9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa	2	2	git show 55bcce69:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S150'; true
```

Artifacts copy: `.ufo/waves/round-44/w2/artifacts/R44W2ScribeSources/receipts.tsv` sha256
`c64654e0aaf30a8b6c7d299c1cec1402c69ecfe185106e521daf7fbb050bc009` (per-receipt `.out` files sit beside it). `census-validate.txt` = R10 stdout,
`census-validate-base.txt` = R38 stdout, `census-freeze.txt` = R19 stdout.

## 11. Scope, non-changes, cleanup

- **Not changed:** no claim text, counter, rubric, frozen path, rubric check, `MANIFEST.json`,
  `LOG.md`, `SCORECARD.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `.ufo/state/`,
  `.ufo/watchdog.log`, `.scratch/`, `templates/`, `scripts/`, fleet root, or sibling lane. No VCS
  mutation anywhere; the only mutating commands were writes into this seat's scratch and the two
  spec-named write locations.
- **Not executed:** the C1/C2 counters were not re-run (they need `--pkg65` and a counter-time REA
  rerun); the claims' `carriers_matched 4` / `entries_evaluated 80` results are taken as contract
  and left to the counter seats. Network was not used; the S138/S139 re-open is peer `R44W2Sources`'
  scope and is referenced, not duplicated.
- **Cleanup:** `/fast/scratch/hyaku/kaidoku-r44/R44W2ScribeSources` was removed with
  `rm -rf --` after this file was written; the tree is reported absent in the yield, not left behind.
