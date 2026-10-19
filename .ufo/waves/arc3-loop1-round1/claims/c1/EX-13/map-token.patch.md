# EX-13 — map-token patch for `corpus/README.md` (PATCH TEXT, not applied)

Seat EX-13 | chain c1 | role executor | wave `arc3-loop1-round1` | 2026-10-19

- Repo HEAD at drafting: `e845c2b524ad2e59871e004c51a1386e192a74ab`
- Before-state: `corpus/README.md` 190 lines, sha256
  `7c0cf67143eebc57a949c54884712262954d2ed984cd66eea8aab44362cb2568`;
  EVM row = line 38 (line sha256 `dad8484c…`), git blob `7bcc4af`
- Chain claim this serves: C1 coverage — command A re-measures
  `knowledge_files`/`mapped` 81 → 82, `missing []`, `dangling []`, rules 13/13,
  prior 81 tokens byte-identical.
- No seat writes `corpus/`; this artifact is proposed patch text only.

## 1. Deliverable

**Primary hunk (recommended): token-only, stem `2026-10-19-arc3-r1-evm-real-solc`.**

- patch: `map-token.primary.patch`, sha256
  `ddfe01165fdbb2fefa9a802b99f454bb574dddb926e5b807018571f78fc29cad`
- applied result: `README.primary.md`, sha256
  `b74b8d34abe47525c92b81f57829f8bd838a62fcc879ea4641277b4986944467`
- **byte-identical to `claims/c1/RV-4/map-token.frozen.patch` and to
  `claims/c1/RV-4/README.after.md`** (RV-4's verified verdict applies to these
  exact bytes), and byte-identical to the map-token hunk EX-12 carries in
  `claims/c1/EX-12/knowledge-entry.patch.md` (their "Hunk B", which they mark
  as carried only for self-containedness). **Land it once, not twice.**

Alternate: `map-token.alt-prose.patch` (same token, plus the same-line state-cell
prose update the chain plan sketched) — see §3.

## 2. Primary hunk — patch text

```diff
diff --git a/corpus/README.md b/corpus/README.md
index 7bcc4af..92c472a 100644
--- a/corpus/README.md
+++ b/corpus/README.md
@@ -35,7 +35,7 @@ A row is written when its file exists, never before.
 | `knowledge/2026-10-13-r4-10-real-version-pair` | full compare pipeline at 41-43MB (`op` 2.34.1→2.40.0, ~6-7min per verb — every verb re-imports fresh); CLI `rea compare` caps at `status:unknown` vs domain `compareBundles`+`record_pairs` → `status:changed`; Go bump (1.25.7→1.26.8) collapses symbol recovery 33,060→11,595 procs — pair by ELF role/address, not symbol name | `rea analyze`/`search`/`function`/`compare` + domain `compareBundles`/`compareFunctions` |
 | Runtime observation | `2026-10-13-r3-runtime-observation` | held — CDP enumerate/inspect on self-launched chromium + electron; scenario capture ran |
 | `knowledge/2026-10-13-r4-08-observe-verbs` | observe/reconcile legs closed: `observe-web-session` (self-scopes origins), `observe-web-execution` (perturbing counter-reset coverage, no self-scope), `observe-javascript-runtime` + `reconcile-javascript-runtime` held end-to-end; `capture-electron-scenario` typed refusal (`cleanup_incomplete`); node `--inspect` targets need a real file | live CDP (:9222 chromium) + V8-inspector (:9229 node) probes |
-| EVM | `2026-10-13-r3-evm-interface` | held — EVMole selectors recovered from synthetic dispatcher; positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc` | held — EVMole selectors recovered from synthetic dispatcher; positional encoding quirk |
 | Host anomaly triage | `2026-10-13-r2-jq-shadow-verdict`, `2026-10-13-r3-jq-provenance` | resolved — byte-identical upstream + provenance traced to kimi swarm bootstrap 2026-10-03 |
 | Synthesized carriers | `2026-10-13-r3-keyed-archive-carriers` | held — keyed-archive/interface-builder/dylib-trace all work on Linux synths; recipes recorded |
 | Evidence model | `2026-10-13-r2-evidence-bundle-schema` | held — snapshot envelope vs inner bundle schema, content-addressed ev_ ids |
```

Form: same physical line, token appended to the row's token cell, **no row
insert**, **no line-count change** (190 → 190), state cell untouched — the
`arc2-loop1-round6` precedent (commit `596df1c`, `corpus/README.md:22` row:
token appended to the existing row's token list).

## 3. Alternate hunk — patch text (optional)

```diff
diff --git a/corpus/README.md b/corpus/README.md
index 7bcc4af..41b2abe 100644
--- a/corpus/README.md
+++ b/corpus/README.md
@@ -35,7 +35,7 @@ A row is written when its file exists, never before.
 | `knowledge/2026-10-13-r4-10-real-version-pair` | full compare pipeline at 41-43MB (`op` 2.34.1→2.40.0, ~6-7min per verb — every verb re-imports fresh); CLI `rea compare` caps at `status:unknown` vs domain `compareBundles`+`record_pairs` → `status:changed`; Go bump (1.25.7→1.26.8) collapses symbol recovery 33,060→11,595 procs — pair by ELF role/address, not symbol name | `rea analyze`/`search`/`function`/`compare` + domain `compareBundles`/`compareFunctions` |
 | Runtime observation | `2026-10-13-r3-runtime-observation` | held — CDP enumerate/inspect on self-launched chromium + electron; scenario capture ran |
 | `knowledge/2026-10-13-r4-08-observe-verbs` | observe/reconcile legs closed: `observe-web-session` (self-scopes origins), `observe-web-execution` (perturbing counter-reset coverage, no self-scope), `observe-javascript-runtime` + `reconcile-javascript-runtime` held end-to-end; `capture-electron-scenario` typed refusal (`cleanup_incomplete`); node `--inspect` targets need a real file | live CDP (:9222 chromium) + V8-inspector (:9229 node) probes |
-| EVM | `2026-10-13-r3-evm-interface` | held — EVMole selectors recovered from synthetic dispatcher; positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc` | held — EVMole selectors recovered from synthetic dispatcher (r3-07) and real solc-compiled runtime (arc3-r1); positional encoding quirk |
 | Host anomaly triage | `2026-10-13-r2-jq-shadow-verdict`, `2026-10-13-r3-jq-provenance` | resolved — byte-identical upstream + provenance traced to kimi swarm bootstrap 2026-10-03 |
 | Synthesized carriers | `2026-10-13-r3-keyed-archive-carriers` | held — keyed-archive/interface-builder/dylib-trace all work on Linux synths; recipes recorded |
 | Evidence model | `2026-10-13-r2-evidence-bundle-schema` | held — snapshot envelope vs inner bundle schema, content-addressed ev_ ids |
```

`map-token.alt-prose.patch` sha256 `87108a29c8fb9433781b0cc1eb38fad76383f9cd5ec6411f5ad828ac21f2bd70`;
applied result `README.alt-prose.md` sha256 `508688f7…`. Same line, same line
count, token set 81 → 82; it repairs the row's state cell, which otherwise still
describes only the synthetic leg (the arc2 precedent left state cells lagging
r6/r7, so the token-only primary is precedent-faithful). If this alternate is
landed, EX-12's carried Hunk B must be dropped (different bytes, same line).

## 4. Stem — resolved by the landed entry

The token is counted by command A's map regex `2026-10-\d{2}-[a-z0-9-]+` over
the `## Coverage map` section and matched against `corpus/knowledge/*.md` stems.
The token must equal the landed entry's stem.

- **Authoritative stem: `2026-10-19-arc3-r1-evm-real-solc`** — EX-12's landed
  artifact `claims/c1/EX-12/knowledge-entry.patch.md` creates
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` and carries the
  matching token; RV-4's frozen artifact, `seats/SC-3.md:89` and the EX-14
  records drafts (`claims/c1/records-drafts/LOG-entry-draft.md:49,130`,
  `SCORECARD-section-draft.md:38,96,105`) all carry the same name.
- **Superseded: `2026-10-19-arc3-r1-evm-solc`** — the name PL-1's plan froze
  (`claims/c1/PL-1/plan.md:273,292,364`) before EX-12 landed. Measured failure
  mode if that name were used with EX-12's entry: command A reads
  `mapped 81, dangling ["2026-10-19-arc3-r1-evm-solc"],
  missing ["2026-10-19-arc3-r1-evm-real-solc"]` — both directions fail loudly,
  but the claim's `missing []` / `dangling []` would not hold (transcript
  variant `v3`).

Coupling (measured): token landed with the entry → `knowledge_files 82,
mapped 82, missing [], dangling [], 13/13`; token without any entry →
`dangling ["<stem>"]`.

## 5. Verification battery (raw output in `verification.txt`)

Before-state byte-copy of the real README; patched commits live in a scratch
bare clone; nothing in the repo was written.

| check | v1 primary (token-only) | v2 alternate (prose) | v3 plan-name stem (attack) |
|---|---|---|---|
| token-insert identity on line 38 | True | True | True |
| line-neutrality 190 → 190; only line 38 differs; other 189 lines byte-identical | True | True | True |
| map tokens: unique 81 → 82; added == {new token}; removed []; prior counts equal | True | True | True |
| `git apply --check` + apply → byte-identical result | exit 0 | exit 0 | exit 0 |
| citation-drift probe at the patched commit | findings=0 | findings=0 | findings=0 |
| command A, EX-12 entry landed | 82/82, missing [], dangling [], 13/13 | same | **mapped 81, dangling/missing non-empty** |
| command A, no entry landed | dangling `["…evm-real-solc"]` | same | dangling `["…evm-solc"]` |

`c1-census-v10.py` is unaffected by construction: its SCOPE table names only
`PROVINCE.md`, `SKILL.md`, `SCORECARD.md` (`.ufo/gates/c1-census-v10.py:86-108`);
`corpus/README.md` is not a census file.

## 6. Attacks run, with verdicts

- **Row insert (counterfactual, refused by the task)**: inserting a new map row
  after line 38 still yields 82 unique tokens — the count cannot see the harm —
  but the citation-drift probe reads **5 `citation_dead` findings**
  (`sc69-readme-177`, `sc72-readme-nitrow`, `readme175-sc1217`,
  `readme175-r7range`, `readme175-r8e2`), because `corpus/README.md:22` and
  `:175` are pinned citing lines in
  `.ufo/gates/citation-drift/pointer-table.json`. Verdict: the same-line form is
  load-bearing; a row insert is refused.
- **Duplicate token**: appending an already-present token leaves unique tokens
  at 81 (silent no-op). Verdict: the appended stem must be genuinely new.
- **Underscore stem**: `2026-10-19-arc3_r1_evm` is extracted by the regex as
  `2026-10-19-arc3` (truncated at `_`) → dangling, loud. Verdict: hyphenated
  stems are load-bearing; failure is visible, not silent.
- **Stem mismatch** (plan name vs landed entry): measured, §4. Verdict: the
  authoritative stem is the landed filename, not the plan's sketch.
- **Side-harm**: probe findings=0 on every patched variant (same as the
  unpatched control run in the same scratch clone); census v10 scope excludes
  README. Verdict: no measured harm to the other chains' instruments.

## 7. Apply recipe (parent, at the records commit)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
git apply --check .ufo/waves/arc3-loop1-round1/claims/c1/EX-13/map-token.primary.patch
git apply         .ufo/waves/arc3-loop1-round1/claims/c1/EX-13/map-token.primary.patch
sha256sum corpus/README.md   # expect b74b8d34abe47525c92b81f57829f8bd838a62fcc879ea4641277b4986944467
```

Then measure command A (`SCORECARD.md:92-124` recipe) at the records commit:
expect `knowledge_files 82, mapped 82, missing [], dangling []`,
`citation_resolved_rules 13, rule_blocks 13`. The hunk context is anchored at
`index 7bcc4af`; if README moved before landing, regenerate from
`README.primary.md` rather than forcing the hunk.
