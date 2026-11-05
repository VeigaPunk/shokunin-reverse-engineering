# ConnectorR89 — cross-lane and cross-source pattern scan (round 89, kaidoku)

Seat: ConnectorR89 (connector, leaf — no dispatch). Read-only scan of
`/home/vgpnk/Projects/shokunin/*-shokunin` (20 sibling lanes) plus this lane's own packed-ELF corpus.
Scan window: `2026-11-04T21:40–21:55-03:00`. Lane base `0ec2bb4016655f605657d6e0e700ec2e6893ac27`;
lane HEAD at scan close `8bbb40cc09fadd211b1aa473605553c9caeef511`.

No tools installed or upgraded (pacman guard respected). No git/jj mutation (read-only `git -C <lane> grep -l`, `log`, `status`, `ls-files` only). No files written outside this seat directory and `.ufo/waves/round-89/w1/ConnectorR89.md`.

---

## 1. Exact scan commands executed

```sh
# Sweep all 20 sibling lane repos for UPX, packer, and b_info/p_info terms
python3 -c "
import os, subprocess, glob
lanes = sorted([p for p in glob.glob('/home/vgpnk/Projects/shokunin/*-shokunin') if os.path.isdir(p) and not p.endswith('kaidoku-shokunin')])
terms = ['sz_cpr', 'sz_unc', 'b_info', 'p_info', 'CantUnpackException', 'CantPackException', 'NotPackedException', 'stored-value-blind', 'chain geometry']
for term in terms:
    for lane in lanes:
        res = subprocess.run(['git', '-C', lane, 'grep', '-En', term], capture_output=True, text=True)
"

# Search PROVINCE.md across all 20 sibling lanes
python3 -c "
import os, subprocess, glob
lanes = sorted([p for p in glob.glob('/home/vgpnk/Projects/shokunin/*-shokunin') if os.path.isdir(p) and not p.endswith('kaidoku-shokunin')])
for lane in lanes:
    prov = os.path.join(lane, 'PROVINCE.md')
    if os.path.exists(prov):
        res = subprocess.run(['grep', '-inE', 'upx|packed|packer|b_info|p_info|unpack', prov], capture_output=True, text=True)
"

# Broad word sweep for UPX across sibling lanes
python3 -c "
import os, subprocess, glob
lanes = sorted([p for p in glob.glob('/home/vgpnk/Projects/shokunin/*-shokunin') if os.path.isdir(p) and not p.endswith('kaidoku-shokunin')])
for lane in lanes:
    res = subprocess.run(['git', '-C', lane, 'grep', '-En', r'\bUPX\b|\bupx\b'], capture_output=True, text=True)
"
```

---

## 2. Sibling lane hits and analysis

Across all 20 sibling lanes (`audio`, `chousa`, `game-dev-2d`, `game-dev-3d`, `kagi`, `kake`, `kama`, `kasegi`, `kengaku`, `kotoba`, `kotodama`, `kumitate`, `lore`, `mado`, `mori`, `revenger`, `souji`, `tabi`, `tameshi`, `tsukuroi`):

| Searched term | Sibling hits | Analysis |
|---|---|---|
| `sz_cpr` | **0 hits** | No sibling lane mentions the field. |
| `sz_unc` | **0 hits** | No sibling lane mentions the field. |
| `stored-value-blind` | **0 hits** | No sibling lane mentions stored-value-blind derivation. |
| `chain geometry` | **0 hits** | No sibling lane mentions chain geometry. |
| `CantUnpackException` | **0 hits** | No sibling lane mentions the UPX refusal class. |
| `CantPackException` | **0 hits** | No sibling lane mentions UPX packing exceptions. |
| `NotPackedException` | **1 hit** | `revenger-shokunin/reports/round-73/tool-probes.md:83`: `upx -t /usr/bin/true` tool-probe ledger entry. Tool availability check on plain binary, not triage or repair. |
| `b_info` | 531 line hits | All hits are variable names or identifiers in unrelated domains (`r95b_info` in audio PipeWire DSP node; `blob_info` in mado/tameshi test harnesses; `napi_get_cb_info` in kotoba Node.js symbols; `shmem_sb_info` in mori Linux kernel shmem). None touches UPX block headers. |
| `p_info` | 595 line hits | All hits are unrelated domain variables (`p_info_redirect.py` test harness in kengaku; `qgroup_info` in mori Btrfs; `startup_info` in kama/souji Git attr; `get_app_info` in revenger JADX APK probe; `div class="p_info "` in chousa captures). None touches UPX pack headers. |

Broad UPX hits across sibling lanes:
1. **`kumitate-shokunin/.ufo/waves/round-89/w1/K89Connector.md:70-73`** (and `build/K89Connector/K89Connector.md:72`):
   Explicit sibling boundary statement in round 89:
   - *Evidence:* `kaidoku-shokunin/PROVINCE.md:522, 544, 552, 624`.
   - *Nature:* "Kaidoku performs packed-ELF reverse engineering, UPX carrier verification, and kernel-side `/proc/<pid>/environ` ancestor tracking for unblob and disassembler routes."
   - *Disposition:* "Reverse engineering and binary carrier unpacking belong strictly to Kaidoku. Reported, not absorbed."
2. **`revenger-shokunin/reports/round-73/tool-probes.md:82-83`**:
   `upx --version` → `upx 5.2.0`; `upx -t /usr/bin/true` → rc 2 `NotPackedException: not packed by UPX`.
   Toolbench presence check, not packer structure.
3. **`revenger-shokunin/reports/round-73/scout-packs/ReFrameworkTargets.md:13-14`**:
   GoReSym README citation: "malformed unpacked binaries, such as from UPX". Consumer-side warning on Go pclntab reconstruction, not packer structural derivation.
4. **`game-dev-3d-shokunin/reports/round-102/adversary/F6.md:54`**:
   Pacman transaction install line mentioning `upx`.
5. **`tameshi-shokunin/.ufo/waves/round-32/w1/CtlRegionDiff.md:276,744`**:
   Base64 test artifact that incidentally encodes bytes matching `UPX!`.
6. **`tsukuroi-shokunin/.ufo/waves/round-19/.../PROVINCE.md` & `round-24`**:
   Read-only archival captures of Kaidoku's historical `PROVINCE.md` or host pacman package lists.

**PROVINCE.md across all 20 sibling lanes:**
`grep -inE 'upx|packed|packer|b_info|p_info|unpack' */PROVINCE.md` returns **0 matches** across all 20 sibling lanes.

**Verdict: No sibling lane holds this ground.**

---

## 3. Province scope check (`kaidoku-shokunin/PROVINCE.md`)

- **Domain:** "reverse engineering of shipped artifacts with REA on this Linux host — native ELF through the Ghidra 12.1.4 provider, Electron/ASAR/JavaScript bundles, archives and packages; evidence-first static analysis that keeps observation, inference and unknowns separate."
- **Host fallback readers:** `PROVINCE.md:64` explicitly lists `upx` among host tools.
- **Round-87 addition to Core:** `PROVINCE.md:668-685` established Core ownership of UPX-packed ELF header reconstruction (anti-UPX magic words tampered).
- **Round-88 addition to Core:** `PROVINCE.md:697-710` established Core ownership of `b_info` field derivation from chain geometry (`sz_cpr` zeroed), and Held status for the refusal-signature matrix (craft rule block 28).
- **Frontier boundary:** `PROVINCE.md:690-692` and `PROVINCE.md:716-718` declared: "Still Frontier: ... tampering of PackHeader/l_info/p_info/b_info fields other than the magic".
- **Unowned boundary:** `PROVINCE.md:107-109` refuses dynamic execution ("Non-REA dynamic analysis — gdb scripting, strace/ltrace, unpacking by execution, Frida-style hooking (unowned)").

The wrong-value `b_info.sz_cpr` class (`T4-chain-szcpr-wrong`) is a purely static structural recovery of packed native ELF headers:
1. It restores the executable's header structure statically via chain geometry and accounting bounds without executing untrusted payloads.
2. It directly moves the declared Frontier boundary of `PROVINCE.md:716` to Core.
3. Sibling lanes (e.g. `kumitate-shokunin`) explicitly disclaim binary unpacking and acknowledge Kaidoku's exclusive ownership.

**Verdict: The class belongs strictly to Kaidoku's province and to no sibling lane.**

---

## 4. Synthesis across round proposals: one non-obvious move

### Evidence
1. **`ExecMatrix/matrix.json` (48 cells over 4 carriers):**
   `matrix.json` landed with all 4 pinned carriers (`jq`, `xxd`, `libz`, `docker-init`) across 12 field classes (`exit: 0, met_target: true, unclassified: []`).
   It revealed that:
   - For `b0.sz_cpr := true ± 8`, all 4 carriers yield `Exception: compressed data violation` (the only class reaching the decompressor payload stage) and all 4 recover via `upx-field-value-repair.py`.
   - For `b0.sz_cpr := sz_unc + 1`, the packer refusal is carrier-variant: `header corrupted` on `jq`, `xxd`, `docker-init`, but `corrupt b_info` on shared object `libz`.
   - For `p_info.p_filesize ^= 0xFF`, `upx -t` yields `CantUnpackException: p_info corrupted`, and `upx-field-value-repair.py` refuses rc 2 because `l_info_candidates()` enforces `p_filesize == PackHeader.u_file_size`, despite `p_filesize` being 100% redundant with `u_file_size`.
2. **`ExecGeomIndep/report.md`:**
   Independent derivation proves `derive()` derives the identical `sz_cpr` (252, 249, 201, 226) across 55 stored values per carrier, whereas a stored-reading mutant fails on `docker-init` (deriving 136 instead of 226).
3. **`ReviewerC2/report.md:120-128` (MED-1):**
   Noted tension: `claims.json:41` declared `.ufo/waves/round-89/w1/ExecMatrix/matrix.json` as C2's evidence, but `SKILL.md` block 29 was committed with interim text naming "two pinned carriers" backed by `l1/scores/block29-cells.json` (2 carriers).

### Affected axes
- **Calibration:** Eliminates the mismatch between the interim 2-carrier prose in `SKILL.md` block 29 and the 4-carrier evidence container declared in `claims.json:41` and delivered in `w1/ExecMatrix/matrix.json`.
- **Depth:** Captures the newly observed carrier variance (`libz` returning `corrupt b_info` where executables return `header corrupted` for `sz_cpr := sz_unc + 1`) and grounds the `p_filesize` redundancy as the next Frontier boundary.
- **Coverage:** Unharmed. C1's frozen 4-carrier battery (`upx-field-battery.py`) and repair remain completely untouched and verified.

### Proposed move
At integration, update `SKILL.md` block 29 to cite the completed 4-carrier evidence from `matrix.json`, annotating that:
1. `b0.sz_cpr := in-range wrong` produces `compressed data violation` consistently across all four pinned carriers (`jq`, `xxd`, `libz`, `docker-init`).
2. Arithmetic overflow `b0.sz_cpr := sz_unc + 1` produces `header corrupted` on native executables (`jq`, `xxd`, `dinit`), but `corrupt b_info` on shared object `libz` (reflecting ELF shared-object layout).
3. `p_info.p_filesize` duplicates `PackHeader.u_file_size`, but remains Frontier because the locator keys on it.

### Risks
- `depth-blocks-v2.py` enforces a shape floor (`MIN_WORDS 25`, `MIN_SPANS 2`) and citation resolution. Any update to block 29 must retain its valid base-present citations (`2026-11-04-r88-binfo-chain-geometry.md`, `2026-11-04-r87-upx-magic-tamper-repair.md`, `2026-11-04-r86-record-agreement.md`) and word/span counts.

### Verification
Run `python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev <rev> --expect-blocks 29` to confirm `blocks 29, resolved 29, unresolved [], met_target: true, exit: 0`.
