# CR3 (critic) — attack C3: is the census scope-table re-key legitimate, or does it move the goalposts on round-2's recorded PASS?

Wave arc2-loop1-round4 · Seat CR3 · 2026-10-18 · HEAD at seat start `158a96611f22afdfa723131f3ec27f39138020e8`; HEAD observed to move mid-seat to `1692acbe48ce0eac3b7c87698be59d8a04f46a08` (commit "rule 11") — `git diff --stat 158a966 1692acb -- PROVINCE.md SKILL.md SCORECARD.md` → empty, so **all three census files are byte-identical across both HEADs** and every measurement below holds at either.
Read-only on the repo: my only write is this file. No git mutation, no config edit, no install, no network command. The live PE analyze was not signalled, renice'd, or read beyond a `ps` name check.

## 1. Verdict

**PARTIAL REFUTE — the re-key is legitimate in KIND but the form on the table is NOT goalpost-neutral, and it is NOT sufficient alone.** Two separable findings:

- **(a) Round-2's PASS is NOT invalidated.** It reproduces exactly: the E22 v9 instrument returns `VERDICT: PASS (0/0/0/0)` rc=0 on the reconstructed `b21c0da` tree. The FAIL is not round-2 claiming a false PASS; it is round-2's own *records* commit breaking the instrument it had just passed with — measured causally (removing that appended section restores PASS). Round-2's sentences are correctly scoped ("at the work tree", `SCORECARD.md:725`, `LOG.md:1037`) and round-2 itself named the debt accurately (`SCORECARD.md:850`).
- **(b) But the re-key, as specified, moves the goalposts in two measured ways.** (i) It is **not a disposition-neutral line remap**: it flips 6 assertions at HEAD out of `undeclared`/`AMBIGUOUS` into `current_ok` **by declaration, not by evidence** — 4 of them from `AMBIGUOUS`, i.e. loci where the instrument's own G14 deliberately refused to guess. (ii) It is **insufficient alone**: after the re-key the run still fails on `G11` at `SCORECARD.md:731`, so reaching C3's stated measurable requires a **second landing that edits round-2's own landed record**. That matches two independent seats (`.ufo/waves/arc2-loop1-round4/E16.md:315`, `.ufo/waves/arc2-loop1-round4/E20.md:18`).
- **(c) The open-ended bound variant recommended by E16/E20 permanently disables the instrument's core guard.** Measured: with `("SCORECARD.md", 703, 9999, …)` a later round's append citing a **fabricated, non-existent version** returns `PASS` rc=0; with the fixed bound `703, 766` the same append returns `FAIL undeclared=1` rc=1. The guard being switched off is exactly the one the instrument was built around — `E22.md:216` "file growth may never silently shrink the census".
- **(d) Independent pre-existing false PASS, unrelated to any re-key, on the very tree whose PASS round-2 recorded.** Mutating `SCORECARD.md:57`'s `Devin/OMP 6.5.0` → `Devin/OMP 6.9.9` (a version with **no cache on this host**) yields `VERDICT: PASS` rc=0 under the **unmodified** v9, because the word "historical" sits in the same physical line and G12's inline-marker test is line-scoped. This does not refute C1's Kimi-scoped claim, but it refutes any reading of this instrument as a general guard, and it must be fixed before a green exit is used as evidence.

**Recommendation to the parent:** land the re-key as a **fixed bound** (`703, 766`) plus the receipt phrase, and record the per-round one-line re-key as a named recurring obligation. Do **not** land `703, 9999`. Do not present the re-key alone as discharging C3.

## 2. Evidence — commands run THIS session, with observed output

### 2.0 Instrument identity and scratch

`/tmp` is quota-exhausted this session (`echo > /tmp/…` → `Disk quota exceeded`; tmpfs 13G/16G, 84% inodes) — my scratch is `/var/tmp/arc2-l4r4-CR3/` (2.8M), and `/tmp/arc2-l4r4-CR3` was removed. The instrument was extracted from the fenced block and hash-verified against its claimed digest:

```
$ sed -n '264,692p' .ufo/waves/arc2-loop1-round2/E22.md > c1-census-v9.py
$ wc -l c1-census-v9.py; sha256sum c1-census-v9.py
429 c1-census-v9.py
213fe679838ea217f4d34aa7d0e85bf73845a42ae49b68c9d8d52b4d38e6707c  c1-census-v9.py
```

Byte-identical to the digest recorded at `.ufo/waves/arc2-loop1-round2/E22.md:698`. Script line numbers below map to report lines as `+263` (fence at `:263`, code starts `:264`): script `:103` → report `:366` (the SCOPE table's last SCORECARD row).

### 2.1 Round-2's PASS reproduces; the FAIL appears at round-2's own records commit

Trees materialized with `git show <rev>:<file>` (no checkout, no worktree mutation). Full sweep, v9 verbatim:

```
$ for c in 165057e b3cd790 b21c0da 679af5d fd30b9c dbba2dd 158a966 1692acb; do … python3 c1-census-v9.py --root t-$c --quiet; done
t-165057e     rc=1  VERDICT: FAIL  (stale=5 ambiguous=1 undeclared=0 unresolved=0)
t-b3cd790     rc=0  VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
tree-b21c0da  rc=0  VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
t-679af5d     rc=1  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)
t-fd30b9c     rc=1  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)
t-dbba2dd     rc=1  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)
t-158a966     rc=1  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)
t-1692acb     rc=1  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)
```

The `165057e` line is an independent reproduction of round-2's recorded baseline (`stale=5 ambiguous=1`, `E22.md:244-249`). The PASS→FAIL transition is between `b21c0da` (round-2 work) and `679af5d` (round-2 records). **Causal isolation** — truncate the appended section out of the records tree:

```
$ cp -r t-679af5d caus-702 && head -702 t-679af5d/SCORECARD.md > caus-702/SCORECARD.md
$ wc -l caus-702/SCORECARD.md
702 caus-702/SCORECARD.md
$ python3 c1-census-v9.py --root caus-702 --quiet | grep VERDICT
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Round-2's records commit added exactly the section `703-766` (`git show 679af5d -- SCORECARD.md` hunks: `@@ -618,7 +618,7 @@`, `@@ -699,3 +699,68 @@`); removing it restores PASS. Round-3 and round-4 inherit the red state; neither caused it.

### 2.2 The re-key is NOT a disposition-neutral line remap

The minimal re-key is one appended row — verified additive by diffing the two SCOPE tables:

```
$ diff <(sed -n '/^SCOPE = \[/,/^\]/p' c1-census-v9.py) <(sed -n '/^SCOPE = \[/,/^\]/p' c1-census-rekey.py)
19a20,21
>     ("SCORECARD.md", 703, 766, "DATED", 703, r"2026-10-18"),
>     ("SCORECARD.md", 768, 854, "DATED", 768, r"2026-10-18"),
```

Per-assert disposition delta, v9 → re-key, on the HEAD tree (same 15 asserts both sides):

```
SCORECARD.md:731  6.7.0  v9=('undeclared','AMBIGUOUS')   rekey=('current_ok','current-ok')
SCORECARD.md:733  6.7.0  v9=('undeclared','current-ok')  rekey=('current_ok','current-ok')
SCORECARD.md:734  6.5.0  v9=('undeclared','AMBIGUOUS')   rekey=('current_ok','current-ok')
SCORECARD.md:736  6.5.0  v9=('undeclared','AMBIGUOUS')   rekey=('current_ok','current-ok')
SCORECARD.md:737  6.7.0  v9=('undeclared','AMBIGUOUS')   rekey=('current_ok','current-ok')
SCORECARD.md:752  6.7.0  v9=('undeclared','current-ok')  rekey=('current_ok','current-ok')
total asserts v9=15 rekey=15
```

**Inference (labeled):** four `AMBIGUOUS` dispositions — the instrument's G14 "refuse to guess" outcome — become `current_ok` with **no content change**. The re-key does not merely tell the census where to look; it decides the verdict for six loci. That is the precise sense in which it moves the goalpost, and it is measured, not argued.

### 2.3 The re-key alone does not reach PASS — a second landing is required

```
1) v9@HEAD     : :731 [bare] None=6.7.0 -> AMBIGUOUS (no client token in clause)
2) rekey@HEAD  : :731 [bare] None=6.7.0 -> current-ok (value equals a live anchor)
3) rekey G11   : G11 current-ok without receipt language: ['SCORECARD.md:731']
4) rekey+edit  : VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)     rc=0
```

Step 4's "edit" was a content change to **round-2's landed record** — inserting `receipt 2026-10-18T17:08:57Z` into the `:731` battery bullet (that timestamp is the real round-2 post-pair stamp, `receipts/config-post-pair.txt:1`). So C3's one-line description ("the E22 census scope-table re-key") understates the move by one landing. This is a **reproduction from a third seat** of `E16.md:315` and `E20.md:18`.

### 2.4 The open-ended bound disables the growth guard — the decisive refutation

E16/E20 recommend an open-ended row `("SCORECARD.md", 703, 9999, …)`. Measured against a simulated next-round append:

```
$ # grow-sim = HEAD tree + an appended "## arc2-loop1-round4" section citing REA 6.9.9
$ python3 c1-minimal.py --root grow-sim --quiet | grep VERDICT      # fixed bound 703,766
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)      rc=1
$ python3 c1-open.py --root grow-sim2 --quiet | grep VERDICT        # open-ended 703,9999
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      rc=0
```

Under the open-ended bound the fabricated `REA 6.9.9` in the later section is classified `historical (dated scope)` — silently trusted forever. Under the fixed bound the same fabrication raises `UNDECLARED`. `6.9.9` does not exist on this host (cache census: `6.7.0`, `6.5.0`, `6.4.0` only).

### 2.5 Laundering inside a declared DATED range — and why it is pre-existing, not re-key-introduced

```
$ # fabricate 6.9.9 inside the RE-KEYED round-2 range (:731)
$ python3 c1-census-rekey.py --root mut-stale --quiet | grep VERDICT
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      rc=0

$ # fabricate rea-agents@6.9.9 inside the ALREADY-LANDED round-1 range (:698), UNMODIFIED v9
BEFORE :698 = (live config now pins `rea-agents@6.7.0` at `config.toml:2940`, SC2-refuted);
AFTER  :698 = (live config now pins `rea-agents@6.9.9` at `config.toml:2940`, SC2-refuted);
$ python3 c1-census-v9.py --root mut-r1b --quiet | grep VERDICT
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      rc=0
```

**This is the honest framing of the "goalpost" question.** The instrument has *always* trusted DATED ranges absolutely — round-2's own table already trusts `635-701`, and a fabricated pin there passes today. The re-key does not create the trust; it **extends the trusted zone over the two blocks that discuss round-2's live battery and its current pins**. The goalpost move is therefore real but bounded: it is an extension of an existing exemption, not a new kind of exemption. The pre-existing precedent is why I do not call the re-key illegitimate in kind.

### 2.6 Non-regression: the re-keyed instrument still catches real staleness

```
$ python3 c1-census-v9.py  --root mut-prov-stale  → -- STALE (1) --  PROVINCE.md block 8-13 [scope CURRENT]   rc=1
$ python3 rk-p4.py         --root mut-prov-stale  → -- STALE (1) --  PROVINCE.md block 8-13 [scope CURRENT]   rc=1
$ python3 rk-p4.py         --root mut-sc59 --quiet | grep VERDICT
VERDICT: FAIL  (stale=1 ambiguous=0 undeclared=0 unresolved=0)      rc=1
```

Mutations: `PROVINCE.md:10` `rea-agents@6.7.0`→`@6.9.9`; `SCORECARD.md:59` `6.7.0`→`6.9.9`. The primary counter is intact under every re-key variant I built.

### 2.7 False PASS at `SCORECARD.md:57` — independent of any re-key

```
$ # b21c0da tree (the tree whose PASS round-2 recorded)
:57 =   receipted inventories (Devin/OMP 6.9.9 207/153, Kimi historical 6.4.0 170/127; both
      :57 [bare] devin=6.9.9 -> historical (inline marker)
      :57 [bare] omp=6.9.9 -> historical (inline marker)
      :57 [bare] kimi=6.4.0 -> historical (inline marker)
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      rc=0
```

Root cause is structural, not a bug in the mutation: `SCORECARD.md:57` carries the word `historical` **on the same physical line** as the Devin/OMP values, and G12's inline marker test is `INLINE_MARKER.search(lines[phys - 1])` — line-scoped by design. `SCORECARD.md:57` verbatim at HEAD: `  receipted inventories (Devin/OMP 6.5.0 207/153, Kimi historical 6.4.0 170/127; both`. Control: the same fabrication in a CURRENT range with no inline marker fires correctly — `PROVINCE.md:10` → `VERDICT: FAIL (stale=1 …)` rc=1.

### 2.8 Variant cost table

| instrument | change vs v9 | HEAD | `b21c0da` |
|---|---|---|---|
| `c1-census-v9.py` | — (frozen) | FAIL `undeclared=2` rc=1 | **PASS** rc=0 |
| `c1-minimal.py` | +1 row `703,766` | FAIL `undeclared=0`, G11@:731 rc=1 | FAIL (scope-error: marker beyond EOF) |
| `c1-census-rekey.py` | +2 rows `703,766` `768,854` | FAIL `undeclared=0`, G11@:731 rc=1 | FAIL (same scope-error) |
| `c1-open.py` | +1 row `703,9999` | FAIL G11@:731 rc=1 | FAIL (same) |
| `rk-p2.py` | re-key + G11 exempts all-DATED blocks | PASS rc=0 | FAIL |
| `rk-p4.py` | re-key + G11 accepts the section heading's date | PASS rc=0 | FAIL |
| `rk-p3.py` | re-key + G16 not applied inside DATED | PASS rc=0 | FAIL |
| `c1-minimal.py` + `:731` receipt phrase | +1 row + 1 content edit | **PASS** rc=0 | — |

Every variant that reaches PASS at HEAD does so by **relaxing a gate** (G11, G16) or by **editing a landed record** — none reaches PASS by measurement alone. The `b21c0da` FAILs in rows 2-4 are the marker-assertion working correctly (a row declaring `703` against a 701-line file is a genuine SCOPE-ERROR); they are not evidence against those variants.

### 2.9 `G11`'s precise semantics (why the second landing is required)

`RECEIPT = re.compile(r"2026-10-18|receipt|SHA-256|re-grepped", re.I)` and `g11 = (disp == "current-ok") and not RECEIPT.search(text)` where `text` is the **whole bullet block** (not the truncated `text[:170]` stored on the record). Re-running `units()`/`RECEIPT` directly over the two blocks:

```
block 686-701 len=1093 RECEIPT='receipt'
   ctx: 'ity improved (the r3/lesson records now match their evidence; custody receipts durable and tracked; SHONEN pointers r'
```

So `:686-701` escapes G11 because the word `receipts` appears late in its 1093-char block, while the `:731` block (469 chars) contains none of the four tokens. **This is not an unexplained asymmetry — the mechanism is the whole-block search extent, and my first check was wrong because I inspected the stored `text[:170]` field instead of the block `classify()` actually searches.** Consequence for the fix: a receipt phrase anywhere in the `:731-737` block satisfies G11, so the landing is one phrase, not a specific placement.

### 2.10 Custody, scope, and non-interference

```
$ tail -n +2 .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
```

5/5 verified before my legs (receipt stamp `2026-10-18T19:03:02Z`). `git status --porcelain` shows only `?? .ufo/waves/arc2-loop1-round4/*` — no tracked file modified, no untracked file outside this round's wave dir, no write to any custody path, no `/tmp` residue of mine left behind.

## 3. Text for the parent to land VERBATIM

### Block A — the C3 claim statement, corrected to its measured cost

```text
C3 freshness (fleet): the E22 v9 census scope table (sha256 213fe679…, 429 lines)
is re-keyed to cover the round-2 and round-3 record sections, as a FIXED bound:
  ("SCORECARD.md", 703, 766, "DATED", 703, r"2026-10-18"),
  ("SCORECARD.md", 768, 854, "DATED", 768, r"2026-10-18"),
plus a receipt-language phrase in the SCORECARD.md:731-737 battery bullet
(the 2026-10-18T17:08:57Z post-pair stamp). TWO landings, both load-bearing:
the scope rows alone leave G11 red at SCORECARD.md:731; the receipt phrase
alone leaves undeclared=2. Together the census reports PASS (0/0/0/0) rc=0 at
the work commit.
Do NOT use an open-ended bound (703, 9999): measured, it permanently disables
the UNDECLARED growth guard — a later section citing a non-existent version
returns PASS rc=0 under 703,9999 where it returns FAIL undeclared=1 rc=1
under 703,766. The fixed bound re-breaks once per round by construction; the
one-line re-key is a named recurring obligation, not a defect.
Cost, stated so it is not discovered later: the re-key is not a line remap.
It moves 6 assertions at HEAD from undeclared/AMBIGUOUS into current_ok by
declaration — 4 of them out of AMBIGUOUS, the instrument's own G14
refuse-to-guess outcome. Round-2's recorded PASS is NOT affected: it
reproduces byte-exactly at b21c0da (rc=0), and the FAIL originates in
round-2's own records append (causally isolated: truncating the appended
section restores PASS).
```

### Block B — named defect for the record (pre-existing, not re-key-introduced)

```text
Named census defect (arc2-loop1-round4, CR3, measured): E22 v9 G12
false PASS at SCORECARD.md:57. The line reads
  "receipted inventories (Devin/OMP 6.5.0 207/153, Kimi historical 6.4.0 170/127; both"
so the token "historical" is on the SAME physical line as the Devin/OMP
values, and INLINE_MARKER.search(lines[phys-1]) marks them historical.
Mutating 6.5.0 -> 6.9.9 (no such cache on host) yields VERDICT: PASS rc=0 on
the b21c0da tree. Control: the same fabrication in a CURRENT range without an
inline marker fires correctly (PROVINCE.md:10 -> FAIL stale=1 rc=1).
This does NOT refute C1's Kimi-scoped claim; it refutes reading the
instrument as a general guard. The class is pre-existing and orthogonal to
the re-key. Also measured: DATED ranges are trusted absolutely — fabricating
rea-agents@6.9.9 inside the ALREADY-LANDED round-1 range (:698) passes under
the unmodified v9, so the re-key extends an existing exemption rather than
creating one.
```

### Block C — scope-table rows, as literal text to append

```python
    ("SCORECARD.md", 703, 766, "DATED", 703, r"2026-10-18"),
    ("SCORECARD.md", 768, 854, "DATED", 768, r"2026-10-18"),
```

## 4. Conclusions, labeled

**Observations** (run or read this session):

1. The v9 instrument extracts byte-exactly to `213fe679…`, 429 lines, from `.ufo/waves/arc2-loop1-round2/E22.md:264-692`.
2. `b21c0da` → PASS rc=0; `165057e` → FAIL `stale=5 ambiguous=1` rc=1; `679af5d` and every later commit → FAIL `undeclared=2` rc=1. Both HEADs (`158a966`, `1692acb`) give identical results; the three census files are byte-identical between them.
3. Truncating the round-2 records section out of the 766-line tree restores PASS rc=0 (§2.1).
4. The minimal re-key is a 1-2 row append and changes 6 assertion dispositions, 4 of them from `AMBIGUOUS` (§2.2).
5. The re-key alone leaves `G11: ['SCORECARD.md:731']`; re-key + a receipt phrase in round-2's own record → PASS rc=0 (§2.3).
6. Open-ended `703,9999` + a later append citing `6.9.9` → PASS rc=0; fixed `703,766` + the same append → FAIL `undeclared=1` rc=1 (§2.4).
7. Fabricating `6.9.9` inside the re-keyed round-2 range → PASS rc=0; fabricating `rea-agents@6.9.9` inside the already-landed round-1 range under unmodified v9 → PASS rc=0 (§2.5).
8. The re-keyed variants still catch CURRENT-range staleness (PROVINCE:10, SCORECARD:59 → rc=1) (§2.6).
9. `SCORECARD.md:57` mutation → PASS rc=0 on the `b21c0da` tree, with `devin`/`omp` classified `historical (inline marker)` (§2.7).
10. Round-4 pre-pair receipt verifies 5/5; `git status` clean apart from this round's wave dir (§2.10).

**Inferences** (from those observations):

1. Round-2 did not overclaim. Its PASS was scoped to the work tree in both the SCORECARD and the LOG, and it reproduces. The red state is round-2's records append breaking its own instrument — the `UNDECLARED` guard firing exactly as designed (`E22.md:216`), which is the guard working, not failing.
2. The re-key is legitimate in kind because the target blocks are round records under dated headings, the same class the instrument already assigns to `635-701`, and because DATED-range trust is a pre-existing property. It is not legitimate as a *neutral* operation: it decides 6 verdicts by declaration.
3. The open-ended bound is the one form that should be refused outright: it converts a per-round maintenance obligation into a permanent, silent exemption, and its effect is measured on a fabricated version.
4. The fixed bound plus the receipt phrase is the honest form — it reaches PASS, it keeps the growth guard alive, and its cost is a named one-line re-key per round.
5. C3's stated measurable ("census PASS at the work commit") is reachable, but the claim text understates the move by one landing. Landing the re-key alone and reporting PASS would be a false report.

**Unknowns:**

1. ~~Why `SCORECARD.md:686-701` …~~ **Resolved this session and removed** — the block contains `receipts` late in its 1093 chars; my first check read the truncated `text[:170]` field instead of the searched block (§2.9). No asymmetry remains.
2. Whether the parent intends the `:731` receipt phrase to be a content edit to a landed record or a supersession note; both reach PASS, but the freeze convention at `SCORECARD.md:266-267` is a parent call I did not resolve.
3. Whether the `:57` inline-marker false PASS is in scope for this round at all — it is a defect in a DATED-record-adjacent CURRENT bullet, and fixing it (giving the Devin/OMP values their own clause away from the word "historical", or scoping the inline marker to the clause rather than the line) is a change to a landed sentence.
4. I built a content-anchored scope resolver (date-carrying `## ` headings become DATED dynamically, no line numbers) as a candidate durable form. **It is NOT a drop-in and I do not recommend it as-is**: it lost the two undated-but-DATED ranges (`SCORECARD.md:619-620`, `## Capabilities` / `## Saturation`) and reported `undeclared=2` at those lines. The approach is feasible but unverified; my prototype regressed two ranges.

## 5. Reproduction

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=/var/tmp/arc2-l4r4-CR3; mkdir -p $W; cd $W
sed -n '264,692p' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc2-loop1-round2/E22.md > c1-census-v9.py
sha256sum c1-census-v9.py            # expect 213fe679838ea217f4d34aa7d0e85bf73845a42ae49b68c9d8d52b4d38e6707c
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
for c in 165057e b3cd790 b21c0da 679af5d fd30b9c dbba2dd 158a966 1692acb; do
  mkdir -p t-$c; for f in PROVINCE.md SKILL.md SCORECARD.md; do git -C $R show $c:$f > t-$c/$f; done
  printf '%-10s ' $c; python3 c1-census-v9.py --root t-$c --quiet | grep '^VERDICT'
done
cp c1-census-v9.py c1-minimal.py && python3 - <<'PY'
p="/var/tmp/arc2-l4r4-CR3/c1-minimal.py"; s=open(p).read()
s=s.replace('    ("SCORECARD.md", 635, 701, "DATED", 635, r"2026-10-18"),\n]',
            '    ("SCORECARD.md", 635, 701, "DATED", 635, r"2026-10-18"),\n    ("SCORECARD.md", 703, 766, "DATED", 703, r"2026-10-18"),\n]')
open(p,"w").write(s)
PY
python3 c1-minimal.py --root t-158a966 --quiet | grep -E 'G11|VERDICT'   # undeclared=0, G11@:731
```

Scratch inventory (`/var/tmp/arc2-l4r4-CR3/`, 2.8M): `c1-census-v9.py` (verbatim), `c1-minimal.py` (+1 row), `c1-census-rekey.py` (+2 rows), `c1-open.py` (open-ended), `rk-p2/p3/p4.py` (gate-relaxation variants), `c1-census-dyn.py` (content-anchored prototype, buggy), `t-<rev>/` × 8 materialized trees, `caus-702/`, and mutation trees `mut-stale`, `mut-current`, `mut-cur-nomark`, `mut-57-falsepass`, `mut-57-head`, `mut-r1b`, `mut-p1*`, `grow-sim`, `grow-sim2`, `rk-receipt`, `leak-head`, `nc-nodate`. `/tmp/arc2-l4r4-CR3` was created, quota-blocked, and removed. No repo file modified; no git mutation; no config read beyond hashes; no network command; the PE analyze process was not touched.
