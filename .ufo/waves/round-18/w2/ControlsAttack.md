BROKEN

# ControlsAttack — author-side advisory, not admission

**Axes:** calibration (truth of preservation flags), operability (what the consumer actually rejects), depth (ordinary mutations versus masked mutations).

**Scope:** `REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, `B=9011581d84527ba34c675f9cf912e54d2e72d470`, freeze `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. All lane `path:line` anchors below refer to bytes obtained with `git show REV:path`, not the moving worktree. `controls.py` is new relative to B. This verdict means the report can falsely assert preservation under a harmful mutation; it does **not** allege those mutations occurred in the delivered revision.

## Findings, by severity

### Medium — F1: an immutable SOURCES cell can change while `immutable_cells_unchanged` remains true

**Observation (reproducer A2/A3):** replacing S003's Base-src.zip SHA-256 anchor with 64 zeros is detected directly: `immutable_violations={"S003":[6]}`. Append the original row at EOF inside an HTML comment, with U+00A0 around its ID, and the same harmful edit instead produces `immutable_cells_unchanged:true`, `immutable_violations:{}`, and `rows_after:36`. The fleet's read-only `sources-census.sh validate "$PWD"` also exited **0**, with exactly the same W04 warning and `ok` outcome as the reference clone. `cmark` emitted the original anchor once at REV, zero times after the mutation; the altered Registry row remained outside the comment.

**Cause:** `.ufo/waves/round-18/controls.py:71` accepts Unicode whitespace; `:169-183` scans the entire file and builds a dictionary using stripped IDs, silently retaining the **last** occurrence. The shadow row therefore replaces the real Registry row before `:393-415` performs immutable-cell comparison. Counts also use this deduplicated dictionary. This defeats the contracted S001–S032 protection (`.ufo/waves/round-18/contract.md:142-145`).

**Repair direction:** validate the one Registry section and reject duplicate IDs/unexpected row-shaped material before comparison; use a consistent row/whitespace grammar with the census. Do not interpret a last-wins map as evidence that every occurrence survived.

### Medium — F2: QUALITY rows can be deleted or weakened while both preservation flags remain true

**Observation (A4/A5):** A4 puts a commented copy of the admission table before the real heading, then deletes row 13 from the real table. A5 instead weakens the real row from `never grep -c` to `or grep -c` and places the original row in a later HTML comment inside the section. Both exited **0** and returned `prior_rows_byte_identical:true`, `rows_1_20_identical:true`, `violations:{}`, `rows_after:21`. For A4, `cmark` emitted the original row-13 prohibition once at REV and zero times after mutation.

**Cause:** `.ufo/waves/round-18/controls.py:194` selects the first **substring** occurrence of `## Admission criteria`, including one inside a comment; `:201-204` treats commented row lines as table entries and silently overwrites duplicate row numbers. `:363-377` consequently compares the concealed copies, not the changed active table. This contradicts the specific row-preservation claim at `:23-25` and `:358-361`, not merely an unclaimed semantic audit.

**Repair direction:** identify the actual Markdown section/table, reject ambiguous headings and duplicate row numbers, then compare its rows. Comment/code-block copies must not stand in for the active criteria.

## Operability and coverage limits — distinguish these from the false flags above

These are demonstrated limits of the no-harm evidence, not all new contract violations. Reproducers are included below.

| Case | Observation; all controls invocations exited 0 | Relevant REV anchors |
|---|---|---|
| A1: edit prior, non-appendable knowledge | **Detected in JSON**, named knowledge violation; exit remains 0. | `controls.py:238-267,794-803` |
| A6: delete `SKILL.md:450`, the quote-fidelity registry row | Listed: deleted count **6→7**, including the removed row. No rejection predicate. A6b comments out the four-row registry table with **no new deleted lines** (deleted/added **6/53→6/55**). | `controls.py:423-445`; contract `:145` explicitly asks for deleted lines to be listed, not judged. |
| A7: add files inside W17 predictions and `evidence/` | Frozen count stays **15517/15517**; no additions list. This protects old blobs, not directory membership. | `controls.py:316-329`; `SKILL.md:593` should not be read as proof of *all* permitted wave-evidence deltas. |
| A8: modify frozen r18 `decision-rule.json` after freeze | B→attack leaves the same clean control flags. **FREEZE→attack does name the changed decision-rule** (and the independently changed `tools/routed-defects.py`). B has no r18 predictions to protect. This probe adds a JSON field; it demonstrates missing freeze-byte coverage, not a changed mechanism verdict. | `controls.py:323-328`; `verify.py:87,105-114,236,268-285` |
| A9: replace contracted r17 receipt validator by an always-clean stub | Same contracted-byte-identity results as REV (all six false); stub `--selftest` prints `SELFTEST: CLEAN cases=1`, exit 0. Path carve-outs do not constrain fix content. | `controls.py:57-64,330-341`; `verify.py:160-162,200-201` |
| A10: same blob, regular file→symlink | Old verifier still reports unchanged/byte-identical. `ls-tree` shows **100644→120000**, same blob `427dcadaeb6a1d1286b3439f452b9bd15eccb21f`. Checkout in a separate temp worktree fails **128**, `unable to create symlink ... File name too long`; do not claim a successful symlink checkout. | `controls.py:104-115,226-234,256-261` retain SHA but discard mode. |
| A11: alter receipt/gate expectations, remove coverage row, weaken QUALITY preamble/remove Signals row | Selected no-harm flags unchanged. `.ufo/receipts`, `.ufo/gates`, `.ufo/rounds`, corpus README and non-admission QUALITY text are outside these controls. Existing B→REV edits to `corpus/README.md:35` and SOURCES Paths `:48` likewise have no dedicated report. | `controls.py:50-56,192-204,381-384,448-480` |

**Consumer inference, not an executed full pass:** `.ufo/waves/round-18/verify.py:236` expects controls exit 0; `:127` checks only the process return code; `:286,294-295` aggregate unexpected exits/pin equality/pycache. It never rejects the controls JSON's violations. Thus an ordinary detected mutation contributes an *expected* controls exit, although other commands might independently fail. This is compatible with the reporter's honest `not a verdict` description (`controls.py:9`) and `conformance_gate:false` (`:497`); it is **not** an automated no-harm gate. If automatic rejection is intended, explicitly consume the preservation predicates or add a strict mode. No claim is made that the entire `verify.py` pass succeeds for any mutant.

## Holds and exercised verification

**Observation:** B→REV controls exited **0**: LOG/SCORECARD old prefixes retained; knowledge **95/95** including the one appendable entry; lessons **22/22**; prior verifiers **6/6**; frozen blobs **15517/15517**; restored sums line accepted; QUALITY **20→21**, rows 1–20 identical; SOURCES **32→36**, no immutable-cell violations; craft **17/17** unchanged; SKILL deleted/added **6/53**. `python3 -I -B .ufo/waves/round-18/controls.py --selftest` in the first temporary clone exited **0**, `SELFTEST: CLEAN cases=23`.

Direct mutations were not silently missed: A1 knowledge title rewrite, A2 S003 anchor rewrite, H1 rewrite within the appendable r17 entry's old prefix, H2 QUALITY row-7 deletion, H3 S010 deletion, H4 W17 carriers.tsv edit, H5 SCORECARD line-1 rewrite. H1 names the knowledge violation; H2 returns `{"7":"row_absent_at_after"}` and both QUALITY flags false; H3 returns `{"S010":"row_absent_at_after"}`; H4 reports **15516/15517** unchanged and `restored_ok:false`; H5 reports SCORECARD `prefix_preserved:false`. **Every one still exits 0**, as the declared reporter interface permits.

## Residual risk and verification gaps

- `xd://lsp` is **not mounted** (`No such tool`); status/references/definition/diagnostics were unavailable. Caller analysis is pinned source/text inspection, not semantic LSP proof.
- No REA, Ghidra, carrier binary, alternate runtime, jj, or full `verify.py` execution. No delegation or integration. Runtime identity/rerouting/saturation/resume-continuity are not exercised by this controls assignment.
- cmark **0.31.2** was used only to establish comment visibility, not GFM table conformance. The false flags also follow directly from the Git-object parser behavior.
- The external sources-census result is a **working-tree tool observation at test time**, not a tool pinned by the lane REV. Its output was checked against the reference clone and still allowed A3.
- SKILL diffs cap lists at 64 lines (`controls.py:77,439-444`); no saturation exploit was run. No claim of exhaustive mutation coverage or full semantic/pointer audit.
- All attack commits and writes were confined to origin-removed `mktemp` clones. Clones/drivers were removed. A temporary `/tmp/controls-attack-path.txt` breadcrumb was created early and immediately removed; no lane content was edited except this report. No installs/updates; existing tools: Git **2.56.0**, Python **3.14.8**, cmark **0.31.2**.

## Reproducing commands and observed exits

The following is the **executed** self-contained reproducer, pasted rather than pointing at a deleted temp script. It was run as `bash /tmp/controls-attack-Wr86eT/repro.sh` (**exit 0**). Each A/H case starts from REV, commits in the clone only, and invokes `python3 -I -B .ufo/waves/round-18/controls.py B ATTACK` (**exit 0 in every case**). The FREEZE→A8 producer and summary pipeline exited **0**; A3 census and A9 stub selftest exited **0**; A10 worktree checkout exited **128**, as printed. Setup/commit/cleanup commands completed; ephemeral commit hashes intentionally vary with commit time.

Observed non-reference changes in the displayed summary:

- A1: knowledge violation; A2: sources `[false,{"S003":[6]},36]`.
- A3/A4/A5/A7/A8/A9/A10/A11: displayed no-harm summary equals reference.
- A6: SKILL `[7,53]`; A6b: SKILL `[6,55]`.
- H1: knowledge violation; H2: QUALITY `[false,false,{"7":"row_absent_at_after"},20]`; H3: SOURCES `[false,{"S010":"row_absent_at_after"},35]`; H4: frozen `[15517,15516]`, sums false; H5: prefix `[true,false]`.
- Reference summary: prefix `[true,true]`, empty knowledge/lesson violations, all verifiers unchanged, frozen `[15517,15517]`, sums true, QUALITY `[true,true,{},21]`, SOURCES `[true,{},36]`, SKILL `[6,53]`, contracted-identical count 0, conformance gate false.

```bash
#!/usr/bin/env bash
# Round-18 w2 ControlsAttack reproducer: throwaway clone, origin removed; never touches the lane.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
B=9011581d84527ba34c675f9cf912e54d2e72d470
REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94
FREEZE=eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0
T=$(mktemp -d) && git clone -q --no-local "$LANE" "$T/c" && git -C "$T/c" remote remove origin
cd "$T/c" && git checkout -q --detach $REV
CTL=.ufo/waves/round-18/controls.py
summ() {
  python3 -I -B -c '
import json,sys
r=json.load(sys.stdin); f=r["prior_wave_evidence_blobs"]; q=r["quality_admission_rows"]; s=r["sources_registry"]; k=r["skill_md_diff"]
print(json.dumps({"prefix_LOG_SCORECARD":[r["old_prefix"][n]["prefix_preserved"] for n in ("LOG.md","SCORECARD.md")],
 "knowledge_violations":r["prior_corpus_text"]["corpus/knowledge"]["violations"],
 "lessons_violations":r["prior_corpus_text"]["corpus/lessons"]["violations"],
 "verifiers_unchanged":all(v["unchanged"] for v in r["prior_verifiers_unchanged"].values()),
 "frozen_checked_unchanged":[f["checked"],f["unchanged"]],"sums_restored_ok":f["r17_sums_restored_line"]["restored_ok"],
 "contracted_byte_identical":[v["byte_identical"] for v in f["contracted_modifications"].values()].count(True),
 "quality":[q["prior_rows_byte_identical"],q["rows_1_20_identical"],q["violations"],q["rows_after"]],
 "sources":[s["immutable_cells_unchanged"],s["immutable_violations"],s["rows_after"]],
 "skill_deleted_added":[k.get("deleted_count"),k.get("added_count")],"conformance_gate":r["conformance_gate"]},sort_keys=True))'
}
run() { python3 -I -B $CTL $B "$1" > ../out.json; echo "controls.py B ${1:0:12} exit=$?"; summ < ../out.json; }
commit() { git add -A && git -c user.name=a -c user.email=a@localhost commit -qm "$1" && git rev-parse HEAD; }
reset() { git checkout -q -f --detach $REV && git clean -qfdx; }

echo "== REV (reference)"; run $REV

echo "== A1 prior knowledge file edited in place"; reset
python3 -I -B - <<'PY'
p="corpus/knowledge/2026-10-13-asar-surface.md"; t=open(p).read(); open(p,"w").write(t.replace("\n"," (edited)\n",1))
PY
X=$(commit a1); run $X

echo "== A2 S003 anchor zeroed (direct)"; reset
python3 -I -B - <<'PY'
p="corpus/SOURCES.md"; t=open(p).read(); old="f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804"
row=[l for l in t.splitlines() if l.startswith("| S003 |")][0]; open(p,"w").write(t.replace(row,row.replace(old,"0"*64),1))
PY
X=$(commit a2); run $X

echo "== A3 S003 anchor zeroed + NBSP-padded original row in an HTML comment at EOF"; reset
python3 -I -B - <<'PY'
p="corpus/SOURCES.md"; t=open(p).read(); old="f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804"
row=[l for l in t.splitlines() if l.startswith("| S003 |")][0]
t=t.replace(row,row.replace(old,"0"*64),1)+"\n<!--\n"+row.replace("| S003 |","|\u00a0S003\u00a0|",1)+"\n-->\n"
open(p,"w").write(t)
PY
X=$(commit a3); run $X
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate "$PWD"; echo "sources-census exit=$?"
echo "rendered(cmark) original anchor at REV: $(git show $REV:corpus/SOURCES.md | cmark | grep -c f00d29c20119)  at A3: $(git show $X:corpus/SOURCES.md | cmark | grep -c f00d29c20119)"

echo "== A4 QUALITY row 13 deleted under a commented copy of the admission table"; reset
python3 -I -B - <<'PY'
p="corpus/QUALITY.md"; t=open(p).read(); head,sep,rest=t.partition("## Admission criteria")
table="\n".join(l for l in rest.split("\n## ",1)[0].splitlines() if l.startswith("|"))
r13=[l for l in rest.splitlines() if l.startswith("| 13 |")][0]
open(p,"w").write(head+"<!--\n## Admission criteria\n"+table+"\n-->\n\n"+sep+rest.replace(r13+"\n","",1))
PY
X=$(commit a4); run $X
echo "rendered(cmark) row-13 text at REV: $(git show $REV:corpus/QUALITY.md | cmark | grep -c 'never <code>grep -c</code>')  at A4: $(git show $X:corpus/QUALITY.md | cmark | grep -c 'never <code>grep -c</code>')"

echo "== A5 QUALITY row 13 weakened + original duplicated in a comment inside the section"; reset
python3 -I -B - <<'PY'
p="corpus/QUALITY.md"; t=open(p).read(); r13=[l for l in t.splitlines() if l.startswith("| 13 |")][0]
t=t.replace(r13,r13.replace("never `grep -c`","or `grep -c`"),1).replace("\n## Signals","\n<!--\n"+r13+"\n-->\n\n## Signals",1)
open(p,"w").write(t)
PY
X=$(commit a5); run $X

echo "== A6 SKILL registry row deleted (quote-fidelity gate)"; reset
python3 -I -B - <<'PY'
p="SKILL.md"; L=open(p).readlines(); open(p,"w").writelines(l for l in L if not l.startswith("| quote-fidelity | gate / kaidoku |"))
PY
X=$(commit a6); run $X

echo "== A6b SKILL four-row registry table wrapped in an HTML comment (no line deleted)"; reset
python3 -I -B - <<'PY'
p="SKILL.md"; L=open(p).readlines(); i=[n for n,l in enumerate(L) if l.startswith("| quote-fidelity | gate / kaidoku |")][0]; s=i
while L[s-1].startswith("|"): s-=1
L.insert(i+1,"-->\n"); L.insert(s,"<!--\n"); open(p,"w").writelines(L)
PY
X=$(commit a6b); run $X

echo "== A7 new files under frozen prefixes (W17 predictions, evidence/)"; reset
cp .ufo/waves/round-17/predictions/pro-aether.prediction.json .ufo/waves/round-17/predictions/pro-forged.prediction.json
echo '{"forged": true}' > evidence/round-1-2026-10-15/forged-receipt.json
X=$(commit a7); run $X

echo "== A8 r18 decision-rule.json edited after the freeze commit"; reset
python3 -I -B - <<'PY'
p=".ufo/waves/round-18/predictions/decision-rule.json"; t=open(p).read(); open(p,"w").write(t.replace("{",'{"forged_after_freeze": true, ',1))
PY
X=$(commit a8); run $X
python3 -I -B $CTL $FREEZE $X | python3 -I -B -c 'import json,sys; f=json.load(sys.stdin)["prior_wave_evidence_blobs"]["files"]; print("controls.py FREEZE A8 changed:", [p for p,v in f.items() if not v["unchanged"]])'

echo "== A9 contracted r17 tool replaced by an always-clean stub"; reset
printf '#!/usr/bin/env python3\nprint("SELFTEST: CLEAN cases=1")\n' > .ufo/waves/round-17/tools/receipt-validate.py
X=$(commit a9); run $X
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --selftest; echo "stub --selftest exit=$?"

echo "== A10 verifier spotcheck turned into a symlink with the same blob"; reset
p=corpus/lessons/round-12-verifier-spotcheck.md
git update-index --cacheinfo 120000,$(git rev-parse $REV:$p),$p && git -c user.name=a -c user.email=a@localhost commit -qm a10
X=$(git rev-parse HEAD); git ls-tree $REV -- $p; git ls-tree $X -- $p; run $X
git worktree add -q --detach ../wt $X; echo "worktree checkout of A10 exit=$?"; git worktree prune; rm -rf ../wt

echo "== A11 out-of-scope lane content (receipt, gate expectations, README row, QUALITY rule text, Signals row)"; reset
echo "FORGED" >> .ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt
python3 -I -B - <<'PY'
p=".ufo/gates/citation-drift/expected.json"; t=open(p).read(); open(p,"w").write(t.replace("{",'{"forged": true, ',1))
p="corpus/README.md"; L=open(p).readlines(); open(p,"w").writelines(l for l in L if not l.startswith("| Runtime observation |"))
p="corpus/QUALITY.md"; t=open(p).read().replace("never rewritten.","or rewritten in place.",1)
open(p,"w").write("".join(l for l in t.splitlines(True) if not l.startswith("| 3 | Findings attached")))
PY
X=$(commit a11); run $X

echo "== H1-H5 hold cases (each from REV)"
hold() { reset; python3 -I -B -c "$2"; X=$(commit "$1"); echo "-- $1"; run $X; }
hold H1-appendable-midprefix 'p="corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md"; L=open(p).readlines(); L[2]=L[2].rstrip("\n")+" [REWRITTEN]\n"; open(p,"w").writelines(L)'
hold H2-quality-row7-deleted 'p="corpus/QUALITY.md"; L=open(p).readlines(); open(p,"w").writelines(l for l in L if not l.startswith("| 7 |"))'
hold H3-S010-row-deleted 'p="corpus/SOURCES.md"; L=open(p).readlines(); open(p,"w").writelines(l for l in L if not l.startswith("| S010 |"))'
hold H4-w17-carriers-tsv-edited 'p=".ufo/waves/round-17/predictions/carriers.tsv"; open(p,"a").write("forged\t/x\n")'
hold H5-scorecard-line1-edited 'p="SCORECARD.md"; L=open(p).readlines(); L[0]=L[0].rstrip("\n")+" (edited)\n"; open(p,"w").writelines(L)'

cd / && rm -rf "$T" && echo "removed $T"
```
