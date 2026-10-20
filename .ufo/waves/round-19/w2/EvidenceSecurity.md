# Round 19 W2 — Evidence security scan

## Scope and method

Scanned the committed Git objects under `.ufo/waves/round-19/runs/`, `evidence/`, and `w1/` (including nested reports and inherited patches) at `refs/heads/main` = `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`. The start and end `main` observations were identical. Coverage: 256 tracked blob entries, 6,247,453 bytes, zero symlink entries. The scan emitted only paths, line numbers, and match classes; it did not print credential values.

Bounded signatures checked: session/credential/auth/private-key-like filenames (including `session.json`); PEM/PGP private-key blocks; JWT and common AWS, GitHub, Slack, bearer, and Basic token forms; URL userinfo and cookie headers; and non-placeholder values associated with password, secret, token, authorization, cookie, session, and related auth-field names.

## Findings

**Severity: Low / no confirmed credential exposure.** No credential/session/private-auth-like filenames matched. No known-format private key, token, URL-userinfo, or cookie signatures matched.

**Observed candidate matches:** four non-placeholder auth-field-value candidates, all in `.ufo/waves/round-19/w1/inherited/ProvincePinsTool.patch` at patch-file lines **408, 458, 463, and 467**. The patch adds `.ufo/waves/round-19/tools/province-pins.py`. Structural inspection of the added source found a module-level `SECRET` constant; the three `write_live` secret-field references are called only from `_selftest`, while `note_output` checks that the constant is absent from captured stdout/stderr. No matching value is reproduced here.

**Inference:** the four candidates are consistent with a test canary and mock configuration fixtures, rather than live auth data. The scan cannot establish from pattern matches alone whether a hard-coded canary was ever reused as a real credential. No other candidate path or content hit was observed in the requested committed scope.

**Exploit path and impact:** no exploit path or live session/credential disclosure is established by this evidence. Conditional risk is limited to the case where the source-level canary is a real credential reused elsewhere; that is not supported by the observed test-only fixture callsites and output-leak check.

**Smallest remediation:** none indicated by current evidence. Keep the canary confined to synthetic self-test use; if it is or was a real credential, rotate it and replace it with a disposable test-only value.

## Commands and exit codes

Commands were read-only. The scanner used Python evaluation to pass the tree's blob IDs to `git cat-file --batch`; it emitted metadata only.

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
exit 0 — d0690fd44f46d8a7fe9da5f01c6be723d12abd41 (observed both before and after scan)

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r -z --full-tree d0690fd44f46d8a7fe9da5f01c6be723d12abd41 -- .ufo/waves/round-19/runs .ufo/waves/round-19/evidence .ufo/waves/round-19/w1
exit 0 — 256 tracked blob entries

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file --batch
exit 0 — stdin was the 256 blob IDs from the scoped tree; 6,247,453 bytes scanned

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show d0690fd44f46d8a7fe9da5f01c6be723d12abd41:.ufo/waves/round-19/w1/inherited/ProvincePinsTool.patch
exit 0 — blob read for structure-only attribution; AST parse succeeded
```

## Limits

This is a bounded pattern scan of the specified committed subtrees only. It does not cover untracked/worktree files, external systems, arbitrary encoded or unfamiliar token formats, or credential-like strings with no matching field/signature. It does not execute artifacts or validate whether the candidate canary is live anywhere outside this scope.
