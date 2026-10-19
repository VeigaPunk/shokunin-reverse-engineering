# proposed SOP amendment — "Config custody for live-probe rounds (SOP)" v2 (patch text)

Authored by SEAT PL-3 (chain c3, planner). **Patch text only** — SKILL.md is not a
seat write target. Intended placement: `SKILL.md:242-281` (the custody SOP section);
keep the existing bullets, and add/replace as marked. Measured basis:
`claims/c3/PL-3/measurements.txt`, tool sha `112d01dc…` (2026-10-19).

## A. New bullet — v2 receipt is the primary artifact (insert after the "Freeze the
pre-pair" bullet)

- **v2 capture (primary).** Freeze the pre-pair with the committed instrument:
  `python3 .ufo/gates/custody-pair/custody-pair.py capture --out "$R/config-pre-pair-v2.txt" --label '<round> PRE-PAIR'`.
  The receipt carries per path: `SHA256`, `MTIME_EPOCH`/`MTIME_NS`,
  `MTIME_UTC_RENDER` (gmtime of the epoch — the v1 label defect cannot recur),
  `MTIME_LOCAL_RENDER` (separate, advisory), `CTIME_EPOCH`/`CTIME_NS`, `INODE`,
  `MODE/UID/GID`, `TYPE`, `SIZE`; the header pins the producing tool's sha256.
  Exit 0 = 5/5 present; exit 13 = a path absent (receipt still written, claim void
  per the drift rule). The sidecar `<receipt>.sha256` is written by the tool.
- **Shape gate is the tool's own.** The v1 `wc -l`/`grep -cE` shape gate stays valid
  for v1 receipts only; v2 receipts are self-verified by `verify` (a truncated or
  empty receipt exits 2 — measured C14 in `claims/c3/PL-3/measurements.txt`, landed
  tool).
- **Post-pair.** `… capture --out "$R/config-post-pair-v2.txt" --label '<round> post'`,
  then `… verify "$R/config-pre-pair-v2.txt" --live` — exit 0 and every path
  `MATCH compared=11/11` is zero drift. Exit 11 (`REWRITE-DRIFT`: sha256 equal but
  inode/mtime/ctime moved) is the same-content-rewrite class and **voids the
  zero-drift claim exactly as a content mismatch does**; exit 12 covers
  metadata-only movement (mode/uid/gid/size/type, `LABEL-DEFECT`); exit 13 covers
  absence. Record the exit and the `VERDICT:` line verbatim.

## B. New bullet — v1 receipts remain evidence (verified, never edited)

- **v1 receipts stay valid and stay byte-frozen.** Verify them with the same tool:
  `… verify <v1 receipt> --live`. Three shapes parse (`sha256sum` form; CU-1 stanza
  form; CU-1 metadata pipe form). The shared verdict is the
  `SHA256-CONTRACT n/n paths agree on sha256` line; v1 fields the receipt does not
  carry are reported as a reduced `compared=k/11`, never back-filled from a live
  read. A v1 receipt whose time strings are the round-1 local-render-under-UTC
  defect reads `LABEL-DEFECT` → exit 12: the defect is reported, the receipt is not
  edited, and the run is not a clean pass. Expected examples (measured): `sums-v1`
  → exit 0, `SHA256-CONTRACT 5/5`; CU-1 stanza and pipe forms → exit 12,
  `SHA256-CONTRACT 5/5` + `LABEL-DEFECT` per path.

## C. New bullet — tool-revision rule (the C1 rule-#14 discipline applied here)

- **A receipt records its producer.** If `.ufo/gates/custody-pair/custody-pair.py`
  is revised after a pair was captured, the pair's header `# tool:` sha is stale by
  construction: either re-capture the pair with the landed revision (preferred —
  cheap, and the field-level diff can be shown empty) or record the revision mapping
  plus a field-level diff audit. A pair captured by a superseded revision cannot
  carry the round's "captured by the landed tool" claim by itself.

## D. Supersession note for the old one-liner

- The `sha256sum … > "$R/config-pre-pair.txt"` one-liner and its `sha256sum -c`
  post-check remain valid as the **v1 form** and as an independent second opinion
  (`tail -n +2 … | sha256sum -c -` semantics unchanged). They are blind to
  same-content rewrites by construction; a v2 pair is required for any claim that
  needs rewrite detection, and both can be recorded side by side without conflict.
