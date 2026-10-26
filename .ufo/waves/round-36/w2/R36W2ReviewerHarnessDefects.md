# R36W2ReviewerHarnessDefects — wave-1 harness defects re-checked against the landed `c1-run.sh`

Seat: reviewer, kaidoku-shokunin round 36 wave 2 (falsify what wave 1 and the L1 landed). Scope:
`tools/round-36/c1-run.sh` vs the wave-1 findings in `.ufo/waves/round-36/w1/R36ExecHarnessRun.md`
(D-1, D-2, D-3, R-1, R-2, R-3) and `.ufo/waves/round-36/w1/R36ReviewerHarnessCode.md` (harness
portion of L1, plus its PASS verdicts); then receipt-impact analysis over
`corpus/evidence/round-36/c1/`; then a routing recommendation for `corpus/lessons/round-36.md`.

**Verdict up front.** Every wave-1 harness finding reproduces against the landed bytes — the
harness was never touched after the freeze, so nothing was repaired. No committed receipt in
`corpus/evidence/round-36/c1/` could have been affected by any of them: the destructive findings
(D-1/R-1) only ever *delete*, and the committed receipts exist; the eight committed REA envelopes
embed the default-scratch shape (no explicit SCRATCH arg was ever used), the before envelopes show
no sasquatch leak, and the package-root question triangulates to the 6.5.0 npx cache root. One
finding sharpens materially: R-3 is worse than "the pin is a literal" — the counter's
evidence-id recomputation is *provably blind* to a 6.4.0-vs-6.5.0 package substitution for these
envelopes; only an out-of-band field check excludes 6.4.0. Recommend routing D-1+R-1 (one guard),
the D-2 exit-contract family, and R-3's receipt-provenance half as next-round fixes; R-2 as a
header note; D-3 as optional.

## 0. Method and identity

- **The reviewed bytes are the landed bytes, everywhere.** `git show <rev>:tools/round-36/c1-run.sh | sha256sum`
  → `16907dca7fc7a104…bf4d4` at freeze `790561d4`, C2 landing `d2e46ef5`, C1 landing `ffc81341`,
  integration tip `01a44dbf`, current HEAD `6f2ba761`, and the worktree — all identical. Absent at
  base `cab59f22` (`git show cab59f22:tools/round-36/c1-run.sh` → `fatal: … exists on disk, but not
  in 'cab59f22'`). The only other commit touching the file is `c341c6f8` — a **non-ancestor**
  snapshot ref (blank subject, 2026-10-26 01:21:38 -03) whose copy is byte-identical
  (`16907dca…`). `git log --oneline --all -- tools/round-36/c1-run.sh` → exactly those two commits.
  Consequence: wave-1 code findings carry over unless the *environment* changed.
- **Environment unchanged since wave 1:** `sasquatch` sha `ad02d27a3d8424b2…` at
  `/home/vgpnk/.local/bin/sasquatch`, `unblob` sha `0ce7b624f540c219…` (symlink →
  `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`), `/usr/bin/unsquashfs` 4.7.5
  (2026/03/01) — all equal to the w1-recorded values.
- **Probes:** the frozen harness executed read-only against lane fixtures, all writes inside my
  scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36W2ReviewerHarnessDefects` (`TMPDIR=$S`); no lane
  file written except this report; no VCS mutation (only `show/log/rev-parse/merge-base --is-ancestor`).
- **No LSP device** in this seat's toolset and the target is a bash script — findings rest on
  full-text review plus live behavioral probes (same recorded gap as w1 `R36ReviewerHarnessCode.md` §0).
- **Tooling directive:** nothing installed or updated (none needed); no pacman transaction; no
  host service touched. REA touched only through the harness's own `npx -y rea-agents@6.5.0` CLI path.

## 1. Re-check verdicts

| w1 id | w1 claim | Verdict | My evidence |
|---|---|---|---|
| D-1 | OUTDIR inside SCRATCH → receipts silently destroyed, exit 0 | **CONFIRMED (raised to Medium)** | §1.1 |
| D-2 | malformed carrier exits 1, contract says 3 | **CONFIRMED (Low), family extended** | §1.2 |
| D-3 | residual empty `kaidoku-r36/` parent | **CONFIRMED (Info)** | §1.3 |
| R-1 | 4th arg SCRATCH is `rm -rf`'d unconditionally | **CONFIRMED (Medium)** | §1.4 |
| R-2 | before filter hides the whole holder dir; name-only unblob would fail | **CONFIRMED (Low), narrowed** | §1.5 |
| R-3 | `rea:"rea-agents@6.5.0"` is an echoed literal; receipts can't prove the root | **CONFIRMED (Low), sharpened into a counter blind spot** | §1.6 |
| RHC-L1 (harness part) | short-ELF carrier → `struct.error` traceback, exit 1 | **CONFIRMED** (folded into the D-2 family) | §1.2 |
| RHC I1/I3/I4/I7 | /tmp, quoting, git-`-C`, sasquatch fields: PASS | **Carried over** by byte + environment identity | §1.7 |

### 1.1 D-1 — silent receipt loss when OUTDIR ⊆ SCRATCH (confirmed; severity raised low → Medium)

Live, with the frozen harness and the committed K1 fixture:

```
$ bash tools/round-36/c1-run.sh oracle corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh \
      "$S/probeA/scr/out" "$S/probeA/scr"
D1 exit=0 ; D1 scratch GONE ; D1 receipt GONE (silently, exit 0)
```

Mechanism unchanged in the landed bytes: `mkdir -p "$outdir"` at `c1-run.sh:21` runs *before* the
trap armed at `:26` (`trap 'rm -rf -- "$scratch"' EXIT`) is pointed at that subtree; `scratch=${4:-…}`
at `:24` accepts the caller's directory verbatim.

Boundary now measured precisely — the dangerous shape is exactly "OUTDIR inside the **explicit
SCRATCH arg**" (or inside the mktemp dir, which a caller cannot name in advance):

```
$ HYAKU_SCRATCH="$S/probeA/h" bash tools/round-36/c1-run.sh oracle …/k1-le-xz.sqsh \
      "$S/probeA/h/kaidoku-r36/out"          # OUTDIR sibling of the default scratch
sibling-OUTDIR exit=0 ; sibling OUTDIR receipt SURVIVES
```

So an OUTDIR under `$HYAKU_SCRATCH/kaidoku-r36/` but *not* under `c1-run.XXXXXX` is safe; the loss
needs the 4th argument. I raise w1's "low" to **Medium** because the destroyed artifact is precisely
the evidence a round commits, the failure is silent with exit 0, and the triggering call shape
(`SCRATCH=$S OUTDIR=$S/out` for one's own session scratch) is natural for a tool whose header says
"Writes only under OUTDIR and a private scratch dir". It cannot corrupt a receipt — only delete it.

### 1.2 D-2 family — undocumented exit 1 (confirmed; three distinct paths)

Header contract (`c1-run.sh:17`): "Exit 0 ok, 2 usage/environment error, 3 tool failure."

```
$ printf 'plain text not squashfs\n' > plain.bin
$ bash tools/round-36/c1-run.sh oracle plain.bin out1
D2 plain exit=1        stderr: unsupported carrier header
$ printf '\x7fELF\x02\x01garbage' > short.elf          # 13 bytes, ELF magic
$ bash tools/round-36/c1-run.sh oracle short.elf out2
L1h short-ELF exit=1   stderr: Traceback … struct.error: unpack_from requires a buffer of at
                               least 48 bytes for unpacking 8 bytes at offset 40 (actual buffer size is 13)
$ bash tools/round-36/c1-run.sh oracle …/k1-le-xz.sqsh "$S/probeB/ro/out"   # parent dir chmod 555
mkdir-fail exit=1      (contract: 2 or 3)
```

- Path 1 (w1 D-2): `sys.exit('unsupported carrier header')` at `:42` propagates python's status 1
  through `set -e`; the explicit `exit 3` at `:46` is never reached.
- Path 2 (w1 RHC-L1): `struct.unpack_from('<Q', b, 0x28)` at `:38` raises on an ELF-magic file
  shorter than 48 bytes — same propagation.
- Path 3 (new here): `mkdir -p "$outdir"` at `:21` fails under a read-only parent → exit 1.

All three fail loud (nonzero + stderr, no receipt JSON written), so the direction is safe — but an
operator scripting the documented 0/2/3 contract misclassifies every one of them. **Low.**

### 1.3 D-3 — residual empty parent (confirmed; Info)

```
$ HYAKU_SCRATCH="$S/probeC" bash tools/round-36/c1-run.sh oracle …/k1-le-xz.sqsh "$S/probeC/out"
exit=0 ; ls -A "$S/probeC/kaidoku-r36" | wc -l → 0 ; dir EXISTS (empty)
```

`mkdir -p "$root"` (`:23`) creates `${HYAKU_SCRATCH}/kaidoku-r36/`; the trap removes only the
per-run `c1-run.XXXXXX`. Cosmetic; the shared root persisting is arguably intentional. **Info.**

### 1.4 R-1 — caller-supplied SCRATCH destroyed unconditionally (confirmed; Medium)

```
$ mkdir -p "$S/probeA/scr2/sub" ; echo precious > "$S/probeA/scr2/precious.txt"
$ bash tools/round-36/c1-run.sh oracle …/k1-le-xz.sqsh "$S/probeA/scr2/out" "$S/probeA/scr2"
R1 exit=0 ; R1 precious DESTROYED ; R1 dir GONE
```

No emptiness/ownership/mktemp-shape check on `$4` (`:24`); the trap `rm -rf`s it at `:26`. Same
`rm -rf` as D-1 — one guard covers both. **Medium** (silent destruction of an arbitrary
caller-populated directory, exit 0).

### 1.5 R-2 — the before filter hides the whole holder directory (confirmed; narrowed)

Filter text at `:71` (unchanged): drops every `$PATH` component holding an executable `sasquatch`.

```
$ path=$(python3 -I -c '<the :71 filter text>' "/usr/bin:$S/probeD/holder")   # holder: sasquatch + customtool, both +x
filtered PATH: /usr/bin
$ PATH="$path" command -v customtool → not found   → customtool HIDDEN too (whole dir dropped)
$ path2=$(<same filter> "$PATH")     → real filtered PATH drops /home/vgpnk/.local/bin
                                        (that dir holds unblob, jq, ~100 other tools)
$ PATH="$path2" command -v unblob    → NOT-FOUND under filtered PATH
```

New evidence that **narrows** w1's risk statement — a live before-mode run with a name-only
`REA_UNBLOB_COMMAND`:

```
$ REA_UNBLOB_COMMAND=unblob bash tools/round-36/c1-run.sh before …/k1-le-xz.sqsh "$S/probeD/out-name"
exit=3
before-run.json: {"mode":"before","exit":1,"sasquatch":"","unblob":"unblob","stderr_head":""}
before.json: {"code":"capability_unavailable","category":"unsupported_provider",
  "message":"This integration requires Linux and an absolute REA_UNBLOB_COMMAND path to the
             caller-supplied tool", …}
```

REA itself refuses a non-absolute unblob command, so the harness's absolute default
(`export REA_UNBLOB_COMMAND=${REA_UNBLOB_COMMAND:-$HOME/.local/bin/unblob}`) is load-bearing on
*every* host, not just this one; the failure shape is loud (harness exit 3, envelope present), never
silent. Residual risk after narrowing: any *other* tool the REA child resolves by name from
`~/.local/bin` silently disappears for before-runs. **Low.**

### 1.6 R-3 — pin fidelity (confirmed; sharpened into a counter blind spot)

Confirmed parts, unchanged bytes: `rea:"rea-agents@6.5.0"` is a literal inside the jq program at
`:87` (echoed, not probed); the envelope carries no version field (`environment: null`,
`analysis_profile: null`; `grep -o "6\.4\.0\|6\.5\.0\|6\.7\.0"` over `K2/after.json` → no matches;
the only version strings are unblob `26.6.4` and a squashfs `version 4.0` inside raw stdout).
Host package inventory: npx cache roots `ad9a3fdbcad992c6` = **6.5.0** and `dea9475797100b20` =
**6.4.0** (the other two `_npx` roots hold chrome-devtools-mcp), plus a **global 6.7.0 on PATH** at
`/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/rea-agents`.

New sharpening — the id rule itself:

1. `semanticProjection` differs between 6.4.0 and 6.5.0 *exactly* by a conditional
   `relationship_coverage` spread (statements extracted with the xpin tool's own brace-matching
   rule: 788 vs 919 bytes; the diff is only `...(evidence.relationship_coverage === null ? {} :
   {relationship_coverage: evidence.relationship_coverage})`).
2. All eight committed envelopes state `relationship_coverage: null`. Recomputing the committed K2
   pair under the **6.4.0** pin (`node tools/round-27/xpin-attribute.mjs --pkg65 <6.4.0 root> …`,
   envelopes wrapped as `{"data": …}` exactly as `c1-counter.py:91-93` does) → stored == recomputed,
   verdict **"both"**. The 6.4.0 and 6.5.0 rules coincide on these envelopes.
3. Decisive blind-spot test — delete the key and recompute: `jq 'del(.relationship_coverage)'` on
   `K2/after.json` → the id is **still** `ev_c939cd88…b0c88f` under *both* pins. The evidence id is
   blind to that field's presence and value (null → omitted by the projection; absent → `undefined`
   dropped by the canonical digest). Therefore the counter's `stored == recomputed-under-6.5.0`
   binding (`c1-counter.py:85-107`, `--pkg65` passed as both pins) **cannot detect a
   6.4.0-produced envelope** for this envelope family — it is not version-evidence here at all.
4. The 6.7.0 rule *does* differ: recomputing the committed K2 pair under the global 6.7.0 root →
   `id67 = ev_aef562a8…` / `ev_3437a35b…` ≠ stored, verdict **"none"** (matches w2
   `R36W2ExecReproFresh.md` §6, which I verified independently).
5. The one post-hoc discriminator that works: the **key's presence**. The string
   `relationship_coverage` occurs **0 times in the entire 6.4.0 package** (`grep -rc` over the whole
   root) vs 23 files in 6.5.0 (output schema declares it at
   `dist/cli-runtime/toolOutputSchemaGroups-DRiYs1je.js:11866`). A 6.4.0 build cannot emit a key
   whose name appears nowhere in it → the committed envelopes were **not** produced by 6.4.0.

**Low** — no false-green was exercised and the committed receipts triangulate clean (§3), but the
calibration lesson is real: "receipt integrity read as provenance" (M36-4 / QUALITY 78) has a
concrete second instance here — the id recomputation is weaker version-evidence than it reads.

### 1.7 Wave-1 PASS verdicts carried over

`R36ReviewerHarnessCode.md` I1 (no hardcoded `/tmp`), I3 (quoting), I7 (sasquatch fields) were
code-read verdicts on bytes that are identical today, in an environment whose probed binaries are
sha-identical — carried over without re-run. I4 (git without `-C`) is trivially re-confirmed: the
harness contains zero `git` invocations (full-text read). I did **not** re-strace `/tmp` behavior;
w1 `R36ExecHarnessRun.md` §3's strace evidence applies to these identical bytes.

## 2. Severity ranking (this seat's independent ranking)

| Rank | Finding | Severity | Rationale |
|---|---|---|---|
| 1 | D-1 | **Medium** | Silent deletion of the round's own evidence with exit 0; natural caller shape (OUTDIR inside an explicit SCRATCH arg); one-line guard fixes it. Raised from w1's "low". |
| 2 | R-1 | **Medium** | Same unconditional `rm -rf` against an arbitrary caller-populated directory; wider blast radius than D-1; same guard covers both. |
| 3 | R-3 | **Low** | Receipt cannot prove which package root ran; counter id check provably blind to a 6.4.0 substitution for these envelopes (latent package-substitution blind spot, not exercised); committed receipts verified clean out-of-band (§3). |
| 4 | D-2 (+ RHC-L1 harness part, + mkdir-fail) | **Low** | Three undocumented exit-1 paths; loud, never corrupts a receipt; contract-only defect. |
| 5 | R-2 | **Low** | Failure is loud (exit 3) and REA itself demands an absolute unblob path, so the harness default is load-bearing everywhere; residual = sibling tools hidden by name from the REA child. |
| 6 | D-3 | **Info** | Empty residual parent; cosmetic; arguably intentional. |

No High: no finding found in this re-check can make a counter reach `met_target` falsely or corrupt
an existing receipt; the destructive pair only deletes, loudly-exiting paths write no receipts, and
the pin gap does not open a scoring pathway that was actually exercised.

## 3. Could any committed receipt in `corpus/evidence/round-36/c1/` have been affected?

What is committed, where: `790561d4` (freeze) added `K{1..4}/{before,before-run}.json`,
`oracle.tsv`, `oracle-run.json`; `3310d8fa` added `K{1..4}/{after,after-run}.json`
(`git show --stat` per commit); the controls under `.ufo/waves/round-36/controls/` are **counter
runs only** (e.g. `ctl-c1-0` at base `cab59f22`, `ctl-c1-1` at a synthetic fixture rev, both
`met_target: false`, exit 1) — no harness execution, so no harness defect can touch them.

**D-1 / R-1 — no, by construction plus embedded-path evidence.**

- Both findings only ever *delete* (exit 0); neither can alter a receipt's content. A deleted
  receipt cannot be committed — all 24 committed receipt files exist and their contents verify (§3
  last bullet), so the runs that produced them had an OUTDIR that survived the trap.
- Stronger, positive evidence of *how* L1 ran: every one of the eight committed envelopes embeds
  REA's output directory under the **default** scratch shape —
  `K1 /fast/scratch/hyaku/kaidoku-r36/c1-run.ktJiZv/out`, `K2 …/c1-run.j2xtr3|Xx3qPx/out`,
  `K3 …/c1-run.xumCxb|7PV16k/out`, `K4 …/c1-run.9SBZDZ|3U654v/out` (eight distinct mktemp suffixes,
  one per run, all `run.json exit: 0`). An explicit SCRATCH arg would have shown that directory
  instead → **no explicit SCRATCH was ever passed**, so R-1's destruction shape never fired on any
  committed-receipt run, and the only deletable subtree was the harness's own scratch.
- The carriers lived outside any scratch-of-the-harness:
  `carrier: /fast/scratch/hyaku/kaidoku-r36/L1/carriers/{k1-le-xz.sqsh, k2-le-gzip.sqsh,
  nvim-linux-x86_64.appimage, nvim-linux-arm64.appimage}` in every `*-run.json`.
- Honest gap: OUTDIR itself is **not a field in any receipt** (`*-run.json` records mode, carrier,
  sha, utc, the literal pin, exit, sasquatch fields, unblob, stderr head; the envelope records REA's
  `$scratch/out`, not the redirect target). The no-impact conclusion therefore rests on the
  existence argument above, not on a recorded OUTDIR. `LOG.md` has no `c1-run` entries and
  `~/.npm/_logs` holds nothing from the run window (only 04:56–05:06 wave-2 entries), so no
  contemporaneous record of L1's OUTDIRs exists anywhere I could find.

**R-2 — no.** Every committed before-receipt records `exit: 0` and the absolute
`unblob: /home/vgpnk/.local/bin/unblob` (the load-bearing default), stamped 04:17:49Z; the after
receipts (04:22:42Z) record the absolute sasquatch. The before envelopes publish no squashfs
members on any carrier — K1/K2: zero `normalized_result.files`; K3/K4: exactly two non-oracle
artifacts each, `…/0-944632.elf64_extract/carved.elf` and the raw `…/944632-11454968.squashfs_v4_le`
chunk (K4: `0-936456` / `936456-11356680`), neither matching an `oracle.tsv` row — i.e. the filter
never leaked sasquatch. The counter's `before_oracle_hits == 0` binding is green at the tip
(`.ufo/waves/round-36/after/c1-at-ffc81341.json`: `met_target: true`, `carriers_matched: 4`).

**R-3 — no impact; the root triangulates to 6.5.0.** For the committed envelopes: stored ==
recomputed under the 6.5.0 rule for **all eight** (independent `xpin-attribute.mjs` run, verdict
"both" ×8); stored == recomputed under the 6.4.0 rule too (rules coincide, §1.6-2); stored ≠ the
6.7.0-rule value (§1.6-4); the `relationship_coverage` key's presence excludes 6.4.0 (§1.6-5); the
frozen harness's npx spec is literally `rea-agents@6.5.0` (`:81`); the local cache root for that
spec contains 6.5.0; the counter receipt names that same root as its `--pkg65`; and w2
`R36W2ExecReproFresh.md` §7 recorded `readlink -f …/.bin/rea` → the 6.5.0 root with execve traces
for its own runs. **[INFERENCE]** the committed runs executed the 6.5.0 cache root — three
independent facts point there and none elsewhere; the residue that keeps this an inference rather
than an observation is that npm's debug logs from L1's 04:17:49–04:22:42Z window have been pruned,
so the exec-time root for *those specific runs* is not directly logged anywhere.

**D-2 / D-3 — no.** Failure-path and cosmetic findings; the paths involved write no receipt that
could have been committed (the capability_unavailable F4 shape produces an envelope, but no
committed receipt has `exit != 0` — all twelve `*-run.json` files record `exit: 0`).

## 4. Routing recommendation

Route them — as **next-round fixes**, not this round (the harness bytes are frozen with the claim
and my bounds forbid repairing the lane; nothing here is repairable without touching frozen bytes).
Current routing status: the lesson's M36 table (M36-1..7) contains **no row** for any of these;
`SCORECARD.md` and `LOG.md` don't mention them; the only records are the two w1 reports. The wave-2
dispatch already routed **part** of R-3 — `w2-spec.json` line 64 instructed
`R36W2ExecReproFresh` to record the resolved npx bin (done, §1.6/§3) — but the harness receipt
itself remains non-self-proving.

Recommended routing, in priority order:

1. **D-1 + R-1 (one guard, highest value):** refuse when `realpath "$outdir"` is inside
   `realpath "$scratch"`, and refuse a SCRATCH arg that is non-empty or not caller-owned (or require
   mktemp-shape). Prevents silent evidence loss and silent destruction of foreign directories; both
   share the single `rm -rf` at `:26`.
2. **R-3 (receipt-provenance half):** record the resolved package root + version in
   `<mode>-run.json` (e.g. `rea_root: $(readlink -f "$(command -v rea || true)")` resolved from the
   npx root, or capture `npx`'s executed path) — this also brings the extraction receipts up to
   QUALITY 78's own sentence ("the receipt names the package root that the recompute used").
   Optionally sharpen the counter or QUALITY: the stored==recomputed id check is blind to a
   6.4.0-substitution for null-`relationship_coverage` envelopes (§1.6-3); a cheap schema-generation
   assertion (e.g. the key's presence) would close it. This is the M36-4 class, second instance.
3. **D-2 family:** map the three exit-1 paths (`:42` sys.exit, `:38` struct.error, `:21` mkdir) to
   the documented 2/3 contract.
4. **R-2:** header note only — state that the before filter hides the *whole* holder directory and
   that `REA_UNBLOB_COMMAND` must be absolute (REA enforces this itself; observed message §1.5).
5. **D-3:** optional — `rmdir --ignore-fail-on-non-empty "$root"` after the trap, or document.

Suggested lesson form: one appended mistakes row (e.g. M36-8, class "harness ergonomics frozen with
unrouted defects") citing `w1/R36ExecHarnessRun.md` §6, `w1/R36ReviewerHarnessCode.md` §1, and this
report — plus the R-3 blind-spot sentence under the M36-4/QUALITY 78 discussion. The defects do not
undermine the round's verdicts (§3): C1's landing stands on the committed receipts as they are.

## 5. Residual risk and verification gaps

- **OUTDIR of the committed runs is unrecorded anywhere I could find** (not a receipt field; no LOG
  entry; npm logs pruned). The no-impact conclusion for D-1/R-1 rests on the deletion-only +
  existence + embedded-default-scratch argument, which I consider direct, but a recorded OUTDIR
  would have made it airtight.
- **Which package root executed L1's runs** is [INFERENCE] (triangulated five ways, §3 R-3); no
  contemporaneous log survives.
- No `/tmp` strace re-run; w1's strace evidence is carried by byte + environment identity.
- K1/K3/K4 were not re-run live by this seat (K2-class behavior was, §1; all four carriers'
  committed envelopes were verified by projection and id recomputation); the AppImage offset
  arithmetic (944632 / 936456) was taken from the committed oracle-run.json files, consistent with
  w1's synthetic-fixture verification of the formula.
- `xpin-attribute.mjs` hardcodes the labels "6.5.0"/"6.7.0" regardless of which root is passed — my
  6.4.0-pin and 6.7.0-pin runs print those labels for the *other* pin's rule; read the columns by
  position, not by label.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36W2ReviewerHarnessDefects` (probes, extracted
  projection statements, wrapped envelopes) was removed at the end of the seat; every result cited
  above is quoted inline. No `find`/`du` under `/fast/scratch`; no VCS mutation; no installs.

## 6. Tooling record

Nothing installed or updated (operator directive 2026-10-19: nothing needed). No pacman
transaction. REA used only via the frozen harness's `npx -y rea-agents@6.5.0` path.
