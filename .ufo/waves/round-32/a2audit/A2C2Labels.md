FALSIFIED — NEW C2v3 Labels control meets the frozen target with four alphabetically sorted, five-token vocabulary bags instead of capability descriptions; exit 0. Honest-stop finding; counter/predicate/target unchanged.

# A2C2Labels — attempt-2 pre-data control

UTC receipt: 2026-10-23T06:47:53.457899+00:00 → 2026-10-23T06:47:53.526981+00:00.

## Axes and bounded finding

- **Calibration (R32-C2/P2-match): exercised.** Four distinct correct capability names and rounds, all frozen anchor paths resolving, and exactly five shared description tokens per row produce `statements=4 match=4 target=4 reverse_mismatch=0`, exit 0.
- **Coverage (R32-C1/ARM64X Frontier→Core): not exercised or changed.** C1 freeze read; no carrier, REA run, or C1 counter involved.
- **Depth: not measured.** No repertoire gain or domain mastery claimed.

Counterexample: each second cell is `" ".join(sorted(desc_anchor_words(item, key, base_scorecard))[:5])`, using the unmodified frozen counter's tokenizer and anchor-word function. The resulting five-word sets are shown verbatim below. They are id/key-selected vocabulary, not an attempted honest repair. [INFERENCE] The sorted fragments do not state what a capability can do, so this passing control does not establish semantic calibration.

Smallest safe correction: stop C2v3 under its frozen rule and preserve this falsifier. Do not amend the predicate, counter, labels, anchors, target, or this control to rescue the claim. No data/repair attempted. The observed issue is non-discrimination of the explicitly frozen overlap rule, not evidence of an implementation/predicate mismatch. No canonical admission judgment was run.

## Identity, bounds, and provenance

- New clone: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone`.
- Base: `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.
- C1 freeze: `9a73680a` (unchanged; no scoring here).
- C2v3 checkout/parent: `f382e3b7978e6091a19ca93277c15a75c0016b43`.
- Sandbox committed control revision: `cbb7dbce50861117076e57d42ec5f471f71bd413`.
- Fleet MANIFEST pin: `cef00867ab3279ac2c2d10421e3e62c0e5d693f3`.
- Only committed sandbox change: `SCORECARD.md`, 4 insertions and 5 deletions. The isolated fixture replaces the original five summary rows with the four controlled rows; it does not add real capabilities or preserve the unrelated summary rows as a production change.
- All Git writes confined to this clone. Git environment keys `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` removed for Git subprocesses and the counter.
- `df -h /fast` before clone: `/dev/nvme1n1p2 804G 559G 245G 70% /fast`; no rebuild.
- One counter run only: timeout 300 seconds, address-space cap 4,294,967,296 bytes; no Ghidra, carrier execution, held-item inspection, or delegated runtime.
- Counter subprocess started in its own process group; completion cleanup attempted SIGKILL on that group and observed `ProcessLookupError` (group absent). All other launched commands returned synchronously.
- No installs/updates. Observed tools: Python 3.14.8; Git 2.56.0; `prlimit` util-linux 2.42.4. Ancillary `timeout --version` returned exit 125 (command requires duration/command); no counter retry followed from that ancillary query.

### SHA-256 identities

```text
bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3  base/freeze SCORECARD.md
593c42f58a5206ec74fd21c0084bb39c11fc372dad3c7b108b9ad541cacc8821  control SCORECARD.md
c58aa1e2c0d6936123f82ad65641760b281b3c5960d0306c26cef46e7809065e  Labels-Capabilities.section.txt
5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f  tools/round-32/c2-capability-calibration-v3.py (before and after commit)
a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d  .ufo/waves/round-32/claims-v3.json (before and after commit)
8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435  .ufo/waves/round-32/claims.json
2e089615936dae60d1b4ab3883dbbc8ed7608018b9c7f4694209207d84b3207f  fleet pin MANIFEST.json
4bf494f8c38b6bfb44980f5b3f493063fc08d50aad8ce9f867907a57654e3970  corpus/SOURCES.md
b2ae45a87e574a25a0ba1505014b9909d3b3dd1a3741db01e20a9a260994ffb3  corpus/lessons/round-13.md
ef3714bbb77df1f03db0de325f6c49ea1a8bbf66a1fdeecdd2e8bb3d5474cadf  .ufo/waves/round-14/fixtures/expected.json
0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8  .ufo/waves/round-14/tools/quote-fidelity.py
dd1c57912a98039af99985063dc7e08697b836bbd41ef8e50b18062f2a5a5a9c  .ufo/waves/round-14/verification.json
acc2769354d452733bd7b70b3a09fadead423a7b5b390758ce589e71eb4d093b  .ufo/waves/round-17/run-carriers.sh
8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708  tools/round-27/xpin-attribute.mjs
```

Actual frozen source reopened on 2026-10-23: [counter lines 117–137, 163–171](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone/tools/round-32/c2-capability-calibration-v3.py#L167), SHA-256 `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f`. Short source quote at line 167: `shared = words(cells[1]) & desc_anchor_words(item, pats[0], base_scorecard)`. The source performs set intersection and a cardinality threshold; this run reports cardinality five for every controlled row.

## Construction and exact Git argv

All commands below completed exit 0 unless explicitly noted. `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE` precedes every Git invocation. Direct `git show` discovery calls used an equivalent sanitized subprocess environment, exit 0, empty stderr.

```text
mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin .
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone checkout --detach f382e3b7
git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone show 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525:SCORECARD.md
git -C /home/vgpnk/Projects/shokunin show cef00867ab3279ac2c2d10421e3e62c0e5d693f3:MANIFEST.json
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone add -- SCORECARD.md
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone -c user.name=R32\ A2\ Labels\ Control -c user.email=r32-a2labels@invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -m control:\ C2v3\ alphabetized\ label-keyed\ vocabulary\ bags
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone rev-parse HEAD
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone diff f382e3b7978e6091a19ca93277c15a75c0016b43 HEAD -- SCORECARD.md
```

Observed clone/commit/revision output:

```text
Cloning into '.'...
done.
HEAD is now at f382e3b7 round-32: freeze R32-C2 v3 (supersedes v2 before any seat or data: an irrelevant-path control met v2) — anchored evidence and description, before receipts
[detached HEAD cbb7dbc] control: C2v3 alphabetized label-keyed vocabulary bags
 1 file changed, 4 insertions(+), 5 deletions(-)
cbb7dbce50861117076e57d42ec5f471f71bd413
```

Discovery used the frozen counter's `manifest_statements`, `KEYS`, `desc_anchor_words`, and `anchors_for` without modifying it; `runpy.run_path(..., run_name='a2c2labels_inspect_only')` did not run its CLI/selftest. The first five sorted tokens for each keyed anchored vocabulary were:

```text
13: auditable bounded cadences claim domain-operation
14: accepts audit bounded committed controls
17: allowlisted-environment analyze before bound capture
27: attributes attribution both bytes canonical
```

## Complete generated section / retained fixture bytes

Standalone `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/Labels-Capabilities.section.txt`: 967 UTF-8 bytes, LF endings, final blank line. This is the complete section committed into the control's `SCORECARD.md`; the last explanatory paragraph was preserved from the baseline, not asserted as truthful evidence for the bags.

```markdown
## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| curated source registry for existing REA frontier | auditable bounded cadences claim domain-operation | `corpus/SOURCES.md`; `corpus/lessons/round-13.md` | round 13 |
| local raw-quote/heading regression audit | accepts audit bounded committed controls | `.ufo/waves/round-14/fixtures/expected.json`; `.ufo/waves/round-14/tools/quote-fidelity.py`; `.ufo/waves/round-14/verification.json` | round 14 |
| retained REA Ghidra-session log capture | allowlisted-environment analyze before bound capture | `.ufo/waves/round-17/run-carriers.sh` | round 17 |
| cross-pin evidence-ID attribution for saved REA envelopes | attributes attribution both bytes canonical | `tools/round-27/xpin-attribute.mjs` | round 27 |

Rows entered through rounds that demonstrated each capability running (`AXES.md` §Capabilities); the conformance rollout itself entered none.

```

## Complete sandbox diff

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index e90a5a01..37391259 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -616,11 +616,10 @@ Retired: none.
 
 | Capability | What it can now do | Evidence pointer | First-working round |
 |---|---|---|---|
-| pre-registered two-lane live battery on REA 6.5.0 | runs a 10-leg frozen-prediction battery with hashed per-lane receipts and cross-lane replay verification | `.ufo/waves/luna-round-6/receipts/` + `receipts-B/`; report `.ufo/reports/luna-round-6/kaidoku.md` | luna-round-6 |
-| version-symmetry battery on REA 6.4.0 | repeats the battery form on the second pin, proving per-name 6.5-only absence/refusal with a live control leg | `.ufo/waves/luna-round-8/receipts/`; `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md` | luna-round-8 |
-| config custody pre/post-pair for live-probe rounds | freezes the five operator paths' sha256s — the three client configs (Devin mcp_config.json, OMP mcp.json, Kimi config.toml) plus the two shell env carriers (~/.bashrc, ~/.profile) — before the round's first probe and re-verifies byte-identity after the battery closes, producing a zero-drift 6-line 5-hash receipt pair | `.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt` + `config-post-pair.txt`; comparison in `.ufo/reports/arc2-loop1-round2/kaidoku.md` | arc2-loop1-round2 |
-| contained user-service analyze of oversized PEs (analyzer-disable recipe) | runs REA/Ghidra analyzes of 91.6MB-class PEs as caller-independent systemd user services with registry-validated analyzer disables and memory caps — the paired demonstrations: r7 wall-fall (ev_a4aa9b0d…) and the r8 natural control (oom-kill; disable proven necessary) | `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` + `.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json` | arc2-loop1-round7 |
-| cross-pin evidence-ID attribution for saved REA envelopes | attributes a saved envelope to the `rea-agents` 6.5.0 id rule, the 6.7.0 rule, both or neither, from its bytes, using each installed package's own canonical digest code | `tools/round-27/xpin-attribute.mjs`; checker `tools/round-27/c2-xpin-check.py`; seat report `.ufo/waves/round-27/w1/BuildXpinTool.md`; receipts `corpus/evidence/round-27/c2/` | round 27 |
+| curated source registry for existing REA frontier | auditable bounded cadences claim domain-operation | `corpus/SOURCES.md`; `corpus/lessons/round-13.md` | round 13 |
+| local raw-quote/heading regression audit | accepts audit bounded committed controls | `.ufo/waves/round-14/fixtures/expected.json`; `.ufo/waves/round-14/tools/quote-fidelity.py`; `.ufo/waves/round-14/verification.json` | round 14 |
+| retained REA Ghidra-session log capture | allowlisted-environment analyze before bound capture | `.ufo/waves/round-17/run-carriers.sh` | round 17 |
+| cross-pin evidence-ID attribution for saved REA envelopes | attributes attribution both bytes canonical | `tools/round-27/xpin-attribute.mjs` | round 27 |
 
 Rows entered through rounds that demonstrated each capability running (`AXES.md` §Capabilities); the conformance rollout itself entered none.
 
```

## Frozen end-to-end scoring receipt

Exact argv, cwd equal to clone path above; environment keys unset as recorded. Run once:

```text
timeout 300 prlimit --as=4294967296 -- python3 -I -B /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone/tools/round-32/c2-capability-calibration-v3.py --root /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/clone --rev cbb7dbce50861117076e57d42ec5f471f71bd413 --fleet /home/vgpnk/Projects/shokunin
```

Complete stdout (tabs retained):

```text
round-13	P2-match	row 1 anchor evidence corpus/SOURCES.md, corpus/lessons/round-13.md; description words 5
round-14	P2-match	row 2 anchor evidence .ufo/waves/round-14/fixtures/expected.json, .ufo/waves/round-14/tools/quote-fidelity.py, .ufo/waves/round-14/verification.json; description words 5
round-17	P2-match	row 3 anchor evidence .ufo/waves/round-17/run-carriers.sh; description words 5
round-27	P2-match	row 4 anchor evidence tools/round-27/xpin-attribute.mjs; description words 5
statements=4 match=4 target=4 reverse_mismatch=0
```

Stderr: empty. Observed exit: **0**. Frozen target: **met**. No scoring adjustment, counter repair, or further experiment after this passing shortcut. Durable machine receipt: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Labels/Labels-C2v3.receipt.json`.

Report: .ufo/waves/round-32/a2audit/A2C2Labels.md
