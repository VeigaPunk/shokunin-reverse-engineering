# SignalCarrierAlternatives — R23-C1 off-line UART fixture scout

Scope: locate one publicly versioned, official `sigrok-dumps` UART fixture and record
its URL, hashes, and README channel parameters. No bulk download, no fixture corpus
retained, no acquisition claim. No debugger, Frida, process attach, device access, or
carrier execution. No REA CLI probe was required for this public-metadata question.

## Findings

### Selected fixture (observation)

- Repository: `sigrokproject/sigrok-dumps`, the sigrok project's official dump
  collection. Root README at the same pinned commit states it is "a collection of
  logic analyzer example data" covering UART among other protocols, and that it "has
  had official tarball releases."
  - https://raw.githubusercontent.com/sigrokproject/sigrok-dumps/6bf0de22955f18e91eb9c2089cb31b7c9252ed47/README
- Version: official tag `sigrok-dumps-0.1.0` → commit
  `c8fad0528648ba58ceddbda9e34e4dfcd293a6b0` (2012-05-18, commit message
  `NEWS: Add date for 0.1.0 release.`). Observed via GitHub tags API and commit API.
- Fixture path: `uart/hello_world/8n1/hello_world_8n1_9600.sr`
- Pinned URL:
  https://raw.githubusercontent.com/sigrokproject/sigrok-dumps/c8fad0528648ba58ceddbda9e34e4dfcd293a6b0/uart/hello_world/8n1/hello_world_8n1_9600.sr
- Size: **58,381 bytes**
- **SHA-256: `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61`**
- Git blob SHA-1: `71f8ecfb173bd8aab17fbf208d3a33e0ec4febff` (matches the GitHub
  contents API entry for the file at the tag)
- README URL (pinned):
  https://raw.githubusercontent.com/sigrokproject/sigrok-dumps/c8fad0528648ba58ceddbda9e34e4dfcd293a6b0/uart/hello_world/README
  - 1,277 bytes, SHA-256
    `7af1c7841a603eb1f6dfecbe1402acd980e175e7e31cd62daf2fe2a0caed6f66`,
    git blob SHA-1 `57365d63825e30abfdc19362d0c8c1da03312535` (matches API).
- Official release tarball directory (observed, deliberately not fetched):
  https://sigrok.org/download/source/sigrok-dumps/ lists
  `sigrok-dumps-0.1.0.tar.gz`, 1.0M, last modified 2012-05-18 13:09.

### README channel parameters (observation, verbatim excerpt)

```
Logic analyzer setup
--------------------

The logic analyzer used was a ChronoVu LA8 at a sample rate of 5MHz (for baud
rates 921600 - 230400), 1MHz (115200 - 19200), and 625kHz (9600 - 1200):

  Probe       UART
  ----------------
  0 (green)   TX

Data
----

The sigrok command line used was:

  sigrok-cli -d 0:samplerate=<hz> --samples 8388608 -p '1=TX' -o <file>.sr
```

Additional README facts: one-direction UART traffic only; repeatedly transmitted
payload `"Hello World!\r\n"`; sender is an Olimex STM32-H103 eval kit, USART1.TX
pin; variants cover 8n1, 8o1, 8e1, 7o1, 7e1. The selected filename encodes **8n1**
(8 data bits, no parity, 1 stop bit) at **9600 baud**.

### Embedded archive metadata (observation)

The 58,381-byte fixture is a zip (sigrok `.sr`) read in memory; members:

| member | uncompressed size | observed |
|---|---|---|
| `version` | 1 B | contents `2` |
| `logic-1` | 8,388,608 B | sample stream, first and last 16 bytes all `0x01` |
| `metadata` | 150 B | see below |

```
[global]
sigrok version = 0.2.0
[device 1]
driver = chronovu-la8
capturefile = logic-1
unitsize = 1
total probes = 8
samplerate = 625 kHz
probe1 = TX
```

This independently confirms the README's 625 kHz rate and TX channel naming.
Inference: README's "Probe 0" is 0-based physical probe numbering while the `.sr`
`probe1=TX` is sigrok's 1-based channel index; both identify the same single TX
line. The `0x01` run at both ends of `logic-1` is consistent with an idle-high
UART line; no UART decode was performed.

### Alternate pin of the same fixture (observation)

Current master tip for the path is commit
`6bf0de22955f18e91eb9c2089cb31b7c9252ed47` (2015-12-25,
`uart/hello_world: Shorten the files a bit.`), and the same path is a compact
705-byte file:

- URL:
  https://raw.githubusercontent.com/sigrokproject/sigrok-dumps/6bf0de22955f18e91eb9c2089cb31b7c9252ed47/uart/hello_world/8n1/hello_world_8n1_9600.sr
- SHA-256:
  `b87f1f632ce0684a79e0391c860f8b55c78ce952d3ea10eaede41e8a7ffdf8ea`
- Git blob SHA-1: `2dc085f3a4bc4d7610a89727ba7d78ea937adfef` (matches API)
- Metadata: `sigrok version=0.4.0-git-ae9ca5b`, `samplerate=625 kHz`,
  `probe1=TX`, member `logic-1-1` 36,506 B.
- README at this pin is byte-identical to the tag README
  (SHA-256 `7af1c784…caed6f66`), so the same channel parameters apply.

Selection guidance: use the `sigrok-dumps-0.1.0` tag pin when a formal release
version is required; use the master-tip pin when a smaller file and a newer `.sr`
format are preferable. Both are the same documented 9600 8n1 TX fixture.

### Probes actually run (observation)

1. `read` GitHub API `repos/sigrokproject/sigrok-dumps/tags` → tag
   `sigrok-dumps-0.1.0` and commit `c8fad05…`.
2. `read` GitHub API `repos/sigrokproject/sigrok-dumps/commits/c8fad05…` →
   2012-05-18 release NEWS commit.
3. `read` GitHub API `contents/uart/hello_world/8n1?ref=c8fad05…` → file sizes and
   blob SHA-1 `71f8ecfb…`.
4. `read` raw `uart/hello_world/README` at tag `c8fad05…` and master tip →
   identical 1,277 bytes.
5. Python `urllib.request` GETs in one `eval` cell: README and one `.sr` at the tag,
   one `.sr` at the master pin; printed size, SHA-256, git-blob SHA-1, zip member
   list, and metadata. Cell completed successfully; all hashes above are from this
   probe.
6. `read` `https://sigrok.org/download/source/sigrok-dumps/` → official tarball
   name/size/date.

No `git clone`, no tarball fetch, no fixture files written to disk, and no bulk
download occurred. The fixture bytes were held only in process memory for hashing
and archive-structure inspection; this report makes no acquisition claim.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SignalCarrierAlternatives.md`
  — this report. SHA-256 recorded by the final file probe.

No other outputs. No fixture bytes, clone, or downloaded tarball were retained.

## Installs

None. No tools installed or upgraded.

## Open risks

- The official `sigrok-dumps-0.1.0.tar.gz` was not downloaded, so its own SHA-256 is
  unknown; the tag/commit pin and raw file hash are verified, host availability is not.
- The 0.1.0 `.sr` uses sigrok 0.2.0-era archive/metadata conventions; a consumer must
  support that format or use the master-tip variant (sigrok 0.4.0-git).
- README parameters are documentary, not runtime-verified UART decoding; no
  functional claim about baud tolerance or decode correctness is made.
- "Probe 0" (README) vs `probe1` (metadata) numbering is reconciled only by
  inference; it is consistent with sigrok conventions but was not tested against a
  decoder.
- Network observations depend on GitHub and sigrok.org being reachable; content
  identity is protected by the immutable commit pin, not by mirror durability.
- Dynamic ownership of any carrier remains out of scope and unresolved;
  this seat produced static, public-source evidence only.
