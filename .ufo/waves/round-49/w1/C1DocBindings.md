# C1DocBindings — round 49 wave 1 (pre-freeze): attack on the six C1 documentation bindings

Seat: C1DocBindings (leaf, no subagents). Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`.
Counter attacked: `draft/tools/round-49/c1-counter.py` (sha256 `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779`),
scored at a throwaway dev freeze `bc6838e650b65a6e03b256ef489871503ec4c296` (built by `mkclone.sh`; not the real freeze).
Tooling installed: none. Nothing in the lane tree, plan, drafts or fleet state was written; all mutation
happened in scratch clones, removed after the receipts were copied here.

## Verdict

**The six documentation bindings are not closed against hollow text.** With genuine REA 6.5.0 receipts
(the real `CTL-C1-POS` capture) in place, a documentation set that asserts the *opposite* of the promotion
(`not promoted`, `remain Frontier`, `placeholder`) still scores `exit 0`, `met_target true`,
`carriers_matched 4`, `failing []` (variant 16). Each binding is also satisfiable alone (variants 02, 04,
05, 07, 09, 10, 11, 13, 15, and the registry-free copy 17). The bindings do catch *absence*: a missing entry
file (01), a row without the entry path (03), a README map without the stem (14), a registry that does not
list the entry (12), an empty entry (08 fails only on `sourced`). They are presence checks, not
truth checks.

The L1 should state this limit in the plan. Two consequences for the freeze, for the L1 to decide:

1. A documentation-only counterfactual reaches `met_target true` with real receipts (variant 16 hollow set;
   variant 17 copy of last round's entry). The plan's kill rule ("any counterfactual control reaching
   `carriers_matched == 4` with every binding true stops C1") would fire if such a control were added. The
   frozen control list (CTL-C1-0..5, POS) contains none, so the rule is silent here. Either add a
   documentation-hollow control (accepting that it reds the claim) or state the limit in the claim text.
2. The drafted landing text contains prose that is false for round 49 and that no binding reads (F1–F6
   below). It must be replaced at landing; the counter will not catch it.

## What was run

| step | command | exit | result / sha256 |
|---|---|---|---|
| build dev-freeze clone | `TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku bash .../draft/mkclone.sh $S/clone` | 0 | `DEV_FREEZE=bc6838e650b65a6e03b256ef489871503ec4c296` (receipts/mkclone.out sha `c330cb47e704343b68fd170e86e9f18ce0e9d0e316442eb61d40e062c76474a0`) |
| real REA 6.5.0 POS capture + draft landing (scratch) | `bash .../draft/run-ctl.sh $S/clone $S/ctl --controls pos` | 0 | CTL-C1-POS `as_expected`, exit 0; controls stdout sha256 `7014f8f31b959903cb5558c1b458f6ee048747a4a67bd1656e36ed6d9a717c22`; receipts/ctl-pos.json sha `7ddc3c02080d3d5c5d0209a02fab7a7d7d5286fb1c85989b6f7010707feed9b0`; POS counter (`ctl-out/pos/counter.json`) sha `1552384f36e223614780bf75e9bc5e76fb35d137d5335c1aa411e3ef3a197d57`, `met_target true`, `carriers_matched 4` |
| hollow-text variants 00–18 | `python3 -I -B att/attack.py <POS sandbox> bc6838e650b65a6e03b256ef489871503ec4c296` | 0 | 19 commits on the POS HEAD `31a1e424…9086` in a scratch clone; each scored by the draft counter in full scoring mode (REA rerun included); receipts/results.json sha `4a52ce23b2b5e0332a45624dbd8a0bb628a61af05845484fc6f2b72123964ac8` |
| harness | — | — | receipts/attack.py sha `bec456354a44c23718f49decbf9fe605901e8417d281f2b06f7da64b2143d09b` |

Digests of the inputs read (full values in receipts/input-sha256.txt): draft plan `984e1026234d66af94b3c6e250e65784dd05141f4c4c7db1f624bb7970a9f492`; `c1-controls.py` `209f0f4ad0568a6e845b72dcd8ca5102caa13423884391dd9a92398e26d087a4`;
`block-a` `1c98017b6e49d6b00bee21a410d2599e51f9b0d63a62c8d8d4d30896a6628ae1`; `block-b` `50f4e2ec1e9a424332373b3e1702cb9e03f1daa77df3004a84d8a6455e0b480b`; `block-c` `a1dffe829f68be83aa8472d5bd3ba1c078a9ad5f6cdfbed027c66bfa6c94fe8b`; entry draft `074c91018a7b4c587ec864ba631201714f4ab436dcb746046187aed71304a07d`.

Scope note: the POS landing (`_doc_landing`) is the draft landing as the controls driver plants it into a
sandbox commit. Receipts are real REA 6.5.0 runs captured in scratch, not the data run. The counter ran in full
scoring mode (not `--dev-arm`); bindings are computed on that path. Each variant is one commit whose changes are
documentation bytes only (`patches/NN_*.patch` = the diff against the POS landing).

## Variant results

`T` true / `F` false. Carriers 4/4 and `failing []` in every row. Exit 0 = met, 1 = not met.

| # | variant | intent | exit | met | prov_sec | prov_row | front | entry | sourced | cov_row |
|---|---|---|---|---|---|---|---|---|---|---|
| 00 | POS baseline (draft landing) | must be green | 0 | T | T | T | T | T | T | T |
| 01 | entry file deleted | control | 1 | F | T | T | T | **F** | **F** | T |
| 02 | Core row: "**not promoted**, both stay Frontier"; still names both handlers, family text and entry path | hollow row | **0** | T | T | T | T | T | T | T |
| 03 | Core row without the entry path | control | 1 | F | T | **F** | T | T | T | T |
| 04 | whole `## Round-49 additions to Core` section wrapped in a ``` fence (renders as literal text) | hollow section | **0** | T | T | T | T | T | T | T |
| 05 | frontier note: "`<stem>` is an empty placeholder; SquashFS v1/v2 remain Frontier and supersede nothing" | hollow note | **0** | T | T | T | T | T | T | T |
| 06 | frontier note with no "SquashFS v1/v2" phrase in its prose ("supersedes the frontier clause for the handler family") | attempted control | **0** | T | T | T | T | T | T | T |
| 07 | entry body is only `source: S138 (see registry)` / `source: S139 (see registry)` | hollow entry | **0** | T | T | T | T | T | T | T |
| 08 | entry file exists, zero bytes | entry_present = existence | 1 | F | T | T | T | **T** | **F** | T |
| 09 | entry: `source: none …; S138 and S139 are named here only so the registry binding can read them` | tokens in non-citation | **0** | T | T | T | T | T | T | T |
| 10 | SOURCES: appended forged duplicate S138/S139 rows (status `rejected`, same opened date and used-by) | duplicate row | **0** | T | T | T | T | T | T | T |
| 11 | SOURCES: S138/S139 status cell `rejected` | status ignored | **0** | T | T | T | T | T | T | T |
| 12 | SOURCES at lane base (no used-by append) | control | 1 | F | T | T | T | T | **F** | T |
| 13 | README row labelled `(round 49)`, stem kept, status **Frontier — not promoted** | hollow map row | **0** | T | T | T | T | T | T | T |
| 14 | README row without the stem | control | 1 | F | T | T | T | T | T | **F** |
| 15 | README row keeps the literal `<AFTER-DATA: …>` placeholder (`block-c` as drafted) | placeholder not rejected | **0** | T | T | T | T | T | T | T |
| 16 | **all documentation hollow together**: row negated, note negated, section fenced, entry = two bare `source:` lines, registry `rejected`, README Frontier | headline | **0** | **T** | T | T | T | T | T | T |
| 17 | round-44 entry bytes copied to the round-49 path (registry appended, rest POS) | copy-last-round | **0** | **T** | T | T | T | T | T | T |
| 18 | variant 17 + README row copy | copy-last-round | **0** | **T** | T | T | T | T | T | T |

Variant 06 was meant as a token-free control; it is green because the stem itself,
`2026-10-28-r49-squashfs-v1v2-core` (in backticks in the note), matches the counter's
`SQFS12_TEXT_RE` (`squashfs-v1`, IGNORECASE; checked by `python3` regex, `group(0) == 'squashfs-v1'`).
So `frontier_note`'s "SquashFS v1/v2 token" is supplied by the file name, not by the prose.

Reading: every binding that is green has a hollow variant that stays green (02/04 section and row, 05 and
06 note, 07/09/10/11/17 `sourced`, 08 `entry_present` alone, 13/15 `coverage_map_row`). Each control expected
to go red does go red (01, 03, 12, 14; 08 reds `sourced` only). The bindings are presence checks.

### Per-binding verdict

| binding | counter reads | satisfiable by hollow text? | variants |
|---|---|---|---|
| `province_core_section` | first exact line `## Round-49 additions to Core`; lines to the next `## ` | **yes** — heading inside a ``` fence still matches (`lines.index`) | 04 |
| `province_core_row` | a `|` line in that section containing literal `squashfs_v1`, `squashfs_v2`, a SquashFS v1/v2 regex match and the full entry path | **yes** — negated row carrying the tokens and the path | 02 (red: 03) |
| `frontier_note` | any line anywhere in PROVINCE.md containing `Round-49 frontier note`, the stem and a v1/v2 regex match | **yes** — negated / placeholder note; the stem alone supplies the v1/v2 match | 05, 06 (red: none tested — the stem always matches) |
| `entry_present` | `git show REV:<entry>` is not None | **yes** — zero-byte file (existence only) | 08 (red: 01) |
| `sourced` | `source:` lines of the entry (any S-token anywhere on them) ∩ {S138, S139}; registry rows with those ids, 11 cells, opened == `2026-10-28`, used-by contains the entry | **yes** — bare `source:` lines (07), tokens in a non-citation sentence (09), forged duplicate rows (10), status ignored (11), round-44 entry copy (17) | 07, 09, 10, 11, 17 (red: 01, 08, 12) |
| `coverage_map_row` | any `|` line in `## Coverage map` containing the stem | **yes** — negated row carrying the stem; unreplaced `<AFTER-DATA>` placeholder | 13, 15 (red: 14) |

### Facts the same runs establish outside the six bindings

- `sourced`'s date half is **already true at the lane base**: `corpus/SOURCES.md` at `e4f2cfa5` has S138
  and S139 with `opened 2026-10-28` and used-by = the round-44 entry (`git show e4f2cfa5:corpus/SOURCES.md`).
  Round 44 wrote that state on the same calendar day. The counter cannot tell a round-49 re-open from the
  round-44 open; only the appended used-by cell is round-49-specific (variant 12 red).
- The counter reads no lesson, no access log and no fetch timestamp; "re-opened this round" in the plan is
  not measured by any binding.

## Findings for the L1 (landing text and plan)

Each is text the drafts would land. None is read by a binding; each is checkable by a reviewer against the
cited bytes. None is a counter patch.

- **F1 — the draft entry names the round-44 freeze as the round-49 freeze.** The entry draft's status block
  says "against the round-49 freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`". That commit exists and is
  `round-44: freeze C1/C2 claims, carriers, counters, and controls` (2026-10-28 09:35:19 -0300;
  `git log -1 c48f8a4b…`), an ancestor of the base. The `recheck:` line repeats it.
- **F2 — the draft entry cites round-44's receipt as this round's scored run, with a dead hash.**
  "Scored-run receipt `.ufo/waves/round-44/controls/pos/counter.json` (revision `6b58a898…`)".
  `git rev-parse --verify -q 6b58a898` finds no object in the lane. This is the A2 class (dead commit hash)
  written into the new entry. The `carriers_matched 4/4`, `met_target true`, `counter sha256 9f2cc140…`,
  `failing []` values in that block are round-44 values stated in the present tense; they are not measured
  this round and must be replaced with the frozen-counter receipt after the data run.
- **F3 — round-44 fetch evidence is presented as the round-49 re-open.** The S138/S139 lines in the draft
  read "the round-44 listings were fetched … 2026-10-28T11:10:29Z–11:12:37Z; manifest … sha256
  `4bc53dbb…`". The plan says S138/S139 are re-opened this round with the access date in
  `corpus/lessons/round-49.md ## Gate`. No round-49 access record exists in the drafts. Either record a round-49
  access (new timestamps and snapshot digests) or write "opened in round 44, not re-opened" and drop the
  plan's "re-opened" wording.
- **F4 — the two landing drafts cite different registry rows for the same handler lines.** `block-a` (PROVINCE
  row) cites `S108 :101-102, :158-159`; the entry cites `S112 :101, :158`. S112's registry scope reads "v4 BE
  extractor dependency and argv for unblob 26.6.4 only; not the binaries themselves, not other versions", with
  anchor "`SquashFSExtractor` lines 24-70"; the v1/v2 handler classes sit at :101–196, outside that anchor. S108's
  scope names "how unblob 26.6.4 names and invokes its SquashFS extractors … the LE/BE argv". The entry should
  cite S108 for handler names, or S112's scope and anchor must be widened. No binding reads this.
- **F5 — the `<AFTER-DATA: …>` marker is not rejected.** `block-c` (README row) carries
  `<AFTER-DATA: frozen-counter receipt headline — …>`. `_doc_landing` replaces it only inside the control
  fixture. A landing that forgets the replacement keeps the marker, and variant 15 shows `coverage_map_row`
  still true. The plan's "quote the receipt, never this marker" is an unchecked text rule; add a grep
  (`grep -c '<AFTER-DATA' corpus/README.md` must be 0) to the data-run procedure, or state it as unchecked.
- **F6 — the README row shares a label with the round-44 row.** Both coverage rows begin
  `SquashFS v1/v2 through REA (round 44)`; the round-49 row differs only by the stem. Not a defect in itself,
  but a reader of the map sees two rows with one label. Relabel the round-49 row when landing.

## Limits of this attack

- The dev freeze is a throwaway commit; the real freeze differs. The bindings do not read the freeze hash, so
  the variant results carry over; the pasted freeze hash in the entry (F1) would not.
- The frozen-path check was not exercised (all variants touch documentation bytes only).
- Not tested: a stale duplicate `## Round-49 additions to Core` heading earlier in PROVINCE.md (the counter uses
  the first exact match); a SOURCES row with a non-11-cell layout; a `frontier_note` red arm (the stem always
  matches the token regex, so no stem-bearing line can be red on the token). Not run, not claimed.
- Carriers were not re-measured in this seat; `carriers_matched 4` in every row comes from the real POS
  captures in scratch.

## Receipts (in this directory)

- `receipts/mkclone.out`, `receipts/pos-run.out`, `receipts/ctl-pos.json`, `receipts/pos-counter.json`,
  `receipts/pos-summary.json`: the POS build and capture.
- `receipts/attack.py`, `receipts/run2.out`, `receipts/results.json`, `receipts/variants-results.json`: the
  harness and its outputs (19 variants: exit, counter stdout sha256, bindings per variant).
- `receipts/input-sha256.txt`: sha256 of the draft counter, controls driver, plan, the three landing blocks and
  the entry draft read by this seat, plus the receipts above.
- `patches/NN_*.patch`: the per-variant documentation diff against the POS landing (variant 00's patch is the
  POS landing itself).

Reproduce: (1) `TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku bash .../draft/mkclone.sh $S/clone` → `DEV_FREEZE=bc6838e6…`;
(2) `bash .../draft/run-ctl.sh $S/clone $S/ctl --controls pos` → exit 0; (3)
`python3 att/attack.py <$S/ctl/ctl-work/run.*/sandbox-pos> bc6838e6…` → 19 rows in `att/results.json`.
