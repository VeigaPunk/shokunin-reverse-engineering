# ScoutArgvDecoy — analyze-step identity in receipt-validate.py (D6d calibration)

Seat: KaidokuR20.ScoutArgvDecoy-2 (read-only). Baseline: `14f0260ad319ecc26994381b2415d5a999003375`
(`git log -1`: `2026-10-20 17:24:21 -0300 round-19 verifier spot-check (integrator, hyaku)`).
Written 2026-10-20T17:50:49-03:00. Labels: **[OBS]** executed/read, **[INF]** inferred.
All experiments ran on the baseline blob extracted from Git into `tempfile.mkdtemp()`
(`/tmp/argvdecoy-lq97cma0`, since removed); no Go/REA/Ghidra execution; only `python3 -I -B` on the
copied validator.

Provenance of the analysed bytes **[OBS]**:
```
$ git -C LANE show 14f0260:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum
6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762  -        (exit 0)
$ sha256sum LANE/.ufo/waves/round-17/tools/receipt-validate.py
6afb7ef6600cdc79... (same)                                                (exit 0)
$ python3 -I -B <copy>/receipt-validate.py --selftest
SELFTEST: CLEAN cases=26                                               (exit 0)
```
The blob was introduced by round-19 wave-two `279e8b19c51658bfd05b9e31a1c0894ab2e70537`
("round-19: wave-two fixes — list identity, alias classifie…", tool sha256 prefix `6afb7ef6600cdc79`);
`279e8b19` is an ancestor of the baseline (`git merge-base --is-ancestor 279e8b19 14f0260` → exit 0) **[OBS]**.

## 1. How the analyze step is identified, by `steps` shape **[OBS]**

Entry point `verify_mid_maps` (`receipt-validate.py:490-631`); identity only matters when
`--require-mid-maps` is set (`:607`), and the flag also requires every `pin_checks` entry to be
map-bearing (`:552-556`). `classify` (`:113-125`) labels a dict receipt with `steps` plus a dict
`carrier` as `carrier`; `_iter_steps` (`:127-131`) addresses object steps as `$.steps.<key>` and list
steps as `$.steps[i]`.

**Object-shaped `steps` (`:611-613`)** — identity is the mapping key alone:
```python
astep = steps.get("analyze")
ok = isinstance(astep, dict) and bool(astep.get("pin_checks"))
```
`argv` is never read on this path. Any key literally named `analyze` with a non-empty `pin_checks`
list satisfies D6d's pre-fix identity test, whatever the step actually ran.

**List-shaped `steps` (`:614-623`)** — no key, so the entry must self-identify via
`_is_analyze_step` (`:134-161`), and exactly one entry may do so (`len(named) == 1`, `:621`):
- declared label: `step`/`name` equal to `"analyze"` (`:145-147`), and
- argv subcommand: first token fullmatching `rea-agents@\d+\.\d+\.\d+` → next token must equal
  `analyze` (`:153-156`); else, if `basename(argv[0])` is `rea` or `rea-agents`, `argv[1]` is the
  subcommand (`:157-158`); if neither yields a command, `return bool(declared)` (`:161`).

Observed consequences of that control flow:
- The package-token scan starts anywhere in argv, so a package-shaped *argument* becomes the package
  token if it precedes the real one.
- `basename(argv[0])` in `{rea, rea-agents}` is accepted as authority (`:157`), so any executable
  with that name authenticates without any `rea-agents@<version>` token.
- A label-only entry (no argv, or argv with no discoverable command) returns `True` (`:161`).
  Selftest case 4m asserts this is green (`:1093-1103`, `carrier_flag_list_declared_name_green`).
- When no list entry self-identifies, `where` keeps its object-style default
  `"$.steps.analyze.pin_checks"` (`:610`, `:622`), so the finding names a non-existent object path
  for list receipts (cosmetic, observed in negative control N1 below).

**Finding emitted when identity fails:** only `mid_checks_absent` (`:626-630`). No
`analyze_step_unauthenticated` string exists at the baseline
(`git show 14f0260:… | grep -c analyze_step_unauthenticated` → `0`, exit 1) **[OBS]**.

## 2. Exact decoy receipt that passes at the baseline **[OBS]**

Built in mkdtemp as a fully self-consistent carrier receipt: real `carrier.bin` (sha256 `S`, md5 `M`),
real `sess/ghidra.log` containing the three lines `check_binding` requires (`:204-218`):
```
2026-10-20 120000 INFO  (LoggingInitialization) Using log file: <tmp>/sess/ghidra.log
2026-10-20 120001 INFO  (HeadlessAnalyzer) IMPORTING: file://<tmp>/sess/target-<S[:12]>.bin
Loading file://<tmp>/sess/target-<S[:12]>.bin?MD5=<M>
```
plus `bound_sessions:["<tmp>/sess"]`, matching `retained_logs`, `pins_pre`/`pins_post` from
`pins.snapshot([carrier])`, `pins_compare` from `pins.compare`, and one mid map
`<tmp>/mid.json = pins.snapshot([carrier])`. Steps are the **object** shape (the shape of all 40
retained lane receipts); the only lie is the `analyze` step's argv:

```json
"steps": {
  "inspect-go-binary": { "argv": ["npx","-y","rea-agents@6.5.0","inspect-go-binary",
                                   "<tmp>/carrier.bin","--format","json"], "...": "normal step fields" },
  "analyze": { "argv": ["npx","-y","rea-agents@6.5.0","inspect-go-binary",
                         "<tmp>/carrier.bin","--format","json","analyze"], "...": "same step fields",
               "pin_checks": [{ "taken_at_utc": "<mid.taken_at_utc>", "equal": true,
                                "changed": [], "missing": [], "entries": 1,
                                "map_path": "<tmp>/mid.json", "map_sha256": "<sha256(mid.json)>" }] }
}
```
`decode()` calls this the "analyze" step; nothing else in the receipt is forged — the map digest,
`pins.compare` verdict, log binding, and every path/sha pair re-verify. The `analyze` argv is
byte-for-byte selftest case 4n's *rejected* list entry (`:1108`), moved from a list slot into the
object key, where `_is_analyze_step` is never called.

Result **[OBS]**:
```
$ python3 -I -B <copy>/receipt-validate.py --require-mid-maps <decoy>.json
{"tool":"receipt-validate.py", ..., "counts":{"receipts":1,"valid":1,"invalid":0,"unreadable":0},
 "exit":0}                                                                            (exit 0)
```

Full variant matrix (same builder, `--require-mid-maps`, findings list `code:where`):

| # | shape | analyze identity in decoy | exit | findings |
|---|-------|---------------------------|------|----------|
| V1 | object | key `analyze`; argv `[…inspect-go-binary, …,"analyze"]` (trailing decoy) | **0** | `[]` |
| V2 | object | key `analyze`; argv `["rea","search","carrier","analyze"]` | **0** | `[]` |
| V3 | list | `["rea","analyze"]` (basename route, `:157`) + map checks | **0** | `[]` |
| V4 | list | `name:"analyze"`, argv `["true"]` (label-only, `:161`; = case 4m) | **0** | `[]` |
| V5 | list | control: genuine `["npx","-y","rea-agents@6.5.0","analyze",<carrier>,"--format","json"]` | 0 | `[]` |
| V8 | list | `name:"analyze"`, argv `["npx","-y","rea-agents@6.5.0"]` (label survives `command=None`) | **0** | `[]` |
| V9 | list | `["/tmp/rea-agents","analyze"]` (basename of an arbitrary path) | **0** | `[]` |
| V10 | object | key `analyze`, argv `["npx","analyze"]` (the selftest's own green fixture) | **0** | `[]` |
| N1 | list | control: `[…inspect-go-binary,…,"analyze"]` + map checks | 1 | `mid_checks_absent:$.steps.analyze.pin_checks` |
| N2 | object | control: empty `analyze.pin_checks`, map checks on another key | 1 | `mid_checks_absent:$.steps.analyze.pin_checks` |
| N3 | list | control: genuine argv, no checks | 1 | `mid_checks_absent:$.steps[1].pin_checks` |

V1 is the one-line counterexample to D6d: the exact token arrangement the list branch already
rejects (`:1108`, `list_identity_argument_red`) is accepted verbatim under the object key. **[OBS]**
**[INF]** Fixing only `_is_analyze_step` leaves V1/V2/V10 green, because the object branch never calls
it; the argv predicate must gate both branches.

## 3. Every retained round-18/19 analyze argv (must stay valid)

`find` reports 23 `receipt.json` files under the two scoped globs (15 round-18, 8 round-19 pass2);
the two `run-log.txt/receipt.json` strings that a shell glob can hand the validator are not files
(`find … -type f | wc -l` → 23) **[OBS]**. All 23 use **object** `steps` with key `analyze`; every
analyze argv is the same strict npx form, package at index 2, subcommand at index 3:

`["npx","-y","rea-agents@6.5.0","analyze", <carrier-arg>, "--format","json"]`

| receipt (round-18/runs/…) | `<carrier-arg>` | analyze pin_checks (all map-bearing) |
|---|---|---|
| calib-aether | `/usr/bin/aether` | 3 |
| calib-notesmd-cli | `/home/vgpnk/.local/bin/notesmd-cli` | 2 |
| real-kimi-webbridge | `/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge` | 2 |
| s1246-noswiss-methods | `…/kaidoku-r18/carriers/s1246-noswiss-methods` | 1 |
| s1246-noswiss-nethttp | `…/carriers/s1246-noswiss-nethttp` | 2 |
| s1246-noswiss-nomethods | `…/carriers/s1246-noswiss-nomethods` | 1 |
| s1246-swiss-methods | `…/carriers/s1246-swiss-methods` | 1 |
| s1246-swiss-nethttp | `…/carriers/s1246-swiss-nethttp` | 1 |
| s1246-swiss-nomethods | `…/carriers/s1246-swiss-nomethods` | 1 |
| s1250-noswiss-methods | `…/carriers/s1250-noswiss-methods` | 1 |
| s1250-noswiss-nethttp | `…/carriers/s1250-noswiss-nethttp` | 2 |
| s1250-noswiss-nomethods | `…/carriers/s1250-noswiss-nomethods` | 1 |
| s1250-swiss-methods | `…/carriers/s1250-swiss-methods` | 1 |
| s1250-swiss-nethttp | `…/carriers/s1250-swiss-nethttp` | 2 |
| s1250-swiss-nomethods | `…/carriers/s1250-swiss-nomethods` | 1 |
| **round-19/runs/pass2/** t1250-asm | `…/go-1.25.0/pkg/tool/linux_amd64/asm` | 3 |
| t1250-cgo | `…/linux_amd64/cgo` | 2 |
| t1250-compile | `…/linux_amd64/compile` | 6 |
| t1250-cover | `…/linux_amd64/cover` | 2 |
| t1250-go | `…/go-1.25.0/bin/go` | 4 |
| t1250-gofmt | `…/go-1.25.0/bin/gofmt` | 1 |
| t1250-preprofile | `…/linux_amd64/preprofile` | 1 |
| t1250-vet | `…/linux_amd64/vet` | 2 |

Census command (exit 0) applied the strict predicate — first `rea-agents@x.y.z` token at index `i`,
`argv[i+1]=="analyze"` — to the `steps.analyze` of each file: `all_strict_npx: True`, one version
(`6.5.0`), one shape (`object`). Lane-wide `glob(".ufo/**/receipt*.json")` finds 41 files; 40 have
`steps` and **all 40** are object-shaped with this strict argv (the extra 17 are round-17/runs,
round-17/verify/replicate and round-19/runs duplicates); 1 (`interactive-r1/receipt-binding-observation.json`)
has no `steps` **[OBS]**. Therefore a fix that requires the npx form on both branches rejects none of
the retained receipts.

**Pre-existing red, unrelated to D6d [OBS]:** running the baseline validator with
`--require-mid-maps` over the exact 23 paths gives `exit 1`, `{"receipts":23,"valid":8,"invalid":15}`,
findings only `sha256_mismatch`+`size_mismatch` (15 each). All 15 round-18 receipts pin
`.ufo/waves/round-17/tools/receipt-validate.py` itself at the round-18 blob
(`70672eb3bd0c06e9…`, commit `eb6c2668`), while the live file at the baseline is `6afb7ef6…`
(round-19 wave-two). The 8 round-19 pass2 receipts validate clean. "Keep them valid" therefore means
*add no identity rejection*; their byte pin cannot be made green without repinning.

## 4. Fix constraints observed in the current selftest (D6d landing)

If the strict npx predicate gates both shapes, these baseline fixtures/fixtures' expectations must be
edited in the same patch, or `--selftest` goes red **[OBS]**:
- `:989-996` case 4h (`carrier_flag_mid_map_green`) builds `steps["analyze"].argv=["npx","analyze"]`
  (no package token) and expects exit 0 → must use the full npx form.
- `:1008` case 4i and `:1030` case 4j use the same bare argv; they expect exit 1, but 4i asserts the
  specific code `mid_checks_absent`, so identity must not short-circuit that finding for an empty
  `pin_checks` list.
- `:1093-1103` case 4m (`carrier_flag_list_declared_name_green`) asserts the label-only route is
  green — directly contradicted by "authenticated only when its argv has the token `analyze`
  immediately after the package token"; it must become the red case (or be renamed and repurposed).
- Docstring promises at `:34-40` and `:137-141` describe the label/basename routes and must be
  rewritten.
- New case `argv_decoy_refused` (contract D6d) should assert V1 and/or N1 exit 1 with
  `analyze_step_unauthenticated`; when no list entry authenticates, `where` should name the offending
  index rather than the object-style default at `:610`.

## 5. Remaining unknowns / limits

- Whether L1 wants the object-key requirement kept *in addition to* the argv predicate (keeps the
  `$.steps.analyze` anchor) or replaced by a scan for an authenticated step anywhere in the mapping
  **[INF]**: keeping both is compatible with all 40 retained receipts.
- Whether `analyze_step_unauthenticated` should replace `mid_checks_absent` or be added alongside it;
  4i/4k currently require `mid_checks_absent` when the authenticated analyze entry has no checks
  **[OBS]**.
- Version regex accepts only `digits.digits.digits`; `rea-agents@latest`/prerelease argv would be
  rejected by any strict fix (no retained receipt uses them — all `6.5.0`) **[OBS]**.
- The decoy was executed on the extracted baseline blob only; no patch was written and no full-lane
  validator run beyond the read-only receipt sweep above.
