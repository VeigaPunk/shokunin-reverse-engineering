# ReviewScope — offline signal / hardware ownership boundary
## Axes

- Coverage: offline signal evidence's fit to R23-C1's finite coverage claim.
- Depth and calibration: not assessed; no improvement is claimed.

## Findings

- **No unexplained hardware or dynamic-analysis bleed observed in the selected signal probes.** `claims.json:29` explicitly limits this round to offline recordings and excludes debugger/Frida execution, device access, and carrier execution. The selected decode record (`evidence/c1/decode-uart-hi.run.json:2-26`) records `npx -y rea-agents@6.5.0 decode-signal-recording` against the local `uart-hi.bin`, with `--input_format binary:numchannels=1:samplerate=960000`, UART RX channel 0 at 9600 baud, exit 0, and no stderr. `generate-uart.run.json:2-11` records that the 2,500-byte subject (SHA-256 `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`) was generated from ASCII `Hi` with `acquisition: "synthetic; no hardware"`. The normalized decode envelope reports exactly two output lines (`48`, `69`), no additional lines, and `hardware_acquisition: "not-performed"` (`evidence/c1/decode-uart-hi.envelope.json:1`). The inventory call likewise used `--dont-scan --list-supported` and its envelope says `hardware_acquisition: "not-performed"` (`evidence/c1/inventory.run.json:2-19`, `inventory.envelope.json:1`). These are analysis-tool processes over decoder definitions / a supplied byte file, not target-carrier execution, device acquisition, process attach, or debugger ownership.

  **Disposition:** offline recordings fit the province's shipped-artifact/evidence-first analysis boundary as a subject class; hardware acquisition and live debugging remain Adjacent/unowned. This does not mean the signal verbs are already Core/held: `PROVINCE.md:31-32` requires an end-to-end `LOG.md` entry citing evidence ID and subject SHA before Core promotion, and `PROVINCE.md:214-218` still records the signal verbs as unexercised in R22. The current `LOG.md` ends at the R23 declaration (`:2587-2600`), without a signal evidence entry. Treat the observed R23 probe as candidate new evidence, not as automatic promotion.

- **Low — inventory saturation must be stated narrowly.** The normalized decoder inventory reports 110 examined/matching/returned and `has_more: false` (`evidence/c1/inventory.envelope.json:1`), but its diagnostics also say the bundled `signature` decoder failed to load under Python 3.5 due to a `SyntaxError` at `signature/pd.py:138` (same envelope). Thus the page is saturated for the decoder set successfully returned by this run; it does not prove every bundled decoder loaded. The diagnostic is exposed, so this is not unexplained hardware bleed, but an unqualified “all installed decoders” assertion would overstate the observation.

## Boundary evidence and residual risk

- The round uses the declared CLI client pin `rea-agents@6.5.0` (recorded argv above); the result identifies `sigrok-cli@0.7.2`. This matches the wave's explicit probe route, not the separately configured 6.7.0 MCP-client requests described in `PROVINCE.md:8-13`. No MCP request was made here.
- `tools/sigrok-cli.sh:9-15` is a pass-through wrapper (`exec ... "$@"`), not an offline-only sandbox. The observed `--version` result lists libusb, libserialport, and SCPI TCP/RPC/serial/USBTMC backends (`sigrok-version-attempt1.json:2-14`); the extracted package also contains device firmware. Those are available capabilities, not evidence of contact. In the actual decode/inventory evidence, the adapter selected `--dont-scan` and file/list operations, and the envelopes explicitly record no acquisition. Therefore no hardware bleed is observed, but the offline boundary is established by this invocation's input/flags and operating discipline, not by a wrapper that prevents future explicit hardware-driver arguments.
- `w1/SignalCarrierAlternatives.md:10-31,36-60,111-157` documents an official historical `.sr` UART sample and its acquisition context (ChronoVu LA8 / STM32-H103 TX, 625 kHz); it also states that fixture bytes were not retained and no decode was performed. It is evidence about a possible offline source, not an executed real-capture test. The exercised R23 input was synthetic; compatibility with that historical `.sr` format and its captured-data provenance remains untested here.
- No same-identity rerouting test was observed. The tested decode subject path and SHA are consistent between the run receipt and normalized envelope; that is identity continuity for one route, not evidence of rerouting equivalence.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewScope.md` — this report; its SHA-256 is supplied in the completion message to avoid self-referential content.

## Installs

None.

## Open risks

- No live device or hardware acquisition was tested; none is claimed. Any future signal invocation that selects a live device/driver, rather than an offline input file, crosses the declared Adjacent boundary.
- The real public `.sr` fixture was metadata-inspected only; current decode evidence covers a locally generated binary raw-logic file.
- The failed `signature` decoder load limits the inventory completeness interpretation as described above.