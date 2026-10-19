# SEAT EX-23 — chain c3 · executor · wave arc3-loop1-round4

**Task (seat line).** After-state (poll for EX-21): the sidecar-scope injection →
its declared class; the neighbour file untouched. Artifact
`claims/c3/EX-23/sidecar-after.md` (this file).

Lane note read and honored: the hyper lane's 402 on the whole roster is a
declared-fallback dispatch recorded in the freeze, not a lane signal.

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`015e1bab914713568f339fd53999bc180459cc40` (read-only `git rev-parse`). Date
2026-10-19. No git mutations. Scratch only under `/var/tmp/ex23` (never `/tmp`,
EDQUOT standing). Custody paths read-only throughout: the real tool was copied
and every run happened on a scratch copy. No corpus/SKILL/PROVINCE/README/LOG/
SCORECARD/SHONEN writes; no installs (the round's one authorized install is
EX-02's, consumed read-only here).

---

## 1. Work performed (evidence pointers)

All paths relative to the repo root unless noted. `$D` = `.ufo/waves/arc3-loop1-round4/claims/c3/EX-23`.

| # | work | evidence |
|---|---|---|
| 1 | Read the freeze (roster, C3 claim, lane note) and the residual's whole paper trail: r3 `c2/verdict.md` §Named residuals item 3, `CR-4/proposed-write-guard.patch.md` item 1, `RV-8/rv8-corrections.patch.md` Gap 2 + `evidence/claims-run.txt` §C-8 | frozen claims file; those r3 paths |
| 2 | Pinned the before-state contract on the frozen base revision (copy `custody-pair.py`, sha `7cd19c3c…` → `/var/tmp/ex23/custody-pair-BASE-7cd19c3c.py`, re-derived) | `$D/before-probe.out` |
| 3 | Wrote a deterministic, diffable injection driver (five arms + control), which EX-21 later adopted as the chain's cross-seat driver | `$D/sidecar-injection.py` (sha `4c31ad6e…`) |
| 4 | Built a scratch-only guarded variant (CR-4's patch shape) to pre-register what "closed" would look like — and found it insufficient for spelling B | `$D/scratch-guarded-variant.py`, `$D/scratch-variant-probe.out` |
| 5 | Polled for EX-21's landing: 25×60 s watcher on the real target's sha256 + `seats/` + `claims/c3/EX-21/`; landing detected at check 6 (11:09:48 local), new sha `29bb45ae…` | `/var/tmp/ex23/poll.log` |
| 6 | **After-state**: ran the byte-identical driver on the landed revision; re-derived the target sha before and after the run (no mid-run movement) | `$D/after-probe.out` |
| 7 | **Attacks on the after-state** (scratch copies only): symlink sidecar, relative spellings, over-refusal control, `--out ''`/`'.'`, and a byte-sabotage that deletes the neighbour term | `$D/after-attacks.py`, `$D/after-attacks.out` |
| 8 | Independent corroboration: EX-21 ran this driver on both revisions themselves; their summaries reproduce mine arm-for-arm | `claims/c3/EX-21/matrix/{before,after}-ex23-sidecar-driver.out`; their `sha256s.txt` pins my driver sha |
| 9 | Chain-level checks: EX-21's live pair verified `MATCH 5/5` (live and receipt-vs-receipt) with and without `--require-paths 5`; both receipts self-pin the landed tool sha; both sidecars `sha256sum -c` OK; landed selftest `CLEAN cases=28 passed=28 failed=0`; command A unchanged at HEAD (`83/83, missing [], dangling [], rules 14/14`); census v10 `PASS` | command outputs in this report's §3/§4; `claims/c3/EX-21/receipts/`, `.../selftest/selftest-landed-28cases.out` |
| 10 | Identity discipline (rule #14): every byte-identity re-derived at write time from the live tree/scratch files | §6 manifest |

## 2. Proposed changes

**none.** This seat is an after-state measurer; it wrote no tool code and no
patch text. The landed revision (`29bb45ae…`) is EX-21's write.

## 3. Before → after measurement for the C3 claim (residual (a))

The injection, all three spellings, plus the consequence arm and a no-regression
control, run by the **same driver bytes** (`4c31ad6e…`) on the base copy and on
the landed copy. "Declared class" = the class EX-21 declared and EX-27's r4
harness asserts: refusal `exit 2` **and** no clobber.

| arm | injection | before `7cd19c3c…` | after `29bb45ae…` | declared class |
|---|---|---|---|---|
| A | `--out X --paths X.sha256` (sidecar lands on the measured file) | exit **0**, measured `X.sha256` clobbered | exit **2**, touched files **(none)** | USAGE 2 — closed |
| B | `--out X.sha256 --paths X` (receipt lands on the measured file's neighbour) | exit **0**, neighbour created/written | exit **2**, touched files **(none)** | USAGE 2 — closed |
| B2 | same, neighbour **pre-exists** (the literal "neighbour file" wording) | exit **0**, neighbour overwritten | exit **2**, neighbour byte-identical (`99364562…` before and after), touched **(none)** | USAGE 2 — closed |
| E | sidecar path is a **hardlink** of the measured inode (`--out` fresh) | exit **0**, measured inode clobbered | exit **2**, measured inode unchanged | USAGE 2 — closed |
| D | consequence: capture a valid receipt of `X.sha256`, run the injection, ask the tool's own `verify` | injection exit 0; `verify --live` → **`CONTENT-DRIFT paths=0/1 drift=1 exit=10`** | injection exit 2; `verify --live` → **`MATCH paths=1/1 drift=0 exit=0`**; measured digest held | USAGE 2 — closed |
| C | control: legitimate capture into a fresh `--out` beside a measured `.sha256` file | exit 0, sidecar written, pins the receipt, `verify --live --require-paths 1` → `MATCH 1/1` | identical (exit 0, pins, `MATCH 1/1`) | no regression |

Refusal line on all four closed arms (verbatim, `$D/after-probe.out`):

```
USAGE: refusing to write a receipt or its derived sidecar over a path it measures,
a custody path, or the sidecar-shaped neighbour of one (resolved path or inode): <candidate>
```

The landed guard is **stronger** than the presumed patch shape (CR-4 item 1 /
RV-8 Gap 2 guard `(out, sidecar)`): it also guards the *sidecar-shaped neighbour*
of every measured path (`<measured> + ".sha256"`), which is exactly spelling B —
the spelling the presumed shape left open. Measured on the scratch variant
(`$D/scratch-variant-probe.out`): A closed, **B/B2 still exit 0** (they write
onto the neighbour name), E closed. So the after-state is not merely "the patch
landed"; it closes a case the patch texts did not.

Chain-level facts re-derived by this seat (not cited):

- landed tool `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf`, 1343 lines;
  README `9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a`, 272 lines
  (the README was re-landed during this window — `f30df42e…` → `125e7e02…` → `9d9400da…`
  as EX-26's (d) ruling text landed; the sidecar/neighbour clauses and the
  28-case selftest sentence hold at the current revision);
- `selftest` on the landed bytes: `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`,
  including `refuses-sidecar-over-measured-file` and `refuses-receipt-over-sidecar-neighbour`;
- EX-21's live pair: `live-pre.txt`/`live-post.txt` both carry
  `# tool: custody-pair.py  sha256 29bb45ae…`; `verify … --live --require-paths 5`
  → `MATCH paths=5/5 drift=0 exit=0` for each, and pre-vs-post → `MATCH 5/5`;
  `sha256sum -c` on both sidecars → OK;
- command A at HEAD: `{"knowledge_files": 83, "mapped": 83, "missing": [], "dangling": [], "citation_resolved_rules": 14, "rule_blocks": 14, "coverage_score": 10.0, "depth_score": 10.0}`
  — unchanged by this round's C3 work;
- census v10 at the work tree: `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`.

## 4. Attacks / refutations attempted, with verdicts

All on scratch copies; the real tool was read-only (hash/stat) throughout, and
its sha was re-derived after every run — no movement observed at any point.

| # | attack | measured | verdict |
|---|---|---|---|
| 1 | "the guard only checks literal names; a **symlink** sidecar to the measured file slips through" | `out.txt.sha256 -> vic.conf`; run → exit 2, measured digest unchanged, no receipt written | **refuted** (resolved-path comparison follows the link) |
| 2 | "**relative spellings** defeat the resolved-path comparison (the half-fix trap)" | `cd` into fixture dir; `--out ./vic.sha256 --paths ./vic` → exit 2, measured digest unchanged | **refuted** |
| 3 | "guarding the name pattern is an **over-refusal**: a legitimate receipt named `q.sha256` is now blocked" | `--out q.sha256 --paths p.conf` (stem not measured) → exit 0, receipt written, sidecar written | **refuted** — no blanket name ban |
| 4 | "deriving the sidecar name inside the guarded region turns `--out ''` / `'.'` into a `ValueError` traceback (CR-4 item 6's trap)" | both spellings → exit 2, `USAGE: --out carries no usable name…`, no `Traceback` in stderr | **refuted** |
| 5 | "the after-state is vacuous: the arms would be red anyway / the neighbour term does nothing" | byte-sabotage deleting the `cand_res in neighbours` term (`scratch-sabotaged-no-neighbours.py`, `5ebafb79…`): arm A stays exit 2, arm **B flips to exit 0 and the receipt lands on the neighbour name** (bytes read back: `# custody-pair receipt v2 …`) | **term is load-bearing** — the closure of B/B2 is caused by that arm, not by luck |
| 6 | "the before-state was mis-measured (wrong revision, stale copy)" | before-run tool sha in every block = `7cd19c3c…` = the r3 landed revision per EX-21's own `sha256s.txt` and CU-1's independent census; EX-21's independent run of my driver reproduces all before arms | **corroborated** |
| 7 | "the after-state is a one-off / not reproducible" | driver re-run (label `AFTER2`): all arm verdicts identical to `AFTER`; only the control receipt's own digest differs (time-dependent receipt body) | **reproducible** |
| 8 | "the driver's landing detection over-reports" (found in my own probe: an arm pre-creating `--out` printed `receipt-landed=True` on a refused run) | fixed: `landed` is now `before != after`, and B2's before-state is the literal wording (pre-existing neighbour, byte-identical after) | **self-refuted and corrected before the after-run** |

## 5. Blockers

None. EX-21 landed within the poll window (check 6 of 25); every after-state
check ran against the landed bytes and the sha was re-derived before and after.

## 6. Identity manifest (rule #14 — re-derived at write time)

| artifact | sha256 |
|---|---|
| `.ufo/gates/custody-pair/custody-pair.py` (landed target, re-derived at write) | `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` |
| `.ufo/gates/custody-pair/README.md` (re-derived at write) | `9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a` |
| `/var/tmp/ex23/custody-pair-BASE-7cd19c3c.py` (before copy) | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` |
| `/var/tmp/ex23/custody-pair-LANDED-29bb45ae.py` (after copy) | `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` |
| `$D/sidecar-injection.py` (driver, final bytes) | `4c31ad6e51bed530e1a69256422b69aa2e0fc3f4885c22da32cb5ea728f97a00` |
| `$D/before-probe.out` | `d85b87774410346072b09ba936361d373dc3ac1bfecdab8e59524047a29bf6fd` |
| `$D/after-probe.out` | `c65695b6a5073d5455ef8fb14a38383f3df1e2001917d71500be1ab68c30478d` |
| `$D/after-attacks.py` | `3b68c2a058fe8d2dbc46e4ae015f9920f0bd48b5948a3f9cc74b0baf6f3a05ee` |
| `$D/after-attacks.out` | `c3974cedb517657c6296ff6328430cb4a28789f0e54998b3b29be38c3e788714` |
| `$D/scratch-guarded-variant.py` (CR-4 shape, scratch only) | `b61cee689fbf24eb4201035b596556872910059d70d8ed8e34f07005f256148f` |
| `$D/scratch-variant-probe.out` | `4e781b5e4a86864520181d36244a424bf7ff877c5573c4bb722aead76642aed2` |
| `$D/scratch-sabotaged-no-neighbours.py` | `5ebafb79435906e33c4714bbbb293913f2b4b90605c73f85736b635c20c72bbc` |
| `$D/sha256s-so-far.txt` (pre-report snapshot) | `5fa150f8005e0e5ffe18268a7b5a1769881b16b3b46e1d09da41b351f778bef1` |

This report cannot carry its own post-edit digest without circularity; the
digests above are the authoritative pointers, re-derived from the files as they
stood when it was written.
