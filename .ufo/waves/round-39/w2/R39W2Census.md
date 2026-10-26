DEFECTS FOUND — the round-39 registry landing is append-only and count-correct, but three landed facts are wrong or hazardous: the new triage entry cites S112 while S112's `used-by` was never updated; the re-used id S122 turns a harmless round-38 staging label in `2026-10-26-unblob-format-matrix.md` into a citation of an unrelated row; and the round-39 SKILL instrument row documents a could-not-evaluate contract the landed `registry-immutable.sh` does not have (measured: unknown revision → exit 1 with 117 fabricated `row deleted` lines, not git's 128).

Seat: `R39W2Census` (round 39, wave 2, falsify the landing). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Registry revision under test `52b0eb2907c704ed5f184c47b14c723208e5cbbc`; base `a2f64e1da78afcf8cc39287106604dbcc270844c`; freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`. Read-only git only; no lane file written outside this report and `.ufo/waves/round-39/w2/artifacts/R39W2Census/`. Nothing installed or upgraded (no package manager invoked). Scratch `/fast/scratch/hyaku/kaidoku-r39/R39W2Census`, removed at exit.

## 1. Required checks — all four ran

### 1.1 `sources-census.sh validate` — exit 0

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
kaidoku	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
kaidoku	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
kaidoku	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
kaidoku	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
kaidoku	W04	S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
kaidoku	W04	S117 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md across scopes
kaidoku	W04	S119 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
EXIT=0
```

No `E`-code fired, so: 11 columns/`NF=13`, ids `S[0-9]{3,}`, no duplicate id, kind/tier/status enums valid, `opened` a valid date, `recheck` valid, community never tier A, every `used-by` path exists on disk (E11). The twelve `W04` rows are warnings and do not affect the clean verdict; `S119` (new) joins the already-warned 6.5.0-tarball URL group `S083/S090/S092` with a distinct scope, the same shape the lane already carries for `S108/S112`. Artifact `census.txt`.

Note for the L1: `E11` only checks that each path in `used-by` **exists**. It does not check the reverse direction (that every entry citing a row is named in it), which is exactly where §3.1 bites — the fleet validator cannot see that defect.

### 1.2 `registry-immutable.sh BASE REV` — exit 0 (appends only)

```
$ bash tools/round-38/registry-immutable.sh /home/vgpnk/Projects/shokunin/kaidoku-shokunin a2f64e1d… 52b0eb29…
EXIT=0
```

Silent, i.e. no base row changed outside `status`/`recheck`/`used-by`, no row deleted, no relative reorder. Artifact `registry-immutable-base-vs-rev.txt`.

### 1.3 Row counts and id set

| revision | rows |
|---|---|
| base `a2f64e1d` | 117 |
| freeze `8fcda41c` | 121 |
| landed `52b0eb29` | 122 |

`comm` on the id sets: **added S118 S119 S120 S121 S122; removed none; no duplicate id.** Ids are contiguous `S001..S122`, sorted, no gaps. Every new row has `NF=13`. `S118–S121` land at the freeze commit, `S122` at `6fdaf4f1` (the C1 receipts commit). Artifact `row-counts.txt`.

### 1.4 Per-tier / status tally of the added rows

All five added rows are identical in class:

| id | kind | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|
| S118 | code | A | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md |
| S119 | code | A | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md |
| S120 | code | A | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md |
| S121 | code | A | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md |
| S122 | code | A | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md |

Added tally: tier A ×5, status mined ×5, kind code ×5. Landed totals from `sources-census.sh census`: rows 122, tier.A 114, tier.B 7, tier.C 1, status.mined 117, status.rejected 5, invalid 0 — exactly base (A 109 / B 7 / C 1, mined 112 / rejected 5) plus the five A/mined rows. `CENSUS_EXIT=0`. Artifact `census.txt`.

### 1.5 Used-by equals the citing entries — true for every new row

Textual check over every `source:` line of every `corpus/knowledge/*.md` at the landed revision:

- `2026-10-26-r39-sqfs-outcome-triage.md` cites `S112 S118 S119 S120 S121`.
- `2026-10-26-r39-be-squashfs-v4-core.md` cites `S122` only.
- `S118`–`S121` each name exactly the triage entry; `S122` names exactly the C1 entry. **No new row lists an entry that does not cite it, and no entry citing a new row is missing from it.**

So the seat's stated criterion ("each new row's used-by equals exactly the knowledge entries whose `source:` lines cite it") **holds for all five rows**. The defect is on the other side of the citation, §3.1. Artifact `usedby-crosscheck.txt`.

## 2. Cross-checks that held (no finding)

- Three committed round-38 receipts replay byte-exactly under the landed, stricter bytes: `77091b49..7a1ac7fe` → rc 0, empty; `77091b49..0fc61133` → rc 1, `S110 changed columns: 6`; `77091b49..77091b49` → rc 0, empty. Matches `.ufo/waves/round-38/l1/registry-immutable/{at-final,at-0fc61133,base-vs-base}.txt`.
- `--selftest`: `registry-immutable.sh` `cases=5 pass=5 fail=0` rc 0; `freeze-drift.py` `cases=8 pass=8 fail=0` rc 0; `intended-doc.py` `cases=9 pass=9 fail=0` rc 0 — the counts SKILL rows 1341–1343 claim. Artifact `selftests.txt`.
- The two Python tools are additively patched: the only removed lines in each diff are the single `import …` line (module list extended). No run-mode logic line changed.
- The landed `registry-immutable.sh` header's own claim about the round-38 behaviour is correct: on a fixture with one deleted row and one reordered pair, the round-38 bytes (sha256 `2595a3970f5ccade5a7d73a378214f1213b16c21b66686d7b345b1e50314d47c`) return **rc 0** for both, the landed bytes **rc 1** with `S003 row deleted (append-only)` and `S001 / S002 row reordered (append-only)`.
- SKILL's instrument example `S100 changed columns: 6` is **not** a typo for the lane's `S110`: the w1 seat exercised its own fixture row `S100` (`.ufo/waves/round-39/w1/artifacts/R39CL2Registry/evidence/registry-immutable-scope.jsonl`), while the lane receipt is `S110`. Both are true statements about different fixtures; reconciled, no defect.

## 3. Findings

### 3.1 S112's `used-by` was not updated for the new triage entry (registry reverse index stale)

`corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md:3` is a `source:` line citing **S112**. `S112`'s `used-by` at base and at landed is byte-identical and names only the round-38 entry:

```
S112 status=mined used-by=corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md
```

Reproduced as a base→landed delta: 25 violations of "cited entry absent from the row's `used-by`" exist at base, **26 at landed**; the only new one is `(triage, S112)`. Introduced at the freeze commit (`8fcda41c` adds the entry) and carried through `52b0eb29`.

Severity and binding: `used-by` is the registry's only reverse index, and SKILL.md:718 / QUALITY rule 29 bind a *counted* entry's `source:` to a row that names it. The triage entry is not the C1 counted entry, so whether the rule binds it literally is [INFERENCE]; the observable fact is that a `source:` citation exists with no reverse pointer, and 25 pre-existing instances show the lane tolerates this class generally. It is a stale index entry, not a fabricated source. `sources-census.sh` cannot detect it (E11 is forward-only, §1.1).

### 3.2 Re-used id S122 converts a round-38 staging label into a citation of an unrelated row

`corpus/knowledge/2026-10-26-unblob-format-matrix.md:1` reads (round-38 bytes, unchanged at landed):

> `source: S116 — … (staged as package S122, renumbered by document)`

At base, `S122` was **not** a registry row: the token was a staging-ledger label and dangled harmlessly (`row absent at this rev` in the cross-check). The round-39 landing allocates `S122` to a different source (`unblob/python/unblob/file_utils.py`, `is_safe_path`). The same string now reads as a citation of a row the entry does not use — the cross-check reports it as `(matrix, S122, cited but absent from row used-by)`, and any human or tool resolving `S122` from that line lands on `file_utils.py`.

This is not a `used-by` omission by the C1 entry (its cell is correct, §1.5); it is an id-collision hazard created by reusing an id that a retained entry still mentions. A qualifier ("staged as package S122 in the round-38 staging ledger, **not registry row S122**") or a different id would remove it.

### 3.3 The round-39 SKILL instrument row documents a could-not-evaluate path the landed gate does not have

SKILL.md:1343 (added by `52b0eb29`) states:

> `No 2`: a bad revision makes the `git show` row set fail under `set -e`, so bash exits with git's own code (128 expected, not exercised) and that code is undeclared → reads could-not-evaluate.

Measured on the landed bytes:

```
$ bash tools/round-38/registry-immutable.sh <LANE> a2f64e1d… deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
fatal: path 'corpus/SOURCES.md' exists on disk, but not in 'deadbeef…'
S001 row deleted (append-only)
… (117 lines)
rc=1   deleted-lines=117
```

and on a **valid** revision whose tree predates `corpus/SOURCES.md` (root commit `b3669e60`): landed `rc=1`, 117 `row deleted` lines; round-38 bytes `rc=0`, no such lines.

Mechanism: `rows()` is invoked through process substitution, so the failing `git show` never reaches `set -e`; `grep` yields an empty rev set and the round-39 deletion branch accuses all 117 base rows. Consequences: (a) the documented `128` is wrong for both byte versions; (b) "reads could-not-evaluate" is wrong — an unevaluable revision is reported with the **same exit code and the same wording** as a genuine append-only violation, so a caller cannot distinguish them; (c) round 39 changed a false-clean (`rc 0`) into a false-violation (`rc 1`, 117 lines). The 5-case `--selftest` does not cover an unknown or registry-less revision.

This is a documentation-and-semantics defect in the landed instrument registry, and it is the one place in this seat's scope where the landed bytes assert something measurable that is false. Side effect for future rounds: an old base revision without `corpus/SOURCES.md` can no longer be used as the `BASE` arm without a 117-line false report.

### 3.4 Delivered `registry-immutable.sh` still carries its candidate self-disclaimer

`tools/round-38/registry-immutable.sh:8-14` at `52b0eb29` says:

> VARIANT NOTE (R39CL2Selftests, advisory): this copy … **is NOT the assigned deliverable; tools/round-38/registry-immutable.sh is unchanged by this seat.** Take this file only if the L1 authorises the behaviour change …

The file **is** `tools/round-38/registry-immutable.sh` and it **was** changed by that commit (the w1 seat's `registry-immutable.fixed.sh` was adopted: +100/−2, run-mode deletion/reorder checks). So the note is now false about itself. The behaviour change is real, intentional, documented at SKILL:1343, and reproduces the three round-38 receipts (§2), so this is a stale-comment defect, not a hidden change — but the target's own summary ("`--selftest` added to tools/round-38/{…,registry-immutable.sh}") also understates it: run-mode exit codes changed, which is more than a selftest addition.

## 4. Limits

- I did not re-run `tools/round-39/c1-counter.py` or `c2-counter.py`; the author's 6/6 and 20/20 at `6fdaf4f1` are other seats' targets (`R39W2C1EntryReview`, `F40TipReceipts`). Nothing in §1 depends on them.
- No REA, unblob or sasquatch run; no carrier inspected. All claims here are over git objects and files.
- The used-by cross-check is textual over lines beginning `source:`; it does not judge whether a citation is *apt*, only whether it is present in both directions.
- The `S100`/`S110` question was settled by reading the w1 evidence file, not by re-running that seat's fixture.

## 5. Artifacts

`.ufo/waves/round-39/w2/artifacts/R39W2Census/`: `census.txt` (validate + census, both exits), `row-counts.txt` (117/121/122, added/removed ids, new-row cells, contiguity, `NF`), `registry-immutable-base-vs-rev.txt` (exit 0), `registry-immutable-behaviour.txt` (three receipts, unknown-rev and root-commit arms for both byte versions), `usedby-crosscheck.txt` (citations, reverse index, 25→26 delta, full violation list), `selftests.txt` (5/5, 8/8, 9/9).

Report: .ufo/waves/round-39/w2/R39W2Census.md
