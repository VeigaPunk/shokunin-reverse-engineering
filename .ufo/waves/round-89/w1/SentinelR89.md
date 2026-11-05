# SentinelR89 — security and cost review of the round-89 repair (R89-C1 / R89-C2)

Seat: `.ufo/waves/round-89/w1/SentinelR89/` (leaf; no dispatch). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base revision
`0ec2bb4016655f605657d6e0e700ec2e6893ac27`; measured worktree HEAD
`8bbb40cc09fadd211b1aa473605553c9caeef511` (`git diff --stat HEAD -- tools/round-89 tools/round-87 tools/round-88`
empty, rc 0 — the instruments I review are the tracked ones).

Instrument under review (hashes taken at 21:42, before the mid-seat replacement below):

| file | sha256 on disk at 21:42 | frozen pin |
|---|---|---|
| `tools/round-89/upx-field-value-repair.py` | `332917f2b620da7a659b78db5bf498c8af2eba6ae529d872c2518b62ad6b1070` | same (container `instruments`) |
| `tools/round-89/upx-field-battery.py` | `f6f5ed61f47e055b7cfa6b58c2e29064d8e4eb31859ff1963a8e80393cd0b720` | same |
| `tools/round-89/depth-blocks-v2.py` | `359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f` | same |
| `tools/round-87/upx-magic-repair.py` | `96da7d8e981b04f5a598dc7eb8ec3f05eeae4b1498f769c83e72c67f6babec24` | same |

The seat prose quotes the repair at `048e2c8e…`; the frozen container and the disk both said
`332917f2…` at 21:42. The prose prefix is stale, the container is authoritative — no receipt is at
fault, but a grader matching the prose would fail a correct receipt (finding F13).

## Instrument replaced mid-seat — read this before applying any finding

The bytes I was assigned are `332917f2…` (10 970 B), which is what the frozen container names and
what every measurement in items 1–2 was taken against (21:42–22:10 local). At **22:16:34** a sibling
replaced the file in place — commit `bc0e0c20` *"round-89: repair hardening (output paths, atomic
temp writes, typed write errors) with its supersession entry and the final receipts"* — and at
**22:19:44** regenerated the committed `pre/c1-candidate-at-declaration.json` against the new bytes.
The shipped file is `41f29f21…` (15 031 B); `git diff 8bbb40cc..HEAD -- tools/round-89/upx-field-value-repair.py`
is the delta.

I re-ran the same hostile matrix against the shipped bytes (`receipts/shipped-bytes-delta.json`):

| case | frozen `332917f2` | shipped `41f29f21` |
|---|---|---|
| FIFO | no exit in 20 s | rc 2 `refused: not a regular file: …/f.fifo` |
| `/dev/zero` | rc 1 `MemoryError` | rc 2 `refused: not a regular file: /dev/zero` |
| symlink → `/usr/bin/jq` | rc 1 traceback | rc 2 `refused: not a regular file: …/link` |
| 300 MiB sparse | rc 1 uncaught `Refused: input larger than 268435456 bytes` | rc 2 `refused: input larger than 268435456 bytes` |
| `--out ../esc.bin` | rc 0, wrote outside | rc 2 `refused: --out carries a '..' component: ../esc.bin` |
| `--out` absolute, outside | rc 0, wrote | rc 0, wrote — **unchanged** |
| `--out` missing directory | rc 1 `FileNotFoundError` | rc 2 `refused: --out parent is not a directory: …/nodir` |
| `--out` is a directory | rc 1 `IsADirectoryError` + stray `<out>.tmp` | rc 2 `refused: --out write failed: …`, no stray |
| pre-planted `<out>.tmp` symlink | rc 0, victim overwritten | rc 0, victim untouched (`VICTIM\n`) |
| plain LE ELF (jq, libz) | rc 1 `r87repair.Refused` traceback | rc 2 `refused: upstream refusal: no validated PackHeader in the tail window` |
| truncated 40 B / 200 B | rc 2 / rc 1 traceback | rc 2 / rc 2 |
| big-endian, non-ELF, directory | rc 2 / 2 / 2 | rc 2 / 2 / 2 |
| `--info` at an existing file | replaced, rc 0 | **replaced, rc 0** — F10 unchanged |

So F1, F2, F3, F5, F6 and the `..` half of F4 are fixed in the shipped bytes; the absolute-path half
of F4 and F7–F13 stand. **F8–F12 are untouched by the hardening**: the battery (`f6f5ed61…`) and the
depth counter (`359f15e1…`) are byte-identical to their pins, and `load_module`/`tool_sha256` are
unchanged in the new file.

The integration consequence is independent of the findings: the committed R89-C1 pre receipt now
names `repair_sha256 41f29f21…`, which is **neither the container pin `332917f2…` nor the bytes the
claim's other receipts were produced with**. The claim's own kill rule — "a receipt whose
`repair_sha256` differs from the frozen pin" — trips on the file the L1 is about to integrate.
Either the container is re-declared with the new pin and the R89-C1 evidence set is retaken, or the
hardening is reverted for this round. That is the L1's call; I only report the state.

All commands below ran as `python3 -I -B <abs tool path> …` (Python 3.14.8). Receipts:
`receipts/hostile-inputs.json`, `receipts/cost-curve.json`, `receipts/receipt-integrity.json`,
`receipts/battery-escape.json`, `receipts/probe-rec.jsonl`, `receipts/shipped-bytes-delta.json`,
`receipts/shipped-repair-battery.json`. Fixtures are the tool's own synthetic
image (`_packed_fixture`), block0 `sz_cpr` stored 32 vs derived 40 at block0 offset 88, file 224
bytes, PackHeader at 188.

---

## Item 1 — hostile inputs

Every case below is a real invocation; rc and text are verbatim. "Outside `--out`" means a path
other than the `--out` argument received bytes.

| # | input | rc | verbatim outcome | writes outside `--out` |
|---|---|---|---|---|
| T1 | FIFO (no writer) | **none in 20 s, killed** | no text; `os.path.getsize(fifo)` is 0 | no |
| T1b | `/dev/zero` (`ulimit -v 600000`) | 1 | `MemoryError` traceback at `data = fh.read()` | no |
| T2 | symlink → `/usr/bin/jq` | **1** | `r87repair.Refused: no validated PackHeader in the tail window` (traceback) | no |
| T3 | 300 MiB sparse | **1** | `Refused: input larger than 268435456 bytes` (traceback, uncaught) | no |
| T3b | 255 MiB sparse (under cap) | 2 | `refused: not a little-endian ELF`; `maxrss_kb=280424` | no |
| T4a | `--out ../escaped.bin --info ../escaped.json`, cwd = scratch/sub | 0 | `field-value: stored 32 -> derived 40 at block0 88` | **yes, `escaped.bin`, `escaped.json`** |
| T4b | `--out /fast/…/abs-outside.bin` | 0 | same stdout | **yes** |
| T5 | `--in "a b\nc.bin" --out "o u\nt.bin"` | 0 | same stdout | no (but the name with a newline is written) |
| T6a | truncated ELF (40 B) | 2 | `refused: not a little-endian ELF` | no |
| T6b | truncated ELF (200 B) | **1** | `r87repair.Refused: no validated PackHeader in the tail window` (traceback) | no |
| T7 | big-endian ELF (`e_ident[5]=2`) | 2 | `refused: not a little-endian ELF` | no |
| T8 | non-ELF text | 2 | `refused: not a little-endian ELF` | no |
| T9 | `--in` is a directory | 2 | `refused: [Errno 21] Is a directory: '/fast/scratch/hyaku/kaidoku-r89/SentinelR89/hostile.dir'` | no |
| T10 | `--out nodir/x.bin` (dir absent) | 1 | `FileNotFoundError: [Errno 2] No such file or directory: '…/nodir/x.bin.tmp'` | no |
| T11 | `--out` is an existing directory | 1 | `IsADirectoryError: [Errno 21] Is a directory: '…/hostile.outdir.tmp' -> '…/hostile.outdir'` | **stray `hostile.outdir.tmp`** |
| T12 | pre-planted `out.tmp` → symlink to `victim.bin` | 0 | same stdout; `victim.bin` now begins `7f454c46…` and equals `out` | **yes: `victim.bin` overwritten** |

The plain-ELF population is the important row: the same traceback, rc 1, for every little-endian
ELF that is not UPX-packed —

```
python3 -I -B tools/round-89/upx-field-value-repair.py --in <file> --out refuse.out
rc=1
  File ".../tools/round-89/upx-field-value-repair.py", line 65, in derive
    ph_off, ph = rep.find_packheader(d)
  File ".../tools/round-87/upx-magic-repair.py", line 87, in find_packheader
    raise Refused("no validated PackHeader in the tail window")
r87repair.Refused: no validated PackHeader in the tail window
```

measured on `elf-min.bin` (64-byte LE ELF header), `/usr/bin/jq`, `/usr/bin/xxd`,
`/usr/lib/libz.so.1.3.2` — i.e. on the battery's own N1 population. No output file was written in
any of the four.

### F1 (High) — no regular-file check; the size cap measures a stat, the read is unbounded
The round-89 tool dropped the guard its two composed parents both carry
(`tools/round-87/upx-magic-repair.py:389`, `tools/round-88/upx-chain-repair.py:253`:
`if not stat.S_ISREG(st.st_mode): raise Refused(...)`, then `fh.read(MAX_INPUT + 1)`). Here
`os.path.getsize(a.src)` (line 242) is 0 for a FIFO, so the cap passes and `open()` blocks in the
kernel with no timeout (T1: no exit in 20 s); on a character device the same gap reads until the
allocator fails (T1b: `MemoryError`). Impact: any wrapper that feeds the tool a path it did not
create can be wedged or OOM-killed. Fix: `st = os.stat(a.src)`; refuse non-`S_ISREG`; keep the cap;
read `MAX_INPUT + 1` bytes so a growing file cannot outrun the stat.

### F2 (High) — the cap's own refusal is an uncaught exception
`raise Refused(f"input larger than {MAX_INPUT} bytes")` sits inside the block whose handler is
`except OSError` (lines 242–246), so the tool's own `Refused` is not caught by it: rc **1** with a
traceback `Refused: input larger than 268435456 bytes` instead of the documented rc 2
`refused: …`. Fix: move the size check out of the `OSError` handler (or add `Refused` to the
handler tuple).

### F3 (High) — two `Refused` classes: every plain LE ELF exits 1 with a traceback
`derive` calls `rep.find_packheader(d)` (line 65) outside any handler; the exception raised is
`r87repair.Refused`, not the tool's own `class Refused`. `repair()` catches `rep.Refused` only
around the *anchor* path (line 121), so the derive-path refusal escapes `main`'s
`except Refused`. This is the most common hostile input and the population of the N1 control.
Impact: the tool violates its own documented exit contract (`2 refused (typed, stderr)`), a caller
that keys on rc 2 treats a plain binary as an unexpected failure, and the battery's N1 arm
(`rc != 0`) cannot tell a crash from a refusal — measured on the four pinned carriers, N1 records
`rc 1` for jq, xxd, libz and dinit and marks all four `refused: true`
(`receipts/battery-escape.json` → `controls.N1-refuse-plain`). Fix: wrap the derive call in
`except rep.Refused as exc: raise Refused(str(exc))`; tighten N1 to `rc == 2 and stderr.startswith("refused: ")`.

### F4 (Medium) — `--out` / `--info` are unvalidated write paths
`../escaped.bin`, `../escaped.json`, an absolute path outside the cwd, and a name containing a
newline all write, rc 0 (T4a, T4b, T5). There is no notion of an output root and no check that the
resolved path stays inside one. Impact: a caller that passes a user-supplied `--out` gets an
arbitrary-file write of attacker-chosen bytes; in this lane a hostile `--repair-cmd` can point
`--info` at `.ufo/waves/*/pre/*.json` (see F10). Fix: refuse a `--out`/`--info` whose realpath is
not under an explicit `--out-root`, or at minimum refuse paths containing `..` and symlinked
parents.

### F5 (High) — predictable temp path, symlink-following open
`tmp = a.dst + ".tmp"` then `open(tmp, "wb")` (lines 254–255) follows a pre-planted symlink: T12
had `out.tmp` → `victim.bin`, rc 0, and `victim.bin` was replaced by the repaired bytes while
`out` ended up a symlink to it. Impact: arbitrary write of a file the tool derived, in any
directory where an attacker can create `<out>.tmp`. Fix: create the temp with
`os.open(tmp, O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW, 0o600)` (or `tempfile.mkstemp(dir=dirname)`),
and unlink it on failure.

### F6 (Medium) — the write path's `OSError` is untyped, and leaves debris
The `try/except (Refused, OSError)` covers only the read. `--out` into a missing directory exits 1
with `FileNotFoundError` (T10); `--out` naming an existing directory exits 1 with
`IsADirectoryError` after `os.replace` and leaves `<out>.tmp` behind (T11). Fix: wrap
write/replace/receipt in the same handler and unlink the temp on any failure.

### F7 (Medium) — 255 MiB under the cap is materialised whole, and the derivation copies it again
T3b: `maxrss_kb=280424` for a 255 MiB input that is refused at the first byte of the ELF check.
`derive` additionally allocates `bytearray(d)` (and `bytes(dd)`) per *surviving* candidate, so the
ceiling is unbounded in the survivor count, not in the file size. Fix: lower the cap to a size the
derivation can afford, or bound survivors and copy once.

### Status of each finding against the two byte sets

| finding | frozen `332917f2` (reviewed) | shipped `41f29f21` (bc0e0c20) |
|---|---|---|
| F1 | open — FIFO hangs, device OOMs | **fixed**: `read_input` (`lstat` + `S_ISREG`) |
| F2 | open — rc 1 traceback | **fixed** — rc 2 `refused: input larger than …` |
| F3 | open — rc 1 traceback on every plain LE ELF | **fixed** — rc 2 `refused: upstream refusal: …` |
| F4 | open — `..` and absolute both written | `..` and symlinked parents refused; **absolute paths still written** |
| F5 | open — victim overwritten | **fixed** — `mkstemp` + `os.replace`, victim untouched |
| F6 | open — rc 1, stray `<out>.tmp` | **fixed** — rc 2, no stray |
| F7 | open | **open** — `derive`'s copies and the 256 MiB cap are unchanged |
| F8–F13 | open | **open** — battery, depth counter and `load_module` are unchanged |

---

## Item 2 — cost bound

Craft family: 32 bytes per `l_info` candidate, `bytes = 64 + 32·N + 36` — the same stride as the
round-88 `c1-candidate-scan-scaling` family (`bytes = 160 + 32·N`). Each record carries
`p_filesize == u_file_size` and `l_version/l_format` matching a checksum-valid PackHeader, so
`l_info_candidates` returns every one and no record carries a derivable first block — both
geometries scan all N and refuse. Generator: scratch `mkcraft.py` (embedded in
`receipts/cost-curve.json` as `layout`). Measurements are sequential, one process at a time.

| candidates | bytes | wall s | rc | refusal text (verbatim) |
|---|---|---|---|---|
| 800 | 25 700 | 6.333 | 2 | `refused: no l_info candidate carries a derivable first block` |
| 3 200 | 102 500 | 88.540 | 2 | `refused: no l_info candidate carries a derivable first block` |
| 12 800 | 409 700 | 1 562.133 | 2 | `refused: no l_info candidate carries a derivable first block` |

No output and no `--info` receipt is written on any of the three (`wrote_output: false`,
`wrote_info: false`). Contention control: the first pass over 800/3 200 ran while this seat's
hostile-input matrix was executing and read 8.378 s / 125.489 s; the table carries the re-measured
idle-host values (6.333 s / 88.540 s), and the contended pair is kept in
`receipts/cost-curve.json` → `contention_control`.

**The curve is quadratic, not linear.** 4× candidates costs 14.0× wall time (800 → 3 200) and
17.6× (3 200 → 12 800) — bracketing the 16× that a Θ(N²) law predicts. The structure says the
same: `derive` runs `for s1 in range(b0 + 13, ph_off - 12)` for **every** candidate, i.e.
Θ(N · ph_off) offset visits before any chain test, and `ph_off` itself grows with N in any input
that carries N candidates. Each *surviving* `s1` additionally copies the whole file
(`bytearray(d)`), walks its chain and re-walks the resumed segment.

**Bound (measured, two-parameter, no linearity assumed).** Fitting `T = c · N · ph_off`:
`c = 3.085e-7`, `2.700e-7`, `2.979e-7` s per (candidate × offset) at 800 / 3 200 / 12 800 —
within 7 % of `c = 2.92e-7`. So

> `T ≈ 2.9e-7 · N · ph_off` seconds (N = `l_info` candidates, `ph_off` = bytes before the PackHeader),

and at the tool's own input cap (256 MiB, 12 800 candidates) that is 3.4 × 10¹² offset visits ≈
**11.6 days** for a single refusal. The practical bound for a counter is therefore a *budget*, not
a shape: the 12 800-candidate point alone needs **26 minutes** of wall time to answer `rc 2`, so
any harness that runs this repair on an untrusted path needs a timeout and a candidate cap (e.g.
refuse when `len(l_info_candidates) · ph_off` exceeds ~10⁹, which is ~5 minutes at `c = 2.9e-7`).

The survivor term is an **unmeasured** upper bound: a craft that plants a valid `b_info` chain at
many `s1` offsets multiplies the per-candidate cost by (survivors × file bytes copied); my family
has zero survivors, so the numbers above are a floor for adversarial input.

---

## Item 3 — receipt integrity

### F8 (High, claim-level) — the `isolation` control cannot fail
`apply_repair` creates `box = tempfile.mkdtemp(prefix="inv-", dir=private_root)`
(`upx-field-battery.py:176`), writes `in`, and then captures
`before = sorted(os.listdir(box))` at line **180 — before the child runs**. `iso_ok` (line 369)
compares that pre-run listing to `["in"]`, so it is true by construction for every repair,
including one that writes a hundred files. The child is spawned without `cwd=` (lines 189–191), so
its working directory is the *battery's* cwd, not the box.

Measured with a probe `--repair-cmd` that delegates to the frozen repair (so the case arms still
pass) and records what it can reach — `receipts/battery-escape.json`, `receipts/probe-rec.jsonl`:

```
recovered 4 of 4 controls_ok={'N1-refuse-plain': True, 'N2-corrupt-payload': True,
 'N3-intact-idempotent': True, 'isolation': True} met=True exit=0
isolation boxes [['in'], ['in'], ['in'], ['in']]
```

while the probe, on every one of its 16 r89-level invocations, saw and did this:

```
argv   = ["--in", ".../r89-battery-jduyeaip/invocations/inv-x3fpyzmo/in",
          "--out", ".../r89-battery-jduyeaip/invocations/inv-x3fpyzmo/out"]
cwd    = /fast/scratch/hyaku/kaidoku-r89/SentinelR89        # the caller's cwd, not the box
writes = {"cwd-relative":  ".../SentinelR89/probe-inside-box.txt",
          "parent-sibling": "/fast/scratch/hyaku/kaidoku-r89/probe-outside-box.txt"}
json_out = .../SentinelR89/battery-escape.json               # read from /proc/<ppid>/cmdline
```

So the repair invocation escaped the private directory by `cwd`, by `..`, and by absolute path,
and the isolation arm still reported true. Additionally all boxes live under one shared
`private_root` (`run_root/invocations`, line 257) and are removed only by the final `rmtree`, so
each child's box parent holds every earlier case's box. Fix: spawn with `cwd=box`, list the box
**after** the child exits and require exactly `["in", "out"]`, use a per-invocation private root,
and fail the arm on any extra path.

### F9 (Medium, claim-level) — the counter does not enforce its own kill rule
`--repair-cmd` accepts any path; `repair_sha256` is recorded (line 396) but never compared to the
frozen `332917f2…`. My probe (`repair_sha256 f1a6b9d7579b153a…`) produced `met_target: True`,
exit 0. The receipt also records the repair as `os.path.relpath(repair, root)` —
`../../../../../fast/scratch/hyaku/kaidoku-r89/SentinelR89/probe-repair.py` — a path that escapes
the repo root and reads as if it were in-tree. Fix: `Unevaluable` unless `repair_sha256` equals the
container pin (or an explicit `--allow-unpinned`), and record the absolute path plus a
`repair_pin_ok` boolean.

### F10 (Medium) — any of the three tools overwrites a committed receipt at a path it is given
`--info` (repair line 262), `--json-out` (battery line 470), `--json-out` (depth counter line 192)
all `open(path, "w")`: no `O_EXCL`, no immutability check, no check that the target is not a
committed `pre/` receipt. Demonstrated on byte-identical copies of the three committed pre
receipts (`receipts/receipt-integrity.json` → `receipt_clobber`):

| writer | rc | effect on the copy |
|---|---|---|
| repair `--info <copy of c1-candidate-at-declaration.json>` | 0 | replaced (sha `ecc29469…` → `7248b0c8…`) |
| battery `--json-out <copy of c2-control-stub-world.json>`, `--work <absent>` | **2** | replaced by `{"exit": 2, "met_target": false, "unevaluable": "work_unusable: …"}` |
| depth counter `--json-out <copy of c2-depth-at-base.json>` | 1 | rewritten (mtime 1793839592 → 1793839610; bytes identical because deterministic) |

The real `.ufo/waves/round-89/pre/` is `drwxr-xr-x vgpnk` with `-rw-r--r--` receipts and
`os.access(..., W_OK)` true, so the same write lands there. A **failed** run (`rc 2`) rewriting a
committed receipt is the sharpest form: a broken harness can silently destroy the `before`
evidence it is being judged against. Fix: write receipts with `O_CREAT|O_EXCL` into a run-owned
directory, and refuse any `--info`/`--json-out` whose realpath is under `.ufo/waves/*/pre/`.

**Live instance, this round** (`receipts/shipped-bytes-delta.json` → `live_pre_rewrite`): the real
`.ufo/waves/round-89/pre/c1-candidate-at-declaration.json` was rewritten at **22:19:44** by a
sibling — sha `ecc29469…` → `c092d08a…` — with the battery's `--json-out` pointed straight into
`pre/`. The new body names `repair_sha256 41f29f21…` (the post-hardening bytes) and still says
`"label": "recovered 4 of 4", "met_target": true, "exit": 0`. Nothing in the chain noticed that a
committed "before" receipt had been replaced, or that the replacement names a repair the container
does not pin. The shipped repair still clobbers an existing `--info` target (measured: `rc 0`,
copy replaced `20907a8f…` → `9957c23d…`), so the hardening fixed the *write* mechanics (F5/F6) but
not this.

### F11 (Medium) — the pinned dependency is executed before it is hashed, and the pin is never checked
`load_module` (repair lines 52–60) does `spec.loader.exec_module(mod)` and only then reads the file
to compute `digest`; `derive`/`repair` never compare that digest to a pin. Demonstrated with a
copy of the tool tree whose `tools/round-87/upx-magic-repair.py` was replaced by a module that
writes a marker at import and then defers to the real one:

```
rc=0   marker: "r87 module executed before any hash check"
receipt upstream_sha256 = b6786d0ed5603dbd70555d31035e102239d908b459913a00306910eea8dc2f50
frozen r87 sha256       = 96da7d8e981b04f5a598dc7eb8ec3f05eeae4b1498f769c83e72c67f6babec24
```

The hostile module executed and the receipt recorded its hash as if that were the pin. Because
`ROOT` is derived from `__file__`, whoever controls the directory layout around the tool controls
which module is executed. Fix: read → sha256 → compare to the frozen constant → `exec_module`; pin
R88 as well as R87; record `r87_pin_ok`/`r88_pin_ok`.

### F12 (Low-Medium) — instrument hashes are self-attested
`tool_sha256` is `sha256(open(__file__))` read at receipt time (repair line 258, battery line 393),
so a modified instrument reports its own new hash; the only binding to the frozen pin is a human
diff against `claims.json`. Fix: compare to the container pin and emit a boolean.

### F13 (Low) — the seat prose and the frozen container disagree on the repair pin
`048e2c8e…` (dispatch/spec prose) vs `332917f2…` (container `instruments`; the disk matched it
until the 22:16 hardening, and has been `41f29f21…` since). A receipt carrying the container's pin
fails a prose-based check, and a receipt carrying the shipped pin fails both. Fix: quote the
container's pin in the dispatch text, and have the counter print the pin it expects next to
`repair_sha256` so a mismatch is visible in the receipt itself.

---

## Verdict for the round

* **R89-C1's capability holds on both byte sets, measured.** Frozen bytes: `recovered 4 of 4`,
  `met_target: true`, exit 0 with a delegating probe (`receipts/battery-escape.json`). Shipped bytes:
  I re-ran the battery myself against `41f29f21…` — `recovered 4 of 4`, `met_target: true`, exit 0,
  `repair_sha256 41f29f211fcaef9c…`, N1 now `rc 2` on all four carriers and the round-88 regression
  arm met (`receipts/shipped-repair-battery.json`, 176 s including REA). The hardening did not
  regress the repair.
* **R89-C1's evidence set is now inconsistent with its own pin.** The container freezes
  `332917f2…`; the committed candidate receipt names `41f29f21…` (the hardening commit
  `bc0e0c20`), and it was written over the previous receipt at 22:19:44 with no immutability check
  (F10, live). The claim's kill rule — "a receipt whose `repair_sha256` differs from the frozen
  pin" — trips on the file the L1 is about to integrate. Either re-declare the container and retake
  the R89-C1 evidence, or revert the hardening for this round.
* **R89-C1's control surface still does not hold**: the `isolation` arm is a tautology (F8 — a
  probe that ran in the caller's cwd, wrote into it and into `..`, and read the parent's
  `--json-out` from `/proc/<ppid>/cmdline` still scored `isolation: True, met_target: True`), and
  the counter does not enforce its own pin (F9 — a probe with `repair_sha256 f1a6b9d7…` scored
  `met_target: True`). The kill rule's isolation clause can never fire.
* **The repair's typed-refusal contract is fixed in the shipped bytes** (F2, F3 measured rc 2 with
  `refused: …` on FIFOs, devices, symlinks, oversize, plain ELF and truncated input) — but the
  battery's N1 arm still only tests `rc != 0`, so it cannot detect a regression to a traceback.
* **R89-C2 is untouched by this review**: the depth counter's only defect in scope is F10 (it
  rewrites whatever `--json-out` names, at any exit code, including `rc 1`). Its target arithmetic
  (`blocks == expect and resolved == blocks and not unresolved`) is the property I checked against
  the two committed controls, and both are red as declared.
* **Cost**: the derivation is Θ(N²) in practice (N candidates each scanning the pre-PackHeader
  region) with an unbounded survivor multiplier; 12 800 candidates costs 26 minutes to refuse, and
  the cap-sized worst case is ~11.6 days. Any harness that runs this repair on untrusted input
  needs a timeout, a candidate cap, and the F1 regular-file guard (now present in the shipped
  bytes).

## Hygiene

* No mutating git/jj command ran; no lane file was created or edited except this report and
  `receipts/` under my own seat directory. `claims.json`, `MANIFEST.json`, `.ufo/state/`,
  `watchdog.log`, sibling lanes and the fleet root were not touched.
* Hostile fixtures were built only in `/fast/scratch/hyaku/kaidoku-r89/SentinelR89`; the receipt
  paths above are copies under my seat.
* No tool was installed or upgraded (the pinned `upx 5.2.0`, `node`, and REA 6.5.0 were used
  read-only as shipped); pacman was not invoked.
* Scratch tree `/fast/scratch/hyaku/kaidoku-r89/SentinelR89` is deleted after the receipts were
  copied into the seat (see the `scratch_deleted` field of `receipts/cost-curve.json`).
