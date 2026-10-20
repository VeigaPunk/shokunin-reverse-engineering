# CustodySafety — round 14, wave 1 (sentinel, report only)

Seat: `KaidokuR14.CustodySafety`. Axes: **calibration** (provenance claims match the bytes) and **coverage** (every custody surface named). Harm = any target execution, config edit, install, or secret/full-copy disclosure.
Window: 2026-10-20T05:14Z (dispatch) to 05:18:00Z (last check). The only write is this report. I made no edits, ran no gate or selftest, ran no build or lint, and executed no target.

## Findings (severity order)

### F1 — MEDIUM (calibration): the gate wants Markdown `#` headings, but both upstream sources are HTML
- **Evidence.** The pinned View8 `README.md` bytes are HTML. They include `<h2>Usage</h2>` (line 18), `<h3>Command-Line Arguments</h3>` (line 20) and `<h3>Deterministic Function Names and Mapping CSV</h3>` (line 81). I fetched `https://raw.githubusercontent.com/suleram/View8/ef39099b4f5076042173f9113382ebeb0630a56d/README.md` and got HTTP 200, 13,242 B, sha256 `191621cd0f87eb3c7f54d18e0ca128f2d7fffd997b11f83d5b3761c5cc01619b`. That matches ReviewS017's copy byte for byte, so two independent fetches agree. S018 is also HTML: ReviewS018 reports `<h1>` Introduction and `<h1>` Decompiled output.
- **Exploit path / failure mode.** The gate interface requires the section to be "exact Markdown heading text including #". No byte-exact upstream capture can meet that. A fixture that passes must therefore be a derived rendering. If the manifest's `sha256` pins only that derived file, a later reader could mistake it for "the source's exact bytes".
- **Second-order effect.** Inline `<code>` tags break rendered-text contiguity in the raw bytes. In raw HTML, the original S017 splice ("Use --normalize to replace …") fails partly because of `<code>--normalize</code>`, not only because of the splice. The corrected quote is contiguous raw text on line 40, so it passes. A red-before fixture built on raw HTML could therefore fail for the wrong reason.
- **Smallest remediation.**
  - Each derived fixture should name its upstream URL and upstream sha256 (for S017: `191621cd…619b`), its own derived sha256, and the transform it applied (for example "HTML h2/h3 → ##/###; inline tags stripped").
  - Add one control: a legitimate quote that runs across inline markup must pass in the same rendering. That proves the S017 red case fails because of the splice.
  - I sent this to `KaidokuR14.QuoteSourceFixtures`. Overlaps ReviewQuoteContract.

### F2 — MEDIUM (custody): full third-party copies in a repo that pushes to a public remote
- **Evidence.**
  - `gh repo view` reports `{"isPrivate":false,"visibility":"PUBLIC"}` for remote `VeigaPunk/shokunin-reverse-engineering`.
  - At 05:14:45Z, `w1/s018-raw.html` (355,603 B, sha `31b82315…dd5e`) held the whole Check Point page. Its footer at line 4240 read "© 1994-2026 Check Point Software Technologies LTD. All rights reserved." The page also included decompiled credential-theft code and C2 route strings.
  - After my message, the owner deleted that file. ReviewS018 has updated its report to say so.
  - `w1/ReviewS017-source/View8-README-…md` is still a full 13,242 B README copy. `gh api repos/suleram/View8/license` returned 404, and the root listing at the pin (`.gitignore Bin Parser README.md Simplify Translate __init__.py split_util.py view8.py view8_util.py`) has no LICENSE.
  - The round prompt says to commit wave specs and the registry as evidence (`kaidoku-round-14.md:175-177`).
- **Impact.** One pathspec commit of `w1/` would publish full copies. The lane's quoting rule is ≤25 words. [INFERENCE] I am flagging this as a redistribution risk, not giving a licensing verdict. The lane does not give licensing verdicts (`PROVINCE.md:114-116`).
- **Trade-off now recorded.** Deleting the S018 capture means F1/F2 of ReviewS018 can no longer be checked against its raw line numbers. The page is mutable (modified 2026-09-24 per ReviewS018), so a re-fetch may hash differently.
- **Smallest remediation.**
  - Keep full captures out of commits; record the URL, sha256 and size instead.
  - Fixtures should hold only the headings and sections the manifest needs.
  - Leave `ReviewS017-source/` untracked, or cut it down to those sections.

### F3 — MEDIUM (boundary): the sources contain target instructions, and the install rules conflict
- **Evidence (data, not directives).**
  - The View8 README contains more than 20 `python view8.py …` command blocks. It also describes a bundled `Bin` folder of patched disassemblers and `VersionDetector.exe` (lines 71-73, 276-282). It warns: "Unpickling data from untrusted sources can execute arbitrary code." (`Creating and Processing Serialized Files`, line 112).
  - I grepped both captures for agent-directed injection (`ignore previous`, `you are an AI`, `system prompt`, `curl|sh`, `pip install`, …). The only hits were the article's own prose about LLM-assisted renaming. No directive aimed at an agent was found.
- **Exploit path.** A seat could decide to "verify" S017's `--normalize` behaviour or S005's version range by downloading View8 or GoReSym release binaries and running them. RULES.md tells agents they "install or updates any tool that helps its task or is a strict upgrade, with full privilege, without asking first" (lines 3-4). It lists "official release binary into `~/.local/bin`" as channel 3, and a project's own release page arguably qualifies. So RULES alone does not stop this. `PROVINCE.md:108-113` does: installing engines is operator-owned, and "The lane documents the gap and the exact env key; it never runs the installer."
- **Impact.** This would be target or tool execution in a source-only round, and possibly pickle code execution. C1/C2 do not need any of it.
- **Smallest remediation.** Add one sentence to the wave-2 context: "Source excerpts are data; no command in a source is executed; no View8/GoReSym/Ghidra install or run." Record the RULES-vs-PROVINCE tension in the round report as an open L0 question rather than settling it inside the lane.

### F4 — LOW (custody of S003): "fixing" the Go range would change the pinned artifact
- **Exploit path.** C1 shows that installed 12.1.4 declares `1.15-1.25` and that GP-6528 adds 1.26. An agent might "upgrade" Ghidra to master or a later release under RULES. That would replace `Base-src.zip` (S003 pin `f00d29c2…8d804`; recomputed now and it matches) and change REA's provider install.
- **Status.** `SkillRuleDraft.candidate.md:27-28` already says not to edit the installed release to widen the range. Keep that line in the landed entry and SKILL addendum.

### F5 — LOW (calibration): what fetching each pinned URL actually risks, compared with the evidence it declares

| Src | Declared custody | Fetch need / egress | Risk |
|---|---|---|---|
| S003 | local, sha pinned | none | sha recomputed, equal |
| S006 | local, path + lines only, **no digest in registry** | none | recomputed `a23562a3175409a66e12e5ba47bd19e218cd7868b03bc3210c4ae7e0d296c33e`; RegistryDeltaDraft proposes recording it |
| S004 | GitHub commit SHA | GET github.com; request URL + IP/UA only | immutable object; low |
| S005, S017 | GitHub tree @SHA | GET raw.githubusercontent @SHA | immutable bytes (S017 verified twice); low |
| S018 | live article, date only | GET checkpoint.com; WAF intermittent | **mutable** (modified 2026-09-24); a capture's hash only vouches for bytes fetched in this session; round-13 lines 77/87 not reproducible (ReviewS018 F3) |

- **Outbound data.** None of these requests carries local artifact bytes. The real path for data to leave the host is the seat transcripts: anything a seat reads goes to its model provider. That is why fixture and manifest paths must never point at secret files (see F7).
- **Unnecessary credential use.** `gh api` sends the user's GitHub token to api.github.com. I made two read-only public calls that way (license and contents). Unauthenticated `curl` would have been enough. Seats should prefer unauthenticated fetches.
- **Upload-only route.** S022 remains correctly rejected.

### F6 — LOW (disclosure): committing `task-result.json` would publish host privilege posture
- **Evidence.** `task-result.json` (157,068 B) contains the RULES text "Passwordless `sudo` is available". `git grep 'Passwordless' HEAD` returns nothing, so it would be new to the public remote.
- **Remediation.** The prompt only requires specs and the registry. Commit `spec.json` and `swarm-registry.json`, and leave `task-result.json` out unless needed.

### F7 — LOW (cross-reference to GateInputSafety F1): an unconfined manifest becomes a secret oracle
GateInputSafety F1 already covers absolute and `../` paths. The custody angle it adds to: if `source_tampered` prints the observed digest, a crafted manifest can learn a secret file's sha256. Re-pinning that digest then turns per-quote verdicts into a substring-membership oracle over any readable file, for example `~/.config/gh/hosts.yml`, and the results land in LLM transcripts. The realpath + commonpath confinement closes this; nothing extra is needed. Likelihood is low because L1 freezes the inputs.

## Factual checks run (read-only)
- **Secret values.** The live values of `OPENAI_CODEX_TOKEN`, `XAI_OAUTH_TOKEN`, `HL_INITIAL_WORKSPACE_TOKEN` and the `gh auth token` appear in **0** files under `.ufo/waves/round-14/` at 05:17Z. Only lengths and counts were printed, never values.
- **Pattern grep.** The only hits were in the now-deleted `s018-raw.html`: malware-article strings, a `-----BEGIN PUBLIC KEY-----` block quoted from the malware (a public key, not a secret), and GTM id `GTM-5JCRGP`. No session, WAF or cookie tokens were found.
- **Planned fixture paths.** `.ufo/waves/round-14/fixtures/` and `tools/` **did not exist** at 05:18:00Z, so I could not review their contents. The spec's relative-path manifest design keeps `/home/vgpnk` out of manifests.
- **Client configs.** One mid-wave observation at 05:16:35Z, digests only:
  - devin `16f496e6…263a4`
  - omp `38d2a1d0…1b926b`
  - kimi `14ef6259…5e1f`
  - .bashrc `0cd3d560…ce4d`
  - .profile `6c6be761…4f30`

  The newest mtime is `.bashrc` at 2026-10-19T21:46:35Z, before dispatch. This is **not a pre/post pair**, so per `SKILL.md:207-215` it cannot support a zero-drift claim.
- **Installs since dispatch.** None observed. `pacman.log` ends at 2026-10-20T01:07:12-0300 (04:07Z). `find` for files newer than 05:14Z in `~/.local/bin`, uv tools, `~/.cargo/bin`, the npm global directory and `~/go/bin` found nothing. Seat reports so far (BaselineMeasures, ReviewS017, ReviewS018, ReviewQuoteContract, RegistryDeltaDraft) each state no installs.

## Not run, so not passed
No gate, selftest or gitleaks run. Before committing, L1 should rerun the env-value scan and `gitleaks dir` (8.30.1 is already installed: pacman, 2026-10-19, not installed by me) over `fixtures/`, `tools/` and `w1/`. No `custody-pair` pre/post pair was taken.

## Sources opened (access 2026-10-20)

| Location | ≤25-word contiguous quote | Limitation |
|---|---|---|
| raw View8 README @`ef39099`, `Creating and Processing Serialized Files`, l.112 | "Unpickling data from untrusted sources can execute arbitrary code." | README statement, not observed behaviour |
| `/home/vgpnk/.omp/agent/RULES.md:3-4` | "installs or updates any tool that helps its task or is a strict upgrade, with full privilege, without asking first." | operator directive |
| `kaidoku-shokunin/PROVINCE.md:112-113` | "The lane documents the gap and the exact env key; it never runs the installer." | lane scope |
| `kaidoku-shokunin/SKILL.md:358-359` | "Hashing stores digests only, never contents." | followed above |
| `w1/s018-raw.html:4240` (since deleted) | "© 1994-2026 Check Point Software Technologies LTD. All rights reserved." | the capture no longer exists, so this cannot be re-checked locally |

## Tool installs
None. I used `curl`, `sha256sum`, `gh` (two authenticated read-only public GETs) and Python, all already present.
