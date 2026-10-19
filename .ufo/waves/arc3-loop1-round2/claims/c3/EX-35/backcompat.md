# EX-35 — C3 back-compat: v1 receipt's sha256 fields via the v2 tool's verify mode

Seat EX-35 · chain c3 · role executor · wave arc3-loop1-round2 · 2026-10-19.
Frozen claim under test: `.ufo/waves/arc3-loop1-round2/claims-frozen.md:52-64`,
clause "v1 receipts remain verifiable against the tool's sha256 fields".

**Result: VERIFIED (sha256 fields), with a measured exit-code caveat.** The
round-1 v1 receipt's sha256 fields verify 5/5 against the live paths and 5/5
against EX-31's round-2 v2 receipt; planted sha256 drift is detected on exactly
the affected paths. In `--live` mode the v1 sample exits **12** (not 0) because
the tool reproduces the round-1 `LABEL-DEFECT`; the cause is isolated below and
is the label, not the digests.

## 1. v1 sample identity

| artifact | path | sha256 | size |
|---|---|---|---|
| v1 receipt | `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt` | `b8ed19365c103a4ab355678f0fffe0db4e0011a18b441e79f38d9e80de3d0776` | 2045 B |
| v1 metadata sidecar | `…/receipts/config-pre-pair-metadata.txt` | `85fa1860000bda4de57ffb17219e59fa0e553d505eb76815c4bcf542f6426a90` | 1111 B |

Both files re-hashed this round (`sha256sum`, read-only) — unchanged from CU-1's
round-1 capture. v2 tool revision verified throughout:
`.ufo/gates/custody-pair/custody-pair.py` sha256
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (889 lines;
its own header self-records this hash, `capture-pre.txt:3`).

## 2. Field mapping v1 → v2 (documented)

| v2 canonical field | v1 source | mapping rule |
|---|---|---|
| `sha256` | `SHA256:` line (`config-pre-pair.txt:17,24,31,38,45`) | verbatim — the contract |
| `sha256` (compact trailer) | `## compact sha256 list (5 paths)` | cross-checked against block values; agrees 5/5 |
| `size` | `SIZE:` | verbatim |
| `mode` `uid` `gid` | `MODE: … UID: … GID: …` | verbatim |
| `mtime_epoch` | `MTIME_UTC:` line | **not UTC** — a local (-03) rendering under an `MTIME_UTC` label; epoch recovered by re-rendering at the v1 zone |
| `inode` | sidecar field 2 | verbatim (sidecar is the pipe-v1 shape) |
| `ctime` | sidecar field 3 | same label defect as `MTIME_UTC` |
| `blocks` | sidecar field 6 | v1-only, informational |

v1 shapes the v2 tool recognises, measured: `stanza-v1` (the receipt),
`pipe-v1` (the sidecar), `sums-v1` (compact list alone).

## 3. Before → after measurement

Command (canonical, per shape):

```bash
T=.ufo/gates/custody-pair/custody-pair.py
python3 $T verify --live <v1 receipt>          # live comparison
python3 $T verify <v1 receipt> <v2 receipt>    # receipt-vs-receipt
```

Measured matrix (`v2-verify-matrix-final.out`, `v2-verify-cross.out`,
`v2-verify-crossversion.out`; run-utc 2026-10-19T12:06Z):

| reference | candidate | SHA256-CONTRACT | verdict | exit |
|---|---|---|---|---|
| v1 receipt (round-1) | live filesystem | **5/5 agree** | METADATA-DRIFT (LABEL-DEFECT ×5) | 12 |
| v1 sidecar (pipe-v1) | live filesystem | **5/5 agree** | METADATA-DRIFT (LABEL-DEFECT ×5) | 12 |
| v1 compact list (sums-v1) | live filesystem | **5/5 agree** | MATCH-V1-PARTIAL | 0 |
| v1 receipt | v1 receipt (self) | **5/5 agree** | MATCH-V1-PARTIAL | 0 |
| v1 receipt (round-1) | RV-12 independent capture (round-2 T0) | **5/5 agree** | MATCH-V1-PARTIAL | 0 |
| v1 receipt (round-1) | EX-31 v2 `capture-pre.txt` (round-2, 12:06Z) | **5/5 agree** | METADATA-DRIFT (LABEL-DEFECT ×5) | 12 |

The last row is the round-boundary case: a round-1 receipt checked against a
v2 receipt captured ~5.5 h later and two commits later (v1 header
`repo-HEAD: e845c2b5…` → v2 header `repo-HEAD: 14b1682b…`) — no CONTENT-DRIFT,
no REWRITE-DRIFT, sha256 5/5. Nothing in the content moved; the only divergence
the tool reports is the label defect it is built to reproduce.

## 4. Cause isolation (what the 12 is, and is not)

| probe (fixture, scratch-only) | expected | measured |
|---|---|---|
| `fixtures/v1-no-time.txt` — v1 receipt with **only the `MTIME_UTC:` lines removed** | sha256 clean, exit 0 | MATCH-V1-PARTIAL 5/5 sha256, **exit 0** |
| `fixtures/v1-swap-sha.txt` — devin/omp digests exchanged | exactly those 2 flagged | CONTENT-DRIFT ×2, `SHA256-CONTRACT: 3/5`, **exit 10** |
| `fixtures/v1-corrupt-sha.txt` — one digest nibble flipped | exactly that 1 flagged | CONTENT-DRIFT ×1, `SHA256-CONTRACT: 4/5`, **exit 10** |
| `fixtures/v1-absent-path.txt` — one path missing | fail closed | ABSENT ×1, **exit 13** |

Removing only the mislabeled time strings moves the sample from exit 12 to
exit 0 with the same 5/5 sha256 agreement, and planting digest drift exits 10 —
so the sha256 verification is discriminating and the 12 is attributable solely
to `LABEL-DEFECT`.

## 5. Attacks / refutations attempted

| # | attack | verdict |
|---|---|---|
| A1 | v1 receipt with one digest corrupted | **tool DETECTS** (exit 10, path named) |
| A2 | two digests swapped (content-vs-order confusion) | **tool DETECTS** (exit 10, both paths named, 3/5) |
| A3 | receipt names an absent path | **tool fails closed** (ABSENT, exit 13) |
| A4 | unparsable input: empty file / comment-only file | **exit 2** (correct usage class) |
| A5 | partial receipt: 1 path of the canonical 5 | **GAP: exit 0**, MATCH-V1-PARTIAL 1/1 — a 1-path reference verifies clean with the other 4 custody paths unaccounted for (`v2-robustness-probes.out`). Not a violation of the frozen claim (no coverage assertion is claimed) and arguably by design ("compared on the fields they actually carry"), but it is the round-1 H1 shape (unaccounted scope reads as pass) applied to receipts. Cheap mitigation proposed below |
| A6 | transient crash on two fixtures | `KeyError: 'sha_agree'` in `verify_sets` **against an intermediate revision** while the tool was being live-edited (883 → 889 lines between reads); same fixtures pass at `112d01dc…`; exact crashing revision hash not captured (`v2-verify-crash-attempt1.txt`). Mitigation: crash paths should return exit 2, not traceback/1 |
| A7 | label defect as a pass-forgery vector | the tool reproduces it as a finding rather than swallowing it — but note the polarity: a v1 receipt *always* exits 12 in `--live` mode, so a gate keyed on `exit == 0` cannot pass any v1 receipt (see §6) |

## 6. Residual and proposed change (patch text)

`proposed-v1-verify-adapter.patch.md` (patch text only — EX-35 is not the C3
implementer). Its now-narrow content, on measured grounds:

1. **exit-code semantics for known-v1 references.** `LABEL-DEFECT` is a true
   finding about the *receipt*, but a v1-form reference can never exit 0 in
   `--live` mode, so "v1 receipts remain verifiable" is only readable via the
   `SHA256-CONTRACT: n/m` line, not via the exit code. Proposal: an explicit
   switch (`--v1-label-defect=note` or `--expect-format v1`) that keeps the
   finding visible but yields exit 0 when the only drift is the reproduced
   defect; or, if the strict exit is intended, the parent should record the
   documented reading (`sha256 contract line`) as the back-compat gate.
2. **coverage assertion** (A5): assert the reference covers the canonical path
   set, or declare the count, so a partial reference cannot verify clean.
3. **crash discipline** (A6): any unhandled exception in a subcommand must map
   to exit 2.

## 7. Independent harness (parallel instrument, same inputs)

`tools/v1-backcompat.py` (also under `/var/tmp/ex35/`): parses the v1 form
directly, re-derives the mtime epoch at a declared v1 TZ, and cross-checks the
compact trailer. Parity (`harness-parity.out`):

| fixture | harness exit | v2 tool exit |
|---|---|---|
| v1 receipt + sidecar vs live | 0 (5/5 sha256, 5/5 inode, 5/5 inferred epoch) | 12 (sha256 5/5) |
| synthetic v1 fixture | 0 | 12 |
| corrupt sha | 1 | 10 |
| absent path | 2 | 13 |
| compact-only (no PATH blocks) | **2 — vacuous PASS refused** (`FAIL could-not-evaluate: no PATH blocks parsed … compact entries=5`) | 0 |

The compact-only row is a deliberate difference: the harness treats zero parsed
paths as a failure (the round-1 H1/H3 lesson); the v2 tool treats it as a clean
v1 partial match. Both readings are defensible — the tool is comparing what a
reference carries, the harness was asserting that a receipt was parsed at all —
but for the back-compat gate the tool's reading is the weaker one, and it is
the same shape as A5.

## 8. Reproduction

```bash
cd /var/tmp/ex35
T=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/cross/receipts
python3 $T verify --live $R/config-pre-pair.txt
python3 $T verify $R/config-pre-pair.txt \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round2/claims/c3/EX-31/capture-pre.txt
python3 tools/v1-backcompat.py --receipt $R/config-pre-pair.txt --sidecar $R/config-pre-pair-metadata.txt
```

Discipline: the 5 custody paths were only `stat`-ed and `sha256sum`-med (never
read into an artifact, never written). All drift fixtures are scratch copies of
the receipt text or synthetic files under `/var/tmp/ex35/`; nothing under
`~/.config`, `~/.omp`, `~/.kimi-code`, `~/.bashrc`, `~/.profile` was modified.
