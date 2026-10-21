# PrimarySigrok — sigrok-cli primary source: recorded decoding vs live acquisition

Seat: `KaidokuR22R.PrimarySigrok-6` (leaf scout, round-22 w2 recovery wave). Author-side evidence only; not outside admission. Opened 2026-10-21.

## Verdict

The source is **accessible**. It gives bounded primary-source support for one fact: sigrok-cli has two distinct input modes. One loads a recorded file (`-i/--input-file`). The other acquires from a hardware driver (`-d/--driver`). Protocol decoders (`-P`) are documented working on recorded files. This is documentation support only. It does **not** count toward R22-C1 (zero T1 credit), and it does not change R22-C2. PROVINCE.md line 205 still holds: the remaining signal verbs stay unclaimed unless separately demonstrated.

## Quote (one contiguous passage, 10 words)

> "Load input from a file instead of a hardware device."

- Page: sigrok wiki `sigrok-cli` (https://sigrok.org/wiki/Sigrok-cli), MediaWiki revision `16563` (`wgRevisionId` = `wgCurRevisionId`).
- Exact heading: section `Manpage` → `OPTIONS` → `-i, --input-file <filename>`.
- Date: page "last edited on 7 July 2023, at 08:09" (action=info: latest editor AtomicFS; 34 edits; created 22:46, 14 March 2010). The embedded manpage footer reads `October 22, 2018`.
- Whitespace: the source has nroff-justified double spaces (`a  hardware  device.`). The quote collapses them to single spaces; the words and their order are unchanged.

## What the page supports (paraphrase, located)

| Point | Location on page | Bears on |
|---|---|---|
| `-i` loads input from a file or stdin, with format autodetection unless `-I` is given | Manpage / OPTIONS / `-i`, `-I` | recorded decoding |
| `-d` selects a driver, and a driver must be selected "unless doing a global scan"; serial devices need `conn=` | Manpage / OPTIONS / `-d` | live acquisition |
| `--samples`, `--time`, `--frames`, `--continuous`, `-t`, `-w` control acquisition; every EXAMPLES entry uses `--driver` (fx2lafw, ols, lascar) | Manpage / OPTIONS, EXAMPLES | live acquisition |
| All `-P` / `-A` / `-M` / `-B` decoder examples use `-i <file.sr>`; decoders stack within one `-P` and run in parallel across repeated `-P` | Manpage / OPTIONS / `-P` … `-B` | recorded decoding |
| `--protocol-decoder-samplenum` adds sample numbers to annotations | Manpage / OPTIONS | recorded decoding (REA passes it) |
| `-L` lists decoders; `--protocol-decoders i2c --show` shows decoder options | Manpage / OPTIONS / `-L`, `--show` | `inspect-signal-decoders` |
| Advice to capture first and decode later (sigrok-cli is single-threaded and overload ends it early) | `Usage tips` | separation of acquisition from decoding |
| Exit status is 0 on success and 1 on most failures | Manpage / EXIT STATUS | interpreting future receipts |

## Relation to REA 6.5.0 (local installed source, not the wiki)

The installed `rea-agents` package at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/` (`package.json` version `6.5.0`; the same root as SOURCES S048) has a provider file, `dist/signals/SigrokRecordingProvider.js` (sha256 `7979bafb84b463d0fc3040d3643e08362326d67fd4543ee690679dc88b2dced7`, 339 lines). That file:
- pins `version: "sigrok-cli@0.7.2"` (line 25);
- records `hardware_acquisition: "not-performed"` (line 160);
- runs `inspect-signal-decoders` as `--dont-scan --list-supported` or `--dont-scan --protocol-decoders=<id> --show` (lines 164–166);
- runs `decode-signal-recording` on a private read-only copy as `--dont-scan --input-file=recording --protocol-decoders=<stack> --protocol-decoder-samplenum [--input-format=…]` (lines 191–198);
- requires `REA_SIGROK_COMMAND` and `prlimit` (lines 70–84).

Observed: REA's decode path uses the page's recorded-file mode (`-i`) plus `-P`, and never the `-d` acquisition mode. The page documents both modes.

## Unsupported inferences (explicitly not established)

1. **`--dont-scan` is not on the page.** `rg -n -i 'dont-scan|-D,'` on the raw wikitext matched only `-d, --driver` (line 67). The page therefore cannot support REA's "no hardware discovery" guarantee. That rests only on REA source plus sigrok-cli behavior that has not been observed here.
2. **Version binding.** The manpage is dated 2018-10-22 and names no sigrok-cli version. REA pins 0.7.2. Treating the page as 0.7.2 behavior is `[INFERENCE]`.
3. **"Instead of a hardware device" does not mean no device access.** The page names an alternate data source. It does not say that `-i` alone avoids USB or serial enumeration.
4. **No host capability.** `command -v sigrok-cli` printed nothing. `pacman -Q sigrok-cli libsigrokdecode` reported both packages as not found (exit 1). No REA signal verb was run. So there is no Evidence id, no bound non-refused record, and nothing that meets the R22-C1 falsifier "a mention without a bound non-refused record counts".
5. **Live acquisition is outside lane bounds.** This wave forbids device contact. The page describes live acquisition but does not make it a lane route. The REA provider also states it does not acquire.
6. **Decoder output fidelity and format autodetection** on any particular recording are documented, not observed.

## Drafted registry row (source accessible; L1 assigns the id — the highest current is S053, and none of S054–S059 appears in the corpus or round-22)

```
| S0xx | sigrok-cli wiki page (embedded manpage) — https://sigrok.org/wiki/Sigrok-cli | docs | A | sigrok-cli's documented split between file input (`-i`) with protocol decoding (`-P`) and driver-based hardware acquisition (`-d`, `--samples/--time/--continuous`); not `--dont-scan`, not the 0.7.2 release, not host installation or any REA run | Revision 16563, last edited 7 July 2023 08:09; Manpage / OPTIONS / `-i, --input-file`; manpage footer October 22, 2018 | Decoding a recorded file and acquiring from hardware are separate documented modes; REA decode-signal-recording maps to the recorded-file mode only, and a doc mention is never T1 evidence. | mined | 2026-10-21 | 90d | .ufo/waves/round-22/w2/PrimarySigrok.md |
```

Gate-table form (round-22 lessons style):

```
| S0xx | https://sigrok.org/wiki/Sigrok-cli ; Manpage / OPTIONS / -i, --input-file (rev 16563, edited 7 July 2023) | “Load input from a file instead of a hardware device.” | Admit documented recorded-input vs hardware-acquisition split; no host install, no REA signal run, no --dont-scan or 0.7.2 claim; zero C1 credit |
```

## Commands, exits, observations

| argv (cwd) | exit | observation |
|---|---|---|
| `curl -sS -L -o sigrok-cli-wiki.html -w '%{http_code} %{url_effective} %{size_download}\n' https://sigrok.org/wiki/Sigrok-cli` (`/tmp`) | 0 | `200 https://sigrok.org/wiki/Sigrok-cli 34557`; sha256 `242b5ad7b6edccc7a7913c760bdb17347fbb297cdc46dff50781383539a04b5d` |
| `curl -sS -L -o sigrok-cli-raw.txt 'https://sigrok.org/w/index.php?title=Sigrok-cli&action=raw'` (`/tmp`) | 0 | `200 18643`; sha256 `3f5b60ae8e5cb14162c3154c9420e6fd09a0ed0a49d10f0eb01cf54fe6e9743b`; 510 lines |
| `curl -sS -L -o sigrok-cli-info.html 'https://sigrok.org/w/index.php?title=Sigrok-cli&action=info'` (`/tmp`) | 0 | `200 15851`; creation 22:46 14 March 2010; latest edit 08:09 7 July 2023; 34 edits, 9 authors |
| `rg -o 'This page was last edited on [^<]*' sigrok-cli-wiki.html` | 0 | `This page was last edited on 7 July 2023, at 08:09.` |
| `rg -o '"wgRevisionId":[0-9]+\|"wgCurRevisionId":[0-9]+' sigrok-cli-wiki.html` | 0 | both `16563` |
| `rg -n -o 'Load input from a file instead of a.{0,40}' sigrok-cli-wiki.html` | 0 | HTML line 156: `Load input from a file instead of a  hardware  device.  You  can` (the first single-space regex returned exit 1 because of nroff double spaces) |
| `rg -n -o 'It is recommended to capture the data first and process them later\.' sigrok-cli-wiki.html` | 0 | HTML line 67, under `id="Usage_tips"` (line 66); the `Manpage` anchor is at line 75 |
| `rg -n -i 'dont-scan\|-D,' sigrok-cli-raw.txt` | 0 | only line 67 `-d, --driver <drivername>`; no `--dont-scan` |
| `command -v sigrok-cli prlimit` | 0 | printed only `/usr/bin/prlimit`; sigrok-cli is not on PATH |
| `pacman -Q sigrok-cli libsigrokdecode` | 1 | `error: package 'sigrok-cli' was not found`; `error: package 'libsigrokdecode' was not found` (read-only query, no transaction) |
| `node -p 'require("./package.json").version'` (REA package root) | 0 | `6.5.0` |
| `sha256sum dist/signals/SigrokRecordingProvider.js; wc -l …` | 0 | `7979bafb…2dced7`, 339 lines |

## Bounds kept

- No installs or updates, so nothing is recorded under the tooling directive. Host pacman transactions are paused, and this task did not need sigrok-cli.
- No REA invocation, MCP use, device or ADB contact, target execution, or account/config inspection.
- No lane writes other than this report.

## Remaining unknowns

- Whether sigrok-cli 0.7.2 `--dont-scan` combined with `--input-file` performs zero device enumeration (needs the 0.7.2 manpage or source, e.g. sigrok-cli git tag `sigrok-cli-0.7.2` `doc/sigrok-cli.1`).
- Whether a sigrok-cli 0.7.2 with libsigrokdecode can be supplied on this host through a non-pacman channel. Without one, both T1 signal verbs stay at zero executed Evidence.
