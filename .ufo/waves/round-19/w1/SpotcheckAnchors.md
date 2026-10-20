# SpotcheckAnchors — R18 anchor and routed-defect verification (read-only)

Read-only seat. Baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (B). No lane edits, no git writes, no
REA/Ghidra/carrier execution. Tool installs/updates: none. All git reads used `git show/cat-file/rev-parse/
ls-tree/status --untracked-files=no`; the one executed lane tool is the static, read-only
`head-rev-lint.py` (git objects only, stdout only, run with `-I -B`).

## 1. Anchor verdicts (all confirmed)

| W19 anchor | Quote (first line of range) | Count | Verdict |
|---|---|---|---|
| `corpus/lessons/round-18-verifier-spotcheck.md:191-199` (seven routed) | `:191` `## Routed defects (kaidoku, next round; status-neutral)`; `:193` `1. **R18-MIDMAP-LISTSTEP.** …`; `:199` `7. **R18-INSTALL-RECORD.** …` | 7 numbered items (`grep -cE '^[0-9]+\. \*\*R18-'` → 7) | **accurate**: range = heading + blank + the 7 defects |
| `…spotcheck.md:201-206` (carried) | `:201` `Carried open (lane-owned, already listed in round-18.md Open):`; `:202` PROVINCE drift; `:203` custody-pair; `:204` jj-red-before; `:205` `revpin.py:6`; `:206` r12 items | 5 bullets | **accurate** |
| `corpus/lessons/round-18.md:86-92` (Open) | `:86` `## Open (routed earlier or found this round, still open)`; `:88` r12 items; `:89` PROVINCE; `:90` citation-drift/custody/jj; `:91` invocation-audit; `:92` adjacency + `revpin.py:6` | 5 bullets, file ends at `:92` | **accurate** |

Blob identities at B: `corpus/lessons/round-18-verifier-spotcheck.md` = `8bb005d9f3825d7c89754696578c16761a464911`;
`corpus/lessons/round-18.md` = `e95c32365b170e0be9018096358dc75bd0e22c25`.

The seven defect IDs in `W19/claims.json` (`C1.claim`) are spelled identically to `:193`–`:199`: R18-MIDMAP-LISTSTEP,
R18-VALIDATOR-DIGEST, R18-STRICT-BASELINE, R18-HEAD-ALIASES, R18-DEADSEAT-RECORD, R18-REGISTRY-PINNED,
R18-INSTALL-RECORD. `C1.falsifiable_before_after` names `:191-199` — consistent.

## 2. Each routed defect at B — still present (not fixed)

### R18-MIDMAP-LISTSTEP — OPEN (observation)
Defect sentence (`:193`): “`.ufo/waves/round-17/tools/receipt-validate.py:576-578`: under `--require-mid-maps`, a
list-shaped `steps` passes if *any* step has `pin_checks`. The `analyze` step is not required, which contradicts the
flag's documented contract.”
Named lines at B (`.ufo/waves/round-17/tools/receipt-validate.py`, blob from B):
```
570  if require_mid_maps:
572      steps = receipt.get("steps")
573      if isinstance(steps, dict):
574          astep = steps.get("analyze")
575          ok = isinstance(astep, dict) and bool(astep.get("pin_checks"))
576      elif isinstance(steps, list):
577          ok = any(isinstance(s, dict) and s.get("pin_checks")
578                   for s in steps)
```
Documented contract at the same blob `:33-36`: “With --require-mid-maps (r18 receipts) every pin_checks entry must
carry map_path+map_sha256 (mid_map_missing) and **the analyze step must retain at least one check**
(mid_checks_absent).” The list branch checks `any(...)` over all steps, not `analyze`. Unchanged at B.
“Real round-18 receipts are object-shaped” confirmed: all 15 `.ufo/waves/round-18/runs/*/receipt.json` have
`steps` of type `dict` (2 keys: `analyze`, `inspect-go-binary`), so the 15/15 result is unaffected as stated.

### R18-VALIDATOR-DIGEST — OPEN (observation)
Defect sentence (`:194`): “`routed-defects.py` `validator-sha256-pinned` checks only the format. Compare it with
`git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum`; the value is correct today
(`618448829ba6…126f`) but is unguarded. Also retain the digest of each remapped receipt copy in
`validate16/summary.json`, so the input binding stops resting on prose.”
Named site resolved to `.ufo/waves/round-18/tools/routed-defects.py:463-467` at B:
```
463  vs = doc.get("validator_sha256")
464  ok = isinstance(vs, str) and len(vs) == 64 and all(
465      c in "0123456789abcdefABCDEF" for c in vs)
466  checks.append(_check("substance", "validator-sha256-pinned", ok,
467                       f"validator_sha256={vs!r} (format only; see limits)"))
```
No comparison against `git show 9011581:… | sha256sum` exists in the tool. The quoted digest reproduces:
`618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f` (exit 0).
Second clause open: `.ufo/waves/round-18/evidence/validate16/summary.json` at B records only
`receipts[].{checks_performed,exit,findings,kind,label,stdout_sha256}` (8 entries) and a `remap` object with
`from/to/scope/tree/live_paths_left_unremapped` — no digest of any remapped receipt copy. It does record
`validator_rev: 9011581…` and `validator_sha256: 618448…126f` (`:81-82`), i.e. the value is stated but unbound.

### R18-STRICT-BASELINE — OPEN (observation)
Defect sentence (`:195`): “The "exit 1 at `9011581`" for `routed-defects.py --strict` (SCORECARD round 18, report)
has no retained receipt. The verification pass keeps only the non-strict baseline (open 6, exit 0). Retain the
strict baseline run.”
Assertion site `SCORECARD.md:2451`: “`…routed-defects.py --root <LANE> --rev <REV> --strict` (exit 1 at `9011581`,
exit 0 at `454dee6`)”.
Retention site `.ufo/waves/round-18/verify.py:173-180`:
```
173  # C1: routed R17 defects at baseline and source (plain reporting; strict
174  # would fail at baseline by design, so strict runs only at source).
175  run("routed-defects-baseline", … "--rev", base], 0)
177  run("routed-defects-source", … "--rev", source], 0)
179  run("routed-defects-source-strict", … "--rev", source, "--strict"], 0)
```
`.ufo/waves/round-18/verify/` at B holds `routed-defects-baseline.{stdout,stderr}` (no `--strict`) and
`routed-defects-source-strict.*`; there is **no** `routed-defects-baseline-strict.*`. Unchanged at B.
Extra mismatch (observation): the retained source-strict receipt belongs to `source_revision`
`db4bdb16b842a93f8ec07523c1275c6dfe0f5229` (`verification.json`), not to the `454dee6` cited in `SCORECARD.md:2451`
— so neither cited rev (baseline `9011581`, source `454dee6`) has a retained strict receipt.
(Related observation, not a routed defect: `SCORECARD.md:2452` also asserts “exit 1 at `9011581`, exit 0 at
`454dee6`” for `head-rev-lint.py`; the two retained strict lint receipts are baseline/source of the same
verification run.)

### R18-HEAD-ALIASES — OPEN in code (observation); limit partly registered already
Defect sentence (`:196`): “citation-drift `:329` refuses only the literal `HEAD`, so `@`, `HEAD~0` and
`HEAD^{commit}` pass. The two nested compare-only reads (`round-17/verify.py:83`, `revpin.py:108`) are invisible to
`head-rev-lint.py`. Carried in the lesson's Open list; fix it or register the limits in the SKILL rows.”
Named site resolved to `.ufo/gates/citation-drift/citation-drift-probe.py:329` at B:
```
329  if rev == "HEAD":
330      tip = git_commit(root, "refs/heads/%s^{commit}" % branch)
…
341  findings.rev_resolved = git_commit(root, "%s^{commit}" % rev) or rev
342  return rev, None
```
Any other explicit rev (`@`, `HEAD~0`, `HEAD^{commit}`) falls through `:339-342` and is evaluated unchanged; no
alias normalization or refusal exists. Unchanged at B (code read; not executed).
Named nested reads: `.ufo/waves/round-17/verify.py:83` = `head = _git_or_none("rev-parse", "--verify",
"HEAD^{commit}")` (with `# head-rev-lint: compare-only` at `:82`); `.ufo/waves/round-18/tools/revpin.py:108` =
`head = _resolve(lane, "HEAD^{commit}")` (no annotation). Invisibility confirmed by running the static scanner at B:
`head-rev-lint.py --rev B --strict` → `live 0, annotated 6, fixture 15, files_scanned 40`, exit 0; its site list has
**no** entry for `round-17/verify.py:83` and **no** entry for `revpin.py:108` (only `revpin.py:218` as `other-HEAD`
fixture). The wrappers (`_git_or_none`→`git(*args)`, `_resolve`→`_git(root,*args)`) do not carry a literal
`["git", ...]` argv in their own bodies, so the linter's literal-or-wrapper rule misses them.
Registration state at B: the alias limit is already written into SKILL, at `SKILL.md:579`: “The refusal matches only
the literal `--rev HEAD`; `@`, `HEAD~0`, `HEAD^{commit}` are not refused (round-18 w2 `CitationDriftReview.md` F1)”.
The nested-wrapper blindness is stated in `SCORECARD.md:2452` limits (“two compare-only HEAD reads behind nested
wrappers are invisible to the lint”), and generically in `SKILL.md:587` (“Syntactic: dynamic revision flow is a
listed blind spot”), but not named in the registry row. [INFERENCE] The “register the limits in the SKILL rows”
branch of the defect is therefore half-satisfied at B; the code branch is untouched. C1's substance fix should be
judged on the `:329` code or on an explicit SKILL row edit for the nested reads, not on the already-present alias
note.

### R18-DEADSEAT-RECORD — OPEN (observation)
Defect sentence (`:197`): “`SCORECARD.md:2462` says "1 dead … 4 not returned (GatePRODUCERREV, TruthREGISTRY,
DecisionRuleApply, ShonenLines)", while the report erratum says 3 dead. The committed wave-2 records hold no error
text for any dead seat. Append a correction and retain the failure causes.”
`SCORECARD.md:2462` at B quotes exactly: “W2: 98 seats (…); 1 dead (GateSUMSRUNLOG, provider usage-policy refusal),
4 not returned at integration (GatePRODUCERREV, TruthREGISTRY, DecisionRuleApply, ShonenLines).”
Erratum located outside the lane at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kaidoku.md:101`:
“Dead seats in W2: 3 (GateSUMSRUNLOG, GatePRODUCERREV, TruthREGISTRY); `ShonenLines` had not returned when this
erratum was written.” (line `:84` of the same report still says the original two dead).
Wave-2 record check at B: `.ufo/waves/round-18/wave2-registry.json` entries for all five seats
(`GatePRODUCERREV` `:63`, `GateSUMSRUNLOG` `:85`, `TruthREGISTRY` `:96`, `DecisionRuleApply` `:569`,
`ShonenLines` `:932`) contain exactly `{kind, agentId, role, item, axes}` — no status, exit, or error text.
`git grep "3 dead"` over `.ufo/waves/round-18` returns no lane file, so the lane retains neither the count
correction nor the causes. Unchanged at B.

### R18-REGISTRY-PINNED — OPEN (observation, one nuance)
Defect sentence (`:198`): “The `pins` ("none") and `go-buildinfo-probe` (constants in code) rows name no pinned-value
path. The gate checks only the token, so name the path or state that the row is a probe with no persisted baseline.”
Rows at B (5th cell):
- `SKILL.md:542` (`pins | probe / kaidoku | …`): “Pinned values: none (no expected digests; each entry records
  sha256, size and mtime_ns at the instant read). Identical bytes at two instants only, never continuity. Write
  scope: … Kind corrected from `tool` to `probe` in round 18 (R17-REGISTRY; PROTOCOL row kinds are gate or probe)”
- `SKILL.md:545` (`go-buildinfo-probe | probe / kaidoku | …`): “Pinned values: the build-info magic and header
  constants of go1.25.0 `debug/buildinfo` (keeps the writable-segment fallback that go1.27.3 removed, S024);
  cross-check with `go version -m`. Write scope: none …”
Neither names a pinned-value file path. Gate at `.ufo/waves/round-18/tools/routed-defects.py:655-661`:
```
660  if "Pinned values:" not in cell:
661      return False, "no 'Pinned values:' in 5th cell"
```
plus `Write scope:` ≥3 words and existence of backticked `.ufo/`/`corpus/` tokens (`:669-676`); both rows are in
`REGISTRY_SCOPED` (`:62-63`). So the token-only nature is confirmed.
[INFERENCE] The `pins` row already says “Pinned values: none (no expected digests; …)” and labels itself `probe`;
that arguably satisfies the defect's second remedy (“state that the row is a probe with no persisted baseline”),
leaving only “name the path” unsatisfied — and there is no baseline to name. `go-buildinfo-probe` names its
constants and source module but does state neither a path nor “no persisted baseline”. A fix that only rewrites
`pins` would close the token gap, not the substance one; record the distinction rather than treating both rows
identically.

### R18-INSTALL-RECORD — OPEN (observation)
Defect sentence (`:199`): “Go 1.24.6/1.25.0 (tool, version, channel, sha, reason) are recorded only in the fleet
report. Add the record to the round lesson, as round 17 did.”
`corpus/lessons/round-18.md` at B (92 lines) has no “Tool installs/updates” section and no install record: grep for
`tool install|installed|channel` returns only content lines (`:5` scope, `:10` Ghidra binding, `:18` knowledge
entry, `:20-21` decisions, `:34-37` SOURCES, `:45` S034 correction, `:65` mistake row, `:80` in-round revisions,
`:92` adjacency) — none records a Go install with tool/version/channel/sha/reason.
The round-17 pattern the spotcheck asks to mirror is `corpus/lessons/round-17.md:135-141` (“Tool installs/updates:
none by the L1. Seat `DraftSourcesRows` (w1) installed Go 1.27.3 linux/amd64 from the official go.dev tarball into
`~/.local/opt/go-1.27.3`, not on PATH; its sha256 matched `go.dev/dl/?mode=json`. … No pacman transaction was run.”).
Unchanged at B.

## 3. Freshness of the lane state (observation)

- `git rev-parse refs/heads/main` → `85589ac757f9ca3cb25efcd702d0963e25c9c4df`; B is its parent:
  `git rev-list --count B..main` → `1`; the sole commit (`round-19: declared claims, seat contract, wave-1
  spec/dispatch/registration, baseline census and emulator prescan`) adds 20 files, all under `.ufo/waves/round-19/`.
  No routed-defect fix has landed in `main` after B.
- Working tree: `git status --porcelain --untracked-files=no` → empty (exit 0). All files named by the seven
  defects are byte-identical to B in the lane tree.
- `.ufo/waves/round-19/` does not exist at B (`git cat-file -t B:.ufo/waves/round-19` → `fatal: … not in <B>`, exit
  128), and at `main` it contains only `claims.json`, `contract.md`, `gen-wave1.py`, wave-1 dispatch/registry/
  registration/spec/result and `evidence/` (census + prescan). In particular `.ufo/waves/round-19/tools/routed-r18.py`
  — the command in `C1.falsifiable_before_after` — does not exist yet; `gen-wave1.py:45` and
  `wave1-dispatch.json:1032` assign its creation. [INFERENCE] The C1 before/after is prospective: “7 open at B” is a
  property the new tool must reproduce by reading B through git objects, not a retained measurement. That is
  legitimate under the contract's revision-scoped rule, but it should be stated as such or the claim will read as
  a retained baseline.

## 4. Anchor/claim calibration nuances (for the L1, not blockers)

1. `claims.json.carried_open` is **not** a verbatim copy of `:201-206`: it omits “PROVINCE REA-pin drift”
   (relocated to C2, where it is the primary claim) and adds “jj 0.45.1 doc triple registration (routing report
   gives it to kumitate)”, which appears only at `round-18.md:92`, not in `:202-206`. The contract's sentence
   (“carried items at :201-206”) is narrower than the claim's list. [INFERENCE] Low severity; the claim's list is a
   union of both anchors. Either cite both ranges in `carried_open`, or drop the round-18.md-only item from it.
2. `round-18.md` itself already records the HEAD-alias limit at `:90` and `revpin.py:6` at `:92`; those two are
   therefore both routed (spotcheck) and Open-listed (lesson) at B — no conflict, but a C1 closure must not count
   the lesson's Open line as the “named correction” for R18-HEAD-ALIASES (the spotcheck requires the SKILL row or
   code fix).
3. Defect 3's cited revs and the retained receipts do not line up (section 2). A round-19 “retain the strict
   baseline run” fix must pin which rev the `--strict` red is run at; B's own SCORECARD sentence names `9011581`,
   while the round-18 verification's own `baseline_revision` is also `9011581` — so the baseline half is
   reproducible if run now; the `454dee6` source half is not the retained receipt's rev (`db4bdb1`).

## 5. Commands and exits (observations)

| Command (abridged) | Exit | Result used |
|---|---|---|
| `git rev-parse refs/heads/main` | 0 | `85589ac…` |
| `git cat-file -t B` | 0 | `commit` |
| `git rev-list --count B..refs/heads/main` | 0 | `1` |
| `git show B:<spotcheck> \| nl -ba \| sed -n '188,210p'` | 0 | anchors `:191-199`, `:201-206` |
| `git show B:corpus/lessons/round-18.md \| nl -ba \| sed -n '84,94p'` | 0 | anchor `:86-92`, file length 92 |
| `git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py \| sha256sum` | 0 | `618448829ba6…126f` |
| `git show B:.ufo/waves/round-17/tools/receipt-validate.py \| nl -ba \| sed -n '566,590p'` | 0 | list branch `:576-578` |
| `git show B:SCORECARD.md \| nl -ba \| sed -n '2455,2470p'` | 0 | `:2462` dead-seat sentence; `:2451` strict claim |
| `git show B:.ufo/waves/round-18/verify.py \| nl -ba \| sed -n '168,192p'` | 0 | strict only at source |
| `git show B:.ufo/gates/citation-drift/citation-drift-probe.py \| nl -ba \| sed -n '300,345p'` | 0 | `:329` literal-only |
| `python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root <LANE> --rev B --strict` | 0 | `live 0, annotated 6, fixture 15, files 40`; no site for `verify.py:83` / `revpin.py:108` |
| `python3 … : all 15 round-18 receipt.json steps types` | 0 | 15/15 `dict` |
| `python3 … wave2-registry.json` five dead-seat entries | 0 | `{kind,agentId,role,item,axes}` only |
| `git grep -n "3 dead\|three dead" B -- .ufo/waves/round-18` | 0 (no output) | no lane erratum |
| `sed -n '99,102p' /home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kaidoku.md` | 0 | erratum: “Dead seats in W2: 3 …” |
| `git --no-optional-locks status --porcelain --untracked-files=no` | 0 (empty) | lane tracked tree clean |
| `git cat-file -t B:.ufo/waves/round-19` | 128 | `.ufo/waves/round-19` absent at B |

## 6. Verdict and remaining unknowns

All three W19 anchors are exact and the seven routed R18 defects are all still present at B, none already fixed.
The two carried/Open anchors also match, with the `carried_open` union nuance above.

Confidence: high on anchors, defect presence, and the two executed checks (digest recompute, static lint run).
Not verified (out of scope or unavailable):
- The R18-MIDMAP-LISTSTEP red case was not executed against a synthetic list-shaped receipt (code read only); the
  `any(...)` shape is unambiguous, so this is observation-level, not execution-level.
- The three citation-drift aliases were not run through the probe (would write snapshot dirs); refusal absence is
  read from `:329-342`.
- The `94`-line round-18.md install record was confirmed by absence of any install mention; the Go 1.24.6/1.25.0
  fleet-report record itself was not re-read (outside lane), only the spotcheck's claim.
- No check was made of whether any round-19 writer has already created `routed-r18.py` in a separate worktree; the
  lane `main` at observation time has no `tools/` dir.
