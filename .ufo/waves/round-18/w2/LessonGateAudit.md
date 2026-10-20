PARTIAL

# LessonGateAudit — `corpus/lessons/round-18.md` `## Gate` at REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`

Seat `KaidokuR18.LessonGateAudit` is author-side and advisory. It does not count as outside verification. Line anchors are `git show b2aad08:<path>` unless marked otherwise. L = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

**Verdict.** Ten of the eleven decision rows (`round-18.md:18-28`) have evidence that resolves and reproduces. Row `:28` cites the shipped `routed-defects.py` selftest, and that selftest is **red at REV**. Four of the five located quotes (`:34-38`) are verbatim at their locators. The S035 `type.go` quote runs one line past its cited range. The four new rows `SOURCES.md:39-42` each have a URL, opened 2026-10-20, and a quote; their recorded digests and PR head re-check today. No finding reverses a Gate decision.

## Findings

### F1 — MEDIUM — the selftest cited as evidence fails at REV (row `:28`; Mistakes row 6 `:67` says "`--selftest` CLEAN 17")
- **Observation.**
  - The REV blob of `.ufo/waves/round-18/tools/routed-defects.py --selftest` exits **1**. 7 of 17 cases fail: `closed-fixture-cli`, `closed-fixture-inprocess`, and `token-only-R17-{VALIDATE16,PRODUCER-REV,SUMS-RUNLOG,REGISTRY,S032-DIGEST}`. Each token-only case fails on `extra_open=['R17-PINMAP']`.
  - The eb6c266 blob exits 0 with `SELFTEST: CLEAN cases=17`. The w1 `RoutedDefectsTool.md:57` "CLEAN cases=17" describes that version.
- **Cause.** The b2aad08 "L1 amendment" (`routed-defects.py:277-283`) now requires both `mid_map_sha256_mismatch` and `mid_map_compare_mismatch`. The selftest's closed fixture at `:914` still writes only `FINDING = "mid_map_mismatch"`. That leaves R17-PINMAP open in every fixture built on the closed one.
- **Isolation.** A scratch copy of the REV blob with only `:914` changed to carry both ids returns exit 0, `CLEAN cases=17`.
- **Impact.** The round's own `.ufo/waves/round-18/verify.py:157-159` expects `--selftest` exit 0 for every round-18 tool. [INFERENCE] It will record this failure when run; it has not been run at REV.
- **What still holds.**
  - Every token-only target keeps `target=(open True, named_open False, substance_open True)`.
  - The real measurement reproduces: `--rev 9011581` gives open_count 6; `--rev b2aad08 --strict` gives open_count 0, exit 0.
  - The row's rejection therefore stands on substance. The instrument it cites is red, and the amended R17-PINMAP check has no passing closed fixture at REV.
- **Fix (author).** Update fixture `:914` to carry both ids, or cite the eb6c266 tool blob explicitly. Correct `:67` "CLEAN 17" with an append-only line.

### F2 — LOW — the S035 quote's locator excludes its last token (`round-18.md:37`)
- The quote `case Map: type u struct { mapType u UncommonType }` ends with `}`. That brace is at go1.25.0 `src/internal/abi/type.go:362`, outside the cited `358-361`.
- Whitespace-normalized substring check: False against 358-361, True against 358-362.
- `SOURCES.md:41` and `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:1,19` cite `358-363`, which contains the brace.
- QUALITY #16/#17 (`corpus/QUALITY.md:26-27`): mislocated quotes fail. Fix: cite `type.go:358-362`.

### F3 — LOW — "first run step (16:24:08Z)" is the second step (`round-18.md:18`)
- calib-aether `runs/calib-aether/receipt.json`:
  - `steps.inspect-go-binary` (`:1987`) started at **16:24:07.220045Z** (`:2000`).
  - `pins_pre` was taken at 16:24:07.202665Z (`:1884`; echoed as `pins_compare.pre_taken_at_utc` at `:352`).
  - 16:24:08.035044Z is `steps.analyze.started_at_utc` (`:1918`, `:1981`).
- `runs/calib-aether/producer.json:3`, `runs/run-log.txt:2` and `LOG.md:2152` all say 16:24:07.
- Ordering is unaffected: 16:23:55Z < 16:24:07.2Z. The margin is 12.2 s, not 13 s. Fix: 16:24:07Z.

### F4 — LOW — the binding-gate validation is unretained, and the harness runs the weaker form (row `:18`)
- **Reproduced.** "15/15 `receipt-validate.py --require-mid-maps` exit 0" gives 15/15 exit 0 today. The 22 retained `pins/mid-*.json` match the entry's "22" (`…r18-swiss-map-replay.md:68`).
- **Not retained at REV.** `git grep -- --require-mid-maps b2aad08 -- runs evidence` exits 1.
- **Weaker harness form.** `verify.py:201` runs `receipt-validate.py <receipt>` without the flag. The frozen binding gate (`predictions/decision-rule.json:2`) names the flag form. Without the flag, `mid_map_missing`/`mid_checks_absent` (`.ufo/waves/round-17/tools/receipt-validate.py:33-36`) are not raised.
- QUALITY #18 (`QUALITY.md:28`) requires retained argv/stdout/exit. Fix: add `--require-mid-maps` at `verify.py:201` and retain its output.

### F5 — LOW, adjacent (outside `## Gate`) — an amendment's "at" postdates its own commit
- `.ufo/waves/round-18/claims.json:35` reads `"at": "2026-10-20T13:25:00-03:00 (after wave 1, before any round-18 REA run)"`.
- The only commit that touches claims.json is eb6c266, committed **13:23:55-03:00**. The first REA run started at 13:24:07-03:00 (`runs/run-log.txt:2`).
- The stated order is true: the commit precedes the run. The instant itself is hand-typed and later than both events.
- Row `:27` ("amended rule, written before measuring") leans on these amendments.

### Info (no action required)
- **S034 quote (`:35`) spans markup.** Raw lines 571-573 contain `<code>map</code>`. A raw-substring check is False; the tag-stripped text matches exactly (21 words). This is manual-only under QUALITY #16/#17, and the Gate does not claim machine grading. A future `quote-fidelity` run would return 1, and that result is void.
- **Row `:27` mixes units.** At 9011581 the tool output is live_count 3, fixture_count **8 sites in 4 files**, excluded **10 distinct paths**. The numbers reproduce exactly.
- **Row `:21`'s "name at `types+40` has no pkgPath" has no citation in the row.** It resolves via w1 `ConnC3Prediction.md:41` and `RevNotesmdMaps.md:135`, and via a byte read of the carriers (read only, never executed):
  - s1250-swiss-nethttp VA 0x552028: flags 0x62, pkgPath bit 0x04 clear.
  - s1246-swiss-nethttp `types+40`: flags 0x6d, bit set.
  - s12{46,50}-swiss-methods `types+24`: flags 0x01.
- **used-by gaps.** S033's used-by (`SOURCES.md:39`) lists only the lesson, but the entry cites S033 (`…r18-swiss-map-replay.md:1,107`). S036 is the only one of 36 rows that lists `SKILL.md`, yet `SKILL.md` also cites S033–S035.

## Gate rows → evidence (observation unless marked)

| Row | Decision | Resolves? | What was checked |
|---|---|---|---|
| `:18` entry | admit | yes (F3, F4) | eb6c266 committer 16:23:55Z; predictions unchanged eb6c266..REV (`git diff --quiet` exit 0); `compare.exit` 15/15 `0`; D labels `compare.json` `all_match` true, `invalid_index_reads` [22386945]/[15606016] predicted = observed; carrier sha256 receipt = prediction; logs `s1246-swiss-nethttp/…/ghidra.log:451`, `real-kimi-webbridge/…/ghidra.log:206` |
| `:19` methods trigger | reject | yes | 8/8 predictions `analyzer_errors_empty` true, 0 failure lines in 8 logs; `uncommonSize` named⇒uncommon at go1.24.6 `reflect.go:60-64` (cited by `CriticC3.md:19`); `RevNotesmdMaps.md` exists |
| `:20` patch fallback | reject | yes | `s1246-swiss-nethttp` log `:180` `INFO (GoApiSnapshot) Using Go API snapshot for 1.24.6` (QUALITY #20 discriminating line), no `Falling back`, failure `:408/:451`; compare `snapshot_route` info=info |
| `:21` 1.25.0 safe | reject | yes (Info) | `predictions/swiss-misread/s1250-swiss-nethttp.json` H1 `pkg_path` 40, `mcount` 0 for MIMEHeader/Values (H0 mcount 5/6); bytes above |
| `:22` map path | reject as stated | yes | `RevGhidraMapTypeRead.md:316-317`; `RevAetherReplay.md:18,26,183-184`; aether log frames `:124,:138` (`GoInterfaceType…:77`), `:147` (`GoStructType…:94`) |
| `:23` QUALITY #21 | admit | yes | `round-17-verifier-spotcheck.md:108` (partial disagree) and `:137` (R17-PINMAP); red-before: r17 receipts `--require-mid-maps` 8/8 exit 1 `mid_map_missing`; 29/29 r17 mid `pin_checks` verdict-only; `receipt-validate.py --selftest` CLEAN 18 exit 0 (forged-entries case `:977-993`) |
| `:24` S033–S036 | admit | yes (F2) | rows `SOURCES.md:39-42` URL + opened 2026-10-20; quotes below |
| `:25` go1.25 notes | reject | yes | page sha256 `c9d872d3…` = S031's recorded digest; `grep -ci swiss` 0 (exit 1), `noswissmap` 0 (exit 1) |
| `:26` jj `latest` | reject | yes | `docs.jj-vcs.dev/versions.json`: `latest` → v0.46.0 (released 2026-10-07); installed `jj 0.45.1` |
| `:27` C2 baseline | reject/admit | yes (F5, Info) | `head-rev-lint.py --rev 9011581` exit 0: live 3 (`citation-drift-probe.py:477`, `custody-pair.py:327`, `round-17/verify.py:59`), fixture 8, excluded 10; `CriticC2.md:18` (8), `ConnSiblingOverlap.md:99`; fleet `JjAuditKaidoku.md:240` §5 |
| `:28` C1 tokens | reject | **evidence red** (F1) | `CriticC1.md:9`; selftest REV exit 1 |
| `:42-43` registry | — | yes | S001–S032 rows byte-identical 9011581→REV; new S033–S036; tiers B/A/A/A; 32→36 |

## Quote re-check (fetched 2026-10-20)

| Gate line | Source / locator | Result |
|---|---|---|
| `:34` S033 | PR #9348 `<title>` "Golang: recover symbols … binaries by kubrickfr · Pull Request #9348 …" | contiguous substring, 9 words ✓. API: state open, merged false, head `a214355498e8…` = `ls-remote` = row; `.patch` sha256 `ae5dc2e3…` = row (3rd stable fetch); page sha `936e9055…` differs from all three recorded (fetch-time only, as S033 says) |
| `:35` S034 | go.dev/doc/go1.24 sha `d35c2d52…` = row; `<h2 id="runtime">` at 560, next `<h2>` at 574; quote at 571-573 | tag-stripped exact, 21 words ✓ (raw-substring ✗, markup; Info) |
| `:36` S035 | `map_select_swiss.go:22` `type mapType = SwissMapType` (`:5` `//go:build goexperiment.swissmap`) | exact, 4 words ✓; local = upstream go1.25.0 (`cmp` identical); sha256 of `map_swiss.go`/`map_noswiss.go`/`map_select_swiss.go` = row; go1.24.6 copies byte-identical; `map_swiss.go:32`/`map_noswiss.go:25` are the struct heads |
| `:37` S035 | `type.go:358-361` | **mislocated by one line** (F2); exact over 358-362, 10 words |
| `:38` S036 | jj v0.45.1 raw `git-compatibility.md` sha `0fb71f99…` = row; under `## … Colocated Jujutsu/Git workspaces` (`:100`); rendered v0.45.1 page has `id="colocated-jujutsugit-workspaces"`; `:208` is inside a ```bash fence | exact incl. upstream typo "there is not concept", **25 words** (at limit) ✓ |

## Commands (cwd L unless noted; scratch S=`/tmp/lessongate.NNOUpx`)
```
git rev-parse HEAD                                                     # b2aad08… exit 0
git show b2aad08:corpus/lessons/round-18.md                            # exit 0 (75 lines; ## Gate :12)
curl -sSL https://go.dev/doc/go1.24 -o S/go124.html; sha256sum         # exit 0, d35c2d52…
curl -sSL https://go.dev/doc/go1.25 -o S/go125.html; grep -c -i swiss S/go125.html   # 0, exit 1 (noswissmap: 0, exit 1)
curl -sSL https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md   # exit 0, 0fb71f99…
curl -sSL https://github.com/NationalSecurityAgency/ghidra/pull/9348 | grep -o '<title>[^<]*</title>'  # exit 0
curl -sSL https://github.com/NationalSecurityAgency/ghidra/pull/9348.patch | sha256sum   # exit 0, ae5dc2e3…
git ls-remote https://github.com/NationalSecurityAgency/ghidra refs/pull/9348/head      # exit 0, a214355…
curl -sSL https://api.github.com/repos/NationalSecurityAgency/ghidra/pulls/9348          # exit 0 (open, merged False)
curl -sSL https://docs.jj-vcs.dev/versions.json                                         # exit 0 (latest → v0.46.0)
(cwd /tmp) jj --version                                                                  # exit 0, 0.45.1
sha256sum ~/.local/opt/go-1.25.0/src/internal/abi/{map_swiss,map_noswiss,map_select_swiss}.go   # exit 0, = row
cmp S/up-<f> ~/.local/opt/go-1.25.0/src/internal/abi/<f>   (4 files)                      # exit 0 each
awk 'NR>=358&&NR<=362' ~/.local/opt/go-1.25.0/src/internal/abi/type.go                    # exit 0; "}" at 362
python3 -I -B S/quotecheck.py                                                             # exit 0 (table above)
git diff --quiet eb6c266 b2aad08 -- .ufo/waves/round-18/predictions/                       # exit 0
git show b2aad08:.ufo/waves/round-18/runs/<label>/compare.exit   (15 labels)               # all "0"
for d in .ufo/waves/round-18/runs/*; do [ -d "$d" ] && python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps "$PWD/$d/receipt.json"; done   # 15/15 exit 0
same over .ufo/waves/round-17/runs/*                                                       # 8/8 exit 1 (mid_map_missing)
python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root "$PWD" --rev 9011581d84527ba34c675f9cf912e54d2e72d470   # exit 0: live 3 / fixture 8 / excluded 10
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root "$PWD" --rev 9011581d…   # exit 0, open_count 6
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root "$PWD" --rev b2aad08c… --strict   # exit 0, open_count 0
(cwd S) git -C L show b2aad08:…/routed-defects.py > rd-REV.py; python3 -I -B rd-REV.py --selftest   # exit 1 (F1)
(cwd S) git -C L show eb6c266:…/routed-defects.py > rd-eb6.py; python3 -I -B rd-eb6.py --selftest   # exit 0, CLEAN cases=17
(cwd S) python3 -I -B routed-defects-fixturefix.py --selftest   # rd-REV.py with only :914 edited → exit 0, CLEAN cases=17
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --selftest   # worktree sha 034f5ead… = REV blob → exit 1
(cwd S) python3 -I -B L/.ufo/waves/round-17/tools/receipt-validate.py --selftest            # exit 0, CLEAN cases=18
git show b2aad08:.ufo/waves/round-18/runs/calib-aether/receipt.json | grep -n _at_utc      # exit 0 (F3 anchors)
git grep -n -- '--require-mid-maps' b2aad08 -- .ufo/waves/round-18/runs .ufo/waves/round-18/evidence   # exit 1 (F4)
git show b2aad08:.ufo/waves/round-18/claims.json | grep -n '"at"'; git log -1 --format=%cI eb6c266   # exit 0 (F5)
python3 ELF PT_LOAD VA→offset byte read on ~/.local/share/kaidoku-r18/carriers/{s1250,s1246}-swiss-nethttp (sha256 = carriers/SHA256SUMS)   # exit 0 (Info)
```

## Residual risk and gaps
- [INFERENCE] The freeze-before-run order rests on two clocks on the same host: the git committer date and the runner's clock. The GitHub API returns eb6c266 with committer date 16:23:55Z, which proves it was pushed. The public events feed (newest event 14:50:05Z) does not yet show that push, so no independent push instant was available.
- Not audited: the `## Mistakes`/R17-routed sections beyond what Gate rows cite, the Search-log tally (`SOURCES.md:67`), and the head-rev-lint/jj-red-before selftests (peer seats cover them).
- Some lane tools ran against the working tree: receipt-validate, head-rev-lint, and routed-defects in real mode. Their paths were `git status` clean, and the routed-defects worktree sha equals the REV blob. Selftests ran from S and create and remove their own mkdtemp. Nothing in the lane was written except this report. No jj or git write ran in the lane, and no carrier ran.
- Tool installs or updates: none. Read-only `pacman -Q jujutsu` reported not installed; jj is the `~/.local/bin` binary. Scratch S is removed after this report is written.
