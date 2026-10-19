# SOP amendment (PATCH TEXT, not applied) — custody pre/post pairs run through the v2 instrument

Seat EX-39 · chain c3 · role executor · wave `arc3-loop1-round2` · 2026-10-19
Target: `SKILL.md`, § "Config custody for live-probe rounds (SOP)" (lines 242-314
at HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420`, file sha256
`483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb`, 371 lines).

Status: **patch text only — not applied.** `SKILL.md` is outside this seat's write
scope (corpus/SKILL/README edits are patch text per the frozen round-2 rules).
The lane repo was not written by this seat; the patch was built, applied and
exercised on `/dev/shm` clones of HEAD (sim3, base `14b1682`).

Claim it serves (C3, `claims-frozen.md:52-64`): future rounds' pre/post pairs go
through the v2 tool rather than ad-hoc `sha256sum` — the operability half of the
custody receipt v2 claim, whose measured origins are the round-1 label defect
(local `-03` mtime printed under an `MTIME_UTC` label) and sha256-only blindness
to a same-content rewrite.

## 1. What the amendment changes (four edit sites)

| # | site (HEAD lines) | change |
|---|---|---|
| 1 | insert after the section preamble (after `:249`) | four new bullets: the v2 capture/verify mandate with exact commands; the declared exit scale and drift classes; the mechanical label rule (a UTC field is the UTC render of its own epoch, with the round-1 defect named); same-content rewrite = REWRITE-DRIFT, and archived v1 receipts stay verifiable |
| 2 | "Freeze the pre-pair…" (`:251-265`) | new captures run through the tool; the inline `sha256sum` form is demoted to the **v1 archive form** (shape gate for archived receipts + independent cross-check); v2 shape gate named (`PATH:` stanzas, epoch/render fields, `.sha256` sidecar), with the tool's `selftest` as the gate command |
| 3 | "Take the post-pair…" (`:283-290`) | post-pair captured through the tool; the round's drift reading is `verify --live` (live vs frozen pre-pair) plus the pair comparison with the frozen pre-pair **first** (reference side); the `sha256sum -c` cross-check retained on the v1 form |
| 4 | "Drift disposes the claim…" (`:304-310`) | the v2 classes named (content / rewrite / metadata / absent — rc 13 is never a skip); the zero-drift claim is VOID on any non-zero reading; an unparsable receipt (rc 2) named |

Untouched: the section preamble and its citations, the shell-file scope bullet,
the read-only bullet, the `tail -n3` selector bullet, the same-round bullet, the
commit bullet, and every pinned citation line. The v1 inline command keeps its
literal five-path form — a change that would have been semantically silent and
therefore not made.

## 2. Patch text (unified diff; applies with `patch -p1` from the repo root)

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -248,8 +248,68 @@
 as "No config-drift pair."
 (`corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15`).
 
+- **The pair is captured and verified by the custody-pair tool (v2); the inline
+  `sha256sum` form is the v1 archive form.** The instrument is committed at
+  `.ufo/gates/custody-pair/custody-pair.py` (landed arc3-loop1-round2): every
+  future live-probe round's pre/post pair goes through it, and an ad-hoc
+  capture is a SOP violation, not a weaker grade. It is read-only over every
+  path it inspects and refuses to write over a custody path (its committed
+  selftest case `refuses-to-write-over-custody-path`). The receipt's header
+  pins the producing build's own digest and the repo HEAD — the producer
+  identity: capture the pair with the landed build, keep that digest
+  re-derivable (do not edit the instrument after the round's pair is
+  captured), and if the instrument moves mid-round record both digests rather
+  than re-verifying silently. Verbs and exact form:
+  - pre-pair, before the round's first probe —
+    `python3 .ufo/gates/custody-pair/custody-pair.py capture --out "$R/config-pre-pair.txt" --label "<wave> pre-pair"`;
+  - post-pair, after the last leg exits and every session is closed —
+    `python3 .ufo/gates/custody-pair/custody-pair.py capture --out "$R/config-post-pair.txt" --label "<wave> post-pair"`;
+  - the round's drift reading —
+    `python3 .ufo/gates/custody-pair/custody-pair.py verify --live "$R/config-pre-pair.txt"`
+    (receipt against the live paths), and the pair comparison with the frozen
+    pre-pair first (the reference side) —
+    `python3 .ufo/gates/custody-pair/custody-pair.py verify "$R/config-pre-pair.txt" "$R/config-post-pair.txt"`
+    (the absent and extra-path classes are judged on the candidate side).
+  The five paths, their fixed order, the read-only rule, and the same-round
+  bracketing rule are unchanged by v2, and `--paths` is for fixtures and
+  self-tests only — a round's pair always covers the five canonical paths.
+- **The exit scale is declared and the drift classes are separated.** `capture`
+  exits 0 on 5/5 present and 13 when a path is absent (the receipt is still
+  written). `verify` exits 0 MATCH, 10 CONTENT-DRIFT (sha256 differs),
+  11 REWRITE-DRIFT (sha256 equal, inode/ctime/mtime moved — the same-content
+  rewrite class), 12 METADATA-DRIFT (mode/uid/gid/size/type movement, an extra
+  path, an epoch/render inconsistency, or a reproduced v1 label defect),
+  13 ABSENT, 2 usage or unparsable receipt, 3 selftest failure; severity
+  precedence CONTENT > ABSENT > REWRITE > METADATA > MATCH. A zero-drift claim
+  requires MATCH, exit 0 — never "sha256 equal" alone; any rc≠0 reading is
+  recorded verbatim and not re-derived by hand.
+- **The label rule is mechanical: a UTC field is the UTC render of its own
+  epoch.** Each v2 stanza carries `MTIME_EPOCH`/`MTIME_NS` rendered twice —
+  `MTIME_UTC_RENDER` (`Z`) and `MTIME_LOCAL_RENDER` (offset) — and the same
+  pair for `CTIME`; a `*_UTC_RENDER` that is not `gmtime(epoch)` is a
+  malformed receipt (the LABEL-DEFECT class, rc 12), never a pass. The round-1
+  canonical receipt printed the local (-03) `17:53:20` under an `MTIME_UTC`
+  label for epoch `1792011200` = `2026-10-14T20:53:20Z` — digests unaffected;
+  the fix lives in the instrument, not in a re-capture. atime is deliberately
+  uncaptured (reading a file moves it, so the field would make the instrument
+  non-idempotent over its own use).
+- **A same-content rewrite is drift, and archived v1 receipts stay
+  verifiable.** sha256 equality cannot see an unlink+recreate or an in-place
+  rewrite of identical bytes; `INODE`/`CTIME_NS` movement with equal hashes
+  reads REWRITE-DRIFT — record both identity readings verbatim, do not edit or
+  restore the path, classify as operator-owned incident. The same tool
+  verifies archived v1 receipts against the live paths in all three v1 shapes
+  (stanza, `sha256sum`, pipe), comparing the fields they carry
+  (`MATCH-V1-PARTIAL`; sha256 is the contract) and reporting `LABEL-DEFECT`
+  where a v1 time string is its epoch's local render — measured 5/5
+  sha256-agreeing on the round-1 canonical receipt with all five flagged.
+
 - **Freeze the pre-pair before the round's first probe — no probe runs on an
-  unpaired round.** Hash exactly five paths, fixed order devin/omp/kimi then
+  unpaired round.** New captures run through the v2 tool above; the v1 inline
+  form below is the archive form, kept as the shape gate for archived receipts
+  and as the independent cross-check of a v2 capture (its five digests must
+  equal the v2 receipt's `SHA256` fields). v1 form: hash exactly five paths,
+  fixed order devin/omp/kimi then
   the two shell files — the three drift-sensitive client configs plus the
   shell files that carry the same drift-prone env-key material — under a UTC
   timestamp line into the round's receipts directory:
@@ -262,7 +322,14 @@
   and five path-identity lines
   (`grep -cE '^[0-9a-f]{64}  /home/vgpnk/\.(config/devin/mcp_config\.json|omp/agent/mcp\.json|kimi-code/config\.toml|bashrc|profile)$'` = 5).
   A missing path leaves no line, so a truncated receipt false-passes
-  `sha256sum -c` — the shape gate is mandatory, not advisory.
+  `sha256sum -c` — the shape gate is mandatory, not advisory. v2 shape gate:
+  five `PATH:` stanzas, the header's UTC timestamp and repo-HEAD lines,
+  `EXISTS: yes` ×5, `SHA256:` ×5, and one
+  `MTIME_EPOCH`/`MTIME_UTC_RENDER`/`CTIME_EPOCH`/`CTIME_UTC_RENDER`/`INODE`
+  set per stanza — the tool's `selftest` (committed fixture cases, exit 0) is
+  the v2 shape and non-vacuity gate, run once per round beside the pair, and
+  the `.sha256` sidecar written beside each receipt is the durable digest of
+  the receipt itself.
 - **Why the shell files are in scope.** `PROVINCE.md:15-26` tracks
   `.bashrc:23-24` and `:61` as drift-prone (and via `:47` `.profile:4`, via
   `:124` `.bashrc:63`). A `.bashrc` edit changes provider wiring while all
@@ -281,11 +348,16 @@
   operator-owned incident, not a custody step. Hashing stores digests only,
   never contents.
 - **Take the post-pair after the last leg exits and every session is
-  closed.** Re-capture with the identical format and shape gate to
-  `"$R/config-post-pair.txt"`; then compare the live files against the frozen
-  pre-pair: `tail -n +2 "$R/config-pre-pair.txt" | sha256sum -c -` — zero
-  drift is rc 0, exactly five `OK` lines, empty stderr. Filter the timestamp
-  line (`tail -n +2`): `-c` on the unfiltered receipt emits
+  closed.** Re-capture through the tool to `"$R/config-post-pair.txt"`
+  (identical schema, labeled as the post-pair); then read the round's drift
+  reading from the instrument: `verify --live "$R/config-pre-pair.txt"` — zero
+  drift is `VERDICT: MATCH`, exit 0 — and record the pair comparison
+  `verify "$R/config-pre-pair.txt" "$R/config-post-pair.txt"` beside it. The
+  independent cross-check remains
+  `tail -n +2 "$R/config-pre-pair.txt" | sha256sum -c -` on the v1 form — five
+  `OK` lines, empty stderr — and the receipt's `SHA256` fields against the live
+  `sha256sum` reading. Filter the timestamp line (`tail -n +2`): `-c` on the
+  unfiltered receipt emits
   `sha256sum: WARNING: 1 line is improperly formatted` with rc still 0 — a
   formatting warning, not a pass and not drift.
 - **`tail -n3` is not a config selector on a five-hash receipt.** On the
@@ -301,13 +373,15 @@
   `.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt:4`; the same
   value sits at line 4 of the superseded three-path receipt,
   `.ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt`).
-- **Drift disposes the claim, not the config.** Content drift (`FAILED`,
-  rc≠0) or state drift (capture rc≠0; check-time unreadable path →
-  `FAILED open or read`, rc≠0): the zero-drift claim is VOID — record the
-  path with both hashes verbatim in the round report and LOG entry, do not
+- **Drift disposes the claim, not the config.** Content drift (sha256
+  differs), rewrite drift (same-content rewrite: inode/ctime movement with
+  equal hashes), metadata drift, or an absent path (rc 13 — never a skip):
+  each is a declared non-zero class in the tool's exit scale, and the zero-drift
+  claim is VOID — record the path with the receipt and live readings verbatim
+  in the round report and LOG entry, do not
   edit or restore the file, classify as operator-owned incident; the round's
   other axis measurements stand. Malformed receipt: re-capture once;
-  persistent malformation is VOID.
+  persistent malformation (or an unparsable receipt, rc 2) is VOID.
 - **Commit both receipts tracked.** The pair is the durable evidence — the
   zero-drift claim cites the pre-pair timestamp and the committed post-pair
   receipt (round-6/round-8 durability precedent, `LOG.md:796`, `LOG.md:850`),
```

## 3. Verified against the landed instrument

Instrument: `.ufo/gates/custody-pair/custody-pair.py`, 889 lines, sha256
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (EX-31's
declared final build; matches the live file at this seat's last read), plus
`README.md` sha256 `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba`.
Every literal the amendment pins was run against that build — transcript
`evidence/sop-commands-verbatim.txt`:

| literal in the SOP text | command run (this seat) | result |
|---|---|---|
| `capture --out … --label "…"` | `capture --out /dev/shm/ex39/evidence/landing-pre.txt --label "ex39-landing pre-pair"` | `CUSTODY_PAIR_CAPTURE: OK paths=5/5 exit=0`; writes `<receipt>.sha256` sidecar |
| `capture` on an absent path | `capture --paths <scratch>/a.json <scratch>/gone.json` | `CUSTODY_PAIR_CAPTURE: PARTIAL paths=1/2`, exit 13, receipt written with `EXISTS: no` for the absent path (`evidence/…`, run this seat) |
| `verify --live "$R/config-pre-pair.txt"` | same command | `VERDICT: MATCH paths=5 MATCH=5 exit=0` |
| `verify "$R/config-pre-pair.txt" "$R/config-post-pair.txt"` | same command | `MATCH 5/5 drift=0 exit=0`; the reversed order also matched on identical receipts, but the tool's `receipt_a` is the reference (`custody-pair.py:872`, help text) and the absent/extra-path classes are judged on the candidate side — hence the order the patch text fixes |
| `selftest` | `selftest --scratch /dev/shm` | `CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0` |
| "refuses to write over a custody path" | `capture --out /home/vgpnk/.bashrc` | `USAGE: refusing to write a receipt over a custody path`, exit 2, live `.bashrc` sha `7d2ca28a…` unchanged |
| REWRITE-DRIFT class | same-content in-place rewrite of a **scratch** copy (2-path `--paths` capture, bytes restored) | `REWRITE-DRIFT exit=11`, `moved=mtime_ns,mtime_epoch`, `SHA256-CONTRACT: 2/2 agree` — sha-only would have read MATCH |
| archived v1 receipt verifiable | `verify --live .ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt` | `SHA256-CONTRACT: 5/5 paths agree`; `METADATA-DRIFT exit 12` with 5 × `LABEL-DEFECT` (the round-1 defect reproduced, not hidden) |

Custody paths were only hashed/stated by this seat (no bytes copied, no writes);
the rewrite attack ran on this seat's own scratch files.

## 4. Before → after measurement (sim3 clone of HEAD, `/dev/shm/ex39/sim3/repo`)

```
base    R0 = 14b1682b1128d2e41085ebc79c9addeb8786d420   SKILL.md 483b0eba…  371 lines
patch   git diff --stat R0..R1:  SKILL.md | 98 +++---  (1 file changed, 86 insertions(+), 12 deletions(-))
after   R1 = e90dd6d58511ceaeabc54b3d669696d5031abb7a   SKILL.md c62a018b…  445 lines
```

| check | command | before (R0) | after (R1) |
|---|---|---|---|
| patch applies | `patch -p1 --dry-run < sop.diff` then apply | — | rc 0 both; only `SKILL.md` in the diff |
| craft section (command A's read surface) | craft-section sha256 at both revs | `5dff0b65…`, 160 lines | identical (`evidence/craft-identity.txt`) |
| SHONEN `SKILL.md:81-243` range | bytes 81-243 at both revs | — | identical (`True`) |
| recipe A | `SCORECARD.md:92-124` recipe at the rev | 82/82, 13/13, 10.0/10.0 | `{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "e90dd6d5…"}` (`evidence/recipeA-R1.json`) |
| census | `python3 .ufo/gates/c1-census-v10.py --root .` | `SKILL.md lines=371 loci=2`, PASS 0/0/0/0, exit 0 (`evidence/census-base-lane.txt`, lane repo at HEAD) | `SKILL.md lines=445 loci=2`, `SCOPE-ERRORS []`, `G2 ok`, `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0 (`evidence/census-patched.txt`) |
| citation-drift probe | `… --root . --rev <rev> --strict` / default | clean 0 findings exit 0 | clean 0 findings exit 0 (strict) and reported 0 exit 0 (default) (`evidence/probe-strict-R1.txt`, `probe-default-R1.txt`) |

The amendment's own text is locus-free: the census counts the same two SKILL.md
loci (both inside the declared `10-16`/`18-20` rows) after adding 74 lines, and
the appended text carries no `rea-agents@` pin, no bare `6.x.y` and no absolute
`path.json:NNN` pointer.

## 5. Landing coupling (for the parent)

1. **The text and the tool land together.** The literals were verified against
   tool sha `112d01dc…`; if the instrument is edited before the records commit,
   re-derive the two `capture`/`verify` forms from `--help` in the same commit.
   The covenant is the verb set + the declared exit scale, not the flags.
2. **Do not edit the tool after the round's pair is captured** (EX-31 §5.1) — the
   receipts pin the producer digest, and the new clause in edit site 1 makes that
   a standing rule for future rounds.
3. **Named mismatch for the round record (not this seat's target):** the
   authoritative pre-pair receipt captured for this round
   (`claims/c3/receipts/config-pre-pair-v2.txt`, receipt sha `fa9706c6…`) pins
   producer tool sha `4862f642…`, which is no longer on disk — the tool moved to
   `b10ad1c8…` (RV-14's capture, 12:04:50Z) and then to `112d01dc…` (EX-31's
   final, 09:06 local, also the live file). The receipt is still verifiable
   (sidecar `…txt.sha256` re-derivable, sha256 fields match the live paths), but
   its producer build is not retrievable; the round record should name that
   rather than re-verify silently. The amendment's producer-digest clause is the
   going-forward fix.
4. **Hygiene:** `.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc` and
   `claims/c3/EX-31/__pycache__/` (if it reappears) are import residue outside
   the gate dirs' intended contents — exclude them from the wave-artifacts
   commit (round-1 precedent).

## 6. Residuals / what is not claimed

- The amendment is **not landed**: `SKILL.md` at HEAD is byte-unchanged
  (`483b0eba…`); the before→after above is a clone measurement, not a repo edit.
- The SOP text proposes the interface; if the parent merges it with other
  SKILL.md patch texts this round, the merge site matters: this amendment touches
  only lines ≥249 (the registry row at `:361+` and the craft section are other
  seats' surfaces).
- The v1 archive form is retained deliberately: retired v1 receipts in the
  arc2/arc3 trees stay re-checkable by hand even if the tool is later removed.
