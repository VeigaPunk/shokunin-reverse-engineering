# CR5 (critic) — attack on C1 census completeness

Seat CR5, wave arc2-loop1-round1, read-only. Every command below was run by
this seat this session at HEAD `4b806e14db22ea44cc57729f5fa3f7b46b616178`
(2026-10-18); scratch only under `/tmp/arc2-l1r1-CR5-sim/`. This report is my
only write; it wholly replaces an interrupted first attempt. No repo file was
modified (`git status --porcelain` → `?? .ufo/waves/arc2-loop1-round1/` only).

## 1. Verdict

**PARTIAL REFUTE — three parts.**

1. **The r3-file census itself is COMPLETE (verified, not assumed).** A wide
   safety-vocabulary sweep of `corpus/knowledge/2026-10-13-r3-jq-provenance.md`
   returns exactly the two loci `:60` and `:136`; the sweep's only extra hit
   (`:118`) is a substring false positive ("cleaned"). C1(a)'s file-scoped
   count N=2 is sound.
2. **The round-level phrasing "unqualified safety-label loci 2→0" OVERREACHES.**
   Two unqualified safety-sense "benign" labels on the *same jq verdict* sit in
   an **editable** corpus file — `corpus/README.md:90` and `corpus/README.md:160`
   — and are owned by **no debt ledger**. The single ledger pointer to `:160`
   (`SCORECARD.md:68`) describes *different content* (frontier staleness), and
   that described debt was in fact discharged at `7125dd4` — so the label on
   `:160` is unowned for a structural reason, not an oversight.
3. **The census instrument S2 proposes to land has two PROVEN failure modes
   plus an escape hatch.** I simulated it on scratch copies:
   - **case-sensitivity hole** — capitalizing `:60` to "Benign" makes the
     census report `n 0`: a silent **false PASS**;
   - **marker-gated hole** — a correct note that omits the literal
     `**Safety-verdict scope` marker makes the census count the note's own
     words: `n 3`, a **false FAIL** on a correct edit;
   - **post-marker escape hatch** — everything after the marker line is exempt
     by construction, so a *new* post-marker label is never counted;
   - **vocabulary hole** — the needle pair is `benign` +
     `malicious or accidental`, not a safety vocabulary; a new label phrased
     "safe, trustworthy, uncompromised" is invisible.
   The command is **not landed anywhere in the repo** (`git grep` for its
   distinctive `partition('**Safety-verdict scope'` string over non-`.ufo`
   tracked files → rc=1). It exists only as a proposal in `S2.md`; these
   defects would ship with it.

Frozen/editable partition and the verbatim block are in §4 and §6.

## 2. Evidence — exact commands with observed output

### 2.1 The r3-file census is complete (wide-vocabulary re-derivation)

```
$ grep -nEi 'benign|malicious|safe|trust|compromis|legit|endors|tamper|suspicious|clean|uncompromised|harmless|risk' corpus/knowledge/2026-10-13-r3-jq-provenance.md
60:  benign, intentional install: an agent-executed copy of the official
118:- `~/Downloads` → no jq archives; no `*jq*`/tool tarballs left in `/tmp`/`~/.cache` (agent cleaned staging dirs).
136:finding; no malicious or accidental pathway indicated. Residual Unknown
$ sed -n '118p' corpus/knowledge/2026-10-13-r3-jq-provenance.md | grep -o 'cleaned'
cleaned
$ wc -l corpus/knowledge/2026-10-13-r3-jq-provenance.md
137 corpus/knowledge/2026-10-13-r3-jq-provenance.md
```

Observation: the wide sweep adds nothing beyond `:60`,`:136`; `:118` is the
substring "cleaned" matching the `clean` needle — a false positive, not a
third locus. EOF is `:137` with no errata tail.

### 2.2 Fleet token census — the real attack surface

```
$ git grep -nE 'benign|malicious' -- . ':(exclude).ufo' | wc -l
17
$ git grep -niE 'benign|malicious' -- . ':(exclude).ufo' | cut -d: -f1 | sort | uniq -c
      1 corpus/knowledge/2026-10-13-crash-evidence.md
      5 corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md
      2 corpus/knowledge/2026-10-13-r3-jq-provenance.md
      1 corpus/knowledge/2026-10-14-r11-01-queue-ops.md
      1 corpus/lessons/2026-10-15-round-1.md
      2 corpus/README.md
      3 LOG.md
      1 PROVINCE.md
      1 SCORECARD.md
```

Per-locus classification (each read this session):

| Locus | Sense | Status | Editable? |
|---|---|---|---|
| `corpus/knowledge/2026-10-13-r3-jq-provenance.md:60` | asserts "benign, intentional install" | C1(a) target | **yes** |
| `corpus/knowledge/2026-10-13-r3-jq-provenance.md:136` | "no malicious … pathway indicated" | C1(a) target | **yes** |
| `corpus/README.md:90` | asserts "byte-identical upstream jq-1.8.2 release — benign" | **unowned, editable** | **yes** |
| `corpus/README.md:160` | asserts "shadow-binary verdict benign" | **unowned, editable** | **yes** |
| `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:217,236-237,12` | historical labels | qualified by `:244` (landed r9) | yes |
| `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:219,41` | negations ("not binary compromise", "not a recompiled trojan") | not asserting | yes |
| `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244` | the qualification note itself | qualifying text | yes |
| `corpus/lessons/2026-10-15-round-1.md:150` | inside its own correction-debt sentence | self-qualified | yes |
| `LOG.md:21` | **asserts** "verified byte-identical to upstream jq-1.8.2 release — benign" | **frozen history** | **NO** |
| `LOG.md:476` | names the bleed ("historical 'benign payload' scope bleed") | debt-naming, not asserting | NO |
| `LOG.md:870` | records the qualification ("naming all four 'benign' loci") | meta-record, not asserting | NO |
| `SCORECARD.md:78` | names the r2 loci as correction debt | debt-naming | frozen section |
| `PROVINCE.md:102` | **refusal-sense** ("does not … label samples malicious/benign") | not a locus | yes (not a target) |
| `corpus/knowledge/2026-10-13-crash-evidence.md:36` | journal-noise characterization ("benign TDX/snapper/keyring lines") | not artifact safety | yes |
| `corpus/knowledge/2026-10-14-r11-01-queue-ops.md:383` | telemetry-size characterization ("telemetry (benign)") | not artifact safety | yes |

```
$ sed -n '90p' corpus/README.md
| `2026-10-13-r2-jq-shadow-verdict` | `~/.local/bin/jq` = byte-identical upstream jq-1.8.2 release — benign | rea analyze + upstream sha256 match | 2026-10-13 |
$ sed -n '160p' corpus/README.md
| `2026-10-13-round-2` | 2 | r1 survives audit (1 erratum); catalog≠provider≠held; doctor aux-blind; 32MiB crash cap; MCP-session-scoped ev_ids; shadow-binary verdict benign |
$ sed -n '17,23p' LOG.md
  admit/reject verdicts upheld; 1 factual erratum (34 Ghidra features), 2
  verify-command defects, criterion-5 labeling gap recorded. Promoted to Core:
  PE-via-Ghidra (proven e2e), cross-version compare machinery, crash-inspect
  mechanism (32 MiB cap found). Headline: `~/.local/bin/jq` verified
  byte-identical to upstream jq-1.8.2 release — benign. Firmware blocked on
  `REA_BINWALK_COMMAND`; AnyCPU managed still rejected; ev_-id session scoping
  and +0x100000 .so rebase rules learned.
$ grep -ciE 'benign|malicious' README.md SHONEN.md MINT.md AGENTS.md EXAMPLE.kama.md SKILL.md corpus/QUALITY.md
README.md:0  SHONEN.md:0  MINT.md:0  AGENTS.md:0  EXAMPLE.kama.md:0  SKILL.md:0  corpus/QUALITY.md:0
```

Observation: `README.md` (root), `SKILL.md`, `SHONEN.md`, `MINT.md`,
`AGENTS.md`, `EXAMPLE.kama.md`, `corpus/QUALITY.md` carry **zero** hits. The
only root-file hit outside LOG/SCORECARD/PROVINCE is none. So the miss surface
is exactly: `corpus/README.md:90,:160` (editable, unowned) and `LOG.md:21`
(frozen).

### 2.3 README is editable — repair precedent, and the label is unowned

```
$ git log --oneline -6 -- corpus/README.md
18dc397 luna-round-8: operability symmetry battery — 6.4.0 entry (78->79) + receipts tracked; 10/10 frozen predictions
3395b6d luna-round-7: coverage — 12 README rows (6 map + 6 Knowledge) for the six 6.5.0-verb entries
7125dd4 luna-round-5: freshness — ... + 2 README repairs
6a71cd5 luna-round-4: freshness debt-drain — 14 repair groups across map/Known-gaps rows (19-finding census target), token set 72 held
$ git show 7125dd4 --stat -- corpus/README.md
 corpus/README.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
$ grep -rn 'README' SCORECARD.md | grep -E ':90|:160'
68:- **Other stale summaries:** `corpus/README.md:160` still lists already-held
```

Observation: `corpus/README.md` is a routinely **edited** index (luna-round-4,
-5, -7, -8 all landed row repairs). No `frozen`/`untouchable`/`byte-identical`
marker attaches to it anywhere in SCORECARD.md (grep for those words beside
`README` → empty). The one ledger mention of `:160` is `SCORECARD.md:68`,
which is about *frontier* staleness, **not** the safety label.

### 2.4 `SCORECARD.md:68`'s `:160` pointer no longer resolves to its described content

```
$ sed -n '68,70p' SCORECARD.md
- **Other stale summaries:** `corpus/README.md:160` still lists already-held
  process/managed/call-target operations as frontier; `:128` says four r13
  nits fixed although `LOG.md:395-401` corrects integration fixes to two.
  (Pointer corrected from the drifted `:157` during luna-round-4 record hygiene; content debt for a future freshness round.)
$ sed -n '160p' corpus/README.md    # at HEAD
| `2026-10-13-round-2` | 2 | r1 survives audit (1 erratum); ...; shadow-binary verdict benign |
$ grep -n 'Runtime-obs' corpus/README.md
177:- Runtime-obs depth — call-target resolution, managed `verify`/`project`, and the process-capture pair are held, not frontier (r5-02, r9-02, r11-01); ...
$ git show 7125dd4 -- corpus/README.md | grep -E '^[-+]- Runtime-obs'
-- Runtime-obs extended: process-capture, managed `verify`/`project` ops, native call-target resolution (per r4-16 rescan: ~26 self-provisionable).
+- Runtime-obs depth — call-target resolution, managed `verify`/`project`, and the process-capture pair are held, not frontier (r5-02, r9-02, r11-01); ...
```

Observation (two independent drifts, both provable):
- **Line drift:** at HEAD the frontier bullet is `:177`, not `:160`; `:160` is
  the round-2 *lessons* row. At luna-round-4 (`6a71cd5`) the bullet was `:163`
  — so `:160` was already off by 3 when last "corrected". README grew
  173 → 185 → 187 lines across luna-round-5/-7/-8.
- **Content discharge:** the staleness `:68` names was in fact **repaired at
  `7125dd4`** ("held, not frontier"), so the debt it names is stale-discharged
  and unmarked. Adjudication (re-correct vs NO-CHANGE-with-cause) is a parent
  call: `LOG.md:884` names only `:79` as frozen/untouchable, not `:68`.

### 2.5 Census-instrument simulation (my namespace, repo untouched)

Command under test — S2's proposed C1a census, reproduced verbatim from
`S2.md:19`:

```
$ python3 -c "import re;t=open(F).read();h,_,n=t.partition('**Safety-verdict scope');L=[i+1 for i,l in enumerate(h.splitlines()) if 'benign' in l or 'malicious or accidental' in l];N=set();[N.update(range(int(a),int(b)+1) if b else [int(a)]) for a,b in re.findall(r':(\d+)(?:-(\d+))?',n)];U=[x for x in L if x not in N];print('loci',L,'unscoped',U,'n',len(U))"
```

| # | Scratch variant (in `/tmp/arc2-l1r1-CR5-sim/`) | Output | Assessment |
|---|---|---|---|
| 0 | unmodified base (`base.md`) | `loci [60, 136] unscoped [60, 136] n 2` | matches S2/E21/V1 — baseline sound |
| A | `sed '60s/benign/Benign/'` | `loci [136] unscoped [136] n 1`; `grep -c 'benign'` → `0` | **false PASS risk** — a capitalized label escapes entirely |
| B | correct note, no literal marker (`## Safety scope note (…)`) | `loci [60, 136, 141] unscoped [60, 136, 141] n 3` | **false FAIL** — note's own words counted as loci |
| C | note **with** marker `- **Safety-verdict scope (…)**` | `loci [60, 136] unscoped [] n 0` | required form works |
| D | marker + quoted phrases on separate lines | `n 0` | range expansion tolerant |
| E | r2-style single-line note (style template form) | `n 0` | template form works |
| F | marker present, **no** range naming | `loci [60, 136] unscoped [60, 136] n 2` | naming the loci is load-bearing |
| G | new mid-file label "safe to use" at `:64` | `loci [60, 137] unscoped [60, 137] n 2` | caught only **incidentally** (line-number shift), not by vocabulary |
| H | marker note **+** new post-marker label "safe to use" | `n 0` while `grep -nEi 'safe\|trust'` finds `:139,:141` | **escape hatch**: post-marker text is exempt by construction |
| I | new EOF label "safe, trustworthy, and uncompromised" at `:139` | `loci [60, 136] unscoped [60, 136] n 2` — **unchanged** | **vocabulary hole**: non-needle safety words invisible |
| J | new EOF label "the artifact is benign." at `:139` | `loci [60, 136, 139] unscoped [60, 136, 139] n 3` | needle-word label *is* caught |

```
$ git grep -ln 'Safety-verdict scope.*partition\|partition.*Safety-verdict' -- . ':(exclude).ufo'
rc=1
```

Observation: the census command is **not landed** in any tracked non-`.ufo`
file — it lives only in `S2.md`'s proposed Block A table. Its defects would
ship with it. **Mitigation is cheap and in scope:** make the needle
case-insensitive (`'benign' in l.lower()`), and assert the *marker's presence*
before trusting `n 0` (variants A/H both report a clean `n 0` while a
safety-sense label stands in the file).

### 2.6 `S2.md` Block C mislabels two pointers it tells the parent to land

```
$ grep -nE 'benign|malicious' corpus/knowledge/2026-10-13-r3-runtime-observation.md ; echo rc=$?
rc=1
$ grep -nE 'benign|malicious' corpus/knowledge/2026-10-13-r4-05-signal-asar.md ; echo rc=$?
rc=1
$ sed -n '128p' corpus/knowledge/2026-10-13-r3-runtime-observation.md
   `--ozone-platform=headless` + omarchy default flags; harmless.)
$ sed -n '57,58p' .ufo/waves/arc2-loop1-round1/V1.md
corpus/knowledge/2026-10-13-r3-runtime-observation.md:128 ["harmless.)" — ozone flag]
corpus/knowledge/2026-10-13-r4-05-signal-asar.md:81    ["harmless (transient window...)" — dangling-specifier note]
```

Observation: `S2.md:129` (Block C — *verbatim block for the parent*) lists
`r3-runtime-observation.md:128` and `r4-05-signal-asar.md:81` as matches of the
`git grep -n -i -E "benign|malicious"` census. They are **not** matches of that
command (rc=1 both). They are `V1.md`'s *different* Population-B vocabulary
(`harmless`). The pointers themselves resolve (`V1.md:57-58`); the **label**
"matches of this command" is false as written. The other four names in Block C
(`README.md:90,:160`; `crash-evidence.md:36`; `r11-01-queue-ops.md:383`;
`LOG.md:21`) I re-ran and all **do** match.

### 2.7 Stale-pointer family — four instances, not two

```
$ git grep -n '107-109' -- . ':(exclude).ufo'
LOG.md:884:  (:60,:136); stale :107-109 refusal pointers at SCORECARD.md:79 (frozen
SCORECARD.md:79:  while `PROVINCE.md:107-109` refuses safety/trust verdicts. Provenance evidence
corpus/lessons/2026-10-15-round-1.md:152:the safety/trust boundary at `PROVINCE.md:107-109`; it remains correction debt,
$ sed -n '12p' SHONEN.md
  asserted boundary only: `PROVINCE.md:88-109`; province-version alignment is contested by the 6.5.0/207/v42 observations in `corpus/lessons/2026-10-15-round-1.md`; no promotion or complete accuracy claimed.
$ sed -n '114p' PROVINCE.md
- **Quality/safety verdicts on findings** — the lane answers "what does this
$ git show 6645585873c4e66372b15687c47000abf8d91978:PROVINCE.md | sed -n '105,112p'
  **operator-owned**. The lane documents the gap and the exact env key; it
  never runs the installer.
- **Quality/safety verdicts on findings** — the lane answers "what does this
  shipped artifact do, per evidence id X" — never "is it safe, trustworthy, or
  licensed for reuse" `(unowned)`.
```

Observation: the family has a **fourth** member — `SHONEN.md:12` asserts its
boundary as the range `PROVINCE.md:88-109`, which **excludes** the refusal at
`:114-116` (`:109` is "never runs the installer.", the bullet ends `:116`).
Also confirmed: the lessons pointer `:152` was **baseline-accurate** at
`6645585…` (refusal was `:107-109` then) and is stale only at current HEAD — so
the C1(b) correction note must say "baseline-accurate, stale at HEAD", not
"wrong when written" (agrees with `S2.md:139-141`). `S2.md:151-152` already
flags the SHONEN instance for a parent include/defer call; I confirm it
independently and add that its range form means the C1(b) repair does **not**
reach it.

## 3. Conclusions, labeled

**Observations** (ran/read this session): everything in §2 — the wide r3 sweep
and `:118` FP; the 17-locus non-`.ufo` token census with per-file counts; the
zero-hit files; the README edit history and absence of any freeze marker; the
two `SCORECARD.md:68` drifts; all ten simulation variants; the `rc=1` on the
landed-census grep; the two Block C non-matches; the four-instance stale-pointer
family and both-revision PROVINCE check.

**Inferences** (from those observations):

1. C1(a)'s **file-scoped** count (N=2 → 0) is defensible and complete. The
   claim's **unscoped fleet phrasing** is not — it must ship with a scope
   sentence (Block C, repaired) or be widened.
2. `corpus/README.md:90,:160` are the only **editable, unowned** siblings the
   census misses. They are the strongest available counterexample to "2→0".
3. `LOG.md:21` is the only **frozen** locus that *asserts* a safety class
   (`:476`/`:870` name debt and record the qualification; they do not assert).
   It cannot be edited; it needs an explicit scope-out, not silence.
4. The census instrument is un-landed and carries two false-verdict modes.
   Landing it unchanged converts C1's acceptance test into a coin-flip on
   drafter wording.
5. `S2.md`'s Block C is the parent's intended landing text and contains a
   demonstrably false pointer-label; landing it verbatim propagates the error.

**Unknowns:**

1. Which census definition the parent freezes for C1 (file-scoped N=2 +
   scope sentence vs widened to include README) — `E23.md:193` also defers this
   (line re-verified after E23 rewrote its file mid-wave; the earlier draft's
   `:86` citation no longer resolves to that text).
2. Whether `SCORECARD.md:68` is inside the frozen 2026-10-15 reconciliation
   scope. `LOG.md:884` names only `:79`; `:68` sits in "Open gaps —
   deliberately not closed by this move" (`:51-84`) and has been *maintained*
   once already (":157 → :160").
3. Whether the parent will land a post-pair receipt and the C3 rule-10 draft
   (no such artifacts existed at my read time; `ls receipts/` →
   `config-pre-pair.txt` only).

## 4. Frozen vs editable — the partition the census must respect

**Editable — census targets (append-only for knowledge/lessons):**

- `corpus/knowledge/*.md` (incl. `2026-10-13-r3-jq-provenance.md` — C1(a))
- `corpus/lessons/*.md` (incl. `2026-10-15-round-1.md` — C1(b))
- `corpus/README.md` — editable index, **repair precedent exists** (7125dd4,
  3395b6d, 18dc397); carries the two unowned labels at `:90`,`:160`
- `corpus/QUALITY.md`, root `README.md`, `MINT.md`, `AGENTS.md`,
  `EXAMPLE.kama.md` — zero hits, not targets

**Frozen / must NOT be edited:**

- `LOG.md` entries — append-only history; `:21` asserts the label, `:476`/`:870`
  are records. New scope-out text goes in a **new** LOG entry.
- `SCORECARD.md:79` — frozen reconciliation table (LOG.md:884 "untouchable");
  NO-CHANGE-with-cause. `:68` is ambiguous (Unknown 2).
- Prior-round `.ufo/waves/*` and `.ufo/reports/*` artifacts — 135 tracked
  token-matching lines live under `.ufo/`, including
  `.ufo/reports/luna-round-9/kaidoku.md:53`. Read-only records.
- `evidence/round-1-2026-10-15/*` — `grep -cE 'benign|malicious'` on
  `rubric.json` → `0`; not a target.

**Special case:** `corpus/lessons/2026-10-15-round-1.md:150` — the token sits
inside its own correction-debt sentence, so it is self-qualified; it is *also*
C1(b)'s append target, so it needs no separate disposition.

## 5. Answers to the seat's three questions

- **Which sibling files could the census miss?** Exactly two classes: (a)
  `corpus/README.md:90,:160` — editable, unowned, same verdict as C1(a)'s file;
  (b) `LOG.md:21` — frozen, asserting, uneditable. Nothing else in
  `SKILL.md`, `PROVINCE.md`, root `README.md`, `SHONEN.md`, `MINT.md`,
  `AGENTS.md`, `EXAMPLE.kama.md`, `corpus/QUALITY.md` matches.
- **Refusal-sense false leads:** `PROVINCE.md:102` and `SKILL.md:240` use the
  words to *refuse* triage — they are the rule that makes the labels
  problematic, not loci. `crash-evidence.md:36` and `r11-01:383` are
  non-safety-sense characterizations.
- **What must NOT be edited:** `LOG.md` (any entry), `SCORECARD.md:79` (frozen
  table), prior-round `.ufo/` artifacts, `evidence/`. C1(b)'s own append goes
  at EOF of the lessons file, never into its historical body — the stale
  `:152` pointer **stays**.

## 6. Verbatim block for the parent (land as-is if used)

```text
C1 census definition (frozen for this round) — scoped, with instrument fixes:

Scope: "unqualified safety-label loci" means artifact-verdict safety labels in
EDITABLE corpus files. Under this definition the count is 2 -> 0
(corpus/knowledge/2026-10-13-r3-jq-provenance.md:60 "benign, intentional
install"; :136 "no malicious or accidental pathway indicated"), qualified by an
append-only byte-identity + recorded-provenance, non-endorsement note.

Explicit scope-outs (named, not counted, not edited):
- corpus/README.md:90 and :160 — unqualified "benign" labels on the same jq
  verdict, in an EDITABLE file, owned by NO debt ledger (SCORECARD.md:68's
  ":160" pointer describes frontier staleness, not this label, and that debt
  was discharged at 7125dd4). Deferred with cause: README label qualification
  is a separate freshness item.
- LOG.md:21 — the same label inside a FROZEN append-only historical entry;
  cannot be edited. Non-endorsement is recorded only by new append-only text
  (this round's LOG entry), never by rewriting history.
- Non-loci (non-safety-sense uses): corpus/knowledge/2026-10-13-crash-evidence.md:36
  (journal noise); corpus/knowledge/2026-10-14-r11-01-queue-ops.md:383
  (telemetry size).
- Refusal-sense uses that are the RULE, not loci: PROVINCE.md:102; SKILL.md:240.

Census instrument (if landed, fix first): make the needle case-insensitive and
assert the literal marker `**Safety-verdict scope` is present before trusting
n=0. Proven defects at HEAD: (i) "Benign" at :60 escapes entirely (n 0 while a
label stands); (ii) a correct note without the literal marker yields n 3
(false FAIL); (iii) post-marker text is exempt by construction (a new label
after the marker is never counted); (iv) the needle pair is not a safety
vocabulary — a new label phrased "safe, trustworthy, uncompromised" is
invisible (variant I: n unchanged at 2).

Stale-pointer family (four instances, one landing decision each):
- corpus/lessons/2026-10-15-round-1.md:152 — C1(b) target; baseline-accurate
  at 6645585…, stale at HEAD; refusal now PROVINCE.md:114-116.
- SCORECARD.md:79 — NO-CHANGE-with-cause (frozen table, LOG.md:884).
- SHONEN.md:12 — range `PROVINCE.md:88-109` excludes the refusal at :114-116;
  include-or-defer is a parent call (S2.md:151-152).
- SCORECARD.md:68 — ":160" no longer resolves to its described content (bullet
  moved to :177; the named staleness was discharged at 7125dd4). Re-correct or
  NO-CHANGE-with-cause; LOG.md:884 freezes only :79, not :68.

S2.md Block C repair (do NOT land as written): r3-runtime-observation.md:128
and r4-05-signal-asar.md:81 do NOT match the "benign|malicious" census command
(rc=1 both); they are V1's Population-B ("harmless") hits. Keep them only if
relabeled as Population-B, or drop them.
```

## 7. Reproduction commands

```bash
git rev-parse HEAD; git status --porcelain
grep -nEi 'benign|malicious|safe|trust|compromis|legit|endors|tamper|suspicious|clean|uncompromised|harmless|risk' corpus/knowledge/2026-10-13-r3-jq-provenance.md
git grep -niE 'benign|malicious' -- . ':(exclude).ufo' | cut -d: -f1 | sort | uniq -c
git grep -n '107-109' -- . ':(exclude).ufo'
sed -n '68,70p;76,82p' SCORECARD.md; sed -n '12p' SHONEN.md
git show 7125dd4 -- corpus/README.md | grep -E '^[-+]- Runtime-obs'
git show 6645585873c4e66372b15687c47000abf8d91978:PROVINCE.md | sed -n '105,112p'
# simulations (scratch only):
mkdir -p /tmp/arc2-l1r1-CR5-sim && cp corpus/knowledge/2026-10-13-r3-jq-provenance.md /tmp/arc2-l1r1-CR5-sim/base.md
#   then variants A–J per §2.5 (census one-liner from S2.md:19)
```

## 8. Convergence note (read after landing)

The wave kept growing while I wrote; I re-checked my claims against the seats
that landed after me rather than leaving them unqualified.

- **Corroborated (not novel):** the `corpus/README.md:90,:160` and `LOG.md:21`
  gaps are now independently named by `C2.md:19-20` ("Two further UNQUALIFIED
  artifact-safety `benign` labels exist at `corpus/README.md:90` and `:160` —
  outside C1's stated file scope … and outside every other seat's sweep"),
  `R1.md:171-175` (R4/R5 observations), `S1.md:128,293`, and `Z2.md:145`. C2
  reached the same README conclusion on an independent 4-term instrument.
- **Unique to CR5:** (a) the `SCORECARD.md:68` pointer drift and
  stale-discharge (§2.4) — no other seat's report mentions `:68`; (b) the
  ten-variant census-instrument simulation (§2.5). E1/R1/V1 use
  case-insensitive greps of their own, but none demonstrated that the *proposed
  landed* census command has a false-PASS and a false-FAIL mode.
- **Also unique:** the `S2.md` Block C pointer mislabel (§2.6). `S2.md:120`
  itself credits the scope sentence to "CR5.md:127-135" (the interrupted
  draft); the repair in §6 is the corrected form.
- **Repo state at my final check:** HEAD `4b806e14` unchanged;
  `git status --porcelain` → `?? .ufo/waves/arc2-loop1-round1/` only; r3 file
  still 137 lines with no errata tail, so **no C1 edit had landed** when I
  finished and every before-state above still describes HEAD.
- **Two seat reports were rewritten mid-wave** (E23 at 13:43). Any pointer I
  give into another seat's file was re-verified at my write time; treat
  cross-seat line pointers as movable.

