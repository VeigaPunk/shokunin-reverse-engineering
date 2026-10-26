# R40AssimReject — assimilation reject leg: the AVM set, re-tested at the round-40 freeze boundary

**Verdict: DEFECTS FOUND** — 2 of 3 re-tested AVM entries are REJECT with spot-checkable reasons,
1 is ADMIT-AFTER-REWRITE; and the rejected mechanism, if it reaches the freeze, makes R40-C1's
fifth kill control unfireable.

Seat: critic / assimilation-reject (leaf, no subagents, no background jobs, no `agent://all`).
Full verdicts: `.ufo/waves/round-40/w1/artifacts/R40AssimReject/verdicts.md`.
Artifacts: `.ufo/waves/round-40/w1/artifacts/R40AssimReject/` (`handler-quote.txt`,
`exit-policy-quote.txt`, `dev-runs.tsv`, `envelope-argv.tsv`, `sha-identities.txt`,
`probe-output.txt`, `probe.py`, `repro.sh`, `repro-output.txt`, `inputs.sha256`, `logs/`).

## Axes named

| axis | what moves here |
|---|---|
| **coverage** | which AVM entry R40-C1 may cite for its Core row: one of three survives a bounded rewrite; two must be rejected before the freeze. |
| **depth** | the discriminating rule the corpus lacks: handler *selection* is marker-independent, the *extractor argv* is marker-dependent on the `Endian.BIG, 4` arm, and the **unblob process exit code witnesses neither success nor failure**. |
| **calibration** | whether each entry's own `recheck:` line can fail: for both rejected entries it cannot — they re-verify an observation that is true under both readings. |

## The strongest counterexample

`avm-firmware-image-unblob.md:16` ("it never notices the AVM marker at all") and `:75-77` ("The AVM
marker is **invisible to unblob** … it selects a handler on the magic and the endianness, never on
the marker").

The pinned handler does the opposite — unblob 26.6.4,
`unblob/handlers/filesystem/squashfs.py` (sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`):

```
47:                    # see …/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt
48:                    is_avm = header.bytes_used == header.mkfs_time
49:                    if not is_avm:
50:                        commands_args.append("-be")
```

and my own two development runs, differing in **4 bytes** of a genuine AVM-BE fixture:

| | child argv | files | unblob exit | failed-extract report |
|---|---|---|---|---|
| marker on (`c7f74691…`) | `sasquatch-v4be -no-exit-code -f -d …` | 4 | 0 | none |
| marker off (`7038aae4…`, `8:12 := 1792847340`) | `sasquatch-v4be -be -no-exit-code -f -d …` | 0 | **0** | `ExtractCommandFailedReport`, extractor exit 1 |

Four independent confirmations that the sentence is false, each cheap for a closure to spot-check:

1. the pinned source above (`:47` cites the AVM format spec in the same block);
2. the entry's **own** table at `:67` prints the BE argv *without* `-be` — the absent flag *is* the
   marker being read;
3. three sibling entries measure the branch as a decision
   (`sasquatch-unblob-avm-branch.md:16-18,27-31` "the AVM case is therefore signalled by the
   **absence** of a flag … **the `-be` is gone**"; `avm-le-variant-reachability.md:25`;
   `avm-image-extraction.md` / `avm-image-build-blocker.md` `image_is_avm` rows) with no pointer
   either way, and the lane's shipped triage table says it correctly at `SKILL.md:339`
   ("unblob read the AVM marker and omitted -be") citing the same `S112 lines 44-50`;
4. the **committed** round-39 evidence: `corpus/evidence/round-39/c2/heldout/H13/envelope.json`
   (class `avm-marker-be-dropped`) logs `sasquatch-v4be -no-exit-code …`, `H15` (class
   `body-extractor-failure`) logs `sasquatch-v4be -be …`.

Round 39 reached this same verdict (`R39AssimAvmCritic.md`, E4). Two waves later the sentence is
**byte-unchanged**, so it is a standing claim with no reversal recorded — the Gate would re-admit it.

## Verdicts (detail and replacement text in `verdicts.md`)

| entry | verdict | reason in one line | flip condition |
|---|---|---|---|
| `avm-firmware-image-unblob.md` | **REJECT** | headline and `:75-79` falsified by the pinned handler, its own table, three sibling entries and the lane's SKILL table; measurements otherwise reproduce | reverses only if `squashfs.py` has no `mkfs_time`/`bytes_used` comparison, or a marker flip changes neither argv nor outcome — measured as changing both |
| `avm-le-variant-reachability.md` | **REJECT** | "marker not set on that path" / "the option build would close it" is overturned by retained bytes: `avm-le-plain550.squashfs` (clean rebuild, `-DTARGET_FORMAT=AVM_LE`, no `-no-mkfs-time`) is **byte-identical** to the option-build image (`18d3ad05…`, 361==361); entry 3 says so in words without naming the file | reverses if that retained image shows `mkfs_time ≠ bytes_used` (it shows 361==361) |
| `avm-le-image-genuine-marker.md` | **ADMIT-AFTER-REWRITE** | central claim confirmed three ways (my probe: 361==361; two clean-rebuild recipes; run C reproduces `squashfs_v4_le` + `sasquatch -le` + 4 files, and `sasquatch-v4be` refusing the same image with "Block size too small"); but `:30` generalises the LE observation, `:55-56` denies a mechanism that exists, and it records success without the exit-code caveat | reverses if the retained image lacks the marker or the LE arm tests it (neither) |

## Consequence for the freeze (smallest safe corrections)

1. **The R40-C1 claim's mechanism sentence is correct; the entry it would cite is not.** Verified at
   `squashfs.py:40-54` and by the mark/no-mark pair. Rewrite `avm-firmware-image-unblob.md:16` and
   `:75-79` to the handler-selection vs extractor-argv split **before** a round-40 Core row cites it,
   or the contradiction lands inside the frozen row.
2. **Do not score R40-C1 kill control 5 on the unblob exit code.** "A genuine AVM body with the
   marker stripped (unblob adds `-be`, extraction fails)" *passes* on exit ≠ 0 today:
   `ExtractCommandFailedReport.severity = WARNING` (`unblob/report.py:91-98`) and the CLI maps
   `WARNING → 0` (`unblob/cli.py:464-475`), so a total failure exits **0** with 0 files (measured,
   `dev-runs.tsv` run B; reproduced by `repro.sh`). Score the kill as "0 published regular files
   **and** `ExtractCommandFailedReport` present" (or "`-be` present in the child argv"), and define
   the receipt binding "no failed chunk" the same way — otherwise the kill cannot fire and R39-CL5's
   re-minted-receipt defect reappears with the counter's own witness.
3. **Triage table v2 must keep the `-be in child argv` column.** `avm-marker-be-dropped` (H13) and
   `body-extractor-failure` (H15) are otherwise identical envelopes (exit 0, `squashfs_v4_be`,
   gap `extractor-failure`, 0 files) and differ only in the logged extractor command; v1 separates
   them by that column (`SKILL.md:334,339-340`, `sqfs-triage.py:43-47`). The v2 change list does not
   name the column — dropping it in a rewrite would collapse two labels into one. (C2 seats own this;
   the evidence came out of this attack.)
4. **Add reversal pointers in both directions between entries 2 and 3**, and retitle entry 2 to its
   surviving fact ("the define's value is `AVM_LE`") so a rejected decision is locatable from the
   admitting row.

## Evidence commands (paste-ready, no scratch required)

```
# 1 the falsified branch, in the installed package
grep -n "is_avm\|commands_args.append" ~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py | sed -n '1,6p'
# 2 why exit code is not a witness
grep -n "Severity.WARNING" ~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/report.py | sed -n '1,4p'
grep -n "Severity.WARNING, 0" ~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/cli.py
# 3 the entry contradicts its own table and the shipped skill
sed -n '67p;75,77p' /home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/avm-firmware-image-unblob.md
sed -n '339p' SKILL.md
# 4 the marker is read in committed evidence
python3 -c "import json;d=json.load(open('corpus/evidence/round-39/c2/heldout/H13/envelope.json'));print([o['command'] for o in [d['raw_result']['report'][0]['reports'][3]['extraction_reports'][0]]])"
# 5 the LE pair is one byte string
sha256sum /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/avm-le-{genuine,plain550}.squashfs
# 6 rebuild my three dev runs + the counterfactual (honours TMPDIR)
bash .ufo/waves/round-40/w1/artifacts/R40AssimReject/repro.sh "$(mktemp -d)"
```

## Method, bounds, ledger

- Inputs: `merge/kaidoku/knowledge/corpus/knowledge/avm-firmware-image-unblob.md`,
  `avm-le-variant-reachability.md`, `avm-le-image-genuine-marker.md` (read-only, hashed);
  development fixtures `lanes/kaidoku/round11/work/avm-be.squashfs`,
  `lanes/kaidoku/round13/work/avm-le-{genuine,plain550,standard-time}.squashfs`,
  `round12/work/avm-le.squashfs`; the pinned unblob 26.6.4 install; the committed round-39 C2
  envelopes; `SKILL.md:333-343`, `tools/round-39/sqfs-triage.py`.
- **No REA call was made.** No frozen carrier was touched (V1's AVM-BE member was not read; no
  vendor image was downloaded). The counterfactual carrier is a **copy** of a 4096-byte development
  fixture with 4 superblock bytes rewritten in scratch; the originals are unmodified (`sha256sum`
  of each is recorded in `inputs.sha256` and `sha-identities.txt`).
- unblob 26.6.4 and sasquatch/sasquatch-v4be 4.5.1 used as installed — **not** reinstalled, moved
  or removed. **No tool installed**; no pacman transaction; no host service touched.
- Scratch `/fast/scratch/hyaku/kaidoku-r40/R40AssimReject` (clones/fixtures/outputs), `TMPDIR` set
  to it for every run; `unblob` run from inside a per-run directory so its `unblob.log` landed
  there; copied logs are in `artifacts/R40AssimReject/logs/`. Scratch removed before yield.
- Read-only git only; none needed this wave. Lane corpus/tools/plans/PROVINCE/SKILL untouched.
- `[INFERENCE]` used twice and marked: the Broadcom handler reaches the same marker arm (read from
  construction sites `:548-553`, not measured); the motive behind entry 2's stale build (the byte
  evidence is direct, the reasoning is not).
