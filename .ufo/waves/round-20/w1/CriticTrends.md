# CriticTrends — what legitimizes `expansion: improved` vs a quality trade (round 20)

Seat: `KaidokuR20.CriticTrends-2` (read-only critic). Written 2026-10-20.
Scope: given `.ufo/waves/round-20/claims.json`, under `LEARNING.md:26-38`
(`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md`),
what evidence makes `expansion: improved` legitimate this round, and what
makes it a trade with quality. Judged axes: calibration, coverage, depth.
Observed at `HEAD = d1d981d2cc041dda4656c5b01d2c8445d8d17124` (the claims
declaration commit; baseline `14f0260` is its ancestor).

## The protocol rule (observation)

`LEARNING.md:33` — expansion's `improved` observable is "admitted
`knowledge/` entries on ground the coverage map did not hold, each `source:`
citing a `mined` `corpus/SOURCES.md` row (`own-work` rows included);
frontier areas entered; new kinds of source; a capability admitted to
`SCORECARD.md`", and `improved` requires "net new admitted entries on
uncovered ground, each citing its coverage-map row". The `harmed` condition
on the same row is "an admitted entry fails the bar it was admitted under".
`LEARNING.md:37-38` — "`expansion: improved` with `quality: harmed` is a
trade, reported as a trade, never admitted"; quality is `harmed` at `:34`
when "an entry is found false or stale and left unmarked". `LEARNING.md:29`
warns "no trend is a scalar": naming 131/153 commands is not itself the
trend verdict.

## What makes `improved` legitimate (inference, mapped to this round's artifacts)

1. **Exercised-grade entries, not mention-level names.** `claims.json:25`
   promises entries "from runs on real (or recipe-retained synthesized)
   carriers", and `claims.json:28` calls the per-target `exercised` field
   "the stronger field" while `:29` admits naming "is not proof of full verb
   mastery". The trend-level bar must therefore be: every verb whose entry
   claims held/works carries an `ev_<64hex>` id plus a retained path under
   `.ufo/waves/round-20/evidence/c2/` existing at the measured REV (contract
   `C2`, `contract.md:71-75`), i.e. QUALITY #10 (`corpus/QUALITY.md:20` —
   "held" only for verbs run this round). An entry that *mentions* a verb
   without a run is legitimate expansion only if it declares itself
   mention-level and does not feed the "named" tally as held ground.
2. **Each entry's `source:` cites a `mined` SOURCES row.** All five
   w1 source drafts currently carry placeholder `S0NN` ids and status
   `queued`, not `mined`: `w1/SourceRizinDocs.md:59,63-64`,
   `w1/SourceHarmonyDocs.md:64-74`, `w1/SourceObjdumpDocs.md:42`,
   `w1/SourceWabtRelease.md` (draft row), `w1/SourceGo1246.md:51-55`. The
   rows must land in `corpus/SOURCES.md` with status `mined` at integration
   or every entry citing them fails `LEARNING.md:33`'s citation clause —
   and QUALITY #1 (`QUALITY.md:11`) as well.
3. **Genuinely uncovered ground, with map rows.** Observation: none of the
   five target verb names appear in `corpus/knowledge/` or `corpus/README.md`
   (`grep` exit 1 group shown below); `wasm`/`rizin` hits are incidental
   (file extensions in `r3-renderer-asar.md:9`, `r4u-15-appimage-inner.md:18,78`;
   "rizin … absent" in `pe-surface.md:65`; an adb regex in
   `r4u-06-adb-surface.md:90`). So WASM inspection (`inspect-wasm-artifact`,
   `compare-wasm-interfaces` + WABT-backed validation), rizin execution
   (`execute-rizin-command`, a new provider class on this lane), and the
   Harmony application-graph projection are new *sections* of ground, not
   new entries under held sections. Legitimate `improved` needs new
   coverage-map rows for these surfaces plus Frontier updates
   (`corpus/README.md:170-181`) — not rows appended under e.g. "Archives &
   packages". Command-A integrity must stay 100%: `claims.json:30` falsifies
   if `coverage_score < 100` (`SCORECARD.md:86-121`, recipe A).
4. **Operation granularity, honestly scoped.** `list-objdump-architectures`
   maps to `inspect_with_objdump`'s `architectures` operation; l7-06 already
   held `file_headers` and declared "other operations untested"
   (`corpus/knowledge/2026-10-16-l7-06-inspect-with-objdump.md`, Unknown
   bullet). A new entry is expansion iff it records running `architectures`
   specifically; re-describing the held verb would be duplicate authority.
5. **C3-side entries count only if ground is new.** A first-failure
   forecast entry over the held-out go1.24.6 toolchain (`claims.json:36`;
   carriers `contract.md:88-92`) re-walks the Go-carrier ground already held
   by `r18-swiss-map-replay`/`r19-go125-toolchain-replay` — that is
   depth/quality work, not expansion ground, unless the entry holds a *new*
   surface (e.g., the v2 emulator as a new source kind) or a new
   `SCORECARD.md` capability row (`SCORECARD.md:615-625`; LEARNING `:86-90`
   routes saturated-proxy growth through that table).
6. **No capability/quality regression elsewhere.** Quality must not be
   `harmed` (`:34`): no admitted entry may fail its bar, and no existing
   entry found stale may be left unmarked.
7. **Verdict posture.** If the admit is disputable rather than mechanical,
   `LEARNING.md:48-50` requires a named non-author reviewer on record —
   never self-attestation (`:42-46`).

## What makes it a trade (counterexamples, strongest first)

- **COUNTEREXAMPLE 1 (strongest, local): `pe-surface.md` is already stale on
  rizin.** Observation: `corpus/knowledge/2026-10-13-pe-surface.md:65` heads
  a section "PE RE tooling gaps — radare2, rizin, mono tools, pedump all
  absent", while the contract records rizin 0.8.2 installed at
  `/usr/bin/rizin` (`contract.md:87`). If the round admits an
  `execute-rizin-command` entry without marking the l1-era absence claim
  (erratum/addendum naming the install), that is exactly `LEARNING.md:34`'s
  "an entry is found false or stale and left unmarked" → `quality: harmed` →
  `LEARNING.md:37-38` makes `expansion: improved` a trade even if all five
  verbs land. Impacted axis: quality trend; fixable.
- **COUNTEREXAMPLE 2: named-but-not-exercised verbs inflating the "new
  ground" claim.** The counter (`contract.md:71-75`) lets an entry "name" a
  verb with no run; `claims.json:30` only falsifies below three exercised
  verbs. If, e.g., only wasm+rizin+harmony entries carry `ev_` ids and the
  objdump/compare entries merely name their verbs, the 128→131 tally can
  pass while the *trend claim* "entries from runs on carriers" fails for two
  entries — those two fail QUALITY #10/#6 the bar they were admitted under →
  expansion `harmed` on its own row (`:33` "an admitted entry fails the bar
  it was admitted under"), not just quality. Fixable by scoping entries to
  what ran.
- **COUNTEREXAMPLE 3: `queued`→never-`mined` SOURCES rows.** If entries cite
  `S0NN` rows that stay `queued` (or cite the rejected rizin release page,
  `SourceRizinDocs.md:66`), every such entry fails the `:33` citation
  clause. Fixable at integration; a canonical judge should reject the trend
  verdict if it lands queued.
- **COUNTEREXAMPLE 4: coverage-map gaming.** Adding the five entries under
  an existing held section (or the `## Knowledge` table only) keeps command A
  at 100% while "ground the coverage map did not hold" is never recorded —
  the observable is satisfied letter-only and the claim of new ground is
  false provenance. Fixable: new map rows + Frontier delta.
- **COUNTEREXAMPLE 5: synthesized-carrier overclaim.** If any verb entry
  (e.g., a synthetic wasm module) claims run-evidence without retaining the
  regenerating recipe, it fails QUALITY #12 (`QUALITY.md:23`) → trade.
- **Weaker candidates:** WABT installed by the L1 (`contract.md:86-87`) —
  entry must pin `REA_WABT_BIN_DIRECTORY` and version (QUALITY #8) or the
  "validated by upstream WABT" claim floats; `compare-wasm-interfaces` on
  two synthesized fixtures admits only synthetic-verdict ground, not real
  pair coverage (QUALITY #11 — state what was not examined).

## Smallest safe correction set (inference)

1. Erratum line on `pe-surface.md:65` (or its README row `:79`) recording
   rizin 0.8.2 present at `/usr/bin/rizin` since round 20, cited to
   `contract.md:87`.
2. Integration rule: no `knowledge/` entry citing a `S0NN` row lands until
   that row is `mined`; each entry's `source:` names the assigned `S0xx` id.
3. New coverage-map section rows for WASM / rizin-execution / Harmony graph,
   and Frontier updates; `l7-06` gains a same-family addendum rather than a
   re-held verb.
4. The round's `## Gate` section (`corpus/lessons/round-20.md`) records
   admit/reject per candidate so the outside spot-check
   (`LEARNING.md:42-46`) can sample the trend claim.
5. Trend verdict wording: report `expansion` from entry/evidence ground,
   not the 128→131 integer (`LEARNING.md:29`); if any admitted entry fails
   its bar, the round reports the trade explicitly.

## Commands run (with exits)

- `ls corpus/ && wc -l corpus/{QUALITY,SOURCES,README}.md; ls corpus/knowledge | wc -l` → 97 files; exits 0.
- `for v in <12 verb-name variants>; do grep -rln "$v" corpus/knowledge/ SKILL.md corpus/README.md; done` → exit 1 (empty final group); only incidental `wasm`/`rizin` hits in 4 files.
- `grep -n "wasm" … ; grep -n "rizin" …` → exit 0, matches at the anchors cited above.
- `git rev-parse main 14f0260…; git status --porcelain` → exit 2 (status truncated stream); main = `d1d981d…`, round-19 D1 scratch residue still untracked in the worktree (observation only; the fix is the tool change, not the residue).
- `git merge-base --is-ancestor 14f0260… main` → exit 0, `baseline-is-ancestor`.
- `ls .ufo/waves/round-20/tools .ufo/waves/round-20/evidence/c2` → exit 2, neither exists yet at `d1d981d` (expected pre-integration).
- `grep -n "S0NN\|rejected\|REJECT" .ufo/waves/round-20/w1/Source{WabtRelease,WasmSpec,RizinDocs,HarmonyDocs,ObjdumpDocs,Go1246,DraftQualityRows}.md` → exit 0; five `queued`/`S0NN` draft rows and one rejected candidate located.

Installs: none. Read-only; no lane writes beyond this report.
