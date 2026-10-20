# CriticC3 — falsify C3 (first-failure forecasting on go1.24.6)

Written 2026-10-20T17:51:46-03:00. Seat: KaidokuR20.CriticC3-2 (read-only). Scope: claims.json C3
(`.ufo/waves/round-20/claims.json:33-40`), C3 interface (`.ufo/waves/round-20/contract.md:76-81`),
executor spec (`.ufo/waves/round-20/gen-wave1.py:227-276`).

Axes attacked: calibration (can the forecast be trivially right?), coverage (is the carrier cohort
held-out?), depth (does first-failure add real discrimination or is it a kind-only re-skin?).

## 1. Can the forecast be trivially right (all silent)? — NO, refuted on the prediction side

**OBSERVATION.** I ran the unchanged round-18 emulator (byte-reading only, permitted by
`contract.md:90-92`) on all 20 go1.24.6 toolchain ELFs:

```
$ cd kaidoku-shokunin && python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py \
    --carrier <each of {bin/go,bin/gofmt,pkg/tool/linux_amd64/*}> \
    --golang-root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang
exit=0 per evaluable carrier; link exit=2 ('no Go build info', same as round-19 t1250-link,
predictions/decision-rule.json "excluded")
```

v1 map-path results (`predicted_failure_h1=True`, kind `invalid_index`, h0 silent):

| label | h1 invalid_index list | h0 list |
|---|---|---|
| bin/go | [35082496] | [] |
| addr2line | [22078465] | [] |
| compile | [36421889] | [] |
| nm | [22070273] | [] |
| objdump | [13816064] | [] |
| pprof | [27091201] | [] |
| trace | [25696001] | [] |
| vet | [13791488, 1801722468895780122] | [1801722468895780122] |

11 silent (gofmt, asm, buildid, cgo, covdata, cover, doc, fix, pack, preprofile, test2json); link
unevaluable. So the forecast is **not** all-silent: ≥7 carriers carry a non-null h1 first-failure
candidate. The r20 carrier cohort in `gen-wave1.py:256-258` keeps only
{go, gofmt, asm, cgo, compile, cover, preprofile, vet, pprof, trace} (10 labels) — it drops
addr2line, nm, objdump (all predicted failing) plus the silent buildid/covdata/doc/fix/pack/
test2json. Even on that reduced cohort, {go, compile, pprof, trace, vet} ≈ 5 predicted failures.

**OBSERVATION / residual threat.** The v1 `walk` channel still carries the unmasked-variadic
artifact (round-19 lesson, `corpus/lessons/round-19.md:35`): go1.24.6 `vet` walk_h0 = walk_h1 =
`1801722468895780122` (the variadic 0x8000-as-param-count signature, path ends `func.param[7]`,
identical failure under h0 and h1). Masking it in v2 removes that h0 read, which *changes* vet's D
status: v1 `predicted_failure_kind_h0='invalid_index'` (non-D), v2 should restore vet to D with
h1 first_failure `invalid_index 13791488` — mirroring round-19 vet (h1-only 13902080 confirmed in
`.ufo/waves/round-19/runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log:229`).
But: `go`, `compile`, `pprof`, `trace` show `walk_h0 index=8` — a *different* walk anomaly, not the
variadic pattern. INFERENCE: if index-8 is another emulator read bug rather than a real Ghidra read,
v2's h0 for those labels must come out null for them to stay D; if it is a faithful read, those four
labels leave D (h0 fails first). Either way the **D-set is sensitive to emulator bugs that are
invisible until Ghidra runs** — the freeze must pin v2's h0 forecasts, not just h1.

**INFERENCE (triviality verdict).** Prediction-side triviality is refuted. Outcome-side triviality
is possible only if Ghidra never fails (contradicts the confirmed mechanism on the same snapshot
path — §2) or if the compare rule degenerates. The real residual triviality channel is
*match-rule weakness*, not silence (§4).

## 2. Is go1.24.6 toolchain held-out? — artifact-held-out YES, version/mechanism-held-out NO

**OBSERVATION (no byte exposure).**
```
$ sha256sum /home/vgpnk/.local/opt/go-1.24.6/bin/* .../pkg/tool/linux_amd64/* > /tmp/kr20-c3-hashes.txt
$ grep -rlf /tmp/kr20-c3-hashes.txt .ufo/waves/round-1*/
→ only .ufo/waves/round-18/evidence/real-carrier-census.json        (exit 0)
```
The census (`real-carrier-census.json:499-595`) recorded each ELF's sha256 + `rea_inspect_exit` —
a byte-level `inspect-go`, not a Ghidra analyze. No prior bound Ghidra log exists for any of these
20 byte sequences. Prior Ghidra/analyze exposure invalidating the claim would be: (a) a bound
ghidra.log for the same sha256 (none found); (b) a frozen prediction emitted *after* seeing its
analysis output (freeze ordering is contract-gated, `claims.json:39`). Neither holds on lane
evidence. CAVEAT [INFERENCE]: my grep covers the lane only; an off-lane Ghidra project dir would
not appear here — the binding gate's run-bound logs + carrier-guard records are the control for that.

**OBSERVATION (version exposure).** The go1.24.6 Ghidra snapshot path was already exercised and the
mechanism *confirmed* on it in round 18:
- `s1246-swiss-nethttp` (go1.24.6, snapshot_status `exact_diff` → `go1.24.0.json` +
  `patchverdiffs/go1.24.6.json.diff`): observed `Invalid index: 22386945`, compare.exit=0.
- `real-kimi-webbridge` (go1.24.13 → fallback_to `1.24.6` diff): observed `Invalid index:
  15606016`, compare.exit=0.
- All four noswiss 1.24.6 synthetics: silent, as predicted.
(`runs/s1246-swiss-nethttp|real-kimi-webbridge/logs/*/ghidra.log`; decision-rule table at
`.ufo/waves/round-18/predictions/decision-rule.json`.)

So "held-out" must be declared **artifact-held-out, same-version-exercised** — exactly the wording
the round-19 amendment was forced into for go1.25.0
(`round-19/claims.json` amendments[0].C3: "artifact-held-out, not version-held-out"). If the r20
decision-rule.json or claims text says "held-out go1.24.6" without that qualifier, that is a
wording falsifier.

**INFERENCE.** Prior exposure that *would* invalidate the claim: an emulator/predictor change tuned
after seeing a go1.24.6-toolchain Ghidra log — impossible today since none exists — OR the v2 mask
being tuned to reproduce the *known* round-19 vet outcome (see §3, retro overfitting). A subtler
one: `*types.valueMap` in go1.24.6 `vet` is the same h1-only type family that produced the confirmed
13902080 in go1.25.0 vet (`diagnostic_detail: [{"type": "*types.valueMap", "h1": "invalid_index"}]`)
— the 1.24.6 vet forecast partially restates already-confirmed knowledge rather than probing new
mechanism surface. Depth-wise this is repetition of the strongest prior result, not a falsifier of
artifact held-outness.

## 3. Retro-check overfitting (depth axis)

The C3 claim says v2 is "checked retrospectively against the round-19 bound go1.25.0 logs, then
frozen" (`claims.json:36`). **OBSERVATION:** round-19 outcomes are public in the lane
(`runs/t1250-vet/.../ghidra.log:229` Invalid index 13902080; 7 silent). A v2 built to match that
table is fitting 8 known labels. The claim's own falsifiers (`claims.json:39`) require the retro
check "is retained" — retention is necessary but not sufficient: what must also be frozen at the
same commit is (a) the v2 source, (b) the retro table itself, (c) a statement that no v2 output was
modified after retro. Otherwise "retrospective check then freeze" can silently become
"tune until retro passes then freeze" — the standard self-calibration trap. INFERENCE: this is a
defect in claim wording, fixable by extending the freeze predicate to cover
`tools/swiss-misread-v2.py`, `tools/first-failure-extract.py`, `tools/compare-first-failure.py` and
the retro artifact, not only `predictions/*.json` blobs.

## 4. Non-trivial discrimination requirement (proposal)

1. **Kind normalization, frozen before runs.** Ghidra reports read failures as
   `java.io.EOFException` whose *message* is `Invalid index: N`
   (`ghidra.log:229`: `Caused by: java.io.EOFException: Invalid index: 13902080`). A class-name
   mapping labels this `eof`; a message mapping labels it `invalid_index`. The v2 kind enum
   (`invalid_index|eof|...`, `contract.md:78`) therefore has a built-in ambiguity that decides every
   match. Require: extractor kind = `invalid_index` iff the EOFException message matches
   `Invalid index: N` (index=N); `eof` iff message is the past-EOF form (`gen-wave1.py:242` already
   names both patterns — pin the precedence in the frozen contract: message-beats-class).
2. **Index semantics, frozen.** The compare matches "same kind and same index"
   (`gen-wave1.py:250`). `index` must be defined as the observed Invalid-index value N, not the
   typelink offset, not `va` — state which field N populates and that `va` is reported but not
   matched (addresses differ across runs only via ASLR? — no: static ELFs, va is stable; still, one
   matching field keeps the rule single-valued).
3. **Anti-degenerate baseline reported.** With ~half the cohort predicted `invalid_index`, report
   k/N alongside two frozen baselines: always-null accuracy and majority-kind accuracy computed
   from the frozen prediction table. If both baselines already score ≥ k, the round adds no
   discrimination and that must be said in the outcome, not hidden behind "match count reported
   whatever it is" (`claims.json:37`).
4. **Cohort must keep ≥1 D and ≥1 non-D among *bound* labels.** With 10 planned labels
   (`gen-wave1.py:257`) this holds (≈5 D-candidates). Pin: if the frozen D-set shrinks to 0 or N,
   c3.first_failure_bound still counts but the claim's depth value is declared vacuous.
5. **h0 forecast also frozen and checked.** The D rule (`h1 non-null ∧ h0 null`,
   `gen-wave1.py:260-261`) depends on h0 being right, and §1 shows v2's mask changes h0 outcomes.
   A label whose observed failure equals the *h0* forecast is `h0_consistent`, non-discriminating
   (round-19 rule, `round-19/predictions/decision-rule.json` "h0_consistent") — retain that class.
6. **Freeze order pinned to Git chronology** (round-19 lesson: commit order, not written
   timestamps): predictions + v2 + extractor + compare + decision-rule all in or before the freeze
   commit; the first `run-carriers.sh` REA invocation strictly after the freeze push
   (`claims.json:39` already says this — extend "prediction blob" to the tool trio).
7. **link (no build info) stays an exclusion record, not a null forecast** — predicting "silent"
   for a carrier Ghidra's Go analyzer skips would inflate k.

## 5. Smallest safe corrections

- Decision-rule.json must say **artifact-held-out, version-exercised** for go1.24.6, or C3 inherits
  the round-19 wording defect a second time.
- Extend `falsified_if`/freeze coverage from prediction blobs to the three new tools + retro table
  (§3).
- Pin kind normalization (message-beats-class) and index semantics in the compare contract (§4.1-2).
- Declare the `walk index=8` anomaly: if it is another emulator defect, record it like the variadic
  bug before freeze — it silently sets D-membership for {go, compile, pprof, trace} (§1).
- Cohort: consider the full 19 evaluable ELFs instead of the 10-label subset — the dropped
  addr2line/nm/objdump are predicted failures and the dropped silent labels are cheap; subsetting
  without a stated rule looks like cherry-picking.

No installs performed. Commands used: v1 emulator runs (exit 0/2 as shown), sha256sum+grep
(exit 0), `date -Iseconds` (exit 0).
