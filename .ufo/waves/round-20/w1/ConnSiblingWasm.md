# ConnSiblingWasm — sibling overlap scan (round 20, w1)

Seat: `KaidokuR20.ConnSiblingWasm-2`. Read-only leaf. Written 2026-10-20T17:52:36-03:00.
Axes named for this pass: **calibration**, **coverage**, **depth**.
Installs / updates: none. `rg` 15.1.0 was already on PATH (`rg --version | head -n 1` returned `ripgrep 15.1.0`, exit 0). No pacman, uv, cargo, or npm transaction.

## Verdict

No sibling lane owns or holds WASM analysis, WABT, or wasm interface comparison on the three assigned surfaces. **Contested scope: none.**

The only token hit is a refused-verifier basename prefix (`wasm-`). It is not a claim on that subject.

## Sibling set

Observation: `/home/vgpnk/Projects/shokunin/*-shokunin` except the home lane `kaidoku-shokunin`. Count **20**. Each has `PROVINCE.md`, `corpus/SOURCES.md`, and a `corpus/knowledge/` directory. `find … -type f` under those knowledge directories: **735** files.

| lane | knowledge files |
|---|---:|
| audio-shokunin | 18 |
| chousa-shokunin | 29 |
| game-dev-2d-shokunin | 5 |
| game-dev-3d-shokunin | 47 |
| kagi-shokunin | 24 |
| kake-shokunin | 22 |
| kama-shokunin | 15 |
| kasegi-shokunin | 30 |
| kengaku-shokunin | 32 |
| kotoba-shokunin | 35 |
| kotodama-shokunin | 225 |
| kumitate-shokunin | 40 |
| lore-shokunin | 26 |
| mado-shokunin | 35 |
| mori-shokunin | 27 |
| revenger-shokunin | 6 |
| souji-shokunin | 8 |
| tabi-shokunin | 36 |
| tameshi-shokunin | 27 |
| tsukuroi-shokunin | 48 |

Sum of the column: 735.

Observation, outside the assigned glob: top-level `tameshi-shokukin` exists. `find /home/vgpnk/Projects/shokunin/tameshi-shokukin -maxdepth 3 \( -name PROVINCE.md -o -name SOURCES.md -o -path '*/corpus/knowledge/*' \)` printed nothing, exit 0. It was not added to the sibling set.

## Commands and exits

`rg` 15.1.0. Scripts used `set +e` so a no-match exit 1 is the search result. The shell wrapper's overall exit was 0 because each script finished on `echo`. The `EXIT_*` values below are the search exits. Harness line `Timeout clamped to 3600s` is not a command failure.

Primary pattern (`PAT`):

```
WebAssembly|WASM|wasm|WABT|wabt|wasm2wat|wat2wasm|wasm-objdump|wasm-validate|wasm-decompile|wasm-interp|wasm-strip|binaryen|wasmtime|wasmer|wit-bindgen|inspect-wasm|inspect_wasm|compare-wasm|compare_wasm|wasm interface
```

`WebAssembly` is in the pattern on purpose: the letters `wasm` are not a substring of `WebAssembly`.

Sibling array (every command below):

```
SIBS=()
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do
  base=$(basename "$d")
  [ "$base" = "kaidoku-shokunin" ] && continue
  SIBS+=("$d")
done
```

### 1. Primary search, default ignore rules on knowledge

```
echo "SIBLING_COUNT:${#SIBS[@]}"
rg -n -i -e "$PAT" "${SIBS[@]/%//PROVINCE.md}"; echo "EXIT_PROVINCE:$?"
rg -n -i -e "$PAT" "${SIBS[@]/%//corpus/SOURCES.md}"; echo "EXIT_SOURCES:$?"
rg -n -i -e "$PAT" "${SIBS[@]/%//corpus/knowledge}"; echo "EXIT_KNOWLEDGE:$?"
```

| label | exit | stdout |
|---|---:|---|
| SIBLING_COUNT | — | 20 |
| EXIT_PROVINCE | 1 | empty |
| EXIT_SOURCES | 1 | empty |
| EXIT_KNOWLEDGE | 0 | one line: `kumitate-shokunin/corpus/knowledge/local-ship.md:107` |

File census in the same script: `province_files:20`, `sources_files:20`, `knowledge_files:735` (`find … -type f | wc -l`), `EXIT_COUNTS:0`.

### 2. Same trees with hidden and ignored files included

```
rg -n -i --hidden --no-ignore -e "$PAT" <20 PROVINCE.md> <20 SOURCES.md>
# EXIT_PS_NOIGNORE:1 (empty)

rg -n -i --hidden --no-ignore --glob '!.git/**' -e "$PAT" <20 corpus/knowledge dirs>
# EXIT_KNOW_NOIGNORE:0
```

Same single knowledge line. No new province or SOURCES hit.

### 3. Binary-mode pass (`rg -a`)

```
rg -n -i -a --hidden --no-ignore --glob '!.git/**' -e "$PAT" <20 corpus/knowledge dirs>
# EXIT_BIN:0
```

Same single line. No extra hit in files ripgrep would otherwise skip as binary.

### 4. Ignore gap closed

```
rg --files <knowledge dirs> | wc -l                         # 719, exit 0
rg --files --hidden --no-ignore --glob '!.git/**' … | wc -l # 735, exit 0
comm -13 <(rg --files … | LC_ALL=C sort) <(rg --files --hidden --no-ignore --glob '!.git/**' … | LC_ALL=C sort)
# EXIT_COMM:0
```

The 16 paths present only in the no-ignore list (pass 2 already searched their contents; no token hit):

- `chousa-shokunin/corpus/knowledge/.gitkeep`
- `game-dev-3d-shokunin/corpus/knowledge/unreal-mcp/.manifest.d/audit-reference.sha256`
- `game-dev-3d-shokunin/corpus/knowledge/unreal-mcp/.manifest.d/seat01.sha256` through `seat11.sha256` (11 files)
- `game-dev-3d-shokunin/corpus/knowledge/unreal-mcp/upstream/.claude-plugin/plugin.json`
- `game-dev-3d-shokunin/corpus/knowledge/unreal-mcp/upstream/.gitignore`
- `mori-shokunin/corpus/knowledge/.gitkeep`

An earlier `comm` without `LC_ALL=C` exited 1 with `comm: input is not in sorted order` while still printing this same set. The `LC_ALL=C` rerun is the one counted.

### 5. Filenames

```
find <20 knowledge dirs> \( -iname '*wasm*' -o -iname '*wabt*' -o -iname '*webassembly*' \) -print
# EXIT_FIND:0, empty
```

### 6. Near-synonym pass

`PAT2`:

```
emscripten|interface types|component model|wat2wasm|wasm-bindgen|wasm-tools|wit-bindgen|WebAssembly
```

```
rg -n -i --hidden --no-ignore -e "$PAT2" on the 20 PROVINCE.md   # EXIT_P2:1
rg -n -i --hidden --no-ignore -e "$PAT2" on the 20 SOURCES.md    # EXIT_S2:1
rg -n -i --hidden --no-ignore --glob '!.git/**' -e "$PAT2" on knowledge  # EXIT_K2:1
```

All three empty. This pass does not contain the bare prefix `wasm-`, so it does not re-hit `local-ship.md:107`.

### Discarded instrument

An editor content search of `**/PROVINCE.md` for the wasm token reported "No matches found". That result was not used as evidence of absence. Direct `rg` of the home-lane file (below) hits `kaidoku-shokunin/PROVINCE.md:54`. Inference: the editor index does not see every tree `rg` sees. Shell `rg` exits above are the evidence.

## Observations

**Sole sibling content hit** — `kumitate-shokunin/corpus/knowledge/local-ship.md:105-110`:

```
- Refused basenames: **95 exact** names (`sh bash zsh fish … env busybox awk
  sed find xargs dd gcc make sudo su …`, :2080-2181) + **13 prefixes**
  (`python pypy node perl ruby php lua docker podman pip npm wasm- qemu-`,
  :2183-2191), ASCII-case-insensitive; THEN a trailing digit/dot strip
  (`python3.12`→`python`, `curl8`→`curl`, `sh.`→`sh`) re-runs both checks
  only when `stripped != raw` (:2064-2078).
```

The token is the prefix `wasm-` on line 107, inside the parenthetical of 13 prefixes. Neighbor lines 102-104 title the section `## Verifier grammar (:2061-2291) — denylist, never inference`.

File subject, `local-ship.md:1`: `` # `local_ship.rs` — local apply/verify/rollback transaction (I10) ``.

Lane that holds the file, `kumitate-shokunin/PROVINCE.md:3`: `**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime`. `PROVINCE.md:5`: `**Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it.`

**Home lane, not a sibling.** Recorded so the token is not later folded into sibling overlap. `kaidoku-shokunin/PROVINCE.md:54` is the EVM-interface row and contains the clause `bundled EVMole 0.9.3/WASM` on the `rea inspect-evm-interface` line. The line is longer than that clause; the rest of it is EVM selector-extraction notes, not WABT.

## Inference

- Contested scope is empty. No sibling `PROVINCE.md` sentence and no sibling `corpus/SOURCES.md` row names WASM analysis, WABT, wasm2wat, wasm-objdump, WebAssembly, or wasm interface comparison.
- `local-ship.md:107` holds `wasm-` as one of 13 refused verifier basename prefixes. Inference: kumitate is recording a denylist (refuse a verifier whose basename starts with `wasm-`), not owning WASM analysis and not holding WABT or an interface comparison.
- `kaidoku-shokunin/PROVINCE.md:54` uses WASM as the bundle vehicle for EVMole on an EVM verb. Inference: that is home-lane EVM work. It is not a sibling contest, and the clause is not `inspect-wasm-artifact`, `compare-wasm-interfaces`, or a WABT pin.

## Coverage limits

- Assigned surfaces only: `PROVINCE.md`, `corpus/SOURCES.md`, `corpus/knowledge`. Sibling `.ufo/`, `corpus/lessons`, scripts, and fleet-root docs were not searched.
- A miss means these token sets were absent, not that every possible paraphrase was read. Bare `wit` was not searched (ordinary English). `wit-bindgen` was, exit 1.
- Default `rg` skips ignored and binary files. Those gaps were closed (`--no-ignore`, `-a`) and added no hits.
- `tameshi-shokukin` is outside `*-shokunin` and has none of the three surfaces within the maxdepth-3 find above.

## Connector proposal (one, not applied)

Evidence: passes 1–6 and the two path:line anchors above (`local-ship.md:107`, home-lane `PROVINCE.md:54`).
Affected axes: **calibration** (a `wasm` token is not a WABT holding). **Coverage** of the negative is recorded with the 16-file ignore gap closed. **Depth** stays: the one hit is classified from its section, not dropped.
Move for L1 at C2 admission: cite this scan as the overlap bound on `inspect-wasm-artifact` and `compare-wasm-interfaces`, and do not treat `kumitate-shokunin/corpus/knowledge/local-ship.md:107` or `kaidoku-shokunin/PROVINCE.md:54` as prior holdings of WABT or wasm interface comparison.
Risk: a sibling sentence that never uses these tokens would not appear. Surfaces outside the three named trees were not read.
Verification: re-run pass 2. Expect province and SOURCES exit 1, and a single knowledge hit at `local-ship.md:107`.

## Clock

`date -Iseconds` immediately before this write: 2026-10-20T17:52:36-03:00.
