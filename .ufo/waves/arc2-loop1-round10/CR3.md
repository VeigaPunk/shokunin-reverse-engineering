# CR3 — critic: is the hyper-lane provider census this lane's province (adjacency) or operator territory?

Seat CR3 (critic), wave `arc2-loop1-round10`, 2026-10-18. Snapshot window
23:56Z–00:58Z (stamps inline). HEAD `c561f00`; working tree clean apart from the
untracked round-10 wave dir and one gate byproduct (`.ufo/gates/__pycache__/`).
Only repo write: this file. Scratch: `/var/tmp/arc2-l10r10-CR3-cust.txt` (custody
re-derivation only). Both live services observed read-only, never signalled;
`arc2-r10-big` and `arc2-r10-mid` reached their terminal states before this seat's
close — no signal was sent by this seat. Custody re-derived by this seat: **5/5
MATCH** (§2.1).

---

## 1. Verdict

**SPLIT, and the claim as dispatched is mis-typed.** The question has two halves
and they land in different places; only one of them is a lane move at all.

1. **The substitution *fact* is operator territory, already recorded — not a
   lane move.** `LOG.md:1273-1282` records the operator directive ("run one
   deepseek round on the hyper provider instead of devin … arc2-loop1-round10
   rides `hyper/deepseek-v4.1-flash`"), and the goal's substitution rule asks
   only that the round *cite* that entry (`LOG.md:1279`; the r9 precedent at
   `LOG.md:1321-1327`). `SCORECARD.md:1264` already carries it as the plan.
   Re-deriving or re-deciding the provider is not evidence this lane can add,
   and `PROVINCE.md:108-113` reserves config/routing-class operator actions.
2. **The model×lane *census* is another domain's surface, so it is adjacency
   only in the AXES.md:16 sense — "evidence belonging to another domain
   reported, not absorbed".** The measurement itself is declared elsewhere:
   kengaku owns "Route telemetry … model×lane and reroute-chain"
   (`../kengaku-shokunin/PROVINCE.md:15`, path currently ABSENT), kumitate owns
   OMP route resolution/fallback policy, and kama was minted for endpoint
   health (`.ufo/l0-questions.md` kama round-10/round-1 entries). The lane's own
   Adjacent section already states the discipline: "reported to the
   orchestrator, never absorbed" (`PROVINCE.md:95-98`). The fleet has a channel
   for exactly this kind of operator question — append-only
   `.ufo/l0-questions.md:24` (`<lane> | round-<N> | <question>`), with the kama
   round-8 provider-substitution question as the direct precedent
   (`.ufo/l0-questions.md:48`).
3. **The census as a *comparison* ("delivery/quality/convergence vs devin-lane
   waves") is NOT landable from this round and must not be scored as an axis
   move.** There is no matched pair across providers in this arc, and three
   confounds are already on the record (§2.3). Landing a provider-effect table
   would absorb a fleet measurement and would over-credit adjacency. **What is
   landable** is the narrow form: cite the operator directive, file the
   report-out naming the contested scope, and keep the lane's own delivery
   ledger where it belongs — in **operability**, which is what E9.md already
   does.

**Attack on the in-flight artifacts.** E9.md's census is honest where it matters:
it records 0 seat reports at its own position, calls the comparison **pending**,
and labels its landable text "record, do not absorb" (`.ufo/waves/arc2-loop1-round10/E9.md:1-16,192-196,206-224`).
Two defects survive against it and one inflation vector sits in the records
skeleton:

- **D1 (precision) — E9's "devin baseline" is not a devin baseline.** E9.md:19-22
  says "every devin 64-seat wave delivered 100% … R1 64/64 items; R2-R5 60/60
  items each", but its own table one screen later assigns **R5 to
  `openai-codex/gpt-6-luna-max`** (`E9.md:118-125`) and R1 to a *recovery*
  dispatch (18 seats + 46 devin replacements, `SCORECARD.md:646-653`). The
  aggregate is therefore a two-lane, recovery-inclusive figure labelled devin.
- **D2 (denominator) — the hyper denominator is not in the repo.** E9.md:120-125
  records R10's "items dispatched" as **"not materialised in repo"**, so the
  only pre-dispatch seat artifact is the roster (`receipts/roster-frozen.txt`).
  "Delivery vs items" for the hyper leg is unmeasurable at close from repo
  state; "delivery vs roster" is measurable but is a different claim. The
  baseline's own denominator was unstable too: rounds 2-4 declared 64 and
  dispatched 60 (`R4.md:71,78`).
- **D3 (inflation vector) — the records skeleton invites the absorbed claim.**
  `E15.md:271` reads `- **C3** — census <FILL: delivery/quality/convergence vs
  devin-lane>`. Filling that slot with a provider comparison would land the
  exact claim §1.3 refuses. The slot must be filled with the report-out form.

**No verdict inflation found elsewhere.** At my snapshot the wave dir holds 23
seat reports / 375,127 B (E9's 0-report number is timestamped at its own
position, not falsified by this); the big leg is terminal `Result=success`
(§2.2) — that outcome is **C1's claim, not mine**; and no seat file inspected
asserts a provider effect. `E3.md:257` explicitly declines the attribution
("Attribution of the outcome to the lane substitution is the parent's
adjudication, not this seat's claim") — correct boundary-keeping.

---

## 2. Evidence

### 2.1 Custody (my scope touches the wave's custody claim)

```text
$ awk 'NR>1{print $1"  "$2}' .ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json
6ba8a0f95b8508229fe7137613819597b4da3ea92a873340f2d82b3cf36a73ac  /home/vgpnk/.kimi-code/config.toml
7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598  /home/vgpnk/.bashrc
6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30  /home/vgpnk/.profile
$ # each line's hash vs fresh sha256sum of its path:
… MATCH ×5   → CUSTODY 5/5 MATCH (pre-pair only; no post-pair exists at my close)
```
Receipt timestamp `2026-10-18T23:56:25Z` (`receipts/config-pre-pair.txt:1`).

### 2.2 The provider's own place in this lane's record (no lane move available)

```text
$ grep -n "substitution" LOG.md | head
1273:### operator directive — provider substitution (between rounds 7 and 8)
1279:  operator directs otherwise. Recorded per the goal's substitution rule; the
1290:  substitution/skip logging rule; the skipped rounds' records will cite this
1321:### operator directive — round 9 model substitution (between rounds 8 and 9)
$ sed -n '1275,1280p' LOG.md
- Operator request 2026-10-18: run one deepseek round on the hyper provider
  instead of devin. Applied to the schedule: **arc2-loop1-round10 (this loop)
  rides `hyper/deepseek-v4.1-flash`** (64-128 seats); … Recorded per the goal's
  substitution rule; the round-10 dispatch and records will cite this entry.
```
Resolving pointers: `LOG.md:1273-1282`; plan row `SCORECARD.md:1264`; lane
boundary `PROVINCE.md:95-98` (Adjacent = reported, never absorbed) and
`PROVINCE.md:108-113` (config/install-class actions operator-owned);
fleet invariants `../PROTOCOL.md:461-462` ("domain-facing actions are
operator-owned") and `../PROTOCOL.md:330-340` (a numeric claim carries its
counting command; an unreachable claim does not exist).

### 2.3 The three confounds that make a provider comparison non-identifiable

```text
$ sed -n '257p' .ufo/waves/arc2-loop1-round10/E3.md   # C3-adjacent item, E3's own words
4. **C3-adjacent, recorded not absorbed:** the hyper-lane launch (this wave) differs from the devin-lane r6 mid leg in exactly two dimensions — a `systemd-run` cgroup wrapper with `MemoryMax=9G`/`MemorySwapMax=1G`, and `npx -y rea-agents@6.5.0` vs the bare `node …/rea.mjs` invocation. …
$ sed -n '25,30p' .ufo/waves/arc2-loop1-round10/C3.md    # host pressure, pre-dating both legs
2. **The two 9G caps do not compose into a host bound.** Both units sit in `app.slice`, whose `MemoryMax=infinity` and whose `MemoryPeak` reached 30,289,674,240 B (28.2 GiB) on a 31,721,792 kB (29.5 GiB) box. A **host-wide** OOM fired at 20:52:36-03 …
```
- **(a) Launch recipe** — cgroup wrapper + `npx` vs bare `node` (E3.md:257). Any
  hyper-vs-devin outcome delta is confounded with the recipe, not just the model.
- **(b) Host contention** — host-wide OOM at 20:52:36 (before either leg), swap
  ~18 GiB of 34 GiB in use, an unrelated `godot --headless` tenant, `pgscan_direct`
  ≈260 GiB scanned (E3.md Unknown 2; C3.md:25-30). Not a controlled environment.
- **(c) Content/denominator mismatch** — the comparison set spans a 64-seat
  rerun/gate wave (r10), a 24-seat textual round (r9), 128 seats (r6) and
  60-item craft waves whose declared count (64) exceeded the dispatched array
  (60) in r2-r4 (`R4.md:71,78`; `E9.md:118-125`). No same-content pair exists.
- **Cap-vs-provider mis-attribution (would corrupt a "quality" column):** the
  mid leg died at its own 9G cap (`.ufo/waves/arc2-loop1-round10/E15.md:200-212`;
  `C3.md:10-11`) while r6 held the same bytes uncapped at ~18.26 GiB tree RSS —
  so that failure is a cap-sizing fact, not a provider fact. Counting it against
  hyper would be a smuggled causal claim.

### 2.4 What *is* measurable now (and where it belongs)

```text
$ ls .ufo/waves/arc2-loop1-round10/*.md | wc -l          → 23
$ du -sb .ufo/waves/arc2-loop1-round10                   → 375127
$ systemctl --user show arc2-r10-big -p Result,ExecMainStatus,ActiveState
Result=success  ExecMainStatus=0  ActiveState=inactive
$ journalctl --user -u arc2-r10-big --no-pager -o short-iso | tail -1
… 21:20:23 … Consumed 42min 43.809s CPU time over 23min 58.082s wall clock time, 7.8G memory peak …
$ systemctl --user is-active arc2-r10-mid                → failed   (OOM at its 9G cap; C3.md:10-11)
$ grep -o 'ev_[0-9a-f]\{8\}' /var/tmp/arc2-l10r10-big/stdout.json | head -1
ev_a4aa9b0d
```
These are **delivery/operability** facts about *this lane's own round* (seat
reports present, leg terminal states, roster reconciliation). They are the right
material for the round's delivery ledger and for an operability note; they are
not a provider-quality statement, and the big leg's `evidence_id` re-derivation
is **C1's verdict, cited here only as delivery state** (`E15.md:30-40`, `SC2.md:159-198`).

---

## 3. Verbatim-landable text

**(3a) C3 wording for the SCORECARD round section / LOG entry — in-lane form,
recorded not absorbed (replaces the E15.md:271 `<FILL>` slot):**

```markdown
- C3 adjacency — the hyper-lane substitution is *reported*, not measured here.
  The provider choice is an operator directive (`LOG.md:1273-1282`; plan
  `SCORECARD.md:1264`); this lane's obligation under the substitution rule is
  to cite it. The model×lane census (delivery/quality/convergence vs
  devin-lane waves) is another domain's surface — kengaku owns route telemetry
  / model×lane (`../kengaku-shokunin/PROVINCE.md:15`), kumitate owns OMP
  route/fallback policy, kama owns endpoint health — so it is filed as a
  report-out under `PROVINCE.md:95-98`, not absorbed. What this lane records is
  its own round's delivery ledger: at the census position the round-10 wave dir
  held 23 seat reports / 375,127 B (0 reports at `E9.md`'s earlier position,
  which said so), and `arc2-r10-big` is terminal `Result=success` while
  `arc2-r10-mid` is `failed` at its own 9G cap. No provider-effect comparison is
  claimed: the hyper launch differs from the devin-lane leg in the launch recipe
  (`E3.md:257`), the host was under a pre-existing host-wide OOM and heavy swap
  (`C3.md:25-30`), the round content/seat count has no cross-provider match, and
  the hyper leg's dispatched-items array is not materialised in the repo
  (`E9.md:120-125`). Named debt: the model×lane census itself, owned outside
  this lane.
```

**(3b) The report-out one-liner (fleet channel, `.ufo/l0-questions.md:24` form):**

```text
kaidoku | round-10 | Report-out, not a lane artifact: round 10 is the first
arc2 wave on hyper/deepseek-v4.1-flash (operator substitution, LOG.md:1273-1282).
A hyper-vs-devin delivery/quality/convergence census is kengaku's model×lane
surface (kengaku PROVINCE.md:15) with kumitate on route/fallback policy — no
kaidoku province claim is made. Confounds already on record: launch recipe
differs (cgroup wrapper + npx vs bare node, E3.md:257), host under pre-existing
host-wide OOM + ~18/34 GiB swap (C3.md:25-30), no same-content cross-provider
pair, and R10's dispatched-items array is not in the repo (E9.md:120-125).
Lane-local delivery facts are recorded in this round's ledger. Decision
requested: who owns the model×lane census now that kengaku's route-telemetry
path is ABSENT.
```

**(3c) Optional PROVINCE.md Adjacent bullet (append to the list at `:95-116`),
if the parent wants the boundary stated in the province rather than only in the
round record:**

```markdown
- **Model-provider / route measurement** — delivery, quality and convergence
  comparisons across model lanes (hyper vs devin etc.), route/fallback policy,
  and endpoint health `(operator/fleet)`. The lane cites the operator's
  substitution directive and records its own round's delivery facts; it does
  not measure another lane's model surface. Owners: kengaku (route telemetry /
  model×lane), kumitate (OMP route + fallback policy), kama (endpoint health).
```

---

## 4. Labels

**Observation** — custody 5/5 MATCH, pre-pair only (§2.1). The operator
substitution directive and its "records will cite this entry" clause
(`LOG.md:1273-1282`). E9's census was taken at 0 seat reports and says so
(`E9.md:1-16,192-196`); the wave dir now holds 23 reports / 375,127 B and
`arc2-r10-big` is terminal `Result=success`, `arc2-r10-mid` `failed` (§2.4).
E9's prose calls R2-R5 "every devin 64-seat wave" while its own table assigns R5
to `openai-codex/gpt-6-luna-max` (`E9.md:19-22` vs `:118-125`). E3 states the
launch-recipe delta and declines the attribution (`E3.md:257`); C3.md records
the pre-existing host-wide OOM and the non-composing caps (`C3.md:25-30`).
`E15.md:271` leaves the C3 slot as a `<FILL>` inviting a provider comparison.

**Inference** — (i) because the provider decision is operator-owned and already
recorded, the only lane-side obligation the substitution rule creates is
citation, so C3 cannot be a *measurement* move in this lane; (ii) because the
model×lane surface is declared by kengaku/kumitate/kama, a hyper-vs-devin census
is adjacency in the report-out sense and its measurement belongs outside this
lane; (iii) because the three confounds are simultaneous and no same-content
cross-provider pair exists, any number the parent fills into the E15 C3 slot as
a provider comparison would be a correlation with four differences, i.e. the
class of causal overreach the r8 erratum and the lane's own rule #13 exist to
prevent (`SCORECARD.md:1332-1338`); (iv) E9's "100% devin baseline" is a
two-lane, recovery-inclusive aggregate, so even the delivery half has no clean
single-provider baseline.

**Unknown** — (1) whether the parent will file the report-out in
`.ufo/l0-questions.md` or only in the round report; without a durable pointer
the adjacency move has no re-derivable before→after, and AXES.md's
exploratory/`unprovable` stop rule would apply rather than an axis score.
(2) Whether kengaku's route-telemetry path (`~/Projects/bounties/ledger/telemetry.jsonl`,
ABSENT per its province) is expected to return; that determines whether the
census is merely deferred or unowned — the report-out asks the operator.
(3) The hyper leg's dispatched-items array: not materialised in the repo, so I
cannot confirm or refute 64 dispatched items independently of the roster
assertion. (4) Whether a matched-pair design (same claims, same recipe, two
providers) is feasible in a later arc round — not tested, and not this seat's
mandate. (5) I did not run the round's gates (command A, census v10,
citation-drift) beyond custody: they measure C1/C2 surfaces, not this claim, and
E15/SC2 already report them at HEAD `c561f00`.
