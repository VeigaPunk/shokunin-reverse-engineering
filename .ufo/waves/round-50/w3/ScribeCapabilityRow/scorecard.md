# ScribeCapabilityRow — paste-ready SCORECARD landing drafts (round 50, attempt 2)

Seat: `ScribeCapabilityRow` (wave 3, build wave). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Drafted at lane tip `addbfb4df0d33fedff51d46f2a983a5bd8ea0c10`; the tip advanced **five** times under me
during this wave (`6f4aba63` pinned the entry stem to the frozen counter's constants; `03f852b9` moved the
C3 instrument to `tools/round-50-c3/`; `d71829bf` folded the C3 pre-freeze amendments; `1439dfe9` landed
the C3 freeze + table v5; `addbfb4d` landed the C3 after-score). All three drafts below are **paste-ready
blocks for the L1 to integrate**; nothing here was written into the lane tree.

**Two facts changed under me and are reflected below:** (a) the C3 table v5 landed as **rule block 26** (the
claims file was corrected from "block 22" in the same commit `1439dfe9`; `SKILL.md`'s craft section now holds
26 bullets, the v5 bullet being the 22nd `- **` bullet and self-labelled "26."), so BLOCK 2's depth row and
BLOCK 3's depth head say 26/26; (b) the C3 before-state is **19** no-reader `clean`/`none` `_ddefault` rows,
not the four v2ns the earlier claims text named — the amended claims (`d71829bf`) already say 19, and I
measured 19 at handler level (4 v2ns + 7 v3_broadcom + 8 v3_nonstandard).

Read the plans, not this file: `plans/round-50-attempt2-claims.md` (R50-C1, R50-C3, landing order 1–4) and
`plans/round-50-claims.md` (R50-C1 section, the frozen predicate).

---

## BLOCK 1 — capabilities-table row (new row, append after `SCORECARD.md:632`)

Insert as the **last row of the `## Capabilities` table**, between the round-49 row (line 632) and the
blank line 633. The table header (`:617`) is `| Capability | What it can now do | Evidence pointer |
First-working round |` — four cells, so the row must have exactly four cells.

**Paste-ready row (single line, no wrapping):**

```
| AVM LE SquashFS v4 carrier custody + REA extraction | holds four chain-pinned public FRITZ!OS little-endian SquashFS v4 members (FRITZ!Box 7581/7582 07.18, 6490 Cable 07.57, 6430 Cable 07.30; `hsqs` v4.0 xz, `mkfs_time == bytes_used`) end to end — vendor image URL → image sha256 → tar-member sha256 → carve to `bytes_used` → carrier sha256 — and has REA 6.5.0 `extract-firmware --max-depth 1` publish every regular file of an independent oracle (unsquashfs 4.7.5 listing + per-file sha256; the lane's pure-Python `tools/round-41/sqfs-list.py` `auto` layout as the second reader) at its exact path relative to the chunk extract root, with the same sha256 and size and no extra regular file; the four carriers are never committed (AVM licence), so the receipts and the frozen oracle tables are the durable evidence | `corpus/evidence/round-50/c1/`; counting command `python3 -I -B tools/round-50/c1-counter.py --root <LANE> --rev <REV> --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --pkg65 <rea-agents 6.5.0 package root> --work <SCRATCH> --carrier-cache <CACHE> --json-out <OUT>` → `carriers_matched 4`, every binding true, `frozen_path_changed []`, exit 0 (receipt `.ufo/waves/round-50/l1/scores/c1-at-<REV>.json`) | 50 |
```

Notes the L1 must apply when pasting:

- **Gate: only paste this row if the C1 data run lands green** (`carriers_matched == 4`, exit 0). Per
  `AXES.md:62-64`, a capability row enters only through a round that demonstrates the capability running;
  a row pasted before the data run is pre-claiming. If C1 stops, delete this row and use the BLOCK 2
  "not met" wording instead — do not soften the claim.
- The row is append-only in the table (after `:632`); it does not rewrite the round-36 / round-41 /
  round-49 rows, whose own "Big-endian/AVM not demonstrated" wording stays as history.
- The evidence-pointer cell must name the **committed** receipt path. `corpus/evidence/round-50/c1/` does
  not exist yet at this tip (only `corpus/evidence/round-50/c2/` does) — it is created by the C1 data run.
  Landing the row before the run would leave a dangling pointer.
- Keep the phrase "never committed (AVM licence)" in the row: the carriers are chain-pinned and are not
  in the repo, so the capability is "custody + extraction", not "the images are held".

---

## BLOCK 2 — `## Round 50, attempt 2 (2026-10-29)` section skeleton

Mirrors the shape of `## Round 34, run-6 re-dispatch (2026-10-25)` (`SCORECARD.md:3353-3372`): a
re-dispatch heading that names what is inherited and what is re-run, a claims table with
before/after/counting-command columns, a freeze-and-receipts paragraph, an owned-axis table, a learning-trends
paragraph, and `planned` / `retired` bullets.

**Paste-ready block** (append at the end of `SCORECARD.md`, after the existing `## Record corrections —
round 50` section; the file currently ends at line 3811):

```
## Round 50, attempt 2 (2026-10-29) — C1 resumed under the frozen bytes, C3 depth added, both landed FILLED-AT-LANDING

Base `f890bbead20ca2c549487167f56876ae47f1e1a4`; the attempt-1 work and its honest stop above are inherited
and are not rewritten. Attempt 2 adds one claim (R50-C3, depth) and resumes R50-C1 under the **same**
frozen bytes: `git diff --stat 435d41fd4ad9211d1579fc447936fb33d2b74467 <TIP> -- tools/round-50/ plans/round-50-claims.md tools/round-41/sqfs-list.py tools/round-27/xpin-attribute.mjs` is empty (receipt `.ufo/waves/round-50/l1/frozen-unchanged-attempt2.txt`), so no new C1 freeze and no amendment. The REA-dependent controls and the C1 data run happen **after** this wave, in the quietest window the host offers.

| claim / surface | before | after | counting command | verdict |
|---|---|---|---|---|
| R50-C1 / coverage — genuine AVM-marker LE SquashFS v4 (`hsqs`), four chain-pinned vendor carriers, Frontier → Core | at the freeze exit 1, `carriers_matched 0` (CTL-C1-0, `.ufo/waves/round-50/controls-attempt2/c0/`, counter exit 1, `met_target false`, 60 failing clauses, `bindings_false` 6) | FILLED-AT-LANDING | `python3 -I -B tools/round-50/c1-counter.py --root <LANE> --rev <REV> --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --pkg65 <rea-agents 6.5.0 package root> --work <SCRATCH> --carrier-cache <CACHE> --json-out <OUT>` | FILLED-AT-LANDING |
| R50-C3 / depth — triage table v5, the no-independent-reader rule table v4 lacks, landed as `SKILL.md` rule block 26 (`1439dfe9`) | at the declared base `f890bbea` the same command exits 1 with the 19 no-reader `clean`/`none` `_ddefault` rows among the mismatches (4 v2ns + 7 v3_broadcom + 8 v3_nonstandard; receipt `.ufo/waves/round-50/c3/c3-before.json`, `pair_mismatch_count 19`) | **already landed**: `verdict met`, `pair_mismatches 0`, `evaluator_missing 0`, `n_envelopes 126`, table v5 matched the independent evaluator on all 126 held-out envelopes; mutation battery green (receipt `.ufo/waves/round-50/c3/c3-after.json`) | `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root <LANE> --rev <REV> --freeze <FREEZE> --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes --json-out <OUT>` | **met under the frozen rule** — the four semantic-red controls each score red on `pair_mismatch_count`: do-nothing 19, junk 126, guard-deleted 26, action-swapped 51 (receipts `.ufo/waves/round-50/c3/ctl-*.json`) |

Freeze and receipts: C3's freeze commit `1439dfe9` (instrument `tools/round-50-c3/sqfs-triage-v5.py` +
its `instrument-registry v2` row + `SKILL.md` rule block 26) precedes any C3 data, and the C3 after-score
`addbfb4d` follows it; the C3 receipts are `.ufo/waves/round-50/c3/c3-{before,after}.json`. The C1 controls
land at `.ufo/waves/round-50/controls-attempt2/`, and the C1 data run writes
`corpus/evidence/round-50/c1/<id>/{after.json,run.json}`. The vendor carrier bytes are chain-pinned and
never committed (AVM licence); only hashes, listings and receipts enter the lane.

| Owned axis | Before → after | Verdict |
|---|---|---|
| coverage | 10 → 10 (index only; one knowledge entry added and mapped, no domain surface) | FILLED-AT-LANDING |
| depth | 10 → 10 (finite proxy saturated; the C3 rule block is the move) | FILLED-AT-LANDING |
| calibration | 10 → 10 (a finite proxy over the atoms its counters name, not an expertise score) | FILLED-AT-LANDING |

Learning trends: expansion **improved** if the C1 entry is admitted (one new knowledge file on LE-AVM ground);
quality **improved** only for the C3 rule (the v4 table's no-reader mis-routing is repaired and the
instrument that scores it is frozen and battery-tested); discernment **unchanged** (the round-49 closure's
F1/F2 disagreements became the C3 claim; the outside spot-check remains the operator's).

- **planned:** FILLED-AT-LANDING
- **retired:** none.

## Record corrections — round-50 attempt 2

Append-only. FILLED-AT-LANDING.
```

**Heading constraint — measured, not assumed.** The section heading must be exactly
`## Round 50, attempt 2 (2026-10-29)` (or a variant that starts with `## Round 50, attempt 2`), and the
corrections heading must **not** start with `## Record corrections — round 50`. Reason: `c2-record.py:322-338`
(`sections()`) selects a section by `startswith(head)`, so a second heading that starts with
`## Record corrections — round 50` becomes a second match for `CORR_HEAD` and `unique_section` fails.
Measured on a scratch clone at `03f852b9`:

| attempt-2 corrections heading | `c2-record.py` at the landing tip |
|---|---|
| `## Record corrections — round 50, attempt 2` | `mismatches 5`, exit 1 — B3, B4, B5, B10, B11 all red: `2 `## Record corrections — round 50` sections, want 1` |
| `## Record corrections — round 50 attempt 2` | `mismatches 5`, exit 1 — same failure (the `startswith` prefix still matches) |
| `## Record corrections — round-50 attempt 2` | `mismatches 0`, exit 0 — safe (the hyphen breaks the prefix) |
| `## Round 50, attempt 2 — corrections` | `mismatches 0`, exit 0 — safe |

So use **`## Record corrections — round-50 attempt 2`** (hyphenated `round-50`) or
`## Round 50, attempt 2 — corrections`. Both were run end-to-end on a scratch clone.

---

## BLOCK 3 — the `## Owned axes` coverage-row head replacement

**What changes and why.** The `## Owned axes` coverage row currently reads
`139/139 knowledge files mapped at the round-50 landing (…)`. Attempt 2 adds exactly one knowledge file —
`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`, the stem the **frozen** counter pins
(`tools/round-50/c1-counter.py:377-378`, `ENTRY`/`STEM`; the attempt-2 claims file was corrected to this
stem at commit `6f4aba63`) — so the count becomes 140 and the head must lead with `140/140`.

The frozen C2 atom **B1** re-derives the head from the repo, not from prose
(`tools/round-50/c2-record.py:504-506`): it takes the **first** `(\d+)/(\d+) knowledge files mapped` match
in the coverage row and requires it to equal the count of `corpus/knowledge/**.md` at REV. `140` must lead,
and every later historical clause must stay intact so the row keeps its history.

**Paste-ready replacement of the leading clause.** In `SCORECARD.md:23`, replace exactly this string
(330 characters, the row's first clause):

**OLD (replace):**

```
139/139 knowledge files mapped at the round-50 landing (the round-47 landing read 138/138; the round-49 entry made it 139; round 50 added no knowledge entry) (`git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'` → 138; command A `mapped 138`, `missing []`, `dangling []`, receipt `.ufo/waves/round-47/l1/scores/`)
```

**NEW (paste):**

```
140/140 knowledge files mapped at the round-50 attempt-2 landing (the round-47 landing read 138/138; the round-49 entry made it 139; the round-50 attempt-1 landing added no knowledge entry; the round-50 attempt-2 landing adds one — `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` — and maps it) (`git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'` → 140; command A `mapped 140`, `missing []`, `dangling []`, receipt `.ufo/waves/round-50/l1/scores/`)
```

Everything after that clause in cell 3 is **unchanged**: `; 133/133 knowledge files mapped after the
round-41 landing (…)`; `; 130/130 …`; `; 128/128 …`; `; 124/124 …`; `; 122/122 at cab59f221…`; `; 116/116 …`;
`; 109/109 …`; `index integrity only, **not** fraction of the REA domain held. History: 78/78 at 3395b6d …,
107/107 at 7ef837a4…, 108/108 after the round-25 EVM selector-naming entry`. Cells 1, 2, 4 and 5 of the row
are also unchanged.

**Measured verification of this exact edit** (scratch clone at the **real C3 landing** `addbfb4d`, entry +
README coverage-map row + this edit applied):

- `tools/round-50/c2-record.py --root . --rev HEAD --freeze 435d41fd…` → `mismatches 0`, `atoms_total 11`,
  **exit 0**; B1 `ok: true`, `why: []`.
- `re.findall(r'(\d+)/(\d+) knowledge files mapped', row)` on the edited row → first match `('140','140')`
  (then `('133','133')`, `('130','130')` — the historical clauses are preserved and only the first is
  load-bearing).
- `tools/round-47/record.py --root . --rev HEAD --no-battery` → `mismatches 0` (the coverage axes atom
  re-derives `(140,140)` from the repo and now matches the row).

**Two couplings the L1 must land in the same commit** (both measured; both turn a green counter red if split):

1. **The `## Owned axes` depth row head — LIVE RED NOW.** The C3 table v5 landed as a **26th** craft rule
   block in `SKILL.md` at `1439dfe9` (the v5 bullet is the 22nd `- **` bullet and is self-labelled "26.";
   the craft section now holds 26 bullets), so `depth_pair` moved from `(25,25)` to `(26,26)`. The depth
   row still says `25/25`, and `tools/round-47/record.py --root . --rev HEAD --no-battery` at the current
   tip returns **`mismatches 1`**:
   `depth 25/25 at the head of its Owned-axes row, claimed [25,25], derived [26,26]`.
   The depth row's leading clause must move to `26/26` in the same landing as the coverage head:

   **OLD (replace, `SCORECARD.md:24` leading clause):**

   ```
   25/25 queue-drain rule blocks have resolvable file/range citations at the round-48 landing (command A, new block 25 with the verdict-meaning table, `citation_resolved_rules 25`; receipt `.ufo/waves/round-48/l1/scores/`)
   ```

   **NEW (paste):**

   ```
   26/26 queue-drain rule blocks have resolvable file/range citations at the round-50 attempt-2 landing (command A, new block 26 with triage table v5, `citation_resolved_rules 26`; receipt `.ufo/waves/round-50/c3/c3-after.json`); 25/25 queue-drain rule blocks have resolvable file/range citations at the round-48 landing (command A, new block 25 with the verdict-meaning table, `citation_resolved_rules 25`; receipt `.ufo/waves/round-48/l1/scores/`)
   ```

   **Verified against the real landing** (scratch clone at `addbfb4d`, depth head patched):
   `tools/round-47/record.py` → `atoms 14`, **`mismatches 0`** (was 1 before the patch). With the coverage
   head patched as well, `tools/round-50/c2-record.py` → `mismatches 0`, `atoms_total 11`, **exit 0**.
   Note the patch is independent of where the v5 bullet sits in the craft section: I measured `depth_pair`
   as `(26,26)` with the v5 bullet inserted at index 22 **and** appended at the craft-section end — the
   denominator is the bullet count either way. The "26" in the text is the block's own label, which is what
   `SKILL.md` and the C3 registry row (`SKILL.md:1800`, "the SKILL rule block 26 triage table v5") say.

2. **The README coverage-map row.** B1 also requires every knowledge file at REV to be mapped by its
   backticked stem in `corpus/README.md` `## Coverage map` (`c2-record.py:510-514`), and the frozen C1
   counter has the same binding (`c1-counter.py:2481-2482`, `coverage_map_row`: a `|`-prefixed line inside
   the Coverage-map section containing the stem). The README row for
   `2026-10-28-r50-avm-le-squashfs-core` must land in the same commit as the SCORECARD head, or B1 goes red
   with `knowledge files not mapped in README Coverage map`.

**Do not** rewrite the historical `## Round 50` section or `## Record corrections — round 50` above; the
attempt-2 section is append-only below them.

---

## The C3 block number — resolved: use "rule block 26"

`plans/round-50-attempt2-claims.md` earlier in this wave said table v5 lands as rule **block 22**; the C3
freeze commit `1439dfe9` **corrected it to rule block 26**, and the landed surfaces agree:

- `plans/round-50-attempt2-claims.md:61` — "land **triage table v5** as `SKILL.md` rule block 26 (the next
  free craft-block number; blocks 22-25 are the freeze-integrity/meaning blocks; dated supersession of
  block 21's routing/action columns for the no-reader families; block 21 stays as history)";
- `SKILL.md:572` (the C3 status line) and `SKILL.md:1800` (the C3 registry row) — both "rule block 26".

**Use "rule block 26" / "new block 26" in the SCORECARD.** Writing "block 22" would name a different block
than the landed `SKILL.md` and the C3 registry row name, putting two landed surfaces in disagreement.

Two numbering schemes coexist, and the distinction matters if the L1 is asked why the number is 26 when the
bullet is the 22nd in the section:

- the **bullet index** — what `craft_blocks()` / `re.split(r"(?m)^- \*\*", craft)` counts and what
  `command A` reports as `rule_blocks`; the v5 bullet is bullet **22**, and blocks 22–25 by index are the
  freeze-integrity and meaning blocks;
- the bullet's **own label** in its text — the v5 bullet reads "**26.**".

`tools/round-45/c1-counter.py:163` asserts `rule_blocks != 22`, so it is already red at the tip
(`rule_blocks 25 != 22` before the C3 landing, `26 != 22` after) — it is a frozen older counter verified at
its own revision, not a round-50 gate, so this is a disclosed limit rather than a break.

---

## C3 before-state, independently re-measured (offline, no REA)

The C3 before-arm is the v4 interpreter over the 126 committed round-42 recon envelopes. I ran the frozen
v4 interpreter offline at the current `SKILL.md` (table v4) — **no REA run in this wave**:

```
python3 -I -B tools/round-42/sqfs-triage-v4.py --skill SKILL.md --json \
  .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/*/envelope.json
```

→ exit 0, stdout sha256 `1a02cbfbd1e2dcdf387311ac64f731808a36ca0494b3f0fa250ef78b4a864611`, 126 results.
Of the 126, the **19** no-reader `_ddefault` envelopes label `clean`/`none` and the other 19 no-reader
envelopes label `depth-limited`/`raise-depth` — 38 no-reader rows in all, exactly as the amended claims
state. The split by family is 4 `squashfs_v2_nonstandard` + 7 `squashfs_v3_broadcom` +
8 `squashfs_v3_nonstandard` `_ddefault` rows.

**Counting criterion — handler-level, not directory-level.** The 19 is the count of envelopes whose
**chunk handler** is in the frozen no-reader set
{`squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`}. Counting by *directory
name* instead gives 20, because `squashfs_v3_broadcom_squashfs_v3_be_ddefault` carries handler
`squashfs_v3` (reader-backed) while its directory is named under the broadcom family. The claims' own
frozen criterion is handler-level ("the no-reader set is handler-level and frozen", `d71829bf`), so **19**
is the right number and the C3 before-receipt's 19 is correct.

Also measured, same offline run: `--table-only` → exit 0, stdout sha256
`65abca784fbaafc0318df5d05eee97036081f8a1a6aff96d38b5c2cbc76c510f`, 15 rules, marker line 526.

---

## Anchor uniqueness (re-checked on the lane file at `addbfb4d`)

| anchor | occurrences | action |
|---|---|---|
| `139/139 knowledge files mapped at the round-50 landing` | 1 | safe `replace(..., 1)` |
| `25/25 queue-drain rule blocks have resolvable file/range citations at the round-48 landing` | 1 | safe `replace(..., 1)` |
| `## Record corrections — round 50` (as a heading) | 1 | do **not** add a second heading with this prefix |
| `## Owned axes` (as a heading) | 1 | the head edit stays inside it |
| `## Capabilities` (as a heading) | 1 | BLOCK 1's row goes inside it |
| capability table last row (`SCORECARD.md:632`, round-49) | 1 | BLOCK 1's row goes after it |
| `## Round 50, attempt 2 (2026-10-29)` (as a heading) | 0 | BLOCK 2's heading is new |

The coverage and depth OLD strings above are **byte-exact** copies of the lane file's current text (verified
by `str.count == 1` and a flattened substring match against this draft). The coverage OLD string is 330
characters; the depth OLD string is 219.
