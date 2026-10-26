# R41W2Reservation — C1 reservation claim

**CONFIRMED — zero hits.** I attacked the claim "no seat ran REA or unblob on the 5490/5491 images, their members, the V3/V4 carves or L3/L4 before the freeze `d764389e`" by four independent routes: (1) text/hash scan of every wave-1 report and artifact (freeze-commit export and live tree); (2) enumeration of every REA envelope's subject digest at any wrapper depth; (3) a scan of the actual tool calls in all 43 wave-1 seat transcripts (the strongest source — reports are self-description, transcripts are what ran); (4) timestamp evidence for the shared vendor cache and the first run on the pins. No hit on any of them. Three wording limits below (not violations) should travel with the claim.

Reserved identifiers searched (full digests, 8-hex prefixes in prose): pins V3 `c4f74f54…f872a`, V4 `ce27ebca…087f`, L3 `04cfb4cd…c45a3`, L4 `4c0e5459…cbfcbc`; plus image/member/nested digests 5490 image `770efb4e…5ab7`, member `87cc5d6b…a0f8`; 5491 image `a5a3a763…f661`, member `4cfc3016…2f6c`, nested core `4d5de25c…d947`; plus names 5490, 5491, `filesystem_core`, `FRITZ`, `download.avm`, `/c1/{V3,V4,L3,L4}`, `{L3,L4}/carrier`.

Freeze = commit `d764389e`, committer time 2026-10-26T18:08:13-03:00 = **21:08:13Z** (transcript timestamps are Z). All wave-1 seats live in 20:18Z–21:03Z (report mtimes 17:23–18:07 -03, all before the freeze).

## 1. Text and hash scan of w1 (route 1)

Commands (scripts in artifacts): `git -C $L archive d764389e… .ufo/waves/round-41/w1 | tar -x -C $S/frz`; `python3 scan.py $S/frz scan-freeze-tree.json`; `python3 scan.py $L/.ufo/waves/round-41/w1 scan-live.json`.

| | freeze-commit export | live tree |
|---|---|---|
| files scanned (.gz decompressed) | 1044 | 1064 (20 added after the freeze: `artifacts/R41C1Counter-postfreeze/*`, 3 extra subject records, all counter dry-runs on round-40 bytes) |
| 41 reports ≙ 41 registry members, no missing/extra | yes | yes |
| files with any reserved 8-hex prefix | 23 | 23 |
| **lines carrying a reserved digest AND a REA/unblob marker** | **0** | **0** |
| files whose bytes sha256 equal a reserved digest | 2 | 2 — `artifacts/R41C1LCarriers/L3/carrier.sqsh` = `04cfb4cd…`, `…/L4/carrier.sqsh` = `4c0e5459…` (the builder's own outputs, never run: see §3) |

The 23 digest-bearing files are identity/provenance records, not runs: reports `R41C1EntryDraft, LCarriers, Sentinel, VendorV3, VendorV4, CritC1Draft, SrcAvm`; artifacts `R41C1LCarriers/{artifact-sha256.txt,build-log.txt,carriers-build.json,carriers.json,probe.json}`, `R41C1VendorV3/{carriers-fragment,fetch-5490,oracle-run,provenance}.json`, `R41C1VendorV4/{budget,carriers-V4,oracle-run,provenance}.json`, `R41SrcAvm/identity-crosscheck.tsv`, `R41CritC1Draft/{reservation-scan-now.json,reservation-scan.py}`. I read the REA/unblob-marker lines in every one of them: all are (a) negative statements ("no REA / no unblob ran…", e.g. `R41C1VendorV3.md:5-6`, `R41C1VendorV4.md:9,232-233,251`, `R41C1LCarriers.md:9,201`, `R41SrcAvm.md:168`), (b) REA source/budget constants read, never executed (`R41C1VendorV4/budget.json`, `R41C1VendorV3/oracle-run.json:93-108`), or (c) the direct decoder note `sasquatch-v4be` without `-be` (the argv unblob uses) — a decoder run, not REA/unblob.

## 2. Envelope census (route 2)

`python3 subjects.py <tree> out.json` walks every .json/.json.gz/.jsonl, finds any dict with `subject.digest.sha256` at any depth (REA envelopes sit under several wrappers, e.g. `{ok,data,meta}` — an earlier top-level-only pass would have missed them).

| | freeze export | live |
|---|---|---|
| JSON files | 447 (1 non-JSON: `R41C2Counter/mutants.json` is JSONL; raw-text scanned) | 458 |
| subject records | 185 | 188 |
| distinct subject digests | 120 | 121 |
| **subject digest ∈ {4 pins, 5 image/member/nested digests}** | **0** | **0** |

Envelope subjects by seat are all seat-local dev carriers (`R41C2Gen` 52 held-out dev carriers, `R41C2ReconDepth` 40, `R41C2Shortcuts` 24, `R41C2TableDraft` 18, `R41C1Collide` 11 + `R41C2ControlTables` 10 predicted, `R41SrcRea` 5, `R41CritC2Draft` 4, `R41C1Run` 1 = round-40 `L1` `2521ded6…`, `R41C1DevCore` = development 7430 `1588129540…`).

Also at the freeze commit outside w1: a `git grep` of the nine digests over the whole tree hits only `carriers.json`, `plans/round-41-claims.md`, `w1-{gen,spec,dispatch}`, `corpus/evidence/round-41/c1/{V3,V4}/oracle-run.json`, and round-40's `R40C1VendorScout/candidates.tsv` (HEAD+hash scout; its report line 12: "No unblob and no REA ran on any image"). `corpus/evidence/round-41/c1/` at the freeze holds oracles, carriers (L3/L4) and oracle-run.json only — no `after.json`/`run.json`. The first commit adding any `after.json` is `5ca6941b` (18:12:01 -03, V3, L3, L4; V4's at `e9a24d07`, 18:14:04), both after the freeze.

## 3. Transcript scan — what actually ran (route 3)

`tx-scan.py` over 43 transcripts (41 registry seats + planner `KaidokuR41` + `KengakuR41`; 3955 tool calls: bash 2538, read 426, edit 412, write 229, grep 70, yield 49, eval 20, wait 17, glob 8; **0 `task` spawns** — leaf seats held). Eleven seats' transcripts carry a `-N` suffix (`R41C1Collide-2`, `R41C1Extra-3`, `R41C1VendorV4-2`, `R41C2AxisFit-3`, `R41C2EntryReview-3`, `R41C2ReconCombined-2`, `R41C2Shortcuts-2`, `R41ConnRouted-2`, `R41CritC2Draft-2`, `R41ScoutCalib-3`, `R41ScoutSkill-2`); each starts 20:18–20:24Z and ends within the wave, so the suffix is a name collision, not a missing earlier attempt [INFERENCE from start/end times; no base file exists].

- Calls naming any reserved identifier **and** able to execute REA/unblob (direct verb, `npx`, `c1-run.sh`, `c1-counter.py`, harness scripts): 80, of which **bash/eval = 12**. I read all 12 plus the 82 other bash/eval calls naming a reserved id (94 listed). Dispositions: curl/tar/sasquatch/own-reader work by the owning seats (VendorV3 5490, VendorV4 5491; `R41SrcAvm` HTTP/info-file reads only); doc/heredoc edits that merely contain the words; fixture repos in `R41C2AxisFit` (`{"honest":"receipt"}` placeholder JSON, no REA); builder runs in `R41C1LCarriers`; `grep` scans in `R41ConnSibling`/`R41CritC1Draft`. **No bash/eval call pairs an `extract-firmware`/`unblob` execution with a reserved input.** The 25 "direct verb + reserved name" rows are all `write`/`yield`/`grep` text (reports and generators), none `bash`.
- Owners' own commands: `R41C1VendorV3` (57 bash/eval), `R41C1VendorV4-2` (56), `R41C1LCarriers` (41), `R41C1Fetch` (52): the `unblob|extract-firmware|npx|REA_UNBLOB` tokens are only (i) `grep`/`sed` reads of `rea-agents/dist/*.js` constants and the unblob handler source and (ii) prose strings inside the build log. None invokes REA or `unblob`.
- All 103 textual matches of `npx … rea-agents@6.5.0 extract-firmware …` or `unblob <arg>` (`direct-invocations.json`, 16 seats; many are prose inside heredocs) take seat-local development inputs: `R41C1Collide` `carriers{,2,3}/{A,B,C,D,E}-*/carrier.sqsh` + `wrap.tar`; `R41C1DevCore` 7430 core/wrapper dev carves; `R41C1Revenger` `fx/F1…F6`; `R41C2Gen/ReconCombined/TableDraft` `devfinal*/dev/absorb/l2/marked-be` dev carriers; `R41RevBudget` `fx*.squashfs`; `R41SrcRea` `mk/*.sqfs`; `R41CritC1Draft` `wrapped.bin`/`two.bin` built from round-40 L2; `R41C1Run` round-40 `L1`; `R41C1Counter` `$T/{whole,trail512,pad8192,twosqfs}.bin` and its own fresh dev carrier (`cb500eb7…`, 1734 B — carries the *label* "L3" in its report, but is a different sha than the frozen L3 `04cfb4cd…`).
- **Planner pre-freeze run:** `KaidokuR41` 20:38:34Z built a trivial two-entry tree (`etc/a`, empty `var/tmp/empty`) with `tools/round-40/gen-squashfs.py --endian avm-genuine --comp xz` under `S=…/kaidoku-r41/L1-empty` and ran REA depth 1 on `img.sqsh`. That is a dev probe; L3/L4 are multi-entry collision carriers (claims §Carriers), so it cannot be either pin. No envelope with that subject appears in w1 (it was not copied).
- **L3/L4 before freeze:** only `R41C1LCarriers` (builds, `probe-avm-chain.py`, sasquatch cross-check) and `KaidokuR41` 21:06:52–21:07:06Z (`mk-l-carriers.py --builds 2` + `sha256sum` to confirm determinism; no REA/unblob in those calls). Other seats' references to `R41C1LCarriers` are `wc -l`/`cp` of `mk-l-carriers.py` (ConnPattern 20:30, KaidokuR41 20:28).
- **Vendor bytes before freeze:** held only in the scratch of `R41C1VendorV3/V4` (and `R41C1DevCore`/`Reader` hold the *development* 7430 image, not reserved). The shared vendor cache `/fast/scratch/hyaku/kaidoku-r41/cache/` that the counters read was **created after the freeze**: `fetch-vendor.py` call at 21:08:29Z; file mtimes `c4f74f54…bin` 18:08:33 -03, `ce27ebca…bin` 18:08:38 -03 (freeze commit 18:08:13). Every wave-1 `--carrier-cache`/`fetch-vendor.py` invocation by other seats (`R41C1Counter` 20:19–21:12Z, `R41C1Fetch`, `R41C1Sentinel`, `R41CritC1Draft`) resolved **round-40** specs/rev `7fce3086` (V1/V2 bytes), recorded in `carrier-cache-or-fetch-invocations.json`.
- `xd://mcp__rea_*` devices: no toolCall path targets one (4 text mentions are prohibitions in generators/reports).

First run of REA on a pin: `KaidokuR41` `c1-run.sh after …` at **21:11:07Z** (L3/L4/V3/V4), i.e. 2m54s after the freeze commit; the do-nothing control at 21:08:49Z reads the cache but the control JSON shows no rerun (`'rerun'` absent, `extract-firmware` count 0).

## 4. Where the claim is looser than its wording (calibration, not defects)

1. **Byte-level, not design-level.** "Fresh" holds for L3/L4 bytes. The collision *design* (both-direction nested-name pairs, deep-tail pair, empty file, absolute symlink) was exercised on look-alike dev carriers by `R41C1Collide` (A–E, REA depth 1/2 + a V3-shaped wrapper `wrap.tar`) before the L3/L4 pins were built; pins are pairwise new, behaviour on that design was predicted by a sibling dev run (`R41C1Counter`'s "fresh carrier" is likewise labelled L3). Fine for a pin-freshness claim; not a claim that the L3/L4 *outcome* was unknown.
2. **Extractor contact is real and disclosed.** The decoder REA/unblob invoke (`sasquatch-v4be`) and the lane reader `sqfs-list.py` read V3, V4 (`R41C1VendorV3/V4` oracle-run.json, `R41C1Reader` on 7430 only) and L3/L4 (`R41C1LCarriers` cross-check against `sasquatch-v4be` without `-be`) before the freeze. The claim text says REA/unblob only — keep that qualifier (`R41CritC1Draft` §(d) and `R41SrcAvm` F7 already require it).
3. **"Every wave-1 report states its runs"** is slightly overstated: by an `no REA|reserved|…` text heuristic, 38 of 41 reports carry an explicit reservation/no-run sentence; `R41Assim`, `R41C2Eval`, `R41C2Mutants` do not (none touched a reserved input per the transcripts: no reserved id in any tool call, no REA on a non-dev input). The `R41CritC1Draft` "112 lines, 0 red" scan was taken at 20:28Z, before most seats finished; this report supplies the full-wave scan. The claim's evidence now rests on transcripts + envelope census, which sit outside the lane tree: the lane tree alone (reports + artifacts) can show absence of a *recorded* run, not of an unrecorded one [INFERENCE: per-seat scratch is deleted, as `R41CritC1Draft` §(d) notes; transcripts at `~/.omp/agent/sessions/…` are the independent witness].

## Limits

Transcripts show tool calls, not host-level process accounting; a process launched by an unobserved path (an agent-spawned shell script that then calls REA on a reserved file) would appear only through its script text, which I scanned for the harness scripts' names and for the reserved names. No REA/unblob re-run was performed by me (not needed; the claim is about history). No tool installed, nothing written outside this report and `w2/artifacts/R41W2Reservation/`; scratch removed.
