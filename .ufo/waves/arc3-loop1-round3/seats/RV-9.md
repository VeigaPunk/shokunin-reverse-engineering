# RV-9 — seat report (chain c2, reviewer, LATE JOIN), wave `arc3-loop1-round3`

Seat RV-9 · chain c2 · role reviewer · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (unchanged throughout; no git mutation).
Task: late join — re-run the live pair independently with the revised tool (capture twice,
verify), corroborate EX-29 (MATCH 5/5); capture my own pair only if EX-29 had not landed.

**EX-29's pair HAS landed** (both receipts present and verifying). I therefore
**VERIFIED existing work** (EX-29's pair and its recorded verifies, EX-21's landed
tool + README + registry-row patch, PL-2's candidate evidence) and **COMPLETED missing
work** (the late-join independent re-run, the tool-free cross-checks, the reviewer
attack battery, and this seat report — the RV-9 directory held harness scripts and two
partial captures from the interrupted run but no seat report and no harness transcripts).

Instrument under review: `.ufo/gates/custody-pair/custody-pair.py`, sha256
`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (1,155 lines,
mtime 10:13:20 −03:00), re-derived by me four times across the review window with no
change. Prior revision under review (HEAD's): `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`
(snapshot in this chain's `claims/c2/RV-9/tool-at-RV9-start.py`; re-derived, and equal to
`git show HEAD:.ufo/gates/custody-pair/custody-pair.py`).

## 1. Work performed (evidence pointers)

All artifacts under `.ufo/waves/arc3-loop1-round3/claims/c2/RV-9/`. Scratch under
`/var/tmp/rv9-scratch/` only. Custody paths touched read-only (sha256 + stat); no write,
rename or `utime` was issued against any of them.

**A. Independent pair re-run (the seat task).** Two fresh captures with the revised tool
— `rv9-T2-revised.txt` (sha256 `ab78e73ac32bfb081e1172530ef6a1b3588aab911cce1279a273b1482e20671d`)
and `rv9-T3-revised.txt` (`20d1fc43e6f93b2c99cc2714c01cf5015679fdb2ad7c874bcff437d4e77ddb01`),
both exit 0, 5/5 present — plus a third post-attack capture `rv9-T4-final.txt`
(`3c678ac1539931e90c7c00e091547c03a8b15dbe44a8f7fa972bfe13ec9fb304`). Transcripts:
`rv9-T2-capture.out`, `rv9-T3-capture.out`, `rv9-T4-capture.out`; sidecars re-verified
(`sha256sum -c` OK ×3). Eleven verify runs in `rv9-latejoin-verify-battery.out`, all
`VERDICT: MATCH paths=5 MATCH=5 exit=0`:

| run | A | B | flag | result |
|---|---|---|---|---|
| 1 | T2 | T3 | — | MATCH 5/5 exit 0 |
| 2 | T2 | T3 | `--require-paths 5` | MATCH 5/5 exit 0 |
| 3 | T2 | EX-29 pre (revised) | — | MATCH 5/5 exit 0 |
| 4 | T2 | EX-29 post | — | MATCH 5/5 exit 0 |
| 5 | T3 | EX-29 post | — | MATCH 5/5 exit 0 |
| 6 | T3 | T2 (reverse) | — | MATCH 5/5 exit 0 |
| 7 | T2 | live | — | MATCH 5/5 exit 0 |
| 8 | T3 | live | — | MATCH 5/5 exit 0 |
| 9 | T2 | live | `--require-paths 5` | MATCH 5/5 exit 0 |
| 10 | T4 | T2 | — | MATCH 5/5 exit 0 |
| 11 | T4 | live | `--require-paths 5` | MATCH 5/5 exit 0 |

EX-29's own recorded pair (`verify-pre-vs-post.out`, `verify-post-vs-live.out`,
`verify-post-vs-pre-reverse.out`, and both `--require-paths 5` variants) read the same
`MATCH 5/5 exit 0`. **EX-29 is corroborated.**

**B. Tool-free identity cross-check** (no custody-pair.py involved) —
`rv9-toolfree-content-identity.out`, `rv9-independent-T4-latejoin.txt`, and the
pre-existing `rv9-independent-T0.txt` / `rv9-independent-T1.txt`. Raw `sha256sum` of the
five live paths equals the SHA256 recorded in every one of the five receipts (EX-29's two,
my three): **0 mismatches**. Inode and size sets agree across all five receipts per path.
A field-by-field diff of my tool-free capture against my revised-tool capture
(`rv9-independent-T4-latejoin.txt` vs `rv9-T3-revised.txt`) shows **0 diffs on all 12
shared fields × 5 paths**; the four tool-only fields are `EXISTS`, `TYPE`,
`MTIME_LOCAL_RENDER`, `CTIME_LOCAL_RENDER` (absent by construction from the tool-free
script). The earlier `rv9-field-diff-exp29pre-vs-mine.out` (16/16 fields × 5 paths,
0 diffs) still re-derives.

**C. Before → after reproduction of the four named holes** on scratch, old vs revised:
`rv9-before-injections-latejoin.out`, `rv9-d2-failopen-contrast.out`, and the revised-side
transcripts in `latejoin-harness/` and `latejoin-harness2/`.

**D. Reviewer attack battery.** `rv9-gate-attacks.out`, `rv9-backcompat-failopen-attack.out`,
`rv9-custody-writeguard-sandbox.out`, `rv9-final-attacks.out`.

**E. Chain-claim corroboration.** Command A re-derived with the canonical recipe
(`claims/c1/PL-1/command-a-recipe.py` at HEAD): `rv9-commandA-head.out` — see §3.
Census (`c1-census-v10.py --root .`) `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
unresolved=0)`. SKILL.md registry-row patch tested on a scratch copy (§2).

**F. Identity re-derivation (rule #14).** `rv9-identity-rederivation-final.out` — every
artifact cited here re-hashed at write time; all receipt sidecars `sha256sum -c` OK.

## 2. Proposed changes

**None authored by this seat.** The chain's real target (`.ufo/gates/custody-pair/`) is
EX-21's write scope and is read-only for me; I did not write it.

Two observations the parent should weigh, neither of them a change request from me:

1. **SKILL.md registry row is not yet updated in the worktree.** `SKILL.md` sha256
   `c134afcb2e648aa3f8ff96f11d03aee2be6715811cb7edb3b7be6ac40aa0aa90` still carries the
   **pre-revision** row (15 fixture cases, no exit 14, no `--require-paths`; grep for
   `require-paths` → 0 hits). The frozen C2 claim requires the registry row + README +
   tool to land in the SAME commit. The README *is* updated in the worktree
   (`f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193`, vs
   `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba` at HEAD), so the
   coupled landing is **one artifact short** as of this review. The patch text exists and
   I verified it is apply-ready — see below. This is the parent's merge call, not mine.
2. **EX-21's `proposed-skill-registry-row.patch` is not `git apply`-able** (`git apply -p0`
   → `error: invalid path '/var/tmp/ex21r3/SKILL.patched.md'`, because the diff header
   carries an absolute scratch path as the `+++` target). It applies cleanly with
   `patch -p0` (dry-run rc 0, real apply rc 0). The companion `apply-registry-row.py` is
   the intended path and it works exactly as declared: on a scratch copy it produced
   `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` and row
   `cf5111a795a7bfee0c49534bd28307d95a8c69e64ce1bf473303e1cf9ddde14b` — both matching
   EX-21's stated identities — with the file still 390 lines (line-neutral) and the
   live `SKILL.md` untouched. Landing command from the repo root, after re-verifying the
   base sha:
   ```sh
   sha256sum SKILL.md   # expect c134afcb2e648aa3f8ff96f11d03aee2be6715811cb7edb3b7be6ac40aa0aa90
   python3 .ufo/waves/arc3-loop1-round3/claims/c2/EX-21/apply-registry-row.py SKILL.md
   ```

## 3. Before → after measurement for the chain's claim (C2)

Measured by me on scratch fixtures, same fixture shapes both sides; old = `112d01dc…`
(copied under its proper filename), new = `7cd19c3c…`.

| # | named hole / item | BEFORE (`112d01dc`) | AFTER (`7cd19c3c`) | evidence |
|---|---|---|---|---|
| D2a | capture, exists-but-EACCES regular file | `PermissionError` traceback, **exit 1**, no receipt | `UNEVALUABLE paths=1/1`, **exit 14**, receipt written | `rv9-before-injections-latejoin.out`; `latejoin-harness/A6a-capture-eacces.out` |
| D2b | verify `--live`, candidate unreadable | `PermissionError` traceback, **exit 1** | `UNEVALUABLE paths=0/1 drift=1`, **exit 14** | `rv9-d2-failopen-contrast.out` |
| D2c | capture, parent-dir EACCES (lstat fails) | `PARTIAL paths=0/1` exit 13, stanza `EXISTS: no` + `STAT-ERROR` | `UNEVALUABLE paths=0/1`, **exit 14** | `rv9-d2-failopen-contrast.out` |
| D2d | **fail-open**: verify that stanza vs live | **`MATCH paths=1/1 exit 0`** | **`UNEVALUABLE`, exit 14** | `rv9-d2-failopen-contrast.out` |
| D3a | verify 1-of-5 reference, no flag | `MATCH-V1-PARTIAL paths=1/1 exit 0` | `MATCH-V1-PARTIAL paths=1/1 exit 0` (unchanged by design) | `latejoin-harness2/B2b-noflag.out` |
| D3b | verify 1-of-5 with `--require-paths 5` | flag **absent** from `verify --help` (grep count 0) | `USAGE: reference covers 1 of the required 5 paths` + `REFERENCE-COVERAGE: 1/5 … unaccounted: ~/.omp/agent/mcp.json ~/.kimi-code/config.toml ~/.bashrc ~/.profile`, **exit 2** | `latejoin-harness2/B2-require5.out` |
| D6 | `selftest --scratch <missing dir>` | `FileNotFoundError` traceback, **exit 1** | `USAGE: scratch base is not a directory: …`, **exit 2** | `rv9-before-injections-latejoin.out`; `latejoin-harness/A7-selftest-missing-scratch.out` |
| WG | write-guard `--paths X --out X` | **exit 0, X clobbered** (content became receipt text) | `USAGE: refusing to write a receipt over a path it measures or a custody path (path or inode)`, **exit 2**, X content preserved | `rv9-before-injections-latejoin.out`; `latejoin-harness/A8a-guard-self.out` |
| ST | selftest case count | `CLEAN cases=15 passed=15 failed=0 exit=0` | `CLEAN cases=22 passed=22 failed=0 exit=0` | `rv9-gate-attacks.out`; `latejoin-harness2/B5-selftest-cases.out` |
| PAIR | live pair | — | `MATCH paths=5/5 drift=0 exit=0` ×11 runs (my T2/T3/T4 + EX-29's), with and without `--require-paths 5`, both directions, vs live | §1A |
| V1 | v1 receipts still sha256-verifiable | — | r2-era pair (`arc3-loop1-round2/claims/c3/EX-31/capture-{pre,post}.txt`) → `MATCH 5/5 exit 0` | `latejoin-harness/A10-v1-v1.out` |
| SELF-PIN | receipt self-pins the tool sha | old receipts pin `112d01dc…` | every round-3 receipt (EX-29's two, my three) pins `7cd19c3c…` in its `# tool:` header | `latejoin-harness/harness.log` A9 |
| CMD-A | command A | — | `knowledge_files 82, mapped 82, missing [], dangling [], rules 14/14, coverage 10.0, depth 10.0` — **identical** to EX-21's recorded `commandA-head.json` on every field except the `revision` rendering (`c07af80` vs the full 40-hex, an invocation artifact of the recipe's `rev[:7]`) | `rv9-commandA-head.out` |

The four injections reproduce as their declared classes. The two honest caveats:
`--require-paths` deliberately does **not** change the no-flag path (D3a unchanged), which
the README and the registry row both state; and the plain 1-of-5 verify still reads
`MATCH-V1-PARTIAL exit 0` — the gate is opt-in, as declared.

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | EX-29's `MATCH 5/5` is vacuous (instrument blind in this configuration) | **REFUTED** — my own mutated-copy positive control fires `CONTENT-DRIFT paths=4/5 drift=1 exit=10` (`latejoin-harness/A5-verify-mutated.out`) |
| A2 | the pair matches only because the receipts grade their own homework | **REFUTED** — tool-free `sha256sum`/`stat` agrees with every receipt (0 mismatches, 12/12 shared fields × 5 paths) |
| A3 | the pair matches in one direction only (asymmetric compare) | **REFUTED** — T3→T2 reverse and EX-29's `verify-post-vs-pre-reverse.out` both `MATCH 5/5` |
| A4 | my reading moved the probed state (read perturbs custody) | **REFUTED** — live digests re-derived after the full battery are unchanged (`16f496e6… 38d2a1d0… bc66d543… 7d2ca28a… 6c6be761…`), and inode/size sets agree across all five receipts |
| A5 | the fail-open (D2) is only fixed for newly written receipts; a legacy receipt still reads as MATCH | **REFUTED** — a legacy receipt written by the old tool (`EXISTS: no` + `STAT-ERROR` stanza) verified by the new tool reads `UNEVALUABLE exit 14` vs live, self-vs-self, and under `--require-paths 1` (`rv9-backcompat-failopen-attack.out`) |
| A6 | `--require-paths N` counts stanzas rather than usable coverage, so a synthetic 5-stanza receipt of nonexistent paths satisfies `N=5` | **PARTIALLY CONFIRMED, not a defect** — it does count stanzas, and a 5-ghost-stanza receipt passes `--require-paths 5` with `MATCH exit 0` (`rv9-gate-attacks.out` attack A). But all five ghosts are *absent on both sides*, which is the genuine `ABSENT`/`MATCH` semantics the tool declares; the D3 hole was a **1-of-5** reference leaving four custody paths unexamined, and that is closed. Worth a line in the README if the operator wants the gate to mean "evaluable coverage". |
| A7 | `--require-paths` can be defeated by a degenerate value | **REFUTED** — `N > stanza count` → `USAGE exit 2` with the coverage line; `N = 0` is inert (no-op gate); non-integer → argparse `exit 2`; an UNEVALUABLE stanza does not count as covered (mixed receipt, `--require-paths 2` → `UNEVALUABLE exit 14`) |
| A8 | the write-guard is name-based, so a hardlink/symlink alias clobbers the target | **REFUTED** — hardlink alias refused (`exit 2`, source content intact, `latejoin-harness2/B1`); **symlink** alias of a scoped path refused (`exit 2`, target intact, `rv9-final-attacks.out` F4); the inode arm is what catches them |
| A9 | the guard only protects paths that happen to exist on this host; a custody path under a different `HOME` is unprotected | **REFUTED** — under a sandboxed `HOME=/var/tmp/rv9-scratch/homesb`, `--out $HOME/.bashrc` and `--out $HOME/.profile` are both refused `exit 2` with contents preserved; the live `~/.bashrc` attempt is likewise refused and its sha is unchanged (`rv9-custody-writeguard-sandbox.out`) |
| A10 | the revised tool is fragile like the old one when invoked under a different filename | **REFUTED** — the old tool's selftest fails one case when copied to another name (it re-invokes `Path(__file__).parent / "custody-pair.py"`, line 733) whereas the revised tool re-invokes `Path(__file__).resolve()` (line 1056) and stays `22/22 CLEAN` under a renamed copy. Incidental robustness improvement, not a claimed item. |
| A11 | other argument/IO edges crash outside the declared map | **REFUTED on all probed edges** — unreadable receipt file → `USAGE 2`; `--out <directory>` → `USAGE 2` (`write failed ([Errno 21] Is a directory …)`); duplicated `PATH` stanzas parse without crashing; `--paths <directory>` is captured as a `TYPE`-recorded entry, not a crash (`rv9-final-attacks.out` F1–F3, F7) |
| A12 | the revised tool has a sha256/size inconsistency on symlinks (I flagged this mid-review) | **REFUTED — my flag was wrong** — the stanza carries `TYPE: symlink`, `SYMLINK-TARGET: <target>`, `SIZE: 35` (the link's own `lstat` size) and `SHA256` of the *link target string* (`8f9e69a0…` = sha256 of the target path, distinct from the followed content's `aef1c130…`). Consistent and deliberate; the tool does not follow symlinks. |
| A13 | command A drifted under this round's edits | **REFUTED** — re-derived 82/82, 14/14, 10.0/10.0; identical to the recorded baseline modulo the `revision` field rendering |
| A14 | EX-21's registry-row patch is not actually apply-ready (i.e. the coupled landing cannot complete) | **REFUTED** — `apply-registry-row.py` on a scratch copy yields exactly EX-21's declared file sha `5eec51c0…` and row sha `cf5111a7…`, 390 lines, live file untouched. (Its sibling `.patch` needs `patch -p0`, not `git apply` — noted in §2, not a blocker.) |

Reviewer-side error I should own: my inherited `harness.sh` A8b asserts "expect 2" for
`--paths guard-a.txt --out guard-b.txt`. That expectation was wrong — `guard-b.txt` is
neither a scoped nor a custody path, so `exit 0` is correct. The genuine cross-guard arms
are A8a (`--paths X --out X` → 2) and B1 (hardlink alias → 2), both of which pass. The
stale comment is in the harness, not in the tool.

## 5. Blockers

None for this seat. Two items for the parent, both in §2: the SKILL.md registry row is
not yet in the worktree (one artifact short of the claim's same-commit coupling, patch
ready), and EX-21's `.patch` form needs `patch -p0` rather than `git apply`.

### 5a. Third-party clobber observed mid-review (not RV-9's doing — needs recovery)

While taking my final `git status`, a **committed round-1 custody receipt was found
overwritten in the worktree**:

- path `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`
- HEAD blob: sha256 `b8ed19365c103a4ab355678f0fffe0db4e0011a18b441e79f38d9e80de3d0776`,
  2,045 bytes / 52 lines
- worktree: sha256 `2d9bc6c0850cde7fef05d6f1cdde0c358b8065f4c615ea9f84eea2919cb7dfbd`,
  21,017 bytes / 305 lines, mtime/ctime `2026-10-19 13:25:02Z` (= 10:25:02 −03:00)
- the new content is a **VZ-4 suite transcript**, beginning
  `== VZ-4 C2 after-state suite ==` / `tool=7cd19c3c… /var/tmp/vz4r3-late/tool/custody-pair.py`

Evidence and exoneration: `rv9-third-party-clobber-observation.out`. RV-9's entire write
set for this session (enumerated there, 51 files) is confined to
`claims/c2/RV-9/**` and `seats/RV-9.md`; RV-9 never names that path as an output target
and its harnesses read only round-2 `EX-31` fixtures. The writer is identified by the
content itself: VZ-4's `c2-verify.sh` `tee -a`s its transcript into its `$3` OUT argument,
and VZ-4's `poll-log.txt` shows check=17 at `2026-10-19T13:25:03Z`, one second after the
file's mtime. This is an out-of-scope write by a concurrent seat, not a custody-path
defect and not part of the C2 claim.

Recovery (parent/operator; RV-9 performs no git mutation):
`git checkout -- .ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`

This also matters for the chain: the clobbered file is a **round-1 v1 receipt** that
EX-28's v1-compat evidence and the registry row both cite as a canonical v1 fixture
(`stanza-v1` row in the README's fixture table). If the round's commit captures the
worktree as-is, the v1 fixture the README pins would be replaced by a transcript — so
the checkout above should happen before the records commit.

**Verdict as reviewer: EX-29's pair is corroborated — `MATCH 5/5` re-derived independently,
in both directions, against live, with and without `--require-paths 5`, and against a
tool-free digest/stat capture. The four named holes reproduce as their declared classes
before and are closed after. No refutation of the chain's claim succeeded.**
