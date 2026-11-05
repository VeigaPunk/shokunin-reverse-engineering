# ScribeLesson — round-89 lesson draft and QUALITY rows (kaidoku)

Seat `ScribeLesson` (scribe, leaf — no subagent dispatch). Lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, round 89, L1 `KaidokuR89`. Base revision
`0ec2bb4016655f605657d6e0e700ec2e6893ac27`. Lane axes: coverage, depth, calibration.

Deliverables in this seat directory:

- `quality-rows.md` — QUALITY rows 161-169 in the file's `- **Row N (title).**` shape, each citing
  the lesson row that produced it.
- `report.md` — this file.
- `.ufo/waves/round-89/w1/ScribeLesson.md` — the seat's wave trailer.

The `## Mistakes` rows and the `## Gate` skeleton are drafted in §2 and §3 below for the L1 to fold
into `corpus/lessons/round-89.md` (the lesson file already exists in the lane's working tree; §2
states which rows are mine and which were already there).

## 1. What I verified myself (every command, with its exit code)

Nothing below is a re-run of a pre-freeze receipt used *as* the receipt; the receipts are cited as
committed evidence, and the commands here are independent re-derivations.

### 1.1 The instrument pins still hold

```
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
$ sha256sum tools/round-89/upx-field-value-repair.py tools/round-89/upx-field-battery.py \
    tools/round-89/depth-blocks-v2.py tools/round-88/upx-chain-repair.py \
    tools/round-88/upx-chain-battery.py tools/round-87/upx-magic-repair.py \
    tools/round-88/depth-blocks.py
```
exit 0. Output sha256, in order:
`332917f2…1070`, `f6f5ed61…b720`, `359f15e1…f18f`, `59ee51b0…0b46`, `a01ed622…7160`,
`96da7d8e…ec24`, `458eeabd…7d5b`. All seven equal the pins in
`.ufo/waves/round-89/claims.json` `instruments`/`pins`.

### 1.2 The three frozen instruments' own selftests

```
$ python3 -I -B tools/round-89/depth-blocks-v2.py --selftest      → SELFTEST cases=10 failures=0   exit 0
$ python3 -I -B tools/round-89/upx-field-value-repair.py --selftest → SELFTEST cases=16 failures=0  exit 0
$ python3 -I -B tools/round-89/upx-field-battery.py --selftest     → SELFTEST cases=9 failures=0   exit 0
```

### 1.3 D3 — the target-blind counter, reproduced in both instruments

```
$ python3 -I -B tools/round-88/depth-blocks.py --root . --rev 0ec2bb40… --json-out …/d3-r88-counter-at-base.json
{"blocks": 28, "met_target": true, "resolved": 28, "revision": "0ec2bb40…", "unresolved": []}
exit 0
```
The round-88 counter — the instrument round 89 superseded — reports `met_target true` and exits 0 at
the round-89 base, where the claim's target is 29 blocks. That is D3 in its exact form, re-measured
on this round's base.

The v2 counter on the same base and the same target is red:

```
$ python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev 0ec2bb40… --expect-blocks 29
blocks 28 resolved 28 expect 29 unresolved 0 met=False exit=1
$ python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev 8bbb40cc… --expect-blocks 29
blocks 29 resolved 29 expect 29 unresolved 0 met=True exit=0
$ python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev HEAD --expect-blocks 29
blocks 29 resolved 29 expect 29 unresolved 0 met=True exit=0
$ python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev HEAD
could-not-evaluate: --expect-blocks N is required (QUALITY 157)      exit 2
$ python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev HEAD --expect-blocks 28
blocks 29 resolved 29 expect 28 unresolved 0 met=False exit=1
```
The last two are the "shown able to fail" arms for D3: the target cannot be omitted (exit 2) and a
wrong target is red (exit 1) even though every block resolves.

### 1.4 D4 — the isolation fix, an A/B against the round-88 battery

I wrote a sibling-copy cheat (`v/cheat-sibling.py`: copy the `packed` sibling of `--in` to `--out`,
no packer probe, no derivation) and ran it under both counters.

Under the **round-89** battery (private directory per invocation):

```
$ python3 -I -B tools/round-89/upx-field-battery.py --root . --repair-cmd …/cheat-sibling.py \
    --upx /usr/bin/upx --work …/w89 --json-out …/cheat-sibling-r89.json --expect-recovered 4 --no-rea
recovered 0 of 4 controls_ok={'N1-refuse-plain': True, 'N2-corrupt-payload': True,
 'N3-intact-idempotent': False, 'isolation': True} met=False exit=1
```
exit 1. The cheat scores 0 of 4: with the input alone in its directory there is no sibling to copy.

Under the **round-88** battery (answer beside the input), the same cheat:

```
$ python3 -I -B tools/round-88/upx-chain-battery.py --root . --repair-cmd …/cheat-sibling.py \
    --upx /usr/bin/upx --pkg <rea> --work …/w88b --json-out …/cheat-sibling-r88-rea.json
recovered 4 of 4 controls_ok={'N1-refuse-plain': False, 'N2-corrupt-payload': False,
 'N3-intact-idempotent': True} met=False exit=1
```
exit 1 (my first cheat is not selective enough and trips the N1/N2 controls), but the *class* arm is
`recovered 4 of 4` with `field_only`, `test_ok` and `identity` all true and
`repaired_equals_packed: true` — the cheat produced the correct answer with zero packer probes.

Round 88's own, selective sibling cheat (`w1/CriticClaims/cheats/sibling-repair-v2.py`, sha256
`ce58a6c4…d4f5`) is the sharper red arm, and it is the one the round-88 lesson cites. Re-run by this
seat under the **round-88** battery:

```
$ python3 -I -B tools/round-88/upx-chain-battery.py --root . \
    --repair-cmd .ufo/waves/round-88/w1/CriticClaims/cheats/sibling-repair-v2.py \
    --upx /usr/bin/upx --pkg <rea> --work …/w88c --json-out …/cheat-r88sibling-v2-mine.json
recovered 4 of 4 controls_ok={'N1-refuse-plain': True, 'N2-corrupt-payload': True,
 'N3-intact-idempotent': True} met=True exit=0
```
exit 0, after 179 s. The receipt reads `met_target: true`, `controls_ok` all true, `recovered 4`,
`exit 0`, `regression met true` (`recovered 8 of 8`) — the round-88 counter cannot tell a
copy-only repair from the real one. That is D4 in its exact form, re-measured first-hand, and it is
the red arm the round-89 battery is supposed to kill.

**The A/B is complete.** The *same* cheat under the **round-89** battery:

```
$ python3 -I -B tools/round-89/upx-field-battery.py --root . \
    --repair-cmd .ufo/waves/round-88/w1/CriticClaims/cheats/sibling-repair-v2.py \
    --upx /usr/bin/upx --pkg <rea> --work …/w89sib --json-out …/cheat-r88sibling-v2-under-r89.json \
    --expect-recovered 4
recovered 0 of 4 controls_ok={'N1-refuse-plain': True, 'N2-corrupt-payload': True,
 'N3-intact-idempotent': True, 'isolation': True} met=False exit=1
```
exit 1, after 147 s. One cheat, two counters: **`met_target true` / exit 0 under the round-88
battery, `recovered 0 of 4` / exit 1 under the round-89 battery.** The D4 fix is measured, not
asserted.

### 1.5 A new finding: the round-89 repair dropped the round-88 guards, and the control that should
have caught it passes on the crash

This is mine, not copied. The round-88 repair's `main()` checked that `--in` is a regular file,
refused a non-regular `--in` with a typed rc 2, and converted the round-87 module's own `Refused`
exception into its own typed refusal. The round-89 repair does none of that:

```
$ python3 -I -B tools/round-89/upx-field-value-repair.py --in fifo --out fifo.out
   (no exit within 5 s; killed; exit 124)
$ python3 -I -B tools/round-88/upx-chain-repair.py --in fifo --out fifo.out2
refused: --in is not a regular file: fifo                                  exit 2
$ (ulimit -v 600000; python3 -I -B tools/round-89/upx-field-value-repair.py --in /dev/zero --out dz2.out)
MemoryError  (traceback at tools/round-89/upx-field-value-repair.py:245, `data = fh.read()`)
$ python3 -I -B tools/round-88/upx-chain-repair.py --in /dev/zero --out dz.out
refused: --in is not a regular file: /dev/zero                             exit 2
$ python3 -I -B tools/round-89/upx-field-value-repair.py --in /usr/bin/jq --out plain.out
r87repair.Refused: no validated PackHeader in the tail window   (traceback, exit 1)
$ python3 -I -B tools/round-88/upx-chain-repair.py --in /usr/bin/jq --out plain2.out
refused: no validated PackHeader in the tail window; no validated PackHeader in the tail window   exit 2
```
The cause is structural, not a slip: `tools/round-89/upx-field-value-repair.py:46` defines its own
`class Refused(Exception)`, and `derive()` at `:65` calls `rep.find_packheader(d)` — which raises
the **round-87** module's `Refused` (`tools/round-87/upx-magic-repair.py:63`). The round-88 repair
converted that upstream exception at `tools/round-88/upx-chain-repair.py:162`
(`except rep.Refused as geo_refusal: raise Refused(...)`); the round-89 repair converts it at `:121`
only around the *anchor* call, so the one inside `derive()` escapes `main()`'s `except Refused`
(the module's own class) and reaches the top as an uncaught traceback.

The control that should have caught this is `N1-refuse-plain`, and it does not, because the battery
asserts `n1["rc"] != 0` (`tools/round-89/upx-field-battery.py:287`), so a crash counts as a
refusal. The two pre-freeze receipts show the divergence directly:

```
$ python3 -c "…pre/c1-candidate-at-declaration.json…['N1-refuse-plain']"
[{"carrier": "jq", "rc": 1, "refused": true}, … ]     # the round-89 repair: rc 1 = crash
$ python3 -c "…pre/c1-base-r88-repair.json…['N1-refuse-plain']"
[{"carrier": "jq", "rc": 2, "refused": true}, … ]     # the round-88 repair: rc 2 = typed refusal
```
Both receipts report `N1-refuse-plain: true`. One is a refusal, the other is a traceback, and the
counter cannot tell them apart.

### 1.6 A new finding: the `isolation` control observes a snapshot, not the invocation

This is mine; the receipt that prompted it is copied (named below).

`tools/round-89/upx-field-battery.py:180` takes `before = sorted(os.listdir(box))` **before** the
child process starts, and `:197` records that pre-run snapshot as the invocation's `box`. The
control therefore certifies what the harness prepared, not what the repair saw or wrote. A repair
that reads the pinned carrier out of band and writes a marker into its own invocation directory
during the run is invisible to it.

ReviewerC1's carrier-read cheat is such a repair. I ran their script **verbatim** under the
round-89 battery:

```
$ python3 -I -B tools/round-89/upx-field-battery.py --root . \
    --repair-cmd /fast/scratch/hyaku/kaidoku-r89/ReviewerC1/attacks/cheat-carrier-read.py \
    --upx /usr/bin/upx --pkg <rea> --work …/wcr3 --json-out …/cheat-carrier-read-r1c1-mine.json \
    --expect-recovered 4
recovered 4 of 4 controls_ok={'N1-refuse-plain': True, 'N2-corrupt-payload': True,
 'N3-intact-idempotent': True, 'isolation': True} met=True exit=0
```
exit 0, after 244 s. `met_target true`. The cheat opens and sha256-hashes `/usr/bin/jq` on every
invocation and writes `carrier-read.marker` into the invocation box. I confirmed the marker
appeared in the cheat's own marker directory. This matches ReviewerC1's own receipt
`.ufo/waves/round-89/w1/ReviewerC1/receipts/attack-carrier-read.json` (`met_target: true`,
`exit: 0`) — the difference is that I re-ran it, so the finding is re-measured rather than copied.

This also means the round-89 kill-rule clause "a repair that names, reads or hashes a carrier
source path or pin" — which round 88's D4 already called "audit-only — no machine check exists" —
is still audit-only, and the round-89 counter's own `isolation` control does not close it.

### 1.7 A new finding: the `u_len` accounting bound is a rank key, not a filter

`tools/round-89/upx-field-value-repair.py:95` computes
`key = (total <= ph["u_len"], total, -derived)`. An over-`u_len` candidate is therefore *ranked
last*, not rejected — and when **every** candidate is over the bound, one is still returned. The
round-88 predecessor is the same shape (`tools/round-88/upx-chain-repair.py:132-136`).

I proved this on a scratch copy of the frozen repair (`v/probe-ulen.py`, a copy with `ph["u_len"]`
forced to 1 so that no candidate can fit; the frozen file itself was not touched):

```
$ python3 -I -B probe-ulen.py --in tampered.bin --out ulen.out --info ulen.json
field-value: stored 244 -> derived 252 at block0 576        exit 0
   info: u_len = 1, uncompressed_accounted = 30800, fits_u_len = False,
         derived_sz_cpr = 252, class = field-value
$ sha256sum ulen.out packed tampered.bin
e8b6c9e7…268a  ulen.out      # == the intact packed carrier
e8b6c9e7…268a  packed
ce77cddc…dde   tampered.bin
```
The repair wrote a value while its own receipt reported `fits_u_len: False` — every candidate
violated the bound the law calls "impossible". The bound is real (it decides between candidates on
docker-init) but it is a preference, and the receipt does not record that the *chosen* candidate
violated it. `rec` carries `uncompressed_accounted`/`u_len`/`fits_u_len` for the winner only
(`:97-99`), so the over-bound status is visible but never acted on.

### 1.8 Sources census (the lane's own gate)

```
$ cd /home/vgpnk/Projects/shokunin
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
… 29 W04 duplicate-URL warnings (all pre-existing rows, plus one new: S311 vs S307,
    the same p_lx_elf.cpp URL at a different scope)
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
exit 0
```
Row count in the working tree: 217 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`),
against 215 in `pre/sources-census-before.txt` — the two new rows are S311 and S312, both in the
working tree and **not yet committed** (`git show HEAD:corpus/SOURCES.md | grep -c S311` → 0).

### 1.9 The `## Gate` rows exist and are consistent with the registry

S311 and S312 are in the working-tree `corpus/SOURCES.md` with their URLs, byte counts and sha256
prefixes, and the working-tree `corpus/knowledge/2026-11-04-r89-binfo-field-value-class.md` cites
both. I did **not** open these URLs myself — no fetch was made from this seat — so the access date
and the located quote in the lesson's `## Gate` must come from the L1's own fetch record and from
ScoutUpxSrc's independent fetch, not from me. See §3.

## 2. `## Mistakes` rows — draft

The QUALITY rows this seat proposes (161-169) each cite a lesson row: 161←M89-1, 162←M89-2,
163←M89-4, 164←M89-6, 165←M89-7, 166←M89-8, 167←M89-9, 168←M89-10, 169←M89-11. Rows 161-165 are
the lane's existing worktree rows reproduced verbatim with the lesson citation appended (the only
text added); 166-169 are this seat's new rows. No row is proposed for M89-3 (its criterion is the
existing QUALITY 157) or M89-5 (a registry row, not a bar).

Rows **M89-1 … M89-7 already exist** in the lane's working-tree `corpus/lessons/round-89.md`
(mtime 2026-11-04 21:44:54, untracked at base). They were authored by the L1's integration pass,
not by this seat. They cover: M89-1 the composition regression arm, M89-2 the D1 docstring, M89-3
the D3 target-blind counter, M89-4 the D4 answer-beside-input, M89-5 the missing registry rows,
M89-6 the refusal string as a class key, M89-7 tolerated-vs-noop. This seat did not author them and
does not claim them.

**What this seat adds** are the three rows below, all from §1.5-1.7 above. They are new ids (M89-8,
M89-9, M89-10) continuing the existing sequence; the L1 should renumber if it prefers.

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M89-8 | a superseding repair that dropped the predecessor's input guards and refusal contract, and a refusal control that cannot tell a refusal from a crash: the round-89 repair reads `--in` with an unbounded `fh.read()` (no regular-file check, no size cap) and does not convert the round-87 module's `Refused` into its own, so a plain original, a FIFO, `/dev/zero` and a missing output directory all end in a traceback (rc 1) or a hang instead of a typed rc 2; the round-88 repair refused all four with typed rc 2 | §1.5 of `w1/ScribeLesson/report.md` (six commands, exits 124/2/1/2/1/2) and `tools/round-89/upx-field-value-repair.py:46,65,121,243-252` against `tools/round-88/upx-chain-repair.py:162,243-256`; the divergence is visible in the two pre-freeze receipts' `N1-refuse-plain` arms (`rc 1` in `pre/c1-candidate-at-declaration.json`, `rc 2` in `pre/c1-base-r88-repair.json`), both reported `refused: true` | none — the round-89 counter's `N1-refuse-plain` asserts `rc != 0` (`tools/round-89/upx-field-battery.py:287`), so the crash satisfies it; QUALITY 166 is written from this finding this round | not repaired this round: the instrument is frozen and the claim is judged on it. Routed: the repair's next revision restores the regular-file and size guards, converts the upstream `Refused` (catch the upstream class, or expose one refusal type), and the counter's refusal control asserts the declared exit code and the refusal text, not merely "non-zero". Shown able to fail: the two receipts' `N1` arms are already red under that assertion (`rc 1` ≠ the declared `rc 2`) |
| M89-9 | an isolation control that observes a pre-run snapshot instead of the invocation: the counter lists the repair's directory *before* the child starts, so a repair that reads the pinned carrier out of band and writes into its own box during the run is invisible to it, and scores the target with every control true | `tools/round-89/upx-field-battery.py:180` (`before = sorted(os.listdir(box))`) and `:197` (that snapshot recorded as `box`); §1.6 of `w1/ScribeLesson/report.md` — ReviewerC1's `cheat-carrier-read.py` re-run verbatim by this seat scores `recovered 4 of 4`, `controls_ok` all true, `met_target true`, exit 0 (244 s) | none — the pre-existing bar (QUALITY 163) requires the *listing* but not that it be taken after the run; QUALITY 167 is written from this finding this round | not repaired this round (frozen counter). Routed: take the listing after the child exits, and check the paths the child opened (or forbid any read outside `--in`) so the carrier-read clause in the kill rule becomes machine-checked rather than audit-only. Shown able to fail: the re-run above is the red arm |
| M89-10 | a bound stated as a filter implemented as a preference: the chain law's `u_len` accounting bound is the sort key `(total <= u_len, total, -derived)`, so an over-`u_len` candidate is outranked, not rejected, and when every candidate is over the bound the repair still writes a value — with `fits_u_len: False` in its own receipt | `tools/round-89/upx-field-value-repair.py:95` (the key) against `:97-99`; §1.7 of `w1/ScribeLesson/report.md` — a scratch copy with `u_len` forced to 1 exits 0, reports `fits_u_len = False` and `uncompressed_accounted = 30800`, and writes the correct output | none — no criterion distinguishes a bound from a preference; QUALITY 168 is written from this finding this round | not repaired this round (frozen repair). Routed: state in the law whether an over-`u_len` candidate is discarded or merely outranked, and have the receipt carry the candidates' `total`/`u_len`/`fits_u_len` for every candidate, not only the winner. Shown able to fail: the probe above is the red arm |

A fourth row is drafted from a wave finding this seat verified from the receipts but did not
re-measure (named in §4): **M89-11**, the refusal string is not a class key *and the exit code is
not a recovery signal* — the same tamper class answers `header corrupted` on jq/xxd/dinit and
`corrupt b_info` on libz, and `b0.method^=0xFF` / `p_info.p_blocksize^=0xFF` exit 0 with class
`intact` on files `upx -t` still refuses. The lane's existing M89-6 covers the first half; the
second half (rc 0 is not recovery) is new and lands as QUALITY 169.

## 3. `## Gate` — skeleton, filled from ScoutUpxSrc's independent fetch

The lesson's `## Gate` section must carry the sources opened this round. The lane's working-tree
`corpus/lessons/round-89.md` already contains a `## Gate` section with S311/S312 rows and two
rejections; those rows are the L1's. **This seat opened no URL** and contributes no access date
and no quote of its own — the rows below are transcribed from **ScoutUpxSrc's** fetch receipts
(`w1/ScoutUpxSrc/receipts/fetch-sha256.tsv` and `fetch-receipts.json`, and §2 of
`w1/ScoutUpxSrc/report.md`), which landed after this seat's own pass. Where the lane's registry
row and ScoutUpxSrc's line numbers disagree, the disagreement is recorded rather than smoothed
over (see the note under the table).

| source | decision | opened (ScoutUpxSrc's fetch) | located quote and judgment |
|---|---|---|---|
| S311 — UPX v5.2.0 `src/p_lx_elf.cpp`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp | admit (code, tier A; same URL as S307, different scope → census W04) | HTTP 200, 373743 bytes, sha256 `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` | `p_lx_elf.cpp:7810-7812` (`PackLinuxElf64::unpack`, opens 7755): "if (ph.c_len > file_size_u \|\| ph.c_len == 0 \|\| ph.u_len == 0 \|\| ph.u_len > orig_file_size) throwCantUnpack(\"b_info corrupted\");" — the block-0 bound, read from `bhdr.sz_unc`/`bhdr.sz_cpr` at 7807-7808. Also 7104-7106 and 7307-7309: "if (sz_block1 < sz_elf_hdrs) { throwCantUnpack(\"corrupt b_info\");" (the shlib variant). 8060-8066: the EOF sentinel `sz_unc == 0` with `sz_cpr` carrying `UPX_MAGIC_LE32` |
| S312 — UPX v5.2.0 `src/p_unix.h`, https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.h | admit (code, tier A, absent → mined) | HTTP 200, 6651 bytes, sha256 `73bd992ec0fb46022e299ec4b2cd696545412453a654573e6246034cf4881a88` | `p_unix.h:109-111` (`packed_struct(b_info)`, base `PackUnix`): "NE32 sz_unc;  // uncompressed_size / NE32 sz_cpr;  //   compressed_size" — the field *meanings*. `p_unix.h:126-130` (`packed_struct(p_info)`): "NE32 p_progid; / NE32 p_filesize; / NE32 p_blocksize;" |
| UPX v5.2.0 `src/headers.h` | **reject** (no row; round-88 rejection stands) | HTTP 404, 14 bytes, sha256 `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` (body is the literal `404: Not Found`) | the path does not exist at tag `v5.2.0`; the v5.2.0 tree lists exactly one `*headers.h*` path, `src/util/system_headers.h`. Flip: the file appears at a later tag the lane pins |
| UPX v5.2.0 `src/p_unix.cpp` (re-opened) | **reject as a `b_info` primary — unchanged** (r87's rejection stands for the base unpacker) | HTTP 200, 24181 bytes, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | its `corrupt b_info` checks live in `PackUnix::unpackExtent` (490-497), the shared block walk, not in `PackUnix::unpack`; the carriers unpack through `PackLinuxElf64::unpack` (S311). ScoutUpxSrc recommends a *new* row for `p_unix.cpp` scoped to the per-block walk bounds — the L1's call, and the URL is not currently in the registry |

**Sourced claim.** R89-C1's knowledge entry cites S311 and S312, both opened this round.

**Assimilation: none** — `merge/kaidoku/` was not consumed this round; no package entry was opened.

**Note on a scope disagreement between the lane's registry rows and the scout's reading** (recorded,
not smoothed): ScoutUpxSrc's §3 says `src/packhead.h` contains **no** `b_info` at all
(`grep -c b_info packhead.h` → 0) and that the NE32 `p_info` copy at `p_unix.h:126-130` — not the
LE32 copy at 200-204 — is the one the carriers instantiate, because
`PackLinuxElf64Le : PackLinuxElf64 : PackLinuxElf : PackUnix`. The lane's working-tree S312 row
anchors the LE32 copy at lines 200-203, and the working-tree knowledge entry cites S312 for "why
the locator finds `u_file_size` twelve bytes after `l_magic`" — a proposition the NE32 copy, not
the LE32 one, is in force for. The L1 should scope S312 to the NE32 copy or add the distinct-scope
token the census validator requires; the URL and the sha256 are right either way, and the census
passes (exit 0). This is a **scope** observation, not a byte-level dispute: the fetched sha256
`73bd992e…` matches ScoutUpxSrc's independently fetched sha256 exactly.

**No source was opened by this seat.** The rows above are ScoutUpxSrc's fetch record, quoted with
attribution; this seat contributes no access date and no quote of its own.

## 4. Copied material — seat attribution

| material | seat | what this seat did with it |
|---|---|---|
| `w1/ReviewerC1/receipts/attack-carrier-read.json` (`met_target true`, `exit 0`) | ReviewerC1 | **re-run by this seat** (§1.6): their `cheat-carrier-read.py` re-run verbatim under the round-89 battery, exit 0, `met=True`. The finding is re-measured; the receipt is the origin |
| `w1/ReviewerC1/receipts/attack-{sibling,oracle-full,selfmutate,arith,field-flip,plus8}.json` | ReviewerC1 | read only, for the wave section. `attack-oracle-full` and `attack-selfmutate` score `recovered 4 of 4` on the class but `met_target false` (the round-88 regression arm catches them); `attack-sibling` scores 0 of 4 — the isolation fix kills it; `attack-arith` and `attack-field-flip` are caught by the `identity`/`field_only` arms |
| `w1/ReviewerC2/receipts/*` (10 files) and `w1/ReviewerC2.md` | ReviewerC2 | read only. Their independent re-derivation reproduces `pre/c2-depth-at-base.json` field-for-field; their red worlds (citation-only stub, one-span block, range past EOF, a doc created this round under `--rev`) are all exit 1. Their two MED notes are the L1's to action |
| `w1/ExecMatrix/matrix.json` + `report.md` (48 cells, 4 carriers × 12 classes) | ExecMatrix | read only. Source of M89-11: `b0.sz_cpr:=sz_unc+1` → `header corrupted` on jq/xxd/dinit, `corrupt b_info` on libz; `b0.method^=0xFF` and `p_info.p_blocksize^=0xFF` → repair rc 0 with `repaired_tests_clean false` |
| `w1/ExecRegress88/r88-chain-regression.json` | ExecRegress88 | read only. The round-88 counter with the round-89 repair: `recovered 4 of 4`, regression arm `recovered 8 of 8`, `met_target true`, exit 0 |
| `w1/ExecGeomIndep/receipts/*` (48 files) | ExecGeomIndep | read only (the seat's own two scripts were removed from the wave dir during its scratch cleanup before I read them) |
| `w1/ScoutUpxSrc/report.md` + `receipts/fetch-sha256.tsv` + `receipts/fetch-receipts.json` | ScoutUpxSrc | **copied, with attribution** — the §3 Gate rows are transcribed from the scout's own fetch receipts (HTTP status, byte count, sha256, line numbers, quotes). This seat opened no URL and contributes no date or quote of its own. The scout's §3 scope observation about `packhead.h` containing no `b_info` and about the NE32 vs LE32 `p_info` copy is recorded as a disagreement for the L1 (§3 note) |
| `w1/ConnectorR89.md`, `w1/ConnectorR89/report.md`, `w1/ConnectorR89/links.md` | ConnectorR89 | read only, for the wave section |
| `w1/ScribeBlock29.md`, `w1/ScribeBlock29/report.md`, `w1/ScribeBlock29/block29.md` | ScribeBlock29 | read only, for the wave section |
| `w1/SentinelR89/report.md` | SentinelR89 | read only. Its `hostile-inputs.json` is the origin of the T12 case this seat re-measured (§4) |
| `w1/SentinelR89/receipts/hostile-inputs.json` (17 cases) | SentinelR89 | read only. Its T12 (`rc 0`, pre-planted `<out>.tmp` symlink redirected the write onto `victim.bin`) and T2/T6b (uncaught `r87repair.Refused`) reproduce the same defects this seat found independently in §1.5 — **this seat re-measured them** on the frozen repair rather than citing the receipt. T12 was also re-run by this seat: planting `out.tmp.tmp -> victim.bin` and passing `--out out.tmp` makes the repair write the ELF bytes into `victim.bin` (exit 0, `out.tmp` still a symlink) |
| `w1/ReviewerC2.md` "declared evidence `w1/ExecMatrix/matrix.json` does not exist yet" | ReviewerC2 | stale as of this seat's read: the file exists (68,246 bytes, mtime 21:50). The L1 should re-check that note |
| `pre/c1-*.json`, `pre/c2-*.json`, `pre/sources-census-before.txt`, `pre/c1-candidate-first-run.log` | L1 (pre-freeze) | read, not re-run as evidence. §1.5 cites two of their `N1` arms as committed evidence of the exit-code divergence |
| `corpus/lessons/round-89.md` `## Mistakes` M89-1…M89-7 and `corpus/QUALITY.md` rows 161-165 | L1 (integration pass, working tree) | read and reproduced verbatim in `quality-rows.md`; not authored by this seat |

## 5. Wave findings I could verify from the receipts in `w1/` (item 2d)

1. **The round-89 counter does not close round 88's carrier-read kill-rule clause.** Re-measured
   by this seat: exit 0, `met_target true` (§1.6).
2. **The round-89 repair regressed the round-88 guards.** Re-measured by this seat (§1.5).
3. **The `u_len` bound is a preference, not a filter.** Re-measured by this seat on a scratch copy
   (§1.7).
4. **A refusal string varies by carrier within one class; `rc 0` is not recovery.** From ExecMatrix's
   48-cell matrix (§4).
5. **The isolation fix works.** This seat's own A/B (§1.4): the sibling cheat scores 0 of 4 under
   the round-89 battery and 4 of 4 on the class under the round-88 battery.
6. **The D3 fix works and is falsifiable.** §1.3.

## 6. Gaps I could not close

- I did **not** open S311/S312; the lesson's `## Gate` needs the L1's fetch record and
  ScoutUpxSrc's independent fetch. §3 is a skeleton on purpose.
- I did not re-measure ExecMatrix's 48 cells or ReviewerC2's ten worlds myself; I read their
  receipts and quoted them with attribution. The one exception is M89-11, whose two facts I
  confirmed by direct grep over `w1/ExecMatrix/matrix.json` (the per-carrier `upx_t` tail strings)
  but did not re-run the matrix.
- `w1/ExecGeomIndep`'s two scripts were removed from the wave directory before I read them; only
  its 48 receipts remain, so I can cite its results but not its method.
- I did not evaluate the round-89 claim's `met_target` end to end with REA enabled and the real
  repair; that is the L1's landing run, and §1.5/§1.6 deliberately used cheats instead.

## 7. Tooling

No tool was installed or upgraded. The operator's tooling directive
(`/home/vgpnk/.omp/agent/RULES.md`, read this round) permits installing helpers; none was needed —
every command here used `python3` (3.14.8), `coreutils`, and the lane's own instruments. `pacman`
was untouched, per the host-wide pause; nothing was written to `~/.local/bin` or any PATH
directory.

## 8. Post-measurement drift in the frozen repair — a blocker for the L1

**Measured after all of §1, at 22:09:10, by the L1 and not by this seat:**
`tools/round-89/upx-field-value-repair.py` changed in the working tree, sha256
`332917f2…1070` → `664b973a3fb129f5920a4f583fee3810183f54a082841c77ba67039332285c37`
(`git diff --stat`: 77 insertions, 6 deletions). The diff's own comments name this seat's
finding — "round-89 wave finding M89-8" — so the L1 acted on §1.5.

**Every measurement in §1 was taken before 22:09:10** and therefore ran against the **pinned**
bytes `332917f2…1070`: the carrier-read run (244.23 s, ended ~22:03), the round-88 sibling run
(178.98 s) and the round-89 sibling run (146.56 s) all finished before the mtime; the
`u_len` probe was run on a copy made before it. The two counters
(`f6f5ed61…`, `359f15e1…`) and the three round-87/round-88 instruments are **unchanged** — all
seven pins still verify except the repair.

**Re-test of §1.5 against the new bytes** (`664b973a`):

| input | pinned bytes `332917f2` | new bytes `664b973a` |
|---|---|---|
| plain original `/usr/bin/jq` | `r87repair.Refused` traceback, exit 1 | `refused: upstream refusal: no validated PackHeader in the tail window`, **exit 2** |
| FIFO | no exit within 5 s (exit 124) | `refused: --in is not a regular file: f1`, **exit 2** |
| `/dev/zero` | `MemoryError` traceback | `refused: not a regular file: /dev/zero`, **exit 2** |

**M89-8 is fixed in the new bytes.** §1.5 stands as a finding against the *pinned* instrument.

**Two things the new bytes do not fix, re-measured against `664b973a`:**

- **M89-9 (isolation pre-run snapshot) — unchanged.** The counter's `apply_repair` still takes
  `before = sorted(os.listdir(box))` before the child starts and records that snapshot
  (`tools/round-89/upx-field-battery.py:180,197`), and the counter's sha256 is unchanged
  (`f6f5ed61…`). The carrier-read cheat's out-of-band read and in-run marker write remain
  invisible to the control. **This is a live gap in the counter the claim is judged on.**
- **M89-10 (`u_len` bound) — documented, not changed.** The new docstring states the behaviour
  explicitly ("`fits_u_len` is a *rank key, not a filter*: when no candidate fits, the best
  non-fitting one is taken…"). Re-measured on a copy of the new bytes with `u_len` forced to 1:
  exit 0, `fits_u_len = False`, `uncompressed_accounted = 30800`, `derived_sz_cpr = 252` — the
  repair still writes a value when no candidate satisfies the bound. That is now a *disclosed*
  choice rather than an undocumented one, which is a legitimate resolution of the wording; the
  receipt still does not make the over-bound status of the chosen candidate visible to a reader.

**Blocker for the L1.** The claim's kill rule reads "a receipt whose `repair_sha256` differs from
the frozen pin" and the container still pins `332917f2…1070`
(`.ufo/waves/round-89/claims.json` `instruments`), but the file on disk is now `664b973a…`. The
container's `instrument_supersessions` currently records only the `depth-blocks-v2.py` supersession
(with `"commit": "pending"`). Until a supersession row for the repair is added to the container
and the pin is re-taken, **any receipt this round produces names a `repair_sha256` that differs
from the frozen pin** — which is the claim's own kill condition. The L1 must either record the
supersession (with the re-taken before record) or restore the pinned bytes. This seat did not
touch the container, the instrument, or any lane file.

**Update, 22:10:39 — the L1 committed the revision** (`7edab6ae5`, "round-89: repair revision
(typed refusals, input guards) with its supersession entry and re-taken receipts"; 5 files, +115/−28).
The container now carries an `instrument_supersessions` row for
`tools/round-89/upx-field-value-repair.py` with `superseding_sha256 = 664b973a…c37`, a `reason`
naming the three defects, and `retaken_before` pointing at
`.ufo/waves/round-89/pre/c1-candidate-at-declaration.json` at `repair_sha256 664b973a`. The
re-taken receipts carry `repair_sha256 = 664b973a…`, `met_target true`, exit 0.

**One residual inconsistency for the L1 to close** (measured, not repaired by this seat):
the container's `instruments` map still pins the *superseded* hash
`"tools/round-89/upx-field-value-repair.py": "332917f2…1070"`, while the file on disk and every
re-taken receipt carry `664b973a…`. The kill rule says "a receipt whose `repair_sha256` differs
from the frozen pin" — read against the `instruments` pin, **every receipt of the round now
differs from it**, which is the claim's own kill condition, even though the supersession row
documents the change and names the new hash. The fix is one line in the container: point the
`instruments` pin at `664b973a…` (or amend the kill rule to read the supersession's
`superseding_sha256` when one exists), and fill the two `"commit": "pending"` fields with
`7edab6ae5`. The `depth-blocks-v2.py` supersession row has the same unfilled `"commit": "pending"`.
This seat did not edit `claims.json` — the file is out of this seat's write scope.

## 9. Scratch and hygiene

- Scratch: `/fast/scratch/hyaku/kaidoku-r89/ScribeLesson/` — created with `mkdir -p`, held the
  probes (`v/`), the receipts named above, and the two `w*` battery work dirs. **Deleted before
  this report was finalised**; the receipts cited here are copied into this seat directory and the
  cited lane/wave paths.
- No git or jj mutation anywhere: only `log`, `status`, `show`, `diff`, `rev-parse`, `cat-file`,
  `ls-files`. No `git add/commit/stash/checkout/switch/reset/pull/push`, no `jj` command.
- Written by this seat, and only these: `.ufo/waves/round-89/w1/ScribeLesson/quality-rows.md`,
  `.ufo/waves/round-89/w1/ScribeLesson/report.md`, `.ufo/waves/round-89/w1/ScribeLesson.md`, and
  the scratch tree above (deleted). The lane's `corpus/lessons/round-89.md`, `corpus/QUALITY.md`,
  `SKILL.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` and
  `.ufo/waves/round-89/claims.json` were **not** modified by this seat.
