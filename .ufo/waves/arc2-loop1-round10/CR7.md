# CR7 (critic) — attack on verdict inflation and smuggled claims

Seat CR7, wave `arc2-loop1-round10`, 2026-10-18/19. HEAD at every sample
`c561f00d9000f5da13719673c6f2c2f79a572d0a`. Read-only throughout the repo and the
host; this file is my only write. No scratch files were needed (every datum below
is a direct read of a sealed artifact or a `systemctl show` property); no git
mutation, no config edit, no install, no network, no signal to either leg.

## 1. Verdict

**The round's central closure is real but smaller than the wave's prose claims it
is, and three sentences that are queued to land are inflated or dangling.**
Six attacks, ordered by blast radius:

- **A1 — "keying confirmed" is a smuggled inference.** The rerun varied *nothing*
  in the id's alleged domain (content, `subject.local_path`, operation, params, and
  the analysis-profile digest `eb30f27a…` are identical at
  `.ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json:61` and
  `/var/tmp/arc2-l10r10-big/stdout.json:61`). An equality under a fully fixed
  request is a *reproducibility* observation; it cannot discriminate
  content+params keying from content-only, path-inclusive, or result-derived
  keying. The defensible sentence is "consistent with `QUALITY.md:25`", not
  "confirmed". `CR8.md:246`, `E14.md:12,34,369`, `E15.md:283-284`, `C3.md:232`
  and `E23.md:291` all state the strong form.
- **A2 — C1's dichotomy is false; the third branch already occurred.** C1 names
  two terminal outcomes (ids equal / different) and one in-flight disposition.
  The wave produced a third: `arc2-r10-big` sealed **equal** (byte-identical) and
  `arc2-r10-mid` produced **no id at all**. So "the r7/r6 entries' last named
  unknown closes either way" is false for the r6 entry in *both* named branches.
  Corroborated in-wave by `E4.md:28`, `E5.md:40`, `E6.md:13`, `E23.md:29`,
  `R1.md:25`.
- **A3 — "two scale points" is unrealized.** Only one point sealed. `P2.md:41`'s
  disposition row closes **both** entries' unknowns on an "equal" outcome;
  `E14.md:369` and `E15.md:260` carry the phrase forward.
- **A4 — "the r6 mid-rung recipe" is recipe infidelity.** r6's leg had **no cgroup
  cap** (bare `timeout -k 60 5400 node …`, `/var/tmp/arc2-l6r6-E9-mid/run-leg.sh`);
  the r10 leg added `MemoryMax=9663676416` + `MemorySwapMax=1073741824`. The
  wave's "18.26 GiB footprint" is a sum of per-process `VmRSS` (double counts
  shared pages), an *upper bound* on memcg charge, not the charge.
- **A5 — "OOM-killed at its 9G cap" is smuggled precision.** `MemoryPeak ==
  MemoryMax == 9,663,676,416` **and** `MemorySwapPeak == MemorySwapMax ==
  1,073,741,824`: both maxima saturated. The unit cgroup is gone, so
  `memory.events` — the only artifact that names the firing limit — is
  unreadable. Which limit fired is **UNKNOWN**.
- **A6 — liveness and extension claims asserted from artifact shapes.**
  `V5.md:92,115` reports the mid leg "growing"/"running" 1m45s after it was
  `failed (Result: oom-kill)`. C2's pointer-table extension has **no landed
  artifact** (table mtime `20:31:48 -0300`, 13 entries, none naming r7/r8/SHONEN;
  `C2.md` absent at my close).

**Not a finding (checked, clean):** custody pre-pair 5/5; the big leg's
byte-identity; the profile-digest reproduction; the command-A baseline's
re-measurement; the fleet's catch of the artifact's own `failure_message`
mislabel. Details in §2.7.

## 2. Evidence

### 2.1 A1 — the id domain was not varied (attack on "confirmed")

The two runs are pinned on every field the id claim names:

```console
$ grep -n "digest: eb30f27a" .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json /var/tmp/arc2-l10r10-big/stdout.json
.ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json:61:      digest: eb30f27ae6ba46f81482f9ffb6e049db505f4edff9ec0ad8c6af4684cb0ad302
/var/tmp/arc2-l10r10-big/stdout.json:61:      digest: eb30f27ae6ba46f81482f9ffb6e049db505f4edff9ec0ad8c6af4684cb0ad302
$ head -12 /var/tmp/arc2-l10r10-big/stdout.json
evidence_id: ev_a4aa9b0d81b0a9e9cd93a5a93399a32fa1aa4abe2076bbf41c69ca6246cde608
subject:
  name: windows_release_arm64.exe
  digest:
    sha256: 7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292
  local_path: /home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/windows_release_arm64.exe
```

Identical content, identical `subject.local_path`, identical operation, identical
params, identical derived profile digest — and an identical id. That is exactly
what "the id is a function of the request" predicts, and it is also what
content-only or path-inclusive keying predicts. No hypothesis is excluded because
no factor was varied; `corpus/QUALITY.md:25` (rule 15) already carries the domain
with its own provenance (r9-02 refuted the rule-#14 universal). The strong form in
the wave:

- `CR8.md:246` — "content+params keying is confirmed, not merely asserted."
  (CR8 is a fellow critic; this is a critic-on-critic disagreement.)
- `E15.md:283-284` (landable LOG block) — "`analyze` ids are content+params-keyed
  and reproduce across a rerun, envelope-inclusive".
- `E14.md:12,34,369` — "content+params-keying is confirmed at the 91.6MB scale point".
- `C3.md:232` — "The id-keying claim both knowledge entries rest on resolves".
- `E23.md:291` — "analyze ids AND the whole evidence envelope are content+params-keyed
  at this scale point".

Two sub-claims inside A1 that are separately wrong:

1. **"The envelope carries no per-run field"** (`E23.md:291` region) is false as a
   general statement about `analyze` envelopes. The *failure* envelope carries
   `run_id: c6b1b41b-f0bf-47ce-ba1c-4f1706396e48`, `runtime_root`, `process_id` and
   `profile_digest: 59e0d37bce87c1b8ccb70c6062be2383648a35642f5a6c85b1db0939164d5e55`
   (`/var/tmp/arc2-l10r10-mid/stdout.json`, head). Only the *result* envelope is
   run-field-free. The sentence must be scoped to the result envelope.
2. **"Two runs … differed in TMPDIR, wall time and swap peak, so the id is
   invariant under those"** (`E4.md` §3a) is sound as an invariance statement but is
   *not* evidence for the keying domain: TMPDIR, wall time and swap peak are not
   candidates for id inputs in any hypothesis on the table, so their variation
   discriminates nothing.

### 2.2 A2/A3 — what actually happened, from the sealed artifacts

```console
$ systemctl --user show arc2-r10-big -p Result -p ExecMainStatus
Result=success
ExecMainStatus=0
$ journalctl --user -u arc2-r10-big --no-pager | tail -1
Oct 18 21:20:23 … arc2-r10-big.service: Consumed 42min 43.809s CPU time over 23min 58.082s wall clock time, 7.8G memory peak, 769.1M memory swap peak.
$ sha256sum /var/tmp/arc2-l10r10-big/stdout.json
a77ebee8794fb5951cc5bc79f46000e1fdd29c3ed09542d30c791a89941c218a  /var/tmp/arc2-l10r10-big/stdout.json
$ diff /var/tmp/arc2-l10r10-big/stdout.json .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json && echo BYTE-IDENTICAL
BYTE-IDENTICAL
$ systemctl --user show arc2-r10-mid -p Result
Result=oom-kill
$ grep -c 'ev_' /var/tmp/arc2-l10r10-mid/stdout.json
0
$ head -c 120 /var/tmp/arc2-l10r10-mid/stdout.json
error: Analysis failed
code: cancelled
category: cancelled
$ sha256sum /var/tmp/arc2-l10r10-mid/stdout.json
56e87061869d8928c84a4c0926c5cd5e17c1ce56a0c0166f48ddafa9e4bb0981  /var/tmp/arc2-l10r10-mid/stdout.json   # 315462 B
```

So the realized outcome is **one equal, one absent** — a branch C1's text does not
enumerate, and the only branch on which *neither* entry's unknown closes for the
mid leg. `P2.md:41`'s row ("equal → content+params-keying confirmed at two scale
points … r6 `:7,:21` and r7 `:7,:37` named unknowns **close**") therefore cannot be
copied to the round section; its condition is unmet, not satisfied.

### 2.3 A4 — recipe infidelity (the r6 leg carried no cap)

```console
$ sed -n '/timeout -k/,+2p' /var/tmp/arc2-l6r6-E9-mid/run-leg.sh
/usr/bin/timeout -k 60 5400 \
  node "$REA_JS" analyze "$BIN" --format json \
  > "$SCRATCH/stdout.json" 2> "$SCRATCH/stderr.log"
$ grep -n "peak_tree_rss_kb\|wall_s" .ufo/waves/arc2-loop1-round6/receipts/mid-rung-meta.txt
12:peak_tree_rss_kb=19149984
14:wall_s=2479
$ systemctl --user show arc2-r10-mid -p MemoryMax -p MemorySwapMax
MemoryMax=9663676416
MemorySwapMax=1073741824
```

The r6 leg ran as a plain shell child under `timeout(1)` — no `systemd-run`, no
`MemoryMax`, no `MemorySwapMax`. `peak_tree_rss_kb=19149984` is the sampler's sum
of per-process `VmRSS` (`run-leg.sh` loops `pgrep -P` over the tree and adds each
`VmRSS`), so shared pages are counted once per process: 18.26 GiB is an **upper
bound on memcg charge, not the charge**. Seats that write "its own uncapped
footprint is ~2x the cap" (`P2.md:44`, `C3.md` §2.2, `E15.md` landable block) state
an upper bound as a measured charge. The decisive, cap-free fact is the absence of
a cap, which `E4.md` F2 (`:30`) and `E5.md` §1.2 state correctly.

### 2.4 A5 — both limits saturated; the firing limit is unestablished

```console
$ systemctl --user show arc2-r10-mid -p MemoryPeak -p MemoryMax -p MemorySwapPeak -p MemorySwapMax
MemoryPeak=9663676416        MemoryMax=9663676416
MemorySwapPeak=1073741824    MemorySwapMax=1073741824
$ cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/arc2-r10-mid.service/memory.events
cat: …/arc2-r10-mid.service/memory.events: No such file or directory
```

The journal reports "9G memory peak, 1G memory swap peak" and nothing more. With
`MemorySwapMax` saturated too, a swap-limit OOM is an unexcluded rival cause. The
honest form is "killed at the unit's cap pair (9G mem + 1G swap), both maxima
saturated; which limit fired is UNKNOWN (unit cgroup gone, `memory.events`
unreadable)".

### 2.5 A6 — V5's liveness claim, and C2's unlanded extension

```console
$ sed -n '92p;115p' .ufo/waves/arc2-loop1-round10/V5.md
… `/var/tmp/arc2-l10r10-mid/stdout.json` growing (315462 bytes). No signal sent.
… both live legs are running.
$ stat -c '%n mtime=%y' /var/tmp/arc2-l10r10-mid/stdout.json ; systemctl --user show arc2-r10-mid -p Result -p StateChangeTimestamp
/var/tmp/arc2-l10r10-mid/stdout.json mtime=2026-10-18 20:57:04 -0300
Result=oom-kill
```

V5's report mtime is 20:59; the mid unit died 20:57:18 and its 315,462-byte
`stdout.json` was the **complete** failure envelope (mtime 20:57:04), not a growing
result. `E9.md:174-180` sampled the same unit and recorded `failed` correctly — the
inflation is local to V5.

```console
$ stat -c '%n mtime=%y' .ufo/gates/citation-drift/pointer-table.json
.ufo/gates/citation-drift/pointer-table.json mtime=2026-10-18 20:31:48 -0300
$ ls .ufo/waves/arc2-loop1-round10/*.md | xargs -n1 basename | tr '\n' ' '
C3.md CR2.md CR6.md E14.md … V6.md          # no C1.md, no C2.md
```

All 13 table ids enumerated (`.ufo/gates/citation-drift/pointer-table.json:entries`):
`sc59-stanza-key-anchor, sc59-receipt-stamp, prov18-stamp-named, prov18-receipt-exists,
prov18-pin-value, sc68-discharge-record, sc69-readme-177, sc72-readme-nitrow,
sc270-dated-record, sc698-sc2-refuted-record, mcpreg-errata-anchor-form,
r416-errata-durable-anchor, skill-registry-row`. None names
`2026-10-18-arc2-r7-pe-wall.md`, the r6 mid-rung entry, the r8 erratum, or
`SHONEN.md`. The table is unchanged since round 9, and `C2.md` has not landed, so
C2's "the citation-drift probe table extends to the r7/r8 citations + SHONEN
pointers" has no artifact at my close. `E21.md:16-17` measured the table **as-is**
(findings=0, strict 0, selftest 11/11) — evidence about the table, not the extension.

**C2 design point for the extension's author.** `SHONEN.md:6` asserts a bare
line-range, `SKILL.md:81-243`, into a 371-line mutable file — the class the probe
exists to report. The table's `exempt` list (`:144`) exempts bare `config.toml:N`
live pointers; whether a bare `SKILL.md:81-243` becomes a pinned `anchor` entry or
an exemption is undecided. An undecided case is how the gate passes while the
class persists; the extension must state which it is.

### 2.6 A1/A2 consequence for the landable text — a dangling path and mixed pointers

`E4.md` §3a (the id-EQUAL erratum destined for
`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`, **37 lines**) cites
`(:81-83: 9 segments / 75218 procedures / 137345 strings)` and `(the profile digest
(:61))`. Those are line numbers into the **receipt** (90 lines; the
`segments[9]{…}` block begins at `:71`), not into the file being edited, and the
erratum names no file for them — a bare line number into an unidentified file,
i.e. the drift class (`SKILL.md` rule #11 asks for the content-anchor form).
`E23.md`'s B1 block cites the receipt by path and carries no line numbers — the
cleaner form. The same §3a cites
`.ufo/waves/arc2-loop1-round10/receipts/r10-big-envelope.json`, which **does not
exist**: at my close the round-10 receipts directory holds only
`config-pre-pair.txt` and `roster-frozen.txt`. `E5.md:170-175`'s land procedure
already requires committing the receipt first; the erratum must not land before it.

**E5's id-DIFFERENT draft is untriggerable and must be recorded as such.**
`E5.md:181` titles its §3a "the second run re-derived a DIFFERENT evidence id — the
rerun id-stability unknown resolves by mapping its boundary"; `E5.md:19-21` labels
it "DRAFT READY — CONDITIONALLY TRIGGERED … NOT triggered". The measured outcome is
the opposite branch (byte-identical, same id), so the draft is dead — but its title
is the most quotable string in the wave and a scribe could land it by headline.
One internal defect worth recording even as a dead draft: `E5.md:200-207` lists
"the **path** (`subject.local_path`, the same string in both)" among four pinned,
excluded inputs and then names "(a) the scratch/session path, which did differ" as
a live candidate — "path" is used for two different fields, so "path is excluded"
is not established. (The draft's profile-digest pin *is* correct: verified in §2.1.)

### 2.7 Checked and clean (no finding — recorded so the clean surface is visible)

```console
$ tail -n +2 .ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt | sha256sum -c - | grep -c OK
5
$ sha256sum .ufo/waves/arc2-loop1-round7/receipts/r7-pe-envelope.json
a77ebee8794fb5951cc5bc79f46000e1fdd29d30… # see §2.2: equals the r10 output
```

- **Custody 5/5** byte-identical by my own re-derivation (no drift at my samples).
- **The r7 entry's cheap check is now a reproduction check**: the committed receipt
  sha256 equals the fresh output sha256, and `evidence_id` equals `ev_a4aa9b0d…`.
  This part of the wave's claim is not inflated — it is understated: the **derived
  profile digest reproduces too** (`eb30f27a…` at both `:61`), which no seat I read
  cites.
- **The artifact's own mislabel is caught by the fleet.** The mid envelope says
  `failure_message: Ghidra startup was cancelled`, yet its body carries 2,384
  `DecompileCallback` lines — the r4 mislabel class. `C3.md:53-58` and `E15.md`
  name the journal as the diagnosis and the wrapper string as the mislabel. Correct;
  my A5 only adds that "9G cap" is not yet the whole diagnosis either.
- **Baseline numbers are re-derived, not restated.** `E21.md` measures command A at
  HEAD (`81/81, 13/13, 10.0/10.0`, `missing=[]`, `dangling=[]`), the probe selftest
  at 11/11 (matching the 11 cases in
  `.ufo/gates/citation-drift/expected.json:selftest`), and the frozen run's `failed`
  verdict under `--strict`; `E8.md:17` re-derives it with `expected.json` unedited.
  One provenance note for the closeout: the brief's "13/13" is SHONEN rule blocks
  and the probe's selftest is 11/11 — two denominators that the phrase "selftest +
  frozen-run re-verified" can conflate.

## 3. Verbatim-landable text

Pre-landing corrections for the parent. This block is advisory text for the
round's records; it asserts nothing this seat did not observe.

```text
CR7 pre-landing corrections (arc2-loop1-round10; apply before landing C1's erratum,
the LOG entry, and the SCORECARD round section):

1. REPLACE every "content+params-keying confirmed" with "consistent with
   content+params keying (QUALITY.md:25, rule #15)" and add the one-line scope:
   "the rerun held content, subject.local_path, operation, params and the
   upstream analysis-profile digest (eb30f27a…) fixed, so this is a
   reproducibility result; no rival keying hypothesis is excluded." Affected:
   CR8.md:246, E14.md:12,34,369, E15.md:283-284, C3.md:232, E23.md:291.
2. DELETE the phrase "at two scale points" from any landed sentence (E15.md:260,
   E14.md:369, P2.md:41). One scale point sealed; the other produced no id.
3. STATE the realized branch explicitly: "arc2-r10-big sealed EQUAL (byte-identical,
   ev_a4aa9b0d… re-derived); arc2-r10-mid produced NO evidence_id (typed
   cancelled, OOM-killed). The r7 entry's id-stability unknown closes for the
   mitigated (+disabled) recipe at 91.6MB; the r6 entry's stays OPEN as named debt."
   Do not write that both entries' unknowns close, on either branch.
4. SCOPE the cap narrative: r6's leg carried NO memcg cap (run-leg.sh: bare
   timeout(1)); its 18.26 GiB figure is a sum of per-process VmRSS (upper bound on
   charge). The r10 leg was killed at its cap PAIR (MemoryPeak == MemoryMax ==
   9663676416 B and MemorySwapPeak == MemorySwapMax == 1073741824 B); which limit
   fired is UNKNOWN (unit cgroup gone, memory.events unreadable).
5. DO NOT LAND E5 §3a (id-DIFFERENT). Record instead: "E5 §3a NOT TRIGGERED — the
   id-EQUAL branch was realized; the draft is retained as a dead branch."
6. LAND ORDER: commit .ufo/waves/arc2-loop1-round10/receipts/r10-big-envelope.json
   (the sealed /var/tmp/arc2-l10r10-big/stdout.json, sha256 a77ebee8…) BEFORE the
   erratum that cites it — that path does not exist yet. In the erratum, replace
   the receipt line numbers (:61, :81-83) with content anchors or the full receipt
   path; the knowledge file it edits is 37 lines long.
7. C2: the pointer-table extension has no artifact at CR7's close (table mtime
   2026-10-18 20:31:48 -0300, 13 entries, none naming r7/r8/SHONEN; C2.md not
   landed). Either land it and cite the new table's hash, or record it as open.
   When it lands, decide explicitly whether SHONEN.md:6's bare `SKILL.md:81-243`
   is a pinned anchor entry or an exemption — an undecided case passes the gate
   silently.
8. V5.md:92,115 ("stdout.json growing", "both live legs are running") is stale by
   1m45s; E9.md:174-180 has the correct read (arc2-r10-mid failed). Correct V5 or
   note the supersession so the wave record does not carry two contradictory
   liveness reads.
```

## 4. Labels

**Observation** — big leg: `Result=success`, exit 0, 23min 58.082s wall, 42min
43.809s CPU, 7.8G peak / 769.1M swap peak, `stdout.json` 5204 B sha256 `a77ebee8…`
byte-identical to the committed r7 receipt, `evidence_id ev_a4aa9b0d…`; profile
digest `eb30f27a…` at `r7-pe-envelope.json:61` and `stdout.json:61`. Mid leg:
`Result=oom-kill`, `MemoryPeak == MemoryMax == 9663676416`,
`MemorySwapPeak == MemorySwapMax == 1073741824`, `stdout.json` 315,462 B sha256
`56e87061…`, zero `ev_` occurrences, head `code: cancelled`. r6 leg: no cgroup cap
in `run-leg.sh`; `mid-rung-meta.txt:12` `peak_tree_rss_kb=19149984`. Custody 5/5.
Pointer table: mtime `2026-10-18 20:31:48 -0300`, 13 entries, none r7/r8/SHONEN.
`C1.md`/`C2.md` absent from the wave dir at my close. Round-10 `receipts/` holds
two files.

**Inference** — (i) the realized outcome is a third branch of C1's disposition,
not one of the two it names; (ii) the id equality is a reproducibility result that
cannot confirm the keying domain because no domain factor was varied; (iii) the
mid leg's death is a dispatch-recipe deviation (an added cap pair), not a datum
about id keying and not a counter-observation to r6's hold; (iv) V5 sampled an
artifact size and inferred growth without reading unit state; (v) `E4.md` §3a's
`r10-big-envelope.json` citation will dangle until the receipt is committed.

**Unknown** — (a) which limit (9G memory or 1G swap) the kernel OOM killer fired
on, and whether the mid leg would seal inside an uncapped or larger-capped
envelope (P2's rerun plan is untested); (b) whether the 18.26 GiB aggregate-RSS
figure exceeds the memcg charge it is used to stand for (the metric double counts
shared pages, so the "~2x the cap" ratio is an upper bound); (c) whether C2's
extension lands before the wave closes, and its resulting table hash; (d) whether
the concurrency of the two legs (both started 20:56:25, `app.slice` peak reported
by `C3.md:25-28` at 28.2 GiB) perturbed the mid leg's charge — not decidable from
the surviving artifacts; (e) the intra-instruction-level identity of the two big-leg
analyses (byte-equality of the sealed output does not assert that).
