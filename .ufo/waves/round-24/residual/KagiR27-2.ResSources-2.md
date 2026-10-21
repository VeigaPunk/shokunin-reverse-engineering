# Round-24 source-row falsification — S064–S068 (rows 70–74 of `corpus/SOURCES.md`)

Reviewer: `KagiR27-2.ResSources-2` (read-only leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
branch `main`, HEAD `69e82c48be5614ce96f7c1c32445fe61c4870630`. Scope: quote location, tier/scope honesty,
used-by targets, search-log counts. No lane file was edited; the only write is this report.
Tools: `sha256sum`, `grep`, `cmp`, `python3` (read-only), `gpg` (throwaway GNUPGHOME under
`/fast/scratch/kaidoku-r24/seats/KagiR27-2.ResSources-2`), `curl` (upstream read-back). No install performed.

## Verdict

**Not verified.** The five quotes are genuinely located and every used-by target exists, but two
content defects (one in the tier-A registry row that the C1 count depends on, one in the lesson Gate
table), one retention defect, and four precision/disclosure defects stand. The coverage count itself
is unaffected: `python3 -I -B .ufo/waves/round-24/tools/count-c1.py --root . --rev 69e82c48…` →
`"finding": "c1_complete"`, `t2_held` = all four verbs, exit 0 (instrument's source-row eligibility
uses tier/status/opened/used-by only, so F1 does not move the number). This review does **not** call
round 24 verified.

## Findings

### F1 — Medium — S066/S065 state a TShark flag the provider never passes (`-T fields` vs `-T json`)

- **Observation.** `corpus/SOURCES.md:72` (S066) `teaches`: "Field queries run as `-r … -T fields -2 -Y -d -e`
  under prlimit". `corpus/SOURCES.md:71` (S065) `scope`: "the TShark options REA's tshark-capture provider
  passes (`-2`, `-G fields`, `-T fields`/`-e`, `-Y`, `-d`)".
- **Observation.** REA 6.5.0's provider builds the argv at
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/captures/TsharkCaptureProvider.js:200-218`:
  `"-n","-r","capture","-T","json","--no-duplicate-keys","--temp-dir=."`, then `...(input.two_pass?["-2"]:[])`,
  `...(packet_limit===null?[]:["-c",…])`, `...(display_filter===null?[]:["-Y",…])`, `...decode_as.flatMap(v=>["-d",v])`,
  `...fields.flatMap(f=>["-e",f])`. `-T` is bound to `json`, never `fields`.
- **Observation.** The retained producer record agrees:
  `.ufo/waves/round-24/evidence/c1/l1-packet-capture-http.envelope.json` →
  `normalized_result.tool.arguments = ['-n','-r','capture','-T','json','--no-duplicate-keys','--temp-dir=.','-2','-Y','http.request','-e','frame.number','-e','http.request.uri','-e','ip.src']`.
- **Observation.** `grep -rn '\-T.*fields' …/rea-agents/dist` → 0 hits: no REA 6.5.0 code path passes `-T fields`.
- **Observation.** The same error is propagated into the admitted knowledge entry
  `corpus/knowledge/2026-10-21-r24-pcap-family-envelopes.md:73-74`: "REA builds `-r … -T fields … -2 … -Y … -d … -e`
  (S066, `TsharkCaptureProvider.js:203-217`)" — the cited range itself contains `-T json` at line 205-206.
- **Inference.** A reader reproducing the argv from the row or the entry would pass the wrong output-format
  flag. `scope`/`teaches` honesty is the axis that fails; the C1 count is not affected (instrument eligibility
  does not read `teaches`).

### F2 — Medium-Low — the round-24 Gate table states three wrong quote word counts

- **Observation.** `corpus/lessons/round-24.md:19` (S065) claims the quote is "(19 words)"; whitespace token
  count of the quoted string as printed there = **17**.
  `corpus/lessons/round-24.md:20` (S066) claims "(17 words)"; actual = **19**.
  `corpus/lessons/round-24.md:22` (S068) claims "(13 words)" for "define the research questions and analysis plan
  before observing the research outcomes"; actual = **12**. The second S068 quote (11) is correct.
- **Inference.** S065/S066 appear transposed and S068 is off by one; the counts were not derived from the quotes.
  The CORPUS ≤25-word rule (CORPUS.md Rule 1) is still met, so this is bookkeeping error in the authoritative
  per-row Gate record, not a protocol breach.

### F3 — Low-Medium — the one excluded source family has no retained copy (reproduces the round's own M24-3 defect)

- **Observation.** `corpus/lessons/round-24.md:23` rejects capinfos(1) 4.6.9 as a row, citing
  `doc/man_pages/capinfos.adoc`, sha256 `76a23815…5f61`, and the quote "-c … Displays the number of packets in
  the capture file."
- **Observation.** No such file exists under the lane (`find … -name 'capinfos*'` → 0 hits inside the repo).
  The file exists only in scratch: `/fast/scratch/kaidoku-r24/tshark/wireshark-4.6.9/doc/man_pages/capinfos.adoc`,
  whose sha256 **does** equal the cited `76a23815609fd0b3b6da63c27a548a7c658744b5cc1ad59f131cc1cf4e275f61`.
- **Inference.** The rejection is truthful but not re-verifiable from lane artifacts — the same
  "reproduction-on-scratch" class the round itself logged as M24-3. The fix pattern already exists in
  `.ufo/waves/round-24/repro/inputs.json` + `fetch-inputs.py`.

### F4 — Low — S065's anchor "line495 `-G fields`" is a paraphrase, not a literal

- **Observation.** `grep -n 'G fields' .ufo/waves/round-24/sources/tshark-4.6.9.adoc` → 0 hits; the literal
  string "-G fields" does not occur in the retained adoc.
- **Observation.** The `-G <report type>` option block starts at `tshark-4.6.9.adoc:428`; the `fields` report-type
  entry is at `tshark-4.6.9.adoc:495` ("*fields*[,__prefix__]  Dumps the contents of the registration database to
  stdout."). REA passes the two argv items separately (`TsharkCaptureProvider.js:170` → `const args = ["-G","fields"];`).
- **Inference.** The anchor resolves to the right description, but a literal re-checker scores 0 hits.

### F5 — Low — S065's quote is not a literal substring of the retained copy, and the normalization is undisclosed

- **Observation.** Raw substring count in `.ufo/waves/round-24/sources/tshark-4.6.9.adoc` = **0** (the sentence
  wraps at `adoc:170-171`); whitespace-collapsed count = **1**. `.ufo/waves/round-24/sources/metadata.json:6`
  records `"located": 1` with no `locate_method`, whereas S068 (same file, line 9) explicitly discloses
  "HTML tags stripped, entities unescaped, whitespace collapsed; exact substring count".
- **Inference.** A reviewer running a plain-substring check would conclude the quote is absent.

### F6 — Low — S066's scope covers "prlimit ceilings" but omits the file that defines the pcap provider's ceilings

- **Observation.** The pcap-summary provider's limits live in
  `…/rea-agents/dist/pcap/PcapNativeBound.js:28-30` (`address_space_bytes: 1024**3`, `file_bytes: 64*1024**2`,
  `cpu_seconds: 300`) — a third REA file not among S066's two cited ones. The tshark provider's ceilings are
  `…/dist/process/LinuxResourceLimits.js:10-17` (`cpu_seconds: 30`).
- **Observation.** The retained envelopes agree with both: `l1-packet-capture-http`/`l1-packet-fields-dns`
  `limits.cpu_seconds = 30` and `resource_limiter.arguments = ['--as=1073741824:1073741824','--fsize=67108864:67108864','--cpu=30:30','--core=0:0','--', …]`;
  the dns/tls capture envelopes carry the limitation text "…67108864 bytes per file and 300 CPU seconds; core dumps
  are disabled." (from `PcapNativeBound.js:45`).
- **Inference.** The knowledge entry's "(300 CPU seconds)" is truthful but rests on an uncited file, so the
  registry row does not cover its own scope.

### F7 — Low — S067's "digest-bound" is not true of the client verb

- **Observation.** `corpus/SOURCES.md:73` (S067) `teaches`: "Each verb returns a typed, digest-bound record on a
  pinned input". `.ufo/waves/round-24/evidence/c1/l1-pcap-client.envelope.json` has `subject: null`, no tool
  digest in `normalized_result` — only `tshark_command`/`tshark_version`/`capinfos_command`/`capinfos_version`
  and the limitation "Artifact identity is unavailable for this observation." The tool digests are in the adjacent
  `.run.json` (`tool_sha256`), which S067's own `anchor` cell does disclose.
- **Inference.** The knowledge entry states the null subject honestly; the registry row generalises over all five verbs.

### F8 — Low — search-log counts are arithmetically consistent but the family grouping is unstated

- **Observation.** `corpus/SOURCES.md` search log, entry "2026-10-21 round24": "Identified 6 source families, screened 6,
  included 5 rows S064–S068, excluded 1 (capinfos(1)…)". 5 + 1 = 6 ✓ and this matches the Gate table
  (5 admitted rows + 1 rejected).
- **Observation.** The "Where searched" clause enumerates eight named places (download directory, SIGNATURES file,
  tarball tshark(1), tarball capinfos(1), online tshark page, REA provider files, L1 envelopes, PNAS paper). The
  total of 6 is reachable only by folding "download directory + SIGNATURES file" into one family and
  "tarball tshark(1) + online tshark page" into one; the entry never states that grouping.
- **Observation.** The "Wireshark 4.6.9 download directory" is named as searched but leaves no retained artifact
  (only the SIGNATURES file fetch does). The capinfos rejection lives only in the lesson, not as a registry row with
  `status=rejected` (precedent both ways: S022/S028 keep rejections as rows; round 23's excluded guide likewise was
  not registered).
- **Inference.** The counts are not wrong, but a re-checker cannot reproduce "6" from the sentence as written.

## Verified (checked, no defect found)

- **S064** (`corpus/SOURCES.md:70`). Retained `evidence/tool/SIGNATURES-4.6.9.txt` sha256
  `bfb295581bb1d8da8fe1406f138d1f12bb9174558824ee7ecfa823bf9e594fb5` = the upstream file fetched now
  (2026-10-21) and byte-identical to the scratch copy (`cmp` → IDENTICAL). The quoted line
  `SHA256(wireshark-4.6.9.tar.xz)=d062d416…465fc0f` is verbatim at `SIGNATURES-4.6.9.txt:5`, unique.
  The tarball actually used, `/fast/scratch/kaidoku-r24/tshark/wireshark-4.6.9.tar.xz`, hashes to
  `d062d416a1ab3a49975aafe3a671c882dde0562ccd71b078808ceb59d465fc0f` — equal to the signed line.
  The gpg locator claim was re-verified independently (throwaway GNUPGHOME, key fetched from keys.openpgp.org):
  "Good signature from "Gerald Combs <gerald@wireshark.org>", using RSA key 5A5ADBA7DBEA6C3F87224F1982244A78E6FEAEEA",
  "WARNING: This key is not certified with a trusted signature" — exactly what the row states. (No gpg output receipt
  is retained in the lane, but the retained clearsigned file makes the claim re-checkable.)
  The three committed captures are byte-identical to upstream `test/captures/` members:
  `dns_port.pcap 78c3c00e…`, `http.pcap 69e489a2…`, `tls12-dsb.pcapng d6034147…`.
- **S065** (`corpus/SOURCES.md:71`). Retained `sources/tshark-4.6.9.adoc` sha256 `231c9896a77aeee5d3ccabd15156d6292ce9586865d86ba21ea3c08fe639834f`
  = scratch tarball member `doc/man_pages/tshark.adoc` (same digest). The two-pass sentence also appears in the
  upstream man page (curl + grep → "Perform a two-pass analysis. This causes"). Adoc anchors 170 (`-2`) and 495
  (`fields` report type under `-G`, block opens at 428) resolve to the described content.
- **S066** (`corpus/SOURCES.md:72`). Both cited digests match the installed files
  (`TsharkCaptureProvider.js fdc1fc13…0549`, `domain/pcap/pcapAnalysis.js 7651b4c5…c641`); the cited line anchors
  170 (`["-G","fields"]`), 203-217 (argv block) and 263 (the prlimit limitation text) are exact; the quoted
  sentence is verbatim at line 263 and unique. (The argv content itself is wrong — see F1.)
- **S067** (`corpus/SOURCES.md:73`). All five listed envelopes exist. For each pair, the `.run.json` `stdout` is
  **byte-equal** to the envelope file (sha256 match, e.g. http `9d0fc2fa35c49c51…`, fields `866b899c09d5b050…`,
  dns `3fd2a32101a4c617…`, tls `76b7702949b4119e…`, client `0f331d5f64642666…`), `exit 0`, empty stderr,
  `ok:true`, `meta.command` equal to the verb in each case. The `teaches` claim about embedded secrets was
  independently confirmed by walking the pcapng blocks of `evidence/c1/captures/tls12-dsb.pcapng`: two
  Decryption Secrets Blocks (block type `0x0000000A`) at offsets **96** and **5224**, both secrets type
  `0x544c534b` ("TLSK"), key logs beginning `CLIENT_RANDOM` — no lane key involved, as claimed.
- **S068** (`corpus/SOURCES.md:74`). Retained `sources/nosek2018-pmc.html` sha256
  `12138cdb33758580f82f07d9aa1e8e7e7fabf65acd62fb919dec9806fc1f7f75` matches the row; both quotes are verbatim,
  one occurrence each, after tag-strip/unescape/whitespace-collapse; the second is still present upstream
  (curl + grep → 1). Contexts match the claimed sections: the first sits in the preregistration discussion
  ("…a process called preregistration"), the second in the reporting-deviations discussion ("Jolene can transparently
  report changes that were made and why…"). Scope is honestly bounded ("applied here only to freezing a round's
  counting instruments").
- **Used-by targets.** All eight used-by paths across S064–S068 exist: `corpus/knowledge/2026-10-21-r24-pcap-family-envelopes.md`,
  `corpus/lessons/round-24.md`, `corpus/QUALITY.md`. Each row parses as 13 cells with tier A, status `mined`,
  opened `2026-10-21`, recheck `on-release`/`365d`. The CORPUS.md census commands (tier enum, status enum, kind enum,
  tier-inflation, mined-used-by existence) print nothing; the tier histogram is `A=62 B=5 C=1`.
- **Append-only.** `git diff --unified=0 fe10219e..69e82c48 -- corpus/SOURCES.md` → 0 removal lines; additions are
  exactly 5 registry rows, 2 `## Paths` lines and 1 search-log entry.
- **Count coupling.** `count-c1.py` at `69e82c48` → exit 0, `"finding": "c1_complete"`, all four T2 verbs held; the
  knowledge entry's `source:` line cites S064–S067, each of which lists that entry in `used-by`, and all five
  envelope paths are cited in the entry body — the row-level eligibility the instrument enforces is satisfied.

## Recommended L1 action

1. **Correct the argv, by superseding row, not by editing a cell.** CORPUS.md Rule 2 allows only `status`,
   `recheck` and `used-by` to change in place; `S065.scope` and `S066.teaches` are therefore fixed by a new row
   (S069) whose `teaches` opens "supersedes S066 — " (and, if S065's scope is corrected in the same row, S065 too),
   stating that REA 6.5.0 passes `-T json` (not `-T fields`) and that `-n`, `--no-duplicate-keys`, `--temp-dir=.`
   are always present while `-2`, `-c`, `-Y`, `-d` are conditional. The knowledge entry line 73-74 must be corrected
   in the same pass (its current sentence is contradicted by the very line range it cites). The correction is a
   disclosure, not a silent rewrite, and does not disturb the 4/4 count.
2. **Fix the three word counts in `corpus/lessons/round-24.md:19,20,22`** (17 / 19 / 12 and 11), and log the
   correction in the same round's correction paragraph, following the round-18 and round-23 "W2 correction" pattern.
3. **Retain or pin the excluded capinfos manual** — copy `doc/man_pages/capinfos.adoc` (sha256 `76a23815…5f61`)
   into `.ufo/waves/round-24/sources/` or add it to `repro/inputs.json` with a fetch recipe, so the one exclusion is
   re-verifiable from the lane and M24-3 is not repeated inside the same round.
4. **Disclose the S065 locate method** in `.ufo/waves/round-24/sources/metadata.json` (whitespace-collapsed match,
   sentence spans `tshark.adoc:170-171`) and state the round-24 family grouping in the search-log entry (or adjust
   "identified 6" so the sentence can be recomputed from its own "Where" list). Also decide explicitly whether a
   rejected family is registered with `status=rejected` (S022/S028 precedent) — and apply the answer consistently.
5. **Add the missing scope file** `dist/pcap/PcapNativeBound.js` (300 CPU seconds) to the row that covers the pcap
   provider's ceilings, and qualify S067's "digest-bound" claim for `inspect-pcap-client` (subject null, digests in
   the adjacent `.run.json`).

## Residual risk and verification gaps

- I did not re-run the REA 6.5.0 verbs or re-derive the envelopes; the five envelope/stdout byte-equality and
  exit/command checks above are file-level, and the producer records remain unauthenticated (as the instrument's own
  `limit` field states).
- The upstream `wireshark.org` and `pmc.ncbi.nlm.nih.gov` pages were read once, now; upstream mutation after
  2026-10-21 is not covered.
- The gpg re-verification used a key fetched now from keys.openpgp.org; the key's own trust path is still absent,
  exactly as the row discloses.
- F1–F2 are content corrections that do not change any count; F3–F8 are retention/disclosure/precision items whose
  effect on the C1 number is nil but whose effect on the lane's honesty bar is not.
