# R36ReviewerReceipts — C1 custody review (round 36, wave 1)

Advisory, read-only. Scope: the C1 custody chain only — git order of
freeze → control receipts → after receipts, per-carrier environment receipts
(sasquatch empty before / pinned after), carrier sha equality, UTC stamp
ordering, and what evidence exists for "install happened after controls".
Not in scope (covered by other seats, not re-checked here): evidence-id
recomputation (R36ExecEvidenceIds + counter), predicate/counting semantics
(R36ExecRecountC1, R36ExecIndependentC1), K3/K4 GitHub-digest equality
(R36ScoutNeovimRelease).

All paths below are relative to the lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
unless absolute. No VCS mutation, no subagents, no background jobs, no pacman
transaction, no host service touched.

Tooling record (operator directive 2026-10-19): nothing installed or upgraded.
Downloads: `sasquatch_1.0_amd64.deb` (187244 B, sha256
`efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95`) from
`https://github.com/onekey-sec/sasquatch/releases/download/sasquatch-v4.5.1-6/sasquatch_1.0_amd64.deb`
into my scratch, unpacked with `ar p … data.tar.xz | tar -xJ`, used only as
provenance evidence; scratch removed at end of review. Used as found:
git (read-only: show, log, merge-base, status, rev-parse), sha256sum, stat,
jq, curl, ar, tar, date.

## Verdict up front

Custody holds. Every assigned check passes on committed evidence, and the
"install after controls" ordering is supported by two independent time sources
(git commit order and the installed binary's filesystem birth time) plus
byte-level provenance to the official deb. The one genuinely weak link — the
control receipts carry no run timestamps, so "controls ran before the install"
is commit-clock + L1's word — is recorded below with the exact limits, and it
does not weaken the kill rule because the controls' verdicts are install-state
independent. No defect found; findings are calibration notes only.

## 1. Git order (verified)

`git show -s --format='%H%nauthor: %aI%ncommitter: %cI%nparents: %P'` and
`git merge-base --is-ancestor` (all exit 0):

| commit | committer date (−03) | parents | content (git show --name-status) |
|---|---|---|---|
| base `cab59f22` | 2026-10-25T23:16:39 | 3b1ab3c9 | (pre-existing interrupted-run snapshot) |
| freeze `790561d4` | 2026-10-26T01:21:38 | `cab59f22` | `plans/round-36-claims.md`, `tools/round-36/{c1-counter.py,c2-counter.py,c1-run.sh}`, `corpus/evidence/round-36/c1/{carriers.json,fixtures/*}`, `K1..K4/{oracle.tsv,oracle-run.json,before.json,before-run.json}`, selftest dev-* files, `.ufo/waves/round-36/census-start.txt` |
| controls `6a870b92` | 2026-10-26T01:22:29 | `790561d4` | only `.ufo/waves/round-36/controls/ctl-{c1-0,c1-1,c1-2,c2-0,c2-1,c2-2,c2-3}*.{json,out}` |
| after `3310d8fa` | 2026-10-26T01:22:59 | `6a870b92` | only `corpus/evidence/round-36/c1/K1..K4/{after.json,after-run.json}` |

- Ancestry: `base → freeze → controls → after → HEAD` all verified
  (`git merge-base --is-ancestor`, exit 0 each). HEAD is `d2e46ef5`
  (2026-10-26T01:27:16−03, C2 self-assessment repairs); `git log 3310d8fa..HEAD`
  shows that is the only later commit.
- Frozen-path immutability: `git log -- <path groups>` over
  `carriers.json`, `K*/oracle.tsv`, `K*/{before.json,before-run.json,oracle-run.json}`,
  both counters, `c1-run.sh`, `plans/round-36-claims.md` returns exactly one
  commit (the freeze) — nothing after it touched them. Control receipts: only
  `6a870b92`. After receipts: only `3310d8fa`.
- Worktree: `git status --porcelain` lists only untracked
  `.ufo/waves/round-36/{assimilation,c2,interim,w1,w1-dispatch.json,w1-gen.py,w1-spec.json,w1.ready,w1.ready.dispatched}/…`
  wave artifacts; no tracked frozen path is dirty, so worktree files equal the
  committed blobs for everything cited here.

## 2. before-run.json ×4 — sasquatch empty (verified)

`corpus/evidence/round-36/c1/K{1,2,3,4}/before-run.json`, all four:

```
"sasquatch": "", "sasquatch_sha256": "", "sasquatch_version": ""
"utc": "2026-10-26T04:17:49Z", "rea": "rea-agents@6.5.0", "exit": 0,
"unblob": "/home/vgpnk/.local/bin/unblob", "stderr_head": ""
```

Calibration note (not a defect): `tools/round-36/c1-run.sh` before-mode removes
every PATH directory containing an executable `sasquatch` and exits 2 if
`command -v sasquatch` still resolves, so the empty fields attest absence from
the *effective (filtered) PATH*, not absence from disk. This is the intended
no-sasquatch pipeline design; the REA envelope inherits the filtered PATH, so
the before envelopes report the `missing-extractor-dependency` gap regardless
of host install state.

## 3. after-run.json ×4 — pinned sasquatch (verified, live)

All four `K*/after-run.json`:

```
"sasquatch": "/home/vgpnk/.local/bin/sasquatch",
"sasquatch_sha256": "ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754",
"sasquatch_version": "unsquashfs version 4.5.1 (2022/03/17)",
"utc": "2026-10-26T04:22:42Z", "exit": 0
```

Live re-check today (2026-10-26):
- `sha256sum ~/.local/bin/sasquatch` → `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`
  (382824 B) — exact match.
- `~/.local/bin/sasquatch -v` → `unsquashfs version 4.5.1 (2022/03/17)` — exact match.

## 4. Carrier sha256 equality (verified end-to-end)

- `carriers.json` frozen values: K1 `93802938…a589`, K2 `ce5bf60e…084f`,
  K3 `b644d034…f29fb`, K4 `8efcec73…e1c2`.
- All 8 `K*/{before,after}-run.json` `carrier_sha256` fields equal their
  carrier's carriers.json value.
- All 8 REA envelopes (`K*/{before,after}.json`) `subject.digest.sha256`
  equal the same values (`jq -r '.subject.digest.sha256'`), and
  `subject.name` matches (k1-le-xz.sqsh, k2-le-gzip.sqsh,
  nvim-linux-x86_64.appimage, nvim-linux-arm64.appimage).
- Byte-level: committed fixtures hash exactly to carriers.json
  (`sha256sum corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh k2-le-gzip.sqsh` →
  both match). The actual run inputs still exist in the L1 scratch the
  receipts point at (`/fast/scratch/hyaku/kaidoku-r36/L1/carriers/`,
  mtimes 01:17): all four hash exactly to carriers.json, so the receipts
  record the digests of the bytes the harness actually consumed. K1/K2 are
  additionally committed in the lane; K3/K4 exist only as fetched bytes in
  that scratch (carriers.json `frozen_note` says so by design).
  Equality of K3/K4 digests to GitHub's *published* release digests is not
  re-verified here (R36ScoutNeovimRelease's assignment).

## 5. UTC stamp ordering (verified)

- Every before receipt: `2026-10-26T04:17:49Z`; every after receipt:
  `2026-10-26T04:22:42Z`. `before < after` holds for all four carriers
  (K1 04:17:49 < 04:22:42, K2, K3, K4 identical).
- Calibration notes: stamps are written once per harness invocation
  (`now=$(date -u +%FT%TZ)` in `c1-run.sh`, 1-second granularity) and are
  identical across K1–K4 within each mode, i.e. each mode's four runs were
  launched in one batch within the same second; per-carrier ordering *inside*
  a mode is not resolvable from the receipts. The predicate does not depend
  on intra-mode ordering. Cross-mode ordering is corroborated by content:
  before envelopes report the sasquatch gap and publish no oracle content,
  after envelopes publish all oracle content (independently confirmed by
  R36ExecIndependentC1).

## 6. Install after controls — evidence vs L1's word

Filesystem-attested (hard):
- `stat` of `~/.local/bin/sasquatch` and `~/.local/bin/sasquatch-v4be`:
  birth = ctime ≈ mtime `2026-10-26 01:22:37.80 −03` (= 04:22:37.8Z) for both.
  Equal birth/ctime/mtime means fresh writes at install time, not a
  mtime-preserving copy of an older file.
- Byte provenance: I downloaded the official
  `sasquatch-v4.5.1-6` `sasquatch_1.0_amd64.deb` (187244 B, sha256
  `efbc92bd…ade95`) and unpacked it: `usr/bin/sasquatch` →
  `ad02d27a…4754` (382824 B), `usr/bin/sasquatch-v4be` → `fac88740…14c6`
  (436232 B) — **byte-identical to both installed files**. R36ScoutSasquatchRelease
  independently downloaded the same deb and recorded the same GitHub API
  digest (`w1/R36ScoutSasquatchRelease.md:23,31-33`), so the installed
  binaries are exactly the official release-asset binaries. The installed
  version string (4.5.1, 2022/03/17) is consistent.

Git-attested (committer-clock claims — honest-host assumption):
- Order is monotone: controls commit 04:22:29Z < binary birth 04:22:37.8Z <
  after-run stamps 04:22:42Z < after commit 04:22:59Z (all −03 conversions
  consistent). Commit times could in principle be forged via
  GIT_COMMITTER_DATE; nothing in this review can rule that out.

Only the L1's word (no independent artifact):
- That the three C1 controls (and the C2 controls) were **run** before the
  install. The committed control receipts (`ctl-c1-*.json`) contain
  argv/bindings/carriers/met_target but **no wall-clock stamp at all**
  (verified field-by-field); their `.out` files record only the counter
  summary and `CTL-C1-x exit=1`. The only time marker placing the controls in
  sequence is the commit time of `6a870b92` plus their parent linkage to the
  freeze commit. No install log or shell history is committed anywhere in the
  lane (I grepped `.ufo/waves/round-36` for sasquatch/install mentions: only
  dispatch prompts and later wave reports, none timestamping the install act).
  The sentinel seat's report (`w1/R36SentinelInstall.md`) did not exist in
  `w1/` at review time (directory listing checked); if it lands, it may add a
  third witness.
- That no sasquatch-enabled carrier run happened between freeze and install.
  Consistent with: after receipts exist only in `3310d8fa` (no earlier
  after.json anywhere in history), and their stamps (04:22:42Z) postdate the
  binary's birth time (04:22:37.8Z). Not independently provable.

Mitigation that bounds the risk: all three C1 controls are frozen-counter runs
over frozen inputs (ctl-c1-0 at `--rev cab59f22` do-nothing; ctl-c1-1/2 over
scratch repos `ctl.5RFJue`/`ctl.5IzfxI` at revs `104dd4a2`/`6a16267c` with all
bindings present), and none consults the host install state. If the controls
had in fact been re-run after the install, their receipts and `exit=1`
verdicts would be byte-identical; the "install after controls" sequencing is
procedural hygiene around the kill rule, not load-bearing for falsification.

## Findings by severity

No defects (no Medium/High findings). Calibration/observation findings:

- **[Low, calibration] Control receipts are timestamp-free.**
  `ctl-c1-*.json`/`.out` carry no run time; sequencing rests on the controls
  commit's clock plus the L1's word. Consider (future rounds, not a repair
  now — the counter/receipt shape is frozen) having counter invocations echo a
  UTC line into `.out` so sequencing becomes artifact-attested.
- **[Low, calibration] before-mode emptiness proves PATH absence, not disk
  absence** (by harness design, `c1-run.sh` before-mode filters PATH dirs).
  Reports citing `before-run.json` as "sasquatch not installed" overstate it;
  "sasquatch absent from the effective PATH" is the supported claim.
- **[Info] Stamp granularity/batching.** Identical 1-second stamps across the
  four carriers per mode mean batch launches; intra-mode per-carrier order is
  not resolvable from receipts (predicate-independent).
- **[Info] Both deb binaries installed** (`sasquatch`, `sasquatch-v4be`,
  byte-identical to the official deb). All claimed carriers are
  little-endian; BE is explicitly unclaimed, so the v4be presence is unused
  but harmless and consistent with the claims' "Not claimed: big-endian".
- **[Info] Post-after activity is clean.** The only commit after `3310d8fa`
  is `d2e46ef5` (C2 repairs, 01:27:16−03); it touches no C1 frozen path
  (verified per-path).

## Residual risk and verification gaps

- Evidence ids of the 8 envelopes not recomputed here — assigned to
  R36ExecEvidenceIds (and checked by the frozen counter); no custody finding
  depends on them.
- K3/K4 digest equality to GitHub's published release digests not re-verified
  here (R36ScoutNeovimRelease); my check ties receipts ↔ carriers.json ↔
  actual run-input bytes, not ↔ GitHub.
- The control scratch roots (`ctl.5RFJue`, `ctl.5IzfxI`) and their revisions
  (`104dd4a2`, `6a16267c`) no longer exist, so the control runs are not
  replayable from artifacts; the counters and their selftests are.
- Commit timestamps are trusted as host-clock outputs (honest-host
  assumption); a fully clock-skeptical custody chain would need a signed or
  externally anchored timestamp source, which this lane does not have.
- Before-run disk-absence of sasquatch on the host at 04:17:49Z is not
  provable from receipts (see Low finding 2); the binary's filesystem birth
  time (04:22:37.8Z) is the earliest filesystem evidence of sasquatch existing
  anywhere under ~/.local/bin, and byte-provenance ties that file to the
  official deb.

Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ReviewerReceipts` (deb + unpacked
`usr/` tree) removed after this report was written.
