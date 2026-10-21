# Fixture08 — source-review of `refused_parent` in R23 counter fixtures (R23-C1 only)

Seat: KaidokuR23.Fixture08 (leaf reviewer, read-only). Candidate source `2838351450ff1ee4baa620c962a1153450d53311`, baseline B `aa1450b82f9ede35aada63efe8a34e01c6e02f72`. All bytes read via `git show <rev>:PATH`; suite NOT executed (out of scope for this seat). `refused_parent` only; sibling cases reviewed solely where they share the mutation chain.

Frozen inputs verified at candidate (observed, `git show … | sha256sum`):
- `expected-v2.json` → `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f` (== `SELFTEST_MANIFEST_SHA256`, `count-c1.py:21`)
- `fixture.json` → `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b` (== pin, `expected-v2.json` inputs)
- `counter-fixtures.py` → `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f` (== pin, same inputs)
- Legacy counter pinned in-wrapper: `LEGACY_SHA256 c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` == observed `git show aa1450b8…:.ufo/waves/round-22/tools/count-c1.py | sha256sum` (observed).

## Findings

### Verdict — the case DOES distinguish the stated fault at candidate source
Observed chain (code-read, not executed):
1. Fixture mutation is exactly parent-flag erasure's inverse: `counter-fixtures.py:50-51` sets `envelope['ok'] = False` on the single `inspect-signal-decoders` synthetic envelope (selected at `:38`). `data.normalized_result` stays clean (`fixture.json` shows only `control` prose), so `r21.refused()` on any node is FALSE — `refused()` checks `error/errors/code/status/completion_status/exit_code` and recurses only through `raw_result`/`normalized_result` (`.ufo/waves/round-21/tools/verb-coverage.py:39-56`), never the `ok` key. The parent `ok` predicate is therefore the SOLE code reachable that classifies this envelope as refused.
2. Reaching the binder requires the whole pipeline live: S058 row eligibility (counter-fixtures.py:78-84; all 13 cells correct: idx4 `A`, idx8 `mined`, idx9 `2026-10-21`, idx11 = entry path), knowledge entry citing path+id, `cited_pattern` match (`count-c1.py:106`), `HEX64` match of `ev_555…5` (r20 `HEX64 = (?<![A-Za-z0-9_])ev_[0-9a-fA-F]{64}(?![A-Za-z0-9_])`, r20:36 — matches), `eid in blob` (`count-c1.py:123`).
3. A counter mutant that skips the parent check counts the envelope: `data = {evidence_id, operation, normalized_result}`; `bind_cli` record walk (r22 counter) finds nothing refused; `r21.bind` → `records()` yields the record unblocked → `evidence_bound` → 0 → verb held → `t1_exercised_count=2`, `finding=c1_complete`, exit 0 ≠ expected {1,1,c1_incomplete} (`expected-v2.json` refused_parent). Case fails on the fault it names.
4. Positive preserved (observed): mutations are in one `if/elif` chain keyed on `name` (`:50-62`) inside the per-case loop; `copy.deepcopy(fixture['documents'])` at `:37`; no shared mutable state across cases.
5. Expected values correct (inference from pinned code, flagged as not executed): with the parent check honored, `bind_new` returns 1 at `count-c1.py:51`; witness list for `inspect-signal-decoders` stays empty; the only other held verb is the pinned historical `identify-flutter-build` (`count-c1.py:82` requires `historical['t1_exercised'] == ['identify-flutter-build']`, else exit 2), so `t1_exercised_count=1` → exit 1 (`:166`), `finding='c1_incomplete'` (`:129`). This matches the frozen `{exit:1, count:1, finding:c1_incomplete}` exactly. Wrong expectation found: none.

### F1 — MEDIUM, weak mutation: `ok: False` does not kill `ok is not True` → `ok is False` mutants
Observed: the only exercised value is Python `False` (`counter-fixtures.py:51`). Inferred: a mutant collapsing `count-c1.py:51` to `node['ok'] is False` (or `== False`) passes `refused_parent` while misclassifying truthy-falsy parents. Escape shapes the frozen fixture never exercises: `"ok": null` → `None`, `"ok": 0`, `"ok": "false"` — all "not True", all currently rejected at :51, all would pass an `is False` mutant and be counted as held evidence. Also kills only one direction: `ok is not True` vs `ok is not True`-with-type-strictness variants are indistinguishable. The positive case uses `"ok": true` (`fixture.json`), so it cannot cover the gap either. No manifest case has `ok: null|0|"false"`. Smallest correction: add a case `parent_ok_null` (`envelope['ok'] = None`) expecting `{exit:1, count:1, finding:c1_incomplete}`, or mutate via `envelope['ok'] = 0`. This is a mutation-strength gap, not a wrong expectation.

### F2 — LOW, the case is not standalone-discriminating: expected `count:1` is also produced by total pipeline failure
Observed: every rejection path collapses to "verb not held" (bind_new 1 or 2 both fail the `== 0` test at `count-c1.py:123`), and the runner (`counter-fixtures.py:64-68`) compares only exit/`t1_exercised_count`/`finding` from the counter's JSON. Inferred: any mutant that makes the new witness non-countable (broken id match, broken citation regex, ineligible source row) leaves `refused_parent` passing with count 1 — indistinguishable from correct refusal handling by this case alone. The companion `positive` case (count 2, same id/path/entry, only `ok` differing) is what makes the suite discriminative; without it this case is vacuous. This mirrors W1's N10 ("every refusal reason collapses to 1"), re-evaluated here: still true at candidate; refusal-vs-unbound remains unauditable from case outcomes. Not a defect in expected values; a structural sensitivity limit of the case.

### F3 — LOW, falsifier-phrase scope: "copy erases parent refusal" cross-file variant not covered by this case
Observed: `refused_parent` mutates the only envelope; there is no second, clean copy of the same `evidence_id` anywhere in the fixture tree, so the "copy survives while the parent refusal is erased" reading (W1 F1/N5 wording) is not what this case exercises — it exercises "refusal flag not honored". Inferred from the per-file loop (`count-c1.py:123`, per cited path) and from r22 `bind_cli` being per-blob: an envelope with a refused parent in one file and a clean copy carrying the same `evidence_id` + matching meta in another cited file would still be counted (code 0 on the clean blob); no manifest case covers `duplicate_id_refused_cross_root`. The single-file refusal semantics ARE correctly distinguished (verdict above); the cross-file falsifier reading remains uncovered at candidate. Coverage gap, not a wrong expectation.

### Re-evaluation of stale W1 proposal findings against candidate (where they touch this case)
- W1 CriticSeparation F1 (`historical_root_injection`) and F2 (`inherited_lost`): addressed at candidate — pins `LEGACY_SHA256`/catalog/tree compare (`count-c1.py:22-27,58-61`) plus manifest cases `historical_root_injection`/`inherited_lost`/`catalog_changed` (all `unevaluable`). `refused_parent` no longer carries any historical-root burden: its count=1 baseline is pinned to the frozen B witness set, so the expectation cannot pass via historical/new confusion. Closed for this item.
- W1 N1 (`meta_ok_false`) / N2 (`sibling_refusal`): now covered by manifest cases `meta_false`, `meta_array`, `sibling_refusal` (mutations at counter-fixtures.py:58-62), each expected count 1. Closed for count-affecting part.
- W1 N8/N10 (refusal classification/audit tags): still uncovered; `refused_parent` continues to collapse "refused" into "not counted" (see F2). Remains open, severity unchanged (audit-visibility, no count risk).

### Oracle independence
Observed: `counter-fixtures.py` imports only stdlib (`copy/json/os/pathlib/subprocess/sys/tempfile`); no `count-c1`/helper/validator import; expectations come solely from the frozen manifest (`expected-v2.json` cases), digest-pinned by the counter's selftest and re-pinned above. The runner treats the counter as a subprocess (`python3 -I -B`, `--root/--rev` at a committed synthetic revision) and compares `{exit, count, finding}` — a behavioral, non-decision-derived check. One structural coupling noted (not a defect): the runner's `observed` keys (`t1_exercised_count`, `finding`) are the counter's own output contract, so a counter that renamed output fields while keeping behavior would fail all cases loudly — safe direction.

## Produced files
- `.ufo/waves/round-23/w2/Fixture08.md` (this report) — sha256 recorded at write time:
`sha256sum .ufo/waves/round-23/w2/Fixture08.md` (fill-in command for integrator; single file, no other writes)

## Installs
None. No tool installed or updated (read-only `git show`/`sha256sum`/`grep`/`sed -n` sufficed).

## Open risks
- All case-behavior statements are code-trace inferences from pinned bytes; the counting command itself was not executed by this seat (designated Run* seats only). Residual risk: a runtime divergence between pinned source and observed execution would not be visible here; the Run seat's captured output covers that.
- F1's escape shapes (`ok: null|0|"false"`) are inferred reachability, not executed mutants.
- F3's cross-file count-through-clean-copy is inferred from the per-blob binder loop; an executed variant would settle it definitively.
