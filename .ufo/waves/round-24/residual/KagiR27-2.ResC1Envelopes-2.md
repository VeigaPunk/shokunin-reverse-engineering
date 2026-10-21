# Residual review — C1 packet-capture family envelopes and their knowledge entry

Seat: `KagiR27-2.ResC1Envelopes-2`. Scope: (a) re-run the five retained argv in
`.ufo/waves/round-24/evidence/c1/l1-*.run.json` into a scratch dir and compare
`normalized_result`/`evidence_id` against the committed envelopes; (b) check every
claim in `corpus/knowledge/2026-10-21-r24-pcap-family-envelopes.md` against those
envelopes (exact values, quotes, the DSB block-walk statement).

Scratch: `/fast/scratch/kaidoku-r24/seats/KagiR27-2.ResC1Envelopes-2`.
No lane file was edited; no mutating git/jj command was run in the lane; the lane
working tree was read only. One throwaway clone under the scratch dir was used to
commit a copy of the working tree so the counter could be run against a rev that
contains the concurrently-updated entry; the lane itself is untouched. Nothing was
installed (no pacman, no tool install) — the pinned Wireshark 4.6.9 build and
`rea-agents@6.5.0` were already present.

## Verdict

**The five envelopes are reproducible; the entry's per-verb factual content checks
out against them.** All five retained argv re-run to exit 0 and reproduce every
`data.evidence_id` and a byte-identical `normalized_result`; the only field that
moves across runs is `meta.duration`. Every numeric value, evidence id, subject
digest, provider/operation name, quote and the DSB block-walk statement in the
entry were checked against the envelopes and hold.

**Three defects remain, all in the entry's prose, not in the envelopes.** Two are
factual errors a reader can be misled by (the version-range sentence and the
timestamp range); one is an over-broad citation glob. None of them changes the
C1 count, which I re-measured as 4/4 at the lane commit and 4/4 against a
commit of the updated entry. **I do not call round 24 verified.**

## Findings

### F1 — Medium — the entry denies a version-range check that both providers perform

- **Observation** (`corpus/knowledge/2026-10-21-r24-pcap-family-envelopes.md:41`):
  "It reports both commands as `environment`-sourced and echoes their version
  strings; **it does not check version range itself** and reads no capture."
- **Observation** (`.../rea-agents/dist/domain/pcap/pcapAnalysis.js` and
  `dist/cli-runtime/cli.js:17660-17666`): the pcap provider's `parseVersion`
  parses the `--version` banner with
  `^${tool} \(Wireshark\) (\d+)\.\d+\.\d+` and then
  `if (parsed[1] !== "4") throw new PcapConfigurationFailure(\`${tool}_version_unsupported\`, …)`.
  That is a version-range gate on the major version.
- **Observation** (`dist/cli-runtime/cli.js:700`, the tshark-capture provider):
  `if (!/^TShark \(Wireshark\) 4\.[0-9]+\.[0-9]+(?:[ .(\r\n]|$)/u.test(version.stdout.text)) throw new Error("Expected TShark 4.x; inspect the selected installation.");`
- **Falsification (executed, exit codes as shown).** With a stub `tshark`/
  `capinfos` printing `TShark (Wireshark) 3.6.20`, `npx -y rea-agents@6.5.0
  inspect-pcap-client --format json --full-output` returns
  `{"ok":false,"error":{"code":"capability_unavailable","category":"unsupported_provider","message":"Packet summary inspection currently requires Wireshark 4.x tools; select an installation with the admitted output profile."}}`
  — the `pcap` provider refuses a 3.x tool. The same stubs against
  `inspect-packet-fields` return `ok:false` with
  `"Expected TShark 4.x; inspect the selected installation."`. Stubs printing
  `4.0.0` and `4.99.99` are **accepted** (`ok:true`), so the gate is major-version-4,
  not a narrower range.
- **Inference.** The sentence is false as written for the family: REA does check
  version range (major version 4) on both the `pcap` and `tshark-capture`
  providers. It is true that the client verb performs *no* version check of its
  own beyond what the provider does — the provider is what refuses — but the
  entry attributes the absence of a check to the wrong layer, and a reader who
  trusts it would expect a 3.x TShark to be accepted. Note the same stale
  "no version range" idea also appears in `corpus/lessons/round-24.md` and in
  `PROVINCE.md`'s round-24 section ("replacing it or its libraries with another
  runnable installation need not be refused" — true only within 4.x).
- **Scope.** This does **not** disturb the count. `count-c1.py` binds on
  `ok:true` / `meta.command` / `data.operation` / evidence id, not on prose.

### F2 — Medium — the entry's input timestamp range excludes `http.pcap`

- **Observation** (`.../2026-10-21-r24-pcap-family-envelopes.md:112`):
  "Inputs are tiny, old, public test captures (**2004–2018 timestamps**)."
- **Observation** (independent, `capinfos -a -e` on the lane's own committed
  copies, and `tshark -T fields -e frame.time_epoch`): `http.pcap` earliest and
  latest packet time is **2002-12-31 11:55:31.300000** (epoch 1041342931.300),
  `dns_port.pcap` is 2004-09-27 (epoch 1096255084.938672), `tls12-dsb.pcapng` is
  2018-11-17 (epoch 1542465083.420067).
- **Inference.** Two of the three inputs are 2004–2018, but `http.pcap` is
  2002, so the stated range does not cover all three inputs the entry names.
  The correct span is 2002–2018. The entry is describing its own inputs, so this
  is an internal factual slip, not a source misattribution.
- **Note.** The `http.pcap` envelope itself carries no timestamp field
  (`inspect-packet-capture` returns only `frame.number`, `http.request.uri`,
  `ip.src`), so this value is not contradicted by the envelope — it is an
  unsupported range claim that happens to be wrong. The `capture_start` fields in
  the two `inspect-pcap-capture` envelopes do read `2004-09-27` and
  `2018-11-17`, which is likely where the range came from.

### F3 — Low — the round-22 citation glob covers only two of the four verbs

- **Observation** (`.../2026-10-21-r24-pcap-family-envelopes.md:13-15`): "Round 22
  placed **all four verbs** `frontier-blocked` … (`.ufo/waves/round-22/evidence/c2/inspect-pcap-*.json`,
  ENOENT and missing REA_TSHARK_COMMAND refusals)".
- **Observation** (glob semantics, verified with `fnmatch`): `inspect-pcap-*.json`
  matches `inspect-pcap-capture.json` and `inspect-pcap-client.json` only. It
  does **not** match `inspect-packet-capture.json` or `inspect-packet-fields.json`,
  which are the two files holding the *other* two verbs' refusals.
- **Observation** (the two refusal families differ, so the sentence's "ENOENT and
  missing REA_TSHARK_COMMAND" describes two distinct records):
  `inspect-pcap-capture.json` / `inspect-pcap-client.json` →
  `code: capability_unavailable`, `"Cannot run selected tool tshark: spawn tshark ENOENT…"`;
  `inspect-packet-capture.json` / `inspect-packet-fields.json` →
  `"Supply absolute REA_TSHARK_COMMAND for TShark 4.x…"`. All four are listed as
  `frontier-blocked` in `PROVINCE.md:190-193`, so the *claim* is right; the cited
  glob does not reach half the evidence.
- **Inference.** The citation should name the two globs (`inspect-pcap-*.json`
  and `inspect-packet-*.json`), or all four paths. Low severity — the substance
  (all four were frontier-blocked, because no TShark existed) is verified by
  `PROVINCE.md` and by the four refusal envelopes I read.

### F4 — Low — the `4 MiB combined output` ceiling is quoted from the wrong provider

- **Observation** (`.../2026-10-21-r24-pcap-family-envelopes.md:100-102`):
  "tshark-capture runs under prlimit: … 4 MiB combined output (S070,
  `TsharkCaptureProvider.js:263`)".
- **Observation** (the two tshark-capture envelopes disagree with each other on
  this ceiling): `l1-packet-capture-http.envelope.json` → `limits.output_bytes`
  = 4194304 (4 MiB); `l1-packet-fields-dns.envelope.json` → `limits.output_bytes`
  = 33554432 (**32 MiB**) plus `record_budget_bytes` = 8388608 (8 MiB).
- **Observation** (`dist/captures/TsharkCaptureProvider.js:60`):
  `const limits = "path" in input ? LIMITS : { ...LIMITS, output_bytes: 32 * 1024 * 1024 };`
  — the no-path (fields) branch raises the output ceiling to 32 MiB, and the
  source comment says why: "TShark 4.6.9 emits a 22.3 MB glossary; keep capture
  output capped at 4 MiB." I measured the glossary at **22302672 bytes (21.3 MiB)**,
  which exceeds 4 MiB — so the 4 MiB figure cannot be the fields path's ceiling.
- **Inference.** The sentence attributes one ceiling to the whole provider. It
  holds for `inspect-packet-capture`; for `inspect-packet-fields` the committed
  envelope reports 32 MiB output and an 8 MiB record budget. The cited line 263
  is the capture-path limitation string. The entry's own `inspect-packet-fields`
  paragraph does not mention the 32 MiB / 8 MiB ceilings at all.

## Checks that passed

- **Replay of all five retained argv.** Ran each `argv` from the five
  `l1-*.run.json` verbatim with the recorded `REA_TSHARK_COMMAND` /
  `REA_CAPINFOS_COMMAND` overrides, into the scratch dir. All five exit 0 and
  reproduce the committed `data.evidence_id` **exactly**, and a
  canonicalised (`sort_keys`, tight separators) `normalized_result` compares
  **byte-identical** to the committed envelope in every case:

  | envelope | evidence_id | normalized_result | full envelope |
  |---|---|---|---|
  | l1-pcap-client | match | byte-identical | differs only in `meta.duration` |
  | l1-pcap-capture-dns | match | byte-identical | differs only in `meta.duration` |
  | l1-pcap-capture-tls | match | byte-identical | differs only in `meta.duration` |
  | l1-packet-capture-http | match | byte-identical | differs only in `meta.duration` |
  | l1-packet-fields-dns | match | byte-identical | differs only in `meta.duration` |

  Stripping `meta.duration` makes all five envelopes equal to their committed
  counterparts. The committed `stdout` in each `*.run.json` is byte-equal to the
  committed `*.envelope.json` (all five), so the envelopes are the producer
  stdout, not a re-serialisation.
- **Entry ↔ envelope value check, all pass.** Evidence ids: the five
  `ev_<64hex>` ids cited in the entry each resolve to exactly the envelope the
  entry names (and to no other). Subject digests: `78c3c00e…` (dns_port.pcap),
  `d6034147…` (tls12-dsb.pcapng), `69e489a2…` (http.pcap), and the fields
  envelope's subject is the tshark binary `00ed7bde…6f770d` — all match. Per-verb
  facts: `inspect_pcap_client` / `inspect_pcap_capture` / `inspect_packet_capture`
  / `inspect_packet_fields` operations; provider ids `pcap` and `tshark-capture`;
  `subject: null` for the client; the client limitation "Artifact identity is
  unavailable for this observation."; dns `pcap`/`ether`/4 packets/
  `eth:ethertype:ip:udp:dns`/2 endpoints/`us.pool.ntp.org`/17 response
  addresses/`coverage: complete`/empty `capinfos_stderr` and `tshark_stderr`/
  `confidence: derived`; tls `pcapng`/`rawip4`/17 packets/SNI `example.com` and
  `example.net`/URIs `https://example.com/` and `https://example.net/`; http
  frame 1, URI `/v4/iuident.cab?0307011208`, source `10.0.0.5`, window 1/1/
  `has_more:false`, `read_scope: to-eof`, `confidence: observed`; fields
  `examined 269366`, `matching 356`, `returned 50`, `has_more:true`.
- **The "269366 registrations" figure is reproducible and correctly attributed.**
  I re-implemented REA's own counting logic
  (`dist/captures/parseFieldDiscovery.js`: skip `P` rows when `kind == "fields"`,
  require exactly 3 or 8 tab columns) over a fresh `tshark -G fields`: 272534
  total lines, 3168 `P` rows, **269366** `F` rows, of which **356** have
  `parent_protocol == "dns"`. Both numbers in the entry are exact.
- **The DSB block-walk statement holds.** Walking the pcapng block headers of
  `tls12-dsb.pcapng` myself: exactly **two** Decryption Secrets Blocks, block
  type `0x0A`, at byte offsets **96** and **5224** — matching the entry. The
  secrets-type field carries `0x544c534b` (TLS Key Log) in both, and the payloads
  are NSS key-log text whose secret lines begin `CLIENT_RANDOM` (block 1 also
  opens with a `# first` comment line). The value matches
  `wiretap/secrets-types.h` (`SECRETS_TYPE_TLS 0x544c534b`) and the IETF pcapng
  draft's "0x544c534b: TLS Key Log".
- **The "TShark applies embedded secrets without any lane-supplied key" claim
  is falsifiable and survives falsification.** I rebuilt the capture with both
  DSB blocks removed (9860 bytes, no `0x0A` blocks) and re-ran TShark: the
  `http` layer vanishes entirely while `tls.handshake.extensions_server_name`
  still yields `example.com` and `example.net`. So the HTTP layer is produced by
  the embedded secrets and the SNI is not — exactly what the entry discloses.
- **The comma-joined `--fields` refusal is real and now has a retained record.**
  `tshark -e "http.request.uri,ip.src"` exits 1 with `tshark: Some fields aren't
  valid:`. The lane's new
  `.ufo/waves/round-24/evidence/probes/refusal-comma-fields.envelope.json` is
  `ok:false`, `execution_failure`, exit 1, stderr
  `tshark: Some fields aren't valid:\n\thttp.request.uri,ip.src`, with a matching
  `*.run.json` whose stdout is byte-equal to the envelope.
- **Tool provenance.** The pinned binaries still match `tool-pins.json`
  (`tshark 00ed7bde…6f770d`, `capinfos 1b3385db…54ba`), the source tarball at
  `/fast/scratch/kaidoku-r24/tshark/wireshark-4.6.9.tar.xx` is
  `d062d416a1ab3a49975aafe3a671c882dde0562ccd71b078808ceb59d465fc0f`, matching
  the `SHA256(...)` line of the retained `SIGNATURES-4.6.9.txt`; I re-ran
  `gpg --verify` in a throwaway GNUPGHOME and got "Good signature from Gerald
  Combs" with "WARNING: This key is not certified with a trusted signature!" —
  i.e. good signature, no web-of-trust path, as claimed. The three committed
  captures are byte-identical to the tarball's `test/captures/` members, and
  TShark reports `-Lua` (Lua off), matching the entry's "Lua disabled".
- **Count re-measurement.** `count-c1.py --rev 69e82c48` → `c1_complete`,
  4/4, exit 0. Because siblings edited the entry and `SOURCES.md` concurrently,
  I also committed a copy of the working tree in the scratch clone and re-ran
  the counter there: `c1_complete`, 4/4, exit 0, with
  `inspect-pcap-capture` holding 2 records and the other three holding 1 each.
  The "rejected" entries in that output are the cross-verb pairings the binder
  correctly refuses (e.g. the client envelope tried against
  `inspect-packet-capture`), not defects.

## Residual risk and verification gaps

- **The `meta.duration` field makes envelope bytes non-reproducible.** A replay
  of the same argv yields the same `evidence_id` and the same `normalized_result`
  but a different `meta.duration` (e.g. client `277ms` → `581ms`), so the
  committed `.envelope.json` is not byte-reproducible by re-running. Any claim
  that the envelopes are byte-reproducible would be false; the correct claim is
  that `evidence_id` and `normalized_result` are. `count-c1.py` compares
  `run.stdout` to the committed envelope blob, so it depends on that pairing
  being captured together — which it was, in the same `run-rea.py` invocation.
- **F1's correct wording is a judgment call for the main agent**, but the
  current sentence is demonstrably false, and the same "no version range" idea
  leaks into `corpus/lessons/round-24.md` and the round-24 `PROVINCE.md`
  section. Those three files should move together.
- **I did not verify** the `prlimit` ceilings are enforced against a hostile
  input (the entry disclaims that), the `capinfos -M` parsing beyond the values
  carried in the envelopes, or the `S070`/`S071` line anchors beyond the
  digests and the quoted lines, which I did check
  (`PcapProvider.js:330` is the `capinfos -M` call, `:361-362` the packet-count
  cross-check, `PcapNativeBound.js:28-30` the 1 GiB / 64 MiB / 300 CPU ceilings;
  `capinfos-4.6.9.adoc` sha256 `76a23815…f61` matches S071 and lines 218/131
  are the `-M` and `-c` descriptions as cited).
- **Sibling reports already cover** the `-T fields` → `-T json` error in this
  entry and in S065/S066 (ResSources-2 F1, ResHonesty-2 finding 18,
  ResC1Instrument-2), and the DSB statement itself (ResSources-2, S067). The
  superseded rows S069/S070/S071 and the corrected entry text already appear in
  the working tree, so those are converging; F1–F4 above are additional and, as
  far as I can tell from the five residual reports present, not yet raised.
- **The 85-seat BUILD wave was refused by the job cap**, so no BUILD probe
  evidence exists for the boundaries the entry lists as open. That is a scope
  limit of the round, not a defect in these envelopes.

## Recommended L1 action

1. **F1** — rewrite entry line 41 to state that REA's `pcap` and
   `tshark-capture` providers **do** enforce major version 4 (a 3.x tool is
   refused as `capability_unavailable` / "Expected TShark 4.x"), and that the
   client verb inherits that provider-level gate rather than omitting one.
   Apply the same correction to `corpus/lessons/round-24.md` and to the round-24
   `PROVINCE.md` section, or record explicitly that the "another runnable
   installation need not be refused" sentence is bounded to 4.x.
2. **F2** — change the input range at entry line 112 from "2004–2018" to
   "2002–2018" (or drop the parenthetical), since `http.pcap` is 2002-12-31.
3. **F3** — widen the round-22 citation at entry lines 13-15 to include
   `inspect-packet-*.json` (or name all four refusal files), so the glob reaches
   all four verbs the sentence asserts.
4. **F4** — at entry lines 100-102, scope the "4 MiB combined output" to the
   capture path and state the fields path's actual ceilings (32 MiB output,
   8 MiB record budget, per the committed `l1-packet-fields-dns.envelope.json`).
5. **Falsifier note** — add to the recheck text that replay equality is defined
   on `evidence_id` + `normalized_result`, not on envelope bytes, because
   `meta.duration` varies per run.
6. Re-run `count-c1.py --rev <new rev>` and the `freeze-gate.py --require-clean
   round-24` gate after the edits, and confirm both still report 4/4 and CLEAN.
   I have not run the freeze gate against these edits — the edits are prose and
   source-row changes, but the gate's disclosure ledger is the thing that must
   be re-checked after them.

**I do not call round 24 verified.** The C1 envelopes reproduce and the count
holds; the residual defects above are corrections to the knowledge entry's
prose and to two source rows, and they should be fixed and disclosed before the
round is admitted.
