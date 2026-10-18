# CR1 — C1: how independent is replay with the same instruments?

**Verdict: PARTIAL — same-instrument re-runs have real reproducibility value, but do not independently validate the instrument’s scope, classification rules, or false-negative rate.** I independently re-derived selected source-shape and structural results from the cited commit archives. I also re-ran the archived R2 v9 instrument and the R4 v10 instrument on their cited archived trees, then reproduced a known false-PASS mutation on both. That defect limits what a PASS can support; it does not, by itself, prove the actual R2 Kimi-pin values were wrong.

## Axes

- **Reproducibility:** does the named source tree plus named tool reproduce the recorded value?
- **Independence:** does a separate method/oracle test the tool’s scope and interpretation, rather than merely run the same logic again?
- **Decision value:** what stronger claim, if any, does the reproduced result justify?

## Evidence — commands run and observed output

All tree-state checks below used `git archive` into my isolated scratch namespace `/var/tmp/arc2-l5r5-CR1-trees.BZt7Ju`. No live config was read: the census runs used a synthetic `HOME` with pins/cache package versions matching the recorded 6.5.0 / 6.5.0 / 6.7.0 values. Therefore those runs re-derived archived-text classification, not current external configuration truth.

### R1: the source append and named loci reproduce; the interpretation is not an objective count

Commands run:

```console
S=/var/tmp/arc2-l5r5-CR1-trees.BZt7Ju
mkdir -p "$S/r1-before" "$S/r1-after"
git archive 4b806e1 corpus/knowledge/2026-10-13-r3-jq-provenance.md | tar -x -C "$S/r1-before"
git archive df31bfb corpus/knowledge/2026-10-13-r3-jq-provenance.md | tar -x -C "$S/r1-after"
python3 - "$S/r1-before/corpus/knowledge/2026-10-13-r3-jq-provenance.md" "$S/r1-after/corpus/knowledge/2026-10-13-r3-jq-provenance.md" <<'PY'
import pathlib,re,sys,hashlib
before,after=map(lambda x:pathlib.Path(x).read_bytes(),sys.argv[1:])
pat=re.compile(rb'benign|malicious|safe|trust',re.I)
for label,data in [('4b806e1',before),('df31bfb',after)]:
 lines=data.decode().splitlines()
 marker=next((j+1 for j,x in enumerate(lines) if 'Safety-verdict scope' in x),10**9)
 print(label,'bytes=',len(data),'matching_loci_before_erratum=',[(i+1,l.strip()) for i,l in enumerate(lines) if i+1 < marker and pat.search(l.encode())])
print('prefix_8453_equal=',before[:8453]==after[:8453], 'sha256_before=',hashlib.sha256(before).hexdigest(), 'sha256_after_prefix=',hashlib.sha256(after[:8453]).hexdigest())
lines=after.decode().splitlines(); marker=next(i for i,x in enumerate(lines) if 'Safety-verdict scope' in x)
print('erratum_mentions_60_136=',all(re.search(fr':{n}(?!\d)', '\n'.join(lines[marker:])) for n in (60,136)))
PY
```

Observed output excerpt:

```text
4b806e1 bytes=8453 matching_loci_before_erratum=[(60, 'benign, intentional install: ...'), (136, '... no malicious or accidental pathway indicated ...')]
df31bfb bytes=9575 matching_loci_before_erratum=[(60, 'benign, intentional install: ...'), (136, '... no malicious or accidental pathway indicated ...')]
prefix_8453_equal=True sha256_before=697804b540c08dbeb09f182dfa3f2784983ed606e4939a83e297a4df1d52fe0a sha256_after_prefix=697804b540c08dbeb09f182dfa3f2784983ed606e4939a83e297a4df1d52fe0a
erratum_mentions_60_136=True
```

This reproduces the two loci and append-only shape underlying `SCORECARD.md:665-680`; the words did not disappear, so `2→0` is a scope/disposition judgment (“named by a qualifying erratum”), not a raw-text count. The note’s own assertions are evidence for that judgment, not an independent oracle for whether its qualification is adequate. Pointers: `SCORECARD.md:653-668`; `corpus/knowledge/2026-10-13-r3-jq-provenance.md:139-141`.

### R2: v9 PASS reproduces on its cited tree, but the same instrument accepts a false-current-value mutation

I extracted the exact 429-line v9 code fence from the archived R2 E22 report and executed it against archived `b21c0da`. `HOME` was set to the scratch fixture below, with pin values and cache-version `package.json` values matching the archived records; no live config was read. I then copied that archive and changed only `SCORECARD.md:57` from Devin/OMP `6.5.0` to uncached `6.9.9`.

```console
S=/var/tmp/arc2-l5r5-CR1-trees.BZt7Ju
mkdir -p "$S/r2-after"
git archive b21c0da corpus/README.md PROVINCE.md SKILL.md SCORECARD.md .ufo/waves/arc2-loop1-round2/E22.md .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt | tar -x -C "$S/r2-after"
H="$S/fakehome"
mkdir -p "$H/.config/devin" "$H/.omp/agent" "$H/.kimi-code" "$H/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents" "$H/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents" "$H/.npm/_npx/dea9475797100b20/node_modules/rea-agents"
printf '{"args":["rea-agents@6.5.0"]}\n' > "$H/.config/devin/mcp_config.json"
printf '{"args":["rea-agents@6.5.0"]}\n' > "$H/.omp/agent/mcp.json"
printf '[mcp_servers.rea]\nargs=["rea-agents@6.7.0"]\n' > "$H/.kimi-code/config.toml"
printf '{"version":"6.5.0"}\n' > "$H/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json"
printf '{"version":"6.7.0"}\n' > "$H/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/package.json"
printf '{"version":"6.4.0"}\n' > "$H/.npm/_npx/dea9475797100b20/node_modules/rea-agents/package.json"
HOME="$H" python3 - "$S/r2-after/.ufo/waves/arc2-loop1-round2/E22.md" "$S/r2-after" "$S" <<'PY'
import os,re,sys,pathlib,shutil
report=pathlib.Path(sys.argv[1]).read_text()
post=report.split('### Block B — the instrument (v9, validated; 429 lines)',1)[1]
code=re.search(r'```python\n(.*?)\n```',post,re.S).group(1)
print('EXTRACTED_V9_LINES=',len(code.splitlines()))
ns={'__name__':'c1audit','__file__':'c1-census-v9.py'}
exec(compile(code,'c1-census-v9.py','exec'),ns)
roots=[('recorded-tree',sys.argv[2])]
mut=os.path.join(sys.argv[3],'r2-after-mutated')
if os.path.exists(mut): raise SystemExit('fixture already exists: '+mut)
shutil.copytree(sys.argv[2],mut)
p=pathlib.Path(mut)/'SCORECARD.md'; lines=p.read_text().splitlines(keepends=True)
assert 'historical' in lines[56] and '6.5.0' in lines[56], repr(lines[56])
lines[56]=lines[56].replace('6.5.0','6.9.9',1); p.write_text(''.join(lines))
roots.append(('mutated-6.9.9-no-cache',mut))
for label,root in roots:
 sys.argv=['c1-census-v9.py','--root',root,'--quiet']
 print('---',label,'---')
 print('RETURN_CODE=',ns['main']())
PY
```

Observed output excerpt:

```text
EXTRACTED_V9_LINES= 429
--- recorded-tree ---
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
RETURN_CODE= 0
--- mutated-6.9.9-no-cache ---
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
RETURN_CODE= 0
```

This is a concrete false-negative for the broad “every current-surface version/pin statement” acceptance framing: `E22.md:551,589-592` uses a same-physical-line `historical` marker to classify the changed Devin/OMP value as historical. The distinction matters: the round’s specific six stale Kimi-pin values may still be correctly reconciled; the tool’s PASS does not independently establish that its whole declared surface has no false current values. R4’s CR3 independently documented the same mutation and the scope of what it does/does not refute at `.ufo/waves/arc2-loop1-round4/CR3.md:10-15,221-235`.

### R3: append shape re-derives, but not the six-locus semantic disposition

Commands run:

```console
S=/var/tmp/arc2-l5r5-CR1-trees.BZt7Ju
mkdir -p "$S/r3-before" "$S/r3-after"
git archive 679af5d corpus/knowledge/2026-10-13-mcp-registrations.md corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md | tar -x -C "$S/r3-before"
git archive dbba2dd corpus/knowledge/2026-10-13-mcp-registrations.md corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md | tar -x -C "$S/r3-after"
for rev in before after; do
  for f in corpus/knowledge/2026-10-13-mcp-registrations.md corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md; do
    printf '%s %s lines=' "$rev" "$f"
    wc -l < "$S/r3-$rev/$f"
  done
done
cmp <(head -n 88 "$S/r3-before/corpus/knowledge/2026-10-13-mcp-registrations.md") <(head -n 88 "$S/r3-after/corpus/knowledge/2026-10-13-mcp-registrations.md") && printf 'prefix_%s_lines_equal=%s\n' '2026-10-13-mcp-registrations.md' 88
cmp <(head -n 936 "$S/r3-before/corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md") <(head -n 936 "$S/r3-after/corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md") && printf 'prefix_%s_lines_equal=%s\n' '2026-10-13-r4-16-frontier-rescan.md' 936
```

Observed output excerpt:

```text
before corpus/knowledge/2026-10-13-mcp-registrations.md lines=88
before corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md lines=936
after corpus/knowledge/2026-10-13-mcp-registrations.md lines=111
after corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md lines=975
prefix_2026-10-13-mcp-registrations.md_lines_equal=88
prefix_2026-10-13-r4-16-frontier-rescan.md_lines_equal=936
```

This independently confirms the append-only landing shape, not E23’s “unwarned dead loci 6→0” classification. That stronger number depends on the instrument’s chosen files, target-resolution model, and definition of “warned”; it should be labeled as instrument-measured unless independently recounted. Pointer: `SCORECARD.md:780-796`; unit and limits are explicit at `.ufo/waves/arc2-loop1-round3/E23.md:244-279` and `:927-963`.

### R4: structural 10→11 reproduces; v10 PASS does not establish its own completeness

I independently counted citation-resolvable rule blocks from the `158a966` and `265e1aa` archives using the recipe’s parsing and line-range semantics. The archive commands and re-derivation were:

```console
S=/var/tmp/arc2-l5r5-CR1-trees.BZt7Ju
mkdir -p "$S/r4-before" "$S/r4-after"
git archive 158a966 SKILL.md SHONEN.md SCORECARD.md | tar -x -C "$S/r4-before"
git archive 265e1aa SKILL.md SHONEN.md SCORECARD.md .ufo/gates/c1-census-v10.py | tar -x -C "$S/r4-after"
git archive 158a966 corpus/knowledge | tar -x -C "$S/r4-before"
git archive 265e1aa corpus/knowledge | tar -x -C "$S/r4-after"
git archive 158a966 PROVINCE.md | tar -x -C "$S/r4-before"
git archive 265e1aa PROVINCE.md | tar -x -C "$S/r4-after"
python3 - "$S/r4-before" "$S/r4-after" <<'PY'
import pathlib,re,sys
roots=[pathlib.Path(x) for x in sys.argv[1:]]
def get(root):
    text=(root/'SKILL.md').read_text()
    section=text.split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
    rules=re.split(r'(?m)^- \*\*',section)[1:]
    pattern=r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    resolved=0
    for rule in rules:
        refs=re.findall(pattern,rule); ok=bool(refs)
        for name,a,b in refs:
            try:
                count=len((root/'corpus/knowledge'/name).read_text().splitlines())
                start,end=int(a or 1),int(b or a or 1)
                ok &= 1 <= start <= end <= count
            except OSError: ok=False
        resolved += bool(ok)
    return rules,resolved,len(list((root/'corpus/knowledge').glob('*.md')))
a,ar,af=get(roots[0]); b,br,bf=get(roots[1])
print(f'158a966: rules={len(a)} resolvable={ar}/{len(a)} knowledge_files={af}')
print(f'265e1aa: rules={len(b)} resolvable={br}/{len(b)} knowledge_files={bf}')
print('first9_equal=',a[:9]==b[:9],'old10_moved_to_after11=',a[9]==b[10])
PY
```

Observed output:

```text
158a966: rules=10 resolvable=10/10 knowledge_files=79
265e1aa: rules=11 resolvable=11/11 knowledge_files=79
first9_equal= True old10_moved_to_after11= True
```

An initial positional comparison put the old tenth rule beside the newly inserted rule and falsely reported a text difference; the insertion-aware match above resolves that. The command-A proxy therefore reproduces, but it tests that citations resolve, not that a craft rule is correct or useful: `SCORECARD.md:24` states this limitation; recipe at `SCORECARD.md:92-123`.

I also ran the committed v10 script on a complete archive of its cited `265e1aa` tree, then on a scratch copy with only the same `6.5.0→6.9.9` mutation at `SCORECARD.md:57`. Both runs used the synthetic anchors above.

```console
S=/var/tmp/arc2-l5r5-CR1-trees.BZt7Ju
python3 - "$S/r4-after" "$S/r4-after-mutated" <<'PY'
import pathlib,shutil,sys
src,dst=map(pathlib.Path,sys.argv[1:])
if dst.exists(): raise SystemExit('fixture exists')
shutil.copytree(src,dst)
p=dst/'SCORECARD.md'; lines=p.read_text().splitlines(keepends=True)
assert 'historical' in lines[56] and '6.5.0' in lines[56], repr(lines[56])
lines[56]=lines[56].replace('6.5.0','6.9.9',1); p.write_text(''.join(lines))
print('MUTATION=Scorecard line 57 Devin/OMP 6.5.0 -> uncached 6.9.9; other archived bytes unchanged')
PY
HOME="$S/fakehome" python3 "$S/r4-after/.ufo/gates/c1-census-v10.py" --root "$S/r4-after" --quiet
HOME="$S/fakehome" python3 "$S/r4-after/.ufo/gates/c1-census-v10.py" --root "$S/r4-after-mutated" --quiet
```

Observed excerpt for **both** runs:

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

The mutated run is a direct counterexample: v10 retains the G12 inline-marker behavior (the `INLINE_MARKER` includes `historical`, then classification marks a locus historical based on that physical line) at `.ufo/gates/c1-census-v10.py:115,290-340`. The census’s declared `SCOPE` is explicit and valuable for fail-closed coverage growth, but its table remains an author-controlled premise, not an independently established census boundary: `.ufo/gates/c1-census-v10.py:85-108,195-199,391-407`. R4’s recorded PASS at the work tree is at `SCORECARD.md:880-888`; it is reproducible on that commit, but the mutation shows what the result cannot establish.

## Steelman: why same-instrument re-derivation still matters

A fresh run by a different verifier against an immutable archive is not pointless. It can catch a wrong revision, missing input, nondeterminism, a transcription error, a broken invocation, or an unlanded change masquerading as measured. R4’s `1692acb` mid-wave commit titled “rule 11” did not change `SKILL.md`; command A read 10 rules there, while the real landing at `265e1aa` reads 11. Re-running the measure at the cited commit distinguishes those states (`SCORECARD.md:864-871,886-888`; `.ufo/waves/arc2-loop1-round4/CR1.md:82-108`). Exact code hashes and immutable trees also make historical results replayable. The value is **reproducibility and commit attribution**, not an independent endorsement of the instrument’s contract.

The theater case is strongest where the instrument author also chooses the scope table, exception markers, disposition unit, and expected outcome: a PASS can mean “the selected rows satisfy the rules I encoded,” while omitted rows, bad classification rules, or a forgiving marker remain invisible. Re-running unchanged code on unchanged inputs reproduces that blind spot. Prior rounds explicitly mark the absence of an outside verifier (`.ufo/reports/arc2-loop1-round2/kaidoku.md:94-112`; `.ufo/reports/arc2-loop1-round4/kaidoku.md:100-101`). R4’s R2-v9 mutation is not hypothetical theater; it is a measured same-instrument false PASS.

## Text the parent should land verbatim

```text
Independent-check label: Re-running an instrument at a cited commit establishes reproducibility, not independent validation of its scope, parser, classification rules, or false-negative rate. Mark a before→after as independently confirmed only when a separately implemented method (not sharing the original instrument’s scope or classifier) derives the same result from the same archived trees, or when an independent oracle and a predeclared adversarial control validate the instrument. Otherwise label it replay-confirmed, not instrument-validated. C1 census PASS values are replay-confirmed unless accompanied by such a check; v9/v10 still PASS an uncached Devin/OMP 6.9.9 mutation at SCORECARD.md:57 because “historical” is line-scoped. This defect does not by itself refute round 2’s Kimi-only pin reconciliation.
```

## Conclusions

- **Observation:** R1’s archived file has the two original label loci at `:60` and `:136`; the 8,453-byte prefix is identical after landing and the erratum names both. This verifies the source change, not the adequacy of its qualification (`SCORECARD.md:665-680`).
- **Observation:** R2’s exact v9 replay passes on archived `b21c0da`; the uncached 6.9.9 mutation also passes. R4’s v10 replay passes on archived `265e1aa`; the same mutation still passes. The false-PASS behavior is independently recorded by CR3 (`CR3.md:13,221-235`).
- **Observation:** R3’s two cited file growth/prefix claims reproduce from archives. I did not rederive the E23 instrument’s full 6→0 warning classification.
- **Observation:** R4’s structural rule count reproduces as 10/10→11/11 with the original tenth block shifted to the eleventh position; the v10 result reproduces at its cited commit using synthetic anchors.
- **Inference:** Same-instrument replay has useful audit value for reproducibility, determinism, and commit attribution. It does not earn an “independent validation” label. The false-PASS witness specifically blocks using census PASS as evidence that the instrument catches every wrong current-surface pin.
- **Unknown:** Whether every falsifiable R1–R4 before→after item has a second, independent derivation. This seat stress-tested representative C1 measurements rather than completing that full ledger. Historical config contents were not available as archived files here, and no live config or REA probe was run.

## Scope

Only this report is a repository write. Scratch archives and synthetic test fixtures are confined to `/var/tmp/arc2-l5r5-CR1-trees.BZt7Ju`; no git mutation, config access, install, network, or live probe. One initial selective archive request asked for the not-yet-existing v10 path at `158a966`, and one incomplete R4 archive omitted `PROVINCE.md`; both were corrected before any reported R4 result. No C1 claim is made from those incomplete runs.
