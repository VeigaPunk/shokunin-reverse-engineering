FALSIFIED — the NEW C2v3 negative-assessment/all-false control met the frozen target, despite all four descriptions explicitly denying demonstration and capability.

# A2C2False — attempt-2 pre-data control

- UTC scoring interval: 2026-10-23T06:47:20.941072Z–2026-10-23T06:47:21.012394Z.
- Axes: **calibration** (exercised: discrimination between capability credit and explicit denial); **coverage** (C1 ARM64X, not exercised). No coverage, depth, saturation, admission, or learning-improvement conclusion is drawn.
- Own sandbox: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone`.
- Frozen parent: `f382e3b7978e6091a19ca93277c15a75c0016b43`.
- Base: `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.
- Committed control revision: `42d814ff5f46ac45bf2b6f9b659ac094bca88f61`.
- Fleet pin read by the unchanged counter: `cef00867ab3279ac2c2d10421e3e62c0e5d693f3`; `MANIFEST.json` Git blob `e6fc0394f5d5d49c665b8575500d3caff182a427`.
- Observed target: `statements=4 match=4 target=4 reverse_mismatch=0`, **exit 0**. One scoring run; no prediction substituted for execution and no retry.

## Counterexample and bounded finding

The fixture retains the four frozen capability identities, resolving frozen anchors, and historical round labels (`arc3-loop1-round13`, `round-14`, `round-17`, `round 27`). Every what-it-can-do cell starts with the exact denial `This capability was never demonstrated and cannot capture anything.` Each then denies the corresponding operation using relevant vocabulary. The counter nevertheless credits all four rows, reporting shared-word counts 8, 12, 12, and 11.

Only `SCORECARD.md` was committed. The four-row control deliberately replaces the whole summary table, including removal of four out-of-statement-set rows and the inherited demonstration sentence; this is a negative control, not an honest repertoire repair or production candidate. The full generated section and exact diff below disclose those deletions.

The bounded defect is **false calibration credit under negative assessment**. This is not a claim that the counter violates its literal frozen overlap predicate: its implemented word-set intersection ignores the polarity of these sentences. It is evidence that meeting that predicate does not distinguish this all-false assessment from capability reconciliation. No anchor tool was executed, and this control does not assess whether the historical capabilities actually work.

Re-opened source evidence (2026-10-23 UTC; freeze `f382e3b7978e6091a19ca93277c15a75c0016b43`; counter SHA-256 `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f`):

- [Frozen counter, lines 125–137](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone/tools/round-32/c2-capability-calibration-v3.py#L125-L137): word extraction and description word-set construction.
- [Frozen counter, lines 163–171](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone/tools/round-32/c2-capability-calibration-v3.py#L163-L171): `shared = words(cells[1]) & desc_anchor_words(item, pats[0], base_scorecard)`; acceptance follows the minimum shared-word check.

**Smallest safe correction under this freeze:** retain this as an honest-stop finding; do not edit the counter, predicate, target, or promote the control as data/repair. Any future semantic-polarity criterion would require a separately frozen attempt. Current disposition belongs to the canonical Rust judge; this report makes no admission or integration decision.

## Exact scoring invocation and output

Working directory: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone`.

Environment: inherited environment with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed. Executed argv (no shell expansion):

```json
["timeout", "--kill-after=5s", "300", "prlimit", "--as=4294967296", "--", "python3", "-I", "-B", "tools/round-32/c2-capability-calibration-v3.py", "--root", "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone", "--rev", "42d814ff5f46ac45bf2b6f9b659ac094bca88f61", "--fleet", "/home/vgpnk/Projects/shokunin"]
```

Observed exit: **0**. Full stdout (tab-separated):

```text
round-13	P2-match	row 1 anchor evidence corpus/SOURCES.md, corpus/lessons/round-13.md; description words 8
round-14	P2-match	row 2 anchor evidence .ufo/waves/round-14/fixtures/expected.json, .ufo/waves/round-14/tools/quote-fidelity.py, .ufo/waves/round-14/verification.json; description words 12
round-17	P2-match	row 3 anchor evidence .ufo/waves/round-17/run-carriers.sh; description words 12
round-27	P2-match	row 4 anchor evidence tools/round-27/xpin-attribute.mjs; description words 11
statements=4 match=4 target=4 reverse_mismatch=0
```

Full stderr: empty. Target verdict: **MET by a vocabulary-only negative control; FALSIFIED / honest-stop finding, not a successful repair**.

The scoring subprocess was started in its own process group. Cleanup attempted `SIGKILL` on that owned group after collection; observed `ProcessLookupError` (group absent after exit). The same cleanup observation applied to staging, commit, revision lookup, and diff capture. No process tree remains from these captured commands.

## Complete generated section — retained fixture bytes

The following UTF-8/LF content is the entire generated `## Capabilities` section, including the final blank line before `## Saturation`. The rest of the parent file is reconstructible from the exact diff below. New source file size remains below 1 MiB (parent size observed: 274232 bytes).

```markdown
## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| curated source registry for existing REA frontier | This capability was never demonstrated and cannot capture anything. It cannot retain opened, scoped study sources, ordered paths, or recheck cadences. | `corpus/SOURCES.md`; `corpus/lessons/round-13.md` | arc3-loop1-round13 |
| local raw-quote/heading regression audit | This capability was never demonstrated and cannot capture anything. It cannot reject the retained splice or wrong section, accept corrected controls, refuse malformed/tampered inputs, or pin frozen manifest/source inputs. | `.ufo/waves/round-14/tools/quote-fidelity.py`; `.ufo/waves/round-14/fixtures/expected.json`; `.ufo/waves/round-14/verification.json` | round-14 |
| retained REA Ghidra-session log capture | This capability was never demonstrated and cannot capture anything. It does not run analyze on a pinned carrier in a private-TMPDIR session and never keeps ghidra.log or script.log; no receipt validates offline. | `.ufo/waves/round-17/run-carriers.sh` | round-17 |
| cross-pin evidence-ID attribution for saved REA envelopes | This capability was never demonstrated and cannot capture anything. It cannot attribute a saved envelope from its bytes using an installed package's canonical digest code, under either rule. | `tools/round-27/xpin-attribute.mjs` | round 27 |

```

## Exact committed diff

Captured 2026-10-23T06:47:20.937558Z–06:47:20.941009Z; exit 0; stderr empty. Exact argv:

```json
["timeout", "--kill-after=5s", "900", "prlimit", "--as=4294967296", "--", "git", "-C", "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone", "diff", "--no-ext-diff", "--unified=3", "f382e3b7978e6091a19ca93277c15a75c0016b43", "42d814ff5f46ac45bf2b6f9b659ac094bca88f61", "--", "SCORECARD.md"]
```

Full diff stdout (raw generated artifact, not an additional source assessment):

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index e90a5a01..5883c84c 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -616,13 +616,10 @@ Retired: none.
 
 | Capability | What it can now do | Evidence pointer | First-working round |
 |---|---|---|---|
-| pre-registered two-lane live battery on REA 6.5.0 | runs a 10-leg frozen-prediction battery with hashed per-lane receipts and cross-lane replay verification | `.ufo/waves/luna-round-6/receipts/` + `receipts-B/`; report `.ufo/reports/luna-round-6/kaidoku.md` | luna-round-6 |
-| version-symmetry battery on REA 6.4.0 | repeats the battery form on the second pin, proving per-name 6.5-only absence/refusal with a live control leg | `.ufo/waves/luna-round-8/receipts/`; `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md` | luna-round-8 |
-| config custody pre/post-pair for live-probe rounds | freezes the five operator paths' sha256s — the three client configs (Devin mcp_config.json, OMP mcp.json, Kimi config.toml) plus the two shell env carriers (~/.bashrc, ~/.profile) — before the round's first probe and re-verifies byte-identity after the battery closes, producing a zero-drift 6-line 5-hash receipt pair | `.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt` + `config-post-pair.txt`; comparison in `.ufo/reports/arc2-loop1-round2/kaidoku.md` | arc2-loop1-round2 |
-| contained user-service analyze of oversized PEs (analyzer-disable recipe) | runs REA/Ghidra analyzes of 91.6MB-class PEs as caller-independent systemd user services with registry-validated analyzer disables and memory caps — the paired demonstrations: r7 wall-fall (ev_a4aa9b0d…) and the r8 natural control (oom-kill; disable proven necessary) | `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` + `.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json` | arc2-loop1-round7 |
-| cross-pin evidence-ID attribution for saved REA envelopes | attributes a saved envelope to the `rea-agents` 6.5.0 id rule, the 6.7.0 rule, both or neither, from its bytes, using each installed package's own canonical digest code | `tools/round-27/xpin-attribute.mjs`; checker `tools/round-27/c2-xpin-check.py`; seat report `.ufo/waves/round-27/w1/BuildXpinTool.md`; receipts `corpus/evidence/round-27/c2/` | round 27 |
-
-Rows entered through rounds that demonstrated each capability running (`AXES.md` §Capabilities); the conformance rollout itself entered none.
+| curated source registry for existing REA frontier | This capability was never demonstrated and cannot capture anything. It cannot retain opened, scoped study sources, ordered paths, or recheck cadences. | `corpus/SOURCES.md`; `corpus/lessons/round-13.md` | arc3-loop1-round13 |
+| local raw-quote/heading regression audit | This capability was never demonstrated and cannot capture anything. It cannot reject the retained splice or wrong section, accept corrected controls, refuse malformed/tampered inputs, or pin frozen manifest/source inputs. | `.ufo/waves/round-14/tools/quote-fidelity.py`; `.ufo/waves/round-14/fixtures/expected.json`; `.ufo/waves/round-14/verification.json` | round-14 |
+| retained REA Ghidra-session log capture | This capability was never demonstrated and cannot capture anything. It does not run analyze on a pinned carrier in a private-TMPDIR session and never keeps ghidra.log or script.log; no receipt validates offline. | `.ufo/waves/round-17/run-carriers.sh` | round-17 |
+| cross-pin evidence-ID attribution for saved REA envelopes | This capability was never demonstrated and cannot capture anything. It cannot attribute a saved envelope from its bytes using an installed package's canonical digest code, under either rule. | `tools/round-27/xpin-attribute.mjs` | round 27 |
 
 ## Saturation
 
```

## Sandbox creation and commit receipts

Before cloning, at 2026-10-23T06:45:05Z, `df -h /fast` exited 0:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  559G  245G  70% /fast
```

Exact setup commands, all exit 0 (Git environment variables unset as above):

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 prlimit --as=4294967296 -- git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 prlimit --as=4294967296 -- git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone checkout --detach f382e3b7
```

Clone output: `Cloning into '/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone'...` then `done.` Checkout output identified `f382e3b7`; `git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone rev-parse HEAD` returned `f382e3b7978e6091a19ca93277c15a75c0016b43`.

The scoped edit replaced original `SCORECARD.md:619–625` with the four retained fixture rows above. Commit commands, executed with the three Git environment variables unset:

```text
timeout --kill-after=5s 900 prlimit --as=4294967296 -- git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone add -- SCORECARD.md
timeout --kill-after=5s 900 prlimit --as=4294967296 -- git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone -c 'user.name=R32 A2C2False control' -c user.email=r32-a2c2false@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -m 'R32 C2v3 negative-assessment all-false control'
timeout --kill-after=5s 900 prlimit --as=4294967296 -- git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2False/clone rev-parse HEAD
```

Staging: 2026-10-23T06:47:19.016648Z–06:47:20.921985Z; exit 0; stdout/stderr empty.

Commit: 2026-10-23T06:47:20.922061Z–06:47:20.935207Z; exit 0; stderr empty; full stdout:

```text
[detached HEAD 42d814f] R32 C2v3 negative-assessment all-false control
 1 file changed, 4 insertions(+), 7 deletions(-)
```

Revision lookup: 2026-10-23T06:47:20.935309Z–06:47:20.937487Z; exit 0; stderr empty; stdout `42d814ff5f46ac45bf2b6f9b659ac094bca88f61` plus LF.

## SHA-256 provenance

Observed with `sha256sum` against the sandbox files, exit 0. Paths below are relative to the sandbox root. Counter and claim hashes were observed both before and after scoring and are unchanged. The counter hash equals the frozen instrument hash in `claims-v3.json`.

```text
bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3  SCORECARD.md at frozen parent
201a320ee75c92fd85ac139943036fbc936b6878dbf0b071229e68db70421796  SCORECARD.md at control revision
5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f  tools/round-32/c2-capability-calibration-v3.py
a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d  .ufo/waves/round-32/claims-v3.json
4bf494f8c38b6bfb44980f5b3f493063fc08d50aad8ce9f867907a57654e3970  corpus/SOURCES.md
b2ae45a87e574a25a0ba1505014b9909d3b3dd1a3741db01e20a9a260994ffb3  corpus/lessons/round-13.md
0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8  .ufo/waves/round-14/tools/quote-fidelity.py
ef3714bbb77df1f03db0de325f6c49ea1a8bbf66a1fdeecdd2e8bb3d5474cadf  .ufo/waves/round-14/fixtures/expected.json
dd1c57912a98039af99985063dc7e08697b836bbd41ef8e50b18062f2a5a5a9c  .ufo/waves/round-14/verification.json
acc2769354d452733bd7b70b3a09fadead423a7b5b390758ce589e71eb4d093b  .ufo/waves/round-17/run-carriers.sh
8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708  tools/round-27/xpin-attribute.mjs
```

Tools observed: existing Python 3.14.8 and Git 2.56.0. Installs/updates: **none**. No pacman transaction. No REA/Ghidra/carrier execution, delegation, routing change, or lane/fleet Git write. Only this report is written in the lane; all control changes and Git writes are inside the assigned sandbox. No unrelated verification was run.

Report: .ufo/waves/round-32/a2audit/A2C2False.md
