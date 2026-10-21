# PublicDownload: R23-C1 source review of official-download.json and the committed hello_world_8n1_9600.sr

Seat: KaidokuR23.PublicDownload (leaf source reviewer).
Candidate: `2838351450ff1ee4baa620c962a1153450d53311` (author 2026-10-21 11:58:15 -0300). Baseline B: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Scope: `.ufo/waves/round-23/evidence/c1/official-download.json` and `.ufo/waves/round-23/evidence/c1/hello_world_8n1_9600.sr`, read only from committed bytes at the candidate revision.

Method and limits: every read was `git show`, `git log`, or `git grep` pinned to the candidate revision, or `python3 -I -B` analysis of those committed bytes passed on stdin. No producer rerun, no network access to the URL or any mirror, no target, device or process access, no subagents, no installs, no edits to any peer report. One temporary copy of the .sr that I wrote to `/tmp` during review was deleted and confirmed absent.

Labels: **[O]** observed by a command at the candidate revision. **[I]** inference from observed facts. **[U]** unknown or not retained in the candidate.

## Bottom line

1. **Bound to the local bytes.** The record's `size` (58381) and `sha256` (`01b72610…f900b61`) equal the committed .sr exactly [O]. REA's decode envelope records the same subject digest [O], and `describe-signals.py` compares them [O].
2. **Not bound to any fetch.** `status: 200` and `captured_at` have no producer, transcript, header capture or checker in the candidate. No committed program downloads or writes `official-download.json` [O]. The URL-to-bytes link rests on a W1 GitHub read whose responses are not retained [O/U].
3. **Attribution is partly unretained.** "Official" appears only in the filename and in W1 quotes from a different commit (6bf0de22) [O]. The tag-to-commit mapping is W1 prose only [O/U]. The fixture has no source row in `corpus/SOURCES.md` [O].
4. **Content facts.** 625 kHz, TX, 8388608 samples and 9600-baud bit timing are supported by the committed sample stream itself [O]. 8n1 framing is bound by no committed artifact [O].
5. **W1 errors.** Several W1 statements about this fixture are contradicted by the committed bytes: the version member, the tail samples, and a "same pinned commit" claim [O].

Supported: the candidate commits a third-party file whose size and digest match the record, at the URL commit string the record names.
Not supported: "HTTP 200 observed at 14:38:57Z", "official" as a record fact, and any fixture-level source row.

## Findings

### F1 · High · Acquisition fields are self-asserted

- `official-download.json:3` `"status": 200` and `:6` `"captured_at": "2026-10-21T14:38:57.638074+00:00"` are the only retained copies of these values [O]. The record has five keys (`url`, `status`, `size`, `sha256`, `captured_at`) and no path, tool identity, argv, headers, ETag or transcript [O].
- **No writer.** A `git grep` for `download|urlopen|requests.get|curl|wget` over `tools/`, `gen-wave1.py` and `gen-wave2.py` returns only prompt strings, a docstring in `setup-sigrok.py:4` stating "No download", and an unrelated read of `legacy-saber-download.json` in `describe-dart.py:34` [O]. A `git grep` for `official-download` across `.ufo/waves/round-23` finds the file itself, prose in W1 documents, and the prompt string in `gen-wave2.py:34` [O].
- **No checker reads the record.** `describe-signals.py` recomputes the .sr sha256 and compares it with the REA envelope subject digest (`describe-signals.py:42, 58–61`) [O]. `count-c1.py` collects only full-path `.ufo/waves/round-23/evidence/c1/…json` citations (`count-c1.py:97, 112–113`). The knowledge entry cites the record bare (`corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:68`), and the .sr path does not end in `.json`. Neither is counted, and `count-c1.py` has no .sr digest comparison [O]. The frozen selftest manifest names no `hello_world_8n1` input [O].
- **Timing.** The record's capture (14:38:57.638Z) precedes the decode run's `captured_at` (`decode-official-uart.run.json:24`, 14:38:58.876Z) and the commit that added the record, 2b40aec, at 11:56:57 -0300 (14:56:57Z) [O]. The record and the .sr were never modified after that commit: `git log <rev> -- <both paths>` lists only 2b40aec [O]. The ordering is consistent [O], but ordering is not acquisition evidence [I].
- **Overstated labels.** `w1/CoverageMap.md:73` calls the record a "fetch receipt" with "HTTP 200". `w1/ReviewArtifactIdentity.md:14` says "downloaded for offline decoding". Neither has a retained producer or transcript [O].

### F2 · Medium · Pinned-commit attribution is unretained

- `url` (`official-download.json:2`) pins `c8fad0528648ba58ceddbda9e34e4dfcd293a6b0` (40 hex) [O]. The same string appears in `evidence/sources/fetches.json:11`, `corpus/SOURCES.md:65` and the knowledge entry at lines 1 and 65 [O]. These are string-level matches only.
- The tag `sigrok-dumps-0.1.0` mapping to c8fad05 (dated 2012-05-18) appears only as W1 prose: `w1/SignalCarrierAlternatives.md:17–19`, "Observed via GitHub tags API and commit API" [O]. A `git grep` for the c8fad05 string and `sigrok-dumps` finds no retained API response [O].
- W1 reports git blob ids `71f8ecfb…` for the .sr and `57365d63…` for the README (`SignalCarrierAlternatives.md:25–26, 31`). I computed the same values from the committed bytes [O]. The API responses those ids came from are not retained [U].
- The URL-to-bytes link therefore cannot be checked offline. Re-fetching is barred by this wave's contract [U].
- **"Official".** The filename `official-download.json` asserts it, and no field in the record does. The retained README (`evidence/sources/uart-README.txt`) never uses the word [O]. W1's support quotes the root README at commit **6bf0de22** (`SignalCarrierAlternatives.md:12–16`). That section calls it "the same pinned commit", but its own URL on line 16 is 6bf0de22 and the selected pin is c8fad05 [O].

### F3 · Medium · The fixture has no source row (claims falsifier "source linkage absent")

- `corpus/SOURCES.md` rows: S058 (line 64, sigrok-cli manual), S059 (line 65, README at c8fad05), S060 (line 66, own envelopes), S061 (line 67, Dart). Only line 65 matches a fixture term (`8n1`, `hello`, `.sr`, `fixture`) [O].
- The knowledge entry header (line 1) cites S058, S059 and S060 and no fixture row. Its body cites the fixture URL (line 65), the committed copy (lines 66–67) and the record as "HTTP200/size/digest receipt" (line 68) [O].
- `w1/SourceRegistry.md:58` says "the README, not the `.sr` fixture, is the registered source". `:145` says "no row". `:258` plans S065 "Only if a knowledge entry uses the fixture itself". That trigger is met and S065 does not exist [O].
- `w1/PlannerDataWalk.md:80` maps the .sr to "Source row S059". S059 is the README row [O].
- `claims.json:28` requires "exact used-by" S058+ citations for new knowledge. The fixture has no such row [O].

### F4 · Low · README: bytes bound, receipt fields unbound

- `evidence/sources/uart-README.txt`: 1277 bytes, sha256 `7af1c7841a603eb1f6dfecbe1402acd980e175e7e31cd62daf2fe2a0caed6f66`, git blob `57365d63825e30abfdc19362d0c8c1da03312535` [O]. These match `fetches.json:14–15` (sha256, size) [O].
- `fetches.json:12` (status 200) and `:16` (`accessed_at` 2026-10-21T14:41:40.337220Z) have no writer in `tools/` or the gen scripts [O]. They are unbound.
- The .sr has no `fetches.json` entry. Its receipt uses a different shape (`captured_at`, no `path`, no `accessed_at`) [O]. Two fetched artifacts in this candidate therefore have receipts in two different shapes.

### F5 · Positive: bytes-level facts confirmed

- **Archive.** `hello_world_8n1_9600.sr`: 58381 bytes; sha256 `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61`; git blob `71f8ecfb173bd8aab17fbf208d3a33e0ec4febff`. ZIP `testzip` OK, empty archive comment, zero trailing bytes after the end-of-central-directory record [O].
- **Members.** `version` (1 byte, content `1`), `logic-1` (8388608 bytes, deflate), `metadata` (150 bytes). The metadata text, verbatim: `[global] / sigrok version = 0.2.0 / [device 1] / driver = chronovu-la8 / capturefile = logic-1 / unitsize = 1 / total probes = 8 / samplerate = 625 kHz / probe1 = TX` [O].
- **Timestamps.** All three ZIP members carry 2011-12-04 14:43:26 [O]. These are upstream packaging times, nearly 15 years before `captured_at`. They are not acquisition evidence [I].
- **Sample stream** (`logic-1`; byte values are only {0, 1}, so bit 0 is the only active channel) [O]:
  - First 16 bytes are `0x01`; last 16 bytes are `0x00` [O].
  - 79,154 runs of bit 0. Run lengths: 65 samples (44,625 runs), 130 (13,865), 195 (3,844), 260 (3,258), 391 (570). No runs in 30–36 [O].
  - Mean of runs in 55–75 samples is 65.1021. At 625 kHz that gives 625000 / 65.1021 = 9600.31 baud [O].
  - 79,152 of 79,154 runs lie within one sample of an integer multiple of 625000/9600 = 65.1042. The two misfits are the first run (index 0, length 42, level 1) and the last run (index 8,388,567, length 41, level 0), i.e. the capture boundaries [O/I].
  - Sample count 8388608 equals README `--samples 8388608` (`uart-README.txt:35`) [O].
  - **Interpretation:** 9600 baud at 625 kHz is supported by the committed bytes themselves, not only by the filename and README [I, with bit 0 = TX inferred from `probe1 = TX` and `unitsize = 1`].

### F6 · Medium · 8n1 framing is not bound

- The .sr metadata has no framing or baud field [O].
- The decode argv for the official fixture is `uart:rx=TX:baudrate=9600`, `--annotations uart=rx-data`, `--all_lines`. It sets no data-bit, parity or stop option. Exit 0, stderr empty (`decode-official-uart.run.json`) [O].
- "8n1" therefore rests on the filename and on the README's generic list of settings (`uart-README.txt:7`) [O]. I did not decode the stream. Decoding belongs to the decode item.

### F7 · Low · README scope is directory-level

- The README describes examples across settings, not this file [O]:
  - one-direction UART (`:5`);
  - payload "Hello World!\r\n" (`:6`);
  - settings such as 8n1, 8o1, 8e1, 7o1, 7e1 (`:7`);
  - sender Olimex STM32-H103, USART1.TX (`:9–11`);
  - ChronoVu LA8 at 625 kHz for 9600–1200 baud (`:22–23`);
  - probe 0 (green) TX (`:27`);
  - command `sigrok-cli -d 0:samplerate=<hz> --samples 8388608 -p '1=TX' -o <file>.sr` (`:35`).
- It does not name `hello_world_8n1_9600.sr`, does not say "official", and states no license [O].
- S059's "The supplied third-party recording documents … 625kHz at 9600 baud" (`SOURCES.md:65`) reads a range table as a per-file statement [I]. Per-file 9600 is now supported by bit timing (F5), not by the README text.

### F8 · Open · No license basis retained

- Neither the README nor the .sr carries license text in the candidate [O]. The candidate commits a third-party 58,381-byte copy with no retained redistribution basis [U].

## Attribution vs acquisition

| Claim | Class | Retained where | Independently bound? |
|---|---|---|---|
| Source is sigrokproject/sigrok-dumps | attribution | `official-download.json:2` string; `SOURCES.md:65` | No (string only) |
| Commit c8fad05 = tag sigrok-dumps-0.1.0 (2012-05-18) | attribution | W1 prose only | No (API unretained) |
| "Official" | attribution | filename only; W1 quote from 6bf0de22 | No |
| Sender Olimex STM32-H103; one direction; payload | attribution | README text | No (documentary) |
| 625 kHz; TX; 8388608 samples | attribution, also in bytes | .sr metadata; `logic-1` length | Yes (bytes) |
| 9600 baud | attribution | filename; README range | Yes (bit timing, F5) |
| 8n1 framing | attribution | filename; README list | No (F6) |
| size 58381; sha256 `01b72610…` | observed, local file | `json:4–5` | Yes (recomputed; REA envelope digest; `describe-signals.py:61`) |
| URL fetched from that commit | acquisition claim | `json:2` | No (no receipt) |
| HTTP status 200 | acquisition claim | `json:3` | No (no producer, no transcript) |
| `captured_at` 14:38:57.638Z | acquisition claim | `json:6` | No (ordering only) |
| "Downloaded" / "fetch receipt" | acquisition wording | `CoverageMap.md:73`; `ReviewArtifactIdentity.md:14` | Overstated |

## Re-evaluation of stale W1 findings against 2838351450ff1ee4baa620c962a1153450d53311

| W1 statement | Location | Result |
|---|---|---|
| `version` contents "2" | `w1/SignalCarrierAlternatives.md:68` | CONTRADICTED. Committed `version` member is `1` [O] |
| `logic-1`: "first and last 16 bytes all `0x01`" | `:69` | HALF CONTRADICTED. First 16 are `0x01`; last 16 are `0x00` [O] |
| "`0x01` run at both ends … idle-high" | `:87–88` | CONTRADICTED at the tail. Final run is low (41 samples, capture boundary) [O] |
| "Root README at the same pinned commit" | `:12–16` | INCONSISTENT. Quoted README is at 6bf0de22; selected pin is c8fad05 [O] |
| 8n1 and 9600 from filename | `:59–60` | 9600 CONFIRMED by bytes (F5). 8n1 NOT bound (F6) |
| 625 kHz and TX "independently confirms" | `:84` | CONFIRMED by metadata [O] |
| Size and sha256 | `:23–24` | CONFIRMED [O] |
| .sr blob `71f8ecfb…` | `:25–26` | Value CONFIRMED against committed bytes; API read UNRETAINED [O/U] |
| README 1,277 B; sha `7af1c784…`; blob `57365d63…` | `:28–31` | Bytes CONFIRMED; API read UNRETAINED [O/U] |
| Metadata block, verbatim | `:72–82` | CONFIRMED [O] |
| README excerpt | `:36–55` | CONFIRMED against `uart-README.txt:19–35` [O] |
| Tag-to-commit; sigrok.org tarball listing; root README quotes | `:12–19, :33–34` | UNRETAINED [U] |
| Alternate pin 6bf0de22 (URL; sha `b87f1f63…`; blob `2dc085f3…`; 705 B; sigrok 0.4.0-git) | `:90–109` | UNRETAINED; not in committed tree; not checked [U] |
| "HTTP 200" | `w1/ConnectSignalFirmware.md:74` | Record-only; UNBOUND (F1) [O] |
| `official-download.json (42648310…)` | `w1/ConnectSourceChain.md:26` | CONFIRMED: record's file sha256 begins `426483100c0df544` [O] |
| "downloaded for offline decoding" | `w1/ReviewArtifactIdentity.md:14` | OVERSTATED (F1) [O] |
| "fetch receipt" | `w1/CoverageMap.md:73` | OVERSTATED (F1) [O] |
| .sr mapped to "Source row S059" | `w1/PlannerDataWalk.md:80` | WRONG ROW (F3) [O] |
| No .sr row; S065 only if used | `w1/SourceRegistry.md:145, :258` | CONFIRMED absent; trigger met (F3) [O] |

## Open risks

- The acquisition event (HTTP status, capture time, and the URL-to-bytes link) cannot be reproduced or audited from committed bytes. Any future audit needs a retained transcript or a committed producer that records response headers and ETag.
- The commit-level identity (c8fad05 contains blob `71f8ecfb…` at the fixture path) is unverified offline. It rests on an unretained W1 API read.
- 8n1 framing is unbound. The sibling decode's initial annotations (`BA BD C9 B1 91 85 0D 0A`, per the knowledge entry lines 77–78 and `w1/ConnectSignalFirmware.md:68`) are outside this item and were not re-derived.
- The license or redistribution basis for committing a third-party fixture is not retained (F8).
- Decode envelopes carry machine-local absolute paths (for example `decode-official-uart.envelope.json` `subject.local_path`), so envelope provenance is not portable across hosts. Low.
- The ZIP member timestamps (2011-12-04) must not be cited as capture or acquisition times.
- The bit-grid result assumes TX = bit 0 (from `probe1` and `unitsize = 1`). It establishes the bit period, not framing or payload correctness.

## Commands (all at the candidate revision; no errors reported)

- `git log -1` and `git log -- <both paths>` (pinned-revision metadata and history).
- `git grep -n -I` over `.ufo/waves/round-23`, `corpus` and `round-22/evidence/c1` for `official-download`, `c8fad05…`, `sigrok-dumps` and `hello_world_8n1`.
- `git grep` over `tools/`, `gen-wave1.py` and `gen-wave2.py` for writers and downloaders (`captured_at|urlopen|official-download|legacy-saber-download`; `download|urlopen|requests.get|curl|wget`; `fetches.json|accessed_at`).
- `git show <rev>:<record> | python3 -I -B` (parse, types, timestamps).
- `git show <rev>:<.sr> | python3 -I -B` (sha256, git blob sha1, ZIP integrity, member metadata, verbatim text, sample-stream run-length analysis, exact misfit count).
- `git show <rev>:<README> | cat -n`, `sha256sum`, `wc -c`, and a git blob sha1 computed in python.
- `git show <rev>:corpus/SOURCES.md | python3 -I -B` (S058–S061 rows; fixture-term matches).
- `git show <rev>:<knowledge entry>`, `<fetches.json>`, `<decode-official-uart.run.json>`, `w1/SignalCarrierAlternatives.md`, `count-c1.py` and `describe-signals.py` (read only).

## Produced files, hashes, installs

- Produced: `.ufo/waves/round-23/w2/PublicDownload.md` (this file). Its sha256 is reported in the final message, since a file cannot hash itself.
- Temporary: one copy of the .sr written to `/tmp` during review, deleted; `test -e` returned absent.
- Installs: none. No packages, tools or configuration changed. python3 was run only with `-I -B` on stdin, writing no bytecode and no temp files.

Report: .ufo/waves/round-23/w2/PublicDownload.md
