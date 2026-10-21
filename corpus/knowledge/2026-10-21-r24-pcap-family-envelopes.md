source: S064 Wireshark4.6.9 signed source release and test captures; S065 tshark(1)4.6.9 manual; S066 REA6.5.0 installed capture providers; S067 original REA6.5.0 envelopes in .ufo/waves/round-24/evidence/c1/
verified-at: 2026-10-21, round24; exact producing argv/environment/stdout/stderr/exit retained in adjacent .run.json files written by .ufo/waves/round-24/tools/run-rea.py
recheck: python3 -I -B .ufo/waves/round-24/tools/count-c1.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <MEASURED-COMMIT>; a real replay re-runs each retained argv with the REA_TSHARK_COMMAND/REA_CAPINFOS_COMMAND recorded in the run file after reproducing the build in .ufo/waves/round-24/tool-pins.json

# Packet-capture REA envelopes on saved captures, not traffic ownership

Coverage-map ground: saved-capture and dissector-registry envelopes, added in
round24. This entry holds the four REA6.5.0 packet-capture family verbs
(`inspect-pcap-client`, `inspect-pcap-capture`, `inspect-packet-fields`,
`inspect-packet-capture`) on inputs taken from the signature-checked Wireshark
4.6.9 source release. It claims no live capture, interface access, decryption
practice, protocol-correctness verification or network-forensics ownership.
Round 22 placed all four verbs `frontier-blocked` because no TShark existed on
the host (`.ufo/waves/round-22/evidence/c2/inspect-pcap-*.json`, ENOENT and
missing REA_TSHARK_COMMAND refusals); those refusals stay valid for that host
state and are not rewritten.

## The tool is a recorded local build

TShark/capinfos 4.6.9 were built from the official source tarball
(SHA256 `d062d416a1ab3a49975aafe3a671c882dde0562ccd71b078808ceb59d465fc0f`,
equal to the `SHA256(...)` line of the signed `SIGNATURES-4.6.9.txt`; gpg
reports a good signature by key `5A5ADBA7DBEA6C3F87224F1982244A78E6FEAEEA`
without a web-of-trust path) into `/home/vgpnk/.local/opt/wireshark-4.6.9`
with Lua disabled; no pacman transaction. Binary digests and the configure
command are in `.ufo/waves/round-24/tool-pins.json`. A missing or replaced
binary at that path ends every holding below; the round-22 refusals show what
REA returns then.

## Client inspection is tool-subject

**Observation:** `inspect-pcap-client` returned
`.ufo/waves/round-24/evidence/c1/l1-pcap-client.envelope.json`,
`ev_2b38caf1a09e30b4dd7affc60a53d635f93cb5a8ba5e4697a9b8b9b4b99857e2`,
operation `inspect_pcap_client`, provider `pcap`. `subject` is null and the
only limitation is "Artifact identity is unavailable for this observation."
It reports both commands as `environment`-sourced and echoes their version
strings; it does not check version range itself and reads no capture.

## Capture summaries are derived, not observed

**Observation:** `inspect-pcap-capture` on `dns_port.pcap`
(`.ufo/waves/round-24/evidence/c1/l1-pcap-capture-dns.envelope.json`,
`ev_c2bb6a6a4287c2454fcb01e839e3656154e69ab153ef75034edb7a2d6612c0bd`,
subject sha256 `78c3c00e4cb155118468e540a6151ca222fa50edd626daf1582d25e3d79626a1`)
reports pcap/ether, 4 packets, one protocol stack `eth:ethertype:ip:udp:dns`,
two endpoints and the query `us.pool.ntp.org` with its response addresses,
coverage `complete`, empty tshark/capinfos stderr. Its confidence is
`derived`. The DNS association is bounded by REA's own limitation: addresses
are tied only to a single question in the same response packet and "may
include additional DNS records, not only final resolution answers".

**Observation:** the same verb on `tls12-dsb.pcapng`
(`.ufo/waves/round-24/evidence/c1/l1-pcap-capture-tls.envelope.json`,
`ev_8464c8143a41c5e7423c56c90e31576e5807be2aefe6cfb6712605651b3f4ca2`,
subject sha256 `d6034147bd02a206cca5d335d11c1292e7ed44a42d58f342c05bbd31318f81d8`)
reports pcapng/rawip4, 17 packets, TLS SNI `example.com` and `example.net`,
and HTTP request URIs `https://example.com/` and `https://example.net/`.
**Observation, disclosed boundary:** walking the pcapng block headers shows two
Decryption Secrets Blocks (block type `0xA`, secrets type `0x544c534b`
"TLSK", key-log lines beginning `CLIENT_RANDOM`) at byte offsets 96 and 5224.
TShark applies embedded secrets without any lane-supplied key. The lane gave
no key file; the HTTP layer is a property of this input, not a decryption
capability the lane holds. SNI is a ClientHello field and needs no decryption.

**Observation:** `inspect-packet-capture` on `http.pcap` with fields
`http.request.uri` and `ip.src` and display filter `http.request`
(`.ufo/waves/round-24/evidence/c1/l1-packet-capture-http.envelope.json`,
`ev_19cfb3145c46283f9c4b123275fc02ff33dffd303ec8dc8623a3fd6cb3c30383`,
subject sha256 `69e489a26a59208a1dd56fbea4c606b1e59e8ac32d3d4789ca6cc81e71bad3f2`)
returned frame 1, URI `/v4/iuident.cab?0307011208`, source `10.0.0.5`,
output window 1 matching/1 returned/`has_more:false`, read scope `to-eof`,
confidence `observed`. REA builds `-r … -T fields … -2 … -Y … -d … -e`
(S066, `TsharkCaptureProvider.js:203-217`); `-2` is two-pass analysis that
"allows it to fill in fields that require future knowledge" (S065).
The fields option is an array: a comma-joined single value was refused by
TShark as an invalid field list (L1 probe before the retained run; repeat
`--fields` per field).

**Observation:** `inspect-packet-fields --kind fields --protocol dns`
(`.ufo/waves/round-24/evidence/c1/l1-packet-fields-dns.envelope.json`,
`ev_defa14b1a3bef7c4cd9bc35d23316c1dec484256e880aa7331078c7369f79433`)
examined 269366 registrations, matched 356 `dns` fields and returned the
first 50 (`has_more:true`). Its subject is the tshark binary itself (sha256
`00ed7bde…6f770d`). REA states these registrations "describe the selected
installation, not traffic observed in a capture". With Lua disabled in this
build, Lua-registered dissectors are absent from that registry.

## Limits carried from the envelopes

- tshark-capture runs under prlimit: at most 1 GiB address space per process,
  64 MiB per file, 30 CPU seconds, no core dumps; resident input 32 MiB, 30 s
  wall clock per command, 4 MiB combined output (S066 line 263). The pcap
  provider reports its own inherited ceilings (300 CPU seconds). Neither is an
  OS sandbox; installed libraries and dissectors are trusted.
- Missing fields are absent producer output, not zero; a filtered result
  does not establish traffic absence.
- Inputs are tiny, old, public test captures (2004–2018 timestamps). Nothing
  here says how these verbs behave on large, truncated, encrypted-without-
  secrets or adversarial captures; those are round-24 BUILD probe questions,
  not holdings.

## Not claimed

Live capture or `dumpcap`; interface or device access; TLS/QUIC decryption
with lane-held keys; protocol-semantics correctness beyond TShark dissector
output; complete REA pcap behaviour; the frozen R23 debugger verbs (still
unheld/Adjacent); outside admission.
