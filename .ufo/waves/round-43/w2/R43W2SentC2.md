# R43W2SentC2 — adversarial path/security review: local-source gate, map parser, symlinks, archives, C2 scratch clone

Seat: sentinel, round 43 wave 2 (falsification wave; read-only). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope: the local-source gate (`tools/round-41/local-source-gate.py`), the map parser
(`corpus/evidence/local-sources.json` + its two readers), symlink handling, archive handling, and the
`c2-score-r43.py` clean `--shared` clone. Attacks C2 only; C1 was not touched.

**Measured revision.** Every attack below was evaluated at **`77d196c6`** (the revision the landed C2 receipt
counts). Lane tip is **`5856614a`**; `git diff --stat 77d196c6 5856614a -- tools/round-43
tools/round-41/local-source-gate.py` is **empty**, so the tool bytes under attack are identical at tip. Round
freeze **`f3f8db38`**; base **`6b9e64fe`**.

| what I read | sha256 |
|---|---|
| `tools/round-41/local-source-gate.py` @77d196c6 | `cafe232a196dd8446bd9b0420b32bf696cba427770eb79edda2be15a45a4ece7` |
| `tools/round-43/c2-score-r43.py` @77d196c6 | `459cbccbb2bf172376357b7e72549add1d99c5d9ed70fecc8acec1ea93432faa` |
| `tools/round-43/verify-copies-r43.py` @77d196c6 | `00b3f7a4c7a2ee7f5a6654f12211cbf2a12e0fe10e9de7fc35ff088ce8f3b020` |
| `tools/round-43/receipt-wrap.py` @77d196c6 | `b5f01904fc20b4cc014f43c3b1e4f120dd3d8e60c942bb5bc11c21bd260d0211` |
| `corpus/evidence/local-sources.json` @77d196c6 | `3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e` |
| `corpus/SOURCES.md` @77d196c6 | `251ec4a72ee3dcf1f0f5e45debc001be2333c0340b661e616ebceaaedb62c68c` |
| `.ufo/waves/round-43/l1/scores/c2-at-77d196c6.json` | read whole; `expect-source-frozen` reports R42 verifier `1f790e10…` at work/freeze/rev |
| `.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json`, `.ufo/waves/round-43/controls/c2/*` | read |

Full command/output record: `artifacts/R43W2SentC2/measurements.txt`. Scratch:
`/fast/scratch/hyaku/kaidoku-r43/w2/R43W2SentC2/` (removed before yield).

---

## F1 — HIGH — the frozen C2 target is unsatisfiable on the landed bytes, and the landed receipt says so

**Finding.** `c2-score-r43.py` binds `sources_numstat == "3\t0\tcorpus/SOURCES.md"`. The measured
`git diff --numstat 6b9e64fe..REV -- corpus/SOURCES.md` is **`4\t0`** at `09ab56b8`, `77d196c6` **and** tip
`5856614a`: the appended block is **S135 + S136 + S137 + one blank separator line**. Both committed receipts
record the failing value and exit 1:

```
c2-at-09ab56b8  sources_numstat='4\t0\tcorpus/SOURCES.md'  exit_code=1  checks_ok=false
c2-at-77d196c6  sources_numstat='4\t0\tcorpus/SOURCES.md'  exit_code=1  checks_ok=false
  failing clause: sources_numstat_three_additions=false   (all other 12 clauses true)
```

**Exploit path / impact.** None needed: this is an honest red that the round's own target ("Target:
`tools/round-43/c2-score-r43.py` exits 0") treats as closure. P43-C2's text ("BASE→REV numstat is exactly 3
insertions and 0 deletions") is contradicted by the append it mandates (3 rows plus a table/paragraph
separator). No injection, no fabrication — the L1 committed a failed receipt and did not re-read the residual
clause as a stop.

**Smallest remediation.** Record C2 as *target unmet* (the frozen tool cannot be changed now), and correct the
predicate text/constant to `4\t0` (three rows + separator) if the round is re-cut. One-line fix in any future
copy: derive the expected numstat from the appended row count instead of a literal, or bind
`git diff --stat` insertion count ≥ 3 plus a content assertion on the three `S13x` rows.

## F2 — HIGH — `copy-in-stated-dir` is a string prefix, not containment

**Code.** `verify-copies-r43.py:248`: `indir = rel.startswith(STATED_DIR) or rel == PRESERVED`. `cp` is set at
line 239 (`os.path.join(root, rel)`) and opened with **no** resolved-path containment test (the gate's own
`inside()`/`normpath` guard is not reused).

**Exploit path (measured, E2).** Rewrite one map entry (S081) to
`copy = "corpus/evidence/round-42/local-sources/../../../../tools/round-41/local-source-gate.py"` with the
gate tool's sha256. Result: gate **exit 0**, `rows_failed []`; verifier **exit 0, `checks: 136, failures: 0`**,
with `copy-in-stated-dir … OK` printed for the escaping path and `map-digest … OK`. The read resolves to
`<root>/tools/round-41/local-source-gate.py` (`readlink -f` in the log).

**Second, structural half.** For the 9 `tree-archive` entries the `member-pin`/`member-present`/`host-identity`
checks do **not** read `entry["copy"]` at all — they re-open `STATED_DIR/<sid>/<fixed tar name>`. So the only
check tying the copy's bytes is `map-digest`, whose expected value the map itself supplies. The copy/provenance
clause is therefore circular for exactly the entries where a wrong copy is most plausible.

**Impact.** Within this round `map_digest_pinned` (one constant) is the only blocker for a map rewrite, and it
blocks by digest, not by containment. The verifier is the predicate's "mandatory structural/content linter",
used as the landing lint and reused by later rounds; its containment clause does not hold.

**Smallest remediation.** `real = os.path.realpath(cp)`; require
`os.path.commonpath([real, os.path.realpath(os.path.join(root, STATED_DIR))])` to equal the stated dir (and
`PRESERVED` exact for S126) before any open; emit the resolved path in the check detail. For archives, require
the copy's sha256 to appear in a row-pin/member-independent set rather than only in the map.

## F3 — HIGH — the "no symlink at any component above it" clause is not implemented anywhere, and it is the clause that matters

**Claim text (plan, P43-C2).** "…a regular file — not a symlink at its own path **or at any component above
it** (the frozen gate's `isfile` follows links, so the scoring wrapper adds a `find -type l`/lstat check over
`corpus/evidence/round-42/local-sources/` and `corpus/evidence/round-41/s126/`)". `c2-score-r43.py` contains
no `find`, no `-type l`, no directory scan; `verify-copies-r43.py` lstat's only each of the 18 mapped file
paths (`copy-regular`, final component). Measured histogram of the committed audit's 136 checks:
`copy-regular 18`, `copy-in-stated-dir 18`, `copy-size 18`, `map-digest 18`, `byte-identical 11`,
`host-sha256 4`, `member-pin 32`, `member-present 4`, `gz-digest 1`, `host-identity 3`,
`upstream-identity 3`, six map/state singles — **no directory or parent-component check**.

**Exploit path (measured, E1).** In a clean clone at 77d196c6 replace `corpus/evidence/round-42/local-sources/S048`
with a directory symlink to an out-of-lane duplicate, commit it as a fixture (`120000 blob`; git reproduces it
on every checkout), then run the frozen tools:

* gate: `exit 0`, rows 137 / checked 19 / `rows_failed []`;
* verifier: `exit 0`, `checks: 136, failures: 0` — all 33 S048 lines OK (`copy-regular`,
  `copy-in-stated-dir`, `copy-size`, `map-digest`, 24 `member-pin`, 4 `member-present`,
  `host-identity S048 … 28 members OK`);
* **frozen scorer** on that committed fixture (`0f8a7a5a`): **12 of 13 clauses true** — `clone_at_rev_clean`,
  `gate_exit_zero`, `rows_failed_empty`, `copy_audit_136_checks`, `copy_audit_no_failures`,
  `map_digest_pinned`, `s126_preserved`, `freeze_ancestor`, `score_tool_frozen` all true; the only false clause
  is F1's `sources_numstat_three_additions`.

`clone_clean` stays true because the worktree is exactly what the commit contains, so a *fresh* clone by the
scorer materialises the symlink and reads the attacker-chosen directory — with map bytes and `MAP_SHA256`
unchanged.

**Impact.** With F1 corrected this is a full false green of the predicate's content proof: the audit reads
bytes from outside the lane while reporting the stated in-lane path. The same construction works at any
ancestor of a mapped copy (e.g. `corpus/evidence/round-42/local-sources` itself → all 17 copies outside the
lane).

**Smallest remediation.** Before the per-entry loop:
`for dp, dns, fns in os.walk(dir, followlinks=False): assert not any(os.path.islink(os.path.join(dp,n)) for n in dns+fns)`
over `STATED_DIR`, `STATED_DIR/../..` chain as needed, and `corpus/evidence/round-41/s126/`; emit one FAIL per
symlink. Cheaper and stronger: compare `realpath(cp)` to the `realpath` of the stated dir (kills F2 and F3
together).

## F4 — MEDIUM — the scorer binds neither the linter's nor the gate's bytes; the gate digest is recorded and never compared

**Code.** `c2-score-r43.py` checks: `score_tool_frozen` (only `c2-score-r43.py`), `gate_exit_zero`,
`rows_total_137`, `rows_checked_19`, `rows_failed_empty`, `copy_audit_*` (parsed from the linter's own stdout
with one regex), `map_digest_pinned`, `sources_numstat_three_additions`, `s126_preserved`, `clone_at_rev_clean`,
`freeze_ancestor`. The wrapper does record `gate.tool_digest_at_rev`, but **no check compares it** — although
the plan binds the gate to `cafe232a…`.

**Measured (E5).** A fixture gate with `check_path` short-circuited to `ok=True` (`d5959be…`) scores
`gate_exit_zero: true`, `rows_failed_empty: true`, `rows_checked_19: true`, `rows_total_137: true` — no check
reds on the changed digest. The verifier compounds this: its `key-set-equals-rows` imports the gate **from the
audited tree**, so the tampered gate supplies both the verdict and the key-set oracle.

**Calibration (this round is not exploited).** The real gate is byte-identical at `d764389e`, freeze,
`77d196c6` and tip (`cafe232a…`, measured), so the clause is *true* now; the defect is that nothing would
detect it if it were not. Cross-claim note: the C1 counter's `FROZEN_PATHS` includes all of `tools/round-43`,
so a changed C2 tool would red *C1* — a cross-claim dependency, not a C2 binding, and C2's own counting
command would still pass.

**Smallest remediation.** Add `gate_sha256 == cafe232a…` and `linter_sha256 == 00b3f7a4…` (compare the bytes
read from the clone, not the wrapper's echo) as required checks; fail closed before parsing the child's
stdout.

## F5 — MEDIUM — upstream inputs are unbound, and absence is scored as a pass

**Finding.** The plan says "Upstream inputs are digest-pinned (Go tags; npm tarballs S081/S090/S092)". Neither
the score receipt nor the copy-audit receipt records a digest for `--upstream-dir`, `--tarball-67` or
`--tarball-65` (measured: no `tarball*`/`upstream*` keys). The three `upstream-identity` verdicts (S035 ×2,
S081) each collapse to a `host-state` line when the input path is absent or unreadable — measured as S081
flipping `OK` → `FAIL` when the sibling's tgz vanished between two identical-argv runs.

**Measured incidental proof.** The sibling scratch that held the two tgz
(`/fast/scratch/hyaku/kaidoku-r43/w2/R43W2C2Pins/`) was deleted by its owner between two of my runs. With an
identical argv, S081 flipped from `OK` to `host-state S081 FAIL … no --tarball`. The symmetric substitution
(unrelated tarball with the same member bytes, or a wrapper path) flips it green with no receipt change. Related
weakening: `host-state` emits `True` when a host object is absent for `byte-identical`/`host-sha256`, i.e.
absence is booked as a passing check. At `77d196c6` the committed audit has **0** `host-state` lines (measured),
so the landed 136/0 is not vacuous on this host — but on a host without those objects the same 136/0 can be
reached with zero content checks.

**Smallest remediation.** Record sha256 of each input path in the receipt and compare against the tag/tarball
pins; emit absence as its own non-OK class rather than `OK`.

## F6 — LOW — committed bytes choose host paths that the auditors open without validation

Three paths, all measured or code-literal, no extraction required:

1. **Tar member names.** `verify-copies-r43.py` iterates *all* members of the lane tars and builds host paths with
   `os.path.join(udir, n)` (S035) and `s048_host_path(n)` (S048). An absolute (or `..`) member name escapes:
   in E4a I appended a member named `/fast/scratch/…/canary.txt` to `S035/internal-abi-go1.25.0.tar`; the
   verifier opened it (`strace`: `openat(AT_FDCWD, "…/canary.txt", O_RDONLY|O_CLOEXEC) = 3`), reported
   `upstream-identity … FAIL … DIFF …/canary.txt` on mismatch and `OK 29 members` when I made the bytes equal.
2. **`copy` field.** `cp = os.path.join(root, rel)` runs before any containment test; an absolute `copy` is
   opened and hashed (then fails `copy-in-stated-dir`).
3. **Map keys / `source_sha256`.** The gate hashes the external path named by a SOURCES row and prints a
   12-hex prefix of the mismatch (by design, but it is a digest oracle over any readable host path named by
   lane bytes).

**Impact.** Equality oracle / digest fingerprint over arbitrary host files named by lane bytes. No content is
written or echoed; no traversal-write exists.

**Smallest remediation.** Reject member names that are absolute, contain `..`, or are non-regular; resolve and
contain every path (`realpath` + `commonpath`) before hashing or comparing.

## F7 — LOW — unbounded expansion of committed archive bytes

`gzip.decompress(fh.read())` (S023) and `{m.name: tar.extractfile(m).read() …}` (every tar) are unbounded.
Measured: a **260,934 B** gz written to `S023/go1.25.0.json.gz` expands to 256 MiB with **534.84 MiB peak child
RSS**; `copy-size` bounds only the *stored* file (5 MiB), so the 5 MiB clause does not bound decoding. There is
no `extractall` anywhere in the round-43 tools or the gate (grep), so this is audit OOM/DoS only, never a green.

**Smallest remediation.** Stream + cap decoded bytes (hash incrementally, refuse > the row's expected size), and
stream tar members instead of materialising a dict of bytes.

## F8 — LOW — host-path leakage in frozen tools and committed receipts

* `c2-score-r43.py:24` hardcodes `S126 = "/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv"` — another lane's path inside a byte-frozen tool (it is also a map key, so it works anywhere; the leak is textual).
* `verify-copies-r43.py` hardcodes 5 host paths (two npx caches, ghidra, the go opt dirs, `/var/lib/pacman/sync/extra.db`).
* Both committed score receipts embed **16 distinct `/home/vgpnk/…` paths** plus `root`, `scratch` and the full
  `argv`, so the "green" is not reproducible off this host and the receipts disclose fleet layout.

**Smallest remediation.** Take host roots from explicit flags (no literal default), record them in an
`environment` block (or as hashes) instead of the paths, and keep the S126 key as a named row constant.

---

## Non-findings (measured, so the frontier is calibrated)

* **Final-component symlink is caught.** `copy-regular` reds on a symlinked copy (`E3`: verifier exit 1,
  `1 failure: copy-regular … FAIL symlink`), matching the committed `ctl-c2-2-summary.txt` ("baseline gate=0
  linter=0; symlink gate=0 linter=1"). The gate's green there is the disclosed, deliberate CTL-C2-2 false-green.
* **The gate is content-based, not name-based.** My first traversal attempt reddened `copy-digest-mismatch` on
  S081 because the declared digest did not match the target's bytes — the gate re-hashes; a bypass needs a
  matching digest, which only a map attacker has (F2).
* **No archive-write traversal.** No `extractall`/`tar -x` into a tree: the S082 pacman probe uses `tar -xOf`
  (stdout only) with a fixed member. Nothing in the chain writes outside `--scratch` and `--json-out`.
* **No shell interpolation.** Every child is a list argv (`subprocess.run([...])`), including the gate, the
  wrapper and the linter; `receipt-wrap.py` runs its `cmd` list with `cwd=root`.
* **Ordering.** `clone_clean` is measured after checkout and before the children run; both children are
  read-only, so the recorded cleanliness covers what was audited.
* **[INFERENCE] Duplicate map keys:** gate `json.load` is last-wins (plan-disclosed); the verifier's
  `object_pairs_hook` applies at every nesting level and reds it. I did not execute a duplicate-key case.

## Limitations

1. The E5 tampered-gate scoring run finished 136/1 because the sibling scratch holding the two tgz inputs was
   deleted mid-run (`host-state S081 FAIL`); I did not re-fetch (no network, and I will not copy published
   tarballs). The gate-side result of E5 is independent of those inputs; E1's 136/0 was measured in the same
   session while the inputs existed.
2. I used those two tgz read-only from the sibling's scratch for E1–E4. Their provenance is **not** verified by
   me (nothing in the receipts pins them) — [INFERENCE] they are the L1's inputs because they reproduce the
   committed `upstream-identity` member verdicts exactly. This is itself the F5 evidence.
3. I rebuilt the `--upstream-dir` go trees by extracting the committed S035 tars into my scratch, so the S035
   `upstream-identity` checks in my runs are circular; they only had to be non-failing to reach 136/0.
4. Reserved inputs respected: no REA/unblob/sasquatch/extractor run, no third-party firmware image opened; the
   only archives touched were the lane's committed MIT-fixture-derived Go/JS tars and my own generated tars.
5. Fixture commits were made only in scratch clones, each after `git -C <clone> rev-parse --show-toplevel`
   printed that clone (`clone` → `0f8a7a5a`, `clone4` → `5f960e3f`). No lane edit, no VCS mutation in the
   lane, no `agent://all`, no subagents.
6. Environment: python 3.14.8, git 2.x, strace used only to observe `openat`; `/fast` had 350 G free
   throughout, no ENOSPC.

## Verdict on the assigned surface

Against the frozen predicates at `77d196c6` (= tool bytes at tip `5856614a`): **C2's target is red on its own
landed receipt (F1), and the two clauses that are supposed to stop a hostile copy tree are unimplemented (F2,
F3)** — the gate + 136-check linter both go green with mapped copies physically outside the lane, and the only
clause standing in the way of a full exit-0 is the unrelated numstat constant. The gate itself is byte-frozen
as claimed, content-hashes copies (a real check), and no archive-extraction or shell-injection path exists.
Latent (would be exploited by a round that fixes F1 without F2/F3): unbound gate/linter/upstream-input bytes
(F4, F5) and unvalidated tar member names (F6).

Report: .ufo/waves/round-43/w2/R43W2SentC2.md
Artifacts: .ufo/waves/round-43/w2/artifacts/R43W2SentC2/
