# Round24 — freeze the instrument first, then hold the packet-capture family

Author: kaidoku r24 L1 (agent KagiR27-2, reused by message under the fleet job cap), claim kaidoku=24 attempt1.
Baseline B=`fe10219ec6e92c32b7eb40d83fbcac888756c6c1` (round23 admitted, fleet MANIFEST rounds[424]).
Instruments committed first at I=`97ade2e5e2dcf6cfd01d0da8634879d14969f9cc`; claims frozen at
F=`5dc49bfe25d21139693161c786e69c5a11a65bcc` (`.ufo/waves/round-24/claims.json`, instruments pinned by sha256).
Two claims: R24-C1 coverage (REA6.5.0 packet-capture family, 0/4 → k/4) and R24-C2 calibration
(claim-freeze audit disclosed, 0/10 → all freezes). Owned finite proxies tie at 10.0; no
capability row, promotion, mastery or outside admission is claimed by the author.

## Gate

Sources opened this round (URL/path, access date 2026-10-21, located ≤25-word quote). Retained
copies and digests: `.ufo/waves/round-24/sources/metadata.json`.

| Row | Decision | Source and located quote |
|---|---|---|
| S064 | admit A/code | https://www.wireshark.org/download/SIGNATURES-4.6.9.txt — “SHA256(wireshark-4.6.9.tar.xz)=d062d416a1ab3a49975aafe3a671c882dde0562ccd71b078808ceb59d465fc0f” (1 token; located once in the retained copy). gpg: good signature, key 5A5ADBA7…AEEA, no web-of-trust path. |
| S065 | admit A/docs | tshark(1) 4.6.9, tarball `doc/man_pages/tshark.adoc:170` (online page https://www.wireshark.org/docs/man-pages/tshark.html carries the same option) — “Perform a two-pass analysis. This causes *TShark* to buffer output until the entire first pass is done” (19 words). |
| S066 | admit A/code | REA6.5.0 `dist/captures/TsharkCaptureProvider.js:263` (sha256 fdc1fc13…0549) — “at most 1 GiB address space per process, 64 MiB per file, 30 CPU seconds and no core dumps” (17 words). |
| S067 | admit A/own-work | `.ufo/waves/round-24/evidence/c1/l1-*.envelope.json` with byte-equal producer stdout in `l1-*.run.json`. |
| S068 | admit A/paper | https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/ (Nosek et al. 2018, PNAS) — “define the research questions and analysis plan before observing the research outcomes” (13 words); “deviations are reported transparently, making it possible to assess their impact” (11 words). |
| capinfos(1) 4.6.9 | reject as a row | Opened (`doc/man_pages/capinfos.adoc`, sha256 76a23815…5f61); `-c` “Displays the number of packets in the capture file.” Not needed: REA's pcap output already records counts/times. Flip: a claim that depends on capinfos semantics directly. |

Registry cells changed old→new: none (rows S001–S063 unchanged; S064–S068 appended).
Sourced claim: R24-C1 rests on S064–S067 (the counting instrument requires an S064+ row opened
this round naming the entry in used-by).

## Claim-freeze audit

`python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root <LANE> --rev <REV> --require-clean round-24 --disclosures corpus/claim-freezes.tsv`
reads only Git objects. Disclosures are in `corpus/claim-freezes.tsv`, one row per retained freeze:

- R14–R16: claims name no measurement script (`INSTRUMENT_NONE`); their measurements lived in prose or entries.
- R17, R18: scripts named by bare file name only (`INSTRUMENT_UNRESOLVED`), so the frozen instrument cannot be identified from Git.
- R19, R20: three of four named instruments absent at freeze and revised after; the present `.ufo/gates/c1-census-v10.py` unpinned and revised once.
- R21: `battery.py` absent at freeze, added after.
- R22: both counters present but unpinned and revised twice each.
- R23: `count-c1.py` absent at freeze `a3c92eb6` and changed in three later commits — the closure's routed defect, now machine-detected.
- R24: instruments committed before the freeze and pinned; one disclosed supersession (below).

This does not say any historical round was wrongly admitted: several closures re-measured with
their own instruments. It says the lane's freezes did not, by themselves, fix the instrument.

**Own supersession, disclosed.** Before any after-measurement the L1 found that the frozen gate's
path regex reported R17/R18 (bare names such as `routed-defects.py`) as `INSTRUMENT_NONE`. The gate
was revised at `9fb4eacd` (adds `INSTRUMENT_UNRESOLVED`) and the change is appended to
`claims.json` `instrument_supersessions` with its reason; the original-instrument before record
(`measure/before-c2.json`) is kept beside the revised one (`measure/before-c2-rev1.json`). Both
show 0/10 disclosed. This is exactly the deviation path QUALITY33 allows; it is not silent.

## Mistakes

| id | class | evidence | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M24-1 | instrument-after-claim | R23 `claims.json` frozen at `a3c92eb6` names `.ufo/waves/round-23/tools/count-c1.py`, absent at that commit and changed by `2b40aec5`, `9d64b953`, `fe18f13f` (fleet MANIFEST rounds[424] routed defect) | none at the time — the closure caught it by hand | QUALITY33 + `freeze-gate.py`: at the final revision it must report round-23 `INSTRUMENT_ABSENT,INSTRUMENT_REVISED` (red) while round-24 is CLEAN (green); a sandbox freeze whose instrument is removed must turn red (BUILD selftest item) |
| M24-2 | bookkeeping regression | round-23 diff `aa1450b8..fe10219e` removed the blank line after the last row of three README tables, so each table abutted the next heading | none — "nonempty-line order preserved" was the only README check | blank lines restored before `## Knowledge`, `## Lessons`, `## Frontier`; the final no-harm check counts a blank line immediately before each `## ` heading |
| M24-3 | reproduction-on-scratch | held witnesses cite inputs under `/tmp/kd22probe`, `/tmp/kd23work`, gitignored `round-23/runtime/` and `~/.local/share/godot`; the closure could not find them on its clone | none | `.ufo/waves/round-24/repro/inputs.json` + `fetch-inputs.py`: official URL, sha256 and size per input; the executed re-acquisition receipt must show `match:true` for each, and a wrong digest exits 1 |
| M24-4 | own-instrument gap | frozen gate missed bare script names (R17/R18 → `INSTRUMENT_NONE`) | L1 review before after-measurement | supersession `9fb4eacd`, disclosed in `claims.json`; `INSTRUMENT_UNRESOLVED` rows in the ledger |

## Tooling and ownership

- Installed: cmake 4.4.4 (`uv tool install cmake`, PyPI) to configure the build; Wireshark/TShark/capinfos 4.6.9 built from the signature-checked official source into `/home/vgpnk/.local/opt/wireshark-4.6.9` (Lua and GUI off). No pacman transaction (host pause respected). Pins: `.ufo/waves/round-24/tool-pins.json`.
- Packet-capture analysis is held only on saved public captures and the installed dissector registry. Live capture, `dumpcap`, interfaces and lane-held decryption keys stay Adjacent/unowned. The TLS test capture's HTTP layer came from Decryption Secrets Blocks embedded in the file (verified by block walk), not a lane key.
- Both debugger verbs stay unheld; the kaidoku/revenger arbitration is still open.

## Limits

- C1's denominator is the four catalog verbs that a local TShark unlocks; it is a finite family, not the network-forensics domain. The frozen R23 six-verb T1 stays 4/6.
- C2 checks only what `claims.json` names; instruments named elsewhere (lesson prose, LOG) are invisible to it. Commit times and authors are not authenticated.
- R22's 102 reportless seats stay uncredited.
