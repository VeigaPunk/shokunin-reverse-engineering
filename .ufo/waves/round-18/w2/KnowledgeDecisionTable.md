PARTIAL

# KnowledgeDecisionTable — round 18 wave 2 (falsify)

Seat `KaidokuR18.KnowledgeDecisionTable` (author-side advisory reviewer; this is a recommendation, not an admission).
Assigned revision (REV) `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`; freeze `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`; baseline `9011581d84527ba34c675f9cf912e54d2e72d470`.
Targets:
- the decision table in `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:90-97` ("entry" below);
- `SKILL.md:548-561` ("Swiss-map misread replay — round 18").

Both are cited from `git show REV:<path>`. For every cited file the working tree equals REV: `git diff --quiet b2aad08 -- .ufo/waves/round-18/runs .ufo/waves/round-18/predictions corpus/knowledge/2026-10-20-r18-swiss-map-replay.md SKILL.md` exited with rc 0, and all 15 `ghidra.log` files are tracked.

Axes:
- (A) each row is backed by observed counts;
- (B) the row is labelled INFERENCE where it goes beyond observation;
- (C) the row's scope matches its evidence;
- (D) operability: a reader can follow the row's instructions as written.

## Row verdicts

| Entry row | SKILL.md | Observed support | Label | Verdict |
|---|---|---|---|---|
| :94 Swiss + `Go analysis failure` + `Invalid index`/`read past EOF` → run `swiss-misread.py`; exact H1 ⇒ `OldMapType` binding | :559 | 3 failing carriers (aether calibrated; s1246-swiss-nethttp and kimi held out). My separate byte decode of the name records reproduces all 3 reads exactly (V3). Ghidra 12.1.4 in 15/15 logs; x86-64 ELF ×3 | "the cause is" carries no label | Counts HOLD; wording F4 |
| :95 same failure on noswiss → not this mechanism | :560 | 0/6 noswiss logs fail; 6/6 carry `X:noswissmap` | Deduced from source; the signal was never observed | HOLDS |
| :96 Swiss, no failure → not evidence of correct layout | :561 | 3 Swiss no-failure labels with emulated silent misreads (4 map types); byte decode shows pkgPath-free names; 0 swiss-only WARN/ERROR classes across 5 twin pairs | INFERENCE ✓ | Support and label HOLD; scope F2, condition F3 |
| :97 "fails on one Go patch and not another (s1246 vs s1250 nethttp)" | absent | 1 pair, and it spans two minor releases | No count; not labelled | BROKEN as worded (F1) |

## Findings (by severity)

**F1 MEDIUM — row :97 names the wrong variable, its decision text is contradicted by its own example, and it has no count.**
- Observation: s1246-swiss-nethttp is `go1.24.6` and s1250-swiss-nethttp is `go1.25.0`. They differ in **minor** version and in snapshot base (`go1.24.0.json` vs `go1.25.0.json`); they are not two patches. No same-minor, different-patch pair was run. The only other 1.24.x carrier is kimi (1.24.13), which is a different program.
- Observation: both carriers come from the same source, `carriers/src/nethttp`, through the same loop at `carriers/build.sh:15-24`. Under the two toolchains the record at types+40 differs: flags `0x6d` (has pkgPath) vs `0x62` (no pkgPath) (V3).
- Consequence: "not on the Go version" is false in letter. The Go version changed the outcome *through* those bytes.
- Supported reading: "the Go version alone does not predict the outcome; the bytes at types+SlotSize do". That rests on n = 1 observed pair; the within-carrier slot variation in aether and kimi is emulated, not logged.
- The Limit "Do not generalize '1.25.0 is safe'" is supported: aether (1.25.14, snapshot 1.25.0) failed.
- The row is missing from the SKILL.md table (`SKILL.md:557-561`), so readers of SKILL.md lose that caution.
- Repro: `git show b2aad08:.ufo/waves/round-18/predictions/decision-rule.json | python3 -I -B -c "import json,sys; t=json.load(sys.stdin)['table']; print([(r['label'],r['go_version'],r['h1'],r['invalid_index_reads_h1']) for r in t if r['label'] in ('s1246-swiss-nethttp','s1250-swiss-nethttp','real-kimi-webbridge')])"`
  - rc 0.
  - Output: `('s1246-swiss-nethttp','go1.24.6','invalid_index',[22386945]), ('s1250-swiss-nethttp','go1.25.0','none',[])`.
  - The byte half of the evidence is V3.

**F2 LOW — row :96 / SKILL.md :561 state amd64-only derivations as universals ("the name at `types+SlotSize`", "`Mcount` always reads 0").**
- Observation (amd64): 18/18 emulated misread map types have `mcount 0` and `pkg_path` equal to the slot size. The source is the frozen `predictions/swiss-misread/*.json`, `per_type[].h1.ghidra_uncommon`.
- Observation (the emulator's own layout law on the installed snapshot):

  | Arch | `OldMapType` | `SwissMapType` | Uncommon read at | PkgPath reads | Mcount reads | Moff reads |
  |---|---|---|---|---|---|---|
  | amd64 | 88 B | 112 B | desc+88 | `SlotSize[0:4]` | `SlotSize[4:6]` | `ElemOff[0:4]` |
  | 386 | 56 B | 64 B | desc+56 | `ElemOff` | `Flags[0:2]` | past the descriptor |

- [INFERENCE] On 32-bit, the misread name sits at types+**ElemOff**, and Mcount equals the low 16 bits of `Flags`. The Flags bits 0-3 are NeedKeyUpdate, HashMightPanic, IndirectKey and IndirectElem (`/home/vgpnk/.local/opt/go-1.24.6/src/internal/abi/map_swiss.go:42,47-50`), so Mcount need not be 0 there. No 32-bit carrier was run.
- The entry discloses 32-bit as not examined (`:113`). Row :96's Limit still omits the "x86-64 ELF" scope that row :94 carries.
- Repro: `eval "python3 -I -B - <<'EOF' …importlib-load .ufo/waves/round-18/tools/swiss-misread.py; Layout(load_snapshot_types(go1.24.0.json,'linux',arch),ptr) for (amd64,8),(386,4)… EOF"` (full text in V5).
  - rc 0.

**F3 LOW — row :96's failure condition is narrower than H1 (`:29-33`) and narrower than the source.**
- Observation: `GoName.readStructure` reads, in order (`Base-src.zip:…/rtti/GoName.java:94-101`):
  - the flags byte (`:94`);
  - the name varlen (`:95`);
  - the tag varlen when HAS_TAG is set (`:96-98`);
  - pkgPath (`:99-101`).

  Any of the varlen reads can throw EOF whether or not pkgPath is set.
- Observation: each of the 3 logged failures happens in the record reached through `GoName.getPkgPath(GoName.java:124)`:
  - aether `ghidra.log:196` (EOF at `:95`);
  - kimi `:220` (`:94`);
  - s1246 `:465` (`:94`).

  The row is therefore not contradicted by any run.
- Observation: the first-level record had HAS_TAG set in aether (`0x954048`, flags `0x6e`), kimi (`0x882028`, `0x67`) and s1250-swiss-nethttp (`0x552028`, `0x62`). In all three, a tag read was performed on misread bytes — a failure path that "silent unless … carries a pkgPath" leaves out.
- Suggested wording: "silent unless decoding the record at types+SlotSize, or the record its pkgPath names, runs out of bounds".
- Repro: V3 (rc 0), plus `unzip -p …/Base-src.zip ghidra/app/util/bin/format/golang/rtti/GoName.java | sed -n '92,125p'` (rc 0).

**F4 LOW — row :94's attribution evidence is understated, and the causal claim is unlabelled.**
- Observation: kimi, like aether, reaches the bad read through struct/interface markup:
  - kimi: `GoStructType.additionalMarkup` ×4 and `GoInterfaceType.additionalMarkup` ×3 (kimi `ghidra.log:100,114,123,136,…`);
  - aether: ×1 and ×2;
  - s1246: ×0 and ×0.

  The entry's INFERENCE bullet (`:101-106`) reports this path for aether only, so it is observed in 2/3 failures, not 1/3.
- Observation: `GoMapType` frames appear 0/3 and `GoUncommonType` frames 0/3. The map path is never visible in a stack trace, so attribution rests on three things:
  - the exact-read fingerprint (which is exactly what row :94 requires — this part of the design is good);
  - one carrier-side minimal pair (s1246 swiss vs noswiss);
  - one route control (s1246 used the exact `INFO 1.24.6` snapshot and still failed).
- "The cause is" has no reader-side intervention: the entry states that PR #9348 was not tested (`:107-108`).
- Suggested Limit: "read fingerprint + 1 minimal pair; no reader-side fix tested".
- Repro: `for d in calib-aether real-kimi-webbridge s1246-swiss-nethttp; do f=$(ls .ufo/waves/round-18/runs/$d/logs/*/ghidra.log); echo "$d GoMapType=$(grep -c GoMapType $f) GoStruct=$(grep -c GoStructType.additionalMarkup $f) GoIface=$(grep -c GoInterfaceType.additionalMarkup $f) getPkgPath124=$(grep -c 'GoName.getPkgPath(GoName.java:124)' $f)"; done`
  - rc 0.
  - Output: `0/1/2/1`, `0/4/3/1`, `0/0/0/1`.

**F5 LOW — operability.**
- (a) The table has no row for "Swiss carrier fails, but H1 does not reproduce the read". The frozen rule covers that case as `refuted`/`unresolved` (`predictions/decision-rule.json`); the table is silent on it.
- (b) `<GOLANG_DIR>` is undefined both in the entry's recheck line (`:3`) and in `SKILL.md:590` (same at `:539`). The value actually used is at `gen-predictions.py:20`: `GODATA = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang"`.
- With that value, the documented command reproduces the frozen output exactly. `python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --carrier <path> --golang-root <GODATA>` gave:
  - real-kimi-webbridge: rc 0, `invalid_index [15606016]`;
  - s1246-swiss-nethttp: rc 0, `[22386945]`;
  - s1250-swiss-nethttp: rc 0, `none`;
  - full JSON equal to `predictions/swiss-misread/<label>.json` in all 3 (`a==b` True).

**F6 LOW — two errors outside the decision table, in text that feeds it; the table's counts are unaffected.**
- Observations row `:80`: "(slot 24 lands on a pkgPath-free name)" is true for only 2 of the 8 labels it covers (s12xx-swiss-methods). The two swiss-nomethods carriers have 0 named map types (`uncommon_map_types 0`), and the four noswiss carriers have no misread.
- Mechanism text `:38-40` says the nethttp carriers carry `http.Header`. The synthetic nethttp carriers contain 0 `*http.Header` name strings, and the emulator lists only `*textproto.MIMEHeader` and `*url.Values`. Aether and kimi contain all three.
- Repro: `python3 -I -B -c "…b.count(s) for s in (b'*http.Header',b'*url.Values',b'*textproto.MIMEHeader')…"`
  - rc 0.
  - s1246 and s1250 nethttp: `{0,1,1}`; aether and kimi: `{1,1,1}`.

## Verified (observation; commands and exit codes)

- **V1 (row :94/:95 counts).** `grep -nE 'Go analysis failure|Invalid index|read past EOF' .ufo/waves/round-18/runs/*/logs/*/ghidra.log`
  - rc 0, 6 lines, in exactly 3 logs: aether l.97/177, kimi l.73/206, s1246 l.408/451.
  - The same pattern on `*noswiss*` logs returns rc 1 (no match): 0 of 6 noswiss logs fail.
- **V2 (frozen and held out).**
  - `git log -1 --format='%h %cI' eb6c266` → `13:23:55-03:00`; the first run starts at `13:24:07-03:00` (`runs/run-log.txt:2`). rc 0.
  - `git diff --stat eb6c266 b2aad08 -- .ufo/waves/round-18/predictions` → empty, rc 0.
  - `cd .ufo/waves/round-18 && sha256sum -c predictions/SHA256SUMS` → 32 OK, rc 0.
  - `git log -S15606016 --all -- . ':!.ufo/waves/round-18/predictions'` → earliest `5441b83` at 13:38:07 (after the run), rc 0.
  - No kimi run exists in `round-17/runs` (`git grep -l kimi-webbridge 9011581 -- .ufo/waves/round-17/runs` → none).
  - `producer.json` `branch_tip` is `eb6c266` in 15/15 runs; `compare.json` `all_match` is true in 15/15; `run-log.txt` shows `compare=0` ×15.
- **V3 (byte decode of the name records, written separately from the emulator).** `eval "python3 -I -B - <<'EOF' …ELF PT_LOAD map; decode GoName at types+slot; follow pkgPath… EOF"` → rc 0:
  - aether: `0x954048` flags `0x6e` → `0x10d4120` → EOF pair `(17645861, 111938854)`, matching `ghidra.log:177`;
  - kimi: `0x882028` flags `0x67` → `15606016` unmapped, matching `:206`;
  - s1246: `0x553028` flags `0x6d` → `22386945` unmapped, matching `:451`;
  - silent cases: s1250-nethttp `0x62`; slot 24 is `0x01` in all four carriers that have a slot-24 named map; aether and kimi slot 32 are `0x00`.

  `readelf -lW` shows both unmapped targets above every PT_LOAD end (rc 0).
  Caveat: the `types` base comes from the emulator's `module.types`. It equals the start of the read-only PT_LOAD for kimi (`0x882000`) and s1246 (`0x553000`), and matches aether's `0x954020` in w1 `RevAetherReplay.md:57`.
- **V4 (row :96 "no log line").** Comparing WARN/ERROR classes (level, component, 30-char normalized prefix) between swiss and noswiss twins (`python3 -I -B -c …classes()…`, rc 0): 0 swiss-only and 0 noswiss-only classes in all 5 pairs (shared 15, 15, 7, 7, 10).
- **V5 (row :95 deduction).** In both `go1.24.0.json` and `go1.25.0.json`, `runtime.maptype` is an alias of `internal/abi.OldMapType` (`Position map_noswiss.go:67:6`/`:68:6`), loaded with the emulator's `load_snapshot_types` (rc 0). `buildinfo-probe.py` on the 12 synthetic carriers shows `X:noswissmap` on exactly the 6 noswiss builds (rc 0 each).
- **V6.** `receipt-validate.py --require-mid-maps` gives rc 0 for all 15 receipts; 22 `pins/mid-*.json` files; 12/12 synthetic carrier sums OK; the 3 real carriers match `carriers.tsv`; `missing_bootstrap` is false for all 3 failing labels; `ghidra_12.1.4_PUBLIC` appears in 15/15 logs.
- **V7 (SKILL.md).** The claims at `SKILL.md:553-555` ("matched 15/15 labels; both held-out diagnostic carriers failed with their exact predicted index") hold per V1/V2/V6.

## Residual risk and verification gaps

- One pass only (`:116`); row :94 is not tested for determinism.
- The silent-misread program state was not inspected. Row :96's "methods dropped" remains INFERENCE, as the entry labels it.
- The V4 class comparison is coarse: a misread witness inside a shared message class (for example a different type name inside a "Failed to get subtype" line) would not show up.
- F2 is a derivation from the layout law, not a run.

## Harness notes (my own command errors; their output is void, not findings)

- The first receipt loop reported a bogus `run-log.txt` rc (`$?` captured after a pipeline); rerun correctly in V6.
- The first `sha256sum -c predictions/SHA256SUMS` ran from the wrong directory (rc 1); rerun in V2.
- The first batch `buildinfo-probe` read the wrong key (`version` instead of `go_version`); rerun in V5.

Installs or updates: none. Writes: this report, plus scratch emulator stdout files `/tmp/kdt-*`, created and then removed (`ls /tmp/kdt-* | wc -l` → 0). No lane edits, no jj, no git writes, no REA or Ghidra runs, no carrier executed.
