# SEAT CR-4 — chain c3, role critic (arc3-loop1-round2)

Seat line: *attack: do `cp -a`/`rsync -a`/backup-restore defeat inode/ctime
detection (preserved timestamps)? What is the tool's true residual threat model —
state it precisely; if the residual is large, say so. Seat report.*

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · 2026-10-19 · host kernel
7.2.3-arch1-3 · repo + scratch on btrfs · local TZ -03 · **no git mutation, no
real-target write, no install**. Instrument under attack pinned at
`custody-pair.py` sha256 `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`
(39157 B) — re-verified after every battery run, so every row is single-revision.

## 1. Work performed (evidence pointers)

Artifacts under `.ufo/waves/arc3-loop1-round2/claims/c3/CR-4/` (scratch under
`/var/tmp/cr4-arc3r2/`; `/tmp` never used):

| Artifact | What it is |
|---|---|
| `residual-threat-model.md` | the seat's core deliverable — the precise threat model, invisibility classes, and the size verdict (sha256 `02ab25eb…`) |
| `attack-matrix.txt` / `.json` | replica battery: 13 attack forms × {v1, v2-seconds, v2-nanoseconds} verdicts + per-field movement |
| `real-tool-battery.txt` | the same attacks against the landed tool, with exit codes, findings, field movement, and appended post-script rows |
| `receipts/` | pre/post receipts for the decisive attacks (`cp_a`, `erasure_samesec`, `custody-live-1/2`, `v1ref`, forged pair, `tar2.verify.txt`, real-v1-receipt verifies, guard, selftest) |
| `block-level/` | out-of-band erasure evidence on an ext4 image: `blk-sha-{pre,mid,post}`, `blk-receipt-{pre,mid,post}`, `blk-ctime-forged` |
| `second-precision-window.txt` | EXP1 (5 same-second erasure reps) / EXP2 (delayed) — sha256 `dece56b4…` |
| `toctou-measurement.py` | the capture-atomicity incidence probe (300 captures vs a live writer) — sha256 `66215fb1…` |
| `proposed-capture-atomicity.patch.md` | patch text (sha256 `9af5f09fca0de6979f6f87da9c57e06b1c82e972ccf185f7b757159813b2f435`) |
| `evidence-index.txt` | all artifact digests + re-runnable commands (sha256 `753ef2653285923bd2f92b08d0f832aff531b606524fec8ff4725482367a11a1`) |
| `tool-revision-pin.txt` | the revision every measurement was taken against |

Read-only custody discipline: the 5 custody paths were only `stat`ted/hashed by
this seat; their sha256 matched the round-1 canonical receipt **5/5** and their
inodes matched round-1's metadata capture (11341318 / 11341316 / 34530637 /
25991953 / 40274). Round-1 canonical v1 receipts were verified against the live
paths read-only. The destructive-write guard was exercised only on a
scratch-patched **copy** of the tool whose `CUSTODY_PATHS` constant points at
/var/tmp fixtures — the real paths were never handed to it.

Peer inputs read: `seats/EX-31.md` (implementer), `seats/EX-32.md` (authoritative
pre-pair), `seats/EX-33.md` (rewrite adversary) — my rows deliberately do not
repeat EX-33's six rewrite forms; they cover the restore-tool class, out-of-band
erasure, and capture atomicity. Polls at 09:0x–09:12 local saw 12 seat reports
landed; gaps named in §5.

## 2. Proposed changes

**Patch text** (this seat wrote nothing under `.ufo/gates/`; EX-31 owns the real
target):

* `claims/c3/CR-4/proposed-capture-atomicity.patch.md` — hash from a retained fd,
  re-stat the same fd after the read, record `stable:`, refuse/label an unstable
  capture; optional identity pins `st_dev`, `st_nlink`, `statx` btime; and
  "verify should fail closed on a `<receipt_a>.sha256` mismatch" (independent
  agreement with `seats/EX-33.md` §2).

Two wording corrections the records should take from this seat, not edits:

* the frozen claim's parenthetical "(inode/ctime movement)" must read **ctime**
  movement for the restore class — `cp -a`, `cp -p`, `rsync --inplace`, `tar` and
  in-place reflink all keep the **inode** (measured), so an inode-pinned receipt
  would be blind;
* "v1 receipts remain verifiable" is true for the sha256 field but must not be
  read as v1-referenced comparisons retaining v2 power (§3c).

## 3. Before → after measurement for the chain claim

C3 claim: *v2 receipt = sha256 + mtime epoch (UTC-rendered, correctly labeled) +
inode + ctime; label defect gone; a live same-content rewrite is detected
(inode/ctime movement); v1 receipts remain verifiable against the tool's sha256
fields; the round's own live pre/post pair (exit 0, 5/5) is captured by the tool.*

**(a) The claimed detection — measured against the landed tool**
(`real-tool-battery.txt`, receipts in `receipts/`):

| attack form (scratch fixture) | inode | sha256 | mtime | ctime | verdict |
|---|---|---|---|---|---|
| `cp -a` restore (timestamps preserved) | same | same | same | **moved** | 11 `moved=ctime_ns` |
| `cp -p` restore | same | same | same | **moved** | 11 |
| `cp -a --remove-destination` | **moved** | same | same | moved | 11 `moved=inode` |
| `rsync -a` default (temp+rename) | **moved** | same | same | moved | 11 `moved=inode` |
| `rsync -a --inplace` | same | same | same | **moved** | 11 `moved=ctime_ns` |
| `tar --overwrite` (extracts in place) | same | same | same | **moved** | 11 `moved=ctime_ns` |
| `cp --reflink=always` over the path | same | same | moved | moved | 11 `moved=mtime_ns,mtime_epoch` |
| in-place tamper → restore bytes → `touch -r` (same clock second) | same | same | same | **moved** | 11 `moved=ctime_ns` |
| in-place tamper persisting (control) | same | moved | moved | moved | 10 `CONTENT-DRIFT` |

Before-state (v1 surface, sha256-only, same fixtures — replica `attack-matrix.txt`):
**BLIND on 5/5 timestamp-preserving restore forms**, and the same-second erasure is
5/5 invisible at whole-second precision while **5/5 caught** at ns precision
(`second-precision-window.txt`). The tool compares `ctime_ns`
(`custody-pair.py:442-466`), which is why it is not blind.

**(b) The label clause — verified on the real defective receipts** (read-only):

```
$ python3 .ufo/gates/custody-pair/custody-pair.py verify \
      .ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt --live
exit=12 | PATH /home/vgpnk/.config/devin/mcp_config.json: METADATA-DRIFT  compared=5/11
       LABEL-DEFECT: MTIME_UTC says '2026-10-14 17:53:20' = localtime(epoch 1792011200);
                     gmtime(epoch) is '2026-10-14 20:53:20'      … 5/5 paths
# pipe shape: 10 such findings (mtime + ctime per path); sha256-CONTRACT 5/5 agree in both
```

**(c) The v1-interop clause — true, but scoped (the new finding):** the same-second
erasure verified against a v1 sha256-only reference returns **`MATCH-V1-PARTIAL`,
exit 0, `compared=1/11`**; against a v1 pipe stanza `compared=3/11` (sha256 + size
+ inode — and in-place restores preserve the inode). v2 discriminating power
exists only **v2↔v2**; the wave's custody argument must rest on the v2 pre-receipt
(EX-32's `claims/c3/receipts/config-pre-pair-v2.txt`), and exit 12 against the
round-1 canonical receipts must not be read as drift (it is the label audit
firing by design).

**(d) The round pair / live idempotence — independently re-measured:** two
read-only captures of the real 5 paths (mine, 09:0x) → `verify live1 live2` =
`MATCH 5/5, compared=11/11, exit 0`; the 5 sha256 match round-1's canonical
receipt 5/5 (`evidence-index.txt`).

## 4. Attacks / refutations attempted (with verdicts)

1. **`cp -a` / `cp -p` / `rsync -a` / `rsync --inplace` / `tar` / reflink restore
   (the seat-line attack).** Verdict: **do not defeat detection** — caught at exit
   11. But they **do defeat the inode pin** (inode preserved in 6 of 7 forms), so
   the claim must credit ctime. REFUTED as a bypass; REFINED in wording.
2. **Timestamp-preserving in-place erasure + `touch -r` (mtime restored exactly,
   content byte-identical).** Verdict: caught only because the comparison is
   nanosecond. At whole-second granularity: **BLIND 5/5** (EXP1) — this is the
   named risk if `CTIME_NS` is ever dropped from `COMPARE_KEYS`.
3. **Hardlink-swap-back (same inode presented again after tampering).** Verdict:
   the pure form (bytes restored) is row 8 above — caught via ctime; my heavier
   body left the attacker bytes in place and landed on `CONTENT-DRIFT` (10). No
   bypass.
4. **Out-of-band block-level erasure (ext4 image, unprivileged actor writing the
   data block directly).** Verdict: **DEFEATS the receipt completely — measured.**
   Content went `6e4192b7…` → `fb5b1a74…` and back to `6e4192b7…` with inode,
   ctime, mtime and size byte-identical throughout; the final receipt equals the
   initial receipt on **every pinned field including sha256**. Live-FS equivalents
   (root: btrfs/ZFS rollback, LVM/VM image revert, `dd` of a partition image) are
   the same class — named, not run.
5. **ctime forgery at the metadata layer.** Verdict: **works** —
   `debugfs -w -R "set_inode_field /custody.json ctime 20261014175320"` set an
   arbitrary ctime. ctime is unforgeable only against userspace (`utimensat`,
   `touch -r` all move it — measured).
6. **Receipt-store forgery.** Verdict: **works** — reference fields copied over
   the candidate receipt plus a regenerated `.sha256` sidecar → `verify` reports
   `MATCH`, exit 0 on a drifted path. The sidecar is not an anchor; only the
   commit / an independent capture is.
7. **Symlink-swap / type-confusion.** Verdict: **fails** — the tool uses
   `os.lstat` and pins `TYPE` (`custody-pair.py:193`); a swap is a custody event.
8. **Destructive-path attack (force the tool to write a receipt over a custody
   path).** Verdict: **refused, exit 2** ("refusing to write a receipt over a
   custody path"), fixture byte-unchanged — verified on a scratch-patched copy so
   the real paths were never at risk.
9. **Capture-atomicity (TOCTOU) race.** Verdict: **defect confirmed, no silent
   bypass measured.** `capture_path` = `lstat` then `sha256_file(path)` (a second
   path-based open, no post-read re-stat; `:189-225`, `:166-172`). 300 captures
   against a live writer: **2/300 receipts internally false** (size from one
   state, digest from another), 30/300 reads saw the inode move, 4/300 pre-stat
   mismatch. Patch text proposed; the harm is misclassification/false alarms, not
   an undetected tamper, because a mixed tuple still needs inode+ctime equality
   with the reference.
10. **Selftest audit.** Verdict: `CLEAN cases=15 passed=15 failed=0 exit=0` in my
    own scratch run. The one `FAIL` I first observed was **my own artifact** (I
    had renamed the copy; the TZ case re-invokes the script by its own path) —
    documented so no one mistakes it for a tool defect.

**Residual verdict (the seat's second question, stated plainly):** the residual
is **small for the threat model the instrument names** — no userspace writer
measured can touch a custody path (rewrite, restore, timestamp-preserve, swap,
reflink) without the v2 receipt declaring it; and it is **total against an actor
with root/raw-device access or write access to the receipt store**: such an actor
produces state-identical erasures (measured class) that no field-pinning receipt
can see, and can rewrite the receipt and its sidecar. In that class the tool is a
**tripwire for attribution, not an integrity control** — it cannot be the
defense, because it shares the trust domain with the thing it measures. Full
statement: `residual-threat-model.md` §4.

## 5. Blockers / gaps

* **None blocking.** Everything the seat line asked for was measured on this host.
* Gaps named, not papered over: (i) the snapshot/volume-revert instance of the
  out-of-band class is **named but not run** (root-only: `btrfs subvolume
  snapshot`/rollback); the ext4-image demo measures the primitive, not that
  live path. (ii) The TOCTOU incidence (2/300) was measured with a replica of the
  tool's capture pattern, not by racing the tool itself — the tool exposes no
  hook to force the interleaving, and its receipts cannot be audited for
  self-consistency externally. (iii) Poll movement during this seat's run: SC-4,
  PL-3, EX-40 and RV-12 reports landed after my first poll; **VZ-3 and RV-14
  reports were still absent at my final poll (26 seat reports present)**, and the
  `records-drafts/` updates landed without a report attached — my cross-checks
  therefore rest on EX-31/EX-32/EX-33 + the round-1 tree, and the parent should
  weigh any later c3 seat text against the revision pin. (iv) The
  tool revision is pinned at `112d01dc…`; if the parent lands the atomicity patch,
  the guard/selftest/battery rows here need a re-run against the new revision.
* One operational note for the parent's commit: `.ufo/gates/custody-pair/__pycache__/`
  and this seat's own scratch produce no commits — the gate dir should ship the
  tool + README only, and no `__pycache__` may enter the wave-artifacts commit.
