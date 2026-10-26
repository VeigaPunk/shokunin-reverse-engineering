# R36CriticPredicateIdentity — predicate identity for R36-C1 / R36-C2

Seat: `R36CriticPredicateIdentity` (critic, round 36 wave 1). Advisory only; nothing in the lane was
changed. Read-only git; every probe ran in `$S=/fast/scratch/hyaku/kaidoku-r36/R36CriticPredicateIdentity`
with fixture repos created `git -C "$D" init -q` (toplevel verified) and removed at the end.

Revisions used: freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`, base
`cab59f221fe19726b5692bfa4d9a9679e96b8a73`, C1 after receipts
`3310d8fa27bfaa95ad858c4aaad6f6377f853982`, C2 repairs `d2e46ef5` (lane HEAD when read), controls
`6a870b9290e9566468d7d9e6d1b8308daf025b12`. REA root
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (`package.json .version` = `6.5.0`).

The rule I tested against is the round contract's §9 (`/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-36.md:439-455`,
item 9 "*Claim sizing*"), not a paraphrase: *"Freeze one predicate that is the same sentence in the
plan, the same condition in the counter's code and the same label in the receipt"*; *"Use no
universal clauses ("all", "complete", "every", "no harm anywhere") unless the counting command
enumerates the full set"*; *"A calibration claim must count mismatches between the lane's
self-assessment (SCORECARD/SHONEN) and observed repo state"*; *"Name the axis by the surface the
round changes, not by the number it produces … A coverage claim names the surface it moves
(frontier → core, a new tool, operation or edge class) and the command that would show it unmoved"*.

---

## 0. Bottom line

| leg | C1 | C2 |
|---|---|---|
| plan sentence == counter docstring (verbatim) | **PASS** (identical modulo the `"(frozen; same sentence…)"` prefix; diffed normally) | **PASS** (same) |
| sentence conditions == code conditions | **FAIL** — 9 divergences (§2), 2 universal clauses without an enumerator (§3) | **FAIL** — 8 divergences (§5), 4 universal clauses without an enumerator (§6) |
| condition == receipt label | **PASS with one gap** — the target labels (`carriers_matched`, `bindings`, `met_target`) exist; `met_target` also ANDs `carriers_unchanged`, which the sentence does not state (§8) | **PASS** — `mismatches`, `guards_ok`, `met_target` all present |
| claim named by the surface moved (§9) | **PARTIAL** — the two named surfaces (PROVINCE frontier bullet, README Firmware row) are never read; a stale Frontier bullet and a stale README Firmware row coexist with a passing counter (§9.1) | **PASS** — §9's calibration clause ("count mismatches between SCORECARD/SHONEN and observed repo state") is what the code does; note the boundary hazard §9.2 |

Strongest single counterexample per claim:

- **C1:** a fabricated `after.json` whose file list was copied from `oracle.tsv` and whose
  `evidence_id` was recomputed with the frozen `xpin-attribute.mjs` reaches `met_target: true` on all
  four carriers even though no REA run happened (§4, probe C1-D). The frozen control CTL-C1-2 fails
  *only* on `after_evidence_id_ok` (its own receipt), i.e. the control kills "forgot to recompute the
  id", not the class "forged oracle-copy envelope" it is named for.
- **C2:** a base pointer `x.md` that does not resolve is "repaired" by `docs/x.md` — a different
  document with the same basename — and the counter reports `mismatches: 0, guards_ok: true`
  (§7, probe C2-A). The frozen CTL-C2-3 kills substitution only when the basename *changes*.

Both counters are internally consistent and honest about what they print; the divergence is between
the sentence and the tested condition, which is the thing §9 freezes.

---

## 1. Method

1. Diffed the predicate sentence in `plans/round-36-claims.md` against each counter's module docstring
   (whitespace-normalized): **identical** for both claims.
2. Enumerated every clause of each sentence and matched it to the expression(s) that implement it in
   `tools/round-36/c1-counter.py` / `c2-counter.py` (line-referenced in §2/§5).
3. Audited the receipt fields the counter actually reads against the fields the committed evidence
   carries (envelopes, `*-run.json`, `oracle-run.json`, control JSONs).
4. Ran the frozen counters against the real repo (read-only) and built fixture repos that exercise
   each clause at its boundary, scoring each with the unmodified `measure()` function imported from
   the frozen module. Every probe is labelled below with its observed JSON.

Fixed-scratch (not evidence) was used for the fixtures; the fixture recipes are reproduced inline so
the probes can be re-run without those paths.

---

## 2. R36-C1 — sentence clauses vs tested conditions

Legend: **S↛C** = the sentence states it, the code does not test it. **C↛S** = the code tests it, the
sentence does not state it.

| # | sentence clause | what the code tests (`c1-counter.py`) | divergence | severity |
|---|---|---|---|---|
| C1-1 | "for each of the four frozen carriers" | `carriers_matched == TARGET` (TARGET=4) over `len(spec['carriers'])` entries; `res['carrier_ids']` is recorded and never compared; list length never checked | **S↛C** the universal is replaced by a count over a caller-supplied list. A 5-entry `carriers.json` with 4 receipted carriers scores true and `K5` (no oracle, no receipts) is simply `matched:false` (§4 C1-A). Carrier *identity* is unbound: renaming the four to `K5..K8` scores true (§4 C1-B) | high |
| C1-2 | "the committed REA … receipt **run with sasquatch on PATH**" / "the paired committed **no-sasquatch** receipt" | only envelope content: `subject.digest.sha256`, `operation=='extract_firmware'`, `provider.id=='unblob'`, `normalized_result.files`, `extraction_gaps` | **S↛C** the PATH state is nowhere tested. All eight envelopes carry `"environment": null`. The only committed attestation is `K*/{before,after}-run.json` (`sasquatch:""` for before; `sasquatch:/home/vgpnk/.local/bin/sasquatch`, `sasquatch_sha256 ad02d27a…`, `sasquatch_version "unsquashfs version 4.5.1 (2022/03/17)"`, `utc` for after; produced by `c1-run.sh:71-77`), and the counter never opens those files. The counter's own green selftest fixture contains no `*-run.json` at all, so the green case proves the omission | high |
| C1-3 | "the committed **REA** … receipt", "recompute to their stored evidence id **under the rea-agents 6.5.0 rule**" | `evidence_ids()` = `node <xpin at freeze> --pkg65 <argv> --pkg67 <argv>`; accept iff `stored == id65` and `id65.startswith('ev_')` | **S↛C** (a) no `--parse`: the tool's `parseEvidence` verdict for 6.5.0 (`xpin-attribute.mjs` `--parse` mode, lines 224-236) is never consulted, so a record the 6.5.0 parser would reject passes if its id matches; (b) `pkg65` is a bare path argument — its version/digest is never checked (it is 6.5.0 today, verified); (c) passing `pkg65` as `--pkg67` discards the tool's pin discrimination (column 5 is always `both`) | high |
| C1-4 | "publishes **every regular file** of the frozen independent unsquashfs oracle" | `hits == len(oracle_rows)` where rows come from `K*/oracle.tsv` at the freeze commit and `oracle_frozen` requires `freeze:oracle.tsv == rev:oracle.tsv` | **S↛C** the oracle's *own* completeness, producer and regular-files-only property are unattested: `K*/oracle-run.json` records `unsquashfs: "unsquashfs version 4.7.5 (2026/03/01)"`, `squashfs_offset`, and `regular_files` = 3/4/2130/2130, and has **no `exit` key**; the counter reads none of it and only requires `oracle_files > 0`. A 1-row oracle with a 1-file after receipt scores true (§4 C1-E) | high |
| C1-5 | "**no sasquatch extraction gap**" | `sasquatch_gap()` = some gap with `kind=='missing-extractor-dependency'` **and** `'sasquatch' in dependencies` | **C↛S** kind-narrowed: a gap of another kind naming sasquatch passes (§4 C1-F). The `kind` narrowing is defensible from the before-clause but is not in the sentence | low-medium |
| C1-6 | "the **frozen** independent unsquashfs oracle", "the four **frozen** carriers" | frozen = *whatever commit `--freeze` names* (`carriers.json` and `oracle.tsv` compared freeze-vs-rev) | **S↛C** nothing anchors `--freeze` to `790561d4…` or to an ancestor of `--rev`. Passing `--freeze <data commit>` makes a carrier rewrite in the data commit invisible: `carriers_unchanged:true`, `carriers_matched:4`, `met_target:true`; the same bytes measured with the real freeze give `carriers_unchanged:false`, `carriers_matched:0` (§4 C1-C) | high (provenance) |
| C1-7 | "Before receipts (frozen with the claim; sasquatch absent from PATH): `K*/before.json`" (claims evidence block) | `before_present`, content/operation/subject/gap/hits + id recompute | **S↛C** identity with the *frozen* before receipt is not tested: a re-run before envelope (`parameters.output_directory` changed, id recomputed) passes (§4 C1-D2). Only "some gap-bearing before envelope" is bound | medium |
| C1-8 | "PROVINCE.md holds a round-36 Core **row naming sasquatch** that **cites** the round-36 knowledge entry" | `section(prov, '## Round-36 additions to Core')` (exact h2 line), then a `|` line whose **first cell** matches `sasquatch` and whose text contains `ENTRY` as a substring | **C↛S** three extra restrictions: (a) exact h2 heading — the lane's existing Core-additions precedent is the h3 `### Round-4 additions to Core (verified 2026-10-13)` at `PROVINCE.md:121`, so an h3 round-36 section is false-red (§4 C1-G3); (b) sasquatch only in the first cell (§4 C1-G2); (c) `ENTRY in row` is an unanchored substring, so `…recursion.md.bak` would also satisfy "cites" | medium |
| C1-9 | "which **cites** a SOURCES.md row opened 2026-10-26" | `sid_tokens()` over lines where `line.startswith('source:')`; registry row must have exactly 11 cells; `c[8]=='2026-10-26'`; `ENTRY` an exact comma-split element of `c[10]` | **C↛S** the `source:` spelling is a format requirement the sentence does not state: 49/122 committed entries begin with `source:`, the most recent (`2026-10-25-r34b-…md:5`) uses `sources:` and would be false-red (§4 C1-G1); a used-by written with a range or backticks is false-red; a registry table with ≠11 columns is silently "unsourced" rather than unevaluable | medium |
| C1-10 | Target: "`carriers_matched == 4` and every binding true (`met_target`)" | `met_target = carriers_unchanged AND carriers_matched==4 AND all(bindings)` | **C↛S** `carriers_unchanged` is an extra conjunct (it is printed, so the label test still passes) | low |
| C1-11 | "publishes every regular file … (same relative path suffix, same sha256)" | `sha==fs and (fp==rel or fp.endswith('/'+rel))`; extra published files allowed | consistent (K3/K4 publish 2147 files vs 2130 oracle rows; each carries 2 `unpublished-entry` gaps and 2 `unpublished_entries`, which do not account for the 17 extra published files) — no divergence; noted so the "every" is not read as "exactly" | — |

## 3. R36-C1 — universal clauses and their enumerators

| universal | enumerator used | full set actually enumerated? |
|---|---|---|
| "for each of the four frozen carriers" | `carriers_matched` count vs `TARGET=4` | **No** — count, not identity; list length free; ids free (probes C1-A/C1-B) |
| "every regular file of the … oracle" | `oracle.tsv` rows (freeze==rev) | **No** — the oracle's own population (2130 for K3/K4) is only in `oracle-run.json`, unread (probe C1-E) |
| "both receipts recompute" | loop over `('before','after')` × carriers | **Yes** |
| "no sasquatch extraction gap" | all `extraction_gaps` with the kind+dependency filter | **Yes**, under the kind-narrowed reading |
| "PROVINCE.md holds **a** round-36 Core row … whose used-by lists that entry" | existential (`any`/`bool`) | **Yes** (existential, correctly) |

## 4. R36-C1 — counterexamples (fixtures scored with the frozen `measure()`)

Fixture recipe (identical to the counter's own selftest): `git init` a scratch repo; freeze commit =
`tools/round-27/xpin-attribute.mjs` + `carriers.json` + `K*/oracle.tsv`; data commit = plus
`K*/{before,after}.json` and the PROVINCE/entry/SOURCES/README fixture texts from
`tools/round-36/selftest/dev-*`. Scores below are `measure(d, rev, freeze, PKG)['met_target']`.

| probe | what changed vs the green fixture | result |
|---|---|---|
| C1-0 green | — | `met_target: true`, `carriers_matched: 4` |
| **C1-A five carriers** | `carriers.json` lists `K1..K5`; only `K1..K4` have oracle/before/after | **`met_target: true`, `carriers_matched: 4`, K5 `{oracle_files:0, before_present:false, after_present:false, matched:false}`** |
| **C1-B ids renamed** | the four carriers are named `K5..K8` (same bytes) | **`met_target: true`, `carriers_matched: 4`** |
| **C1-C freeze := data commit** | freeze commit's `carriers.json` carries `sha256:"aaa…"`; the data commit rewrites it to the receipt sha and adds the receipts | **`--freeze <data>`: `met_target:true, carriers_unchanged:true`; `--freeze <real freeze>`: `met_target:false, carriers_matched:0, carriers_unchanged:false`** |
| **C1-D forged after + recomputed id** | `after.json` = copy of `before.json` with `normalized_result.files` = `oracle.tsv` rows and `extraction_gaps: []`; `evidence_id` set to the id `xpin-attribute.mjs` computes from those bytes | **`met_target: true`, `carriers_matched: 4`** — no REA run involved; the before receipt is untouched |
| C1-D2 before is not the frozen one | `before.json` re-run signature (`parameters.output_directory` changed) with recomputed id | **`met_target: true`** |
| C1-E truncated oracle | `oracle.tsv` = 1 row per carrier; after publishes exactly that row (id recomputed) | **`met_target: true`, `oracle_files:1`, `after_oracle_hits:1` on all four** |
| C1-F gap kind | after has a gap `{kind:'unsupported-compression', dependencies:['sasquatch']}` | **`met_target: true`** |
| **C1-G stale named surfaces** | PROVINCE keeps the frozen Frontier bullet `- **sasquatch** — unblob's squashfs recursion extractor (AUR-only); 7z fallback covers the carved-image path today.` and README keeps `…recursion blocked by missing sasquatch` in the Firmware row, *and* adds the round-36 Core row | **`met_target: true`** (all seven bindings true) |
| C1-G1 entry header | entry cites `Sources: S107 — x` instead of a `source:` line | `met_target: false`, `carriers_matched: 4` (false red) |
| C1-G2 sasquatch in a non-first cell | Core row `| squashfs recursion | sasquatch | <entry> |` | `met_target: false`, `carriers_matched: 4` (false red) |
| C1-G3 h3 Core heading | `### Round-36 additions to Core` (the lane's Core-additions level) | `met_target: false`, `carriers_matched: 4` (false red) |

Real-repo reading at the C1 after-receipts commit (bindings not yet landed, so this is the expected
mid-round state, quoted to show the carrier side is what scores):

```
$ python3 -I -B tools/round-36/c1-counter.py --root . --rev 3310d8fa27bfaa95ad858c4aaad6f6377f853982 \
    --freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0 --pkg65 …/rea-agents
{"bindings": {"coverage_map_row": false, "entry_present": false, "entry_source_ids": [],
 "opened_source_rows": [], "province_core_row": false, "province_core_section": false,
 "sourced": false}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": false,
 "revision": "3310d8fa…"}   EXIT=1
```

---

## 5. R36-C2 — sentence clauses vs tested conditions

| # | sentence clause | what the code tests | divergence | severity |
|---|---|---|---|---|
| C2-1 | "**every** backticked repo pointer in them resolves at that revision (path exists, line range inside the file)" | `TOKEN = `([^`\s]+)`` then `PTR = ^([A-Za-z0-9_.][A-Za-z0-9_./+-]*?)(?::(\d+)(?:-(\d+))?)?$`, then `'/' in path or path.endswith('.md')`; `resolves()` = `cat-file -e` + `1<=lo<=hi<=lines` | **S↛C** the universal runs over a filtered subset. Tokens lacking `/` and not ending `.md` are dropped: real backticked repo pointers `config-post-pair.txt` (the sibling of the counted `…/config-pre-pair.txt` in the same capability cell) and `result.json`, plus the bare ranges `95-116`, `:114-116`, `88-116` in box 4. A fabricated `missing-receipt.txt` in the same cell scores `mismatches: 0` (§7 C2-C) | high |
| C2-2 | "the **four** stated counts equal the counts the lane's command A / command B observe" | O1 `(\d+)/(\d+) knowledge files mapped`; O2 `(\d+)/(\d+) queue-drain rule blocks`; O3 `(\d+)/(\d+) preselected reconciliation obligations`; O4 box1 `(\d+)/(\d+) rule blocks` | **S↛C / C↛S** (a) the surfaces state **14** count-like `N/M` values at HEAD, of which 4 are compared: the coverage row's history `116/116`, `109/109`, `78/78`, `107/107`, `108/108`, the depth row's second `17/17` and `9/9`×2, and box 4's `207/153`, `0/207` are unchecked — including exactly the stale-number class that produced the base mismatch; (b) the "four" cover only **three** distinct commanded observables (O2 and O4 both compare command A's `resolved_rules/rule_blocks`); (c) the revision a stated count is attributed to is not tested (the coverage row says "…mapped at `cab59f22`" while the comparison runs at `--rev`) | high |
| C2-3 | "the **three** stated section ranges equal the observed heading-to-last-non-blank-line ranges" | R1 depth row `SKILL\.md:(\d+)-(\d+)`; R2 box1 same; R3 box4 `PROVINCE\.md:(\d+)-(\d+)` (all `re.search`, i.e. first match) | **S↛C** the surfaces state **five** ranges at HEAD: `SKILL.md:81-314` (depth), `SKILL.md:77-191` (depth, historical baseline), `SKILL.md:81-314` (box1), `PROVINCE.md:97-118` (box4), `PROVINCE.md:8-14` (box4). Two of the three checks are the same SKILL range; `SKILL.md:77-191` and `PROVINCE.md:8-14` are only checked for resolvability. A fabricated fourth wrong-but-resolving range passes (§7 C2-E). The observed-range method also differs between the checks: craft stops at `## `, Adjacent stops at `#` (any level) | high-medium |
| C2-4 | "every pointer unresolved at the base **repaired by a resolving pointer to the same document**" | `unrepaired` if no rev pointer in the same unit satisfies `p2==path or p2.endswith('/'+path)` | **S↛C** "same document" is implemented as a *suffix* match: a same-basename document in another directory counts as repaired (§7 C2-A). The frozen CTL-C2-3 only kills basename changes | high |
| C2-5 | "the SCORECARD `## Capabilities` **table rows**" | `units()`: iterate the section, take `|` lines once started, **break at the first non-`|` line** | **S↛C** only the first contiguous table block is enumerated; a capability row after a blank line or a note is never scanned (§7 C2-B). Units are also keyed by first cell, so two rows with the same first cell collapse to one | medium |
| C2-6 | "the SHONEN.md **boxes**" | `^- \[[ x~]\] (.*)$` plus `\n  `-indented continuation | **S↛C** a box written with any other marker (`- [X]`, `- [!]`) or a tab/single-space continuation is invisible; a *newly added* such box with a broken pointer passes (§7 C2-D). A *changed* marker on an existing box is caught, but as a removed unit by the delete guard, not as an unresolved pointer | medium |
| C2-7 | "the counts the lane's **command A / command B** observe" | `command_a()` is a faithful port of SCORECARD `## Measurement recipes` A (same `ls-tree`, same section split, same regexes, same per-ref bounds; only `missing`/`dangling`/`*_score` are dropped); `command_b()` counts `status=='aligned'` in `evidence/round-1-2026-10-15/result.json` only | **S↛C** documented recipe B reads `rubric.json` *and* `result.json` and says "review those sources before accepting the count" (SCORECARD `## Measurement recipes`, **B**); the counter never opens `rubric.json`, so the calibration row's cited pointer is only tested for resolvability and a flag flip with no source support would score. Command A's port is correct (line-by-line compared) | medium |
| C2-8 | "**zero mismatches** with observed repo state" | `mismatches = len(unresolved) + len(assertion_mismatches)` | **S↛C** as a summary: the tested set is 15 units → the filtered pointer set + 7 hardcoded checks. The "zero" is true over that set, not over the sentence's set (§C2-1..3) | high (summary of the above) |

## 6. R36-C2 — universal clauses and their enumerators

| universal | enumerator | full set? |
|---|---|---|
| "every backticked repo pointer in them" | `TOKEN`+`PTR`+`'/'-or-.md` filter | **No** — bare filenames and bare ranges dropped (probe C2-C) |
| "the four stated counts" | four hardcoded regexes | **No** — 14 count-like statements exist; the four chosen are not named in the sentence |
| "the three stated section ranges" | three hardcoded regexes | **No** — five range statements exist; the three are not named in the sentence |
| "the SCORECARD `## Capabilities` table rows" | first contiguous `|` block | **No** — rows after a blank line escape (probe C2-B) |
| "the SHONEN.md boxes" | `^- \[[ x~]\]` only | **No** — other markers escape (probe C2-D) |
| "no unit removed / no fewer pointers / every base-unresolved repaired" | unit-key dict (deduped by first cell), aggregate pointer count, per-path suffix match | **Partially** — the delete guard is sound; the repair clause is suffix-based, not identity |

## 7. R36-C2 — counterexamples

Fixtures: two commits (base, rev) built from the counter's own selftest tree
(`SCORECARD.md`/`SHONEN.md`/`SKILL.md`/`PROVINCE.md`/`corpus/README.md`/`result.json`/
`corpus/knowledge/2026-10-01-{a,b,c}.md`/`docs/x.md`/`d/y.md`); base row = `cov='2/2'`,
`cap_ptr='`x.md`'` so both base mismatches exist. Scores are `c2.measure(d, rev, base)`.

| probe | change vs green | result |
|---|---|---|
| C2-0 green | — | `met_target: true`, `mismatches: 0`, `guards_ok: true` |
| **C2-A same-basename repair** | rev capability row cites `` `docs/x.md` `` (exists); base cited `` `x.md` `` (absent) | **`met_target: true`, `mismatches: 0`, `guards_ok: true`, `unrepaired: []`** — a different document accepted as "the same document" |
| **C2-B row after a blank line** | rev Capabilities table gets `\n| cap two | w | `d/missing.md` | r |` after a blank line | **`met_target: true`, `mismatches: 0`** — the row is never scanned |
| **C2-C bare missing filename** | rev capability row adds `` `missing-receipt.txt` `` (no such file) | **`met_target: true`, `mismatches: 0`** — filtered out as a non-pointer |
| **C2-D new box, marker `X`** | base and rev both carry `- [X] New box\n  asserted `d/missing.md`` | **`met_target: true`, `mismatches: 0`, `missing_units: []`**; the same box written `- [~]` gives `met_target:false`, `unresolved:[["shonen:New box","d/missing.md"]]` |
| C2-D2 existing box marker changed | box 2 marker `~`→`X` in rev | `met_target: false` — caught as a removed unit (`guards_ok:false`), which is the delete guard, not the pointer check |
| **C2-E extra wrong-but-resolving range** | rev capability row adds `` `PROVINCE.md:1-2` `` (resolves; the observed Adjacent range is 3-5) | **`met_target: true`, `mismatches: 0`** — only the three hardcoded ranges are compared |
| C2-F count phrase deleted | coverage cell without `knowledge files mapped` | `met_target:false`, `O1 stated:null` (covered by the selftest's "count deleted" case) |

Real-repo reading (controls, committed):

```
ctl-c2-0-do-nothing.json : mismatches 3, unresolved [["cap:pre-registered two-lane live battery on
  REA 6.5.0","receipts-B/"], ["shonen:No cross-domain bleed (PROVINCE.md still accurate)",
  "ScoutSkillPlacement.md"]], guards_ok false
  observed: command_a {mapped 122, knowledge_files 122, resolved_rules 17, rule_blocks 17},
            command_b [9,9], craft_range [81,314], adjacent_range [97,118]
ctl-c2-2-delete-bad-pointers.json : mismatches 0, guards_ok false (pointers_not_fewer)
ctl-c2-3-substitute-other-document.json : mismatches 0, guards_ok false, unrepaired = both paths
  (the substitution there changes the basename — the case C2-A passes)
```

Units enumerated at HEAD: 15 (`owned:` 3, `cap:` 8, `shonen:` 4). Of the 122 knowledge entries,
49 begin a line with `source:` (the only form C1's `sid_tokens()` accepts) and the most recent entry
uses `sources:`; 50 match a `^[Ss]ources?` header or a `| S###` row. No *currently* skipped token in
the three surfaces is a broken pointer (`config-post-pair.txt` and `result.json` both exist), so the
filter is a latent hole, not a live one.

---

## 8. Receipt labels

- C1 receipt: `predicate:"P36-C1"`, `target:4`, `revision`, `freeze`, `carriers_matched`,
  `carriers_unchanged`, `bindings{province_core_section, province_core_row, entry_present,
  entry_source_ids, opened_source_rows, sourced, coverage_map_row}`, `met_target`. The claim's target
  names `carriers_matched`, every binding and `met_target` — all present. `carriers_unchanged` is
  printed but absent from the sentence (C1-10).
- C2 receipt: `predicate:"P36-C2"`, `revision`, `base`, `pointers`, `unresolved`, `assertions`,
  `assertion_mismatches`, `observed{command_a, command_b, craft_range, adjacent_range}`,
  `guards{missing_units, base_pointers, pointers_not_fewer, base_unresolved, unrepaired}`,
  `guards_ok`, `mismatches`, `met_target`. Labels match the target sentence exactly.
- Neither receipt carries the *freeze* hash it is bound to for C2 (C2 has none), and C1's freeze is
  only in `argv`.

---

## 9. §9 checks

### 9.1 C1 is not fully named by the surface it moves

The claim names two surfaces moved — the `PROVINCE.md` `### Round-4 frontier (post-unlock)` **sasquatch**
bullet (`PROVINCE.md:149-150` at HEAD, verbatim the quoted text) and the `corpus/README.md` Firmware
row (`corpus/README.md:44`, "…AppImage SquashFS carved but recursion blocked by missing sasquatch";
the same gap also at `:162` and `:227`). The counter reads **neither**: its only PROVINCE read is the
literal `## Round-36 additions to Core` section, and its only README read is the `## Coverage map`
section. Probe C1-G shows both stale sentences surviving a `met_target: true` run, producing a lane
that says "recursion blocked by missing sasquatch" and "Core: sasquatch works" in the same file.

The measured subject is in fact the REA capability (receipts + oracle); the province/README move is
only half-bound (Core row presence). Under §9 ("A coverage claim names the surface it moves
(frontier → core, …) and the command that would show it unmoved"), the frontier half needs a
condition (e.g. the bullet absent, or its first cell no longer carrying the blocked-by clause).

### 9.2 C2 satisfies §9's calibration clause; two boundary hazards remain

§9: "A calibration claim must count mismatches between the lane's self-assessment (SCORECARD/SHONEN)
and observed repo state. It cannot be an assertion." C2 does exactly that (`mismatches` over
SCORECARD+SHONEN units vs command A/B + ranges) — **pass**.

Hazards, not defects:

- The repaired surfaces are the **coverage** row's number, a capability pointer and a SHONEN pointer;
  the calibration row itself (O3, 9/9) is unchanged, so the claim's delta on its named axis is 0 and
  the coverage row is edited by both claims in this round (C2 → `122/122 at cab59f22`, then re-stated
  after C1's entry to `123/123`). The claims disclose this ("the row is re-stated then"), and C2 is
  verifiable at its own landing commit, so §2.3 separability holds; the final-tip pass depends on a
  second post-C2 edit.
- The SCORECARD coverage row now defines its own observable as *the counter itself* ("the command-A
  observable in `tools/round-36/c2-counter.py`"). §9 asks for a command over committed bytes; citing
  the measuring instrument inside the measured row makes the "command A" clause self-referential —
  a duplicate authority even though `command_a()` is a faithful port of the documented recipe.

### 9.3 Do-nothing reachability

Both claim targets are unreachable by do-nothing: CTL-C1-0 `met_target:false` (exit 1) at base,
CTL-C2-0 `mismatches:3, guards_ok:false` at base. No violation. The controls' *fixture repos* for
CTL-C1-1 / CTL-C1-2 / CTL-C2-1 / -2 / -3 were scratch clones (`/fast/scratch/hyaku/kaidoku-r36/L1/ctl.*`
in their `argv`) that are not committed, so those five receipts are not re-derivable from the lane —
an evidence-custody gap in the control set, separate from the predicate.

### 9.4 Selftest red cases assert only the exit code

Both selftests assert `met_target`/exit only, never *which* condition the case broke. That is how
CTL-C1-2's class survives: the control's own JSON shows the forged envelopes failing on
`after_evidence_id_ok` alone (`after_oracle_hits == oracle_files` 3/4/2130/2130,
`after_sasquatch_gap:false`, `before_*` all true). The "13 red" in the claims is therefore not
evidence that each *named* class is killed.

---

## 10. Smallest safe corrections (advisory; both counters are frozen for this round)

C1 — in priority order:

1. Bind carrier identity: `res['carrier_ids'] == ['K1','K2','K3','K4']` and
   `len(spec['carriers']) == 4` (kills C1-A/C1-B).
2. Bind the freeze: make `790561d4…` a constant (or require it to be an ancestor of `--rev` and
   `carriers.json`/`oracle.tsv` blobs to equal the lane's frozen blobs) — kills C1-C.
3. Read `K*/{before,after}-run.json`: require `before.sasquatch == ''`,
   `after.sasquatch` non-empty with a sha and version, `after.utc > freeze commit time`,
   `carrier_sha256 == carriers.json sha`, `exit == 0` — kills C1-2.
4. Cross-check `oracle.tsv` row count against `oracle-run.json.regular_files` and its
   `unsquashfs` version; add an `exit` key to `oracle-run.json` — kills C1-E (and closes the
   "regular files only" identity).
5. Run `xpin-attribute.mjs --parse` and require `parseEvidence-6.5.0 accept`; pin `--pkg65` by
   `package.json` version + digest — kills C1-D/half of C1-3.
6. Widen the Core-row test (sasquatch in any cell, heading level as frozen and stated, anchored
   `ENTRY`) or state the narrow form in the sentence; accept `sources?:` for entry citation, or put
   the `source:` requirement in the predicate — removes C1-G1..G3 false reds.
7. Move `carriers_unchanged` into the sentence; add the frontier-bullet condition.

C2 — in priority order:

1. Replace the suffix repair test with identity (exact path, or "the base path with a directory
   prefix added, where the added prefix is the wave directory the base sentence itself names") —
   kills C2-A. A cheap formal version: also require the repaired pointer's basename and its
   final two path components to match.
2. Enumerate all capability rows (do not break at the first non-`|` line) and key units by
   (section, first cell, ordinal); accept every `^- \[[^]]\]` box marker — kills C2-B/C2-D.
3. Treat any backticked token containing `/` or a known extension (`.md .json .txt .py .sh .mjs .tsv
   .log`) as a pointer, and print the skipped tokens as a receipt field — closes C2-C and makes the
   universal auditable.
4. Name the four counts and three ranges explicitly in the predicate (or compare every stated `N/M`
   and `path:N-M` in the units); that removes the ambiguity C2-2/C2-3 rest on.
5. Read `rubric.json` for command B, or state in the predicate that B is the `aligned/total` flag
   count over `result.json`.
6. Have the coverage row cite the documented recipe in SCORECARD rather than the counter.

---

## 11. Live state observed (no verdict on the claims; L1 owns the target)

- C1 at `3310d8fa`: `carriers_matched:4`, `carriers_unchanged:true`, all seven doc bindings false,
  `met_target:false` (the entry/Core/README/SOURCES chain has not landed at HEAD `d2e46ef5`).
- C1 evidence is materially as the claim describes: `before.json` carries
  `extraction_gaps[0] = {kind:"missing-extractor-dependency", handler:"squashfs_v4_le",
  dependencies:["sasquatch"]}` and 0/0/2/2 published files; `after.json` carries no sasquatch gap and
  publishes 3/4/2147/2147 files against 3/4/2130/2130 oracle rows.
- C2 at HEAD: base control `mismatches:3`; the two base-unresolved pointers now resolve at HEAD
  (`.ufo/waves/luna-round-6/receipts-B/`, `.ufo/waves/round-30/w1/ScoutSkillPlacement.md`), and the
  coverage row reads `122/122 knowledge files mapped at cab59f22` — which will need re-stating after
  C1's entry moves the denominator to 123.

## 12. Limits

- I did not re-run REA extraction, unsquashfs, or any carrier fetch; all carrier-side facts are read
  from committed evidence.
- I did not run either selftest end to end against the real toolchain (the lane's own seats do); the
  fixture probes above exercise the same `measure()` code path and are labelled as fixtures.
- `[INFERENCE]` marks: (a) that a forged envelope with a recomputed id is indistinguishable from a
  real one *to this counter* is demonstrated, but I did not attempt to show that such a forgery
  would survive a human review of `raw_result`; (b) probe results are properties of the frozen code
  and of my fixtures, not of the lane's currently committed surfaces, except where a real-repo
  reading is quoted.
- No tooling was installed or upgraded for this seat (nothing was needed beyond `python3`, `git`,
  `node` and the already-installed REA 6.5.0 root).
- `PROVINCE.md` and `corpus/SOURCES.md` carried uncommitted working-tree edits when I read (the C1
  landing in progress). Every counter reading quotes a commit (`git show`/`ls-tree` at `--rev`), so
  the worktree plays no part in any result above.

## Appendix — compact reproducers

Forged-id probe (C1-D), run from the lane root:

```sh
S=$(mktemp -d); cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B - "$S" <<'PY'
import json, subprocess, sys, importlib.util, os
S=sys.argv[1]; LANE='.'; PKG='/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
sp=importlib.util.spec_from_file_location('c1','tools/round-36/c1-counter.py')
c1=importlib.util.module_from_spec(sp); sp.loader.exec_module(c1)
B=json.load(open('tools/round-36/selftest/dev-before.json'))
OR=open('tools/round-36/selftest/dev-oracle.tsv').read().splitlines()
rec=json.loads(json.dumps(B))
rec['normalized_result']['files']=[{'relative_path':'x/'+l.split('\t')[0],'sha256':l.split('\t')[1]} for l in OR]
rec['normalized_result']['extraction_gaps']=[]
p=os.path.join(S,'r.json'); json.dump({'data':rec},open(p,'w'))
out=subprocess.run(['node','tools/round-27/xpin-attribute.mjs','--pkg65',PKG,'--pkg67',PKG,p],
                   capture_output=True,text=True).stdout.split('\t')
print('stored-before', out[1], 'computed-650', out[2])   # set rec['evidence_id']=out[2]; the counter then passes
PY
```

The rest of the C1 fixtures are the same files with `carriers.json`/`oracle.tsv` variants as listed in
§4; the C2 fixtures are the counter's own selftest tree with the row/pointer/marker variants of §7.
