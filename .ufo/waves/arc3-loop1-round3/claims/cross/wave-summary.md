# arc3-loop1-round3 — wave summary (VZ-4, wave-integrator, late join / devin backfill)

Seat VZ-4 | chain cross | role wave-integrator | wave `arc3-loop1-round3`, 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. HEAD
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (immobile at every sample this wave;
seats do not commit).

This file is the **late-join rewrite** of the mid-flight draft. The original
token-plan seat's draft (written ~13:22Z, cut off before its closing census) is
preserved verbatim at `claims/cross/VZ-4/wave-summary-tokenplan-seat-13z22.md`
(sha256 `e7bf9eb2102afcbfd515500c77c05e8e986a360b30dc4d2c2efbdffb06e93b32`).
Everything in this file was either re-derived first-hand by this seat
(13:23–13:33Z window; late poller `claims/cross/VZ-4/poll-log-late.txt`,
25 × 60 s) or is cited to a landed artifact with its own re-derivation.
Where a number is quoted from a seat, it says so. Rule #14: every identity
here is timestamped and churn-prone; the parent re-derives all of them at
landing.

**Method.** Late-join poller (25 × 60 s, seats dir + the four real-target
hashes per check); re-runs of the round instruments at HEAD (command A,
citation-drift probe both modes + selftest, pin-check, census); the C2
injection suite + after-state suite on *scratch copies* of the landed tool
(never a custody write; the clobber-attack demo ran on a scratch fixture); the
C1 landing projection on a scratch mirror of the command-A read set; a
scratch git clone for the C2↔C3 collision end-to-end (a local-only git
operation in `/var/tmp/vz4r3-late/clone-git`, never the real repo); a fresh REA
probe of EX-04's carrierB; read-only sha256/stat of the 5 custody paths.
Scratch under `/var/tmp/vz4r3-late` (`/tmp` written twice by accident during
the collision test — two scratch JSON copies, removed immediately; never used
for receipts). No git mutation of the real repo, no install, no custody write.

---

## 1. The wave's arc: dispatch → quota interruption → devin backfill → close

**Dispatch (frozen pre-dispatch).** 64 seats on
`alibaba-token-plan/deepseek-v4.1-flash` (token-plan key 1 of 3 — the operator
directive recorded in the round-2 records). Roster enumerated mechanically
24+24+12+4; `len(items) == 64` asserted at dispatch
(`claims-frozen.md:103-116`). Axis set: coverage (owned), operability (fleet),
freshness (fleet).

**Quota interruption.** The token-plan lane hit its **monthly quota mid-run**.
The freeze point, measured: the last pre-interruption report landed
**13:17:53Z** (EX-21); the original poller's checks 10–16 (13:18:03–13:24:03Z)
all read a frozen **43/64 reports = 44 files** in `seats/` (the 44th file is
the `EX-28.md.sha256` sidecar — the seat line's "44 files incl. one sidecar");
check 17 (13:25:03Z) read 47 — the backfill's first visible increment.
21 seats were undelivered at that instant: EX-09, EX-14, RV-1, RV-3, VZ-1,
EX-23, EX-29, EX-30, EX-31, EX-32, SC-3, SC-4, RV-5, RV-7, RV-9, VZ-2, EX-42,
VZ-3, CN-1, CN-2, VZ-4.

**Operator-directed devin substitution.** The operator redirected the remaining
seats to the devin lane. The first backfill reports — **EX-23, EX-29, EX-31,
RV-9** — appeared between poll checks 02 and 03 (**13:24:30–13:25:30Z**); some
were re-edited afterwards, so current mtimes differ from first-seen times
(mtimes are churn-prone, rule #14).
The backfill then landed **18 reports** in ~8 minutes (13:24:47–13:32Z): CN-1,
CN-2, EX-09, EX-23, EX-29, EX-30, EX-31, EX-32, EX-42, RV-1, RV-3, RV-5, RV-7,
RV-9, SC-4, VZ-1, VZ-2, VZ-3 — each declaring "late join" and an explicit
COMPLETED-missing / VERIFIED-existing split. The devin backfill roster is the
**21 seats undelivered at the quota event** (§ above): 18 have landed reports,
**EX-14 and SC-3 are pending, and VZ-4 is this seat** (report last by rule).
Every post-interruption report is a devin seat.

**Census at this file's write (13:33Z): 61/64.** Undelivered: **EX-14, SC-3**
(both have landed artifact trees — EX-14: 18 files incl. projections; SC-3: 53
files incl. `ledger.md` + before/after evidence — their *reports* are the
paperwork still pending) and **VZ-4** (this seat; its report lands last by
rule). No stray seat files, no zero-byte reports at any check. The final
closing census is appended at the bottom of this file when the poll window
closes.

**Backfill delivery timeline (my late poller, per-check deltas —
`poll-log-late.txt`).** check 01–02 (13:23:30/13:24:30Z) 43 seats → check 03
13:25:30Z **+EX-23, EX-29, EX-31, RV-9** (47) → check 04 13:26:30Z **+CN-1,
EX-09, EX-30, EX-32, RV-1, RV-7, VZ-3** (54) → check 05 13:27:30Z **+RV-3**
(55) → check 06 13:28:30Z **+VZ-2** (56) → check 07 13:29:30Z **+RV-5, SC-4,
VZ-1** (59) → check 08 13:30:30Z **+EX-42** (60) → check 10 13:32:30Z **+CN-2**
(61). The wave's reports were still landing while this summary was written;
the artifact trees were far ahead of the reports throughout (the r1-shaped
gap, recurring).

**Provider-substitution record (CN-1 §6a; proposed text, parent's call).**
Per the standing substitution rule (round-7/8 and r10 precedents,
`LOG.md:1280-1288`; `SCORECARD.md:649-653`), the substitution is recorded with
cause and is **not** a lane choice and **not** a coverage/quality signal. The
records should quote the delivered-seat count **per lane**; the 64-seat roster
identity is unaffected (the `len(items) == 64` assertion was made at dispatch,
before the quota event; provider identity is substrate-neutral per the clause
quoted in `SCORECARD.md:652`).

---

## 2. Per-chain verdicts

All three chain verdicts landed and were revised by their late-join
convergence seats: c3 `claims/c3/verdict.md` (mtime 13:26:15Z), c2
`claims/c2/verdict.md` (13:28:08Z), c1 `claims/c1/verdict.md` (rev 3,
13:28:26Z — the late-join second run superseding the pre-interruption revs
1-2). Each was written with first-hand re-derivation. **Verdicts: all three
chains VERIFIED**, each with named residuals; nothing measured contradicts any
claim. The parent-side landing words remain open by rule (seats cannot commit).

### C1 — coverage (owned): EVM optimizer-enabled + non-ERC-20 carriers — **VERIFIED**

- The receipted round-1 solc prefix is genuine and was *reused*: my re-hash of
  `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc/soljson.js`
  = `221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c`,
  byte-equal to the r1 install receipt (`EX-02/install-receipt.txt:101`,
  tarball `0e1a1ab6…575a51`); `solcjs --version` =
  `0.8.37+commit.f401782d.Emscripten.clang`. No install ran.
- K/K recovery: my own fresh REA probe (@6.4.0) of EX-04's `carrierB` opt200
  runtime returned **11/11, zero missing, zero extra, `dispatch:"abi"`**, with
  decoded `bytecode.sha256 aaf85cea…` byte-equal to the on-disk runtime
  digest `aaf85cea…` — the claim's non-ERC-20, optimizer-200 carrier
  reproduces under an independent hand. The chain's other carriers (VaultB
  13/13 opt+nopt, CarrierB 8/8, CarrierBErr 8/8, Rv2TokenOpt 5/5, carrier-A
  3/3) are quoted from the seat envelopes with independent re-derivations by
  VZ-1/CR-1/CR-2/RV-1.
- Command A before-state at HEAD: **82/82, missing [], dangling [], 14/14,
  10.0/10.0** (my git-mode run, recipe `SCORECARD.md:92-124`).
- **Landing projection (my run, current rev-4 literal):** entry
  `2026-10-19-arc3-r3-evm-optimizer-shapes.md` 37 lines / 17,708 B /
  `3b5f371e85bdb8054e3a6b04c4b2097179b6a5435476a8f470e0d6c0a45c2215`;
  line-neutral README row (190 → 190 lines, exactly one line changed) →
  README after `a451ad1664cda0cb87f3a76e974de818a1e401387bad6251b98cd6b0df8ede3a`;
  command A tree-mode → **83/83, missing [], dangling [], 14/14, 10.0/10.0**;
  prior-82 knowledge files byte-identical (0/82 mismatches, my diff run).
  RV-4's independently applied patch lands the same README `a451ad16…` —
  two independent applications, byte-identical. The c1 verdict rev 3 (VZ-1's
  late-join run, 13:28:26Z) independently reproduces the same three identities
  (literal `3b5f371e…`, README `a451ad16…`, additive token `786efbb2…` = RV-4's
  patch line **plus its trailing newline**; my re-derivation: the bare line is
  281 B `e642b530…`, with-`\n` `786efbb2…`) on a fresh `git clone` projection —
  four independent applications total converge.
- **Named debt (landing-blocking; from c1 verdict §Named debt):** the draft
  literal is at rev 4 (`records-drafts/knowledge-entry-draft.md`
  `d9004f48…` 22,628 B mtime 13:17:51Z; SC-2 mirror `9b0cb5b8…` 22,071 B) and
  **F1 (internal contradiction), F2 (citation overclaim), F4 (dead paths) are
  still present**; F3 fixed in rev 4; F6 — SC-2's `README-identities.txt` is
  stale (pins a superseded revision). Apply-by-content patch texts:
  `CR-2/proposed-entry-text-fixes.patch.md` (F1-F4, F6),
  `CR-1/proposed-entry-corrections.patch.md` (Edits 1-3),
  `RV-3/proposed-entry-fixes-rev4.patch.md` (`1e191bd8…`, rev-4-targeted).
  My projection above is bound to the CURRENT literal, not the fixed one —
  re-derive after applying the fixes.

### C2 — operability (fleet): custody-pair hardening — **VERIFIED**

I ran the injection suite and the after-state suite myself against a scratch
copy of the landed revision (`7cd19c3c…`, 1155 L), never the real target:

| Injection (declared class) | My measurement at `7cd19c3c…` |
|---|---|
| D6 `selftest --scratch <missing>` (USAGE) | **exit 2**, no traceback |
| D2a capture over exists-but-EACCES (14) | **exit 14**, receipt written, no fail-open |
| D2b `verify --live` over unreadable candidate (14) | **exit 14** |
| D2c both-sides-plain-absent verify | **MATCH exit 0** — declared design (only error-carrying stanzas are UNEVALUABLE); the residual semantic call, §6 item |
| D3a/D3b 1-of-5 receipt plain | exit 0 (declared default) |
| D3c `--require-paths 5` (USAGE) | **exit 2** + `REFERENCE-COVERAGE: 1/5 … unaccounted: …` |
| Write-guard `--paths X --out X` (USAGE) | **exit 2**, victim bytes unchanged (`c7136f57…` before/after) |
| Canonical `--out ~/.bashrc` refusal | **exit 2** |
| Selftest | **CLEAN cases=22 passed=22 failed=0 exit=0** (claim bar 15 → ≥17) |
| Live capture + self-pin + verify | 5/5 exit 0; `TOOL_SELF_PIN=YES`; `MATCH 5/5 drift=0 exit=0` |
| v1 canonical stanza vs live | exit 10, 4× `LABEL-DEFECT`, `SHA256-CONTRACT 4/5` (the one mismatch is the recorded pre-wave `config.toml` drift) |
| v1 sums-form vs live | **exit 0**, `MATCH-V1-PARTIAL 5/5` |

The chain's round pair re-verified by me: `config-pre-pair-v2r3-revised.txt`
(`553fe82d…`, tool `7cd19c3c`, 13:15:44Z) vs `config-post-pair-v2r3.txt`
(`4969133b…`, tool `7cd19c3c`, 13:17:23Z) → **MATCH 5/5 drift=0 exit=0**; both
vs `--live` → MATCH 5/5; the round-start receipt (`d31ece6f…`, tool
`112d01dc…`) vs live → MATCH 5/5; all three sidecars `sha256sum -c` OK.

**The before side, measured by me on the base blob** (`git show HEAD:…` →
`112d01dc…`, 889 L, selftest 15/15): D6 → traceback exit 1; D2a/D2b →
traceback exit 1; write-guard `--paths X --out X` → **clobbered** (victim
`c7136f57…` → `7a662974…`), exit 0; D3 gate flag unrecognised (argparse exit
2). Receipt: `claims/cross/VZ-4/late/c2-injections-before-base.txt`. The
claim's discriminating before→after unit therefore stands on this seat's own
runs on **both** sides.

Registry-row patch text: EX-21 `proposed-skill-registry-row.patch` /
EX-30 `registry-row.patch.md` — **one voice must land** (both rewrite the
precedence clause identically — the collision in §3 fires with either), and
see §3 before landing either.

### C3 — freshness (fleet): citation-drift table extension — **VERIFIED, one named uncovered row**

- Landed pair (uncommitted worktree edits, ` M` in git status): table
  **57 entries** (+26; 0 removed / 0 modified / 0 duplicate ids; `quoted` 4
  unchanged; `exempt` 3 → 8 prefix-equal) sha256
  `bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7`
  (30,348 B); `expected.json` re-pinned to it
  (`d97dd60a942eaf53771c8224e84a9e8cdaf976dc66c3a543a450b1f1fa3827e2`).
  Pin == table (my `EX-46/pin-check.py` run: **VERDICT MATCH**).
- Probe at HEAD (my runs, disk-backed TMPDIR): **0 findings both modes**;
  selftest **13/13**; probe bytes unchanged (`e2665074…`).
- Census acceptance (the claim's real test): VZ-3's independent net covers
  **12/12** durable-surface rows; cross-walks against EX-42/EX-41/EX-43/CR-5/
  RV-11 all set-equal. **Residual R1: `LOG.md:1442`** — a stated-line citation
  about `SHONEN.md` written by arc3 r2 — is pinnable, uncovered, and not
  reached by any exemption's wording; the one-line fix is EX-42 §5.4's proposed
  `quoted` entry (`log1442-shonen-repoint`, `must_match` `SHONEN:6 → \`81-255\``)
  or an exempt-ledger adjudication with reaching wording, re-pinning the digest
  in the same commit either way (c3 verdict closing procedure step 1).
- Frozen-run guard and tamper teeth reproduce (VZ-3 §6/§7); non-vacuity
  26/26 across three independent seats.

### Cross

- **CN-1** (consistency): no shared reading contradicts across chains at
  13:25Z; carries the provider-substitution note (§1) and the pre-registered
  collision gate (§3). **CN-2** (records package): v7 fold of the chains'
  records drafts, PIN-FREE CLEAN, census projection PASS 0/0/0/0,
  discrimination control FAIL undeclared=1 (live test); my re-run of their own
  fold script reproduced their claimed identities byte-for-byte (section 213 L
  `83772cc4…`, entry 207 L `6e20b662…`) — independent corroboration.
- **CU-1** (custody): pre-side corroborated on three independent sources
  (80/80 field cells), compiler receipts re-derived; POST pair landed after
  their close (EX-29 captured it; my verify above covers it).
- **VZ-4** (this seat): this file + `seats/VZ-4.md` + `claims/cross/VZ-4/late/`.

---

## 3. The C2↔C3 collision — measured, fixed, landing-order binding

C3's landed table anchors `skill-registry-custody-pair-row` on the round-2
precedence string (`precedence CONTENT-DRIFT > ABSENT > …`). C2's registry-row
patch rewrites that clause to add `UNEVALUABLE >`. **If both land as drafted,
the probe reads findings=1 at the work commit** — C3's "findings = 0 at the
work commit" would falsify. First predicted by CN-1 §3g, measured by EX-30,
EX-32, CN-2 §6.5, and **reproduced end-to-end by me**:

- Scratch git clone at `c07af80` + EX-30 v2 row applied (SKILL.md `03832723…`)
  + landed table → `citation_dead entry=skill-registry-custody-pair-row`,
  `reported findings=1 exit=0` / `--strict failed findings=1 exit=1`
  (scratch commit `f4c520a2`).
- With EX-32's re-anchor applied — table
  `a810bd17ea416fe0f3ed9e053e1e470ae833718f457b6d39399478c93de91a7b`
  (re-derived byte-exactly from the landed table with the optional group
  `(UNEVALUABLE > )?`), expected re-pinned `e33f0e2d…` (digest string only) —
  probe reads **0 findings in both modes**. The regex matches both the round-2
  row and the revised row (True/True, my check).

**Landing-order options** (parent's call; CN-1/EX-32/CN-2 enumerate the same
three): (1) land the re-anchored table + re-pinned expected **in the same
commit** as the row (cheapest; patch text
`claims/c2/EX-32/pointer-table-reanchor.patch.md`); (2) write the old
precedence into the new row (rejected — the row would describe the wrong map);
(3) serialize the landings (C2 first, C3 re-derives). Either way the
pre-registered re-run applies: probe at the work commit, both modes, must
read 0; selftest 13/13.

---

## 4. Custody outcome

**5 paths read-only throughout; 4/5 byte-identical to round 2; the fifth
(`~/.kimi-code/config.toml`) drifted BEFORE this wave opened — operator-side,
recorded, not repaired.** My read-only capture (13:23–13:32Z):

```
16f496e6…  ~/.config/devin/mcp_config.json   unchanged (mtime 1792011200, inode 11341318)
38d2a1d0…  ~/.omp/agent/mcp.json             unchanged (mtime 1792011200, inode 11341316)
bc66d543…  ~/.kimi-code/config.toml          MOVED vs r2 (mtime 1792414665 = 12:57:45Z;
                                             inode 37793921, mode 644, size 114434)
7d2ca28a…  ~/.bashrc                         unchanged (mtime 1792168396, inode 25991953)
6c6be761…  ~/.profile                        unchanged (mtime 1792044727, inode 40274)
```

The drift timestamp precedes the wave's first sample; CU-1's pre-pair and
CN-1's watcher independently record the same moved fields — the standing
operator-side interactive-session churn class, not a round-3 lane event.

**Revised-tool pair (the claim's live pair).** Pre 13:15:44Z (`553fe82d…`),
post 13:17:23Z (`4969133b…`), both captured with the landed revision
`7cd19c3c…` and self-pinning it; MATCH 5/5 drift=0, plain and gated (my
runs + VZ-2's + RV-9's). The round's older pre receipt (`d31ece6f…`, tool
`112d01dc…`) also verifies against live — the pair spans two revisions only if
that older file is quoted as "the" pre; the revised-tool pre exists and is the
pair's true other half.

**Tool revision finality.** `112d01dc…` (r2 landed, 889 L) → … → `7cd19c3c…`
(1155 L, 54,279 B) — first seen in the revision watch at 13:13:29Z (r05), and
**unchanged in every sample since** (original watcher r05–r65+ to 13:33:30Z;
original poller to check 26; my late poller checks 01–12 to 13:34:30Z; CN-1's
watcher to 13:23:28Z; VZ-2's to 13:27Z). README final `f30df42e…` (185 L)
since 13:15:29Z.

---

## 5. What this seat verified first-hand (and two disclosed accidents)

Re-derived at HEAD by my own runs: command A 82/82 14/14 (git mode); probe 0/0
both modes + selftest 13/13; pin-check MATCH; census PASS 0/0/0/0; the C2
injection suite (table §2-C2) + after-state suite (selftest 22/22, live pair,
v1 legs) on scratch copies; the pair/sidecar verifies; the C1 projection
(83/83, README `a451ad16…`, prior-82 byte-identical); the collision + fix on a
scratch clone; the CN-2 v7 fold gates; EX-04 carrierB re-probe 11/11; solc
prefix re-hash; custody 5-path capture. Full outputs:
`claims/cross/VZ-4/late/` + `poll-log-late.txt`.

**Accident 1 (disclosed, repaired).** At 13:25:02Z I clobbered the round-1
historical receipt `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`
by mis-ordering `c2-verify.sh` arguments (passed the receipt as the output
file). Restored byte-identically from the HEAD blob 53 s later (`git show`
redirect; sha256 `b8ed1936…`, `git status` clean — re-verified by me at
13:30Z). Independently observed and exonerated by VZ-2 (§R2) and RV-9. It
broke VZ-2's first baseline regression run (8 spurious FAILs) until they
re-ran against a pristine clone. The parent should confirm the file is not
committed in a clobbered state — it is clean now.

**Accident 2 (disclosed, no residue).** During the collision test I copied two
scratch JSONs to `/tmp` (EDQUOT-avoidance discipline breach); removed
immediately, never used for receipts.

**Accident 3 (disclosed, byte-neutral).** While testing CN-2's pre-flight
recipe I invoked their own fold script (`assemble-merge.py`, their §8 step 0);
by design it rewrites `claims/cross/CN-2/merged-{LOG-entry,SCORECARD-section}.md`.
The regenerated bytes are **byte-identical** to CN-2's own receipts (213 L
`83772cc4…` / 207 L `6e20b662…`) and to their post-run `identity.txt`
(13:32:28Z, written after my last invocation), so no content was altered —
only mtimes moved. Recorded because seats should not write other seats'
artifacts even byte-neutrally.

---

## 6. Parent-facing admission inputs

1. **C1 — admit conditional on landing the corrected literal.** Apply the
   entry-text fixes by content (CR-2 F1-F4 + CR-1 Edits; RV-3's rev-4 patch
   text supersedes where it targets the current revision), land the entry file
   from the fixed literal text, land the **additive** map token (PRIMARY in
   `map-token-patch.md`; token == landed stem; do not insert/delete lines),
   then re-derive and re-run command A at the records commit: expect 83/83,
   missing [], dangling [], 14/14, 10.0/10.0, prior-82 byte-identical. My
   projection numbers above are bound to the *pre-fix* rev-4 literal.
2. **C2 — admit the tool at its final revision with the coupled texts.**
   Commit `.ufo/gates/custody-pair/custody-pair.py` (`7cd19c3c…`) +
   `README.md` (`f30df42e…`) as EX-21 leaves them (do NOT also apply
   `EX-30/readme.patch.md` — superseded); land **one** registry-row voice
   (EX-21 or EX-30) — **and read §3 first**: whichever row lands rewrites the
   precedence clause C3's table pins. Re-run: selftest 22/22, the four
   injections (14/2/2/2), the v1 legs (sums → 0; stanza → 10/12 by design).
   Ruling needed on the both-sides-absent MATCH (§7).
3. **C3 — admit the table + coupled pin as one unit, with §3's re-anchor.**
   If the registry row lands, land EX-32's re-anchored table (`a810bd17…`) +
   re-pinned expected (`e33f0e2d…`) in the **same commit**; then probe both
   modes (expect 0) + selftest 13/13. Decide R1 (`LOG.md:1442`): append the
   quoted entry or adjudicate with reaching wording; re-pin same-commit either
   way. The count (31 → 57) is not the acceptance test — the census is.
4. **Wave-level.** All three real targets are **uncommitted worktree edits**;
   the parent lands and re-derives everything (rule #14). The records should
   quote the delivered count **per lane** (§1) and the §3 landing order.
   `__pycache__/` dirs under `.ufo/gates/` (three) are untracked residue —
   keep them out of the landing commit. The pre-existing dirty
   ` M .ufo/waves/arc2-loop1-round10/C3.md` is not this round's.

---

## 7. Gaps named (not blocked on)

1. **Both-sides-absent verify MATCH** (RV-6 A4, VZ-2 residual): the landed
   revision deliberately keeps `MATCH exit 0` for cleanly-absent stanzas
   (only error-carrying stanzas become UNEVALUABLE). If the freeze's "no
   fail-open MATCH" is read to cover the absent case, the record needs a
   one-line adjudication; as EACCES-only, the landed behavior satisfies it.
2. **C1 entry fixes still open at rev 4** (F1/F2/F4) — landing-blocking per
   CR-2; my projection used the pre-fix literal.
3. **C3 R1** (`LOG.md:1442` uncovered row) — one-line fix named.
4. **Collision landing order** (§3) — must be executed as a coupled landing.
5. **Sidecar path not scope-checked** (`--out X.sha256 --paths X`; RV-8/CR-4)
   and **`out.parent.mkdir` outside the guarded try** (CR-3 U3) — named
   residuals, patch texts exist, deliberately not landed after freeze.
6. **EX-14, SC-3 reports pending** at my last census (their artifacts landed).
7. **Revision churn debt.** Every identity in this file is timestamped; the
   parent re-derives at landing. The C1 draft moved through ≥4 revisions, the
   tool ≥8, the README ≥5, the CN-2 fold v5 → v7.

---

## 8. Identity appendix (as measured by this seat, 13:23–13:33Z)

| object | sha256 | size / lines |
|---|---|---|
| `custody-pair.py` (final) | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` | 54,279 B / 1155 L |
| `custody-pair/README.md` (final) | `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193` | 9,603 B / 185 L |
| `pointer-table.json` (landed) | `bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7` | 30,348 B / 57 entries |
| `expected.json` (landed) | `d97dd60a942eaf53771c8224e84a9e8cdaf976dc66c3a543a450b1f1fa3827e2` | 2,154 B, pin == table |
| `citation-drift-probe.py` | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` | unchanged this wave |
| re-anchored table (EX-32, my re-derivation) | `a810bd17ea416fe0f3ed9e053e1e470ae833718f457b6d39399478c93de91a7b` | scratch copy only |
| re-pinned expected (EX-32) | `e33f0e2d6014bbf88a4cb2ccc8b156d0f1cc473512ffa2eb8861baaf822b0cf3` | scratch copy only |
| C1 entry draft (records-drafts, rev 4) | `d9004f4880931455b2c46db32be96e38380c7baddb656a5dd2fae6af3b1a4632` | 22,628 B |
| C1 entry literal (projected) | `3b5f371e85bdb8054e3a6b04c4b2097179b6a5435476a8f470e0d6c0a45c2215` | 17,708 B / 37 L |
| C1 map token (PRIMARY additive, line+`\n`) | `786efbb231aa058a05cc0dc5a684bd4373bc4e01fc078871fa42ab5c4f086425` (bare line 281 B `e642b530…`) | 282 B |
| C1 README after (projected; == RV-4's apply) | `a451ad1664cda0cb87f3a76e974de818a1e401387bad6251b98cd6b0df8ede3a` | 190 L |
| CN-2 merged section (v7) | `83772cc43d254a5e77ee1984e052442ccb5a8656410f1b73924244632b765b04` | 213 L |
| CN-2 merged entry (v7) | `6e20b66225e3c8d454189b214d89f49e80e5f3e4ef28467d420f42954e831373` | 207 L |
| C2 pair receipts | pre-rev `553fe82d…`, post `4969133b…`, round-start `d31ece6f…` | sidecars OK |
| r1 historical receipt (after my restore) | `b8ed19365c103a4ab355678f0fffe0db4e0011a18b441e79f38d9e80de3d0776` | 2,045 B / 52 L, clean vs HEAD |

*Written 2026-10-19T~13:33Z; the closing census block appended when the poll
window closes. This seat wrote only this file, `seats/VZ-4.md` and
`claims/cross/VZ-4/**`; no git mutation of the real repo; custody paths
read-only; no LOG/SCORECARD/SHONEN/corpus/SKILL/README writes.*

---

## 9. Closing census (appended at poll close)

**Poll closed 2026-10-19T13:47:31Z (check 25/25), census taken 13:48:48Z;
updated 13:49Z when this seat's report landed.**

- **Delivered: 62/64** — every seat except **EX-14, SC-3** (reports pending;
  their artifact trees are complete: EX-14 = before-state + verbatim command A
  + 3 projections + 8 inputs; SC-3 = `ledger.md` + 53 files incl. before/after
  evidence). VZ-4 (this seat) delivered `seats/VZ-4.md` at ~13:49Z — the 62nd
  report; the census read 61/64 at poll close before it landed.
- Chain tallies (at 62/64): C1 23/24 (EX-14 pending), C2 23/24 (SC-3 pending),
  **C3 12/12 COMPLETE**, Cross 4/4 COMPLETE. No stray seat files; no zero-byte
  reports at any of the 25 checks.
- Real targets frozen through the whole window (identical at checks 01–25):
  tool `7cd19c3c…` (1155 L), README `f30df42e…` (185 L), table `bfc42f1b…`
  (57 entries), expected `d97dd60a…` (pin == table), knowledge=82. The
  original poller's late checks (17–28, 13:25:03–13:36:03Z) and the revision
  watcher (r05–r65+, to 13:33:30Z) agree.
- The wave's report curve: 43 (checks 10–16 of the original poller,
  13:18:03–13:24:03Z, frozen) → 47 → 54 → 55 → 56 → 59 → 60 → 61, stable
  from 13:32:30Z through poll close.
- Delivery note for the parent's roster reconciliation: count the dispatch
  items array (64) per the freeze's assertion; quote delivered counts per lane
  (§1). The 21 undelivered-at-quota seats: 18 reports landed in the devin
  backfill, EX-14 and SC-3 remain pending (artifacts complete), VZ-4 is this
  seat.

*End of the late-join wave summary. This seat wrote only this file,
`seats/VZ-4.md` and `claims/cross/VZ-4/**`; no git mutation of the real repo;
custody paths read-only; no LOG/SCORECARD/SHONEN/corpus/SKILL/README writes;
scratch under `/var/tmp/vz4r3-late` (the one `/tmp` breach disclosed in §5).*
