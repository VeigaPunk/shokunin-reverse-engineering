# CR-4 — residual threat model of the v2 custody receipt (chain c3, critic seat)

Instrument under test: `.ufo/gates/custody-pair/custody-pair.py`
rev **`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`**
(39157 B, mtime 2026-10-19 09:05:19 -03) — hash re-verified after every battery
run, so all rows below are single-revision. Commit-time hash may differ (the
parent lands the file); re-run the batteries if the code moves.

Compared field set (`custody-pair.py:145-155`, `:420-471`):
`sha256, size, inode, mtime_epoch, mtime_ns, ctime_epoch, ctime_ns, mode, uid,
gid, type` (11). Findings: `CONTENT-DRIFT` (10), `REWRITE-DRIFT` (11),
`METADATA-DRIFT` (12), `ABSENT` (13), `USAGE` (2). Scratch fixtures only — no
byte of any real custody path was written at any point (round-1 hashes were
re-verified read-only, 5/5, see `evidence-index.txt`).

## 1. The seat-line question, answered by measurement

*Do `cp -a` / `rsync -a` / backup-restore defeat inode/ctime detection
(preserved timestamps)?*

**No — they are all caught, but not by the inode.** Measured against the real
tool on scratch fixtures (`real-tool-battery.txt`, receipts under `receipts/`):

| attack (fixture) | inode | sha256 | mtime | ctime | tool verdict |
|---|---|---|---|---|---|
| `cp -a` restore (in-place truncate, timestamps preserved) | same | same | same | **moved** | 11 `REWRITE-DRIFT` `moved=ctime_ns` |
| `cp -p` restore | same | same | same | **moved** | 11 |
| `cp -a --remove-destination` (new inode) | **moved** | same | same | moved | 11 `moved=inode` |
| `rsync -a` (default: temp file + rename) | **moved** | same | same | moved | 11 `moved=inode` |
| `rsync -a --inplace` | same | same | same | **moved** | 11 `moved=ctime_ns` |
| `tar --overwrite` restore (GNU tar extracts in place) | same | same | same | **moved** | 11 `moved=ctime_ns` |
| `cp --reflink=always` over the existing path (btrfs) | same | same | moved | moved | 11 `moved=mtime_ns,mtime_epoch` |
| in-place tamper → restore bytes → `touch -r backup` (one clock second) | same | same | same | **moved** | 11 `moved=ctime_ns` |
| in-place tamper that persists (control) | same | moved | moved | moved | 10 `CONTENT-DRIFT` |

Two consequences the records must state exactly:

1. **The inode pin is decorative against every libc-level restore.** `cp -a`,
   `cp -p`, `rsync --inplace`, `tar` and in-place reflink all *preserve the
   inode*, and all preserve mtime; sha256 is unchanged by construction in a
   same-content restore. The only field that moves is **ctime** — the field no
   userspace API can set. A receipt carrying `{sha256, size, inode, mtime}`
   (i.e. v2 minus ctime, or any v1 shape) is **blind** to this entire class
   (measured: replica v1 surface `BLIND` on 5/5 restore forms,
   `attack-matrix.txt`). So the frozen claim's parenthetical
   "(inode/ctime movement)" must be read as **OR**, and the round report must
   credit **ctime**, not the inode, with closing the restore class.
2. The inode field is *not* useless: it is the field that catches replace-style
   restores (`cp -a --remove-destination`, default `rsync`) and it is the field
   that would catch a content replacement whose ctime was forged but whose inode
   number was not re-used (an FS-assigned value the attacker does not choose;
   EX-33 measured 0/200 inode re-use on this FS — agreement in
   `seats/EX-33.md` §3). The two fields are complementary; neither alone is the
   claim.

## 2. Precision is the whole pin

`custody-pair.py:442-466` compares `inode`/`mtime_ns`/`mtime_epoch` first, then
`ctime_ns`/`ctime_epoch`. Measured sensitivity: 20/20 consecutive in-place
identical rewrites on this btrfs host yield 20 distinct `ctime_ns` values
(min Δ 16 787 ns). Measured degenerate case: the same-second erasure
(tamper → restore bytes → `touch -r` to the exact original mtime) is

* **5/5 invisible** to a whole-second comparison (v1-shaped surface, and
  `ctime_epoch`-only comparisons), and
* **5/5 caught** by the ns comparison the tool actually performs
  (`second-precision-window.txt`, EXP1/EXP2).

Named risk for any future revision: dropping `CTIME_NS` from `COMPARE_KEYS` (or
comparing only the epoch) re-opens a one-clock-second invisible window at every
capture. Keep the ns key and keep it compared.

## 3. The v1-interop clause carries v1 power, not v2 power

Claim clause: "v1 receipts remain verifiable against the tool's sha256 fields."
**True, measured, and now scoped.** Against the round-1 canonical receipts with
`--live` over the real 5 paths, the sha256 contract is 5/5 agreed in every case;
the verdict is exit 12 only because the tool *detects the old label defect in
those files* (5 × `LABEL-DEFECT` for the stanza receipt, 10 for the pipe
receipt), not because of drift (`receipts/v1real-*.out`).

The scoping the records need: **v2 discriminating power exists only in a
v2↔v2 comparison.** Measured: the same-second erasure, verified against (a) the
round-1 `sums-v1` sha256-only list → `MATCH-V1-PARTIAL`, exit 0, `compared=1/11`;
(b) a v1 pipe stanza (sha256+size+inode compared, `compared=3/11`) → no drift
reported, because in-place restores preserve inode. So the wave's custody
argument must rest on the **v2 pre-receipt** (EX-31/EX-32 captured one:
`claims/c3/receipts/config-pre-pair-v2.txt`), never on a v1 reference. Also
operational: no v1 canonical receipt can ever verify to exit 0 (the label audit
fires by design) — exit 12 there must not be read as drift.

## 4. The residual threat model, stated precisely

The instrument is an **endpoint state comparator, not a write log**. Its
guarantee, stated with all its clauses:

> Given a pre-receipt that was captured honestly and anchored outside the writer's
> reach, the tool reports (exit ≠ 0, classed) any change to a pinned path that is
> **still visible in the pinned field set** at the post-capture instant — and, for
> every userspace writer measured, also any tamper-then-restore, because ctime
> moves on every in-place write and cannot be set from userspace.

Invisible classes — measured where a measurement was possible on an unprivileged
host, named otherwise:

1. **Out-of-band (block-level) state-identical erasure — MEASURED.** On an ext4
   image, writing the file's data block directly (`dd` at the block offset;
   unprivileged because the image is a scratch file) changed the content
   (`6e4192b7…` → `fb5b1a74…`) while **inode, ctime, mtime, size stayed
   byte-identical**, then restored the original bytes out-of-band: final receipt
   identical to the initial receipt on **every** field including sha256
   (`block-level/*`). An actor with raw-device / FS-image / snapshot access has
   an undetectable erasure channel. Live-FS instances of the same class (root
   required — **named, not run**): btrfs/ZFS subvolume rollback, LVM thin or VM
   disk-image revert, `dd` of a saved partition image.
2. **Metadata-layer ctime forgery — MEASURED PRIMITIVE.** `debugfs -w -R
   "set_inode_field <file> ctime <epoch>"` sets an arbitrary ctime on an
   unmounted image (demo: forced to `2026-10-14 14:53:20` while content was
   attacker bytes). ctime's unforgeability is a **syscall-level** property only.
3. **Receipt-store compromise — MEASURED.** Copying the reference receipt's
   pinned fields over the candidate receipt and regenerating the tool-written
   `.sha256` sidecar makes `verify` report **`MATCH`, exit 0** on a path whose
   content drifted (`receipts/forge-*.out`, `forged-post-receipt.txt`). The
   sidecar is not an anchor (same writer, same directory). The only real anchors
   are outside the writer's reach: the parent's commit of the pre-receipt, an
   independent seat's capture, or an out-of-band digest record.
   (Independent agreement: `seats/EX-33.md` §2 — `verify` should check the
   sidecar and fail closed; necessary, not sufficient, since the forger
   regenerates it.)
4. **Capture-window placement.** The pair certifies two instants. Anything that
   begins and ends before the pre-capture, or after the post-capture, is outside
   the instrument's epistemics. Do not read the pair as an audit trail.
5. **Capture atomicity defect (integrity of the receipt itself) — MEASURED.**
   `capture_path` takes `os.lstat(path)` and then calls `sha256_file(path)`,
   which opens the path **again** and never re-stats after the read
   (`custody-pair.py:189-225`, `:166-172`). A writer active inside that window
   yields a receipt whose metadata belongs to one state and whose digest belongs
   to another. Measured on the identical pattern (300 captures against a writer
   alternating 4 KiB/200 KiB contents): **2/300 receipts internally inconsistent
   (SIZE from one state, SHA256 from the other), 30/300 reads where the inode
   moved during hashing, 4/300 pre-`lstat` ≠ inode-at-read**
   (`toctou-measurement.py`). Verdict: a **defect, not a silent bypass** — a
   mixed tuple still needs inode+ctime equality with the reference to yield
   `MATCH`, and any tamper-and-restore moves ctime; the practical harm is a
   receipt that is internally false and classes it can misfire. Fix (patch text:
   `proposed-capture-atomicity.patch.md`): hash from a retained fd, re-stat that
   same fd after the read, and record/refuse on movement.
6. **Consumer resolution (scope note).** The receipt pins one path's bytes and
   metadata; it says nothing about which file a consumer of that config
   actually reads (include chains, env overrides, an alternate path). Outside
   the instrument's scope by construction; must not be claimed as covered.

**Size of the residual, honestly.** For the threat model this instrument names —
userspace writers, in-band tooling, accidental or semi-deliberate config drift —
the residual is **small and fully enumerated**: 9/9 measured attack forms are
caught, the three invisible classes require either raw-device/metadata control
(root) or write access to the receipt store, both of which are outside the
instrument's trust boundary. For an adversary **with root** the residual is
**total**: such an actor owns the receipt store, the tool, and the interpreter
that runs it, so no file-level receipt can be the control — the instrument is a
**tripwire**, and its value there is attribution and noise, not assurance. The
claim should land with the qualifier *"against userspace writers"*, and the
records must not present v2 as tamper-proof. That is the whole honest extent of
the "v2 closes attack 3" statement.

## 5. What the instrument gets right (credited, so the verdict is not one-sided)

* `os.lstat` + `TYPE`/`MODE`/`UID`/`GID` pins — a symlink swap is a custody event
  (`custody-pair.py:193`).
* Destructive-path guard: `capture --out` over a custody path is refused with
  exit 2 before any write. Verified on a **scratch-patched copy** of the tool
  (constant re-pointed to /var/tmp fixtures; the real paths were never handed to
  the guard): `USAGE: refusing to write a receipt over a custody path`, exit 2,
  fixture byte-unchanged (`receipts/guard.out`).
* Selftest independently re-run in a scratch sandbox: `CLEAN cases=15 passed=15
  failed=0 exit=0` (`receipts/selftest-scratchcopy-canonical.out`). The single
  FAIL I first saw was **my own artifact** — I had renamed the copy, and the
  TZ-independence case re-invokes the script by its own path; re-running under
  the canonical filename clears it. Renaming the file breaks that one case
  (harmless at the committed path).
* The tool records its own hash inside each receipt, and the label fix is
  TZ-independent by construction (`render_utc`, `custody-pair.py:174-176`).
* Read-only discipline is real: the tool never opens a custody path for writing,
  and the round's custody hashes re-verified 5/5 against the round-1 canonical
  receipt at my capture time (`custody-live-1/2.txt`, `evidence-index.txt`).
