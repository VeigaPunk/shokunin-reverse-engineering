PARTIAL — the measured forecast is a clear, non-trivial depth improvement for the defined first-failure task, but “held-out” must be limited to exact-artifact Ghidra outcomes, not pristine artifacts or unseen Go 1.24.6 behavior.

## Axes and measured result

- **Depth/calibration — OBSERVED:** At S, all 19 retained post-run comparisons match with log hashes bound (`.ufo/waves/round-20/evidence/compare-rerun/summary.txt:1-19`). D is the eight predicted failures: `t1246-addr2line`, `compile`, `go`, `nm`, `objdump`, `pprof`, `trace`, `vet`; none failed the forecast, and each observed index is exact (`corpus/knowledge/2026-10-20-r20-go1246-first-failure-forecast.md:28,35-42`). The 11 predicted-silent labels (`asm`, `buildid`, `cgo`, `covdata`, `cover`, `doc`, `fix`, `gofmt`, `pack`, `preprofile`, `test2json`) likewise have no logged Go-analysis failure through log end; none failed (`…forecast.md:43`). Thus k=19/19, D misses=0/8, silence misses=0/11. The all-silent baseline is 11/19 (57.9%) versus 19/19 (100%), +8 correct / +42.1 percentage points; this is not a trivial all-silent forecast (`…forecast.md:28-29`).
- **Coverage — OBSERVED:** The scored set is 19, not all 20 toolchain ELFs: `t1246-link` was excluded before freeze after emulator exit 2 (`…forecast.md:27`; `.ufo/waves/round-20/predictions/carriers.tsv:1-21`). Claims apply to these 19 supported labels only.
- **Timing/measurement — OBSERVED:** Freeze F is timestamped `2026-10-20T18:01:54-03:00`; first run starts 18:02:05 and last ends 18:17:55 (`.ufo/waves/round-20/runs/run-log.txt:1-60`). The original in-run compare step returned 2 for all labels due prediction-envelope mismatch, while the retained comparisons were re-run after the runs using frozen comparator/extractor bytes and frozen emulator outputs, after checking forecast-file equality (`…forecast.md:55-58`). Report 19/19 as the retained frozen-prediction-to-bound-log rerun, not as successful in-run compares.

## Pre-freeze information / held-out scope

- **OBSERVED:** The entry says round 18 ran `inspect-go-binary` (build metadata) on all 20 exact go1.24.6 toolchain ELFs, and expressly says “not version-held-out” (`…forecast.md:14-17`). The R18 census identifies the actual `pprof` ELF by path, digest, REA inspect exit 0 (`.ufo/waves/round-18/evidence/real-carrier-census.json:973-985`) and its pre-freeze census time/method (`:1473-1475`). This metadata identifies artifact/version; it is not a Ghidra first-failure result.
- **OBSERVED:** Before F, the distinct synthetic `s1246-swiss-nethttp` (SHA `5c9faf…`) had a Ghidra log with `invalid_index_reads:[22386945]` (`.ufo/waves/round-18/runs/s1246-swiss-nethttp/observation.json:72-92`), and its comparator matched that prediction (`…/compare.json:51-58`). Same-release failure behavior was therefore already known; a “novel Go 1.24.6 failure” or version-held-out claim would be false. The prior index 22386945 is not among the eight R20 indices (`…forecast.md:35-42`); e.g. actual `t1246-pprof` is SHA `8218e4…` and forecast/observed index 27091201 (`…/predictions/swiss-misread-v2/t1246-pprof.json:21-24,41-49`). No exact prior Ghidra outcome for these 19 target ELFs is evidenced.
- **OBSERVED / INFERENCE:** R18 had already ranked the same `t1246-pprof` ELF second as a likely HTTP-map candidate, explicitly a role-based inference rather than dependency evidence (`…/real-carrier-census.json:1494-1505`). This weakens any “blind label” characterization, but does not establish its first-failure outcome or index.

## Safe knowledge-entry claims

**May claim:** for these 19 Linux/amd64 go1.24.6 toolchain ELF hashes, with REA 6.5.0/Ghidra 12.1.4, frozen H1 forecasts matched the first logged Go-analysis failure’s `kind` and `index`, or silence through the retained log end, 19/19; eight exact `Invalid index` values plus 11 silent cases (`…forecast.md:64-72`). This is outcome-held-out at exact artifact/Ghidra-result level, with previously known build metadata and same-release synthetic evidence disclosed.

**Must not claim:** unseen Go 1.24.6 behavior, fully untouched artifacts, 20/20 coverage, clean REA analysis for every label, successful type recovery, broad Go-version/application generalization, or full first-failure-object accuracy. The comparator checks `kind` and `index`, not `phase`/`va`; “silent” is bounded to the retained log prefix; `t1246-objdump` had REA `execution_failure` from a later Java heap OOM (`…forecast.md:39,50-53,65-72`).

**Smallest safe wording correction:** replace “artifact-held-out” with “held out from prior Ghidra first-failure outcomes”; explicitly add the pre-freeze R18 synthetic `22386945` result and pprof candidate lead. Existing entry already discloses the metadata inspections, non-version-held-out status, link exclusion, and comparator rerun.

## Commands and exit codes (revision-scoped; all reads at S unless F named)

- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show -s --format='%H %cI' 808cbb31a1e24656da5ba4967497e602fbca7415` — exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/evidence/compare-rerun/summary.txt | nl -ba` — `git-show` exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:corpus/knowledge/2026-10-20-r20-go1246-first-failure-forecast.md | nl -ba` — `git-show` exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/runs/run-log.txt | nl -ba` — `git-show` exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/predictions/carriers.tsv | nl -ba` — `git-show` exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-pprof.json | nl -ba` — `git-show` exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-18/runs/s1246-swiss-nethttp/observation.json | nl -ba` — `git-show` exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-18/runs/s1246-swiss-nethttp/compare.json | nl -ba` — `git-show` exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-18/evidence/real-carrier-census.json >/dev/null; printf 'exit=%s\n' "$?"` — exit 0.
