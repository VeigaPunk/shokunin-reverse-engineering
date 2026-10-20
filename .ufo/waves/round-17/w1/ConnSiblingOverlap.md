# ConnSiblingOverlap — round 17 sibling-overlap scan (advisory, read-only)

Scope searched: all 21 `*-shokunin` lanes — 21 `PROVINCE.md`, 18 `SKILL.md` (no `SKILL.md`:
`audio`, `game-dev-2d`, `revenger`), plus the concurrent `kama` r16 and `tameshi` r16 waves,
`revenger` corpus, the r17 pilot, and live host state. Terms: Go binaries / `go1.x` /
`debug/buildinfo` / Golang analyzers / Ghidra / provider / analyzer-log retention.
No sibling file was edited; nothing below is absorbed.

## 1. Who claims the searched ground

| lane | anchor | claim | relation to kaidoku r17 |
|---|---|---|---|
| revenger | `../revenger-shokunin/PROVINCE.md:3-7` | owns RE of shipped artifacts: "native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, browser/Electron runtime evidence" | **direct contest** with kaidoku `PROVINCE.md:3-4` |
| revenger | `../revenger-shokunin/PROVINCE.md:15` | "Host engines as they become available (caller-supplied per REA: Ghidra, IDA, JADX, Binwalk/Unblob, pwntools)" | same engine family kaidoku already holds; claim is eligibility, not availability |
| tsukuroi | `../tsukuroi-shokunin/PROVINCE.md:26`; `:51` (ADJ-06); `:79-81` | routes driver binary RE to "kaidoku/revenger"; ADJ-06 route owner "kaidoku/revenger ownership unresolved"; "both declare shipped-artifact RE. The integrator must arbitrate this shared scope" | third-lane confirmation that ownership is unresolved |
| tabi | `../tabi-shokunin/PROVINCE.md:15` | "reverse engineering as forensics (→ revenger/kaidoku)" | ambiguous pair, no arbiter |
| game-dev-3d | `../game-dev-3d-shokunin/PROVINCE.md:38-41`; `:78` | static inspection only; "contested lane: `revenger`" | names only revenger, not kaidoku |
| kagi | `../kagi-shokunin/PROVINCE.md:63` | "kaidoku reads 1Password binaries statically and tsukuroi tracks the 1Password packages" | single-owner routing to kaidoku |
| tameshi | `../tameshi-shokunin/PROVINCE.md:10-12`; `:34` | **Owns** the method "`kaidoku-shokunin`'s audit-lane pattern (verify: lines, bit-exact evidence ids)" | method ground for C1, not product/domain |
| mori | `../mori-shokunin/PROVINCE.md:22`; `:54` | watchdog log freshness; journal "retention behavior beyond the exact-match refusal" is **Frontier**, not held | no analyzer-log-retention claim |
| souji | `../souji-shokunin/PROVINCE.md:4`; `:34`; `:36`; `:40-41` | owns removal of stale artifacts; excludes "any artifact whose owning lane has dirty or unpushed work" and "Live lane work products (current-round drafts, uncommitted reports)" | does not reach C2's in-round retained logs |
| kama | `../kama-shokunin/PROVINCE.md:1-52`; `SKILL.md:3` | model serving / endpoint drift only; no Ghidra, Go, or RE claim | no contest. r16 advice cites `~/.local/opt/ghidra_12.1.4_PUBLIC` only as an install-path convention (`../kama-shokunin/.ufo/waves/round-16/build/advice/SentinelInstallChain.md:40`; `ConnectKumitate.md:61`) |
| kaidoku | `PROVINCE.md:46-48`; `:52`; `SKILL.md:454-506` | Ghidra 12.1.4 provider (installed, JDK 21); Go ELF cross-version row; Go RTTI / snapshot-selection sections | only lane with Go-analyzer ground |

**Bounded no-finding — Go binaries / `debug/buildinfo`:** no sibling `PROVINCE.md`/`SKILL.md`
claims Go binary analysis, Go build-info parsing, or Go snapshot selection. A repo-wide search for
`go1\.[0-9]|inspect-go|GoApiSnapshot|GoRttiMapper|GolangSymbol|Go carrier|Go ELF` outside
kaidoku's own lane and its fleet-root `.ufo` copies returned no sibling-lane hit. `tsukuroi`'s
`.BUILDINFO` is pacman package metadata,
not Go's `debug/buildinfo` (`../tsukuroi-shokunin/.ufo/waves/round-12/PackageBlind.md:110,:140`);
only a lexical collision, no claim conflict.

**Bounded no-finding — log-retention ground:** no sibling claims retained *analyzer* logs.
`mori` keeps journal retention in its Frontier (`PROVINCE.md:54`); `souji`'s exclusions
(`PROVINCE.md:34,:36`) cover live/unpushed lane work. C2's retained logs are new artifacts under
kaidoku's own tree, not a claim on a sibling surface.

## 2. Contested scope (reported, not resolved here)

### S1 — native / shipped-artifact RE ownership: revenger vs kaidoku
Already named by tsukuroi ADJ-06 (`PROVINCE.md:51,:79-81`) and reported by revenger as
"adjacency (not owned)" (`../revenger-shokunin/LOG.md:777`; `SCORECARD.md:136`).
Neither `PROVINCE.md` contains an arbitration; tsukuroi explicitly refuses to pick.

A second-order hazard travels with it — the two lanes disagree at the fleet level on whether a
Ghidra provider exists on this host, because each uses a different probe:
- **Observation:** `../revenger-shokunin/corpus/knowledge/seed.md:17` records "Host engines
  ABSENT at mint: ghidra, jadx, binwalk, unblob, pwntools"; its appended 2026-10-19
  re-verification keeps F08 as `command -v ghidra` → absent → "holds"
  (`seed.md:63`); checklist rows repeat ABSENT (`2026-10-12-rea-readiness-checklist.md:16,:39`).
- **Observation:** kaidoku records Ghidra 12.1.4 installed with JDK 21 and `rea doctor`
  provider checks (`PROVINCE.md:25,:46-47`); `~/.bashrc:28` exports
  `GHIDRA_INSTALL_DIR="$HOME/.local/opt/ghidra_12.1.4_PUBLIC"`.
- **Observation (this scan):** `command -v ghidra` exits 1, while
  `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` exists. Both records are literally true.
- **Inference:** a PATH probe is not a provider probe for REA — the engine is a directory
  resolved through `GHIDRA_INSTALL_DIR` + `rea doctor`, not a PATH launcher. Any cross-lane
  citation of "Ghidra absent/present" must name the probe, or a fleet reader can mistake
  revenger's mint-era PATH absence for current provider state. This is a calibration defect in
  the shared surface, not a falsity in either lane. Do not edit revenger.

### S2 — evidence-pattern ownership: tameshi C2 vs kaidoku C1(a)
`tameshi PROVINCE.md:10-12` owns the *method* of kaidoku's audit-lane pattern, and its r16
overlap scan says kaidoku r17 C1(a) is repairing exactly the defect class its C2 pin can exhibit;
it requires any citation of the pattern to pin kaidoku baseline `b563c799…` (`claims.json:4`),
"never kaidoku HEAD, and never the in-flight r17 files as landed evidence"
(`../tameshi-shokunin/.ufo/waves/round-16/w1/Overlap2.md:143-149`). It also rules kaidoku r17 is
a candidate second lane for the "pre/post pin map" craft only **after it commits**, not during
(`Overlap2.md:165-166`).
Consequence for kaidoku: C1 is a lane-local provenance repair; it may be cited against tameshi's
prior art but must not claim the pre/post-pin pattern as general, and this round must not cite
tameshi's in-flight C2. No write collision exists.

### S3 — shared `/tmp/rea-ghidra-*` runtime namespace (the actionable one)
- kaidoku already states the boundary: sessions are "shared across lanes — never clean another
  session's dir" (`SKILL.md:39-40`).
- **Observation:** churn is documented, not hypothetical: a fleet-root artifact records a
  persistent `rea mcp` server plus sibling analyses rotating session dirs, each with
  `session.json`/`ownership.json` and a distinct `target_sha256`
  (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaidoku-r2/15-doctor-fresh.md:54-69`).
- **Observation (this scan):** `npx rea-agents@6.5.0 mcp` is live (PIDs 3221/3234, ~36 min);
  no `/tmp/rea-ghidra-*` dirs existed at scan time. Foreign sessions can therefore appear
  between polls.
- **Contract gap:** `contract.md:36-39` records the pre-existing dir set, then copies
  `ghidra.log`/`script.log` from **every NEW dir**; `retained_logs[]` carries
  `{session_dir, files, polls, last_copy_utc}` with no carrier or step binding (`contract.md:44-45`).
  A concurrent sibling or MCP session started mid-run would be copied and, because the log format
  is identical, `log-extract.py` would parse it and the receipt would attribute it to the carrier.
- **The free discriminator is already in the pilot bytes** [observation]:
  each retained log line 2 names its own session dir, and line 46 names the imported target with
  the carrier SHA-256 prefix:
  - shfmt: `pilot/shfmt-log/ghidra.log:2` → `/tmp/rea-ghidra-LuPZRm/ghidra.log`;
    `:46` → `target-58f765638eed.bin`; carrier SHA-256 `58f76563…`
    (`pilot/README.txt:7`).
  - esbuild: `pilot/esbuild-0.25.12-log/ghidra.log:2` → `/tmp/rea-ghidra-r9xmGu/ghidra.log`;
    `:46` → `target-bab29b2ca7a9.bin`; carrier SHA-256 `bab29b2c…` (`pilot/README.txt:8`).
  Both are `target-<sha256[:12]>.bin`, so attribution needs no new tool, no REA call, and no
  sibling cooperation.

## 3. Proposed move (one bounded; synthesis of C1 + C2)

**Bind each retained log to its carrier and step in `W/tools/carrier-run.py`, using the log's own
target filename — the same "name what the evidence proves" discipline C1 applies to time-based
pins, applied here to artifact identity.**

- After each step starts and new dirs are detected, read the candidate `ghidra.log`; accept it only
  if the first `IMPORTING: file://…/target-<hex>.<ext>` name starts with
  `target-<sha256(carrier)[:12]>.` (prefix match; observed suffix `.bin` on two ELF carriers).
- Receipt `retained_logs[]` gains `step_index`, `target_filename`, and
  `attribution: "target-match" | "unmatched" | "no-log-yet"`. Unmatched dirs go to a new
  `foreign_sessions[]` list and are **not** fed to `log-extract.py`.
- Add the red case to `--selftest`: a fake new dir whose log names `target-deadbeef…` must be
  classified `unmatched`, excluded from `retained_logs`, and must not change the exit class.
- Keep the existing `log_capture_limit` wording (`contract.md:46-47`); this proves ownership of the
  captured bytes at the instant of copy, never completeness through the run.

**Affected axes.** Calibration improves: the receipt currently shows "a new session dir existed";
after the move it shows "this log's imported target digest equals the carrier's pinned SHA-256
prefix", which is falsifiable and shown able to fail. Depth improves: multi-verb runs
(`analyze` plus each `--search NAME`) become step-attributable instead of one undifferentiated log
bucket, so the prediction/observation comparison can cite the exact analyzer invocation.
No other axis is harmed: no carrier is added, no sibling repo is touched, no target is run.

**Risks, stated.** (1) Target naming could differ for non-ELF carriers — use a prefix, not an
exact suffix, and report the observed name rather than assuming `.bin`. (2) A dir can vanish before
its first poll; classify `no-log-yet`, count it, and never silently drop it (the contract already
admits final lines can be missed). (3) A sibling analyzing the *same* SHA-256 would pass the
filter; record `session_dir` plus the ownership pid so duplicates are visible, and claim
uniqueness only if those differ. (4) New receipt keys are additive; check that
`receipt-validate.py`'s required-field logic does not reject them before landing.

**Verification.** `python3 -I W/tools/carrier-run.py --selftest` (new red case included, clean);
one pilot-style run with a synthetic foreign session dir created mid-run → `foreign_sessions`
names it, `retained_logs` target matches the carrier, `receipt-validate.py` exits 0; re-run
`log-extract.py` on the retained logs and confirm the pilot diagnostics survive (shfmt
`GoRttiMapper` untested/missing bootstrap at `pilot/shfmt-log/ghidra.log:83-84`; esbuild
`GoApiSnapshot`/`Go version 1.23.12` at `pilot/esbuild-0.25.12-log/ghidra.log:63-64,:67`).
The L1 owns the single sequential carrier run; this seat ran no REA analysis.

## 4. Evidence labels
All path/line content above is observation from read-only reads or from the pinned pilot bytes;
the ownership conflict (S1), the cross-lane reading hazard, and the attribution failure mode are
inference. No sibling file was edited and no arbitration is proposed beyond reporting the conflict
to L1 and, through L1, the integrator.
