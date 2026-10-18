# CR2 (critic) — attack on C2: is a registered drift *probe* a no-op over the re-keyed census + content-anchor discipline?

Seat CR2, wave `arc2-loop1-round4`, read-only on the repo and home. Every command
below was run by this seat this session (2026-10-18, stamps 19:04Z–19:14Z).
HEAD at leg start `158a96611f22afdfa723131f3ec27f39138020e8`; HEAD advanced to
`1692acbe48ce0eac3b7c87698be59d8a04f46a08` ("rule 11") at 19:09Z and every
load-bearing measurement was re-run at the new HEAD. `git status --porcelain` at
my leg start → `?? .ufo/waves/arc2-loop1-round4/` only; at my leg end the only
new entries are other seats' report files. **This report is my only write.**
Scratch confined to `/tmp/arc2-l4r4-CR2/` (48 MB; `/tmp` is a 16 GB tmpfs at 80%
and refused one redirect mid-leg — see §7). The live 91.6 MB PE analyze was never
signalled, renice'd or touched; it ended on its own during my seat (§6.3).

**Pre-pair receipt (my leg):** `.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt`
verified **5/5, rc=0** — re-checked at 19:11Z, after the `rule 11` commit (§2.1).

## 1. Verdict

**The no-op case is SUSTAINED on the axis C2 actually claims (drift detection), and
the probe is worse than a no-op on the axis it does touch. But the no-op case does
NOT extend to "nothing is needed": the re-keyed census cannot see the pointer family
at all, so C2's fallback is empty too. The honest minimal capability is neither of
the two artifacts on the table.**

Four measured grounds:

1. **The composite C2 names does not exist.** C2's base is "E15's proven
   implementation + R3's F1-F3 fixes + R6's defect fixes". Those are three different
   instruments with three different digests: E15's gate `0c5350b1…`
   (`/tmp/arc2-l3r3-E15/citation-drift-gate.py`), the C3 draft R3 reviewed
   `0a3e7480…` (`R3.md:40`), the census R6 reviewed `cf5d65b6…` (`R6.md:126`).
   R3's F1–F3 are fixes to the *C3 draft*; R6's defects are defects of *E23's census*.
   Neither is a fix to E15's script. Round-4 seat CR5 reached the same conclusion
   independently (`CR5.md:17-19`). There is no artifact to register.
2. **E15's gate fails OPEN in four configurations I measured, and its self-test
   cannot see the dead branch that causes it.** `--rev deadbeef…` on the real repo →
   `clean findings=0 exit=0`. `--root /nonexistent` → `clean findings=0 exit=0`.
   A table with `"entries": []` → `clean findings=0 exit=0`. Any table whose rows
   cite files absent at the graded rev → `clean findings=0 exit=0`. Mechanism is a
   dead branch: `Tree.lines` adds *every* resolution failure to `self.reported`
   (`citation-drift-gate.py:121`) and `check_entry` then suppresses the
   `citation_file_absent` finding for exactly that case (`:163`), so the intended
   finding at `:164` is unreachable. The self-test's `file_absent` case passes
   because it removes the *cited target* (`:294`), exercising the `:210` path, not
   the `:163` path. A tool whose `clean` is emitted when its input is unreadable is
   not a probe in PROTOCOL's sense — PROTOCOL:363-364 reserves that word for a tool
   that *cannot fail*, i.e. a reporter whose output is read as an observation. Here
   the observation would be false.
3. **The probe reddens round-3's own correct repair, and its red count went UP when
   the lane fixed the defect.** Fed the pre-repair table, the probe reports at
   `679af5d` (pre-repair): 9 × `citation_dead` + 1 × `citation_historical_ok`;
   at `158a966` (post-repair): **10 × `citation_dead`, 0 historical**. The two lines
   that flipped are `PROVINCE.md:18` and `SCORECARD.md:59` — precisely the two the
   round-3 C1 commit `fd30b9c` re-anchored into content-anchor form. Both are
   *correct at HEAD* (the live pin is at `:3298`; the census classifies both
   `current-ok`, §2.6). They now read `citation_dead … states no resolvable pointer
   (pattern 'relocated it to :([0-9]+)' absent)` — the probe's `pattern` matches a
   *phrasing*, and the repair changed the phrasing. This is R6's round-3
   "repair makes the count rise" trap (`R6.md:504-525`) landing on the repair
   itself. Round-4 CR5 measured the same two false reds (`CR5.md:57-60`).
4. **The re-keyed census is not the fallback, because it cannot see the family.**
   Measured at HEAD: **15** `config.toml` line-pointer loci across tracked
   non-`.ufo` files, **12 content-dead**. The census's `PTR` regex
   (`c1-census-v9.py:108`) requires a colon plus a `~`/`/` prefix and sees **7 of 15**;
   its `SCOPE` table (`:85-107`) covers only `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`
   and contains **3 of 15** loci. Intersection (regex-visible **and** in-scope) = **2**,
   of which **1** is dead (`SCORECARD.md:291`) — and `:291` falls inside a `DATED`
   range (`:273-326`) so it is classified `historical`, not `stale`. Net: the census
   at HEAD reports `stale=0`, `historical=5`, and its JSON output never mentions
   `1478` or `291` at all, while 12 content-dead `config.toml` pointers sit in the
   tree. Its only failure is `undeclared=2` — the scope-table artifact C3 proposes to
   re-key. **Re-key it and the census returns a PASS-shaped `stale=0` over a tree with
   12 dead pointers**, 10 of them outside its scope files and 2 invisible to its regex.
   The content-anchor discipline is a *writing* convention; it has no detector.

**What the steelman does establish.** The probe's *incremental* coverage over the
already-committed `e16-table.json` is close to nil: of E15's 13 entries, the 8
config-target rows are excluded by C2's own spec, leaving 5 in-repo rows — and 4 of
those 5 (`SCORECARD.md:270` ×2, `:69`, `SKILL.md:336`) are already rows in the
committed table (§2.5). So C2's stated scope adds **one** row (`SCORECARD.md:72`)
over what is already in the repo, plus a *grader* for a table that currently has
none (`pointers.py`/`emit2.py` are untracked — `git ls-files | grep -E
'pointers\.py|emit2\.py'` → empty). That last point is the only live argument for
C2, and it is an argument about *running the table already landed*, not about
drift detection. If the parent wants it, the honest form is "commit the grader for
`e16-table.json`, fix the four fail-open paths, and call it a gate or a probe by its
measured behaviour — not by its aspiration."

**The honest minimal capability** (what neither artifact supplies): a pointer census
with a **content predicate** over the **full tracked tree**, failing closed on
unreadable input. My own family census is ~25 lines of Python, runs in under a
second, and is reproduced verbatim in §3.

## 2. Evidence — exact commands with observed output

### 2.1 Pre-pair receipt 5/5 (my leg, re-checked after `rule 11`)

```console
$ tail -n +2 .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
$ wc -l < .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt     → 6
$ sha256sum .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt
231edd7d83cdfe7787e91d8b6f672f89551a6fe50013df23a5421f5ffadafc62
$ head -1 .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt    → 2026-10-18T19:03:02Z
```

### 2.2 The three instruments C2 conflates (three digests)

```console
$ sha256sum /tmp/arc2-l3r3-E15/citation-drift-gate.py | cut -c1-16
0c5350b1c9a937fe        # E15's gate  — the one C2 calls "E15's proven implementation"
$ sha256sum /tmp/arc2-l3r3-R3/verify-citations.py | cut -c1-16
0a3e74801114e866        # the C3 draft R3's F1-F3 are fixes to (R3.md:40)
$ sha256sum /tmp/arc2-l3r3-R6-probe/c2-census.py | cut -c1-16
cf5d65b6a7037c87        # E23's census, whose defects R6 fixed (R6.md:126)
```

Three artifacts, three digests. R3's F1–F3 are `R3.md:325-339` (hardening *that*
script); R6's fixes are `R6.md:529-566` (defects of *that* census). C2's
"E15 + R3's fixes + R6's fixes" names a composite that has never existed.

### 2.3 Fail-open #1 and #2 — bogus revision, nonexistent root

```console
$ python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --root . \
    --rev deadbeefdeadbeefdeadbeefdeadbeefdeadbeef \
    --table /tmp/arc2-l3r3-E15/pointer-table.json \
    --expected /tmp/arc2-l3r3-E15/expected.json --snapshot-dir /tmp/arc2-l3r3-E15
CITATION_DRIFT_REVISION: deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
rc=0

$ python3 … --root /tmp/arc2-l4r4-CR2/nope --rev HEAD …
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
rc=0
```

Both should be `could-not-evaluate` (exit 2). Both read `clean` (exit 0) — the code
PROTOCOL:365 assigns to "a compared verdict came out clean".

### 2.4 Fail-open #3 and #4 — empty table, and every citing file absent

```console
$ python3 -c "import json; json.dump({'entries':[]}, open('/tmp/arc2-l4r4-CR2/t-empty.json','w'))"
$ python3 … --table /tmp/arc2-l4r4-CR2/t-empty.json …
CITATION_DRIFT_VERDICT: clean findings=0 exit=0

$ python3 -c "import json; json.dump({'entries':[{'id':'citing-absent','kind':'extracted',\
  'file':'NO_SUCH_CITING.md','line':1,'pattern':'x(\\\\d+)','target':'SCORECARD.md',\
  'target_group':1,'must_match':'x'}]}, open('/tmp/arc2-l4r4-CR2/t4.json','w'))"
$ python3 … --table /tmp/arc2-l4r4-CR2/t4.json …
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

Zero rows checked, and every row unchecked, both read `clean`. The loop is
`for entry in table.get("entries", [])` (`citation-drift-gate.py:252`) — a table
using any other top-level key yields zero rows and a `clean` verdict.

### 2.5 The dead branch, and why the self-test cannot see it

```console
$ sed -n '113,122p' /tmp/arc2-l3r3-E15/citation-drift-gate.py
    def lines(self, target):
        if target in self._cache:
            return self._cache[target]
        if target.startswith("@"):
            out = self._snapshot(target[1:])
        else:
            text, err = git_show(self.root, self.rev, target)
            if err:
                self.reported.add(target)          # ← :121 — added unconditionally
            out = (None, err) if err else (text.splitlines(), None)

$ sed -n '159,165p' /tmp/arc2-l3r3-E15/citation-drift-gate.py
    citing, err = tree.lines(target)
    if citing is None:
        # a resolution failure was already reported by Tree (snapshot classes)
        # or is reported here for an absent in-repo file
        if target not in tree.reported:            # ← :163 — false for every git_show failure
            findings.add("citation_file_absent", eid, "%s: %s" % (target, err))
        return
```

`:121` adds every failure; `:163` then suppresses the finding for exactly that
condition; the `findings.add` at `:164` is unreachable for the `git_show` path.

The self-test cannot catch it because its `file_absent` case deletes the **cited
target**, not the **citing file**:

```console
$ grep -n 'os.remove' /tmp/arc2-l3r3-E15/citation-drift-gate.py
294:        os.remove(os.path.join(d, "TARGET.md"))     # ← the cited target
$ python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --selftest --expected /tmp/arc2-l3r3-E15/expected.json | tail -2
SELFTEST_CASE: CLEAN case=file_absent exit=1 expected=1 finding=citation_file_absent
CITATION_DRIFT_SELFTEST: CLEAN cases=10 passed=10 failed=0 exit=0
```

Deleting the *target* reaches the working path at `:210`. I confirmed the contrast
directly — an `extracted` row whose cited target is absent **does** fail closed:

```console
$ # row: SCORECARD.md:69 cites NO_SUCH_TARGET.md (pattern matches the citing line)
CITATION_DRIFT: citation_file_absent entry=target-absent NO_SUCH_TARGET.md (cited by SCORECARD.md:69): absent at HEAD
CITATION_DRIFT_VERDICT: failed findings=1 exit=1
```

So the gate has one working absence path and one dead one, and the self-test covers
only the working one. Round-4 seat CR5 found the same dead branch independently
(`CR5.md:33-38`); my §2.3/§2.4 configurations (bogus rev, absent root, empty table)
are additional to its fixture.

### 2.6 The probe reddens the lane's own correct repair — and its red count rose

```console
$ for R in 679af5d 158a966 1692acbe; do   # 679af5d = pre-repair, 158a966 = post-repair
    python3 … --rev $R … | grep -c "citation_dead"
    python3 … --rev $R … | grep -c "citation_historical_ok"
  done
  679af5d : citation_dead=9   citation_historical_ok=1
  158a966 : citation_dead=10  citation_historical_ok=0
  1692acbe: citation_dead=10  citation_historical_ok=0
```

The two lines that changed composition:

```console
$ # at 679af5d (pre-repair) — the pre-repair form
CITATION_DRIFT: citation_dead entry=province-18-kimi-pin PROVINCE.md:18 cites
  @config-toml-landmarks:3227-3227, which lacks 'args = \[ "-y", "rea-agents@6\.7\.0", "mcp" \]' (holds '')
CITATION_DRIFT: citation_historical_ok entry=scorecard-59-pin-receipted SCORECARD.md:59 cites
  @config-toml-landmarks:2940-2940, … [stamp: 16:57:35Z custody receipt]

$ # at 158a966 / 1692acbe (post-repair) — the re-anchored form
CITATION_DRIFT: citation_dead entry=province-18-kimi-pin PROVINCE.md:18
  states no resolvable pointer (pattern 'relocated it to :([0-9]+)' absent)
CITATION_DRIFT: citation_dead entry=scorecard-59-pin-receipted SCORECARD.md:59
  states no resolvable pointer (pattern 'config\.toml:([0-9]+)' absent)
```

The table rows that produce these (`/tmp/arc2-l3r3-E15/pointer-table.json`):

```json
{"id": "province-18-kimi-pin", "kind": "extracted", "file": "PROVINCE.md", "line": 18,
 "pattern": "relocated it to :([0-9]+)", "target": "@config-toml-landmarks",
 "must_match": "args = \\[ \"-y\", \"rea-agents@6\\.7\\.0\", \"mcp\" \\]"}
{"id": "scorecard-59-pin-receipted", "kind": "extracted", "file": "SCORECARD.md", "line": 59,
 "pattern": "config\\.toml:([0-9]+)", "target": "@config-toml-landmarks",
 "must_match": "rea-agents@6\\.7\\.0", "stamp": "16:57:35Z custody receipt"}
```

Both lines are correct at HEAD. The live pin is at `:3298`:

```console
$ sed -n '18p' PROVINCE.md
… `rea-agents@6.7.0` (`~/.kimi-code/config.toml:3298` at the 17:55:49Z receipt; value
unchanged through 2026-10-18's rewrites — earlier pointers :2940 [16:57:35Z receipt]
and :3227 [17:32Z rewrite] are historical). Cache/catalog
$ sed -n '59p' SCORECARD.md
  (arc2-loop1-round2): Kimi pin is `rea-agents@6.7.0` in `config.toml`'s `[mcp_servers.rea]` per the
$ grep -n 'rea-agents' /home/vgpnk/.kimi-code/config.toml | head -1
3298:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```

And the census — the artifact C2 pairs with the discipline — classifies both as
`current-ok`, i.e. it *verifies* the repair the probe reddens:

```console
$ python3 /tmp/arc2-l3r3-R6-probe/c1-census-v9.py | grep -E '^ *:(18|59) '
      :18 [pin] kimi=6.7.0 -> current-ok (matches live kimi)
      :59 [pin] kimi=6.7.0 -> current-ok (matches live kimi)
```

Note the asymmetry that matters for the parent: the probe's `citation_dead` on
`:59` **also drops its `stamp`**. The stamp branch is honoured only on the
target-comparison path (`citation-drift-gate.py:225,230`), never on the
pattern-absent path (`:192-196`), so a stamp-qualified pointer that is merely
*reworded* is reported as a plain failure. Confirmed directly:

```console
$ # stamped entry whose pattern no longer matches its (reworded) citing line
CITATION_DRIFT: citation_dead entry=stamped-reworded PROVINCE.md:18
  states no resolvable pointer (pattern 'NEVER_MATCHES_([0-9]+)' absent)
CITATION_DRIFT_VERDICT: failed findings=1 exit=1
```

### 2.7 Coverage arithmetic — the census cannot see the family

Family definition: every tracked non-`.ufo` file line containing `config.toml`
together with a line-number token; each cited number tested against the live file
for the `[mcp_servers.rea]` / `rea-agents` anchor.

```console
$ python3 - <<'PY'   # (full script in §3)
…
locus                                                       ->line  alive  PTRvis  inSCOPE
LOG.md:1005                                                   1478  False   False    False
LOG.md:1018                                                   2940  False   False    False
PROVINCE.md:18                                                3298   True    True     True
SCORECARD.md:291                                              1478  False   True     True
SCORECARD.md:698                                              2940  False   False    True
corpus/knowledge/2026-10-13-mcp-registrations.md:11           1285  False   False    False
corpus/knowledge/2026-10-13-mcp-registrations.md:18           1288  False   False    False
corpus/knowledge/2026-10-13-mcp-registrations.md:88           1284  False   False    False
corpus/knowledge/2026-10-13-mcp-registrations.md:93           3296   True    True     False
corpus/knowledge/2026-10-13-mcp-registrations.md:108          3298   True    True     False
corpus/knowledge/2026-10-13-r2-doctor-reverify-r2.md:46       1290  False   False    False
corpus/knowledge/2026-10-13-r3-jq-provenance.md:121             18  False   False    False
corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:43       1284  False   True     False
corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:942      1284  False   True     False
corpus/lessons/2026-10-15-round-1.md:82                       1287  False   True     False

family: 15   content-dead: 12
census-PTR visible: 7   in census SCOPE file: 3
census sees BOTH (ptr-visible AND in scope): 2
dead AND census-visible-in-scope: 1
```

The one dead-and-visible locus is neutralised by scope class:

```console
$ # SCOPE range covering SCORECARD.md:291
  :291 falls in SCOPE SCORECARD.md 273-326 class=DATED
$ python3 /tmp/arc2-l3r3-R6-probe/c1-census-v9.py --json | python3 -c "
  import json,sys; d=json.load(sys.stdin); s=json.dumps(d)
  print('  json mentions 1478:', '1478' in s, '| mentions 291:', '291' in s)
  print('  stale:', len(d.get('stale',[])), 'historical:', len(d.get('historical',[])))"
  json mentions 1478: False | mentions 291: False
  stale: 0 historical: 5
```

The census's whole verdict at HEAD:

```console
$ python3 /tmp/arc2-l3r3-R6-probe/c1-census-v9.py --quiet | tail -5
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)
rc=1
```

`stale=0` is the number that would survive C3's re-key. `undeclared=2` is the only
failure, and it is round-2's own record append against E22's hardcoded scope table
(round-3 R6 measured the same two blocks, `R6.md:456-461`).

Content predicate vs existence predicate — every dead locus resolves to an
existing, non-empty line carrying unrelated content (12/12 by construction of the
table above; the `alive` column is the content test).

### 2.8 The committed table and its missing grader

```console
$ git ls-files | grep -E 'pointers\.py|emit2\.py'          → (empty)
$ git ls-files | grep -E '\.py$'
.ufo/rounds/interactive-r1/verify-recovery.py              # the lane's only tracked script
$ python3 -c "import json; t=json.load(open('e16-table.json')); \
  print('keys:', list(t.keys()), '| rows:', len(t['pointers']))"
keys: ['pin_rev', 'pointers'] | rows: 51
$ grep -n 'json.dump' /tmp/arc2-l3r3-E16/emit2.py
110:json.dump({"pin_rev": "679af5d", "pointers": rows}, open("e16-table.json", "w"), indent=1)
```

`e16-table.json` is committed at HEAD (it arrived in `1692acbe`), pinned to
`679af5d`, and its 51 rows carry only `{id, kind, file, line, must_match}` — the
BASELINE/QUOTED/SYMBOL classes exist in `E16.md` prose, not in the artifact
(round-4 CR5 measured this too, `CR5.md:63-70`). **The grader is untracked.**

Fed to E15's gate, the schema mismatch is decisive in both directions:

```console
$ # as committed — wrong top-level key, so zero rows
$ python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --root . --rev HEAD \
    --table e16-table.json --expected … --snapshot-dir …
CITATION_DRIFT_VERDICT: clean findings=0 exit=0            # ← the "composite" C2 names

$ # same rows re-keyed to "entries" — kind "line"/"symbol" is not a kind E15 knows
$ python3 … --table /tmp/arc2-l4r4-CR2/t6.json …
     50 CITATION_DRIFT: pointer_table_unreadable
CITATION_DRIFT_VERDICT: could-not-evaluate findings=50 exit=2
```

So C2's declared base, run against C2's declared table, reads **clean** — a green
light over 51 unchecked rows. (Round-4 CR5 reports 50 unreadable + silence for the
51st on the re-keyed form, `CR5.md:38-42`; my re-keyed run gives 50 findings and
exit 2, which I report as I measured it.)

Incremental coverage over the committed table:

```console
$ python3 -c "
import json
e15=json.load(open('/tmp/arc2-l3r3-E15/pointer-table.json'))['entries']
e16=json.load(open('e16-table.json'))['pointers']
e16tl={(r['file'],r.get('line')) for r in e16}
for e in e15:
    if not str(e.get('target','')).startswith('@'):
        print('  ',e['id'], f\"{e['file']}:{e.get('line')}\",
              'IN E16' if (e['file'],e.get('line')) in e16tl else 'NOT IN E16')"
   scorecard-270-readme-bullet SCORECARD.md:270 IN E16
   scorecard-270-readme-head-claim SCORECARD.md:270 IN E16
   scorecard-69-readme-177 SCORECARD.md:69 IN E16
   scorecard-72-readme-nitrow SCORECARD.md:72 NOT IN E16
   skill-registry-row SKILL.md:336 IN E16
```

Under C2's own scope ("NO config.toml line numbers"), the probe adds **one row**.

### 2.9 Registry and invocation reality

```console
$ grep -n "^| " SKILL.md | sed -n '1,2p;31,33p'
44:| Target | First move | Status |          # (capability table, not the registry)
334:| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
336:| interactive-r1-recovery | gate / kaidoku | `python3 .ufo/rounds/interactive-r1/verify-recovery.py`; 0 clean, 1 failed, 2 could-not-evaluate | …
$ ls -la .git/hooks/ | grep -v '\.sample'      → (nothing but . and ..)
$ ls -d .github .gitlab-ci.yml Makefile justfile 2>&1
ls: cannot access '.github': No such file or directory  … (all four absent)
$ grep -rn 'verify-recovery' --include='*.md' --include='*.sh' --include='*.py' . \
    | grep -v '^./.ufo/waves' | wc -l        → 9   (all documentation, no caller)
$ # breakdown: corpus/lessons/2026-10-15-round-1-admission-correction.md ×2,
$ #            corpus/lessons/2026-10-15-round-1-recovery.md ×1, LOG.md ×1,
$ #            SKILL.md ×1 (the registry row), .ufo/reports/round-1/kaidoku.md ×4
```

One registry row today, zero probe rows, and **nothing in the repo invokes any
gate**: no hook, no CI, no Makefile. A registry row is a pointer a human or a seat
reads and then runs by hand. That is the strongest structural part of the steelman:
the row's cost is not the issue, but neither is its automatic effect.

## 3. VERBATIM — text the parent may land (as-is if used)

### 3a — the disposition

```text
CR2 disposition on C2 (probe-vs-gate), arc2-loop1-round4, HEAD 158a966→1692acbe,
measured 2026-10-18 19:04Z-19:14Z. Pre-pair 5/5 rc=0 (self-hash 231edd7d…).

DO NOT register C2's probe as scoped. Three measured grounds:
 (1) The composite C2 names does not exist. "E15's implementation + R3's F1-F3 +
     R6's fixes" spans three instruments with three digests: E15's gate
     0c5350b1…, the C3 draft R3 reviewed 0a3e7480…, the census R6 reviewed
     cf5d65b6…. R3's fixes harden the second; R6's fix the third; neither
     touches the first.
 (2) E15's gate fails OPEN in four measured configurations, and its selftest
     cannot see the dead branch. --rev deadbeef… → clean findings=0 exit=0;
     --root /nonexistent → clean findings=0 exit=0; {"entries":[]} → clean
     findings=0 exit=0; every row citing a file absent at the graded rev →
     clean findings=0 exit=0. Mechanism: Tree.lines adds every resolution
     failure to self.reported (citation-drift-gate.py:121) and check_entry
     suppresses citation_file_absent for exactly that case (:163), so the
     finding at :164 is unreachable on the git_show path. The selftest's
     file_absent case removes the CITED TARGET (:294), reaching the working
     path at :210 — it never exercises the dead one. A tool that emits
     `clean` when its input is unreadable is not a probe in PROTOCOL's sense
     (PROTOCOL.md:363-364): its output is read as an observation, and the
     observation is false.
 (3) The probe reddens round-3's own correct repair, and its red count ROSE
     when the lane fixed the defect: 679af5d → 9 citation_dead + 1
     citation_historical_ok; 158a966 → 10 citation_dead + 0. The two flipped
     lines are PROVINCE.md:18 and SCORECARD.md:59 — exactly the two the C1
     commit fd30b9c re-anchored into content-anchor form, both correct at
     HEAD (live pin :3298; the census classifies both `current-ok`). The
     rows match a PHRASING ("relocated it to :([0-9]+)"), so the repair that
     removed the phrasing reads as death. A stamp-qualified pointer that is
     merely reworded also loses its stamp, because the stamp branch is
     honoured only on the target-comparison path (:225,:230), never on the
     pattern-absent path (:192-196).

DO NOT treat the re-keyed census as the fallback either — it cannot see the
family. At HEAD: 15 config.toml line-pointer loci across tracked non-.ufo
files, 12 content-dead. The census's PTR regex (c1-census-v9.py:108) sees 7
of 15 (colon + ~// prefix required); its SCOPE table (:85-107) covers only
PROVINCE.md/SKILL.md/SCORECARD.md and contains 3 of 15. Intersection = 2, of
which 1 is dead (SCORECARD.md:291) — and :291 sits inside a DATED range
(:273-326), so it is classified `historical`, not `stale`. Net: the census
reports stale=0, historical=5, and its JSON never mentions 1478 or 291,
while 12 content-dead config.toml pointers sit in the tree. Its only failure
is undeclared=2 — the scope-table artifact C3 proposes to re-key. Re-key it
and the census returns a PASS-shaped stale=0 over that tree. The
content-anchor discipline is a writing convention with no detector.

WHAT THE STEELMAN DOES ESTABLISH (the live argument for C2, stated honestly):
under C2's own scope ("no config.toml line numbers"), E15's 13 entries yield 5
in-repo rows, and 4 of those are already rows in the committed e16-table.json
(SCORECARD.md:270 ×2, :69, SKILL.md:336). C2 adds ONE row (SCORECARD.md:72)
plus a grader for a table that currently has none — pointers.py/emit2.py are
untracked (git ls-files | grep -E 'pointers\.py|emit2\.py' → empty), so
e16-table.json (51 rows, committed at 1692acbe, pin_rev 679af5d) is a
committed table nothing runs. Fed to E15's gate as committed it returns
`clean findings=0 exit=0` (its top-level key is `pointers`; the gate reads
`entries` at :252). If the parent wants C2, the honest form is: commit the
grader for e16-table.json, fix the four fail-open paths, and name the row by
the artifact's MEASURED behaviour — not by its aspiration.

THE HONEST MINIMAL CAPABILITY (neither artifact supplies it): a pointer census
with a CONTENT predicate over the FULL tracked tree, failing closed on
unreadable input. Every dead locus resolves to an existing, non-empty line
with unrelated content (12/12), so any existence-only predicate is clean on
the whole family. The census in §3b is ~25 lines, runs in under a second, and
covers all 15 loci — including the 7 in corpus/knowledge/ that neither the
gate table nor the census scope contains.
```

### 3b — the family census, verbatim (the artifact I actually measured)

```python
#!/usr/bin/env python3
"""Pointer-family census over every tracked file: for each `config.toml` line
pointer, does the cited line carry the anchor the citation claims?

Content predicate, not existence: R6.md:344-364 measured 16/16 dead pointers
resolving to existing non-empty lines. Fails closed when the live file is
unreadable. Read-only; writes nothing.
"""
import os, re, subprocess, sys

CFG = os.path.expanduser("~/.kimi-code/config.toml")
# any config.toml pointer form: :N, `lines N-M`, `line N`, (lines N-M)
ANY = re.compile(r"config\.toml[^A-Za-z0-9\n]{0,4}(?:`?\s*(?:lines?|line)\s*)?:?\s*(\d{2,7})")
ANCHORS = ("mcp_servers", "rea-agents", "startup_timeout_sec", "GHIDRA_INSTALL_DIR")

def live():
    try:
        return open(CFG, encoding="utf-8", errors="replace").read().splitlines()
    except OSError as exc:
        print("could-not-evaluate: live config unreadable (%s)" % exc)
        sys.exit(2)

def main():
    L = live()
    files = [f for f in subprocess.check_output(["git", "ls-files"], text=True).split()
             if not f.startswith(".ufo")]
    dead, total = [], 0
    for f in files:
        try:
            lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
        except OSError:
            continue
        for i, l in enumerate(lines, 1):
            if "config.toml" not in l:
                continue
            for m in ANY.finditer(l):
                n = int(m.group(1))
                if n > 100000:            # sha-prefix artifact, not a pointer
                    continue
                total += 1
                txt = L[n - 1] if 1 <= n <= len(L) else ""
                if not any(a in txt for a in ANCHORS):
                    dead.append((f, i, n, txt.strip()[:60]))
    for f, i, n, txt in dead:
        print("DEAD  %s:%d -> :%d  %r" % (f, i, n, txt))
    print("TOTAL %d  content-dead %d  content-alive %d" % (total, len(dead), total - len(dead)))
    sys.exit(1 if dead else 0)

if __name__ == "__main__":
    main()
```

At HEAD `1692acbe` this prints `TOTAL 15  content-dead 12  content-alive 3` and
exits 1.

## 4. Conclusions, labeled

**OBSERVATIONS** (ran/read this session):

- Pre-pair verified 5/5 rc=0 at 19:04Z and again at 19:11Z, self-hash
  `231edd7d…`, stamp `2026-10-18T19:03:02Z`. (§2.1)
- The three round-3 instruments carry three distinct digests; the composite C2
  names is not one artifact. (§2.2)
- E15's gate returns `clean findings=0 exit=0` for a bogus revision, a nonexistent
  root, an empty `entries` list, and a table of rows citing absent files. (§2.3, §2.4)
- The `self.reported`/`check_entry` dead branch at `:121`/`:163`; the selftest's
  `file_absent` case removes the cited target (`:294`) and passes; the cited-target
  absence path (`:210`) fails closed correctly. (§2.5)
- The probe's finding composition moved 9 dead + 1 historical → 10 dead + 0 between
  `679af5d` and `158a966`; the two flipped lines are `PROVINCE.md:18` and
  `SCORECARD.md:59`, both correct at HEAD, both classified `current-ok` by the
  census. A stamped entry whose pattern stops matching loses its stamp. (§2.6)
- Family census: 15 `config.toml` line-pointer loci, 12 content-dead; census PTR
  regex sees 7/15, census SCOPE contains 3/15, intersection 2, dead-and-in-scope 1
  (`SCORECARD.md:291`, inside a DATED range). Census at HEAD: `stale=0`,
  `historical=5`, JSON never mentions `1478` or `291`. (§2.7)
- `e16-table.json` is committed at HEAD with 51 rows pinned to `679af5d`;
  `pointers.py`/`emit2.py` are untracked; the gate fed the committed table returns
  `clean findings=0 exit=0`; re-keyed to `entries` it returns 50
  `pointer_table_unreadable` and exit 2. Under C2's scope the probe adds one row
  over the committed table. (§2.8)
- One registry row, zero probe rows; no hook, no CI, no Makefile, no in-repo
  caller of any gate. (§2.9)

**INFERENCES**:

1. C2's probe would not be a no-op — it would be a net negative on the drift axis:
   it adds ~1 row of coverage while reddening two correct citations and emitting a
   fail-open `clean` on unreadable input. Registering it as `kind=probe` does not
   neutralise that, because PROTOCOL's probe category is for a tool whose output is
   a true observation, and this output is false in both directions.
2. The steelman holds for the *detection* value but not for "nothing is needed":
   the census is a statement census over three files, and the discipline is a
   writing convention. Neither detects a dead pointer in `corpus/knowledge/`.
3. The cheapest non-no-op capability is a content-predicate census over the whole
   tracked tree (§3b) — which is neither artifact on the table and needs no new
   instrument category.
4. The deeper issue for the lane is that the probe's `pattern` field binds a
   *phrasing*. Any wording change — including the lane's own repairs — reads as
   death. A drift detector whose activation condition is drafter wording is the
   failure class R6 named in round 3 (`R6.md:42-49`), and C2 has not inherited
   the fix.

**UNKNOWNS**:

- Whether the parent lands the probe at all, and under which row class. If it does,
  the four fail-open configurations in §2.3/§2.4 must be closed first, or the row's
  verdict map is a claim the artifact does not meet.
- Whether `SCORECARD.md:291`'s `:1478` pointer is an assertion or a dated receipt
  record. It sits in a `DATED` range and its clause reads as a receipted record; I
  did not adjudicate, and the answer decides whether it is a defect or history.
- Whether the parent intends the census re-key (C3) to be the standing detector.
  If yes, §2.7 is the objection: it cannot see 10 of the 12 dead loci.
- Whether E16's BASELINE/QUOTED/SYMBOL classes are meant to be encoded in the
  table artifact or stay as prose in `E16.md`. As committed they are prose only.
- The operator's rewrite cadence for `~/.kimi-code/config.toml`. It was stable at
  `bd5a78d1…`, 3322 lines, pin at `:3298`, across every check I ran (19:04Z–19:14Z);
  round-3's own record documents three rewrites in a day.

## 5. Pointer-resolution base for this report

- `citation-drift-gate.py:NNN` → line NNN of the **extracted** E15 gate at
  `/tmp/arc2-l3r3-E15/citation-drift-gate.py`, sha256
  `0c5350b1c9a937fe9b3fd0942705edf77ecbe8c573f0965a81171e6b0eb79d8f`, 415 lines
  (matches `E15.md:232`). Same basis as round-3 R6's convention.
- `c1-census-v9.py:NNN` → line NNN of the extracted E22 census at
  `/tmp/arc2-l3r3-R6-probe/c1-census-v9.py`, sha256 `213fe679…` per round-3 R6
  (`R6.md:442-443`); 429 lines.
- `emit2.py:110` → line 110 of `/tmp/arc2-l3r3-E16/emit2.py`.
- `e16-table.json` → the **committed** file at this repo's root, HEAD `1692acbe`.
- `PROTOCOL.md:NNN` → `/home/vgpnk/.kimi-code/skills/shokunin/protocol/PROTOCOL.md`;
  byte-identical to the fleet-root copy (both sha256
  `b1d4f4c0940522981a6ace84d8528acb0bad470ebaa69faeeb0dbd017b330c20`).
- `config.toml` → the live `~/.kimi-code/config.toml`, read as line content and
  hashes only; no secret values emitted.
- All other paths are repo-relative at HEAD.

## 6. Infrastructure observations (read-only, not my scope)

### 6.1 The PE leg ended on its own

```console
$ cat /var/tmp/arc2-l4r4-pe/exit.txt
exit=1 wall_utc=2026-10-18T19:07:45Z
$ systemctl --user list-units --type=scope --all | grep -iE 'arc2|run-p'
● run-p4175743-i29293759.scope   loaded failed failed   arc2-pe-wall
$ ps -eo pid,etime,rss,comm,args --sort=-rss | grep -iE 'java|ghidra|rea-agents' | grep -v grep
(empty)
```

The contained analyze exited **1** at 19:07:45Z and left a `failed` transient scope
unit. I did not signal, renice or touch it at any point; I only read `/var/tmp`
and the unit list. The residue sweep the parent planned will need
`systemctl --user reset-failed run-p4175743-i29293759.scope` (round-3 CR2 §3.10
documented the same class).

### 6.2 /tmp is at its ceiling

```console
$ df -h /tmp | tail -1
tmpfs            16G   13G  3.1G  80% /tmp
```

One of my `sed` redirects failed with `sed: couldn't flush stdout: Disk quota
exceeded`. Round-4 seats CR5 and E3 report the same (§7). Scratch-heavy seats
should use `/var/tmp`.

### 6.3 HEAD moved mid-seat

`158a966` → `1692acbe` ("rule 11") at 19:09Z, artifact-only: it added
`.ufo/waves/arc2-loop1-round4/{E23,E4}.md`, the pre-pair receipt, and
`e16-table.json`. Every load-bearing measurement in this report was re-run at
`1692acbe` with identical results.

## 7. Scope compliance and residue

- **Only repo write: this report.** `git status --porcelain` at leg start →
  `?? .ufo/waves/arc2-loop1-round4/`; at leg end the new entries are other seats'
  report files only. No git mutation, no config edit, no install, no network
  fetch, no `npx` resolution. The live PE leg was never signalled.
- Scratch: `/tmp/arc2-l4r4-CR2/` (48 MB — the `cl` clone of this repo plus seven
  one-row tables, the tamper dir, and pre/post finding captures). All fixture work
  used a throwaway clone or a `git archive` extraction; the real repo was never
  staged or edited. No processes of mine remain.
- Custody paths were read as line content, line counts and hashes only; no secret
  values read or emitted. The one config-derived artifact in this report is the
  anchor test in §3b, which reads lines and prints at most 60 characters of a
  cited line only when the citation is dead — all of which are model-table lines,
  not the `[mcp_servers.rea]` stanza.
- No battery leg was mine; no REA/MCP session; no session to close.
- Every `path:line` pointer in this report was resolved by a command shown above
  this session. Cross-seat pointers into `.ufo/waves/arc2-loop1-round{2,3,4}/` were
  read this session; treat them as movable.
