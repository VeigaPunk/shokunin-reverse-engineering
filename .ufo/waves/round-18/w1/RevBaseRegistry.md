# RevBaseRegistry — is R17-REGISTRY open at 9011581?

**Verdict: `open` at `9011581d84527ba34c675f9cf912e54d2e72d470` (B).** Both limbs of
`corpus/lessons/round-17-verifier-spotcheck.md:144-146` reproduce on B's `SKILL.md`; nothing at B
closes them. One enumeration defect: `pins` states its only write in the *entry* cell, so "4/10" is
4 on a fifth-cell reading and 3 on a whole-row reading (calibration, not a refutation). The cited
authority resolves (`PROTOCOL.md:377-379`, `:401-403`), so this is not a dangling citation.

## Inspected identity (observation)

```console
$ L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin; B=9011581d84527ba34c675f9cf912e54d2e72d470
$ git -C "$L" rev-parse HEAD refs/heads/main
9011581d84527ba34c675f9cf912e54d2e72d470
9011581d84527ba34c675f9cf912e54d2e72d470
$ git -C "$L" cat-file -t $B
commit
$ git -C "$L" hash-object SKILL.md; git -C "$L" rev-parse $B:SKILL.md
cfa3b54c87d267fb4fcf14f4036804d1a8b6a0e8
cfa3b54c87d267fb4fcf14f4036804d1a8b6a0e8
$ git -C "$L" diff --stat $B -- SKILL.md corpus/lessons/round-17-verifier-spotcheck.md
$ git -C "$L" status --porcelain --untracked-files=no
 M .ufo/waves/round-17/tools/compare.py
$ git -C "$L" ls-tree --name-only $B PROTOCOL.md
exit=0 (each command; the diff printed nothing and the ls-tree listed nothing)
```

The worktree `SKILL.md` **is** B's blob (`cfa3b54…`) and the lesson file is unchanged from B, so
every line number below is baseline and not a later drift. The one tracked modification is a
working-tree edit to `compare.py` consistent with the contract's C3 additive fix; it is unrelated
and was not touched. `PROTOCOL.md` is **not** in the lane tree; the authority read is the fleet file
`/home/vgpnk/Projects/shokunin/PROTOCOL.md`, whose own repo reported it unmodified (empty
`git status --porcelain -- PROTOCOL.md`).

`exit=0` below is the shell's last-command status; in pipelines that is the consumer (`awk`, `cut`,
`grep`), not necessarily the git producer.

## The claim and its authority

- `corpus/lessons/round-17-verifier-spotcheck.md:144` — `5. **R17-REGISTRY.**`
- `:145` — "4/10 new SKILL registry rows (go-route-compare, receipt-validate, pins,
  go-buildinfo-probe; `SKILL.md:540-542,545`) give no pinned-value path or write scope (PROTOCOL
  §Gate standard row fields)."
- `:146` — "The citation-drift row (`:448`) is registered `probe` while its registered `--strict`
  entry can exit 1, which makes it a gate."
- `/home/vgpnk/Projects/shokunin/PROTOCOL.md:377-379` — "A **gate** is a committed, re-runnable
  verdict script … it reads surfaces, compares them against expected values persisted in its own
  repo, and returns a verdict. A tool that cannot fail is a **probe**, and is registered as one."
- `PROTOCOL.md:401-403` — "Row fields: name, `gate|probe`, entry command, verdict map (code →
  class), self-test command and spelling, pinned-value path, write scope, owner."
- The lane table header carries those fields in five merged columns: `SKILL.md:445` — `| Name |
  Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |`; the 5th
  is the pinned-value/write-scope field.

The anchors `SKILL.md:540-542,545` and `:448` land on exactly the named rows:

```console
$ git -C "$L" grep -n -E '^\| (go-route-compare|receipt-validate|pins|go-buildinfo-probe|citation-drift) ' $B -- SKILL.md | cut -c1-120
B:SKILL.md:448:| citation-drift | probe / kaidoku | `python3 -I …
B:SKILL.md:540:| go-route-compare | probe / kaidoku | `python3 -I -B …
B:SKILL.md:541:| receipt-validate | gate / kaidoku | `python3 -I -B …
B:SKILL.md:542:| pins | tool / kaidoku | `python3 -I -B …
B:SKILL.md:545:| go-buildinfo-probe | probe / kaidoku | `python3 -I -B …
exit=0
```

## Limb 1 — the four rows (observation)

Fifth cell (field 5), verbatim at B:

| line | row | kind | field 5 | write-scope token in row | pinned-path token in field 5 |
|---|---|---|---|---|---|
| 540 | go-route-compare | probe | "`snapshot_label` is marked non-discriminating; route fields and a hand prediction's `extra_expectations` are compared when present" (132 B) | none anywhere | none |
| 541 | receipt-validate | gate | "Consistency of recorded digests, pins and log binding now; not authenticity against a forger who rewrites and rehashes, and not during-run integrity" (150 B) | none (only `rewrites`, not a scope) | none |
| 542 | pins | tool | "Identical bytes at two instants only, never continuity" (56 B) | **entry cell**: "`snapshot --out <FILE> <PATH>` writes one map" | none |
| 545 | go-buildinfo-probe | probe | "Stdlib reader modelled on go1.25.0 `debug/buildinfo` … cross-check with `go version -m`" (154 B) | none anywhere | none |

Contrast with the rows the lesson does **not** list: `:537` go-carrier-run has both ("… frozen
prediction and all 143 installed Go data files pinned pre … writes only `runs/<LABEL>/`"); `:538`
and `:539` state "Read-only; stdout only". That contrast also rules out the only alternative
reading of the rule — that the fifth field binds gates only: `:538`/`:539` are `probe` rows and the
lane still gives them a write scope, so the lane applies the field to probes. A whole-file token
sweep confirms 540/541/542/545 are the only r17 rows with no `read-only|stdout only|writes only`
text:

```console
$ git -C "$L" grep -n -i -E 'read-only|stdout only|writes only' $B -- SKILL.md | cut -c1-90
B:SKILL.md:355:- **Read-only, always …
B:SKILL.md:447:| interactive-r1-recovery | gate / kaidoku | …
B:SKILL.md:448:| citation-drift | probe / kaidoku | …
B:SKILL.md:449:| custody-pair | tool / kaidoku | …
B:SKILL.md:475:Go recovery diagnosis, retain the read-only inventory …
B:SKILL.md:487:| go-snapshot-inventory | probe / kaidoku | …
B:SKILL.md:506:| go-selection-preview | probe / kaidoku | …
B:SKILL.md:507:| round16-structural-controls | probe / kaidoku | …
B:SKILL.md:537:| go-carrier-run | probe / kaidoku | …
B:SKILL.md:538:| go-log-extract | probe / kaidoku | …
B:SKILL.md:539:| go-route-predict | probe / kaidoku | …
exit=0
```

There is no section-level prose that supplies the missing scope: the r17 section's prose between
the signal table and the registry table (`SKILL.md:530-533`) is about `TMPDIR`/log binding, and
`:535`'s header is the only other text before the rows.

**"10 new" is exact**: all ten r17 registry names are absent at the r16 tip `27b8fc1`:

```console
$ for n in go-carrier-run go-log-extract go-route-predict go-route-compare receipt-validate pins \
    temporal-sweep invocation-audit go-buildinfo-probe round17-structural-controls; do
    echo "$n at r16: $(git -C "$L" grep -c "| $n |" 27b8fc1 -- SKILL.md 2>/dev/null || echo 0)"; done
go-carrier-run at r16: 0
go-log-extract at r16: 0
go-route-predict at r16: 0
go-route-compare at r16: 0
receipt-validate at r16: 0
pins at r16: 0
temporal-sweep at r16: 0
invocation-audit at r16: 0
go-buildinfo-probe at r16: 0
round17-structural-controls at r16: 0
exit=0
```

**"4/10" holds only on the fifth-cell reading.** `pins` (`:542`) names its single write target in
the entry cell ("`snapshot --out <FILE> <PATH>` writes one map"); a whole-row reader can say pins
*does* give a write scope, which makes the count 3/10. Since the lesson cites PROTOCOL's *field*, the fifth cell is the
defensible unit and 4/10 survives — but the wording "give no … write scope" is literally false for
pins' row content. `[INFERENCE]` This over-inclusion is the item's only inaccuracy; it does not
close the defect because 540/541/545 lack both fields anywhere and 542 still lacks a pinned-value
path in field 5.

Also `[INFERENCE]`: read per-field, PROTOCOL:402 requires *both* a pinned-value path and a write
scope. Only `:537` carries an explicit value-bearing pinned path among the ten new rows (a `.py`
import such as `:539`'s `selection.py` is code, not a persisted expected value), so a per-field
reading makes **9/10** rows nonconformant, not 4/10. The lesson's 4 is the "lacks both" count — a
lower bound on the schema gap, not a complete census.

```console
$ git -C "$L" show $B:SKILL.md | awk -F'|' 'NR>=537&&NR<=546{gsub(/^ +| +$/,"",$2); c=$6;
    hit=(c ~ /\.json|predictions\/|expected|pinned|SHA256SUMS|carriers\.tsv/);
    printf "%s value-path=%s\n", $2, (hit?"YES":"no")}'
go-carrier-run value-path=YES
go-log-extract value-path=no
go-route-predict value-path=no
go-route-compare value-path=no
receipt-validate value-path=no
pins value-path=no
temporal-sweep value-path=no
invocation-audit value-path=no
go-buildinfo-probe value-path=no
round17-structural-controls value-path=no
exit=0
```

## Limb 2 — citation-drift kind vs its registered entry (observation)

- `SKILL.md:448` field 2 = `probe / kaidoku`; its entry, same line, registers
  `… citation-drift-probe.py --root … --rev <REV> --table …/pointer-table.json --expected
  …/expected.json --strict`, and its entry/verdict-map cell (cell 3) says "`--strict` restores the
  gate map 0 clean / 1 failed / 2 could-not-evaluate". (The row also already states a write scope:
  "normal entry
  read-only over the tree it grades; selftest writes only isolated temp fixture repos" — so limb 2
  is purely the kind label.)
- The script at B confirms the exit-1 capability: `CLEAN, FAILED, CNE = 0, 1, 2` (`.ufo/gates/
  citation-drift/citation-drift-probe.py:64`); `Findings.verdict(strict=False)` returns CNE for the
  tamper/unpinned classes and `CLEAN` when `not strict` (`:80-87`), then `return FAILED` for the
  strict gate (`:93`); `report()` returns that verdict (`:329-334`); `main()` returns `report(...)`
  (`:494-495`) and `sys.exit(main())` (`:499`); `--strict` is the flag whose help text is "gate
  semantics 0/1/2" (`:482-484`).
- Therefore the registered argv can exit 1, so under PROTOCOL:377-379 the registered invocation is
  a gate and field 2's `probe` is the wrong label. Observed in source; not executed (see gaps).

## Minimal objective test (Git objects only; deterministic)

```text
closed(REV) :=
  S = git show REV:SKILL.md ; rows = the 5-column rows parsed with trimmed cells
  1) for n in {go-route-compare, receipt-validate, pins, go-buildinfo-probe}:
       c = row(n).cell5
       write_scope(c) := /(?i)\bread[- ]only\b/ over a named surface
                       | /writes only <target>/ where <target> is "none" or a LANE path
                       | /^Write scope: \S/
       pinned(c)     := exists token p in c with `git cat-file -e REV:p` exit 0
                       | /(?i)pinned values?: none\b/ with a one-line reason
       require write_scope(c) AND pinned(c)
  2) d = row(citation-drift)
       require d.cell2's first token in {gate, probe}
       require (d.cell2's first token == gate)
             == (the exact argv in d.cell3 can exit 1 under the script at REV:
                 for B, "--strict" is present and verdict(strict=True) returns FAILED=1)
```

At B this is red on every clause: 0/4 rows pass (1), and (2) has kind `probe` while capability is
`gate`. It is objective (two parsed cells, one source-file predicate), revision-scoped, and admits
both PROTOCOL-valid repairs of limb 2: relabel `gate` and keep `--strict`, **or** drop `--strict`
from the registered entry (registered form then cannot fail → `probe` is honest). It also rejects a
token-only fix, because a path must resolve at REV or the row must say "pinned values: none".

## Comparison with `contract.md:41-43` (the R17-REGISTRY routed-defects definition)

> "in `SKILL.md`, the table rows whose first cell is `go-route-compare`, `receipt-validate`, `pins`,
> `go-buildinfo-probe` each have a 5th cell containing `Write scope:`; the `citation-drift` row's
> 2nd cell starts with `gate`."

**Baseline red is correct.** At B, none of the four fifth cells contains `Write scope:` (132/150/56/
154 bytes; none names a write target or a pinned path) and citation-drift's 2nd cell is
`probe / kaidoku`. So the claimed `open` at B is reproduced by this definition; the contract does
not manufacture the baseline.

**Too weak.** (a) It drops the pinned-value path that PROTOCOL:402 lists and the lesson names, so
`Write scope: none` alone would clear a row that still has no pinned-value statement. (b) It tests
substring containment, so `Write scope:` with an empty value, or inside a negation, passes. (c) It
never resolves a path at REV. (d) It leaves `pins`' field-2 kind `tool` untouched, though
PROTOCOL:402's vocabulary is `gate|probe` and the lesson's own "can exit 1 ⇒ gate" rule is not
applied to `pins` (its `compare` exits 1 on differ — a classification question the lesson leaves
open; `tool` is outside the schema either way). (e) It accepts any string starting `gate` (e.g.
`gatekeeper`) and does not require the 0/1/2 map to remain declared after relabeling.

**Too strong.** (a) The literal token is not PROTOCOL's requirement; the lane's own accepted style
is `Read-only; stdout only` (`:538`, `:539`) and `writes only \`runs/<LABEL>/\`` (`:537`). A
semantically complete fix written in that house style would still be reported open — a false red.
(b) For citation-drift it hard-codes one of the two valid remedies (relabel `gate`); the
capability-matched alternative (register the probe argv) closes the defect but not the check. The
lesson's wording "which makes it a gate" does choose the relabel, so this is a remedy choice rather
than a misread — but as a *closure* test it grades spelling, not the defect.

**Verdict on the definition:** adequate to reproduce the baseline (red), inadequate as a closure
test. Either adopt the semantic test above, or widen the row check to "fifth cell states a write
target (any house phrasing) **and** a resolving pinned path or explicit none" and make the
citation check capability-matched.

## Residual risk and verification gaps

- I did not execute `citation-drift-probe.py`; the exit-1 capability is read from the baseline
  source anchors above. The registered argv's actual exit at B is unmeasured `[GAP]`. Executing it
  would be read-only (`--root LANE --rev B`), but it was outside my assignment and the lane's
  evidence standard requires a recorded run, not a seat anecdote.
- `[GAP]` The `pins` whole-row reading is a judgment call; I report both counts rather than choosing
  silently.
- `[INFERENCE]` The 9/10 per-field count assumes PROTOCOL:402's pinned-value path is required even
  when a probe pins nothing; an explicit "none" statement would satisfy my test but is absent.
- Line anchors are against B's immutable blob; the worktree `SKILL.md` matched it at inspection
  time (`cfa3b54…`). If a sibling edits `SKILL.md` later, anchors remain valid only against B.
- No tool was installed or updated; no gate, REA verb, Ghidra run or carrier execution was used.
