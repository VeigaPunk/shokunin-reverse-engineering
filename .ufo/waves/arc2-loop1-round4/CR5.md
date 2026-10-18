# CR5 (critic) — census completeness: missed pointer classes in the probe table

Seat CR5, wave `arc2-loop1-round4`, 2026-10-18 (stamps 19:04:44Z–19:11:55Z). Read-only
on every repo and home file; **the only write is this report**. No git mutation, no
config edit, no install, no network, no REA/MCP session; the live 91.6 MB PE analyze was
never signalled. Scratch: `/var/tmp/arc2-l4r4-CR5/` only (`/tmp` hit its 16 GB tmpfs
ceiling mid-leg — `Disk quota exceeded` on the first `git init` — so all fixtures moved
to `/var/tmp`; see §7). HEAD at leg start `158a96611f22afdfa723131f3ec27f39138020e8`;
HEAD at leg end `1692acbe48ce0eac3b7c87698be59d8a04f46a08` (another seat's `rule 11`
commit, §6). Every command below was run by this seat this session.

## 1. Verdict

**REFUTE — the probe table as drafted is not census-complete, and three of its four
gaps are silent (no finding, `exit 0`). The round-3 findings transfer, and four
additional classes do not survive contact with the gate that is C2's declared base.**

C2's claim names its base as "E15's proven implementation + R3's F1-F3 fixes + R6's
defect fixes". Measured this session, that composite does not exist: the three round-3
scripts are three different instruments, and the fixes named are fixes to two of them,
not to E15's gate. Concretely:

1. **A dead range tail is a silent pass.** A citing line reading `` `TARGET.md:7-9999` ``
   against an 8-line file produces **no finding at all** — `clean`, `exit 0` — because
   the entry's `pattern` captured only the head number and `check_entry` joins a
   one-line blob. Changing only the pattern to capture the tail on the *same citing
   line* flips it to `citation_out_of_range`. The gate can see the tail; the table
   never asks it to. **No entry in E15's 13-entry table sets `target_group_end`**
   (`citation-drift-gate.py:198-202`).
2. **An elided second token is a silent pass.** `` `TARGET.md:7,:9999` `` → `clean`,
   `exit 0`. 11 real in-repo citations use this form (§2.6).
3. **A file absent at the graded revision is a silent pass — and it makes the
   `unknown kind` guard unreachable.** An entry whose `file` does not exist at `--rev`
   yields `clean findings=0 exit=0`. Root cause is a dead branch:
   `Tree.lines` adds *every* resolution failure to `self.reported`
   (`citation-drift-gate.py:119-121`), then `check_entry` suppresses the
   `citation_file_absent` finding whenever `target in tree.reported`
   (`:163`), so the intended finding at `:164` can never fire. Measured consequence:
   feeding E16's 51 landed rows to E15's gate reports `pointer_table_unreadable` for
   **50** rows and **silence for the 51st** (`e16-e1-symbol-rea-stanza`, whose target
   `~/.kimi-code/config.toml` resolves) — the row that most needs a verdict is the one
   that gets none.
4. **A spaced path is a false red.** `` `TARGET.md :7` `` — a real pointer, and a form
   present in this repo (`LOG.md:774`) — is reported `citation_dead`, because a
   colon-only pattern misses it. Same class as R6's round-3 §3.1, now measured against
   a real repo instance rather than a scratch sample.

Two further structural findings that bear on what the parent can land:

5. **E16's table cannot serve as the census base.** Its 51 rows contain **zero**
   `corpus/knowledge/` rows — the entire C1 dead-pointer family
   (`2026-10-13-mcp-registrations.md:11,:12,:18,:88`, `2026-10-13-r4-16-frontier-rescan.md:43`)
   is unrepresented. It also encodes **no class semantics**: the landed
   `e16-table.json` rows carry only `{id, kind, file, line, must_match}`; the BASELINE,
   QUOTED and SYMBOL classes exist only in `E16.md` prose, not in the artifact. Its one
   `symbol` row is invisible to E15's gate (§1.3).
6. **The probe reddens round-3's own correct repairs.** At `1692acbe`, two entries
   report `citation_dead` against lines that are correct at HEAD:
   `PROVINCE.md:18` (which now states `` `~/.kimi-code/config.toml:3298` `` — verified
   correct, the live pin is at `:3298`) and `SCORECARD.md:59` (which now states
   `[mcp_servers.rea]` by key, no number — verified present at `:3296`). At round-3's
   HEAD the same two entries produced *different* findings. A probe whose redness
   tracks the drafter's reword rather than the tree's state reports drift on a repair
   — the class R6 named, now firing on the fix instead of the defect.

Findings 1–4 are the census-completeness attack the seat line asks for; 5–6 are
landing consequences. §4 carries the verbatim block; §5 the falsifiable
re-measurement.

## 2. Evidence — exact commands with observed output

### 2.1 Round-4 pre-pair — verified 5/5 before my leg

```
$ R=.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt
$ wc -l < "$R"                                              → 6
$ grep -cE '^[0-9a-f]{64}  /' "$R"                          → 5
$ tail -n +2 "$R" | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
$ sha256sum "$R"
231edd7d83cdfe7787e91d8b6f672f89551a6fe50013df23a5421f5ffadafc62
```

Shape 6/5, stamp `2026-10-18T19:03:02Z`, self-hash `231edd7d…`, live verify **5/5
rc=0**. No probe of mine ran, so this seat's custody contribution is nil.

### 2.2 The gate under test — identity

```
$ sha256sum /tmp/arc2-l3r3-E15/citation-drift-gate.py
0c5350b1c9a937fe9b3fd0942705edf77ecbe8c573f0965a81171e6b0eb79d8f   (415 lines)
$ python3 …/citation-drift-gate.py --selftest --expected /tmp/arc2-l3r3-E15/expected.json
CITATION_DRIFT_SELFTEST: CLEAN cases=10 passed=10 failed=0 exit=0
```

Byte-identical to E15's §5.7 identity; selftest green at 10/10 — so every defect below
is a defect of a *self-test-passing* artifact, not of a broken copy. This is the
important framing: the self-test does not cover the classes in §1.

### 2.3 The canonical class fixture — one run, six entries

Fixture `/var/tmp/arc2-l4r4-CR5/canon` (fresh `git init`, `TARGET.md` 8 lines,
`CITER.md` 5 lines, committed `4d499e2`):

```
CITER.md:1  A-dead-tail: `TARGET.md:7-9999` the whole block
CITER.md:2  B-elided: `TARGET.md:7,:9999` both tokens
CITER.md:3  C-spaced: `TARGET.md :7` the block
CITER.md:4  D-contig: `TARGET.md:7` the block
CITER.md:5  E-missing-file: `ABSENT.md:1` cites a file not in this repo
```

```
$ python3 …/citation-drift-gate.py --root . --rev HEAD \
    --table /var/tmp/arc2-l4r4-CR5/canon-table.json \
    --expected /var/tmp/arc2-l4r4-CR5/fixture-expected.json
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /var/tmp/arc2-l4r4-CR5/canon-table.json
CITATION_DRIFT: citation_out_of_range entry=A2-dead-tail-captured TARGET.md:7-9999 beyond EOF (8 lines), cited by CITER.md:1
CITATION_DRIFT: citation_dead entry=C-spaced-path CITER.md:3 states no resolvable pointer (pattern 'TARGET\\.md:([0-9]+)' absent)
CITATION_DRIFT_VERDICT: failed findings=2 exit=1
```

Reading, entry by entry — **A, B, D, E produce no finding; A2 and C do**:

| entry | citing line | pattern | verdict | correct? |
|---|---|---|---|---|
| `A-dead-tail` | `TARGET.md:7-9999` | head only | **no finding** | **NO — tail is dead** |
| `A2-dead-tail-captured` | *same line* | head + tail | `citation_out_of_range` | yes |
| `B-elided-second-token` | `TARGET.md:7,:9999` | head only | **no finding** | **NO — 2nd token dead** |
| `C-spaced-path` | `TARGET.md :7` | colon-only | `citation_dead` | **NO — real pointer** |
| `D-contiguous-control` | `TARGET.md:7` | head only | no finding | yes |
| `E-missing-file` | `ABSENT.md:1` | — | **no finding** | **NO — file absent** |

A and A2 are the **same citation**; only the `pattern` differs. That is the whole
finding: whether a dead tail is caught depends on how the drafter spelled a regex, not
on the state of the tree.

### 2.4 The tail-blindness in the table the round actually proposes

```
$ python3 -c "… E15 pointer-table.json …"   # every range-citing entry
id                             pattern                        target_group_end  window
scorecard-270-readme-bullet    '`:([0-9]+)`'                  None              None
scorecard-270-readme-head-claim 'at `:([0-9]+)` in HEAD'       None              None
scorecard-69-readme-177        'corpus/README\.md:([0-9]+)'   None              None
scorecard-72-readme-nitrow     'corpus/README\.md:([0-9]+)'   None              None
province-18-kimi-pin           'relocated it to :([0-9]+)'    None              None
scorecard-698-live-pin         'config\.toml:([0-9]+)'        None              None
scorecard-59-pin-receipted     'config\.toml:([0-9]+)'        None              None
mcpreg-11-kimi-source          'config\.toml lines ([0-9]+)'  None              None
mcpreg-12-kimi-verify          "sed -n '([0-9]+),"            None              None
mcpreg-18-kimi-line            'config\.toml line ([0-9]+)'   None              3
mcpreg-88-erratum              'config\.toml:([0-9]+)'        None              None
r416-43-kimi-stanza            'config\.toml:([0-9]+)'        None              None

entries with target_group_end set: 0 of 13
```

**Observation.** Three entries cite a *range* in their own text
(`mcpreg-11` says `lines 1285-1292`; `mcpreg-12` says `sed -n '1285,1293p'`;
`r416-43` says `:1284-1292`) and every one of them captures the head only. The live run
shows the collapse directly:

```
CITATION_DRIFT: citation_dead entry=mcpreg-11-kimi-source …:11 cites @config-toml-landmarks:1285-1285, …
CITATION_DRIFT: citation_dead entry=mcpreg-12-kimi-verify …:12 cites @config-toml-landmarks:1285-1285, …
```

The report says `1285-1285` where the source says `1285-1292`. The range is silently
halved before it is checked. `citation-drift-gate.py:198-202` reads
`m.group(entry.get("target_group", 1))` and
`m.group(entry.get("target_group_end", entry.get("target_group", 1)) or lo)` — with
`target_group_end` absent, `hi == lo`.

### 2.5 The dead `citation_file_absent` branch

```
$ sed -n '119,121p' /tmp/arc2-l3r3-E15/citation-drift-gate.py
            text, err = git_show(self.root, self.rev, target)
            if err:
                self.reported.add(target)
$ sed -n '161,164p' /tmp/arc2-l3r3-E15/citation-drift-gate.py
        # a resolution failure was already reported by Tree (snapshot classes)
        # or is reported here for an absent in-repo file
        if target not in tree.reported:
            findings.add("citation_file_absent", eid, "%s: %s" % (target, err))
```

`Tree.lines` unconditionally adds the failing target to `reported` (`:121`); the comment
at `:161-162` says the finding is filed "here for an absent in-repo file", but the
guard at `:163` suppresses exactly that case. The `citation_file_absent` finding is
therefore **unreachable for in-repo files** — it can only fire for `@snapshot` targets,
which `_snapshot` already reports under its own kinds.

Measured consequence, feeding E16's landed table to E15's gate:

```
$ python3 …/citation-drift-gate.py --root . --rev HEAD \
    --table /var/tmp/arc2-l4r4-CR5/e16-landed-as-entries.json --expected …
exit=2
     50 pointer_table_unreadable
rows NOT flagged:  e16-e1-symbol-rea-stanza kind= symbol
```

50 of 51 rows are `unknown kind 'line'`; the 51st — the `symbol` row, the only one
whose target resolves — produces **nothing**. Its target file exists, so `check_entry`
proceeds past `:164` and falls through to the bottom of the function without a kind
match and without the `unknown kind` guard. That guard sits after the `extracted`
block's `return`, so any unknown kind on a *resolvable* file is silently skipped.

### 2.6 Real-repo exposure of the missed classes

Pointer-form census at `158a966`, all non-`.ufo` tracked files, read via
`git show {rev}:{path}`:

```
colon_range  (path:N-M)      295
colon_single (path:N)        230
prose_lines  (lines N-M)      50
sed_range    (sed -n 'N,Mp')  29
distinct file:line loci      443
```

**Range tails.** Of 294 range citations, 129 name a file that has at least one pinned
row in either table. Of those: **11 have both ends pinned, 11 have exactly one end
pinned, 107 have neither.** The one-end-only set includes real, load-bearing
citations — `LOG.md:735` → `SKILL.md:81-195`, `SCORECARD.md:659` → `SCORECARD.md:16-17`,
`SCORECARD.md:717` → `SCORECARD.md:68-72`, `SKILL.md:246` → `PROVINCE.md:108-113`.
Three range citations at HEAD have a tail **beyond EOF**:

```
corpus/knowledge/2026-10-14-r14-02-final-sweep.md:99   cites SHONEN.md:7-18  (SHONEN.md is 12 lines)
corpus/knowledge/2026-10-14-r14-02-final-sweep.md:150  cites SHONEN.md:11-18 (SHONEN.md is 12 lines)
evidence/round-1-2026-10-15/rubric.json:75             cites SHONEN.md:11-18 (SHONEN.md is 12 lines)
```

All three resolve at their citing entry's own revision — `6645585`, where `SHONEN.md`
is 18 lines (`git show 6645585:SHONEN.md | wc -l` → 18; at HEAD → 12). They are
convention-legal baseline-revision citations, which is precisely why a *tail-blind*
gate is the wrong instrument for them: it cannot distinguish "dead tail" from
"baseline-revision tail" because it never looks.

**Elided second tokens.** 11 real citations of the form `path:N,:M`:

```
LOG.md:995   corpus/knowledge/2026-10-13-r3-jq-provenance.md:60,:136
LOG.md:996   corpus/README.md:90,:160
LOG.md:1005  PROVINCE.md:10,:18
LOG.md:1060  corpus/knowledge/2026-10-13-mcp-registrations.md:9,:80
LOG.md:1083  SCORECARD.md:270, :698
SCORECARD.md:680, :696, :718  corpus/README.md:90,:160
SCORECARD.md:697, :741         PROVINCE.md:10,:18
SCORECARD.md:759               corpus/knowledge/2026-10-13-mcp-registrations.md:9,:80
```

Every one of these carries a second token that no entry in either table reads.

**Spaced paths.** One real instance, `LOG.md:774`:
`corpus/README.md :131 (four-nit dispositions) + :163 (held-vs-frontier` — a space
before the colon, and a second bare `:163`. A colon-only pattern misses the first
token; nothing reads the second.

**Multi-line needles.** No pinned needle in either table currently needs to span a
line break (measured: 0 of 68), so this class is latent rather than live. But it is
armed: the same phrase written with a literal space fails over a wrapped phrase,
while the `\s+` spelling of the same phrase succeeds, because `re.M` makes `^`/`$`
work but does not make a literal space match a newline. Fixture:

```
TARGET.md:4  the claim is held, not
TARGET.md:5  frontier as recorded
CITER.md:1   cited: `TARGET.md:4-5` holds the claim
```

```
must_match: "held, not frontier"      → citation_dead   (false red; phrase IS present, wrapped)
must_match: "held, not\s+frontier"    → no finding     (correct)
```

Observation: whether a wrapped phrase reads green or red is a property of the
needle's *spelling*, not of the tree.

### 2.7 E16's landed table — coverage and class encoding

```
$ python3 -c "… e16-table.json …"
    5  LOG.md
    5  PROVINCE.md
   25  SCORECARD.md
    3  SHONEN.md
   11  SKILL.md
    1  corpus/README.md
    1  ~/.kimi-code/config.toml
corpus/knowledge rows: 0
total rows: 51
$ grep -c 'mcp-registrations\|r4-16-frontier' e16-table.json → 0
$ python3 -c "… row keys …"
top-level keys: ['pin_rev', 'pointers']
row keys (first row): ['id', 'kind', 'file', 'line', 'must_match']
kind values: {'line': 50, 'symbol': 1}
```

**Observation.** The table grades 50 green / 1 red at both `158a966` and `1692acbe`
(the single red being `e16-x14-sc270-target`, C1's pending repair) — but it carries no
row into `corpus/knowledge/` at all, so the C1 dead-pointer family it was written to
cover is outside its census. And the three classes E16.md documents in prose (BASELINE,
QUOTED, SYMBOL) are **not encoded in the JSON**: a consumer reading `e16-table.json`
cannot tell a baseline-revision row from a current-state row, and the one `symbol` row
is silent when fed to E15's gate (§2.5).

### 2.8 The gate reddens round-3's own repairs

Same table, same command, two revisions:

```
$ for R in 679af5d… 1692acbe…; do python3 …/citation-drift-gate.py --root . --rev $R \
    --table /tmp/arc2-l3r3-E15/pointer-table.json --expected … --snapshot-dir …; done

=== rev 679af5d ===
CITATION_DRIFT: citation_dead entry=province-18-kimi-pin PROVINCE.md:18 cites @config-toml-landmarks:3227-3227, which lacks … (holds '')
CITATION_DRIFT: citation_historical_ok entry=scorecard-59-pin-receipted SCORECARD.md:59 cites @config-toml-landmarks:2940-2940, … [stamp: 16:57:35Z custody receipt]
CITATION_DRIFT_VERDICT: failed findings=10 exit=1

=== rev 1692acb ===
CITATION_DRIFT: citation_dead entry=province-18-kimi-pin PROVINCE.md:18 states no resolvable pointer (pattern 'relocated it to :([0-9]+)' absent)
CITATION_DRIFT: citation_dead entry=scorecard-59-pin-receipted SCORECARD.md:59 states no resolvable pointer (pattern 'config\\.toml:([0-9]+)' absent)
CITATION_DRIFT_VERDICT: failed findings=10 exit=1
```

Both lines are correct at `1692acbe`:

```
$ sed -n '18p' PROVINCE.md
`rea-agents@6.7.0` (`~/.kimi-code/config.toml:3298` at the 17:55:49Z receipt; value unchanged through 2026-10-18's rewrites — earlier pointers :2940 [16:57:35Z receipt] and :3227 [17:32Z rewrite] are historical). Cache/catalog
$ sed -n '3298p' /home/vgpnk/.kimi-code/config.toml
args = [ "-y", "rea-agents@6.7.0", "mcp" ]
$ sed -n '59p' SCORECARD.md
  (arc2-loop1-round2): Kimi pin is `rea-agents@6.7.0` in `config.toml`'s `[mcp_servers.rea]` per the
$ grep -n '^\[mcp_servers\.rea\]' /home/vgpnk/.kimi-code/config.toml
3296:[mcp_servers.rea]
```

`PROVINCE.md:18` states `:3298` and `:3298` **is** the pin. `SCORECARD.md:59` states the
stanza key and no number — the content-anchor form C2 mandates — and the key is present
at `:3296`. The probe calls both `citation_dead`. The finding count is identical (10)
across the two revisions while its *composition* changed, which is exactly the
signal-vs-noise failure: a reader watching the count sees no change, and a reader
watching the findings sees two correct lines reddened.

### 2.9 C2's declared base is a composite of three different scripts

```
$ for f in citation-drift-gate.py c2-census.py c1-census-v9.py; do … done
citation-drift-gate.py   1 check_entry; 0 in_strict; 415 lines
c2-census.py             0 check_entry; 3 in_strict; 274 lines
c1-census-v9.py          0 check_entry; 0 in_strict; 429 lines
```

- **R6's defects 1, 2, 3, 7** target `c2-census.py` — its exit expression, its
  `in_strict`/`wide_review` partition, its `'still lists already-held'` anchor, and its
  `git show`-only read path (`c2-census.py:82`, `:222`, `:126-128`, `:274`). None of
  those lines exist in E15's gate.
- **R3's F1–F3** target `verify-citations.py` — C3's round-3 draft, extracted by R3
  from `C3.md:415-949`. That artifact never landed; `.ufo/gates/` does not exist
  (`ls: cannot access '.ufo/gates': No such file or directory`), and
  `git ls-files | grep -c 'verify-citations'` → 0.
- **E15's gate** is a third artifact with its own `check_entry`/`Tree` structure.

So "E15's proven implementation + R3's F1-F3 + R6's defect fixes" names a file that
would have to be assembled from three sources. Measured: feeding E16's rows to E15's
gate is `could-not-evaluate` exit 2 (§2.5) — the two round-3 tables are not composable
as they stand, and neither table plus E15's gate constitutes a working probe.

**E15's gate error paths do pass R3's F1 class** (this is a point in its favour and I
record it): missing `--root`, unreadable table, and unknown-kind entries all return
`could-not-evaluate` `exit 2`, not an uncaught traceback with `rc=1`.

### 2.10 E22's census at HEAD — re-confirmed, and its PTR blindness

```
$ python3 /var/tmp/arc2-l4r4-CR5/e22-fence.py --root . --json
verdict: FAIL
  undeclared: 2
      SCORECARD.md block 731-737  (5 asserts, 4 AMBIGUOUS, 1 current-ok)
      SCORECARD.md block 747-766  (1 assert, current-ok)
  stale: 0   ambiguous: 0   unresolved: 0   scope_errors: 0
```

The instrument's fence extracted from `.ufo/waves/arc2-loop1-round2/E22.md:264-692` is
**byte-identical** to the seat-line identity: sha256
`213fe679838ea217f4d34aa7d0e85bf73845a42ae49b68c9d8d52b4d38e6707c`, 429 lines. Its
`UNDECLARED` verdict at HEAD is **FAIL undeclared=2**, both blocks created by round-2's
own record append — E22's `SCOPE` table ends at `SCORECARD.md 635-701`
(`e22-fence.py:103`). C3's re-key claim is therefore live and correctly scoped.

Its pointer regex remains blind to the real corpus:

```
$ python3 -c "… PTR = re.compile(r'((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)') …"
  MISS   'corpus/README.md:90,:160'      MISS   '`corpus/README.md :131`'
  MISS   '`SCORECARD.md:16-17`'          MISS   '`SKILL.md:81-195`'
  MATCH  '`~/.kimi-code/config.toml:3298`'
  MISS   '`config.toml lines 1285-1292`' MISS   '`PROVINCE.md:114-116`'
```

Repo-wide, over the forms the lane actually uses:

```
total real pointer-token instances (in-repo forms): 561
  visible to E22's PTR regex: 17
  INVISIBLE to E22's PTR regex: 544
missed by form: {'colon_range': 291, 'colon_single': 214, 'spaced': 1, 'sed': 29,
                 'prose_lines': 4, 'prose_line': 5}
```

**Observation: 544 of 561 real pointer tokens — 97% — are invisible to E22's `PTR`
regex.** It requires a `~`/`/` prefix, a `.json|.toml|.yaml` extension, and a colon; the
lane's dominant form is `.md` with a colon (214 single + 291 range), and every prose
`lines N-M` and `sed -n 'N,Mp'` form is missed outright. R6 measured this at 7/7 on
the round-3 pointer family; at repo scope the miss rate is 544/561.

### 2.11 The content-anchor form the claim mandates

C2 requires "NO config.toml line numbers — content-anchor form instead". E15's gate has
an `anchor` kind, so I tested whether it can express that:

```
$ # entry: kind=anchor, file=TARGET.md, must_match='golf line seven', NO pin_line
CITATION_DRIFT: citation_moved entry=anchor-no-line-pin TARGET.md: content at [7], citation pins None
CITATION_DRIFT_VERDICT: failed findings=1 exit=1
```

`citation-drift-gate.py:170` is
`elif entry.get("pin_line") not in hits:` — with `pin_line` absent, `None not in [7]`
is always true, so a pure content anchor with no line pin is `citation_moved` **by
construction**. The `anchor` kind can only express "content is at this specific line",
which is the line-pinning the claim forbids. With `pin_line` supplied it works
correctly (verified: needle present at the pin → `clean exit 0`; needle moved away →
`citation_dead exit 1`), but that is a line pin in disguise.

Observation: the gate's three kinds are `extracted` (read a number out of the citing
line), `exact` (match the citing line at a pinned line), and `anchor` (match content
*at a pinned line*). **None of the three expresses "this content exists, at any line"** —
which is precisely the durable repair round-3 landed on `SCORECARD.md:59`.

## 3. Cross-check — what R6's round-3 findings did and did not transfer

| R6 round-3 finding | transfers to E15's gate? | measured here |
|---|---|---|
| 3.1 case-sensitivity / form coverage | **yes, and worse** | colon-only misses the `lines N-M` and spaced forms; 544/561 invisible (§2.10) |
| 2.4 note-extent escape | n/a — different script | `c2-census.py` only; E15's gate has no note partition |
| 2.3 pointer clause anchor-fragile | **yes, as §2.8** | a reword flips the finding; here the reword was round-3's own *repair* |
| 2.9 Git-objects-only read | n/a — E15's gate has a `--rev` and a worktree mode | it names the revision it grades; not a defect of this gate |
| 2.7 existence-vs-content predicate | **yes** | `exact` checks the pinned line only; a needle present elsewhere is `citation_dead` — measured |
| 3.2 "repair makes the count rise" | **yes** | the finding count is 10 at both revisions while its composition changed (§2.8) |

Three of R6's six findings transfer; the ones that do not belong to a different script,
which is itself the §2.9 finding.

## 4. VERBATIM — text the parent may land (as-is if used)

```text
CR5 review of the C2 probe base (arc2-loop1-round4, HEAD 158a966 → 1692acbe).

Do NOT land "E15's implementation + R3's F1-F3 + R6's defect fixes" as the C2 base.
Those three sets of fixes target three different scripts: R6's defects 1-3/7 are
fixes to c2-census.py (274 lines, in_strict/wide_review, anchor 'still lists
already-held', exit line :274); R3's F1-F3 target verify-citations.py (C3's
round-3 draft, which never landed — .ufo/gates/ does not exist); E15's gate is
citation-drift-gate.py (415 lines, check_entry/Tree). No single artifact carries
all the named fixes, and the two round-3 tables are not composable: feeding
E16's 51 landed rows to E15's gate yields could-not-evaluate exit 2 with 50x
"unknown kind 'line'" and SILENCE for the 51st (the symbol row).

Four census-completeness defects in E15's gate, all fixture-proven this session
(fixture /var/tmp/arc2-l4r4-CR5/canon, TARGET.md 8 lines):
  (1) A DEAD RANGE TAIL IS A SILENT PASS. A citing line "TARGET.md:7-9999"
      produces NO finding — clean, exit 0 — because the entry's pattern captured
      only the head and check_entry joins a one-line blob. Change ONLY the
      pattern to capture the tail, same citing line -> citation_out_of_range.
      NO entry in E15's 13-entry table sets target_group_end, so the three range
      entries (mcpreg-11 "lines 1285-1292", mcpreg-12 "sed -n '1285,1293p'",
      r416-43 ":1284-1292") each silently halve their range before checking —
      visible in the live output as "cites @config-toml-landmarks:1285-1285".
      Fix: capture the tail (target_group_end) and fail on a dead tail; and
      require target_group_end whenever the citing pattern can match a range.
  (2) AN ELIDED SECOND TOKEN IS A SILENT PASS. "TARGET.md:7,:9999" -> clean,
      exit 0. 11 real in-repo citations use path:N,:M (LOG.md:995,:996,:1005,
      :1060,:1083; SCORECARD.md:680,:696,:697,:718,:741,:759). Fix: a second
      capture group for the elided token, checked like the first.
  (3) A FILE ABSENT AT THE GRADED REVISION IS A SILENT PASS, and the
      unknown-kind guard is unreachable. check_entry's citation_file_absent
      branch (:163) is dead: Tree.lines adds every resolution failure to
      self.reported (:121), and :163 suppresses the finding for exactly that
      case. Fixture: an entry citing ABSENT.md -> clean findings=0 exit=0.
      Consequence: the 51st E16 row (e16-e1-symbol-rea-stanza, the only one
      whose target resolves) gets no verdict at all, because the unknown-kind
      guard sits after the extracted block's return. Fix: report
      citation_file_absent for in-repo targets (drop the :163 guard for the
      git-show path), and move the unknown-kind guard so it cannot be skipped.
  (4) A SPACED PATH IS A FALSE RED. "TARGET.md :7" — a real pointer, and the
      form at LOG.md:774 ("corpus/README.md :131 ... + :163") — is reported
      citation_dead because a colon-only pattern misses it. Fix: allow optional
      whitespace around the separator, as R6's round-3 §3.1 already prescribed.

Two landing consequences:
  (5) E16's table cannot serve as the census base: ZERO rows into
      corpus/knowledge/, so the whole C1 dead-pointer family
      (mcp-registrations.md:11,:12,:18,:88; r4-16-frontier-rescan.md:43) is
      outside its census; and the landed e16-table.json encodes no class
      semantics — rows are {id,kind,file,line,must_match} only, so BASELINE /
      QUOTED / SYMBOL exist in E16.md prose but not in the artifact. A consumer
      cannot tell a baseline-revision row from a current-state row.
  (6) The probe reddens round-3's own correct repairs. At 1692acbe,
      province-18-kimi-pin and scorecard-59-pin-receipted report
      citation_dead against PROVINCE.md:18 (states config.toml:3298 — verified
      correct, the pin IS at :3298) and SCORECARD.md:59 (states the stanza key
      [mcp_servers.rea] and no number — the content-anchor form C2 mandates —
      verified present at :3296). The finding COUNT is 10 at both revisions
      while its composition changed, so a count-watcher sees no signal.

Also measured, for the re-key half of C3:
  (7) E22's c1-census-v9.py (fence sha256 213fe679…, 429 lines, byte-identical
      to E22.md:264-692) is FAIL undeclared=2 at HEAD, both blocks
      (SCORECARD.md 731-737, 747-766) created by round-2's own record append;
      its SCOPE table ends at SCORECARD.md 635-701. Its PTR regex is blind to
      544 of 561 real in-repo pointer tokens (97%): it requires a ~// prefix
      and a .json|.toml|.yaml extension, so it misses every .md citation
      (214 single + 291 range), all 29 sed forms and all 4 prose 'lines N-M'.
  (8) E15's gate CANNOT express a pure content anchor. Its 'anchor' kind is
      `elif entry.get("pin_line") not in hits:` — with no pin_line, None not in
      hits is always true, so a content-only entry is citation_moved by
      construction. Its three kinds (extracted/exact/anchor) all pin a line.
      C2 mandates the content-anchor form for config.toml; the gate has no
      vocabulary for it.

Latent, armed: a needle written with a LITERAL SPACE fails over a phrase the
repo has wrapped across two lines (citation_dead — false red), while the same
phrase spelled \s+ succeeds. re.M makes ^/$ work but does not make a literal
space match a newline. No pinned needle currently needs to wrap (0 of 68), but
the failure mode is a needle-spelling property, not a tree property.
```

## 5. Falsifiable re-measurement (the acceptance test I propose)

Each command is executable with no scratch state beyond the named fixture:

```bash
# 0. the fixture (fresh repo, TARGET.md 8 lines) — the six-entry class table
#    A: TARGET.md:7-9999   B: TARGET.md:7,:9999   C: TARGET.md :7
#    D: TARGET.md:7        E: ABSENT.md:1
python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --root /var/tmp/arc2-l4r4-CR5/canon \
  --rev HEAD --table /var/tmp/arc2-l4r4-CR5/canon-table.json \
  --expected /var/tmp/arc2-l4r4-CR5/fixture-expected.json
#  TODAY: 2 findings, exit 1 — A, B, E silent; C false red.
#  AFTER the fixes: A citation_out_of_range, B citation_out_of_range,
#  C clean, D clean, E citation_file_absent -> exit 1 with 3 findings.

# 1. a dead tail must not pass
#    expect a finding naming TARGET.md:7-9999 (today: none)

# 2. an elided second token must not pass
#    expect a finding naming :9999 (today: none)

# 3. a file absent at --rev must not pass
#    expect citation_file_absent (today: clean findings=0 exit=0)

# 4. the two round-3 tables must be composable, or the incompatibility declared
python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --root . --rev HEAD \
  --table /tmp/arc2-l4r4-CR5/e16-landed-as-entries.json --expected …
#    TODAY: could-not-evaluate exit 2, 50 unknown-kind + 1 silent skip.
#    AFTER: either the rows are consumable, or the exit names the mismatch.

# 5. round-3's own repairs must not be red
python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --root . --rev 1692acbe \
  --table /tmp/arc2-l3r3-E15/pointer-table.json --expected … --snapshot-dir …
#    TODAY: province-18-kimi-pin and scorecard-59-pin-receipted both
#    citation_dead on lines verified correct at HEAD.
#    AFTER: PROVINCE.md:18 (states :3298, correct) clean;
#    SCORECARD.md:59 (content-anchor, no number) clean.

# 6. a pure content anchor must be expressible
#    expect a kind that reports "content present at :N" without a line pin
#    (today: anchor with no pin_line -> citation_moved by construction)
```

## 6. Round-state note the parent should carry

HEAD moved during this leg: `158a966` (round-4 claim base) → `1692acbe` ("rule 11"),
which landed `e16-table.json` at repo root (sha256
`89eddae03d52cb8baede95256439f355d39c765d8f4700d75e73c4e7d5a20e31`, byte-identical
to `/tmp/arc2-l3r3-E16/e16-table.json`) plus `.ufo/waves/arc2-loop1-round4/{E23.md,E4.md}`
and a copy of the round-4 pre-pair receipt. `SKILL.md` is 336 lines at both revisions —
**rule 11 has not landed in `SKILL.md` yet**, despite the commit message. I graded E16's
table at both revisions: 50 green / 1 red (`e16-x14-sc270-target`) at each. Other seats'
round-4 reports (`E13.md`, `E20.md`, `SC2.md`, `V3.md`) were present as untracked files
at leg end; I did not read them beyond `E20.md`'s header, and nothing in this report
depends on them.

## 7. Scope compliance and residue

- **Only write: this report.** `git status --porcelain` at leg start →
  `?? .ufo/waves/arc2-loop1-round4/` only; at leg end the same plus four other seats'
  untracked reports (`E13.md`, `E20.md`, `SC2.md`, `V3.md`) — not mine, not touched.
  No git mutation in the lane repo by me; no config edits, no installs, no network
  fetches, no REA/MCP session.
- **All scratch under `/var/tmp/arc2-l4r4-CR5/`** (my namespace). `/tmp` filled to its
  16 GB tmpfs ceiling mid-leg (`Disk quota exceeded` on the first `git init`); I moved
  every fixture to `/var/tmp` (disk-backed, 773 GB free) and left no `/tmp` residue of
  mine beyond an abandoned empty directory. No other seat's files were touched.
- **Fixtures** (each a fresh `git init`, no live-tree write):
  `canon/` (`4d499e2`, the six-entry class table), `fx/`, `fx2/`, `final/`, `clone/`
  (a `git archive HEAD` materialization), plus the tables and captured outputs.
- The live 91.6 MB PE analyze was observed read-only via `df`/`du` only (it is what
  filled `/tmp`); never signalled, never renice'd, never touched.
- Home files were read as digests and stanza greps only; no secret value read or
  emitted. Every `path:line` pointer above was resolved by a command shown this session.

### Pointers used (all resolved this session)

`/tmp/arc2-l3r3-E15/citation-drift-gate.py:119-121` (the `reported` add),
`:161-164` (the dead `citation_file_absent` branch), `:170` (the `anchor` pin_line
test), `:198-202` (`target_group`/`target_group_end` read), `:213-226` (window + blob
join), `:240-244` (`run_check`); `/tmp/arc2-l3r3-E15/pointer-table.json` (13 entries,
0 with `target_group_end`); `e16-table.json` (landed, 51 rows, 0 into
`corpus/knowledge/`); `/var/tmp/arc2-l4r4-CR5/e22-fence.py:103` (SCOPE end `635-701`),
`:108` (the `PTR` regex); `PROVINCE.md:18`; `SCORECARD.md:59`, `:270`;
`corpus/knowledge/2026-10-13-mcp-registrations.md:11,:12,:18,:88`;
`corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43`;
`corpus/knowledge/2026-10-14-r14-02-final-sweep.md:99,:150`;
`evidence/round-1-2026-10-15/rubric.json:75`; `LOG.md:774`, `:995-1005`, `:1060`,
`:1083`; `corpus/lessons/2026-10-15-round-1.md:82`;
`.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt:1-6`.
