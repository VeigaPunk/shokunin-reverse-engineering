# A fresh-pack held-out arm separates a derivation from a table: the round-92 repair label admitted two five-carrier forgeries, and the fresh arm refuses both (round 93, R93-C1 calibration)

source: S318, S317, S271 — UPX 5.2.0 `src/p_unix.cpp` `PackUnix::unpackExtent` (p_unix.cpp:476) and its bound at :496, `src/p_lx_elf.cpp` `PackLinuxElf64::unpack` (p_lx_elf.cpp:7755) and its end-of-file trailer check at :8065, and `doc/upx-doc.txt` lines 441-442 under `NOTES FOR LINUX/ELF386` (heading line 433). S318 is the row this round opens; S317 is re-grounded here and S271 is re-opened. The packExtent writer (p_unix.cpp:335) and the S313 wording are named as prose context only and are not cited by this entry.
verified-at: 92a240521bd1bf2213b75d18d9b176a8dafdc67c (counter `tools/round-93/stop-boundary-repair-battery-v3.py`, sha256 `60026511e54cdc1df71233c491392fafcc89705808fa5c187d96a85862cbd4e3`; candidate repair `tools/round-92/upx-stop-boundary-search-repair.py`, sha256 `ce1b1769d56c1d90fcf2ee0800ca508476b45eddc2e8a6d7e2f01aa8d12a70c1`; the after-state is measured at the landing commit named in SCORECARD round 93); base `0a2a23da5eb50410a8a0df90c031d9f4fdadb024`.
recheck: 180d, and on any UPX release. The counting command and the receipts are named under Measured; the source anchors are re-fetchable with `curl -fsSL https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp` and the two sibling paths.

## The class the arm measures

The round-92 repair label (`repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`) scores a repair over five public carriers — `jq`, `xxd`, `libz` (`/usr/lib/libz.so.1.3.2`), `dinit` (`/usr/bin/docker-init`) and `xz` (`/usr/bin/xz`) — two directions each, plus ten far cells at ±40 and five intact controls. It is a label over a *fixed carrier set*, and two forgeries pass it:

- **F1, the pinned-image table** (`.ufo/waves/round-93/controls/table5-window.py`): pack the five carriers once, keep the pristine packed bytes and each carrier's last-block `sz_cpr`, and on any input whose bytes match a pinned image outside the four-byte window, write the pinned image back. No packer verdict is ever consulted.
- **F2, the carrier-read** (`.ufo/waves/round-93/controls/carrierread5.py`): the round-92 repair itself, with its `upx_green` verdict function (the packer's own `upx -t`) replaced by membership against the five carriers' packed images, built fresh once per process.

Both are admitted by the frozen round-92 label at base. The receipts are committed:

| forgery | receipt (base `0a2a23da`) | label | met | exit |
|---|---|---|---|---|
| F1 pinned-image table | `.ufo/waves/round-93/pre/r93-do-nothing-r92label-F1.json` | `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10` | True | 0 |
| F2 carrier-read | `.ufo/waves/round-93/pre/r93-do-nothing-r92label-F2.json` | `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10` | True | 0 |

Re-derived from the committed receipts with `jq -r '.label, .met_target, .exit'` over each file. The negative control `.ufo/waves/round-93/pre/r93-negative-control-identity-r92label.json` (the `identity_noop.py` control) is met False, exit 1, label `repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 0 of 10`; the positive control `.ufo/waves/round-93/pre/r93-positive-r92repair-r92label.json` is met True, exit 0. So the round-92 label does discriminate *something*: it is not vacuous, and it does reject a no-op. What it cannot see is a forgery whose answer is a lookup.

## What the fresh-pack held-out arm is

`tools/round-93/stop-boundary-repair-battery-v3.py` keeps the round-92 public battery unchanged (imported by path, sha256 `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc`) and adds one arm whose input is a packed image **no table can contain**, because it is built at measure time:

1. **A pinned, nonce-marked source.** `/usr/bin/env`, sha256 `a9ba02dcad338ee7f0b03e58a1cf44009b2bd645b09c2b423242e9791d202301` (verified on this host: `sha256sum /usr/bin/env` → the same digest). The source is mutated by writing the marker `KAIDOKU-R93-<16 hex nonce>` into the middle of its largest non-executable `PT_LOAD` segment (`mutate_source`, `tools/round-93/stop-boundary-repair-battery-v3.py:81-115`), so the marker is present in the mutated source and absent from the original.
2. **Packed fresh, twice.** The mutated source is packed with the pinned packer (`/usr/bin/upx` 5.2.0, sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`) inside `--work`, twice. **Determinism guard:** the two packed images must be byte-identical (`provenance.deterministic`); a non-deterministic pack makes the arm `unevaluable`, not green.
3. **No collision with the public set.** The fresh packed image's sha256 must not be in the set of the public carriers' packed sha256s (`provenance.collides_public_packed` must be false).
4. **Tamper the last block.** The chain walk (`v2.layout`) yields the block list; the last block's `sz_cpr` is moved by −7 and +7 (near) and by −40 and +40 (far), the same deltas and the same ±16 window the round-92 label uses. Each cell is a fresh copy of the fresh packed image with four bytes changed.
5. **A roundtrip oracle.** A cell classified `repaired` must additionally satisfy `upx -d` on the repair's output: the decompressed bytes' sha256 must equal the sha256 of the *mutated source*. A repair that writes something that decompresses to the wrong bytes is reclassified `roundtrip-fail` and is not counted as repaired. The round-92 label has no such clause — it can only compare bytes, so a repair that "repairs" to a self-consistent but wrong image was invisible to it.
6. **An intact control.** The pristine fresh packed image is handed to the repair unchanged; a repair that refuses or alters it fails the intact clause.

The five provenance atoms (marker present in the mutated source, marker absent from the original, pack determinism, no collision with the public packed images, at least one block in the chain) are required: if any fails, the arm returns exit 2 `unevaluable` and the label is not computed at all.

## What it kills

Both round-92 forgeries score met False under v3, and the mechanism is visible in the receipt: **both fresh near cells are refused**, and the fresh cells carry no repaired output at all.

| forgery | receipt | label | met | exit | fresh near cells |
|---|---|---|---|---|---|
| F1 pinned-image table | `.ufo/waves/round-93/w1/ScribeKnowledge/receipts/r93-c1-v3-F1-table5.json` | `repaired 10 of 12; wrong 0; unsafe 0; intact 5 of 6; far-refused 12 of 12; fresh-roundtrip 0 of 2` | False | 1 | refused, refused |
| F2 carrier-read | `.ufo/waves/round-93/w1/ScribeKnowledge/receipts/r93-c1-v3-F2-carrierread5.json` | `repaired 10 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 0 of 2` | False | 1 | refused, refused |

Both receipts were produced by this seat with

```sh
python3 -I -B tools/round-93/stop-boundary-repair-battery-v3.py --root . \
  --repair-cmd .ufo/waves/round-93/controls/table5-window.py \
  --work "$S/work/v3-F1" --rev 92a240521bd1bf2213b75d18d9b176a8dafdc67c \
  --expect 'repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2' \
  --json-out "$S/work/v3-F1.json"
```

and the same command with `--repair-cmd .ufo/waves/round-93/controls/carrierread5.py` for F2; both exited 1. The F1 receipt's `fresh_cells` are all `class: "refused"` with `typed_strict: true`, and `fresh_provenance` carries `deterministic: true`, `collides_public_packed: false`, `marker_in_mutated: true`, `marker_absent_in_original: true`, `blocks: 5`. The F2 receipt differs in one visible place: `fresh_intact.identity` is true and `rc` 0 (the carrier-read repair copies the fresh image back unchanged, since it does not know the fresh carrier), while F1's fresh intact cell is a typed refusal with `identity: false` — F1 refuses the intact fresh input because it has no pinned image matching it.

The **unscored** probe committed at the declaration is the same measurement, taken before the freeze: `.ufo/waves/round-93/pre/probe-v3-F1-unscored.json` — F1 under v3, label `repaired 10 of 12; wrong 0; unsafe 0; intact 5 of 6; far-refused 12 of 12; fresh-roundtrip 0 of 2`, met False, exit 1, with the same four fresh cells all `class: "refused"`. The probe's `revision` field reads `probe-unscored`, so it is evidence, not a scored receipt.

The honest repair stays admitted under v3: with `--repair-cmd tools/round-92/upx-stop-boundary-search-repair.py` the label is `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2`, met True, exit 0 (this seat's run, `--work "$S/work/pos3"`, no `--json-out`; see Limits for why the receipt form matters).

## The mechanism floor it does NOT claim

**The fresh arm does not claim to reject a forger that derives the stored value by walking the chain without the packer's verdict.** Such a forger is a *derivation*, not a table: it reads the bytes in front of it and computes the answer. Nothing about a held-out carrier distinguishes it from the honest repair, because it produces the same correct bytes on the held-out cell. The fresh arm's discriminating power is exactly this: it separates *lookup* from *derivation*. It cannot separate two derivations from each other.

This limit was named before the freeze in the round-93 lesson (`corpus/lessons/round-93.md`, Named limits 1) and it is not closed here.

[INFERENCE] The floor is also the reason the arm needs the roundtrip oracle and not only a fresh carrier: a walk-based forger that computes a *plausible but wrong* value would pass a bare fresh-carrier check if it merely produced some output, whereas the roundtrip clause demands the original bytes back.

### A measured illustration of the floor

This seat built a forger that is neither a table nor a carrier-read — it is the round-92 repair with its oracle swapped: `upx_green` (the packer's `upx -t` verdict) replaced by an `upx -d` decompression oracle. It is a different mechanism, on the same derivation, and it **passes** the frozen label:

```sh
python3 -I -B tools/round-93/stop-boundary-repair-battery-v3.py --root . \
  --repair-cmd "$S/probe/f4-oracle-swap.py" --work "$S/work/v3-F4b" \
  --rev 92a240521bd1bf2213b75d18d9b176a8dafdc67c \
  --expect 'repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2'
```

→ `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True exit 0`, exit 0. The probe is retained at `.ufo/waves/round-93/w1/ScribeKnowledge/probes/f4-oracle-swap.py` (unscored, not landed as an instrument). **Observation:** the fresh arm does not certify *which* mechanism produced the answer; it certifies that the answer was not looked up from a fixed carrier set. A second probe that is a pure table over an unrelated source set is likewise out of the arm's reach, because the arm pins exactly one source (`/usr/bin/env`).

## Strict typed parsing

The round-92 parser is weaker than the lane's own criterion in two ways. `tools/round-92/stop-boundary-battery-v2.py` `typed_refusal` checks **key presence only**: it returns true for `{"refused": null}` and it never looks at the exit code. QUALITY row 185 states the stricter contract — "a refusal is typed only when the child exits 2 and the last stdout line is a JSON object with a `refused` key" — and the round-92 spot-check §6 item 3 names the gap verbatim: "C2 parser is key-presence-only (`refused: null` counts as typed — ReviewerContract)". The v3 arm's `strict_typed` (`tools/round-93/stop-boundary-repair-battery-v3.py:118-133`) closes **both** gaps and adds a third: exit code exactly 2, the last non-empty stdout line parsing as a JSON **object**, and its `refused` value being a **non-empty string**. The per-cell flag is `typed_strict` in the receipt.

**Observed limit, and it is a real one:** `typed_strict` is computed and recorded but **never read by the verdict**. The `met` expression in `tools/round-93/stop-boundary-repair-battery-v3.py:315-321` folds in the label, the counts and `prov_ok`; no `typed_strict` value appears in it. Two probes show the consequence:

- a repair that refuses everything with **rc 1** and a JSON body (`{"tool":"f5-rc1-refuse","refused":"untyped rc 1"}`) is scored `far-refused 12 of 12; fresh_far_refused 2` with `typed_strict: false` on every fresh cell and on `fresh_intact` — the refusal count is met by an **untyped** refusal (probe `.ufo/waves/round-93/w1/ScribeKnowledge/probes/f5-rc1-refuse.py`, receipt `.ufo/waves/round-93/w1/ScribeKnowledge/receipts/r93-c1-probe-F5-rc1-refuse.json`);
- a repair that refuses with **rc 2** but the **empty string** as the `refused` value is likewise scored `far-refused 12 of 12`, `typed_strict: false` on all four fresh cells (probe `.ufo/waves/round-93/w1/ScribeKnowledge/probes/f6-empty-refused.py`, receipt `.ufo/waves/round-93/w1/ScribeKnowledge/receipts/r93-c1-probe-F6-empty-refused.json`).

Both probes exit 1 overall only because the other counts fail (`repaired 0 of 12`, `intact 0 of 6`, `fresh-roundtrip 0 of 2`), not because the typing was checked. **A strict typing that is computed but not asserted is decoration, not a clause** (QUALITY row 105's shape: "a count a counter computes and prints is not a check"). The claim's own text says the parser is strict; the parser is, and the verdict does not consume it. This is a gap in the *v3 instrument as frozen*, not a statement about the honest repair, which refuses typed (rc 2 + a non-empty `refused` string) on every far and fresh-far cell measured here.

## Measured

| claim | before | after | receipt |
|---|---|---|---|
| round-92 label admits F1 (pinned-image table) | met True, exit 0, label `repaired 10 of 10; …` | v3: met False, exit 1, both fresh near cells refused | `.ufo/waves/round-93/pre/r93-do-nothing-r92label-F1.json`; `…/w1/ScribeKnowledge/receipts/r93-c1-v3-F1-table5.json` |
| round-92 label admits F2 (carrier-read) | met True, exit 0, label `repaired 10 of 10; …` | v3: met False, exit 1, both fresh near cells refused | `.ufo/waves/round-93/pre/r93-do-nothing-r92label-F2.json`; `…/w1/ScribeKnowledge/receipts/r93-c1-v3-F2-carrierread5.json` |
| negative control `identity_noop.py` under the round-92 label | met False, exit 1 | v3: met False, exit 1 | `.ufo/waves/round-93/pre/r93-negative-control-identity-r92label.json`; this seat's run (no receipt written — see Limits) |
| positive control, honest repair | round-92 label met True, exit 0 | v3 label `repaired 12 of 12; …; fresh-roundtrip 2 of 2`, met True, exit 0 | `.ufo/waves/round-93/pre/r93-positive-r92repair-r92label.json`; this seat's run at `--rev 92a240521…` |
| unscored probe, F1 under v3 | — | `repaired 10 of 12; …; fresh-roundtrip 0 of 2`, met False, exit 1 | `.ufo/waves/round-93/pre/probe-v3-F1-unscored.json` |

Every number above is re-derivable from the named receipt with `jq -r '.label, .met_target, .exit'` (or `.counts`). The **frozen after-label** for the honest repair is `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2`, and it is the `--expect` string of the counting command below.

### Counting command

```sh
python3 -I -B tools/round-93/stop-boundary-repair-battery-v3.py --root . \
  --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py \
  --work <scratch> --rev <measured> \
  --expect 'repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2' \
  --json-out <receipt>
```

Exit 0 means the label equals `--expect` and the counter's own conditions hold.

## Limits (measured where stated; none is closed here)

1. **The v3 counter cannot write its own receipt when a fresh near cell is repaired.** `score_fresh_cell` keeps the repair's raw output bytes in `row["output"]`, and `json.dump` cannot serialize `bytes`. The run therefore **crashes with `TypeError: Object of type bytes is not JSON serializable` when serializing dict item 'output'`**, after the score is computed but before the receipt is complete; the process exits 1 and the `--json-out` file is left as a truncated, unparseable JSON prefix. Measured: the honest repair under v3 with `--json-out` exits 1 with that traceback and a 706-byte unparseable file, while the identical run **without** `--json-out` prints `repaired 12 of 12; …; fresh-roundtrip 2 of 2 met True exit 0` and exits 0. The same crash hits F3 (`identity_noop.py`) and the oracle-swap probe, for the same reason (both produce output bytes). It does **not** hit F1 or F2, whose fresh cells are refusals with no output file — which is exactly why the committed probe receipt `.ufo/waves/round-93/pre/probe-v3-F1-unscored.json` parses cleanly while the positive control's does not. **The frozen counter's sha256 is `60026511…`, unchanged in this round; this entry does not edit it.** The after-receipt at the measured revision must therefore be taken without `--json-out` (stdout only), or the receipt must be recorded by a caller that writes the label and the counts itself — the L1's decision, not this seat's.
2. **The strict typing is not asserted** (see the section above). Two probes show an untyped rc-1 refusal and an rc-2 empty-string refusal both scoring `far-refused 12 of 12`. This is QUALITY row 185's own clause unmet in the frozen instrument: "A label that asserts refusal must also assert the typed count." The v3 label asserts `far-refused 12 of 12` and asserts no typed count anywhere, and the `typed_strict` flag the receipt carries is never read by the `met` expression.
3. **One source only.** The arm pins `/usr/bin/env` and one nonce. It kills the five-carrier table class by construction and says nothing about a table over other sources.
4. **The mechanism floor stands.** A forger that derives the stored value by walking the chain without the packer's verdict is not a table forgery and is not claimed to be rejected; the oracle-swap probe above passes the frozen label (exit 0).
5. **The ±16 window and the ±40 far arm are unchanged** from round 92 (that entry's limit 1 and limit 3). The fresh arm reuses `v2.DIRECTIONS` and `FAR_DELTAS = (-40, 40)`.
6. **Non-ELF packed inputs remain unmeasured** (round-92 limit 6): no PE or Mach-O packed sample was built, and the fresh source is an ELF only (`mutate_source` refuses a non-ELF or a non-little-endian-64-bit source).
7. **Packer dependence.** The result depends on UPX 5.2.0, sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`; the counter refuses to score (`unevaluable: packer sha256 drift`) if the host packer differs.
8. **The walk cannot locate the pristine value by geometry alone.** This seat measured the chain walk on the fresh image: for every candidate value `v` in the window `[stored−16, stored+16]` the walk yields the *same* result (5 blocks, last block at offset 29841) — the walk does not discriminate the candidates. The stored `sz_cpr` was 575 and the PackHeader offset 34400, and `last.block + 12 + stored = 30428 ≠ 34400`, so the chain does not even land on the PackHeader. **Observation:** the pristine value is not recoverable from the walk's landing point, which is why the packer's own verdict is the oracle. This is the geometric counterpart of QUALITY row 179 and of the round-91 finding. Probes retained at `.ufo/waves/round-93/w1/ScribeKnowledge/probes/p2-geometric.py` and `…/p3-geomwalk.py`.
9. **Fresh-pack determinism is per-nonce, not across runs.** The nonce is `secrets.token_hex(8)` per invocation, so the fresh packed image's sha256 differs between runs (`f2cdab48…` in this seat's F1 run, `812bc45a…` in F2's, `99268486…` in the committed probe). The determinism atom is *within* one invocation (two packs of the same mutated source), which is what it claims to be; it is not a claim that the arm is byte-reproducible across invocations, and the receipts' `fresh_packed_sha256` values are therefore not comparable between receipts.
10. **Not examined.** This seat did not build a PE or Mach-O packed sample; did not test a packer other than UPX 5.2.0; did not measure the arm's cost on a large input; did not exercise the `two or more green values` branch (no second green value was found in the window, so the branch is code, not measurement); did not test the arm against a carrier set other than the five public ones plus `/usr/bin/env`; and did not run the v3 counter at any revision other than `92a240521…`.

## Gate

| row | URL | access date | HTTP / size / sha256 | located quote (≤25 words) | used for |
|---|---|---|---|---|---|
| S318 | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp | 2026-11-05 (opened this round) | 200 / 24181 / `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | line 496: `if (sz_cpr > sz_unc \|\| sz_unc > (int)blocksize)` | the per-block bound in `unpackExtent`; the caller scope is per-family, not one loop (limit 8) |
| S316 | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp | 2026-11-05 (re-opened this round) | 200 / 24181 / `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | line 449: `fo->write(&tmp, sizeof(tmp));` | `packExtent` writes the twelve-byte header before exactly `sz_cpr` payload bytes — the pack side of the fresh arm's determinism guard |
| S271 | https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt | 2026-11-05 (re-opened this round; sha re-derived by this seat) | 200 / 37208 / `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` | lines 441-442: `Packed programs will be byte-identical to the original after uncompression.` | the packer's byte-restoration statement — the authority behind the `upx -d` roundtrip oracle |
| S317 | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp | 2026-11-05 (re-opened this round) | 200 / 373743 / `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` | line 8065: `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic` | the caller's end-of-file trailer check that decides the stop-boundary class |
| S313 | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp | 2026-11-05 (re-opened this round) | 200 / 24181 / `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | line 476: `unsigned PackUnix::unpackExtent(unsigned wanted, OutputFile *fo,` | the block-extent consumer the fresh arm's chain walk models |

Line numbers verified by `sed -n '476p;496p'` and `sed -n '335p;449p'` on the fetched bytes (`p_unix.cpp`), `sed -n '8065p'` on `p_lx_elf.cpp`, and `sed -n '433p;441,442p'` on `upx-doc.txt`. The three digests match the SOURCES.md locators for S313, S316, S317 and S271 exactly.

**A correction to the S318 draft's caller list.** The row draft at `.ufo/waves/round-93/l1/drafts/s318-draft.md` lists the `unpackExtent` call sites in `p_lx_elf.cpp` as "7181, 7381, 7902, 7907, 8051, 9149, 9154, 9296". `grep -n 'unpackExtent('` over the fetched `p_lx_elf.cpp` returns **ten** call sites — the draft's eight plus **7102** and **7305**, which are the `un_shlib_1` peek calls (`PackLinuxElf64::un_shlib_1`, declared at 7011, and `PackLinuxElf32::un_shlib_1`, declared at 7214). The draft's `teaches` text names `un_shlib_1` as a caller family, so the omission makes the enumeration incomplete rather than the prose false. **Observation:** the two omitted lines are `unsigned const sz_block1 = unpackExtent(sz_elf_hdrs, nullptr,` at 7102 and 7305 — the header peek, whose `fo` argument is `nullptr`. The row's own claim ("cite the call site before citing the loop") is unaffected; the locator's call-site list should carry all ten. This is reported, not edited: the S318 row is the L1's to land.

Round-92 entry this extends: `corpus/knowledge/2026-11-05-r92-stop-boundary-repair.md`. Its limit 2 (a pinned-image table passes the frozen C1 label) and limit 3 (a carrier-read and a five-entry table pass v2) are the limits this round's arm closes; its limit 1 (the ±16 window is a cap, not a packer property) and limit 4 (the two-green refusal branch has no measured instance) are unchanged.
