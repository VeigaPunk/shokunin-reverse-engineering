CONTROL REJECTED — the NEW C2v3 Garbage control did not meet the frozen target. No honest-stop trigger was observed for this control.

# A2C2Garbage — attempt-2 pre-data control

- Report timestamp: **2026-10-23T06:48:17Z**. Counter execution timestamp: **2026-10-23T06:47:18Z**.
- Assigned counterexample: four distinct capability rows with correct names, rounds and frozen resolving anchor paths; every second cell is exactly `junk irrelevant bananas`.
- Exercised result: **`statements=4 match=0 target=4 reverse_mismatch=4`, exit 1**.
- Frozen target: **`statements=4 match=4 target=4 reverse_mismatch=0`, exit 0**. **Not met.** This is the counter's target comparison, not a canonical Rust admission judgment.
- Axes: **calibration** exercised (Capabilities summary versus pinned non-author closure). **Coverage** (ARM64X Frontier→Core) not exercised; no coverage change proposed.
- Smallest safe correction: **none demonstrated necessary by this control**. Leave counter, predicate and target frozen. No honest repair or data change was made.
- Bound: this result concerns the exact three-word garbage cell below. It does not establish semantic sufficiency of the five-word overlap rule, reject unexercised vocabulary variants, or establish saturation.

## Provenance and scope

| Item | Value |
|---|---|
| Production lane, read-only except this Report | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| Unique scratch | `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage` |
| Clone | `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage/clone` |
| Starting freeze / committed control parent | `f382e3b7978e6091a19ca93277c15a75c0016b43` |
| Frozen base used by counter | `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525` |
| Frozen fleet pin | `cef00867ab3279ac2c2d10421e3e62c0e5d693f3` |
| Sandbox committed revision scored | **`9b939fce514b34581dc76b9f900f6993b9c1f47c`** |
| Sandbox production-file delta | Only `SCORECARD.md`: 4 insertions, 7 deletions |
| Retained fixture | `capabilities-garbage.md` (614 bytes, UTF-8, LF; complete section below) |
| Retained output / diff | `counter-stdout.txt` (809 bytes), `control.diff` (2800 bytes), under unique scratch |

Read `claims.json` C1 and `claims-v3.json` C2. Did not inspect or retry held item `U064N008Hf47eb933`. No fleet/sibling/lane Git state, production code, docs or index was written. Sandbox Git writes were confined to this clone; `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were explicitly unset for Git commands and the counter.

No REA, Ghidra, carrier binary, judge, other runtime or subagent was launched. The one counter invocation used timeout 300 seconds and an inherited 4 GiB address-space limit. All launched command invocations exited; no persistent process/service was started.

## Environment and resource evidence

At `2026-10-23T06:45:06Z`, before cloning:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  559G  245G  70% /fast
```

Observed existing tools: `git version 2.56.0`; `Python 3.14.8`; `prlimit from util-linux 2.42.4`. `type -a timeout` reported a shell builtin and `/usr/bin/timeout`; the invocation below places `timeout` after `env`, using executable lookup rather than the shell builtin. **No tool installed or updated.** Operator rules were read first; no pacman transaction was attempted.

Two setup-only nonzero results were not counter runs: the initial `printenv GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE` printed nothing and returned 1; the version-probe chain reached the shell builtin `timeout --version`, which printed a missing-`<COMMAND>...` usage error and returned 125. No scoring retry followed either probe.

## Exact setup and sandbox commands

Working directory for clone setup: `/fast/scratch/hyaku`.

```sh
mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage/clone && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300 prlimit --as=4294967296 -- git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage/clone clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin . && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300 prlimit --as=4294967296 -- git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage/clone checkout --detach f382e3b7
```

Exit 0; relevant complete output:

```text
Cloning into '.'...
done.
HEAD is now at f382e3b7 round-32: freeze R32-C2 v3 (supersedes v2 before any seat or data: an irrelevant-path control met v2) — anchored evidence and description, before receipts
```

A surgical edit replaced original `SCORECARD.md:619-625` with the four rows below. The rest of that file was retained. The standalone fixture file retains the entire resulting `## Capabilities` section. Commit working directory: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage`.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300 prlimit --as=4294967296 -- git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage/clone -c core.hooksPath=/dev/null -c user.name=A2C2Garbage -c user.email=a2c2garbage@example.invalid commit -m 'control: C2v3 four garbage descriptions' -- SCORECARD.md
```

Exit 0; complete commit output:

```text
[detached HEAD 9b939fce] control: C2v3 four garbage descriptions
 1 file changed, 4 insertions(+), 7 deletions(-)
```

Revision/diff argv (both exit 0):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage/clone rev-parse HEAD
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage/clone diff --no-ext-diff --no-textconv --unified=0 f382e3b7978e6091a19ca93277c15a75c0016b43 HEAD -- SCORECARD.md
```

The revision output was `9b939fce514b34581dc76b9f900f6993b9c1f47c`; complete raw diff is retained below.

## Complete generated fixture bytes

This is the complete 614-byte `capabilities-garbage.md`, including its final blank line. It is the resulting `SCORECARD.md:615-623` section, immediately before `## Saturation` at line 624.

```markdown
## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| curated source registry for existing REA frontier | junk irrelevant bananas | `corpus/SOURCES.md` | round 13 |
| local raw-quote/heading regression audit | junk irrelevant bananas | `.ufo/waves/round-14/tools/quote-fidelity.py` | round 14 |
| retained REA Ghidra-session log capture | junk irrelevant bananas | `.ufo/waves/round-17/run-carriers.sh` | round 17 |
| cross-pin evidence-ID attribution for saved REA envelopes | junk irrelevant bananas | `tools/round-27/xpin-attribute.mjs` | round 27 |

```

## Exact scoring argv and complete output

Working directory: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage/clone`. One invocation, no retry.

```sh
date -u +%Y-%m-%dT%H:%M:%SZ && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300 prlimit --as=4294967296 -- python3 -I -B tools/round-32/c2-capability-calibration-v3.py --root /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage/clone --rev 9b939fce514b34581dc76b9f900f6993b9c1f47c --fleet /home/vgpnk/Projects/shokunin
```

Observed process exit: **1** (not timeout). Complete relevant command output follows; first line is the timestamp command, remaining lines are counter stdout. No counter stderr text was emitted by the tool.

```text
2026-10-23T06:47:18Z
round-13	P2-mismatch	row 1 what-it-can-do cell shares 0 words with the anchored description (< 5)
round-14	P2-mismatch	row 2 what-it-can-do cell shares 0 words with the anchored description (< 5)
round-17	P2-mismatch	row 3 what-it-can-do cell shares 0 words with the anchored description (< 5)
round-27	P2-mismatch	row 4 what-it-can-do cell shares 0 words with the anchored description (< 5)
reverse	P2-mismatch	row 1 names MANIFEST-closed round(s) [13] without a credited capability
reverse	P2-mismatch	row 2 names MANIFEST-closed round(s) [14] without a credited capability
reverse	P2-mismatch	row 3 names MANIFEST-closed round(s) [17] without a credited capability
reverse	P2-mismatch	row 4 names MANIFEST-closed round(s) [27] without a credited capability
statements=4 match=0 target=4 reverse_mismatch=4
```

The tool also appended its temporary-shell transport notice; that notice was not counter stdout and is not included in `counter-stdout.txt`.

## Source evidence and hashes

Reopened actual frozen clone source `tools/round-32/c2-capability-calibration-v3.py:163-171` at `2026-10-23T06:47:18Z`; [local source URL](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2Garbage/clone/tools/round-32/c2-capability-calibration-v3.py#L163). SHA-256 is `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f`, matching the frozen instrument hash in `claims-v3.json:48`.

Short source excerpt, line 168: `if len(shared) < MIN_DESC_WORDS:`. `MIN_DESC_WORDS` is 5 at line 45. **[INFERENCE, bounded to this control]** The emitted description-overlap failures occur after the name, round and resolving-anchor checks in lines 155-166. Thus these controls reached the description gate; they were not rejected for a malformed identity, round or evidence anchor. Each reported overlap was zero. With the exact three-word cell, even maximal overlap would be below the frozen threshold of five distinct words.

Observed SHA-256 values (existing anchor files were hashed without executing them):

| File, relative to clone unless stated | SHA-256 |
|---|---|
| Frozen counter `tools/round-32/c2-capability-calibration-v3.py` | `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` |
| Frozen `.ufo/waves/round-32/claims-v3.json` | `a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d` |
| Original frozen `SCORECARD.md` | `bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3` |
| Control committed `SCORECARD.md` | `aa139db5711778442acae8ee0153b129322f682bf586ef0fa69dcd13eb0ea947` |
| Scratch `capabilities-garbage.md` | `c85fdae4b03c7a2bb045df3fa5a546cfa0dfefd1a8f56ffdf159cd137a58a3f0` |
| Round 13 anchor `corpus/SOURCES.md` | `4bf494f8c38b6bfb44980f5b3f493063fc08d50aad8ce9f867907a57654e3970` |
| Round 14 anchor `.ufo/waves/round-14/tools/quote-fidelity.py` | `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8` |
| Round 17 anchor `.ufo/waves/round-17/run-carriers.sh` | `acc2769354d452733bd7b70b3a09fadead423a7b5b390758ce589e71eb4d093b` |
| Round 27 anchor `tools/round-27/xpin-attribute.mjs` | `8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708` |

## Complete raw sandbox diff

This is retained control-delta evidence from the exact diff argv above, not an outside-source prose quotation.

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index e90a5a01..dfe4ea9b 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -619,7 +619,4 @@ Retired: none.
-| pre-registered two-lane live battery on REA 6.5.0 | runs a 10-leg frozen-prediction battery with hashed per-lane receipts and cross-lane replay verification | `.ufo/waves/luna-round-6/receipts/` + `receipts-B/`; report `.ufo/reports/luna-round-6/kaidoku.md` | luna-round-6 |
-| version-symmetry battery on REA 6.4.0 | repeats the battery form on the second pin, proving per-name 6.5-only absence/refusal with a live control leg | `.ufo/waves/luna-round-8/receipts/`; `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md` | luna-round-8 |
-| config custody pre/post-pair for live-probe rounds | freezes the five operator paths' sha256s — the three client configs (Devin mcp_config.json, OMP mcp.json, Kimi config.toml) plus the two shell env carriers (~/.bashrc, ~/.profile) — before the round's first probe and re-verifies byte-identity after the battery closes, producing a zero-drift 6-line 5-hash receipt pair | `.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt` + `config-post-pair.txt`; comparison in `.ufo/reports/arc2-loop1-round2/kaidoku.md` | arc2-loop1-round2 |
-| contained user-service analyze of oversized PEs (analyzer-disable recipe) | runs REA/Ghidra analyzes of 91.6MB-class PEs as caller-independent systemd user services with registry-validated analyzer disables and memory caps — the paired demonstrations: r7 wall-fall (ev_a4aa9b0d…) and the r8 natural control (oom-kill; disable proven necessary) | `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` + `.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json` | arc2-loop1-round7 |
-| cross-pin evidence-ID attribution for saved REA envelopes | attributes a saved envelope to the `rea-agents` 6.5.0 id rule, the 6.7.0 rule, both or neither, from its bytes, using each installed package's own canonical digest code | `tools/round-27/xpin-attribute.mjs`; checker `tools/round-27/c2-xpin-check.py`; seat report `.ufo/waves/round-27/w1/BuildXpinTool.md`; receipts `corpus/evidence/round-27/c2/` | round 27 |
-
-Rows entered through rounds that demonstrated each capability running (`AXES.md` §Capabilities); the conformance rollout itself entered none.
+| curated source registry for existing REA frontier | junk irrelevant bananas | `corpus/SOURCES.md` | round 13 |
+| local raw-quote/heading regression audit | junk irrelevant bananas | `.ufo/waves/round-14/tools/quote-fidelity.py` | round 14 |
+| retained REA Ghidra-session log capture | junk irrelevant bananas | `.ufo/waves/round-17/run-carriers.sh` | round 17 |
+| cross-pin evidence-ID attribution for saved REA envelopes | junk irrelevant bananas | `tools/round-27/xpin-attribute.mjs` | round 27 |
```

Report: .ufo/waves/round-32/a2audit/A2C2Garbage.md
