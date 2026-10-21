HOLDS — the scoped claim “10/11 closed at S; D5 only open; strict exit 1” reproduces exactly.

## Measured result

**Observation.** Ran:

```text
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/routed-r19.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 --strict --live
exit=1; stderr empty
```

Output resolved the requested revision and reported `named_open=0`, `substance_open=1`, `open_count=1`:

| Item | named | substance | why |
|---|---:|---:|---|
| D1 | true | true | both name and substance checks passed |
| D2 | true | true | both name and substance checks passed |
| D3 | true | true | both name and substance checks passed |
| D4 | true | true | both name and substance checks passed |
| D5 | true | false | final-census.json absent or invalid at REV |
| D6a | true | true | both name and substance checks passed |
| D6b | true | true | both name and substance checks passed |
| D6c | true | true | both name and substance checks passed |
| D6d | true | true | both name and substance checks passed |
| D6e | true | true | both name and substance checks passed |
| D6f | true | true | both name and substance checks passed |

**Observation.** The no-`--live` variant also exited 1 with `open_count=1`, `named_open=0`, `substance_open=1` and the same item booleans. `python3 -I -B .../routed-r19.py --selftest` exited 0 (`SELFTEST: CLEAN cases=4`: token-only closures stay open, missing name counts open, strict open exit, AST/revexec-only). At baseline B, the strict counter exited 1 with 11 open, all 11 unnamed and without substance. The counter source hash was identical at S, the worktree, and HEAD: `548b8ac791245cf69cc8b93e89ffca3b90b4b37db51674de722c319a7a133bd2`.

## Substance and D5 check

**Observation.** The counter enumerates all 11 items at `routed-r19.py:55`, reads revision blobs for naming at `:190-218`, evaluates every substance function and counts an item open unless both fields pass at `:1018-1045`; strict mode maps any open item to exit 1 at `:1049-1050`. Its substance checks are not name-only: D1 executes in-worktree refusal and outside-scratch cleanup checks (`:352-396`); D2 requires the baseline future-timestamp finding and future/past selftest (`:413-435`); D3 checks carrier-guard selftest plus retained arm/check/disarm evidence (`:485-567`); D4 archives S and runs the census on that export (`:609-642`); D6a-f run/recompute the named lint, sandbox, slug-escape, argv-decoy, seat-name, and `jj_` cases (`:695-992`). `measure` converts check exceptions to `substance=false` (`:1020-1024`).

At S, `git rev-parse HEAD` and S both returned `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`. `git cat-file -e 'S:.ufo/waves/round-20/verify/final-census.json'` failed (exit 128: path absent); the same check at HEAD also failed (exit 128). This is the observed reason D5 is open at S. The D5 logic requires a successful record, argv lists, a safe stdout path and matching stdout hash, then verifies the record revision differs only by the record/stdout pair (`routed-r19.py:644-682`).

**Scratch control (observation, not a lane write).** In a clean `/fast/scratch` clone at S, `final-census.py --root <clone> --out-dir .ufo/waves/round-20/verify` exited 0; the record named S, had `exit=0`, `worktree_clean=true`, and its stdout SHA-256 matched the retained bytes. After committing those two outputs as fixture commit `04140e19254b323ff6aa7d2673735fbf495fb9d8`, the strict counter exited 0 with all 11 items named and substantive (D5 included). This confirms the D5 gate accepts the intended record shape; it is not evidence that the real lane has yet landed that final record.

## Residual risk and verification gaps

**Observation.** At inspection time HEAD was still S and the final-census record was absent there. Thus this seat verifies the requested S result, not the eventual delivered-tip census/record. `claims.json:15-18` describes final closure and says any open item at the measured source revision falsifies C1; that broader C1 end-state is not established by this intermediate-S run. The scratch `/tmp` clone attempt was discarded: `PrivateTmp=yes` hid its path from sandboxed checks; relocating the fixture to `/fast/scratch` made all 11 pass. No LSP device/server is mounted (`read xd://lsp` returned “No such tool”); no semantic references/definition/diagnostics were available. Static anchors used: claims `:15-18`; lesson `:66-84`; counter `:55`, `:207-218`, `:352-396`, `:413-435`, `:485-567`, `:609-682`, `:695-992`, `:1005-1050`; final-census record creation `final-census.py:130-199`.