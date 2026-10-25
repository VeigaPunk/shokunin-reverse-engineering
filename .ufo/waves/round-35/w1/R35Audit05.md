# R35Audit05 — w1 report (C1 trio check audit)

Seat: R35Audit05 (executor). Item: "Audit C1 trio check." Milestone: build evidence and first falsifications.
Read-only audit; no lane writes beyond this report. No scoring performed (data not yet landed).

## Scope & sources
- `plans/round-35-claims.md` (claim C1 wording, controls, kill rule)
- `.ufo/waves/round-35/claims-canonical.json` (predicates, instrument pins, supersessions, frozen inputs)
- `tools/round-35/c1-coverage-counter.py` (the instrument; trio checks at lines 101-141)
- `.ufo/waves/round-35/controls/c1-do-nothing.json` (pre-data control receipt)
- `.ufo/waves/round-35/w1-spec.json` (wave/seat spec)

## Evidence

### 1. Frozen bytes match canonical pins
|File|sha256 (worktree)|Canonical pin (claims-canonical.json)|Match|
|---|---|---|---|
|tools/round-35/c1-coverage-counter.py|e28792c7e54fcfa2185fe12f07c9e3eb328652d405e98d1ffaf2737b28d24220|e28792c7...d24220|yes|
|tools/round-35/c2-calibration-counter.py|576c14dd95c0a54b2de05b765d171b25429a893289b85516258e83daa9179b94|576c14dd...b9b94|yes|
|plans/round-35-claims.md|45b644a44851b8302dd0a3699e09220ca3b39aad8685ffeb3ae1b6aca9167138|45b644a4...9167138|yes|

Counter constant `PREDICATE` is byte-identical to the `predicate` string in `claims-canonical.json` and to the receipt `predicate` field (gate `PREDICATE not in json.dumps(claims_obj)` passed on real repo runs; synthetic claim with a different predicate exited 2 as designed). The plan document states the claim in prose, not the verbatim P35-c1 sentence; the byte-identity requirement is carried by claims JSON + counter constant + receipts.

### 2. Live runs (read-only git objects; receipts to /tmp)
|Run|Command|Exit|Result|
|---|---|---|---|
|Selftest|`python3 -I -B tools/round-35/c1-coverage-counter.py --selftest --root <LANE>`|0|`C1_SELFTEST: ok` green=0 red=1|
|Base control|`--rev aa04633a686d49756763b1feed4be6830d5bb479 --freeze 2323d197456f1328459d9420aff025cffbcb3e27`|1|exactly the 8 pre-data failures: entry_missing x2, registry_row_missing S125/S129, province_missing x2, readme_missing x2; `pass:false`|
|Current HEAD (3ecf4298)|same flags, `--rev HEAD`|1|identical 8 failures — C1 data has not landed yet (HEAD is "commit failing do-nothing controls before claim data")|

### 3. Falsification probes (synthetic git repos in private /tmp; each committed, counter run with `--freeze` = that commit)
Synthetic repos mirror the instrument's own green fixture (entries, SOURCES rows, PROVINCE, README, claims file with the real predicate).

|Probe|Mutation vs "opens with trio + cites row"|Counter exit|Observation|
|---|---|---|---|
|A|Trio present but buried mid-file (preamble/heading before `source:`/`verified-at:`/`recheck:`)|0 `C1_CLEAN`|Instrument checks presence anywhere, not opening position. Predicate wording "opens with the provenance trio" is not enforced.|
|B|Contract entry source line = `https://example.test/S1250-alpha` (substring S1250 contains "S125"); no genuine S125 citation|0 `C1_CLEAN`|`row_citation_missing` is a raw-substring `re.search(r"(?m)^source\s*:.*S125", body)`; any occurrence of "S125" on the source line passes, including as a prefix of another token.|
|C|Trio lines reordered (recheck before source before verified-at)|0 `C1_CLEAN`|No ordering/adjacency enforcement among the three keys.|
|D|recheck line removed from contract entry|1|`C1_FAIL: trio_missing_recheck:corpus/knowledge/...-mapper-contract.md` — negative direction works.|

### 4. Receipt `checks` map defect (confirmed, not just code-read)
Receipt generation maps six constant labels (`entry_exist`,`trio`,`row_citation`,`registry_rows`,`province`,`readme`) with `(f not in fails)`; actual fail strings (`entry_missing:...`, `trio_missing_...`, ...) never equal those labels, so every `c1_N` field is always `true` even when the corresponding invariant fails.
Observed in both live runs: `c1_0..c1_5` all true while `pass:false` and 8 failures listed. The `checks` map is therefore non-informative; consumers must rely on the `failing` array. This affects the C1 receipt only (label-vs-failstring mismatch), not exit-code correctness (exit 1/0/2 behave per spec).

### 5. Exit-code contract
Exit 0 iff clean; exit 1 with named failures; exit 2 for missing args / claims file absent at freeze / unparseable claims / predicate mismatch — all observed or code-confirmed (probe runs exited 2 until the real predicate was embedded, confirming the gate).

## Limits
- Lane read-only (git show/ls-tree only by the instrument); no worktree/REA/source fetch executes — matches the frozen control design.
- Audit covers the C1 trio/row-citation component and receipt integrity; C2, S125/S129 content provenance, and scoring are out of seat scope (sibling seats own those).
- No `find`/`du` under /fast/scratch; no background/delegated work; no VCS mutation; pacman untouched.

## Risks
- Lenient trio/citation checks (A/B/C) mean a non-conforming document can score C1 clean; if strict "opens with" semantics are intended, the counter predicate gate should be tightened before the measured revision is fixed (kill-rule freeze makes post-data changes impossible).
- The all-true `checks` map could mask a failing invariant in human review; rely on `failing`.

## Final answer
C1 trio instrument pins match canonical bytes; selftest green/red ok; base and HEAD both exit 1 with the 8 expected pre-data failures (data not yet landed).
Falsifications found: (A) trio presence anywhere passes — "opens with" not enforced; (B) substring citation (S1250) passes; (C) trio order not enforced; (D) genuine absence fails correctly.
Receipt `checks` map is all-true by construction (label vs fail-string mismatch) and non-informative; `failing` array is the reliable channel.
Recommend tightening checks to opening position and exact token citation if strict semantics are intended; otherwise document leniency.
No lane writes beyond this report; no scoring performed.
