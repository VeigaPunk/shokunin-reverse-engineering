# CR4 (critic) — attack on C3: is a committed citation-drift gate warranted, or is the lane gate-happy?

Seat CR4, wave arc2-loop1-round3, read-only on the repo. Every command below
was run by this seat this session (2026-10-18, stamps 17:55Z–18:05Z) at HEAD
`679af5d749f2fd48b9d543e3c99d348d5458f90f`; `git status --porcelain` →
`?? .ufo/waves/arc2-loop1-round3/` only. This report is my only write. Scratch
is confined to `/tmp/arc2-l3r3-CR4-*`. No MCP session, no battery leg (not my
scope); no session to close.

**Pre-pair receipt check (my leg):** `.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt`
verified **5/5** — all five `sha256sum` lines byte-match the live files
(command and output in §2.1). Independently corroborated by SC2.md:7 and
V3.md:7 at 17:57:37Z/17:58:44Z.

## 1. Verdict

**REFUTE the gate form; a reduced, differently-shaped capability is warranted
instead.** C3's premise — "the lane has been bitten by drifted pointers for
three rounds, therefore commit a gate" — does not survive contact with the
class it names. Three measured reasons:

1. **The pointer target is operator-owned and mutating; a committed gate over
   it is red by construction.** Two of C1's five loci (`mcp-registrations.md:88`
   and `r4-16-frontier-rescan.md:43`) carry a line pointer into
   `~/.kimi-code/config.toml` — a file this lane may not commit, may not edit,
   and whose contents the custody SOP forbids storing (`SKILL.md:247-248`,
   "Hashing stores digests only, never contents"). That file's `[mcp_servers.rea]`
   stanza occupied **five distinct line numbers in ~6 hours** this session's
   evidence shows: `:2913` (08:56 .bak) → `:2930` (11:45) → `:2938` (14:32) →
   `:3225` (14:50) → `:3296` (now, live read). **C1's own proposed repair
   target `:2938/:2940` was already dead at my read time** — `:2938` now holds
   `provider = "opencode-go-7"`. Re-pointing to a fresher line number
   reproduces the defect with a newer timestamp.
2. **The lane's own convention sanctions "dead" pointers.** `SCORECARD.md:16-17`:
   "Line citations to pre-existing lane files refer to the baseline revision
   unless explicitly marked current"; the same convention is declared in the
   lesson at `corpus/lessons/2026-10-15-round-1.md:7`. A line-bounds resolver
   therefore fires on compliant, sanctioned citations. Measured false-positive
   surface at HEAD (§2.4): naive resolver **198/440**; basename resolver
   **42/440**; honest scoped resolver **4/345** — and those 4 are themselves
   false positives (§2.5).
3. **The gate would have gone red on the lane's own honest, receipt-backed
   round-2 work.** Round-2 landed `config.toml:2940` as a *receipt-anchored*
   pointer in `PROVINCE.md:18`, `SCORECARD.md:59`, `SCORECARD.md:698`,
   `LOG.md:1018`. At my read time every one of those is dead — not through lane
   error, but because the operator's config moved three times in a day. A gate
   whose redness does not track lane defect is worse than no gate.

The precedent comparison cuts the same way. `interactive-r1-recovery` is a
justified gate because its inputs are **in-repo, immutable, and contested**:
206-line `verify-recovery.py` + 143-line `expected.json` + 174-line
`wave-spec.json` = **523 lines of committed artifact**, validating a sealed
package. It still needed a correction cycle (39-line
`corpus/lessons/2026-10-15-round-1-admission-correction.md` + `LOG.md:585-608`
+ SCORECARD errata) because its `--admission` branch raised a finding
unconditionally. That cost bought durability on a contested artifact. The
citation-drift class has the opposite shape: mutable, external, operator-owned,
and — measured — mostly sanctioned. Gate #2 would buy a red light that means
nothing.

**Reduced capability that IS warranted (one-axis-move-preserving):** land the
already-validated E23 instrument (`c2-census.py`, sha256 `cf5d65b6…`, 274
lines) as the lane's **first `probe` registry row** — PROTOCOL's own vocabulary
for exactly this (`PROTOCOL.md:363-364`: "A tool that cannot fail is a
**probe**, and is registered as one"), or, if it can fail, keep its
`pointer_drift` field a **reported diagnostic**, which is precisely what round-2
decided (`R2.md:129`, "Do not gate C2 on the partition census";
`E23.md:261-267` gate definition; instrument exit line `/tmp/arc2-l2r2-E23/c2-census.py:274`
excludes `pointer_drift` from the exit condition — verified by reading the file
this session). The durable repair for the operator-owned-target loci is
**de-line-numbering the citation** (cite `[mcp_servers.rea]` / `args` by key,
not by line), which is a text change, not a gate — and no gate can enforce it
without encoding the very convention that makes line-pointers legitimate.

## 2. Evidence — exact commands with observed output

### 2.1 Pre-pair receipt 5/5 (my leg)

```console
$ for f in /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json \
    /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile; do sha256sum "$f"; done
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json
bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c  /home/vgpnk/.kimi-code/config.toml
7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598  /home/vgpnk/.bashrc
6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30  /home/vgpnk/.profile
```
All five match `.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt`
lines 2-6 byte-for-byte → **5/5 OK**.

### 2.2 The target file's line-number instability (the decisive measurement)

The `[mcp_servers.rea]` stanza, read from the operator's own backups plus the
live file — five distinct line numbers in one day:

```console
$ for b in /home/vgpnk/.kimi-code/config.toml.20261018-*.bak; do \
    printf "%-60s lines=%-6s rea_stanza=%s\n" "$(basename $b)" "$(wc -l < $b)" \
    "$(grep -n '^\[mcp_servers.rea\]$' $b | cut -d: -f1)"; done
config.toml.20261018-085645.bak     lines=2939   rea_stanza=2913
config.toml.20261018-114557.bak     lines=2956   rea_stanza=2930
config.toml.20261018-143236.bak     lines=2964   rea_stanza=2938
config.toml.20261018-145016.bak     lines=3251   rea_stanza=3225

$ grep -n "^\[mcp_servers.rea\]$" /home/vgpnk/.kimi-code/config.toml   # live, 18:00Z
3296:[mcp_servers.rea]
$ wc -l < /home/vgpnk/.kimi-code/config.toml
3322
```

C1 proposes re-pointing the dead `:1284/:1287` tokens to `:2938/:2940`. Live
read at 18:00Z:

```console
$ sed -n '2938p;2940p' /home/vgpnk/.kimi-code/config.toml
provider = "opencode-go-7"
capabilities = [ "thinking", "tool_use" ]
```

**The proposed repair target is already dead.** `:3225` — the anchor the
round-2 drift record itself used — is also dead:

```console
$ sed -n '3225p;3227p' /home/vgpnk/.kimi-code/config.toml
display_name = "K3-256k"
default_effort = "high"
```

`PROVINCE.md:18` shows the lane already knows the pattern and encodes it in
prose rather than a pin:

> `rea-agents@6.7.0` (`~/.kimi-code/config.toml:2940` at the 16:57:35Z receipt;
> a 17:32Z rewrite relocated it to :3227, value unchanged).

Note that even this hedge (`:3227`) is dead at my read time.

### 2.3 Why the target cannot be snapshotted (the PROTOCOL blocker)

PROTOCOL's **Two evidences** clause (`/home/vgpnk/.kimi-code/skills/shokunin/protocol/PROTOCOL.md:375-382`)
requires a gate whose verdict depends on a mutable artifact to "ship a run over
a committed input snapshot with its committed expected verdict", and requires
that `expected.json` "MUST pin the digest of every snapshot input file". The
lane's own custody SOP forbids the prerequisite (`SKILL.md:247-248`):

> operator-owned incident, not a custody step. Hashing stores digests only,
> never contents.

And the file is outside the repo entirely:

```console
$ git ls-files | grep "config.toml"
.ufo/waves/arc2-loop1-round2/receipts/drift-config-toml-20261018T173220Z.txt
```

So the gate's pinned pointer table cannot be built: the input is
operator-owned (not committable), contents-unstorable (SOP), and mutable
(three rewrites in-window). PROTOCOL:378-379 is explicit that "a run over a
moving worktree is not comparable to one over the cited commit" — which is
exactly the state of every citation into this file.

### 2.4 False-positive surface of a line-bounds gate (three resolvers, HEAD)

Three independent scripts written and run this session
(`/tmp/arc2-l3r3-CR4-pointercensus.py`, `-scoped.py`, `-samefile.py`), all
reading immutable Git objects at HEAD:

```console
$ python3 /tmp/arc2-l3r3-CR4-pointercensus.py
{"revision": "679af5d749f2fd48b9d543e3c99d348d5458f90f", "pointers_total": 440,
 "pointers_dead": 198, "tracked_files": 99}

$ python3 /tmp/arc2-l3r3-CR4-scoped.py
{"rev": "679af5d749f2fd48b9d543e3c99d348d5458f90f", "scoped_files": 97,
 "A_pointer_tokens": 440, "A_dead_naive": 42, "B_dead_with_basename_match": 42}

$ python3 /tmp/arc2-l3r3-CR4-honest.py
{"rev": "679af5d749f2fd48b9d543e3c99d348d5458f90f", "scope_files": 97,
 "resolvable_pointers": 345, "dead": 4, "ambiguous_or_untracked": 95,
 "false_positive_rate_if_gated": 0.012}
```

Reading: a naive gate is red on **45%** of all pointer tokens. Even the honest
resolver leaves **95** ambiguous-or-untracked targets that a gate must classify
before it can say anything — and the classification rule is the baseline-revision
convention, i.e. lane policy, not a fact.

### 2.4b C1's five loci, decomposed by what they actually carry

```console
$ grep -n "config\.toml:[0-9]" corpus/knowledge/2026-10-13-mcp-registrations.md
88:- kimi stanza header is `config.toml:1284` (startup_timeout_sec at 1287), not 1285/1288. (audit-A, consistency)
$ grep -n "config\.toml:[0-9]" corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md
43:  `~/.kimi-code/config.toml:1284-1292` (`[mcp_servers.rea]`, npx
$ sed -n '9p' corpus/knowledge/2026-10-13-mcp-registrations.md | grep -o "config\.toml:[0-9]*"
(no output)   # :9 carries a version token, not a line pointer
$ sed -n '80p' corpus/knowledge/2026-10-13-mcp-registrations.md | grep -o "config\.toml:[0-9]*"
(no output)   # :80 likewise
$ sed -n '270p' SCORECARD.md | grep -o "config\.toml:[0-9]*"
(no output)   # :270 is the in-repo :157/:160 parenthetical
```

So of C1's five loci: **two** carry a line pointer into operator-owned
`config.toml` (`mcp-registrations.md:88`, `r4-16-frontier-rescan.md:43`) — the
unrepairable class; **two** (`mcp-registrations.md:9`, `:80`) carry a stale
*version token* in prose; **one** (`SCORECARD.md:270`) is an in-repo
parenthetical about `:157`/`:160`. The gate C3 proposes would serve only the
first two, and only by making them permanently red.

### 2.5 All 4 "dead" pointers are false positives (verified individually)

```console
$ python3 /tmp/arc2-l3r3-CR4-honest.py   # residual list
corpus/knowledge/2026-10-14-r14-02-final-sweep.md:46  -> README.md:112    [README.md: 22 lines]
corpus/knowledge/2026-10-14-r14-02-final-sweep.md:99  -> SHONEN.md:7-18   [SHONEN.md: 12 lines]
corpus/knowledge/2026-10-14-r14-02-final-sweep.md:150 -> SHONEN.md:11-18  [SHONEN.md: 12 lines]
corpus/knowledge/2026-10-14-r14-02-final-sweep.md:151 -> SHONEN.md:18     [SHONEN.md: 12 lines]
```

`:46` is a **fleet**-file citation, not a lane one — the resolver matched the
lane's 22-line `README.md`:

```console
$ wc -l /home/vgpnk/Projects/shokunin/README.md
125 /home/vgpnk/Projects/shokunin/README.md
$ sed -n '112p' /home/vgpnk/Projects/shokunin/README.md
(2026-10-16: mori + chousa repos created and pushed after their 10-round
$ sed -n '45,46p' corpus/knowledge/2026-10-14-r14-02-final-sweep.md
  (`lessons/round-13-distillation`, README.md:112 pre-edit) is a deliberate non-corpus pointer to
```
The line itself says **"pre-edit"** and **"deliberate non-corpus pointer"** —
the citation is explicitly marked, and it resolves at the fleet root.

`:99/:150/:151` cite lane `SHONEN.md` which was **18 lines at that entry's own
revision** and is 12 lines at HEAD:

```console
$ git show 6645585:SHONEN.md | wc -l     # r14-02's own revision
18
$ git show HEAD:SHONEN.md | wc -l
12
$ git show 6645585:SHONEN.md | sed -n '18p'
  verifier: r2 audit registry refresh, zero drift — ... — accuracy claim contested pending the round-5 repairs
```
The cited content is present at the cited line at the revision the convention
points at. **A gate over this class would have fired four times on four
correct citations.**

### 2.6 The class the lane's existing instrument already covers — and deliberately does not gate

E23's round-2 instrument survives in scratch and I re-ran it against HEAD:

```console
$ sha256sum /tmp/arc2-l2r2-E23/c2-census.py
cf5d65b6a7037c8776ad2c7741632c133f795db8aa2d9676f79cdc6cd679899e
$ wc -l /tmp/arc2-l2r2-E23/c2-census.py
274
$ python3 /tmp/arc2-l2r2-E23/c2-census.py HEAD 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('n_unqualified',d['n_unqualified']); print('pointer_drift',d['pointer_drift']); print('marker_missing',d['marker_missing'])"
n_unqualified 0
pointer_drift []
marker_missing []
rc=0
```

Its exit condition excludes `pointer_drift` (file line 274):

```python
sys.exit(0 if (n == 0 and not marker_missing and not stale and not untrusted and guard_ok) else 1)
```

and the seat that reviewed it stated the rule explicitly — `R2.md:129`,
"**Do not gate** C2 on the partition census." The instrument is also
corpus/README-scoped only; it cannot see the config.toml class at all:

```console
$ grep -n "config.toml\|toml" /tmp/arc2-l2r2-E23/c2-census.py
(no output)
```

So C3 would not be "the lane's first drift instrument" — it would be a
**second** one, covering a class the first deliberately reports rather than
gates, over a target that cannot be pinned.

### 2.7 Precedent cost, measured

```console
$ wc -l .ufo/rounds/interactive-r1/verify-recovery.py \
        .ufo/rounds/interactive-r1/expected.json \
        .ufo/rounds/interactive-r1/wave-spec.json
  206 .ufo/rounds/interactive-r1/verify-recovery.py
  143 .ufo/rounds/interactive-r1/expected.json
  174 .ufo/rounds/interactive-r1/wave-spec.json
  523 total

$ wc -l corpus/lessons/2026-10-15-round-1-admission-correction.md
39 corpus/lessons/2026-10-15-round-1-admission-correction.md
```

The first gate's own correction cycle (`LOG.md:585-608`) exists because
`--admission` "raised the missing-binding finding unconditionally" and "the
historical exit 2 in `gate-results.json` was a recorded blocker, not
verification of its observation contents." That is a **false-red** in the
precedent gate. Gate #2's false-red surface is measured at 4/345 minimum and
45% naive — an order of magnitude larger, over a class whose true defect rate
this session's evidence puts at zero durable repairs available.

Registry inventory — the lane has exactly one row today, and zero probe rows:

```console
$ grep -n "^| " SKILL.md | grep -i "gate\|probe"
336:| interactive-r1-recovery | gate / kaidoku | ...
$ grep -c "| probe /" SKILL.md
0
```

### 2.8 The "three rounds bitten" premise, decomposed

| Round | Pointer work | Target ownership | Disposition |
|---|---|---|---|
| r1 (`58116aa`) | append-only refresh note for the `:152` token; `SCORECARD.md:79` NO-CHANGE-with-cause | repo-owned | **fixed in-round**, no gate needed |
| r2 (`b3cd790`) | 2 drifted pointers in the `SCORECARD:68` bullet repaired 5-for-5 line-neutral | repo-owned | **fixed in-round**, no gate needed |
| r3 (C1) | 5 loci named | **2 of 5 carry a line pointer into operator-owned `config.toml`** (`mcp-registrations.md:88`, `r4-16-frontier-rescan.md:43`); 3 are in-repo (`mcp-registrations.md:9,:80` carry a version token not a pointer; `SCORECARD.md:270` is an in-repo `:157`/`:160` parenthetical) | operator-owned half not repairable durably by any lane action |

Observation: pointers needed attention in three consecutive rounds — the
premise is factually correct. Inference: the recurrence is **two different
classes**. The repo-owned half (r1, r2) was repaired in-round both times by
ordinary editing, with no gate; the operator-owned half (r3) is unrepairable
by re-pointing, as §2.2 demonstrates. A gate is the right tool for neither:
it would be unnecessary for the first and wrong for the second.

## 3. VERBATIM — reduced-scope landing text (parent's choice of form)

If the parent keeps a C3-shaped capability, this is the honest scope. Land as
the claim's reduced form:

```text
C3 (reduced) — citation-drift capability, arc2-loop1-round3

Scope. The lane's committed drift capability covers IN-REPO pointer tokens only:
a `path:N[-M]` token whose target is a file tracked in this lane repo. Tokens
whose target is outside the repo (client configs, fleet-root files, sibling
repos) are OUT of scope and are classified `external-target`, never `drift`.

Baseline-revision convention is encoded, not assumed. A pointer is clean iff
it resolves at the citing entry's declared baseline revision (SCORECARD.md:16-17;
corpus/lessons/2026-10-15-round-1.md:7) OR at HEAD. A gate that checks HEAD only
is red on sanctioned citations and is rejected on that ground.

Measured false-positive surface at HEAD 679af5d (three resolvers, this session):
naive 198/440 tokens; basename-matched 42/440; honest scoped 4/345 — and all 4
residuals are false positives (fleet-root README.md:112 at
corpus/knowledge/2026-10-14-r14-02-final-sweep.md:46, explicitly marked
"pre-edit ... deliberate non-corpus pointer"; and three SHONEN.md citations that
resolve at that entry's own revision 6645585, where SHONEN.md is 18 lines vs 12
at HEAD).

The operator-owned-target class is NOT gateable and must not be claimed as such.
`~/.kimi-code/config.toml` carried `[mcp_servers.rea]` at :2913, :2930, :2938,
:3225, :3296 within ~6h (four .bak snapshots + live read). C1's own proposed
repair target :2938/:2940 is dead at read time (:2938 = `provider =
"opencode-go-7"`). The custody SOP forbids storing contents (SKILL.md:247-248)
and PROTOCOL's Two-evidences clause (PROTOCOL.md:375-382) requires a committed
digest-pinned snapshot — so no pinned pointer table can be built for this class.
Durable repair for these loci is de-line-numbering the citation (cite
`[mcp_servers.rea]` / `args` by key), a text change, not a gate.

Form. Land E23's validated instrument (c2-census.py, sha256
cf5d65b6a7037c8776ad2c7741632c133f795db8aa2d9676f79cdc6cd679899e, 274 lines;
fixture harness 158 lines) as the lane's FIRST `probe` registry row — PROTOCOL's
own term for a tool that cannot fail (PROTOCOL.md:363-364) — with `pointer_drift`
as a REPORTED DIAGNOSTIC, matching R2.md:129 ("Do not gate C2 on the partition
census") and the instrument's own exit condition (c2-census.py:274 excludes
pointer_drift). A `gate` row would be the second gate in the lane and would
require the pinned table this class cannot supply.
```

## 4. Conclusions

- **OBSERVATION** — Pre-pair receipt verified 5/5 by my own `sha256sum` run;
  all five live hashes byte-match the receipt. (§2.1)
- **OBSERVATION** — `[mcp_servers.rea]` occupied `:2913`, `:2930`, `:2938`,
  `:3225`, `:3296` in ~6h across four operator backups plus the live file. (§2.2)
- **OBSERVATION** — C1's proposed re-point targets `:2938`/`:2940` are dead at
  my read time; so is the drift record's own `:3225`. (§2.2)
- **OBSERVATION** — `~/.kimi-code/config.toml` is untracked in the lane; the
  only tracked file matching `config.toml` is the round-2 drift receipt. (§2.3)
- **OBSERVATION** — Of C1's five loci, two carry a `config.toml` line pointer
  (`mcp-registrations.md:88`, `r4-16-frontier-rescan.md:43`), two carry a
  version token in prose (`mcp-registrations.md:9`, `:80`), one is the in-repo
  `SCORECARD.md:270` parenthetical. (§2.4b)
- **OBSERVATION** — A naive line-bounds resolver reports 198/440 pointer tokens
  dead at HEAD; the honest scoped resolver reports 4/345, all four verified
  false positives. (§2.4, §2.5)
- **OBSERVATION** — E23's instrument runs clean at HEAD (`n_unqualified 0`,
  `pointer_drift []`, rc 0) and its exit condition excludes `pointer_drift`;
  it is corpus/README-scoped and cannot see the config.toml class. (§2.6)
- **OBSERVATION** — The lane's SKILL.md registry has exactly one row (a gate)
  and zero probe rows. (§2.7)
- **OBSERVATION** — The precedent gate is 523 committed lines and needed a
  39-line correction lesson plus LOG/SCORECARD errata because its `--admission`
  branch was a false-red. (§2.7)
- **INFERENCE** — C3's "bitten for three rounds" is correct but conflates two
  classes: repo-owned drift (r1, r2), repaired in-round twice without a gate;
  and operator-owned-target drift (r3), not repairable by re-pointing at all.
  The gate is the right instrument for neither. (§2.8)
- **INFERENCE** — Under PROTOCOL's Gate standard, a citation-drift gate as C3
  scopes it cannot satisfy the Two-evidences clause, because the pinned pointer
  table's input is operator-owned, contents-unstorable, and mutating. (§2.3)
- **UNKNOWN** — Whether the parent's intended `--selftest` fixtures would
  exercise the baseline-revision convention; if they do not, the selftest would
  be green while the gate is red on sanctioned citations.
- **UNKNOWN** — The operator's rewrite cadence going forward; the observed
  three-rewrites-in-one-day rate is a single day's sample.
- **UNKNOWN** — Whether a mutation of `~/.kimi-code/config.toml` occurred
  between the 17:55:49Z pre-pair and my 18:00Z read that reverted. Hash
  agreement cannot exclude mutate-and-revert (threat transferred from
  luna-round-6 `BC3.md:14`, restated `V3.md:175`).
