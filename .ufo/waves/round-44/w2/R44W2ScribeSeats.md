# R44W2ScribeSeats — seat / round-shape annex (kaidoku round 44, wave 2)

Seat: `R44W2ScribeSeats` (scribe). Round: kaidoku 44, wave 2 = falsification.
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Captured: 2026-10-28T14:22:11Z (11:22:11 −03 host local). Every number below is re-derived from
the wave files by `artifacts/R44W2ScribeSeats/verify_seats.py`; nothing is copied from the seat
prompt. Machine-readable form: `artifacts/R44W2ScribeSeats/shape.json`
(sha256 `d54d56f1…6845790a`); full derivation: `artifacts/R44W2ScribeSeats/verify.json`
(sha256 `70a61f38…79e5706d`).

## 0. Sentence the report's "Work performed" bullet can use

> Shape: two v1 waves — wave 1 **37 seats** (build), wave 2 **42 seats** (falsify), **79 seats**
> total under the 128 cap; attack share 25/79 = **31.6 %** by the policy's attack-role set
> (reviewer/critic/mutation-tester; `labrat` carries no seats; w1 21.6 %, w2 40.5 %) and
> 38/79 = 48.1 % counting
> sentinel/revenger/connector as attack; **0 dead seats** in wave 1 (37/37 reports landed) and
> wave 2 in flight at annex capture; **no residual call**.

## 1. Table (verified against the files)

| field | value | verification |
|---|---|---|
| shape | **two v1 waves** — both dispatches carry policy v1 `waveMinLanes 32` / `waveMaxLanes 64` (v2 policy is 64/128) | `w1-dispatch.json.policy`, `w2-dispatch.json.policy` |
| wave 1 seats | **37** | `w1-spec.json` items = 37; `w1-dispatch.json.counts.spawn = 37`; `w1/swarm-registry.json` members = 37; `r44-w1-results.json.seats = 37`, results = 37 |
| wave 2 seats | **42** | `w2-spec.json` items = 42; `w2-dispatch.json.counts.spawn = 42`; `w2/swarm-registry.json` members = 42 |
| wave-1 dispatch | 2026-10-28T08:12:09 −03 (11:12:09Z), one `task` call (37 tasks), 0 resumes | `w1.ready.dispatched:1`, `w1-dispatch.json.counts` |
| wave-2 dispatch | 2026-10-28T11:18:59 −03 (14:18:59Z), one `task` call (42 tasks), 0 resumes | `w2.ready.dispatched:1`, `w2-dispatch.json.counts` |
| wave-2 gating | dispatched only after wave 1 returned: `r44-w1-results.json` mtime 09:26:05 −03 precedes `w2-spec.json` 11:17:55 −03 | `checks.txt` mtimes |
| attack share (policy set) | w1 **8/37 = 21.6 %** · w2 **17/42 = 40.5 %** · round **25/79 = 31.6 %** | `verify.json.attack_share.*_narrow` |
| attack share (wide set) | w1 13/37 = 35.1 % · w2 25/42 = 59.5 % · round 38/79 = 48.1 % | `verify.json.attack_share.*_wide` |
| dead seats | wave 1: **0** (37/37 `.md` reports present and non-empty, 37/37 results, 0 `error` outputs, 0 unparsable outputs) · wave 2: **not determinable** (in flight; `r44-w2-results.json` absent) | `verify.json.w1.results`, `.w2.results` |
| residual call | **none** — no `*resid*`/`w3*` artifact in the round dir; round total sits under the cap | `verify.json.residual` |
| round total | **79** (= 37 + 42), inside 32–128 | `verify.json.bands.round_total*` |
| role validity | all 79 seats carry roles inside the policy's `proposalRoles`; no `planner` seat in either spec | `checks.txt`, `verify.json.*.spec.planner_seats` |

The prompt's stated wave-1 tally reproduces **exactly**: executor 8, scribe 8, scout 7,
reviewer 4, critic 3, connector 3, revenger 1, sentinel 1, mutation-tester 1, simplifier 1 = 37.

## 2. Per-wave role mix

| role | w1 | w2 | round |
|---|---:|---:|---:|
| scout | 7 | 7 | 14 |
| executor | 8 | 5 | 13 |
| scribe | 8 | 4 | 12 |
| reviewer | 4 | 7 | 11 |
| critic | 3 | 7 | 10 |
| connector | 3 | 3 | 6 |
| mutation-tester | 1 | 3 | 4 |
| sentinel | 1 | 3 | 4 |
| revenger | 1 | 2 | 3 |
| simplifier | 1 | 1 | 2 |
| **total** | **37** | **42** | **79** |

Source: `verify.json.w1.spec.roles`, `verify.json.w2.spec.roles`; the same tally is returned by
the dispatch task lists and by both `swarm-registry.json` files (three independent surfaces agree,
zero role mismatches — `verify.json.*.dispatch.task_roles_equal_spec_roles`,
`verify.json.*.registry.role_mismatches_vs_spec`).

## 3. Findings (reported, not fixed — this seat changes no claim, counter, rubric or doc)

**F1 — the ≥25 % attack-share floor is met at round level but not by wave 1 on the policy's own
attack set.** The policy's attack roles are `reviewer, critic, mutation-tester, labrat`
(`/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:203`); the run-11 header keeps
"≥25 % attack share" binding (`lane-addendum.md:5`). Observed tallies:
`round-44/w1-spec.json` → reviewer 4 + critic 3 + mutation-tester 1 = **8/37 = 21.6 %** (below
25 %); `round-44/w2-spec.json` → 7 + 7 + 3 = **17/42 = 40.5 %**; round → **25/79 = 31.6 %**.
Counting connector/revenger/sentinel as attack gives w1 13/37 = 35.1 %, w2 25/42 = 59.5 %,
round 38/79 = 48.1 %. Command: `python3 .ufo/waves/round-44/w2/artifacts/R44W2ScribeSeats/verify_seats.py`,
exit 0. This is a labelling question, not a gate the validator enforces (neither dispatch policy
carries an attack threshold: `w1-dispatch.json.policy` has only lane bands). It also confirms and
extends the wave-1 seat's own finding E (`w1/R44Watchdog.md` §3, which computed the same 8/37 and
the 35.1 % wide figure). Recommendation for the report: quote the round-level 31.6 % (and the
wide-set 48.1 %) and disclose the wave-1 21.6 % under the narrow set, rather than a single
unqualified "≥25 %".

**F2 — accounting joins must key on the spec id, not the dispatched id.** 8 of 37 wave-1 seats were
dispatched under suffixed ids after retries — `R44RevKill→R44RevKill-2`, `R44Prefile→-4`,
`R44Simplify→-5`, `R44ScoutSEAT→-3`, `R44C1FixtureAudit→-2`, `R44C2Plan→-2`,
`R44C2SentReview→-2`, `R44Watchdog→-2` (`w1.ready.dispatched:2`); wave 2 has one,
`R44W2Wave→R44W2Wave-2` (`w2.ready.dispatched:2`). Output files, results rows and registry
members all use the **spec** id (verified: 37/37 `.md` present under spec names, name sets equal
across spec/dispatch/registry/results). A tallier keyed on `task`-returned ids under-counts wave 1
by 8. Wave-level counts are not affected: 37 and 42 are the spec, dispatch-count and registry
numbers alike.

**F3 — one markdown file in `w1/` is not a seat.** `w1/` holds 38 `.md` files for 37 seats; the
extra is `w1/R44C1Oracle-r48-ready.md` (a supplementary annex, absent from `w1-spec.json`).
Counting files instead of spec items reports 38. Observed value:
`verify.json.w1.results.md_files_not_a_seat = ["R44C1Oracle-r48-ready"]`, reports present 37,
total 593,232 bytes.

**F4 — the `*.ready.dispatched` timestamps are host-local (−03), not UTC.** First lines are
`2026-10-28T08:12:09` and `2026-10-28T11:18:59`; the corresponding UTC instants are 11:12:09Z and
14:18:59Z (`checks.txt`: `host_local=…-0300`, `host_utc=…Z`). Any report that mixes these with UTC
receipts is three hours off; the annex uses both forms explicitly. No defect in the lane — a
reading hazard only.

**F5 — wave 2 had no results file at annex capture.** `r44-w2-results.json` absent at
14:22:11Z, 3 min 12 s after dispatch (42 spawns). Dead-seat accounting for wave 2 cannot be
finished from the artifacts that exist now; the report must either wait for `r44-w2-results.json`
or state "42 dispatched, results pending". This annex reports wave 1 only as final.

## 4. Receipts

| id | command | exit | stdout sha256 | wall s |
|---|---|---:|---|---:|
| R1 | `python3 <scratch>/verify_seats.py > .ufo/waves/round-44/w2/artifacts/R44W2ScribeSeats/verify.json` | 0 | `70a61f38f70e72ed8c52c5fa7d7cf135905db323d11d33a78b96d8e879e5706d` | 0.020 |
| R2 | `bash .ufo/waves/round-44/w2/artifacts/R44W2ScribeSeats/checks.sh > …/checks.txt` | 0 | `4f06a2cddc4a4e2704c3fb6a8b016d4b456867a2d294d278b9ecfbc3785c8c0d` | 0.014 |
| R3 | `python3 …/artifacts/R44W2ScribeSeats/mkshape.py …/artifacts/R44W2ScribeSeats > shape2.out` | 0 | `d54d56f1f016cfd192cc7f0d15df2365b73866bd41beda1fdf6973926845790a` (= `shape.json`, `cmp -s` 0) | 0.012 |

R1 was executed from scratch; the executed script is byte-identical to
`artifacts/R44W2ScribeSeats/verify_seats.py` (sha256 `b5dd9ccc…3beb09b31`) and the output's
`as_of_utc` field makes a re-run's sha differ — the sha above is the captured bytes. Full detail:
`artifacts/R44W2ScribeSeats/receipts.json`.

Read-only inputs re-opened for the band/attack-set verification (no writes):
`/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`,
`…/ufo-wave-policy-v2.json`, `…/lane-addendum.md`.

## 5. Limits and disclosures

- This seat wrote only `.ufo/waves/round-44/w2/R44W2ScribeSeats.md` and
  `.ufo/waves/round-44/w2/artifacts/R44W2ScribeSeats/**`. No git/jj mutation, no lane production
  file, no claim/counter/rubric byte, no PATH entry, no fleet-root tracked file.
- No tool was installed or upgraded.
- Wave-2 role mix is the **spec** mix (roles are fixed when the wave is generated); it is not a
  report of completed wave-2 work. Wave-2 dead seats and any wave-2 seat that fails to land need
  `r44-w2-results.json` plus a `.md` presence check, exactly as done here for wave 1.
- Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2ScribeSeats/` was deleted before yielding; the
  two scripts and all captured outputs live under `artifacts/R44W2ScribeSeats/`.
