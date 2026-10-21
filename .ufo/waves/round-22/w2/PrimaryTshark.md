# PrimaryTshark — bounded primary-source support for the TShark missing-provider rows

Seat: `KaidokuR22R.PrimaryTshark-6` (leaf scout, author-side only; not outside admission).
Baseline under review: `PROVINCE.md` §"Round-22 catalog dispositions" rows `inspect-packet-fields`,
`inspect-packet-capture`, `inspect-pcap-client`, `inspect-pcap-capture`; claim `R22-C2` in
`.ufo/waves/round-22/claims.json`. Lane HEAD observed: `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`.

## Result

The source was accessible, so a registry row is drafted below. It gives narrow support: the page
names the TShark version it documents and says TShark is part of the Wireshark distribution.
It says **nothing** about REA's provider contract, environment keys, `capinfos`, or whether a host
has TShark. Each of those parts of the four reasons rests on REA's receipts and host lookups, not on this source.

## Source access (observed)

| step | argv | exit | observed |
|---|---|---|---|
| fetch | `curl -sS -L -o tshark_man.html -w 'http=%{http_code} size=%{size_download} url=%{url_effective}\n' https://www.wireshark.org/docs/man-pages/tshark.html` (cwd `/tmp`) | 0 | `http=200 size=173588 url=https://www.wireshark.org/docs/man-pages/tshark.html` |
| digest | `sha256sum tshark_man.html` | 0 | `35a040d9079272f014f616d48dea173ef7d3069ac47b22fb712171c8e3dd515c` |
| headers | `curl -sS -I -L <same URL>` filtered to date headers | 0 | `date: Wed, 21 Oct 2026 13:03:17 GMT`; `last-modified: Wed, 07 Oct 2026 21:24:12 GMT` |
| text extract | python3 tag-strip of `/tmp/tshark_man.html` → `/tmp/tshark_man.txt` | 0 | 2221 lines; top-level headings NAME, SYNOPSIS, DESCRIPTION, OPTIONS, DIAGNOSTIC OPTIONS, CAPTURE FILTER SYNTAX, READ FILTER SYNTAX, FILES, ENVIRONMENT VARIABLES, SEE ALSO, NOTES, AUTHORS |

The page body has no date of its own. Its generator is `Asciidoctor 2.0.26`. The only date
available is the HTTP `Last-Modified` header, 2026-10-07. The version comes from the NOTES section: TShark 4.6.9.

## Quoted passage (contiguous, 15 words)

Heading: **NOTES** (`<h2 id="_notes">`, HTML lines 4583–4587). Page documents TShark 4.6.9; HTTP Last-Modified 2026-10-07; fetched 2026-10-21.

> "This is the manual page for TShark 4.6.9. TShark is part of the Wireshark distribution."

Secondary anchor, not quoted for the registry: under OPTIONS, `-G <report type>` "will cause TShark to dump one of several
types of glossaries and then exit". This is the upstream operation behind a field or protocol
registration listing, which is what `inspect-packet-fields` would surface.

## What the source supports vs. what it does not

| row / inference | supported by this page? | basis |
|---|---|---|
| "TShark 4.x" is a real upstream program, documented here as release 4.6.9 | **Yes**, version identity only | NOTES quote |
| TShark is distributed as part of Wireshark, matching REA's "Supply Wireshark 4.x tshark" wording | **Yes** | NOTES quote |
| Field and protocol registrations come from a TShark glossary dump (`-G`), so with no TShark run, "no field registrations examined" is accurate | **Partly**. The page defines `-G`. It does not say REA calls `-G` | OPTIONS `-G`; REA's real invocation not traced (this seat did not read the REA source) |
| `REA_TSHARK_COMMAND` / `REA_TSHARK_PRLIMIT_COMMAND` / `REA_CAPINFOS_COMMAND` must be absolute or are required | **No** | These are REA keys. The page's ENVIRONMENT VARIABLES section lists only `WIRESHARK_*` variables. The real source is the REA receipt text (`inspect-packet-fields.json`, `inspect-pcap-client.json`) |
| `capinfos` is needed and is shipped with tshark | **No** | The string `capinfos` does not appear on the page. SEE ALSO lists editcap, dumpcap, mergecap, text2pcap, not capinfos. The row reason "capinfos availability not independently established" stays correct and must stay unsupported |
| TShark is absent on this host | **No**, out of scope for a man page | Only host observation counts: `command -v tshark` exit 1, `capinfos` exit 1, `dumpcap` exit 1; `pacman -Q wireshark-cli wireshark-qt` exit 1 (both "was not found"); `prlimit` → `/usr/bin/prlimit` exit 0 |
| An empty pcap carried no traffic, or traffic is absent | **No**, and the row correctly disclaims it | Without dissection, nothing can be said about traffic |
| TShark will stay unavailable, or REA's provider is broken | **No** | One observation, 2026-10-21. `claims.json` `not_claimed` already excludes "provider availability over time" |

## Receipts cross-checked (read-only)

All four were `npx -y rea-agents@6.5.0 <verb> … --format json --full-output` with `env_overrides {}`, exit 1, error code `capability_unavailable`, category `unsupported_provider`:

- `inspect-packet-fields`, `inspect-packet-capture` (`empty.pcap --fields frame.number`): provider `tshark-capture`, reason `Supply absolute REA_TSHARK_COMMAND for TShark 4.x.`
- `inspect-pcap-client`, `inspect-pcap-capture` (`empty.pcap`): provider `pcap`, reason `Cannot run selected tool tshark: spawn tshark ENOENT`

Calibration note: the four PROVINCE reasons match their receipts. The two `tshark-capture` rows say "configuration unavailable", which is accurate. They do not claim ENOENT, because that provider refused before spawning anything. The two `pcap` rows say ENOENT, which matches the receipt text. No row should be strengthened from this source into "TShark is not installed". Only the host `command -v` and `pacman -Q` observations above support that, and only for this instant.

## Drafted registry row (for L1; id assigned at integration)

The next free id in `corpus/SOURCES.md` is S054. No `S05[4-9]` rows were present when I searched.

```
| S054 | TShark manual page — https://www.wireshark.org/docs/man-pages/tshark.html | docs | A | Upstream identity of TShark 4.6.9 as part of the Wireshark distribution and the meaning of `-G` glossary reports; not REA's REA_TSHARK_*/REA_CAPINFOS_* contract, not capinfos, not host presence | NOTES section; page documents TShark 4.6.9; HTTP Last-Modified 2026-10-07; fetched 2026-10-21, HTML sha256 `35a040d9079272f014f616d48dea173ef7d3069ac47b22fb712171c8e3dd515c` (173588 bytes); OPTIONS `-G` | REA's "Wireshark 4.x tshark" names a real upstream program, but a missing-provider refusal is REA/host evidence, never upstream evidence of absence. | opened | 2026-10-21 | 90d | PROVINCE.md §Round-22 catalog dispositions (pcap/tshark rows) |
```

## Unknowns

- How REA actually invokes TShark (is it `-G fields` / `-G protocols`?) was not traced. I did not read the REA source for that.
- I did not check that `REA_TSHARK_COMMAND` is unset in the probe environment. I did not inspect config or accounts. The receipts show `env_overrides {}`, and the refusal text is the only signal.
- The page is a live URL with no version pin. Later fetches may document a different release.

## Constraints honoured

No installs or updates. No pacman transaction: only the read-only `pacman -Q`. No target execution, no device or remote contact, no config or account inspection, no edits to the lane outside this report and its `.json` attachment.
