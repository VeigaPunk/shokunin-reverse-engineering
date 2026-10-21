# Fixture04 — R23-C1 `mention_only` source review

Seat: `KaidokuR23.Fixture04` (leaf reviewer, source-only). Candidate `2838351450ff1ee4baa620c962a1153450d53311`; baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72` (= `fixture.json` `base` = `count-c1.py` `BASELINE`). All candidate bytes were read with `git show <candidate>:PATH`.

Labels: **observed** = bytes or command output I produced; **peer-observed** = another seat's report, cited and not reproduced; **inferred** = static trace of the exact lines cited; **unknown** = not established.

The suite was NOT executed by this seat. No mutant was executed; mutant results are inferred from source.

## Verdict

1. **Expectation is correct.** `frozen/expected-v2.json:23-27` gives `mention_only = {exit 1, count 1, finding c1_incomplete}`. Count 1 is the frozen baseline (`claims.json` `before` = 1: the inherited identify witness). It is a literal template: no decision import, no counter output used to build it. The same tuple appears in `expected.json` and `expected-v1.json`, and the frozen directory and `tools/counter-fixtures.py` were last changed in `2b40aec`. No late oracle edit.
2. **Fixture branch is correct and minimal.** `counter-fixtures.py:43-44` sets `selected = []`, so no envelope and no citation path is written. `:73-74` appends one bare mention plus a HEX64-shaped fake id to an otherwise eligible S058 entry.
3. **It does distinguish the falsifier's no-evidence form** ("verb named, nothing cited"). Mutants M1-M2 below would count and fail the case.
4. **It does not distinguish three live or uncovered variants**: (a) a verb token in the `source:`/`recheck:` header, in a negation, or in a cited filename, alongside a genuinely bound envelope. The candidate still counts these (`count-c1.py:119-124`) and no case covers them. (b) A cited path that is absent from the tree. (c) Which verb supplies the count (the oracle compares only exit/count/finding).

## Findings

### F1 — observed: pinned inputs match the candidate; fixture base equals baseline

- `expected-v2.json` sha256 `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f` = `count-c1.py:25` `SELFTEST_MANIFEST_SHA256` (candidate blobs).
- `counter-fixtures.py` sha256 `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f`, pinned in `expected-v2.json` `inputs`.
- `fixture.json` sha256 `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b`, pinned in `expected-v2.json` `inputs`.
- Legacy R22 `count-c1.py` sha256 `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` = `count-c1.py:23` `LEGACY_SHA256`.
- Helper pins: `round-20/tools/verb-coverage.py` `cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f`; `round-21/tools/verb-coverage.py` `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b`. Both equal the R22 `HELPER_SHA256` constants.
- `fixture.json` `base` = `aa1450b82f9ede35aada63efe8a34e01c6e02f72` = `count-c1.py:26` `BASELINE`. For `mention_only`, `documents` is deep-copied (`counter-fixtures.py:37`) but never read: `for verb in selected` (`:48`) iterates an empty list. Only `base` matters.
- `git show aa1450b:corpus/SOURCES.md | grep -c S058` = 0. The inserted S058 row (`counter-fixtures.py:83-84`) is therefore unique in the disposable clone. The `\n## Paths` anchor exists at base line 65.

### F2 — inferred from exact lines: mention_only reaches eligibility but never reaches the mention gate

- `counter-fixtures.py:47` header `source: S058 …`; `:83` row with 13 cells: `S058 | A | mined | 2026-10-21 | used-by = ENTRY`.
- `count-c1.py:101-110`: first line starts with `source:`; `:105` finds `S058`; `:107` predicate holds (58 ≥ 58, tier A, `mined`, `2026-10-21`, ENTRY in used-by), so the entry is eligible.
- `:111` `ids = [ev_aaaa…]`: HEX64 matches via the `ev_` prefix (`r20 verb-coverage.py:36`).
- `:112` `cited_pattern.findall(text)` is empty: the text contains no `.ufo/waves/round-23/evidence/c1/` string. The loop body `:113-124` never runs.
- So the only witness-producing gate, the mention check at `:119-121`, is never reached. `targets[verb]['new']` stays empty. `held` (`:127`) is the inherited identify only. Result: count 1, exit 1 (`main`), `c1_incomplete` (`:129`). Matches the expectation.
- **Non-vacuity caveat (inferred):** count 1 is also what an ineligible or broken entry yields. mention_only proves "mention ignored" only jointly with `positive` (count 2) and `all_six` (count 6), which together prove the shared S058 template is eligible.
- Peer-observed: `w2/RunSelftest.md:24-27` (positive 1/2, all_six 0/6, mention_only 1/1/c1_incomplete at candidate; 21/21 clean).

### F3 — observed (scratch git probe) + peer-observed: no git failure on the empty evidence directory

- mention_only creates an empty `.ufo/waves/round-23/evidence/c1/` (`counter-fixtures.py:45-46`) and includes it in `git add` (`:100-102`).
- Probe, git 2.56.0, scratch repo inside my ignored runtime dir (not a suite run): `git add -- <new file> <modified tracked file> <empty untracked dir>/ <tracked dir>` → exit 0, stage shows `A` new file and `M` tracked file. `git add -- <empty dir>/` alone → exit 0, no output.
- `w2/RunSelftest.md:77-80` (F6, peer-observed) reports mention_only passing with no evidence file under git 2.56.0. Consistent. Other git versions unchecked.
- Conclusion: no defect; the case cannot abort the selftest through this path.

### F4 — inferred from exact lines: the mention gate is full-text and location-blind (live at candidate; not covered)

- `count-c1.py:119-121` tests `r20.command_pattern(verb).search(text)` on the whole entry, including the `source:` header, `recheck:` header, any negation text, and cited filenames. `:122-124` then binds the envelope by its own `meta.command` and appends the witness.
- Consequence: an eligible entry whose only verb token is in `recheck: inspect-signal-decoders`, or in a negation ("NOT exercised; ignore inspect-signal-decoders"), or in a cited filename, and which cites a genuinely bound `inspect-signal-decoders` envelope, is counted. This matches CriticVacuity §4 F1-F4 (`w1/CriticVacuity.md:33-42`), measured at `a3c92eb` (its line 4-5). Re-evaluated: **still live at candidate**.
- Not covered by mention_only (no envelope there). No other fixture case has the verb only outside a body line (`counter-fixtures.py:70` puts the verb in the body with its path).
- Classification: consistent with the R22 policy text (the entry must "name the verb"), so this is a policy-level gap, not a binding defect. L1 decision.

### F5 — inferred: count-only oracle cannot attribute the count to a verb

- `counter-fixtures.py:111-112` compares `exit`, `count`, `finding` only. The `stdout` of each case is retained (`:114`) but not compared.
- Compound mutant M7 (drop the inherited identify witness and count an inspect mention) yields count 1 and passes mention_only. `positive` (count 2) catches it. Peer-observed: `w2/RunSelftest.md:66-70` (F4) reports the same oracle limit.

### F6 — inferred: no case covers a verb mention with a cited but absent path

- `count-c1.py:113-118`: a cited `.json` path is read with `git show rev:path` at `:118`. For an absent path, the `git()` helper (`count-c1.py:29-33`) raises `ValueError('git_input_unreadable')` → `main` exit 2, `unevaluable` (inferred). No fixture cites an absent path: `counter-fixtures.py:65-69` always writes the cited envelope, and mention_only cites none.

### F7 — W1 proposal findings re-evaluated against the candidate (stale → status)

| Item | Source | Status at candidate (exact lines) |
|---|---|---|
| CriticVacuity §4 F5: prose mention, no envelope → k=0 | `w1/CriticVacuity.md:34` | **holds**; this is mention_only (`count-c1.py:112` empty, `:119` unreached) |
| CriticVacuity §4 F1-F4: header/negation/recheck/filename mention + bound envelope counted | `w1/CriticVacuity.md:35-42` | **still live** (`count-c1.py:119-124`); uncovered by any case (F4 above) |
| CounterRefusals N16: eligible entry other than the binder supplies linkage | `w1/CounterRefusals.md:243` | **resolved**: witness records `entry` in the same loop that checks eligibility and path (`:107-110`, `:124`) |
| CounterRefusals N17: hyphen-only, case-sensitive token | `w1/CounterRefusals.md:244` | **resolved**: gate uses `r20.command_pattern` (`:120`) |
| ConnectCounters: mention growth never counted as k; mention-only labelled separately | `w1/ConnectCounters.md:138-140, 195-199` | **consistent**: mentions feed only `catalog_mentioned_count` (`:100`, `:131`), not `held` (`:127`) |
| CriticScopeFinal: a mention alone adds only to `catalog_mentioned_count` | `w2/CriticScopeFinal.md:33` | **consistent** |
| Fixture18: absolute-citation not-counted coherent with mention_only | `w2/Fixture18.md:64-66` | **consistent** |
| RunSelftest F4: oracle compares only exit/count/finding | `w2/RunSelftest.md:66-70` | **live** (F5 above) |
| RunSelftest F6: mention_only passes with no evidence file under git 2.56.0 | `w2/RunSelftest.md:77-80` | **consistent** with F3 probe |

### F8 — mutation strength of mention_only (static inference; no mutant executed)

| ID | Mutant (counter behaviour) | mention_only result | Covered by |
|---|---|---|---|
| M1 | bare verb mention in an eligible entry counts | count 2 → **fails** | mention_only |
| M2 | verb mention + HEX64 id in an eligible entry counts (no path) | count 2 → **fails** | mention_only |
| M3 | verb named in any knowledge entry feeds `held` (catalog `mentioned` used for k) | count ≠ 1 whenever another entry names an unheld T1 verb (not computed) → fails | mention_only and other cases |
| M4 | mention + id present in the R23 tree, uncited, counts | fabricated id not in tree → **passes** | only `absolute_citation` (count 2 vs expected 1), indirectly |
| M5 | mention + cited absent `.json` path counts (missing-blob read skipped) | no path → **passes** | **none (gap)** |
| M6 | header/negation/recheck/filename token + bound envelope counts (= current candidate, F4) | no envelope → **passes** | **none (gap; policy)** |
| M7 | compound: drop inherited identify, count inspect mention | count 1 → **passes** | `positive` (count 1 vs 2), indirectly |
| M8 | mention in an ineligible entry (no S-row linkage) without path counts | not exercised by mention_only | `missing_source`/`wrong_usedby` carry paths, so M8 yields count 2 there, indirectly |

## Wrong expectations and weak mutations (summary)

- **Wrong expectation: none found** for `mention_only`.
- **Weak mutations / power gaps:**
  - Count-only oracle (F5): cannot attribute the count to a verb; M7 passes mention_only.
  - Fabricated id (M4): an id-existence-gated mutant passes mention_only; only `absolute_citation` catches it.
  - No phantom-citation case (M5, F6).
  - No header/negation/recheck/filename case (M6, F4).
  - Non-vacuity depends on the shared template being proven by `positive`/`all_six` (F2).

## Positive preservation

- Candidate positive path traced: `counter-fixtures.py:70` puts the verb, the `ev_` id and the path on one body line. `r21 verb-coverage.py:21` `ID` matches `ev_5555…`. `r21:58-74` `records` yields the data record. `:85` operation `inspect_signal_decoders` equals `verb.replace('-','_')`. `:99` returns `evidence_bound`. `count-c1.py:122-124` appends the witness → count 2. Peer-observed: `w2/RunSelftest.md:24` (positive 1/2).
- mention_only does not alter positive state: each case resets (`counter-fixtures.py:35-36`).
- Constraint on any future fix: a body-only mention rule (verb outside header, negation and cited path) would preserve `positive` (the verb token at `:70` is a body token) and leave mention_only unchanged. No existing case would catch its regression (M6).

## Produced files and hashes

- `.ufo/waves/round-23/w2/Fixture04.md` (this report). Its sha256 is computed after writing and is given in the final message, not embedded.
- Ignored runtime copies, `.ufo/waves/round-23/runtime/KaidokuR23.Fixture04/blobs/` (candidate `git show` bytes):
  - `count-c1.py` `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`
  - `counter-fixtures.py` `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f`
  - `r20-verb-coverage.py` `cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f`
  - `r21-verb-coverage.py` `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b`
  - `catalog.json` (round-20 `verb-coverage.json`) `7c0d57d748720dcdaa69c2e481c62893b7185c663564a9f3e793dae0574fc515`
- Scratch git probe repository: removed.

## Installs

None. Used the installed git 2.56.0. No pacman, no tool installs, no config edits.

## Open risks and disclosures

- The suite was not run by this seat. Suite-level evidence is only the peer observation in `w2/RunSelftest.md` (21/21 at the same candidate). Not reproduced here.
- One `git status --short --ignored` ran in the lane root (read-only intent). Git may refresh the `.git/index` stat cache; this is the same caveat `RunSelftest.md` F7 raised. No tracked content, ref or stage was changed by me. Index bytes were not compared.
- The git probe ran a one-off `git add` semantics check in my ignored runtime directory, not in the lane.
- Git 2.56.0 only; other versions unchecked.
- Remediation options (none applied; L1 decision). Any new case or oracle field changes `counter-fixtures.py` or `expected-v2.json`, which changes pinned hashes. Re-pinning `SELFTEST_MANIFEST_SHA256` and the `inputs` table would be required, so this cannot be patched in place:
  - (a) assert the `t1_exercised` list in expectations (closes F5);
  - (b) a phantom-citation case (inferred expectation: exit 2, `unevaluable`, from `count-c1.py:118`);
  - (c) header/negation/recheck mention cases with a bound envelope, plus a policy decision on whether such mentions count (F4/M6);
  - (d) an id-existence variant to pin M4 directly.
- Adjacent, outside this item and peer-reported: `count-c1.py` itself is not in `expected-v2.json` `inputs` (`RunSelftest.md` F2).
