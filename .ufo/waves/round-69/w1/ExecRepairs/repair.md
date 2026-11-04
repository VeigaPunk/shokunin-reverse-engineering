# ExecRepairs — R68-V4 repair draft (kaidoku round 69, w1)

Seat: `ExecRepairs` (executor, leaf). Drafts only: nothing under a tracked path was edited, and the L1
lands every file. Target: `tools/round-29/prefile-check.sh` (sha256
`569576937e6d08f62ce8c4435918d7f807b9c818128d7371e996d6ae758ff59c`, 52 lines, file max width 122).
Source of the assignment: `corpus/lessons/round-68-verifier-spotcheck.md` §5 defect **R68-V4** and
`.ufo/waves/round-68/w1/ExecLedger/report.md` §2.5.

Measured at lane HEAD `3f3d20fc065b5be62f676028b9a38d316ddfe8fd`; base
`d7d9a62cc70935304e600ed0dee864fc4f1751f7`. Every conclusion below is labelled **observation**
(a command was run, or a source file was read) or **inference**. Nothing was re-frozen, narrowed or
widened: the defect is attacked as written.

Line-number note (**observation**): the closure cites `:31-35`, but the comment block that carries both
false sentences is lines **31-36**, and the failure branch is lines **38-44** (`legacy_sha` sits on 37
between them). Both hunks below are stated with the line numbers of the file as it stands.

---

## 1. Frozen inputs read (read-only)

| path | sha256 |
|---|---|
| `tools/round-29/prefile-check.sh` | `569576937e6d08f62ce8c4435918d7f807b9c818128d7371e996d6ae758ff59c` |
| `.ufo/waves/round-24/tools/freeze-gate.py` (the round-24 gate) | `8a71fe84b94310b1b600793b4af011e586359304a6302ee33662d6522290b329` |
| `corpus/claim-freezes.tsv` (retired ledger) | `2a840d72acfd71e55fc16aa614dcefee7afd0cf67e276b799ac9d41e773dda81` |
| `tools/round-29/freeze-gate.py` (the round-29 gate) | `25b54339ce5f966309ce159fd2767579521d05eb239916d7dee0269f88b93eb2` |

The round-24 gate is **read-only** (**observation**, source read): its only external effects are six
`git` read subcommands — `cat-file`, `log`, `ls-tree`, `rev-list`, `rev-parse`, `show` — and a
`print(json.dumps(...))` to stdout. `grep -nE "write_text|open\(.*['\"]w|\.write\(|mkdir|unlink|rename|shutil|tempfile"`
over it returns nothing; its `main()` has no `--json-out` and calls no writer. Its bytes are identical
(`8a71fe84…`) at `f78fc766`, `6ffa9ce1`, `9be55c41`, `3f3d20fc` and the base `d7d9a62`, and its last
modification is `9fb4eacd` (2026-10-21, round 24), i.e. the gate pre-dates every revision it was run
against here. Running it is therefore a read, not a state change.

---

## 2. The three named defects, measured

### 2.1 (a) "It stops at round-52" — **false**

```
$ tail -n +2 corpus/claim-freezes.tsv | grep -c .
21
```
```
$ tail -n +2 corpus/claim-freezes.tsv | cut -f1
round-14 … round-32, round-34, round-35        (21 lines, in file order)
```
```
$ tail -n +2 corpus/claim-freezes.tsv | cut -f1 | sed 's/round-//' | sort -n | awk 'NR==1{min=$1} {max=$1} END{print "min="min" max="max}'
min=14 max=35
```
```
$ for r in 33 36 40 50 51 52 53 68; do printf 'round-%s: %s\n' "$r" "$(grep -c "round-$r" corpus/claim-freezes.tsv)"; done
round-33: 0
round-36: 0
round-40: 0
round-50: 0
round-51: 0
round-52: 0
round-53: 0
round-68: 0
```
```
$ wc -l corpus/claim-freezes.tsv ; tail -n +2 corpus/claim-freezes.tsv | grep -c '^$'
22 corpus/claim-freezes.tsv
0
```

**Observation:** the file holds 21 data rows under its 4-column header (`round verdict findings
pointer`): rounds **14-32, 34, 35**. Its last round is **round-35**, not round-52, and it carries no
blank rows. The rounds absent between 14 and 68 are `33` and `36-68`.

**Observation (why 36-52 is not a dropped range):** those rounds never carried a `claims.json`, which
is the only container the round-24 gate's expected set admits:

```
$ for n in $(seq 36 52); do c=$(ls .ufo/waves/round-$n/claims*.json 2>/dev/null | wc -l); printf '%s:%s ' "$n" "$c"; done
36:0 37:0 38:0 39:0 40:0 41:0 42:0 43:0 44:0 45:0 46:0 47:0 48:0 49:0 50:0 51:0 52:0
$ git log --all --format='%h %ci %s' --diff-filter=A -- '.ufo/waves/round-3[6-9]/claims.json' \
    '.ufo/waves/round-4[0-9]/claims.json' '.ufo/waves/round-5[0-2]/claims.json'
(no output — never added, never deleted)
```

So "stops at round-52" overstates the file by 17 rounds that never existed there; the true sentence is
"it carries nothing after round-35". This is the same reading the ExecLedger seat recorded
(`report.md` §2.5 nit 1), re-derived here from the bytes.

**Observation (the stray row):**

```
$ grep -n '^round-35' corpus/claim-freezes.tsv
22:round-35	FLAGGED	INSTRUMENT_ABSENT,INSTRUMENT_REVISED	counter and freeze file were first committed …
$ ls .ufo/waves/round-35/ | grep claims
claims-canonical.json
claims-frozen.json
$ test -f .ufo/waves/round-35/claims.json && echo YES || echo NO
NO
$ git log --format='%h %ci %s' --diff-filter=D -- .ufo/waves/round-35/claims.json
13d7a815 2026-10-25 16:07:04 -0300 round-35: freeze commit F3 — canonical claims-frozen.json (complete instruments container), counters read the frozen path; draft claims.json removed
$ git cat-file -e 13d7a815^:.ufo/waves/round-35/claims.json && echo present-before
present-before
```

**Observation:** round-35's container is `claims-frozen.json`; its `claims.json` existed until
`13d7a815` and was removed there. The round-24 gate's `CLAIMS` regex matches only
`.ufo/waves/(round-N)/claims.json$`, so a `round-35` row can never enter its expected set — the gate
reports it as `stray` at every revision measured below.

### 2.2 (b) "the gate reported 20 exact of 36 on every round from 53 on" — **false as written**

The round-24 gate **can** be run read-only (see §1), so it was run rather than cited. Command shape:

```
$ python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py \
    --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev <rev> --disclosures corpus/claim-freezes.tsv
```

| revision | audited | exact | of | missing | stray | exit |
|---|---|---|---|---|---|---|
| `f78fc766` (round-53's ledger-verdict commit) | 21 | 20 | **21** | `["round-53"]` | `["round-35"]` | 1 |
| `6ffa9ce1` (round-68 landing) | 36 | 20 | **36** | round-53 … round-68 (16 keys) | `["round-35"]` | 1 |
| `d7d9a62…` (this round's base) | 36 | 20 | **36** | same 16 keys | `["round-35"]` | 1 |
| `3f3d20fc` (lane HEAD at measurement) | 37 | 20 | **37** | round-53 … round-69 (17 keys) | `["round-35"]` | 1 |

Receipts: `evidence/r24-gate-at-f78fc766.json`, `evidence/r24-gate-at-6ffa9ce1.json`,
`evidence/r24-gate-at-d7d9a62cc70935304e600ed0dee864fc4f1751f7.json`, `evidence/r24-gate-at-head.json`.

**Observation:** `exact` is `20` at all four revisions, but `of` is the audited `claims.json`
population and moves 21 → 36 → 36 → 37. The only invariant across "round 53 on" is
`stray ["round-35"]` plus exit 1 — not "20 of 36". `of` also cannot be 36 at round 53: at `f78fc766`
the population was 21. The ExecLedger receipt (`evidence/r24-verdicts.tsv`,
`evidence/r24-gate-claim-freezes-at-4b0892cd.json`) reads `audited 36, exact 20 of 36` at the round-68
close, which this table reproduces at `6ffa9ce1`; the 21/37 rows are first-hand here.

**Observation:** the gate's expected set is built from `git ls-tree -r … .ufo/waves/` filtered by
`^\.ufo/waves/(round-[0-9]+)/claims\.json$` (gate source, `audit()`), so "of" is the lane's claims.json
count by construction — the denominator grows with the lane and can never be pinned at 36.

### 2.3 (c) `${got:-absent}` is unreachable — **confirmed**

```
$ git -C /fast/scratch/hyaku/kaidoku-r69/ExecRepairs/fixtures/absent show HEAD:corpus/claim-freezes.tsv
fatal: path 'corpus/claim-freezes.tsv' does not exist in 'HEAD'
rc=128
$ git -C …/fixtures/absent show HEAD:corpus/claim-freezes.tsv 2>/dev/null | sha256sum
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  -
$ printf '' | sha256sum
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  -
$ got=$(git -C …/fixtures/absent show HEAD:corpus/claim-freezes.tsv 2>/dev/null | sha256sum | cut -d' ' -f1)
$ echo "got=[$got]"; [ -z "$got" ] && echo EMPTY || echo NONEMPTY; echo "expansion=[${got:-absent}]"
got=[e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855]
NONEMPTY
expansion=[e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855]
```

**Observation:** a failed `git show` leaves stdout empty, `sha256sum` still emits the digest of empty
input, so `got` is never the empty string and `:-` never substitutes. The "absent" case is therefore
reported as `got e3b0c442…`, i.e. as if the ledger had changed. Functionally the step still fails
(which is the safe direction); only the diagnostic is wrong. Verified on a scratch fixture where the
path is absent at `HEAD`, in §4.

---

## 3. Exact replacement text

### Hunk A — comment, replacing current lines **31-36** (6 lines → 9)

```text
# ledger1 (round-68 erratum r68-1): corpus/claim-freezes.tsv is RETIRED as a gate input. It carries
# 21 rows (rounds 14-32, 34, 35), nothing after round-35; its stray round-35 row can never match
# because round-35's container is claims-frozen.json (its claims.json was removed at 13d7a815) and
# the round-24 gate's expected set is .ufo/waves/round-N/claims.json only. The gate's denominator
# follows the lane's claims.json population, so the "of" grows while the exact count held at 20:
# 20 of 21 at f78fc766 (round 53), 20 of 36 at 6ffa9ce1 (round 68), 20 of 37 at 3f3d20fc (round 69),
# stray ["round-35"] and exit 1 at each, so the step failed by construction at every revision. The
# file is kept as frozen evidence: this step asserts its bytes are identical to its retirement pin,
# and the live check is ledger2 below.
```

Widths: 99, 96, 98, 97, 96, 100, 98, 99, 38 — all ≤ 100, inside the file's existing 93-100 comment
convention (whole-file max stays 122).

### Hunk B — failure branch, replacing current lines **38-44** (7 lines → 11)

Inserted guard (lines 41-45 of the patched file), then the existing compare is unchanged:

```sh
if git -C "$root" cat-file -e "$rev:corpus/claim-freezes.tsv" 2>/dev/null; then
    got=$(git -C "$root" show "$rev:corpus/claim-freezes.tsv" 2>/dev/null | sha256sum | cut -d' ' -f1)
else
    got=
fi
if [ "$got" = "$legacy_sha" ]; then
    echo "prefile: ledger1 retired (erratum r68-1) — legacy ledger byte-identical to its retirement pin"
else
    echo "prefile: ledger1 legacy ledger changed (want $legacy_sha, got ${got:-absent})"
    fail=1
fi
```

The `got=` assignment and every line after it are byte-identical to today's; the guard only makes `got`
_genuinely_ empty when the path does not exist at `$rev`, which is the condition `${got:-absent}`
already tries to describe. The presence test is the idiom the same script already uses one step below
for the v2 ledger (`if git -C "$root" cat-file -e "$rev:corpus/claim-freezes-v2.tsv" 2>/dev/null`), so
this adds no second convention. It also removes reliance on a magic digest: the empty-input hash never
appears in the message path.

### Full unified diff (identical to `evidence/patch.diff`)

```diff
--- a/tools/round-29/prefile-check.sh
+++ b/tools/round-29/prefile-check.sh
@@ -28,14 +28,21 @@
     echo "prefile: tree clean"
 fi
 rev=$(git -C "$root" rev-parse HEAD) || exit 2
-# ledger1 (round-68 erratum r68-1): corpus/claim-freezes.tsv is RETIRED as a gate input. It stops at
-# round-52 while rounds 53-68 live in the v2 ledger, and it carries a stray round-35 row whose
-# container is claims-frozen.json, which the round-24 gate's expected set (claims.json files only)
-# cannot match; the gate reported 20 exact of 36 on every round from 53 on, so this step failed by
-# construction and the prefile gate never passed. The file is kept as frozen evidence: this step
-# asserts its bytes are identical to its retirement pin, and the live check is ledger2 below.
+# ledger1 (round-68 erratum r68-1): corpus/claim-freezes.tsv is RETIRED as a gate input. It carries
+# 21 rows (rounds 14-32, 34, 35), nothing after round-35; its stray round-35 row can never match
+# because round-35's container is claims-frozen.json (its claims.json was removed at 13d7a815) and
+# the round-24 gate's expected set is .ufo/waves/round-N/claims.json only. The gate's denominator
+# follows the lane's claims.json population, so the "of" grows while the exact count held at 20:
+# 20 of 21 at f78fc766 (round 53), 20 of 36 at 6ffa9ce1 (round 68), 20 of 37 at 3f3d20fc (round 69),
+# stray ["round-35"] and exit 1 at each, so the step failed by construction at every revision. The
+# file is kept as frozen evidence: this step asserts its bytes are identical to its retirement pin,
+# and the live check is ledger2 below.
 legacy_sha=2a840d72acfd71e55fc16aa614dcefee7afd0cf67e276b799ac9d41e773dda81
-got=$(git -C "$root" show "$rev:corpus/claim-freezes.tsv" 2>/dev/null | sha256sum | cut -d' ' -f1)
+if git -C "$root" cat-file -e "$rev:corpus/claim-freezes.tsv" 2>/dev/null; then
+    got=$(git -C "$root" show "$rev:corpus/claim-freezes.tsv" 2>/dev/null | sha256sum | cut -d' ' -f1)
+else
+    got=
+fi
 if [ "$got" = "$legacy_sha" ]; then
     echo "prefile: ledger1 retired (erratum r68-1) — legacy ledger byte-identical to its retirement pin"
 else
```

Apply with `patch -p0` against a copy, or take the ready file:

**Complete patched draft:** `.ufo/waves/round-69/w1/ExecRepairs/prefile-check.patched.sh`
(52 → 59 lines; sha256 `d19a650817102d66f877bacb9a1e7ffc6c890d093528271697a09518489fe26d`). Diffed
against the tracked file it is exactly the two hunks above; `sh -n` passes; `patch -p1` from the lane
root against HEAD's bytes reproduces it byte-for-byte (`checking file …, dryrun_rc=0`).

### 3.5 Concurrent edit observed in the working tree (adaptation, not this seat's)

At **23:38:55**, after this seat's 23:36 copy, the tracked `tools/round-29/prefile-check.sh` gained an
**uncommitted** modification (`git status --porcelain` → ` M tools/round-29/prefile-check.sh`; HEAD is
still `3f3d20fc`). It is a third-party repair of the same defect: 58 lines, 16 insertions / 10
deletions against HEAD, sha256 `9a403dc11594a78a23629034bced6b6e0b33160f08a30d00a53d4bd860c1390d`.
This seat did not make that edit and did not write to the file; it is recorded here because the L1 has
to choose between it and this draft. Bytes: `evidence/prefile-check.as-found-in-worktree.sh`; diff:
`evidence/worktree-diff-vs-head.diff`.

The L1's own round-69 carry-in entry (working-tree `LOG.md:4156`, uncommitted at the time of writing)
already names R68-V4 with this same target — "prose and branch corrected (the filed LOG line stays as
filed; the correction is appended below)" — so §5's block below is the ready wording for that appended
correction, whichever script variant is landed.

What the as-found edit does (**observation**, source read + execution):

- comment (31-37): 21 data rows, last round `round-35`, "no row for any round 36-68", the stray
  round-35 container (`claims-frozen.json`), and "the gate's disclosure receipt recorded `exact 20 of
  21` at f78fc766, not a clean ledger". Both false sentences — "stops at round-52" and "20 exact of 36
  on every round from 53 on" — are gone.
- branch (39-50): a `cat-file -e` guard wrapping a nested compare; the absent case prints
  `prefile: ledger1 legacy ledger absent at $rev`. `${got:-absent}` is removed rather than made
  reachable, and `fail=1` is set in both branches.

Verified by this seat on a scratch copy of the as-found bytes (`sh -n` OK):

```text
fixture=pinmatch  → prefile: ledger1 retired (erratum r68-1) — legacy ledger byte-identical … ; PASS ; exit 0
fixture=changed   → prefile: ledger1 legacy ledger changed (want 2a840d72…, got f062ae34…) ; FAIL ; exit 1
fixture=absent    → prefile: ledger1 legacy ledger absent at 34e73a7e7c704d856d0903c596d6839f5e1abecc ; FAIL ; exit 1
```

So the as-found edit satisfies (a) and (c) and deletes the (b) falsehood. Three things it leaves open
(**observation**, none of them status-changing):

1. Its cited command `awk -F'\t' 'NR>1{print $1}' corpus/claim-freezes.tsv | sort -u` prints the rows
   that exist; the "no row for any round 36-68" claim is read off that listing rather than printed by
   it, and round 33's absence is not mentioned. Hunk A states the same fact without a command.
2. It records only the `20 of 21` reading, so the denominator growth that actually falsifies the filed
   sentence (`of 36` at round 68, `of 37` at round 69) is not carried into the artifact. §5's LOG
   correction carries it either way.
3. `git show`'s stderr is no longer suppressed and `got` is printed unguarded; harmless after the
   presence test, and identical in the three fixtures above.

**Recommendation.** If the L1 lands the as-found edit, hunks A/B here are redundant and only §5's LOG
correction is still needed, because `LOG.md:4137` still says "stops at round-52". If the L1 wants the
measured denominator in the artifact, land hunk A over the as-found comment and keep the as-found
branch, or take the whole draft in `prefile-check.patched.sh`; the two versions were run side by side
on all three fixtures and agree on message and exit code in every cell except the absent cell's wording
(`got absent` vs `absent at <rev>`), which is cosmetic.

---

## 4. Red-before / green-after

`sh /fast/scratch/hyaku/kaidoku-r69/ExecRepairs/redgreen.sh` — three throwaway git fixtures under
scratch plus the real lane root read-only. Each fixture asserts `git rev-parse --show-toplevel` equals
its own directory before any commit. Full output: `evidence/redgreen.out` (sha256
`fb730f0754e0daf3dfc542f515692a5ae4a2925cdb69a75c76271f9e770f71d4`).

```text
=== sh -n syntax check ===
orig:    sh -n OK
patched: sh -n OK

================ fixture=pinmatch HEAD=745d5a8a0cfcbdddcc3686778d38d1819daf8cf5 ================
---- ORIG ----
prefile: tree clean
prefile: ledger1 retired (erratum r68-1) — legacy ledger byte-identical to its retirement pin
prefile: PASS
exit=0
---- PATCHED ----
prefile: tree clean
prefile: ledger1 retired (erratum r68-1) — legacy ledger byte-identical to its retirement pin
prefile: PASS
exit=0

================ fixture=changed HEAD=35332d61bcf1f33976487e699add9e9b0dd53654 ================
---- ORIG ----
prefile: tree clean
prefile: ledger1 legacy ledger changed (want 2a840d72acfd71e55fc16aa614dcefee7afd0cf67e276b799ac9d41e773dda81, got f062ae34a8466821a5baeabed5ab2f7d64c1c65abda9ff62b6721430ad6d8c10)
prefile: FAIL
exit=1
---- PATCHED ----
prefile: tree clean
prefile: ledger1 legacy ledger changed (want 2a840d72acfd71e55fc16aa614dcefee7afd0cf67e276b799ac9d41e773dda81, got f062ae34a8466821a5baeabed5ab2f7d64c1c65abda9ff62b6721430ad6d8c10)
prefile: FAIL
exit=1

================ fixture=absent HEAD=34e73a7e7c704d856d0903c596d6839f5e1abecc ================
---- ORIG ----
prefile: tree clean
prefile: ledger1 legacy ledger changed (want 2a840d72acfd71e55fc16aa614dcefee7afd0cf67e276b799ac9d41e773dda81, got e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855)
prefile: FAIL
exit=1
---- PATCHED ----
prefile: tree clean
prefile: ledger1 legacy ledger changed (want 2a840d72acfd71e55fc16aa614dcefee7afd0cf67e276b799ac9d41e773dda81, got absent)
prefile: FAIL
exit=1

================ real lane root (read-only), /home/vgpnk/Projects/shokunin/kaidoku-shokunin ================
---- ORIG ----
 M PROVINCE.md
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/knowledge/2026-11-03-r68-packed-elf-route.md
?? .ufo/waves/round-69/r69-w1.ready
?? .ufo/waves/round-69/r69-w1.ready.dispatched
?? .ufo/waves/round-69/w1/
?? corpus/knowledge/2026-11-03-r69-packed-route-contract.md
?? corpus/lessons/round-69.md
prefile: tree NOT CLEAN (9 paths)
prefile: ledger1 retired (erratum r68-1) — legacy ledger byte-identical to its retirement pin
prefile: round-29 gate --disclosures corpus/claim-freezes-v2.tsv at 3f3d20fc065b5be62f676028b9a38d316ddfe8fd exit=1
prefile: FAIL
exit=1
---- PATCHED ----
 M PROVINCE.md
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/knowledge/2026-11-03-r68-packed-elf-route.md
?? .ufo/waves/round-69/r69-w1.ready
?? .ufo/waves/round-69/r69-w1.ready.dispatched
?? .ufo/waves/round-69/w1/
?? corpus/knowledge/2026-11-03-r69-packed-route-contract.md
?? corpus/lessons/round-69.md
prefile: tree NOT CLEAN (9 paths)
prefile: ledger1 retired (erratum r68-1) — legacy ledger byte-identical to its retirement pin
prefile: round-29 gate --disclosures corpus/claim-freezes-v2.tsv at 3f3d20fc065b5be62f676028b9a38d316ddfe8fd exit=1
prefile: FAIL
exit=1
```

Reading of the cells (**observation**):

| cell | orig | patched | verdict |
|---|---|---|---|
| ledger present, byte-identical to the pin | `retired …`, exit 0 | `retired …`, exit 0 | no regression |
| ledger present, bytes changed | `got f062ae34…`, exit 1 | `got f062ae34…`, exit 1 | no regression, identical text |
| **ledger absent at `HEAD`** | `got e3b0c442…`, exit 1 | **`got absent`**, exit 1 | **red → green** |
| real lane root (read-only) | step 2 `retired`, step 3 `exit=1`, final `FAIL` | identical byte-for-byte | behaviour unchanged |

The real-tree row is mid-round on purpose: the tree is dirty with the wave's writes and the round-29
gate exits 1 because the round-69 v2 row has not landed yet. The point of that row is that orig and
patched agree exactly, so hunk B changes no verdict — only the diagnostic.

---

## 5. LOG.md append-only correction (exact text)

Never rewrite `LOG.md:4137`. Append the block below at EOF (after the round-69 landing/close entries,
in the house `## … — correction: …` shape used by rounds 65, 66 and 67):

```markdown
## 2026-11-03 — round 69, KaidokuR69 — correction: the r68 retirement erratum misstates the legacy ledger's last round and the round-24 gate's readings (the r68 closure's routed defect R68-V4)

- **Measured correction (QUALITY #65).** The round-68 landing entry (line 4137) says the retired `corpus/claim-freezes.tsv` "stops at round-52" and that "the gate reported 20 exact of 36 on every round from 53 on". Measured: the file carries 21 rows — rounds 14-32, 34, 35 — and nothing after `round-35` (`tail -n +2 corpus/claim-freezes.tsv | grep -c .` = 21, no `round-52` row), and rounds 36-52 never carried a `claims.json` at all (`git log --all --diff-filter=A -- '.ufo/waves/round-3[6-9]/claims.json' '.ufo/waves/round-4[0-9]/claims.json' '.ufo/waves/round-5[0-2]/claims.json'` empty), so the ledger dropped nothing there. The round-24 gate (`.ufo/waves/round-24/tools/freeze-gate.py`, sha256 `8a71fe84…`, unchanged since `9fb4eacd`) reads `exact 20 of 21` at `f78fc766`, `20 of 36` at `6ffa9ce1` and `20 of 37` at `3f3d20fc`, with `stray ["round-35"]` and exit 1 at each: the `exact` count is stable, the `of` is the lane's `claims.json` population and grows. `tools/round-29/prefile-check.sh` is corrected in the same round — its step-2 comment now carries these measurements, and its failure branch prints `absent` for a ledger missing at the revision instead of the empty-input digest `e3b0c442…`.
- Filed LOG and report bytes are not rewritten; the script's step-2 comment and its failure-branch diagnostic change, while its mechanics (`legacy_sha`, the compare, the exit codes) do not. Red/green: `.ufo/waves/round-69/w1/ExecRepairs/evidence/redgreen.out`.
- Files touched by this entry: `tools/round-29/prefile-check.sh`, this LOG — append-only.
```

If the L1 prefers to fold the correction into an existing round-69 bullet instead of opening a heading
(the precedent is a heading), the one-line form is:

```markdown
- **Correction (QUALITY #65, the r68 closure's R68-V4).** `tools/round-29/prefile-check.sh`'s erratum comment is corrected against measurement — the retired `corpus/claim-freezes.tsv` carries 21 rows (rounds 14-32, 34, 35) and stops at `round-35`, not round-52, and the round-24 gate read `exact 20 of 21` / `20 of 36` / `20 of 37` at `f78fc766` / `6ffa9ce1` / `3f3d20fc` (not "20 of 36 throughout") with `stray ["round-35"]` and exit 1 each time; its failure branch now prints `absent` for a ledger missing at the revision instead of the empty-input digest `e3b0c442…`. Filed bytes are not rewritten; `LOG.md:4137` stands as filed.
```

Both variants are additions; neither edits line 4137 or any other filed byte.

---

## 6. Observed but not part of R68-V4 (L1's call, no action taken)

`tools/round-29/prefile-check.sh` lines **11-12** still carry the wrap introduced by the round-68
edit — the ExecLedger's parenthetical in `report.md` §2.5:

```text
#               gate (the
#               freeze-gate.py next to this script) with --disclosures on it exits 0 at HEAD.
```

Optional hunk C (replaces those two lines with one, width 98; independent of hunks A/B, which are below
it, so it does not shift the line numbers used above if applied in the same edit):

```text
#               gate (freeze-gate.py next to this script) with --disclosures on it exits 0 at HEAD.
```

It is cosmetic and is **not** one of the three defects the assignment names; it is recorded so the L1
can decide rather than rediscover.

---

## 7. Evidence inventory (in this wave dir)

| file | content |
|---|---|
| `prefile-check.patched.sh` | complete draft of the repaired script (59 lines, `d19a6508…`), the file to land if this draft wins |
| `evidence/patch.diff` | unified diff with repo-relative labels (`08e1c43f…`), applies with `patch -p1` from the lane root against HEAD's bytes |
| `evidence/prefile-check.as-found-in-worktree.sh` | scratch copy of the **third-party uncommitted** repair found in the working tree at 23:38:55 (`9a403dc1…`), for comparison only |
| `evidence/worktree-diff-vs-head.diff` | `git diff` of that uncommitted edit against HEAD (`a09309f2…`), 16 insertions / 10 deletions |
| `evidence/redgreen.out` | full red-before/green-after run (`fb730f07…`), three fixtures + real tree |
| `evidence/r24-gate-at-f78fc766.json` | round-24 gate at round-53's commit: `exact 20 of 21`, exit 1 |
| `evidence/r24-gate-at-6ffa9ce1.json` | round-24 gate at round-68's landing: `exact 20 of 36`, exit 1 |
| `evidence/r24-gate-at-d7d9a62cc70935304e600ed0dee864fc4f1751f7.json` | round-24 gate at this round's base: `exact 20 of 36`, exit 1 |
| `evidence/r24-gate-at-head.json` | round-24 gate at `3f3d20fc`: `exact 20 of 37`, exit 1 |

Scratch (`/fast/scratch/hyaku/kaidoku-r69/ExecRepairs/`: `patched/`, `fixtures/`, `apply/`,
`redgreen.sh`, `redgreen.out`, `patch.diff`, `worktree-diff-vs-head.diff`, `r24-gate-at-*.json`) is
deleted before this seat yields; the copies above are the retained receipts.

## 8. Risks, limits, unknowns

- **Observation:** the patched script's step 2 is still a byte-identity pin, so it cannot pass on a tree
  where the retired ledger is absent. That is intended (the pin is the point) and hunk B only fixes the
  message; the exit code is 1 in the absent case before and after.
- **Observation:** hunk B costs one extra `git cat-file -e` per prefile run. No measurable cost at this
  scale.
- **Inference (disclosed):** a ledger whose *blob* exists but is unreadable by `git show` (corrupt
  object) would still surface as `got e3b0c442…`; `git show`'s stderr is suppressed by the existing
  `2>/dev/null`, which this repair deliberately leaves untouched (minimal diff). If the L1 wants that
  class named too, the guard would need `if ! got=$(…); then got=unreadable; fi` — not proposed here,
  as it is outside the three named defects.
- **Observation (interface changed mid-seat):** `tools/round-29/prefile-check.sh` was byte-stable at
  `56957693…` when copied (23:36) and was modified in the worktree by a third party at 23:38:55
  (`9a403dc1…`, uncommitted). Every number in §2 is unaffected (it measures the ledger, the gate and
  `git`, none of which changed); §3.4/§3.5 say which base each patch assumes. Re-check
  `sha256sum tools/round-29/prefile-check.sh` before landing, and land exactly one of the two drafts.
- **Unknown:** none of the three defects is falsified by this measurement; no additional claim depends
  on these numbers, and no claim predicate was re-read or re-frozen by this seat.
- No tool was installed or upgraded; no pacman transaction ran; no git/jj mutation was issued against
  the lane or any fixture outside `/fast/scratch/hyaku/kaidoku-r69/ExecRepairs/`.
