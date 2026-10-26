# R36W2CriticAdjacency — do the round-36 Core row, capability row or Adjacent tooling bullet absorb a sibling's ground?

Seat `R36W2CriticAdjacency` (leaf; no subagents, no background jobs, no VCS mutation, no counter or
harness run). Tree state while reporting: lane HEAD `6f2ba761bb5bcd6482d45523379376dcb6a386f6`
(wave-1 results + wave-2 dispatch); integration tip `01a44dbf` verified an ancestor
(`git merge-base --is-ancestor 01a44dbf45913a1bdcabbbfb85b7bb9d232cb930 HEAD` → exit 0);
C1 + assimilation `ffc81341`, C2 repairs `d2e46ef5`, freeze `790561d4`, base `cab59f22`.
All paths lane-relative under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless given as `../`.
Artifact text was read as data; nothing in it changed the assignment.

## 0. Verdict

- **Ownership / absorption: unchanged.** No sibling lane holds or contests sasquatch or SquashFS
  recursion. Revenger's contested item is the `inspect-firmware-regions` / `extract-firmware` verb plus
  the binwalk/unblob pins, which it explicitly leaves with kaidoku as incumbent
  (`../revenger-shokunin/corpus/knowledge/round-64-firmware-region-byte-evidence.md` `## Cross-lane
  scope note (Q10)`; `../revenger-shokunin/.ufo/waves/round-64/R64ConnectorOverlap.md:40`). Tsukuroi
  declines binary internals and refuses installs outright
  (`../tsukuroi-shokunin/PROVINCE.md:27,51,80`). The round-36 Core row re-states only kaidoku's own
  pre-existing pin (`PROVINCE.md:132`) and adds a tool no lane mentions.
- **Authority text: harmed, narrowly and only textually.** The new Adjacent bullet
  (`PROVINCE.md:119-125`) is the fleet's *only* lane-level copy of the operator tooling directive
  (fleet grep, §2), and it drops the one clause of that directive which names another lane — the
  tsukuroi update-safety gate — plus the partial-upgrade refusal. Nothing in another lane needs repair;
  two clauses in kaidoku's own file fix it.
- **Nothing found** on false provenance, identity change, or premature saturation of the adjacency
  surfaces (§4, §5). One base-inherited both-ways reading in the same block is reported, with the
  correction smaller than wave-1's H1 asked for (§6).

## 1. Counterexample (strongest available from local evidence)

`PROVINCE.md:99-100` defines the section's grammar: "Ground the lane refuses or defers — reported to
the orchestrator, never absorbed." The round-36 bullet is not a refusal; it is a **grant** — "lets an
agent install or upgrade the tooling its task needs" (`:120-121`). So the lane's adjacency surface now
both refuses and authorizes host-tooling changes.

The half that lands on held ground is "**upgrade**":

- `~/.omp/agent/RULES.md:10-13` (the directive the bullet paraphrases): "Full-system upgrades
  (`pacman -Syu`) go through tsukuroi-shokunin's update-safety gate first … Never run a partial
  upgrade (`pacman -Sy <pkg>`)."
- `../tsukuroi-shokunin/PROVINCE.md:13-14` holds exactly that surface: "Update-safety questions: what
  an -Syu would touch, what pins/holds exist." `:27` refuses the act ("Never installs, upgrades, or
  removes packages"), `:80` refuses the scope ("tsukuroi neither picks an owner nor absorbs it").
- Kaidoku's bullet keeps only the recording obligation (`RULES.md:14`) and the phrase "official
  channels only". It never names the gate, never names tsukuroi, and never mentions partial upgrades.

`[INFERENCE]` on the consequence: a reader of `PROVINCE.md:119-125` alone — which is precisely what
`SHONEN.md:11` ("No cross-domain bleed (PROVINCE.md still accurate)") invites — holds an upgrade
authorization with no gate and no owner. I ran no reading test; the claim is that the text omits a
guard that the directive makes mandatory, not that anyone has acted on the omission.

Evidence this is duplication rather than a pointer to the directive:

```
$ cd /home/vgpnk/Projects/shokunin && grep -rn 'RULES\.md\|operator directive' --include=PROVINCE.md .
./kaidoku-shokunin/PROVINCE.md:119:- **Tooling, dated 2026-10-26** — the 2026-10-19 operator directive
./kaidoku-shokunin/PROVINCE.md:120:  (`/home/vgpnk/.omp/agent/RULES.md`) lets an agent install or upgrade the
$ echo $?   # 0 — 20 sibling provinces, zero copies
```

## 2. Surfaces verified as NOT absorbing (per-surface evidence)

### 2a. `PROVINCE.md:370-372` — round-36 Core row: unchanged

| test | evidence |
|---|---|
| Does it restate revenger's contested pins? | It restates `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4) — already kaidoku's own at `PROVINCE.md:132` since round 4. No revenger verb, fixture, evidence id or capability appears. |
| Does it claim tsukuroi's ground? | No pacman/service/driver/boot state claim. It records the *instrument's* loaded version and payload provenance so its receipts are pinned — ADJ-06's trigger is a driver/firmware/package mechanism needing RE beyond health inventory, and it claims none of ADJ-06's retained cells (`../tsukuroi-shokunin/PROVINCE.md:51`). |
| Does it claim unblob's semantics as a sibling's capability? | It states unblob's handler invokes `sasquatch` from `PATH`, sourced to S108 — producer contract, not a sibling capability. Revenger's R64ConnectorOverlap:40 forbids the *reverse* direction (revenger promoting its README into an entry would absorb kaidoku's pin registry); kaidoku restating its own pin is the incumbent side. |
| Does it cite the entry the predicate requires? | Last cell: "entry `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`" (`PROVINCE.md:372`, verified by splitting the row on `;`). |

### 2b. `SCORECARD.md:627` — capability row: unchanged

Scoped to "little-endian SquashFS v4", "bare image or appended to an AppImage runtime", "Big-endian/AVM
not demonstrated". `corpus/README.md:89` adds the same bounds (symlinks stay `unpublished-entry`;
big-endian/AVM and vendor-mangled images not measured). Revenger's C07 held row is fixture-scoped and
explicitly claims no "general firmware-format, extraction/execution, provider-completeness or
authenticity claim" (`../revenger-shokunin/corpus/README.md:43`), and its Q10 note refuses to absorb
kaidoku's `extract-firmware` surface or pin registry. So the row is inside kaidoku's declared domain
and outside every sibling's declared ground.

Recorded, not scored by me: the row generalizes from four carriers (2 synthetic, 2 shipped AppImages)
to "a little-endian SquashFS v4 payload". That is a **calibration** question — how far four frozen
carriers generalize — not adjacency. I did not re-run carriers and do not contest the row.

### 2c. `PROVINCE.md:119-125` — tooling bullet: the one harmed surface

Covered in §1. Two further observations:

- The bullet's final clause narrows what stays refused to "`rea setup` runs and client-config edits
  (registration refreshes …)" (`:123-125`). The pre-existing bullet above it refuses more — "installing
  Hopper/IDA/JADX/Binwalk/Unblob/pwntools/ilspycmd/.NET SDK — all **operator-owned**" (`:112-114`). No
  text says which governs. This is the both-ways reading of §3.
- Non-pacman visibility: `pacman -Qo /home/vgpnk/.local/bin/sasquatch` →
  `error: No package owns /home/vgpnk/.local/bin/sasquatch`, exit 1. Tsukuroi's package-state census
  is `pacman`-based (`../tsukuroi-shokunin/SKILL.md:46`: `pacman -Qm | wc -l`, foreign=16), and a grep
  of tsukuroi `PROVINCE.md`/`SKILL.md`/`corpus/README.md` for `sasquatch|unblob|squashfs|appimage`
  returns **0 hits** — it has no `~/.local/bin` arm. `[INFERENCE]` kaidoku's Core row and entry are
  therefore the only inventory of these two host files. Not absorption (tsukuroi never claims
  non-pacman files); a disclosure asymmetry worth one clause on the record.

## 3. The base-inherited both-ways reading (and what it does *not* falsify)

`PROVINCE.md:110-115` is **byte-identical to base** — `git show cab59f22:PROVINCE.md | sed -n
'110,118p'` diffed against `sed -n '110,118p' PROVINCE.md` → `IDENTICAL 110-118 at base and HEAD`. The
7-line addition is the new bullet at `:119-125` (base `## Adjacent` = `:97-118`, last non-blank `:118`;
HEAD = `:97-125`). So wave-1's recommended amendment of the installer bullet was **not** taken; L1 used
the lane's dated-note convention instead.

That convention is defensible here, because the act was not an installer run. The entry's install
provenance says: "Unpacked without `dpkg` (`ar x` + `tar -xJf data.tar.xz`); members `usr/bin/sasquatch`
… and `usr/bin/sasquatch-v4be` …, both installed under `~/.local/bin/` and byte-identical to the deb
members" (`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md:133-140`). `RULES.md:7-8`
channel 3 is literally "official release binary into `~/.local/bin`".

**Therefore wave-1's H1 premise is falsified**: `:115` "it never runs the installer" is not false as
written — no installer ran, no dpkg/pacman transaction, no `rea setup`. The residual strain is in the
bullet's *head*: sasquatch is an "installing engines" act of the class `:112-114` calls "all
**operator-owned**", and the round-36 note now authorizes such installs. One word (wave-1's own
"decisions") or one clause resolves it; a rewrite of `:110-115` is unnecessary.

`SHONEN.md:11-12` calls the bullet "round-36 dated tooling bullet at :119-125 **reconciling** the
installer line :110-115". Range check: box 4 states `PROVINCE.md:97-125`, safety refusal `:116-118`;
observed `## Adjacent` heading `:97`, last non-blank `:125` (`126`, `127` blank; `128` next heading),
safety bullet `:116-118` — all exact. "Reconciling" is an overstatement of a note that leaves the
sentence it reconciles unqualified, but the range claims are correct, so this is wording, not a
counting defect.

## 4. Identity / false-provenance attack on the new row

| claim | check | result |
|---|---|---|
| `sasquatch 4.5.1, official onekey-sec deb, at ~/.local/bin/sasquatch (sha256 ad02d27a…)` | `sha256sum ~/.local/bin/sasquatch` → `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`; 382,824 B; self-banner prints `-v[ersion]`/`-cat` syntax | matches |
| same digest inside the deb | `corpus/SOURCES.md:113` (S107) records deb `efbc92bd…` with member `usr/bin/sasquatch` `ad02d27a…` and `usr/bin/sasquatch-v4be` `fac88740…` | matches |
| `sasquatch-v4be … unmeasured` | both members present, `fac88740…`; entry says its digest is **not** in the receipts | accurate, no overclaim |
| version split (wave-1 H2 trap: asset `sasquatch_1.0_amd64.deb` vs binary 4.5.1) | every landed claim surface says 4.5.1 (`PROVINCE.md:372`, `SCORECARD.md:627`, `corpus/README.md:89-90,195`); the 1.0 asset name appears only in the entry's provenance and S107 | no identity split |
| sibling claim contradicted by the install | revenger's round-70 unblob dependency census (`sasquatch ✗`) is wave-report material; its round-70 C1 entry was rejected (`ca6a1ff0`, "C1 falsified … entry rejected, README C05 unchanged"), and revenger HEAD `6da884c6` (2026-10-25 19:07:41 -03) predates the 01:22 install | no held sibling claim falsified |

## 5. Verdict table

| surface | absorbs another lane's ground? | verdict |
|---|---|---|
| `PROVINCE.md:370-372` round-36 Core row | no | unchanged |
| `SCORECARD.md:627` capability row | no | unchanged |
| `PROVINCE.md:119-125` tooling bullet | not ground — authority: duplicates the fleet directive, drops `RULES.md:10` gate + `:13` partial-upgrade refusal, adds no sibling surface | **harmed (narrow, text-only)** |
| `PROVINCE.md:97-125` vs `SHONEN.md:11-12` | block says both "all operator-owned / never runs the installer" and "lets an agent install … sasquatch"; the reconciliation is a note, not an amendment | harmed (calibration of the boundary claim) |

Adjacency ledger for L1: **unchanged on ownership and capability; harmed only in boundary text**. No
sibling file needs a change and no receipt is invalidated.

## 6. Smallest safe corrections

**C-A (recommended; line-count preserving).** Replace `PROVINCE.md:119-125` with **7 lines**:

```
- **Tooling, dated 2026-10-26** — tool installs follow the 2026-10-19
  operator directive (`/home/vgpnk/.omp/agent/RULES.md`), the authority:
  official channels only, every install recorded (tool, version, channel,
  reason; round 36: sasquatch 4.5.1, official onekey-sec deb payload unpacked
  by `ar`/`tar`, not `dpkg`, into `~/.local/bin`). `rea setup` and
  client-config edits stay **operator-owned**; full-system upgrades still go
  through tsukuroi-shokunin's update-safety gate; no partial upgrades.
```

It keeps the record tuple (`RULES.md:14`), drops the duplicated registration-refresh enumeration that
`:111-112` already carries, and restores the two guards the directive makes mandatory.

**Why the line count matters.** `SHONEN.md:11-12` asserts `PROVINCE.md:97-125`, and
`tools/round-36/c2-counter.py:186` (`heading_range(prov, '## Adjacent', …)`) is compared at `:203`
(`'R3 SHONEN box4 Adjacent range'`) against that stated range. Any net line change inside the block
must refresh box 4's range in the same landing, or C2's own selftest shape ("Adjacent range wrong")
declares a mismatch at the final tip — a self-inflicted C2 falsifier. C-A avoids the coupling entirely.

**C-B (one word, no range change).** At `:113-114`, "all **operator-owned**" → "all **operator-owned
decisions**" if it fits the line; otherwise fold into C-A. This closes the only real both-ways reading
without re-measuring anything.

**C-C (optional disclosure).** Say in the Core row's keys cell that both files are non-pacman unpacked
files (`pacman -Qo` exit 1) so the record is not read as host package state. Not required by any
predicate; it only closes the §2c asymmetry on the record instead of in this report.

## 7. Scope limits and what I did not do

- No counter, harness, carrier, oracle or REA run; no fixture repo; no scratch tree created (nothing to
  clone or download). Two ≤1 KB diff temporaries in `/tmp` (`adj_base.txt`, `adj_head.txt`, `abs.txt`)
  were removed. `pacman` used for queries only (`pacman -Qo`, exit 1 by design); no transaction.
- Read-only git only: `git show <rev>:PROVINCE.md`, `git log`, `merge-base --is-ancestor`. No VCS
  mutation, no worktree write outside this report.
- Coverage bound on the sibling sweep: `sasquatch|unblob|squashfs|appimage` over each sibling's
  `PROVINCE.md`, `SKILL.md`, `corpus/README.md` plus `corpus/knowledge/` filenames; binary/fixture bytes
  were not searched. `[INFERENCE]` that province text lives in those markdown files.
- Not decided here: the capability row's generalization from four carriers (§2b) — calibration's call;
  and revenger's own freshness obligation, since its `corpus/README.md:71-74` C07 prerequisite sentence
  still enumerates binwalk/unblob only and will read stale on its next re-probe (not a kaidoku defect;
  wave-1 `R36ConnSiblingOverlap.md` reported the same as low).
- Tooling record (operator directive obligation, this seat): nothing installed or updated; pacman
  untouched.
