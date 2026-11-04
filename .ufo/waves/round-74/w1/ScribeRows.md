# ScribeRows — round 74 wave 1

## Behavior and touched surfaces

Axes: provenance accuracy, registry completeness, scope isolation.

`corpus/SOURCES.md`: appended S278 mined (`ptrace(2)`, docs/A, on-release) and S279-S282 rejected with explicit reasons and flip conditions; appended the required S275 used-by consumer; added bounded round-73 and round-74 search notes. No filed row was deleted. Original row count 184; resulting count 189. All five new rows have 11 cells and located quotes of 15, 14, 5, 17 and 1 words respectively. The unchanged-row comparison excludes only the intentional S275 modification; all other 183 original rows match their original text.

S275 old used-by, verbatim:

`corpus/knowledge/2026-11-04-r72-checker-env-capsule.md, .ufo/waves/round-72/w1/ScoutSource.md`

Appended `corpus/knowledge/2026-11-04-r73-kernel-witness-record.md`.

## Opening provenance and findings

One fresh GET: `https://man7.org/linux/man-pages/man2/ptrace.2.html`, HTTP 200, 104833 bytes, SHA-256 `69cd309ece177d54086771701b2085e31cabd14a92484647392bcda468f7bd35`. Exact saved bytes: `.ufo/waves/round-74/w1/ScribeRows/ptrace.2.html`.

Located quote, raw lines 1438-1439, 15 whitespace-separated words: “Use the caller's filesystem UID and GID (see credentials(7)) or effective capabilities for LSM checks.” The definition of the combined mode is at lines 1450-1451; its literal OR separator is deliberately not copied into the registry cell. READ mode's examples include environ at lines 1421-1425. The exact file-specific binding is additionally documented by S275's retained `proc_pid_environ.5.html`, lines 90-91: permission to access this file is governed by a ptrace access-mode READ_FSCREDS check. Omitting unreadable processes instead of manufacturing empty samples is the reader policy derived from that boundary, not an observed kernel execution result.

S279-S282 reuse round-73 ScoutSource HTML bytes and its opening receipt, copied into this seat's evidence directory, without new GETs. Every new row's opened date, snapshot size, SHA-256, exact quote and line locator is in `ScribeRows/source-evidence.json`. The copied `fetch-receipt.txt` is historical evidence, not a claim that this seat exercised its recorded GET/HEAD commands. Its listing also mentions `proc_pid_cmdline.5.html`, whose original snapshot remains in the round-73 directory and was not needed as a new-row artifact here.

## Commands and outcomes

All Bash calls used cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Scratch was `/fast/scratch/hyaku/kaidoku-r74/ScribeRows`, exported/passed as TMPDIR where applicable, with `trap 'rm -rf -- "$S"' EXIT` in each shell creating it. Both shells exited and removed scratch before handoff.

Acquisition command (after mkdir, trap and TMPDIR export):

```sh
curl --fail --silent --show-error https://man7.org/linux/man-pages/man2/ptrace.2.html --output /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ScribeRows/ptrace.2.html --write-out 'http=%{http_code} bytes=%{size_download}\n'
cp /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/w1/ScoutSource/{proc.5.html,proc_cmdline.5.html,proc_pid.5.html,dir_section_5.html,fetch-receipt.txt} /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ScribeRows/
sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ScribeRows/*.html
wc -c /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ScribeRows/*.html
```

Acquisition exit 0, `http=200 bytes=104833`. Sizes/digests recorded in source-evidence.json agree with the copied historical receipt.

Required validator command:

```sh
TMPDIR="$S" /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

First invocation exited 1, reporting 23 W04 duplicate-URL warnings and the sole error, verbatim:

```text
kaidoku	E11	S278 missing used-by corpus/knowledge/2026-11-04-r74-probe-mutation-closure.md
```

That consumer is owned by the knowledge scribe; this seat requested prerequisite completion rather than creating a placeholder or weakening the source row. After the owner reported its successful write, the same required command was run once more, with `set -o pipefail` and `2>&1` piped to `tee /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/ScribeRows/census-final.txt`. Exit **0**. Full output, pasted:

```text
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
kaidoku	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
kaidoku	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
kaidoku	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
kaidoku	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
kaidoku	W04	S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
kaidoku	W04	S117 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md across scopes
kaidoku	W04	S119 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S123 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S138 duplicate url github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs across scopes
kaidoku	W04	S142 duplicate url git-scm.com/docs/git-log across scopes
kaidoku	W04	S246 duplicate url plato.stanford.edu/entries/popper across scopes
kaidoku	W04	S247 duplicate url man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 across scopes
kaidoku	W04	S248 duplicate url github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs across scopes
kaidoku	W04	S245 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
kaidoku	W04	S271 duplicate url raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt across scopes
kaidoku	W04	S272 duplicate url docs.python.org/3/library/subprocess.html across scopes
kaidoku	W04	S273 duplicate url github.github.com/gfm across scopes
kaidoku	W04	S276 duplicate url docs.python.org/3/library/tempfile.html across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
```

## Gates, limits and out-of-scope

No product code, judge, scripts, templates, fleet-state paths, git/jj writes, installs, commits, publishing or deployment. No raw environment values were persisted. Frozen C1/C2 scores and mutation outcomes were not rerun or certified by this source-registry seat. This report does not promote assignment declarations to execution evidence. Existing duplicate-URL warnings are not new failures or a claim of a warning-free census.

Artifacts: `corpus/SOURCES.md`, `.ufo/waves/round-74/w1/ScribeRows.md`, and `.ufo/waves/round-74/w1/ScribeRows/{ptrace.2.html,proc.5.html,proc_cmdline.5.html,proc_pid.5.html,dir_section_5.html,fetch-receipt.txt,source-evidence.json,census-final.txt}`.

Self-evaluation: accuracy 4/5 (permission policy is explicitly an inference, not a kernel run); completeness 5/5 (all five rows, S275 linkage, two search notes and required successful census retained); clarity 4/5 (historical receipt lists an additional snapshot not copied here, explicitly disclosed); actionability 5/5 (exact command and artifact paths provided); conciseness 4/5 (full required warning output is lengthy). Overall 4.4/5. Highest-impact improvement: use source-evidence.json for compact machine reading while preserving the full raw census transcript. User-agreement self-check: scope and execution limits are explicit.

Routed label clarification: ScoutSource-8 reported that the frozen D11 audit matches the literal round-73 label `index.html#_section_5` in a rejected source cell. S282 preserves that label explicitly as a label, not an opened URL, alongside the actual opened section-5 index URL. No new fetch or alternate-source claim was made.

Concurrent-edit conflict, verbatim: an intervening S282 source cell stated “the same table served at https://man7.org/linux/man-pages/dir_section_5.html” and “the index anchor re-opened 2026-11-04, 4 530 B”. ScoutSource-8 reported “index.html#_section_5 is NOT a resolvable URL” and “has no anchors at all”. This seat does not certify that intervening fetch; it corrected S282 to distinguish the historical label from the opened page and notified Main before editing. The required census is refreshed after this clarification.

Post-clarification required census: exit **0**, identical 23 W04 warnings and final `kaidoku ok` line to the pasted output. `census-final.txt` contains this last invocation's full output. Its shell EXIT trap removed scratch before handoff.

Report: .ufo/waves/round-74/w1/ScribeRows.md
