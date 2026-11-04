# Round 72 — checker-mode children, the checker's binding verdict, and the raw witness

author: KaidokuR72 (L1), lane kaidoku-shokunin
round: 72, attempt 1
base: `56241b1c8baff95862730c008f1ae5132b03388e`
declaration: `6316c1053f927a1a1cdc3e0960b70acab5f56381` (+ pre-freeze fixes `17d8b5f785a449aed76f42e697071007ae9e226f`, `306cbb3fb11661fba6f364f73ad0b1eeb24a959f`, `25ecc71116bad0673416ebfc128be5a16e03b7e2`, `1563ea353ab32acc2141c82b89299580cb73f4c8`)
freeze: `34fe7aa70b627d92e2d27dbce308d9f5bebda63d` (the round-29 gate audits it CLEAN, findings [])
landing: the round-72 record commit in the lane (cite the lane report for the hash); the measured
receipts are `.ufo/waves/round-72/l1/scores/*.json` and the wave evidence is
`.ufo/waves/round-72/w1/` with `r72-w1-results.json`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **The capture claim stopped at the mode** — the round-71 instrument recorded every route child while the checker's own `git`/`readelf` children inherited the caller's whole environment (275 keys, canary present), and its docstring said "every child". A reader of the round-71 receipt could not see the gap. | `.ufo/waves/round-72/l1/pre/c1-at-base.json` (9/11, A11 false; shim keys HOME/LANG/PATH/PWD/SHLVL/TMPDIR/_ with `KAIDOKU_ENV_CANARY`); `ExecC1Base.md` (five records, 275 keys each); the round-71 container's own atom A2 ("The checker's own readelf/git reads are outside the claim's scope") | none at the time — no arm enumerated the checker-mode child inventory; QUALITY row 121 bound a capture claim to the children it records but not to the mode. The fix is C1's A11: the arm now derives the census from the checker's log bytes and requires `git`/`readelf` counts. | `tools/round-72/seam-probe.py` `checker_env_arm`/`a11_verdict`; `tools/round-72/packed-elf.py --check-receipt --child-env-log`; receipt `l1/scores/c1-at-landing.json` (11/11). |
| **A mutation survivor was reported but not bound to a failing case** — round-71's MutReaders reported survivor i (`probe:471 binding_ok = True`) and said "redundant protection"; the next round inherited a probe whose binding verdict was re-derived from receipt fields. | `.ufo/waves/round-71/w1/MutReaders/mutants.md` (row i); `.ufo/waves/round-72/l1/pre/c2-at-base.json` (patch set r71: survivor 1) | the round-71 closure recorded the survivor without creating a selftest case that binds it (QUALITY row 109's case-inventory claim covers case *names*, not a survivor's *predicate*). | `binding_verdict` + `a10-binding-from-checker`; `mutation-check.py --patch-set r72` kills the same mutation (`.ufo/waves/round-72/l1/scores/c2-at-landing.json`). |
| **A shell shim measures the shell, not the exec boundary** — the first A11 shim was `/bin/sh` + `cat /proc/self/environ`; the landing run showed seven keys (`PWD`, `SHLVL`, `_` added by the shell), so the exact-allowlist clause failed for a measurement artifact. | landing run of `tools/round-72/seam-probe.py` before supersession `6284abeb` (shim keys HOME/LANG/PATH/PWD/SHLVL/TMPDIR/_) | the arm's own exactness clause — it failed closed rather than green-washing the artifact; the grader was the landing counter, not a case. | perl shims (`exec` after a `/proc/self/environ` read); verified four keys under a four-key exec (supersession `6284abeb`, listed in `claims.json`). |
| **A control's aggregate read the loose verdict** — `controls.py` gated `all(a["met"])` while the c3 arm's strict verdict was `met_control`; a mocked audit that accepted pollution still produced rc 0. | wave `ReviewerGates` receipts `.ufo/waves/round-72/w1/ReviewerGates/controls-lying-audit.json` (`met: true`, `met_control: false`, `ok: true`) | the control instrument had no selftest; the wave's reviewer found it. Fix: the aggregate now prefers `met_control`; the `Controls` seat re-ran it (`l1/scores/controls-at-landing.json`, all arms met). | supersession `4913b5e67cedf9fe3fd4d52ab85e8c21ad9af7c6`. |

## Gate — sources opened this round

| row | URL | opened | quote (≤25 words) | snapshot |
|---|---|---|---|---|
| S275 | https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html | 2026-11-04, HTTP 200 | "This file contains the initial environment that was set when the currently executing program was started via execve(2)." (18 words) | 7 747 B, sha256 `93394d9edb801ad44e342e8e8ab057bea619d995803221edaf008226b2062c46`; the requested `proc.5.html` is a 31 125-byte stub carrying only a SEE ALSO link (31 125 B, sha256 `b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97`) |
| S276 | https://docs.python.org/3/library/tempfile.html | 2026-11-04, HTTP 200 | S274's page restated for the registry's column contract; `mkdtemp()` paragraph: "mkdtemp() returns the absolute pathname of the new directory." (9 words) | 75 198 B, sha256 `edf721761f0de44769b1fb817b8105447a9a8cecb1d6df1c6347a804db442560`; rejected as a distinctness source (flip in `teaches`) |

S275 is the round's sourced claim (R72-C1 cites it through the knowledge entry); S276 is the
round-71 routed defect 4 repair (reason and flip in `teaches`, scope clean, supersedes S274's
cell contract without rewriting it). The quote's anchor (`execve(2)` link) splits the sentence
in the raw HTML; the locator is recorded in the row's anchor cell.

## What the wave found

- **ReviewerGates** (real, fixed in-round): A11 consumed the checker's JSON summary and gated
  containment on `--work`; a fabricated summary with a zero census passed. Fixed: the arm
  parses the checker's log itself, requires `git`/`readelf` counts ≥ 1, and gates on the
  checker's own `run_root` (`a11_verdict`, supersession `d8297e85`). The control aggregate
  defect above was also theirs.
- **ReviewerGates** (real, fixed in-round): a receipt-named lane-relative capsule that is
  absent was silently skipped. Fixed: named-and-absent fails closed; the route summary records
  `log_sha256` so the digest clause is evaluable (supersession `4913b5e6`).
- **CriticClaims** (real, fixed in-round): a checker returning rc 0 with `met false` and true
  clauses was accepted by A10. Fixed: `checker_met()` requires `met` and `clauses.met` to agree
  (supersession `d8297e85`). Their wrapper attack that forges both A11 witnesses is a class
  boundary, recorded in the knowledge entry's limits, not a falsification of the measured route.
- **SentinelScope** (blocking, fixed in-round): receipt-selected capsule paths could read
  outside the lane (`../`, absolute paths, symlink). Fixed: resolved `commonpath` containment,
  regular-file and 64 MiB bounds, external pointers recorded as `skipped_external` and never
  read (supersession `e67f3a1b`); real tools prefer `/usr/bin` over PATH (SS72-1).
- **MutProbe / MutReaders** (quality debt, routed): the selftest still has survivors among the
  arm's auxiliary conjuncts and the reader's env-threading lines (behavioral fixtures kill them;
  the selftest does not). `a11-arm-cases` now binds A11's conjuncts; the route's `env=` threading
  and the implicit-capsule path remain selftest-uncovered — round-73 queue.
- **ExecSweep / ExecC1 / ExecC1Base / ExecC2 / ExecC3** reproduced the three claims and the
  before states independently (see their reports; the base before is 9/11 with 275-key inherited
  children, the landing after is 11/11 with four-key checker children).
- **ScoutSource** found the assignment's premise stale (man-pages 6.19 split `proc(5)`; the
  paragraph lives on `proc_pid_environ(5)`) and proved the id guard on an indented fixture.
- **ConnectorCross** found no sibling owner for the checker-mode/capsule surfaces; its
  cross-source rule ("a verdict is read from the producer's verdict fields") became QUALITY 124.
- **Transient measurement note:** the first base probe attempt at rev `e67f3a1` recorded A8 rc 2
  (one-carrier route unevaluable) while the control's identical arm passed; the re-run at the
  same rev is green (9/11, failed A10/A11 only). The receipt of record is the re-run.

## Non-author closure

`[L1 — filled by the non-author closure.]`

## Security incident — live credentials in a seat's env dump (reported, redacted pre-push)

The `ExecC1` seat wrote `caller-env.txt` to prove the caller environment had reached its shims.
That file held all 272 variables **with values**, including a 1Password service-account token
(`ops_…`) and an OpenAI Codex token. GitHub push protection rejected the record commit (`GH013`,
path `.ufo/waves/round-72/w1/ExecC1/caller-env.txt:193`). The file was replaced by a key-name
census (`caller-env.redacted.txt`), the unpushed commit was rewritten to drop the raw dump, the
pushed range was re-scanned for token shapes and is clean, and no secret was pushed. CLASS:
credential capture by an evidence file. CAPTURED-BY: GitHub push protection (an external gate),
not a lane rule — QUALITY row 128 now binds the lane rule; the wave context's "never write outside
the lane" did not say "and never write values". FIX: key census only, redaction before the first
push, and the L0 line below.

L0 (appended): `kaidoku | round-72 | the ExecC1 seat's raw caller-env dump carried live 1Password
and Codex tokens; push protection blocked it, the file is redacted to a key census, the unpushed
commit rewritten and the pushed range scanned clean — no secret was pushed. Should raw child-env
dumps be forbidden lane-wide (key census only) in the wave context?`
