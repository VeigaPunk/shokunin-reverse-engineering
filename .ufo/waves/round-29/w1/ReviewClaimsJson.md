# ReviewClaimsJson — round-29 claims.json vs frozen inputs

Scope: verify every count and statement in `.ufo/waves/round-29/claims.json` at `dbd87cfa09eb89306c4e07d3171a4556eb732024` against the committed inputs and `.ufo/waves/round-29/before/` receipts. Read-only; no lane files modified. All commands run 2026-10-22 UTC in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Working-tree `claims.json` sha256 `76bc0d8f…cf79` equals `git show dbd87cfa:.ufo/waves/round-29/claims.json` — reviewed bytes are the frozen bytes.

## Verdicts

### Top-level fields
- `"round": "round-29"`, `"base": "bacbe9cc…"` — supported (observation: `git log`, base is the parent).
- `frozen_by` ("before any R29-C1 REA run, any R29-C1 lookup and any R29-C2 fetch") — supported (observation): `git ls-tree dbd87cfa` under `corpus/evidence/round-29/` contains only `carriers.tsv`, `heldout.tsv`, `src/`, `compiled/`, `selectors.tsv`, `canonical-signatures.json`; no `tally.json`, `runs.tsv`, `db/`, envelopes or responses.
- `freeze_kind` (same commit holds counters+selftests, inputs, producers, receipts; counters refuse pre-commit data) — supported (observation): `git show --name-only dbd87cfa` = 69 files = claims.json + 4 inputs + 32 compiled files + 16 sources + 7 tools + 9 before receipts. Refusal logic observed at `c1-fresh-naming.py:184,193,244,248` (`utc_start not after counter commit`, `first committed before the counter`); red cases pass in selftest receipts. Note: two extra receipts (`preseen-c1-flag.txt`, `select-heldout.txt`) are in the commit beyond the ones claims.json cites — consistent, not contradictory.

### screens_before_freeze
- `hex` — supported (observation): `before/hex-screen-c1.txt` prints `carriers=16 fail=0`, exit 0, command matches text. All 16 `*.runtime.hex` are non-empty, pure even-length hex (regex check), no `library` keyword in any `src/*.sol` (`grep -rln library` → none), and `carriers.tsv` runtime/abi sha256 columns match the committed files (16 match, 0 mismatch). QUALITY row 43 exists and matches the cited semantics.
- `preseen_c1_name` — supported (observation): receipt prints `test_selectors=152 seen_set=58720 overlap=0`, exit 0. `name_seen` (`preseen.py:33-45`) is `git grep -I -h -o -i -w -E "(0x)?[0-9a-f]{8}"` over the whole tree at the base — supports the statement's "present as a word in any lane file at the base" for selector tokens.
- `preseen_c2_flag` — supported (observation): receipt `test_selectors=178 seen_set=230 overlap=0`, exit 0. `flag_seen` (`preseen.py:48-82`) covers both `openchain-<sel>.json` paths and `result.function.<0xsel>` keys in tracked JSON.
- `selection_exclusions` (26 of 178 dropped: 19 prior + 7 name_seen; 10 canonical keys dropped with openchain responses) — supported (observation): `before/select-heldout.txt` lists exactly 19 `prior-round-test-set` + 7 `name_seen` EXCLUDE lines and `CANONICAL_FLAG_SEEN` with exactly 10 keys; JSON summary `abi_selectors:178, excluded:26, c1_heldout:152, canonical_keys:36, canonical_unseen:26, c2_selectors:178, c1_heldout_that_are_canonical:0`. Spot-check at base: `openchain-*.json` files exist at `bacbe9cc` for the 10 flag-seen keys (e.g. `round-25/.../openchain-dd62ed3e.json`), confirming "already have an openchain response in the lane".

### instruments / loaded_by_counter / producers_not_counters
- All 12 sha256 pins match the working-tree files exactly (observation, `sha256sum` on each). Map completeness matches the counters' `PINS` dicts: c1 = resolver + carriers.tsv + heldout.tsv (`c1-fresh-naming.py:67-71`), c2 = selectors.tsv + canonical-signatures.json (`c2-filtered-unseen.py:61-64`).

### pre_freeze_probe
- "none; no REA call, no 4byte/openchain request" — supported (observation: no run/lookup/response files in the freeze commit; `utc: null` consistent). The named pre-freeze opens (canonical list, two Sourcify files, ERC-4626 text) match SOURCES rows S087 (handlers.ts + canonical-signatures.json at `0966a3bc`) and S088 (erc-4626.md). Negative claim (nothing else opened) is a lane attestation — cannot be falsified from committed bytes; verdict: not contradicted.

### R29-C1
- "16 carriers … compiled this round by make-carriers.py with solcjs 0.8.37" — supported (observation): 16 `src/*.sol` + 16 compiled pairs committed in the freeze commit; all 16 runtime hexes carry solc metadata trailer `64736f6c6343 000825 0033` = 0.8.37; `make-carriers.py` uses standard-JSON `solcjs` with `optimizer.enabled: False` (`:131`) matching the limits' "no optimizer".
- "hex-screened 16/16 before this freeze" — supported (receipt above).
- "152 distinct selectors among them in heldout.tsv" — supported (observation): heldout.tsv = 152 data rows, 152 distinct first-column selectors. Caveat (clarity, not a defect): "among them" reads post-exclusion — 178 distinct ABI selectors exist across the carriers; 26 were dropped by the disclosed exclusions, leaving 152. Also carrier `n09` (Weth9) contributes 0 heldout rows (its only 2 selectors `d0e30db0`, `2e1a7d4d` were excluded as prior/name_seen) — the statement does not require each carrier to contribute.
- "none in round 25's 43 or round 28's 187" — supported (observation): recomputed r25 in-sample set via the pinned resolver over `round-25/a2/c2/carriers.tsv` ABIs at base = 43; `round-28/c1/heldout.tsv` = 187 rows; intersection with the 152 = ∅ for both.
- "none present as a word in any lane file at the base" — supported (receipt `overlap=0` over `seen_set=58720`).
- "one REA 6.5.0 inspect-evm-interface call per carrier and one saved 4byte.directory and openchain lookup set per selector" — supported (observation): `collect-c1.py` `runs`/`lookups` subcommands implement exactly that; counter `ARGV`/`PKG_VERSION`/`RUNS_HEADER` and per-selector db checks (`:218-249`) match.
- "knowledge entry … cites S088 … new since base, opened 2026-10-22, status mined, listed in ## Gate" — supported as a well-formed requirement (observation): counter `CLAIM["row"]="S088"` and check `:348-350` enforce it; S088 is absent in base SOURCES (`git show bacbe9cc:SOURCES.md`), present in working tree with 11 columns, status `mined`, opened `2026-10-22`, and `S088` ∈ Gate ids of `corpus/lessons/round-29.md`.
- `primary_rule` unchanged from round 28 — supported (observation: rule name and rule table `:74-80` carry the same `openchain_sole_unfiltered_args_consistent` semantics; `scoring_unit` matches `heldout.tsv` column 3 = carrier).
- `before` block — supported (observation): `before/c1-at-bacbe9cc.txt` prints `PIN pinned input absent: corpus/evidence/round-29/c1/carriers.tsv`, `exit=2`; all numeric fields 0, `why` matches.
- `target` — internally consistent with `TARGET={"runs":16,"rows":152}`.
- `kind` (round-28 test used lane's own carriers/lane-invented names, missed one carrier on unscreened input = M28-1) — supported (observation: `corpus/lessons/round-28.md` M28-1 row names the h09 placeholder refusal).
- `limits` — consistent (one compiler/pin/snapshot; Weth9 covered above; screen-removes-written-down-only caveat matches `name_seen` design).

### R29-C2
- "178 selectors … 26 canonical-list keys with no openchain response in the lane at the base, and the 152 R29-C1 held-out selectors, none of them a canonical key" — supported (observation): selectors.tsv = 26 `canonical` + 152 `c1` rows; `c1` column equals heldout.tsv selector set exactly; heldout ∩ canonical keys = ∅; the 26 canonical rows equal exactly the 36 canonical-signatures.json keys minus the 10 `CANONICAL_FLAG_SEEN` keys.
- "one openchain filter=false response fetched after this freeze" — supported (observation): `collect-c2.py:34` URL is `…lookup?function=0x%s&filter=false`, one file per selector into `c2/db/` with manifest.
- "filtered is true exactly when the selector is a key of the pinned canonical-signatures.json and the name differs from that key's signature (a key with no signature: every candidate)" — supported as the instrumented rule (observation: counter logic + S087 Gate anchor `:47-48` `signatureItem.filtered = signatureItem.name !== expectedCanonical.signature`; canonical-signatures.json has 36 keys, of which the 5 `system:magic` keys carry no `signature` field — "a key with no signature" is real in the pinned list).
- "mismatches 0, both branches present" — target form, consistent with `separation` analysis (see below).
- "entry … cites S087 …" — supported like C1: `CLAIM["row"]="S087"`, check `:143-144`; S087 new since base, `mined`, `2026-10-22`, in Gate.
- `before` block — supported (observation): `before/c2-at-bacbe9cc.txt` `PIN pinned input absent: …/c2/selectors.tsv`, exit 2.
- `separation` (hasVerifiedContract / mark-all-but-first / different-list alternatives; same-on-these-26 not separated) — supported (observation: honest dual of M28-5's defect, which required naming a concrete separated alternative; the c1 set's all-false prediction and the 26 keyed rows give both branches a falsification surface).
- `kind` (S084 at master `189cd726`; S087 at staging `0966a3bc`, identical bytes) — supported (observation): SOURCES rows record handlers.ts sha256 `30981efb…` at both commits and canonical-signatures `5572beb5…` (the pinned file's own sha256 matches S085/S087's recorded hash); round-28 re-observation criticism = M28-4, present in `corpus/lessons/round-28.md:50`.

### not_claimed
- "six routed defects of corpus/lessons/round-28-verifier-spotcheck.md" — supported (observation): the file's `## Routed defects` section lists exactly items 1–6; QUALITY rows 45–47 map to defects 6, 5, 1.
- "Calibration is not claimed" — self-consistent; nothing in targets implies it.

## Statement the inputs do not support
None found. Every count (16, 152, 178 = 26+152, 26 = 19+7, 10 of 36, 22 and 19 selftest cases, 43 and 187 prior sets) matches the committed inputs or receipts.

## Residual notes (non-blocking)
1. `c1-fresh-naming.py` docstring (`:14`) says "corpus/evidence/round-28/c1/carriers.tsv" while `EVDIR` and the code use round-29 — cosmetic docstring slip in a frozen instrument, not a claims-file defect.
2. C1's "152 distinct selectors among them" counts post-exclusion selectors (178 ABI selectors exist); the parenthetical discloses the screen, so it is accurate but compresses a step.
3. `pre_freeze_probe` is an attestation of absence; nothing in committed bytes contradicts it, and the receipts it does cite (S087/S088 opens at 19:52Z/20:00Z) precede the freeze CommitDate 20:03:06Z while all counter-input receipts (20:01Z) sit between them — timing is coherent.
4. Minor timing observation: committed receipt `c2-selftest.txt` is stamped 20:01:33Z and CommitDate is 20:03:06Z — consistent; AuthorDate 19:30:33Z predates receipts, normal for amended commits.

## Commands / evidence
- `git show dbd87cfa:.ufo/waves/round-29/claims.json | sha256sum` → `76bc0d8f556019763157bbb74cd43b9983b9e7cf77ad9d92cae898365a60cf79` (= working tree).
- `sha256sum` of the 12 pinned paths — all equal to `instruments`/`loaded_by_counter`/`producers_not_counters` values (exit 0).
- `before/*.txt` receipts: c1 selftest `cases=22 failures=0`, c2 `cases=19 failures=0`; at-base receipts `PIN … absent`, `exit=2`.
- `before/select-heldout.txt`: 19 `prior-round-test-set` + 7 `name_seen` EXCLUDE; `CANONICAL_FLAG_SEEN` 10 keys; JSON `{carriers:16, abi_selectors:178, r25_in_sample:43, excluded:26, c1_heldout:152, canonical_keys:36, canonical_unseen:26, c2_selectors:178, c1_heldout_that_are_canonical:0}`.
- Recompute: r25 prior set = 43 (pinned resolver over base carriers ABIs); r28 heldout = 187; heldout∩prior = ∅; selectors.tsv sets = {canonical:26, c1:152} with c1 = heldout selectors and canonical = 36 keys − 10 flag-seen.
- Runtime hexes: all 16 pure hex, solc metadata 0.8.37; carriers.tsv sha columns verified; no `library` in `src/`.
- SOURCES: S087/S088 absent at `bacbe9cc`, present now (`status` col `mined`, `opened` `2026-10-22`); Gate section ids {S084, S085, S087, S088}.
- `corpus/lessons/round-28-verifier-spotcheck.md` `## Routed defects` = 6 items; M28-1/M28-4/M28-5 rows exist in `corpus/lessons/round-28.md`; `PROVINCE.md:91` holds the "EVM bytecode (extended)" Frontier bullet.

No tools installed. No scratch artifacts beyond `/tmp/c16`, `/tmp/hc` (throwaway sorts, not persisted).

Report: .ufo/waves/round-29/w1/ReviewClaimsJson.md
