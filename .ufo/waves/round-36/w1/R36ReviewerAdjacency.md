# R36ReviewerAdjacency — sasquatch install→Core adjacency review (round 36, wave 1)

Reviewed at lane HEAD `d2e46ef5e2b2e8ba681b2fa4d9a9679e96b8a73` (base `cab59f22`, freeze `790561d4`,
controls `6a870b92`, C1 after-receipts `3310d8fa`). Read-only git only; no fixture repo needed; no
tool installed or updated by this seat; scratch removed.

## Question

Does installing sasquatch into `~/.local/bin` and moving it to Core conflict with
`PROVINCE.md:97-118` `## Adjacent` (esp. :110-115 "Installing engines … operator-owned … never
runs the installer") or SHONEN box 4 ("No cross-domain bleed (PROVINCE.md still accurate)")?
Weigh against the operator tooling directive in `~/.omp/agent/RULES.md` (2026-10-19). Recommend
the minimal accurate PROVINCE amendment and the ledger call: harm, unchanged, or improved.

## Verdict

**No boundary conflict; one mandatory text reconciliation; ledger = improved, no adjacency harm.**

1. **The Core move itself conflicts with nothing.** `## Adjacent` refuses ground, not tools: the
   installing-engines bullet (:110-115) governs the *act and decision of installation* and client
   config edits, while r4 already holds binwalk (`/usr/bin/binwalk`) and unblob
   (`~/.local/bin/unblob`, uv-managed symlink observed) in Core rows *inside the same file*
   (PROVINCE.md `### Round-4 additions to Core`, row "Firmware regions + extract"). Holding and
   probing an installed extractor is the lane's own domain (extraction of declared, caller-supplied
   artifacts); installation authority is a separate, operator-side matter. Sasquatch moving
   Frontier→Core is exactly the binwalk/unblob pattern.
2. **The install act is covered by the operator directive, which supersedes the lane's blanket
   "never runs the installer" practice.** RULES.md (2026-10-19) is dated *after* the r4-era bullet,
   is marked "always on, every agent", authorizes any agent to "install or update any tool that
   helps its task … with full privilege, without asking first", and mandates recording. The channel
   used matches the directive's channel order: sasquatch is AUR-only (unreachable via pacman; all
   pacman transactions are paused host-wide), not a uv/npm package, so channel 3 — "official
   release binary into `~/.local/bin`" — is the correct and used channel (official onekey-sec
   release deb payload). `[INFERENCE]` on authority ordering: an operator-level standing directive
   outranks lane-authored practice text; the operator moved installer authority, the lane did not
   absorb it.
3. **No enumerated Adjacent refusal was breached even before amendment.** Sasquatch is not on the
   bullet's enumerated list (Hopper/IDA/JADX/Binwalk/Unblob/pwntools/ilspycmd/.NET SDK, :113), and
   no `rea setup` run, registration refresh, or client-config edit occurred — wiring is PATH
   (`~/.local/bin` resolved by `command -v sasquatch`; PATH position 4) plus the pre-existing
   `REA_UNBLOB_COMMAND` export. The amendment below is needed for *textual accuracy*, not
   legality.
4. **SHONEN box 4 is currently range-correct but accuracy-fragile.** Box 4 cites
   `PROVINCE.md:97-118` / safety `:116-118`; verified exact at HEAD (`## Adjacent` at :97;
   safety bullet at :116-118). But "PROVINCE.md still accurate" is already strained at HEAD: the
   Frontier bullet (:149-150) describes sasquatch as absent ("AUR-only; 7z fallback covers the
   carved-image path today") while the binary is installed and C1 after-receipts are committed
   (`3310d8fa`). It becomes defensible only when C1's landing (bullet removal + round-36 Core row)
   *and* the Adjacent-sentence reconciliation land together.

## Findings (by severity)

- **H1 — PROVINCE.md:114-115 is now false as written and must be amended at C1 landing.**
  "The lane documents the gap and the exact env key; it never runs the installer." Evidence of
  contradiction: commit `3310d8fa` message "sasquatch 4.5.1 official deb in ~/.local/bin"; frozen
  claims plan discloses pre-freeze dev probes running an unpacked official
  `sasquatch_1.0_amd64.deb`; installed binary present
  (`~/.local/bin/sasquatch`, 382,824 B, ELF x86-64 stripped, mtime 2026-10-26 01:22, self-reports
  "unsquashfs version 4.5.1 (2022/03/17)", sha256
  `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`). Without the amendment, box
  4's "PROVINCE.md still accurate" is false and the lane's boundary text contradicts its own
  recorded practice.
- **H2 — Version-naming calibration trap in the replacement text.** The frozen plan names the deb
  `sasquatch_1.0_amd64.deb` (fork release tag 1.0); the binary self-reports 4.5.1 (the patched
  upstream squashfs-tools version). The round-36 Core row, knowledge entry and SOURCES row must
  state one consistent identity (recommend: "sasquatch (onekey-sec fork of squashfs-tools) 4.5.1,
  release payload of onekey-sec deb sasquatch_1.0_amd64") or a future c2/calibration pass reads a
  mismatch. The "AUR-only" phrase must not survive into the Core row — the actual channel was the
  official release deb, not AUR.
- **M1 — SHONEN box-4 range refresh is a hard coupling.** Amending the bullet at :110-115 shifts
  the safety bullet below it, so both cited ranges (`97-118`, `:116-118`) go stale in the same
  commit. P36-C2 re-measures at the final tip and its frozen selftest includes an "Adjacent range
  wrong" case — an unrefreshed box 4 is a C2 falsifier. Land the PROVINCE amendment and the box-4
  range refresh together, then re-run c2-counter at the final tip. Precedent for the refresh
  ritual is recorded inside box 4 itself (rounds 25/30 drift notes).
- **M2 — Recording obligation.** RULES.md requires every install recorded with
  tool/version/channel/reason. Present: `3310d8fa` commit message + frozen-plan disclosure + the
  binary identity above. Gap: the full tuple (incl. binary sha256 and deb asset identity) should
  also appear in the round-36 report and the round-36 Core row so the record survives outside git
  metadata.
- **L1 — The bullet's half that stays true should stay.** "The lane documents the gap and the
  exact env key" was honored end-to-end (corpus/README.md:44/:162/:227 gap rows; PROVINCE :149
  gap bullet; env key `REA_UNBLOB_COMMAND` already exported). The amendment should preserve that
  clause for what remains refused (`rea setup`, registrations, client-config edits).

## Minimal accurate PROVINCE amendment

Replace `PROVINCE.md:110-115` (the **Installing engines…** bullet) with:

```
- **Installing engines, Python packages, or editing client configs** —
  `rea setup` runs, registration refreshes for `claude_code`/`codex`/
  `grok_build`/`opencode`/`pi` (all `missing` per doctor), installing
  Hopper/IDA/JADX/Binwalk/Unblob/pwntools/ilspycmd/.NET SDK — all
  **operator-owned** decisions. The lane documents the gap and the exact env key; it never
  runs `rea setup`, registration refreshes or client-config edits. Tool installs/updates
  follow the operator tooling directive of 2026-10-19 (`~/.omp/agent/RULES.md`: official
  channels only, every install recorded with tool/version/channel/reason) — e.g. sasquatch
  4.5.1 (official onekey-sec release payload into `~/.local/bin`, round 36).
```

Delta: +5 lines inside the Adjacent block (safety bullet shifts to :121-123; block ends ~:123 —
re-measure with the counter, do not trust arithmetic). One-word change "operator-owned." →
"operator-owned **decisions**." resolves the apparent contradiction between the enumeration and
the directive sentence. Nothing else in `## Adjacent` needs to move; the Frontier bullet
(:149-150) removal is already frozen into P36-C1 and does not shift the Adjacent block (it sits
below it).

## Ledger call

**Improved — no adjacency harm to report.** The frontier gap ("sasquatch AUR-only, recursion
blocked; 7z fallback") is closed into Core through an operator-authorized channel; no client
config edited; no pacman transaction; no other lane touched; none of the enumerated Adjacent
refusals exercised; no debugger/dynamic-analysis/malware ground absorbed. The required actions are
disclosure-shaped only: the H1 amendment, the M1 box-4 range refresh in the same landing commit,
and the M2 install record in the round report. If L1 rejects the H1 amendment, the round must
instead report a boundary-text inconsistency (a calibration defect, not an adjacency harm).

## Residual risk / verification gaps

- I did not re-run the counters, harness or carriers; those mechanics belong to sibling seats
  (R36ExecHarnessRun, R36ExecRecountC1/C2). My scope was the boundary question only.
- The authority-ordering argument (RULES.md supersedes the lane's installer refusal) is
  `[INFERENCE]` from the directive's "always on, every agent" wording and its 2026-10-19 date
  post-dating the r4-era bullet; the operator can override this reading.
- I did not verify the deb asset digest against the upstream onekey-sec release
  (R36ScoutSasquatchRelease covers that side); my identity evidence is the installed binary
  itself (sha256, size, BuildID `96e3fa396ab92666dd5845e8b9cd44b1b704fa87`, self-version).
- Tooling record (RULES.md obligation, this seat): nothing installed or updated; pacman untouched
  (paused host-wide); no AUR access attempted.
