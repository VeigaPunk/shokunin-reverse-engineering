# EX-22 — BEFORE-STATE baseline: the four named custody-pair holes (chain c2)

Seat EX-22 (chain c2, executor), wave arc3-loop1-round3, 2026-10-19.
Task: reproduce the BEFORE state of the **current** tool on `/var/tmp` copies, verbatim.
All four reproduced. Nothing in `.ufo/gates/custody-pair/` was written by this seat.

## 0. Identity & scope

| item | value |
|---|---|
| repo | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| repo HEAD at run time | `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` |
| tool sha256 (BEFORE rev) | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` |
| provenance of the BEFORE rev | `git cat-file -p HEAD:.ufo/gates/custody-pair/custody-pair.py \| sha256sum` → the same digest (HEAD blob `f3abeb2`), so this before-state is reproducible from git, not only from scratch — `transcripts/identity-head-blob.txt` |
| working copy actually executed | `/var/tmp/ex22-baseline/tool/custody-pair.py` |
| copies re-derived | same sha256 before the session and after it (`transcripts/r5-tool-rehash.txt`; 13:08Z, worktree still `112d01dc…`) |
| worktree after 13:09:24Z | diverged from HEAD — EX-21's round-3 revision, still in flight while this seat wrote up (see `aftersmoke.md`); the BEFORE evidence below is unaffected |
| host / user / kernel | `plazir27` / `vgpnk` (uid 1000, non-root) / `7.2.3-arch1-3` |
| python | `3.14.7` |
| run window (UTC) | 2026-10-19T13:06:13Z … 13:08Z |
| custody paths | READ-ONLY: capture/verify only; self-attested in §7 |

Revision linkage (rule #14): the round-2 records name the *same* revision as the frozen
instrument — `seats/EX-31.md:9,19`, `seats/EX-35.md:29`, `seats/CU-1.md:37` in
`.ufo/waves/arc3-loop1-round2/`. So this before-state is the revision round 2 measured and
the one the C2 claim calls "before". EACCES is reachable because the seat is non-root
(`id` → `uid=1000(vgpnk)`).

Method: every case runs against scratch fixtures under `/var/tmp/ex22-baseline/work/`,
with the tool executed from a byte-identical `/var/tmp` copy. No custody path was opened
for writing by any command below; the only custody-path reads are the read-only captures in
§7 and the tool's own guarded selftest case (which refuses and is asserted unchanged).

## 1. Case (a) — exists-but-EACCES path → fail-open MATCH exit 0

Fixture: `/var/tmp/ex22-baseline/work/a/noaccess/secret.conf`, 15 bytes, mode 000 **on the
containing directory** so `lstat` itself fails (that is the exists-but-unreadable shape).

Existence proof before and after (the file was present and unchanged for the whole case —
this kills the "maybe the fixture was really absent" reading):

```
$ stat -c 'name=%n inode=%i size=%s mtime=%Y' .../a/noaccess/secret.conf      # before chmod
name=/var/tmp/ex22-baseline/work/a/noaccess/secret.conf inode=11176693 size=15 mtime=1792415213
ab7ef8904c06161234c178b820e6121f55ee9952156d930b696e51aaff7241e6  .../a/noaccess/secret.conf
$ stat .../a/noaccess/secret.conf                                             # after chmod 000
stat: cannot statx '.../a/noaccess/secret.conf': Permission denied
[exit-status] 1
$ python3 -c "os.lstat(...)"
lstat raised: PermissionError: [errno 13] Permission denied
[exit-status] 1
...
# after the verify runs, dir restored to 755:
name=/var/tmp/ex22-baseline/work/a/noaccess/secret.conf inode=11176693 size=15 mtime=1792415213
ab7ef8904c06161234c178b820e6121f55ee9952156d930b696e51aaff7241e6  .../a/noaccess/secret.conf   (a7)
```

Capture (writes the receipt to scratch, never to the custody path):

```
$ python3 /var/tmp/ex22-baseline/tool/custody-pair.py capture \
      --out .../work/a/a-rec-A.txt --paths .../work/a/noaccess/secret.conf
RECEIPT: /var/tmp/ex22-baseline/work/a/a-rec-A.txt  sha256=52dee497fe0b2ae7346b44fa6d6585231a42a36cc11253c2a67b88a70c9dce80
SIDECAR: /var/tmp/ex22-baseline/work/a/a-rec-A.txt.sha256
CUSTODY_PAIR_CAPTURE: PARTIAL paths=0/1 label=(none) exit=13
[exit-status] 13
```

The receipt body — the path **exists**, the receipt says it does not:

```
# custody-pair receipt v2 — READ-ONLY capture (sha256 + stat); no bytes written
# receipt-version: 2
# tool: custody-pair.py  sha256 112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa
# captured-utc: 2026-10-19T13:06:53Z
...
# paths: 1  present: 0
...
PATH: /var/tmp/ex22-baseline/work/a/noaccess/secret.conf
EXISTS: no
STAT-ERROR: [Errno 13] Permission denied: '/var/tmp/ex22-baseline/work/a/noaccess/secret.conf'
```

Verify, both sides (this is the fail-open — both modes, exit 0):

```
$ python3 /var/tmp/ex22-baseline/tool/custody-pair.py verify .../a-rec-A.txt --live
A format: v1-stanza   B format: live
CUSTODY-PAIR VERIFY (v2 instrument)
A (reference): /var/tmp/ex22-baseline/work/a/a-rec-A.txt  stanzas=1
B (candidate): live filesystem  stanzas=1
PATH /var/tmp/ex22-baseline/work/a/noaccess/secret.conf: MATCH  compared=0/11
SHA256-CONTRACT: 0/0 paths agree on sha256 (v1/v2 receipts compare on this field)
VERDICT: MATCH  paths=1  MATCH=1  exit=0
CUSTODY_PAIR_VERIFY: MATCH paths=1/1 drift=0 exit=0
[exit-status] 0

$ python3 .../custody-pair.py verify .../a-rec-A.txt .../a-rec-B.txt     # receipt-vs-receipt
PATH /var/tmp/ex22-baseline/work/a/noaccess/secret.conf: MATCH  compared=0/11
VERDICT: MATCH  paths=1  MATCH=1  exit=0
[exit-status] 0
```

**Before-state (a): CONFIRMED.** An unreadable path is recorded `EXISTS: no`, and a
receipt-vs-live or receipt-vs-receipt comparison of two paths that were both "unreadable"
verdicts **MATCH exit 0** with `SHA256-CONTRACT: 0/0` — zero fields compared, no field in
which the false `EXISTS: no` could contradict anything. Behaviour maps to
`custody-pair.py:197-200` (`except OSError` → `exists="no"` + `stat_error`) and
`custody-pair.py:428-430` (`not ref_exists and not cand_exists` → `MATCH`).

## 2. Case (b) — 1-of-5 receipt vs live → exit 0

```
$ python3 .../custody-pair.py paths            # the coverage contract, 5 paths
~/.config/devin/mcp_config.json
~/.omp/agent/mcp.json
~/.kimi-code/config.toml
~/.bashrc
~/.profile

$ python3 .../custody-pair.py capture --out .../work/b/b-rec-one.txt \
      --paths /home/vgpnk/.bashrc --label 1-of-5
RECEIPT: .../b-rec-one.txt  sha256=524d2ef92dd64f7175ad9f57f5872916473254b75388726c5a9ea3172f1846ab
CUSTODY_PAIR_CAPTURE: OK paths=1/1 label=1-of-5 exit=0
[exit-status] 0
$ grep -n '^# paths:\|^PATH:' .../b-rec-one.txt
10:# paths: 1  present: 1
17:PATH: /home/vgpnk/.bashrc

$ python3 .../custody-pair.py verify .../b-rec-one.txt --live
A format: v2   B format: live
A (reference): .../b-rec-one.txt  stanzas=1
PATH /home/vgpnk/.bashrc: MATCH  compared=11/11
SHA256-CONTRACT: 1/1 paths agree on sha256 (v1/v2 receipts compare on this field)
VERDICT: MATCH  paths=1  MATCH=1  exit=0
CUSTODY_PAIR_VERIFY: MATCH paths=1/1 drift=0 exit=0
[exit-status] 0
```

The consequence, with a counterfactual control on scratch copies (same drift event, two
receipts captured **before** it, one in scope and one not):

```
$ ... capture --out b-rec-scope1.txt --paths .../q1.conf            # q1 only
$ ... capture --out b-rec-scope2.txt --paths .../q1.conf .../q2.conf # q1 + q2
$ printf 'q2-DRIFTED\n' > .../q2.conf ; sha256sum .../q2.conf
6b02ceae67f7205ae2d7b10b31639a6c9d74b917c191c5b8af6275e10b3ce07b  .../q2.conf

$ ... verify b-rec-scope1.txt --live        # q2 OUT of the receipt's scope
PATH .../q1.conf: MATCH  compared=11/11
SHA256-CONTRACT: 1/1 paths agree on sha256
VERDICT: MATCH  paths=1  MATCH=1  exit=0
[exit-status] 0

$ ... verify b-rec-scope2.txt --live        # q2 IN scope (control)
PATH .../q1.conf: MATCH  compared=11/11
PATH .../q2.conf: CONTENT-DRIFT  compared=11/11 moved=sha256
SHA256-CONTRACT: 1/2 paths agree on sha256
VERDICT: CONTENT-DRIFT  paths=2  CONTENT-DRIFT=1 MATCH=1  exit=10
[exit-status] 10
```

**Before-state (b): CONFIRMED.** Detection works when a path is in the reference; the hole
is that reference *scope* is never declared or checked. `verify --help` offers only
`receipt_a [receipt_b] --live`; `grep -c -- '--require-paths' custody-pair.py` → `0`
(exit 1). The proposed fix text is EX-35's `--require-paths` adapter
(`.ufo/waves/arc3-loop1-round2/claims/c3/EX-35/proposed-v1-verify-adapter.patch.md:48-63`,
which already names this exact `1 of 5` measurement at line 81).

## 3. Case (c) — `--paths X --out X` clobbers the measured file

```
$ sha256sum .../work/c/target.conf
c94c0aa42882cb2e2a97b50eb39fe9605a6ae127ed2ce252ec8e091d967f9cca  .../target.conf   (17 bytes)

$ python3 .../custody-pair.py capture --out .../work/c/target.conf \
      --paths .../work/c/target.conf --label before-state-clobber-demo
RECEIPT: /var/tmp/ex22-baseline/work/c/target.conf  sha256=e64f106c9eced197b1b988978251f6de631113142484db47bf84b7585b26b3b8
SIDECAR: /var/tmp/ex22-baseline/work/c/target.conf.sha256
CUSTODY_PAIR_CAPTURE: OK paths=1/1 label=before-state-clobber-demo exit=0
[exit-status] 0

$ sha256sum .../target.conf
e64f106c9eced197b1b988978251f6de631113142484db47bf84b7585b26b3b8  .../target.conf   (1337 bytes)
$ cat .../target.conf | head -1
# custody-pair receipt v2 — READ-ONLY capture (sha256 + stat); no bytes written
$ grep -n '^SHA256:' .../target.conf
21:SHA256: c94c0aa42882cb2e2a97b50eb39fe9605a6ae127ed2ce252ec8e091d967f9cca
```

**Before-state (c): CONFIRMED.** The measured file is destroyed after measurement: its 17
canary bytes are replaced by the 1337-byte receipt, the tool prints `OK paths=1/1 … exit=0`
at the moment of destruction, and the receipt's own stanza records the digest
(`c94c0aa4…`) of the bytes it just overwrote — so the artifact documents a state the path no
longer has, under the header line "READ-ONLY capture … no bytes written". The guard at
`custody-pair.py:564` compares `out.resolve()` **only** against the 5 canonical
`CUSTODY_PATHS`, so any other path passed to both `--paths` and `--out` is unguarded.
Post-hoc verification of the clobbered file does report it — `verify .../target.conf --live`
→ `VERDICT: CONTENT-DRIFT … exit=10` — i.e. self-detecting only after the bytes are gone.
Control (distinct `--out`): the measured file is untouched, sha256 `2e7f1f7a…`, `rc=0`.

## 4. Case (d) — `selftest --scratch <missing dir>` → traceback, exit 1

```
$ python3 .../custody-pair.py selftest --scratch /var/tmp/ex22-baseline/work/does-not-exist-xyz
Traceback (most recent call last):
  File "/var/tmp/ex22-baseline/tool/custody-pair.py", line 889, in <module>
    sys.exit(main())
  File "/var/tmp/ex22-baseline/tool/custody-pair.py", line 885, in main
    return args.func(args)
  File "/var/tmp/ex22-baseline/tool/custody-pair.py", line 630, in cmd_selftest
    root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))
  File "/usr/lib/python3.14/tempfile.py", line 381, in mkdtemp
    _os.mkdir(file, 0o700)
FileNotFoundError: [Errno 2] No such file or directory: '/var/tmp/ex22-baseline/work/does-not-exist-xyz/custody-pair-selftest-go3bggp9'
[exit-status] 1
```

Same for `--scratch <regular file>` → `NotADirectoryError … [exit-status] 1`
(`transcripts/d3-selftest-file-scratch.txt`). Exit 1 is **outside the declared map**
(docstring `custody-pair.py:59-73`; constants `:119-125` declare 0,2,3,10,11,12,13).

Happy path (= the round's "15 → ≥17" baseline), on scratch:

```
CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0
[exit-status] 0
```

**Before-state (d): CONFIRMED**, and broader than the named case: the crash class is any
non-directory/uncreatable `--scratch`.

## 5. Extra findings observed while reproducing (chain c2's debt, not in the seat task list)

- **E1 — unreadable-but-statable file ⇒ raw traceback in BOTH subcommands, exit 1.**
  With the file itself mode 000 (directory traversable, so `lstat` succeeds and the sha256
  read fails): `capture` → `PermissionError … custody-pair.py:219 sha256_file(path)` →
  `[exit-status] 1`; `verify <receipt> --live` → same traceback at `custody-pair.py:593` →
  `[exit-status] 1`. This is the second half of the named D2 debt ("`--live` against an
  unreadable candidate dies with a traceback outside the declared map"), reproduced
  (`transcripts/a9-*.txt`, `a10-*.txt`). After restoring mode 644, the same receipt-vs-live
  reports `REWRITE-DRIFT … moved=ctime_ns exit=11` — the chmod round-trip itself is caught by
  the ctime pin, so no drift went unseen here.
- **E2 — format tag mislabel on an EACCES-only receipt.** A receipt carrying
  `# receipt-version: 2` prints as `A format: v1-stanza` whenever its stanzas carry no
  `mtime_epoch` (`custody-pair.py:358`), i.e. exactly the fail-open receipts of §1. Any
  consumer keying class semantics on the printed format tag would read a v2 receipt as v1.
- **E3 — `/tmp` guard does not fire when `--scratch` is explicit.** The guard is
  `if str(base).startswith("/tmp") and not args.scratch` (`custody-pair.py:627`), so an
  explicit `--scratch /tmp/...` bypasses it. Executed **without touching `/tmp`** by
  intercepting `tempfile.mkdtemp`:
  `SPY: mkdtemp called with dir='/tmp/ex22-should-be-refused' (no /tmp write performed)`
  (`transcripts/d4-selftest-tmp-explicit.txt`; the `exit-status 1` there is the spy's own
  `RuntimeError`, not the tool's behaviour).

## 6. Read-only self-attestation on the real custody paths (§7 of the task's hard rules)

Two read-only captures of the 5 real paths, 2 s apart, verified against each other:

```
RECEIPT: .../ro-pre.txt  sha256=2fe501a169ba19ab96aafbaf28e002aea497ef79b91ac64b767b8c26dae16ecb
CUSTODY_PAIR_CAPTURE: OK paths=5/5 label=ex22-readonly-attestation-pre exit=0
$ ... verify ro-pre.txt ro-post.txt
PATH /home/vgpnk/.config/devin/mcp_config.json: MATCH  compared=11/11
PATH /home/vgpnk/.omp/agent/mcp.json: MATCH  compared=11/11
PATH /home/vgpnk/.kimi-code/config.toml: MATCH  compared=11/11
PATH /home/vgpnk/.bashrc: MATCH  compared=11/11
PATH /home/vgpnk/.profile: MATCH  compared=11/11
SHA256-CONTRACT: 5/5 paths agree on sha256
VERDICT: MATCH  paths=5  MATCH=5  exit=0
```

Identity fields (inode/ctime/mtime/mode) are compared 11/11 on every path, so a write by any
actor inside that window (including this seat) would have surfaced. This is an independent
third-party check, not the round's own pre/post pair (EX-21's deliverable).

## 7. Attacks / refutations attempted, with verdicts

| # | attack on my own before-state | result | verdict |
|---|---|---|---|
| A1 | EACCES MATCH is a fixture artifact — the file was really absent | pre/post inode 11176693 and sha256 `ab7ef890…` identical across the whole case | refuted; file existed and was unchanged |
| A2 | capture's `exit 13` already flags the EACCES path, so nothing fails open | 13 is the ABSENT class while the path exists; a gate that only runs `verify` never sees capture's exit; and the receipt's own field is false | hole stands (fail-open is in the verify path) |
| A3 | EACCES MATCH also in receipt-vs-receipt mode (not just `--live`) | reproduced: exit 0 both modes | hole stands, both modes |
| A4 | clobber is harmless — the receipt records the pre-clobber digest | that digest is of the bytes the receipt itself replaced; capture reports `OK … exit=0`; only a later `verify --live` (exit 10) notices | hole stands |
| A5 | §2's exit 0 is because q2 was never driftable — verify can't detect drift at all | control b6: same drift, in-scope receipt → CONTENT-DRIFT exit 10 | refuted; the hole is scope, not detection |
| A6 | I tested a modified tool | copy sha256 == repo target sha256 == `112d01dc…` before and after the session | refuted |
| A7 | the round's "before" rev differs from mine | round-2 seats EX-31/EX-35/CU-1 record the same `112d01dc…` | refuted; same revision |
| A8 | selftest crash is specific to a missing dir | a regular file as `--scratch` crashes the same way (NotADirectoryError, exit 1) | hole is broader than named |

## 8. Before → after table for the chain's claim (c2 = EX-21's landing)

| item | BEFORE (this seat, rev `112d01dc…`, verbatim above) | declared AFTER (C2 claim) |
|---|---|---|
| (a) exists-but-EACCES path | receipt `EXISTS: no` + STAT-ERROR; verify → **MATCH exit 0** | EACCES → its own class; no fail-open MATCH |
| (a′) unreadable-but-statable file | **traceback, exit 1** (capture and `--live`) | inside the declared exit map |
| (b) 1-of-5 receipt vs live | **MATCH exit 0**, scope silent | `verify` coverage declared (`--require-paths`) |
| (c) `--paths X --out X` | X **clobbered**, capture `OK paths=1/1 exit=0` | write-guard `set(paths) ∪ CUSTODY_PATHS` |
| (d) `selftest --scratch <missing>` | **FileNotFoundError traceback, exit 1** | USAGE (exit 2) |
| selftest case count | **15/15 CLEAN, exit 0** | ≥17 |
| live pair on the 5 paths | MATCH 5/5 (this seat's read-only attestation, §6) | round's live pre/post pair MATCH 5/5 vs the revised tool |
| command A / other chains | untouched by this seat (no repo writes outside `claims/c2/EX-22/` + seat report) | unchanged |

## 9. Transcripts & reproduction

`transcripts/` holds 56 files: one raw capture per command (`# cwd=…`, `$ <argv>`,
combined stdout+stderr, `[exit-status] N`), plus the two artifacts of record
(`artifact-a-rec-A-receipt.txt` = the fail-open receipt; `artifact-c-clobbered-target.conf`
= the clobbered file), the §6 read-only receipt pair with sidecars, and
`identity-head-blob.txt` (git provenance of the BEFORE rev).
`transcripts-after/` holds 29 files for the advisory in-flight probe (`aftersmoke.md`),
including `snapshot-9860149d-custody-pair.py.txt` (the exact revision those probes ran) and
the post-run custody recheck (`f3-capture.txt`, `f4-verify.txt`, `ro-post3.txt`).
Machine list of digests: `sha256s.txt` (same directory). Fixtures are reproducible with:

```bash
S=/var/tmp/ex22-baseline        # scratch root; never /tmp (EDQUOT)
mkdir -p $S/tool $S/work && cp <repo>/.ufo/gates/custody-pair/custody-pair.py $S/tool/
# (a) mkdir $S/work/a/noaccess; printf 'secret-bytes-A\n' > $S/work/a/noaccess/secret.conf;
#     chmod 000 $S/work/a/noaccess; then: capture --out <scratch> --paths <that file>;
#     verify <receipt> --live  → MATCH exit 0
# (b) capture --out <scratch> --paths ~/.bashrc; verify <receipt> --live → MATCH exit 0
# (c) printf 'canary-content-A\n' > $S/work/c/target.conf;
#     capture --out $S/work/c/target.conf --paths $S/work/c/target.conf → exit 0, file gone
# (d) selftest --scratch $S/work/does-not-exist-xyz → traceback, exit 1
```

No blockers. Nothing in this seat's evidence depends on another seat's output.