# RevCounterEscape: attacks on the v1 C1 counter and the planned v2 design

Seat: RevCounterEscape (reviewer, r52-w1). Read-only on the lane. Base `c525de54a53eb3c4fee28ede2721da4527cf8ece`,
claims draft `ab0eafedc41402b43b41a4362084119578dfe7ce`. Counter read: `tools/round-50/c1-counter.py`
(4836 lines, read at base). Probe receipts: `receipts/probe-escapes.sh`, `receipts/probe-escapes.out`,
`receipts/history-grep.out`. Line numbers below are `tools/round-50/c1-counter.py` unless stated.
Probed = run here on the host. [INFERENCE] = read from code or standard semantics, not run.

## Verdict

v1 is closed against two of the four classes named in the task: a rule or receipt substituted in the
working tree (every content read is `git show` at FREEZE or REV, 2174/2214/2302) and a receipt-shaped
file planted in a receipts directory (v1 has no such directory input). v1 is open on everything the
independent-rerun and evidence-id clauses trust: the execution environment (PATH, inherited env,
`--unblob`, `--pkg65`), the git object view (`refs/replace`), and the freeze anchor (`--freeze`, `--root`).
Several planned v2 additions (`--gap-rule`, `--receipts`, `--provenance-base`, `--receipt-fresh-base`,
ENOENT retry, prior-pin waiver) reopen escapes unless the MUST list in section 4 lands. As drafted,
the v2 design cannot refuse a forged green. Four escapes below were probed; the rest are code-derived.

## 1. The four questions

**(1) Caller inputs: forged receipts dir + rule file on the controls mode.**
- v1 blocks the simple form. The rule is read from git at FREEZE (2174, 2177-2180, 2214) and no
  rule-path flag exists. Receipts are read from git at REV (2302). A forged directory has no effect.
- The planned v2 flags reopen it. Claims lines 89-90 put `--receipts corpus/evidence/round-52/c1` in
  the predicate command, and the claims (F8/F10 note) add `--gap-rule`, `--receipts`,
  `--provenance-base`, `--receipt-fresh-base`. If any is read from the filesystem, the controls
  (CTL-OLD, CTL-NEW, M1-M4) become forgeable, and `--provenance-base kaidoku-r50/` makes round-50
  receipts pass `run_provenance_ok` (2379), while `--receipt-fresh-base <older commit>` makes them pass
  `receipt_fresh` (2313-2317, currently based on `freeze`). See E7.
- "Receipt digest not bound to git": `receipt_digest` (2310) is the sha256 of bytes returned by
  `git show` and is never compared with the blob id. Because `git show` honours `refs/replace` (probed,
  E6), the digest describes replaced bytes. See E8.
- "Freeze pin stale": yes. `--freeze` is caller-supplied, no expected freeze SHA is compared, and no
  `is_ancestor(freeze, rev)` exists in `measure()`. A later freeze hides any rule edit before it
  (`frozen_drift` walks only `freeze..rev`, 1675-1676). See E5.

**(2) Projection rerun: can a planted receipt satisfy `projection_ok` with no genuine REA run?**
- A planted receipt in the working tree cannot: v1 reads the committed receipt at REV (2302), and the
  rerun output is compared with that committed projection (2406-2412). This is blocked.
- `projection_ok` can be satisfied with no truthful extraction. The "REA run" is
  `node <entry> extract-firmware` where `entry` is the `bin` of the caller's `--pkg65` package
  (1937-1955, 2041). Its child environment is `dict(os.environ)` (2037), so NODE_OPTIONS hooks run inside
  the child (probed, E2). `--unblob` is accepted on version output alone (1977-1982; 2038 sets
  `REA_UNBLOB_COMMAND` to it, E3). Only `package.json` and `package-lock.json` are hashed (643-645, E4).
  So any of these returns `('ok', data)` on demand, and projection equality follows.
- The evidence id is recomputed with the same caller package (686-687). A forged envelope with a
  self-computed id passes `evidence_id_ok` (2424).

**(3) Prior-pins allow-list: can a non-allow-listed stale pin slip through? Exact check.**
- Yes. `prior_pins` (1596-1646) enumerates only: `carriers.json prior_pins` (1609-1615),
  `carriers[].sha256` of exactly two tables `.ufo/waves/round-41/c1/carriers.json` and
  `tools/round-49/carriers.json` (1616-1629), and `pins[]` of three candidate documents (1630-1645).
  Not enumerated at base: `tools/round-44/carriers.json` (v1le `b45925fa…`, v2le `7c62dbe3…`, be pins),
  `corpus/evidence/round-36/c1/carriers.json`, `.ufo/waves/round-38|39|40/c1/carriers.json`
  (round-40 LE L1 `2521ded0…`, L2 `fec0f72d…`), every `corpus/evidence/**/after.json` subject digest, and
  `external.member_sha256` / `external.image_sha256` / `nested.sha256`. A pin scored by any of these is
  "fresh" at 2250: `carrier_fresh_ok = pin is not None and pin not in prior`.
- The four round-50 pins are not in any enumerated table (git grep at base: they occur only from
  round-50 onward), so the enumeration gap does not currently admit them. They are stale by definition
  (scored by round-50 receipts), so the waiver is needed, and it is the place to add a slip. The
  claims text (lines 79-85) says the four pins "are listed in the round-52 carrier table's
  `prior_pins`". If the implementation waives "any pin in `prior_pins`", a stale pin added to that list
  is waived too. See E10.

**(4) Bindings: can a binding pass with a placeholder file (empty entry, right stem)?**
- `entry_present` (2457-2458) passes for an empty file: `ent is not None` and `b''` is not `None`.
- `sourced` (2459-2478) then fails for an empty entry, but a one-line `source: S243 - x` plus a
  SOURCES row edit passes it. The opened date (2475) and `used-by` are self-declared registry text.
- `province_core_row` (2445-2451): one table row under the heading containing `squashfs_v4_le`, the
  marker and the path passes. Nothing checks the entry.
- `frontier_note` (2453-2456): any line in PROVINCE.md with the mark, the stem and an LE token passes,
  anywhere in the file. It does not check that LE `hsqs` left `## Frontier`, which claims line 168 requires.
- `coverage_map_row` (2479-2482): any line beginning `|` containing the stem in `## Coverage map`
  passes, including inside a fenced block or an HTML comment.
- Not a counter escape by itself, but it is the binding layer the L1 is trusting. See E11.

## 2. Escape register

Each entry: attack, what v1 does (file:line), evidence, and the v2 requirement (M-numbers in section 4).

### E1. `git` and `chmod` resolved from the caller's PATH (HIGH)
- Code: `git()` runs `['git', '-C', root, ...]` (461); `chmod` runs by bare name (2123, 2141).
  `show()` (468-470) is the only content reader.
- Attack: a `git` earlier on PATH returns attacker bytes for every `show()`: the rule (2174), carriers
  (2165), receipts (2302), counter identity (2157), PROVINCE/entry/SOURCES (2441-2465). `counter_not_frozen`
  (2160) then passes for any copy the shim says is frozen.
- v1 blocks: nothing. `FIXED_PATH` (409-412) is set only for node, sasquatch and the REA child (2040).
- Evidence: [INFERENCE], standard execvp lookup; not run.
- v2: M-2.

### E2. Environment inherited into node and unsquashfs (HIGH; PROBED)
- Code: `env = dict(os.environ)` for the REA child (2037), with only REA_UNBLOB_COMMAND, TMPDIR and PATH
  overridden. `subprocess.run([node, tpath, ...])` (686-687) and `subprocess.run([UNSQUASHFS, ...])`
  (2117-2118) pass no env, so they inherit everything. `_first_line` (1961) inherits too.
- Probed (receipts/probe-escapes.out): `NODE_OPTIONS=--require hook.js node ...` runs the hook inside
  the child (`HOOK-RAN`). `LD_PRELOAD=hook.so /usr/bin/unsquashfs -version` runs the constructor
  (`LDPRELOAD-RAN`); the control without it does not.
- Consequences: (a) a genuine REA 6.5.0 run can be made to emit a fabricated envelope, so
  `projection_ok` (2403-2412) holds without a truthful extraction; (b) the evidence-id recompute
  (686-687) can be hooked, so `evidence_id_ok` (2424) holds for a self-computed id; (c) unsquashfs can be
  hooked to emit an oracle equal to the receipt's files, so `oracle_rederived_ok` (2280-2288) holds, and
  so would v2's `census_rederived_ok` (the `-lln` listing).
- v1 blocks: nothing.
- v2: M-1.

### E3. Caller-chosen unblob (HIGH)
- Code: `--unblob` (2519) reaches `make_real_runner` as `unblob_path` (2025), and `toolchain_record`
  (1977-1982) accepts it if `unblob --version` prints `26.6.4`. The path is recorded by sha256 but not
  compared with any frozen value. 2038 sets `REA_UNBLOB_COMMAND` to it.
- Attack: a shim that prints `26.6.4` on `--version` and does whatever it likes is the rerun.
- v1 blocks: nothing. The frozen tool pins (`unsquashfs 4.7.5`, `sasquatch 4.5.1`, `unblob 26.6.4`) are
  named in claims and the harness but not hashed in the counter.
- v2: M-3.

### E4. Caller-chosen REA package; code not hashed (HIGH)
- Code: `rea_package_problems` (624-656) hashes two files only, `package.json` and `package-lock.json`
  (643-645), and checks the version. `rea_entry` (1937-1955) takes the `bin` path from that
  `package.json` and runs it. `evidence_ids` (686-687) runs `xpin-attribute.mjs --pkg65 <caller>`, so the
  caller's package supplies `semanticProjection` and the digest.
- Attack: copy the real `package.json` and lock (sha-match) and replace `bin` and lib code. The check
  passes, and the rerun and the evidence-id recompute both run the replacement.
- The claims' "tree_sha256 deliberately absent (no frozen canonical form)" is a reason to omit a tree
  hash. A sorted file list with sha256 each is a definable canonical form.
- v1 blocks: nothing.
- v2: M-4.

### E5. Freeze anchor and root unanchored (HIGH)
- Code: `counter_not_frozen` (2155-2163) checks only that the running counter equals `COUNTER_PATH` at
  the caller's `--freeze`. Drift (2199-2202) walks `freeze..rev` (1675-1676). `measure()` has no
  `is_ancestor(freeze, rev)` and no expected-SHA check. `--root` is any git directory (2514-2516).
- Attack A (stale freeze): pick `--freeze` = a commit after a rule edit. `freeze..rev` does not include the
  edit, so `frozen_path_changed []`, and the edited rule is "frozen". Probe not run; the logic follows from 1675.
- Attack B (forged lane): a fixture repo whose "freeze" commit carries a copy of the counter and a permissive
  rule. The byte-dependent clauses need real carriers and REA, which are available through the pinned
  chain, so only the rule and receipt content are forged. `gaps_ok` then passes.
- v1 blocks: nothing.
- v2: M-5.

### E6. `refs/replace` changes content, not the drift view (HIGH; PROBED)
- Probe (receipts/probe-escapes.out): with `refs/replace/<blob>` set to a forged blob, `git show HEAD:rule.json`
  and `git cat-file -p HEAD:rule.json` return `{"forged":true}`, while `git rev-parse HEAD:rule.json`
  returns the honest blob id, and `--no-replace-objects` restores the honest bytes.
- Consequence: `show()` returns forged content, while `frozen_drift`'s blob-equality check (1713-1722) uses
  `rev-parse` and sees nothing. `receipt_digest` (2310) describes the forged bytes. `grafts` and `shallow`
  files in `.git` are [INFERENCE] the same class (they change ancestry seen by `is_ancestor` and `all_adds`).
- v1 blocks: nothing.
- v2: M-6.

### E7. Caller-supplied round constants as flags (HIGH if the v2 flags land as drafted)
- Code (v2 draft, claims 89-90 and the F8/F10 note): `--gap-rule`, `--receipts`, `--provenance-base`,
  `--receipt-fresh-base`. v1 has none (`main` 2511-2598).
- Attack: each flag that reads the filesystem makes the controls (CTL-OLD 2/4, CTL-NEW 4/4, M1 red, M2
  green) a function of caller input. `--provenance-base` and `--receipt-fresh-base` change the freshness
  and provenance tests for committed receipts. The predicate's `--receipts` adds no protection, because
  freshness is read from git adds, and it adds forgery surface.
- v1 blocks: the flags do not exist.
- v2: M-7.

### E8. Receipt digest and counter identity self-attested (MEDIUM)
- `receipt_identity_ok` (533-554) reads the counter path from the receipt itself (`doc['counter']`, 544)
  and checks that file's sha. Any file whose sha equals the declared digest passes, so `--verify-receipt`
  (2536-2550) certifies nothing about who wrote the receipt.
- `receipt_digest` (2310) and `evidence_digests` (2433-2435) are sha256 of `git show` bytes (E6), never
  compared with a blob id.
- v1 blocks: `counter_not_frozen` (2160) pins the running counter, so this is not a score escape by
  itself. It becomes one if v2 compares `counter_sha256` with the receipt's own path.
- v2: M-8.

### E9. Retry policy as retry-until-green (MEDIUM; design)
- v1 retries only REA's `provider_timeout` (2073-2074, `MAX_REA_ATTEMPTS` 1923) and records attempts
  (2078). The v2 draft (claims 107-114) adds up to 2 retries on an ENOENT `execution_failure` "naming a path
  inside the extraction tree", each on a fresh root.
- Attack: with no terminal rule, a sequence [ENOENT, ENOENT, ok-match] passes. The rule for
  [ok-mismatch, ...] is unspecified. The failing diagnostic is REA output, so E2-E4 can script it.
- v2: M-9.

### E10. Prior-pin enumeration and the waiver (MEDIUM)
- Enumeration gap (see question 3): `prior_pins` 1608-1646 misses tables for rounds 36-40 and 44,
  every receipt subject digest, and the `external.*` and `nested.*` pin fields. Latent for the four pins
  (they are not in those tables), but open to any future carrier table.
- Waiver form: if "waived" is implemented as membership in `prior_pins` (claims 79-85 say the four are
  listed there), the waiver covers any pin placed in that list. The allow-list must be a separate key,
  equal to exactly the four round-50 (id, pin) pairs read from `tools/round-50/carriers.json` at FREEZE.
- Anti-replay for the four: `receipt_fresh` (git adds, post-freeze) accepts a copy of a round-50 receipt
  committed at a round-52 path. What stops it is `run_provenance_ok` (2379, a prefix string) and
  `evidence_id_ok` (2424, forgeable by E4/E2). So the copy plus a rewritten `output_directory` plus a
  forged package passes. The round-52 `after.json` must also not be byte-equal to any round-50 blob.
- v2: M-10.

### E11. Bindings satisfied by placeholders (MEDIUM)
- Table of weak points (question 4): `entry_present` 2457-2458; `sourced` 2459-2478 (self-declared
  opened date, `used-by` text only, no Gate record); `province_core_row` 2445-2451; `frontier_note`
  2453-2456 (anywhere in the file; LE-leaves-Frontier not checked); `coverage_map_row` 2479-2482.
- None of them checks the entry body against the four fresh receipts. `evidence_digests` (2433) already
  computes the digests the entry should cite.
- v2: M-11.

### E12. Frozen-path lists are round-50 names (LOW, latent)
- `FROZEN_PATHS` (413-422) lists `plans/round-50-claims.md` and not the round-52 claims. `FROZEN_PREFIXES`
  (425) is `tools/round-50/`. If v2 keeps these, edits under `tools/round-52/` and to the round-52 claims
  are not drift.
- v2: M-12.

### E13. Harness data-run guard is an env var (LOW; advisory)
- `c1-run.sh` reads `KAIDOKU_C1_DATA_RUN` (125) and gates `after` on it (168-173). Any process can set it.
  It is not a score input, and freshness is git-based, so impact is limited to operator procedure.

### E14. Disposition default for unlisted kinds (LOW)
- `required.get(kind, bool(allowed.get(kind)))` (1552): a kind absent from `required` with empty `allowed`
  is never required. Under the law rule, `fifo`, `socket` and `block-device` are explicit false, so no
  current hole. A future kind in an oracle is only caught by `gap_rule_ok` (2487-2488).
- v2: M-13.

### Not an escape (checked)
- `carrier_cache` (2239-2244): bytes are checked against the pin (2248-2249). Blocked.
- Oracle table forgery without env tricks: the table is re-derived from the carrier bytes (2280-2288), and
  `unsquashfs` is at a fixed path (2104). Blocked, except via E2.
- Working-tree planted receipt (question 2): blocked, git-only reads (2302).

## 3. What was run, what was not

- Probed (receipts/probe-escapes.sh; output in receipts/probe-escapes.out): `refs/replace` against
  `git show`, `cat-file`, `rev-parse` and `--no-replace-objects` (E6); `NODE_OPTIONS` into a node child
  (E2); `LD_PRELOAD` into `/usr/bin/unsquashfs` with a control (E2). Fixture repos and hooks were in
  scratch and removed.
- Not run: the counter, the controls, REA, any `--data-run`, `npx rea-agents`, the REA package. The task
  did not name the REA source, so I did not read it. E4 rests on the counter's own hash list (643-645),
  not on the package's contents.
- Not probed: the PATH `git` shim (E1), the `--unblob` shim (E3), the `--pkg65` replacement (E4), the
  stale-freeze and forged-lane attacks (E5), the prior-pin enumeration miss beyond the table reads (E10).
  Each is marked [INFERENCE].

## 4. v2 MUST list (ordered by severity; each closes a named escape)

- **M-1 (E2): scoring env is a fresh minimal dict.** `env -i`-style: PATH=FIXED_PATH, HOME, TMPDIR, LC_ALL=C.
  Refuse any run with an inherited `NODE_*`, `LD_*`, `GIT_*`, `PYTHON*`, `npm_*`, `REA_*` key other than the
  ones the counter sets. Record the env key names in the receipt. Apply to every subprocess: REA child,
  xpin, unsquashfs, unblob --version, sasquatch -version, node --version, and `chmod`.
- **M-2 (E1): absolute tool paths, pinned.** Resolve `git`, `chmod` and `unsquashfs` to fixed absolute paths.
  Hash the binaries (git, chmod, unsquashfs 4.7.5, sasquatch 4.5.1, unblob 26.6.4, node v24.21.0 as observed)
  in a frozen table and refuse on mismatch. Record the sha256s in `rerun_toolchain`.
- **M-3 (E3): no caller-chosen toolchain in scoring mode.** Drop `--unblob`, `--pkg65` and `--carrier-cache`
  path overrides from the predicate. Scoring uses the frozen pins; any path override is a controls-only
  flag and is recorded as such.
- **M-4 (E4): hash the whole REA package tree.** Freeze in `tools/round-52/rea-pkg.json` a sorted list of
  (relative path, sha256) for every regular file under the pkg65 tree, including any nested dependency
  directory. Compare the set in `rea_package_problems`: extra, missing or changed files are a problem.
  Compute it at freeze, from a clean 6.5.0 install.
- **M-5 (E5): anchor the freeze.** Require `--freeze` to equal an expected SHA recorded outside the
  candidate's history, and assert `is_ancestor(freeze, rev)`. Compare the frozen paths' blob ids at FREEZE
  with a manifest committed in the freeze (sha256 of each frozen file), so a later freeze cannot be
  chosen. Require `git rev-parse --show-toplevel` to equal the lane root. Disclose that a rewritten history
  is out of scope.
- **M-6 (E6): git reads with no replace view.** Every git call carries `--no-replace-objects` (probed as a
  global option). Refuse when `refs/replace/` is non-empty, `.git/info/grafts` exists, or the repository is
  shallow. Compare the bytes read with `git rev-parse REV:path` blob ids (computed without replacement).
  Record the blob ids in the receipt.
- **M-7 (E7): no round constants from the filesystem.** Delete `--gap-rule`, `--receipts`,
  `--provenance-base`, `--receipt-fresh-base` from the scoring predicate. The round-52 constants are
  module constants in the frozen counter. Controls read committed bytes only, via `git show <commit>:path`
  for the round-50 receipts (their own commit, not the working tree). Remove `--receipts` from claims
  lines 89-90.
- **M-8 (E8): identity against the frozen counter.** `receipt_identity_ok` compares the receipt's
  `counter_sha256` with `show(root, freeze, COUNTER_PATH)` read through the M-6 path, not with
  `doc['counter']`. `--verify-receipt` reports that comparison, not a self-declared path.
- **M-9 (E9): retry as a terminal policy.** The first attempt with `ok:true` decides. A projection mismatch is
  never retried. Retry only REA's `provider_timeout`, and ENOENT only when the same path appears in the
  attempt-1 diagnostic and lies inside the extraction root. Record every attempt's outcome, code and path.
  The deterministic-ENOENT control must come from real REA on a fixture, not a shim.
- **M-10 (E10): separate allow-list, id-bound, exact.** `prior_pins` holds only stale pins. A separate
  `re_scored_pins` holds exactly the four round-50 (id, pin) pairs, checked for equality with
  `tools/round-50/carriers.json` at FREEZE. `carrier_fresh_ok = pin ∉ prior_pins OR (id, pin) ∈ re_scored_pins`.
  Enumerate every committed `carriers.json` and every `subject.digest.sha256` and `external.*`/`nested.*`
  pin at FREEZE by `git ls-tree`, not from a hand list. The round-52 `after.json` must not be byte-equal to
  any round-50 blob.
- **M-11 (E11): entry and binding content checks.** The entry must cite the four fresh receipts'
  sha256 digests (from `evidence_digests`), name the claimed S-ids exactly (S243, S244, S245, S249, S250,
  S251, S252), and carry `source:` lines matching them. Each S-id row must exist with `used-by` containing
  the stem and an `opened` date of 2026-10-30. `frontier_note` must sit inside `## Frontier` or the
  round-52 section, and the LE row must be absent from `## Frontier`. `coverage_map_row` must be a table
  row whose first cell is the stem. `entry_present` needs non-empty content and the required headings.
- **M-12 (E12): update the frozen lists.** `FROZEN_PATHS` gains `plans/round-52-claims.md`,
  `tools/round-52/gap-rule.json`, `tools/round-52/carriers.json`. `FROZEN_PREFIXES` = `tools/round-52/`.
  Keep `tools/round-50/` frozen as well.
- **M-13 (E14): explicit required map.** `gap_rule_model` lists all six kinds in `required` and rejects a
  rule that omits one a frozen oracle table contains.
- **M-14 (E13): drop the env guard as a control.** Either remove the guard from the harness or state in the
  claims that it is procedure, not a binding.

## 5. Confidence and disclosure

- High: E2 (probed), E6 (probed), E1, E3, E4, E5, E7-E11, E14 (code citations checked against the file at base).
- Medium: E9 (depends on how the retry is implemented in v2; described from the claims text).
- Not verified: REA's behaviour on `REA_UNBLOB_COMMAND` and the bin-path semantics (taken from the harness
  and counter comments, not run). The round-52 claims text as amended in the freeze may already close some
  items; I attacked the draft at `ab0eafed`.
