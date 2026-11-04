# overlap — sibling-overlap scan, kaidoku-shokunin round 69 wave 1 (seat ConnectorCross)

Deliverable for the seat prompt's step 4. Read-only on the lane and the fleet: no tracked file was
written, no `git`/`jj` mutating verb run, no sibling tool executed, no sibling file imported. Writes:
this directory only. Scratch `/fast/scratch/hyaku/kaidoku-r69/ConnectorCross` was created for the
binding probe and is removed after its receipts are copied here (see `bindprobe.out`).

Observed ground (observation; the lane moved under this scan). Start of scan: `HEAD` =
`3f3d20fc065b5be62f676028b9a38d316ddfe8fd`, worktree dirty with 14 entries. At 23:44:58 the L1 landed
`5ee94c56ce7490938ee38c2e5c10930a1fd1330a` ("round-69 landing: the packed route's gate, contract and
shared-object carrier; the six r68 repairs; S270; QUALITY 112-114; the provenance gate"); after it the
worktree is clean except the untracked wave/report dirs. The four frozen instruments were re-hashed at
start, at 23:43, and after the landing — all match `claims.json` on every read: `packed-elf.py`
`4ac0d83b…`, `mutation-check.py` `51b64c56…`, `contract-probe.py` `e609d85d…`, `controls.py`
`1f8f78c1…`; `tools/round-68/packed-elf.py` `48ef4c68…`; `claims.json` itself `ebc68ac5…` unchanged.
The landing added a fifth **tracked** instrument, `tools/round-69/provenance-check.py` (sha
`dff47b92…`, 200 lines, registered at `SKILL.md:1866`) — see D2/D4; it is not in the frozen container
and is not a claim counter. Host pins observed: `/usr/bin/upx` = `upx 5.2.0`, sha256 `cf2f6e7c…`;
`/usr/lib/libz.so.1.3.2` sha256 `6c78c5e5…`. `/usr/bin/jq` and `/usr/bin/xxd` were **not** re-hashed
by this seat (their pins are the container's A-atoms, unverified here). Sibling province/SKILL files
were read at their on-disk state, unpinned by commit — this is a *declaration* sweep, not a
cross-revision audit.

Axes this seat's output serves: **adjacency** (`AXES.md:16` — "cross-domain awareness — evidence
belonging to another domain reported, not absorbed"; "Lane reports name contested scope") and, through
D1–D4 below, **calibration** (`AXES.md:15` — "gaps named honestly, confidence graded, overreach
caught").

---

## 1. Sweeps (verbatim; outputs kept in `sweep/`)

Run from `/home/vgpnk/Projects/shokunin` (fleet root), 2026-11-03.

| id | command | observed |
|---|---|---|
| S1 | `grep -rn -iE 'mutation' --include='PROVINCE.md' . \| grep -v '^./kaidoku-shokunin/' \| grep -v '/.ufo/'` | 34 matched lines (captured file 35 incl. its header); ownership-bearing hits in §2 |
| S2 | `grep -rn -iE '\bupx\b\|packed[- ]elf\|packer route' --include='SKILL.md' --include='PROVINCE.md' --include='QUALITY.md' . \| grep -v '^./kaidoku-shokunin/'` | **0 sibling declarations**; 2 hits are archived copies of *kaidoku's own* PROVINCE under `tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/kaidoku/*/PROVINCE.md:62` |
| S2b | `grep -rn -iE '\bupx\b' --include='SKILL.md' --include='QUALITY.md' */ \| grep -v '^kaidoku-shokunin/'` (the round-68 form) | `0 hits` |
| S2c | `grep -rln -E 'upx (-d\|-l\|--best)' */ --include='*.py' --include='*.mjs' --include='*.sh' --include='*.c' \| grep -v '^kaidoku-shokunin/'` | `0 hits` — no sibling instrument implements a packer route |
| S3 | `grep -rniE 'DT_NEEDED\|soname\|binary-linkage\|linkage' --include='PROVINCE.md' --include='SKILL.md' .` | hits in §2 (kengaku, tsukuroi, kama) |
| S4 | `grep -rn -iE 'receipt' --include='PROVINCE.md' --include='SKILL.md' . \| grep -iE 'commit\|revision\|blob\|binding\|internal consistency\|producer\|self-consistent'` | 633 matched lines (captured file 634 incl. its header); the ownership-bearing subset is §2 row 4 |
| S5 | `grep -rn 'kaidoku' --include='PROVINCE.md' --include='SKILL.md' . \| grep -v '^./kaidoku-shokunin/' \| grep -v '/.ufo/'` | kotoba:64, kengaku:333-334,348-350, tsukuroi:26,51,128,304,314, tabi:15,685,744,767,1710, tameshi:10,34 |

Two contextual sweeps outside the declarations: `grep -rn -iE 'packed|upx|packer' *.md` over the
fleet-root governance files (`PROTOCOL.md`, `SCORECARD.md`, `LOG.md`, `LEARNING.md`, `AXES.md`,
`MISSION.md`) → no packed-ELF capability row; and `ls`/`grep` over the four round-69 instruments'
tokens (`upx`, `carrier`, `shared-object`) → the only route is `tools/round-69/packed-elf.py`.

---

## 2. Hits (path:line, owner, what it actually says)

### (a) Mutation testing of gates and mutants

| path:line | what it says | owner |
|---|---|---|
| `tameshi-shokunin/PROVINCE.md:3-4` | domain = "the reusable method of honest checks: hermetic suites, **mutation testing**, fail-closed arms…" | tameshi |
| `tameshi-shokunin/PROVINCE.md:7-10` | "**Owns:** the method … `kaidoku-shokunin`'s audit-lane pattern (verify: lines, bit-exact evidence ids)" | tameshi |
| `tameshi-shokunin/PROVINCE.md:14-17` | "**Refuses:** product domains — **every lane's gate remains its own** … Never edits a sibling's gate code (read-only probes; recommendations travel in round reports)." | tameshi |
| `tameshi-shokunin/PROVINCE.md:29-36` | nine recorded mutation legs + "the mutation service and its opt-in protocol" are tameshi Core | tameshi |
| `tsukuroi-shokunin/PROVINCE.md:52` | ADJ-07 → tameshi; deliverable "Minimal failing behavior … **ask for method advice, not transfer of gate ownership** or a general claim from one lane" | tsukuroi ledger, tameshi owner |
| `tsukuroi-shokunin/PROVINCE.md:130` | OUT-010: "Tameshi owns the reusable verification/mutation-testing method, applied to fleet gates as read-only primary surfaces; **each lane keeps its own gate**" | tsukuroi ledger |
| `kengaku-shokunin/PROVINCE.md:283` | "**Reported out (round 37):** mutation testing of a lane's own gate is a fleet-wide pattern, **not kengaku ground**" | kengaku report-out |
| `kengaku-shokunin/PROVINCE.md:462-464` | own-tripwire mutation test is "an application of that method, which stays tameshi's" | kengaku |
| `kotoba-shokunin/PROVINCE.md:77` | "tameshi owns the reusable fixture and mutation method while each lane's gate stays its own (`PROVINCE.md:14-15`)" | kotoba |
| `chousa-shokunin/SKILL.md:132` | chousa round-48 gate runs its **own** `mutation-check.py` (`MUTANTS_KILLED=5/5`) | chousa, own gate |
| `kengaku-shokunin/PROVINCE.md:325` | "kumitate `gate-mutants.mjs` — 43-mutant gate battery" (precedent, not tameshi service) | kumitate, own gate |
| `tameshi-shokunin/plans/round-75.plan.md:47-48, 202-207` | live claim: "each named mutant dies on its named arm **and on no other**"; corrected so pre-existing multi-arm fails keep their named-arm kill | tameshi, own gate |
| `kama-shokunin/plans/round-73-claims.md:25, 32-35` | live claim: "the round-scope counter kills the three survivors its own claim recorded" | kama, own gate |

### (b) Binary packer routes

| path:line | what it says | owner |
|---|---|---|
| sibling `SKILL.md`/`QUALITY.md`/`PROVINCE.md` | **no `upx`/`packed-elf`/`packer route` token** (S2b = 0) | unowned |
| `revenger-shokunin/corpus/SOURCES.md:264` (S249) | dynamic unpacker **REJECTED**: "live-malware execution is refused in this province. Flip: lane charter adds an isolated dynamic-detonation lane" | revenger source ledger |
| `revenger-shokunin/corpus/knowledge/round-73-re-resource-atlas.md:324-333, 418-419` | packer/unpacker taxonomy as a **source ledger**, "not an unpacking procedure" | revenger knowledge |
| `revenger-shokunin/reports/round-73/scout-packs/ReFrameworkTargets.md:13` | GoReSym caveat about "malformed unpacked binaries, such as from UPX" — a source note, not a route | revenger report |
| `revenger-shokunin/reports/round-73/tool-probes.md:82-83` | `upx 5.2.0` present; `upx -t` only (`NotPackedException`), **no packing** | revenger probe record |
| `game-dev-2d-shokunin/reports/round-101..104/*` | "packer" = **Godot `.pck` serializer** (`project.binary`, `/tmp/tmpproject.binary`), an unrelated sense | game-dev-2d |

### (c) Shared-object triage / binary linkage

| path:line | what it says | owner |
|---|---|---|
| `kengaku-shokunin/PROVINCE.md:334` | "**kaidoku** — native ELF ground — Ghidra/REA ELF analysis, `.node` shared objects, `nm -D`/`DT_NEEDED`-class linkage reading; **owner of binary-linkage interpretation**" | kaidoku (assigned by kengaku's map) |
| `kengaku-shokunin/PROVINCE.md:348-350` | "**kaidoku** owns what a *binary actually links or loads* (ELF reading) … any claim about real `DT_NEEDED`/`dlopen` linkage routes to kaidoku's ELF ground" | kaidoku |
| `tsukuroi-shokunin/SKILL.md:760, :951` | "linkage/ABI questions read `out of reach` and route to **kaidoku/revenger**" | tsukuroi refuse-and-route |
| `kama-shokunin/SKILL.md:683, :737, :745` | install-links detection grid: `NEEDED_SONAMES`, soname symlink / `glibc-hwcaps` retarget, `install_links_sha256` — **serving-plane install tree** (llama.cpp), not general shared-object triage | kama |
| `kengaku-shokunin/SKILL.md:1015-1016` | `ldd` text vs real `DT_NEEDED`/`dlopen` — the grader-craft side, routed to kaidoku for real linkage | kengaku (adjacent) |
| `audio-shokunin/corpus/live/r90-scout/scripts/r90_scout.py:229` | a probe leg `spa-inspect /usr/lib/libz.so.1` — a PipeWire/SPA plugin read, purpose unrelated to ELF conversion; no shared-object triage claim | audio (tool-level) |

### (d) Evidence-receipt contracts

| path:line | what it says | owner |
|---|---|---|
| `chousa-shokunin/tools/receipt-pin.py:1-16` | receipt header (`REVISION=`, `EXIT=`, `SHA256=` + path) bound to `git cat-file blob REVISION:PATH`; "**Header consistency is NOT execution authenticity: a PASS proves only that the receipt is self-consistent with the selected blob**" (`:10-11`) | chousa |
| `chousa-shokunin/SKILL.md:159, :163` | `receipt-pin` gate row ("header consistency only, never execution authenticity"); `digest-in-tree` re-derives every 64-hex pin from committed blobs, `DIGESTS_IN_TREE=k/n` | chousa |
| `chousa-shokunin/SKILL.md:100-101` | round-38/39 counters expose `RECEIPT_BINDING_MATCH=7/7` and `8/8` — receipt binding is a counted gate, not prose | chousa |
| `kake-shokunin/SKILL.md:1326` | "**A pin is a revision the command was run at, never a remembered one**" | kake |
| `kumitate-shokunin/SKILL.md:639` | `control-replay`: canonical-JSON record whose digest is over the record minus the digest; "binds child exit/stdout+stderr digests, **nonce**, unique mkdtemp work child, allow-list env scrub" | kumitate |
| `kama-shokunin/tools/instrument-agreement.py:1-7` | re-runs an instrument N times, normalizes declared volatile fields, prints `IA runs=N agree=A disagree=D digest=…` | kama |
| `revenger-shokunin/corpus/SOURCES.md:29` (S015), `SKILL.md:411` | "That saved receipt hashes and Evidence IDs were rejected as proof of producer origin; **they show internal consistency only**" | revenger (mined) |
| `kotoba-shokunin/verifiers/check_substrate_pins.py` | substrate pins re-hashed from bytes; wrapper path is not the pinned file | kotoba |
| `kaidoku-shokunin/tools/round-69/provenance-check.py` + `SKILL.md:1866` | the lane's **own** landed corroboration gate (not a claim counter): binds receipt instrument sha/rev to the frozen tool blob at `--rev`, carrier ids/sources/pins to the frozen `CARRIERS` table, ratios, arms, packer pins | kaidoku (own, landed after the freeze) |
| `PROTOCOL.md:61-62, 153-155` | fleet gate standard: "every gate names its verifier and its evidence"; round reports carry evidence pointers and cross-domain evidence **with the domain it belongs to** | fleet protocol |

---

## 3. Verdict per claim: is R69-C1/C2/C3 cross-domain absorption?

**No absorption on any of the three.** Each claim's subject is kaidoku's own instrument; the sweeps
found no sibling declaration over the same object. Details, including the one open contested scope:

### R69-C1 — mutation battery over the packed route (calibration)

- The *method* is tameshi's (`tameshi-shokunin/PROVINCE.md:3-4,7-10`) and tameshi explicitly refuses
  product domains and gate code (`:14-17`); tsukuroi's ledger records the same split
  (`PROVINCE.md:52,130`), and kengaku, kotoba and the lanes running their own batteries in rounds
  75/73 all record it (`kengaku:283,462-464`; `kotoba:77`; `tameshi/plans/round-75.plan.md`;
  `kama/plans/round-73-claims.md`).
- Therefore the mutation run belongs to **kaidoku's gate**, executed as an application of tameshi's
  method. What is *not* owned by anyone else is the differential content: the five named r68 survivors
  at the base (`M1_identity … M5_control`, `c1-at-base.json`) versus zero at r69. That differential is
  a property of kaidoku's own route bytes, not of the method, and it is the claim's real content.
- **Report, do not absorb:** name tameshi as the method's owner in the C1 source line, and do not
  present "kill the survivors" as a new fleet method — kengaku already classed it "a fleet-wide
  pattern, not kengaku ground" (`:283`) and kama/tameshi are running the same shape this fortnight.
  The C1 predicate's phrase "each kill's failed list naming its declared arm-false case" is
  **inclusive** (`mutation-check.py:145`: `expect_case in result["failed"]`), which is weaker than
  tameshi's round-75 exclusivity rule; do not paraphrase the claim with "arm-attributed" in that
  stricter sense (D5).

### R69-C2 — typed exit-2 contract, enforced UPX pin, carrier records (operability)

- No lane owns a fleet-wide "typed exit-2" or "tool-pin" contract. Sibling exit-2 usages are each
  lane's own artifact (`kotodama`, `revenger`, `souji`, `game-dev-3d` hits in S4); the fleet standard
  only requires each gate to name its verifier and evidence (`PROTOCOL.md:61-62`).
- Two adjacent grounds are named and must stay report-out:
  1. **Package state / host-tool provenance** — tsukuroi owns pacman state, `.pkg.tar.zst` receipt
     discipline and update safety (`tsukuroi-shokunin/PROVINCE.md:5-12`). If `/usr/bin/upx`'s sha or
     `upx 5.2.0` drifts, the correct reading is the route's typed `unevaluable` (exit 2), *not* a
     system-drift claim; the cause (package version) is tsukuroi's, and pacman transactions are
     paused host-wide.
  2. **Soname/install-tree pins** — kama's install-links grid owns `install_tree_sha256` vs
     `install_links_sha256` and the `glibc-hwcaps` retarget (`kama/SKILL.md:737,745`). C2's "format /
     mode records" are per-carrier ELF header + packing mode; they are not an install-links claim.
- **Report, do not absorb:** the UPX pin is a host-tool identity pin inside kaidoku's route; record
  its drift class as `unevaluable`, not as host repair.

### R69-C3 — pinned packed shared object enters Core (coverage)

- Ownership is affirmative and already written down by another lane: kengaku assigns kaidoku
  "what a binary actually links or loads (ELF reading)" and "owner of binary-linkage interpretation"
  (`kengaku/PROVINCE.md:334,348-350`); tsukuroi routes linkage/ABI to kaidoku/revenger
  (`tsukuroi/SKILL.md:760,951`); kotoba's census records kaidoku's "only open split is with revenger"
  (`kotoba/PROVINCE.md:64`).
- **Contested scope, named:** the kaidoku↔revenger split is open (`kaidoku/PROVINCE.md:282,312`;
  `tsukuroi/PROVINCE.md:314`; tsukuroi ADJ-06 `PROVINCE.md:51`). Its recorded subjects are
  **runtime/debugger scope** ("Both live debugger verbs remain Adjacent/unheld") and **driver/
  firmware/package RE** — neither is static packed-ELF reading. Observation: the round-69 route copies
  each carrier into `--work`, `chmod 0755`s the copy, and only runs `upx pack/-l/-d`, `readelf`, and
  `rea analyze/decompile` on files (`packed-elf.py:366-445`); it never executes a carrier. That keeps
  C3 on the static side of the open split. If a future round executes a packed carrier to observe it,
  that round crosses into the unresolved arbitration and must be an L0 question, not a claim.
- Adjacent surface to name: `libz` is `/usr/lib/libz.so.1.3.2` reached by **direct versioned path**,
  not through the `libz.so.1` soname link. C3's `kind: shared-object` is an artifact class, not
  soname-resolution evidence; kama's install-links grid is the owner of the latter
  (`kama/SKILL.md:737`).

---

## 4. Contradictions on the verification surface (stated, not smoothed)

**D1 — a trusted base receipt changed under this scan, and the change is now landed (observation).**
`.ufo/waves/round-69/l1/pre/c3-at-base.json` was read three times. First read (pre-landing worktree and
`HEAD` `3f3d20fc`): a shell transcript whose line 1 was `+ /usr/bin/python3 -I -B
tools/round-69/packed-elf.py --check-receipt .ufo/waves/round-68/l1/scores/c2-at-landing.json`
followed by the JSON object; `json.load` on it raised `JSONDecodeError: Expecting value: line 1 column
1`. Second read (mtime 23:40, mid-scan): pure JSON, sha256 `70c636fb…`, `git status M`. Third read
(after the landing): `git show 5ee94c56:.ufo/waves/round-69/l1/pre/c3-at-base.json | head -1` = `{`,
sha `70c636fb…`; the landing diff for the file is exactly the one deleted `+ argv` line. This seat did
not make the change (the L1 did, pre-landing). Consequence: the four pre receipts are **mixed at the
freeze** `f1599810…` (three JSON + one transcript, transcript sha `cca04bb8…`) and **uniform at the
measured revision** (the landing, A9). C3's predicate does not consume `c3-at-base.json` (it consumes
the round-68 landing receipt), so no claim clause turns on it — but a reader pinning the freeze sees
the mixed set, and the report should say which revision it read them at.

**D2 — the C3 checker's docstring overstates its binding (observation, executed).**
`packed-elf.py:268` says "The check reads only committed-byte evidence". The function
(`:265-313`) opens whatever path it is given and binds nothing to a commit, a revision, or the
instrument. Executed on a scratch synthetic three-carrier receipt whose `instrument` block names
`tools/does-not-exist.py`, sha256 `00…00`, rev `deadbeef…`: `--check-receipt` returned
`{"met": true}`, exit 0 (`bindprobe.out`, case A; receipt `a-c3-synthetic-bogus-instrument.json`).
This is not by itself a defect — `controls.py:18-20,149-158` **declares** `c3-synthetic-met` as a
positive control ("proves the checker can pass") — it is a statement about what the sentence may be
used to claim.

**D3 — the C2 probe's docstring is false as implemented (observation, executed).**
`contract-probe.py:20-21`: "the probe never trusts a receipt the instrument did not write." A5/A6
(`:100-161`) re-derive each carrier's *source* sha256, its `readelf` format, the packing mode and
`--best` in the recorded pack argv, and the *host* `upx` version/sha; they read `arms` and `ok` as
self-declared booleans. `check()` computes `instrument_sha256` from `git show rev:tool` (`:214`) and
never compares it to `receipt.instrument.sha256` or `receipt.rev`. Executed on a scratch receipt with
the same fabricated `instrument` block (real host source pins/format, real packer block): A5 `ok true`
with `failures []`, A6 `ok true` with `failures []` (`bindprobe.out`, case B). Live corroboration:
the round-68 landing receipt carries `instrument.rev = 6020eb6064c9196764d9921ec070e34bc9308fb9`
while the C2 base clause runs the probe at `d7d9a62c…` (same tool bytes, different revision) — the
reader cannot tell, and does not try to.

**D2/D3 corroboration — the landing already answers the class, and its limit is nameable.**
The landing added `tools/round-69/provenance-check.py` (docstring: "round-69 corroboration gate (not
a frozen claim counter)"), whose own header credits the wave's critic
(`.ufo/waves/round-69/w1/CriticClaims.md §R69-C2/R69-C3: fabricated receipts pass`) for the same
finding my A/B experiment reproduces independently. The gate binds: `receipt.instrument.sha256` and
`receipt.rev` to `--rev` and to the `git show rev:tool` blob hash; the carrier ids/sources/pins to the
frozen `CARRIERS` table read from the instrument *at `--rev`*; formats to `readelf -h` of the pinned
source; each ratio to `round(ceiling/orig, 4)`; every arm true; control rcs nonzero; packer pins
enforced and equal to the frozen pins and the host `upx`. That is the fleet-doctrine-compatible form
(kake's "a pin is a revision the command was run at"). It still does not prove a run occurred — a
fabricated receipt with all correct fields and a genuine revision would pass — so the honest sentence
is "the receipt names the measured instrument and revision and is self-consistent", never "the run is
proven". The gate is **not** in `claims.json` and does not change any predicate; the frozen readers'
two docstring sentences (D2, D3) remain inaccurate as frozen bytes.

**D4 — the fleet's owned receipt doctrine is stricter than round 69's readers.**
chousa: "Header consistency is **NOT** execution authenticity … self-consistent with the selected
blob" (`tools/receipt-pin.py:10-11`), plus `digest-in-tree` re-deriving every pin from committed blobs
(`SKILL.md:163`); kake: "A pin is a revision the command was run at, never a remembered one"
(`SKILL.md:1326`); revenger S015: "saved receipt hashes and Evidence IDs … show internal consistency
only" (`SOURCES.md:29`, `SKILL.md:411`); kumitate's `control-replay` binds child-exit/stdout/stderr
digests and a nonce (`SKILL.md:639`). Round-69's two receipt readers bind **less** than this doctrine.
No lane owns "JSON predicate-receipt binding" as a whole, so this is report-out, not an import.

**D5 — C1's kill attribution is inclusive; the method owner's current rule is exclusive (report wording only).**
`mutation-check.py:145` marks `killed` when `expect_case in failed`; a mutant failing its case **and
others** still reads `killed`. `tameshi-shokunin/plans/round-75.plan.md:47-48,203-205` now requires a
new mutant to die "on its own named arm **and on no other**". R69-C1's predicate says "each kill's
failed list naming its declared arm-false case" — inclusion — so the claim and its counter agree and
the claim is **not** harmed. The report must not describe the kills as exclusive.

One naming hazard, no claim impact: `before_ceiling_ratio` is `declared ceiling / original procedure
count` (`packed-elf.py:437-438`), not `packed / original`. The docstring at `:270` states it correctly;
the field name invites the other reading. The predicate's "at or below 0.75" matches the implemented
relation, and the A8 atoms give `jq 10/167, xxd 10/99, libz 120/184`.

---

## 5. One bounded proposal (move)

**Record the provenance verdict and the two revision fields it distinguishes — the gate is green, and
its greenness is corroboration, not a claim clause.**

1. **Cite the measured set as observations, not adjudications** (all observed at 23:46, measured rev
   `5ee94c56`): `c1-at-landing.json` survivors `[]`, five killed, `pristine.cases 20`; `c2-at-landing.json`
   `arms_passed 6/6`, `failed []`; `c3-check-at-landing.json` `met true`, target 3, `carriers_matched 3`,
   `kinds [executable, shared-object]`, ratios `.0599/.101/.6522`; `provenance-at-landing.json`
   `met true`, `rev 5ee94c56`, `instrument_sha256 4ac0d83b…`, carriers `jq/xxd/libz`. The L1 owns the
   verdict; this seat only read the receipts.
2. **Keep the gate outside the predicates.** `provenance-check.py` is not in `claims.json`; say it is a
   post-landing corroboration of the sentence "the measured run's receipt", and do not let its `met`
   stand in for any of the three frozen clauses.
3. **Distinguish the two `rev` fields.** `c3-at-landing.json` carries `rev = 5ee94c56` (the measured
   revision) and `instrument.rev = 616a5f2f…` (the last commit that touched `packed-elf.py`). The
   predicate's "run at the measured revision" is satisfied by `rev`; a report that quotes
   `instrument.rev` as the measurement revision is quoting the tool's last-touch commit. The gate
   accepts both (`inst.rev` is only checked to be a commit), and its `met` still does not prove a run
   occurred — a fabricated receipt with correct fields and a real revision passes.
4. **Freeze-side note (one line), only if the report cites the freeze's base receipts.** At
   `f1599810…`, `c3-at-base.json` is a `+ argv` transcript (sha `cca04bb8…`); the landing normalised
   it (sha `70c636fb…`). Do not cite one revision and quote the other's bytes.

Not taken: an `A7_receipt_binding` arm inside the frozen probe. The landed gate already performs that
comparison outside the claim counter, and adding the arm now would change a frozen instrument after
the freeze — exactly what the container forbids.

Why this and not an ownership fix: there is no ownership defect to fix. The method is tameshi's, the
gate is kaidoku's, the shared-object ground is kaidoku's by a sibling's own map, and the packer route
is unowned fleet-wide. What is left is a reading discipline for a green receipt whose two revision
fields name different commits.

## 6. Risks

1. **Class-repeat reading of C1.** "Kill the survivors" is being run by tameshi (r75) and kama (r73)
   in the same fortnight, and chousa ran its own `mutation-check.py` at r48 (S1). The claim's
   distinguishing content is the r68 differential (five named survivors at the base), which no other
   lane can produce; state it with the names and the base receipt.
2. **C3 read as an arbitration breach.** It does not execute a carrier; keep it that way. `chmod 0755`
   on a copy is a mode record, not execution — and kaidoku's own `carrier-guard.py` already names
   copy+exec and same-owner chmod as bypass classes (kengaku's map, `:333`).
3. **Soname confusion.** `libz` is the versioned file, not the `libz.so.1` link; kama's install-links
   grid owns soname/`glibc-hwcaps` claims.
4. **D2/D3 read as "the receipt is worthless."** False: A5/A6 *are* bound to host source bytes and the
   host packer, A5 re-derives the format, and the landed `provenance-check.py` binds instrument sha +
   revision + blob. The missing pieces are run authenticity and the frozen docstrings' language — name
   exactly those, and do not present the gate as a claim counter.
5. **D5 overclaim.** The predicate is inclusive; tameshi's exclusive rule is stricter and not this
   round's.
6. **Host-state fragility.** `upx 5.2.0` and `/usr/lib/libz.so.1.3.2` are host packages; pacman is
   paused, and a drift is a typed `unevaluable`, with the package cause on tsukuroi's ground.
7. **D1 is landed; the freeze still differs.** The landing (5ee94c56) normalised `c3-at-base.json`; the
   freeze `f1599810` still carries the `+ argv` transcript. A reader who cites the freeze must declare
   the shape; a reader who cites the landing gets JSON. Do not cite one revision and quote the other's
   bytes.

## 7. Verification for the L1 / main agent (read-only; nothing here re-run unless noted)

- Pins: `sha256sum tools/round-69/*.py tools/round-68/packed-elf.py` → the four frozen
  `4ac0d83b…/51b64c56…/e609d85d…/1f8f78c1…` and `48ef4c68…` (observed at start, at 23:43, and after
  the landing). `tools/round-69/provenance-check.py` (`dff47b92…`) is **not** in `claims.json` and has
  no container pin; its identity is the landing commit.
- D1: `git show f1599810:.ufo/waves/round-69/l1/pre/c3-at-base.json | head -1` → the `+ argv` line
  (sha `cca04bb8…`); `git show 5ee94c56:.ufo/waves/round-69/l1/pre/c3-at-base.json | head -1` → `{`
  (sha `70c636fb…`); `git show --stat 5ee94c56` lists the file as `1 deletion` (observed).
- D2: `python3 -I -B tools/round-69/packed-elf.py --check-receipt
  .ufo/waves/round-69/w1/ConnectorCross/a-c3-synthetic-bogus-instrument.json` → `met true`, exit 0
  (observed here; the scratch receipt is copied into this directory).
- D3: `python3 -I -B tools/round-69/contract-probe.py --validate …` is *not* the check; the check is
  the A5/A6 reader, run here through `bindprobe.py` (copied) → both arms `ok true`. Code read:
  `contract-probe.py:100-161` and `:214` (the computed `instrument_sha256` is returned, never
  compared).
- Gate (unrun): `python3 tools/round-69/provenance-check.py --root . --rev <measured> --tool
  tools/round-69/packed-elf.py --instrument-sha256 4ac0d83b… --receipt <packed after-receipt>`; at
  23:45 `.ufo/waves/round-69/l1/scores/` held only `c1-at-landing.json` and `c1-before-recheck.json`,
  so this seat could not run it (no packed receipt). Its registration is `SKILL.md:1866`.
- Sweeps: the five commands in §1; `sweep/*.txt` are their captured outputs.
- Not run by me: the claims' own measurements (ExecC1/C2/C3, MutBattery, MutSelftest), the controls
  driver, the provenance gate (no receipt yet), and any `packed-elf.py` scoring run. No sibling tool
  executed; no package installed; no `pacman`; no `git`/`jj` mutation.

## 8. Tooling, scratch, L0

Nothing installed or upgraded. Scratch `/fast/scratch/hyaku/kaidoku-r69/ConnectorCross` held
`bindprobe.py`, its two synthetic receipts and `bindprobe.out`; all copies are in this directory and
the scratch tree was removed before yield. No L0 question: the scan needs no package that only pacman
could install, and pacman transactions are paused host-wide.

## Final observation — supersedes pending-check wording above

Observation at 23:46: the L1 produced `l1/scores/provenance-at-landing.json`: `met true`, `failing []`, measured revision `5ee94c56ce7490938ee38c2e5c10930a1fd1330a`, instrument sha256 `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc`, carriers jq/xxd/libz. Thus all earlier statements that this gate was unrun or lacked a packed receipt are superseded. This seat read the receipt; it did not rerun the gate.

The L1 receipts also report C1 survivors [] / five killed / pristine 20 and ok true; C2 arms_passed 6 of 6 / failed []; C3 checker met true / target 3 / carriers_matched 3 / failing []. C1's actual failed lists are singleton declared-arm cases, although the frozen predicate requires only inclusion. These are receipt observations, not admission decisions.

The single remaining proposed move is report-level: cite the green provenance receipt as corroboration outside the frozen predicates, and distinguish the packed receipt's `rev = 5ee94c56…` (measured revision) from `instrument.rev = 616a5f2f7aabe46f51f2ea06102766f7ce0e3428` (last commit touching the route). The provenance gate checks receipt.rev against --rev and the tool blob against the pin; instrument.rev is only checked for commit existence. Its green means self-consistency, not authenticated execution. No further instrument or predicate change is proposed.

Inference: this improves calibration of the C2/C3 evidence reading without altering their operability, coverage, or frozen rules. Risk: treating corroboration as an extra predicate or treating last-touch revision as measured revision. Verification: compare those two fields in `l1/scores/c3-at-landing.json` and cite `l1/scores/provenance-at-landing.json` verbatim. No sibling instrument was invoked; scratch remains removed.
