# ScoutS321 — independent non-author verification of the S321 measurement

Seat: `ScoutS321` (scout). Lane: `kaidoku`, round 96, attempt 1.
Declaration commit read: `e4d1f7de9deae83e6d5f78d2d7f0157196002af0` (base `0ea695e826f2dca53dd55ac0bafead93de26b173`).
Lane READ-ONLY for this seat. Lane writes: only
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-96/w1/ScoutS321/` (this file + receipts)
plus the report `.ufo/waves/round-96/w1/ScoutS321.md`.
Scratch `/fast/scratch/hyaku/kaidoku-r96/ScoutS321` deleted before yield.
No tool installed or upgraded (`sha256sum`, `file`, `upx` 5.2.0, `python3` 3.14.8 were already present).

**Bottom line: the S321 measurement reproduces exactly — every field of the committed receipt
re-derives byte-for-byte, and the receipt is the committed blob at the declaration commit. One
calibration finding the L1 must carry: the S321 arm does NOT inherit the round-93 fresh arm's
anti-table property (it does not nonce-mutate its source), so the S321 arm is satisfied by a
one-entry pinned-image table — measured, exit 0, `met True`. The claim as frozen does not assert
anti-table for S321, so this is not a kill-rule violation; it is a bound the S321 knowledge entry
must state.**

## 1. Host digests and identities

```
sha256sum /usr/bin/printf /usr/bin/env
→ b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7  /usr/bin/printf
→ a9ba02dcad338ee7f0b03e58a1cf44009b2bd645b09c2b423242e9791d202301  /usr/bin/env

file /usr/bin/printf /usr/bin/env
→ /usr/bin/printf: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked,
  interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e7eb13c0620dda16d8b82cd2b7ab2ac854a0355a,
  for GNU/Linux 4.4.0, stripped
→ /usr/bin/env:    ELF 64-bit LSB pie executable, x86-64, ... BuildID[sha1]=0643d2009289281a0847fa2d38bce244239b9755, ... stripped

stat -c '%n inode=%i links=%h size=%s' /usr/bin/printf /usr/bin/env
→ /usr/bin/printf inode=13516862 links=1 size=76088
→ /usr/bin/env    inode=13516828 links=1 size=68312        (distinct files, not hardlinks)

upx --version   (exit 0)
→ upx 5.2.0 / UCL data compression library 1.03 / zlib 1.3.1.1-motley / LZMA SDK 4.43
  Copyright (C) 1996-2026 Markus Franz Xaver Johannes Oberhumer et al.
sha256sum /usr/bin/upx
→ cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969
  (identical to UPX_SHA256 pinned in tools/round-92/stop-boundary-battery-v2.py:50 and to
   .ufo/waves/round-96/pins.sha256)
```

`printf`'s sha256 equals the claim's declared source digest
`b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7` and the pin at
`.ufo/waves/round-96/pins.sha256:60`.

## 2. Pack determinism, `upx -t`, and execution of the packed image

Scratch only (no lane write, no clone needed):

```
S=/fast/scratch/hyaku/kaidoku-r96/ScoutS321
mkdir -p "$S/pack"; cd "$S/pack"
cp /usr/bin/printf ./in && chmod 755 ./in
upx --best -q -o ./packed1 ./in                                  # exit 0
mkdir -p b2 && cp /usr/bin/printf b2/in && chmod 755 b2/in
upx --best -q -o b2/packed2 b2/in                               # exit 0
sha256sum ./packed1 b2/packed2
→ 95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6  ./packed1
→ 95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6  b2/packed2
cmp ./packed1 b2/packed2                                        # exit 0 (identical)
```

Third pack under a **different input filename** (`b3/othername`) → same digest
`95f2beb3…adb6` (exit 0): the packed bytes are independent of the input file name, so the
packed digest is reproducible by any third party with the same packer — see §5.

```
upx -t ./packed1                                                # exit 0
→ testing ./packed1 [OK] / Tested 1 file.
chmod 755 ./packed1
./packed1 --version                                             # exit 0
→ printf (GNU coreutils) 9.12 … Written by David MacKenzie.
./packed1 'hello %s\n' world                                     # exit 0
→ hello world
```

`packed_sha256` = `95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6` — **identical to
the committed receipt's `packed_sha256`** (`.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json`).

## 3. Full independent re-run of the frozen S321 command, and field-by-field cross-check

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-96/fresh-source2-check.py --root . \
  --work /fast/scratch/hyaku/kaidoku-r96/ScoutS321/fs2-work \
  --rev 0ea695e826f2dca53dd55ac0bafead93de26b173 \
  --json-out /fast/scratch/hyaku/kaidoku-r96/ScoutS321/s321-repro.json
# exit 0
→ stdout tail: fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0
```

Field-by-field, my receipt vs the committed one (`pre/s321-fresh-source2-at-base.json`):

| field | my re-run | committed | match |
|---|---|---|---|
| `source` | `/usr/bin/printf` | `/usr/bin/printf` | yes |
| `source_sha256` | `b2265abe…74d7` | `b2265abe…74d7` | yes |
| `packed_sha256` | `95f2beb3…adb6` | `95f2beb3…adb6` | yes |
| `deterministic` | `true` | `true` | yes |
| `collides_public_packed` | `false` | `false` | yes |
| `intact_identity` | `true` | `true` | yes |
| `blocks` | `5` | `5` | yes |
| `counts` | `{near:2, repaired:2, far:2, far_refused:2}` | same | yes |
| `label` | `fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1` | same | yes |
| `met_target` / `exit` | `true` / `0` | `true` / `0` | yes |
| `revision` | `0ea695e8…173` | `0ea695e8…173` | yes |
| `tool` | `tools/round-96/fresh-source2-check.py` | same | yes |
| `cells` | near −7 repaired rc 0; near +7 repaired rc 0; far −40 refused rc 2; far +40 refused rc 2 | same | yes (`cells_equal: True`) |

`cells` are byte-equal (list comparison `True`), including the `tail` refusal strings.

**Public-carrier collision check, done by me from scratch** (the tool's own check packs the five
public carriers; I packed them independently):

```
for c in /usr/bin/jq /usr/bin/xxd /usr/lib/libz.so.1.3.2 /usr/bin/docker-init /usr/bin/xz; do
  cp "$c" "./$(basename $c)"; chmod 755 …; upx --best -q -o "./$(basename $c).packed" …   # all exit 0
done
sha256sum ./*.packed
→ b67ce1bdda27880a3448e25d519bcc7af2ffb073bf2ea2867a1d16dbb9f14bc7  docker-init.packed
→ e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a  jq.packed
→ a9c544e6da4f93418f15b768873f9ce5177d490e8de7f2e0c30a3f8e0065da5b  libz.so.1.3.2.packed
→ 1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff  xxd.packed
→ a7b4d929441c01673bb336d69052bb362faa0a9d10504a30b691ce0fd43a889b  xz.packed
```
None equals `95f2beb3…adb6` → `collides_public_packed: false` re-derived independently.
For contrast, the round-93 arm's source `/usr/bin/env` packs to
`e703277bc092ad8845bd9539d0743266573863b2da1e57884632383d59eb61c5` — a different image, so
printf is a genuine second source at the packed-byte level too.

**Negative control (source-pin drift):**
```
python3 -I -B tools/round-96/fresh-source2-check.py --root . --source-sha 0000…000 \
  --work <scratch> --rev 0ea695e8…173
# exit 2
→ {"exit": 2, "unevaluable": "fresh source sha256 drift", …}
```
The arm fails closed on a pin drift instead of scoring (receipt: `s321-drift-control.stdout`).

**Byte provenance of the committed receipt:**
```
git show e4d1f7de9deae83e6d5f78d2d7f0157196002af0:.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json | sha256sum
→ cf46dbf3e7e25aedea88eaf0e3cfed75c6dcea07ecee0997bd62d82c37c8437c
sha256sum .ufo/waves/round-96/pre/s321-fresh-source2-at-base.json
→ cf46dbf3e7e25aedea88eaf0e3cfed75c6dcea07ecee0997bd62d82c37c8437c   (identical)
git show e4d1f7de9deae83e6d5f78d2d7f0157196002af0:tools/round-96/fresh-source2-check.py | sha256sum
→ 124f71f75548c9c46e6e2fdf88c569c54cd2a3339abcdcbb4dd9561915d008f9
sha256sum tools/round-96/fresh-source2-check.py
→ 124f71f75548c9c46e6e2fdf88c569c54cd2a3339abcdcbb4dd9561915d008f9   (identical)
```
Both match `.ufo/waves/round-96/pins.sha256` (lines 1 and 36).
`sha256sum -c .ufo/waves/round-96/pins.sha256` → **60 files OK, 0 mismatches, exit 0**.

## 4. Independent re-derivation of the four cell classes (bypassing the tool's scoring)

Re-implemented the lane's own layout/repair invocation by hand against my own packed image
(`v2.layout` → 5 blocks, last block at offset `31358`, `sz_cpr=246`, `sz_unc=1364`):

| cell | tampered `sz_cpr` | repair rc | result |
|---|---|---|---|
| near −7 | 239 | 0 | output **byte-identical to the pristine packed image** (35 592 B) |
| near +7 | 253 | 0 | output **byte-identical to the pristine packed image** (35 592 B) |
| far −40 | 206 | 2 | no output; typed refusal `stop-boundary: no green value in the +/-16 window (spots [(31358, 206)])` |
| far +40 | 286 | 2 | no output; typed refusal `stop-boundary: no green value in the +/-16 window (spots [(31358, 286)])` |
| intact | 246 | 0 | output byte-identical to the pristine packed image |

So "repaired 2 of 2" means *the repaired bytes equal the pristine packed bytes*, not merely
"the tool exited 0" — checked at the byte level, independently of `score_cell`.
(Inherited, already-disclosed bound: the far refusal is a consequence of the repair tool's own
`WINDOW = 16` cap around the *tampered* stored value, so the far arm measures the tool's window
cap, not an independent packer property — round-92 named limit 5 / round-93 limit 3.)

## 5. Calibration finding — the S321 arm is table-able (the round-93 arm is not)

`tools/round-96/fresh-source2-check.py` packs the **pristine** source: it contains no nonce and
never calls `mutate_source` (`grep -c mutate_source tools/round-96/fresh-source2-check.py` → `0`).
The round-93 fresh arm does mutate (`tools/round-93/stop-boundary-repair-battery-v3.py:196-198`,
`nonce = secrets.token_hex(8)` → `mutate_source(raw, nonce)`), which is precisely what makes
its packed image un-tableable.

Measured attack — a one-entry pinned-image table forgery (no packer call, no derivation; it
stores the pristine packed bytes of `/usr/bin/printf` and rewrites the tampered 4-byte field back
when it is within ±7, refusing otherwise):

```
python3 -I -B tools/round-96/fresh-source2-check.py --root . \
  --repair-cmd /fast/scratch/hyaku/kaidoku-r96/ScoutS321/attack/table-forgery.py \
  --work <scratch> --rev 0ea695e826f2dca53dd55ac0bafead93de26b173
# exit 0
→ fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0
→ cells: near −7 repaired rc 0; near +7 repaired rc 0; far −40 refused rc 2; far +40 refused rc 2
```

So the S321 arm's frozen label `fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1`
is met by a table over one fixed packed image. This does **not** contradict the frozen claim:
the declaration describes S321 as "pack determinism, no public-carrier collision, near cells
repaired, far cells refused" and states it is "a supplementary measurement: it is NOT part of the
R96-C1 frozen label". But the claim's summary sentence — "Closes the round-93 carried limit 'the
fresh-pack arm has one source'" — must be read narrowly: it closes *the count* of measured
sources (2 instead of 1) for the **repair-capability** question, and it does **not** restore the
round-93 arm's "kills the table class by construction" property for the second source, because
that property came from the nonce and S321 has none. The S321 knowledge entry should state the
nonce asymmetry explicitly and should not claim anti-table for S321.

**The limit line closed** (the round-93 line the claim names):
`corpus/lessons/round-93.md:22` —
> `2. **The fresh-pack oracle has one source** (`/usr/bin/env`, sha `a9ba02dc…d202301`). It kills the five-carrier table class by construction and says nothing about a table over other sources.`

Its two later restatements (same limit, carried):
- `corpus/lessons/round-94.md:71` — "The fresh-pack arm still has one source (`/usr/bin/env`); a derive-by-walk forger is not refuted by it (round-93 limit 1 unchanged)."
- `corpus/lessons/round-95.md:68` — "Unchanged from round 94: the fresh-pack arm has one source (`/usr/bin/env`); PE and Mach-O remain unmeasured."
- `corpus/knowledge/2026-11-05-r93-fresh-pack-oracle.md:135` — "**One source only.** The arm pins `/usr/bin/env` and one nonce. It kills the five-carrier table class by construction and says nothing about a table over other sources."

Note the limit's own second clause ("says nothing about a table over other sources") is exactly
what S321 does *not* settle for the new source — see §5 above.

## 6. Registry / integration state observed (read-only)

- `corpus/SOURCES.md` contains **no** `S321` row (`grep -c S321 corpus/SOURCES.md` → `0`). The
  claim text says the S321 registry row "lands at the round's integration commit", so this is
  open, not a defect — but it is a debt the round must discharge.
- `corpus/lessons/round-96.md` does not exist yet (expected: the R95-VD-2 correction entry lands
  at integration). `corpus/knowledge/` has no round-96 entry yet.
- `SKILL.md` has **no** registry row for any `tools/round-96/*` instrument
  (`grep -n "round-96" SKILL.md` → no hits). The round-93/94/95 instruments have rows (26 lines
  mention `round-9x`); the round-96 instruments do not. This is R95-VD-3's debt, and it now
  covers five more instruments (`stop-boundary-repair-battery-v6.py`, `kill-rule-v2.py`,
  `symlink-probe-v2.py`, `legacy-kill-rule.py`, `fresh-source2-check.py`) plus the before-arm
  drivers (`r95-unbound-at-base.py`, `probe-writer-legs.py`, `gen-forgery-fixtures.py`).
- `HEAD` = `3baac2ef4b9b2830d299125b8184ca06d9e6584d` (the disclosed instrument-supersession
  commit); the S321 receipt and tool are byte-identical between the declaration commit and
  `HEAD`, so the supersession did not touch the S321 arm.

## Files written (lane)

- `.ufo/waves/round-96/w1/ScoutS321.md` (report)
- `.ufo/waves/round-96/w1/ScoutS321/s321-verify.md` (this file)
- `.ufo/waves/round-96/w1/ScoutS321/s321-repro.json` (my independent re-run receipt, exit 0)
- `.ufo/waves/round-96/w1/ScoutS321/s321-repro.stdout` (stdout of the same run)
- `.ufo/waves/round-96/w1/ScoutS321/s321-drift-control.stdout` (pin-drift negative control, exit 2)
- `.ufo/waves/round-96/w1/ScoutS321/packed-printf.sha256` (my packed-image digest line)

Scratch `/fast/scratch/hyaku/kaidoku-r96/ScoutS321` (packs, the table-forgery attack script,
independent cell re-derivations) was deleted before yield. No lane file outside the seat
directory and the report was created, edited or deleted. No mutating git/jj command was run in
the lane (`git rev-parse`, `git status`, `git log`, `git show`, `git ls-tree` only); no clone or
worktree was made — every measurement ran in scratch against the lane repo read-only.
