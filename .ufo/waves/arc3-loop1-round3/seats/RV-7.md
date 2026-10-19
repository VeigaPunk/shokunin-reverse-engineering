# RV-7 — seat report (chain c2, reviewer seat, wave arc3-loop1-round3)

Task (seat line): **late join** — mutation-test the guard extension + D3 on
`/var/tmp` copies of the revised tool; reverts must restore the clobber / the
1-of-5 exit 0 (load-bearing proof).

Verdict: **both load-bearing proofs CONFIRMED on the landed revision
`7cd19c3c…`**, and the prior `/dev/shm` matrix independently reproduced on
`/var/tmp` with fresh harness code. One coherence defect found in the D3 gate
(dup-stanza subversion), one cross-referenced open bypass independently
reproduced (sidecar escape).

Disposition: **COMPLETED the missing work** (seat report, `/var/tmp` matrix,
canonical-scope control, four-way D3 transcript, identity re-derivation,
proposal text) and **VERIFIED the pre-existing work** (the prior seat's
`mutants.py` matrix and its verdicts — reproduced, not trusted).

## 1. Work performed (evidence pointers)

All scratch under `/var/tmp/rv7v/` (never `/tmp`). Nothing under `.ufo/gates/`
was written — the real custody paths and the landed tool were read-only
throughout (hash/stat capture only). No git mutations.

**What existed when I joined** (prior seat, before the wave interruption):
`mutants.py`, `run-matrix.sh`, `summarize.py`, `specs/*.json`,
`pre-112d01dc*.json`, `snap-7cd19c3c-*.json`, `snap2-7cd19c3c-*.json`,
`poll-seats.sh`, `poll-log.txt`. No `seats/RV-7.md` and no `/var/tmp` run
existed.

**What I completed:**

| artifact | what |
|---|---|
| `seats/RV-7.md` | this report (was missing) |
| `rv7v-harness.py` | fresh independent harness (does not import `mutants.py`); guard scenario A1–A5 + coverage B1–B6 + selftest, class-line assertions |
| `V-clean.json`, `V-pre.json`, `V-M1.json`, `V-M1a.json`, `V-M1b.json`, `V-M2.json` | full matrix on `/var/tmp` copies (six arms) |
| `specs-v/*.json` | the four revert specs as I applied them (anchors count==1 enforced by the harness) |
| `canonical-scope-probe.py`, `canonical-scope-results.json` | canonical-`~/.bashrc` scope control: import the tool, monkeypatch `Path.write_text`, prove write-attempt vs refusal **without touching the real file** |
| `d3-fourway-transcript.txt` | PRE/POST × default/flag5 on the round-2 `v1-partial-1of5.txt` fixture |
| `m2-live-1of5-transcript.txt` | M2 load-bearing proof (1-of-5 ref, `--live --require-paths 5`: POST exit 2 + class, M2 exit 0 MATCH) |
| `clobber-fiveway-summary.txt` | PRE/POST/M1/M1a/M1b clobber demo with before/after sha256 per arm |
| `identity-rederivation.out` | rule-#14 re-derivation of every cited byte-identity |
| `rv7-proposed-coverage-gate.patch.md` | proposal text (patch text only — no tool edit) |
| `MANIFEST.sha256` | hashes of the artifacts above |

**Method notes.** The harness materialises each arm as
`<tag>/tool/custody-pair.py` because the tool's own selftest re-invokes a
sibling named `custody-pair.py`; a differently-named copy fails a case that is
not about the code under test (same observation as the prior seat). Mutants are
applied by textual revert with `count(old) == 1` asserted, so a silently
non-matching anchor aborts rather than producing a fake revert. Assertions are
on the **class line** (`REFERENCE-COVERAGE` / `USAGE: refusing`), never the exit
code alone: at PRE `--require-paths` does not exist and argparse returns exit 2
— the same code as the declared USAGE class, with no class line.

## 2. Proposed changes

`claims/c2/RV-7/rv7-proposed-coverage-gate.patch.md` — two items:

1. **Sidecar escape** (cross-ref, CR-4 `proposed-write-guard.patch.md` §1):
   `capture --paths X.sha256 --out X` → exit 0, X.sha256 overwritten by the
   receipt sidecar. Independently reproduced here (A5); no new patch text — CR-4's
   `(out, sidecar)` guard covers it. Recorded so the round report sees two
   independent reproductions.
2. **`--require-paths` coherence** (this seat's finding): the gate counts
   stanzas while printing an `unaccounted:` list it does not enforce — a
   reference repeating one path 5× prints `5/5 … unaccounted: <all five> …
   exit 0`. README wording says "stanzas", so the claim is not violated; the
   defect is that the flag does not prove canonical-path coverage. Two
   alternative one-line shapes given (enforce distinct paths, or declare the
   field advisory), plus a suggested selftest case pinning the choice.

No other change proposed: A1–A4 and B1–B5 are confirmations of the landed
declarations.

## 3. Before → after measurement (my slice of the c2 claim)

All numbers re-measured by me on `/var/tmp` copies; `PRE` = `112d01dc…`
(git HEAD blob of the tool), `POST` = `7cd19c3c…` (worktree/landed revision,
re-derived at 13:24:21Z).

**Write-guard scope (VZ-4).** Load-bearing: reverts must restore the clobber.

| arm | tool sha256 | A1 `--paths X --out X` | A2 hardlink alias | A3 symlink alias | A4 control | selftest |
|---|---|---|---|---|---|---|
| PRE `112d01dc` | `112d01dc034c…` | exit 0 **CLOBBER** | exit 0 **CLOBBER** | exit 0 **CLOBBER** | ok | 15/15 |
| POST `7cd19c3c` | `7cd19c3cfd83…` | exit 2 BLOCKED (byte-stable) | exit 2 BLOCKED | exit 2 BLOCKED | ok | 22/22 CLEAN |
| M1 (round-2 predicate restored) | `5ec0ea0b92db…` | exit 0 **CLOBBER** | exit 0 **CLOBBER** | exit 0 **CLOBBER** | ok | 20/22 DIRTY |
| M1a (scoped arm `+ paths` dropped) | `c1909a249793…` | exit 0 **CLOBBER** | exit 0 **CLOBBER** | exit 0 **CLOBBER** | ok | 20/22 DIRTY |
| M1b (inode arm dropped) | `e8fbb263ed47…` | exit 2 BLOCKED | exit 0 **CLOBBER** | exit 2 BLOCKED | ok | 21/22 DIRTY |

The guard extension is **load-bearing**: removing either the scoped arm or the
inode arm restores a measured clobber; the shipped selftest kills both mutants
(M1/M1a fail `refuses-to-write-over-scoped-path` + `refuses-write-through-hardlink-alias`;
M1b fails the hardlink case only). Causal attribution is clean — M1b shows the
resolve arm alone still catches the same-path and symlink spellings, so the
inode arm's contribution is specifically the hardlink alias.

**D3 reference coverage.** Load-bearing: reverts must restore the 1-of-5 exit 0.

| shape | PRE `112d01dc` | POST `7cd19c3c` | M2 (gate disabled) |
|---|---|---|---|
| `verify r1 --live` (1-of-5, no flag) | exit 0 `MATCH-V1-PARTIAL` | exit 0 `MATCH-V1-PARTIAL` (declared opt-in) | exit 0 `MATCH` |
| `verify r1 --live --require-paths 5` | exit 2, **no class** (argparse: flag unknown) | exit 2 + `REFERENCE-COVERAGE: 1/5 … unaccounted: <4>` | exit 0 `MATCH paths=1` |
| `verify r1 r5 --require-paths 5` | exit 2, no class | exit 2 + class | exit 12 (drift) |
| `verify r5 r5 --require-paths 5` (control) | exit 2, no class | exit 0 `MATCH 5/5` | exit 0 |
| v1-1of5 fixture, `--live --require-paths 5` | exit 2, no class | exit 2 + class | — |
| dup-stanza ref (5 stanzas, 1 path), `--require-paths 5` | exit 2, no class | **exit 0 `MATCH paths=1`** ← subversion | exit 0 |

M2 restores the round-2 behaviour exactly: the flag is parsed and then ignored,
so a 1-of-5 reference reads exit 0 `MATCH paths=1/1` with four paths unexamined
— the debt D3 named, reproduced. The landed gate closes it on the flag path.

**Canonical-scope control** (all five arms, write intercepted): every arm,
including PRE and all mutants, returns exit 2 with **no write attempt** and
`~/.bashrc` sha256 `7d2ca28a…` unchanged before and after. This confirms the
mutation is observable only on the scoped arm (the canonical five were guarded
in round 2 as well) and that no arm can clobber a real custody path even when
its guard is reverted.

**Selftest census** (POST, default scratch): `CUSTODY_PAIR_SELFTEST: CLEAN
cases=22 passed=22 failed=0 exit=0` — the claim's 15 → ≥17 is exceeded (22).

## 4. Attacks / refutations attempted

1. **"The landed guard is only the canonical-path guard; the scoped arm is
   dead code."** Refuted: M1a (scoped arm dropped, everything else intact)
   restores the clobber at exit 0. The scoped arm is the difference between
   BLOCKED and CLOBBER. *Verdict: guard extension confirmed load-bearing.*
2. **"The inode arm is unnecessary; the resolve arm suffices."** Refuted on the
   hardlink spelling: M1b (inode arm dropped) clobbers through a hardlink alias
   at exit 0 while the same-path and symlink spellings stay BLOCKED. *Verdict:
   inode arm load-bearing for the hardlink shape only — precisely scoped.*
3. **"D3's flag was cosmetic (always-on gate would be needed)."** Partially
   refuted and partially confirmed: the flag path is load-bearing (M2 restores
   exit 0), but the default path is still exit 0 on a 1-of-5 reference — by
   design, declared in README and docstring. *Verdict: claim-conformant; the
   gate is opt-in.*
4. **"The gate cannot be satisfied by a degenerate reference."** **Refuted
   (new finding).** A 5-stanza reference repeating one path passes
   `--require-paths 5` at exit 0 while the printed line lists all five canonical
   paths as unaccounted. *Verdict: subversion confirmed; proposal item 2.*
5. **"The write-guard covers everything it writes."** **Refuted (reproduction
   of CR-4 §1).** The derived sidecar path escapes the guard: `--paths
   X.sha256 --out X` → exit 0, X.sha256 overwritten. *Verdict: open bypass
   reproduced independently; cross-referenced, not re-proposed.*
6. **"The prior `/dev/shm` matrix was measuring a different revision."**
   Refuted: the prior JSONs pin `tool_src_sha256 7cd19c3c…` — the same landed
   revision I used; their mutant shas differ from mine only in comment text
   (verified semantically identical revert specs, anchors count==1 in both).
   *Verdict: prior matrix valid; my run is an independent reproduction, not a
   correction.*
7. **"A reverted guard would clobber a real custody path."** Refuted by the
   canonical-scope probe (item: all arms refuse, `~/.bashrc` untouched). The
   guard's canonical arm was never the mutation target, and the canonical five
   were guarded pre-revision too. *Verdict: no custody path was ever at risk in
   this seat's work.*
8. **"The exit-2 collision makes the PRE/POST D3 comparison vacuous."**
   Acknowledged and handled: PRE's exit 2 comes from argparse with **no**
   `REFERENCE-COVERAGE` line; POST's exit 2 carries the class line. The
   discriminating assertion is the class line, and M2 (flag exists, ignored)
   breaks the tie with exit 0. *Verdict: comparison is sound.*

## 5. Blockers

None. `/tmp` was never used; `/var/tmp` had ample space (697G free). The real
tool and custody paths were read-only for this seat. The two open items in §2
are proposals, not blockers — they do not block the c2 claim as frozen (the
sidecar item is CR-4's open proposal; the dup-stanza item is a coherence defect,
not a named debt).

Rule-#14 note: every identity cited above is re-derived in
`identity-rederivation.out` (tools, mutants, git blobs, EX-21's own receipt
self-pin `# tool: custody-pair.py sha256 7cd19c3c…`, canonical control). The
artifact hashes are re-derived in `MANIFEST.sha256` after the last write to
each file.
