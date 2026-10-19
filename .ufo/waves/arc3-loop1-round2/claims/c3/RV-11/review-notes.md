# RV-11 review notes — custody-pair v2 tool, static inspection (chain c3, reviewer seat)

Reviewed bytes: `.ufo/gates/custody-pair/custody-pair.py`, 889 lines, size 39157,
sha256 `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`
(mtime 2026-10-19 09:05:19 -0300). All line cites are this revision.
`README.md` (same dir): `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba`.

Mid-review revision observed: first read `4862f6426a7589cf239da9c46af6db4140c381d2d6bfe0cbc06bcc84a62f2a29`
(883 lines, size 38651, mtime 09:04:00). The revision (a) added per-row
`sha_agree` + the `SHA256-CONTRACT` disclosure line (`verify_sets`, :514-517) and
(b) fixed `_label_audit` to use the same clock's epoch per check (:395-397 —
the first revision used the mtime epoch for both the MTIME and CTIME v1 checks).
Every measurement below was run against a pinned copy of the final revision
(`claims/c3/RV-11/tool-identity.txt`), then the landed bytes were re-hashed
unchanged and the selftest re-run on them.

## 1. epoch / UTC / inode / ctime capture — correct on inspection

- `capture_path` (:189-222) is read-only and uses `os.lstat` (:193) so a symlink
  swap is itself a custody event (`TYPE: symlink` + target digest, :212-216).
- Identity fields: `inode = st.st_ino` (:207); `mtime_epoch = int(st.st_mtime)`
  (:208); `mtime_ns = int(st.st_mtime_ns)` (:209); `ctime_epoch = int(st.st_ctime)`
  (:210); `ctime_ns = int(st.st_ctime_ns)` (:211); mode/uid/gid (:204-206).
  Epochs are truncated to whole seconds and the sub-second part is carried
  separately in the `*_NS` fields — no precision loss, no float rounding.
- `render_utc` (:174-176) is `time.gmtime` only — TZ-independent by construction.
  `render_local` (:179-186) uses `time.localtime` + `tm_gmtoff` and is emitted
  under its own label (`MTIME_LOCAL_RENDER`/`CTIME_LOCAL_RENDER`, :278-283).
  The receipt header states the label contract (:256-258) — the v1 defect
  (local render under `MTIME_UTC`) is structurally impossible in v2 capture.
- `atime` deliberately omitted (:33-35) — reading cannot move any captured field.
- Receipt embeds the tool's own sha256, re-derived at every run (:243, :248)
  (C1 rule-14-friendly self-identity).

## 2. comparison logic — sound; measured classes match declarations

- Formats parsed (`parse_receipt` :338-385): v2 stanza, v1-stanza, sums-v1,
  pipe-v1; format tag printed by `cmd_verify` (:599).
- `compare_section` (:420-473): sha256 first → CONTENT-DRIFT (:447-449); then
  rewrite identity (`inode`, `mtime_ns`, `mtime_epoch`, :451-454) → REWRITE-DRIFT;
  else `mode/uid/gid/size/type` → METADATA-DRIFT vs residual `ctime_*` →
  REWRITE-DRIFT (:457-466); partial comparison downgrades MATCH →
  MATCH-V1-PARTIAL (:468-469).
- `_label_audit` (:392-417): per-clock v1 time vs epoch renders; LABEL-DEFECT on
  local-render match (:403-407); notes on unmatched strings (:408-409); v2
  epoch-vs-`MTIME_UTC_RENDER` consistency check (:410-416).
- `verify_sets` (:476-523): candidate-only path → METADATA-DRIFT/EXTRA-PATH
  (:484-487); missing stanza → ABSENT (:488-491); worst-severity resolution
  (:498) against `SEVERITY` (:127-134); exit mapping `EXIT_FOR` (:135-142);
  SHA256-CONTRACT disclosure (:514-517).
- Exit codes 0/10/11/12/13/2/3 were each exercised end-to-end and matched the
  docstring table (:59-73) — see `attacks-isolated.out`, `attacks-two-receipt.out`,
  `v1-compat-and-tz.out`.
- Write guard: `cmd_capture` refuses `--out` resolving onto one of the 5 custody
  paths (:562-566) and the guard case asserts the custody path is byte-stable
  around the attempt (:817-824). Path-based only — see finding F2.

## 3. selftest fixtures — real (and shown to have teeth)

- All fixtures are real files under `tempfile.mkdtemp` (:623-635): real in-place
  rewrite + mtime restore + inode/ctime assertions (:666-679); real temp+rename
  (:682-691); content drift (:694-699); absent path (:702-711); chmod (:714-724);
  TZ-independence via subprocess with `TZ=UTC/UTC-3/UTC+5` on the round-1 defect
  epoch 1792011200 (:732-752); v1-stanza + mutated-sha pair (:755-779); sums
  (:782-790); pipe (:793-805); unparsable (:808-814); write-guard (:817-824).
- Teeth proven by mutation: three sabotage copies each fail the right cases —
  `sabotage/summary.txt`: neuter-rewrite → 2 failing cases (exit 3);
  `gmtime`→`localtime` → label case fails (exit 3); neuter-sha-compare → 2 failing
  cases (exit 3). A fixture that only printed would leave these green.
- The selftest never touches a custody path (`refuses-to-write-over-custody-path`
  asserts before==after on `CUSTODY_PATHS[3]`; fixtures root defaults away from
  `/tmp`, :620-624, :530-537).

## 4. Findings (named for CR-4 / parent; none refutes the C3 claim)

- **F1 — v1 LABEL-DEFECT audit is verifier-TZ-dependent.** `_label_audit`
  compares the v1 string against `time.localtime` *of the verifying process*
  (:402). Measured (`v1-compat-and-tz.out`): canonical round-1 receipt → exit 12
  under host TZ (-03), but exit 0 under `TZ=UTC` (condition unsatisfiable there;
  string reported as a `note` only) and exit 0 under `TZ=Asia/Tokyo`. Capture
  side is TZ-independent; only this v1-compat *classifier* is not. Disclosure
  survives as the note line; sha256 contract unaffected.
- **F2 — write guard is inode-blind: hardlinks evade it.** The guard compares
  resolved *paths*, not `(st_dev, st_ino)` (:562-566). Scratch reproducer
  (`hardlink-guard/run.out`): `guarded.conf` hardlinked as `alias.out`;
  `capture --out alias.out --paths guarded.conf` exited 0 and wrote the receipt
  through the shared inode (sha256 8af5b1d5… → 67e161eb…; bytes = receipt).
  Requires a pre-existing hardlink; the default flow never creates one. Optional
  mitigation: `proposed-hardlink-guard.patch.md` (not applied).
- **F3 — a v2 stanza with its SHA256 field deleted degrades to exit 0.**
  Measured: class `MATCH-V1-PARTIAL`, `compared=10/11`, `SHA256-CONTRACT: 4/4`
  (`attacks-two-receipt.out` E6). Disclosed (partial count + contract line), but
  field absence is a downgrade, not a fault class.
- **F4 — boundary call**: EX-31 created `custody-pair/README.md` (new file inside
  its authorized target dir). The hard rules forbid *editing* README files; this
  is a new file under the dir the implementer is allowed to write. I read it as
  authorized by target dir; CR-4/parent should rule. Related wording nit: tool
  docstring :4 calls it "a committed instrument" though seats commit nothing —
  the parent commits.
- **N5 (minor)** — `capture --paths` with zero arguments: `nargs="*"` yields `[]`,
  and `args.paths or CUSTODY_PATHS` (:552) silently falls back to the full 5-path
  set. A footgun, not a defect.
- **N6** — running/importing the tool left `.ufo/gates/__pycache__/` (census pyc,
  other seat) in the tree; EX-31's own `custody-pair/__pycache__/` was removed
  (verified: dir contains exactly tool + README). Records commits should exclude
  `__pycache__` (round-1 SC-2 precedent).
- **N7 (minor)** — receipt writes are non-atomic (`write_text` + sidecar,
  :568-572); a crash
  mid-write leaves a partial receipt + no sidecar. Evidence-capture grade, fine.
