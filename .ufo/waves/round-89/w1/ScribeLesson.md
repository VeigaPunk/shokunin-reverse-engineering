# ScribeLesson — round-89 lesson draft and QUALITY rows (kaidoku)

Seat `ScribeLesson` (scribe, leaf — no subagent dispatch). Lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, round 89, L1 `KaidokuR89`. Base `0ec2bb4016655f605657d6e0e700ec2e6893ac27`.

**Deliverables.** `w1/ScribeLesson/quality-rows.md` (QUALITY rows 161-169) and
`w1/ScribeLesson/report.md` (full evidence, §-numbered commands with exit codes, and the
seat-attribution table). This file is the seat trailer.

**Behaviour.** Three lesson rows drafted from findings this seat verified itself, all against the
frozen round-89 instruments, plus one row from a wave receipt:

- **M89-8 / QUALITY 166 — the round-89 repair dropped the round-88 guards and its refusal
  contract, and `N1-refuse-plain` passes on the crash.** The round-88 repair refuses a non-regular
  `--in` (FIFO, `/dev/zero`) and a plain original with a typed rc 2; the round-89 repair hangs on a
  FIFO (exit 124 at 5 s), raises `MemoryError` on `/dev/zero`, and lets the round-87 module's
  `Refused` escape as an uncaught traceback (rc 1) because it defines its own `Refused` class
  (`tools/round-89/upx-field-value-repair.py:46`) and never converts the upstream one in `derive()`
  (`:65`). The counter's refusal control asserts `rc != 0`
  (`tools/round-89/upx-field-battery.py:287`), so the crash satisfies it: the two pre-freeze
  receipts both report `N1-refuse-plain: true` at `rc 1` (round-89 repair) and `rc 2` (round-88
  repair) respectively.
- **M89-9 / QUALITY 167 — the `isolation` control observes a pre-run snapshot, not the
  invocation.** `tools/round-89/upx-field-battery.py:180` lists the box *before* the child starts.
  ReviewerC1's carrier-read cheat, re-run verbatim by this seat, scores `recovered 4 of 4`,
  `controls_ok` all true, `met_target true`, **exit 0** (244 s). The kill-rule clause "a repair
  that names, reads or hashes a carrier source path or pin" — which round 88's D4 already called
  audit-only — is still audit-only.
- **M89-10 / QUALITY 168 — the `u_len` accounting bound is a rank key, not a filter.**
  `tools/round-89/upx-field-value-repair.py:95` computes `key = (total <= u_len, total, -derived)`,
  so an over-`u_len` candidate is outranked, not rejected. On a scratch copy with `u_len` forced
  to 1 (the frozen file untouched) the repair exits 0, reports `fits_u_len = False` with
  `uncompressed_accounted = 30800`, and writes the correct output.
- **M89-11 / QUALITY 169 — the refusal string varies by carrier within one class, and rc 0 is not
  recovery.** From ExecMatrix's 48-cell matrix: `b0.sz_cpr:=sz_unc+1` answers `header corrupted` on
  jq/xxd/dinit and `corrupt b_info` on libz; `b0.method^=0xFF` and `p_info.p_blocksize^=0xFF` exit 0
  with class `intact` on files `upx -t` still refuses.

**Gates.** The three frozen instruments' own selftests pass (`depth-blocks-v2` 10 cases, repair 16,
battery 9; all exit 0), all seven instrument sha256s equal the pins in `claims.json`, the sources
census validates exit 0 (29 W04, one new: S311 vs S307, same URL at a different scope), and the
depth counter is red at the base (exit 1), green at the landed tip (exit 0), refuses to run without
`--expect-blocks` (exit 2) and red on a wrong target (exit 1).

**Round-88 spot-check defects D1/D3/D4 — status.** D1 (docstring-vs-code) is in the lane's
existing M89-2 and QUALITY 162; the frozen round-88 bytes are unchanged, as they must be. D3
(target-blind counter) is fixed by `depth-blocks-v2.py` and re-measured: the round-88 counter still
reports `met_target true` / exit 0 at the round-89 base, while v2 is red there, refuses to run
without `--expect-blocks` (exit 2) and is red on a wrong target (exit 1). D4 (answer beside the
input) is fixed by the round-89 battery's private-per-invocation directory, and the A/B is
**measured with one cheat against both counters**: round 88's own `sibling-repair-v2.py` scores
`met_target true` / **exit 0** with all controls true under the round-88 battery (179 s) and
`recovered 0 of 4` / exit 1 under the round-89 battery (147 s).

**Gate.** This seat opened no URL. The lesson's `## Gate` rows are transcribed from
**ScoutUpxSrc's** fetch receipts (`w1/ScoutUpxSrc/receipts/fetch-sha256.tsv`, status/bytes/sha256
for all eleven files it fetched) and are quoted with attribution in `w1/ScribeLesson/report.md` §3.
One disagreement is recorded rather than smoothed: ScoutUpxSrc's §3 states that `src/packhead.h`
contains no `b_info` at all and that the NE32 `p_info` copy (`p_unix.h:126-130`), not the LE32
copy at 200-204, is the one the carriers instantiate — while the lane's working-tree S312 row
anchors the LE32 copy. The URL and sha256 agree; the scope needs the L1's attention.

**Touched surfaces.** `w1/ScribeLesson/quality-rows.md`, `w1/ScribeLesson/report.md`,
`w1/ScribeLesson.md`, and the scratch tree `/fast/scratch/hyaku/kaidoku-r89/ScribeLesson/` (deleted).
No lane file was modified: `corpus/lessons/round-89.md`, `corpus/QUALITY.md`, `SKILL.md`,
`PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` and `claims.json` are untouched by this seat.

**Out of scope.** No source was opened by this seat, so the lesson's `## Gate` carries a skeleton
only — the access date and the located quote must come from the L1's fetch record and
ScoutUpxSrc's independent fetch. The `## Mistakes` rows M89-1…M89-7 and QUALITY 161-165 already in
the working tree are the L1's integration pass, reproduced verbatim in `quality-rows.md` and not
claimed by this seat.

**Findings routed to the L1.** (1) The round-89 repair's regression against the round-88 guards
(M89-8) — **the L1 has since fixed this in the working tree** (see the drift note below); the next
revision must also make the counter's refusal control assert the declared exit code, not merely
"non-zero". (2) The carrier-read cheat passing `met_target true` under the round-89 battery
(M89-9) — **still live**: the counter is unchanged (`f6f5ed61…`), so the round-89 counter, like the
round-88 one, does not force the *provenance* of a repair; round 88's D4 audit-only clause stays
audit-only. (3) The `u_len` bound is weaker than the law words it (M89-10) — **now documented in
the new docstring** ("`fits_u_len` is a *rank key, not a filter*"), which is a legitimate
resolution of the wording; re-measured on the new bytes, the repair still writes a value when no
candidate fits (`fits_u_len = False`). (4) ReviewerC2's MED note that
`w1/ExecMatrix/matrix.json` "does not exist yet" is stale — the file exists (68,246 bytes,
mtime 21:50). (5) `corpus/SOURCES.md`'s S311/S312 rows and the round-89 knowledge entry are in the
working tree but **not committed** at the time of writing.

**Blocker — the frozen repair no longer matches its pin.** At 22:09:10 the L1 modified
`tools/round-89/upx-field-value-repair.py` in the working tree (sha256 `332917f2…1070` →
`664b973a3fb129f5920a4f583fee3810183f54a082841c77ba67039332285c37`, +77/−6), and the diff's own
comments name this seat's M89-8. **Every measurement in this seat's report was taken before
22:09:10 and therefore ran against the pinned bytes**; the two counters and the three
round-87/round-88 instruments are unchanged. Re-tested on the new bytes, M89-8 **is fixed**
(plain original, FIFO and `/dev/zero` all now exit 2 with a typed refusal, where the pinned bytes
gave a traceback, a hang and a `MemoryError`).

**Update, 22:10:39 — the L1 committed it** (`7edab6ae5`): the container now carries an
`instrument_supersessions` row for the repair with `superseding_sha256 = 664b973a…`, a reason
naming the three defects, and `retaken_before`; the re-taken receipts carry `repair_sha256
664b973a…`, `met_target true`, exit 0. **One residual inconsistency remains for the L1 to close:**
the container's `instruments` map still pins the *superseded* `332917f2…1070`, and the claim's
kill rule reads "a receipt whose `repair_sha256` differs from the frozen pin" — so read against
that pin, every receipt of the round differs from it. Fix: point the `instruments` pin at
`664b973a…` (or amend the kill rule to read the supersession's `superseding_sha256`), and fill the
two `"commit": "pending"` fields with `7edab6ae5`. `claims.json` is out of this seat's write
scope and was not edited.

**Commits.** None. No git or jj mutation of any kind was run: only `log`, `status`, `show`,
`diff`, `rev-parse`, `cat-file`, `ls-files`.

**Tooling.** No tool installed or upgraded (`/home/vgpnk/.omp/agent/RULES.md` read this round);
`pacman` untouched per the host-wide pause; nothing written to any PATH directory.
