# R41MistakeHunt — one new mistake for the round-41 `## Mistakes` table

**Verdict: DONE** — one mistake class mined that is absent from the round-38/39/40 `## Mistakes`
tables, with a check script RED at the lane base and GREEN on a repaired scratch fixture, two
controls that show the check able to fail on the repaired state, and the sweep that establishes
the class is a singleton on the registry surface.

Measured at base `49096c7e6f226af0c750c4b003be58883cb6049f` (lane main at dispatch). Nothing
committed; lane corpus/tools/plans untouched; report and artifacts are my only writes.

---

## 1. The proposed lesson row

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| MH-1 | **provenance written against the authoring host while the artifact already holds the bytes**: a registry row pins three bodies by absolute path into a *read-only sibling project repo at an unpinned revision*, though two of the three are already committed in the lane (four paths) and the third exists in-lane only as a **different file with the same basename**. The row's own pointer therefore cannot be followed or checked from a lane checkout, and the cheapest repair substitutes the wrong body. | `corpus/SOURCES.md:132` (S126, status `mined`, tier A, kind `own-work`, `used-by` the AVM entry) citing `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/{lead1-avm-image.tsv,avm-be.squashfs,unblob.log}`; the same pointer repeated as lineage at `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md:5`; in-lane copies nobody cites: `.ufo/waves/round-40/w1/artifacts/R40C1Revenger/round11-avm-be.squashfs`, `…/R40Quarantine/avm-be-r11.squashfs`, `…/R40C1Counter/dev-avm-be-4096.squashfs`, `…/R40C1MarkerBoundary/fixtures/avm-be.squashfs`, `…/R40Quarantine/lead1-avm-image.tsv`; the decoy: lane-root `unblob.log` = `2d651a4aa6ea…f16299` — same basename, different body, *not* the pinned round-11 log `352e0d79…d5d7` (its prefix matches M38-7's recorded lane-root log but its tail does not, so I withhold that attribution; the isolation stands on digests); closure already filed it status-neutral at `corpus/lessons/round-40-verifier-spotcheck.md:87` (D1) | **none** — QUALITY 4 ("absolute path plus a stable identity") is *satisfied* by a sibling-repo path, so the row passed admission on its letter; 12 ("synthesized carriers retain their exact bytes inline or the full regenerating recipe") is satisfied only outside the lane and has no gate; 81 binds a *repaired* pointer to a git blob, and no repair was ever triggered because the pointers do resolve on this host | `.ufo/waves/round-41/w1/artifacts/R41MistakeHunt/registry-body-reach.py` — base lane: **exit 1, 3 `external-body`** (2 in the S126 row, 1 in the entry's lineage); repaired fixture (bodies committed under `corpus/evidence/round-11/avm-be/`, row and lineage repointed): **exit 0**; same-name wrong bytes **exit 1 `pin-mismatch`**; lane-root `unblob.log` substituted for the round-11 log **exit 1 `pin-mismatch`**; `--selftest` 10/10 |

One-sentence form for the lesson: *a body the lane already holds is not evidence until a citation
names it — a row that points at the host passes every absolute-path and byte-scan check and still
leaves the observation unverifiable, and the only in-lane file with the right basename may be a
different observation.*

## 2. Why this is not a re-mine

Read at base: `corpus/lessons/round-38.md`, `round-39.md`, `round-40.md`, `## Mistakes` (I read all
three tables in full; the round-40 table is five rows, round-39 ten, round-38 nine).

Mined classes there: freeze amendment after scoring; degenerate/inverted control generator;
control receipts re-scored in place; stale PATH premise; harness pre-create vs a refusing tool;
false correction of a count; existence-only calibration counter; misroot `unblob.log`; registry
append-only violation; measured revision not shipping the rule; false absence sweep (wrong root,
twice); routed defects dropped between rounds; uncommitted wave reports; a fix typed into one wave
context lapsing; POSIX `..` clamping; lane carrier writer mis-encoding; shell fallback writing into
the fleet root; report in the fleet repo; post-freeze edits; **suffix-vs-exact path matching**
(M40-1); carrier pick is not a reservation (M40-2); duplicate reports under `artifacts/` (M40-3);
**vendor bytes in the lane tree** (M40-4); a recon recipe failing on a fresh seed (M40-5).

Three nearest relatives and the distinction I had to pass:

- **M40-1 / M40-5 (path domain, `same_rel`)** — about what a matcher *computes* over paths inside
  one extract root. MH-1 is about whether a *citation* names a body the artifact holds at all; no
  matcher is wrong here, the pointer is.
- **M40-4 (vendor bytes in the lane tree)** — about bytes that must *not* be in the lane. MH-1 is
  the mirror image: lane-held, licence-clean, own-work bytes that *should* be cited and are not.
  A byte-scan in the M40-4 style passes on the base tree, which is exactly how this hole survived.
- **M38-6 / QUALITY 81 (pointer repair)** — Q81 requires a *repair* claim to bind the repaired
  pointer to the document's git blob. MH-1 never reaches a repair: the host path resolves, so no
  claim is filed, and the closure recorded D1 as status-neutral.

## 3. What was measured

All commands run from `/fast/scratch/hyaku/kaidoku-r41/R41MistakeHunt`; receipts in
`artifacts/R41MistakeHunt/receipts/`.

**a. The check on the untouched lane (`receipts/fixture-run.txt` §1, §7; `--rev` = base):**

```
rows=126 pointers=66 lane=39 tool=24 scratch=0 external=3 rev=49096c7e6f22
FATAL external-body  corpus/SOURCES.md:132 S126   sha=f205807de801 /home/…/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv
FATAL external-body  corpus/SOURCES.md:132 S126   sha=c7f74691b3e8 /home/…/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs
FATAL external-body  corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md:5 S126 sha=- /home/…/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv
findings=3
exit=1
```

126 rows scanned; 66 absolute/relative pointers extracted from the `source` and `anchor` columns
plus numbered `source: SNNN` lineage lines: 39 lane, 24 tool/OS-package, 0 scratch, **3 external —
all S126**. So the class is a singleton on the registry surface, not a corpus-wide pattern.

**b. Integrity holds; reach does not** (`receipts/sweeps.txt` §D): all three sibling bodies still
hash to the row's pins (`f205807d…9eb0`, `c7f74691…d32d32`, `352e0d79…d5d7`). This is a durability
defect, not a wrong pin — the fix must never re-pin.

**c. The bodies are (mostly) already in the lane** (`§I`): the image is committed at four paths,
all `c7f74691…d32d32` (`.ufo/waves/round-40/w1/artifacts/{R40C1Revenger/round11-avm-be.squashfs,
R40Quarantine/avm-be-r11.squashfs, R40C1Counter/dev-avm-be-4096.squashfs,
R40C1MarkerBoundary/fixtures/avm-be.squashfs}`), and the tsv at
`…/R40Quarantine/lead1-avm-image.tsv` = `f205807d…9eb0`. **No registry row or knowledge entry
names any of those five paths** (`grep` exit 1).

**d. The decoy** (`§J`): two lane files are called `unblob.log` at the base — the lane-root copy
(`2d651a4aa6ea…f16299`) and a round-39 artifact
(`.ufo/waves/round-39/w2/artifacts/R39W2C1Fabricate/unblob-K1/unblob.log`, `826e278a…4e28`) — and
neither is the pinned round-11 log `352e0d79…d5d7`, which exists **nowhere** in the lane. A repair
that points S126 at `unblob.log` would silently swap bodies; the pin is the only thing that catches
it, which the control in §4 proves. (Observation, [INFERENCE], not scored: M38-7 renders the
lane-root log as `2d651a4a…9299`; the base file is `2d651a4a…f16299` — the prefixes agree, the
tails do not. Either the path was re-used by a later write or that rendering is off; the isolation
above does not depend on which.)

**e. The sibling tree is not the lane's** (`§E`): the bodies are committed in
`/home/vgpnk/Projects/shokuknow` at `8b94c5c1…` (2026-10-24) — a tree the seat spec marks
read-only and forbids running campaign tools in — and the row pins file digests, not that commit.
A fresh lane checkout has `corpus/evidence/round-11` absent (`§F`), while the same lane commits a
lane-built carrier at `corpus/evidence/round-40/c1/L1/carrier.sqsh` (230 884 B) — the in-lane
convention already exists for the carrier shape.

## 4. The check, and proof it can fail

`registry-body-reach.py` (stdlib, no scratch in production, reads git objects at `--rev`):
findings `external-body`, `scratch-body`, `lane-untracked`, `pin-mismatch`; exit 0 clean / 1 finding
/ 2 could-not-evaluate. Tool roots (`/usr`, `/opt`, `/srv`, `<home>/.local|.agents|.npm|.cache|
.config`, `/var/lib|/var/cache`) are *not* findings, so the 24 re-obtainable tool citations do not
drown the signal.

Fixture (`receipts/fixture-run.txt`, driver `run-fixture-receipt.sh`, repair recipe
`fixture-repair.py`; `--shared` clone of the lane at the base, `rev-parse --show-toplevel` asserted
equal to the clone, fixture identity `-c user.name=fx -c user.email=fx@fx`):

| step | state | exit | findings |
|---|---|---|---|
| 1 | clone at base, unmodified | 1 | 3 `external-body` |
| 2 | three own-work bodies committed under `corpus/evidence/round-11/avm-be/`, row + lineage repointed | 0 | 0 |
| 3 | repaired path holds 4096 zero bytes (right name, wrong body) | 1 | 1 `pin-mismatch` (image) |
| 3b | lane-root `unblob.log` (`2d651a4a…`) substituted for the round-11 log | 1 | 1 `pin-mismatch` (log) |
| 4 | both bodies byte-exact again | 0 | 0 |
| 5 | `--selftest` (9 fixture repos + before/after) | 0 | 10/10 cases |

Selftest cases, all passing: external sibling body fatal; tracked lane copy with matching pin
clean; same-name stub red; lane path absent from the revision fatal; scratch body fatal; installed
tool path not a finding; URL-only row clean; knowledge-lineage pointer scored; rowless surface
could-not-evaluate; tracked lane *directory* citation clean.

## 5. Smallest safe correction (for the L1; I did not apply it)

1. Commit the three bodies under `corpus/evidence/` at their existing pins — reuse the two
   already-in-lane copies (`cp` from `.ufo/waves/round-40/w1/artifacts/R40Quarantine/
   lead1-avm-image.tsv` and `R40C1Revenger/round11-avm-be.squashfs`) and take only the round-11
   `unblob.log` from the sibling tree (2 153 B; the one body with no in-lane copy). Do **not** re-pin.
2. Repoint `corpus/SOURCES.md:132` and
   `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md:5` at those lane paths, keeping the
   three digests verbatim. (My fixture used `corpus/evidence/round-11/avm-be/`; landing them under
   `corpus/evidence/round-40/c1/` beside the carrier is equally fine — the check does not care which
   lane path, only that it is tracked and digest-equal.)
3. If the row must keep a host path as a courtesy, it also carries the lane copy; citation of the
   host alone is the defect.
4. Gate for the freeze: `python3 -I -B <artifacts>/registry-body-reach.py --root <LANE> --rev
   <FREEZE>` must exit 0. On the base it exits 1; on the repaired fixture it exits 0 (§4).

**Do not** "fix" it by pointing the log at the lane-root `unblob.log`: that file is a *different*
body (`2d651a4aa6ea…f16299`), and step 3b is the receipt that the check refuses it. Take the
round-11 log from the sibling tree, or mark the row host-local for that one body and say so.

## 6. Calibration — what this is not

- **Not "the bytes are missing".** Four image copies and the tsv are in-lane (§3c). The defect is
  the citation, and the missing body is one 2 153-byte log. Anyone may say "the lane already keeps
  the evidence"; the row simply is not the thing that keeps it.
- **Not a wrong pin and not evidence tampering.** All three digests verify on the host (§3b); the
  finding is unfollowability, not falsity. Marked accordingly: `external-body`, never
  `pin-mismatch`, on the base.
- **Not M40-4 recurrence.** No vendor bytes are involved; the bodies are lane-built own work, so the
  repair is licence-clean and 4 KB+2 KB in size.
- **Boundary case, reported not claimed:** `corpus/QUALITY.md:11-13` grounds its admission standard
  on `CORPUS.md` / `PROTOCOL.md`, which exist only at the fleet root
  (`/home/vgpnk/Projects/shokunin/{CORPUS.md,PROTOCOL.md,LEARNING.md}`, tracked in the *fleet* repo,
  `CORPUS.md` last changed `f47ad6ba`, 2026-10-25) and are **absent from the lane tree at base**
  (`git ls-tree … | grep -i 'corpus.md|learning.md'` → nothing). Same family, milder: a parent repo
  rather than a foreign project, and a policy question (copy the standard into `corpus/`, or cite a
  fleet commit) that belongs to the L1/operator, not to a wave-1 seat.
- **Scope of the check, stated so nobody over-reads the 66:** it scores the SOURCES registry table
  and numbered `source: SNNN` lineage lines. Free-form `- source:` bullets in older knowledge
  entries are out of scope — many cite deleted `/tmp` scratch by design and declare it in their own
  `## Scratch` section.
- **Two sweep hits I refused to score** (`§C`): the only `/tmp` strings in `corpus/SOURCES.md` are
  `var/tmp/filesystem.image` and `var/tmp/x86/filesystem.image` *inside the vendor image* (S125
  row). The classifier anchors at `^/tmp`, so they are not scratch citations; reporting them would
  have been a false positive.

## 7. Why it matters to the round-41 freeze

P41-C1 requires the round's knowledge entry to cite a SOURCES row *absent at the base* whose
`used-by` lists it (`plans/round-41-claims.md:42-43`), and scores four carriers, two of them
lane-built (L3/L4). The same failure mode is one copy-paste away: a row that cites a carrier,
receipt or oracle by wherever the seat happened to write it. The gate in §5.4 runs in milliseconds
against git objects and would hold the new row to "the artifact holds the body it cites" — the
property the base row, filed last round and marked `mined`, does not have.

## 8. Bounds and hygiene

- Wrote only `.ufo/waves/round-41/w1/R41MistakeHunt.md` and
  `.ufo/waves/round-41/w1/artifacts/R41MistakeHunt/` (scripts + two receipts). `git status
  --porcelain` on the lane shows nothing from me outside that path (the other entries are the L1's
  and siblings' `round-41/`, `plans/round-41-claims.md`, `tools/round-41/`).
- Fleet repo: `git status --porcelain | grep -i round-41` → 0 hits. No file in `~/.local/bin`, no
  `corpus/`, `tools/`, `plans/`, `SKILL.md`, `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, `LOG.md`
  touched.
- No git/jj mutation outside the throwaway clone; every call there named `-C` and asserted its
  toplevel; fixture identity only `-c user.name=fx -c user.email=fx@fx`.
- No tool installed, upgraded or removed. No REA, unblob, sasquatch or `sasquatch-v4be` run; no
  reserved carrier touched; no vendor firmware bytes copied into the lane (the only bodies copied
  anywhere are the lane's own 4 096-byte AVM-BE image, its 21-line tsv and the 17-line log, into
  scratch and a scratch clone).
- Scratch `/fast/scratch/hyaku/kaidoku-r41/R41MistakeHunt/` removed before yield.

## 9. Artifacts

| path (under `artifacts/R41MistakeHunt/`) | sha256 | what |
|---|---|---|
| `registry-body-reach.py` | `a5b33ab48313b731647f1ccb1fa95cf606848641e24a6a2c6a3567e7c3c534df` | the check (4 finding classes, `--selftest` 10 cases) |
| `fixture-repair.py` | `97be6c4a85527c4541115ce2097bf1e563492e9fbcad9a910dc580553304fc76` | repair recipe; refuses to proceed if a copied body disagrees with the row pin |
| `run-fixture-receipt.sh` | `123ad60da93e95acfd86f87811b33269a367bc5100d2ea51a274ae574ac2e230` | clone → repair → 3 controls → selftest → diff → production run |
| `run-sweeps.sh` | `d7b2cfd88f1165303a539860479cc03221e68a4e416235450921bbb5eaaa78f4` | sweeps A–J behind every number above |
| `receipts/fixture-run.txt` | `021b6cb7077ce60e4ae112f45e890052aa5a68b14f945b91b820f48b12abf651` | the run in §4 |
| `receipts/sweeps.txt` | `8ab0d01d37be4201546189bd91b6f1c0d6a35065b31eb05137236462211459cd` | the sweeps in §3 and §6 |

Reproduce: `bash run-sweeps.sh <WORKDIR>` and `bash run-fixture-receipt.sh <WORKDIR>` (both honour
`TMPDIR`, write only beneath `<WORKDIR>`, and leave the lane untouched).
