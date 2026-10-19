# arc3-loop1-round3 — wave summary (VZ-4, wave-integrator)

Seat VZ-4 | chain cross | role wave-integrator | wave `arc3-loop1-round3`, 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (immobile at every sample — seats do
not commit). Wave dir created 13:03Z; `claims-frozen.md` frozen pre-dispatch (64 seats
enumerated 24+24+12+4); this seat's first sample 13:06:44Z.

This seat wrote only this file, `claims/cross/VZ-4/*` (harnesses, captures, poll and
revision logs) and `seats/VZ-4.md`. No git mutation, no custody write (read-only
sha256/stat capture only; the custody tool was exercised from scratch copies), no
install; scratch under `/var/tmp/vz4r3` (`/tmp` untouched — standing EDQUOT record).
The receipted round-1 solc prefix was *reused*, never reinstalled.

**Method.** A 60 s poller of `seats/` (30 checks, `claims/cross/VZ-4/poll-log.txt`), a
20 s real-target watcher for the three worktree targets (`revisions.log`), a mechanical
roster census (`roster-census.py`, roster parsed from `claims-frozen.md:103-116`), and
three purpose-built harnesses run at my own hand: `c1-harness.sh` (independent
optimizer-enabled carrier compiled with the receipted solc + probed with the pinned
REA), `c2-attacks.sh` + `c2-verify.sh` (the four named holes + after-state suite on
*scratch copies*), `c3-probe.sh` (entry count, digest pin, selftest, HEAD run in both
modes), plus `mirror-root.sh` + `commandA.sh` (recipe A in git mode and tree mode over
a scratch mirror) and `seat-digest.py` (per-seat report digest). Every number below is
bound to a sha256 or a command output; every artifact identity I quote was re-derived
by me, not copied from a seat report.

## 1. Seats delivered vs the frozen roster

_Roster source `claims-frozen.md:103-116`; census `python3 .ufo/waves/arc3-loop1-round3/claims/cross/VZ-4/roster-census.py`._

**Census at the last check of this seat's poll window (13:15:03Z): 21/64.** See §1a for
the final count taken when this summary was written.

- C1 chain **13/24** (undelivered: EX-02, EX-03, EX-09, EX-14, SC-2, RV-1, RV-2, RV-3,
  CR-1, CR-2, VZ-1) — the chain's work was far ahead of its reports.
- C2 chain **4/24** (undelivered: PL-2, EX-21, EX-23, EX-24, EX-26, EX-27, EX-29, EX-30,
  EX-31, EX-32, EX-33, SC-3, SC-4, RV-5, RV-6, RV-7, RV-8, RV-9, CR-3, VZ-2).
- C3 chain **3/12** (undelivered: PL-3, EX-42, EX-44, EX-45, EX-46, RV-11, RV-12, CR-5,
  VZ-3).
- Cross **1/4** (undelivered: CN-1, CN-2, VZ-4 — this seat's own report lands last by rule).
- No stray seat files, no zero-byte seat reports at any check.
- The wave was still in flight when this seat's poll budget closed (see §7). Seat files
  appear in `seats/` only when a seat closes its report, so the artifact tree (792+
  files under `claims/` by 13:10Z) was far ahead of the report census — the r1-shaped
  gap (artifacts ahead of reports) recurred by the time the budget closed.

### 1a. Closing census

_Filled at write-out time — see the closing census block appended below._

## 2. Per-chain verdicts

### C1 — coverage (owned): optimizer-enabled + non-ERC-20 carriers — **SUBSTANCE REPRODUCED first-hand; landing is a verified projection**

What I measured myself, not what the seats say:

1. **The receipted solc prefix is genuine and works** (reuse clause): `solcjs --version`
   from `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/.bin/` reads
   `0.8.37+commit.f401782d.Emscripten.clang`, and the prefix's `soljson.js` hashes
   `221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c` — the exact
   digest the round-1 install receipt records for both trees (`EX-02/install-receipt.txt`
   §6; tarball sha256 `0e1a1ab6…575a51`). No install was run by me.
2. **An independent optimizer-enabled, non-ERC-20-shaped carrier survives the extractor.**
   I compiled my own `VzPayable` (standard-JSON, optimizer enabled, runs 200; payable
   `receive()` + payable `fallback()`; mixed mutability; an internal library call;
   1,103-byte runtime) with that prefix and probed it with `rea-agents@6.4.0` under a
   disk-backed `TMPDIR`: **9/9 planted selectors, zero missing, zero extra**,
   `dispatch:"abi"`, mutability set `{nonpayable, payable, view}`, evidence
   `ev_811cdebf…`, decoded bytecode sha256 `7b2b4803…`.
3. **The chain's own carrier reproduces under my hand.** EX-04's `carrierB` (VaultB
   multisig shape, optimizer 200, K=11, no ERC-20 selectors) re-probed by me with
   `rea-agents@6.4.0`: **11/11 both legs** — hex `ev_fc573e7d…`, raw `ev_bc7f5a61…`,
   zero missing / zero extra on both, decoded bytecode sha256 `aaf85cea…` on both,
   equal to the on-disk runtime `.bin` digest `aaf85cea…`.
4. **Command A before → after.** At HEAD (git mode) and over an unpatched mirror (tree
   mode) identically: `knowledge_files 82, mapped 82, missing [], dangling [],
   citation_resolved_rules 14, rule_blocks 14, coverage 10.0, depth 10.0`. Over the
   mirror with the chain's landing drafts applied (§4.1): **`knowledge_files 83,
   mapped 83, missing [], dangling [], 14/14, 10.0/10.0`** — the claim's 82 → 83 with
   the prior 82 tokens untouched (the map row is line-neutral, 190 → 190 lines, README
   after-sha `016b632e…`). RV-4's independent application of its own patch text lands
   the same README digest `016b632e…` — two independent applications, byte-identical.

Caveats, named: the after-state is a **projection on a scratch mirror**, so rule #14
applies at landing (re-derive the entry bytes, the README digest, and re-run command A
at the records commit). The entry draft I projected was `records-drafts/knowledge-entry-draft.md`
sha256 `5c1818c7…` (identical to SC-2's copy), stem `2026-10-19-arc3-r3-evm-optimizer-shapes`,
37 lines / 17,563 B / `189ac2a2…`; the map patch `333ca590…`. Both are DRAFTS — the
parent must land the final revision's bytes, not these pins.

### C2 — operability (fleet): custody-pair hardening — **ALL FOUR NAMED HOLES REPRODUCED AS DECLARED CLASSES at the revision I measured**

I ran the four injections and the after-state suite myself against *scratch copies*
(never the real target, never a custody write).

| Injection | Before (my 13:08Z run at `7b848eaf…`, and r2's verdict at `112d01dc…`) | After (my 13:14:52Z run at `7cd19c3c…`, 1155 L) |
|---|---|---|
| D2 EACCES: capture over an unreadable file | raw `PermissionError` traceback, exit 1 | **exit 14** `UNEVALUABLE`, declared; receipt still written |
| D2 EACCES: `verify --live` over an unreadable candidate | raw traceback exit 1 | **exit 14** (declared class) |
| D2 both-sides plain-absent verify | `MATCH exit 0` (`compared=0/11`) — the fail-open | **still `MATCH exit 0`** — by the tool's declared design (only error-carrying stanzas are UNEVALUABLE) — *flag for the parent, §7* |
| D3 1-of-5 receipt vs live, no gate | `MATCH exit 0 paths=1/1` | `MATCH exit 0` (gate is opt-in) but `--require-paths 5` → **exit 2**, `REFERENCE-COVERAGE: 1/5 … unaccounted: [4 paths]` |
| Write-guard: `capture --paths X --out X` | **clobbered X** (`c7136f57…` → `e50a7f9b…`), exit 0 | **refused, exit 2, victim bytes intact** (`c7136f57…` unchanged before/after) |
| Write-guard: `--out ~/.bashrc` (canonical) | refused exit 2 | refused exit 2 |
| D6 `selftest --scratch <missing>` | `FileNotFoundError` traceback, exit 1 | **exit 2 USAGE** (declared) |
| selftest | (not runnable at my scratch path — canonical-filename caveat, below) | **21/21 CLEAN exit 0** |

After-state suite at `7cd19c3c…`: live capture **5/5 exit 0**; the receipt **self-pins
the tool's sha256** (header vs computed: match); `verify <my receipt> --live` →
`MATCH 5/5 drift=0 exit 0`; a v1 sums-form receipt → `MATCH-V1-PARTIAL 5/5`,
`SHA256-CONTRACT 5/5`, exit 0; the round-1 canonical **v1 stanza** → exit 10 with 4×
`LABEL-DEFECT` reproduced and `SHA256-CONTRACT 4/5` (the one mismatch is the drifted
`config.toml`, §3 — operator-side, pre-window).

Caveats, named:

1. **Revision churn.** The tool was rewritten continuously through my window:
   `112d01dc…` (r2's landed revision, 13:07:31Z) → `7b848eaf…` (13:08:15Z) →
   `68e30768…` (13:08:32Z, 918 L) → `a611ede4…` → `03bd6242…` (1109 L) → `89bfebec…` →
   `7cd19c3c…` (1155 L, 13:13:49Z) with further revisions observed by CR-4
   (`57dffff1…`, `dc841464…`, `ec2b2d48…`). Every number above is bound to the sha256
   I measured it at; the parent must re-derive at the committed revision and record
   which one moved. The README was rewritten several times inside the window too
   (`fa484d57…` → `039993ed…` → `752032cf…` → `83f07f83…` → `f30df42e…`).
2. **My scratch-copy selftest caveat:** the tool's own selftest re-invokes itself by
   *canonical filename* (`custody-pair.py:839`), so a scratch copy under a different
   name makes the TZ-independence case fail spuriously. My suite copies as
   `custody-pair.py`; at that path the mid revision read `CLEAN 21/21`. A parent
   re-running the suite should keep the canonical name.
3. **The round's live pre-pair was captured with the PREVIOUS revision** (`EX-29`'s
   `claims/c2/receipts/config-pre-pair-v2r3.txt`, tool `112d01dc…`, 13:06:57Z). I
   verified it against live myself: `MATCH 5/5 exit 0`. The post side must be captured
   with the landed revision; if the claim's wording "captured by the revised tool" is
   read strictly, the pair spans two revisions (payloads comparable — r2 precedent).
4. **The README patch text (`EX-30/readme.patch.md`) is superseded**: it targets base
   `fa484d57…` while EX-21's revision already carries every semantic element it proposes
   (verified by grep: `UNEVALUABLE`, `require-paths`, `hardlink`, `REFERENCE-COVERAGE`,
   `never /tmp` all present). The registry-row patch (SKILL.md) **does** apply cleanly to
   the current SKILL.md (`patch -p1 --dry-run` OK) — the parent should land that one and
   skip the README one, or re-base it.

### C3 — freshness (fleet): citation-drift pointer table — **LANDED STATE MEASURED GREEN at every sample; the coupled pin held through the write**

- Before: **31 entries / 4 quoted**, table sha256 `738b3a56…`, expected pin matched, probe
  selftest 13/13, HEAD findings 0 in both modes (my 13:09:08Z run).
- After (EX-41's landing, first seen by me at 13:13:10Z and stable in every later sample):
  **57 entries / 4 quoted** (26 added; `entries` prefix equal, `quoted` unchanged, `_doc`
  prefix preserved — EX-41's additive proof, which matches what I see on disk), table
  `bfc42f1b…` (30,348 B), `expected.json` re-pinned to it (`d97dd60a…`), probe
  `e2665074…` unchanged.
- My re-run of the probe at that state (`c3-probe.sh`, disk-backed TMPDIR): **pin MATCH,
  selftest `cases=13 passed=13 failed=0 exit=0`, HEAD default run `findings=0 exit=0`,
  `--strict` run `clean findings=0 exit=0`.**
- **Cross-chain interference checked**: C3's new entries anchor into
  `.ufo/gates/custody-pair/README.md`, the very file C2 kept rewriting
  (`fa484d57… → f30df42e…`). All such entries are `anchor`-kind with no pin line, so the
  probe stayed **findings=0** across C2's revisions — measured, not assumed. (A
  line-pinned form would have gone RED; the design choice is what saved it.)
- EX-43's before-state census artifacts reproduce under my hand: their scratch extension
  table `.ufo/.../EX-43/scratch-table-ext.json` hashes **`0b01f521…`**, exactly the
  digest their artifact claims (48 entries / 5 quoted), and their teeth control flips
  one needle to `citation_dead exit=1` (the instrument is non-vacuous).

Caveats: the table I measured is **uncommitted** (`?? .ufo/gates/citation-drift/` is
tracked, but the edits are worktree mods — `git status` reads ` M pointer-table.json` +
` M expected.json` per EX-41). The acceptance test the freeze names is the arc3-citation
*census* (covered-or-adjudicated), not the count; EX-43's census (candidates + NO-ENTRY
adjudications with causes) plus EX-41's landed entries are the chain's answer, and my
independent spot-checks of the entry→target resolvability found no dead pointer (the
probe resolved all 57 at HEAD with 0 findings, which is the strongest available check).

### Cross

- **CU-1** — custody corroboration: PRE-side corroborated (their independent raw capture
  + tool-side grades; their `write-guard-attack*.out` battery under a fake `HOME`, which
  corroborates my own clobber finding and the fix). Their r2-post vs r3-pre diff is the
  cleanest statement of the config drift (§3), and I reproduce it: 4/5 paths MATCH
  16/16 fields, `config.toml` moved 11/16. Post-side section was pending at their write.
- **CN-1 / CN-2** — not delivered at the census time of this draft; see §1a.
- **VZ-4** — this file + `seats/VZ-4.md`.

## 3. Custody outcome

**5 paths read-only throughout; 4/5 byte-identical to round 2; the fifth (`config.toml`)
drifted BEFORE this wave opened — operator-side, recorded, not repaired.**

My pre capture (13:06:44Z, read-only sha256+stat) vs round-2's canonical close:

```
16f496e6…  ~/.config/devin/mcp_config.json   unchanged (mtime 1792011200, inode 11341318)
38d2a1d0…  ~/.omp/agent/mcp.json             unchanged (mtime 1792011200, inode 11341316)
bc66d543…  ~/.kimi-code/config.toml          MOVED vs r2's 8cbacd48… (mtime 1792414665
                                             = 2026-10-19T12:57:45Z; inode 34530637 → 37793921;
                                             mode 600 → 640; size 114434)
7d2ca28a…  ~/.bashrc                         unchanged (mtime 1792168396, inode 25991953)
6c6be761…  ~/.profile                        unchanged (mtime 1792044727, inode 40274)
```

The drift timestamp (12:57:45Z) precedes this wave's first sample (13:06:44Z) and CU-1's
pre-pair (13:06:57Z) independently records the same moved fields — so it is the standing
operator-side interactive-session churn class the r2 record already carries, not a
round-3 lane event. My tool-captured pre-pair (`vz4-pre.json`, tool `7cd19c3c…`,
13:13:5xZ, label `vz4-r3-pre-midwave`) and EX-29's pre-pair both verify `MATCH 5/5
drift=0 exit 0` against live at my measurement time.

## 4. Parent-facing admission-recommendation inputs

1. **C1 — admit conditional on landing a verified projection.** Land (a) the new entry
   file `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md` from the FINAL
   revision of `claims/c1/records-drafts/knowledge-entry-draft.md` (the literal text
   between the BEGIN/END LITERAL ENTRY TEXT markers), and (b) the line-neutral EVM row
   replacement in `corpus/README.md` from `map-token-patch.md` (PRIMARY form; the
   HONEST-STOP variant is not needed — the optimizer legs recovered K/K, measured by me
   on both the chain's carrierB and my own carrier). At the draft revision I projected:
   entry 37 lines / 17,563 B / `189ac2a2…`; README after `016b632e…` (190 → 190 lines,
   one line changed); command A tree-mode → **83/83, missing [], dangling [], 14/14,
   10.0/10.0**. Re-derive both identities after the seats stop writing, then run command
   A at the records commit. Pairing rule: the map token must name the landed stem.
2. **C2 — admit the tool at its FINAL revision with the coupled texts.** Commit
   `.ufo/gates/custody-pair/custody-pair.py` + `README.md` **as EX-21 leaves them**
   (README already rewritten; do NOT also apply `EX-30/readme.patch.md` — superseded),
   land `EX-30/registry-row.patch.md` (dry-run clean against current SKILL.md), then
   re-run: selftest (expect `CLEAN`, 21+ cases), the four injections (expect 14 / 2 / 2 /
   2 as measured), and capture the post-pair with the landed revision. Quote the v1
   numbers in pairs: sums-form → exit 0, stanza-form → exit 12/10 by design with
   `SHA256-CONTRACT` intact. Decide and record the both-sides-absent ruling (§7.1).
3. **C3 — admit the table + the coupled pin as one unit.** Commit
   `.ufo/gates/citation-drift/pointer-table.json` (`bfc42f1b…`, 57 entries) and
   `expected.json` (`d97dd60a…`) **in the same commit** (a stale pin is
   `pointer_table_tampered`, exit 2 — the F3 coupling), then re-run the probe at the
   commit in both modes (expect `clean findings=0 exit=0`) and `--selftest` (13/13).
   The count (31 → 57) is not the acceptance test — EX-43's census + EX-41's landed
   entries are.
4. **Wave-level.** All three real targets are worktree files; nothing is committed (by
   rule). Seats do not commit; the parent re-derives every identity at landing (rule
   #14) — every identity quoted here is churn-prone and timestamped. `.ufo/gates/`
   is not in command A's read set, so no gate edit can move command A's numbers
   (consistent with r2's finding). The pre-existing dirty
   ` M .ufo/waves/arc2-loop1-round10/C3.md` is not this round's.

## 5. Attacks / refutations run by this seat (verdicts)

| # | Attack | Verdict |
|---|---|---|
| A1 | "The optimizer destroys the recoverable dispatch shape" | **REFUTED** — my own optimizer-200 payable/fallback/library carrier: 9/9, zero extras; the chain's carrierB: 11/11 both legs |
| A2 | "C1's carrierB selectors are claimed, not measured" | **REFUTED** — re-probed from the carrier bytes with the pinned REA; K/K on both legs; decoded bytecode sha equals the on-disk `.bin` digest `aaf85cea…` |
| A3 | "The solc prefix was reinstalled or is ambient-tainted" | **REFUTED** — version string + `soljson.js` `221d7a66…` reproduce the r1 receipt's two-tree identity; no install ran |
| A4 | "C2's D2 EACCES hole is closed" (before-state) | **REFUTED at the pre-state** (raw tracebacks at `7b848eaf…`), then **CONFIRMED closed at `7cd19c3c…`** (exit 14 both branches) |
| A5 | "C2's write-guard clobber is fixed" | **CONFIRMED** — `--paths X --out X` refused, victim bytes unchanged (before: clobbered) |
| A6 | "C2's D6 is closed" | **CONFIRMED** — `selftest --scratch <missing>` → exit 2 USAGE, no traceback |
| A7 | "A 1-of-5 receipt can still read exit 0 with four paths unexamined" | **PARTIALLY CONFIRMED as designed**: without `--require-paths` it still reads exit 0; with the gate → exit 2. The residual is a caller-discipline matter, stated in the tool's own docs |
| A8 | "Both-sides-absent verify is still fail-open" | **CONFIRMED as unchanged** (exit 0) — see §7.1; the fix's scope covers error-carrying stanzas only |
| A9 | "C3's new entries might break under C2's README churn" | **REFUTED** — probe stayed findings=0 across five README revisions (anchors carry no pin line) |
| A10 | "C3's scratch extension identity claim is stale" | **REFUTED** — I re-hashed their scratch table: `0b01f521…`, byte-for-byte as claimed |
| A11 | "C1's map token patch is not line-neutral / touches more than the EVM row" | **REFUTED** — 190 → 190 lines, 1 line changed, prior tokens byte-identical; two independent applications land `016b632e…` |
| A12 | "EX-30's README patch is still applicative" | **REFUTED in effect** — its semantic content is already in EX-21's README; base digest superseded |
| A13 | Custody drift this wave | **REFUTED for 4/5 paths; CONFIRMED pre-window for `config.toml`** (§3) |

## 6. Custody sha256s at my captures (read-only)

Pre 13:06:44Z (`/var/tmp/vz4r3/custody-pre.txt`, reproduced by the tool capture at
13:13Z): the five digests in §3. Every later sample (revisions.log + my tool captures)
shows the same five — no round-3 write touched them.

## 7. Gaps named (not blocked on)

1. **Ruling needed: both-sides-absent verify.** r2's D2 named the `MATCH exit 0` on a
   both-sides-absent path as part of the fail-open; the landed revision deliberately
   keeps that behavior for cleanly-absent stanzas (only `STAT-ERROR`/`READ-ERROR`
   stanzas become UNEVALUABLE). If the freeze's "no fail-open MATCH" is read to cover
   the absent case too, the claim needs a one-line adjudication in the record; if it is
   read as EACCES-only, the landed behavior satisfies it. I did not find a seat that
   adjudicates this explicitly — measured and reported, not resolved.
2. **Revision churn debt.** Three of the four shipped objects churned inside the window
   (custody tool ≥8 revisions, README ≥5, table once landed; the probe and census are
   inert). Every pin in this file is bound to a timestamp + sha256; the parent must
   re-derive, not copy.
3. **Pre-pair tool revision.** The round's pre-pair embeds `112d01dc…` (the r2
   revision); the post must be captured with the landed revision — record both hashes
   or re-capture (operator-owned surface, read-only, safe to re-capture).
4. **Seat census gap.** The poll budget (30 × 60 s) closed while the wave was still in
   flight; the delivered fraction at my last check is in §1a, with the undelivered names.
   No backfill claim is made: a seat with artifacts but no report file counts as
   undelivered (r1 precedent), and this summary says which those were at my census.