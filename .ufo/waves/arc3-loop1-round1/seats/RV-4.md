# SEAT RV-4 | CHAIN c1 | ROLE reviewer

Task (seat line): verify `map-token.patch.md` is truly line-neutral on a /tmp copy:
apply, count README lines before/after (must be equal), confirm token set 81→82 and
prior 81 tokens byte-identical. Verdict in seat report.

**VERDICT: PASS** (final artifact state, 07:16 local) — the delivered
`claims/c1/EX-13/map-token.patch.md` (sha256 `27d59a11…`) carries two machine-applicable
hunks, both verified by this seat on scratch copies:
**primary** (embedded block = `map-token.primary.patch`, sha256
`ddfe01165fdbb2fefa9a802b99f454bb574dddb926e5b807018571f78fc29cad`) is line-neutral
(190 → 190), Coverage-map token set 81 → 82 unique, prior 81 tokens byte-identical
(set and occurrence order), applied result `b74b8d34…`; **alternate** (embedded block =
`map-token.alt-prose.patch`, sha256 `87108a29…`) is line-neutral with the same token-set
result (`b74b8d34`-class, result `508688f7…`) and additionally edits the row's state
prose by design. The primary bytes are exactly the artifact this seat froze and
verified earlier (`claims/c1/RV-4/map-token.frozen.patch`, `README.after.md`); EX-13's
own final `verification.txt` designates them `v1` and confirms the same numbers. The
token stem is resolved to `2026-10-19-arc3-r1-evm-real-solc` (EX-12's landed entry).
Two defects found during the churn are recorded below (§1, §4): an earlier revision of
the doc (sha256 `b9a8b3b0…`) carried non-applying embedded blocks (context corruption),
and a stem divergence (`evm-solc` vs `evm-real-solc`) was live until EX-12 landed.

## 1. Work performed

- Captured the before-state at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`:
  `corpus/README.md` 190 lines, sha256
  `7c0cf67143eebc57a949c54884712262954d2ed984cd66eea8aab44362cb2568`; 81
  `corpus/knowledge/*.md` files (dir listing = 82 entries incl. `.gitkeep`, which
  command A does not count — it filters `.md`). Evidence: `claims/c1/RV-4/README.before.md`
  (byte-copy, same sha256).
- Independently extracted the Coverage-map token set with the recipe's own regex and
  section boundary (`SCORECARD.md:92-124`): 83 token occurrences, 81 unique; mapped 81,
  missing [], dangling []. Baseline corroborated by EX-11's independent run
  (`claims/c1/EX-11/command-A-before.txt` — identical JSON).
- Built and self-tested a verification harness: `claims/c1/RV-4/verify_map_token.py`.
  Self-tests: synthetic positive (token appended to one row line) → PASS
  (`selftest-positive.out`); synthetic negative (new row line inserted) → FAIL on
  `line_neutral: False` (190 → 191) (`selftest-negative.out`). Two harness defects were
  found and fixed during self-test before any real artifact was judged: (a) relative
  patch path broke `git apply` (false FAIL); (b) zero-context hunks need
  `git apply --unidiff-zero` (false FAIL on a valid patch).
- Located and verified the producer artifact: `claims/c1/EX-13/_scratch/map-token.patch`
  — 2073 bytes, mtime `2026-10-19 07:06:01 -0300` (= 10:06:01Z), sha256
  `ddfe01165fdbb2fefa9a802b99f454bb574dddb926e5b807018571f78fc29cad`. A byte copy is
  committed at `claims/c1/RV-4/map-token.frozen.patch` (same sha256).
- Applied the artifact to a scratch copy (git repo seeded with the before-state README
  only, on tmpfs — see §5 for the /tmp substitution) with `git apply` — clean apply,
  exit 0. Full harness output: `claims/c1/RV-4/frozen-verification.out`; applied file:
  `claims/c1/RV-4/README.after.md` (sha256 `b74b8d34…`); unified diff of the change:
  `claims/c1/RV-4/frozen-readme.diff`.
- Cross-checked against the producer's own scratch: `README.after.md` is byte-identical
  (sha256 `b74b8d34…`) to EX-13's `_scratch/README.patched` and to the README blob at
  EX-13's scratch commit `295cd30a` (`git --git-dir=…/_scratch/repo.git show
  295cd30a:corpus/README.md | sha256sum`). The artifact diff and a locally regenerated
  diff differ only in the path prefix (`a/b/` vs the local `i/w/` config) — content
  hunks identical.
- Ran a command-A preview over EX-13's scratch repo via `GIT_DIR` at two revisions
  (`claims/c1/RV-4/command-A-preview.txt`): `e845c2b` → 81/81, missing [], dangling [],
  13/13; `295cd30a` (patch only, no knowledge entry) → mapped 81, dangling
  `["2026-10-19-arc3-r1-evm-real-solc"]`, 13/13.
- Cross-checked the producer's variant matrix and own verification
  (`claims/c1/EX-13/verification.txt`, updated 07:10–07:11 local): its h3 row (result
  `b74b8d34…`, token `evm-real-solc`) matches this seat's measurement number-for-number;
  h1/h2 are alternates (`evm-solc`) not delivered. Independently reproduced the
  entry-coupling (V6): scratch clone at `295cd30a` + stub entry with the matching stem
  → command A 82/82, missing [], dangling [], 13/13
  (`claims/c1/RV-4/v6-coupling-reproduction.txt`, scratch commit `a516bafb…`).
- Final-artifact verification (post-churn, 07:16 local): extracted both fenced diff
  blocks from the delivered `map-token.patch.md` (sha256 `27d59a11…`) and ran the full
  harness on each. Block 1 (primary) is byte-identical to `map-token.primary.patch`
  (= the frozen `ddfe0116…`) → applies clean, 190→190, tokens 81→82, prior 81
  byte-identical, result `b74b8d34…`, VERDICT PASS (`frozen-verification.out` covers
  the same bytes). Block 2 is byte-identical to `map-token.alt-prose.patch`
  (`87108a29…`) → applies clean, 190→190, tokens 81→82, prior 81 byte-identical,
  result `508688f7…`; its one changed line also updates the state prose (documented
  alternate), so the strict token-append-only check is False by design for this variant
  (`ALT` run output in `claims/c1/RV-4/alt-prose-verification.out`).
- Churn defect recorded: an earlier revision of `map-token.patch.md`
  (sha256 `b9a8b3b0…`, 07:12 local) embedded two hunks whose context line for
  `corpus/README.md:37` read `… no self-scope); …` while the repo line reads
  `… no self-scope), …` (byte diff at col 197; both fenced blocks fail
  `git apply`/`patch` against HEAD's README). The same revision's companion machine
  copies `map-token.h1.patch`/`map-token.h2.patch` carried a different corruption in
  the same context line (`end-to-end,` vs repo `end-to-end;`). Both were replaced at
  07:13 by `map-token.primary.patch`/`map-token.alt-prose.patch`, whose context lines
  match the repo exactly (verified byte-for-byte) and which apply cleanly.
- Write surface: only `seats/RV-4.md` (this file) and `claims/c1/RV-4/*`. No git
  mutations, no LOG/SCORECARD/SKILL/corpus edits. Scratch under `/dev/shm/rv4-scratch`
  (see §5); no repo pollution.

## 2. Proposed changes

none (reviewer seat; no patch-text artifacts — the artifact under review is EX-13's,
and it is already in proposed-patch form at the path in §1).

## 3. Before→after measurement (chain c1 claim — map-token line-neutrality)

Artifact under test: `claims/c1/EX-13/_scratch/map-token.patch` (sha256 `ddfe0116…`),
applied with `git apply` to a scratch copy of
`corpus/README.md@e845c2b5` (sha256 `7c0cf671…`). Command:
`python3 verify_map_token.py map-token.frozen.patch README.before.md work-frozen`
(full output `frozen-verification.out`):

| check | before | after | required | verdict |
|---|---|---|---|---|
| README line count | 190 | 190 | equal | PASS |
| Coverage-map unique tokens | 81 | 82 | 81 → 82 | PASS |
| token occurrences | 83 | 84 | +1 | PASS |
| prior 81 tokens byte-identical (set) | — | — | yes | PASS |
| prior token occurrence order identical | — | — | yes | PASS |
| removed/changed prior tokens | — | none | none | PASS |
| insertion text on the one changed line | — | `, \`2026-10-19-arc3-r1-evm-real-solc\`` | token only | PASS |
| files touched by patch | — | `corpus/README.md` only | one file | PASS |
| README sha256 | `7c0cf671…` | `b74b8d34…` | — | — |

- New token: `2026-10-19-arc3-r1-evm-real-solc` (matches the recipe regex
  `2026-10-\d{2}-[a-z0-9-]+`; whole-file multiset gained exactly this one occurrence —
  no duplicate insertion elsewhere in README).
- Diff shape: one hunk, one line changed (line 38, the EVM row); common prefix+suffix
  cover the entire old line, so the only byte difference in the whole file is the
  inserted `, \`2026-10-19-arc3-r1-evm-real-solc\``.
- Command-A preview at EX-13's patch-only commit `295cd30a`: `mapped 81, dangling
  ["2026-10-19-arc3-r1-evm-real-solc"], 13/13` — i.e. for the claim's (e) step (82/82,
  missing [], dangling []) the records commit must also land
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` with exactly that stem; at
  report time that file is absent (checked 10:08Z). Rules 13/13 hold at the patch-only
  commit (SKILL.md untouched).
- Naming caveat: the artifact as-found is named `map-token.patch`, not
  `map-token.patch.md`, and lives under `claims/c1/EX-13/_scratch/`. This verdict binds
  the bytes with sha256 `ddfe0116…`; a later re-delivery under another name must match
  those bytes (or be re-verified).
- Variant matrix + producer cross-check (EX-13 was still iterating at 07:10 local):
  EX-13's scratch holds three candidate variants and their own
  `claims/c1/EX-13/verification.txt` covers all three (07:10 and 07:11 updates):
  h1 (`evm-solc` token, state-cell prose changed, result `ec1d53f4…`), h2 (`evm-solc`,
  prose unchanged, result `b206e597…`), **h3 (`evm-real-solc`, prose unchanged, result
  `b74b8d34…`)**. In the 07:11 revision EX-13 designates h3's **patch sha256 as
  `ddfe01165fdbb2fefa9a802b99f454bb574dddb926e5b807018571f78fc29cad`** — byte-for-byte
  the artifact this seat verified — and lands the applied result in its claims dir as
  `claims/c1/EX-13/README.rv4-frozen.md` (sha256 `b74b8d34…`). The h1/h2 variants are
  consolidated as `claims/c1/EX-13/map-token.h1.patch` / `map-token.h2.patch`
  (sha256 `30edcc65…` / `69f13257…`), both `evm-solc`, not delivered. EX-13's own h3
  row independently reports: line-neutral 190→190, tokens 81→82 (+`evm-real-solc`),
  pipes 4→4, apply byte-identical, command A 82/82 with the entry landed (V6) and
  `dangling [token]` without it (V7) — consistent with every number in this seat's
  measurement.
- Name reconciliation (integration constraint): the token stem must equal the landed
  knowledge-entry stem. Current wave state: delivered artifact + SC-3's records drafts
  (`claims/c1/records-drafts/*.md`) + CN-1/CN-2 cross-consistency
  (`claims/cross/consistency.md:162`) all use `2026-10-19-arc3-r1-evm-real-solc`;
  PL-1's plan (`seats/PL-1.md:51`, `plan.md`) used the older `…-evm-solc` name and is
  stale. The parent must land `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`
  (not `…-evm-solc.md`) for command A to read 82/82.
- Independent V6 coupling reproduction (this seat): scratch clone of EX-13's repo at
  `295cd30a` + stub `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`, committed
  (`a516bafb…`) → command A: `knowledge_files 82, mapped 82, missing [], dangling [],
  13/13` (`claims/c1/RV-4/v6-coupling-reproduction.txt`). The coupling is reproduced,
  not just cited.
- Final-state verification of the delivered doc (`map-token.patch.md`, sha256
  `27d59a11…`, both fenced blocks extracted and run through the harness; summary
  `claims/c1/RV-4/final-artifact-verification.txt`):

  | artifact (as delivered) | apply | lines | tokens | prior 81 | result sha256 | verdict |
  |---|---|---|---|---|---|---|
  | primary block = `map-token.primary.patch` (`ddfe0116…`) | clean | 190→190 | 81→82 | identical | `b74b8d34…` | PASS (full) |
  | alternate block = `map-token.alt-prose.patch` (`87108a29…`) | clean | 190→190 | 81→82 | identical | `508688f7…` | PASS on the three required checks; also edits row prose by design (append-only strengthening False by design) |
  | earlier doc revision (`b9a8b3b0…`, 07:12) | FAILS to apply | — | — | — | — | artifact defect, replaced at 07:13 |

- Stem resolution (final): EX-12's landed entry patch
  (`claims/c1/EX-12/knowledge-entry.patch.md`) creates
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`; EX-13's final doc §4 declares
  that stem authoritative and the plan's `…-evm-solc` superseded (its `v3` transcript
  measures the failure mode: token `evm-solc` + real-solc entry → `mapped 81, dangling
  ["…-evm-solc"], missing ["…-evm-real-solc"]`). The frozen/primary bytes carry the
  authoritative stem, so the claim's `missing []`/`dangling []` end-state is reachable
  with the delivered primary patch + EX-12's entry.
- EX-12's carried map hunk ("Hunk B", inside `claims/c1/EX-12/knowledge-entry.patch.md`,
  file sha256 `d662c195…`): extracted (1917 B, hunk sha256 `312a1344…`) and verified —
  applies cleanly, line-neutral 190→190, tokens 81→82, prior 81 byte-identical,
  append-only, result `b74b8d34…` (`claims/c1/RV-4/ex12-hunkB-verification.out`).
  Its six hunk content lines are byte-identical to this seat's frozen patch; only the
  `@@` header suffix differs (cosmetic). So three carriers of the token change
  (EX-13 primary, EX-12 Hunk B, RV-4 frozen copy) all resolve to the same result bytes —
  the parent must land exactly one of them.

## 4. Attacks/refutations attempted

- Harness self-test (positive + negative synthetic cases): found 2 harness bugs before
  any real verdict was issued (relative path; zero-context hunk) — both fixed, then
  re-run clean. Verdict: harness validated, not merely written.
- Row-insert alternative: EX-13's scratch also holds `README.rowinsert` (191 lines,
  adds a new `EVM (real bytecode)` row). If that shape had been delivered as the
  artifact, it would FAIL the claim's line-neutrality requirement (190 → 191). The
  delivered `map-token.patch` is the append variant; verdict: PASS on the delivered
  shape, and the alternative correctly excluded.
- Extraction-format attacks: harness run on fenced diff, raw diff, and with a
  `patch -p1` fallback path (TMPDIR redirected around the host /tmp quota failure);
  all three reproduce the same after-bytes (`b74b8d34…`). Verdict: extraction
  robust to the artifact's wrapper format.
- Double-insertion attack: occurrence delta measured +1 and whole-file multiset delta
  exactly +1 (new token appears once). Verdict: no double append.
- Whitespace/format attack: the inserted text is `, \`token\`` — no pipes added, no
  trailing whitespace introduced (common prefix+suffix check); the row remains a valid
  table row. Verdict: PASS.
- Cross-source identity: applied bytes equal EX-13's `README.patched` and commit
  `295cd30a` blob; my baseline equals EX-11's independent command-A run. Verdict: no
  drift between producer's scratch, committed scratch blob, and my application.
- Token-name churn attack: three candidate tokens were live in the wave
  (`…-evm-solc` in h1/h2 + PL-1's plan; `…-evm-real-solc` in the delivered artifact,
  the records drafts and CN-1/CN-2). The delivered bytes carry `evm-real-solc`; the
  drafts that the parent will apply use the same stem. Verdict: no mismatch in the
  delivered/draft path; the stale `evm-solc` plan name is the integration hazard and
  is named in §3/§5.
- Coupling attack (V6/V7): reproduced the entry-absent dangling state at the patch-only
  commit and the entry-present 82/82 state with a matching-stem stub — verdict: the
  claim's 82/82 is reachable only with the exact stem, and reachable with it.
- Embedded-block context attack (found a real defect): the delivered-doc revision
  `b9a8b3b0…` (07:12) embedded hunks whose context line for `corpus/README.md:37`
  contained `… no self-scope); …` while the repo line has `… no self-scope), …`
  (byte diff at col 197) — both blocks fail `git apply`/`patch` against HEAD's README,
  i.e. the doc's own apply recipe would not have worked from the embedded text alone.
  Its companion machine copies at that moment (`map-token.h1.patch`/`h2.patch`) had a
  different single-character corruption in the same line (`end-to-end,` vs repo
  `end-to-end;`). Both were replaced at 07:13 by `map-token.primary.patch` /
  `map-token.alt-prose.patch`, whose context lines match the repo byte-for-byte and
  which apply cleanly. Verdict: defect real and caught by review; fixed in the final
  revision (`27d59a11…`) whose embedded blocks are byte-identical to the machine
  patches and apply cleanly. Lesson for the integrator: apply the machine `.patch`
  files (recipe §7 of the doc), and if copying embedded text, re-check with
  `git apply --check` first.
- Observation (judgment item for the integrator, NOT a line-neutrality failure): the
  EVM row's state prose is unchanged — it still reads "held — EVMole selectors
  recovered from synthetic dispatcher; positional encoding quirk", while the new token
  points at the real-solc entry. Precedent rows (r6 mid-rung / r7 wall, `corpus/README.md`
  PE rows) updated the row prose when appending tokens. The frozen claim only requires
  the line-neutral token, so this does not fail the claim; flagging for the parent's
  records commit whether the row prose should be refreshed there. (EX-13's h1 variant
  did change the prose; h2/h3 — including the delivered h3 — did not.)

## 5. Blockers

- Host `/tmp` is unusable for scratch: tmpfs + usrquota exhausted — even 1-byte writes
  fail with `Disk quota exceeded` (EDQUOT); `df` shows 3.1G "available" but every write
  fails. Independently observed by EX-02 (`claims/c1/EX-02` report section on /tmp
  failure). Substitution used: `/dev/shm/rv4-scratch` (tmpfs, writable), harness and
  all intermediates run there; `TMPDIR` redirected for the `patch` fallback. This is a
  deviation from the "scratch under /tmp" rule, caused by the host condition, recorded
  here rather than silently.
- The claim's end-state (command A 82/82, dangling []) is not reachable from the patch
  alone: `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` must land in the same
  records commit (§3 preview shows dangling otherwise). Not this seat's write target.
- Artifact-name timeline: the artifact my seat line names (`map-token.patch.md`) did not
  exist at capture time — I verified its eventual primary bytes first as
  `claims/c1/EX-13/_scratch/map-token.patch` (sha256 `ddfe0116…`) and re-verified them
  after they landed as `map-token.patch.md` §2's embedded block and
  `map-token.primary.patch`. All three are byte-identical; the verdict binds those
  bytes. The producer revised the artifact set several times between 07:06 and 07:13
  local (h1/h2/h3 → primary/alt-prose; doc revision `b9a8b3b0…` → `27d59a11…`); the
  final set is self-consistent and verified. If the parent applies the recommended
  primary hunk, expect `corpus/README.md` sha256 `b74b8d34…` after the apply.
- The claim's (e) step remains unverifiable until the records commit exists: command A
  at 82/82 requires `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` in the same
  tree as the patched README (reproduced in §3; EX-13's V6 row measured it with EX-12's
  landed entry patch). The stem divergence that could have broken this is resolved:
  EX-12's entry patch uses the same stem as the primary token. One integration hazard
  remains: EX-12's `knowledge-entry.patch.md` carries the map-token hunk as well
  ("Hunk B") — the parent must land the token **once**, not twice (a second application
  would not apply cleanly at the same line, and a duplicated token elsewhere would not
  add to the unique count but is still wrong).
