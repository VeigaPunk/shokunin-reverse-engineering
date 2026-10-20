# ToolWaveOutcomes review

## Scope and revision

Axes: calibration (concrete behavior over plausible defects), freshness (test the observed main tip), depth (the assigned adversarial cases). **[O]** The observed `refs/heads/main` tip was `279e8b19c51658bfd05b9e31a1c0894ab2e70537`; target `wave-outcomes.py` is absent at B `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` and is an 844-line addition at that tip. Tests ran against a detached private clone at that tip. No production file was edited; no tools were installed or updated.

## Findings by severity

### P3 — Flat-map causes cannot represent a seat literally named `causes`

**Observation:** registration accepts any safe bare filename as a seat (`.ufo/waves/round-19/tools/wave-outcomes.py:118-122,143-147`), and the documented flat-map form is keyed by seat (`:23-29`). But `load_causes` treats every top-level object containing `"causes"` as the wrapped form before resolving keys (`:237-243`); a registered `causes` seat with flat input `{"causes":"worker failed"}` is therefore refused as `causes_invalid` rather than interpreted as that seat's cause. In the private-clone fixture, the command exited 2 and wrote no output. The list-row shape for the same seat succeeded and recorded the cause (exit 0), so this is a limited shape inconsistency with a workaround, not a blocker for other names.

**Inference:** either reserve/document wrapper-key seat names or disambiguate the wrapper after considering registered seats; otherwise the accepted flat-map contract is narrower than the registration validation implies.

### P3 — `MISSING` diagnostic is imprecise for a zero-byte report file

**Observation:** a zero-byte `Alpha.md` is correctly absent under the declared predicate (`:16-18,170-176`), and the result is red as expected. Its summary nevertheless says `MISSING ... (rule: seat has no report file)` (`:381-382`) although that path exists. The same output's `OUTCOMES` line does state the precise regular-file-and-size rule (`:375-380`), so counts and JSON remain interpretable.

**Inference:** use wording such as “no non-empty regular report” for the per-seat diagnostic to avoid contradicting the zero-byte case.

## Requested adversarial checks and interpretation

- **Selftest [O]:** `SELFTEST: CLEAN cases=33`, exit 0, both from the lane working tree (selftest fixtures are temporary) and from the detached clone at the observed tip.
- **Mismatched registration/report filename [O]:** synthetic registration had seat `SeatAlpha`; only `Kaidoku19.SeatAlpha.md` existed and causes were empty. The tool looked up `<report-dir>/SeatAlpha.md`, returned `reports=0 missing=1 uncaused=1`, named `SeatAlpha`, wrote the record, and exited 1. This matches the explicit name-based rule (`:16-21,312-325`); it does not infer a report filename from the agent ID. **Inference:** callers must keep report filenames aligned with registration member keys. No finding for this result under the documented contract.
- **Report present, terminal aborted [O]:** the actual W1 terminal evidence records `MidmapListStep` with `report_present:true`, `stop_reason:"aborted"`, and cause `"Request was aborted"` (`.ufo/waves/round-19/evidence/wave-outcomes/w1-terminal.json:16-20`). The corresponding outcomes row is `{report_present:true,cause:null}` (`.ufo/waves/round-19/wave1-outcomes.json:267-271`). Re-running the tool in the clone against W1's registration, `w1/`, and `w1-causes.json` reproduced the row and exited 0 with `seats=90 reports=48 missing=42 uncaused=0`. This is consistent with the literal report-presence/exit contract (`:16-21,312-353`): the tool does not read terminal records, and `report_present` is not a terminal-success assertion. **Residual risk:** do not interpret this record's zero exit as proof every worker terminated cleanly or that terminal causes were retained; it answers the narrower report-file question.
- **Unknown causes key [O]:** a cause for unregistered `Ghost` produced `REFUSED causes_unknown_seat`, exit 2, and no output file. This agrees with the explicit selftest case (`:576-584`) and fails closed; no finding.

## Verification gaps and command record

The `lsp` device is not mounted: `read xd://lsp` returned “No such tool” and listed only the available REA/AST/debug devices. Accordingly, no LSP status/references/definition/diagnostics were available; literal text search was used only to locate the exact `MidmapListStep` data rows, not as semantic caller proof. No build, formatter, or broad test suite was run.

Commands and exits observed (fixture registration/report/causes files were created only inside the clone):

```text
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B .ufo/waves/round-19/tools/wave-outcomes.py --selftest
  SELFTEST: CLEAN cases=33; exit 0

cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git rev-parse refs/heads/main
  279e8b19c51658bfd05b9e31a1c0894ab2e70537; exit 0
git cat-file -e 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0:.ufo/waves/round-19/tools/wave-outcomes.py
  absent at B; exit 128
git diff --stat 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main -- .ufo/waves/round-19/tools/wave-outcomes.py
  1 file changed, 844 insertions(+); exit 0

git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane
  exit 0
git -C /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane checkout -q --detach 279e8b19c51658bfd05b9e31a1c0894ab2e70537
  exit 0
git -C /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane rev-parse HEAD
  279e8b19c51658bfd05b9e31a1c0894ab2e70537; exit 0
python3 -I -B /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/tools/wave-outcomes.py --selftest
  SELFTEST: CLEAN cases=33; exit 0

# Real W1 inputs; output directed only into the clone.
python3 -I -B /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/tools/wave-outcomes.py --registration .ufo/waves/round-19/wave1-registration.json --report-dir .ufo/waves/round-19/w1 --causes .ufo/waves/round-19/evidence/wave-outcomes/w1-causes.json --out /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-w1-outcomes.json
  OUTCOMES seats=90 reports=48 missing=42 uncaused=0; MidmapListStep report_present=true cause=null; exit 0

# Adversarial mismatch: only Kaidoku19.SeatAlpha.md exists for registered SeatAlpha.
python3 -I -B /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/tools/wave-outcomes.py --registration /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-mismatch/registration.json --report-dir /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-mismatch/reports --causes /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-mismatch/causes.json --out /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-mismatch/out.json
  missing=["SeatAlpha"], uncaused=["SeatAlpha"]; exit 1

# Unknown Ghost cause against an Alpha-only registration.
python3 -I -B /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/tools/wave-outcomes.py --registration /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-unknown/registration.json --report-dir /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-unknown/reports --causes /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-unknown/causes.json --out /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-unknown/out.json
  REFUSED causes_unknown_seat; no output; exit 2

# Flat-map key collision for registered seat "causes".
python3 -I -B /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/tools/wave-outcomes.py --registration /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-reserved/registration.json --report-dir /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-reserved/reports --causes /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-reserved/flat-causes.json --out /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-reserved/flat-out.json
  REFUSED causes_invalid; no output; exit 2

# Same legal seat encoded with the supported list shape.
python3 -I -B /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/tools/wave-outcomes.py --registration /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-reserved/registration.json --report-dir /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-reserved/reports --causes /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-reserved/causes.json --out /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-reserved/list-out.json
  cause="worker failed" retained; exit 0

# Zero-byte Alpha.md exists but does not satisfy report predicate.
python3 -I -B /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/tools/wave-outcomes.py --registration /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-empty/registration.json --report-dir /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-empty/reports --causes /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-empty/causes.json --out /tmp/kr19-w2-ToolWaveOutcomes-4bjw6tc9/lane/.ufo/waves/round-19/w2/_review-empty/out.json
  MISSING ... (rule: seat has no report file); exit 1
```

No installs or updates were made.