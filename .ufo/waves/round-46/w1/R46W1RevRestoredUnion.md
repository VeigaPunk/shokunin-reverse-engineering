# R46W1RevRestoredUnion — freeze-integrity restore arm and R45-CL18 re-entry

Seat: wave 1 reviewer. Lane `kaidoku-shokunin`. Read-only on the lane tree; every write is
under `.ufo/waves/round-46/w1/R46W1RevRestoredUnion/`. Scratch root
`/fast/scratch/hyaku/kaidoku-r46/R46W1RevRestoredUnion` (removed after the receipts below
were copied here). No installs.

Lane revisions measured (the lane is live — it moved four times while this seat ran):

| label | commit | note |
|---|---|---|
| declared freeze | `31820472784284727546808acc31b3ea1e73919b` | prompt + `plans/round-46-claims.md`; `git log -1 -- plans/round-46-claims.md` still returns it |
| F2 | `50862e4a` | `attest.py`, `gate.py`, `registry.py` |
| F3 | `65678df0` | `attest.py` |
| F4 = last frozen-byte touch | `0425224756791b414454df28a9abf93dcdf154ce` | `registry.py` |
| HEAD at measurement | `21b55a8f`, then `deee6595` | no frozen path touched (`git log -1 -- tools/round-46/` = `0425224`) |

## 1. The assigned checks

**R45-CL18 cannot re-enter by its own vector.** Round 46 exposes no caller-supplied frozen
path at all: `--freeze-path` is rejected by both counters with exit 2 (receipts E13/E14),
and both call `gate.freeze_state(root, freeze, rev, SPECS[spec]["claims"])` with the same
claims path (`attest.py:442`, `registry.py:390`). The derived set is therefore identical in
both receipts: `["tools/round-46/", "plans/round-46-claims.md"]` (E5 vs E6).

**Restore-only history now reads `restored` and exit 2 — for a file and for a directory.**
Fixture: one repo per case, `git init -q` into `$S`, toplevel asserted before the first
commit, claims file listing a FILE (`plans/round-46-claims.md`) and a DIRECTORY
(`tools/round-46/`).

| case | history | exit | `touched` | `blob_changed` | `restored` |
|---|---|---|---|---|---|
| C0 control | freeze == rev | **0** | `[]` | `[]` | `[]` |
| C1 file, tamper kept | 1 commit | **2** | `[claims]` | `[claims]` | `[]` |
| C2 file, tamper + restore | 2 commits | **2** | `[claims]` | `[]` | **`[claims]`** |
| C3 dir file, tamper kept | 1 commit | **2** | `[attest.py]` | `[tools/round-46/]` | `[attest.py]` ← see F4 |
| C4 dir file, tamper + restore | 2 commits | **2** | `[attest.py]` | `[]` | **`[attest.py]`** |
| C5 dir, **add-only** commit | 1 commit | **2** | `[extra.py]` | `[tools/round-46/]` | `[extra.py]` ← see F4 |
| C6 dir file, delete + restore | 2 commits | **2** | — | `[]` | `[gate.py]` |
| C7 dir file, rename out + back | 2 commits | **2** | both names | `[]` | both names |

So the answer to the seat question is **yes**: a restore-only history yields non-empty
`restored` and exit 2, for a frozen file and for a file inside a frozen directory; a commit
that only adds a file inside the frozen directory also exits 2. C1/C3 are the controls that
show the arm is not simply reporting exit 2 unconditionally (C0 is 0).

**The exact R45-CL18 shape, same history, two instruments.** Fixture: frozen file named only
on the command line + frozen directory named by the pathspec; freeze → tamper the file →
restore the exact bytes (E11):

```
round-45 frozen-path-preflight.py --pathspec tools/round-46/ --freeze-path plans/round-46-claims.md
  exit 0   touched []  blob_changed []  restored []   verdict clean      <- the hole reproduces
round-46 gate.freeze_state
  exit 2   touched [claims]  blob_changed []  restored [claims]
round-46 attest.py   (fixture's own copy)  exit 2  reason frozen_path_changed
round-46 registry.py (fixture's own copy)  exit 2  reason frozen_path_changed
```

Round 45 read `clean` because `touched` came only from the `--pathspec`-scoped log while the
`--freeze-path` file entered just the blob arm
(`tools/round-45/frozen-path-preflight.py:107-138`). Round 46 feeds both arms from one
derived set, so that specific divergence is gone.

## 2. Findings

### F1 (HIGH, mechanical, blocks admissibility) — the declared freeze cannot be scored

`tools/round-46/` was modified by three commits **after** the declared freeze, so both
counters exit 2 `frozen_path_changed` at every rev ≥ `50862e4a`:

```
git diff-tree -r --name-status 3182047 HEAD -- plans/round-46-claims.md tools/round-46/
M  tools/round-46/attest.py
M  tools/round-46/gate.py
M  tools/round-46/registry.py

attest.py   --freeze 3182047 --rev 21b55a8f   exit 2  (E5)   sha 8e32d11e…
registry.py --freeze 3182047 --rev 21b55a8f   exit 2  (E6)   sha 2f6a9035…
```

and the same counters cannot rescue it by scoring *at* the freeze, because the artefact does
not exist there:

```
attest.py --freeze 3182047 --rev 3182047      exit 1  rule_blocks 22  marker 0  block_present 0  (E7)
```

Only the last frozen-byte touch scores, and it is not the freeze the claims file names:

```
attest.py --freeze 0425224 --rev 21b55a8f     exit 0  met_target true  13 rows, 9 refs      (E8)
attest.py --freeze 0425224 --rev 0425224      exit 0  met_target true                        (E9)
attest.py --freeze 65678df --rev 21b55a8f     exit 2  (registry.py changed at 0425224)       (E10)
```

This corroborates `R46W1RegC` (line 41+), `R46W1RegD` (line 47+), `R46W1RegG` (§F1) and
`R46W1RegH` (§F1) — no disagreement, and my values match theirs commit for commit. The
instrument is behaving correctly; the round's own history violates the rule it froze
(`plans/round-46-claims.md` §Freeze-integrity: "A score at `REV` is admissible only if no
commit in `FREEZE..REV` touches a frozen path"). `git log --format=%H -1 --
plans/round-46-claims.md` re-derives `3182047`, so the claims file's own re-derivation rule
also cannot name a scorable freeze.

Cheap guard that would have made this impossible to write down (recommendation, not applied):
assert `git log -1 -- <each derived frozen path>` at `rev` equals `freeze`, exit 2
`freeze_is_not_last_touch` otherwise. Measured cost: one `git log` per entry.

### F2 (HIGH, instrument; new) — the frozen set is derived from the measured revision, so the measured revision can shrink it

`gate.py:152` derives the set at `tip` (`frozen_set(root, tip, claims)`), and `tip` is the
artefact's own revision. One commit that rewrites the `## Frozen paths (exact)` section and
edits a frozen tool makes the arm read clean:

```
E1a  gate.py edited by one comment line, genuine frozen section   exit 2  frozen_path_changed
     [tools/round-46/, tools/round-46/gate.py]  restored [tools/round-46/gate.py]
E1b  + one commit rewriting the section to `- `corpus/``           exit 0  met_target true
     frozen_derived [corpus/]  frozen_path_changed []  restored []
     (history still contains M tools/round-46/gate.py; no arm reads it)
E1c  union arm: frozen_set at the FREEZE + history/blob arms
     touched [plans/round-46-claims.md, tools/round-46/gate.py]  blob_changed both  -> exit 2
```

The decoy does not even have to exist: `- `does/not/exist/`` gives exit 0
(E12, `shrink2.out`), because `frozen_set` never checks existence and `blob_changed` treats
two absent blobs as equal (E1b receipt `frozen_derived ["does/not/exist/"]`, `touched []`).
Partial shrink is caught (C9/`C9_partial_shrink`: dropping only the directory line leaves
the claims file self-listed, so its own edit is touched → exit 2). The minimal attack is
therefore: remove both real lines, add any one decoy line, edit the tool, one commit.

Class-wise this *is* R45-CL18 re-entering through a different door: round 45's defect was
"the arm's scope is not the frozen set"; here both arms share a set the measured revision
controls. Fix measured in E1c: derive at `freeze` too and take the union (or require the
base set ⊆ tip set and use the base set).

### F3 (HIGH, instrument; new) — the bytes that compute the verdict are never the bytes examined

`freeze_state` reads Git objects only; the counter itself executes from the worktree. No arm
reads the worktree: `gate.dirty()` exists (`gate.py:132`) and has **no caller** anywhere in
`tools/round-46/` (E16 static grep: only `attest.py:46`/`:508` vocabulary mentions and the
definition). Meanwhile `plans/round-46-claims.md:172` asserts the derived set is used "for
the history arm, the blob arm **and the dirty scope**" — that third scope does not exist.

Measured red→green flip with zero commits:

```
E2a  gate.py comment-line edit committed, clean worktree    exit 2  frozen_path_changed
E2b  same revs, worktree gate.py replaced with a permissive freeze_state
     exit 0  met_target true  frozen_derived []   (stub ran)
git status --porcelain:  M tools/round-46/gate.py
```

The pin clause does not close this: block 23 pins `tools/round-46/attest.py` **at `--rev`**
(`attest.py:247-251`), not `gate.py`, and not the executing file. A dirty `gate.py` is
therefore unpinned and unread. This is the same failure family as R45-CL15 (the dirty arm)
with a sharper consequence: the verdict computer, not just the graded surface, is forgeable.

### F4 (MEDIUM, diagnostic; verdict unaffected) — `restored` is not restoration for directory entries

`gate.py:160` computes `restored = [p for p in touched if p not in changed]`, but `touched`
carries file paths while `changed` carries the directory token for a frozen directory. Every
touched file under a changed directory is therefore reported as restored. Measured:

- C3 (tamper **kept**): `blob_changed [tools/round-46/]`, `restored [tools/round-46/attest.py]`
  — the file is net-modified, and `restored` says the blob arm finds it clean.
- C5 (**add-only**): `restored [tools/round-46/extra.py]` — a file that did not exist at the
  freeze and was never restored is named restored.
- E1a and the real lane (E5): all three genuinely modified files are named restored while
  `blob_changed` reports the directory.

So block 22's "`restored[]`, disjoint from `blob_changed[]`" is satisfied only textually, and
the claims file's "`restored` names a path the history arm saw and the blob arm finds clean"
is false for directory entries. Exit codes stay 2, so no score changes; the evidence field
does. Escape hatch used above: `git diff-tree` and `git diff 3182047 HEAD -- <file>` show the
truth. Fix: expand directory entries to the touched file set and blob-compare per file, then
keep `restored` only for paths whose blobs are equal at both revisions.

Corroborates `R46W1RegD` §F6 and `R46W1RegH` §F2 (same mechanism); my file-freeze control
(C1, `restored []` when the change is kept; C2, `restored [claims]` when it is restored)
bounds the defect: it is directory-entry-only, not general.

### F5 (LOW) — the restore-only path is not in the selftest, and `--selftest` is unreachable as written

`attest.py` has 16 cases, not the 15 the claims file's Satisfiability preflight prints
(E15). The only frozen-touch case, `red-frozen-touched-is-exit-2`, **appends** to the claims
file (`attest.py:593-598`) — a net change, not a restore — so no case exercises the
restore-only path this seat was asked about; the C1–C7 matrix above is the first evidence
for it. And `python3 -I -B tools/round-46/attest.py --selftest` exits 2 at argparse because
`--root/--freeze/--rev` are `required=True` and `--selftest` is handled after `parse_args`
(E4); the preflight sentence is false as spelled. Same for `registry.py`. Corroborates
`R46W1RegH` §F3.

### F6 (INFO) — rename pairs are parsed one-sided, but the blob arm covers it

`history_touched` does not pass `--no-renames` (`gate.py:99`), and the `-z` parser advances
two tokens per status (`gate.py:105-112`), so an `R100` record contributes only the first
path of the pair. Measured C7 (rename out then back): both names appear only because two
commits each contribute one side. A net rename still exits 2 through the directory blob
entry, so the verdict is sound; the `touched` list is incomplete, which matters only if a
consumer reads `touched` as a census of edits.

## 3. Reconciliation and residual risk

- Corroborating, not contradicting: F1 = RegC/RegD/RegG/RegH §F1; F4 = RegD §F6, RegH §F2;
  F5 = RegH §F3. Distinct from them: F2 (self-shrink, with the decoy-existence and
  partial-shrink bounds and a measured union fix) and F3 (dirty verdict computer, with the
  `dirty()`-uncalled and `plans/round-46-claims.md:172` text mismatch).
- **Not run, so not passed:** the merge arm (`-m --diff-merges=first-parent`, R45-CL6) —
  another seat's; the C1 9-forgery battery and the C2 7-forgery battery; C2's clauses 1–5;
  the squash-fold limit of R45-CL19 (stated as inherent in the claims file, nothing to add).
- The `--check-dirty` arm does not exist in round 46 to run (F3), so R45-CL15's union
  question has no instrument here to answer it.
- All lane measurements used `--no-battery`; exit codes and receipts are for the freeze arm,
  which short-circuits before scoring anyway when it trips.
- Caveat on admissibility of F2/E1b: E1b/E2b are scratch fixtures built from `git archive
  HEAD`; they are evidence about the instrument, not a claim about the lane's history.

## 4. Receipts (exact command → exit, stdout sha256, UTC)

Files in this directory; `sha256` of each receipt file listed at the end.

| id | command | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| E5 | `python3 -I -B tools/round-46/attest.py --root . --freeze 3182047 --rev 21b55a8f --no-battery` | 2 | `8e32d11e7da64a6e22cc4be682ccc6b0d7e4741b33da82bbba15671ea9dbab6d` | 17:04 |
| E6 | `python3 -I -B tools/round-46/registry.py --root . --freeze 3182047 --rev 21b55a8f` | 2 | `2f6a9035929498abc996f622eba92b008aedab406be433600b48c5a6a8c5d63b` | 17:01 |
| E7 | `… attest.py --freeze 3182047 --rev 3182047 --no-battery` | 1 | `547507e636c98d5152689d179b2dbb98841a1257428261ae0b26fd11aa94eb45` | 17:01 |
| E8 | `… attest.py --freeze 0425224 --rev 21b55a8f --no-battery` | 0 | `13e4e16e24469fd1ce2c286acd842153abe51e920373a0023e19ddacf96378df` | 17:04 |
| E9 | `… attest.py --freeze 0425224 --rev 0425224 --no-battery` | 0 | `0866041b0d3f220c61b421fa494c0a2e6e6c1cfe5a33586315362b8f2f6109d2` | 17:04 |
| E10 | `… attest.py --freeze 65678df0 --rev 21b55a8f --no-battery` | 2 | `268e99823cb29bb7826086511a6c1efbac727611a29744b86a4b9612ad393182` | 17:04 |
| E13 | `… attest.py --freeze-path plans/round-46-claims.md` | 2 | `e4be0e2ed9bc39b0b949722cbbb73392d6908a8a145631924ffff4f37e50a06a` | 17:04 |
| E14 | `… registry.py --freeze-path plans/round-46-claims.md` | 2 | `8a1e279d11c5130ab2085fe1427719d7c3ca668ada49b974a7d83ae58535ba0d` | 17:04 |
| C0–C9 | `drive.py` (fixture matrix; per-case cmd/exit/sha/utc in `receipts.json`) | 0 for C0, C8, C8b; 2 for C1–C7, C9 | see `receipts.json` | 17:00 |
| E11 | `contrast.py` (R45 vs R46 on the CL18 history) | 0 then 2,2,2 | see `cl18-receipts.json` | 17:02 |
| E1a–E1c, E2a–E2c | `exploit.py` (archive fixtures) | 2→0, 2→0 | see `exploit-receipts.json` | 17:03 |
| E12 | `shrink2.py` (decoy that exists nowhere) | 0 | receipt in `shrink2.out`; self-hash `a412d933b7dd20cbfda5519830505418315e65fa9c1d55e108c1967d85d86e86` | 17:05:46 |
| E15 | `… attest.py --selftest` (as the claims file spells it) | 2 | — (argparse; case list with args: 16 cases) | 17:04 |

Receipt-file digests (sha256 of the file as stored here):
`receipts.json e0312ba82a5b4ce54b106d59377f322afaf89960c4245f224a9a829dc0751559`,
`summary.json 812998ad866ba536308b02df53bd012623e10413e8bf78e5184bc5a715ec2726`,
`cl18-receipts.json fbdb35be0fd78d2e6f653466023fe0dd0c935f87d8a6249694f996f3f3708308`,
`exploit-receipts.json 2be4e0eb88ffb4bac48e29b368c5f5cdaa94969558ce238790597749b0ced522`,
`shrink2.out e15f974b31830db1f40b4abb274afb85ec046ee68ce7e53bf7e6c48086d0edc6`.
Lane stdout captures: `stdout-declared-current.txt`, `stdout-0425224…txt`,
`stdout-65678df…txt`, `stdout-self-0425224.txt`, `stdout-freeze-path-rejected.txt`,
`stdout-reg-freeze-path-rejected.txt`, `at-*.json`, `reg-3182047-HEAD.json`.

Provenance of the scripts stored here: `drive.py`, `contrast.py`, `exploit.py`,
`shrink2.py` are the drivers that produced the receipts above, with one post-run
change — each now bootstraps its own `$S/lib/gate.py` copy from the lane before
importing, so they run without the deleted scratch tree. Nothing else differs.
No lane file was modified by this seat: `git status --porcelain -- 
plans/round-46-claims.md tools/round-46/` is empty at the time of writing.

## 5. What the L1 can land

1. **Admissibility**: the round's `met` is reproducible only at `FREEZE=0425224`. Either
   record it as such (and accept that the frozen text names `3182047`), or land the claim as
   not admissible this attempt. Do not cite `3182047..HEAD` as clean: E5/E6.
2. **Block-23 row R45-CL18 is true as stated** ("one frozen set derived from the claims file
   feeds both arms, so the sets cannot differ") — E11 closes it for the file-only-CLI vector.
   It should not be widened to "restore is detected in every case": F2/F3 are the two cases
   where the class re-enters.
3. If a row is added for the closure, the honest wording carries the two new red cases:
   `frozen-set shrunk at the measured revision` → exit 2 required, currently exit 0 (F2);
   `verdict computer edited in the worktree` → exit 2 required, currently exit 0 (F3).
   Both have measured red fixtures (`exploit.py`) and a measured green fix for F2 (union at
   the freeze), so they are landable rows, not observations.
