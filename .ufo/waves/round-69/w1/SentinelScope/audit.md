# round-69 w1 — SentinelScope audit

Seat: SentinelScope (sentinel). Lane: kaidoku-shokunin. Wave: r69-w1.
Base `d7d9a62cc70935304e600ed0dee864fc4f1751f7`; operative freeze `f15998102f1ce3569e61faa2ac6f286bc414538e`.
Every check below was run read-only against the lane; no lane file, index, or history was modified.
Labels: **(observation)** = directly seen in tool output; **(inference)** = derived from code/evidence; **(unknown)** = not established.

---

## 1. Scope of the round's diff

### 1.1 Lane working tree
```
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain
?? .ufo/waves/round-69/r69-w1.ready
?? .ufo/waves/round-69/r69-w1.ready.partial
?? .ufo/waves/round-69/w1/
```
**(observation, timestamped)** At 23:33 this command reported 0 tracked modifications. **At 23:39 the same command reported five modified tracked files and two new untracked corpus files** — a live writer changed tracked lane paths during the audit. See §7. The untracked entries at 23:33 were the wave dispatcher's ready markers and the per-seat `w1/` draft tree.

### 1.2 Diff from base to HEAD
```
$ git -C .../kaidoku-shokunin diff --stat d7d9a62cc70935304e600ed0dee864fc4f1751f7..main
 .ufo/waves/round-69/claims.json                  |  44 ++
 .ufo/waves/round-69/gen-w1.py                    | 365 ++++++++++++++
 .ufo/waves/round-69/l1/census-start.txt          |  20 +
 .ufo/waves/round-69/l1/pre/c1-at-base.json       |  78 +++
 .ufo/waves/round-69/l1/pre/c2-at-base.json       |  94 ++++
 .ufo/waves/round-69/l1/pre/c3-at-base.json       |  19 +
 .ufo/waves/round-69/l1/pre/controls-at-base.json | 105 +++++
 .ufo/waves/round-69/r69-w1-dispatch.err          |   4 +
 .ufo/waves/round-69/r69-w1-dispatch.json         | 223 +++++++++
 .ufo/waves/round-69/r69-w1-spec.json             |  83 ++++
 SKILL.md                                         |   4 +
 plans/round-69-claims.md                         | 136 ++++++
 tools/round-69/contract-probe.py                 | 282 +++++++++++
 tools/round-69/controls.py                       | 173 +++++++
 tools/round-69/mutation-check.py                 | 237 ++++++++++
 tools/round-69/packed-elf.py                     | 576 +++++++++++++++++++++++
 16 files changed, 2443 insertions(+)
```
**(observation)** All 16 paths are inside the lane and inside the allowed set (`tools/round-69/`, `plans/round-69-claims.md`, `SKILL.md`, `.ufo/waves/round-69/`). `tools/round-68/` does not appear in the diff; its route is untouched by this round.

### 1.3 Fleet root (misroot candidates)
```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .scratch/goal-20261103-hyaku-run15.md
 M .scratch/run15-state.json
?? .scratch/run13-state.json
?? .scratch/run15-kernel.py
?? after
```
```
$ find . -maxdepth 4 \( -iname '*round-69*' -o -iname '*r69*' -o -iname '*round69*' \) -not -path './kaidoku-shokunin/*' ...
./.ufo/reports/round-69
./.ufo/prompts/closure/*-round-69.md        (11 other lanes)
./.ufo/prompts/kaidoku-round-69.md          (orchestrator prompt)
./audio-shokunin/corpus/live/r69-reviewer   (audio lane's own round 69)
./audio-shokunin/corpus/live/r69-scout
./audio-shokunin/corpus/live/r69-scribe
./audio-shokunin/corpus/live/r69-boundary
```
- **(observation)** `after` is a 24-byte untracked file at the fleet root containing `== SCORECARD diff base-\n`, mtime 2026-11-03 20:05 — three hours before this wave's first write (23:22) and naming neither this lane nor the round. It is a pre-existing stray, not a round-69 misroot. Reported, not deleted, per instructions.
- **(observation)** `.scratch/` holds run15 kernel/state files from the orchestrator's own runs; none names round-69 or kaidoku.
- **(observation)** Every `r69`-named artifact outside the lane belongs to another lane's own round 69 (audio-shokunin) or to the fleet-level prompt/closure directories. No kaidoku round-69 artifact was written outside `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. **(inference)** The round is correctly rooted.
- **(observation)** `MANIFEST.json`, `.ufo/state`, `.ufo/watchdog.log` have recent mtimes but `git status` shows no content change; `.ufo/watchdog.log` is gitignored (`.gitignore:10`). No fleet-root tracked file was modified.

### 1.4 Tool-dir hygiene
```
$ git status --porcelain --untracked-files=all tools/      → (empty)
$ git check-ignore -v tools/round-69/__pycache__
.gitignore:1:__pycache__/   tools/round-69/__pycache__
```
**(observation)** `tools/round-69/__pycache__/packed-elf.cpython-314.pyc` (23:36) and `tools/round-68/__pycache__/*` exist, but `__pycache__/` and `*.pyc` are gitignored (`.gitignore:1-2`). No `.pyc` is tracked. Not a landing hazard; it shows the tools were imported in place, which is harmless.

---

## 2. The `--upx` seam: execution before the pin check

### 2.1 Code path (frozen bytes, sha256 4ac0d83b…)
`tools/round-69/packed-elf.py:253-259` in `preflight()`:
```python
version = run([upx, "--version"]).get("stdout", "").strip().splitlines()   # EXECUTES the caller path
version = version[0] if version else ""
if version != UPX_VERSION_PIN:
    raise Unevaluable(f"packer_mismatch: version {version!r} != pin {UPX_VERSION_PIN!r}")
sha = sha256_file(upx)                                                     # hashes AFTER exec
if sha != UPX_SHA256_PIN:
    raise Unevaluable(f"packer_mismatch: sha256 {sha} != pin {UPX_SHA256_PIN}")
```
`run()` (`packed-elf.py:185-189`) is `subprocess.run(argv, capture_output=True, text=True, timeout=900)` — **no `env=`**, no `cwd=`, no privilege drop, no sandbox.

**(observation)** The order is exec → version compare → hash compare. The pin is a post-execution check on a path that the executed process can rewrite.

### 2.2 What an untrusted `--upx` can do in that one invocation
Before any refusal is possible, the binary runs with the invoking user's full authority:
1. **Arbitrary code execution** as the caller (same uid, same groups) — no confinement of any kind.
2. **Inherit the full environment.** `env | cut -d= -f1` on the host lists `OPENAI_CODEX_TOKEN`, `XAI_OAUTH_TOKEN`, `OP_SERVICE_ACCOUNT_TOKEN`, `OPKEY_VAULT`, `SSH_AUTH_SOCK`, `STARSHIP_SESSION_KEY`, `PI_SESSION_ID`, `PI_SESSION_FILE`. A hostile `--upx --version` can read and exfiltrate every one of them. **(observation)** of variable names; **(inference)** that a child inherits them, since `run()` passes no `env`.
3. **Read/write as the user**: the whole lane (including `.git/`), other lanes, `~/.ssh`, `~/.npmrc`, provider configs, receipts and future landing paths. It can install a git hook in the lane's `.git/hooks` or drop a binary in `~/.local/bin` (on PATH) — persistence that outlives the invocation.
4. **Network egress** for exfiltration or C2.
5. **Fork/daemonize** so work continues after `subprocess.run` returns; the parent captures only this child's pipes, so a detached grandchild leaves no trace in the return record.
6. **Stall the route** for up to 900 s per call (`timeout=900`), repeatedly.
7. **TOCTOU self-restore** — the sharpest form: the binary prints `upx 5.2.0` and then restores the pinned bytes over its own path (it can copy readable `/usr/bin/upx`, root:root 0755) before the parent reaches `sha256_file(upx)`. Both the version and the sha256 then equal the pins, so `preflight` returns `pin_enforced: True`. The later pack/list/unpack calls use the module global `UPX = "/usr/bin/upx"` (`packed-elf.py:387,391,397,411,412`), so the run completes normally and the receipt records a clean packer. **(inference)** from the code order and POSIX semantics; not executed (out of bounds for this seat and unnecessary — the ordering is plain in the source).
8. **(observation)** The contract probe's own A4 arm demonstrates the pre-pin execution benignly: it builds `/usr/bin/upx` + one NUL byte and passes it as `--upx`; the instrument executes it for `--version` and only then refuses on sha256. The arm scores "killed" because the *message* names sha256, not because no code ran.

### 2.3 Does the pin check make the seam safe?
- For **the work** (pack, `-l`, `-d`): yes — those calls use the module global `/usr/bin/upx`, which is root-owned 0755 and hashes to the pin. **(observation)**.
- For **the seam itself** (`--version` on a caller-supplied path): **no**. The check runs after the code has run and can be satisfied by restoring bytes; "exit 2 after execution" is a refusal, not a safety property.
- For **this lane's own invocation**: the L1 uses the default `--upx` (`/usr/bin/upx`, sha256 `cf2f6e7c…`, root:root 0755) and never passes a custom path. **(observation)** from the scratch run records and the default in `argparse`. So the lane's measured runs are not exposed through this seam; the exposure is to any third party who re-runs with `--upx <untrusted>`, and to the claim's framing that the pin is "enforced" as a safety property.

### 2.4 Secondary inconsistency: validated path ≠ executed path
**(observation)** `score(..., upx=UPX)` passes `upx` only to `preflight()`; every `run([UPX, ...])` in the carrier loop uses the module global `/usr/bin/upx`. If a caller passes `--upx /opt/copy-of-upx` with byte-identical content, the receipt records `/opt/copy-of-upx` as the packer while the actual pack ran `/usr/bin/upx`. Byte-identity makes this immaterial to the pin, and A6 would catch a *different* binary because it compares the receipt's `sha256` against `sha256_file("/usr/bin/upx")` (`contract-probe.py:139`). **(inference)** Latent footgun, no live defect for this claim.

### 2.5 Smallest remediation
In `preflight()`, move the sha256 compare **before** the `--version` exec:
```python
sha = sha256_file(upx)
if sha != UPX_SHA256_PIN: raise Unevaluable(...)
version = run([upx, "--version"]) ...
```
Three lines reordered; the version arm still checks the banner. Optional hardening: pass a minimal `env={"PATH": …, "HOME": …}` to the packer calls and use the validated `upx` variable in the carrier loop instead of the global.

---

## 3. Credential material in the round's new files

```
$ git diff --name-only d7d9a62..HEAD > diffnames            # 16 files
$ while read f; do grep -nE '(ghp_[A-Za-z0-9]{20,}|gho_…|sk-[A-Za-z0-9]{20,}|xox[baprs]-…|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|Bearer [A-Za-z0-9._-]{20,})' "$f"; done
(no output)  SCAN_DONE
```
A broader scan (`api[_-]?key|secret|token|password|session[_-]?id|bearer|credential|BEGIN … PRIVATE KEY`) over `tools/round-69/*.py`, `plans/round-69-claims.md`, `.ufo/waves/round-69/claims.json`, and `SKILL.md` produced only prose matches (e.g. SKILL.md:932 "Never copy `session.json` (it holds the bridge token)" — a warning clause) and the word "token" in documentation examples.
**(observation)** No credential value is present in any file the round added or changed. No secret is required to run the instruments.

---

## 4. Scratch discipline

```
$ find /fast/scratch/hyaku/kaidoku-r69 -maxdepth 1 -mindepth 1
probe  l1  after  ExecC3  ExecC1  ExecRepairs  ReviewerGates
MutBattery  MutSelftest  ScoutSource  ConnectorCross   (+ SentinelScope, created by this seat)
$ du -sh /fast/scratch/hyaku/kaidoku-r69   → 7.1M
```
- **(observation)** Nothing exceeds 50 MB; total 7.1 MB. No clone of the lane exists (no `.git` or `*.bundle` under scratch).
- **(observation)** Every seat has its own directory named after it; L1 owns `l1/` and `after/`; `probe/` predates the wave (23:22). No seat wrote into another seat's directory.
- **(observation)** Cleanup status at audit time: `ExecC1`, `ExecC3`, `ExecRepairs`, `ScoutSource` hold live work products; `MutBattery`, `MutSelftest`, `ReviewerGates`, `ConnectorCross` are empty (created, no content yet). All seats are still running, so "delete before yield" is not yet due. **(unknown)** whether each seat deletes its dir on exit — checkable only after the wave.
- **(observation)** `/tmp` scan for kaidoku/round-69 artifacts: none. The `r69`-named files found belong to other lanes (`/tmp/mado-r69-closure.json`, mado round 69; `/tmp/gitreplace-r69.adoc`, git-replace docs; `/tmp/kaidoku-r67-closure.json`, a stale r67 closure). No >50 MB scratch in `/tmp` from this round.

### 4.1 `/tmp` strings in committed tools
```
$ grep -n '/tmp' tools/round-69/*.py
tools/round-69/contract-probe.py:85:  "HOME": os.environ.get("HOME", "/tmp"),
$ grep -n '/tmp' tools/round-68/*.py
(no output)
```
**(observation)** One literal `/tmp` in the round: a fallback `HOME` for the *instrument under test*'s child environment in `contract-probe.py:85`. It is not a scratch path, and `HOME` is set on this host, so the fallback is dead in practice. It does violate the literal rule "no /tmp paths in committed tools". **(inference)** Severity low; the clean form is `os.environ["HOME"]` or a required argument. `gen-w1.py:86,268-269` mention `/tmp` only in prose that quotes the same rule.

---

## 5. Evidence integrity (read-only observations)

### 5.1 Frozen bytes
```
sha256sum tools/round-69/{packed-elf,mutation-check,contract-probe,controls}.py
4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc  packed-elf.py
51b64c56c48899d5d2d707298431861f8465e5422e53ee7dceb903d1b56d33c2  mutation-check.py
e609d85d0fc4604ef582ae886da38b4d335c558a1954c12344df0e468669061d  contract-probe.py
1f8f78c177b33196cb2a4cb6c9c4c999e70d07c4c158ddac250dae2a0196b918  controls.py
48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e  tools/round-68/packed-elf.py
```
**(observation)** All four match `claims.json` `instrument_pins` and the assignment's declared hashes exactly; `tools/round-68/packed-elf.py` matches its stated `48ef4c68…`.
```
$ git show f1599810:tools/round-69/packed-elf.py | sha256sum   → 4ac0d83b…  (same)
$ git show HEAD:tools/round-69/packed-elf.py | sha256sum       → 4ac0d83b…  (same)
$ git show d7d9a62c:tools/round-68/packed-elf.py | sha256sum   → 48ef4c68…  (same)
$ git log --diff-filter=A --format=%H -- .ufo/waves/round-69/claims.json → f15998102f1ce3569e61faa2ac6f286bc414538e
$ git log --oneline f1599810..HEAD -- tools/round-69/ tools/round-68/ → (empty)
```
**(observation)** The freeze commit is genuinely the add-point of `claims.json`; no tool was touched after the freeze; the tools are byte-identical at freeze and at HEAD.

### 5.2 Host pins
```
sha256sum /usr/bin/upx /usr/bin/jq /usr/bin/xxd /usr/lib/libz.so.1.3.2
cf2f6e7c…  /usr/bin/upx          (root:root 0755; UPX_SHA256_PIN match)
e8156675…  /usr/bin/jq           (jq pin match)
7b1e5d0c…  /usr/bin/xxd          (xxd pin match, symlink → tinyxxd)
6c78c5e5…  /usr/lib/libz.so.1.3.2 (libz pin match; kind shared-object)
```
**(observation)** Every carrier and packer pin equals the live host bytes, including the third (shared-object) carrier. **(inference)** The pins are re-derivable on this host today.

### 5.3 Base receipts
- `l1/pre/c1-at-base.json`: `survivors` = the five declared ids, `pristine {cases: 13, ok: true}`, `ok: true`. Matches the declared base state. **(observation)**
- `l1/pre/c2-at-base.json`: `arms_passed: 0`, `target: 6`, `failed` names all six arms. **(observation)**
- `l1/pre/controls-at-base.json`: `ok: true`, seven rows including c1-do-nothing (5 survivors), c2-do-nothing (0 of 6), c3-do-nothing (target 2), synthetic-met and loose-ceiling. **(observation)**
- `l1/pre/c3-at-base.json` **was** a transcript, not JSON: a 19-line file — the command line followed by the `--check-receipt` JSON. Parsed as text it reported `target 2`, `carriers_matched 2`, `no shared-object carrier: kinds [None]`, exit 1, matching the assignment's characterisation exactly. **(observation)** A consumer that `json.load`ed it got a parse error. **Resolved at 23:40 (observation):** the transcript prefix was removed in the working tree (−1 line, uncommitted); the file now parses and reports `check R69-C3`, `target 2`, `met false`, 5 failing entries.

### 5.4 After-state (dry-run scratch only — not re-derived here)
`/fast/scratch/hyaku/kaidoku-r69/after/`:
- c1: `survivors []`, `killed` all five, `killed_wrong_case []`, `pristine {cases: 20, ok: true}`, `rev f1599810…`, each mutant `failed` naming its declared case (`arm-pack-identity-false`, `…recovery-false`, `…detected-false`, `…before-false`, `…control-false`). **(observation)** of the dry-run JSON; **not** a re-execution by this seat.
- c2: `arms_passed 6`, `target 6`, `failed []`, `rev f1599810…`. **(observation)**
- c3: `met_target true`, `carriers_matched 3`, `control_ok true`, `failing []`; per-carrier `before_ceiling_ratio` jq 0.0599, xxd 0.101, libz 0.6522 — all ≤ 0.75; kinds `{executable, shared-object}`. **(observation)**
**(inference)** The three predicates appear satisfied in dry-run form; whether the *landed* receipts reproduce them is the L1's after-run and the reviewers' re-derivation, not this audit's claim.

---

## 6. Write scope of the instruments

```
grep -nE "open\([^,)]*,\s*['\"]w|makedirs|mkdir|rmtree|remove\(|unlink|chmod|copy|write_text|write_bytes" tools/round-69/*.py
```
- **(observation)** `packed-elf.py` writes only `receipt_path` (under the per-carrier `cdir` inside `tempfile.mkdtemp(dir=work)`), `out` (`--json-out`), and removes `run_root` in a `finally`. `mutation-check.py` writes only under `work/mutation-check/` plus `--json-out`. `contract-probe.py` writes only under `work/contract-probe/` plus `--json-out`. `controls.py` writes only under `--work` plus `--json-out`. No tool writes to the lane.
- **(observation)** Git is invoked read-only: `git show <rev>:<tool>` (`contract-probe.py:167`, `mutation-check.py:110`) and `git log` (`packed-elf.py:320`). No mutating subcommand in any of the four.
- **(observation)** `contract-probe.py:172` and `mutation-check.py:124` do `shutil.rmtree` on a **fixed** name under `--work` (`contract-probe`, `mutation-check`). Two concurrent runs sharing one `--work` clobber each other; `packed-elf.py` is safe here because it uses `mkdtemp`. **(inference)** Low; only matters for parallel reuse of a work root.
- **(observation)** `contract-probe.py` hard-links host tools by symlink into `pathbin` (`git`, `readelf`, `upx`) — a deliberate PATH sandbox for A1. It does not copy user-writable binaries into it.

---

## 7. Live writes into tracked lane paths during the audit

**(observation)** Between 23:36:20 and 23:38:55 — while this audit was running — five tracked lane files were modified in the working tree and two new corpus files were created. None was committed.

| path | state | numstat | mtime |
|---|---|---|---|
| `PROVINCE.md` | M | +8 / −0 | 23:37:12 |
| `corpus/README.md` | M | +3 / −2 | 23:36:55 |
| `corpus/SOURCES.md` | M | +2 / −0 | 23:37:20 |
| `corpus/knowledge/2026-11-03-r68-packed-elf-route.md` | M | +21 / −0 | 23:38:35 |
| `tools/round-29/prefile-check.sh` | M | +16 / −10 | 23:38:55 |
| `corpus/knowledge/2026-11-03-r69-packed-route-contract.md` | ?? | 6 048 B | 23:36:20 |
| `corpus/lessons/round-69.md` | ?? | 6 696 B | 23:38:19 |

### S-0 — process / landing ambiguity (high for integrity)

- **(observation)** Every one of those seven paths is outside the assignment's declared touched set (`tools/round-69`, `plans/round-69-claims.md`, `SKILL.md`, `.ufo/waves/round-69`) and outside any seat's own `w1/<Name>/` directory. A seat writing them violates "it never edits a tracked lane file … seats return drafts and findings; the L1 lands them".
- **(observation)** `w1/ScribeKnowledge/` was created at 23:36 and is **empty**, while the round-69 knowledge entry, the lesson, the SOURCES row, the README row and the PROVINCE section all exist in the tracked corpus. **(inference)** the scribe wrote its output directly into the corpus instead of returning drafts; the draft directory is the seat's declared write surface and it holds nothing.
- **(observation)** `w1/ExecRepairs/` *does* hold a proper draft (`prefile-check.patched.sh`, sha256 `d19a6508…`) plus `evidence/patch.diff` and `evidence/redgreen.out`, yet the working-tree `tools/round-29/prefile-check.sh` is a **different edit** (sha256 `9a403dc1…`). `diff` shows different comment prose ("21 data rows whose last round is round-35" vs "21 rows (rounds 14-32, 34, 35)") and a different `${got:-absent}` branch structure. **(inference)** the in-place edit was not produced from the seat's declared draft, so there are two divergent versions of the same repair and no record of which one the round endorses.
- **(observation)** Nothing is committed, so authorship is not recorded. **(unknown)** whether the writer is a seat (a rule violation) or the L1 landing incrementally (in-role, but then it must commit and re-run the gates before filing). Either way the round's landing state is ambiguous at audit time.

### S-0b — content defect in the new README row (medium)

**(observation)** `corpus/README.md:118` is `| entry | topic | source | verified-at |` (4 cells, 5 pipes); the edit replaced the 4-column delimiter with `|---|---|---|` at line 119 (3 cells, 4 pipes) while every data row has 4 cells. GFM requires the delimiter to match the header; the fourth header cell (`verified-at`) falls outside the declared columns. The same edit also moved the r68 row below the delimiter (a genuine fix), but introduced this regression. Fix: restore `|---|---|---|---|`.

### S-0c — a stale registered pin, now doubly stale (medium; pre-existing)

**(observation)** `SKILL.md:1363` pins `tools/round-29/prefile-check.sh` at sha256 `5c3586b2…`. Hashing every historical blob shows that value is the **round-29 landing version** (`2f18996d`). HEAD (`978436bd`, the round-68 landing) already carried a different version (`56957693…`), so the pin was stale before this round; the in-place round-69 edit makes the file a third value (`9a403dc1…`). **(inference)** Landing must refresh the row's pin (and its behaviour/date cell), or the registry row states a hash the file never had.

### S-0d — the hygiene gate is red at HEAD for exactly one reason (observation)

```
$ python3 -I -B tools/round-29/freeze-gate.py --root . --rev 3f3d20fc… --disclosures corpus/claim-freezes-v2.tsv
{"audited": 44, "clean": 21, "disclosures": {"exact": 43, "mismatched": [], "missing": ["round-69"],
 "of": 44, "path": "corpus/claim-freezes-v2.tsv", "present": true, "stray": []}, ...}
EXIT=1
```
The sole disclosure failure is the absent `round-69` row in `corpus/claim-freezes-v2.tsv` (`mismatched []`, `stray []`). `freeze-gate.py` itself hashes to its `SKILL.md` pin (`25b54339…`). **(observation)** The ExecRepairs `redgreen.out` shows the same exit 1 for both the original and the patched gate at HEAD, so the redness is not caused by the repair. **Later observation (23:40):** a `round-69` row was appended to the ledger in the working tree (`round-69 FLAGGED INSTRUMENT_NONE`, disclosing that the gate reads top-level `instruments` while the container uses `instrument_pins`), but it is **uncommitted**, and the gate reads the file at `--rev` — so at HEAD the result is unchanged: `missing ["round-69"]`, exit 1. **(unknown)** whether the disclosure step turns green once the row is committed; the L1 must commit and re-run. **(inference)** Until then the round cannot claim the prefile gate passes: `prefile-check.sh` additionally reports "tree NOT CLEAN" while these edits sit uncommitted.

### 23:40–23:41 snapshot (observation)

Four further tracked changes landed while this audit was closing: `LOG.md` (+9), `corpus/QUALITY.md` (+2), `corpus/claim-freezes-v2.tsv` (+1 row, `round-69 FLAGGED INSTRUMENT_NONE`), and `.ufo/waves/round-69/l1/pre/c3-at-base.json` (−1 line: the transcript prefix, making it pure JSON). The pattern — LOG, QUALITY, the ledger row and a base receipt — is L1-typical landing work, and it strengthens the "L1 landing incrementally" branch of the attribution question above, without proving it.

The two scribe seats' drafts also appeared in their own wave directories at 23:40–23:41 (`ScribeKnowledge/entry.md`, 22 145 B; `ScribeLesson/lesson.md` 14 283 B, `sources-opened.md` 3 655 B, `fetches.json` 1 004 B). **(observation)** Those mtimes are 2–5 minutes **after** the corpus copies (23:36:20–23:38:35), so the corpus copies cannot have been read from these drafts; authorship of the corpus writes remains **(unknown)** and the L1 must own the landing.

## Verdict

The **committed** round is correctly rooted and frozen: every path in `d7d9a62..HEAD` is inside the lane and inside the allowed set; no fleet-root or cross-lane write appears in Git; all four instrument pins, the round-68 pin and the three carrier pins match the live bytes; the freeze commit is the true add-point of the container and nothing touched the tools after it; no credential material was committed; scratch is inside its budget and no `/tmp` scratch was used.

The **working tree at 23:39** is not clean, however: five tracked files and two new corpus files were written directly into the tracked lane (§7), outside the declared path list and outside every seat's `w1/<Name>/` draft surface, and remain uncommitted. That is an integrity finding against the *process*, not against the three claims' inputs: none of those paths is an instrument the claims run, and the frozen tool bytes are unaffected. It must be resolved before filing — either the L1 owns and commits the landing (and refreshes the stale `prefile-check.sh` pin, S-0c), or the writes are reverted to drafts. Related content defects: the README delimiter regression (S-0b) and the prefile gate's red disclosure state, whose sole cause is the not-yet-landed `round-69` ledger row (S-0d).

Two defects in the `--upx` seam survive the claim as written and should be recorded even though they do not falsify R69-C1/C2/C3:

- **S-1 (high for the seam contract; not reachable in the lane's own invocation).** `preflight()` executes the caller-supplied `--upx` for `--version` *before* the sha256 pin check, with the full parent environment inherited (provider tokens, `SSH_AUTH_SOCK`, op-vault tokens) and no confinement. A hostile binary gets RCE and credential access before any refusal; a self-restoring binary can satisfy both pins and leave a clean-looking receipt. The pin makes the *work* safe (the pack/list/unpack calls use the pinned global), not the *seam*. Smallest fix: hash first, then exec.
- **S-2 (low).** `preflight(upx)` validates one path while the carrier loop executes the module global `/usr/bin/upx`; immaterial under byte-identity, but the parameter is a footgun and the recorded packer is not necessarily the binary that packed.

Minor observations: one dead `/tmp` HOME fallback (`contract-probe.py:85`); fixed-name `rmtree` under `--work` in two tools; the C3 base receipt was a transcript until 23:40 and is now pure JSON (uncommitted); a pre-existing 24-byte fleet-root stray (`after`, 20:05) that names neither the lane nor the round and was left in place.
