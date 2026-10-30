# RevSweep — round 51 wave 1

Recommendation: do not integrate misroot-sweep.sh snapshot D99A unchanged.

1. High: filename-only classification selects foreign round-51 files for deletion and misses kaidoku content under neutral filenames (helper lines 6–11, 23, 35–41).
2. High: no forbidden-prefix or resolved-destination containment checks; apply can touch excluded paths or follow destination-parent symlinks outside the lane (lines 23–25, 35–41).
3. Medium: collapsed untracked directories cannot be recovered per-file; cmp failure deletes the lane target beyond the allowed operation; selftest defaults to `/tmp` unless TMPDIR is supplied (lines 27, 39–40, 47).

Full numbered findings, contract mismatch, evidence, and verification gaps: `.ufo/waves/round-51/w1/RevSweep/findings.md`.

Draft initially absent, then available and reviewed statically. Producer notified of concrete defects. Default report branch has no explicit write command; fixture git identity is locally scoped with toplevel assertion. Neither observation is a runtime pass.

LSP unavailable (`xd://lsp`: no such tool); text review only. Helper/selftest/REA: not run. No installations, scratch files, mutations outside this seat's two report files, or git mutations. Specific misroot exception was not located in the named protocol text; assignment supplies the reviewed copy/cmp/delete requirement. Claims lines 178–181 must distinguish report-only default from authorized apply before freeze.
