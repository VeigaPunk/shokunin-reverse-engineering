# ConnectorR89 — scoped findings (round 89, kaidoku)

Seat: ConnectorR89 (connector, leaf). Scan window: `2026-11-04T21:40–21:55-03:00`.
Full links and evidence: `.ufo/waves/round-89/w1/ConnectorR89/links.md` (and `report.md`).
No tools installed or upgraded (pacman guard respected). No git/jj mutations.

## 1. Sibling-lane overlap scan (wrong-value `sz_cpr` class)

A read-only sweep (`git -C <lane> grep -En`) across all 20 sibling lanes (`audio`, `chousa`, `game-dev-2d`, `game-dev-3d`, `kagi`, `kake`, `kama`, `kasegi`, `kengaku`, `kotoba`, `kotodama`, `kumitate`, `lore`, `mado`, `mori`, `revenger`, `souji`, `tabi`, `tameshi`, `tsukuroi`) confirms: **no sibling lane holds this ground**.

- `sz_cpr`: 0 hits across all sibling lanes.
- `sz_unc`: 0 hits across all sibling lanes.
- `stored-value-blind`: 0 hits across all sibling lanes.
- `chain geometry`: 0 hits across all sibling lanes.
- `CantUnpackException` / `CantPackException`: 0 hits across all sibling lanes.
- `NotPackedException`: 1 hit in `revenger-shokunin/reports/round-73/tool-probes.md:83` (`upx -t /usr/bin/true` toolbench availability probe on an unpacked binary; does not touch packer internals, triage, or repair).
- `b_info` (531 hits) & `p_info` (595 hits): all matches are variable names in unrelated domains (`r95b_info` PipeWire DSP node in audio; `blob_info` in mado/tameshi; `napi_get_cb_info` in kotoba; `p_info_redirect.py` in kengaku; `qgroup_info` in mori; `startup_info` in kama/souji; `get_app_info` in revenger). None relates to UPX block or pack headers.
- Sibling attribution: `kumitate-shokunin/.ufo/waves/round-89/w1/K89Connector.md:70-73` explicitly records that Kaidoku exclusively owns packed-ELF reverse engineering, UPX carrier verification, and binary carrier unpacking, and disclaims absorbing it.
- Sibling `PROVINCE.md`: `grep -inE 'upx|packed|packer|b_info|p_info|unpack' */PROVINCE.md` yields **0 matches** across all 20 sibling lanes.

## 2. Province scope check (`kaidoku-shokunin/PROVINCE.md`)

The wrong-value `b_info.sz_cpr` class (`T4-chain-szcpr-wrong`) belongs strictly to Kaidoku:
- `PROVINCE.md:3-6` defines the domain as reverse engineering of shipped artifacts on this Linux host (native ELF through Ghidra provider, REA CLI/MCP, and host fallback readers including `/usr/bin/upx` at `:64`).
- `PROVINCE.md:107-109` unowns dynamic unpacking execution, obliging static structural recovery.
- `PROVINCE.md:690-692, 716-718` explicitly designated "tampering of PackHeader/l_info/p_info/b_info fields other than the magic" as Frontier. R89-C1 moves the wrong-value `sz_cpr` slice of that declared Frontier into Core.

## 3. Bounded non-obvious move (synthesis across round proposals)

- **Evidence:** `ExecMatrix/matrix.json` (48 cells over 4 carriers × 12 field classes, exit 0, met_target true) delivered the completed evidence declared in `claims.json:41`. It proves `b0.sz_cpr := in-range wrong` produces `Exception: compressed data violation` across all four carriers (`jq`, `xxd`, `libz`, `docker-init`), while revealing that `sz_cpr := sz_unc + 1` produces `header corrupted` on executables but `corrupt b_info` on shared object `libz`. In contrast, `SKILL.md` block 29 was committed with interim text stating "On two pinned carriers packed by `upx 5.2.0`..." (noted as MED-1 by `ReviewerC2.md`).
- **Affected axes:** Improves **calibration** (aligning block 29 self-assessment text with the 4-carrier evidence container in `matrix.json`) and **depth** (documenting carrier-dependent refusal semantics for shared objects vs executables) without harming **coverage** (C1's frozen battery and repair are unmutated).
- **Proposed move:** At L1 integration, update block 29 to cite the full 4-carrier population in `matrix.json`, noting that `compressed data violation` is invariant across all four carriers, while annotating the shared-object variance on arithmetic overflow (`sz_unc + 1` → `corrupt b_info` on `libz`) and recording `p_filesize` redundancy as the next Frontier boundary.
- **Risks:** The updated block must preserve `depth-blocks-v2.py` shape floors (`MIN_WORDS 25`, `MIN_SPANS 2`) and cite only base-present knowledge documents (`2026-11-04-r88-binfo-chain-geometry.md`, `2026-11-04-r87-upx-magic-tamper-repair.md`, `2026-11-04-r86-record-agreement.md`).
- **Verification:** `python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev <rev> --expect-blocks 29` reports `blocks 29, resolved 29, unresolved [], met_target: true, exit: 0`.
