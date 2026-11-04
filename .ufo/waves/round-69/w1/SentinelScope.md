# SentinelScope — round-69 w1 scope and safety audit

Seat: SentinelScope (sentinel). Lane: kaidoku-shokunin. Round 69, wave w1.
Base `d7d9a62cc70935304e600ed0dee864fc4f1751f7`; operative freeze `f15998102f1ce3569e61faa2ac6f286bc414538e`.
Full command log and raw results: `.ufo/waves/round-69/w1/SentinelScope/audit.md`.
Labels: **(observation)** directly seen; **(inference)** derived from code/evidence; **(unknown)** not established.

## Verdict

**Scope: the committed round is clean; the working tree at audit close was not. Safety: one high-severity ordering defect in the `--upx` seam, not reachable through the lane's own invocation.** The committed diff is correctly rooted and frozen; the three claims' base/after states are internally consistent; no credential material, no cross-lane write and no `/tmp` scratch escape was found. However, **five tracked lane files and two new corpus files were written directly into the tracked tree at 23:36–23:39, outside the declared path list and outside any seat's draft directory, and remain uncommitted** (S-0); one of those edits regresses a Markdown table (S-0b), the repair's registered pin was already stale (S-0c), and the prefile hygiene gate is red at HEAD solely for the missing round-69 ledger row (S-0d). Those are process/landing findings, not defects in the three claims' instruments. The `--upx` seam defect does not falsify R69-C1/C2/C3 as written, but it means "the enforced UPX pin" is enforcement of *use*, not of *execution*, and A4's kill is not evidence of safety.

## Findings

### S-0 — HIGH (process integrity) — five tracked lane files and two new corpus files written mid-wave, uncommitted, outside the declared path list

**Evidence (observation).** At 23:33 the tracked tree was clean; at 23:39 `git status --porcelain --untracked-files=no` reported five modifications:

| path | numstat | mtime | what it contains |
|---|---|---|---|
| `PROVINCE.md` | +8 | 23:37:12 | a new "Round-69 additions to Core" section and frontier note (S270, `2026-11-03-r69-packed-route-contract`) |
| `corpus/README.md` | +3/−2 | 23:36:55 | a new round-69 knowledge-index row, the r68 row moved below the delimiter, and the delimiter itself changed from 4 to 3 columns |
| `corpus/SOURCES.md` | +2 | 23:37:20 | new row S270 (UPX 5.2.0 `doc/upx.1`) |
| `corpus/knowledge/2026-11-03-r68-packed-elf-route.md` | +21 | 23:38:35 | an appended round-69 correction block (provenance trio, S269 word-count label fix) |
| `tools/round-29/prefile-check.sh` | +16/−10 | 23:38:55 | the R68-V4 repair to the ledger1 branch |

plus two new untracked corpus files: `corpus/knowledge/2026-11-03-r69-packed-route-contract.md` (23:36:20) and `corpus/lessons/round-69.md` (23:38:19).

**Why it matters.** (a) Every path is outside this seat's allowed write set and outside the assignment's declared touched set; (b) `w1/ScribeKnowledge/` was created at 23:36 and is **empty**, while the scribe's corpus output exists in the tracked tree — the draft directory is the seat's declared write surface; (c) `w1/ExecRepairs/` holds a proper draft `prefile-check.patched.sh` (sha256 `d19a6508…`) plus a patch and a red/green log, but the **working-tree** `tools/round-29/prefile-check.sh` is a *different* edit (`9a403dc1…`): the comment prose and the `${got:-absent}` branch structure differ, so the applied edit did not come from the endorsed draft; (d) nothing is committed, so authorship is unrecorded. **(unknown)** whether the writer is a seat (rule violation) or the L1 landing incrementally (in-role, but then it must commit and re-run the gates).

**23:40–23:41 closure (observation).** Four more tracked changes appeared — `LOG.md` +9, `corpus/QUALITY.md` +2, `corpus/claim-freezes-v2.tsv` +1 row, `c3-at-base.json` −1 line — and the two scribe seats' drafts showed up in their own wave directories (`ScribeKnowledge/entry.md` 22 KB; `ScribeLesson/lesson.md` 14 KB, `sources-opened.md`, `fetches.json`). The drafts' mtimes are 2–5 minutes **after** the corpus copies, so the corpus copies cannot have been read from them. The L1-typical pattern (LOG, QUALITY, ledger, receipt) makes the incremental-L1 branch the more likely one; authorship is still unrecorded and the tree is still uncommitted.

**Remediation.** The L1 must own the writes: either commit them as the landing (refreshing the `prefile-check.sh` pin, S-0c, and restoring the README delimiter, S-0b) or revert them and land the seat drafts. Nothing here touches the three claims' instruments — the frozen bytes are unaffected — but the round cannot be filed with an ambiguous working tree.

### S-0b — MEDIUM — the new README row breaks the table delimiter

**Evidence (observation).** `corpus/README.md:118` is `| entry | topic | source | verified-at |` (4 cells) but line 119 is `|---|---|---|` (3 cells) while every data row has 4. The edit replaced `|---|---|---|---|` with the short form. GFM aligns by the delimiter row, so the `verified-at` column is undeclared for the whole table.
**Remediation.** Restore `|---|---|---|---|`.

### S-0c — MEDIUM (pre-existing, now doubly stale) — the round-29 gate's registered pin is not the file at HEAD

**Evidence (observation).** `SKILL.md:1363` pins `tools/round-29/prefile-check.sh` at `5c3586b2…`; hashing every historical blob shows that is the round-29 landing version (`2f18996d`). HEAD's version (`978436bd`, round-68 landing) is `56957693…`, and the working tree is now `9a403dc1…`. The `freeze-gate.py` pin (`25b54339…`) is correct.
**Remediation.** Landing must refresh the row's pin and its behaviour/date cell to the landed bytes.

### S-0d — INFO/OBSERVATION — the hygiene gate is red at HEAD for exactly one reason

```
$ python3 -I -B tools/round-29/freeze-gate.py --root . --rev 3f3d20fc… --disclosures corpus/claim-freezes-v2.tsv
{"audited": 44, "clean": 21, "disclosures": {"exact": 43, "mismatched": [], "missing": ["round-69"],
 "of": 44, "stray": []}, ...}   EXIT=1
```
The only disclosure failure is the absent `round-69` row in `corpus/claim-freezes-v2.tsv`; `mismatched` and `stray` are empty. The ExecRepairs red/green log shows the same exit 1 for both the original and the patched gate, so the repair did not cause it. At 23:40 a `round-69` row was appended in the working tree (`round-69 FLAGGED INSTRUMENT_NONE`) but is still uncommitted, and the gate reads the file at `--rev` — so at HEAD the result is unchanged, `missing ["round-69"]`, exit 1.
**Remediation.** Commit the round-69 disclosure row at landing, then re-run `sh tools/round-29/prefile-check.sh <lane>` on a clean tree. **(unknown)** whether the disclosure step then turns green: the row's own verdict is `FLAGGED INSTRUMENT_NONE` (the container uses `instrument_pins`, the gate reads top-level `instruments`), and the gate must be allowed to say so. Until it is committed and re-run, no hygiene claim is supported.

### S-1 — HIGH (seam contract) — `--upx` is executed before its pin is checked, with the full environment inherited

**Evidence (observation).** `tools/round-69/packed-elf.py:253-259`:
```python
version = run([upx, "--version"]).get("stdout", "").strip().splitlines()  # EXECUTES caller-supplied bytes
if version != UPX_VERSION_PIN: raise Unevaluable(...)
sha = sha256_file(upx)                                                    # hashes AFTER execution
if sha != UPX_SHA256_PIN: raise Unevaluable(...)
```
`run()` (`:185-189`) is `subprocess.run(argv, capture_output=True, text=True, timeout=900)` — **no `env=`, no privilege drop, no sandbox**. `env | cut -d= -f1` on the host lists `OPENAI_CODEX_TOKEN`, `XAI_OAUTH_TOKEN`, `OP_SERVICE_ACCOUNT_TOKEN`, `OPKEY_VAULT`, `SSH_AUTH_SOCK`, `STARSHIP_SESSION_KEY`, `PI_SESSION_ID`, `PI_SESSION_FILE`. The contract probe's A4 arm builds `/usr/bin/upx` + one NUL and passes it as `--upx` (`contract-probe.py:190-196`); the instrument executes it and only then refuses — the arm scores "killed" because the message names `sha256`, not because nothing ran.

**Exploit path (inference from the code order; not executed).** A caller — or any config/env path that resolves `--upx` — points the seam at attacker-owned bytes. Before any refusal: (1) arbitrary code executes as the invoking user; (2) the child reads every token in the inherited environment and exfiltrates over the network; (3) it can read/write the lane including `.git/hooks`, other lanes, `~/.ssh`, `~/.local/bin` on PATH for persistence; (4) it can fork/daemonize so it survives `subprocess.run`, which captures only this child's pipes; (5) it can stall the route for 900 s per call. Sharpest form: the binary prints `upx 5.2.0`, then restores the pinned bytes over its own path (readable `/usr/bin/upx`, root:root 0755) before the parent reaches `sha256_file()` — both pins then pass, `pin_enforced` is recorded true, the carrier loop runs the pinned global, and **the receipt contains no trace that hostile code ran**. A6 would pass because it compares the receipt against `sha256_file("/usr/bin/upx")`, which is the restored pinned file.

**Impact.** Full local RCE and provider/SSH credential theft for any third party that re-runs the instrument with an untrusted `--upx`. For this lane's own runs the exposure is nil: the L1 never passes `--upx`; the default is `/usr/bin/upx`, root:root 0755, sha256 `cf2f6e7c…` = pin. The claim-level impact is evidentiary: R69-C2's "enforced UPX pin" and arm A4 cannot be read as a safety property.

**Smallest remediation.** In `preflight()`, compute and compare `sha256_file(upx)` **before** `run([upx, "--version"])`; keep the banner check after. Three lines reordered, no semantic change to the six arms. Optional: pass a minimal `env=` to the packer calls.

### S-2 — LOW — validated packer path ≠ executed packer path

**Evidence (observation).** `score(..., upx=UPX)` passes `upx` only to `preflight()`. Every carrier-loop call — `:387` (`--best`), `:391` (`-l`), `:397` (`-d`), `:411`, `:412` — uses the module global `UPX = "/usr/bin/upx"`. A caller passing `--upx /opt/copy` with byte-identical content gets a receipt naming `/opt/copy` while the pack ran `/usr/bin/upx`.
**Impact.** None for the pins (content hash; A6 cross-checks against the host file, so a *different* binary fails A6). **(inference)** A footgun rather than a live defect.
**Remediation.** Thread the validated `upx` variable through the carrier loop instead of the global.

### S-3 — LOW — one `/tmp` literal in a committed tool

**Evidence (observation).** `grep -n '/tmp' tools/round-69/*.py` → only `contract-probe.py:85`: `"HOME": os.environ.get("HOME", "/tmp")`, a fallback in the env handed to the instrument under test. Not a scratch path; `HOME` is set on this host, so the fallback is dead. `tools/round-68/*.py` has none.
**Impact.** Violates the literal "no /tmp paths in committed tools" rule; no observed write lands there.
**Remediation.** `os.environ["HOME"]` or a required `--home`.

### S-4 — LOW — fixed-name work subdirectories are deleted on each run

**Evidence (observation).** `contract-probe.py:172` and `mutation-check.py:124` do `shutil.rmtree(work/<fixed-name>)` then `makedirs`. Two concurrent runs sharing a `--work` clobber each other. `packed-elf.py` is safe (`tempfile.mkdtemp(dir=work)` + `finally` rmtree).
**Impact.** Concurrency only, inside the caller's declared work root.
**Remediation.** `mkdtemp(prefix=..., dir=work)` in both.

### S-5 — INFO — `c3-at-base.json` is a transcript, not JSON

**Evidence (observation).** The 502-byte file is the command line plus the `--check-receipt` JSON; `json.load` fails. Parsed as text it reports `target 2`, `carriers_matched 2`, `no shared-object carrier: kinds [None]`, exit 1 — exactly the declared base state.
**Impact.** A machine consumer of the base receipt must strip the first line. As evidence-of-record it is faithful.
**Remediation.** Record future base checks with `--json-out` beside the transcript, or prefix the transcript with a marker. **Resolved at 23:40 (observation):** the transcript prefix was removed in the working tree; the file is now pure JSON and parses (`check R69-C3`, `target 2`, `met false`, 5 failing). The change is uncommitted.

## Scope checks (all observed clean)

| Check | Result |
|---|---|
| Lane `git status --porcelain` | At 23:33: no tracked file modified; only dispatcher markers and the untracked `w1/` draft tree. At 23:39: **5 tracked files modified + 2 new corpus files, uncommitted** — see S-0. |
| `diff --stat base..main` | 16 files, all inside the lane, all in the allowed set (`tools/round-69`, `plans/round-69-claims.md`, `SKILL.md`, `.ufo/waves/round-69`). `tools/round-68/` absent → untouched. |
| Fleet root misroot scan | No kaidoku round-69 artifact outside the lane. `r69`-named files elsewhere belong to audio-shokunin's own round 69, mado's round 69 (`/tmp`), or fleet-level prompts/reports. One pre-existing stray: fleet-root file `after` (24 bytes, `== SCORECARD diff base-`, 20:05 — three hours before the wave), names neither lane nor round; reported, not deleted. |
| Frozen pins | All four round-69 tools hash to their `claims.json` pins and to the assignment's declared values; `tools/round-68/packed-elf.py` = `48ef4c68…`; the blobs at freeze and at HEAD are identical; `claims.json`'s add-point is `f1599810…`; no tool commit after the freeze. |
| Host pins | `/usr/bin/upx`, `/usr/bin/jq`, `/usr/bin/xxd`, `/usr/lib/libz.so.1.3.2` each hash to their declared pins; upx is root:root 0755. |
| Credentials | Tight scan (gh*/sk-*/xox*/AKIA/private-key/Bearer) over all 16 changed files: no hits. Prose mentions of "token"/"session" only. |
| Scratch | 7.1 MB total; per-seat dirs only; no lane clone; four seat dirs still hold live work, four empty, all seats still running — cleanup not yet due; no kaidoku round-69 artifacts in `/tmp`. |
| Tool write scope | The four instruments write only under `--work`, `--json-out`, and `tempfile.mkdtemp(dir=work)`; git is only `show`/`log`. No tool writes to the lane. |
| Tool-dir hygiene | `tools/*/__pycache__` exists but `__pycache__/` and `*.pyc` are gitignored; nothing tracked. |
| Base receipts | c1 (`survivors` five, `pristine.cases` 13), c2 (0 of 6, all six named), controls (seven arms, `ok true`) all match the declared base state; c3 transcript matches `target 2`, exit 1. |
| After state (dry-run scratch, **not re-derived here**) | c1 `survivors []`, five kills each naming its declared arm-false case, `pristine.cases` 20; c2 6 of 6; c3 `met true`, `carriers_matched 3`, `control_ok true`, ratios 0.0599 / 0.101 / 0.6522 ≤ 0.75, kinds `{executable, shared-object}`. Recorded as observation of `/fast/scratch/.../after/`, not as this seat's verification. |

## Limits of this audit

- The seam exploit path is reasoned from the source ordering (S-1), not executed; running hostile bytes was out of bounds for this seat and unnecessary for the conclusion.
- I did not re-run any of the frozen instruments against the carriers. Every "met" statement about the three claims above is a reading of existing JSON, labelled as such; the L1's landed after-receipts and the reviewers' re-derivations carry that authority.
- Cleanup of the scratch tree is checkable only after the wave; at audit time all seats were still live, so `MutBattery`, `MutSelftest`, `ReviewerGates`, `ConnectorCross` being empty is not a violation.
- Tooling: no install or upgrade was needed or performed.
