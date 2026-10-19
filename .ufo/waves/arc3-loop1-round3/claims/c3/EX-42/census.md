# EX-42 — the arc3-citation census (acceptance test)

Seat EX-42, chain c3, wave `arc3-loop1-round3`, 2026-10-19.
Measured revision: `HEAD` = `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (the arc3 r2
records commit); the landed table + `expected.json` under measurement are the
EX-41 worktree revision (uncommitted at capture; identities in §6).
Scratch: `/var/tmp/ex42-census/` (`/tmp` never used). Read-only over every
graded file; the real table was never written by this seat.

This artifact is the C3 claim's **acceptance test**: a mechanical list of every
arc3-introduced in-repo citation with its pinnability verdict and its
disposition (entry id, or NO-ENTRY with cause). Entry count is *not* the test;
this census is.

---

## 0. Verdict summary

1. **Baseline (before, at `c07af80`)**: table 31 entries / 4 quoted / 3 exempt,
   sha256 `738b3a56…`; probe `findings=0` in both modes; selftest 13/13; the
   only arc3 citation the pre-round table graded was `SHONEN.md:6` (the
   pre-existing `shonen-skill-range`). Everything else the arc3 rounds wrote
   was uncovered — the named debt this round closes.
2. **Census ledger** (mechanical; 88 raw rows over 57 distinct path tokens —
   `enumeration.tsv`): **45 pinnable rows, each with a proposed entry**
   (18 required / 20 recommended / 7 discretionary; `entries-proposal.json`),
   **1 row covered by a pre-existing entry**, **12 NO-ENTRY rows** in five named
   cause classes (§4.4). No pinnable live pointer is left without a disposition.
3. **Acceptance result against the landed table** (EX-41 revision
   `bfc42f1b…`, 57 entries / 4 quoted / 8 exempt): required rows **18/18
   covered**; the 26 evidence-provenance rows **adjudicated by class exemption**
   (an explicit scope narrowing, stated in the table's `exempt` ledger — but one
   clause of its recorded cause is *falsified by the table's own rows*, §5.3);
   **one gap**: the `LOG.md:1442` record (`SHONEN:6 → 81-255`) is neither
   covered nor inside the exemption's own wording (§5.4).
4. **Independent reproduction of the landed gate**: probe `findings=0` default
   and strict; selftest 13/13; frozen-run record re-derives (verdict `failed`,
   32 findings, `citation_dead` present, exit 1); a one-byte table mutation
   reads `pointer_table_tampered` exit 2 (`landed-table-acceptance.txt`).
5. **Non-vacuity**: nine controls across two scratch fixtures fire every
   declared class for both my proposal's entries and the landed table's new
   entries (`battery-EX42.txt`, `battery-landed.txt`).

---

## 1. Scope declaration (mechanical, not widened)

**A census row exists iff** a citation token sits on a line that one of the four
arc3 r1/r2 landing commits (`fbbbd45` r1 work, `14b1682` r1 records, `28aa7a9`
r2 work, `c07af80` r2 records) **added or modified** in one of the lane's
durable documents:

`SCORECARD.md`, `corpus/README.md`, `SHONEN.md`, `SKILL.md`, `LOG.md`,
`PROVINCE.md`, `corpus/knowledge/*` (this round: the arc3-r1 entry).

**Boundary (declared, r10-style durable-surface scope).** The arc3 wave and
round-report trees are *record-class citing texts*: they state where things sat
at their round's revision and are append-only by rule. They are graded only as
**targets** (precedent: `readme22-r8envelope`, `readme175-r8e2`). Their surface
is not small — at `HEAD` the four texts carry **8,187 stated-line citation
occurrences across 1,075 files** — which is why the boundary is declared rather
than silently dropped. `.ufo/gates/*` instrument *comments* are likewise
record-class. EX-41's census drew the same boundary with two extra durable
surfaces (see §4.5).

**Citation token kinds** (the enumeration net, `enumerator.py`): `A` stated
`path:NN[-NN]`; `B` file-level path (backticked or bare, extensions +
knowledge slugs); `C` `config.toml:N`; `D` section-key form
(`` `SCORECARD.md`'s `arc3-loop1-round1` section ``); `E` named receipt stamps
and `receipts/<path>`.

**Pinnability under rule #11** means: the target is an in-repo committed object,
and the citation form is not a bare line number into an operator-mutable file
(SKILL.md queue-drain rule #11; the table's own `_doc`). **Measured: arc3 r1/r2
introduced zero `config.toml:N` line citations** (kind `C` = 0 rows) — the
records were deliberately written pin-free (`SCORECARD.md:1393`). The single
operator-mutable surface mentioned (the Kimi config drift) is named without a
number and stays in the NO-ENTRY ledger by the table's own standing class.

---

## 2. Method and reproduction

1. Enumerate added/modified lines per commit per scoped file, then extract
   citation tokens: `python3 enumerator.py` → `enumeration.tsv` (88 rows).
2. Resolve every stated line/range against `HEAD` git objects and locate every
   file-level target: `python3 resolver.py` → `resolve.txt`.
3. Verify every entry's needle against the target's committed bytes with the
   real probe against the real tree:
   `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD
   --table /var/tmp/ex42-census/proposed-table.json
   --expected /var/tmp/ex42-census/proposed-expected.json --strict`
   → `clean findings=0 exit=0` (both modes; `battery-EX42.txt` control 0 runs
   the same on a fixture).
4. Non-vacuity: mutate a scratch copy of each cited surface and confirm the
   declared class fires (`battery-EX42.txt` for the proposal, `battery-landed.txt`
   for the landed table).
5. Cross-walk the landed table against the census ledger and re-run the landed
   gate (`landed-table-acceptance.txt`).

---

## 3. Baseline at HEAD (before)

| measure | value | evidence |
|---|---|---|
| table entries / quoted / exempt | 31 / 4 / 3 | `python3 -c` on `HEAD` bytes |
| table sha256 | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` | `sha256sum` = `expected.json` pin |
| probe at `HEAD`, default/strict | `reported findings=0 exit=0` / `clean findings=0 exit=0` | `--root . --rev HEAD` |
| selftest | `CLEAN cases=13 passed=13 failed=0 exit=0` | `--selftest` |
| arc3-r1 entry identity (re-derived) | 10,225 B, sha256 `dd986f562a6c7b2e759ebb90c9855adff38e9226b1d9e27af36b6e3a2aefc3d4` | `sha256sum`, `wc -c` |
| arc3 citations covered by the pre-round table | 1 (`SHONEN.md:6` via `shonen-skill-range`) | cross-walk |

---

## 4. The census ledger

### 4.1 Stated line/range citations (kind A + D) — 12 rows, all resolve at HEAD

Every row was resolved against `HEAD` objects; "holds" = the content the citing
sentence claims, read from the target range (`resolve.txt` lines 1–231).

| # | citing (HEAD line) | token | target state at HEAD | disposition |
|---|---|---|---|---|
| 1 | `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:17` | `…r3-evm-interface.md:149-155` | 155-line file; 149-155 = the round-4 erratum ("JUMPDEST dispatch-target position") | ENTRY `kbarc3-r3evm-offsets` → landed `arc3r1-entry-r3-offsets` |
| 2 | `…arc3-r1-evm-real-solc.md:18` | `…r3-evm-interface.md:59-70` | 59-70 = stub legs, `inferred_state_mutability: "pure"` for all three | ENTRY → `arc3r1-entry-r3-stub-mutability` |
| 3 | `…arc3-r1-evm-real-solc.md:21` | `corpus/QUALITY.md:24-25` | 24-25 = evidence-id full-domain rule | ENTRY → `arc3r1-entry-quality-ids` |
| 4 | `…arc3-r1-evm-real-solc.md:24` | `corpus/QUALITY.md:21` | 21 = parsed-and-empty vs excluded-from-inventory | ENTRY → `arc3r1-entry-quality-11` |
| 5 | `…arc3-r1-evm-real-solc.md:25` | `…r3-evm-interface.md:44-45` | 44-45 = the refuted candidate-2 note ("needs richer bytecode") | ENTRY → `arc3r1-entry-r3-hypothesis` |
| 6 | `…arc3-r1-evm-real-solc.md:26` | `…r3-evm-interface.md:93-96` | 93-96 = positional-encoding CLI quirk | ENTRY → `arc3r1-entry-r3-cli-quirk` |
| 7 | `SKILL.md:246` | `.ufo/waves/arc3-loop1-round1/seats/CR-2.md:86-89` | 247-line report; 86-89 = F2, stale `8,316 B` | ENTRY → `skill-rule14-cr2-identity` |
| 8 | `SKILL.md:248` | `…/claims/c1/verdict.md:149-153` | 207-line report; 149-153 = D9, three applied identities | ENTRY → `skill-rule14-verdict-identities` |
| 9 | `SKILL.md:252` | `…arc3-r1-evm-real-solc.md:7` | line 7 = the `recheck:` line; disk-backed `TMPDIR` / EDQUOT | ENTRY → `skill-rule14-entry-recheck` |
| 10 | `SKILL.md:254` | `LOG.md:1411-1412` | 1411-1412 = "10,225 B, sha256 `dd986f56…`" | ENTRY → `skill-rule14-log-fresh-identity` |
| 11 | `SKILL.md:253` | `SCORECARD.md`'s `arc3-loop1-round1` section (kind D) | heading at `:1338`; no line pinned (rule-#11 form) | ENTRY `skill14-scores-section` → `sc-arc3r1-section-key` (+ r2 key) |
| 12 | `SCORECARD.md:1435` | `SHONEN.md:6` | 12-line file; line 6 = the refreshed assertion `SKILL.md:81-255`, 14/14 | ENTRY `sc1435-shonen-record` → landed in the stronger `extracted` form `sc-arc3r2-cites-shonen` |

Covered by a pre-existing entry: **`SHONEN.md:6 → SKILL.md:81-255`** —
`shonen-skill-range` reads the range out of the line, so the arc3-r2 same-commit
refresh is already its subject; verified passing at `HEAD` (rule #13's
natural-control text sits at `SKILL.md:233`, inside the range). This is a
**repoint** row: the citation is not new, its numbers were rewritten by arc3 r2.

### 4.2 Durable file-level rows (registry rows, map row, records)

| # | citation | disposition |
|---|---|---|
| 13 | `corpus/README.md` EVM row token `2026-10-19-arc3-r1-evm-real-solc` (`:38`) | ENTRY `readme38-evm-arc3token` (anchor, line deliberately unpinned) → `readme38-arc3r1-token` |
| 14 | same row, token `2026-10-13-r3-evm-interface` | ENTRY `readme38-r3-target` (target anchor on the r3 entry) → lands transitively (the r3 entry is a target of four landed entries; deletion reads `citation_file_absent`) |
| 15 | the r1 entry as a target of the row | ENTRY `readme38-evm-target` → lands transitively (target of `skill-rule14-entry-recheck`) |
| 16 | `SKILL.md` citation-drift registry row (guard semantics; modified by arc3 r1) | ENTRY `skl389-probe-guard-row` (anchor `frozen-run preflight`) → `skill-registry-citation-drift-row` (needle identical) |
| 17 | `SKILL.md` custody-pair registry row (new, arc3 r2) | ENTRY `skl390-custody-row` → `skill-registry-custody-pair-row` |
| 18 | `LOG.md:1411` landing-identity record | ENTRY (quoted) `log1411-arc3-identity` → lands transitively (`skill-rule14-log-fresh-identity` grades lines 1411-1412 as a target; the quoted strengthening was adjudicated away with the LOG exemption) |
| 19 | `LOG.md:1442` record `SHONEN:6 → 81-255` | ENTRY (quoted, recommended) `log1442-shonen-repoint` → **GAP** (§5.4) |
| 20 | `corpus/README.md` token set is consulted by `readme38-*` only; no other durable row gained citations | — |

### 4.3 Evidence-provenance rows (kind B, from the r1 entry's `source:`/`recheck:` rosters) — 26 targets

One row per distinct in-repo target (target-granularity policy; the same 25
targets appear on two physical lines, `:5` and `:33`). Each target exists at
HEAD; each proposed needle was verified against the committed bytes.

| tier | rows | disposition |
|---|---|---|
| recommended (19) | install-receipt, planted-K, expected-selectors, attack expected-many, `Rv2Token.runtime.hex`, probe 6.4.0 hex/raw, probe 6.7.0 hex, rerun-a, probe-many, creation probe, smoke probe, Kdx hex leg, recon verdict, sha3 vectors, m1 rv2 digest, ABI, transcript, m1 kdx digest | ENTRY proposed (`entries-proposal.json`); **landed disposition: adjudicated NO-ENTRY by class** (§5.3) |
| discretionary (7) | rerun-b, cwd-root, Kdx raw twin, m2 keccak detail, `solc-input.json`, `compile.js`, `Rv2Token.creation.hex` | same; mirrors of a pinned primary |

The absolute-path form `…/RV-2/Rv2Token.runtime.hex` inside the `recheck:`
command is the same target as the `kbarc3-ev-rv2-hex` row (in-repo, tracked —
`git cat-file -e` verified; an earlier checker run that read it as ABSENT was
this seat's own path-form bug, corrected and re-measured).

### 4.4 NO-ENTRY ledger — 12 rows, five cause classes, none convenient

| # | row | cause class |
|---|---|---|
| 1-2 | `bytecode.sha256`, `subject.digest.sha256` (r1 entry `:7`, `:17`) | **field/key name**, not a pointer (the probe grades pointers) |
| 3 | `.ufo/waves/arc2-loop1-round10/C3.md` (SCORECARD `:1415`, `:1494`) | **dirty-worktree-state record**: the referent is an uncommitted worktree state, not committed content |
| 4 | `config.toml` bare mention (SCORECARD `:1495`) | **operator-mutable class**, no line number: the class the probe reports is a live `config.toml:N`; the standing `exempt` row already covers it |
| 5 | `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/` (r1 entry `:11`) | **gitignored install prefix** (`node_modules/` wave-.gitignore): no committed git object to grade; provenance is the receipted install-receipt anchor |
| 6-7 | `corpus/lessons/2026-10-15-round-1-recovery.md`, `LOG.md` (SKILL.md `:384`) | **line reworded, no arc3-introduced citation**: the sentence was edited by arc3 r2; its citations pre-date the arc |
| 8-10 | `.ufo/waves/arc3-loop1-round1/claims-frozen.md` (LOG `:1400`); `SKILL.md` + `SHONEN.md` (LOG `:1443`); bare `SCORECARD.md` (SHONEN `:6`) | **record-class path mentions, no stated number** (LOG/report prose; append-only history by rule) |
| 11 | `.sha256` (SKILL.md `:390`) | **suffix token in prose**, not a path |
| 12 | `bytecode.sha256` on the `recheck:` line `:7` | duplicate of rows 1-2 (same key-name class) |

### 4.5 Scope deltas vs EX-41's census (both declared, neither silent)

- EX-41's census is **wider** on two surfaces this census excluded: `.ufo/gates/c1-census-v10.py` header citations (3 rows → landed entries) and the custody-pair README/instrument surfaces (7 rows + 3 example anchors). Those are real arc3-r2 artifacts; the landed table grades them.
- This census is **wider** on the durable entry → evidence roster (26 rows), which EX-41 adjudicated by class (§5.3).
- No scope *widening* occurred in the sense the wave freeze forbids: the c1-census instrument's scope rows were not touched (`git status` at census time: only the two gate files + the two custody files are modified).

---

## 5. Acceptance result against the landed table (EX-41 rev `bfc42f1b…`)

### 5.1 Required rows: 18/18 covered

15 land 1:1 on new entries; 2 (`readme38-evm-target`, `readme38-r3-target`) land
transitively (the targets are graded by other landed entries, so deletion reads
`citation_file_absent`); 1 (`log1411-arc3-identity`) lands transitively plus the
LOG exemption; `SHONEN.md:6` stays on the pre-existing `shonen-skill-range`.
Two landed entries are *stronger* than my proposal: `sc-arc3r2-cites-shonen`
is an `extracted` pin reading the range out of `SCORECARD.md:1435` and grading
`SHONEN.md:6`, where I proposed an `exact` word pin; and `sc-arc3r2-section-key`
covers the r2 section key I had not separately proposed.

### 5.2 Adjudicated with cause (the claim's second arm): the 26 provenance rows

EX-41's census row 20 + the `exempt` ledger entries ("wave-internal citations
…", "LOG.md / report prose naming in-repo paths without a stated number")
make the class-exemption explicit and recorded. This is a **scope narrowing**,
not an omission: the exemption states the operative rule ("wave targets are
graded where a durable surface cites them") and the round did land the two
durable-surface wave-target pins (`skill-rule14-cr2-identity`,
`skill-rule14-verdict-identities`). The claim's "or adjudicated" arm is
satisfied.

### 5.3 One recorded cause is falsified by the table's own rows (**finding**)

The adjudication's first clause — "no stated number means no drift class for
this probe to grade" — is **not true of this table**: the anchor kind exists
for exactly that class, and the landed table itself carries no-number anchors —
`readme22-r8envelope`, `readme22-r4file`, `shonen-lesson-file`,
`shonen-evidence-bundle` (pre-existing) and `custody-readme-v1-stanza-example`,
`-sums-example`, `-pipe-example` (landed this round, grading wave receipt
files). The exemption's *operative* ground is the scope judgment (wave-internal
evidence provenance is not a lane citation), which is coherent and is what the
ledger's second sentence says; the "no drift class" wording is inaccurate and
should be corrected when the ledger is next touched (patch text not required —
one clause of one `cause` string). Until then the exemption is *under-stated*,
not wrong in effect: the census accepts the adjudication on its scope ground.

### 5.4 The gap

`LOG.md:1442` states `SHONEN:6 → 81-255, 14/14 same commit` — a stated-line
citation written by arc3 r2 in a durable document. It is not covered by any
entry (the LOG entry id `sc-arc3r2-cites-shonen` pins the SCORECARD record, not
the LOG record), and the exemption classes do not reach it by their own wording
(the LOG class covers line numbers *inside* LOG and path mentions *without*
numbers; this is a stated number about another file). Proposed fix (one entry,
already non-vacuity-tested against my proposal): quoted,
`LOG.md:1442`, `must_match` "SHONEN:6 → \\`81-255\\`". Minor, recorded for the
parent rather than argued as blocking: the live pointer (`SHONEN.md:6`) is
graded; it is the *record* side that is ungraded.

---

## 6. Measurements (before → after) and independent reproduction

| measure | before (`c07af80`) | landed (EX-41 worktree, measured by this seat) |
|---|---|---|
| table entries | 31 | **57** (counted mechanically) |
| quoted / exempt | 4 / 3 | 4 / **8** |
| table sha256 | `738b3a56…` | `bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7` (30,348 B) |
| `expected.json` pin | `738b3a56…` | `d97dd60a942eaf53771c8224e84a9e8cdaf976dc66c3a543a450b1f1fa3827e2` (2,154 B) — pin matches the landed table (coupled, same revision) |
| probe at HEAD | 0 findings, both modes | **0 findings, both modes** (independently re-run) |
| selftest | 13/13 | **13/13** (independently re-run) |
| frozen run at `679af5d` | membership re-derives | **`failed findings=32 exit=1`, 17 × `citation_dead` ⊇ the record's `["citation_dead"]`** |
| tamper guard | declared exit 2 | **one-byte mutation → `pointer_table_tampered`, exit 2** (scratch copy) |
| my census's coverage | — | **45/45 pinnable rows carry an entry id or a proposed entry; 18/18 required covered** |

Artifact identities (rule #14; re-derived after the final revision of each —
values recorded in the seat report, not inside the files they describe):

- `entries-proposal.json` — sha256 `8a9583ce4664874d6e4caec9f0e301c674fbc37a8a53a1d0635c136a714e41c8`, 17,219 B → renamed copy verified byte-identical at placement.
- `enumeration.tsv`, `resolve.txt`, `battery-EX42.txt`, `battery-landed.txt`, `landed-table-acceptance.txt`, `enumerator.py`, `resolver.py` — identities in `.ufo/waves/arc3-loop1-round3/seats/EX-42.md`.

---

## 7. Attacks / refutations attempted, with verdicts

1. **Net-too-narrow (missed citations).** Cross-check sweep: every path-like
   token on every arc3-added scoped line re-extracted with a second, broader
   regex, plus a distinct-token diff against the first net. **Verdict: no
   misses** (57 distinct tokens; the sweep's list ⊆ the census's). Residual
   risk named: tokens that are not path-shaped (symbol names, count tokens) are
   out of the probe's contract.
2. **Stale ranges (a cited range moved).** All 12 stated-line rows resolved at
   HEAD, target line counts checked, and the claimed content read out of each
   range. **Verdict: none stale**; every range holds what its sentence claims.
3. **Vacuous entries (proposed needles always green).** Nine controls in two
   scratch git fixtures: cited-text mutation, range truncation, target deletion,
   needle neutering, section-heading rewrite, record rewording, LOG word
   rewrite, registry-row text removal, quality-needle mutation. **Verdict: all
   fire their declared classes** (`citation_dead`, `citation_out_of_range`,
   `citation_file_absent`, `record_word_missing`), fixture clean after revert.
   Two of my own first-pass needles were caught bad by the positive control
   (missing backticks in the r3 stub quote; a digest absent from the keccak
   recon file) and fixed — recorded because a census that cannot fail its own
   checks is not a test.
4. **The landed table is vacuous.** Same battery against the landed table on a
   fixture carrying exactly its cited surface (26 files): baseline clean, five
   mutations each redden their declared entry. **Verdict: non-vacuous.**
   Caveat measured (L3a): anchor `must_match` is a substring search, so
   *extending* a cited token (`…-solc` → `…-solc-XX`) does **not** redden an
   anchor; only deleting the token does (L3b fires). Renames of the tail of a
   token are therefore invisible to anchors — a probe-semantics caveat worth
   recording, not a defect of this round's entries.
5. **Escape-hatch NO-ENTRY (uncomfortable rows parked with a cause).** Each of
   the 12 NO-ENTRY rows is assigned to one of five named classes; none is
   "pinning is inconvenient". The largest adjudicated group (26 provenance
   rows) is EX-41's, is explicit, and is reported in §5.2–§5.3 with its one
   inaccurate clause named. **Verdict: no convenience adjudication survives.**
6. **The r2 SHONEN re-point silently broke `shonen-skill-range`.** Re-ran the
   landed table at HEAD (0 findings) and checked the entry's own needle lands
   inside the new range (rule #13 text at `SKILL.md:233` ∈ 81-255).
   **Verdict: no break.**
7. **The frozen-run record cannot detect a grown table** (CR2's r10 caveat).
   Re-derived at `679af5d`: the record's *membership* requirement is met
   (`citation_dead` present; 32 findings). **Verdict: record re-derives; the
   membership-vs-measurement caveat is unchanged and carried.**

---

## 8. Limitations

- My census grades the durable-surface scope only; wave/report-internal
  citations (8,187 stated-line occurrences) are record-class by declaration and
  are not enumerated (they are graded only as targets).
- The acceptance result is against the **worktree** revision of the two gate
  files (uncommitted at capture). The parent's landing re-derivation is the
  binding one; if the table changes after this census, the cross-walk in §5
  must be re-run (the census's own rows do not depend on the landed table).
- `entries-proposal.json` is a proposal, not the target: EX-41 owns
  `.ufo/gates/citation-drift/pointer-table.json` and `expected.json`.
- The three LOG/report record-class rows and the `config-filename` mention rest
  on the table's standing exemption wording; no re-argument of that class is
  offered here.

## 9. Evidence pointers (all under `.ufo/waves/arc3-loop1-round3/claims/c3/EX-42/`)

`enumeration.tsv` (88 raw rows) · `resolve.txt` (A-row resolutions, B-row target
locations) · `entries-proposal.json` (45 rows, ready-to-merge shape) ·
`battery-EX42.txt` · `battery-landed.txt` · `landed-table-acceptance.txt` ·
`enumerator.py` · `resolver.py`.