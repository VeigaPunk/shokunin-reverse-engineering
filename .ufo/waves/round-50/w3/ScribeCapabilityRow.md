# ScribeCapabilityRow — SCORECARD bindings (round 50, attempt 2, wave 3)

**Verdict: the three SCORECARD bindings are drafted, paste-ready, and mechanically verified — but two of them
are not optional cosmetics. The `## Owned axes` depth row is LIVE RED at the current tip, and the
`## Record corrections` heading the attempt-2 section needs will break five frozen C2 atoms if written the
obvious way. Both are below with the exact text and the measured receipts.**

Paste-ready blocks: `.ufo/waves/round-50/w3/ScribeCapabilityRow/scorecard.md`
(blocks: 1 capabilities row · 2 `## Round 50, attempt 2` section skeleton · 3 `## Owned axes` head edits).

Lane tip when drafted: `addbfb4df0d33fedff51d46f2a983a5bd8ea0c10` (the tip advanced **five** times under
me during this wave — `6f4aba63`, `03f852b9`, `d71829bf`, `1439dfe9`, `addbfb4d`). The frozen C1 bytes are
byte-unchanged at the tip: `git diff --stat 435d41fd… HEAD -- tools/round-50/ plans/round-50-claims.md
tools/round-41/sqfs-list.py tools/round-27/xpin-attribute.mjs` → empty, exit 0.

No REA run was made by this seat (contract). No lane file was written by this seat. All measurement below is
offline: git objects, the frozen v4 triage interpreter, the frozen C2 counter, and the frozen round-47 record
counter, run against scratch clones.

---

## Findings

| # | Sev | Finding | Evidence (command → exit, stdout sha256) |
|---|---|---|---|
| F1 | **HIGH** | **The `## Owned axes` depth row is live red.** The C3 table v5 landed as a 26th craft rule block (`1439dfe9`), so `depth_pair` moved `(25,25)` → `(26,26)`, but the row still leads with `25/25`. `tools/round-47/record.py --root . --rev HEAD --no-battery` → **`mismatches 1`**: `depth 25/25 at the head of its Owned-axes row, claimed [25,25], derived [26,26]`. The depth head must move to `26/26` in the same landing as the coverage head. | `python3 -I -B tools/round-47/record.py --root . --rev HEAD --no-battery` → exit 0, stdout `{"atoms":14,"mismatches":1}`; after the depth-head patch on a scratch clone at `addbfb4d` → `{"atoms":14,"mismatches":0}` |
| F2 | **HIGH** | **The attempt-2 corrections heading breaks five frozen C2 atoms if written the obvious way.** `c2-record.py:322-338` selects a section by `startswith(head)`, so a heading starting `## Record corrections — round 50` becomes a **second** match for `CORR_HEAD` and `unique_section` fails. Measured on a scratch clone: `## Record corrections — round 50, attempt 2` → `mismatches 5`, exit 1, with B3/B4/B5/B10/B11 all red: *"2 `## Record corrections — round 50` sections, want 1"*. The same happens with `## Record corrections — round 50 attempt 2`. **Safe:** `## Record corrections — round-50 attempt 2` (hyphen breaks the prefix) and `## Round 50, attempt 2 — corrections`, both `mismatches 0`, exit 0. | `python3 -I -B tools/round-50/c2-record.py --root <clone> --rev HEAD --freeze 435d41fd… --work <scratch> --json-out <out>` → bad heading: exit 1, `{"mismatches":5,"atoms_total":11,"exit_code":1}`; safe heading: exit 0, `{"mismatches":0,"atoms_total":11,"exit_code":0}` |
| F3 | **MED** | **The C3 block number was a live trap, now resolved — but the SCORECARD must use "rule block 26".** Earlier in this wave `plans/round-50-attempt2-claims.md` said table v5 lands as rule **block 22**; the landed craft section has **26** bullets, of which the v5 bullet is the 22nd `- **` bullet but is **self-labelled "26."** (blocks 22–25 are the freeze-integrity/meaning blocks). The claims file was corrected to "rule block **26**" in the C3 freeze commit `1439dfe9`, and `SKILL.md:572` (status line) and `SKILL.md:1800` (registry row) both say "rule block 26". **The SCORECARD must therefore say "rule block 26" / "new block 26"** — writing "block 22" would name a different block than the landed `SKILL.md` and the C3 registry row do, putting two landed surfaces in disagreement. Note the two numbering schemes coexist deliberately: bullet index (what `command A` reports as `rule_blocks`; v5 = 22) vs the bullet's own label (26). The depth head text (F1) uses the label, matching `SKILL.md`. | `git show 1439dfe9 -- plans/round-50-attempt2-claims.md` → claims line 61 reads "rule block 26 (the next free craft-block number; blocks 22-25 are the freeze-integrity/meaning blocks…)"; `SKILL.md:572` and `SKILL.md:1800` both read "rule block 26"; `grep -c 'rule block 2[0-9]' SKILL.md` → 6 |
| F4 | **MED** | **The C3 before-state is 19 no-reader rows, not 4 — and the count is handler-level, not directory-level.** Counting by *directory name* gives 20, because `squashfs_v3_broadcom_squashfs_v3_be_ddefault` carries handler `squashfs_v3` (reader-backed) while its directory sits under the broadcom family. The frozen criterion is handler-level ("the no-reader set is handler-level and frozen", `d71829bf`), giving 19 = 4 v2ns + 7 v3_broadcom + 8 v3_nonstandard — which matches the landed `c3-before.json` (`pair_mismatch_count 19`, `verdict not met`). My earlier 4-row reading came from the pre-amendment claims text and is wrong for attempt 2. | `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill SKILL.md --json .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/*/envelope.json` → exit 0, stdout sha256 `1a02cbfbd1e2dcdf387311ac64f731808a36ca0494b3f0fa250ef78b4a864611`, 126 results; handler-level recount → 19 `_ddefault` `clean`/`none` + 19 `depth-limited`/`raise-depth` = 38 no-reader rows |
| F5 | **MED** | **The C1 coverage head must lead with `140/140`, and it is coupled to a README coverage-map row in the same commit.** The frozen C2 atom B1 takes the **first** `(\d+)/(\d+) knowledge files mapped` match in the coverage row and requires it to equal the count of `corpus/knowledge/**.md` at REV (`c2-record.py:504-506`); attempt 2 adds exactly one file (`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`, the stem the frozen counter pins at `c1-counter.py:377-378`). B1 also requires every knowledge file to be mapped by its backticked stem in `corpus/README.md` `## Coverage map` (`c2-record.py:510-514`), and the frozen C1 counter has the same binding (`c1-counter.py:2481-2482`). Split the commit and B1 goes red with *"knowledge files not mapped in README Coverage map"*. | `python3 -I -B tools/round-50/c2-record.py --root <clone> --rev HEAD --freeze 435d41fd…` with entry + README row + the head edit → exit 0, `{"mismatches":0,"atoms_total":11,"exit_code":0}`, B1 `ok: true, why: []`; `re.findall` on the edited row → first match `('140','140')` |
| F6 | **LOW** | **The capabilities row is gated, not free.** `AXES.md:62-64`: a capability row enters only through a round that demonstrates the capability running. The C1 data run has not happened, `corpus/evidence/round-50/c1/` does not exist yet (only `corpus/evidence/round-50/c2/` does), and the C1 control at the freeze is red (`carriers_matched 0`). **Land the capability row only after the C1 data run lands green** (`carriers_matched == 4`, exit 0); otherwise it is pre-claiming and the round records an honest stop. | `ls corpus/evidence/round-50/` → `c2` only; `.ufo/waves/round-50/controls-attempt2/c0/counter.json` → `{"carriers_matched":0,"met_target":false,"exit_code":1}` (60 failing clauses, `bindings_false` 6), sha256 `1615b563eb1f3db50f74dde6b0a01194641ccf5ad5d3c2b46ac967c6033f8469` |
| F7 | **LOW** | **`tools/round-45/c1-counter.py` is already red on `rule_blocks` and stays red.** It asserts `rule_blocks != 22` (`:163`); the count is 25 before the C3 landing and 26 after, so it reads `rule_blocks 25 != 22` / `26 != 22`. It is a frozen older counter verified at its own revision and **not** a round-50 gate, so this is a disclosed limit, not a break — but the L1 should not treat it as a regression caused by C3. | `python3 -I -B tools/round-45/c1-counter.py --root . --rev HEAD --freeze HEAD` → exit 0, `{"failing":["rule_blocks 25 != 22"],"rule_blocks":25}` |

---

## The three bindings (paste-ready; full text in `scorecard.md`)

**1. Capabilities row** — `| AVM LE SquashFS v4 carrier custody + REA extraction | … |` inserted after
`SCORECARD.md:632` (the round-49 row), inside the four-cell `## Capabilities` table. Evidence pointer:
`corpus/evidence/round-50/c1/` + the C1 counting command; first-working round **50**. Gated on F6.

**2. `## Round 50, attempt 2 (2026-10-29)` section** — mirrors `## Round 34, run-6 re-dispatch (2026-10-25)`
(`SCORECARD.md:3353-3372`): inherited-work paragraph, claims table (before / after / counting command /
verdict), freeze-and-receipts paragraph, owned-axis table, learning-trends paragraph, `planned`/`retired`.
C1's row is `FILLED-AT-LANDING` (the data run is the L1's); C3's row is filled from the landed receipts
(`verdict met`, `pair_mismatches 0`, `evaluator_missing 0`, `n_envelopes 126`; controls red at
`pair_mismatch_count` 19 / 126 / 26 / 51). The corrections heading must be
**`## Record corrections — round-50 attempt 2`** (F2).

**3. `## Owned axes` head edits** — two in-place refreshes, both `replace(..., 1)` on byte-exact unique
anchors, both landing in the **same commit** as the C1 entry and its README coverage-map row:

- coverage row (`:23`), leading clause only, later historical clauses byte-unchanged:
  `139/139 knowledge files mapped at the round-50 landing …` → `140/140 knowledge files mapped at the
  round-50 attempt-2 landing (… the round-50 attempt-2 landing adds one —
  \`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md\` — and maps it) …`
- depth row (`:24`), leading clause only: `25/25 … at the round-48 landing …` → `26/26 … at the round-50
  attempt-2 landing (command A, new block 26 with triage table v5, \`citation_resolved_rules 26\`; receipt
  \`.ufo/waves/round-50/c3/c3-after.json\`); 25/25 … at the round-48 landing …`

## Verification performed

| check | command | exit | result |
|---|---|---|---|
| frozen C1 bytes unchanged at the tip | `git diff --stat 435d41fd… HEAD -- tools/round-50/ plans/round-50-claims.md tools/round-41/sqfs-list.py tools/round-27/xpin-attribute.mjs` | 0 | empty |
| anchor uniqueness (both heads) | `sc.count(old)` on the lane file | — | 1 each; coverage OLD = 330 chars, depth OLD = 219 chars |
| draft strings byte-exact vs the lane file | flattened substring match of OLD and NEW against `scorecard.md` | — | all four present verbatim |
| coverage head edit → B1 green | `c2-record.py` on a clone at `addbfb4d` + entry + README row + edit | 0 | `mismatches 0`, `atoms_total 11`, B1 `ok: true` |
| depth head edit → round-47 green | `round-47/record.py --root . --rev HEAD --no-battery` on the same clone | 0 | `atoms 14`, `mismatches 0` (was 1) |
| both edits together | same clone | 0 | `c2-record.py` `mismatches 0`, exit 0 |
| corrections heading, 4 candidates | `c2-record.py` per candidate on clean clones | 0/1 | 2 safe (exit 0), 2 break 5 atoms (exit 1) |
| C3 before-state recount | frozen v4 interpreter over the 126 committed envelopes | 0 | 19 no-reader `_ddefault` `clean`/`none` (handler-level) |
| v4 table still parses | `sqfs-triage-v4.py --skill SKILL.md --table-only` | 0 | 15 rules, marker line 526, stdout sha256 `65abca784fbaafc0318df5d05eee97036081f8a1a6aff96d38b5c2cbc76c510f` |
| command A at the attempt-2 base | the recipe-A python at `f890bbea` | 0 | `mapped 139`, `missing []`, `dangling []`, `rule_blocks 25`, `citation_resolved_rules 25`, stdout sha256 `7ee3abeb4c045ca0394be2b987d61d02fc56517e59d03b670e29c90761b736e0` |
| C2 at the tip | `c2-record.py --root . --rev HEAD --freeze 435d41fd…` | 0 | `mismatches 0`, `atoms_total 11` (B1–B11 all `ok: true`) |
| depth_pair with v5 inserted vs appended | `round-47/record.py.depth_pair` on both variants | — | `(26,26)` either way — the denominator is the bullet count, so the head text is position-independent |

**Not run (and not claimed):** the C1 data run, the C1 controls beyond the already-scored CTL-C1-0, any REA
invocation, `tools/round-50/c1-counter.py` in scoring mode, and the C3 instrument's own scoring run (its
receipts are the landed `c3-{before,after}.json`, which I read rather than re-ran). `tools/round-27/c2-xpin-check.py`
was invoked once and refused on a package-identity check of a *different* npx cache
(`/home/vgpnk/.npm/_npx/a1722018f28f9df2/…`), not on the lane's bytes — it is not a round-50 gate and no
verdict is claimed from it.

## Tooling

No tool was installed, upgraded or removed. No pacman transaction. Nothing written under `~/.local/bin` or
any other PATH directory. The only writes by this seat are the two named paths: this report and
`.ufo/waves/round-50/w3/ScribeCapabilityRow/scorecard.md`.

## Scratch

`S=/fast/scratch/hyaku/kaidoku-r50/w3-ScribeCapabilityRow` (`TMPDIR` pointed there throughout). It holds the
offline receipts (`triage-v4-126b.json`, `triage-v4-table-only.txt`, `cmdA-at-f890bbe.json`, the
`c2-*.json` counter receipts) and the scratch clones used for the fixture tests. **Removed before yield**,
after the receipt values above were copied into this report; the two named lane paths keep the drafts.
Nothing under `/tmp` was written or is cited.

## Note for the L1

`plans/round-50-attempt2-claims.md` landing-order step 3 says the Owned-axes coverage head is updated
`140/140` "in the same commit as the entry". That is right and necessary (F5), but it is **not sufficient**
on its own: the depth head (F1) and the README coverage-map row must ride in that same commit too, and the
attempt-2 corrections heading (F2) must not use the `## Record corrections — round 50` prefix. All three are
in `scorecard.md` as paste-ready text.
