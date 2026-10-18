# CR7 (critic) — attack: smuggled exploratory claims (unprovable-but-better shapes lacking a named non-author reviewer)

Seat CR7, wave arc2-loop1-round1, 2026-10-18. Read-only over the repo; this
report is the seat's only write. Snapshot: **2026-10-18T16:45:02Z**, final
census re-run **16:47Z**, HEAD `4b806e14db22ea44cc57729f5fa3f7b46b616178`,
`git status --porcelain` → only `?? .ufo/waves/arc2-loop1-round1/` (nothing
landed; the wave dir grew from 32 to 57 files during this session — the
census below was re-run over the complete final set; R8.md was concurrently
rewritten by its author, quote now at :101).

## Verdict

**ATTACK FAILS — no smuggled exploratory claim exists.** All three declared
claims (C1 freshness, C2 operability, C3 depth) are measurable, each carrying
a counting command run in this session's re-verification; **zero** exploratory
claims are declared (the protocol's one-per-round exploratory slot is unused);
and the round's only taste-bearing decision — which verbatim wording variant
lands — is explicitly parent-adjudicated and measurement-neutral (both/all
drafts measure identically). One residual to carry, not an exploratory
smuggle: the C1 census phrase "unscoped benign loci N→0" read fleet-wide is
**provable-but-false** at landing (`corpus/README.md:90,:160`, `LOG.md:21`
remain unqualified), not unprovable-but-better; the CR5/S2 scope sentence is
its required landing companion.

## Evidence — commands run this session, observed output

### 1. The bar (read this session, fleet repo, read-only)

- `/home/vgpnk/Projects/shokunin/AXES.md:43-55` — exploratory claim verifies
  only as `unprovable-but-better` "**with a named non-author reviewer on
  record** (reasons included; a dispatched subagent does not count) …
  Without that judgment it lands `unprovable` and the honest-stop rule
  applies. At most one exploratory claim per round."
- `/home/vgpnk/Projects/shokunin/AXES.md:79` — SCORECARD axes row: exploratory
  moves carry "`unprovable-but-better` verdict + named non-author reviewer".
- `/home/vgpnk/Projects/shokunin/PROTOCOL.md:488-493` — same rule restated
  ("An exploratory claim verifies only as `unprovable-but-better` with a
  named non-author reviewer on record (§Appendix, 'Exploratory claims')").
- `/home/vgpnk/Projects/shokunin/PROTOCOL-APPENDIX.md:50` — incident row:
  "taste admitted through the outside-discernment gate (`LEARNING.md`), never
  through self-attestation; unjudged, they land `unprovable` and honest stop
  applies | operator amendment 2026-10-16".
- `/home/vgpnk/Projects/shokunin/PROTOCOL.md:63-72` — promotion gate: `[x]`
  needs a named non-author verifier; "a subagent the lane dispatched is still
  the lane".

### 2. Exploratory-claim census over the complete seat set (57 files, final re-run 16:47Z)

```
$ ls .ufo/waves/arc2-loop1-round1/*.md | wc -l
57
$ grep -rn -iE "exploratory|unprovable|elegance|technique quality|taste-bound" \
    .ufo/waves/arc2-loop1-round1/*.md   # (excluding this report)
.ufo/waves/arc2-loop1-round1/R8.md:101:     multi-claim rounds + capabilities + exploratory claims + godspeed L2
.ufo/waves/arc2-loop1-round1/CR8.md:219:   pre-14:49:13Z history of the configs is unprovable by this instrument —
.ufo/waves/arc2-loop1-round1/CR8.md:284:  config history (unprovable by hash custody, by construction); whether any
$ grep -rn "unprovable-but-better" .ufo/waves/arc2-loop1-round1/ | grep -v CR7.md
NONE outside CR7
$ grep -rn -i "discernment" .ufo/waves/arc2-loop1-round1/*.md
E21.md:81:Learning trends: expansion <fill>; quality <fill>; discernment <fill>.
Z2.md:135:Learning trends (parent fill): expansion <fill>; quality <fill>; discernment <fill>.
```

Observation: the **only** occurrence of the word "exploratory" in the entire
wave directory is R8.md:101 (was :89 before its author's concurrent rewrite),
which quotes a fleet-repo commit message (`84bade0` "protocol: multi-claim
rounds + capabilities + exploratory claims + godspeed L2 lead") as a
hash-resolution example — not a claim declaration. The exact phrase
`unprovable-but-better` appears nowhere outside this report. CR8.md:219,284
use "unprovable" only to state a custody limitation ("the pre-14:49:13Z
history of the configs is unprovable by this instrument") — a named
limitation, the opposite of a smuggled taste claim. Zero taste/elegance
language exists. The learning-trend cells that could carry a soft
"discernment improved" statement are still `<fill>` placeholders for the
parent (E21.md:81, Z2.md:135).

### 3. All three claims are measurable — re-verified by this seat

C1 census (the after-measurement instrument), run at HEAD against the
un-landed target:

```
$ python3 -c "import re;t=open('corpus/knowledge/2026-10-13-r3-jq-provenance.md').read();h,_,n=t.partition('**Safety-verdict scope');L=[i+1 for i,l in enumerate(h.splitlines()) if 'benign' in l or 'malicious or accidental' in l];N=set();[N.update(range(int(a),int(b)+1) if b else [int(a)]) for a,b in re.findall(r':(\d+)(?:-(\d+))?',n)];U=[x for x in L if x not in N];print('loci',L,'unscoped',U,'n',len(U))"
loci [60, 136] unscoped [60, 136] n 2
$ grep -nE "benign|malicious|accidental|safe|trust|compromise" corpus/knowledge/2026-10-13-r3-jq-provenance.md
60:  benign, intentional install: an agent-executed copy of the official
136:finding; no malicious or accidental pathway indicated. Residual Unknown
```

C2 custody (zero-drift counting command), run this session:

```
$ sha256sum ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json ~/.kimi-code/config.toml
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json
3546e033aeaf68093faf4099ea8289de5dea7ec224e7c557f08bfa9d51cf9a2a  /home/vgpnk/.kimi-code/config.toml
$ tail -n +2 .ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
custody-rc=0
```

C3 command A (SCORECARD.md:92-123 recipe, run verbatim at `REV=$(git rev-parse HEAD)`):

```
{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "4b806e14db22ea44cc57729f5fa3f7b46b616178",
 "rule_blocks": 9}
```

Each claim's acceptance test is a counting command with a numeric
before→after: C1 2→0 loci; C2 rc 0 with 3/3 OK; C3 rules 9→10, 10/10
resolvable (draft-measured at E17.md:29-33, E18.md:36-40, P4.md:64-68,
E19.md:88-95 — all 10/10/10.0; independently corroborated later this session
by R4.md:11-15, which also confirms the move must be recorded as rules 9→10
at 10/10, NOT a score change). None requires an `unprovable-but-better`
judgment, and none claims one.

### 4. The only taste decision is adjudicated and measurement-neutral

- E19.md:159-163 (Unknown): "which draft the parent lands (E17's 9-line text
  and E18's 12-line text converge in substance but are not byte-identical;
  both measure 10/10/10.0 — **this is a wording choice, not a measurement
  choice**)". Same for C1a (P1.md:34-49 vs E6.md:33-35 vs E3.md) and C1b
  (E8.md:37-63 vs E7.md:136-148 / P2.md §3 / E10.md): every variant was
  independently measured; no variant's superiority is claimed on taste
  grounds. R4.md adds a merged 11-line block that also measures 10/10/10.0 —
  still a wording choice among equals.
- The one place a reviewer-gated verdict could have been smuggled — SHONEN
  `[x]` — is explicitly refused by the design itself: Z2.md:113-114 "`[x]`
  needs a named non-author verifier — **none exists**; all four boxes stay
  `[~]`"; E23.md:153 SHONEN box 1 "no semantic audit, no outside verifier".
  That is honest-stop handling, not a smuggle.
- E15.md:3-10: the 5-path custody scope is proposed as a **forward contract
  only**; "For this round the demonstrated pair stays the frozen 3-file
  pair" — the claim's measurement is not widened to an unmeasured surface.
- E26.md:7 (battery leg 3, landed 13:43:55 -0300): PASS with sha256, decode,
  export, close — measurable, no taste element. E28.md confirms zero session
  residue; CR8.md confirms the custody chain post-battery.

## Verbatim block for the parent (land in the round record if used)

```text
CR7 (critic) — smuggled-exploratory-claim scan: CLEAR.
No claim in arc2-loop1-round1 is exploratory-shaped. The protocol's one
exploratory-claim slot is unused (zero declarations across all seat files;
excluding this report, the sole "exploratory" token is R8.md:101, which
quotes a fleet commit message).
All three claims carry counting commands (C1 census 2->0; C2 sha256 pair
rc 0 / 3 OK; C3 command A rules 9->10, 10/10 resolvable). The wording
choice among measured draft variants (E19.md:159-163) is parent-adjudicated
and measurement-neutral. Do not record any axis verdict as
unprovable-but-better this round; none is needed and none would have the
required named non-author reviewer.
Required companion if the C1 axis row uses fleet-wide wording: land the
CR5/S2 scope sentence (S2.md:120-131) — the fleet-wide "N->0" reading is
false at landing (corpus/README.md:90,:160; LOG.md:21 remain); only the
r3-file-scoped reading (n 2 -> 0) is the measured claim.
```

## Conclusions

- **Observation** (ran/read this session): the exploratory/unprovable census
  over the complete final seat set (57 files) returns one "exploratory" hit
  (R8.md:101, a quoted fleet commit message) and two "unprovable" limitation
  statements (CR8.md:219,284) — no verdicts; the three counting commands above
  ran with the shown output; HEAD and worktree state as stated; the protocol
  bar text read at AXES.md:43-55,79, PROTOCOL.md:488-493,63-72,
  PROTOCOL-APPENDIX.md:50; the self-limitation at Z2.md:113-114 and
  E23.md:153; the wording-choice adjudication at E19.md:159-163; the 5-path
  forward-scope restraint at E15.md:3-10; leg 3 landed at E26.md:7.
- **Inference**: no claim in this round's design has the
  unprovable-but-better shape, so no claim lacks the named non-author
  reviewer the bar would require — the attack surface is empty. The design
  in fact keeps its two reviewer-gated surfaces honest (SHONEN `[x]`
  refused; all four boxes `[~]` with the reason stated).
- **Unknown**: (a) the parent's final variant choices (C1a/C1b/rule-10
  texts) — nothing has landed (`git status` shows only the untracked wave
  dir), and every variant was measured, so no claim's verifiability turns on
  the choice; (b) what the parent fills into the learning-trend cells
  (E21.md:81, Z2.md:135) — trend cells carry no reviewer gate in the
  protocol, but if "discernment improved" is recorded it should follow the
  luna-round precedent's "locally" scoping, since no outside verifier
  exists; (c) whether the CR5/S2 scope sentence actually lands with the C1
  row (outside this seat); (d) whether the post-pair receipt lands (C2's
  post-half; receipts/ still holds only `config-pre-pair.txt` at snapshot —
  other seats' scope).

## Reproduction commands

```bash
git rev-parse HEAD && git status --porcelain
grep -rn -iE "exploratory|unprovable|elegance|technique quality|taste-bound" .ufo/waves/arc2-loop1-round1/*.md
grep -rn "unprovable" .ufo/waves/arc2-loop1-round1/
# command A: SCORECARD.md:92-123 verbatim with REV=$(git rev-parse HEAD)
# C1 census: the python3 one-liner above (S2.md:19-20)
tail -n +2 .ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt | sha256sum -c -
sed -n '43,55p' /home/vgpnk/Projects/shokunin/AXES.md; sed -n '79p' /home/vgpnk/Projects/shokunin/AXES.md
sed -n '113,114p' .ufo/waves/arc2-loop1-round1/Z2.md; sed -n '159,163p' .ufo/waves/arc2-loop1-round1/E19.md
```
