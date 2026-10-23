# A2Capability17 — C2 statement round-17 audit: "Ghidra-session log capture"

Seat: `KaidokuR32A2.A2Capability17` (leaf, no dispatch). Timestamp: 2026-10-23T06:55–06:58Z.
Scope (assigned): C2 statement for **round 17**, key `/Ghidra-session log capture/` — independently open
MANIFEST at fleet `cef00867`, the matching append-only SCORECARD records at base `283aad7f`, re-open the
frozen anchor paths, locate capability evidence (not file existence), draft a faithfully copied summary row
only if evidence exists, state semantic-vs-lexical limits. No lane edits; draft lives here and in scratch only.

## 1. Frozen inputs and environment

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD `f382e3b7` (freeze commit of `claims-v3.json`,
  subject "round-32: freeze R32-C2 v3 …"; adds claims-v3.json, counter v3, two control receipts — receipts
  committed in the freeze commit itself, before any data).
- C1 freeze `9a73680a` (adds `claims.json`); base `283aad7f` (round-31 non-author verifier spot-check).
- Worktree files `claims.json` / `claims-v3.json` sha256-identical to their `f382e3b7` blobs
  (`8aa0672c…b435`, `a3be7e40…1d` — exercised).
- Frozen anchors for round 17 (`claims-v3.json anchors_at_freeze`): `[".ufo/waves/round-17/run-carriers.sh"]`.
- Frozen counter `tools/round-32/c2-capability-calibration-v3.py` extracted at `f382e3b7`:
  sha256 `5955e8ac…44d6` — **matches** `claims-v3.json instruments` pin.
- Fleet repo: `/home/vgpnk/Projects/shokunin` (owns `MANIFEST.json`, 1 242 275 bytes at pin,
  sha256 `2e089615…07f4`; rounds list len 515).
- Sandbox clones (contract-compliant; `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE` unset per invocation,
  `git -C <abs>` every time):
  `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2Capability17/{fleet,lane}` — `git clone --no-checkout file://…`.
  Lane/fleet repos never written; all revision access via the clones.
- Tools installed by this seat: none (no pacman; pacman paused anyway). Used: `git`, `python3 3.14.8`,
  `sha256sum`, `awk/sed/grep`. `df -h /fast`: 242G avail.
- Scratch artifacts (extraction evidence, not fixtures): `manifest-cef00867.json`, `scorecard-283aad7f.md`
  (sha256 `bba9f55d…38e3`, 3267 lines), `scorecard-drafted.md` (`6ca79397…76b`), `run-carriers.sh`
  (`acc27693…093b`), `ghidra-calib-shfmt.log` (`5179baf1…8581`), `receipt-calib-shfmt.json`
  (`404a6f59…aac6`), `verification-r17.json` (`af312ef6…1312`), `report-r17.md` (`27c7f021…dc13`),
  `retain.py`, `carrier-run.py`, `c2-v3-counter.py` (`5955e8ac…44d6`).

## 2. MANIFEST at fleet cef00867 — the outside record (re-opened)

`MANIFEST.json` rounds entry `{round:17, lane:kaidoku, type:closure, admitted:true, verdict:"admitted",
campaign:"hyaku", closed_at:"2026-10-20T15:07:22Z", commit:"kaidoku-shokunin@de6c721b…66dd"}` carries
`capabilities_added`: exactly one item —

> `"retained REA Ghidra-session log capture"` (verbatim, MANIFEST.json rounds[round=17,lane=kaidoku],
> fleet `cef00867`, file sha256 `2e089615…07f4`)

Written by a **non-author closure**: `verification.reviewer` = `"hyaku-closure (@m_opus session, non-author)"`;
rechecks state "no lane tool/gate executed", Git-object census `b563c799→de6c721b`, and
"8+8 receipts exit/compare 0, routes re-derived 8/8 per pass from committed ghidra.log lines".
`de6c721b` is an ancestor of base `283aad7f` (exercised, `git merge-base --is-ancestor` → 0).
Report pointer `.ufo/reports/round-17/kaidoku.md` resolves **fleet-relative** (fleet `cef00867` tree;
sha256 `27c7f021…dc13`, 124 lines; report commit `7807afe5`, "round-17: kaidoku report"). It names the lane
artifacts under `kaidoku-shokunin/` — fleet hosts the reports tree; this is consistent, not an anomaly.

## 3. SCORECARD.md append-only records at base 283aad7f (re-opened)

- `## Capabilities` at base spans lines 615–626; data rows at :619–:623 credit luna-round-6, luna-round-8,
  arc2-loop1-round2, arc2-loop1-round7, round 27. **Round 17 absent** — statement currently mismatched
  (as the claim asserts).
- Append-only capability tables sit deeper; the round-17 row is the data row under
  `### Capability addition (demonstrated before this row)` :2371, header :2373, data row **:2375**
  (first cell `| retained REA Ghidra-session log capture |`). (claims cite :2373 — the table opener; the row
  is :2375; same for :2134/:2206 = round-13/14 table separators, rows :2135/:2207.)
- The earlier observation noted-without-repair is at :3116 (":615-624 says the `## Capabilities` section
  lists the lane's capabilities … a reader of `## Capabilities` alone undercounts by 3"), with the
  four-table census inside the same bullet (:3115 tail) and the round-27 follow-up correction at :3125–:3130.
- Same section state at `f382e3b7` (HEAD): unchanged, still 5 rows, no round-17 row (exercised).

## 4. Frozen anchor re-open — `.ufo/waves/round-17/run-carriers.sh`

Exists at base; extracted sha256 `acc27693…093b`, 39 lines. First committed at `da64646a`
(2026-10-20T11:06-03:00, pass 1), hardened at `95e34db6` (11:27, pass 2) — `git log -- path` shows only
these two commits. Substance (re-opened source, not existence):

- Header: "REA analyze imports a copy into Ghidra headless (static analysis)"; "Never executes a carrier"
  (run-carriers.sh:2–6 @`283aad7f`, hash above).
- Drives `tools/carrier-run.py --carrier … --timeout 1500 --poll 0.5 --pin predictions/<label>.prediction.json`
  (line 25–27); on a bound session runs `log-extract.py` then `compare.py` (lines 30–35).
- `carrier-run.py` mechanism (base, sha256 spot-grepped): private `TMPDIR` `tempfile.mkdtemp(prefix="kr17-rea-")`
  (:301), `ENV_ALLOW` allowlist + `TMPDIR` override (:271–285), `SESSION_GLOB="/tmp/rea-ghidra-*"` re-scoped to
  the private root (:305), poller copies `ghidra.log`/`script.log` via `*.tmp`+`os.replace` (:205–238),
  `bind_session` regexes the log's own `Using log file` and `target-<sha12>.bin` lines plus full MD5 (:128–152),
  `start_new_session=True` (:107).
- **Executed, not merely present**: committed `runs/run-log.txt` records `argv: bash …/run-carriers.sh (all
  labels)`, 8/8 `carrier-run=0 compare=0`, `run-carriers exit=0` at 2026-10-20T11:27–11:40 -03:00.

## 5. Capability evidence — does it demonstrate "Ghidra-session log capture"?

Exercised against base `283aad7f`:

- **Retained artifacts**: `git ls-tree -r` shows `runs/<8 dirs>/logs/rea-ghidra-*/{ghidra.log,script.log}`
  committed at base (second pass), plus `pilot/{esbuild-0.25.12,shfmt}-log/` and
  `verify/replicate/calib-shfmt/logs/rea-ghidra-fSsMxk/`. First pass (8 dirs) at ancestor `da64646a` —
  matches the row's "16 across two passes, 8 retained at HEAD, 8 at `da64646`".
- **Log is a genuine Ghidra session log**: `ghidra.log` (125 lines) opens `Using log config file: …generic.log4j.xml`,
  `Using log file: /tmp/kr17-rea-rexl9ss6/rea-ghidra-kc2RG0/ghidra.log`, `Headless startup complete`,
  `REPORT: Analysis succeeded for file: file:///tmp/kr17-rea-rexl9ss6/rea-ghidra-kc2RG0/target-58f765638eed.bin`,
  then `SCRIPT: ReaGhidraBridge.java …/session.json` (lines 1–2, 13, 117–125 @base blob, sha256 `5179baf1…8581`).
- **Run binding**: receipt `runs/calib-shfmt/receipt.json` records `bound_sessions[0]=/tmp/kr17-rea-rexl9ss6/
  rea-ghidra-kc2RG0`, `carrier.sha256_post=58f76563…8e5a` (== log's `target-58f765638eed` prefix),
  `retained_logs[0].binding.logfile_ok=true target_ok=true`, `files.ghidra.log.sha256=5179baf1…8581` —
  I re-hashed the committed log: **byte-identical to the receipt's recorded sha256** (exercised).
  `pins_pre/pins_post` maps with `taken_at_utc` 14:27:41.9/14:28:19.5Z, `pins_compare.equal=true` —
  the "pre/mid/post pin maps with instants" claim.
- **Offline validation recorded**: `verification.json` (79 commands, `unexpected_exits: []`,
  `baseline_revision b563c79`, `source_revision d0ab299`): `receipt-validate-<label>` exit 0 ×8/8,
  `log-extract-*`/`compare-*` exit 0 ×8, `compare-route-red` exit 1 as expected (validator can fail),
  `go-carrier-run-replicate` exit 0. Replicate receipt `.ufo/waves/round-17/verify/replicate/calib-shfmt/
  receipt.json` exists; its `evidence_id ev_2b29a1dd…c5be3` **equals** the original run's (exercised);
  its retained `ghidra.log` sha256 differs (`28dcebac…`), expected for a fresh session.
- **Closure agreement**: non-author recheck "routes re-derived 8/8 per pass from committed ghidra.log lines".
- **Continuity**: same `runs/*/logs/rea-ghidra-*/` convention in rounds 18/19/20 at base — mechanism kept working.
- **First-working round**: no `ghidra.log`/`script.log` blob exists anywhere in the base tree outside
  `.ufo/waves/round-17/` (full-tree grep over `git ls-tree -r`, exercised) → first demonstrable retention
  is round 17; outside record credits round 17. **first-working round = 17**.

Conclusion: **evidence exists and demonstrates the capability** beyond file existence (committed session
logs byte-bound to run receipts, exercised end-to-end run record, recorded validation, non-author recheck).

## 6. Drafted summary row — verbatim copy (draft only; NOT landed)

Faithfully copied, cell-for-cell, from `SCORECARD.md:2375 @283aad7f` (the deeper append-only row whose
first cell matches the statement's key):

```markdown
| retained REA Ghidra-session log capture | Runs REA `analyze` on a pinned carrier in a private-TMPDIR, allowlisted-environment session and keeps that session's `ghidra.log`/`script.log`. The log is retained before REA's close deletes it, is bound to the run by its own records (log path, imported target, full MD5), and carries pre/mid/post pin maps with instants. The receipt validates offline | `bash .ufo/waves/round-17/run-carriers.sh <LABEL>`; receipts `.ufo/waves/round-17/runs/*/receipt.json` (16 across two passes, 8 retained at HEAD, 8 at `da64646`); `receipt-validate.py` exit 0 ×8 in `verification.json`; replicate `verify/replicate/calib-shfmt` | round-17 |
```

- name = MANIFEST item verbatim; description/evidence = the anchored deeper row verbatim;
  first-working round = `round-17` (MANIFEST round).
- Predicate fit (counter source read, `c2-v3-counter.py`): first cell matches only key 17; last cell names
  exactly `{17}`; evidence cell contains `.ufo/waves/round-17/run-carriers.sh` inside a backticked span —
  that is the statement's only anchor (see §7); description words = full subset of the anchored description.

### Exercised counter runs (exact argv)

```
python3 -I -B $S/c2-v3-counter.py --root $S/lane --rev 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525 --fleet $S/fleet
→ round-13 P2-mismatch; round-14 P2-mismatch; round-17 P2-mismatch "no `## Capabilities` row matches …";
  round-27 P2-match "row 5 anchor evidence tools/round-27/xpin-attribute.mjs; description words 16";
  statements=4 match=1 target=4 reverse_mismatch=0 ; exit 1        (base: reproduces unmoved_command)
```

Scratch plumbing commit (objects only inside my clone; lane/fleet untouched):
`1d2c9814eef3ea3f7ea95704f3670dd27ee6a66d` — `SCORECARD.md` base + the drafted row inserted at file :624.

```
python3 -I -B $S/c2-v3-counter.py --root $S/lane --rev 1d2c9814eef3ea3f7ea95704f3670dd27ee6a66d --fleet $S/fleet
→ round-17 P2-match "row 6 anchor evidence .ufo/waves/round-17/run-carriers.sh; description words 29";
  round-27 P2-match; statements=4 match=2 target=4 reverse_mismatch=0 ; exit 1
  (expected partial: statements 13/14 are other seats' rows)
```

## 7. Semantic vs lexical overlap — limits

- **Lexical floor is copyable by construction.** The counter's description test is ≥5 distinct words
  (`[A-Za-z][A-Za-z-]{3,}`, case-folded) shared with the anchored description (MANIFEST item + second cells
  of base rows matching the key). claims-v3 `limits` itself: "a row that copies the anchored description
  passes (that copy is the claimed repair)". My verbatim copy scored 29/29 — this certifies the *mechanical
  repair*, not the capability.
- **Anchor check is path-resolution, not capability.** For statement 17 the anchors derive to exactly
  `{.ufo/waves/round-17/run-carriers.sh}`: the MANIFEST item names no path; the deeper row's other
  backticked strings are filtered by `REL_PATH_RE` — `runs/*/receipt.json` (wildcard segment),
  `receipt-validate.py` (no directory component), `verification.json` (same), `verify/replicate/calib-shfmt`
  (no extension). A row could name the anchor and fail semantically; the gate cannot see that. Re-opening
  the evidence is this seat's job, done in §5.
- **Reverse direction blind spot**: `closed` = every kaidoku MANIFEST entry with `admitted != null`
  (rounds 12–31); a section row naming a closed round must forward-match a statement — rounds 13/14/27's
  only legal matches are their own statement rows.
- **Semantic limits of the capability itself** (from the lane's own Limits block :2377–:2390, re-opened):
  capture is a polling prefix (post-kill lines can be lost; receipt `log_capture_limit` agrees); it reads
  REA 6.5.0's private undocumented session dir and REA 6.7.0 has no keep-log knob (recheck per release);
  `receipt-validate` proves internal consistency, "not authenticity against a forger who rewrites and
  rehashes"; only `ghidra.log`/`script.log` are copied, never `session.json`.
- **My audit's own limits**: contract forbids executing carrier binaries; I did not reproduce a live run —
  strongest binding exercised is committed-log sha256 == receipt-recorded sha256 plus the recorded
  non-author route re-derivation. `logfile_ok`/`target_ok` are producer-written booleans. I verified at
  base `283aad7f`; later revisions could differ (HEAD spot-checked only for the `## Capabilities` section).
- **Row placement note**: the deeper-row evidence text is a narrative pointer ("receipts `…runs/*/
  receipt.json` … `receipt-validate.py` exit 0 ×8 in `verification.json`"); only `run-carriers.sh` is a
  counter-visible anchor. Drafting verbatim is the faithful copy and is what the predicate can check.

## 8. Findings / residual risk

1. **Evidence exists** for "retained REA Ghidra-session log capture", first-working round 17; drafted row
   (§6) is verbatim-faithful and passes the frozen predicate in a scratch rev (`P2-match`, 29 words).
2. **No defect found in-scope.** Residual: lane-side, not gate-side — the MANIFEST `report` pointer is
   fleet-relative (`.ufo/reports/round-17/kaidoku.md` under the fleet tree), so any lane-relative reader of
   that pointer finds nothing at base/HEAD (exercised `ls-tree` both revs). Cosmetic; outside the counter.
3. Verification gaps: no live re-run (contract), authenticity-not-forgery stands as the lane's own
   disclosed limit, REA-version sensitivity disclosed (6.7.0 no keep-log knob).
4. Process hygiene: no background processes started; nothing to kill. No lane/fleet writes; only this
   report and my scratch dir. `git` writes confined to `$S/lane` plumbing + `a2audit-draft` tag in scratch.

Report trailer: `.ufo/waves/round-32/a2audit/A2Capability17.md`
