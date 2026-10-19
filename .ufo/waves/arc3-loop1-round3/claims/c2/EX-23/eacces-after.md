# EX-23 — AFTER-STATE EACCES fixture on the REVISED custody tool (chain c2)

Seat EX-23 (chain c2, executor, LATE JOIN), wave `arc3-loop1-round3`, 2026-10-19.
Task: on `/var/tmp` copies of the **revised** tool, the declared class must fire for the
exists-but-EACCES fixture and there must be **no fail-open MATCH**; compare against the
before-state in `claims/c2/EX-22/baseline.md`.

**Status: this seat COMPLETED missing work** (the `claims/c2/EX-23/` dir did not exist and
`seats/EX-23.md` was absent; `.ufo/waves/arc3-loop1-round3/claims/cross/wave-summary.md:37`
lists EX-23 among the undelivered c2 seats). No landed work was redone; the before-state
differential below is new measurement that EX-22's baseline did not run (it measured the
before rev only). Nothing in `.ufo/gates/custody-pair/` was written, renamed or `utime`d by
this seat — read-only sha256/`stat` captures only.

## 0. Identity & scope (rule #14 — every byte-identity below re-derived at write time)

| item | value | how re-derived |
|---|---|---|
| repo | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` | — |
| repo HEAD | `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` | `git rev-parse HEAD` (`transcripts/identity-after.txt`) |
| **AFTER rev** (revised tool) | sha256 `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`, 1155 lines | `sha256sum` of the worktree file **and** of the `/var/tmp` copy actually executed — digests equal (`identity-after.txt`) |
| **BEFORE rev** | sha256 `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`, 889 lines | `git cat-file -p HEAD:….py \| sha256sum` → same digest; copy executed = `…/tool/custody-pair.before.py` |
| mutation copy | sha256 `85dd8cd3f8e957df5887ad61198e7c25fe2a7dcd56cda1b2ca8878f9080bd0bc` | parser arms neutered in a scratch copy (see §3) |
| README (same commit) | sha256 `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193` | `sha256sum` (read-only) |
| working copies executed | `/var/tmp/ex23-after/tool/{custody-pair.py, custody-pair.before.py, custody-pair.mut-noparser.py}` | all three re-hashed after the session (`sha256s.txt`) |
| host / user / kernel / python | `plazir27` / `vgpnk` (uid 1000, **non-root** — EACCES is reachable) / `7.2.3-arch1-3` / `3.14.7` | `id`, `uname -r`, `python3 --version` |
| scratch | `/var/tmp/ex23-after` (never `/tmp`) | — |
| custody paths | READ-ONLY: capture/verify only; self-attested in §7 | — |

The declared contract this fixture tests is the tool's own: exit class `14 UNEVALUABLE` —
"a path exists but could not be evaluated (EACCES on open, or a stat error other than
ENOENT); the receipt is still written, carrying STAT-ERROR/READ-ERROR" and "`verify` never
reads such a path as `MATCH`" (docstring `custody-pair.py:103-105`; `README.md:122`).
Severity precedence `CONTENT-DRIFT > UNEVALUABLE > ABSENT > … > MATCH` (`:115`, `README.md:131`).

## 1. Claim clause — the declared class fires, no fail-open MATCH

Fixture `/var/tmp/ex23-after/work/a/noaccess/secret.conf`, 15 bytes, sha256
`ab7ef8904c06161234c178b820e6121f55ee9952156d930b696e51aaff7241e6` — **the same payload
digest EX-22's before-state used** (`baseline.md:45`), with the containing directory at mode
`000` so `lstat` itself fails (the exists-but-unreadable shape, `baseline.md:36-38`).

Existence proof across the whole case (kills the "the fixture was really absent" reading):

```
$ stat -c 'name=%n inode=%i size=%s mtime=%Y' …/a/noaccess/secret.conf      # before chmod
name=/var/tmp/ex23-after/work/a/noaccess/secret.conf inode=11389938 size=15 mtime=1792416164
ab7ef8904c06161234c178b820e6121f55ee9952156d930b696e51aaff7241e6  …/a/noaccess/secret.conf
$ stat …/a/noaccess/secret.conf                                             # after chmod 000
stat: cannot statx '…/a/noaccess/secret.conf': Permission denied   [exit-status] 1
$ python3 -c "os.lstat(...)" → PermissionError: [errno 13] Permission denied   [exit-status] 1
$ stat -c … …/a/noaccess/secret.conf                                        # after verify, dir restored
name=… inode=11389938 size=15 mtime=1792416164   (a7-post-stat.txt)
ab7ef890…  (a7-post-sha256.txt)                                             # (a7) unchanged
```

Capture and verify, revised tool (`transcripts/a2-…`, `a3-…`, `a4-…`, `a5-…`):

```
$ python3 …/tool/custody-pair.py capture --out …/work/a/a-rec-A.txt --paths …/noaccess/secret.conf
RECEIPT: …/a-rec-A.txt  sha256=15404cd91cbd60f29681224ca642966b375ff633a1f6d0299085a7be61b5add5
SIDECAR: …/a-rec-A.txt.sha256
CUSTODY_PAIR_CAPTURE: UNEVALUABLE paths=0/1 label=(none) exit=14
[exit-status] 14

$ python3 …/custody-pair.py verify …/a-rec-A.txt --live
PATH …/noaccess/secret.conf: UNEVALUABLE  compared=0/11 moved=unevaluable
    note: exists but not evaluable on reference+candidate side
VERDICT: UNEVALUABLE  paths=1  UNEVALUABLE=1  exit=14
CUSTODY_PAIR_VERIFY: UNEVALUABLE paths=0/1 drift=1 exit=14
[exit-status] 14

$ python3 …/custody-pair.py verify …/a-rec-A.txt …/a-rec-B.txt      # receipt-vs-receipt
PATH …/noaccess/secret.conf: UNEVALUABLE  compared=0/11 moved=unevaluable
VERDICT: UNEVALUABLE  paths=1  UNEVALUABLE=1  exit=14
[exit-status] 14
```

The receipt body carries the marker the parser keys on, and self-pins the revised tool:

```
# tool: custody-pair.py  sha256 7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09
PATH: /var/tmp/ex23-after/work/a/noaccess/secret.conf
EXISTS: no
STAT-ERROR: [Errno 13] Permission denied: '/var/tmp/ex23-after/work/a/noaccess/secret.conf'
```

Sidecar == receipt digest, re-derived (`sha256sum` → `15404cd9…` == the sidecar's first field);
receipt `# tool:` line == independent `sha256sum` of the tool. **The declared class fires
(capture 14, verify 14) and no fail-open MATCH occurs in either verify mode.**

## 2. Before → after differential (identical fixture shapes, same inputs)

The strongest form: the *same* fixture construction and payload digest, run on both
revisions; plus EX-22's own recorded artifact receipt fed to the revised tool.

| case | BEFORE rev `112d01dc…` | AFTER rev `7cd19c3c…` |
|---|---|---|
| capture, blocked parent dir | `PARTIAL paths=0/1 exit=13` (`d-before-capture.txt`) | `UNEVALUABLE paths=0/1 exit=14` (`a2-…`) |
| verify `--live` | **`MATCH … exit=0`** (`d-before-verify-live.txt`) | `UNEVALUABLE … exit=14` (`a3-…`) |
| verify receipt-vs-receipt | **`MATCH … exit=0`** (`d-before-verify-pair.txt`) | `UNEVALUABLE … exit=14` (`a5-…`) |
| receipt tag printed | `A format: v1-stanza` (the EX-22 E2 mislabel) | `A format: v2` (honours the header version) |
| EX-22's artifact receipt (`52dee497…`, self-pins the BEFORE tool) vs `--live` | `ABSENT exit=13` (`x1-before-…`) | **`UNEVALUABLE exit=14`** (`x1-revised-…`) |
| EX-22's artifact receipt vs itself | — | `UNEVALUABLE exit=14` (`x1-revised-…-pair`) |

Reproduction check on the before rev: my `d-before-verify-{live,pair}` transcripts are
line-for-line identical to EX-22's recorded `a3-verify-live.txt` / `a5-verify-pair.txt` after
normalising only the fixture directory letter (`a/` vs `d/`) — i.e. the before-state fail-open
is independently reproduced by this seat, not merely quoted.

Cross-revision reading (measured, not assumed): the revised tool reads a **pre-revision**
receipt whose stanza says `EXISTS: no` + `STAT-ERROR:` and classifies it UNEVALUABLE rather
than trusting the false absent field — the receipt-vs-live case where the candidate side is
genuinely unreadable still exits 14.

## 3. Mutation proof — the parser arm is load-bearing (for receipt-side evidence)

Scratch copy with only the two parser arms neutered
(`"stat_error"/"read_error"` regexes renamed so they can never match), digest
`85dd8cd3…` — nothing else changed:

| run | result |
|---|---|
| receipt-vs-receipt on the EACCES fixture | **`MATCH exit=0`** (`a11-mut-noparser-verify-pair.txt`) — the fail-open returns |
| `--live` with the fixture blocked | `UNEVALUABLE exit=14` (`a11c-…`) — still closed |
| `--live` with the fixture restored readable | `ABSENT exit=13` (`a11b-…`) |

Reading: the parser arm is the *only* thing standing between a parsed receipt and the
fail-open in receipt-vs-receipt mode; in `--live` mode the candidate side is re-derived by
`capture_path`, which carries the error itself, so the arm is not needed there. This matches
RV-6's mutation finding ("A5 explicitly refutes that EX-40's patch alone closes D2 — the
parser arm was required", `seats/EX-21.md:126`) and localises *where* it is required.

## 4. Controls — the closure is not over-refusal

| control | result |
|---|---|
| readable file, same tool, same flow | `MATCH compared=11/11 exit=0` (`a8b-…`) |
| genuinely absent path (ENOENT, no marker) | capture `ABSENT exit=13`; verify-vs-live `MATCH exit=0` with `compared=0/11` (`a9b-…`) — the declared absent/absent contract, not swallowed by 14 |
| blocked receipt vs clean receipt (either side) | `UNEVALUABLE exit=14` both orders (`a10b-…`, `a10c-…`) |
| selftest at this revision | `CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0` (`selftest-after.txt`) |
| 5 canonical custody paths, two read-only captures 1 s apart | `MATCH 5/5 exit=0`, 11/11 fields each (`ro3-verify-pair.txt`) |
| traceback sweep over all after-state transcripts | revised tool: **0 tracebacks** in every run; the only traceback in the tree is the BEFORE rev's file-mode-000 capture (`b2-before-…`), reproduced for contrast |

## 5. Negative-space sweep — hunting a counterexample

Every plausible invocation of the revised tool against the EACCES fixture, looking for any
`rc==0` (a MATCH would be a counterexample to the claim): `verify --live`;
`--live --require-paths 1`; `--live --require-paths 5`; reversed pair; self-pair;
EX-22-artifact pair; `capture --out -`; EX-22-artifact vs live. Result — `sweep-summary.txt`:
`14, 14, 2, 14, 14, 13, 14, 14`; **`grep -l 'VERDICT: MATCH' s0*.txt` → (none)**. The only
`rc==0` runs anywhere in this seat's after-state set are the controls of §4, the before-rev
differential of §2, the two residuals of §6, and the selftest's own internal cases.

## 6. Attacks / refutations attempted, with verdicts

| # | attack on my own after-state | result | verdict |
|---|---|---|---|
| A1 | the fixture was really absent, so 14 is trivially right | inode `11389938` + sha256 `ab7ef890…` identical before/during/after (`a7-*`) | refuted; path existed throughout |
| A2 | 14 is the ABSENT class wearing a new name | distinct classes measured side by side: ENOENT → `ABSENT 13`, EACCES → `UNEVALUABLE 14` (`a9-*` vs `a2/a3`) | refuted; classes are distinct and the precedence is declared |
| A3 | the closure only works in `--live` (candidate re-derived), not on receipts | receipt-vs-receipt on the EACCES fixture → 14 (`a5-…`), and EX-22's artifact receipt → 14 (`x1-revised-…`) | refuted; receipt mode closed |
| A4 | the parser arm is decorative — the closure is really the capture-side change | neutering only the parser arms restores `MATCH exit=0` in receipt mode | **confirmed load-bearing** (§3); in `--live` the arm is redundant by construction |
| A5 | the closure over-refuses legitimate receipts | readable control `MATCH 0`; 22/22 selftest; live pair 5/5 | refuted |
| A6 | I measured a mutated tool | all three executed copies re-hashed after the session; after copy == repo file == `7cd19c3c…` | refuted |
| A7 | EX-22's "before" rev differs from mine | git HEAD blob re-hashed to `112d01dc…` in this session; their baseline pins the same digest | refuted; same revision |
| A8 | a hand-stripped receipt (no marker) still fails open | **reproduced, twice** (`t2`, `t4`) — see §6.1 | hole exists in a class *outside* the tool's own contract; see residual R1 |
| A9 | the E2 format mislabel hides the class | revised tool prints `A format: v2` on the same receipt that the before rev printed as `v1-stanza` | closed (matches EX-21 A5) |

### 6.1 Residuals — characterized, NOT claimed closed

- **R1 — hand-stripped receipt.** Deleting the `STAT-ERROR:` line from a genuine EACCES
  receipt and comparing it (`t2-stripped-vs-stripped`, `t4-handabsent-vs-live`) yields
  `MATCH compared=0/11 exit=0`: with the marker gone, the stanza is indistinguishable from a
  genuine ENOENT stanza, and `absent=absent` is the **declared** MATCH contract (the same
  class as RV-6's open A4, `seats/EX-21.md:130`). The claim's clause — "the declared class
  must fire and NO fail-open MATCH" — is about paths the tool itself recorded; a receipt
  edited after issuance is a different threat model. Practically, the tamper *is* detectable:
  the stripped file hashes to `17860154…` while its sidecar still pins `15404cd9…`
  (sidecar-vs-receipt mismatch). Patch-ready if the parent wants it: make `verify` refuse a
  receipt whose sidecar disagrees (or require the marker set on `EXISTS: no` stanzas) —
  outside this seat's write scope, so recorded as text only.
- **R2 — file-mode-000 shape (D2b) in the before rev crashes, after rev closes it.**
  Contrast measured: before rev `capture` → `PermissionError` traceback `exit 1`, and the
  subsequent `verify` → `USAGE exit 2` because no receipt was written (`b2-before-*`);
  revised → `UNEVALUABLE exit 14`, receipt written with `READ-ERROR`, verify 14 both modes
  (`b2-*`). Not a hole in the revised tool — recorded because EX-22's E1 predicted exactly
  this and the claim names D2b.
- **R3 — the revision is not the frozen instrument of the *round-2* tree.** Round-2 seats
  measured `112d01dc…`; this seat measures `7cd19c3c…` in the worktree, which is the wave's
  declared after-state (EX-21 owns the real path). If the parent lands a further revision,
  this artifact's after-state pins go stale — re-run the harnesses in `claims/c2/EX-23/*.sh`.

## 7. Read-only self-attestation on the real custody paths

Two read-only captures of the 5 canonical paths, verified against each other
(`ro1-…`, `ro2-…`, `ro3-…`): `VERDICT: MATCH paths=5 MATCH=5 exit=0`, 11/11 identity fields
per path, `SHA256-CONTRACT: 5/5`. A write by any actor inside that window — including this
seat — would have surfaced in inode/ctime/mtime. This is this seat's own attestation, not
the round's pre/post pair (EX-21's deliverable). No command in this seat wrote, renamed or
`utime`d any path under `.ufo/gates/custody-pair/`; `git status --short` there shows only
EX-21's ` M` entries plus the pre-existing untracked `__pycache__/`
(`transcripts/identity-after.txt`).

## 8. Evidence index

`transcripts/` — 58 files: one raw capture per command (`# cwd=…`, `$ <argv>`, combined
stdout+stderr, `[exit-status] N`), plus the artifacts of record
(`artifact-after-a-rec-A-receipt.txt` + sidecar = the EACCES receipt,
`artifact-after-b2-file000-receipt.txt` = the file-mode-000 receipt), the read-only pair
(`ro-pre.txt`, `ro-post.txt`), the identity re-derivation (`identity-after.txt`), the
traceback sweep and the negative-space summary (`sweep-summary.txt`). Harnesses:
`run.sh` (§1), `run2.sh` (§2), `run3.sh` (§3-4), `run4.sh` (§3-4 identity + attestation),
`run5.sh` (§5), `run6.sh` (§6.1). Digests: `sha256s.txt`.

Reproduce (scratch only, `/var/tmp`; the fixture digest is the one EX-22 used):

```bash
S=/var/tmp/ex23-after
mkdir -p $S/tool $S/work/a/noaccess && cp <repo>/.ufo/gates/custody-pair/custody-pair.py $S/tool/
git -C <repo> cat-file -p HEAD:.ufo/gates/custody-pair/custody-pair.py > $S/tool/custody-pair.before.py
printf 'secret-bytes-A\n' > $S/work/a/noaccess/secret.conf && chmod 000 $S/work/a/noaccess
bash <this-dir>/run.sh && bash <this-dir>/run2.sh && bash <this-dir>/run3.sh
bash <this-dir>/run4.sh && bash <this-dir>/run5.sh && bash <this-dir>/run6.sh
```

No blockers. Nothing here depends on another seat's output; every digest cited was
re-derived in this session.
