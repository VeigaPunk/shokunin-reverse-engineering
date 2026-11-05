# ScoutS321 — independent non-author verification of the S321 measurement

Seat: `ScoutS321` (scout). Lane: `kaidoku`, round 96, attempt 1.
Declaration commit read: `e4d1f7de9deae83e6d5f78d2d7f0157196002af0` (base `0ea695e826f2dca53dd55ac0bafead93de26b173`).
Lane READ-ONLY for this seat; lane writes are confined to
`.ufo/waves/round-96/w1/ScoutS321/` plus this report.
Scratch `/fast/scratch/hyaku/kaidoku-r96/ScoutS321` deleted before yield. No tool installed or upgraded.

**Verdict: the S321 measurement reproduces exactly — every field of the committed receipt
re-derives byte-for-byte. One calibration finding the L1 must carry into the S321 knowledge
entry: the S321 arm does not inherit the round-93 fresh arm's anti-table property (it does not
nonce-mutate its source), so a one-entry pinned-image table meets the S321 arm — measured, exit 0,
`met True`. The frozen claim does not assert anti-table for S321 (it calls S321 a supplementary
measurement outside the R96-C1 frozen label), so this is a bound to state, not a kill-rule hit.**

Full detail, tables and every command: `.ufo/waves/round-96/w1/ScoutS321/s321-verify.md`.

## Host measurements

```
sha256sum /usr/bin/printf /usr/bin/env
→ b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7  /usr/bin/printf   (= the claim's digest; = pins.sha256:60)
→ a9ba02dcad338ee7f0b03e58a1cf44009b2bd645b09c2b423242e9791d202301  /usr/bin/env
file /usr/bin/printf  → ELF 64-bit LSB pie executable, x86-64, dynamically linked, BuildID[sha1]=e7eb13c0…, stripped
file /usr/bin/env     → ELF 64-bit LSB pie executable, x86-64, dynamically linked, BuildID[sha1]=0643d200…, stripped
stat -c '%n inode=%i links=%h size=%s' → printf inode=13516862 size=76088 ; env inode=13516828 size=68312 (distinct files)
upx --version (exit 0) → upx 5.2.0 (UCL 1.03, zlib 1.3.1.1-motley, LZMA SDK 4.43)
sha256sum /usr/bin/upx → cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969  (= the lane's UPX_SHA256 pin)
```

## Pack determinism, `upx -t`, execution (scratch only)

```
S=/fast/scratch/hyaku/kaidoku-r96/ScoutS321; mkdir -p "$S/pack"; cd "$S/pack"
cp /usr/bin/printf ./in && chmod 755 ./in ; upx --best -q -o ./packed1 ./in      # exit 0
mkdir -p b2 && cp /usr/bin/printf b2/in && chmod 755 b2/in ; upx --best -q -o b2/packed2 b2/in   # exit 0
sha256sum ./packed1 b2/packed2  → both 95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6
cmp ./packed1 b2/packed2        → exit 0 (identical)
third pack from a differently-named input (b3/othername) → same digest 95f2beb3…adb6 (exit 0)
upx -t ./packed1                → exit 0, "testing ./packed1 [OK] / Tested 1 file."
chmod 755 ./packed1; ./packed1 --version  → exit 0, "printf (GNU coreutils) 9.12 …"
./packed1 'hello %s\n' world              → exit 0, "hello world"
```

`packed_sha256 = 95f2beb3…adb6` — **identical to the committed receipt's `packed_sha256`**.

## Frozen command re-run, field-by-field vs the committed receipt

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-96/fresh-source2-check.py --root . --work <scratch>/fs2-work \
  --rev 0ea695e826f2dca53dd55ac0bafead93de26b173 --json-out <scratch>/s321-repro.json
# exit 0
→ fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0
```

All 13 checked fields match the committed receipt (`pre/s321-fresh-source2-at-base.json`):
`source`, `source_sha256` (`b2265abe…74d7`), `packed_sha256` (`95f2beb3…adb6`), `deterministic`=true,
`collides_public_packed`=false, `intact_identity`=true, `blocks`=5,
`counts`={near 2, repaired 2, far 2, far_refused 2},
`label`=`fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1`, `met_target`=true, `exit`=0,
`revision`, `tool`; and the `cells` list is byte-equal (near −7/+7 repaired rc 0; far −40/+40 refused rc 2,
identical `tail` strings).

**Collision check re-derived independently**: I packed the five public carriers myself
(`/usr/bin/jq`, `/usr/bin/xxd`, `/usr/lib/libz.so.1.3.2`, `/usr/bin/docker-init`, `/usr/bin/xz`; all
exit 0) → `b67ce1bd…`, `e8b6c9e7…`, `a9c544e6…`, `1727faf9…`, `a7b4d929…` — none equals
`95f2beb3…adb6` → `collides_public_packed: false` confirmed. `/usr/bin/env` packs to
`e703277b…61c5`, so printf is a distinct second source at the packed-byte level too.

**Negative control**: `--source-sha 0000…000` → **exit 2**, `{"unevaluable": "fresh source sha256 drift"}`
(fails closed instead of scoring).

**Independent re-derivation of the cells** (hand-built layout + repair invocation, not the tool's
scorer): last block at offset `31358`, `sz_cpr=246`, `sz_unc=1364`. near −7 (239) and +7 (253) → rc 0 with
output **byte-identical to the pristine packed image** (35 592 B); far −40 (206) and +40 (286) → rc 2,
no output, typed refusal `stop-boundary: no green value in the +/-16 window`; intact (246) → rc 0,
byte-identical. So "repaired" means the bytes equal the pristine image, checked at byte level.

**Provenance**: the committed receipt blob at `e4d1f7de` and the worktree file both hash
`cf46dbf3e7e25aedea88eaf0e3cfed75c6dcea07ecee0997bd62d82c37c8437c`; the tool blob at
`e4d1f7de` and worktree both hash `124f71f75548c9c46e6e2fdf88c569c54cd2a3339abcdcbb4dd9561915d008f9`
(both equal to `pins.sha256` lines 36 and 1). `sha256sum -c .ufo/waves/round-96/pins.sha256` →
**60 OK, 0 mismatches, exit 0**. `HEAD` = `3baac2ef…6584d`; the S321 receipt and tool are unchanged
between the declaration commit and HEAD.

## The round-93 limit this closes (verbatim)

`corpus/lessons/round-93.md:22` —
> `2. **The fresh-pack oracle has one source** (`/usr/bin/env`, sha `a9ba02dc…d202301`). It kills the five-carrier table class by construction and says nothing about a table over other sources.`

Restatements (carried forward, unmodified by this round):
- `corpus/lessons/round-94.md:71` — "The fresh-pack arm still has one source (`/usr/bin/env`); a derive-by-walk forger is not refuted by it (round-93 limit 1 unchanged)."
- `corpus/lessons/round-95.md:68` — "Unchanged from round 94: the fresh-pack arm has one source (`/usr/bin/env`); PE and Mach-O remain unmeasured."
- `corpus/knowledge/2026-11-05-r93-fresh-pack-oracle.md:135` — "**One source only.** The arm pins `/usr/bin/env` and one nonce. It kills the five-carrier table class by construction and says nothing about a table over other sources."

## Finding for the L1 (calibration) — the nonce asymmetry

`tools/round-96/fresh-source2-check.py` packs the **pristine** source: no nonce, and
`mutate_source` is never called (`grep -c mutate_source tools/round-96/fresh-source2-check.py` → `0`).
The round-93 fresh arm does mutate (`tools/round-93/stop-boundary-repair-battery-v3.py:196-198`,
`nonce = secrets.token_hex(8)` → `mutate_source(raw, nonce)`) — that mutation is exactly what makes
its packed image un-tableable.

Measured attack — a one-entry pinned-image table forgery (stores the pristine packed bytes of
`/usr/bin/printf`, rewrites the tampered 4-byte field back when it is within ±7, refuses otherwise;
no packer call, no derivation):

```
python3 -I -B tools/round-96/fresh-source2-check.py --root . --repair-cmd <scratch>/attack/table-forgery.py \
  --work <scratch>/fs2-tbl --rev 0ea695e826f2dca53dd55ac0bafead93de26b173
# exit 0
→ fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0
→ cells: near −7 repaired rc 0; near +7 repaired rc 0; far −40 refused rc 2; far +40 refused rc 2
```

Consequence for the wording: the S321 arm raises the count of measured sources (2 instead of 1) for
the **repair-capability** question, but it does **not** restore "kills the table class by construction"
for the second source. The S321 knowledge entry must state the nonce asymmetry and must not claim
anti-table for S321. This is consistent with the declaration's own scoping ("proves source diversity
of the held-out arm, not a new repair capability"; "NOT part of the R96-C1 frozen label") — it is a
bound to state, not a kill-rule violation, and it does not touch the frozen label
`mutants killed 10 of 10; forgeries refused 10 of 10; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1`.

Also inherited and already disclosed: the far refusal is the repair tool's own `WINDOW = 16` cap around
the *tampered* stored value (round-92 named limit 5 / round-93 limit 3), so the far arm measures the
tool's window cap, not an independent packer property.

## Registry / integration state observed (read-only)

- `corpus/SOURCES.md` has **no** `S321` row (`grep -c S321` → 0); the claim says the row lands at the
  integration commit — open debt for this round, not a defect.
- `corpus/lessons/round-96.md` and any round-96 `corpus/knowledge/` entry do not exist yet (expected:
  R95-VD-2's appended correction entry lands at integration).
- `SKILL.md` has **no** registry row for any `tools/round-96/*` instrument (`grep -n "round-96" SKILL.md`
  → no hits; 26 lines mention `round-9x`). R95-VD-3's debt therefore now spans the round-96 instruments
  (`stop-boundary-repair-battery-v6.py`, `kill-rule-v2.py`, `symlink-probe-v2.py`, `legacy-kill-rule.py`,
  `fresh-source2-check.py`) plus the before-arm drivers (`r95-unbound-at-base.py`,
  `probe-writer-legs.py`, `gen-forgery-fixtures.py`).

## Files written

- `.ufo/waves/round-96/w1/ScoutS321.md` (this report)
- `.ufo/waves/round-96/w1/ScoutS321/s321-verify.md` (full detail)
- `.ufo/waves/round-96/w1/ScoutS321/s321-repro.json` (independent re-run receipt, exit 0)
- `.ufo/waves/round-96/w1/ScoutS321/s321-repro.stdout`
- `.ufo/waves/round-96/w1/ScoutS321/s321-drift-control.stdout` (pin-drift control, exit 2)
- `.ufo/waves/round-96/w1/ScoutS321/packed-printf.sha256`

Scratch `/fast/scratch/hyaku/kaidoku-r96/ScoutS321` deleted before yield. No lane file outside the seat
directory and this report was created, edited or deleted; no mutating git/jj command was run in the lane
(`git rev-parse`, `git status`, `git log`, `git show` only); no clone or worktree was made — every
measurement ran in scratch against the lane repo read-only.
