# PathsAudit — SOURCES `## Paths` B→REV (round 18 wave 2)

HOLDS

Seat: KaidokuR18.PathsAudit (reviewer, author-side advisory). Axes worked: calibration (verdict grounded in reproduced commands), operability (reproducing commands pasted), depth (chain-level, not token-level, checks). No tools installed (none needed; pacman pause respected).

Target: `git diff 9011581d84527ba34c675f9cf912e54d2e72d470 b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- corpus/SOURCES.md`; audit the `## Paths` section: S032 removed from the route path, two new paths, every id resolves, no row cell other than allowed fields changed.

## Commands (all exit codes pasted)

```
$ git diff 9011581d84527ba34c675f9cf912e54d2e72d470 b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- corpus/SOURCES.md
corpus/SOURCES.md | 12 +++++++++++-
1 file changed, 11 insertions(+), 1 deletion(-)
exit=0
```
Observation: exactly three hunks — (1) four added rows S033–S036 after S032; (2) the "Go carrier route diagnosis" bullet rewritten (S032 dropped from the chain) plus two new bullets; (3) one added round-18 census entry (+blank) and two added Leads bullets. 11 insertions = 4 rows + 1 route line + 2 path bullets + 1 census + 1 blank + 2 leads; 1 deletion = the old route line. Nothing else in the file changed.

```
$ git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:corpus/SOURCES.md > /tmp/sources_rev.md   # 77 lines
exit=0
$ git show 9011581d84527ba34c675f9cf912e54d2e72d470:corpus/SOURCES.md > /tmp/sources_base.md  # 67 lines
exit=0
$ git log -1 --format='%H %s' b2aad08ceeee8dd125ce0d316056d8bd766c7f94
b2aad08ceeee8dd125ce0d316056d8bd766c7f94 round-18: carrier runs, corpus corrections, knowledge entry, registry and SOURCES (pre-falsify)
exit=0
$ git diff --stat b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- corpus/SOURCES.md   # working tree vs REV
exit=0            # empty output: live file matches REV, anchors below apply to the working tree too
```

Analysis (read-only scripts on the two extracted git objects, run as `python3 -I -B /tmp/paths_audit.py` and `/tmp/paths_audit2.py`, both `exit=0`):

```
REV rows: 36 unique: 36 | BASE rows: 32 unique: 32
added rows: ['S033', 'S034', 'S035', 'S036'] | removed rows: [] | dup ids REV: []
existing row lines changed B->REV: NONE
BASE L44 chain=['S024','S026','S031','S025','S003','S023','S029','S030','S032']  <== S032 PRESENT
REV  L48 chain=['S024','S026','S031','S025','S003','S023','S029','S030']
REV  L49 chain=['S034','S035','S023','S003','S033']  missing=[]
REV  L50 chain=['S036']  missing=[]
(all 10 REV path bullets: missing=[] for every id)
BASE header cols=11 bad_rows=NONE | REV header cols=11 bad_rows=NONE | header identical: True
REV S032 at line 38, S033 at 39, S034 at 40, S035 at 41, S036 at 42
```

## Findings (all observations unless labeled)

1. **S032 removed from the route path — holds.** BASE `corpus/SOURCES.md:44` chain ends `… → S030 → S032`; REV `corpus/SOURCES.md:48` chain is `S024 → S026 → S031 → S025 → S003 → S023 → S029 → S030` with no S032. Caveat for token-scan auditors: the same REV line still *mentions* S032 in its trailing note "(Round 18: S032 left this path; its successor S033 closes the Swiss replay path below.)" — the note is outside the chain (text between the em-dash and the first colon); a naive `grep S032` over the bullet would false-positive. The S032 row itself remains at REV `corpus/SOURCES.md:38` (superseded by S033 per its `teaches` cell) — removal was from the path, not the registry, matching the target wording.

2. **Exactly two new paths — holds.** REV `corpus/SOURCES.md:49` "Swiss-map replay — S034 → S035 → S023 → S003 → S033" and `:50` "Revision pins under jj — S036". Path bullets go 8 (BASE :42–:49) → 10 (REV :46–:55); the unified diff of the Paths sections shows only these 3 changed lines (1 rewrite + 2 additions); every other bullet is byte-identical. Inference (qualitative): each new bullet's prose has one clause per chain element in chain order (5 clauses for :49, 1 for :50), so the chains are not decorative.

3. **Every id resolves — holds.** All 10 REV path bullets: every `S\d+` token in the chain resolves to a registry row (missing=[] for all). New rows S033–S036 exist at REV `corpus/SOURCES.md:39–:42`, ids unique (36 unique rows, no dups, no removals), each with the full 11-column shape matching the header (`bad_rows=NONE`); header and separator rows are byte-identical to BASE. Inference: the REV row-id set is S001–S036 (32 unique BASE ids + exactly the 4 added, 0 removed).

4. **No row cell other than allowed fields changed — holds, in the strongest form.** Byte-exact comparison of every `| Sxxx |` line B→REV: `existing row lines changed B->REV: NONE` — zero existing cells (allowed or not) were touched; the only row-level changes are four whole-row additions. Note: no contract text defines "allowed fields" for SOURCES rows (wave2-spec.json:397-401, my item, is the only definition and adds none), so the check passes vacuously under any definition — zero edits is stricter than any allow-list.

## Consistency with claims.json amendments (inference)

- C1 "S033 (supersedes S032)" ↔ REV :48 note "its successor S033" and S033's `teaches` cell "supersedes S032" (:39). Consistent.
- C2 sourced S036 ↔ new path :50. C3 sourced S034/S035 ↔ new path :49. Consistent.
- Census entry REV :67 arithmetic: 11 identified − 4 included = 7 excluded ✓; its enumeration lists 6 exclusion reasons, one ("jj revsets/bookmarks and config defaults") plausibly covering 2 candidates — out of my scope (SearchLogAudit/CensusRerun seats), no finding filed.

## Residual risk / scope boundaries

- used-by resolution for the new rows and census/search-log content are sibling seats' scope (UsedByResolve, SearchLogAudit); not checked here.
- The route-line rewrite also dropped the prose clause "and finally the open swiss-map change for post-bootstrap markup failures" — part of the same expected line edit, not a row change; no finding.
- No reproducing failure found; nothing to reproduce.

Verdict: **HOLDS** on all four target checks.
