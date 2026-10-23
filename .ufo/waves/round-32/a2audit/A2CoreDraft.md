# A2CoreDraft — bounded ARM64X decision prose

**UTC:** 2026-10-23T06:48:09Z  
**Axis:** R32-C1 coverage (ARM64X hybrid PE); calibration/R32-C2 is out of scope.  
**Status:** draft only. No postcontrol carrier data is included or assessed here. This report does not claim ARM64X is held or move the province to Core.

## Draft: knowledge entry

> # ARM64X hybrid PE: bounded native-view import (draft; pre-data)
>
> **State:** Draft only; carrier-result fields are unavailable. The pre-freeze probe is a synthetic probe, not a carrier.
>
> **Frozen decision boundary:** Classify a candidate as ARM64X only when the frozen oracle identifies COFF machine `0xAA64` and a CHPE code map containing at least one ARM64 and one ARM64EC range. A qualifying carrier must then produce a successful REA 6.5.0 `inspect` envelope for `binary_overview` on the pinned subject bytes. Compare the frozen format, architecture, document, image base, ordered segment fields, segment count and procedure count against the oracle; procedure count must also equal its frozen native-view export-count prediction. The committed envelope must match the corresponding live envelope except for `meta`, and the entry must name that evidence.
>
> **Pre-data probe, not a carrier result:** The frozen record describes REA 6.5.0 `inspect` and `analyze` runs on synthetic `x.dll` (`sha256 424777cbc93ea5c2aef4125352dcc7b5ed8c590d4ea47796ad36a53f759274dc`), with two native and two EC exports. The saved `inspect`/`analyze` envelopes report `binary_overview`, `format=pe`, `architecture=arm64`, `segment_count=8`, and `procedure_count=2`. The freeze says two inspect runs were equal except for `meta`. These are probe observations only: equal native/EC export counts do not distinguish native-count, EC-count, max, or union interpretations of `procedure_count`; the probe does not validate the carrier oracle classification or establish carrier behavior.
>
> **Limits:** Synthetic exported leaf functions only; the report is a native-view overview, not dual-view analysis. It does not cover internal or call-reached functions, runtime behavior, or ARM64EC decompilation. No broader ARM64X capability is claimed.
>
> **Carrier-result slots:** oracle classification — **UNAVAILABLE**; pinned carrier identity/subject digest — **UNAVAILABLE**; live inspect exit/envelope — **UNAVAILABLE**; oracle-field and prediction comparison — **UNAVAILABLE**; committed-envelope comparison/evidence identifier — **UNAVAILABLE**; per-carrier and aggregate outcomes — **UNAVAILABLE**.
>
> **Decision:** Do not call this held. Keep the ARM64X subtype at Frontier unless and until postcontrol evidence satisfies the unchanged predicate and the required entry/PROVINCE gates. The frozen C1 source list identifies S099 (Microsoft Learn, “Arm64X PE files,” https://learn.microsoft.com/en-us/windows/arm/arm64x-pe; opened 2026-10-23); this draft adds no source-derived technical assertion beyond the frozen predicate and probe.

## Draft: PROVINCE decision prose

**Not applied.** At the frozen base, ARM64X is a Frontier reserve. Proposed bounded disposition for later integration:

> Keep ARM64X hybrid PE in Frontier until postcontrol carrier evidence satisfies the frozen R32-C1 predicate. If that gate is later met, any Core row must name the cited round-32 entry and explicitly scope the holding to the synthetic exported-leaf carrier class and REA 6.5.0 native-view `binary_overview` observations. It does not establish runtime behavior, ARM64EC decompilation, or coverage of internal/call-reached functions. Leave unevaluated ARM64X cases outside that bounded class in Frontier.

This is conditional drafting, not a present Core claim. Do not add an unqualified ARM64X Core authority from the pre-freeze probe alone.

## Draft: SKILL decision prose

**Not applied.** Add a subtype-specific decision row only after the postcontrol disposition is known:

> **PE ARM64X hybrid:** Pin the subject bytes; require the frozen oracle's ARM64X/CHPE classification and evaluate the REA 6.5.0 `inspect` `binary_overview` against the frozen native-view fields and prediction. The pre-freeze synthetic probe supplies only a native-view envelope-shape observation; it is not a carrier holding. Do not imply runtime analysis or ARM64EC decompilation. Status remains **not held / postcontrol evidence unavailable** in this draft.

## Evidence and provenance

### Frozen sources and reopened quotations

- Base revision: `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525` (commit date `2026-10-23T02:44:59-03:00`). C1 freeze: `9a73680af21b002e3b99956c89234b2bbde2a71b` (commit date `2026-10-23T03:03:46-03:00`). C2 v3 freeze: `f382e3b7978e6091a19ca93277c15a75c0016b43` (commit date `2026-10-23T03:10:01-03:00`; read only to confirm it supersedes C2, not C1).
- Reopened at the frozen base, `PROVINCE.md:83`: “Reserve: ARM64X hybrids (the 91MB Godot ARM64 template is held, arc2-r7).” URL: `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md#L83`; date: base commit above; SHA-256: `c167827aa47405e51fa14891a52d0d2c2346c069e4a6151e40add67d2b3e8c4c`.
- Reopened at the frozen base, `SKILL.md:48`: “PE x86-64 / ARM64 | `rea analyze` (Ghidra PeLoader, wine-free) | held (cli-64, cli-arm64).” URL: `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md#L48`; date: base commit above; SHA-256: `efc57e7601669a06de5d994f1ff64654dfd0069fd88199d4c22dc351f0f5e860`.
- Reopened frozen C1 wording, `claims.json:9`: “probe cannot separate native-count from EC-count, max or union rules”. URL: `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims.json#L9`; date: C1 freeze above; SHA-256: `8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435`.
- Reopened frozen C1 wording, `claims.json:18`: “procedure_count also equals the frozen prediction in predictions.tsv (the native-view export count)”. URL: `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims.json#L18`; date: C1 freeze above; SHA-256 as above. The C1 rule, target and predicate were not altered.
- `claims-v3.json` at the C2 freeze has SHA-256 `a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d`; its stated supersession is C2 only. No C2 control or result was evaluated for this report.

### Committed pre-freeze probe artifacts

The frozen `claims.json` says the probe was not a carrier and records the full subject SHA-256 above. Its committed `before/probe` records were reopened; the JSON envelopes show REA metadata commands `inspect`, `analyze`, and `inspect_artifact`, but do **not** retain the original CLI argv. The exact argv for those historic REA runs is therefore unavailable and is not reconstructed here. No REA command was run by this seat.

| Frozen artifact | SHA-256 |
|---|---|
| `.ufo/waves/round-32/before/probe/insp.json` | `4eabbb60e11610f915c3e649f6c2afe8261fe25972f0f0cf2a623d6b165e1b15` |
| `.ufo/waves/round-32/before/probe/insp2.json` | `dac0c7598aac5b0f19db43d4454a95e50c4554bfa5c9523b5d6eef091ec85697` |
| `.ufo/waves/round-32/before/probe/an.json` | `98c11d7229b0b9534d45069243d93a246c6de2dd1a94cc9660566ec711500ce5` |
| `.ufo/waves/round-32/before/probe/ia.json` | `ecce983eef883ca663986a4a86bd2dea84714402f5ae342be16d359acfe5e59e` |
| `.ufo/waves/round-32/before/probe/x.dll.sha256` content | `424777cbc93ea5c2aef4125352dcc7b5ed8c590d4ea47796ad36a53f759274dc` (subject digest recorded by the receipt) |

The `insp.json` and `an.json` envelopes report `ok=true`, operation `binary_overview`, format `pe`, architecture `arm64`, eight segments and `procedure_count=2`. `insp.json` records `meta.command=inspect`; `an.json` records `meta.command=analyze`. Those counts describe the probe output only, not carriers. The freeze states that the two inspect runs match except for `meta`; no rerun or postcontrol comparison was performed here.

### Sandbox and exact commands

A bare evidence clone was created only in the permitted unique scratch path. No lane/fleet Git or jj state was written. The clone fetched lane refs and contains the frozen/base revisions named above; it has no checkout or product-file edits. `git rev-parse --is-bare-repository` returned `true`.

Exact shell command used to initialize and fetch the scratch clone:

```sh
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2audit/A2CoreDraft/clone && git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2CoreDraft/clone init --bare && git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2CoreDraft/clone fetch --no-tags /home/vgpnk/Projects/shokunin/kaidoku-shokunin '+refs/*:refs/*'
```

Observed stdout included `Initialized empty Git repository in /fast/scratch/hyaku/kaidoku-r32/a2audit/A2CoreDraft/clone/`, `From /home/vgpnk/Projects/shokunin/kaidoku-shokunin`, and successful fetch output for 601 updates. Full captured ref listing: `artifact://412`. The bash wrapper did not expose a numeric process exit status; no exit code is invented.

Exact revision/hash query command:

```sh
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; set -o pipefail; C=/fast/scratch/hyaku/kaidoku-r32/a2audit/A2CoreDraft/clone; git -C "$C" rev-parse 283aad7f^{commit} 9a73680a^{commit} f382e3b7^{commit}; printf '\nFrozen blob ids:\n'; git -C "$C" rev-parse 283aad7f:PROVINCE.md 283aad7f:SKILL.md 9a73680a:.ufo/waves/round-32/claims.json f382e3b7:.ufo/waves/round-32/claims-v3.json 9a73680a:.ufo/waves/round-32/before/probe/insp.json 9a73680a:.ufo/waves/round-32/before/probe/insp2.json 9a73680a:.ufo/waves/round-32/before/probe/an.json 9a73680a:.ufo/waves/round-32/before/probe/ia.json; printf '\nCommitted byte SHA-256:\n'; git -C "$C" show 283aad7f:PROVINCE.md | sha256sum; git -C "$C" show 283aad7f:SKILL.md | sha256sum; git -C "$C" show 9a73680a:.ufo/waves/round-32/claims.json | sha256sum; git -C "$C" show f382e3b7:.ufo/waves/round-32/claims-v3.json | sha256sum; git -C "$C" show 9a73680a:.ufo/waves/round-32/before/probe/insp.json | sha256sum; git -C "$C" show 9a73680a:.ufo/waves/round-32/before/probe/insp2.json | sha256sum; git -C "$C" show 9a73680a:.ufo/waves/round-32/before/probe/an.json | sha256sum; git -C "$C" show 9a73680a:.ufo/waves/round-32/before/probe/ia.json | sha256sum; printf '\nLive file SHA-256:\n'; sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md /home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims-v3.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/before/probe/insp.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/before/probe/insp2.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/before/probe/an.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/before/probe/ia.json
```

Observed output: full revisions `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`, `9a73680af21b002e3b99956c89234b2bbde2a71b`, `f382e3b7978e6091a19ca93277c15a75c0016b43`; the committed and live SHA-256 values matched for the listed source and probe files. The specific hashes are listed above. Again, the wrapper did not expose numeric exit status.

Exact date/revision check command:

```sh
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; printf 'UTC now: '; date -u +%Y-%m-%dT%H:%M:%SZ; C=/fast/scratch/hyaku/kaidoku-r32/a2audit/A2CoreDraft/clone; git -C "$C" show -s --format='%H %cI %s' 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525; git -C "$C" show -s --format='%H %cI %s' 9a73680af21b002e3b99956c89234b2bbde2a71b; git -C "$C" show -s --format='%H %cI %s' f382e3b7978e6091a19ca93277c15a75c0016b43; git -C "$C" rev-parse --is-bare-repository
```

Observed stdout: UTC `2026-10-23T06:48:09Z`; base, C1 freeze and C2-v3 freeze dates/subjects as stated above; `true` for the bare clone. Numeric exit status was not surfaced.

## Findings, boundaries, and touched surfaces

- The saved probe supports only that the synthetic sample produced a REA native-view `binary_overview` envelope. It is not an ARM64X carrier outcome and cannot establish the frozen oracle's carrier classification or carrier predicate.
- The frozen C1 acceptance contract is the authority for any later carrier decision. The pre-freeze probe does not settle the equal-export-count ambiguity for `procedure_count`.
- All carrier-result slots remain **UNAVAILABLE**. This seat did not read carrier files, run REA/counters/builds/tests, execute binaries, inspect/retry the held item `U064N008Hf47eb933`, or use attempt-1 seat outputs. No runtime or EC decompilation is claimed.
- Lane product files changed: none. Only this report was written in the lane. Scratch artifact created: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2CoreDraft/clone`.
- No tools were installed or updated. No product verification was run.

Report: `.ufo/waves/round-32/a2audit/A2CoreDraft.md`
