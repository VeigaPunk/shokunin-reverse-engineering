# ScoutQualRows — QUALITY coverage map for round-51 routed defects

Seat: ScoutQualRows (scout). Wave r52-w1. Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Lane tip at read time: `c525de54a53eb3c4fee28ede2721da4527cf8ece` (round base; `git status --porcelain` shows
only untracked `.ufo/waves/round-52/` — no tracked-file modification by this seat).

**Read-only.** No lane file outside `.ufo/waves/round-52/w1/ScoutQualRows/` was written; no git mutation;
no REA run; no download.

## 0. Measured QUALITY row inventory (the numbers the round needs)

Commands (cwd = lane root), exit 0; full transcript in `qual-inventory.txt`
(sha256 `991082a18d0548e03dad7c9e496cc8e0d2880329ebf1312dfef87bec6424d154`; UTC 2026-10-30T10:49:51Z):

| check | command | result |
|---|---|---|
| C1 admission-table row numbers | `awk '/^## Admission criteria/,/^## Signals of weak material/' corpus/QUALITY.md \| grep -oE '^\| [0-9]+ \|'` | `1..74, 77..93` — **75 and 76 exist only as appended bullets**, never as table rows |
| C2 last row number (table+bullets) | `grep -oE '^\| [0-9]+ \||^- \*\*Row [0-9]+' corpus/QUALITY.md \| grep -oE '[0-9]+' \| sort -n \| tail -1` | **98** |
| C3 distinct numbers / total numbered entries | same grep \| `sort -n -u \| wc -l`; \| `wc -l` | **98 distinct numbers, 107 numbered entries** (9 duplicate-number entries) |
| C4 duplicate row numbers | same grep \| `sort -n \| uniq -d` | `1 2 3 4 5 6` (the *Signals* table re-uses 1–6 — a different table, not a criterion collision) **and `77 78 79`** |
| C5 numbers with no admission-table row | `for i in $(seq 1 98); do grep -qE "^\| $i \|" … \|\| echo -n "$i "; done` | `75 76 94 95 96 97 98` — bullet-only rows |
| C6 keyword coverage of the six routed classes | `grep -c -iE '<pattern>' corpus/QUALITY.md` | see §2 table |
| C7 file shape | `wc -l`; `grep -cE '^\| [0-9]+ \|'`; `grep -cE '^- \*\*Row [0-9]+'` | 156 lines; 97 table rows (91 admission + 6 Signals); 10 bullet rows |

### Where new rows would start

**Next free row number: 99.** But the round must resolve a numbering hazard first:

**Rows 77, 78 and 79 each exist twice with different text.**
- `corpus/QUALITY.md:85` — table row 77 "A counter over self-assessment surfaces enumerates **every** occurrence…"
  (from `corpus/lessons/round-36.md` M36-3, landed `01a44dbf` 2026-10-26).
- `corpus/QUALITY.md:145` — bullet "**Row 77 added after the round (a craft block must cite knowledge, and an instrument
  must be executed before it is frozen).**" (from `corpus/lessons/round-46.md` M46-4, landed `49e6cac4` 2026-10-28).
- Same collision for 78 (`:86` round-36 M36-4 vs `:147` round-47 M47-6) and 79 (`:87` round-38 M38-1 vs `:149` round-48).
- Consequence, observed: `corpus/lessons/round-51.md:74` (M51-8) cites "**QUALITY 77** and command A" — that citation
  is ambiguous between the two row-77 texts, and the intended target is the round-46 bullet (citation-range drift).
  A reader resolving "row 77" to the table row gets a different criterion.
- `corpus/lessons/round-36.md:57` ("Criteria added (QUALITY 77–78)") and `round-38.md:147` ("QUALITY 79, 80, 81") also
  cite the table rows; `round-46-verifier-spotcheck.md:134` and `round-47-verifier-spotcheck.md:92` cite the bullets.
  Both families of citation are live in the corpus.

**Recommendation to the L1 (not applied by this seat):** start the round's new rows at **99** (not 75/76/77/78/79, and
not at 94–98, which are taken), and either (a) disambiguate 77/78/79 in the same commit — e.g. by renaming the
round-36/38 table rows to a distinct band and adding a one-line collision note — or (b) leave them and require new
rows to cite the section ("table row N" / "bullet row N") rather than the bare number. A bare `QUALITY 77` citation is
already ambiguous today, so any round-52 lesson row that cites a row number must not use 77/78/79 bare.

**Row-count caveat for the round:** "the current QUALITY row count" is ambiguous between **98 distinct numbers**,
**107 numbered entries** and **91 admission-table rows**. QUALITY.md's own discipline (CORPUS.md `### Rules` 2,
append-only; row 74 on tallies) and the r48 lesson M49-1 (one freeze named once) both argue for naming the *count* as
"98 distinct criterion numbers (91 in the admission table, 7 appended as bullets, 3 numbers doubly used)" rather than
a bare integer.

## 1. Method

Read in full: `corpus/QUALITY.md` (156 lines, all numbered rows), `corpus/lessons/round-51.md` `## Mistakes`
(M51-1…M51-8) and its `## Gate`, `corpus/lessons/round-51-verifier-spotcheck.md` §6 (routed defects 1–7) and §7
(admission). Cross-read: `corpus/lessons/round-50.md` (M50-5, M50-9, M50-10), `corpus/SOURCES.md` (158 rows),
fleet `CORPUS.md` `### Rules`, `scripts/sources-census.sh` (W04/E04 logic at `:645`/`:647`), and the round-52 wave
artifacts `.ufo/waves/round-52/{w1-spec.json,w1-dispatch.json}` and
`.ufo/waves/round-52/w1/ExecWaveCheck/{check-dispatch.py,receipt.json}`.

Each routed defect below is judged against **two** questions:
1. **Is the class already criterion'd?** → cite the QUALITY row number (or say none).
2. **If uncriterion'd**, the corpus discipline is: *the lesson row must cite the fix's observed failure before any new
   criterion*. `corpus/lessons/round-52.md` does not exist yet (round-52 lesson is a draft owned by seat `ScribeLesson`
   under `.ufo/waves/round-52/w1/ScribeLesson/lesson.md`); its seeded rows per `gen-w1.py:391-397` cover M51-6,
   per-seat results fields and the round-band shortfall. **Rows for misroot prevention, census W04 hygiene and the
   carried L0 credential class are NOT seeded** — see §3.

## 2. Per-defect map

| # | round-51 routed defect (source) | class | QUALITY row that already covers it | verdict |
|---|---|---|---|---|
| D1 | **Round shape below band** — 36 identities, floor 64 not met, no falsify wave (`round-51-verifier-spotcheck.md` §6.1; `round-51.md` "Claims and stop"; `wave-accounting.json` `floor64_met:false`, `second_wave:"not launched"`) | seat accounting / band shape | **#76** ("seat accounting": "A round's record states seat totals, settled seats and outstanding seats with timestamps in the same commit as any stop, and a stop waits for the seats that will attack it. A manifest may not claim a round shape it has not settled… A generated per-seat prompt is asserted to begin with the directive bytes before dispatch (M34-16, D4)") and **#98** ("a stopped draft is not a delivered gate … state the unmet seat floor") | **criterion'd** (76, 98). #76 already forbids claiming a shape the round has not settled; #98 requires stating the unmet seat floor. Round-52's fix (64-seat v2 wave + falsify wave) satisfies #76 by *settling* the shape, and the honest-stop wording of #98 is the fallback if it cannot. No new criterion needed. |
| D2 | **Per-seat results fields** — `r51-w1-results.json` has no per-seat id/status, so the dead-seat count is unverifiable (`round-51-verifier-spotcheck.md` §6.2; `wave-accounting.json` `result_rows_have_ids:false`, `result_rows_have_status:false`) | per-seat record | **#22** ("A seat-status statement about a round's waves … is reproducible from a retained per-seat record … A headline count with no per-seat record is inadmissible") and **#76** (seat totals / settled / outstanding with timestamps) | **criterion'd** (22, 76). Round-52's `status.json` convention (`.ufo/waves/round-52/w1/<Seat>/status.json` with `seat`/`role`/`status`/`summary`/`artifacts`) is exactly the per-seat record #22 demands. **Observed at read time**: 38 of 48 seat directories carry a `status.json`; 10 do not yet (`RevCounterEscape`, `RevExtractor`, `ScoutCarrierChain`, `ScoutCensusRecheck`, `ScoutMknod`, `ScoutV6Corpus`, `ScribeEntryC1`, `ScribeMergeAdopt`, `SentCreds`, `SentSecrets`). #22 also requires each seat without a report to carry a retained cause or be marked `cause unknown` — a `status.json` with `status:"failed"`/`"blocked"` and a summary is the vehicle; the L1's wave accounting must not fold these into a headline count. |
| D3 | **Dispatch interpolation** — M51-6: all 36 r51 item prompts carried unresolved `{LANE}`/`{W1}` markers; the taken dispatch is immutable (`round-51.md` M51-6; `round-51-verifier-spotcheck.md` §6.3) | dispatch payload placeholder resolution | **#76, second sentence only** ("A generated per-seat prompt is asserted to begin with the directive bytes before dispatch (M34-16, D4)") — covers the *prefix*, not the *placeholder resolution*. Nothing in QUALITY.md requires the emitted item strings to be placeholder-free: `grep -c -iE 'interpolat|unresolved \{' corpus/QUALITY.md` → **0**; the only `placeholder` hit is **#43**, an unrelated EVM `__$…$__` linker placeholder; the only `unresolved` hit is **#81**, an unrelated "unresolved path". | **uncriterion'd → the lesson row must cite the fix's observed failure before any new criterion.** The r52 lesson's seeded M51-6 row (fix = a pre-dispatch assertion on the generator) is the required carrier; only after that row lands with its evidence pointer may a QUALITY row 99+ be added. **Observed at read time**: the r52 generator does carry the obligation (`gen-w1.py:4-5`, `:325-327`) and a checker exists (`w1/ExecWaveCheck/check-dispatch.py`, receipt `exit_code 0`, `stdout_sha256 d610c20f…`, `captured_at_utc 2026-10-30T10:47:22Z`, "dispatch placeholder check: clean"), and the emitted payloads carry **0** `{IDENT}`-shaped markers (`grep -oE '\{[A-Za-z_][A-Za-z0-9_]*\}'` over `w1-spec.json` → 0, over `w1-dispatch.json` → 0). Caveat for the L1: the checker's marker regex is `\{[A-Z_0-9]{2,}\}` plus one literal-path-brace pattern — it does **not** catch lowercase or mixed-case placeholders, and `w1-spec.json`/`w1-dispatch.json` are the *spec* files, not the rendered per-seat prompts actually delivered to the 48 seats; the claim that the *delivered* prompts are placeholder-free is **not established by what I read**. |
| D4 | **Misroot prevention** — M51-1: `MutGapRule` wrote `kaidoku-r51/w1-MutGapRule/amended-law-battery.py` at the **fleet** root; contained byte-exact, then removed; "no preventive helper is claimed fixed" (`round-51.md` M51-1; `round-51-verifier-spotcheck.md` §6.4). Same class as r50 M50-9 (fleet stray `tools/round-50-c3/sqfs-triage-v5.py`). | write-root / stray-output prevention | **none.** `grep -c -iE 'misroot\|stray file\|writes? (in)?to the fleet\|write scope' corpus/QUALITY.md` → **0**; `misroot` → **0**; `fleet root` → **0**. The nearest neighbours are #60 (scratch disk-inventory restriction — a *different* prohibition, about auditing the scratch tree, not about where a write lands), #82 (root the *sweep* at the base — about claim scope, not write targets) and #92 (registry row "write scope" cell — a registry field, not a write-root rule). | **uncriterion'd → the lesson row must cite the fix's observed failure before any new criterion.** The observed failures to cite are **M50-9** (`corpus/lessons/round-50.md:85`, fleet stray; "no preventive fleet-root control exists or was tested") and **M51-1** (`corpus/lessons/round-51.md:67`, the r51 recurrence — the class recurred after r50, which is the stronger evidence). The r52 repair named in `plans/round-52-claims.md` §Routed-defect-repairs 5 is a **read-only sweep helper** (`tools/round-52/misroot-sweep.sh`) with a fixture-repo selftest — a *detector*, and per the r51 closure the preventive side stays operator-side; a new criterion must therefore not claim prevention, only detection-and-containment. **This row is not seeded in the r52 lesson draft** — the L1 should require it before any QUALITY row 99+ on this class. |
| D5 | **Census hygiene — 19 W04 duplicate-URL warnings** (`round-51-verifier-spotcheck.md` §6.5; `round-51.md` "Census and bounded verification": "156 rows, 19 W04 warnings"; carried from r50 "18 W04") | registry duplicate-URL hygiene | **none** as a *criterion*: `grep -c -iE 'W04\|duplicate url' corpus/QUALITY.md` → **0**. The neighbouring criteria are #74 (a registry/index edit is verified by row count **and** per-status/per-tier tallies against the base blob — a *verification* rule for edits) and #93 (a routed registry defect closes only by a new `supersedes` row — a *closure* rule). Neither states that a duplicate URL across scopes must be resolved, nor that W04 is benign. | **uncriterion'd → the lesson row must cite the fix's observed failure before any new criterion.** Two observations that bear on how the round should treat it: (a) **replication** — I re-implemented the census W04 rule (`scripts/sources-census.sh:645`) against `corpus/SOURCES.md` (158 rows) and reproduced exactly **19** W04 rows, matching the committed r51 receipt (`corpus/lessons/round-51.md` "156 rows, 19 W04 warnings"; my census run over the current tree also prints 19 and `ok`, exit 0 — `census-w04.txt`); (b) **classification** — of the 19, **7 are explained by a `supersedes S0NN` relation** (S033→S032, S054→S052, S062→S058, S069→S065, S246→S147, S247→S149, S248→S138), i.e. the CORPUS.md rule-2 shape (a narrowing/superseding row reusing the URL), and **12 are not**: S047, S083, S090, S092, S102, S112, S117, S119, S123, S138, S142, S245. For those 12 I verified at row level that no same-URL sibling shares an identical `scope` or an identical `teaches` (0 duplicates of either), and that the census's stricter same-URL+same-scope rule (**E04**) fires **0** times — so the 12 are legitimately *distinct* scopes over a shared URL (e.g. the six `rea-agents-6.5.0.tgz` rows S079/S083/S090/S092/S119/S123 each teach a different reader/subsystem; S112/S245 split BE vs LE). **Inference (not a defect):** the "19 W04" count is largely a *warning-level* artifact of one package/doc URL serving several distinct scopes, not 19 wrong rows; a "row-by-row audit landing a correction set" (`plans/round-52-claims.md` §Routed-defect-repairs 6) would need a per-row wrongness finding that I did not find. The honest r52 disposition is to say the audit found no wrong row for 12 of the 19 and 7 rule-2 supersessions — not to append 19 superseding rows. **This row is not seeded in the r52 lesson draft.** |
| D6 | **Carried L0** — `kaidoku \| round-50`: unredacted GitHub `set-cookie` values (`_gh_sess`, `_octo`) remain in pushed history at `.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr`; a purge needs an operator-authorised force-push (`round-51.md` "Open L0 line"; `round-51-verifier-spotcheck.md` §6.6; `round-50.md` M50-5) | credential material in pushed history | **none.** `grep -c -iE 'credential\|set-cookie\|session cookie\|secret\|redact\|purge' corpus/QUALITY.md` → **0**. The binding rule lives **outside** QUALITY.md, in fleet `CORPUS.md`: "**No credential material, ever.** Secret values, session tokens, cookies …" (`CORPUS.md:49`) and rule 6 (`:129`) "No credential material, session or private URLs … — ever." QUALITY.md's own preamble says it is the *admission* bar and CORPUS.md rule 3 says admission stays in QUALITY.md — but CORPUS rule 3 also says SOURCES.md duplicates neither; the credential prohibition is a *protocol* rule, not an admission criterion. | **uncriterion'd as a QUALITY criterion, and deliberately so** — the class is already governed by fleet CORPUS.md rules (`:49`, `:129`), and the purge is operator-owned (force-push), not lane-fixable. **Recommendation: do NOT add a QUALITY row 99+ for the credential class**; record the carried L0 as an operator note in the r52 lesson (as r51 did) and let CORPUS.md rule 6 carry it. The r52 round-52 prompt/contract already forbids pasting `Set-Cookie` headers into receipts — that is a contract obligation, not a new criterion. **This row is not seeded in the r52 lesson draft**; per `plans/round-52-claims.md` §Routed-defect-repairs 7 the L0 is "not re-appended", which is consistent with no criterion. |

### D2-adjacent observation (not a routed defect, but it is the #22/#76 test surface)

Round-52's per-seat `status.json` shape (`seat`, `role`, `status`, `summary`, `artifacts`) satisfies #22's
"retained per-seat record" requirement *if* the files are committed. At read time
`git ls-files .ufo/waves/round-52 | wc -l` → **5** (only `gen-w1.py`, `w1-dispatch.json`, `w1-spec.json`,
`w1-validate.log`, `w1.ready`); the wave directories are untracked (`git status --porcelain` → `?? .ufo/waves/round-52/w1/`).
#22 says "reproducible from a **retained** per-seat record" and #76 requires the totals/settled/outstanding record
"in the same commit as any stop" — so the L1's wave accounting must read the `status.json` files **and** land them
(or land a derived per-seat ledger) in the lane before filing, or the #22 test is unmet at filing.

## 3. Gap summary for the L1

| item | state |
|---|---|
| QUALITY distinct criterion numbers | **98** (last = 98) |
| admission-table rows | 91 (numbers 1–74, 77–93) |
| bullet-only rows | 7 (75, 76, 94, 95, 96, 97, 98) |
| doubly-used numbers | **77, 78, 79** (table vs bullet) — an ambiguity already in the corpus, cited bare by r51 M51-8 |
| next free row number | **99** |
| routed defects already criterion'd | D1 (rows 76, 98), D2 (rows 22, 76) |
| routed defects uncriterion'd, lesson row required first | **D3** (interpolation), **D4** (misroot), **D5** (census W04) |
| routed defect where a new criterion is *not* advised | **D6** (credential L0 — governed by fleet CORPUS.md `:49`/`:129`; operator-owned purge) |
| r52 lesson rows the draft must seed before any QUALITY 99+ | M51-6-style interpolation row (seeded ✓), **misroot row (M50-9 + M51-1 evidence — NOT seeded)**, **census-W04 audit row (19 W04 / 7 rule-2 / 12 distinct-scope — NOT seeded)**; credential L0 row = operator note, not a criterion |

## 4. Receipts

- `qual-inventory.txt` — sha256 `991082a18d0548e03dad7c9e496cc8e0d2880329ebf1312dfef87bec6424d154`;
  the six C1–C7 checks above; run cwd = lane root; UTC 2026-10-30T10:49:51Z; exit 0.
- `census-w04.txt` — sha256 `bdf9fdb4197a209eae134e4ff4d8c05502d11732709341fae3ef6afd3bf8f93e`;
  command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`;
  stdout = 19 `W04` lines + `kaidoku ok <SOURCES.md>`; exit 0; UTC 2026-10-30T10:49:51Z.
  (Read-only; the script writes stdout only — no `--out` used.)
- W04 replication and classification were computed by re-implementing `scripts/sources-census.sh:645`
  over `corpus/SOURCES.md` (158 rows, 11 cells each) — the classifier is quoted in §2 D5; result: 19 warnings,
  7 supersedes-explained, 12 not, 0 same-URL+same-scope (E04) hits, 0 shared-`scope`/0 shared-`teaches` pairs
  inside the 12. This is my own re-derivation over committed bytes, not a lane-gate run.

## 5. Observation for the L1 — a sibling seat wrote into a *round-50* wave path (not mine)

At 07:53:57 local (mtime) — i.e. during this seat's read pass, after my own writes began — the tracked file
`.ufo/waves/round-50/w3/ScribeEntryC1.md` was **modified** in the lane tree (`git status --porcelain` now shows
` M .ufo/waves/round-50/w3/ScribeEntryC1.md`, `git diff --stat` → `30 insertions(+)`; the addendum is headed
"Addendum — the landing outcome"). **Not my write** — this seat touched only `.ufo/waves/round-52/w1/ScoutQualRows/`
and `.ufo/waves/round-52/w1/ScoutQualRows.md`. The round-52 seat that owns this material is `ScribeEntryC1`, whose
own seat dir is `.ufo/waves/round-52/w1/ScribeEntryC1/`; the modified path is under the **round-50** wave tree.
Two consequences for the L1: (a) a wave seat edited a **committed** lane file outside its own seat directory, which
the wave contract forbids ("Write ONLY inside …/<YourSeatName>/"); (b) the round-50 file's committed content changes,
so any r52 instrument that pins or diffs round-50 wave bytes sees a moved baseline. I did not modify, stage or
revert it (no git mutation permitted); the diff is preserved in the working tree for the L1 to judge.

## 6. Limits of this map

- QUALITY.md was read at the **working tree** (which equals the round base for this file: `git status --porcelain`
  lists no modification to `corpus/QUALITY.md`). If the L1 amends QUALITY.md in the freeze commit, the row numbers
  in §0 shift and the map must be re-derived against the freeze commit.
- I did not execute any lane instrument, the census in `--check` mode against the census3 tool, or any REA call.
- The §2 D5 classification is a re-derivation of the census's *warning* logic; it is not a judgment that the 12 rows
  are correct in their tier/anchor/teaches (that is #90/#91's business and needs source re-opening).
