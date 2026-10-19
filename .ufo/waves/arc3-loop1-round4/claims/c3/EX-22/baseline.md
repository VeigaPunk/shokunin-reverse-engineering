# EX-22 — BEFORE-STATE baseline: the three C3 residuals (sidecar scope, mkdir traceback, stanza-count gate)

Seat EX-22 (chain c3, executor), wave `arc3-loop1-round4`, 2026-10-19.
Task: reproduce the BEFORE state of the **current** tool on `/var/tmp` copies, verbatim.
All three reproduced, plus both directions of (a), a consequence chain, and controls.
Nothing in `.ufo/gates/custody-pair/` was written by this seat.

## 0. Identity & scope

| item | value |
|---|---|
| repo | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| repo HEAD at run time | `015e1bab914713568f339fd53999bc180459cc40` |
| tool sha256 (BEFORE rev) | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` |
| provenance of the BEFORE rev | `git cat-file -p HEAD:.ufo/gates/custody-pair/custody-pair.py \| sha256sum` → same digest; `git status --porcelain -- .ufo/gates/custody-pair/` → empty at 14:08:24Z (`transcripts/0g-head-blob.txt`, `0h-status.txt`, `0k-stat.txt`) |
| working copy actually executed | `/var/tmp/ex22-baseline/tool/custody-pair.py` (sha256 equal; `cmp` exit 0 — `transcripts/0j-copy-sha.txt`, `0l-cmp.txt`) |
| copies re-derived | same sha256 at session end (`transcripts/zQ-exec-copy-sha-final.txt`, `zR-head-blob-final.txt`) |
| revision churn (in-flight, after this seat's runs) | at **14:09:25Z** the repo tool became `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` (1343 lines / 65902 B; `git status` → `M`; EX-21's r4 landing). This seat's injections completed 14:08:24–14:09:18Z, i.e. **before** the change; the BEFORE evidence below is of `7cd19c3c…` only (`transcripts/zF…zM`, `zS`). The in-flight revision is used in §4 as an advisory discrimination check, not as before-state. |
| host / user / kernel | `plazir27` / `vgpnk` (uid 1000, non-root) / `7.2.3-arch1-3` |
| python | `3.14.7` |
| run window (UTC) | 2026-10-19T14:08:24Z … 14:10:40Z |
| custody paths | READ-ONLY: two captures + verify only; self-attested in §5 |

Revision linkage (rule #14): EX-21's seat report (`seats/EX-21.md`) records the same
BEFORE rev `7cd19c3c…` (1155 lines / 54279 B) as the round's before-side, and the r3
records (`arc3-loop1-round3/claims/c2/`) pin the same digest as the r3 landing. So this
before-state is the revision the C3 claim's "before" names.

Method: every case runs against scratch fixtures under `/var/tmp/ex22-baseline/work/`,
with the tool executed from a byte-identical `/var/tmp` copy. No custody path was opened
for writing by any command below. Re-runs used `cwd` = the kaidoku repo so each receipt's
`# repo-HEAD:` line records the repo revision (`a1r`, `c1r`, `c3r` transcripts); the first
(a)-run's receipt recorded the outer `shokunin` repo HEAD `46904d90…` because `cwd` was
`/home/vgpnk/Projects/shokunin` — noted, and superseded by the `a1r` rerun.

## 1. Case (a) — sidecar-scope injection: the derived sidecar is never scope-checked

The guard examines `--out` only (grep `transcripts/b6-traceback-line-check.txt` shows the
guard block; `transcripts/aA-control-direct-refusal.txt` shows it refusing `--out X
--paths X`). The sidecar `out.with_name(out.name + ".sha256")` is written **unguarded**.

### (a1) `--paths X.sha256 --out X` → the sidecar clobbers the measured file itself

```
$ python3 /var/tmp/ex22-baseline/tool/custody-pair.py capture \
      --paths /var/tmp/ex22-baseline/work/a/vic.sha256 --out /var/tmp/ex22-baseline/work/a/vic
RECEIPT: /var/tmp/ex22-baseline/work/a/vic  sha256=de0bf33b0fd3783321095e8f0233ddfa4359dd264e008352bf98a5d25816ba4b
SIDECAR: /var/tmp/ex22-baseline/work/a/vic.sha256
CUSTODY_PAIR_CAPTURE: OK paths=1/1 label=(none) exit=0
[exit-status] 0
```

The measured file before: sha256 `2a7f8b6b6e1a153e0aefacdfc6185e552bd849709bc7964a1c2ae8c82865d65a`
(70 B, `1111…1111  vic`). After the clean-exit run:

```
$ cat /var/tmp/ex22-baseline/work/a/vic.sha256
de0bf33b0fd3783321095e8f0233ddfa4359dd264e008352bf98a5d25816ba4b  vic
$ sha256sum /var/tmp/ex22-baseline/work/a/vic.sha256
b902dfa85930732729347046a693540e1beeb71c2026d3758011a66975fdb944  /var/tmp/ex22-baseline/work/a/vic.sha256
```

(`transcripts/a1-…`, `a2-after-ls.txt`, `a2b-after-cat.txt`, `a2c-after-sha.txt`.)

The receipt's own stanza recorded the **pre-clobber** bytes it then replaced
(`transcripts/a1b-receipt-vic-body.txt`: `SHA256: 2a7f8b6b…`), and `verify --live` now
reads the destroyed file as drift — the tool's own clean-exit run broke its own receipt:

```
$ python3 …/custody-pair.py verify /var/tmp/ex22-baseline/work/a/vic --live
PATH /var/tmp/ex22-baseline/work/a/vic.sha256: CONTENT-DRIFT  compared=11/11 moved=sha256
SHA256-CONTRACT: 0/1 paths agree on sha256 (v1/v2 receipts compare on this field)
VERDICT: CONTENT-DRIFT  paths=1  CONTENT-DRIFT=1  exit=10
[exit-status] 10
```
(`transcripts/a3-consequence-verify-live.txt`.)

Rerun with repo `cwd` (clean provenance): `--paths …/vr.sha256 --out …/vr` → exit 0,
`SIDECAR: …/vr.sha256`, `vr.sha256` content replaced by `b790a021…  vr`
(`transcripts/a1r-inject-repo-cwd.txt`, `a1r-after-cat.txt`, `a1r-after-sha.txt`,
`a1r-receipt-head.txt` — receipt `# repo-HEAD: 015e1bab…`, `# tool: … 7cd19c3c…`).
Fixture preserved as `fixtures/clobbered-vr.sha256` (`a4e50bc2…`).

### (a2) same shape, second instance (independent fixture)

`--paths …/vic2.sha256 --out …/vic2` → exit 0; `vic2.sha256` `014aa63e…` → `feb18966…`
(`transcripts/a5-inject2-same-shape.txt`, `a6-after2-sha.txt`). Receipt body in
`a6b-after2-cat-vic2.txt` (its `# repo-HEAD: 46904d90…` line reflects the outer-repo
`cwd`; noted in §0). Fixture preserved as `fixtures/clobbered-vic.sha256` (`b902dfa8…`).

### (a3) reverse direction — `--out X.sha256 --paths X` (sidecar-shaped neighbour as target)

`--paths …/vic3 --out …/vic3.sha256` → exit 0; the measured file `vic3` is untouched
(`5661a703…` before and after), but its sidecar-shaped neighbour `vic3.sha256`
(`d05beeff…` = `3333…3333  vic3`) is replaced by the receipt, and a further
`vic3.sha256.sha256` appears (`transcripts/a8-inject3-out-sidecar-shaped.txt`,
`a9-after3-ls.txt`, `a9b-after3-sha.txt`). This is the "aim a derived sidecar at a
measured file's neighbour" vector named in the frozen claims.

### (a4) control — the direct form is refused (so the hole is scope, not a missing guard)

```
$ python3 …/custody-pair.py capture --paths …/vic3 --out …/vic3
USAGE: refusing to write a receipt over a path it measures or a custody path (path or inode): …/vic3
[exit-status] 2
```
(`transcripts/aA-control-direct-refusal.txt`.)

## 2. Case (b) — `out.parent.mkdir` outside the guarded `try`: raw traceback, exit 1

`--out <regular-file>/sub/r.txt`:

```
$ python3 …/custody-pair.py capture \
      --out /var/tmp/ex22-baseline/work/b/blocker/sub/r.txt --paths /var/tmp/ex22-baseline/work/b/blocker
Traceback (most recent call last):
  …
  File "/var/tmp/ex22-baseline/tool/custody-pair.py", line 653, in cmd_capture
    out.parent.mkdir(parents=True, exist_ok=True)
  File "/usr/lib/python3.14/pathlib/__init__.py", line 1011, in mkdir
    os.mkdir(self, mode)
NotADirectoryError: [Errno 20] Not a directory: '/var/tmp/ex22-baseline/work/b/blocker/sub'
[exit-status] 1
```
(`transcripts/b1-mkdir-traceback.txt`; line anchor re-checked at run time by
`b6-traceback-line-check.txt` → `653: out.parent.mkdir(parents=True, exist_ok=True)`.)

Exit 1 is **outside the declared exit map** (README "Exit codes" table: 0, 2, 3, 10–14).
The existing `try/except OSError` covers only the two `write_text` calls, not the `mkdir`
above them. Controls: `--out <the measured file itself>` → USAGE exit 2 (the guard fires
before the mkdir — `b3-control-declared-path.txt`); a creatable path still works —
`--out …/fresh2/deep/r.txt` → receipt written, exit 0 (`b5-control-normal-mkdir-clean.txt`).
The failure leaves no partial write (`b2-after-ls.txt`: only `blocker` remains).

## 3. Case (c) — coverage gate counts stanzas, not distinct paths

`reference_coverage()` decides with `len(ref_sections) >= required` while its own
`unaccounted:` list is computed over resolved-path identity — so a reference padded with
duplicate stanzas for ONE path passes `--require-paths 5` **silently** (0
`REFERENCE-COVERAGE` lines; the line is printed only on the failure path).

### (c1) v2 duplicate-stanza receipt

`capture` a 1-path receipt, then pad its stanza 5×:

```
$ grep -c '^PATH:' /var/tmp/ex22-baseline/work/c/c1-dupe5.txt
5
$ python3 …/custody-pair.py verify /var/tmp/ex22-baseline/work/c/c1-dupe5.txt --live --require-paths 5
A (reference): /var/tmp/ex22-baseline/work/c/c1-dupe5.txt  stanzas=5
PATH /var/tmp/ex22-baseline/work/c/ref1.conf: MATCH  compared=11/11
SHA256-CONTRACT: 1/1 paths agree on sha256 (v1/v2 receipts compare on this field)
VERDICT: MATCH  paths=1  MATCH=1  exit=0
[exit-status] 0
```
(`transcripts/c2b-dupe-stanza-count.txt`, `c3-dupe-gate-pass.txt`; grep:
`c3r2-grep-coverage.txt` → `0` coverage lines. Repo-`cwd` rerun: `c1r`, `c2r`, `c3r`.)

### (c2) v1 sums duplicate-stanza receipt

Five identical sums lines for one path:

```
$ python3 …/custody-pair.py verify /var/tmp/ex22-baseline/work/c/c1-sums-dupe5.txt --live --require-paths 5
A format: sums-v1   B format: live
A (reference): …  stanzas=5
PATH /var/tmp/ex22-baseline/work/c/ref1.conf: MATCH-V1-PARTIAL  compared=1/11
VERDICT: MATCH-V1-PARTIAL  paths=1  MATCH-V1-PARTIAL=1  exit=0
[exit-status] 0
```
(`transcripts/c5-sums-dupe-build.txt`, `c5b-sums-dupe-cat.txt`, `c6-sums-dupe-gate-pass.txt`.)

### (c3) the strongest instance — padded **canonical** receipt

One real custody path (`~/.bashrc`) captured, stanza padded 5× → gate passes:

```
$ python3 …/custody-pair.py verify /var/tmp/ex22-baseline/work/c/bashrc-dupe5.txt --live --require-paths 5
PATH /home/vgpnk/.bashrc: MATCH  compared=11/11
VERDICT: MATCH  paths=1  MATCH=1  exit=0
[exit-status] 0
```
(`transcripts/cE-canonical-1of5-capture.txt`, `cF-canonical-1of5-padded.txt`,
`cG-canonical-padded-gate.txt`.) A gate consumer asking "are all 5 custody paths covered"
gets exit 0 with four of them never examined.

### (c4) r3 fixtures and the same-second control

- EX-24's `v2-dupe-5x.txt` (r3 fixture): `verify … --live --require-paths 5` → exit 0,
  `MATCH paths=1/1`, 0 coverage lines (`c9-ex24-fixture.txt`).
- EX-24's `v1-dupe-5x.txt`: `MATCH-V1-PARTIAL exit 0` (`cD-ex24-v1-dupe.txt`).
- **Control, same fixture family, un-padded:** the 1-stanza receipt → USAGE exit 2 with
  `REFERENCE-COVERAGE: 1/5 paths present in reference; unaccounted: …` and
  `USAGE: reference covers 1 of the required 5 paths` (`c4-control-1of5-gated.txt`,
  `cH-canonical-1of5-gated-control.txt`). So the gate works on the count it intends to
  enforce; the hole is that the count is stanza multiplicity.
- A 5-distinct-scratch-path receipt → exit 0 `MATCH 5/5` (`c7-capture-5scratch.txt`,
  `c8-unrelated-gate-pass.txt`) — the declared D3 semantics, unchanged; not a defect.

## 4. Discrimination check vs the in-flight r4 revision (`29bb45ae…`) — advisory

After EX-21's landing (14:09:25Z), the same three injections were re-run **on a scratch
copy** of `29bb45ae…` (`/var/tmp/ex22-baseline/tool2/`; sha re-derived, `zT`):

| probe | BEFORE `7cd19c3c…` | in-flight `29bb45ae…` |
|---|---|---|
| (a) `--paths vi.sha256 --out vi` | exit 0, measured file destroyed (§1) | **exit 2**, `USAGE: refusing to write a receipt or its derived sidecar …: …/vi.sha256`, file intact (`f1-…`, `f1b-…`) |
| (b) `--out blocker/sub/r.txt` | traceback exit 1 (§2) | **exit 2**, `USAGE: cannot create the receipt directory ([Errno 20] …)` (`f2-…`) |
| (c) padded dupe ×5 `--require-paths 5` | exit 0, 0 coverage lines (§3) | **exit 2**, `USAGE: reference covers 1 of the required 5 distinct paths` + `REFERENCE-COVERAGE: 1/5 …` (`f3-…`) |
| selftest | `CLEAN cases=22 passed=22 failed=0 exit=0` (`s1-selftest.txt`) | `CLEAN cases=28 passed=28 failed=0 exit=0` (`f0-selftest-inflight.txt`) |

This is not part of the before-state; it is recorded so the chain's before→after pair is
traceable end to end from this artifact alone.

## 5. Read-only self-attestation on the real custody paths

Two read-only captures of the 5 real paths (receipts written to scratch), 1 s apart,
plus verify:

```
RECEIPT: …/work/live/pre.txt   sha256=ac0d2528e7af84055b8a789b0d11ddf779ae27a1dd059f8c522efe33a8eb536a
RECEIPT: …/work/live/post.txt  sha256=9969dae93b467b2c1dc29a12722194cd47174d0e69ebd3373b7387e00a9d6e41
CUSTODY_PAIR_CAPTURE: OK paths=5/5 exit=0  (both)
$ python3 …/custody-pair.py verify pre.txt post.txt --require-paths 5
PATH /home/vgpnk/.config/devin/mcp_config.json: MATCH  compared=11/11
PATH /home/vgpnk/.omp/agent/mcp.json: MATCH  compared=11/11
PATH /home/vgpnk/.kimi-code/config.toml: MATCH  compared=11/11
PATH /home/vgpnk/.bashrc: MATCH  compared=11/11
PATH /home/vgpnk/.profile: MATCH  compared=11/11
VERDICT: MATCH  paths=5  MATCH=5  exit=0
```
(`transcripts/l1-…l7`; receipts + sidecars preserved in `receipts/`; sidecars
`sha256sum -c` OK — `l5-sidecar-check.txt`.) 11/11 fields compared per path
(inode/ctime/mtime/mode included), so a write by any actor inside the window would have
surfaced. This is this seat's own read-only attestation, not the round's live pair
(EX-21's deliverable, `claims/c3/EX-21/receipts/`).

## 6. Attacks / refutations attempted, with verdicts

| # | attack on this before-state | result | verdict |
|---|---|---|---|
| A1 | the (a) clobber is a fixture artifact — maybe `vic.sha256` was never measured | receipt stanza records `PATH: …/vic.sha256`, `SHA256: 2a7f8b6b…` (pre-clobber); post-run digest `b902dfa8…` differs; `verify --live` → CONTENT-DRIFT | refuted; the measured file was destroyed by the run |
| A2 | `exit 0` from (a) is fine because the tool is "read-only over every path it inspects" | the sidecar write is a **write**, not an inspection; README's read-only claim is about the instrument's inspect pass, and the clobber happens in the same clean-exit run | hole stands |
| A3 | (a) needs `--paths X.sha256` — an unnatural invocation | (a3) shows the reverse spelling (`--out X.sha256 --paths X`) destroys the neighbour; both spellings exit 0 | hole stands, both directions |
| A4 | the (b) traceback is specific to a missing directory | a regular file as a parent **component** (NotADirectoryError) is the measured case; the class is any uncreatable parent | hole is the unguarded `mkdir` |
| A5 | (c) is refuted because `--require-paths` without padding correctly exits 2 | control c4/cH: un-padded 1-of-5 → exit 2. The padded receipt is built by the tool itself (capture) then replicated — no field is tampered; the gate is what fails to see it | hole stands (count basis) |
| A6 | I tested a modified tool | copy sha256 == repo sha256 == HEAD blob `7cd19c3c…`, re-derived before and after (`0i`, `0j`, `0g`, `zQ`, `zR`); `cmp` exit 0 (`0l`) | refuted |
| A7 | the round's "before" rev differs from mine | EX-21's report names `7cd19c3c…` (1155 lines) as the before-side; r3 records pin the same digest | refuted; same revision |
| A8 | my before-state is stale because the tool changed under me | change at 14:09:25Z (`29bb45ae…`) landed **after** all injections (14:08:24–14:09:18Z); the executed copy remained `7cd19c3c…` byte-identical all session (`zQ`); §4 re-runs the same probes on the new revision and they close — so the before/after pair is clean | refuted; churn is temporal, not contamination |
| A9 | the in-flight revision might silently keep the holes (my probes only test three spellings) | its selftest grows to 28 cases including `coverage-gate-rejects-duplicate-stanzas`, `refuses-sidecar-over-measured-file`, `refuses-receipt-over-sidecar-neighbour`, `out-parent-not-a-directory-usage-exit` (f0 transcript); still, only the chain's own reviewers can close the claim | recorded as advisory only |

## 7. Before → after table for the chain's claim (c3 = EX-21's landing)

| item | BEFORE (this seat, rev `7cd19c3c…`, verbatim above) | declared AFTER (C3 claim) |
|---|---|---|
| (a) sidecar scope | derived sidecar written unguarded; `--paths X.sha256 --out X` → exit 0, X destroyed; `--out X.sha256 --paths X` → neighbour destroyed | USAGE 2 refusal; measured file and neighbours intact |
| (b) `out.parent.mkdir` | traceback exit 1 (outside declared map) | USAGE 2 with message |
| (c) coverage gate | `len(ref_sections) >= required` — padded 5× dupe passes exit 0, 0 coverage lines | distinct-path count; padded dupe → exit 2 |
| selftest case count | `CLEAN cases=22 passed=22 failed=0 exit=0` | ≥24 with new fixtures (in-flight: 28) |
| live pair on the 5 paths | MATCH 5/5 (this seat's read-only attestation, §5) | round's live pair MATCH 5/5 vs the revised tool |
| command A / other chains | untouched by this seat (writes only under `claims/c3/EX-22/` + seat report) | unchanged |

## 8. Transcripts & reproduction

`transcripts/` holds 108 files: one raw capture per command (`$ <argv>`,
combined stdout+stderr, `[exit-status] N`; re-runs also carry `cwd=`), the live-pair
receipts' hashes, the fixture digests, the identity re-derivations (`z*`), the in-flight
discrimination probes (`f*`), and the `git` provenance of the BEFORE rev. Machine list:
`sha256s.txt` (this directory; re-generated after this file). Fixtures of record:
`fixtures/clobbered-vic.sha256` (`b902dfa8…`), `fixtures/clobbered-vr.sha256`
(`a4e50bc2…`), `fixtures/c1-dupe5.txt` / `c1r-dupe5.txt` / `c1-sums-dupe5.txt` /
`bashrc-dupe5.txt` (padded references), `fixtures/vr` (the receipt whose sidecar
clobbered `vr.sha256`). Harness: `harness/run.sh`, `harness/run2.sh`,
`harness/build_dupe.py` (reproduce everything from a fresh `/var/tmp/ex22-baseline`).

Reproduction sketch:

```bash
S=/var/tmp/ex22-baseline        # scratch root; never /tmp (EDQUOT)
mkdir -p $S/tool && cp <repo>/.ufo/gates/custody-pair/custody-pair.py $S/tool/
# (a) printf '1111…  vic\n' > $S/work/a/vic.sha256;
#     capture --paths $S/work/a/vic.sha256 --out $S/work/a/vic   → exit 0, vic.sha256 clobbered
# (b) printf 'regular\n' > $S/work/b/blocker;
#     capture --out $S/work/b/blocker/sub/r.txt --paths $S/work/b/blocker → traceback, exit 1
# (c) capture --out $S/work/c/rec.txt --paths $S/work/c/ref1.conf;
#     python3 build_dupe.py $S/work/c/rec.txt $S/work/c/dupe5.txt;
#     verify $S/work/c/dupe5.txt --live --require-paths 5 → exit 0, 0 coverage lines
```

No blockers. Nothing in this seat's evidence depends on another seat's output; the
before-state is reproducible from the HEAD blob `7cd19c3c…` alone.
