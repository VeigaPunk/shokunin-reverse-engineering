# SimplifyTools — YAGNI pass over the round-17 contract (advisory)

Status: advisory, read-only. No deletion made: at review start `.ufo/waves/round-17/tools/` was empty;
`measure.py` landed at 10:37 while I read, so tool-level findings cite `contract.md`, not implementations.
O = observed by reading/running something named; I = inference. No installs.

## Axes

calibration (C1), depth (C2), no-harm (controls), re-runnability (registry surface). Move rule used:
a deletion is kept only if no named C1/C2 consumer loses its instrument. Frontier stops where the next
deletion removes a metric's falsifier.

## Preserved contract (what must not be cut)

C1 instruments: pins red case (`contract.md:17-19`, `claims.json:13`), temporal-sweep, invocation-audit
(`claims.json:13`). C2 instruments: carrier-run steps (`contract.md:34-47`), log-extract (`:51-60`),
predict (`:62-73`), compare (`:75-78`), receipt-validate (`:106-108`; capability row only if the receipt
validates, `claims.json:22`). controls.py and measure.py carry no C1/C2 metric themselves but are cited by
the operability/coverage scorecard rows (`w1/draft-scorecard.md:18-19`). Every tool in `measure.py:26-38`
except `carrier-census.py` maps to a named C1/C2 consumer; the only tool-level drop candidate is T2.

## Deletion candidates

### T1. `carrier-run.py --search NAME` steps — DROP (no consumer)
Anchors: `contract.md:33` and `contract.md:40-41`.
No C1/C2 consumer: both claims name `analyze` only (`claims.json:12`, `:22`); the pilot argv is analyze
alone (`pilot/README.txt:4-5`); the observation surface is the retained log, and the non-claims promise no
symbol recovery. The in-range log already carries the symbol facts a search would restate
(`pilot/esbuild-0.25.12-log/ghidra.log:71-73`). Effect: removes a second step template, a flags dependency
(`contract.md:41` "verify exact flags"), and a timeout/failure mode. Harm to C1/C2: none.

### T2. `carrier-census.py` — FOLD into the probe or DROP (the one real duplication)
O: `npx -y rea-agents@6.5.0 inspect-go-binary /usr/bin/shfmt --format json` (allowed verb, 0.64 s) returns
`subject.digest.sha256`, `normalized_result.build_info.go_version` = `go1.27.0-X:nodwarf5`, and
`evidence_id`. `contract.md:111-113` asks the census for sha256, size, ELF magic, go_version, evidence_id,
pacman owner — so 3 of those 6 columns are exactly `inspect-go-binary` output, and `carrier-run` already
re-derives them per chosen carrier (`contract.md:34-35` + pins). Unique census columns are size, ELF magic
and pacman owner: selection prose, not C1/C2 verification.
Recommendation: if the pool table is cited in the knowledge entry, keep the tool but have it import
`buildinfo-probe`'s reader (same `importlib` pattern as retain→pins, `contract.md:24`) instead of 11 npx
calls; otherwise drop it. Do not keep three readers of the same blob (REA-in-census, REA-in-carrier-run,
stdlib probe). Cost of dropping: `measure.py:26-38` lists it (one-line edit).

### T3. Field `pins.snapshot.monotonic_ns` (`contract.md:13`) — DROP
No reader: `compare` emits only equal/changed/missing plus pre/post UTC (`contract.md:15-16`), and
QUALITY row 19 asks for UTC timestamps only (`w1/draft-quality-19.md:11`). Keeping it invites a second
clock into the record.

### T4. Field `carrier {path, sha256 pre/post}` (`contract.md:43`) — DROP the two digests
The same facts are entries in `pins_pre`/`pins_post` for the same path (`contract.md:34`, `:42`). Two
authorities for one fact can disagree, and nothing says which one is evidence. Keep `carrier.path`.

### T5. `buildinfo-probe` pre-1.18 `pointer_format` branch (`contract.md:103`) — DROP for this round
No caller: all four named carriers are inline-format (O for shfmt: my `inspect-go-binary` run reports
`build_info.encoding = "inline"`; esbuild 0.25.12 carries go1.23.12, i.e. >= 1.18). Keep `found:false` only
if T2 folds census into the probe.
Cost of keeping: a second format branch plus a synthetic fixture in selftest.

### T6. `log-extract.classification` (`contract.md:58-59`) — DROP
No program consumer: `compare` reads exactly `untested_version`/`snapshot_label`/`missing_bootstrap`
(`contract.md:77-78`). It is derivable from retained fields at read time; the entry can state its own label.

### T7. `measure` README map tokens (`contract.md:119`; `measure.py:161-164`) — out of C1/C2
It feeds only the draft coverage row (`w1/draft-scorecard.md:18`). Keep while that row exists; drop the
block with the row. SOURCES histograms (`measure.py:165-167`) are in scope for C2's `sourced` note — keep.

## retain.py vs carrier-run.py vs pins.py — the asked overlap

- `pins.py` is the only hashing/stat/compare authority (`contract.md:12-20`); both other tools import it
  (`contract.md:24`). Keep one authority.
- `retain.py` is the only producer that yields an argv+pin receipt for a **non-REA** command; C1(b)'s
  citation-drift receipt needs exactly that (`claims.json:12`). The r16 exercised form was
  `python3 -I /abs/.../citation-drift-probe.py --root /abs/... --strict`
  (`.ufo/waves/round-16/verification.json` `commands[17]`). Keep.
- `carrier-run.py` is the only poller and the only producer of retained `ghidra.log` (C2). Keep.
- The duplication is the **record shape**, not the responsibility: retain's
  `{argv, cwd, started/ended, exit, stdout/stderr path+sha256}` (`contract.md:26-28`) is repeated per step
  in carrier-run (`contract.md:43-44`). Fix at the schema: state the step record once (retain's shape) and
  make carrier-run's steps emit that exact object.
- Rejected merges (recorded so they are not re-litigated): folding retain into carrier-run makes
  carrier-run two tools; having carrier-run shell out to retain duplicates pin scopes and produces two
  authorities for `pins_compare`; having carrier-run read census's inspect-go JSON breaks re-runnability
  for a carrier that was never censused.

## Precision guards — do not loosen these while pruning

**G1 invocation-audit matcher (`contract.md:85-87`).** The defect it exists to catch: `SKILL.md:448` row
`python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . …` vs exercised
`python3 -I /abs/… --root /abs/… --strict` (`verification.json` `commands[17]`). Normalize only `argv[0]`;
never swallow interpreter flags (`-I` must be compared); declare whether relative path tokens resolve
against `--root`. Red fixture required: row-448 text vs `commands[17]` must **not** classify
`exercised_match`.

**G2 template rows.** `SKILL.md:449`'s first backticked span is a template with an optional segment
(`… capture --out <receipt> [--label <L>]`); `<...>` wildcarding cannot match `[--label <L>]`. O: no
custody-pair argv exists in any of the 84 receipt-like blobs under `.ufo/` at `b563c799…`, and no registry
row contains `unexercised`. So row 449 is `unlabelled_variant`; M→0 needs a label or a retained capture
receipt (doc-side, not a new tool). Add the `[...]`/`{...}` rule to the contract instead of leaving it to
the implementer.

**G3 M is under-sized.** My approximation of the contract's classifier over the 7 baseline rows gives
match for 447/487/506/507 and variant for 448/449, and for 450 unless relative anchors resolve. That is
≥2, not the single surviving variant routed at `corpus/lessons/round-16-verifier-spotcheck.md:184`. The
InvocationAudit seat's run is authoritative; C1's "M→0" should quote that number.

**G4 temporal-sweep scope/regex (`contract.md:91-93`).** Two known sites are invisible as specced:
- `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` "pins were unchanged during the run" —
  matches the regex, but the file is not in the site set; only `--extra` reaches it.
- `LOG.md:2012` "hashes remain unchanged across execution" — no alternative matches, and draft row 19
  explicitly covers "across" (`w1/draft-quality-19.md:11`).
Both are already on the correction list (`w1/draft-scorecard.md:32-33`), so after the two visible sites
are corrected the tool would report `unqualified: 0` while these two remain uncorrected → C1's "N→0" is a
false-clean. Cheapest fix: add `remain(s|ed)? unchanged across (the )?(run|execution)` and pass the
knowledge file via `--extra`. Do NOT drop `--extra`.

**G5 pins equality vs record.** `compare.equal` is sha256/size only (`contract.md:16`) while row 19's
record includes `mtime_ns`. A touch-only rewrite reads `equal=true` with differing `mtime_ns`; state
"byte identity at two instants", not stat identity.

**G6 go_version_logged pattern (`contract.md:55`).** "Go version X" must anchor to `GolangSymbolAnalyzer`
(`pilot/esbuild-0.25.12-log/ghidra.log:67`) so it does not match "Untested Go version [1.27.0]"
(`pilot/shfmt-log/ghidra.log:83`, `:87`); otherwise the out-of-range run reports a "logged version" from
its own rejection line.

## Interface gaps (name once; no new tool)

- Run layout: carrier-run takes `--out-dir` (`contract.md:32`), measure counts `W/runs/*/receipt.json`
  (`contract.md:118`; implemented `measure.py:50`, `:139`), and the capability draft requires ≥3 such
  receipts each validated (`w1/ConnCapabilityHistory.md:70`, `:91`). State `DIR = W/runs/<label>` and the
  file name `receipt.json` once.
- `receipt-validate`'s required-field set (`contract.md:108`) is unstated while the producer's set is
  `contract.md:43-47`; two seats write these concurrently. Pin the validator to exactly `contract.md:43-47`.
- Keep carrier-run step 2 `inspect-go-binary` (`contract.md:35`): O, the pilot analyze JSON has **no**
  `build_info` (`pilot/shfmt.json` `normalized_result` = document/image_base/segments/procedure_count/
  string_count), and only `inspect-go-binary` supplies `normalized_result.build_info.go_version` (my 0.64 s
  run). A "simplification" that reads the version from analyze exits 2.
- Provenance inversion worth fixing (not a drop): `contract.md:34` pins the r16 `selection.py` inside
  carrier-run, which never reads it, while `predict.py` does (`contract.md:67`) and the prediction's real
  inputs (selection.py + the selected golang JSON) are unpinned. Move the pin to the prediction
  invocation via `retain.py --pin …`; carrier-run then pins only what it executes. This removes an
  invariance claim for a file outside the run's dependency set (the exact defect class C1 discharges) and
  adds provenance where it is needed.

## Tradeoffs / stop

- T2 loses pool-search provenance (which installed binaries are Go, at which version, package owner).
  That is knowledge-entry evidence, not C1/C2 verification; it is the one drop with a visible cost.
- T1 loses nothing C1/C2 reads: the log already reports the Go analyzer outcome on both carriers
  (`pilot/shfmt-log/ghidra.log:84-85`; `pilot/esbuild-0.25.12-log/ghidra.log:65-67`).
- Next deletion that would harm: any other of the 11 tools in `measure.py:26-38` (T2 aside), or the
  pre/post pin maps. At that point C1's red-case/false-clean check or C2's "mismatches reported, never
  hidden" loses its instrument. I stopped there.

## Searched / not searched

Read: `contract.md`, `claims.json`, `wave1-spec.json` items 0-13 and 76, `wave1-assignments.json`,
`pilot/*` (README, both ghidra.log/script.log, both JSON), baseline `SKILL.md` registry rows, all 84
receipt-like `.ufo/**` blobs at `b563c799…` (argv scan), r16 `selection.py`/`measure.py`/`controls.py`,
and w1 drafts (`draft-scorecard.md`, `draft-quality-19.md`, `ConnCapabilityHistory.md`).
Allowed REA only: `inspect-go-binary --help/--schema` and one `inspect-go-binary /usr/bin/shfmt --format
json`. No analyze/search/decompile, no Ghidra, no carrier execution, no round-17 tool run (none existed at
review start), no other seat's tool.
