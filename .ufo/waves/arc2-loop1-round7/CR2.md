# CR2 — attack C2: is rule #12 generic agent advice (the CR14 question, formally)?

**VERDICT: ATTACK SUSTAINED against rule #12 as dispatched.** The CR14
question is formally answerable — it decomposes into three checkable prongs
(§1) — and the dispatched one-liner ("long Ghidra analyze runs are
caller-independent systemd user services, never `--scope` (r4 teardown, r6
holds as evidence)") fails all three. The rule is landable only in the
coupled, bounded, cited form of §3: same-commit knowledge citations that
command A can resolve, the arc's sealed causal records, and no "never
`--scope`" absolutization. Baseline re-verified at HEAD: command A reads
`{"citation_resolved_rules": 11, "rule_blocks": 11, knowledge_files: 80,
mapped: 80, coverage 10.0, depth 10.0}`.

Axes: formal answerability (is the genericity test well-defined),
mechanical resolvability (command A), causal honesty (the two sealed
unit-death records), harmlessness (one write: this file).

Observed 2026-10-18T22:06:40Z. HEAD `995e6a0799c4dad26942de15bd9058fe7acb676d`.
Read-only except this file. `arc2-r7-pe` observed via `systemctl show` only;
no signal, no kill, no other live probe. Scratch: `/var/tmp/arc2-l7r7-CR2-scratch/`
(empty; no scratch was needed).

## 1. The CR14 question, formalized

The invariant bar is textual and partly mechanical. A queue-drain craft rule
is generic agent advice iff it fails any prong:

- **G1 — domain anchor** (`/home/vgpnk/Projects/shokunin/PROTOCOL.md:439-440`
  "Specialize, don't generalize: a shokunin's `SKILL.md` contains *cited,
  verifiable* knowledge of its domain — never generic agent advice";
  restated `/home/vgpnk/.kimi-code/skills/shokunin/SKILL.md:189-190`;
  admission `corpus/QUALITY.md:13` criterion 3 "Domain-specific — no
  generic agent advice"). The rule text must name this domain's concrete,
  verifiable objects — artifact digests, unit names, measured outcomes —
  not a prescription true of any agent on any host. CR14's operational
  probe: does it name an artifact / sha256 / evidence id / measured lane
  failure, or does it restate upstream documentation (`systemd-run(1)`)?
- **G2 — resolvable citation** (mechanical; command A,
  `SCORECARD.md:103-117`). A rule block is one `- **` bullet of
  `SKILL.md`'s `## Queue-drain craft` section (`:81`, next heading `:219`);
  its only valid citations match
  `corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?`
  (`SCORECARD.md:105`) and must resolve file+range at REV; `valid =
  bool(refs)` (`SCORECARD.md:109`) — a rule with zero `corpus/knowledge/`
  refs is unresolvable **by construction**. E21 recorded the consequence
  (`.ufo/waves/arc2-loop1-round1/E21.md:43`, V3): "a rule bounded only by
  SCORECARD/LOG citations would score … a depth regression."
- **G3 — causal honesty** (`corpus/QUALITY.md:15` observation/inference/
  unknown labels; CR14's OOM≠teardown ruling; E52's "Do not write 'proven'
  for that sentence"). The rule's stated evidence must be the story the
  journals support; a hypothesis stated as a finding fails.

## 2. Evidence

### 2.1 G2 fails today — mechanically, not rhetorically

```text
$ grep -rInE 'systemd-run|--scope|user service|Linger' corpus/knowledge/
(no matches)
$ grep -nE 'systemd|service|scope|Linger|caller|arc2-r6-pe|user manager' \
    corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md
(no matches; file is 21 lines)
```

All 80 knowledge files at HEAD (`git ls-tree -r --name-only HEAD --
corpus/knowledge | wc -l` → 80 via command A's `knowledge_files`) contain
**zero** lines stating the service-form facts. The only corpus home for
them is the not-yet-landed `corpus/lessons/2026-10-18-caller-independent-services.md`
(drafted by E52 §3.1; absent — `corpus/lessons/` holds 8 files, none by
that name; no README row either, `corpus/README.md:155-167`). **Lessons-dir
citations do not resolve**: command A's pattern is `corpus/knowledge/…`
only (`SCORECARD.md:105`). Therefore rule #12 cannot reach 12/12 today by
citing the lesson; it can only resolve by citing a knowledge entry that
lands in the same commit (C1's r7 entry is the only planned candidate —
and it is in-flight: the r7 big leg was still `active/running` at
22:06:40Z, §2.4).

### 2.2 G3 fails — the dispatched parenthetical contradicts both sealed records

- **"r4 teardown"**: round 4's scope died by **memcg OOM at its own cap
  with its launcher still alive** — `SCORECARD.md:894-901` ("OOM-killed
  itself at its own memory cap in 4m42s … the containment worked exactly as
  designed (kernel `CONSTRAINT_MEMCG`, one in-scope victim, zero bystander
  kills)"); journals re-read by round-6 seats (`arc2-loop1-round6/CR14.md:29-34`,
  `E52.md:35-45`: `exit.txt` written by the launcher in the same second ⇒
  caller alive; no `Stopping`/`Killing` line). No caller teardown ever
  occurred in this arc.
- **"r6 holds"**: the only **measured** r6 service, `arc2-r6-pe`, sealed a
  typed **refusal** in 7.554 s (`SCORECARD.md:1043-1052`) — a non-hold.
  The r6 HOLD was the **mid-rung** (17.7MB `agent-browser` PE), a different
  binary whose unit type was never examined (`E52.md:172-176`, "The
  separate mid-rung analyze … was not examined"; §4 unknowns). It is
  therefore not evidence about unit lifetime in either direction.
- Under its natural reading the parenthetical is false on both halves;
  under the charitable reading ("r4's teardown record + r6's holds as the
  evidence corpus") it carries zero unit-lifetime measurement. Either way
  G3 fails as worded.

### 2.3 G1 fails — "never `--scope`" is a man-page universal that inverts the arc's own verdict

The lifetime mechanism ("scope is a child of `systemd-run`; a service is
parented by the user manager") is an installed-man-page fact
(`/usr/share/man/man1/systemd-run.1.gz`, `/usr/share/man/man5/systemd.scope.5.gz`;
round-6 CR14/E52 read them) that no arc measurement exercised: **no caller
was ever killed on this host** (E52's standing unknown,
`E52.md:265-271`; CR14: "Unit type is an untested lifetime hypothesis",
`arc2-loop1-round6/CR14.md:75`). Worse, the arc's only measured scope run
(r4) is a **success story for the scope form's containment**
(`SCORECARD.md:894-898`); it failed at the memory wall, not the unit type.
So "never `--scope`" is (a) stronger than the adjudicated E52 text, which
is a bounded preference ("Prefer that form when the run must outlive the
dispatching turn", `E52.md:269-270`; standing rule 1 `E52.md:275-280`,
itself conditioned on `KillUserProcesses`/`Linger` recording), and (b)
ungrounded in any lane event. On the dispatched one-liner alone — no
artifact, no unit name, no envelope, no digest — it is exactly the slogan
CR14 sustained against (`arc2-loop1-round6/CR14.md:3,22`).

### 2.4 Baseline and live state (observations, read-only)

```text
$ git rev-parse HEAD
995e6a0799c4dad26942de15bd9058fe7acb676d          # r6 records commit on top of b910a33
$ command A (SCORECARD.md:93-123) with REV=HEAD
{"citation_resolved_rules": 11, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 80, "mapped": 80, "missing": [],
 "revision": "HEAD", "rule_blocks": 11}
$ systemctl --user show arc2-r7-pe -p Id -p Type -p FragmentPath -p ActiveState \
    -p SubState -p Result -p ExecMainStatus -p MemoryMax -p MemoryPeak \
    -p CollectMode -p KillMode      # 2026-10-18T22:06:40Z
Id=arc2-r7-pe.service  Type=simple  ActiveState=active  SubState=running
FragmentPath=/run/user/1000/systemd/transient/arc2-r7-pe.service
MemoryPeak=8130965504  MemoryMax=9663676416  CollectMode=inactive
KillMode=control-group        (loginctl: Linger=yes)
$ cd .ufo/waves/arc2-loop1-round7/receipts && tail -n +2 config-pre-pair.txt | sha256sum -c -
5× OK, rc=0        # custody 5/5 (not this seat's scope; verified read-only)
```

The service form is real on this host right now (a transient user service,
peak 8,130,965,504 of `MemoryMax=9,663,676,416` ≈ 84% of cap) — but note:
**the run is not sealed, so it is not yet citable evidence for any rule.**
The passing precedent for rule form is landed rule #11 (`SKILL.md:196-206`):
bounded to the arc's churn chain, citing `corpus/knowledge/…:938-950` with
resolvable ranges, token-free text (r4 close: `SCORECARD.md:867-870`,
"11/11 resolvable … token-free per E21"). Craft section bounds: `:81`–`:218`
(next heading `## Config custody for live-probe rounds (SOP)` at `:219`).

## 3. Verbatim-landable (conditional; parent lands, this seat does not edit)

**Precondition (coupling, Z1's r6 token shape):** land rule #12 only in the
same commit as the knowledge entry that carries its citations, and only if
that entry states the service-form facts; otherwise defer the rule. The two
`<R7-STEM>:N-M` placeholders must be filled from the entry's final line
numbers and must resolve at REV (command A). Text is token-free (no
`rea-agents@`, no bare `6.x.y`, no `config.toml:N`); "never `--scope`" and
"r4 teardown, r6 holds" are refused and do not appear.

```markdown
- **Unit type is a launch decision, not a result — bound it to the run that
  must outlive its dispatcher.** A named transient user service is parented
  by the user manager; a `--scope` run blocks inside the dispatcher's own
  process tree. This arc's sealed records: round 4's contained scope died
  at its own memory cap with its launcher still alive — never record that
  as a caller teardown; round 6's named service sealed a typed refusal in
  seconds under its cap — service mode is not a held analysis
  (`corpus/knowledge/<R7-STEM>.md:N-M`). Prefer the service form only when
  the analysis must outlive the dispatching turn, and record the host's
  `KillUserProcesses` and `Linger` with the recipe
  (`corpus/knowledge/<R7-STEM>.md:N-M`). Survival past an actual caller
  kill is untested on this host — keep it marked unknown.
```

For the round record (if the parent wants the attack's disposition as a
sentence; pin-free, census-safe under `:854` scope discipline):

```text
C2 depth — CR2 sustained the generic-advice attack on the dispatched rule-#12 one-liner (no artifact or measurement named; "never --scope" restates systemd-run(1) and inverts round 4's own containment verdict; "r4 teardown, r6 holds" contradicts the sealed OOM-with-launcher-alive and typed-refusal records). Rule #12 may land only coupled to a same-commit knowledge entry whose line ranges command A resolves; absent that entry it would land uncited and regress depth (command A: valid = bool(refs)).
```

## 4. Labels

**Observation:** command A at HEAD = 80/80, 11/11, 10.0/10.0 (re-run by this
seat); grep over all 80 knowledge files for systemd/`--scope`/user
service/Linger → no matches (incl. the 21-line midrung entry);
`corpus/lessons/` = 8 files, no caller-independent-services entry; README
lessons table `:155-167` has no such row; command A's citation pattern and
`valid = bool(refs)` at `SCORECARD.md:105,109`; craft section `:81-218`
with 11 `- **` rules, next heading `:219`; rule #11's landed cited form at
`SKILL.md:196-206`; r4 containment verdict `SCORECARD.md:894-901`; r6 big
leg 7.554 s typed refusal `SCORECARD.md:1043-1052`; r6 HELD was the
mid-rung binary with unit type unexamined (`E52.md:172-176`);
`arc2-r7-pe` active/running at 22:06:40Z, transient `Type=simple`,
`MemoryPeak=8130965504` / `MemoryMax=9663676416`; custody pre-pair 5/5
rc=0; invariant text at `PROTOCOL.md:439-440` (shokunin repo),
skills `SKILL.md:189-190`, `corpus/QUALITY.md:13`.

**Inference:** the CR14 question is formally decidable (G1/G2/G3); the
dispatched rule fails all three prongs; "never `--scope`" is stronger than
both the adjudicated E52 text and any arc measurement, and the arc's only
measured scope run supports the scope form's containment; rule #12 is
mechanically unlandable today (no resolvable knowledge citations exist)
and is coupled to C1's r7 entry the same way Z1 coupled tokens to their
knowledge file ("Do not land the token unless the knowledge file lands in
the same commit, otherwise command A dangles" — `arc2-loop1-round6/C2.md:96`).

**Unknown:** the r7 big leg's terminal state (in-flight at 22:06:40Z; this
seat did not wait on it or signal it); whether C1's entry lands HELD and
which line ranges it will carry; whether any sibling seat drafts a rule-#12
variant (wave dir held only the pre-pair receipt at check time); whether
the parent sequences rule #12 with C1 or defers it.
