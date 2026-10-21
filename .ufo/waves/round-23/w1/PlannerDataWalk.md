# PlannerDataWalk — R23-C1 offline UART: source → carrier → envelope → entry → S row → count

Seat: `KaidokuR23.PlannerDataWalk` (leaf scout, author-side). No production edit; no delegation.
Observed 2026-10-21 11:35–11:46 -0300 (UTC-3), repo HEAD `a3c92eb6bc70984e90ae5b895412de978840b2c5`.
L1 remains the canonical planner and sole integration owner. This report is a data walk and a
pre-commit check of the live working tree, not outside verification.

## Verdict

- The complete path exists in the working tree: S058–S060 rows, the knowledge entry, and four
  bound REA envelopes (plus one refusal control). **None of it is committed**; at HEAD the frozen
  counter still returns **1/6** (`identify-flutter-build` only), exit 1 (observed).
- **One blocking defect:** the live entry cites the binary `.sr` carrier under
  `.ufo/waves/round-23/evidence/c1/` (line 66). The R23 counter reads every cited C1 path as
  UTF-8 (`git show rev:path` then `.decode('utf-8')`), so the ZIP bytes raise
  `UnicodeDecodeError` and the whole measure exits **2 / `unevaluable`**. Removing that citation
  is mandatory before commit.
- With the `.sr` citation removed, an in-process replay of the counter's own entry-side loop
  yields new witnesses for **`inspect-signal-decoders`** and **`decode-signal-recording`**; union
  with the preserved R22 `identify-flutter-build` witness gives **k = 3/6, incomplete = 3**
  (`inspect-dart-aot`, `debug-with-gdb`, `debug-with-rizin` remain unheld). This is an
  `[INFERENCE]` from the counter loop, not a count at a committed revision.
- The claim target is `>=2/6`. Even inventory alone would reach k=2; the decode leg makes k=3.
  No mastery or dynamic ownership is implied.

## The concrete path

### 0. Claim and denominator

- Frozen claim: `.ufo/waves/round-23/claims.json` R23-C1, T1 =
  `identify-flutter-build`, `inspect-dart-aot`, `debug-with-gdb`, `debug-with-rizin`,
  `inspect-signal-decoders`, `decode-signal-recording`. Total 6; baseline 1/6.
- Counter: `.ufo/waves/round-23/tools/count-c1.py` (sha256
  `7220573647a41052c539ea08f3c2b33f9b41d68bd8e0a9a6b05150e86a045b97`). It pins the R22
  counter `.ufo/waves/round-22/tools/count-c1.py` by sha256
  `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879`, fixes historical
  revision `aa1450b82f9ede35aada63efe8a34e01c6e02f72`, and requires the round-20 catalog to be
  unchanged (`count-c1.py:24,26-27,46-58`).
- Cumulative semantics: `historical` is measured once at `aa1450b`; `new` witnesses are read only
  from `.ufo/waves/round-23/evidence/c1/`; a verb is held if `historical or new`
  (`count-c1.py:57,88-106`). More than one envelope for the same verb cannot raise the count.

### 1. Source rows (live working tree, uncommitted)

`.ufo/waves/round-23/...` is not an S row; the rows are in `corpus/SOURCES.md:64-66` (observed
`git diff`: 3 added lines, `git status` `M corpus/SOURCES.md`). All three rows are 13-cell pipe
rows, tier A, status `mined`, opened `2026-10-21`, used-by
`corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md, corpus/lessons/round-23.md`.

| row | source | pinned anchor observed | relevance |
|---|---|---|---|
| S058 | sigrok-cli 0.7.2 manual — `https://raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1` | tag `sigrok-cli-0.7.2` commit `b584f959edb788f1731d5a304badf241ac21bf65` (`git ls-remote`, exit 0); retained copy `.ufo/waves/round-23/evidence/sources/sigrok-cli.1`, sha256 `e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9` (19,180 B), byte-identical to upstream (`diff`, exit 0) | `-I, --input-format` and the colon `key=value` example `binary:numchannels=4:samplerate=1mhz` at lines 128–145; `-P` decoder options and explicit channel mapping at lines 274–322; `-A` annotation selection at 360–368 |
| S059 | sigrok-dumps UART README — `https://raw.githubusercontent.com/sigrokproject/sigrok-dumps/c8fad0528648ba58ceddbda9e34e4dfcd293a6b0/uart/hello_world/README` | release commit `c8fad0528648ba58ceddbda9e34e4dfcd293a6b0`; retained copy `evidence/sources/uart-README.txt`, sha256 `7af1c7841a603eb1f6dfecbe1402acd980e175e7e31cd62daf2fe2a0caed6f66` (1,277 B) | Declares one-way UART, TX probe/channel, 625 kHz / 9600 baud, 8n1 fixture; attribution only, not host acquisition |
| S060 | Round-23 original offline signal CLI envelopes — `inventory.envelope.json`, `decode-uart-hi.envelope.json`, `decode-official-uart.envelope.json` under `.ufo/waves/round-23/evidence/c1/` | own-work; producing argv/env/exit in adjacent `.run.json`; opened 2026-10-21 | Records the exact requests and observed outputs; not device state or tool authentication |

Observed gap (not a counter gate): there is **no S row for `libsigrok` `src/input/binary.c`** or
`libsigrokdecode` `decoders/uart/pd.py`. S058 grounds the `-I` syntax and S060 grounds the
observed selector, but the decoder's own option ids/defaults are not a cited source row. If the
source-quality review requires decoder semantics, add S061 (uart `pd.py`, pinned below) rather
than relying on the envelope alone.

Pinned upstream files available if a row is added:
- `libsigrok` tag `libsigrok-0.5.2` → commit `a6b07d7e28fe445afccf36922ef7d20e63e54fe6`
  (`git ls-remote`, exit 0); `src/input/binary.c` sha256
  `fa037abe4beaf00ff35470f4a78989c2237663edad79b9fd53af6375e72dd9d1` (4,394 B). Lines 48–60
  define `numchannels`, `samplerate`, and generated channel names `"0"…"n-1"`; lines 159–160
  declare both options.
- `libsigrokdecode` tag `libsigrokdecode-0.5.3` → commit
  `97991a3919da6a07c4c87308ae66fb441bd512e3`; `decoders/uart/pd.py` sha256
  `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62` (23,007 B), identical to
  the runtime copy and `tool-runtime-pins.json`. Lines 95–122: optional `rx`/`tx`, `baudrate`
  (default 115200), `data_bits` 8, `parity` none, `stop_bits` 1.0, `bit_order` lsb-first,
  `format` hex; annotations 124–143.

### 2. Carriers (offline; no acquisition)

| carrier | identity observed | provenance |
|---|---|---|
| Synthetic raw UART8N1 `uart-hi.bin` | 2,500 B, sha256 `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`; 960,000 Hz, 100 samples/bit, baud 9600, channel 0 in bit 0, LSB-first, payload ASCII `Hi` (`4869`) | `.ufo/waves/round-23/tools/make-uart.py` (sha256 `e22a8f1f11b4cf844904ce78c63d12f6e280f041653bced0c639ef03a21f0fce`); `generate-uart.run.json` exit 0, stdout carries path/digest/size/bits and `"acquisition": "synthetic; no hardware"` |
| Official sigrok-dumps `hello_world_8n1_9600.sr` | 58,381 B, sha256 `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61`; `.sr` ZIP with `probe1 = TX`, 625 kHz, 8n1 | `official-download.json`: pinned URL, HTTP status 200, size, sha256, `captured_at 2026-10-21T14:38:57.638074+00:00`. Source row S059 / `SignalCarrierAlternatives.md` |

Both are inert bytes and untrusted data. The synthetic carrier exercises exact-byte control; the
official carrier is third-party acquired data used only as provenance-bearing input.

### 3. REA envelopes (original CLI output)

Environment for every run: `REA_SIGROK_COMMAND=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/tools/sigrok-cli.sh`
(sha256 `50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902`), `cwd` lane root.
Launcher selects the AppImage-extracted runtime and preloads host `libgmodule`; AppImage sha256
`49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614` (49,558,848 B). REA is
`npx -y rea-agents@6.5.0`; `node -p` on the cached `package.json` printed `6.5.0` (exit 0).
`/usr/bin/prlimit` sha256 `092bb6db10a743ecccfc7d6e72055007064abf8910c85d736832fb53697fff96`.

| envelope | `meta.command` | `data.operation` | evidence id | observed result | `bind_cli` |
|---|---|---|---|---|---|
| `inventory.envelope.json` | `inspect-signal-decoders` | `inspect_signal_decoders` | `ev_940cf7bbd6ba6e8def3e7f29dad9dc03bccbd0f39a094a4787d3dd563164fdd0` | 110 decoders, `uart` present, `examined/matching/returned = 110/110/110`, `has_more:false`; run exit 0 | 0 |
| `uart-help.envelope.json` | `inspect-signal-decoders` | `inspect_signal_decoders` | `ev_4be13793b8a767184ddcfb301b3f0e06c1333e12e533347c68eb1b53d169e94a` | 81 help lines, `has_more:false`; run exit 0 | 0 |
| `decode-uart-hi.envelope.json` | `decode-signal-recording` | `decode_signal_recording` | `ev_bcadf773da826e70bfb79c492ddf111cd3f226fdd30addb4a15aabdc3602bd3e` | `total_lines:2`, `annotations_text` exactly `300-1100 uart-1: 48\n1300-2100 uart-1: 69\n`; run exit 0 | 0 |
| `decode-official-uart.envelope.json` | `decode-signal-recording` | `decode_signal_recording` | `ev_1d361f25aeaa07b5c03ffbbd43c61d061407b96c6c62bf783913d03a62c67e5c` | `total_lines:12885`, `has_more:false`; first bytes `BA BD C9 B1 91 85 0D 0A 48 65…`; run exit 0 | 0 |
| `decode-invalid-decoder.envelope.json` | `decode-signal-recording` | absent | absent | `ok:false`, `error.code: execution_failure`, run exit 1; **control, not a witness** | n/a (no data/id) |

Exact producing argv (retained in the adjacent `.run.json`):

```text
npx -y rea-agents@6.5.0 inspect-signal-decoders --all --format json --full-output
npx -y rea-agents@6.5.0 inspect-signal-decoders --decoder uart --all --format json --full-output
npx -y rea-agents@6.5.0 decode-signal-recording <uart-hi.bin> --decoders uart:rx=0:baudrate=9600 \
  --input_format binary:numchannels=1:samplerate=960000 --annotations uart=rx-data --all_lines \
  --format json --full-output
npx -y rea-agents@6.5.0 decode-signal-recording <hello_world_8n1_9600.sr> \
  --decoders uart:rx=TX:baudrate=9600 --annotations uart=rx-data --all_lines \
  --format json --full-output
```

The provider's original argv inside the decode envelopes is
`--dont-scan --input-file=recording --protocol-decoders=… --protocol-decoder-samplenum
[--input-format=…] [--protocol-decoder-annotations=…]`; the recording is a private copy, and
`hardware_acquisition` is `"not-performed"` (provider declaration, not an independent monitor).
Successful decode `diagnostics` still contain embedded-Python warnings
(`Could not find platform independent libraries…`); `refused()` checks structural fields only,
so these do not refuse the record.

Binding predicate actually used (R22 counter `bind_cli`, preserved by R23): envelope `ok:true`,
`meta.command == verb`, `data` has `evidence_id` + `operation`, no `error`/`errors` or refusal
code anywhere in the record, then R21 `bind` matches `operation == verb.replace('-','_')` and the
exact `ev_` id. All four success envelopes returned code 0 in-process; the invalid control has no
`data`/id and cannot bind.

### 4. Knowledge entry

Live path `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md`, sha256
`7598d2cb436ceee4b6dc01c10869a9db0cd0f49afaf971aa02eb9f771aee6c35` (observed; currently
untracked, `git status` `??`).

Predicates against the R23 counter (`count-c1.py:74-98`):

| predicate | observed |
|---|---|
| first line starts `source:` | yes; `S058`, `S059`, `S060` extracted |
| each cited S row exists, id ≥ 58, tier A/B, `mined`, opened `2026-10-21`, entry in used-by | S058/S059/S060 all pass (checked cell-by-cell) |
| verb token present | `inspect-signal-decoders` and `decode-signal-recording` both match `command_pattern` |
| exact C1 file citations | 7 matches: inventory, uart-help, decode-uart-hi, decode-official-uart, decode-invalid-decoder, `uart-hi.bin`, `hello_world_8n1_9600.sr` |
| `ev_` ids present | 3: inventory `ev_940c…`, decode-uart-hi `ev_bcad…`, decode-official `ev_1d36…` |
| binding | inventory + both decode envelopes bind (code 0) to their own verbs |

Defects found:

1. **Blocking — binary citation at line 66:** `Committed copy
   `.ufo/waves/round-23/evidence/c1/hello_world_8n1_9600.sr` has…`. The R23 counter does
   `git show rev:<path>` then `.decode('utf-8')` (`count-c1.py:88-90`). The ZIP starts
   `PK\x03\x04…`; decoding fails at byte 0x84, position 12. `main` catches `UnicodeError` and
   prints `{"finding":"unevaluable"}` with exit 2. This happens whether or not the `.sr` is
   committed: if it is committed, decode fails; if it is omitted, `git show` fails first
   (`git_input_unreadable`, also exit 2). **Fix:** remove the full C1 path; keep only the
   basename, or cite the safe JSON receipt `official-download.json` (its URL/sha256 locate the
   source) and let the envelope's `artifact.path` carry the local path.
2. **Non-fatal — `uart-help` id absent:** the entry cites `uart-help.envelope.json` (line 29) but
   does not include `ev_4be13793…`. The verb still counts through `inventory.envelope.json`; the
   help envelope is merely an unbound citation. Adding the id gives a second witness for the same
   verb (no count change).
3. **Non-fatal, fragile — `uart-hi.bin` cited at line 38:** the 0x00/0x01 bytes are valid UTF-8,
   so the counter does not crash; `bind_cli` returns 2 (not JSON) and no witness. Prefer citing
   `generate-uart.run.json`, which contains the carrier path, digest, size and generator output.
4. **Non-fatal — S060 scope omits `uart-help.envelope.json`** while the entry relies on it for the
   RX-optional/help statement. Add it to S060's source list or drop that reliance.

### 5. S rows

Rows at `corpus/SOURCES.md:64-66` (live, uncommitted). Each has 13 pipe cells; the gate
(`count-c1.py:83`) passes:

- S058: docs, A, `mined`, `2026-10-21`, used-by contains the entry path.
- S059: dataset, A, `mined`, `2026-10-21`, used-by contains the entry path.
- S060: own-work, A, `mined`, `2026-10-21`, used-by contains the entry path.

Registry-side caveat: all three used-by cells also list `corpus/lessons/round-23.md`, which does
not exist yet (`ls` exit 2). That does not affect the counter gate, but it is a false used-by
until the lesson is written.

### 6. Cumulative count

Command (from the frozen claim):

```text
python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <LANE> --rev <REV>
```

Observed at `a3c92eb` (the only committed rev available now), exit 1:

```json
{"claim":"R23-C1","finding":"c1_incomplete","t1_exercised":["identify-flutter-build"],
 "t1_exercised_count":1,"t1_total":6,"historical_rev":"aa1450b…"}
```

`targets` at that rev: `identify-flutter-build` historical 2 / new 0; every other verb 0/0.
`catalog_mentioned_count` 135/153; `catalog_zero_count` 18.

Expected after the fix and one commit containing S rows + entry + evidence + counter (inference
from the counter's own loops):

| verb | source | witnesses |
|---|---|---|
| `identify-flutter-build` | historical R22 | `ev_6a84742a…` (Saber), `ev_3458b996…` (Godot) |
| `inspect-signal-decoders` | new C1 | `ev_940cf7bb…` / `inventory.envelope.json` (help envelope unwitnessed because its id is absent) |
| `decode-signal-recording` | new C1 | `ev_1d361f25…` / `decode-official-uart.envelope.json`; `ev_bcadf773…` / `decode-uart-hi.envelope.json` |

→ `t1_exercised = ["identify-flutter-build", "inspect-signal-decoders",
"decode-signal-recording"]`, count **3/6**, `finding: c1_incomplete`, exit **1** (the counter
returns 0 only at 6/6). Exact incomplete count **3**; remaining verbs `inspect-dart-aot`,
`debug-with-gdb`, `debug-with-rizin`. The claim's `>=2/6` target is met with room to spare, but
no completion or mastery is claimed.

## Prerequisites (ordered)

1. **Atomic commit at one measured rev** of: S058–S060 rows, the entry, every cited envelope,
   the counter, and (if retained) carriers. The counter reads only `git show rev:path`; untracked
   files do not exist (`count-c1.py:46-50,88-90`). `GIT_*` is cleared and replacement refs are
   disabled by the counter itself.
2. **R22 counter untouched** at sha256 `c925918f…`; **round-20 catalog unchanged** versus
   `aa1450b`; otherwise `legacy_source_untrusted` / `catalog_changed` → exit 2
   (`count-c1.py:47-49`).
3. **REA 6.5.0 through npx**, absolute executable `REA_SIGROK_COMMAND`, `prlimit` readable, and a
   version banner matching `^sigrok-cli 0\.7\.2` and containing `libsigrokdecode`
   (`SigrokRecordingProvider.js:139-141`). The launcher must be executable and stable for the
   whole run (the provider re-hashes it before/after).
4. **Carrier**: absolute local path, ≤ 32 MiB, selectors ≤ 32 KiB total; explicit
   `--input_format binary:numchannels=1:samplerate=960000` for the raw carrier (omit for `.sr`
   autodetect); `--decoders uart:rx=0:baudrate=9600` for channel 0 or `uart:rx=TX:baudrate=9600`
   for the `.sr`; `--annotations uart=rx-data`.
5. **Entry**: first line exactly `source: S058…, S059…, S060…`; verb tokens present; every cited
   C1 path is a **regular UTF-8 JSON/text file**; each cited envelope's `ev_` id appears in the
   entry and in that file; `meta.command` is the hyphen command and `data.operation` the
   underscore operation; no refusal ancestor.
6. **S rows**: id ≥ S058, tier A/B, status `mined`, opened exactly `2026-10-21`, used-by cell
   containing the exact entry path comma-separated.
7. **Calibration**: treat non-empty decode output as required for the entry's claim even though
   the binder does not enforce it. Synthetic expected `total_lines = 2` and `48`,`69`; official
   `12,885` lines with leading noise `BA BD C9 B1 91 85` and a final partial byte (`64`), so do
   not claim a clean `Hello World!` stream.

## Failure cases

| # | failure | where it bites | observed / inferred |
|---|---|---|---|
| F1 | Cite a binary carrier (`*.sr`, `*.bin` with non-UTF-8 bytes) under C1 | `count-c1.py:88-90` `.decode('utf-8')` | **Observed**: ZIP 0x84 at byte 12 → `UnicodeDecodeError` → measure exits 2 / `unevaluable` |
| F2 | Cite a C1 path not present at the measured rev | `git show` fails → `git_input_unreadable` | Inferred from `count-c1.py:44-46`; exit 2 |
| F3 | Cite a directory (`…/c1/subdir` or a bare root) | regex may match a subdir, `git show` cannot read a tree | Inferred; keep exact files |
| F4 | Path followed by punctuation without a backtick/bracket | regex class includes `.`/`-`/`_`, so the punctuation joins the path | Inferred; wrap paths in backticks |
| F5 | Entry/evidence/S rows left uncommitted | `git show`/`ls-tree` at rev | **Observed**: HEAD counter still 1/6 |
| F6 | First line not exactly `source:` | `count-c1.py:78` skips entry | Inferred; no witness |
| F7 | S row id < 58, tier C, not `mined`, wrong opened date, or used-by mismatch | `count-c1.py:83` | Inferred; no witness |
| F8 | Duplicate S id | `count-c1.py:66` raises | Inferred; exit 2 |
| F9 | Cite `*.run.json` instead of an envelope | `bind_cli` sees no `ok`/`data` → code 2 | Observed in R22 (`unsupported_candidates`); no witness |
| F10 | `meta.command` hyphen/underscore mismatch or split `evidence_id`/`operation` | `bind_cli` + R21 `bind` (`verb-coverage.py:85-88`) | Inferred; code 1, no witness |
| F11 | Refusal ancestor anywhere in the record | `count-c1.py:80-86`, R21 `refused` | Observed control: `execution_failure` has no data/id; cannot bind |
| F12 | Two envelopes for one verb | union by verb (`count-c1.py:99-106`) | Observed: Saber + Godot = one identify; inventory + help = one inspect |
| F13 | Wrong channel/baud/format, exit 0, empty output | binder accepts a non-refused exit-0 record | **Calibration gap**: `total_lines:0` still binds; entry must assert non-empty output |
| F14 | Missing provider, non-absolute `REA_SIGROK_COMMAND`, wrong banner, missing `libsigrokdecode` | provider configuration phase → `capability_unavailable` | Inferred; refused, no witness |
| F15 | Recording > 32 MiB, output > 4 MiB, 30 s deadline | resource constraints | Inferred; error → refused |
| F16 | Modified R22 counter, modified catalog, invalid rev, helper drift | `count-c1.py:47-49`, exit 2 | Inferred; whole measure unevaluable |
| F17 | Entry cites a carrier path that is safe UTF-8 but not JSON (`.bin`) | `bind_cli` code 2 | Observed; harmless but fragile |
| F18 | Used-by lists a non-existent lesson | registry honesty only | Observed (`corpus/lessons/round-23.md` absent) |

## Observations and probes (author-side)

All commands ran in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` or its subdirectories; no
carrier was executed by this seat.

| probe | exit | result |
|---|---|---|
| `sha256sum /home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage` | 0 | `49d2f597…b614`, 49,558,848 B |
| `node -p 'require("…/rea-agents/package.json").version'` | 0 | `6.5.0` |
| `git ls-remote` for `sigrok-cli-0.7.2`, `libsigrok-0.5.2`, `libsigrokdecode-0.5.3` | 0 | commits `b584f959…`, `a6b07d7e…`, `97991a39…` (dereferenced tags) |
| `curl …/doc/sigrok-cli.1 \| sha256sum`; `diff` against retained copy | 0 | `e3f06dfe…a5f9`, identical |
| `curl …/libsigrokdecode-0.5.3/decoders/uart/pd.py \| sha256sum`; `diff` | 0 | `51a29d0e…7da62`, identical |
| `curl …/libsigrok-0.5.2/src/input/binary.c \| sha256sum` | 0 | `fa037abe…dd9d1`, 4,394 B |
| `sha256sum` of S058/S059 retained copies, entry, counter, evidence | 0 | values in §§1,3,4 |
| `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root … --rev a3c92eb…` | 1 | k=1, `c1_incomplete`, historical identify only |
| in-process `bind_cli` on four success envelopes | — | 0 for inventory, uart-help, decode-uart-hi, decode-official-uart |
| in-process replay of the R23 entry loop, as written | — | aborts at `hello_world_8n1_9600.sr` with `UnicodeDecodeError` |
| in-process replay without the `.sr` citation | — | new witnesses: `inspect-signal-decoders` (inventory), `decode-signal-recording` (official + synthetic) |
| `ls corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` after entry arrival | 0 | 7,598-byte entry, sha256 `7598d2cb…6c35` |

The decode/inventory/help receipts carry `captured_at` 14:38 UTC, before these probes; this
seat did not produce them, and read and bound the retained records without replaying them. The
in-process replays are author-side checks of the counter's predicates, not the frozen counter at
a committed revision.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/PlannerDataWalk.md`
  — this report. SHA-256 (remove this line, then hash the remaining bytes): `38358b9cc013cb72b39a30215bf3570893abe8ec5fe2c0afcc5a1e31f1c497ac`.

No other files written. No production lane file, entry, SOURCES row, counter, evidence file, or
git state was modified.

## Installs

None. No pacman, uv, npx install, cargo, or npm transaction. REA was read/executed only through
the already-cached `npx -y rea-agents@6.5.0` where the receipts show it; this seat ran no REA
carrier command. `curl` and `git ls-remote` were read-only network probes.

## Open risks / unknowns

1. **No committed count yet.** k=3/6 is inferred from the counter's own loops and the live entry;
   only a commit + the frozen command can turn it into an observed `k`.
2. **Blocking `.sr` citation** (F1) is still present in the live entry at the time of writing.
   Until L1 removes it, the first committed measure will exit 2 rather than report a count.
3. **Decoder-source provenance gap.** S058/S059/S060 do not include the `uart/pd.py` or
   `binary.c` rows; the exact option ids/defaults rest on the observed envelopes and the manual's
   example. Add S061 if source relevance is reviewed strictly.
4. **S060 scope vs entry citation mismatch** for `uart-help.envelope.json`; the entry relies on it
   but S060 does not list it.
5. **`uart-help` evidence id absent** from the entry; the verb still counts, but the help
   envelope is not a bound witness.
6. **Empty-output binder gap.** An exit-0 decode with `total_lines:0` binds. The entry asserts
   exact non-empty output, but the counter does not enforce it; reviewers must keep that
   distinction.
7. **Trust boundary.** The AppImage runtime embeds Python 3.5 and prints library-prefix warnings
   on success; decoder modules and the preloaded host `libgmodule` are trusted, not authenticated.
   `hardware_acquisition:"not-performed"` is a provider declaration, not a syscall monitor.
8. **Dynamic ownership remains unresolved.** No debugger/Frida execution, attach, device access,
   or carrier execution was performed by this seat. `debug-with-gdb` and `debug-with-rizin`
   remain unheld; no claim here changes that.
9. **Used-by hygiene.** S058–S060 list `corpus/lessons/round-23.md`, which does not exist yet.
10. **Official carrier shape.** 12,885 lines include leading noise bytes and a final partial byte;
    the entry correctly avoids claiming a clean `Hello World!` stream, but any future calibration
    assertion must preserve that shape.
