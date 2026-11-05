# ReviewerRepair — R91-C1 surgical correctness review (candidate vs predecessor)

Seat: ReviewerRepair (w1). Lane: kaidoku-shokunin. Frozen revision measured: `deb2765a55fef0e4e81500a027dfe59951b69e87`.
Candidate: `tools/round-91/upx-stop-boundary-repair.py` sha256 `473bb3a937a60b0b785a6c814b0e25cacc67c97b85cc1cb9704985781d829b91` (matches claims.json pin).
Predecessor: `tools/round-90/upx-break-repair.py` sha256 `90dea08720a37e876e7f08eafe339a62c710baf402c1342924f9b41b44d5cd6a` (matches pin), run from a scratch clone checked out at the frozen rev.
Worktree drift: `git diff --stat deb2765a… -- tools/round-87 tools/round-88 tools/round-89 tools/round-90 tools/round-91` is EMPTY — the working-tree modules the candidate loads are byte-identical to the declared ones.

Pins re-verified against `claims.json` instruments: upx `cf2f6e7c…`, r87 `96da7d8e…`, r88 `59ee51b0…`, r89 `41f29f21…`, r90 `90dea087…`, candidate `473bb3a9…`, battery `5998b6bd…` — all match. No tools were installed or upgraded (operator tooling authorization unused); upx 5.2.0 and system Python 3.14 preexisting.

## (1) Branch-by-branch diff of `repair()`

Both at the frozen rev. Candidate `repair()` = `tools/round-91/upx-stop-boundary-repair.py:164-198`; predecessor = `tools/round-90/upx-break-repair.py:252-293`.

| # | Branch | Candidate | Predecessor | Can change a byte? | rc 0 with changed file? | Output on refusal? |
|---|--------|-----------|-------------|--------------------|--------------------------|--------------------|
| a | ELF guard (`:165-166`) | identical | `:258` | no | — | no (rc 2 both, observed on non-ELF) |
| b | Module loads + pins (`:167-172`) | loads r87/r88/r89 **and r90**; records only `r90_sha256` (re-reads R90 bytes) | loads r87/r88/r89, digests all three (`upstream_sha256`/`r88_sha256`/`r89_sha256`) | no | — | — (info/stdout content only) |
| c | Classification (`classify` `:124-134` via `r90.longest_prefix/chain_ok/accounted`) | byte-equivalent to predecessor's inline `:275-281` (same frozen functions) | — | no | — | — (verified: same prefix/stored_total on all fixtures) |
| d | prefix <2 or none (`:175-179`) | `r90._block0(...)` + dead `setdefault` | own `_block0` (`:274`, `:291`) | no (same r89 law, same args) | only as predecessor did (r89 repairs) | — |
| e | prefix ≥2, `derive_break` patches (`:181-184`) | `r90.derive_break(d, rep, r88, min_total, u_len)`, `min_total = stored_total if stored_ok else None` — identical args to predecessor's two branches (`:282-283`, `:286-287`); `_patched` unchanged | same | window-only 4-byte patch, unchanged from predecessor | only as predecessor did (P1 class) | — |
| f | prefix ≥2, `derive_break` → None (**the changed branch**, `:189-196`) | `upx_test(d)`: green → `return d` identity, rc 0, class `intact`; red → typed `stop-boundary` refusal rc 2, no output | stored_ok: `return _block0(...)` (`:284`) — rc 0, may return broken bytes unchanged or write sentinel bytes outside the window; not stored_ok: `Refused` rc 2 (`:289`) | **no** — green arm returns the input byte-identical; red arm writes nothing | **no** (green output == input, sha-verified) | **no** (out-ABSENT observed on both directions) |
| g | `upx_test` (`:137-159`) | NEW external call `/usr/bin/upx -t -q` on a TMPDIR temp copy | none | no (temp removed; never produces output bytes) | — | — |
| h | Exception mapping (`:197-198`) | catches **only `rep.Refused`** | same (`:292-293`) | no | — | see MED-1: round-90-module `Refused` escapes to rc 1 |
| i | `main()` write path (`:286-293`) | `write_atomic` without OSError→Refused conversion; `except Exception` → rc 1 typed JSON | `write_atomic` converts post-mkstemp OSError → Refused rc 2 (`upx-break-repair.py:132`); its own `Refused` caught → rc 2 (`:433-435`) | no | — | refusal still writes no output; rc differs on write-failure paths (LOW-2) |

Net: no branch of the candidate can return rc 0 with a changed file where the predecessor did not, and no branch writes an output file on refusal (verified empirically below). The claim sentence "identical to the round-90 repair in every branch except the one it previously fell through" is inaccurate in exactly two places: branch (f) also changed the `not stored_ok` refusal sub-branch (LOW-1), and the exception surface of branches (d)/(e) changed (MED-1).

## (2) Three concrete inputs (plus one bonus), observed behavior

Fixtures in scratch (`S=/fast/scratch/hyaku/kaidoku-r91/ReviewerRepair/work`):
- `python3 -I -B tamper.py`-style layout (battery-equivalent `layout()`): xxd packed to 19,560 bytes, sha256 `1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff`, **5 walkable blocks**, last block at offset 15455, stored `sz_cpr` 163, `sz_unc` 784.
- `xxd-last+7.packed` (value 170, sha256 `8c829813238f52da25880f2f17a9bdfc12f084e4dd224a327268a1cd542631f7`); `xxd-last-7.packed` (value 156, sha256 `bde43bc6d56432ce5570f320e2b82f13a7cdcc257cc1800e75f5e4ecc63f2d69`); `nonelf-4k.bin` (4,096 urandom bytes, sha256 `13452efee661ee772ba86dbeb2fe85a684664d29c1b05d9858f1384ff661032e`).
- Direct packer verdict: `/usr/bin/upx -t -q xxd-last+7.packed` → `Exception: compressed data violation`, rc 1; on `xxd-packed` → rc 0.

Command form: `TMPDIR=$S/tmp python3 -I -B <tool> --in $W/<f> --out <o> --info <i>`; rc, output presence and output sha256 recorded.

| Input | Candidate (r91) | Predecessor (r90 at frozen rev) |
|---|---|---|
| `xxd-packed` (intact) | **rc 0**, out present, sha `1727faf9…` = byte-identical, stdout `{"class": "intact", "break_index": null, …}` | rc 0, out present, sha `1727faf9…` byte-identical, class `intact` via block-0 law (derived 249 == stored 249) |
| `xxd-last+7.packed` | **rc 2**, out **ABSENT**, `{"refused": "stop-boundary: … no successor that accounts for the declared u_len (38928) and \`upx -t\` refuses the input (prefix 5 blocks, stored_total 38928)…"}` | **rc 0**, out present, sha `8c829813…` = the tampered input returned unchanged (the QUALITY-167 silent defect) |
| `xxd-last-7.packed` | **rc 2**, out **ABSENT**, same `stop-boundary` refusal (stored_total 38928) | **rc 0**, out present, sha `bde43bc6…` = tampered input returned unchanged |
| `nonelf-4k.bin` | **rc 2**, out ABSENT, `"refused": "not a little-endian ELF"` | rc 2, out ABSENT, identical message |
| `/usr/bin/xxd` (plain ELF, N1-like) | **rc 2**, out ABSENT, `"refused": "upstream refusal: no validated PackHeader in the tail window"` | rc 2, out ABSENT, identical message |

Candidate selftest: `python3 -I -B …/upx-stop-boundary-repair.py --selftest` → `SELFTEST cases=4 failures=0` (exit 0). The candidate's observed behavior on the frozen class (refuse ±7, identity when intact, no unsafe byte, no output on refusal) is exactly the declared contract; the predecessor's rc-0-silent behavior on the same bytes reproduces the declared "before".

## (3) `upx_test()` temp-file handling

`tools/round-91/upx-stop-boundary-repair.py:137-159`.
- **Location**: `tempfile.mkstemp(prefix=".r91-test-", dir=tempfile.gettempdir())` — honors `TMPDIR`; the batteries set `TMPDIR=<work>/tmp`, so the temp never lands in the invocation box (isolation control unaffected) nor in `/tmp`.
- **Collision-free**: `mkstemp` (O_EXCL, random suffix) — yes.
- **Removed on every path**: `finally: os.unlink(path)` (`:152-157`) covers success, `upx -t` nonzero, subprocess raise (timeout/FileNotFoundError) and write errors. Verified empirically: with `TMPDIR` pointed at an empty watcher dir, the dir is empty after both a red run (+7, refusal) and a green run (intact). Only nit: if `os.fdopen(fd)` itself raised, the file is still unlinked but the bare fd would leak — not reachable in practice.

## (4) Composition and read scope

- Modules are loaded **by absolute path under ROOT**: `:53` `ROOT = dirname³(abspath(__file__))` (self-relative, not cwd-relative); `:167-170` `load_module(os.path.join(ROOT, R87/R88/R89/R90), …)`. Invoked in-lane, that is the lane tree; verified byte-identical to the frozen rev (empty diff above).
- **Reads outside the lane**: none. The tool reads only (i) the caller-supplied input, (ii) the four module files under ROOT plus a re-read of R90 for its pin (`:171-172`), and executes `/usr/bin/upx` (absolute path; child env has `HOME=tempfile.gettempdir()` so even packer HOME writes would land under TMPDIR). `upx -t` output is consumed as a returncode only. Caveat: a copy of the script outside the lane resolves ROOT against the copy's tree (observed: a bare scratch extraction failed with `FileNotFoundError: …/kaidoku-r91/tools/round-87/…` and never touched the lane) — in-lane and clone invocations are the supported paths.

## Findings

**HIGH** — none. The candidate's changed branch does what the claim says on measured bytes: refuse both directions with no output, return identity on the intact carrier, no unsafe write anywhere.

**MED-1 — upstream typed refusals are demoted to rc 1 `error` instead of rc 2 `refused`.**
`repair()` catches only `rep.Refused` (`tools/round-91/upx-stop-boundary-repair.py:197-198`), but `r90._block0`/`derive_break`/`_patched` raise the **round-90 module's own** `Refused` (e.g. `tools/round-90/upx-break-repair.py:314-315` `"round-89 refusal: …"`), which escapes to `main()`'s `except Exception` (`:290-293`) → rc 1. The predecessor caught its own class in `main()` (`upx-break-repair.py:433-435`) → rc 2.
Repro: `python3 -I -B tools/round-91/upx-stop-boundary-repair.py --in xxd-b0zero.packed --out o` (xxd-packed with block-0 `sz_unc` zeroed at b0=576, crafted in scratch).
Observed: candidate rc 1 `{"error": "Refused: round-89 refusal: no l_info candidate carries a derivable first block"}`; predecessor rc 2 `{"refused": "round-89 refusal: no l_info candidate carries a derivable first block"}`.
Frozen-claim impact: none found — the scored populations do not reach the escape: T7 cells decide at `:189-196` (observed), plain-ELF N1 maps at classify via `rep.Refused` → rc 2 (observed, both tools), P2/P3 reach r89's derivation with `sz_unc0 ≠ 0` so it does not refuse. It violates the tool's own docstring contract ("2 = typed refusal") on an adjacent class and would mislabel an upstream refusal as an internal error for any caller keying on rc 2.

**LOW-1 — second behavioral change beyond the declared fall-through (docstring overstates "identical in every branch").** For prefix ≥2 with a broken stored chain, `derive_break` → None now runs `upx_test` and returns rc 0 identity where the predecessor refused rc 2 (`upx-break-repair.py:289` vs candidate `:189-191`). Semantically sound (`upx -t` green ⇒ intact ⇒ identity is the right verdict), unscored. Could NOT reproduce: it needs a file whose chosen longest-prefix chain fails r87's sentinel walk while `upx -t` is green (a non-canonical candidate walking past the canonical one) — not constructed.

**LOW-2 — write-failure exit-code mapping diverges.** Candidate `write_atomic` (`:101-121`) does not convert post-`mkstemp` OSErrors to `Refused`; predecessor did (`upx-break-repair.py:132`, rc 2). On `mkstemp` failure itself both exit 1 — observed on an unwritable outdir: candidate rc 1 typed JSON (strictly better), predecessor rc 1 raw traceback. The ENOSPC-class write/replace sub-path (candidate rc 1 vs predecessor rc 2) was NOT separately reproduced (no cheap full-filesystem harness); same exception-mapping family as MED-1. Candidate also adds an `--out`-is-directory guard (`:96-97`) the predecessor lacked (both end rc 2 there).

**LOW-3 — `upx_test` environment coupling** (`:148-152`): hard-coded `/usr/bin/upx` → `FileNotFoundError` → rc 1 typed error if the packer is absent (not a refusal); a packer segfault/negative rc on an intact file would be read as red → false refusal (theoretical, not reproduced); `timeout=600` sits inside the battery's own 600 s child timeout, so a hang would surface as the battery's `rc None` "other" cell, not the repair's refusal.

**LOW-4 — dead code**: `info.setdefault("class", "block0-or-intact")` (`:177`) can never fire — `r90._block0` always sets `class` (its own `setdefault("intact")` at `upx-break-repair.py:316` or r89's class value). Cosmetic.

**LOW-5 — observability**: the candidate's `--info`/stdout drop fields the predecessor emitted (`stored_accounted`, `sentinel`, `candidates`, the r87/r88/r89 digest pins; it records only `r90_sha256`, `:171-172`). Both counters parse neither stdout nor `--info` content (they read rc, output bytes, box listing), so no scored impact.

## Verification gaps

- Manual runs covered the xxd carrier (both directions), intact, non-ELF, plain ELF and the crafted b0zero input. The remaining six T7 cells (jq, libz, docker-init) were not manually driven here; the shared code path is input-independent (classification + `upx_test` gate), and the 8-cell battery receipt is the executor's instrument.
- LOW-1's green-on-broken-chain corner and LOW-2's ENOSPC sub-path are reasoned from code, not reproduced (constructed inputs or a filesystem fault injector would be needed).
- MED-1's fix (catch `r90.Refused` alongside `rep.Refused` in `repair()`) is a recommendation only; this seat edits nothing.
