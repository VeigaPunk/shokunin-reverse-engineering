# SentinelScope — round-67 w1 findings (trust boundaries on the committed bytes)

Range audited: `a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92` → `3663e6b21dccf4c4957f459301156664d8b151d6` (11 added, 2 modified,
0 deleted, +2129/−0 lines). Full evidence log: `.ufo/waves/round-67/w1/SentinelScope/audit.md`.

**Bottom line.** The write scope is clean, no vendor bytes and no credential material are committed, all seven pinned
instruments match their recorded sha256, both gap rules parse, and both do-nothing controls reproduce byte-for-byte (C1:
9/9 fields; C2: 5/5 fields plus identical mutant hashes). Eight items need action or recording; two are material (F1, F2).

---

## F1 — MEDIUM — frozen atom A5 and the counter docstring assert `removed` is unchanged; `removed.silent` was deleted

**Files.** `tools/round-67/gap-rule-v2.json:32-38` (the `removed` object now has only `diagnostic`, `kinds`,
`disposition`); `tools/round-67/avm-le-counter.py:21-22` ("`allowed`/`removed`/`structural` are unchanged");
`.ufo/waves/round-67/claims.json:39` (A5: "keeps allowed/removed/structural from the round-50 rule").
Round-50 reference: `tools/round-50/gap-rule.json` carried `removed.silent = {"char-device": ["247:0"]}`.

**Evidence.** `diff -u tools/round-50/gap-rule.json tools/round-67/gap-rule-v2.json` shows the `silent` sub-object removed
(the only `removed` change). The field is load-bearing in the pinned engine, not dead config:
`tools/round-50/c1-counter.py:1550-1568` reads `removed.get('silent')` and admits matching rows with no record. The deletion
is observable in the counter's own output: `.ufo/waves/round-67/l1/pre/control-dryrun.json` reports
`"1 silent"` under the round-50 rule and `"0 silent"` under rule v2 for `c6490` and `c6430` (both reproduced by me:
`--control` exit 0, identical 9/9 fields). The silent entry was the Cable carriers' `dev/led` (`247:0`) — verified in
`tools/round-50/oracle/c6490.nonregular.tsv`.

**Exploit / impact.** No false green: the deletion *narrows* the rule (a silently-deleted char-device row no longer counts
as disposed), and `required.char-device=false` makes the loss inert on these four carriers — the reproduced
`gaps_ok_round50 2` / `gaps_ok_round67 4` still holds. The defect is provenance: a frozen atom (A5) and the instrument's own
docstring state a property the bytes contradict, in a round whose routed defect (1) is precisely "a record cites something
that does not exist". A later reader auditing A5 against the rule gets a false statement; a gate that trusts atoms inherits
it.

**Smallest remediation.** Do not rewrite the frozen rule (it would break pin `e66ba022…` and the freeze). Record the delta
explicitly in the landing prose: "`removed.silent` was dropped; inert because `required.char-device` is false; the control
notes show 1 silent → 0 silent on the two Cable carriers", and correct the A5 sentence in the round record/lessons. If the
round requires atoms to be literally true, that is a re-freeze decision above this seat.

---

## F2 — MEDIUM-LOW — `--score` accepts any `--gap-rule` and never checks the rule digest, though the contract promises a drift refusal

**Files.** `tools/round-67/avm-le-counter.py:185` (`rule = Path(args.gap_rule).resolve() if args.gap_rule else repo / RULE_V2`),
`:188` (`rule_digest = sha256_file(rule)` — computed, then only written into the receipt), `:342` (`--gap-rule` option).
The docstring at `:51` says exit 2 for a "drifted/absent engine **or rule**"; `claims.json` R67-C1 `kill_rule` says "a
drifted engine/rule/carrier table … → not verified". The engine is pinned (`load_engine`, `ENGINE_PIN`); the rule is only
checked for existence. `RULE_V2` (`e66ba022…`) is a path constant, not a digest assertion.

**Exploit path.** A hand-run that deviates from the declared command:
`python3 -I -B tools/round-67/avm-le-counter.py --score … --gap-rule /path/to/waive-all.json`.
`control()` proves a permissive rule defeats the only symlink guard — the committed receipt's own red fixture reports
`junk_rule_would_pass: true` for a rule with `required.symlink=false`. With all other clauses green, `--score` would emit
`exit 0`, `met_target true`, and a `rule.sha256` field naming bytes that are not rule v2. Only a reader comparing that field
to `e66ba022…` catches it; the instrument does not.

**Impact.** Receipt-level false green under a rule the claim does not authorise. The declared harness (`c1-run.sh`) never
passes `--gap-rule` (verified: no occurrence in the 868 lines), and the claim's own command line omits it, so exploitation
requires stepping off the declared command — hence MEDIUM-LOW rather than MEDIUM.

**Smallest remediation.** Add `RULE_V2_PIN = "e66ba022…a4169e"` and, in `score()`, `if rule_digest != RULE_V2_PIN: raise
Unevaluable(...)` before measuring (exit 2). Keep `--gap-rule` only behind an explicit dev flag that the receipt records, or
drop the option. No behaviour change on the declared command.

---

## F3 — MEDIUM-LOW — R67-C1's second conjunct is not bound by `--score`

**Files.** `plans/round-67-claims.md:42-45`, `claims.json` R67-C1 predicate: "… while the four frozen envelopes scored under
the round-50 rule report gaps_ok on 2 of 4." `avm-le-counter.py` `score()` emits `schema, claim, rev, freeze, predicate,
counter, engine, rule, patches, failing, bindings_false, exit_code` over the engine's result — no round-50 control field, no
digest of `l1/pre/control-dryrun.json`, no re-run of `control()`.

**Evidence.** In my reproduction, `--control` is deterministic and cheap (exit 0, 9/9 fields identical, run in ~1 s from
committed envelopes via `git show`). `--score` does not invoke it.

**Impact.** The C1 verdict is a conjunction of two artifacts, but only one is produced by the scoring run. A stale or edited
control receipt would leave the score green while half the predicate is unevidenced at the record. (The committed control
receipt is correct today — I reproduced it.)

**Smallest remediation.** Record `control_receipt.sha256` (and `gaps_ok_round50`) inside the score receipt, or call
`control()` from `score()` and assert `gaps_ok_round50 == 2`.

---

## F4 — LOW — A0 cites an order-check receipt that does not exist at the freeze

**Files.** `.ufo/waves/round-67/claims.json:34` (A0: "… receipt l1/records/r67-order.txt").

**Evidence.** `git ls-tree -r 3663e6b | grep round-67/l1/records` → empty; `ls .ufo/waves/round-67/l1/` →
`census-start.txt  pre  scores`. The underlying property is true and I verified it directly:
`git merge-base --is-ancestor cf705c53 3663e6b` → 0 and `… 39a91a99 3663e6b` → 0 (carry-in → instruments → freeze).

**Impact.** A dangling evidence pointer in a frozen atom; the ordering itself is sound. Same defect class as the round's own
routed defect about `02d4880b`.

**Smallest remediation.** Have the L1 write `l1/records/r67-order.txt` before the record, or change A0 to cite the two
`is-ancestor` commands and their exit codes.

---

## F5 — LOW — "byte-identical" predicate claim is false as bytes

**Files.** `plans/round-67-claims.md:19,39,90`; `avm-le-counter.py:38`; `mutation-battery.py:31`.

**Evidence.** The plan stores each predicate as a `>` blockquote with hard wrapping (lines 42–45, 93–96), so `PREDICATE in
plan_text` is `False`. After stripping `^> ?` and reflowing whitespace, both match **exactly** (word-for-word), and
`claims.json` ↔ instruments ↔ receipts are byte-identical.

**Impact.** Precision only; no verdict risk.

**Smallest remediation.** Say "verbatim in words; blockquoted in the plan" — or store the predicate unwrapped in the plan.

---

## F6 — LOW — three stated exit-2 contracts are unimplemented (all fail conservative, exit 1)

1. `avm-le-counter.py:202-210`: `except Exception` re-raises any exception whose class name is not one of the four
   whitelisted engine names. An unexpected engine crash prints a traceback and exits 1 — the same code as "not verified"
   (docstring `:50-51` promises exit 2 for could-not-evaluate).
2. `mutation-battery.py:257` `control()` has no sha256 pin check and no guard around `read_text`; a drifted or absent r66
   instrument yields `FileNotFoundError` → exit 1 (docstring `:40` promises exit 2 for a drifted/absent pinned instrument).
   Note `--score` *does* check both pins (`:305-308`) — the control is the gap.
3. `mutation-battery.py:219` calls `fixture_repo(...)` outside any `try`; a fixture `git` failure raises
   `CalledProcessError` → exit 1 (docstring `:40` promises exit 2 for "fixture git failure").

**Impact.** Exit-code contracts are what the L1 keys on; a crash is reported as a falsification. No false green.

**Smallest remediation.** Wrap these paths and map to the documented code 2 (a small helper reused in both instruments).

---

## F7 — INFO — freeze-ledger row for round-67 is absent (expected at the freeze; must land before close)

`LOG.md` work item (4) says the ledger "gains the missing round-64 and round-66 rows **and this round's row**". The range adds
two rows only (`.ufo/waves/round-67/l1/pre/…` aside, `corpus/claim-freezes-v2.tsv:41-42`); `grep -c '^round-67'` → 0.
Absence at `3663e6b` is structural — the row must name freeze sha `3663e6b2…`, which only exists at that commit — so this is a
pending deliverable, not a defect. Also: the `round-64` row is appended **after** `round-65` (line 41 after 40), breaking the
ledger's numeric order.

---

## F8 — INFO — L1 data-run output appeared under `corpus/evidence/round-67/c1/` during this audit (untracked, out of range)

At 21:53 the directory was empty; by 21:56 it held
`c1/g7581/{after.json,run.json}`, `c1/g7582/…`, `c1/c6490/…` (mtimes 21:54:37 / 21:55:17 / 21:56:06), with `c6430` absent
at 21:56:21 and `.ufo/waves/round-67/l1/scores/c1-data-stage.json` at 21:57. `c6430/after.json` landed at 21:59, so all
four carriers are now on disk. `git status` shows the whole tree as `??` (untracked); `git ls-tree 3663e6b` has **no** blob
under `corpus/evidence/round-67/`.

This is the L1's declared post-freeze data run, not a seat overrun, and it is **not** part of the audited bytes; it is
recorded here so the audit's "no vendor bytes at the freeze" statement is not misread as "the directory is empty". The
receipts are REA envelopes (2.1–2.2 MB JSON), not vendor bytes; they must not be committed (the carriers are AVM-licensed),
consistent with A6.

---

## Cleared by this audit (positive results)

- **Scope:** all 13 changed paths lane-relative, inside the declared write scope, no `..`, no absolute path, no deletion, no
  rename; `git ls-files` delta +11 equals the 11 additions.
- **No vendor bytes:** zero blobs under `corpus/evidence/round-67/` at the freeze; `corpus/evidence/` count 3645 → 3645;
  `carriers.json` untouched and hash-only.
- **No secrets:** 0 matches across 2129 added lines for key/token/cookie/password/secret/`op://`/bearer/AKIA patterns; no
  host `/tmp` path; the 9 `/fast/scratch` mentions are the documented scratch base (constants and usage text).
- **Pins:** 7/7 claims-map digests equal the actual files, including the harness `00be5a87…` and both r66 instruments.
- **Structure:** both Python instruments compile, the harness passes `bash -n`, the rule parses with zero backslashes (hence
  no escaped pipe), and the engine's parser reports no problems for rule v2, the round-50 rule, or the junk control rule.
- **Claim substance:** both controls reproduce exactly (C1 9/9 fields; C2 5/5 + identical mutant hashes `5e84208a…`,
  `2b98a7f7…` and 30/26-case summaries); the char-device census 13/13/1/1 and the exact device names match the counter
  docstring and the committed oracle tables; ordering ancestors both exit 0.
- **Disclosed narrowing:** dropping `carrier_fresh_ok` is stated in the docstring and receipt (`patches.dropped_clauses`) and
  is justified by the re-freeze; no undisclosed clause change.

## Limits

`--score` was not run (needs the carrier cache, `--pkg65` rea-agents 6.5.0, a full REA extraction, and documentation
bindings that do not exist until the prose lands); carrier pins were verified as hashes, not by re-hashing vendor bytes; the
device census was verified against the committed round-50 oracle tables, not re-derived from the carriers. Nothing was
installed or upgraded; scratch was removed before yield.
