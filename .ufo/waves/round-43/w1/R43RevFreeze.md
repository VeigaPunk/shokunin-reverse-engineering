# R43RevFreeze — freeze-plan review of `plans/round-43-claims.md`

**Verdict: DEFECTS FOUND** — 9 predicate-read paths missing from `## Frozen paths`, 2 demonstrated
holes in the freeze-integrity enumeration carried from rounds 39–42, 3 plan-internal contradictions
(C2). All fixes land before the freeze without changing either claim's shape.

Scope: pre-freeze review of the draft only; no lane file outside `.ufo/waves/round-43/w1/` was
written. Reference implementation for both mechanics fixes:
`artifacts/R43RevFreeze/freeze_mechanics_reference.py` (stdlib-only, selfcheck PASS against the
live lane). No tools installed or upgraded (none needed; tooling directive record is empty).

---

## 1. Missing paths — predicate reads NOT in `## Frozen paths`

Round-42 precedent applied throughout: post-freeze *evidence* (the round-43 heldout dir, the
landing copies, receipts the scorer itself writes) is legitimately not frozen, and the score receipt
carries digests for files that cannot be drift-checked (R42C1Sentinel L4). The gaps below are
**inputs the predicate or its committed controls read**, whose post-freeze mutation would change
score outcomes or receipts without tripping the per-claim freeze rule.

### C1 — add to frozen paths

| # | Path (lane-relative) | Why the predicate reads it | Evidence |
|---|---|---|---|
| M1 | `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` | Plan text: "the round-42 stop receipt **stays byte-committed** at" this path. A post-freeze touch voids the citation; the freeze rule never blocks it. | `ls .ufo/waves/round-42/l1/scores/` → `c1-at-eb8215ac.json`, `c2-at-eb8215ac.json` present |
| M2 | `corpus/evidence/round-42/c2/heldout/manifest.json` | CTL-C1-1 copies it to the round-43 path; CTL-C1-2 feeds it to the tuple check. Both controls read it at scoring time. | manifest exists (78 carriers, keys incl. `declared_features`, `declared_schema`); no `observed_*` keys on carriers |
| M3 | `corpus/evidence/round-42/c2/heldout/C02/` (at minimum `envelope.json`; name the exact files the check reads) | The round-42 manifest records **declared only** — verified C02 `declared_features.gap_kinds = [extractor-failure, unpublished-entry]` with no observed fields, while C02's committed envelope carries observed gap kinds `{depth-limited, extractor-failure, unpublished-entry}`. The red control's observed tuple can only come from the committed envelope (or a fresh REA run on the C02 carrier, a reserved dev input). | commands in §7 E5 |
| M4 | `.ufo/waves/round-42/controls/c2/` — the CTL files the CTL-C1-3 driver re-scores (`CTL-C2-0-base-SKILL.md`, `CTL-C2-0b`, `CTL-C2-0c`, `CTL-C2-1`, `CTL-C2-3`, `CTL-C2-4`, `CTL-C2-8`, `CTL-C2-9`, `CTL-C2-10`, `CTL-C2-7b`, `CTL-C2-7c`, `CTL-C2-7x`, `CTL-C2-REF-v4-precedence.md`) and the receipts `c2-counter-at-freeze.json`, `dev-scores-prefreeze.json` | CTL-C1-3: "the round-42 shortcut controls re-scored … (the r42 control receipts are reproduced)". Reproduction reads the control documents and the original receipts; only `CTL-C2-7-lookup.md` is frozen today. | `ls .ufo/waves/round-42/controls/c2/` |
| M5 | `corpus/SOURCES.md` — the S135 row | P43-C1 fixtures clause: the fixtures' license basis is "cited by the new SOURCES row S135 opened this round". Nothing binds the row between FREEZE and REV; a post-freeze edit changes what the counter reads. Fix: land S135 **pre-freeze** and add the clause "the S135 row is byte-identical between FREEZE and REV" (or freeze the whole file, see C2 M7). | plan §Frontier step |
| M6 | — conditional | If `tools/round-43/heldout-gen-v4r43.py` (or any round-43 tool) imports a `tools/round-42` module at runtime (e.g. `heldout-gen-v4.py`), that module joins the predicate's read set unfrozen. The plan calls the generator "a port"; ports vendor, imports freeze. Enforce: no runtime imports of round-42 tools from round-43 tools. | plan R43-C1 generator bullet |

Post-freeze by design (do **not** freeze; bind by digest instead): `.ufo/waves/round-43/controls/c1/`,
`.ufo/waves/round-43/controls/c2/`, `.ufo/waves/round-43/l1/scores/`. The score receipt must carry
sha256 of every control receipt it cites (round-42 after.json precedent), otherwise a post-freeze
receipt edit is only caught by re-running the controls.

### C2 — add to frozen paths / fix the predicate text

| # | Path | Defect | Fix |
|---|---|---|---|
| M7 | `corpus/SOURCES.md` | **Contradiction**: P43-C2 says the table is "byte-identical to the base except nothing", but the frontier step appends S135 this round. As drafted, either the byte-identity clause fails at the measured revision (S135 present, base lacks it) or S135 can never land. Also, the C2 freeze list omits SOURCES.md entirely, so a post-freeze URL-cell edit fails late (exit 1) instead of being blocked (exit 2). | Land S135 pre-freeze; freeze `corpus/SOURCES.md` for C2; restate the clause as "byte-identical to the **freeze** commit" (S135 then included, rows keep their host paths). |
| M8 | `corpus/evidence/round-41/s126/lead1-avm-image.tsv` (+ `lead1-avm-image.tsv.sha256`, named by the map's `sha256_file`) | **Contradiction**: P43-C2 says "every out-of-lane path … bound to exactly one in-lane regular-file copy **under `corpus/evidence/round-43/local-sources/`**", but the "preserved S126 entry" binds S126's path to `corpus/evidence/round-41/s126/lead1-avm-image.tsv` (exists at the base; the existing map's one entry, `sha256_file` sidecar included). The R42LocalSrc draft map keeps that round-41 copy path verbatim. | Restate: "…exactly one in-lane regular-file copy named by the map; 17 copies under `corpus/evidence/round-43/local-sources/` plus the preserved S126 entry at its round-41 path." Freeze `corpus/evidence/round-41/s126/` for C2. |
| M9 | the 18 out-of-lane host objects (e.g. `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist`, `/var/lib/pacman/...`, `/home/vgpnk/.local/opt/...`) | Read live at score time for the re-verify clause; unfreezable by nature. **But the clause "every copy's digest re-verifies against the live host object it copies" is already unsatisfiable for S081**: the 6.7.0 npx cache dir `/home/vgpnk/.npm/_npx/a1722018f28f9df2` is **absent on this host today** (verified; it was absent at R42LocalSrc prep too — `host_present False` in `copies.tsv`), and its draft map entry carries no `source_sha256`. | Scope the clause: "where the live object exists; for rows whose host object is an npm-cache directory, the verification object is the registry tarball's cited members (committed member archives), with `src[skipped-absent]` recorded". Record S081's host-absent status in the plan's disclosed limits. |

Also note (not defects, but the plan should say them):

- **R42LocalSrc draft map copy paths are `corpus/evidence/round-42/local-sources/...`; the frozen
  round-43 map must name `corpus/evidence/round-43/local-sources/...`.** The draft map and its
  sandbox receipts (`build/receipts/gate-*.json`, rows_total 129) cannot be committed or quoted
  verbatim; the round-43 landing regenerates copies + receipts under the round-43 paths in a fresh
  sandbox clone (the plan's "this round re-verified against the live host objects" covers this —
  make it a named control receipt, not prose). Base gate receipts show rows_total 134; with S135 the
  target "≥ 129" still binds.
- One map entry serves four rows: `…/rea-agents/dist` (S048's members tar) also resolves S079/S090/S092
  (cells name `dist/` with a trailing slash, normalised away by the gate), and S066's
  `TsharkCaptureProvider.js` entry also resolves S070 (its other two paths are relative, not matched
  by the gate's ABSPATH). Verified against `gate-with-copies.json` (exit 0, `rows_failed []`, 19
  paths checked). Path-centric binding is correct; keep it.
- Closure-cited but **not predicate-read** (no freeze need): the knowledge entry, PROVINCE.md row,
  corpus/README.md rows, SCORECARD/LOG/SHONEN lines, `corpus/lessons/round-42-verifier-spotcheck.md`,
  seat artifacts under `.ufo/waves/round-43/w1/artifacts/`. Listed to close the enumeration.

## 2. Freeze-integrity mechanics — enumeration of FREEZE..REV

**What round 42 actually shipped** (both frozen this round as "carried" mechanics, both with the same
hole): `tools/round-42/c1-counter.py:2001` walks `git log --pretty=format: --name-only --no-renames
FREEZE..REV` and intersects pathnames with the frozen set; `tools/round-42/c2-counter.py:247` walks
per-path `git log --format=@@%H --name-status --no-renames FREEZE..REV -- path` and flags only
M/D/R/T/U ("a creation (`A`) is not a touch"). Neither passes any merge-diff option, and neither
asserts ancestry.

**Hole 1 — evil merge (demonstrated).** Default `git log` suppresses merge diffs
(`--diff-merges=none`). A merge commit whose conflict resolution writes a frozen path, with both
branches individually clean of it, is invisible to both walks:

```
f.txt at HEAD: freeze,EVIL            # merge resolution appended 'EVIL'; neither parent touched f.txt
default per-path walk:  @@29c800c…    # commit listed, zero status lines -> c2-counter parses nothing
c1-counter style:       (empty)       # f.txt invisible in the whole-range name-only listing
-m --diff-merges=first-parent:  M f.txt   # detected
tree backstop git diff FREEZE HEAD -- f.txt:  1 file changed   # detected
```

**Hole 2 — rewrite/re-add (demonstrated).** On rewritten history, FREEZE is no longer an ancestor
(`git merge-base --is-ancestor` exits 1), and a frozen path's re-appearance shows status `A` — which
the round-42 filter drops as "creation". Result: altered content passes the status walk.

**Fix the round-43 counter must implement** (reference code in the artifact):

1. `git merge-base --is-ancestor FREEZE REV` — hard fail (exit 2 `frozen_path_changed` class,
   never `met_target`) before any walk.
2. Per frozen path: `git log --format=@@%H --name-status --no-renames -m --diff-merges=first-parent
   FREEZE..REV -- path`; flag M/D/R/T/U always, and flag `A` whenever the path exists at FREEZE
   (`git cat-file -e FREEZE:path`) — a re-add of a frozen path is a rewrite signature. Keep
   `--no-renames` so renames surface as D(+A).
3. SKILL region: list commits with **no path filter** (`git log --format=%H FREEZE..REV`, merges
   included), extract the region at every commit, compare to the freeze region — immune to both
   holes for the region itself, and it implements "a later restore does not un-block" literally.
4. Tree-level backstop: `git rev-parse FREEZE:path` vs `REV:path` blob-hash equality for every
   frozen regular file. Cheap, option-independent; a differing blob with a clean walk means the
   walk has a bug, so log it as an internal error, not as cleanliness.

Receipt hygiene (round-42 L4 carried): the score receipt records `counter_sha256`,
`counter_sha256_at_freeze`, and **sha256 of every post-freeze control receipt it cites** (controls
under `.ufo/waves/round-43/controls/` cannot be drift-checked; digest-binding is the only honest
binding).

## 3. SKILL table-region byte comparison — the shared extraction

The region is defined by the interpreter's documented rule (`tools/round-42/sqfs-triage-v4.py`
docstring + `parse_skill`/`craft_bounds` at lines 291–560). Both tools — the frozen interpreter and
the round-43 counters — must run **one** stdlib extraction:

1. lines = `text.splitlines()` (utf-8);
2. craft section: first `_is_h2` line whose `[3:].strip().lower().startswith('queue-drain craft')`,
   body = up to the next `_is_h2` (`## ` and not `### `, case-sensitive marker, prefix
   case-insensitive);
3. marker: first line in the section **containing** `<!-- sqfs-triage-table v4 -->` (substring);
4. table: the first maximal run of `lstrip().startswith('|')` lines after the marker inside the
   section;
5. region = `lines[marker : table_end]`; canonical bytes = `'\n'.join(region).encode('utf-8')`;
   identity = sha256 equality of canonical bytes.

Validated against the live lane (artifact selfcheck): region = SKILL.md lines 521–539 (marker,
actions line, header, separator, 15 rows), sha256 `92540586b8c03dcd…`, **identical at d1681696, at
the base 6b9e64fe, and at HEAD** — so the binding "byte-identical to d1681696 at the region" is
satisfiable at the freeze today, and `git log d1681696..HEAD -- SKILL.md` (46486e7a touched the
file) does not threaten it. Two disciplines: the counter must **fail closed** (extraction failure at
any rev ⇒ exit 2, never compare empty-to-empty), and it must validate the
`<!-- sqfs-triage-actions:` line directly above the table (blank-skipping) exactly like the
interpreter, so a region without its vocabulary line is malformed, not comparable. Disclosed limit:
`splitlines()` normalises CRLF, so a CRLF flip inside the region passes the compare while raw bytes
differ; semantically inert, but the plan should say "byte-identical (canonical LF-joined region
bytes)" so both tools and any verifier agree.

## 4. Round-42 tools re-frozen for round 43 — deadlock check

**No deadlock; the constraint set is consistent and currently satisfied.** Verified: no commit in
`d1681696..HEAD` touches `tools/round-42/` at all, and the three files' blob hashes are identical
at d1681696 and HEAD (`sqfs-triage-v4.py`, `indep-eval-v4.py`, `fixtures.json`; artifact selfcheck
PASS). The drift window `d1681696..REV` is longer than `FREEZE..REV`, which is correct: it covers
the round-42 landing commits too, and those are already clean.

A round-43 commit must NOT touch (complete list): `tools/round-42/sqfs-triage-v4.py`,
`tools/round-42/indep-eval-v4.py`, `tools/round-42/fixtures.json` — by edit, delete, rename
(`--no-renames` shows D), **or mode-only change** (chmod +x trips `M` in name-status). Nothing else
under `tools/round-42/` is path-frozen (`c1-counter.py`, `c2-counter.py`, `c2-controls.py`,
`heldout-gen-v4.py`, …) — but wave 2's R42-CL2 re-run scores them "as frozen", so editing them
mid-round would void that item's semantics even where the freeze rule stays silent.

Cases that *would* need a touch, and their only honest resolutions:

1. **A defect is found in a frozen tool while scoring** (crash on an envelope shape, parse bug):
   cannot patch in-round. If the shape is avoidable, regenerate the held-out set (the generator is
   new; a different seed derivation is not available — the seed IS the freeze hash — so the fix is
   a carrier-class tweak in `heldout-gen-v4r43.py`, itself frozen at the freeze, i.e. this must be
   caught before the freeze); otherwise the claim stops honestly (target unreachable, never
   `met_target`). A pre-freeze plan amendment is the only unfreeze path; post-freeze unfreezing is
   drift, full stop.
2. **Fixture re-pin / URL rot in `fixtures.json`**: waits for the next round's plan.
3. **The port imports round-42 code** (see M6): vendor it; otherwise a bug in the imported module
   deadlocks the generator — it cannot be fixed without touching `tools/round-42`.
4. **pycache**: `.gitignore` already covers `__pycache__/` and `*.pyc` (verified); counters run
   `python3 -I -B` per the counting commands, so bytecode cannot dirty the tree.

## 5. Residual freeze-drift risk

After the fixes above, the residual risk is not in the walk mechanics but in the **semantics the
walk cannot see**: (a) freeze lists are only as complete as the predicate-read audit — this report
closes the enumeration as of the draft, but any path a future control *happens* to read (a receipt
writer's `git show`, a verifier's `jq`) is frozen only if named, so the counters should derive their
frozen sets from one manifest in `plans/round-43-claims.md` and assert every file they open is in
it; (b) the tree backstop and ancestry assertion bind content, not intent — a change delivered
through the *next* round's legitimate unfreeze (plan amendment) is indistinguishable from drift by
design, so rounds must keep freezing superseded tools rather than editing them; (c) out-of-lane host
objects (M9) are the largest live surface — npm-cache and pacman rows drift silently and can vanish
(S081 already has), which the gate correctly reports but cannot prevent, so the disclosed limit must
name the tarball/member fallback as the verification object; (d) an L1-side mistake outside git
(force-push, lane re-clone with different object store) breaks `FREEZE..REV` reachability and is
caught only by the ancestry assertion — which is why it must exit 2, never silently re-range.
Nothing observed in this review suggests the freeze rule as *repaired* is bypassable within the
lane's linear-commit discipline; the demonstrated holes were reachable only through merge
resolutions or history rewrites that the lane contract forbids seats and that the L1 does not
perform — they are cheap to close now and expensive to excuse after a score.

## 6. Evidence (commands and outputs)

- E1 Draft read: `plans/round-43-claims.md` (base `6b9e64fe`; draft commit `d22686e1`).
- E2 Region stability: extraction per §3 at three revs → all `SKILL.md:521-539 (19 lines)`,
  sha256 `92540586b8c03dcd…` (artifact selfcheck output, §3 above).
- E3 Round-42 tools clean: `git log --oneline --name-status d1681696..HEAD -- tools/round-42` →
  empty; `sha256sum` of `git show d1681696:<f>` vs worktree → SAME for all three files.
- E4 Gate at base: `python3 -I -B tools/round-41/local-source-gate.py --root . --rev 6b9e64fe --json`
  → exit 1; `rows_total 134`, 19 out-of-lane path cells, `rows_failed` = the 18 plan rows
  (S035 counted once per row despite two paths; S126 already resolves via the existing map entry
  `corpus/evidence/round-41/s126/lead1-avm-image.tsv` + `.sha256`).
- E5 C02 binding: `corpus/evidence/round-42/c2/heldout/C02/envelope.json` gap kinds =
  `{depth-limited, extractor-failure, unpublished-entry}`; manifest C02
  `declared_features.gap_kinds = [extractor-failure, unpublished-entry]`; carrier keys contain
  `declared_features`/`declared_extras`, no observed fields.
- E6 R42LocalSrc coverage: draft map 18 entries (17 copy files + preserved S126); copies.tsv
  `host_present False` for S081; `gate-with-copies.json` exit 0 `rows_failed []` at rev c4a38ea;
  `/home/vgpnk/.npm/_npx/a1722018f28f9df2` absent today, `ad9a3fdbcad992c6` present.
- E7 Evil-merge and rewrite-readd transcripts: §2 (scratch repos under
  `/fast/scratch/hyaku/kaidoku-r43/w1-R43RevFreeze`, removed after use).
- E8 `.gitignore` lines 1–2: `__pycache__/`, `*.pyc`.

Report: `.ufo/waves/round-43/w1/R43RevFreeze.md` — seat R43RevFreeze, round 43 wave 1.
