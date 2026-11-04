# SentinelScope — round 71 / attempt 1 / w1

Audit target: frozen commit `b827a8b5d54f2885ec9be7786389f356c59226ce`, base `82c8e620c9222fb218aa0260570a3765da2afb44`. Read round-70 verifier spot-check first, including all seven routed items. Axes: credential exposure; scratch containment; completeness of child-environment evidence; network; nonce confidentiality; write scope/process cleanup. This is a safety report, not a claim judgment or remediation.

## Blocking

### SS-1 — receipt-controlled destination escapes `--work`

**Evidence:** `tools/round-71/controls.py:84-91` reads `carriers[0].runs.pack.argv[0]` from the round-70 receipt, then calls `makedirs`, `copy2('/usr/bin/upx', expect_upx)`, and `chmod` on that path. The frozen committed receipt actually names `/fast/scratch/hyaku/kaidoku-r70/l1/landing/upx-pinned-copy`, outside any round-71 seat scratch. Its enclosing `finally` at 194-195 only removes `scratch`.

**Exploit path / impact:** running the normal controls on the real lane resurrects/writes another run's path; a replaced receipt can select any writable destination and overwrite it with the packer, including through a symlink. This is an actual scope escape in the frozen implementation, not merely the dead scratch-pointer reporting limitation from round 70. No exploit executed here.

**Smallest remediation:** copy the packer only into controls' newly allocated scratch and thread that path through a scratch-owned fixture receipt, or run unchanged historical receipts inside a filesystem sandbox mapping that historical location to seat-owned scratch. Never grant a receipt write authority. ExecControls independently reports using the latter sandbox, with host root read-only, to obtain its receipts; that containment does not repair the frozen code.

### SS-2 — “every child observed” is not implemented

**Evidence:** `packed-elf.py:285-315` captures only calls supplied `capture`; REA's `rea()` at 399-401 never passes capture (therefore analyze/decompile are omitted). The `score()` git child at 758-762 uses direct `subprocess.run`, also uncaptured. A8 at `seam-probe.py:354-368` checks only basename presence `{upx,node,readelf}`: captured `node --version` at `packed-elf.py:475-478,810-811` satisfies node without any REA child. The launcher records `dict(os.environ)`, not a `/proc/self/environ` read as the documentation states.

**Exploit path / impact:** a regression confined to REA execution's environment could retain A8 green because the observed node is a version probe, not an analysis/decompile process. Git observations are absent outright. The present score route does pass `cenv` to those children, but the claimed runtime evidence is incomplete. Additionally receipt-check mode inherits the caller environment in `git_blob_sha256()` at 500-502 and `run(['readelf',...])` at 687-689, whose `env` defaults to None at 305-315.

**Smallest remediation:** thread capture through REA and git and require the actual REA argv plus git in the raw-log inventory; pass the same explicit environment to checker children or explicitly exclude checker mode from the claim. Describe the actual launcher observation honestly. Preserve the one declared `PYTHONCOERCECLOCALE` exclusion rather than silently excluding anything else.

## Advisory

### SS-3 — selftest writes outside caller work unless separately contained

**Evidence:** `packed-elf.py:1033` uses `mkdtemp(prefix='packed-selftest-')` without `dir`; `main():1103-1104` ignores `--work` for selftest. `seam-probe.py:139-155,247` invokes this selftest with an environment omitting TMPDIR, even though `--work` is passed. This reaches the platform temporary default rather than the seat work root. Selftest does remove its allocated child at 1055-1056. `registry-census.py:245-249` chooses TMPDIR or a shared `.../registry-census-selftest` parent, not `--work`; TemporaryDirectory removes its child but not a newly created parent. Forged-receipts CLI correctly requires work at 591-597 and cleans the selftest child at 529-530; its internal fallback is unreachable through that CLI.

**Impact:** seat scope is not preserved by selftest defaults; shared-parent residue is possible. **Smallest remediation:** require caller-owned work and use it explicitly for every temporary root, including selftests; do not rely on environment survival through probe invocation. No selftests executed by this seat.

### SS-4 — scratch and process cleanup are partial

**Evidence:** `seam-probe.py:194-202,260,280,292,327,379,481,527-533` creates roots but has no cleanup/finally for any of them. `forged-receipts.py:261-446` similarly never removes its full-battery scratch. `packed-elf.py:768-791` can fail after preflight but before its carrier-loop finally (831-917), leaving run_root behind. Concurrent probe Popen children at `seam-probe.py:383-419` have no enclosing kill/wait finalizer if communication times out or an earlier operation raises.

**Impact:** caller cleanup is required on success and failure; interrupted concurrent probes can leave children running against deleted fixtures. **Smallest remediation:** put full per-run lifetimes inside finally/TemporaryDirectory, and on any concurrent failure terminate then reap all started children. Preserve receipts before removal. Static finding; no timeout/cleanup attack executed.

### SS-5 — nonce plaintext publication must not follow ordinary receipt filing

**Evidence:** `packed-elf.py:920-935` writes `run_nonce` plaintext in the normal output receipt; `--skip-run` does so too (818-826). The code has no publication/redaction distinction. The frozen claims' A2 says the landing nonce lives only in scratch.

**Impact:** committing the raw run receipt would disclose the nonce and contradict that requirement; anyone reading it can recompute the public hash-based binding. This hash is a run-binding/check field, not authentication against a party who knows the nonce and can rewrite receipts. **Smallest remediation:** retain raw nonce-bearing receipt only in scratch and publish only separately specified non-secret verification evidence, or explicitly revise the confidentiality contract before filing. No plaintext run_nonce found in frozen committed receipts, nor in the 13 committed round-71 files at observed HEAD `46d9e311563233b27196604e33398123820e821e`; this is a prospective filing risk, not a demonstrated committed leak.

## Notes / negative findings

- **Credentials:** scanned all 45,966 frozen `.ufo/` files plus five frozen tools (672,387,261 bytes), then 3,710 additional non-`.ufo` receipt/evidence/scores-named paths. Pattern families: provider keys, private-key headers, credential assignments, cookies/authorization headers, `op://`, plaintext run_nonce. No new round-71 hits. Historical hits were synthetic scanner fixtures/canaries, vendored HTML token-shaped strings, reference/instruction text, code identifiers, redacted cookie headers, and one binary-patch coincidence. The historical secret-echo finding explicitly labels its key synthetic and says real output was not stored (its lines 9-12). Old raw-cookie-history concerns are already disclosed in `round-52/w1/SentCreds/vendor-and-cookie-details.txt`; this audit does not assert historical Git-object erasure. No live credential validity tested. Match hashes/locations only are retained in `secret-scan.json`, `secret-triage.json`, and `additional-receipt-scan.json`, not possible values. Assignment text embedded in dispatch/spec JSON is not evidence of a leak; reference strings are not resolved secret material.
- **Launcher exclusion:** `packed-elf.py:311` supplies `PYTHONCOERCECLOCALE=0` only to the Python launcher; 295 removes it before recording and exec. The observed object deliberately excludes that marker. The run route's intended four keys are HOME/LANG/PATH/TMPDIR; PATH's value is inherited intentionally (190-203). This is not a general executable sandbox: caller-controlled PATH still controls resolution of node/git/readelf. No shell=True or network primitive/command found in the five frozen instruments. Arguments are argv arrays; the generated impostor shell at `seam-probe.py:205-207` interpolates an unquoted scratch path, an additional reason to keep fixture paths trusted and avoid treating this probe as safe with hostile work-path strings.
- **Network:** no socket/HTTP/download primitive, curl/wget, or git fetch/pull/push/clone in frozen instruments. The provided package path is consumed locally; this seat performed no network action or install.
- **Scope:** current wave spec names 16 seats and reportDir `.ufo/waves/round-71/w1`; observed output directory names match seat names. A directory listing cannot prove every peer's writes. This seat created/wrote only `w1/SentinelScope/` and its designated scratch; no git/jj mutation, state/watchdog/MANIFEST write, host-service restart, PATH-directory write, or fleet-root write. The conflicting flat `w1/SentinelScope.md` trailer was not used because the binding directory-only write rule is narrower; canonical report is this `SentinelScope/scope.md`.
- **Host guard:** reading `/var/log/pacman.log` for `2026-11-04` returned no matching entries. This seat ran no pacman command and installed/updated no tool. The pacman pause and path/write guard stayed binding.
- **Resume rejection contract:** none of the five frozen instruments contains `resume_continuity_v1`; no canonical resume runner is assigned here. No resume-mutation guarantee is asserted from these unrelated instruments.
- **Evidence limits:** code paths audited statically from extracted freeze blobs, all five SHA-256 pins matched claims. No frozen full battery, child runtime probe, or offensive automation executed by this seat. `call-inventory.json`, `audit-inputs.json`, and `nonce-scan.json` retain audit provenance. Scratch extraction is removed before return.

Self-evaluation: accuracy 4 (static behavior grounded in frozen lines, no dynamic exploit claim); completeness 4 (all assigned surfaces covered, concurrent peers' complete write history cannot be proved from a snapshot); clarity 4 (blocking versus prospective risks separated); actionability 4 (minimal fixes named, no unauthorized repair); conciseness 4 (retained historical scan limits rather than a blanket no-secrets assertion). Overall 4.0/5.

VERDICT: not-met — SS-1 receipt-directed out-of-scope write and SS-2 incomplete child observation; SS-3/SS-4 scratch-cleanup defects; no new committed credential or nonce leak observed.
