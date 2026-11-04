# SentinelR87: hostile-input review of tools/round-87/upx-magic-repair.py

Round 87 (kaidoku), seat SentinelR87 (sentinel, read-only). Target: `tools/round-87/upx-magic-repair.py`
at b5c7a49e2, sha256 `f4ebd152495dc832180fff3d1ca3447937a7dad121ba63d57872003ffcc49723` (re-hashed on disk).
Host: Python 3.14.8, /usr/bin/upx 5.2.0 (sha256 `cf2f6e7c…c969`, matching the counter pin), GNU time `/usr/bin/time -v`.
All probes ran as `env -i PATH=/usr/bin LANG=C HOME=… TMPDIR=… python3 -I -B <tool> --in <f> --out <o>` from
scratch dir `/fast/scratch/hyaku/kaidoku-r87/SentinelR87/`. The scratch dir was deleted afterwards. Receipts
in this directory: `gen.py` (crafted inputs, sha256 `89fcf9e9…93a9`), `drive.sh` (timeout + time -v driver),
`decoy_probe.py` (F1 repro). Nothing in the frozen files was changed. No input was executed.

## Severity-ranked findings

### F1 MEDIUM: a decoy sentinel steers the resume scan, so the tool exits rc 0 after writing the wrong window
`find_sentinel` resumes at the **first** offset after the first walk's stop whose chain (same method)
ends in a 12-byte zero-ish record. A 25-byte decoy (`b_info{sz_unc=2, sz_cpr=1, method=<chain method>, 0,0,0}` +
1 byte + 12 zero bytes) planted 64 bytes after the stop offset, inside the loader stub, wins over the real chain.

| case | real sentinel | decoy | tool `b_info_end` | real end-of-chain magic after repair | `upx -t` in → out |
|---|---|---|---|---|---|
| jq T1 + decoy | 13988 | 10161 | 10178 | `00000000` (not restored) | 2 → **1** |
| dinit T1 + decoy | 357734 | 352738 | 352755 | `00000000` (not restored) | 2 → **1** |
| jq intact + decoy | 13988 | 10161 | 10178 | `UPX!` | 0 → 0, but tool reports `restored ['b_info_end']` and **mutates 4 loader bytes** |
| dinit intact + decoy | 357734 | 352738 | 352755 | `UPX!` | 0 → 0, same 4-byte mutation |

- Exploit path: the tamperer zeroes the magics (the frozen T1 tamper) and also writes the decoy into stub bytes. `upx -t`
  does not check those bytes: the intact+decoy file still passes `upx -t` (rc 0). Result: the repair reports success
  (rc 0, "repaired: restored 3 anchor(s)") and the output is still not unpackable (`upx -t` rc 1, "compressed data violation").
  On an intact packed file with a decoy, the N3 idempotence property breaks: the tool rewrites 4 loader bytes.
- Impact on the frozen claim: none. The frozen population only overwrites `UPX!` windows, so the 8/8 score is not
  affected. The finding limits what can be promoted: Core coverage holds for "magic-only tamper", not for
  "anti-UPX stub tampering". [INFERENCE, not tested] I did not test whether a decoy can sit in stub bytes that
  never execute, so the packed binary would still run. The bytes I chose are inside the loader, and I executed nothing.
- Evidence hashes: jq.packed `e8b6c9e7…268a`, dinit.packed `b67ce1bd…14bc7`, jq T1+decoy `3d7a7667…21e2`,
  jq intact+decoy `3a3f0d8b…5ff1`, dinit T1+decoy `fb37ecdf…cdea`, dinit intact+decoy `bef56d69…17d3`.
- Repro: `S=/fast/scratch/hyaku/kaidoku-r87/SentinelR87; mkdir -p $S/tmp; TMPDIR=$S/tmp python3 -I -B .ufo/waves/round-87/w1/SentinelR87/decoy_probe.py $S/decoy`
- Smallest fix: (a) scan **all** resume candidates and keep the one whose sentinel is nearest `ph_off`, not the first.
  On the executable carriers the gap from the real sentinel to the PackHeader is 0–3 bytes (jq 0, xxd 3, dinit 2),
  which leaves no room for a later decoy. libz (a shared object) has 1815 bytes of appended data, so it can still be
  steered there. (b) Add an invariant check where it holds: the sum of `sz_unc` over the first and resumed blocks
  equals the PackHeader `u_len` for jq (30800) and xxd (38928). It does **not** hold for libz (98592 vs 108560), so it
  must be gated per format. Also refuse when more than one candidate qualifies, and never touch a window on an input
  whose PackHeader and l_info already read `UPX!` unless the chosen sentinel is unambiguous.

### F2 LOW-MEDIUM: CPU DoS from the quadratic resume scan (and K× l_info candidates)
Memory stays flat (about 15.5–16 MB RSS). Runtime grows quadratically. Each resume candidate re-walks the whole
suffix of the chain, and every `u_file_size` occurrence restarts the scan.

| input (crafted; `gen.py`) | size | rc | wall | peak RSS |
|---|---|---|---|---|
| G-quadchain m1000 (13-byte blocks, no sentinel) | 13 KB | 2 | 0.27 s | 15.7 MB |
| G m2000 / m4000 / m8000 | 26/52/104 KB | 2 | 0.65 / 1.93 / 8.51 s | ~15.9 MB |
| G m16000 / m32000 | 208/416 KB | 2 | 32.91 s / 2:06.33 | ~16.0 MB |
| G m64000 (sha256 `a139c7d2…ea92`) | 832 KB | **killed** | **> 300 s** | – |
| F-ufs ×250 / ×500 / ×1000 / ×2000 / ×4000 (u_file_size repeated K times) | 11–180 KB | 2 | 0.34 / 1.45 / 6.02 / 17.16 / 66.33 s | ~15.8 MB |
| H combined k20 × m2000 | 26 KB | 2 | 10.22 s | 15.5 MB |

- Exploit path: a sample under 1 MB makes the standalone tool spin indefinitely. It has no timeout, so this is a CPU
  DoS for an analyst who runs it on a hostile file. Inside the counter, `apply_repair` has `timeout=300`, so a hang
  becomes rc None and counts as "not recovered". The counter cannot hang.
- Repro: `S=/fast/scratch/hyaku/kaidoku-r87/SentinelR87; python3 -I gen.py $S/in && TO=300 ./drive.sh $S/in/G-quadchain-m8000 $S/in/F-ufs-x2000`.
  For the larger rows, set the F/G tuples in gen.py to `(4000, 8000)` / `(16000, 32000, 64000)`.
- Smallest fix: memoize `walk_chain` end offsets per start offset. Candidates on one chain share a suffix, so the
  scan becomes O(n). Alternatively, bound the resume window: the real loader gap was 3131 bytes on jq
  (10097→13228) and 3154 bytes on dinit (352674→355828). Also deduplicate l_info candidates whose first walk stops
  at the same offset.

### F3 LOW: unbounded read and an exit-code contract gap on I/O errors
- `--in /dev/zero`: unbounded `fh.read()`. Under `prlimit --as=1GiB` it dies with rc 1 after 0.44 s at 930 MB RSS.
  With no limit, it consumes host RAM. `--in <fifo>` with no writer blocks forever (killed by `timeout 5`, rc 124).
- No input size cap. On success, peak RSS is about 3.2× the input (a 64 MiB valid crafted input takes 0.19 s at
  212 MB, since data, bytearray and bytes all exist at once). Refusals stay at about 1.2× (64 MiB of zeros: 81 MB).
- The docstring promises "2 refused". A missing `--in`, a directory as `--in` or `--out`, or an unwritable `--out`
  instead raises a Python traceback with **rc 1**. This is harmless to the counter, where any non-zero rc counts as
  a refusal for N1, but the documented contract is wrong.
- Fix: refuse non-regular `--in` (`os.stat` + `S_ISREG`) and inputs over a cap (for example 256 MiB), and map `OSError` to rc 2.

### F4 LOW / INFO: `--out` follows symlinks and the write is non-atomic
- `--out` → existing symlink: the link target is overwritten (victim file replaced by the repaired bytes; the link itself remains).
  `--out` → dangling symlink: the target file is created. `open(…, "wb")` opens with `O_WRONLY|O_CREAT|O_TRUNC` and
  no `O_NOFOLLOW` (strace). `--in == --out` works, because the whole input is read before the output is opened.
- On refusal nothing is written: a pre-existing `--out` containing `KEEP` was left as `KEEP` (rc 2).
- Impact: an operator chooses the paths, and the counter writes into its own work dir, so there is no privilege
  boundary. If hardening is wanted, write to a temp file in the destination dir and `os.replace` it, or open with
  `O_NOFOLLOW|O_EXCL`.

### F5 INFO / calibration: the repair restores 3 anchors, while jq and xxd carry 4 `UPX!` words
- In packed jq, `UPX!` appears at 556, 10971, 13992, 14000. In packed xxd it appears at 556, 16499, 19513, 19524.
  The fourth word (10971 / 16499) is inside the loader stub. T1/T2 overwrite it, and the tool does not restore it.
  So for jq and xxd the repaired bytes are **not equal to the packed bytes** (4 of the 8 cases;
  `repaired_equals_packed` will be false in the receipt). libz and dinit have 3 words each, and their repaired output
  equals the packed bytes.
- `upx -t` (rc 0) and `upx -d` → original bytes (cmp equal) still pass for jq and xxd. So the frozen arms
  (windows_only, test_ok, identity) hold, and this is not a claim defect. [INFERENCE, not executed] Whether the
  repaired jq or xxd *runs* depends on whether the stub reads its own `UPX!`. That is unverified.
- Hashes: jq.T1 `bdfa7aef…9134`, jq.rep `1b7ed8a2…1624`, xxd.packed `1727faf9…89ff`, xxd.rep `6e072d88…0e0e`.

### F6 INFO: verified-safe properties
- Never executes input: strace (`-f -e execve,openat,rename*,unlink*,mkdir,symlink,chmod`) shows a single execve
  (python3 itself) and exactly one write-open (`--out`). There is no rename, unlink or mkdir, and no child process.
- No import from cwd under `-I`: shadow `json.py`/`struct.py`/`argparse.py` in the cwd, in the script's own directory,
  and on `PYTHONPATH` were **not** imported (no marker files). **Without `-I`**, script-dir shadows **are** imported
  (PWNED markers for all three, rc 1). The counter always passes `-I -B` (battery line 159), and `tools/round-87/`
  currently holds only the two .py files. The shebang `#!/usr/bin/env python3` has no `-I`, so running the tool as
  `./upx-magic-repair.py` is the unsafe path.
- Self-referencing chains terminate. `sz_cpr == 0` (E1) and `sz_cpr == 0xffffffff` (E2) are refused immediately,
  because `q` strictly increases and `MAX_BLOCKS = 65536` caps each walk.
- Degenerate inputs refuse quickly (rc 2): empty and 4-byte inputs (0.06 s, 15.5 MB), 64 MiB of zeros (0.09 s,
  81 MB), an ELF header with a 1 MiB random tail (0.06 s), an ELF header with 64 MiB of zeros (0.06 s, 81 MB), and a
  32 MiB file with a valid PackHeader but no l_info (0.10 s, 48 MB).
- A crafted non-UPX ELF that satisfies all three anchors (I-crafted) gets "repaired" (rc 0, 3 windows). This is by
  design (structure, not provenance). It writes only those 4-byte windows.
- Real carriers, tampered with T1: jq, xxd, libz and dinit each take 0.03–0.06 s at about 16–17 MB RSS. All anchors
  were found structurally (l_info 556/556/9284/556).

## Counter note
`upx-tamper-battery.py` bounds each repair with a 300 s timeout and records `rc None` on a timeout. It builds argv as
a list (no shell) and gives the repair a four-key environment. A hostile repair script is out of scope: the counter
runs whatever path `--repair-cmd` names, with the caller's privileges.
