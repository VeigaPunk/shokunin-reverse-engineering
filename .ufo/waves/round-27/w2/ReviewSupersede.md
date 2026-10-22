# ReviewSupersede — consistency of the round-27 narrowing of the "seven content-keyed verbs"

Seat KaidokuR27.ReviewSupersede, 2026-10-22, wave 2. Attack target: after round 27 narrowed
`analyze`/`inspect` to "content-keyed across directories only while the file extension class
stays the same" (`corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md:75-76`),
does every scoped-path place that still says analyze/inspect are content-keyed across paths
carry or reach a round-27 pointer? Scope: SKILL.md, corpus/README.md, corpus/knowledge,
PROVINCE.md, all at git rev `main`.

All greps were run against the committed `main` tree with `git grep ... main`, never the
working copy. Labels: (obs) = observed output, (inf) = my inference.

## Check 1 — lane tip identity
- Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse main`
- Excerpt (obs): `4084d8975b684a8837b1c858eea0008ce9ab49e0`
- Exit 0, 2026-10-22T15:36:10Z. Matches the frozen lane tip. Verdict: holds (obs).

## Check 2 — inventory of "content-keyed" claims in scoped paths
- Command: `git -C <lane> grep -n -i -E "content-keyed" main -- SKILL.md corpus/README.md corpus/knowledge PROVINCE.md` (raw: content-keyed-scoped.txt, 29 hits)
- Excerpt (obs): `main:SKILL.md:894:| 'analyze', 'inspect' (one operation, 'binary_overview'; same id for both) | content-keyed across directories |` and `main:corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md:32:| 'analyze' | base = repeat = copy ... | content-keyed |`
- Exit 0, 2026-10-22T15:36:10Z. Verdict: holds as inventory (obs).

## Check 3 — spelling and phrasing variants (catches claims without the literal token)
- Commands (both exit 0, 2026-10-22T15:39:05Z):
  - `git grep -n -i -E "content[-+ ]?keyed|content.address" main -- <scoped paths>` (raw: content-variants.txt, 82 hits)
  - `git grep -n -i -E "(analyze|inspect).{0,90}(content-keyed|content keyed|across director)|(content-keyed|content keyed|across director).{0,90}(analyze|inspect)" main -- <scoped paths>` (raw: proximity-analyze-inspect.txt, 14 hits)
  - `git grep -n -i -E "same id across|across two paths|id across" main -- <scoped paths>` (same time, exit 0)
- Excerpt (obs): `main:corpus/README.md:207: ... while 'analyze'/'inspect' and 'analyze_function' ids are content+params-keyed — 'analyze_function' proven to keep the same id across two paths (r9-02) ...` — this variant is invisible to the plain "content-keyed" grep.
- Verdict: holds as inventory (obs); the variant pass found one extra candidate (F2 below).

## Check 4 — where the round-27 pointers live
- Command: `git grep -n -i -E "round.?27" main -- SKILL.md corpus/README.md corpus/knowledge PROVINCE.md` (raw: round27-pointers.txt, 19 hits; exit 0, 2026-10-22T15:39:05Z)
- Excerpt (obs): `main:SKILL.md:912:## Evidence-ID identity under a renamed copy and on a second carrier — round 27`; `main:PROVINCE.md:305:## Round-27 renamed-copy identity and cross-pin attribution — 2026-10-22`; `main:corpus/README.md:76`, `:209`.
- Key negative (obs): no hit in `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` and none in `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md`.
- Verdict: holds as pointer map (obs).

## Check 5 — per-location coverage of every stale-or-ambiguous claim
Each row: place that still states analyze/inspect content-keyed across paths without the
extension limit, and the round-27 pointer that reaches it. All quotes (obs) at main.

| place | claim | round-27 pointer | covered? |
|---|---|---|---|
| SKILL.md:894 (r26 table row) | "content-keyed across directories" for analyze, inspect | SKILL.md:912-915 "This section narrows the round-26 table above for `analyze` and `inspect`: they are content-keyed across directories only while the file extension class stays the same" | yes, explicit, same file |
| corpus/README.md:75 (r26 evidence row, "seven content-keyed ... different file names not tested") | seven content-keyed | row 76 directly below: "against round 26, `analyze` and `inspect` turn rename-sensitive because the file extension reaches `normalized_result.document`" | yes, adjacent, explicit |
| corpus/README.md:208 (Knowledge r26 bullet) | "analyze, inspect, ... are content-keyed" | bullet 209 directly below ("Round 27 update ... Against round 26, `analyze` and `inspect` turn rename-sensitive ...") | yes, adjacent, explicit |
| corpus/README.md:207 (top Knowledge bullet) | "analyze/inspect ... ids are content+params-keyed" | only via sub-bullet 209, which names round 26 but not bullet 207; 207's wording unchanged | in substance, not by wording — finding F2 |
| corpus/knowledge/2026-10-22-r26-...md:32-33,46 | analyze/inspect rows "content-keyed"; "the content-keyed verbs the same id at a third directory" | r27 entry:75-76 "This narrows the round-26 entry's 'seven content-keyed verbs'" — external, names the r26 entry; the r26 file itself has no forward pointer | yes, external only — note in F1's class |
| corpus/knowledge/2026-10-20-r17-...md:118 (filed) and :211 (appended round-26 pointer) | "consistent with the content-keyed `analyze` id"; "/usr/bin/jq is content-keyed (`...r26-...md`)" | none in the file; chain r17:211 -> r26 entry -> r27 entry:75 is transitive only | no direct round-27 pointer — finding F1 |

Clean neighbors, no action (obs): SKILL.md:895 (five verbs stayed content-keyed, r27 confirms);
PROVINCE.md:305-318 already carries the narrowing and says no Frontier bullet retired;
r27 entry rows 30-34 (five address verbs content-keyed — correct under r27);
corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:979 and 2026-10-14-r12-01-queue-b-ready.md:124
are appended round-26 pointers about `inspect-binary-layout` only, which stays path-sensitive;
r3-mcp-session and r9-02 talk about `analyze_function` and MCP surfaces, which the r27 Limits
(:83-84) explicitly do not cover.

## Findings by severity

- F1 (LOW, gap): `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` has a round-26
  pointer appended at :209-211 but no round-27 pointer, and :211 restates the unrestricted
  phrase "content-keyed `analyze` id" while citing only the round-26 entry. A reader who
  stops there misses that at 6.5.0 the phrase now holds only within one extension class.
  Mitigation (obs): the r17 observation was same-path repeats, and r27 measured base = repeat
  equal in all 16 pairs (r27 entry:36), so the filed observation stays true; only the
  unrestricted wording is unguarded. Evidence: checks 2 and 4, exit 0.
- F2 (LOW, gap): `corpus/README.md:207` still says "`analyze`/`inspect` ... ids are
  content+params-keyed" with no extension limit; the narrowing sits two bullets down (:209)
  and never names :207. A reader quoting bullet 207 alone states the superseded claim.
  Evidence: checks 3 and 4, exit 0.
- No HIGH/MEDIUM finding: every load-bearing pointer location (SKILL r26 table, README
  evidence rows, README r26 Knowledge bullet, the r26 entry itself) is covered by an explicit
  round-27 narrowing statement, and PROVINCE/SKILL round-27 sections restate the mechanism.

## Verdict on the assigned item
Holds (inf from obs): the round-27 narrowing is consistently propagated to every scoped-path
place a practitioner would consult for identity decisions; two LOW wording-coverage gaps (F1,
F2) remain in historical and summary bullets.

## Residual risk and verification gaps
- Text grep on the `main` rev only; I did not diff pre-round-27 history to prove no other
  wording exists (inf: variant pass over content-addressed/content+params/same-id phrasings
  makes additional forms unlikely but not impossible).
- QUALITY.md rows 38-40, corpus/lessons/round-27.md, LOG and SCORECARD are outside my scoped
  paths and were not attacked.
- No LSP server applies to markdown; classification rests on git grep plus manual reading of
  every scoped hit (raw files below).

## Artifacts (raw grep output, sha256)
- /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReviewSupersede/raw/content-keyed-scoped.txt — b5b0d746b267f96819c4e728e27516e3e3868110effafb80d5477f2345d13301
- /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReviewSupersede/raw/content-variants.txt — b19a8a61c13d9d278624c56dbccdaf1afff4366eb6cc681facd5eff119a1e02f
- /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReviewSupersede/raw/proximity-analyze-inspect.txt — 1272b281e6dbd4bb7618e2ce1942f2c7249b9fd2827486d4dc2c15848b4b5e59
- /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReviewSupersede/raw/round27-pointers.txt — f2702ee8901c9555eda0f1303307e78bb321790c396af4be59dbca2f80af034e

No tools were installed or updated; only read-only git commands against the lane.
