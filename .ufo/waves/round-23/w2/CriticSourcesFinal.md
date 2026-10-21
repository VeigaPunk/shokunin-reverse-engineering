# CriticSourcesFinal — R23-C1 source rows vs actual claims

Seat: KaidokuR23.CriticSourcesFinal (critic, author-side, source review only).
Candidate C=`2838351450ff1ee4baa620c962a1153450d53311`, B=`aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
All reads were `git show C:PATH` (except the `git diff B C` stat and row diff). No counter, test, build, producer replay, target execution or network fetch was run. Not a Run* seat, so the count of 4 out of 6 is **not re-measured here**.

Axes: source relevance, quote and teaches support, provenance and ownership, no Dart version mapping, not counting source-only rows.

## Verdict

No source row is held proof by itself, and no refusal is counted through a row. The four new rows S058–S061 are relevant to the verbs they support. Every located quote in the gate table is verbatim in the retained bytes, and both external retained copies match their recorded digests. I found two fixable overreaches in the `teaches` cells (S058, S061), one unlocated source claim, and one inherited unadmitted vocabulary leak ("legacy"). None of them changes which envelope binds to which verb. None needs a tradeoff rejection by the judge.

## Findings

### Verified (observed)

| Item | Evidence | Result |
|---|---|---|
| S058 retained bytes | `sha256sum` of `git show C:.ufo/waves/round-23/evidence/sources/sigrok-cli.1` = `e3f06dfe…a5f9`; fetches.json status 200, size 19180 | Matches the row |
| S058 quote | `sigrok-cli.1:111` "Load input from a file instead of a hardware device." | Verbatim (`corpus/lessons/round-23.md:16`) |
| S058 relevance | decode envelopes' `normalized_result.tool.arguments`: `--dont-scan`, `--input-file=recording`, `--protocol-decoders=…`, `--protocol-decoder-samplenum`, `--protocol-decoder-annotations=uart=rx-data`. The manual documents `-D/--dont-scan` (:67–70), `-i` (:110), `-I` (:130–145), `-P` (:300–346), `-A` (:348–385) and `--protocol-decoder-samplenum` (:425–427) | REA passes exactly the flags the manual documents, so the row is relevant |
| S059 retained bytes | `uart-README.txt` sha256 `7af1c784…6f66`, status 200, size 1277 | Matches |
| S059 quote and teaches | README "This is a collection of example UART communication (only in one direction)."; "625kHz (9600 - 1200)"; "0 (green) TX" | Verbatim, and teaches is supported. The `.sr` metadata (`git show C:…/hello_world_8n1_9600.sr`, zip `metadata`) independently reads `samplerate = 625 kHz`, `probe1 = TX`, driver `chronovu-la8`, consistent with the README |
| S060 quote | `inventory.envelope.json` contains `"returned":110,"has_more":false` (grep count 1) | Verbatim |
| S060 claims | inventory: 110 decoders and `signature` absent. Diagnostics: `SyntaxError … pd.py, line 138` (`0b0000_0010_1001_0001`). decode-uart-hi `annotations_text` = `300-1100 uart-1: 48\n1300-2100 uart-1: 69\n`. Official decode: 12885 lines, `has_more:false`, first lines BA BD C9 B1 91 85 0D 0A, first `48 65 6C 6C …` at 5512. Invalid-decoder: `ok:false`, `execution_failure`, run exit 1 | All match `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:17–23,53–56,76–78,84–86` |
| S061 quote | `"snapshot_hash_sources":2` present in the envelope | Verbatim |
| S061 claims | ABI x86_64. libapp sha256 `f82ab411…a8a8`. Four sections with offsets, sizes, magic, kind and length exactly as in the table at `…dart-legacy-layout-boundary.md:37–42`. `snapshot_hash` `78da37fe…3f3f`. `string_pool.coverage:partial`. Run argv `npx -y rea-agents@6.5.0 inspect-dart-aot <apk> --format json --full-output`, exit 0, stderr empty | Match |
| Original-envelope identity | For all six signal and Dart pairs, `.run.json` `stdout` is byte-equal to the committed `.envelope.json` | Envelopes are untouched originals |
| UART help claim | `uart-help.envelope.json` help lines 45–49 list rx and tx under "Optional channels". Line 32 is the row "rx-data (RX): rx-data, rx-start, …". Manual :371–373: "When names are ambiguous then class names take precedence." | The knowledge claim "`rx-data` selects one annotation class" is supported (manual plus help), and the output contains only data annotations |
| R22 carrier identity | R22 run.json URL `https://f-droid.org/repo/com.adilhanney.saber_1360103.apk`; refusal message lists all four `_kDart…` symbols missing from dynsym | Matches "Saber1360103 refusal" (`…dart-legacy-layout-boundary.md:8`) |
| No universal Dart mapping in admitted text | Searched C's `corpus`, `LOG/SCORECARD/SKILL/PROVINCE` and round-23 evidence/tools for `2\.14`, `dart 2`, `sdk version`, `version map`. Admitted knowledge only *denies* mapping (`…dart-legacy-layout-boundary.md:54–55`; R22 refusal entry :21) | Holds for admitted text |
| Source-only rows are not counted | `count-c1.py:104–124`: a row only gates *eligibility*. Credit needs a cited `.json` under `round-23/evidence/c1/`, an evidence id that appears in that blob, and `bind_new` returning 0. `bind_new` returns 1 on any `ok` other than True or refusal ancestry (:42–56), and `bind_cli` requires `meta.command == verb` (R22 counter :79) | Holds. Refusal and invalid-decoder are not credited, and connector files under `connect-dart-symbols/` are only cited as a directory (`…dart…md:31`), which the `.json` filter skips |

### Defects (fixable)

1. **S058 `teaches` is false for the public decode (observed).** The cell says "decimal samplerate and decoder selections are explicit in the exercised calls". But `decode-official-uart.envelope.json` has `parameters.input_format: null`, and its `tool.arguments` contain no `--input-format`. The 625 kHz rate came from the `.sr` metadata, not an explicit call argument. Only the synthetic call passed `samplerate=960000`. The clause is also about our own calls, not about what the manual teaches.
   - Axes: quote/teaches support, relevance.
   - Smallest correction: change it to "decoder selections are explicit in both exercised calls; samplerate is explicit only for the synthetic binary input, while the `.sr` call uses its file metadata". Optionally add the `-A` row/class precedence (:371–373) to the S058 anchor, because the knowledge relies on it.

2. **S061 `teaches` overgeneralizes the success condition (observed).** "A carrier exporting the four supported snapshot symbols yields complete libapp section/header observations" treats a necessary condition as a sufficient one. The same envelope's `limitations` say complete decoding requires kind 3, a valid hash, and a declared length that fits its symbol, and that "other kind values remain observed with partial coverage". Two further gaps:
   - The envelope's top-level `normalized_result.coverage` is `partial`. The knowledge entry never states this; it reports only `libapp.coverage:complete` and `string_pool.coverage:partial`.
   - Axes: quote/teaches support, premature generalization.
   - Smallest correction: change it to "This carrier, exporting the four symbols with kind-3 data headers and two hash sources, yields libapp coverage complete; top-level and string-pool coverage stay partial". Add one sentence to the knowledge entry recording top-level `coverage:partial`.

3. **An external source is claimed without a locator (observed absence).** The knowledge entry (`…offline-signal-envelopes.md:87–88`), the census (`corpus/SOURCES.md`, round23 search-log line) and the lesson (`round-23.md:24–26`) all assert that the "current upstream REA signal guide" describes `invalid_request`. No URL, commit or digest is recorded: `evidence/sources/fetches.json` has only two entries, and the source is not under Leads. The claim isn't used for counting, but "source linkage absent" is one of the frozen falsifiers.
   - Axes: provenance.
   - Smallest correction: either record the URL, commit and sha in the census exclusion, or delete the sentence about the guide's contents and keep only "6.5.0 observed `execution_failure`".

4. **The "legacy-layout" label comes from unadmitted connector work (observed source, inferred influence).** The word "legacy" appears in the S061 name, the knowledge title and the README map row. It matches the connector's classification (`connect-dart-symbols/preflight_dart_carrier.py:7`, "legacy"; `README.md` "legacy-complete (Dart 3.11.4)", "new-layout (Dart 3.13.2)"; carriers.json labels). Those per-carrier Dart version labels are read from libflutter strings by an unadmitted author-side tool, and the knowledge says connector outputs "stay unadmitted". The admitted evidence shows only "these four symbol names present here, absent in the R22 carrier". The version codes 1330203 < 1360103 suggest an order, but no admitted source establishes a layout generation. The body hedges correctly (:57–60).
   - Axes: false provenance (mild), Dart mapping boundary.
   - Smallest correction: rename the label to "four-symbol-layout" / "dynsym-four-symbol", or add one sentence that "legacy" is a descriptive label borrowed from unadmitted connector receipts, not a sourced SDK generation.

### Tradeoffs and risks (no defect)

- **A producer-text Dart label is present but correctly not adopted (observed).** The S061 envelope's `limitations[2]` says "kind 3 (the Dart 2.14 FullAOT layout)". The unadmitted connector carriers.json/README attributes Dart 3.11.4 and 3.12.2 to kind-3 carriers. If that is accurate, the producer's own kind→version label isn't universal. The knowledge paraphrases neighbouring limitations but omits this one, which is the safe choice. An optional one-line note ("the producer's kind-3 label is producer text, not adopted") would make the omission explicit. This is not a count defect.
- **The S061 source is circular (own-work = the counted envelope)** and no non-own-work source backs the Dart interpretation. This is permitted by the acceptance ("own-work permitted"), and the counter still binds the envelope rather than the row. Source relevance is "manual" (`count-c1.py:8`): any S058+ row in the first line makes every cited `.json` plus evidence id in that entry eligible, regardless of which row is relevant. This is safe today only because each entry's cited envelopes and mentioned verbs line up (observed). A future entry could cite an irrelevant docs row to gain eligibility. This is a counter-design residual, not a C defect.
- **S059 "Release commit" wording.** I didn't verify whether sigrok-dumps has release tags (no network). The URL is commit-pinned, so the `180d` recheck is only conservative. Status unknown.
- **Fetch order.** The official `.sr` was fetched at 14:38:57 and its README at 14:41:40, so the carrier was chosen before its provenance doc was opened. This is harmless and disclosed by the timestamps.

## Produced files and hashes

- `.ufo/waves/round-23/w2/CriticSourcesFinal.md` (this file). Its hash is not recorded inside itself because it would be self-referential; compute it with `sha256sum` on the path.
- Scratch copies were made under `/tmp/csf` (git-show extracts only), outside the lane, and are not retained as evidence.

## Installs

None.

## Open risks

- The 4/6 count is inferred from source only. It must come from the designated Run seat's counter at C.
- Defects 1–4 are source-text fixes. If L1 edits S058/S061 after admission, the counter's prefix check (`count-c1.py:72`) only freezes rows S001–S057, so the edits are allowed but need re-review.
