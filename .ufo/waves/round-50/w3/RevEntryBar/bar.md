# Entry acceptance bar — `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` (R50-C1 landing)

Pre-written acceptance rubric for the falsify wave (seat `RevEntryBar`, round 50 attempt 2, wave 3).
Applied to the LANDED entry at the landing REV. Written 2026-10-29T20:37Z against the frozen bytes:
`tools/round-50/c1-counter.py` at HEAD 6f4aba63 sha256 `9820811bf29f…9bd813`, verified byte-unchanged
from the C1 freeze `435d41fd4ad9211d1579fc447936fb33d2b74467` (receipt R1 in `RevEntryBar.md`).

**Verdict rule.** Every item met → exit 0 (admit). Any item violated → exit 1 (reject; cite the item).
An item whose evidence does not exist at REV (e.g. the L1's re-open receipts not yet written) is
**unevaluable (2) for that item, never clean** — per QUALITY 16/17 exit-2 discipline. The frozen
counter is the rule where this bar restates a binding; the counter's code lines are cited.

**The pinned identity (checked first, gates everything else).** The frozen counter pins
`ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'`, `STEM = '2026-10-28-r50-avm-le-squashfs-core'`
(`c1-counter.py:377-378`). The name `2026-10-29-r50-le-avm-hsqs-core` was the attempt-2 claims file's
first draft, corrected at `6f4aba63` ("the counter, not this file, is the rule"). An entry under any
other stem fails item 1.

## A. Identity and placement

1. **Entry exists at the counter-pinned path, and no entry exists under the corrected-away stem.**
   Enforces: predicate documentation binding "the entry exists at REV" (`plans/round-50-claims.md`
   R50-C1; `c1-counter.py:2457-2458` `entry_present`); QUALITY 4 (artifact named by path + identity).
   Command:
   `git cat-file -e <REV>:corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md && echo PRESENT; git cat-file -e <REV>:corpus/knowledge/2026-10-29-r50-le-avm-hsqs-core.md || echo WRONG-STEM-ABSENT`
   (expect `PRESENT` then `WRONG-STEM-ABSENT`; also `git show <REV>:tools/round-50/c1-counter.py | grep -n "^ENTRY = \|^STEM = "` prints the two constants above).

## B. Provenance block first

2. **The provenance block leads the entry: `source:` lines cite S243, S244, S245, S249** (Freetz
   AVM_LE/AVM_BE patch, AVM download index, unblob 26.6.4 LE handler, AVM licence — the four ids the
   claim's frontier step names, `plans/round-50-attempt2-claims.md` §"Frontier step"). The counter
   accepts any in-window rows; this item enforces the claim's *named* four. Each `source:` line
   carries URL, located quote, re-read date, byte size and sha256 (QUALITY 1, 29).
   Command:
   `grep -n '^source: S243 \|^source: S244 \|^source: S245 \|^source: S249 ' <entry>` (exactly 4 hits)
   and `awk '/^source:/{n++; if ($0 !~ /sha256/) print "NO-SHA " NR} END{print "source-lines="n}' <entry>`
   (no NO-SHA lines).

3. **Quote fidelity: every located quote is ≤25 words, contiguous, with its containing section/line
   locator** (QUALITY 42; 16/17; locator rule 91 — the heading that structurally contains the quote).
   Command: re-run the frozen `python3 -I -B tools/round-50/quote-check.py` over the entry's quotes
   as the w1 seats did (receipts `.ufo/waves/round-50/w1/C1SrcFreetz/tools/round-50/quote-check.out.txt`
   pattern) and require `missing=0`; per-quote spot check `grep -F '<quote words>' <committed snapshot>`
   finds one contiguous run.

4. **Attempt-2 re-open receipts exist for the cited source bytes, sha256-equal to the entry's cites.**
   Enforces QUALITY 18/73 (receipt states argv, exit, stdout, UTC). Expected paths:
   `.ufo/waves/round-50/l1/srcs-attempt2/` (S243/S245), the S244 index re-open, the S249 licence
   re-open (w3 `SrcReopen*` seats' outputs), with copies under `corpus/evidence/round-50/c1/index/`.
   Command:
   `sha256sum .ufo/waves/round-50/l1/srcs-attempt2/* corpus/evidence/round-50/c1/index/* 2>/dev/null`
   — every sha256 the entry cites on its `source:` lines appears in this output. Absent files make
   this item 2, never clean.

## C. Bidirectional registry linkage

5. **Each cited S-id resolves to a `corpus/SOURCES.md` row, 11 cells, `opened ∈ {2026-10-28,
   2026-10-29}`, `used-by` naming the entry path or stem** — and the reverse: those rows' `used-by`
   cells point back at this entry. Enforces QUALITY 29; counter logic `c1-counter.py:2462-2477`
   (selftest reds: `S-id substring S1120` — `SID_RE` is boundary-anchored `(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])`
   so `S2430` does not match; `source row opened before/after the window`; `used-by lacks the entry`).
   Command:
   `python3 -I -B -c "import re,subprocess; E='<entry-path>'; S='<stem>'; ent=subprocess.run(['git','show','<REV>:'+E],capture_output=True,text=True).stdout; ids=set(re.findall(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z]','\n'.join(l for l in ent.splitlines() if l.startswith('source:')))); reg=subprocess.run(['git','show','<REV>:corpus/SOURCES.md'],capture_output=True,text=True).stdout; rows={}; [rows.update({r.split('|')[1].strip(): [c.strip() for c in r.split('|')[1:-1]]}) for r in reg.splitlines() if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', r)]; ok=[i for i in ids if i in rows and len(rows[i])==11 and rows[i][8] in ('2026-10-28','2026-10-29') and (E in rows[i][10] or S in rows[i][10])]; print('cited',sorted(ids)); print('linked',sorted(ok)); exit(0 if set(ok)==ids else 1)"`
   (expect cited == linked == {S243,S244,S245,S249}; also print `rows[i][10]` to eyeball the reverse link).

## D. Content discipline

6. **Every conclusion paragraph is labelled [observation] / [inference] / [unknown]; layout- and
   provenance-derived statements are inference, never observation** (QUALITY 5; SKILL.md
   observation/inference/unknown discipline). Headings, `source:/status:/verified-at:/recheck:` lines,
   tables and the HTML comment are exempt.
   Command:
   `awk 'BEGIN{inc=0} /<!--/{inc=1} /-->/{inc=0; next} !/^#/ && !/^\[/ && !/^[0-9]+\. \[/ && !/^source:/ && !/^\|/ && !/^ *$/ && !/^status:/ && !/^verified-at:/ && !/^recheck:/ && !inc {c++; if(c<=5) print NR": "$0} END{print "unlabelled="c+0}' <entry>`
   (expect `unlabelled=0`; any hit is a fail unless the reviewer classifies it as caption).

7. **A "What was NOT examined" section names the unexamined surfaces**: no REA run by the draft
   author; the other census models; non-xz LE bodies; xattr-bearing bodies; AVM kernel images; nested
   sub-images below depth 1; the cable images' BE ARM member; the census `sqsh` v3 / zero-length rows;
   the AVM 8-byte trailer (QUALITY 7).
   Command (heading present AND at least five named surfaces):
   `s=$(sed -n '/NOT examined/,/^## /p' <entry>); echo "heading=$(echo "$s" | grep -c 'NOT examined')"; for t in 'depth 1' 'kernel image' 'xattr' 'ARM member' 'trailer' 'zero-length'; do echo "$t: $(echo "$s" | grep -ic "$t")"; done`
   (expect `heading=1` and at least five token lines with count ≥1).

8. **Capability/tool pins present: rea-agents@6.5.0, unblob 26.6.4, sasquatch 4.5.1, unsquashfs
   4.7.5**, each with its claim source (QUALITY 8, 39 — the pin rides the call record that produced
   the evidence, `runs.tsv` row / envelope, not the prose alone).
   Command (backticks stripped first — the entry writes `` `sasquatch` 4.5.1 ``):
   `e=$(sed 's/[\x60]//g' <entry>); for t in 'rea-agents@6\.5\.0\|rea-agents 6\.5\.0' 'unblob 26\.6\.4' 'sasquatch 4\.5\.1' 'unsquashfs 4\.7\.5'; do echo "$t: $(echo "$e" | grep -c "$t")"; done`
   (each count ≥1; the run receipt `corpus/evidence/round-50/c1/<id>/run.json` names the same pins).

9. **Counts carry their commands or frozen tables**: oracle regular-file counts in the results table
   equal the frozen `tools/round-50/oracle/<id>.oracle.tsv` row counts (the tsvs have no header and no
   trailing newline — use `awk END NR`, not `wc -l`); census counts (70 model directories, 28 LE `hsqs`
   rows, 16 models) re-derive from the corrected w1 census (`.ufo/waves/round-50/w1/C1CarrierAdversary.md`
   finding 2), and each count names its producer (QUALITY 1, 6, 13 — `grep -o … | wc -l` on
   minified/multi-row surfaces, never `grep -c`).
   Command:
   `for f in tools/round-50/oracle/g7581.oracle.tsv tools/round-50/oracle/g7582.oracle.tsv tools/round-50/oracle/c6490.oracle.tsv tools/round-50/oracle/c6430.oracle.tsv; do echo "$f $(awk 'END{print NR}' "$f")"; done`
   compared against the entry's four results rows (4 556 / 4 564 / 4 709 / 3 955 at the freeze).

10. **Every `ev_` evidence id cites its reproducing call** — tool name, carrier sha256 pin, run
    parameters (QUALITY 6; if an id-identity *class* is claimed it names verb/pin/carrier and the
    class per QUALITY 37/41). Command:
    `grep -n 'ev_' <entry>` — each hit sits in a sentence naming the producing call and carrier pin;
    a bare id is a fail.

## E. Required disclosures (the plan's own words, verified present)

11. **Carrier-swap disclosure present**: 7530/7590 named, ~13.4k regular files, the pre-freeze dev-arm
    `provider_timeout` receipt, the load-dependence rationale, replacement by 7581/7582 07.18 — and
    the 13k-file LE rootfs stays Frontier ("Still Frontier"), not claimed (plan R50-C1 "Carrier
    swap"; QUALITY 18).
    Command: `grep -n '7530\|7590\|dev-arm-timeouts\|Still Frontier' <entry>` (≥4 hits across both).

12. **Marker-constant disclosure present**: the marker is "a constant of the pinned bytes",
    re-stampable, invisible to unblob's LE branch (its `is_avm` test sits in the BE v4 branch only),
    and proves no origin — `layout_ok` is a frozen-layout statement, not a genuineness test (counter
    docstring "What the layout test is NOT", `c1-counter.py:44-61`; plan disclosed limit 1).
    Command: `grep -in 'constant of the pinned bytes\|re-stamp' <entry>` (≥2 hits) plus
    `grep -n 'What the layout test is NOT\|invisible to unblob' <entry>` (the disclosure verbatim).

13. **The seven disclosed limits of R50-C1 are restated** in a Limits section (plan "Disclosed
    limits" (1)–(7)). Command:
    `sed -n '/## Limits/,/^## /p' <entry> | grep -c '^[0-9]\+\.'` (≥7 numbered items).

14. **Scope sentences carry no universal beyond the four carriers**: no unqualified "every LE AVM
    image", "all AVM images", "hsqs always/never …"; universals appear only as scoped census
    statements (70 dirs on `download.avm.de`, 28 rows, none without the marker — with the search
    named) or as explicit negations of scope ("not 'every LE AVM image'"). Enforces QUALITY 5/7 and
    plan disclosed limit 5.
    Command: `grep -in 'every LE\|all AVM\|always\|never ' <entry>` — inspect every hit; an
    unscoped universal is a fail.

## F. Hygiene and landing integrity

15. **No credential material**: no cookies, session ids, `Authorization`/`Bearer`/`Set-Cookie`
    values anywhere (QUALITY; M50-4; the w1 S150-class lesson). Licence prose (S249 quote) is the
    only expected near-hit and contains no credential.
    Command: `grep -in 'set-cookie\|cookie:\|authorization\|bearer\|session=' <entry>` (zero hits).

16. **No placeholders remain and results numbers come from the committed receipts**:
    zero `FILLED AT LANDING` / `TODO` strings; the published/gap/removal columns equal
    `corpus/evidence/round-50/c1/<id>/after.json` (QUALITY 2, 18). Command:
    `grep -c 'FILLED AT LANDING\|TODO' <entry>` (expect 0) — and the falsify wave's counter re-run
    (item 18) is the authoritative equality check of numbers vs receipts.

17. **Temporal statements are in instant-pin form or absent; all zoned timestamps ≤ the landing
    commit's committer time** (QUALITY 19, 23 — `evidence-timestamps.py --strict` exit 0; zoneless
    timestamps stated as unchecked).
    Command: `grep -in 'unchanged\|stable\|throughout' <entry>` (inspect; require instant-pin form
    with retained records) and
    `python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root <LANE> --rev <REV> --path corpus/knowledge --strict` (exit 0).

18. **The entry's frozen-counter score is green at the landing REV and the companion bindings land
    in the same commit**: PROVINCE `## Round-50 additions to Core` row (cell 0 `squashfs_v4_le`,
    `AVM[ _-]marker` token outside the entry path, entry path in the row — `c1-counter.py:2443-2448`);
    one PROVINCE line with `Round-50 frontier note` + stem + `LE-AVM`/`AVM-LE` token outside the stem
    (`:2454-2455`); README `## Coverage map` table row containing the stem (`:2481-2482`); the
    counter run itself `carriers_matched 4`, every binding true, `frozen_path_changed []`, exit 0
    with the rerun receipt under `/fast/scratch/hyaku/kaidoku-r50/` (predicate `parameters.output_directory`
    prefix clause).
    Command (bindings, offline): import the frozen counter and apply its exact predicates —
    `python3 -I -B .ufo/waves/round-50/w3/ScribeProvinceBinding/check-bindings.py <landed-PROVINCE-snippet> <LANE>`-style
    run, or the equivalent snippet reusing `c1-counter.py`'s `section/cells/HANDLER_RE/AVM_MARKER_RE/LE_AVM_RE`
    (`check-bindings.py` ships in the w3 seat dir for this); the counter run is the L1's
    `python3 -I -B tools/round-50/c1-counter.py --root <LANE> --rev <REV> --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --pkg65 <pkg> --work <SCRATCH> --carrier-cache <CACHE> --json-out <OUT>` (exit 0).

19. **Every receipt path the entry names exists at REV** (QUALITY 52 — cite only committed runs).
    Command:
    `for p in $(grep -oE '[./][A-Za-z0-9_./-]*\.(json|txt|tsv|md)' <entry> | sort -u | grep -v '^\./tools\|corpus/knowledge'); do git cat-file -e "<REV>:$p" 2>/dev/null || echo "MISSING $p"; done`
    (no MISSING lines; the frozen `tools/round-50/` paths are checked by the counter's own pin rules).

## Residual notes for the reviewer

- Items 4, 16(second half) and 18(counter run) depend on L1-produced artifacts (re-opens, data run,
  counter run). Until they exist, score those items **2**, per the verdict rule.
- This bar checks the entry's text and its linkage. It does not re-derive the carrier pins, the
  oracle, or the REA projection — those are the frozen counter's clauses and the falsify wave's
  re-run duties under the same predicate.
- The four S-rows (S243/S244/S245/S249) do not exist at the freeze; they land with the entry
  (scanned at HEAD 2026-10-29T20:37Z: only S246–S248 registered). Item 5 therefore cannot go green
  before the landing commit itself — that is expected, not a defect.
