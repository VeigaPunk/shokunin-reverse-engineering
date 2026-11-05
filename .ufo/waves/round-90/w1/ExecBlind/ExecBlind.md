# ExecBlind — R90-C1 carrier-blind arm, empirical attack (round 90, kaidoku)

Seat: `ExecBlind` (executor, leaf), lane `kaidoku-shokunin`, round 90, wave r90-w1.
Assignment: attack the counter's carrier-blind arm (QUALITY 168/170) empirically
inside the counter's own `bwrap` sandbox shape, and answer two questions: (1) can
a repair that only reads its `--in` still be scored `recovered`; (2) does the
`isolation` listing (taken after the child exits) catch a sibling write.

**No tools installed or upgraded this session** (host already had the pinned
packer and bubbelwrap at the pinned versions; nothing routed through
pacman/uv/npm). Verified pins: `/usr/bin/upx` sha256
`cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969` = the
`UPX_SHA256_PIN`, version string `upx 5.2.0` (first line of `upx --version`);
carrier source shas match `CARRIERS` exactly (`sha256sum /usr/bin/jq
/usr/bin/xxd /usr/bin/docker-init /usr/lib/libz.so.1.3.2` → the four pin values
in `claims.json`); `tools/round-90/upx-break-repair.py` sha256
`aaf3536ea2226ac8ec498603d50b7b1b4a57c5572c7edef4fcf0e2a91d35590b` and
`tools/round-90/control-cheat-repack.py` sha256
`faafc982ca5c7fcf2e787a8f78f81c5eb687c74998d2552ddd8935d01759b826` match the
declared instrument pins; `bwrap --version` → `bubblewrap 0.13.1`; uid 1000.

## Sandbox shape (replicated, not asserted)

Mirror of `tools/round-90/upx-later-block-battery.py` `score()` (audited lines:
`boxes = mkdtemp("r90-boxes-", work)` with the comment `# outside run_root`,
line 265; blind argv built exactly as `invoke()` lines 181–186:
`["bwrap","--dev-bind","/","/","--tmpfs",<run_root>] + ["--bind",<decoy>,<p> for
p in realpaths] + ["--",sys.executable,"-I","-B",cmd,"--in",src,"--out",dst]`).
My driver (`receipts/driver.py`) rebuilds the live loop's leftover state with the
same prefixes and code paths (`mkdtemp("inv-", boxes)`, `cand-*` via the same
`tempfile` roles): the counter leaves these in `boxes` before the blind arm
runs, byte-for-byte what my leftovers are — per carrier one `inv-*/in`=intact
`out`=intact (N3), one plain-input N1 box, one corrupt N2 box, P2/P3 tamper
boxes, and for every P1 cell an `inv-*` box plus `cand-<id><delta>` (the live
run's `mkstemp(prefix="cand-", dir=boxes)` output = the intact packed bytes) and
`cand-<id><delta>-nw` (the round-89 no-work leftover = the tampered bytes).
Leftovers totalled 59 entries in `boxes` (receipts
`harness-summary.json` → `isolation.boxes_listing_sample`).

Packed carriers (all `upx --best -q`, env `HOME`/`TMPDIR` under `run_root`, the
counter's `child_env`): jq len 14036 `e8b6c9e7…5268a`, xxd len 19560
`1727faf1…8e9ff`, libz len 65580 `a9c544e6…5da5b`, dinit len 357784
`b67ce1bd…14bc7`; original pins = the pre-declared carrier shas. Precondition
for the repack route measured first: `upx --best` is **byte-deterministic** —
two independent packs of `/usr/bin/jq` both hashed `e8b6c9e7…5268a`, equal to
the `run_root` pack (`harness-summary.json` → `determinism.deterministic: true`,
`pack_a_sha256` = `pack_b_sha256` = `jq.packed_sha256`). P1 first-segment block
geometry (from `layout()`): jq block@840 stored 1651 → 1644/1658; xxd block@837
stored 950 → 943/957; dinit block@814 stored 202 → 195/209. Blind mounts
(all four realpath'd sources decoy-bound, as `blind_paths` at
`harness-summary.json`): `/usr/bin/jq`, `/usr/bin/tinyxxd` (`/usr/bin/xxd` is a
symlink; the counter's realpath comment holds), `/usr/lib/libz.so.1.3.2`,
`/usr/bin/docker-init`.

## Answers to the two assigned questions

**Q1 — yes, and there is no impairment for the honest path.** The pinned lane
repair (`upx-break-repair.py`, sha pin above) run blinded on the jq −7 cell in
the counter's exact sandbox shape: rc 0, `field_only` true, `identity` true,
`upx -t -q` rc 0, `upx -d` rc 0 with sha256 == the original pin
`e815667…f7806` (“unpack_pin”) — all five consumed arms true → `recovered: true`
(`receipts/harness-summary.json` → cell `honest-jq-m7`; probe findings
`receipts/probe-findings-honest-jq-m7.json` show only the `R1` blind mount +
`R2` tmpfs-empty routes fired — the repair only ever touched `--in`).

**Q2 — no for sibling writes; own-box leftovers are the only thing it sees.**
The scored child (cheat mode) wrote `canary-sibwrite` into a sibling `inv-*` box
and a `cand-probe-scan` dump into `boxes`; the counter's own verdict code path
(`invoke()` line 245 `after = sorted(os.listdir(box))` taken after the child
exits, ok-check `sorted(after) in (["in"], ["in","out"])` at lines 341–343) read
the child's **own** box → `['in', 'out']` → `isolation_ok: true` for both cheat
cells, and `sibling_write_caught_by_box_after: false`
(`harness-summary.json`). The canary file provocatively exists
(`cheat_canary_sibling_exists: true`, `probe_dump_exists: true`).
Contrast cell (`ownbox-jq-p7`): the same probe writing `canary-ownbox` inside
its **own** box → `box_after ['canary-ownbox','in','out']` →
`isolation_ok: false` (`ownbox_write_caught_by_box_after: true`). The
about-to-exit listing per QUALITY 170 observes the invocation's own directory
only; anything the child does to a sibling directory is invisible to it.

## Route-by-route results (two cheat cells: jq −7, dinit +7; probe `receipts/probe_cheat.py`)

| Route | What the blind child observed | Intact packed bytes obtained? |
|---|---|---|
| R1 pinned paths | `/usr/bin/jq`, `/usr/bin/xxd`, `/usr/bin/tinyxxd`, `/usr/lib/libz.so.1.3.2`, `/usr/bin/docker-init` each hash `367675832d0a33eaddbd91a66f3286007842f5270b72e05ead8588d9b31b936e` (len 1280), byte-equal to the decoy (`equals_decoy: true` ×5) | **No** |
| R2 run root | `run_root` listing `[]` (tmpfs), `run_root/jq/packed` → `FileNotFoundError`; but the **work dir** sibling listing is visible (`r90-battery-ew1_30i2`, `r90-boxes-rislbavm`…) and `boxes` is fully traversable | run root: **No**; sibling `boxes`: **Yes** |
| R3 neighbours (winner) | 64 blobs seen, 17 length-matched; chosen `cand-jq-7` sha `e8b6c9e7…5268a` (ndiff 1 vs input — the −7 delta touches only the low byte of the stored LE word, first differing byte 844, inside the tampered window [844, 848)), dinit cell chose `cand-dinit-7` sha `b67ce1bd…14bc7` | **Yes — both cells** |
| R4 /proc walk | `/proc/self/mountinfo` leaks the run-root tmpfs line (`… - tmpfs tmpfs rw,mode=755,uid=1000…` at `<run_root>`); `/proc/<bwrap>/cmdline` and `/proc/<driver>/cmdline` readable (leak `--tmpfs <run_root>`, `--bind <decoy> <path>`, driver argv); but `os.getppid()` chain to the outside driver gives `readlink /proc/<driver>/cwd` = EPERM, driver fds list = `PermissionError` per fd, `driver_environ` unreadable, and every `/proc/<outside-pid>/root/…` escape (driver pid 4044250 in run 5, 201111 in run 6; plus `/proc/1/root/usr/bin/jq`) → **EACCES/EPERM** | **No** (bubblewrap's unprivileged userns denies the ptrace-class reads; cmdline/stat readable only) |
| R5 upx runs | `upx --best -q` on the decoy → rc 1 `UnknownExecutableFormatException` (junk, not a carrier); repack of the real jq reached as `/proc/<driver>/root/usr/bin/jq` → rc 1 `IOException: Permission denied` (blocked by the same R4 EPERM) | **No** |
| R6 lane fixtures | Bounded sweep (first 4096 B, ≤8 MiB, ≤40 000 files, skipping `.git`): the only `UPX!`-bearing lane files are the four r87/r88/r89/r90 knowledge `.md`s (text mentions, e.g. `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md` sha `74d856ea…740d8`) — **no packed binary fixture exists in the lane** | **No** |
| R7 receipts | 287 files read under `.ufo/waves/round-90/`; sha-like tokens = 61; token hits include the four **orig** pins AND all four **packed** shas (they appear in engine receipts such as `w1/ScribeEntry/receipts/indep-cells.json` and `w1/ExecMatrix/tamper-matrix.json`); 0 base64 blobs with `UPX!`/ELF magic; `UPX!` text hits 87 (prose) — **pins only, zero intact packed bytes recoverable** | **No** |

Net attack verdict — **the carrier-blind control, as currently built, is
penetrable by the neighbour route and no other sampled route**: a blind "repair"
that never opens any pinned carrier path, never touches the run root, and never
walks a single external fixture — it merely lists the parent directory of its
own box (which is `<boxes>`, sibling of `run_root`, not tmpfs'd, per counter
line 265), length-filters the visible `cand-*` / sibling `inv-*/in|out`
leftovers, and returns the unique nonzero-small-diff match as its `out`. Both
probe cells then score, under the counter's own arms, `repair_rc0` true,
`field_only` true, `identity` true, `test_ok` true, `unpack_pin` true →
**`recovered: true`, blinded** (`receipts/harness-summary.json` cells
`cheat-jq-m7` and `cheat-dinit-p7`; per-route probes
`receipts/probe-findings-cheat-jq-m7.json`,
`receipts/probe-findings-cheat-dinit-p7.json`). `box_after` stays
`['in','out']`, so `isolation` stays true while the sibling canary sits in a
neighbouring box — the control pair (168+170) cannot distinguish this from the
honest derivation: the honest cell scores identically (`honest-jq-m7`
recovered, isolation true) **and** the cheat scores identically to the honest
cell on every observable.

Attribution: intact bytes reach `boxes` because `score_case` writes every live
run's candidate to `boxes` via `mkstemp(prefix="cand-", dir=boxes)` and every
`invoke()` box persists (N3's `in` holds the intact carrier); the blind arm then
runs in the same `boxes` directory (`score_case(..., blind)` reusing `boxes`),
so "carrier blindness" is enforced only against the *pinned carrier paths and
the run root*, not against the process's own directory neighbourhood. The blind
mounts bind the four realpath'd source paths; everything else on `/` remains
visible through `--dev-bind / /`.

## Secondary measured observations

1. **Dangling `TMPDIR`/`HOME` inside the sandbox**: the counter's `child_env`
   points both at subdirectories of `run_root`, which the tmpfs mount makes
   non-existent in the blind view (`R5.tmpdir_env` = `<run_root>/tmp`,
   `tmpdir_exists` = **true** only because the probe created it itself in its
   visible box — measured on the probe side: the first run's `upx` output to
   `<run_root>/tmp/decoy-packed` failed with `No such file or directory`
   before I re-targeted the output to the visible box in run 6). Any blind-mode
   repair child that writes through `tempfile` with the env `TMPDIR` inherits
   that failure mode; the pinned repair avoids it because `write_atomic` uses
   `mkstemp(dir=output_dir)` (its own box, visible).
2. **A blind child's imports are narrower than its host's**: `binascii` (and
   therefore `base64` and `zlib`) fail to import in the sandbox with
   `ImportError: /usr/lib/libz.so.1: invalid ELF header`, because the decoy is
   bound over `libz.so.1.3.2` and `binascii.cpython-314…so` on this host NEEDs
   `libz.so.1` (verified with a per-module import matrix: os/re/json/hashlib/
   struct/subprocess/tempfile/argparse/importlib rc 0; binascii/base64/zlib
   rc 1). Consequence: any round-90 repair revision that reaches for `base64`
   would die in the carrier-blind arm for an accidental reason, not a
   derivation one — worth knowing before anyone adds a base64 dependency to
   the repair.
3. route 168's probe (`pr = bwrap … print sha256 of each blind path`) is
   satisfied by the decoy equality measured in R1 — my R1 result is consistent
   with the counter's probe design intent (see R1 table above, all
   `equals_decoy: true`).

## Fix shape (finding, not instruction)

The leak is one directory relationship: the invocation boxes live in
`<boxes>` = a sibling of `run_root` under `<work>` and are not hidden by the
blind sandbox, and they are full of intact bytes. Any of these closes it:
(a) per-cell `--tmpfs <box>` around blind invocations (input visible, siblings
    gone) — the same trick already used for `run_root`;
(b) putting `boxes` under `run_root` (then the tmpfs hides the leftovers — but
    read the pseudocode at line 265 again: the separation is deliberate;
    re-deriving why would be needed);
(c) deleting each `inv-*`/`cand-*` leftover immediately after the live loop,
    before the blind arm begins.
(a) is the smallest change: one extra bwrap arg in `invoke()` when `blind` is
set — the counter already constructs that argv (lines 181–186).

Everything claimed above is reproduced by `python3 -I -B receipts/driver.py`
(copy it anywhere writable); final-state receipts:
`receipts/harness-summary.json` (cells + isolation + determinism),
`receipts/route-analysis.txt` (route-by-route values),
`receipts/probe-findings-*.json` (R1–R7 detail per cell),
`receipts/driver-stdout-final-run.txt`,
`receipts/run2.out`–`run5.out` (the intermediate runs, kept because they
document the binascii/zlib sandbox crash and the `--mode honest` probe-harness
false start), `receipts/driver.py`, `receipts/probe_cheat.py`.

Scope note: I did not run the full battery tool end-to-end, did not modify any
lane-tracked file, and produced no verdict about R90-C1's green/red overall —
this seat's deliverable is the measured answer to the two questions plus this
route table, for the L1 to fold into the C1 verdict and corpus materials.
