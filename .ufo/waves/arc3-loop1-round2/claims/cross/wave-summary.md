# arc3-loop1-round2 — wave summary (VZ-4, wave-integrator)

Seat VZ-4 | chain cross | role wave-integrator | wave arc3-loop1-round2, 2026-10-19.

HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420` (round-1 records commit; immobile at
every sample — seats do not commit). Wave window: wave dir created 08:27 local,
`claims-frozen.md` 08:28 local (11:28Z); this summary written from 12:21Z.
This seat wrote only this file, `claims/cross/VZ-4/*` (poll/watch logs, harnesses,
captures) and `seats/VZ-4.md`. No git mutation, no custody write (read-only
sha256/stat capture only), no install, scratch in `/var/tmp/vz4` (`/tmp` untouched —
standing EDQUOT record).

Method: a 60 s poller of `seats/` (`claims/cross/VZ-4/poll-log.txt` — checks 1–21,
12:00:41→12:20:41Z; the process died at check 21 and the gap is reported, not
smoothed), a 30 s real-target watcher for 52 samples
(`claims/cross/VZ-4/watch-log.txt`, 12:04→12:29Z), a 6×30 s closing poller
(`claims/cross/VZ-4/close-poll-log.txt`, 63→64 seats), ~25 additional direct
listings, mechanical roster census (`claims/cross/VZ-4/roster-census.py`, roster
parsed from `claims-frozen.md:84-96`), and VZ-4's own re-verification of all three
chains' after-states with purpose-built harnesses (`c2-verify.sh`, `c3-attacks.sh`,
`c1-verify.sh`, `c1-rulecheck.py`, `commandA.sh`, `custody-capture.sh`). Every
verification below is bound to a sha256.

Instrument identity at close (all three real targets are worktree files; the parent
commits them):

| Target | sha256 | size |
|---|---|---|
| `.ufo/gates/c1-census-v10.py` (C2's EX-16) | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` | 610 L |
| `.ufo/gates/custody-pair/custody-pair.py` (C3's EX-31) | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` | 889 L |
| `.ufo/gates/custody-pair/README.md` (C3) | `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba` | — |
| `SKILL.md` (C1's patch target — **unpatched**) | `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb` | 371 L |

## 1. Seats delivered vs the frozen roster

Roster source: `claims-frozen.md:84-96` (64 seats, enumerated per chain; parsed
mechanically by `roster-census.py`, not hand-counted). Census command:
`python3 .ufo/waves/arc3-loop1-round2/claims/cross/VZ-4/roster-census.py`.

**Delivered: 64/64** at the wave close (closing poller: 63 at 12:30:09Z → 64 at
12:31:09Z when this seat's own report landed; first seat report 12:05:31Z —
`seats/RV-8.md`; wave opened 11:28Z). The 12:27Z census that this section was first
drafted from read 63/64, with only VZ-4 outstanding.

- C1 12/12 — complete (chain verdict `claims/c1/verdict.md`, VZ-1, mirror of
  `claims/c1/VZ-1/verdict.md`).
- C2 30/30 — complete (verdict `claims/c2/verdict.md`, VZ-2).
- C3 18/18 — complete (verdict `claims/c3/verdict.md`, VZ-3).
- Cross 4/4 — CN-1 (connector, `seats/CN-1.md`, status COMPLETE: all shared
  readings consistent, flags ranked in `claims/cross/consistency.md`), CN-2 (records
  outline), CU-1 (custody corroboration; post-pair pending at its write), VZ-4 (this
  file + `seats/VZ-4.md`).
- Claim artifact dirs exist for every seat plus `receipts/` and `records-drafts/`;
  no strays, no zero-byte seat reports.

Every seat on the frozen roster delivered a report.

Per the r5 counting lesson the count is against this wave's frozen roster artifact,
not against another round's roster. No stray seat files; no zero-byte seat reports.

## 2. Per-chain verdicts

### C1 — depth (owned): queue-drain rule #14 — **VERIFIED IN SUBSTANCE, patch NOT applied**

VZ-4 applied EX-01's patch text (`claims/c1/EX-01/rule14.patch.md`, artifact sha256
`885fa537…`) to a scratch SKILL.md copy at the patch's own frozen anchor and
re-derived every identity the artifact claims (`claims/cross/VZ-4/c1-verify-out-v3.txt`):

- payload (markers stripped, trailing newline included) = **1,071 B / `6cc388cb…`** —
  exactly the artifact's revised identity line;
- patched SKILL.md = **387 lines / `a8170b96…`** — exactly EX-01's claimed patched
  identity (line 102 of the patch text);
- lines 1–239 **byte-identical** (`cmp`); pure tail append, 0 changed lines;
- rule blocks **13 → 14**, citation-resolved **13 → 14** (VZ-4's own per-rule parser,
  `c1-rulecheck.py`, `tree:` mode; every cited range re-resolved inside its file);
- census (landed v11) over the patched root: **PASS 0/0/0/0** with `SKILL.md
  lines=371→387, loci=2` unchanged — the benign E21-predicted diff;
- control: same census over the unpatched repo root: PASS, `lines=371`.

Chain-side corroboration (not relied on): PL-1's plan/patch, CR-1's review +
citation-form fix (`rule14-citation-fix.patch.md`), RV-1's review and rewording
proposal, EX-02's command-A replay, EX-04's pointer-refresh audit.

Caveats, named:

1. **The after-state is a verified projection, not a landed state.** SKILL.md is
   patch-text-only this round (frozen rule); at close the worktree `SKILL.md` is
   still the 371-line pre-image. The claim's "after the round's commit" is therefore
   parent-side: land the payload, then re-run command A at the records commit.
2. **Self-identity churn on the artifact itself.** EX-01's patch text was revised
   mid-wave; its first payload identity (13 lines / 896 B / `a47dc38d…`) went stale,
   and EX-01 self-corrected it with a revision note + fresh identity (rule #14
   exercised on the very artifact that lands it). At my first read the file was at
   `7cd9e950…`, 60 s later at `885fa537…`; all numbers above are from `885fa537…`.
   The integrator must re-derive the payload identity at landing.
3. **Chain verdict (VZ-1) adds a blocking landing condition.** `claims/c1/verdict.md`
   (`5a62eac2…`, mirrored at `claims/c1/VZ-1/verdict.md`) verdicted C1 **VERIFIED at
   tree level with 1 blocking landing condition**: the frozen claim's clause
   "citations in rule-#11 form (stanza key + receipt, **no bare line numbers**)" is
   **failed as-written by EX-01 rev B**, whose payload cites
   `` `SCORECARD.md:1366-1368` `` bare into a file whose head is rewritten each round
   (verified at source by VZ-4: payload line 15). VZ-1 measured a conforming variant
   (EX-01 rev B + RV-2's one-sentence rewrite: payload 1,129 B / `7e76e2e7…` →
   SKILL.md 388 L / `60dfbe02…`, command A 14/14, 0 form flags). VZ-4 independently
   built its own wording of the same fix and confirmed the shape: payload 1,118 B /
   `6a483c84…` → 388 L / `47505059…`, rules 14/14 resolvable, census PASS with
   `lines=371→388, loci=2`; the only remaining bare reference is `LOG.md:1411-1412`,
   which is exempt (append-only record naming its capture stamp).
   **Landing instruction: do not land EX-01 rev B verbatim; land a form-fixed payload.**
   VZ-1 also reports that "prior 13 rules byte-identical" reads 12/13 under a raw
   block-split (separator attribution) but 13/13 under rstrip-normalized comparison
   plus a pure-insertion proof (`before == after[:k] + after[end:]`) — the round
   record must use the precise phrasing.
4. **README/SHONEN carry-over**: the rule #14 landing also obliges `SHONEN.md:6`
   refresh (range + 13/13 → 14/14) and the C1 records drafts — named in EX-01 §4 and
   left to the parent.

### C2 — freshness (fleet): census fail-closures H1 + H3 — **VERIFIED at the landed revision**

VZ-4's own harness (`c2-verify.sh`; log `claims/cross/VZ-4/c2-verify-closing-final.txt`)
at the closing revision `d0772ce8…`, over the round-1 fixtures that previously read
silent PASS:

| case | before (`6f1d19ff…`, round-1 HEAD) | after (`d0772ce8…`) |
|---|---|---|
| ordinary run, repo root | PASS 0/0/0/0 exit 0 | **PASS 0/0/0/0 exit 0** (`G2 … ok, current-ok loci per file: PROVINCE=17, SCORECARD=14, SKILL=3; floor=1/file`) |
| `atk-missing` (SKILL.md absent) | **PASS exit 0** (silent absorption) | **FAIL exit 1**, `UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError']` |
| blind needles (PIN/VER/PTR→`(?!)`) | **PASS exit 0** (`G2 … ok`) | **FAIL exit 1**, `G2 … SUSPECT (…=0 …)`, `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` |
| `atk-undecl` | FAIL undeclared=1 | FAIL undeclared=1 (unchanged) |
| `atk-no-province` / `atk-no-scorecard` / `atk-empty` | FAIL | FAIL, now also naming the unreadable file |
| scope-diff vs round-1-committed bytes | — | rows 20→20, **ADDED 0 / REMOVED 0 / CHANGED 0, CREEP FLAGS []** |
| scope-diff vs pre-E22 v10 (`36e96cd5…`) | — | CHANGED 1 (the round-1 marker re-key 40→45 only), **CREEP FLAGS []** |

So the frozen claim's clauses hold at the landed bytes: declared-class FAILs for the
absent-file and blind-instrument injections, ordinary run PASS, scope bounds
byte-stable.

Caveats, named:

1. **Mid-wave over-fail, caught and fixed (not a defect of the landed revision).**
   Revision `c95a5cf3…` implemented the per-file floor in the census's *block* unit;
   SKILL.md legitimately has 0 current-ok *blocks*, so that revision FAILed the
   ordinary HEAD run (`G2 SUSPECT`). I measured it in flight
   (`claims/cross/VZ-4/c2-verify-after-snap2-blockunit.txt`); CR-2/CR-3/EX-14/PL-2
   measured the same class independently. EX-16 re-keyed the floor to *detections*
   and the revision after (`df9ffdf9…` → `a4c16763…` → `d0772ce8…`) reads PASS.
2. **Chain verdict pin — re-pinned in place.** `claims/c2/verdict.md` (VZ-2) was
   first pinned to `df9ffdf9…`/601 L; VZ-2 updated it during the wave to the final
   `d0772ce8…`/610 L (read by VZ-4 at 12:25Z, line 15 and the verdict heading agree
   with the live file's sha256). VZ-2's own ordinary-run stdout sha
   (`1db2ec31…`) equals EX-16's, i.e. the doc-only steps are behaviour-neutral —
   confirmed independently by my harness at both revisions. No stale pin remains;
   the integrator still re-derives at landing (C1 rule #14).
3. **Residuals stay named, not closed**: H2 (same-line inline-marker excusal) —
   VZ-4 reproduced it at the landed revision: a fabricated `rea-agents@9.9.9` pin
   with the inline marker retained still reads `PASS`, `historical (inline marker)`;
   H4 (self-certification) — the external diff audit remains the certificate; H5/H6
   (gate-free statement, fixed-bound rationale) untouched this round.
4. **Non-vacuity of the new floor was attacked, not assumed**: EX-14's occupancy map
   refutes per-ROW floors (4 DATED rows are legitimately zero-locus at HEAD); the
   landed unit is per-readable-file over current-ok detections, with unreadable files
   exempt because they force FAIL via the H1 class.

### C3 — operability (fleet): custody receipt v2 — **VERIFIED at frozen revision `112d01dc…`**

VZ-4 re-ran the tool at its own hand (`claims/cross/VZ-4/c3-*.txt`):

- **selftest `CLEAN cases=15 passed=15 failed=0 exit=0`** (scratch in `/var/tmp`);
- **live capture 5/5 exit 0**; every stanza's `SHA256`/`INODE`/`CTIME_EPOCH`/`SIZE`
  cross-checked by my independent `stat`+`sha256sum` capture — all match;
- **label defect gone and *detected*, not merely avoided**: for all 5 paths my
  independent `gmtime(epoch)` equals `MTIME_UTC_RENDER` (0 mismatches); local renders
  are recorded separately; and `verify` on round-1's v1 canonical receipt produces
  5× `LABEL-DEFECT` while reporting `SHA256-CONTRACT 5/5` — i.e. **v1 receipts remain
  verifiable on the field the claim names**;
- **same-content rewrite detected** on a scratch copy: content sha256 unchanged
  (`7d2ca28a…` both sides — sha-only custody is provably blind), yet
  `REWRITE-DRIFT exit 11`, `moved=mtime_ns,mtime_epoch`; a rename-swap with restored
  mtime is caught by `moved=inode,mtime_ns`. EX-31's A1 shows the mtime-restored
  in-place variant is caught by `ctime_ns` alone;
- **the round's live pre/post pair**: EX-31's `capture-pre.txt` / `capture-post.txt`
  (sidecars re-verified by me) re-verify independently → `MATCH 5/5 drift=0 exit=0`;
  VZ-4's own pair (pre 12:10:22Z → post 12:20:40Z, `vz4-frozen-rev` →
  `vz4-post-close`) → `MATCH 5/5 drift=0 exit=0`;
- read-only discipline held: no custody byte written, renamed or utime'd; the five
  digests are identical to the round-1 canonical receipts (see §6).

Caveats and one VZ-4 finding, named:

1. **Tool revision churn**: `custody-pair.py` was rewritten at least five times
   (RV-11 observed 4; I saw `72d5231f…` → `112d01dc…` mid-measurement). Every number
   in this section is bound to `112d01dc…` (889 L), which EX-31's report declares
   final ("do not edit the tool after this report").
2. **Write-guard scope (minor, measured by VZ-4)**: the read-only write guard covers
   only the canonical 5 paths (`out.resolve() in {CUSTODY_PATHS}`). With a `--paths`
   override, `capture --out X --paths X` silently *clobbers* the scoped file it is
   measuring — measured on a scratch copy (`c3-attacks-out.txt`, case F: the scratch
   file's sha changed to the receipt's, exit 0). The canonical-path guard itself
   holds (selftest case 12 re-run by me, real path unchanged). Recommendation for a
   future revision, not a blocker: extend the guard to `set(paths) ∪ CUSTODY_PATHS`.
3. **Residual threat model named, not absorbed**: CR-4's independent battery states
   the invisibility classes (atime-only touches by design; `cp -a`/restore-style
   replays that preserve inode+ctime; sub-nanosecond write/revert); PL-3 and EX-40
   independently refute "sha256 alone suffices" and "second-resolution ctime is
   enough" with measurements. Responsiveness/registry-row patch texts exist
   (EX-36) and are unapplied.

### Cross

- **CU-1** — custody corroboration: authoritative pre-pair (EX-32, 12:04:06Z)
  corroborated; v1-vs-live complete; **post-pair section PENDING at CU-1's write**.
  The gap is closed materially: EX-31's post receipt exists (12:0xZ) and I
  re-verified the pair MATCH 5/5 (§C3); the chain's own post-pair artifact is still
  owed by CU-1/EX-32.
- **CN-2** — records outline v1 (`claims/cross/records-outline.md`); notes that C1's
  rule #14 had not landed at its write.
- **CN-1** — **COMPLETE** (`seats/CN-1.md`; deliverable
  `claims/cross/consistency.md`, 24 KB, 12:22Z; receipts under `claims/cross/CN-1/`).
  All three shared instruments re-derived independently before any seat artifact was
  read: command A 82/82 · 13/13 · 10.0/10.0; census PASS 0/0/0/0 (counts 162/6 ·
  1417/9 · 371/2); probe 13/13, findings 0; custody 5/5 with identical
  inode/ctime/mtime per path — **every cross-chain reading consistent**. Four ranked
  flags, all consistent with this summary's findings: F1 revision churn (C2 records
  drafts pinned `df9ffdf9…` while the worktree had moved; the parent must record the
  revision actually committed); F2 C1 claim-vs-text (an incident-only citation form
  measures 13/14 = depth 9.29, so the landed text must carry a resolvable
  `corpus/knowledge/…` citation — EX-01 v2 does); F3 C1↔SHONEN same-commit coupling
  (range end 254 for the v2 payload, measured); F4 C3 v1-receipt verification exits
  12 by design — read "verifiable" through `SHA256-CONTRACT`, and name EX-31's pair
  (both `112d01dc…`) rather than the chain-level receipt, which embeds a superseded
  tool hash `4862f642…`.
- **VZ-4** — this file + `seats/VZ-4.md`.

## 3. Custody outcome

**Clean: zero drift, correctly labeled, and the pair mechanism now exists.**

- The 5 paths were read-only for every seat (hash/stat capture only); the digests at
  this seat's pre capture (12:01:47Z), at the closing post capture (12:20:40Z), and
  in EX-31/EX-32/RV-12/RV-14's receipts are all identical to the round-1 canonical
  receipts (§6).
- v2 instrument installed at the designated target (`.ufo/gates/custody-pair/`),
  selftest 15/15, live pair captured by the tool itself (EX-31) and independently
  re-verified by VZ-4 (MATCH 5/5, exit 0, both pairs).
- The round-1 label defect (`MTIME_UTC` carrying local −03 time) is **gone from the
  instrument and detected in old receipts**: the v2 tool renders UTC from the epoch
  (`gmtime`, TZ-independent by a selftest case that varies `TZ`), records local
  renders separately, and re-reading round-1's v1 receipt yields 5× `LABEL-DEFECT`
  alongside `SHA256-CONTRACT 5/5`.
- sha256-only blindness (round-1 attack 3) is answered: content-identical rewrites
  leave the digest untouched (measured) but move `ctime_ns`/`inode` and are declared
  `REWRITE-DRIFT exit 11`.

## 4. Parent-facing admission-recommendation inputs

1. **C1 — admit conditional on landing a *form-fixed* payload, not rev B verbatim.**
   Apply EX-01's payload (`claims/c1/EX-01/rule14.patch.md`) **with RV-2's
   one-sentence citation rewrite** (`claims/c1/RV-2/proposed-rule14-citation-form.patch.md`:
   `SCORECARD.md:1366-1368` → the `arc3-loop1-round1` section key + the fresh-identity
   line), per VZ-1's blocking landing condition. Measured shapes: VZ-1's variant →
   payload 1,129 B / `7e76e2e7…`, SKILL.md 388 L / `60dfbe02…`; VZ-4's independent
   wording of the same fix → payload 1,118 B / `6a483c84…`, SKILL.md 388 L /
   `47505059…`; both give `rule_blocks: 14`, `citation_resolved_rules: 14`, 0 form
   flags, census PASS with `loci=2` unchanged. Refresh `SHONEN.md:6`, land the C1
   records drafts, then run command A at the records commit and expect
   `rule_blocks: 14, citation_resolved_rules: 14, coverage/depth 10.0`. Re-derive the
   payload + SKILL identities at landing (they churned once inside the round).
   Two further landing conditions from CN-1's sweep: (F2) the landed text must carry
   a resolvable `corpus/knowledge/…` citation — an incident-only citation form
   measures 13/14 (depth 9.29) and fails the claim on its own instrument; EX-01 v2
   has one. (F3) land SKILL.md **in the same commit** as the `SHONEN.md:6` refresh,
   with the refresh's range end matching the landed craft geometry (254 is the
   measured end for the v2 payload).
2. **C2 — admit with the fresh identity.** Commit `.ufo/gates/c1-census-v10.py` at
   `d0772ce8…` (610 L), not at the chain verdict's stale pin `df9ffdf9…`; land
   EX-23's header patch and the C2 records drafts; exclude
   `.ufo/gates/__pycache__/` and `citation-drift/__pycache__/` (untracked, not
   gitignored); re-run the ordinary run + one absent-file fixture at the commit.
   Record the transient block-unit over-fail (`c95a5cf3…`) as a caught-in-wave
   defect, and keep H2/H4/H5/H6 named as open.
3. **C3 — admit by committing the new gate dir.** `.ufo/gates/custody-pair/`
   (`custody-pair.py` `112d01dc…`, `README.md` `fa484d57…`) — the tool is final and
   must not be edited post-report (its receipts embed its own hash). Land EX-36's
   registry-row patch and the C3 records drafts; exclude the tool's `__pycache__/`.
   CU-1/EX-32 still owe the formal post-pair section (materially verified here).
4. **Wave-level.** All three owned axes have measured after-states on disk; none of
   the three real targets is committed yet (the parent commits). **No seat on the
   frozen roster is undelivered** (64/64; CN-1's earlier apparent absence was a stale
   listing — corrected in place). ` M .ufo/waves/arc2-loop1-round10/C3.md` was
   already dirty before this wave — do not attribute it to round 2.

## 5. Attacks / refutations run by this seat (verdicts)

| # | Attack | Verdict |
|---|---|---|
| A1 | C2 before-state: absent SKILL.md under round-1 v10 | **CONFIRMED silent PASS exit 0** — the claim's premise is real |
| A2 | C2 before-state: needles neutered under v10 | **CONFIRMED silent PASS** (`G2 … ok`) |
| A3 | C2 after-state at `82fb807e…` (landed H1+H3) | **both injections now declared FAIL**; HEAD PASS |
| A4 | C2 revision `c95a5cf3…` (block-unit per-file floor) | **REFUTED as shippable**: ordinary HEAD run FAILs (`G2 SUSPECT`, SKILL.md=0). Caught live by this seat; fixed downstream → re-verified PASS at `d0772ce8…` |
| A5 | C2 creep: did the fix widen scope? | **REFUTED** — 20 rows, 0 added/removed/changed vs round-1-committed; CREEP FLAGS [] |
| A6 | C2 residual boundary: H2 fabricated pin `9.9.9` + inline marker at v11 | **CONFIRMED still open** (`PASS`, `historical (inline marker)`) — named residual, outside the frozen claim |
| A7 | C3: same-content in-place rewrite on a scratch copy | **DETECTED** `REWRITE-DRIFT exit 11`; sha-only would have said IDENTICAL |
| A8 | C3: rename-swap with restored mtime | **DETECTED** (`moved=inode,mtime_ns`) |
| A9 | C3: v1 receipt unverifiable by v2 tool | **REFUTED** — 3 v1 shapes parse; stanza-v1 → `SHA256-CONTRACT 5/5` + 5× LABEL-DEFECT |
| A10 | C3: UTC render is really localtime again (v1 defect) | **REFUTED** — my independent `gmtime` re-derivation: 0 mismatches on 5/5 |
| A11 | C3: write-guard protects everything it measures | **REFUTED (scoped)** — canonical 5 protected; `--paths`+`--out` same file clobbers it. Scratch-only demo; recommendation filed |
| A12 | C1: patch identity claims | payload and patched-file identities **reproduce exactly** at `885fa537…`; prior-rule bytes identical; 14/14 resolvable. (My own first harness run dropped the payload's trailing newline — **my** artifact, corrected, not EX-01's error) |
| A13 | Custody: pre/post drift | **REFUTED** — two independent pairs MATCH 5/5 exit 0 |
| A14 | C1 citation **form** (freeze: rule-#11 form, no bare line numbers) | **REFUTED for EX-01 rev B** — payload line 15 cites `SCORECARD.md:1366-1368` bare; my form-fixed variant (payload 1,118 B / `6a483c84…` → 388 L / `47505059…`) lands clean, 14/14, 0 flags |

## 6. Custody sha256s (VZ-4 captures, unchanged across the wave)

Pre 12:01:47Z (`custody-pre.txt`), post 12:20:40Z (`c3-capture-post-vz4.txt`), and
EX-31's pair — all five identical to round 1:

```
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  ~/.config/devin/mcp_config.json  (mtime 1792011200, inode 11341318)
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  ~/.omp/agent/mcp.json            (mtime 1792011200, inode 11341316)
8cbacd48ab85ea86e122bae102d8ee63e2fd3181aa551603b3923b912573c38d  ~/.kimi-code/config.toml         (mtime 1792376443, inode 34530637)
7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598  ~/.bashrc                        (mtime 1792168396, inode 25991953)
6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30  ~/.profile                       (mtime 1792044727, inode 40274)
```

## 7. Gaps named (not blocked on)

- **CU-1/EX-32 post-pair section** still formally pending (materially verified here:
  both pairs MATCH 5/5; VZ-3 records the same nuance).
- **Residuals carried, not closed**: C2's H2 (inline-marker excusal, reproduced),
  H4 (self-certification — external audit is the certificate), H5/H6; C3's
  non-user-space invisibility classes (CR-4's threat model) and the `--paths`
  write-guard scope finding.
- **Hygiene for the integration commit**: two untracked `__pycache__` dirs under
  `.ufo/gates/` (`c1-census-v10.cpython-314.pyc` + `custody-pair/__pycache__/`) —
  exclude; and ` M .ufo/waves/arc2-loop1-round10/C3.md` was already dirty before
  this wave.
- **Revision-churn debt for the round record**: three of the four shipped objects
  were rewritten many times inside the wave (census 8+ revisions, custody-pair 5,
  EX-01's patch 2+). Every number in this summary is bound to a sha256; the parent
  must re-derive at landing rather than trust any recorded pin.
- **Tooling observations for the parent's round record**: `.ufo/gates/` is not in
  command A's read set (EX-24/EX-37 verified), so no gate edit can move command A's
  numbers; the recipe-A invocation form in `SCORECARD.md` remains a trap
  (`REV=HEAD python3 - "$REV"` expands before assignment) — my `commandA.sh` binds
  `REV` first.
