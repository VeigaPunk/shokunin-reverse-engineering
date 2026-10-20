HOLDS

# IntermediateFallback — round 18 wave 2 (falsify), author-side advisory reviewer

REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, baseline `9011581d84527ba34c675f9cf912e54d2e72d470`, C3 freeze `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`.
Anchors are `git show REV:<path>` line numbers unless marked otherwise. Everything in this review was read-only: no REA or Ghidra run, no carrier executed, no lane edit. Axes: calibration, operability, depth.
Abbreviations: `K17` = `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`, `K18` = `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md`, `KW` = `.ufo/waves/round-18/runs/real-kimi-webbridge`.

## Verdict: all three parts of the target hold

### 1. The log line exists and is bound to the run (OBS)

- `KW/logs/rea-ghidra-ZSUHpG/ghidra.log` shows:
  - `:68` `WARN (GoApiSnapshot) Falling back from 1.24.13 to 1.24.6 for Go API snapshot`
  - `:69` the `GoRttiMapper` echo of the requested version: `…for version 1.24.13`
  - `:72` `Go version 1.24.13`
  - `:73` `Go analysis failure`
  - `:206` `Invalid index: 15606016`
- The log's sha256 is `fae34819…c5d051`, the same digest the receipt records at JSON paths `/retained_logs/0/files/ghidra.log` and `/steps/analyze/retained_logs/0/files/ghidra.log`. The analyze Evidence ID is `ev_3d0da594…5c320b4096`.
- `KW/observation.json`:
  - `:18-22` is the extracted WARN record.
  - `:91` is `snapshot_route: "fallback"`.
  - `snapshot_fallbacks` is `[{"from":"1.24.13","to":"1.24.6"}]`.
- The prediction was frozen before the run:
  - It was frozen at `eb6c2668` (13:23:55 -0300). That commit is an ancestor of REV, and the prediction file is byte-identical at REV (`cmp` exit 0).
  - It sets `fallback_to: "1.24.6"` (`.ufo/waves/round-18/predictions/real-kimi-webbridge.prediction.json:31`) and `snapshot_route: "fallback"` (`:34`).
- The run lasted 13:31:09–13:32:10 -03 (`runs/run-log.txt`). `KW/carrier-run.exit` and `KW/compare.exit` are both `0`.
- Why the target is 1.24.6: the installed 1.24 patch diffs stop at `go1.24.6.json.diff`, and the receipt pins exactly `go1.24.0.json` plus diffs 1.24.1–1.24.6. The r15 source model predicted this route in advance (`.ufo/waves/round-15/w1/ReviewPatchCases.md:52`, R3: "1.24.7+ would hit this with 1.24.6").

### 2. r17 listed this route as unexercised (OBS)

- `K17:185-187`: "Fallback to an intermediate patch diff (e.g. 1.24.7+ → 1.24.6): no host carrier exercises it."
- `K17:129` agrees: "Only fallback to the base (Y = M.m.0) was observed … fallback to an intermediate diff was never observed".
- `SKILL.md:524` agrees: "Only fallback to the base (Y = M.m.0) was observed".
- `git log -S` shows that all three first appeared in `d0ab2992` (2026-10-20 11:47:24 -0300). They are absent at `da64646` and present unchanged at baseline `9011581` and at REV.

### 3. "first observed" is correct across the corpus (OBS, bounded)

- The claim appears in two places:
  - `corpus/README.md:35`: "plus the first observed intermediate patch fallback (1.24.13→1.24.6)"
  - `LOG.md:2157-2158`: "kimi-webbridge also exercised the first intermediate patch fallback (WARN 1.24.13 → 1.24.6)"
- REV retains 26 `ghidra.log` files. Five contain a `GoApiSnapshot` fallback WARN:
  - Four fall back to the base: r17 `pro-aether:92` and `pro-notesmd-cli:68`, r18 `calib-aether:92` and `calib-notesmd-cli:68` (all `→1.25.0`).
  - Only `KW/…/ghidra.log:68` falls back to a nonzero patch.
- Every other intermediate-form string at REV is source-derived or a model output:
  - r15 `PatchLookup.md:155-160`, "Case C (e.g. 1.21.14 → 1.21.13)". This is a source trace; the seat ran no live binary (`:3`).
  - r17 `w1/ScoutGoDataInventory.md:140`, labelled "derived, not observed".
  - r17 `w2/route-diff.json:3436-3448`, a model-vs-predict sweep row for 1.24.13 (`agree: true`).
  - r16 source-model lines `LOG.md:1934-1937` and `:1995-1999` (`source_model, patch_applied:false`).
- The assignment's grep returns 5 hits:
  - Primary: `ghidra.log:68`.
  - Derived from it: `observation.json:21-22`.
  - Citation of it: `K18:81`.
  - Hypothetical: `w1/DraftSwissTable.md:27`, a mismatch-signal row "1.24.6 → 1.24.0" that no retained log contains.
- The working tree adds 7 files after REV. All are wave-2 artifacts that re-cite `ghidra.log:68`.
- None of the 20 sibling `*-shokunin` lanes contains an intermediate-form string.

## Findings (adjacent; none breaks the target claim)

### F1 — MEDIUM (calibration): r17's host-wide absence claim was false when written and is still uncorrected at REV

- **What r17 claimed.** `K17:185-186` says "no host carrier exercises it". It was written at `d0ab2992` (2026-10-20 11:47:24 -0300).
- **The carrier was already on the host.**
  - OBS: `stat /home/vgpnk/.kimi-webbridge/bin/kimi-webbridge` shows birth 2026-10-11 10:39:40 -0300 and ctime 2026-10-11 10:39:44.84 -0300.
  - OBS: its sha256 is `71067480…f8ad35d`, equal to `K18:52` and the r18 receipt.
  - INFERENCE: userspace cannot set ctime, so these bytes have been unchanged on the host since 9 days before r17 wrote the claim. System-clock manipulation is not excluded.
- **The Ghidra data needed for the route was the same at r17 run time (OBS).** The r17 `runs/pro-aether/receipt.json` and the r18 `KW/receipt.json` pin identical digests:
  - `go1.24.0.json`: `aab28c8f…e124c571`
  - `go1.24.6.json.diff`: `e169e8dd…dd9cded6`
- **Why r17 missed it (OBS).** r17's census roots, listed at `.ufo/waves/round-17/w1/CriticSampleSize.md:5`, were `/usr/bin /usr/lib /usr/local /opt ~/.local/bin ~/go ~/.cargo/bin ~/Projects ~/.npm ~/.cache`. They exclude `~/.kimi-webbridge`. r18 found the carrier only after widening its scan to `/home …` (`.ufo/waves/round-18/w1/RealCarrierCensus.md:14-16,44-47,68-69`).
- **What the claim actually supports.** The statement held only within r17's census roots. It is false under its plain reading as a statement about the host. Under a narrow reading ("none of r17's carriers") it is true, but then "host" is the wrong scope word.
- **No correction exists at REV (OBS):**
  - The `K17` "Round-18 correction" section (`:200-206`) has 0 lines mentioning 1.24.13, kimi or intermediate.
  - `corpus/lessons/round-17.md` and `round-18.md` record no census-scope miss.
  - `K18:51-53` presents kimi as "the only non-r17 Go 1.24/1.25 ELF on the host" without noting that r17's census missed it.
- **Effect.** "first observed" stays true, because existing on the host is not the same as being observed in a run. But the r17 entry still states something false about the host.
- **Advisory fix.** Append one named line to `K17` "Round-18 correction": `:185-186` held only for the census roots in `CriticSampleSize.md:5`; `kimi-webbridge` (go1.24.13, ctime 2026-10-11) was present and exercises the route (`KW/…/ghidra.log:68`).
- **Reproduce:** B6, B8, B9, B11 and B7a below.

### F2 — LOW (calibration/consistency): live guidance still says only base fallback was observed

- **SKILL.md:524 (OBS).** Its Limit column still reads "Only fallback to the base (Y = M.m.0) was observed".
- **The same table was otherwise updated at REV (OBS).**
  - REV qualified row `:528` of this table in place with a "Round 18: replayed and confirmed" note.
  - `LOG.md:2164-2166` lists which SKILL rows were aligned. Row 524 is not among them, so this is an omission, not a misstatement by LOG.
- **The r18 SKILL section does not mention it (OBS).** `SKILL.md:548-561` has 0 lines mentioning intermediate, 1.24.13, 1.24.6 or the fallback.
- **The r17 entry has no forward pointer (OBS).** `K17:129` ("never observed") was true for r17's runs but carries no pointer to the r18 observation.
- **Effect.** At the same REV, a reader of the decision table is told the opposite of `corpus/README.md:35` and `LOG.md:2157-2158`.
- **Advisory fix.** Qualify `:524` in place, the way `:528` was qualified.
- **Reproduce:** B5b, B6b and B7b below.

## Reproduction (lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `R=b2aad08…`, `set -o pipefail`)

| # | Command | Exit | Observed |
|---|---|---|---|
| G | `git grep -n 'Falling back from 1.24' $R` | 0 | 5 hits (classified above) |
| A1 | `git show $R:KW/logs/rea-ghidra-ZSUHpG/ghidra.log \| awk 'NR==67\|\|NR==68\|\|NR==69\|\|NR==72\|\|NR==73\|\|NR==206'` | 0 | lines quoted above |
| A2 | `git show $R:KW/logs/rea-ghidra-ZSUHpG/ghidra.log \| sha256sum` | 0 | `fae34819…c5d051` |
| A3 | `git show $R:KW/receipt.json \| python3 -I -B -c '<walk: ghidra.log sha256, evidence_id>'` | 0 | same digest ×2; `ev_3d0da594…` |
| A4 | `git show $R:KW/observation.json \| python3 -I -B -c '<print route fields>'` | 0 | `fallback`; `1.24.13→1.24.6`; `invalid_index_reads [15606016]` |
| A5 | `git merge-base --is-ancestor eb6c2668… $R`; `cmp <(git show eb6c2668…:$P) <(git show $R:$P)` | 0; 0 | frozen before the run; byte-identical |
| A7 | `git show $R:KW/carrier-run.exit $R:KW/compare.exit`; run-log rows | 0 | `0`/`0`; 13:31:09–13:32:10 -03 |
| B1 | `git ls-tree -r --name-only $R \| awk '/ghidra\.log$/' \| wc -l` | 0 | 26 |
| B2 | `git grep -n 'WARN  (GoApiSnapshot) Falling back from' $R -- '*ghidra.log'` | 0 | 5 lines: 4 `→1.25.0`, 1 `→1.24.6` |
| B3 | `git grep -nE 'Falling back from [0-9]+\.[0-9]+\.[0-9]+ to [0-9]+\.[0-9]+\.[1-9]' $R` | 0 | 6 hits: kimi log/observation ×2, `K18:81`, two source-derived docs |
| B4 | `git grep -n 'first observed intermediate' $R`; `git show $R:LOG.md \| awk 'NR==2157\|\|NR==2158'` | 0; 0 | `corpus/README.md:35`; `LOG.md:2157-2158` |
| B5 | `git show $R:K17 \| awk 'NR==129\|\|(NR>=185&&NR<=187)'`; b: `git show $R:SKILL.md \| awk 'NR==524'` | 0; 0 | quoted above |
| B6 | `git log -S'Fallback to an intermediate patch diff' --format='%H %ci' $R -- K17`; b: same with `-S'Only fallback to the base (Y = M.m.0) was observed' -- SKILL.md` | 0; 0 | `d0ab2992… 2026-10-20 11:47:24 -0300` (both) |
| B7 | a: `git show $R:K17 \| awk 'NR>=200 && /1\.24\.13\|kimi\|intermediate/' \| wc -l`; b: `git show $R:SKILL.md \| awk 'NR>=548&&NR<=561&&/intermediate\|1\.24\.13\|1\.24\.6\|[Ff]alling back/' \| wc -l` | 0; 0 | 0; 0 |
| B8 | `stat -c 'birth=%w mtime=%y ctime=%z' ~/.kimi-webbridge/bin/kimi-webbridge`; `sha256sum` (same path) | 0; 0 | birth/ctime 2026-10-11; `71067480…` |
| B9 | `git show $R:.ufo/waves/round-17/w1/CriticSampleSize.md \| awk 'NR==5'` | 0 | census roots exclude `~/.kimi-webbridge` |
| B10 | `ls <ghidra>/…/typeinfo/golang/patchverdiffs/ \| awk '/^go1\.24\./'` | 0 | `go1.24.1`…`go1.24.6` diffs only |
| B11 | r17 `pro-aether/receipt.json` vs r18 `KW/receipt.json`, `python3 -I -B` digest walker | 0; 0 | identical `go1.24.0.json` / `go1.24.6.json.diff` digests |
| W | `LC_ALL=C comm -13 <(git grep -l 'Falling back from' $R \| sed 's/^[^:]*://' \| sort) <(git grep -l --untracked 'Falling back from' \| sort)` | 0 | 7 post-REV wave-2 files. A first run without `LC_ALL=C` warned "not in sorted order" and exited 1 with the same list |
| X | `git check-ignore -v kaidoku-shokunin` (fleet root, read-only) | 0 | `.gitignore:1:*-shokunin/` |
| Y | harness grep tool, B3 pattern, over the 20 sibling `*-shokunin` lane roots | — | No matches. The same regex finds the kimi hits when aimed at this lane |

## Residual risk and verification gaps

- **Route observed, content not.** The WARN line proves the route. It does not prove that the 1.24.6 diff bytes were applied: the receipt pins only that the file is present (`e169e8dd…`), and `K17:183-184` (no log of applied bytes) still applies. "first observed intermediate patch fallback" is accurate as a route observation; a reader should not take it as a patched-content observation.
- **One pass only.** The kimi run was a single pass (`K18:116`). I did not rerun REA (contract).
- **Search scope.** Absence claims cover the lane's Git objects at REV plus untracked working-tree files. The sibling sweep respects each lane's `.gitignore`. Ghidra session directories under `/tmp` and other host paths were not searched.
- **F1 rests on ctime.** The claim that the carrier's bytes were present on the host at r17 time comes from ctime (INFERENCE).

## Tool installs / writes

- Tool installs: none.
- Writes: only this report.
