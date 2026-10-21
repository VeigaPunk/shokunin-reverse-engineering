# CriticQuality — QUALITY26 binding representation vs REA `--full-output` data wrapper

Seat: KaidokuR22R.CriticQuality-6 (author-side critic; not outside admission). Lane read-only; all mutations were in a temporary clone `/tmp/critic-quality-PHyl` (removed). No REA/provider call, no target execution, no install. Judged at lane HEAD `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`, baseline `7787fea4d6fd718726de92ed20759d11ce7b8b48`.

## Verdict

**R22-C1's single exercised verb is counted from a derived, author-extracted carrier. The binding authority (QUALITY #26 / r21 `bind`) can't read REA's own `--full-output` envelope.** The counted witness is `identify-godot.evidence.json`. It is the `data` member copied out of the producer envelope. The counter never checks it against the producer bytes, and the extraction step discards the envelope-level `ok`/`error`/`meta.command`. So QUALITY #26's rule that "typed refusal/error envelopes do not count" can be bypassed by extraction (counterexample X2). This is a fixable defect, not a tradeoff.

The retained artifact itself is honest. The extraction is disclosed, and it currently equals the producer stdout's `data` (checked below). The defect is that the counter doesn't *enforce* that equality. C2 is consistent with the REA wrapper; it reads the envelope directly.

Impacted axes: **calibration** (the counter admits records whose producer refused) and **coverage** (genuine REA output can never count, so held coverage depends on an unverified copy step).

## Observed evidence (exact lines)

- `.ufo/waves/round-21/tools/verb-coverage.py:72` — `records()` descends only `('evidence', 'evidences', 'records', 'result')`. REA 6.5.0 `--full-output` emits `{"ok","data":{record},"meta":{"command",...}}` (see `.ufo/waves/round-22/evidence/c1/identify-godot.envelope.json`), so `data` is never visited.
- `verb-coverage.py:39-56` — `refused()` inspects `error`/`errors`/`code`/`status`/`completion_status`/`exit_code`. It never inspects envelope `ok`, so `ok:false` without an `error` member wouldn't be treated as a refusal even if `data` were walked.
- `corpus/QUALITY.md:36` (#26) — "Unsupported representations are unevaluable, not guessed." The REA producer's own representation is exactly such an unsupported representation.
- `.ufo/waves/round-22/tools/count-c1.py:66-72` — a witness is any cited file under `evidence/c1/` for which `bind(...)[1] == 0`. There is no check that this file matches the producer's run record (`*-run.json` `stdout`) or the envelope's `ok`/`meta.command`.
- `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md:1,11` — `source:` S053 cites the derived `.evidence.json`. Line 11 states the data member "was extracted without changing members … for the existing R21 record-binding representation". The disclosure is honest, but it is not machine-enforced.
- `.ufo/waves/round-22/tools/counter-fixtures.py:39-54` (C1 fixtures, line 46) — every C1 fixture is a bare `{evidence_id, operation}` record. No case uses the REA envelope, and none uses a derived record whose producer envelope refused. The selftest is therefore blind to both directions of this defect.
- `.ufo/waves/round-22/tools/count-c2.py:102-121` — C2 reads the same producer shape directly (`env["meta"]["command"]`, `env["data"]`). The lane therefore has **two authorities for one REA output shape**: C2 binds to the envelope, while C1 can bind only to a stripped copy.

## Commands and observed exits

All commands ran from the lane root unless noted.

1. `python3 -I -B .ufo/waves/round-21/tools/verb-coverage.py --evidence .ufo/waves/round-22/evidence/c1/<f> --verb identify-flutter-build --evidence-id ev_3458b996…866b`
   - `identify-godot.envelope.json` → exit **2**, `unsupported_evidence_representation`
   - `identify-godot.evidence.json` → exit **0**, `evidence_bound`
   - `identify-godot-run.json` → exit **2**, `unsupported_evidence_representation`
2. `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root . --rev HEAD` → exit **1**. `t1_exercised=['identify-flutter-build']` (1/6), `catalog_zero_count` 19. Its `bound_evidence` is `[[ev_3458…, …/identify-godot.evidence.json]]` and its `unsupported_candidates` are `[…/identify-godot-run.json, …/identify-godot.envelope.json]`.
3. `count-c1.py --rev 7787fea4…` → exit **1**, 0/6, zero 20 (matches `before_expected`).
4. `count-c2.py --root . --rev HEAD` → exit **0**, accounted 14/14, mismatched `[]`, foreign `[]`.
5. Derivation check: `json.loads(run["stdout"])["data"] == evidence.json` → **True**, and `stdout == envelope.json` → **True**. The run argv is `npx -y rea-agents@6.5.0 identify-flutter-build <apk> --format json --full-output`, exit 0.
6. C2 consistency: for all 15 `c2/*.json` receipts, `receipt == json.loads(run.stdout)` is **True**, and the argv verb equals the receipt name. The ADB runs retain `env_overrides {'REA_ADB_PATH': '/usr/bin/false'}`.
7. `count-c1.py --selftest` → exit **0**, `counter_controls_clean` (6/6 cases). The C1 cases never include an envelope (see fixtures above).

### Counterexamples (temp files and temp clone only)

These were run through `bind` via the r21 CLI `--evidence` (synthetic files written in the temp directory):

| Case | Exit | Finding | Meaning |
|---|---|---|---|
| A: genuine REA envelope (copy) | 2 | unevaluable | genuine producer output cannot count |
| B: `{"ok":false,"error":{"code":"capability_unavailable"},"data":<same record>,"meta":…}` | 2 | unevaluable | the refusal is classified only as "unsupported", never seen as a refusal |
| C: `data` extracted from B | **0** | **evidence_bound** | **refusal erased by extraction and accepted** |
| D: extracted record with `normalized_result.flutter_detected` flipped to `true` | **0** | evidence_bound | no producer-byte cross-check |
| E: extracted from an envelope whose `meta.command` is `inspect-dart-aot` | **0** | evidence_bound | producer verb identity is lost |

Counter-level tests in the temp clone at `2ee3d9f`:

- **X1**: removed `identify-godot.evidence.json` and re-pointed the entry's citation to `identify-godot.envelope.json`. Result: `count-c1` exit 1, **count 0**, envelope listed under `unsupported_candidates`. The genuine REA record cannot hold the verb.
- **X2**: kept the derived `.evidence.json`, but rewrote the cited producer envelope to `ok:false` + `error.code=capability_unavailable`. Result: `count-c1` exit 1, **count still 1** for `identify-flutter-build`. This falsifies C1's falsifier "a typed refusal envelope counts" in its strong form: a refusal at the producer counts whenever an extracted copy is present.

## Smallest safe correction (for L1; not applied)

Make the binding authority read REA's own wrapper, and stop crediting derived copies:

```python
# .ufo/waves/round-22/tools/count-c1.py (or a round-22 successor of r21 bind; r21 file stays historical)
def refused(node):
    ...existing checks...
    if isinstance(node, dict) and 'meta' in node and 'ok' in node and node.get('ok') is not True:
        return True
    ...

# records(): add 'data' to the carrier tuple
for key in ('evidence', 'evidences', 'records', 'result', 'data'):
```

I probed this patch in memory against the lane's r21 module (no file written):

- genuine envelope A → `evidence_bound` exit 0;
- B (`ok:false` + error) → `evidence_refused` exit 1;
- `ok:false` without an `error` member → `evidence_refused` exit 1.

Accompanying edits:

1. Also require, for a wrapped record, that `meta.command == verb`. This closes case E.
2. Cite the envelope (S053 → `identify-godot.envelope.json`) and drop `identify-godot.evidence.json` from the witness set. Alternatively, have the counter credit a derived file only when its value equals `json.loads(<sibling>-run.json stdout)["data"]` and that envelope is not refused. This closes C and D.
3. Add three frozen C1 fixtures to `counter-fixtures.py`:
   - an REA envelope positive (expect count 6);
   - an `ok:false` envelope plus its extracted `data` (expect 0);
   - a tampered extraction (expect 0).
4. Supersede QUALITY #26 with a row stating that the REA CLI `{ok,data,meta}` envelope is a supported carrier, that `ok!==true` is a refusal for every enclosed record, and that extracted copies are not independent authority.

The measured count stays 1/6 under the corrected counter, because the genuine envelope binds. The claim isn't weakened; only its authority moves from the copy to the producer bytes.

## Addendum — coordinator interjection (2026-10-21 13:06 UTC)

I re-read the current lane at HEAD `2ee3d9f`, which is unchanged, along with the uncommitted working-tree edits to `tools/count-c1.py`, `tools/count-c2.py`, `corpus/SOURCES.md` (new S054) and the knowledge entry (S054 qualification). I repeated no REA probes.

- **Working-tree `count-c1.py`:** the edit restructures eligibility (`DEFAULT_TARGETS = ()`, `texts`/`eligible` set, per-verb `unsupported_candidates`). It doesn't touch `bind`, `records()` or the carrier keys. Re-run in a temp clone with the working-tree counter, SOURCES and knowledge bytes:
  - as-is → exit 1, count **1**, witness `identify-godot.evidence.json`, with the envelope and run record listed as unsupported;
  - **X2** (producer envelope rewritten to `ok:false` + `capability_unavailable`, derived copy kept) → exit 1, count **still 1**;
  - **X1** (derived copy removed, citation re-pointed to the envelope) → exit 1, count **0**;
  - `--selftest` → exit 0, `counter_controls_clean`.

  **The finding stands unchanged against the current bytes.**
- **Working-tree `count-c2.py`:** only the docstring and an unused-import change. The `probe == verb` linkage is already at HEAD, and the C2 results above still hold.
- **`verify/red-C1.json` and `red-C2.json`:** these are the frozen counters' fixture runs, retained as red receipts with exit 1 as intended. Their C1 cases are the same bare-record fixtures, so they don't cover the REA envelope either. The correction's fixture items still apply.
- **`verify/frida-unsupported-env.json`:** `REA_FRIDA_PYTHON=/usr/bin/false` → exit 0, `ok:true` device list, `finding: undocumented_override_did_not_disable_provider`, `control_pass: false`. This agrees with PROVINCE.md:191-193 (Frida "adjacent", the impossible-PID refusal is not provider absence). It is outside the wrapper scope and raises no finding here. Note that this receipt is still untracked, so a counter or verifier at a commit can't cite it until it's committed.

## Addendum 2 — source-only re-review of current `count-c1.py` (2026-10-21 13:29 UTC)

This addendum is from reading source only. Per the coordinator, I ran no checks and no tests. "Current" means the working-tree bytes of `.ufo/waves/round-22/tools/count-c1.py` and `counter-fixtures.py` as read at this time.

**The cause is fixed.** Each of my earlier counterexamples is now closed by the following source lines:

- **Envelope required:** `count-c1.py:60-61` requires the `ok` and `data` members. A bare derived copy (`identify-godot.evidence.json`), the `-run.json` record, and the extraction cases C, D and E all return 2 (unsupported). They can never be witnesses (`:138`).
- **Refused producer can't count:** `:62-63` returns 1 when `ok is not True` or `refused(envelope)`. This covers X2 and also the `ok:false`-without-`error` gap I had noted in `refused()`.
- **Producer verb pinned:** `:64-66` requires `meta.command == verb` and checks the meta for refusals. This closes case E.
- **Single direct record:** `:67-69` requires `data` to be one dict carrying `evidence_id` and `operation`.
- **Nested refusals:** `:70-77` walks the record and its `raw_result`/`normalized_result` chain for `ok` not equal to `true`. r21 `bind` (`:79`) then re-applies the round-21 `refused()` check to the record, so QUALITY #26's same-record rule is kept.
- **Strict decoding:** `:58-59` uses the strict decoder plus `allow_nan=False`, so duplicate members and overflowing numbers return 2.
- **Fixtures:** `counter-fixtures.py:52-54` makes the positive case a real `{ok,data,meta}` envelope. `:82-88` adds `extraction_only`, `refused_with_extraction`, `wrong_command`, `nested_refusal`, `record_refusal`, `normalized_refusal`, `overflow_metadata`, `meta_error` and `meta_exit`, which covers both directions of my original finding. I didn't run them.
- **Current lane under this source:** the knowledge entry cites `identify-godot.envelope.json` (entry line 11). That envelope satisfies every gate, so it should be the single witness, and the derived copy should appear only under `unsupported_candidates`. This agrees with the stated count of one verb, but I have not measured it.

**Residuals.** These are narrow and none of them reverses the fix:

1. **The GDB/Rizin aliases have no retained grounding** (`count-c1.py:27-28`, `debug-with-gdb → gdb_console`, `debug-with-rizin → rizin_debug_command`). A search of the lane outside `w2/` finds no `gdb_console`/`rizin_debug_command` in any retained REA record or source excerpt. The fixture `forged_debug_operation` (`counter-fixtures.py:134-135`, expected count 4) hard-codes the alias as ground truth, so the control is circular: it checks the counter against the same constant. Today the effect is confined to future runs, since no debugger record exists and the aliases only gate what *would* count.
   - Action: cite the REA 6.5.0 package location that emits those operation names (file and SHA-256, as earlier rounds did with `package-source-hashes.txt`), or drop the aliases until a retained record exists.
2. **S053 still names the copy as its source.** `corpus/SOURCES.md:59` gives the source as `identify-godot.evidence.json`, which is the copy the counter now refuses.
   - Action: add a superseding row that names `identify-godot.envelope.json` (following the S054 pattern), without rewriting S053.
3. **Stale docstring.** `count-c1.py:2-10` still describes "a non-refused JSON record (r21 `bind`)" and omits the envelope, `meta.command`, alias and extraction rules. The `limit` string (`:162`) is current.
   - Action: update the docstring to state the envelope rule.
4. **Envelope is not cross-checked against producer stdout.** A hand-edited envelope with `ok:true` would still count. This is within the declared limit ("no cryptographic authentication"), so it is not a defect.
   - Optional hardening: require the cited envelope to equal `json.loads(<sibling>-run.json stdout)` with `exit == 0`.

The aliases don't authorize or evidence any debugger run, and nothing here does either.

## Non-findings and limits

- C2 shows no wrapper defect. It reads the envelope, and every receipt equals its run stdout. Separately, the C2 counter checks only `meta.command`, not argv. For example, `cutter-command.json` (`VALIDATION_ERROR`) and `cutter-command-missing.json` (`invalid_request`) share `meta.command`. A different-argv receipt would pass the probe check if its error code matched. That gap is outside this seat's wrapper scope and is only noted here.
- The live `tools/count-c{1,2}.py` differ from the freeze-commit bytes (`75f04a4`, retained as `frozen/`, cmp rc 0). `corpus/lessons/round-22.md:50-54` discloses this. It is not judged here.
- These are observations at a single revision. Nothing here claims cryptographic Evidence authentication or provider behavior over time. No tool was installed or updated.
