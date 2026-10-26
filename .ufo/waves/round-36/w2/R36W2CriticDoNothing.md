# R36W2CriticDoNothing — cheapest skip controls against the landed round-36 state

Seat `R36W2CriticDoNothing` (leaf, advisory), round 36 wave 2. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. State attacked: **the final landed tip**
`01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`, freeze `790561d4`, base `cab59f22`. Both frozen counters
were run **unmodified** (sha256 equal to their freeze bytes, §2) on fixture repos built from
`git archive` of those three revisions. Nothing in the lane was written except this report; no counter,
predicate, carrier, oracle, harness or surface was edited.

## Verdict

**Both frozen counters are green at the landed tip** (C1 exit 0, `carriers_matched: 4`; C2 exit 0,
`mismatches: 0`). Of the 17 controls below, **12 stay green** and 5 are correctly rejected. Of the 12 greens,
three are **predicate-level** falsifications (the predicate's own wording fails while the counter reports
`met_target`), one is a **claim-level** falsification (the claim's "moved" sentence is false), and eight show
surfaces the counter never reads or reads only as a substring. The three predicate-level classes:

| class | what fails at the green revision | where |
|---|---|---|
| **G1** duplicate SHONEN box shadows a restored, non-resolving pointer | P36-C2 "every backticked repo pointer in them resolves" | `SHONEN.md:11-12` carries `ScoutSkillPlacement.md`, which does not resolve (`git cat-file -e 35a8e28:ScoutSkillPlacement.md` → absent); counter `unresolved: []` |
| **G2** duplicate Capabilities row shadows a restored, non-resolving pointer | same clause, other named surface | `SCORECARD.md:619` carries bare `receipts-B/` (absent); counter `unresolved: []` |
| **G3** duplicate Owned-axes row shadows a restored stale count | P36-C2 "the four stated counts equal the counts … observe" | `SCORECARD.md:23` states `116/116 knowledge files mapped`, observed `124/124`; counter `mismatches: 0` |

And one **claim-level** falsification that neither predicate can see: the claim's first sentence —
"Surface moved: `PROVINCE.md` … bullet **sasquatch** … and `corpus/README.md` Firmware row"
(`plans/round-36-claims.md:14-17`) — **did not move either surface**. `corpus/README.md:44` (Firmware row)
is byte-identical at base and at the tip (sha256 `00c4f1cb5abbe8940afb9691816141ab06c2f8cb05c552eaae6c7c9eaf18fc97`
both) and still states "AppImage SquashFS carved but recursion blocked by missing sasquatch" in the
present tense; `PROVINCE.md:156` still reads "- **sasquatch** — unblob's squashfs recursion extractor
(AUR-only); 7z fallback" (base `PROVINCE.md:149`, same bullet). P36-C1 asks only for a round-36 Core row's
*presence*; it contains no clause about either old surface, so a green C1 receipt is compatible with the
"move" never having happened (controls T3, T4).

## 1. Method

```
S=/fast/scratch/hyaku/kaidoku-r36/R36W2CriticDoNothing ; export TMPDIR="$S"
D=$S/fx.ctrl ; git -C "$D" init -q          # rev-parse --show-toplevel == $D, checked
for rev in cab59f22… 790561d4… 01a44dbf…; do
  git -C D ls-files -z | xargs -0 -r rm -f
  git -C <lane> archive "$rev" | tar -x -C "$D"
  git -C "$D" add -A && git -C "$D" commit -qm "$rev"
done
```

Fixture commits: `93cc119aefa90b…` = `cab59f22` tree (23,168 files), `83205910b2901c…` = `790561d4` tree
(23,204), `b1f848e59e382c…` = `01a44dbf` tree (23,291). Each control: `git -C D checkout -f TIP`,
`git -C D clean -fdq`, one targeted edit, commit, run the frozen counter with `--root D --rev <new>`.
No `find`/`du` under `/fast/scratch`.

Frozen-counter invocations (identical to the frozen counting commands except `--root`/`--rev`/`--freeze`/`--base`):

```
python3 -I -B tools/round-36/c1-counter.py --root D --rev <rev> --freeze 83205910b2901c13fb449da859646aac6f59a774 \
        --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
python3 -I -B tools/round-36/c2-counter.py --root D --rev <rev> --base 93cc119aefa90b08d2610cece62865db228b3c24
```

## 2. Fixture fidelity (measured, not assumed)

| check | result |
|---|---|
| counters unmodified | `c1-counter.py` sha256 `5533e17d022a7e25a442ec650743b3958a5c86a44a0194eed08fe3085e6581b5` = worktree = `790561d4`; `c2-counter.py` sha256 `f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f` = worktree = `790561d4` |
| frozen inputs byte-identical | fixture `8320591` vs lane `790561d4`: `carriers.json` `2ebcf15a…ca81` = `2ebcf15a…ca81`; `tools/round-27/xpin-attribute.mjs` `8ea63837…f708` = same; `K3/oracle.tsv` `9924ec69…1f0e` = same; `K3/before.json` `6d2457a1…79b5` = same |
| fixture reproduces the lane run | lane tip run vs fixture tip run, receipts equal field-for-field after removing only `revision`, `argv`, `freeze`/`base` (fixture commit ids): C1 `True`, C2 `True` |
| green baseline on the **real lane** | C1: `{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107","S108","S109"], "opened_source_rows": ["S107","S108","S109"], "province_core_row": true, "province_core_section": true, "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true, "revision": "01a44dbf45913a1bdcabbbfb85b7bb9d232cb930"}`, exit 0. C2: `{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "01a44dbf…", "unresolved": []}`, exit 0 |

## 3. Controls and outcomes

Each row: mutation applied to the fixture tip, then the frozen counter. Full six-key stdout is quoted in §4–§5.

| # | control | expect | exit | counter verdict | caught? |
|---|---|---|---|---|---|
| T1 | `K2/after.json := K2/before.json` | red | 1 | `carriers_matched: 3`, K2 `after_sasquatch_gap true`, `after_oracle_hits 0` | **yes** |
| T2 | blank `opened` cell on all three cited rows S107/S108/S109 | red | 1 | `opened_source_rows: []`, `sourced: false` | **yes** |
| T2b | blank `opened` on S108+S109 only | ? | **0** | `opened_source_rows: ["S107"]`, `sourced: true` | **no** |
| T3 | move the Core row out of `## Round-36 additions to Core` (into the preceding section) | red | 1 | `province_core_row: false` | **yes** |
| T4 | delete both reconciling notes (`PROVINCE.md:374`, `corpus/README.md:233`) | ? | **0** | all bindings true | **no** |
| T5 | degrade the three cited SOURCES rows (`opened 2026-10-25`, used-by `corpus/lessons/round-36.md`) and append three duplicate rows with the same ids, `opened 2026-10-26`, used-by the entry | ? | **0** | `opened_source_rows: ["S107","S108","S109"]` | **no** |
| T6 | replace the knowledge entry with a 47-byte stub (`# Stub` + one `source:` line) | ? | **0** | `entry_present: true`, `sourced: true` (entry 16,477 B → 47 B) | **no** |
| T7 | mislabel the coverage-map row so it no longer maps the entry, stem left in the row's prose cell | ? | **0** | `coverage_map_row: true` | **no** |
| T8 | delete all four `K*/after-run.json` | ? | **0** | `carriers_matched: 4` | **no** |
| U1 | revert SHONEN box-4 pointer to the base token `ScoutSkillPlacement.md` | red | 1 | `unresolved: [[box4, ScoutSkillPlacement.md]]`, `guards_ok false` | **yes** |
| U2 | U1 + append a duplicate box with the identical title carrying the repaired pointer | ? | **0** | `unresolved: []`, `mismatches: 0`, `pointers 38` | **no** |
| U3 | U1 + duplicate box inserted **before** the real box | red | 1 | `unresolved: [[box4, ScoutSkillPlacement.md]]` | **yes** |
| U4 | revert Capabilities row 619 evidence cell to base (`receipts-B/`) + append duplicate row with the repaired cell | ? | **0** | `unresolved: []`, `mismatches: 0`, `pointers 41` | **no** |
| U5 | revert Owned-axes coverage row to `116/116 knowledge files mapped` + append duplicate `coverage` row stating `124/124` | ? | **0** | `mismatches: 0`, `pointers 36` | **no** |
| U6 | add a stale `PROVINCE.md:95-116` range in an unparsed form (backtick + trailing space) beside the correct range | ? | **0** | `unresolved: []`, `assertion_mismatches: []`, `pointers 41` | **no** |
| U6b | add an **out-of-file** range `PROVINCE.md:1-9999` in the same unparsed form (the class wave-1 V15 rejects when parseable) | red | **0** | `unresolved: []`, `assertion_mismatches: []`, `pointers 41` | **no** |
| U7 | point the Capabilities evidence cell at a planted `.ufo/waves/round-36/w2/receipts-B/PLACEHOLDER.txt` instead of the luna-round-6 lane | ? | **0** | `unresolved: []`, `guards_ok true` | **no** |

## 4. C1 findings, with the exact counter output

### N1 — the claim's "moved" surfaces were not moved, and the predicate never asks (T4, T3)

At the **unmutated** tip, both surfaces still carry the pre-round statement:

- `corpus/README.md:44` Firmware row — sha256 `00c4f1cb…18fc97` at `cab59f22:corpus/README.md:44` **and** at
  `01a44dbf:corpus/README.md:44`; text: "unblob: ucodes empty, .pkg.tar.zst carved, AppImage SquashFS carved
  but recursion blocked by missing sasquatch". `git show ffc81341 -- corpus/README.md` has no hunk touching
  line 44 (hunks at `@@ -86,6`, `@@ -190,6`, `@@ -217,6`, `@@ -225,6`).
- `PROVINCE.md:156` (base `:149`): "- **sasquatch** — unblob's squashfs recursion extractor (AUR-only); 7z
  fallback". The round-36 reconciliation is a **separate paragraph at `PROVINCE.md:374`**, outside
  `## Frontier`, which says the bullet "is superseded for little-endian SquashFS v4".
- `corpus/README.md:232`: "- sasquatch (AUR) — unblob squashfs recursion; 7z fallback covers today.", with a
  note at `:233`.

T4 deletes `PROVINCE.md:374` and `corpus/README.md:233` — the notes that reconcile the two surviving Frontier
bullets (`PROVINCE.md:156`, `corpus/README.md:232`); the Firmware row at `:44` is not reconciled anywhere — and
the counter is **green**:

```
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107","S108","S109"], "opened_source_rows": ["S107","S108","S109"], "province_core_row": true, "province_core_section": true, "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true, "revision": "dab222f7c40c11d8401a25d480823389880f58a7"}
```

T3 shows the contrast — the *Core* side is measured (`province_core_row: false`, exit 1) when the row leaves
`## Round-36 additions to Core`, so the counter's asymmetry is deliberate: presence in the new section, no
statement about the old one. `[INFERENCE]` the round's own lesson (M36-1) treats the surviving AUR wording as
"kept as history" on purpose; the defect is that the *claim sentence* says "moved" while the *predicate*
only says "holds a Core row", i.e. claim and predicate have different truth conditions.

### N2 — the knowledge entry body is unmeasured (T6)

`c1-counter.py:204-210` reads the entry only for existence and for `source:`-line ids. Replacing the 16,477-byte
entry with 47 bytes stays green:

```
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107"], "opened_source_rows": ["S107"], "province_core_row": true, "province_core_section": true, "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true, "revision": "c63adefb2b592437cbca350bb47c8e447445a3b1"}
```

stub bytes, `git show c63adef:corpus/knowledge/… | od -c` (verbatim):

```
0000000   #       S   t   u   b  \n  \n   s   o   u   r   c   e   :
0000020   S   1   0   7     342 200 224       o   n   e       l   i   n
0000040   e   ,       n   o       c   o   n   t   e   n   t   .  \n
0000057
```

47 bytes, 45 characters (the em dash is `342 200 224`). A green C1 therefore establishes "a file with that
name exists and names a source"; the claim's "knowledge entry" is not measured.

### N3 — source-row provenance is existential, not universal (T2 vs T2b)

The entry cites `S107, S108, S109`. Blanking the `opened` cell of **all three** is caught (`opened_source_rows: []`,
exit 1, rev `cd9c6807f957`). Blanking only S108+S109 is **green**:

```
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107","S108","S109"], "opened_source_rows": ["S107"], "province_core_row": true, "province_core_section": true, "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true, "revision": "9ef15532bf1aa5b5b9b0320dcccf1e0e6759ee2f"}
```

At that revision, `corpus/SOURCES.md:114` and `:115` read `opened=[  ]` with used-by intact
(`awk -F'|' '/S10[789]/ {…}'`). Two of the three citations the entry leans on may carry no opened date at all.
This matches the predicate's literal wording ("cites **a** SOURCES.md row opened 2026-10-26"), so it is a
predicate-strength calibration datum, not a counter bug.

### N4 — registry duplicate ids let a shadow row carry the provenance (T5)

Real rows degraded to `opened 2026-10-25` / used-by `corpus/lessons/round-36.md` (`corpus/SOURCES.md:113,114,115`),
then three appended rows with the same ids at `:118,119,120` carry `opened 2026-10-26` / used-by the entry.
Green:

```
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107","S108","S109"], "opened_source_rows": ["S107","S108","S109"], "province_core_row": true, "province_core_section": true, "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true, "revision": "87abc70a71c6350eb6d99206e2b7bc21d6cb557b"}
```

`c1-counter.py:212-223` collects every row whose id is cited, with no uniqueness test, so the registry can hold
two contradictory rows per id and the entry's citation no longer identifies a document. This is the C1 analogue
of the lesson's M36-3 (duplicate shadow) class; wave 1 did not test it. No instrument in `tools/` tests SOURCES
id uniqueness: `grep -rn duplicate tools/` returns 33 hits, all JSON-member / oracle-case / freeze-integrity
checks (`tools/round-25/*`, `tools/round-34/*`, …) and none referring to `SOURCES.md` or a registry row
(`grep -rn duplicate tools/ | grep -i 'sources\|S1[0-9][0-9]\|registry'` → no output). The `citation-drift`
gate pins 60 specific citations and none of them is a SOURCES row id (`pointer-table.json` contains
`receipts-B` 0×, `ScoutSkillPlacement` 0×, `knowledge files mapped` 0×).

### N5 — the coverage-map binding is one substring test (T7)

Rewriting the round-36 map row's entry cell to "(indexed only, not mapped here)" and leaving the stem in the
row's prose cell keeps `coverage_map_row: true` (rev `6e9079d049d0`, exit 0) — the entry is no longer a *row*
of the map (command A's `mapped` would drop by one) while the binding is satisfied. The predicate does not
mention the coverage map at all; this is an extra binding whose mechanism is `STEM in line`
(`c1-counter.py:227-228`).

### N6 — the only committed record of the invocation is unread (T8)

Deleting all four `corpus/evidence/round-36/c1/K*/after-run.json` (530, 532, 543, 542 bytes) keeps
`carriers_matched: 4`, exit 0 (rev `91ab096a3f91`). The predicate names only the envelope; nothing reads the
run record (sasquatch path/version, REA exit code, carrier path). Combined with wave-1's F1 (a fabricated
envelope re-hashed with REA's own rule scores 4/4), the capability clause rests entirely on claimant-authored
envelope bytes and **even the invocation record can be removed at zero cost**.

## 5. C2 findings, with the exact counter output

### G1 — revert one repaired pointer, add a duplicate box: red → green (U1, U2, U3)

This is the assignment's example, measured at the landed state:

- U1 (revert only, rev `11a78c23135a`): exit 1,
  `{"assertion_mismatches": [], "guards_ok": false, "met_target": false, "mismatches": 1, "revision": "11a78c23135abc7c16221586d593cbcabc4837ed", "unresolved": [["shonen:No cross-domain bleed (PROVINCE.md still accurate)", "ScoutSkillPlacement.md"]]}`
- U2 (revert **+ duplicate box appended at EOF**, rev `35a8e28b6892`): exit 0,
  `{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "35a8e28b6892932bc957263b9d7016ef9c83d98c", "unresolved": []}`
- U3 (revert **+ duplicate box inserted before the real box**, rev `ab40b45b1f5b`): exit 1, identical
  `unresolved` to U1 — the mechanism is pinned: `units()` keys SHONEN boxes by title and **the last occurrence
  wins** (`c2-counter.py:81-86`), so a duplicate is scored and the original is not.

At U2's revision the scored file contains, in the same SHONEN box set:

```
SHONEN.md:11  - [~] No cross-domain bleed (PROVINCE.md still accurate)
SHONEN.md:12    asserted boundary only: … (w1 `ScoutSkillPlacement.md`); …
SHONEN.md:13  - [~] No cross-domain bleed (PROVINCE.md still accurate)
SHONEN.md:14    asserted boundary only: `PROVINCE.md:97-125` (duplicate … repaired pointer `.ufo/waves/round-30/w1/ScoutSkillPlacement.md`)
```

`grep -o '(w1 `ScoutSkillPlacement.md`)'` on `35a8e28:SHONEN.md` → `(w1 \`ScoutSkillPlacement.md\`)`;
`git cat-file -e 35a8e28:ScoutSkillPlacement.md` → absent. So P36-C2's "every backticked repo pointer in them
resolves at that revision" is **false** at a revision the counter scores `met_target`. Note also
`pointers: 38` vs 41 at the tip: the real box carries 5 pointers and the duplicate carries 2, so shadowing
removes `PROVINCE.md:8-14`, `PROVINCE.md:24` and `corpus/lessons/2026-10-15-round-1.md` from measurement while
the count guard (base 34, `c2-counter.py:226-228`) absorbs the loss.

### G2 — the same shadow on a Capabilities row (U4)

Row 619 reverted to base's evidence cell and a duplicate row appended at `:620`:

```
SCORECARD.md:619  | pre-registered two-lane live battery on REA 6.5.0 | … | `.ufo/waves/luna-round-6/receipts/` + `receipts-B/`; … |
SCORECARD.md:620  | pre-registered two-lane live battery on REA 6.5.0 | … | `.ufo/waves/luna-round-6/receipts/` + `.ufo/waves/luna-round-6/receipts-B/`; … |
```

`git cat-file -e 4319c68:receipts-B` → absent; counter exit 0,
`{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "4319c6817ea5d5c0366f4e0043b0c039ade621a4", "unresolved": []}`.
The base-unresolved pointer is back inside the scored surface and P36-C2's pointer clause fails again.

### G3 — the same shadow on a count (U5)

`SCORECARD.md:23` reverted to `116/116 knowledge files mapped`; duplicate `coverage` row appended at `:24`
stating `124/124 knowledge files mapped (recount row)`. Counter exit 0,
`{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "8191c4663f37681aabd28f2efdfff8885d94130b", "unresolved": []}`.
The false count sits inside `## Owned axes` — the surface P36-C2 names — and `O1` reads only the
last-inserted row under the key `owned:coverage`.

### G4 — a range the pointer parser cannot parse is invisible (U6)

Two runs, same mechanism. **U6**: correct `PROVINCE.md:97-125` retained, `PROVINCE.md:95-116 ` (trailing space
inside the backticks) appended to the same box — exit 0, `unresolved: []`, `assertion_mismatches: []`,
`pointers: 41` (rev `c4bce984f120`). **U6b** (fresh fixture): the same slot carrying `PROVINCE.md:1-9999 ` — an
out-of-file range, the exact class wave-1 V15 rejects when it is parseable — exit 0,
`{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "194b76057e8b5d0951de39a633c0c3f40abdf4dd", "unresolved": []}`
(rev `194b76057e8b`, base `2b42f4b7b06e` of that fixture; `grep -o 'PROVINCE.md:1-9999 '` returns the text).

`TOKEN = re.compile(r'`([^`\s]+)`')` needs a non-space run closed by a backtick, so neither token is resolved,
counted, or seen by `stated()`. A formatting quirk removes a statement from the surface entirely: the same
out-of-file range is red as a parseable token (V15) and green four characters later with a trailing space.

### G5 — "repaired by a resolving pointer to the same document" is unimplemented (U7)

The Capabilities evidence cell was pointed at `.ufo/waves/round-36/w2/receipts-B/` with a single planted
`PLACEHOLDER.txt` (`git ls-tree … .ufo/waves/round-36/w2/receipts-B` → one file); the honest target
`.ufo/waves/luna-round-6/receipts-B/` still exists (12 files). Counter exit 0,
`{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "1261db399c4389ed9105f857e872efb762db95f7", "unresolved": []}`.
The repair guard matches a basename suffix (`c2-counter.py:220-225`), so the clause is satisfied by any
document whose last path component matches. Wave-1 A4 demonstrated this against the base; U7 shows it survives
the repair, on the pointer the repair introduced.

## 6. Calibration — what the frozen counters do catch

Observed red, correctly: **T1** (`after := before` on K2 → 3/4, K2 `after_sasquatch_gap true`,
`after_oracle_hits 0`), **T2** (all three opened cells blank → `sourced: false`), **T3** (Core row moved out of
the round-36 section → `province_core_row: false`), **U1** (pointer revert without a shadow → 1 unresolved,
`guards_ok: false`), **U3** (same edit with the duplicate placed first → red; the shadow is order-dependent).
The after/before discrimination, section membership, source-row date binding and the unresolved-pointer guard
are real. The defects are in *what the surfaces are allowed to contain twice* and in *which surfaces are read
at all*.

## 7. Smallest safe corrections (advisory; nothing was edited)

The predicate, counters, carriers and oracle are frozen for round 36, so none of this is applied.

1. **C2, one change, closes G1/G2/G3.** Index every row/box occurrence instead of a dict keyed by unit name
   (`f'{key}#{n}'`), validate statement shapes with `findall` over all occurrences, and resolve pointers over
   all of them. (Wave-1 §corrections 2–3 said the same; U1/U2/U3 supply the before/after pair that proves the
   mechanism at the landed state, and U3 shows the fix must not depend on order.)
2. **C2, one change, closes G4.** Scan the three surfaces for `[A-Za-z0-9_./-]+\.md:\d+` *without* requiring
   backtick framing, and treat any hit as a stated range to validate. A formatting quirk must not remove a
   statement from the surface.
3. **C2, one change, closes G5.** Name the intended documents in the claim at freeze time and compare exact
   paths (`base path` or a relocation the claim names) instead of a basename suffix.
4. **C1, one change, closes N1.** Delete the word "moved" from the claim, or add the clause that makes it
   measurable: the named old surface must be absent, or carry an in-place dated supersession that cites the
   entry — and bind `corpus/README.md`'s **Firmware row** (today *no* binding reads it: the only README binding
   is the `## Coverage map` section, `c1-counter.py:227-228`).
5. **C1, one change, closes N2.** Require the entry to carry the measured facts (carrier ids, oracle file
   counts, the counter path) — e.g. the four `oracle_files` values `3/4/2130/2130` and the entry stem — instead
   of only its existence.
6. **C1, two changes, close N3/N4.** Make the provenance clause universal over the entry's cited ids
   (every cited row must be opened 2026-10-26 with used-by listing the entry) and require S-ids to be unique
   across the registry.
7. **C1, one change, closes N5.** Match the coverage-map row by shape: the row's entry cell must *equal* the
   stem, not contain it.
8. **C1, cost-raiser only, closes N6 partially.** Require `K*/after-run.json` to agree with the envelope, or
   pair the receipt with an out-of-band re-run witness (wave-1 §8 items 1–2). This raises cost; it does not
   authenticate the bytes.

## 8. Impacted axes

- **coverage (C1's own axis).** The claim moves a surface Frontier → Core. At the tip, both named old
  statements survive (README Firmware row byte-identical; PROVINCE bullet unchanged), and the counter cannot
  see them (T4 green, T3 red only for the Core side). The entry body is unmeasured (T6), the source-row
  provenance is existential (T2b) and shadowable via duplicate ids (T5), and the map binding is a substring
  test (T7). A green C1 receipt does not establish the coverage move it is filed under.
- **calibration (C2's own axis).** Three predicate-level falsifications at the landed state (G1/G2/G3): the
  scored surfaces can carry a non-resolving pointer and a stale count while the receipt reports zero
  mismatches. G4/G5 add two ways a false or decoy statement stays green. The tip C2 receipt is therefore not
  evidence about the surfaces' content; the honest repairs are correct on inspection but the *instrument*
  cannot say so.
- **falsifiability / kill rules.** None of the frozen controls (`CTL-C1-0..2`, `CTL-C2-0..3`) has any of these
  shapes (T4/T5/T6/T7/T8/U2/U4/U5/U6/U6b/U7), so the kill rules could not have fired on them. Wave 1 reached the
  same conclusion for fabrication (C1) and duplicate units (C2) on pre-landing fixtures; this wave confirms
  both classes survive the landing and adds six flat-surface and two parse/decoy classes.
- **depth.** Not touched by these controls. `[INFERENCE]` the same duplicate-unit mechanism applies to the
  depth row's `17/17` and `SKILL.md:81-314` statements, since they are read by the same `units()` map.

## 9. Limits and disclosure

- No REA invocation, no `extract-firmware` run, no network, no sasquatch/unblob execution this seat. I did not
  re-run wave-1's fabrication class (F1) or the C1 harness: cost, and both are already measured.
- The fixture re-commits the three trees, so its freeze/base/tip commit ids differ from the lane's
  (`8320591`/`93cc119`/`b1f848e`); every file the counters read was hash-compared (§2) and the fixture's
  receipts equal the lane's modulo those ids.
- Control revisions quoted above (`b0a00b0…`, `35a8e28…`, …) are commits in the scratch fixture, which was
  removed after the run. Every counter output cited is inlined in §3–§5; no /tmp or scratch path is offered as
  evidence.
- `[INFERENCE]` markers: the reading of P36-C2's "the four stated counts" as covering a fifth, contradictory
  stated count (G3); the depth-row extrapolation in §8; the intent reading in N1.
- Installs: none. `pacman` untouched (host-wide pause respected). VCS: read-only in the lane
  (`git show/log/ls-tree/archive/rev-parse/cat-file`); all fixture mutations used `git -C $D`, whose
  `rev-parse --show-toplevel` equals `$D`, checked before the first commit. Scratch
  `/fast/scratch/hyaku/kaidoku-r36/R36W2CriticDoNothing` removed before this report was finished.
