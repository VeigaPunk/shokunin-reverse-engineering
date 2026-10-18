# CR8 (critic) — provenance attack on the receipts: timestamp/forgeability, cross-seat agreement, residual holes

Seat CR8, wave arc2-loop1-round1, 2026-10-18. Read-only except this report
(the seat's only write; scratch confined to `/tmp/arc2-l1r1-CR8-*`). All
commands below were run by this seat in this session; all `path:line`
pointers were read/re-verified this session.

## Verdict

**ATTACK FAILS — the pre-pair receipt survives both the timestamp-forgeability
and content-forgeability attacks; cross-seat agreement CONFIRMED and extended
by this seat to true post-battery (all 3 legs complete, sessions closed).**
The scope's "parent + E11 + V4 + V5" agreement is real (I re-extracted the
hash lines mechanically from their files, not their self-reports), and the
chain is now 18 capture instants across 7 seats + parent, ending with my
post-battery captures at 16:44:25Z / 16:45:32Z (after E26 leg-3 landed
16:43:55Z, `pgrep` clean). The attack's only surviving footholds are the
inherent custody limits (no pre-first-capture history; no running-client
identity) plus three clerical gaps, all named in §4. None of them falsifies
C2's zero-drift claim; the post-half receipt file and the commit are still
the parent's steps.

## 1. Target and attack model

Target: `.ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt` (4 lines,
328 bytes): `:1` timestamp `2026-10-18T14:49:13Z`; `:2` devin
`/home/vgpnk/.config/devin/mcp_config.json` sha256
`16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4`; `:3` omp
`/home/vgpnk/.omp/agent/mcp.json` sha256
`38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b`; `:4` kimi
`/home/vgpnk/.kimi-code/config.toml` sha256
`3546e033aeaf68093faf4099ea8289de5dea7ec224e7c557f08bfa9d51cf9a2a`.

Attack 1 (timestamp): the receipt's `:1` timestamp is self-asserted text — a
forger could write the file late (after the battery) and backdate line 1, so
the "pre-pair" ordering is unproven. Attack 2 (content): the receipt could
have been fabricated from a different config state than the one the battery
ran under. Attack 3 (agreement): E11/V4/V5 could be colluding reports
echoing the parent rather than independent observations.

## 2. Attack 1 — timestamp forgeability: FAILS

### E1. Receipt file-creation forensics (single write burst)

Command:
```
stat -c '%n size=%s mtime=%y ctime=%z btime=%w' .ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt
```
Observed:
```
...config-pre-pair.txt size=328 mtime=2026-10-18 11:49:13.582974229 -0300
  ctime=2026-10-18 11:49:13.582974229 -0300 btime=2026-10-18 11:49:13.582974229 -0300
```
`btime == ctime == mtime == 14:49:13.583Z` (UTC) — the file was created in a
single write burst and never edited afterward (any later edit would move
`ctime`/`mtime`; `btime` on btrfs records creation). The self-asserted `:1`
timestamp `14:49:13Z` matches the filesystem creation instant to within
0.583 s. A backdating forger would have to have created the file within that
same second — possible in principle, but then the file's *creation* still
provably precedes every battery leg (E2), which is the ordering the receipt
claims. The timestamp attack reduces to "the file could have been created at
14:49:13.583Z with dishonest content" — which is attack 2, addressed in §3.

Supporting: `stat -f` shows `fstype=btrfs` for both the receipt and the
configs (same filesystem family for all four paths). Wave dir and `receipts/`
dir `btime` = `2026-10-18 11:49:13.580974220 -0300`, i.e. 2 ms before the
receipt file — a single `mkdir -p` + write sequence, no room for a hidden
earlier/later artifact in that directory.

### E2. Ordering: receipt predates every battery leg and every seat report

- Leg 1 (`doctor`): capture mtime `2026-10-18 11:51:50.786984442 -0300` =
  `14:51:50Z` — `E24.md:20`. Receipt is 2m37s earlier.
- Leg 2 (census): server `started_at` `2026-10-18T14:53:21.522Z` embedded in
  the captured JSON-RPC response — `/tmp/arc2-l1r1-E25/binary-session-call.json:2444`
  (= `E25.md:5`). Receipt is 4m8s earlier.
- Leg 3 (libjq): run window ~`13:40–13:42 -0300` = `16:40–16:42Z` — `E26.md:3`;
  `E26.md` mtime `2026-10-18 13:43:55 -0300` = `16:43:55Z`. Receipt is ~1h51m earlier.
- Earliest seat-report mtime in the wave dir (observed this session): `V4.md`
  `11:52:51 -0300` = `14:52:51Z`. Receipt is 3m38s earlier.
- Live process observation: `pgrep -af '[r]ea.mjs'` at `16:40:56Z` caught leg
  3's server in flight (pid 1894652, `--mcp`); by `16:41:50Z` the pid was
  gone; at `16:44:22Z`/`16:45:32Z` `pgrep` exit 1 (no REA process). Consistent
  with E26's reported clean closure; no orphan.

So the file's *existence* at `14:49:13.583Z` is filesystem-verified, and that
instant precedes all three battery legs and all delivered seat reports.

## 3. Attack 2 — content forgeability: FAILS (no-write window + 8-way agreement)

### E3. No config write occurred in the entire window — the capture instant collapses

Commands (this seat, five capture instants: 16:39:38Z, 16:40:56Z, 16:44:00Z,
16:44:25Z, 16:45:32Z):
```
sha256sum ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json ~/.kimi-code/config.toml
stat -c '%n size=%s mtime=%y ctime=%z btime=%w' ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json ~/.kimi-code/config.toml
```
Observed (identical every time):
```
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json
3546e033aeaf68093faf4099ea8289de5dea7ec224e7c557f08bfa9d51cf9a2a  /home/vgpnk/.kimi-code/config.toml
```
mtimes: devin/omp `2026-10-14 17:53:20 -0300` (= `2026-10-14T20:53:20Z`), kimi
`2026-10-18 11:45:57 -0300` (= `14:45:57Z`), ctime/btime consistent
(kimi btime `11:45:57.649`, ctime `.910` — one rewrite burst). All config
mtimes are *older* than the receipt (`14:49:13.583Z`) and older than every
capture in the window `[14:45:57Z, 16:45:32Z]`. **No config was written during
the window**, so every capture — parent, E11, V4, V5, R7, E27, E26, mine —
necessarily observed the same bytes. The receipt's content is not merely
"true at 14:49:13Z" but true across the whole battery window: the distinction
between the claimed capture instant and any other instant collapses.

### E4. Mechanical diff, receipt vs live, post-battery

Commands (final, at `16:45:32Z` — after E26 leg 3 landed and sessions closed):
```
tail -n +2 .ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt | diff - <(sha256sum ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json ~/.kimi-code/config.toml)
```
Observed: `FINAL diff exit: 0`, empty output (byte-identical). Same result at
`16:44:00Z` and `16:44:25Z` (scratch
`/tmp/arc2-l1r1-CR8-receipt-hashes*.txt`, `/tmp/arc2-l1r1-CR8-post-battery-hashes.txt`).

### E5. Receipt artifact self-hash reproduced

Command: `sha256sum .ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt`
Observed: `7369fbcb3bfd91cf5bdf48d0871ae670bce133d5d091a35e8fd7826c0cef04e4`
— identical to the pins at `E11.md:76` and `V5.md:67`; 328 bytes, and byte
accounting closes exactly (lines 20+107+97+100 bytes + 4 LF = 328; file ends
with a single LF). All seats compared against the same artifact identity.

### E6. Cross-seat agreement re-derived mechanically (not trusted from self-reports)

This seat re-extracted the hash lines from the other seats' files and diffed
them against the receipt and against the live capture:

Commands (excerpt):
```
sed -n '15,17p' .ufo/waves/arc2-loop1-round1/E11.md | awk '{print $1}'
sed -n '17p;20p;23p' .ufo/waves/arc2-loop1-round1/V4.md | awk '{print $1}'
sed -n '17,19p' .ufo/waves/arc2-loop1-round1/V5.md | awk '{print $1}'
sed -n '39,41p' .ufo/waves/arc2-loop1-round1/R7.md | awk '{print $1}'
sed -n '11,13p' .ufo/waves/arc2-loop1-round1/E27.md | awk '{print $1}'
sed -n '93,95p' .ufo/waves/arc2-loop1-round1/E26.md | awk '{print $1}'
```
Observed: every extraction is the identical ordered triple
(`16f496e6…`, `38d2a1d0…`, `3546e033…`) matching the receipt `:2-4` and my
live captures. Capture events verified: parent `14:49:13Z`; E11 `14:52:07Z`
(`E11.md:15-17`); V5 `14:52:33/14:53:08/14:53:38Z` (`V5.md:17-19`, plus
openssl second method); V4 `14:52:34Z` (`V4.md:17,20,23`); R7
`14:53:07/14:54:55Z` (`R7.md:39-41`); E27 four captures
`16:38:59–16:39:53Z` (`E27.md:11-13, :22-24, :31-33, :66-68, :81-83`);
E26 post-battery `16:41–16:42Z` (`E26.md:93-95`); CR8 (this seat)
`16:39:38–16:45:32Z`. That is **18 capture instants across 7 seats +
parent** (E11 1, V4 1, V5 3, R7 2, E27 4, E26 1, CR8 5) — the scope's
"parent + E11 + V4 + V5" four-way is confirmed as a
subset, not merely restated.

Collusion counter: the same triple is *independently re-derived from the live
files* by this seat at five instants spanning the entire window, and the
no-write window (E3) means any colluding echo would have to match a state that
any honest capture also matches. The attack has no room to distinguish.

### E7. Whole-wave divergence scan — zero divergent hash lines

Command (python, this session): scan every `.ufo/waves/arc2-loop1-round1/*.md`
for lines containing a config path plus a 64-hex token; classify each against
the expected value. Observed: `mcp_config.json` 26 matching occurrences, `omp`
26, `kimi` 25; **zero divergent full-hash occurrences** on config-path lines.
Two scanner false positives were closed: `SC2.md:61` is a single line
containing all three *correct* hashes; `R3.md:103`'s 64-hex is the self-hash of
R3's own 328-byte scratch file `/tmp/arc2-l1r1-R3/reverify.txt` (verified:
`5be2d202…`, and its `diff` vs the receipt differs only in line 1's timestamp
— `16:41:57Z` vs `14:49:13Z`). Whole-dir grep for the receipt timestamp
variant: 34 occurrences, all `14:49:13Z` (no rival timestamp anywhere).

### E8. Raw /tmp artifacts re-hashed — cited hashes are current

- E25: `sha256sum /tmp/arc2-l1r1-E25/*` — all 5 files match `E25.md:79`
  (`binary-session-call.json c5fae8e4…`, `tools-list.json 94a56cd2…`,
  `close-binary-call.json 31b3102b…`, `server-stderr.log 4292c60b…`,
  `mcp-census.mjs 492cf2be…`).
- E24: `/tmp/arc2-l1r1-E24-doctor.out` sha256 `0f48f419…` and empty
  `.err` `e3b0c442…` match `E24.md:20-21`.
- E26: `rea-evidence-bundle.json a1194382…` (`E26.md:27,:53`),
  `mcp-instr-117070.json cb60760d…` (`E26.md:48`), `mcp-get-bundle.json
  4545895f…` (`E26.md:50`); decoded bytes verified in the raw JSON:
  `"address":"0x117070" … "bytes":"f30f1efa" … "mnemonic":"ENDBR64"`.

These artifacts live in /tmp (mutable by anyone), so their hashes pin current
state, not history; the report mtimes (14:51–14:56Z, 16:43:55Z) and embedded
server timestamps (`binary-session-call.json:2444`) are consistent with the
claimed run windows, which is as far as any critic can go without the
instruments themselves being tamper-evident.

## 4. Residual holes (ranked)

1. **No post-pair receipt file yet** (`config-post-pair.txt` absent at
   `16:45:32Z`; `ls receipts/` → `config-pre-pair.txt` only). C2's post-half
   now *can* be closed: all 3 legs are complete (E24, E25, E26 all landed),
   no REA process remains (`pgrep` exit 1), and this report carries a true
   post-battery capture + diff exit 0 (E4) the parent may use as raw material
   — though the parent's own capture at integration time is preferable.
   Note: E27's draft receipt (`E27.md:66-84`) is explicitly labeled
   "post-legs-1&2, pre-leg-3" — **now stale**; if landed as-is its label
   understates coverage, and if relabeled without a fresh capture it remains
   a mid-battery capture. Parent should re-run the 1-line capture post-E26.
2. **Receipts untracked**: `git status --short` → `?? .ufo/waves/arc2-loop1-round1/`
   (whole dir; verified `git check-ignore` exit 1 — not ignored, just
   uncommitted). C2's "receipts committed" clause is not yet true; durability
   precedent (luna-round-6/8 committed bundles) unmet until the parent commits.
3. **Pointer defect, minor**: `E24.md:33` cites
   `receipts/config-pre-pair.txt:1-5` on a 4-line file (328 B, `wc -l` = 4,
   trailing LF; a `:1-5` range overruns to an empty line 5). Other seats cite
   `:1-4` correctly (`E14.md:46`, `E23.md:17`, `R7.md:34`, `S2.md:53`,
   `V4.md:27`). Cosmetic; fix or note at integration.
4. **Inherent custody limits (not defects, must land as limitations)**: hash
   custody cannot exclude mutate-and-revert *before* the first capture (the
   pre-14:49:13Z history of the configs is unprovable by this instrument —
   already named at `R7.md:15` from BC3's threat list); and the pair proves
   byte-identity of the 3 named files only, not that the battery *ran under*
   those configs (legs launched via explicit `@6.5.0` pin / bare `npx`, not
   via the configured clients — `R3.md:5`). Both belong in the round report's
   limitations; neither falsifies zero drift.
5. **Observed, not a hole**: kimi `config.toml` was rewritten at
   `14:45:57Z`, 3m16s *before* the pre-pair (re-verified mtime) — the receipt
   correctly froze the post-rewrite state; the receipt cannot certify the
   earlier 6.4.0→6.7.0 pin history (owned by SC2/R3).

## 5. Text for the parent to land VERBATIM (if desired)

Post-battery capture (CR8, this session — the parent's own capture should
supersede this if taken at integration):

```
2026-10-18T16:45:32Z
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json
3546e033aeaf68093faf4099ea8289de5dea7ec224e7c557f08bfa9d51cf9a2a  /home/vgpnk/.kimi-code/config.toml
```

Zero-drift verdict text for the round report / LOG (C2):

```
C2 zero-drift verdict (post-battery): 0/3 files drifted. All three client-config
sha256s byte-identical to config-pre-pair.txt:2-4 (`diff` exit 0, empty output;
`sha256sum -c` = 3 OK in E27's run). Captured by CR8 at 2026-10-18T16:45:32Z —
after leg 3 (E26) landed and all sessions closed (`pgrep -af '[r]ea.mjs'` exit 1).
Agreement chain: 18 capture instants across 7 seats + parent (parent 14:49:13Z;
E11 14:52:07Z; V4 14:52:34Z; V5 14:52:33/14:53:08/14:53:38Z; R7 14:53:07/14:54:55Z;
E27 16:38:59-16:39:53Z (4 captures); E26 16:41-16:42Z; CR8 16:39:38-16:45:32Z (5 captures)) — all 3/3
byte-identical; receipt artifact sha256 7369fbcb… reproduced by E11, V5 and CR8.
No config write occurred in [14:45:57Z, 16:45:32Z] (mtimes), so the receipt's
content is true across the whole battery window, not just at its capture instant.
Limitations: hash custody cannot exclude mutate-and-revert before the first
capture; byte-identity of the 3 named files only; no running-client identity.
```

## 6. Conclusions (labeled)

- **OBSERVATION**: receipt file has `btime == ctime == mtime == 14:49:13.583Z`,
  matching its self-asserted `:1` timestamp to sub-second; single write burst,
  never edited; created 2 ms after its parent dir; on btrfs (E1).
- **OBSERVATION**: the receipt file provably predates leg 1 (`E24.md:20`,
  14:51:50Z), leg 2 (`binary-session-call.json:2444`, 14:53:21.522Z), leg 3
  (`E26.md:3`, ~16:40–16:42Z), and the earliest seat report (V4, 14:52:51Z) (E2).
- **OBSERVATION**: all three config mtimes predate the receipt and no config
  was written through 16:45:32Z; five CR8 captures + mechanical diff (exit 0)
  + receipt self-hash `7369fbcb…` all reproduce (E3–E5).
- **OBSERVATION**: hash lines mechanically re-extracted from E11, V4, V5, R7,
  E27, E26 all equal the receipt `:2-4` and the live files; whole-wave scan
  found zero divergent hash lines (26/26/25 path-plus-hash occurrences, 2
  false positives closed) (E6–E7). Raw /tmp artifacts for E24/E25/E26 re-hash
  to their cited values (E8).
- **INFERENCE**: attacks 1–3 fail. The receipt is timestamp-credible (file
  creation verified, ordering proven), content-true (no-write window makes
  capture instant irrelevant), and the agreement is 8-seat-wide (7 seats +
  parent), not 4-way — and
  now includes true post-battery captures, so the same instrument that
  verified the pre-half also shows the post-half holds at 16:45:32Z. C2's
  zero-drift claim is sound as written for the 3 named files.
- **UNKNOWN**: whether the parent will take its own post-battery capture or
  reuse CR8's/E27's (either closes the post-half; E27's draft needs a relabel);
  whether the receipts will be committed before round close; the pre-14:49:13Z
  config history (unprovable by hash custody, by construction); whether any
  deeper config-registration surfaces changed (outside the 3 named files and
  outside this seat's scope).

## 7. Scope compliance

Read-only on configs (sha256sum/stat only; contents never read), read-only on
all repo files except this report, no git mutations, no installs, no network,
scratch confined to `/tmp/arc2-l1r1-CR8-*`. LOG.md/SCORECARD.md entries are
the parent's integration step (AGENTS.md rule).
