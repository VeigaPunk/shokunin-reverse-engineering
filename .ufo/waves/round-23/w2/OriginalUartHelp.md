# OriginalUartHelp: R23-C1 source review of the uart-help envelope/run pair

Seat: KaidokuR23.OriginalUartHelp. Author-side source review, not independent outside admission. L1 holds the canonical planner.
Candidate: 2838351450ff1ee4baa620c962a1153450d53311 ("round-23: retain measured four-of-six coverage and refusal controls"). Baseline aa1450b82f9ede35aada63efe8a34e01c6e02f72 was not used for any verdict.

## Method and limits

- Only committed candidate bytes were read: `git show <rev>:<path>`, `git grep -F <rev> -- <paths>`, `git cat-file -s`. Tar members were streamed in memory (`git show <rev>:<tar> | tar -xzOf - <member>`). I did not run `git status`, `diff`, or `add`, and wrote nothing to the index.
- No producer replay: no `npx`, no `sigrok-cli`, no decoder execution, no hardware or device access. The counter `count-c1.py` was read, not executed.
- The "model" check below is my read-only reconstruction, in memory, of sigrok-cli `show_pd_detail_single` output from upstream sources. It is not a byte comparison against producer stdout. Raw sigrok stdout is not retained anywhere (`raw_result: null`).

## Bound inputs (observed)

| Item (candidate rev) | Bytes | sha256 | Use |
|---|---|---|---|
| `.ufo/waves/round-23/evidence/c1/uart-help.envelope.json` | 8504 | `462bc694a020c6b6eb9eeb171c5d7bfcf48c30a733ffe07c7df186b9d58c4d90` | matches W1 CounterRefusals.md:321 |
| `.ufo/waves/round-23/evidence/c1/uart-help.run.json` | 9723 | `20819612158048e687df0a59fab58b4d10bd71c238fc4bb0afa309bd846e4b17` | argv, env_overrides, exit 0, stderr `""` |
| envelope `data.evidence_id` | | `ev_4be13793b8a767184ddcfb301b3f0e06c1333e12e533347c68eb1b53d169e94a` | self-issued |
| `.ufo/waves/round-23/tools/sigrok-cli.sh` (698 B) | 698 | `50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902` | equals `data.subject.digest.sha256` and `normalized_result.tool.sha256` |
| `.ufo/waves/round-23/w1/_uart/sigrok-cli-0.7.2.tar.gz` | | `71d0443f36897bf565732dec206830dbea0f2789b6601cf10536b286d1140ab8` | show.c; configure.ac AC_INIT 0.7.2 (line 23) |
| `.ufo/waves/round-23/w1/_uart/libsigrokdecode-0.5.3.tar.gz` | 892783 | `c50814aa6743cd8c4e88c84a0cdd8889d883c3be122289be90c63d7d67883fc0` | member `decoders/uart/pd.py` = `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62`; member `decoders/uart/__init__.py` = `351098a23f5caa205068688550af53bd44a63776e1d02921ba32487ce720b92f` |
| `.ufo/waves/round-23/evidence/sources/sigrok-cli.1` | | `e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9` | equals tarball `doc/sigrok-cli.1` and the S058 row hash |
| `.ufo/waves/round-23/tool-runtime-pins.json` | | `02ef8379734f3bf9d25b893b7170e36aaab32805c542c613e399307490a68f73` | `captured_at` 2026-10-21T14:42:59.166503+00:00 |

Commands and results (all read-only, exit 0 unless noted):
- `git show <rev>:…/uart-help.envelope.json | sha256sum` gives `462bc694…`, 8504 bytes.
- `git show <rev>:…/uart-help.run.json | python3 -I -B` gives `run.stdout` byte-equal to the envelope file: True.
- `git grep -n -F 4be13793 <rev> -- corpus/` gives no output (no matches).
- `git grep -n -F 462bc694 <rev> -- corpus/ .ufo/waves/round-23/w1/` matches only W1 files (ConnectSourceChain.md:118, CounterRefusals.md:321).
- Model comparison, described under Findings F2: 81 expected lines, 81 actual, 0 mismatches.

## Verdict

1. **Bound and consistent (observed).** The subject is the committed wrapper. `run.stdout` is byte-equal to the envelope. The decoder selection `uart` is bound by argv, `parameters`, and `tool.arguments`. All 81 `help_lines` are reproduced by the upstream-source model with 0 mismatches. The tag omission is a real build-level omission, not truncation. Diagnostics are retained.
2. **Not counted (observed).** `uart-help` is not evidence-id bound in the candidate knowledge. Its `ev_4be13793…` id appears in no corpus file. Under `count-c1.py`, an envelope can bind only when a knowledge-cited id appears in it (line 111 collects ids from the knowledge text; line 123 requires `eid in blob`). The knowledge cites `ev_940cf7bb…`, `ev_bcadf773…`, and `ev_1d361f25…`, none of which is in the uart-help blob. So uart-help contributes 0 to k. This is an inference from code plus grep, not an executed count.
3. **Misattributed claim (observed).** The sentence "at least one actual direction is still required" (knowledge lines 30–31) is attributed to the help envelope. The envelope does not contain it. It says `Required channels: None.` (help line 46). Its only support is source code, `pd.py:505–507`, which raises `ChannelError('Need at least one of TX or RX pins.')` in the decode path.
4. **Source gap (observed).** S058 is the sigrok-cli manual (SOURCES.md:64). It does not contain the decoder help text. The manual has no "Possible decoder", "Baud rate", or "Annotation classes" help sections. It covers `-P` syntax and annotation-selection prose only. No admitted row covers libsigrokdecode 0.5.3 uart documentation, options, or annotation classes. S060 (SOURCES.md:66) lists inventory, decode-uart-hi, and decode-official-uart, and not uart-help.
5. **Unbound fields (observed).** The Documentation block comes from the runtime `decoders/uart/__init__.py`, which is not pinned. The pins cover `pd.py` only. Tool identity is pinned 4 min 52 s after the producer run. The ELF, libraries, and prlimit are not committed. REA 6.5.0 appears only in the run argv. The envelope's `provider.version` is `sigrok-cli@0.7.2`.

## Findings

**F1. Subject, run, and selection bindings hold (observed).**
- `data.subject.digest.sha256` and `data.normalized_result.tool.sha256` both equal the committed wrapper sha `50fe4359…` (698 bytes).
- `run.stdout` equals the envelope bytes (8504 bytes). `run.exit` is 0. `run.stderr` is `""`.
- `data.parameters` is `{decoder: uart, query: "", offset: 0, limit: null}`. Run argv is `… inspect-signal-decoders --decoder uart --all --format json --full-output`. `tool.arguments` is `--dont-scan --protocol-decoders=uart --show`, which matches show.c's `opt_pds && opt_show` branch at main.c:310–311.
- The wrapper is a plain `exec` with no output filter (sigrok-cli.sh line 15).

**F2. Literal help and the 81-line count (observed, plus model).**
- `help_lines` is numbered 1..81 contiguously. `output_window` is `{examined: 81, matching: 81, returned: 81, has_more: false}`.
- I rebuilt the output in memory from upstream sources. The inputs were `pd.py` class attributes (ast literal parse; `id`, `name`, `longname`, `desc`, `license`, `inputs`, `outputs`, `tags`, `optional_channels`, `options`, `annotations`, `annotation_rows`, `binary`; no `channels`, so "Required channels: None."), the `__init__.py` package docstring (srd reads `__doc__` from the package module at decoder.c:887–890, which is `py_mod` from decoder.c:705), and the show.c format strings at show.c:856–990. The model gave 81 expected lines and 81 actual, with 0 mismatches.
- Line 81 is a real output line. show.c:980–981 prints `"Documentation:\n%s\n"` with `doc[0]=='\n'` stripped. The docstring ends in `"or others.\n"` (`__init__.py` lines 37–38), so the printed text ends `"…or others.\n\n"`.
- The text is 81 newline-terminated lines. A naive `split("\n")` gives 82 elements, so the count of 81 requires splitlines-style normalization. The normalizer is not committed (REA rea-agents@6.5.0 is an npx fetch), so that normalization is unbound.
- The model assumes glib `g_variant_print` formats strings as `'x'` and integral doubles as `1.0`. The envelope agrees with that assumption; glib is not committed.
- "Literal" therefore means normalized-literal, consistent with upstream source. Byte identity with producer stdout is unverified.

**F3. Tags omission is literal, not truncation (observed).**
- `pd.py:94` declares `tags = ['Embedded/industrial']`.
- show.c:25–27 defines `DECODERS_HAVE_TAGS = (SRD_MAJOR > 0) || (SRD_MAJOR == 0 && SRD_MINOR > 5)`. For libsigrokdecode 0.5.3 that is 0.
- show.c:896–897 prints the `Decoder tags:` header with nothing under it when the macro is 0. Envelope help lines 10–11 match exactly. No tag claim should be drawn from this envelope.

**F4. Options: no selection is retained, and none is claimed (observed).**
- The 12 `Options:` entries (help lines 51–62; `pd.py:101–123`) are catalog text. show.c:962–976 prints every option with its values and default.
- `parameters` has no option field. `tool.arguments` has no `--protocol-decoder-options`. The run argv has none either.
- The knowledge (lines 28–33) makes no option-selection claim for uart-help. Any "selected options" wording would be unbound.

**F5. Decoder module identity is partly bound (observed).**
- Runtime `pd.py` pinned at `51a29d0e…` (tool-runtime-pins.json) equals the upstream tarball member. This is a hash match, so the same bytes at one instant.
- The Documentation block comes from `__init__.py` (help lines 63–81 match tarball `__init__.py` lines 21–37 line-for-line). That file has no pin, so the runtime copy that produced the envelope is unbound.

**F6. uart-help has no id binding and no source-row registration (observed).**
- `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` cites the uart-help path (lines 28–29) but not its id.
- SOURCES.md has no row listing uart-help.
- W1 PlannerDataWalk.md:158 already says the verb "still counts through inventory.envelope.json" because uart-help's id is absent. My independent check agrees.
- Caveat: the verb-level hold, if any, rests on the inventory envelope. I did not evaluate inventory, which is sibling scope.

**F7. Diagnostics are retained once and not independently bound (observed).**
- `data.normalized_result.diagnostics` is the three-line CPython prefix message ("Could not find platform independent libraries <prefix>…").
- `run.stderr` is `""`, and that is the REA CLI's stderr, not the child's. The child's stderr has no separate capture.
- The knowledge's "remain visible; exit0 did not erase them" (line 33) is accurate.
- The `--version` record (sigrok-version-attempt1.json, stderr `""`) does not load decoders, so it does not contradict the message.
- The inventory's signature-module failure, which the knowledge describes at lines 21–26, is absent here. This is an inference from the absence, since this run loads only `uart`.

**F8. Version banner is retained but undated (observed).**
- `tool.version_banner` is byte-equal to `sigrok-version-attempt1.json` stdout. That record has no timestamp, so the banner is not bound to the uart-help run instant.
- The format matches show.c:70–122.

**F9. Run-time tool identity is post-hoc (observed).**
- The run captured_at is 2026-10-21T14:38:07.478161Z. The pins captured_at is 14:42:59.166503Z.
- The pins therefore cannot show which files executed. Only the wrapper is bound at run time (F1).
- W1 ConnectSourceChain.md:32 says "Which files actually executed". That is not supported by the pins.

**F10. Producer version and environment are partial (observed).**
- "6.5.0" appears in `run.argv` only (`npx -y rea-agents@6.5.0`). It is absent from the envelope. `meta` is `{command, duration}`.
- No integrity digest for the npm package is committed, so npx resolution is unbound.
- The knowledge (line 2) says "argv/environment/…". Only `env_overrides` (one key, REA_SIGROK_COMMAND) is retained.

**F11. Limits: part declared, part applied (observed).**
- `resource_limiter.arguments` (`--as=1073741824`, `--fsize=67108864`, `--cpu=30`, `--core=0`) matches `limits.address_space_bytes`, `file_bytes`, `cpu_seconds`.
- `input_bytes`, `output_bytes`, and `command_timeout_ms` have no committed source. They are provider declarations.
- The knowledge's "declared/measured provider settings" over-states "measured" for those three. Only prlimit application is measured.
- `resource_limiter.sha256` (`/usr/bin/prlimit`, `092bb6db…`) is a host binary. It is neither committed nor pinned.

**F12. No catalog-as-functionality inference is present (observed).**
- `normalized_result.decoders` is `[]` for this selection, so `uart` appears only in `help_lines`. This envelope is help, not catalog membership.
- The knowledge never infers that the decoder works from this envelope. "UART help/selected decoding succeed separately" (line 25) refers to `ok:true` on each call.
- The docstring's capability text ("This decoder should work on all UART-like async protocols…", `__init__.py` lines 24–26) is the decoder author's prose. REA labels it help, not validation. Reading it as functionality would be the overreach to avoid.
- `authority: shipped-artifact` and `confidence: observed` are REA labels on a lane-local launcher. The knowledge does not repeat them and they are not publisher authority.

**F13. Refusal shape (observed).**
- The only refusal-shaped key in the envelope is top-level `ok: true`. Scanned keys: error, errors, code, status, completion_status, exit_code, refused, refusal, finding, ok, reason, message.
- So the uart-help envelope is not a refusal, and the "refusal counted" falsifier does not arise for it.

## Claimed-field binding table

| Claimed or retained field | Where retained | Independently bound? | Status |
|---|---|---|---|
| Subject = committed wrapper | `subject.digest`, `tool.sha256` | yes, sha `50fe4359…` = committed bytes | bound |
| Producer stdout = envelope | `run.stdout` | byte-equal | self-consistency |
| Decoder `uart` selected | `parameters`, run argv, `tool.arguments` | argv and record agree | bound to producer invocation |
| 81 help lines, literal | `help_lines`, `output_window` | upstream model 81/81; raw stdout not retained | normalized-literal; byte-literal unbound |
| Documentation block (help 63–81) | `help_lines` | tarball `__init__.py` match; runtime file unpinned | source-consistent, runtime unbound |
| Annotation, option, binary text | `help_lines` 12–62 | `pd.py` hash equal to tarball | bound to upstream (pins post-run) |
| Tags absent | none | `DECODERS_HAVE_TAGS=0` | literal omission |
| Options selected | none | none | not retained; not claimed |
| Diagnostics | `diagnostics` | none independent | retained, single copy |
| Version banner | `tool.version_banner` | equals undated attempt1 stdout | retained, undated |
| Run-time ELF and libs | pins only | not committed; pins at 14:42:59 | unbound at run time |
| prlimit sha | `resource_limiter.sha256` | not committed, not pinned | unbound |
| Limits: input, output, timeout | `limits` | none | declared |
| prlimit ceilings | `resource_limiter.arguments` | matches `limits` | consistent |
| REA 6.5.0 | run argv only | npx, no integrity | unbound |
| Environment | `env_overrides` (one key) | none | partial |
| evidence_id `ev_4be13793…` | envelope and run | self-issued | not cited in knowledge, so not countable |
| "RX optional" | `Optional channels` rx, tx; `Required channels: None.` | literal | bound |
| "at least one direction required" | not in envelope | `pd.py:505–507` | misattributed to help envelope |
| Exit 0 and diagnostics retained | run and envelope | run exit 0 | bound |

## W1 proposal re-evaluation against candidate (stale items)

- **CoverageMap.md:69**: 8504 bytes, ev id, 81 help lines, `has_more:false`. Confirmed.
- **ConnectSourceChain.md:52–53**: "exact byte comparison not run". Still true, since raw stdout is absent. The model check (81/81) now supports the content claim.
- **ConnectSourceChain.md:116–119**: a k=3/6 projection that cites uart-help as an inspect-signal-decoders witness. Not supported by the binder. The verb holds, if at all, via inventory. W1 overstates uart-help's role.
- **PlannerDataWalk.md:158**: "does not include ev_4be13793…; counts through inventory". Confirmed.
- **ConnectSourceChain.md:31–32**: pins `02ef8379…` and extraction `2b84f466…`. The pins hash is confirmed. "Which files actually executed" is not supported (F9).
- **CoverageMap.md:246**: the W1 proposed S058 row adds "REA6.5.0 inspect-signal-decoders catalog and decoder-help pages". The candidate S058 row is the manual only (SOURCES.md:64). The proposed row is not in the candidate.
- **CounterRefusals.md:169**: `uart-help.envelope.json` maps to `ev_4be13793…` `inspect_signal_decoders`. The id matches the envelope. Confirmed.

## Produced files and hashes

- This report: `.ufo/waves/round-23/w2/OriginalUartHelp.md`. Hash recorded in the handoff after write.
- Scratch copies of `uart-help.envelope.json` and `uart-help.run.json` were written to `.ufo/waves/round-23/runtime/OriginalUartHelp/` (ignored runtime path). They duplicate committed bytes and were removed after review.
- One accidental scratch file `/tmp/__omp_show_c_candidate.c` was created, outside the allowed write paths, and removed. Its absence was verified.
- No other files were written. No peer report was edited.

## Installs

None. No install, update, or pacman operation was run.

## Open risks and unknowns

- Raw sigrok stdout and the REA normalizer are not committed. Byte-literal help and the splitting semantics for the 81st line cannot be proven from committed bytes.
- Runtime binaries, the AppImage, host libraries, and prlimit are not committed. Run-time custody is unknown.
- The inventory envelope, which is the only id-bound holder of inspect-signal-decoders, was not evaluated (sibling scope). If it fails the binder or the refusal scan, the verb is unheld at candidate, and uart-help cannot rescue it under current citations.
- `evidence_id` is self-issued and not recomputable from committed bytes. Binding is text equality, not authentication.
- The model comparison assumes glib formatting and that srd reads `__doc__` from the package module. The envelope's agreement supports both but does not prove them.
- Counting-effect statements are inferences from code and grep. The counter was not run.

## Recommendations for L1 (not applied; I did not edit production files)

1. If uart-help should be an id-bound witness, cite `ev_4be13793b8a767184ddcfb301b3f0e06c1333e12e533347c68eb1b53d169e94a` in the knowledge entry. Expected effect on k is zero, because `exercised` is a boolean and inspect-signal-decoders is already held through inventory, if inventory binds.
2. Re-attribute "at least one actual direction is still required" to `pd.py:505–507` (decode path), or tag it `[INFERENCE]`. Remove "retains" for that clause.
3. Source the help documentation and option text with a mined A/B row for libsigrokdecode 0.5.3, citing tarball `c50814aa…`, `pd.py` `51a29d0e…`, and `__init__.py` `351098a2…`. S058 cannot carry it.
4. Pin `decoders/uart/__init__.py` in tool-runtime-pins, or drop "installed module's literal help" wording.
5. Replace "measured" with "declared" for the input, output, and timeout constants. Replace "environment" with "env_overrides".
6. State that the tool-runtime pins post-date the run by 4 min 52 s.
