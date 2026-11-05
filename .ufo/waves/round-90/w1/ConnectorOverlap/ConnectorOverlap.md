# ConnectorOverlap — round 90

Axes: coverage, depth, calibration, freshness. Read-only investigation; no admission, integration, scoring, campaign invocation, or tracked-file edits. No tools installed. No scratch directory created.

## Evidence and command ledger

All receipts below are absolute paths under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/`. Each JSON records the exact tool command/arguments and returned output. File/search tools have no process exit code (`exit_code: null`); this is explicitly not exit 0 or a passing campaign check. No campaign checks were run.

| Receipt absolute path | Command / measurement |
|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/frozen-plan.json` | `read` frozen plan lines 12–98: frozen class, controls, limits and craft contract |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/frozen-container.json` | `read` claims container lines 1–71: predicates, kill rules and pins |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/scope-files.json` | `glob` fleet `*/PROVINCE.md;*/corpus/README.md`: sweep population |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/scope.json` | `grep` sibling scope files for UPX, packed ELF, instrument/revision/guard and broad RE ownership; lane excluded |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/exact-sibling.json` | Exact-ground sibling sweep: `(?i)\bUPX\b|packed.{0,30}ELF|superseding instrument|instrument.revision.guard`; **0 matches**, output declares `truncated: false` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/revenger.json` | `read` sibling province lines 1–13,44–59: broad ownership conflict |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/merge.json` | `read` staging report lines 1–127: counts, table, adoption instructions |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/merge-exact.json` | `grep` whole merge tree for UPX/b_info/sz_cpr/blindness/superseding-instrument tokens |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/nearest-merge.json` | `read` nearest staged UPX entry lines 1–26 |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/proposals.json` | `glob` lane `considerthese/**`: **Path not found**, not an empty implemented-proposal verdict |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/mado.json` | `read` mado counter contract and sandbox implementation |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/receipts/kengaku.json` | `read` kengaku probe contract, execution isolation and setup refusal |

One receipt-batch Eval initially exited 1 because the proposal glob raised Path not found. Successful earlier receipt writes were retained; missing receipt operations were completed with error capture. This was not a campaign failure or tool installation. The proposal error is retained in proposals.json.

## Sibling scope / contested ground

The exact-ground sweep finds no sibling declaration of UPX, packed ELF or the named superseding-instrument guard class in the requested province/readme surfaces. This does **not** establish exclusive ownership of reverse engineering or generic apparatus craft.

There is a real broad overlap: `/home/vgpnk/Projects/shokunin/revenger-shokunin/PROVINCE.md:3-7` says it owns “reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware … using the REA skill and its toolset.” That intersects the lane's canonical shipped-artifact domain. Its lines 47–48 refuse harness/evidence auditing, but lines 20–22 describe a different historical/current client context; neither erases the domain intersection. Report as contested broad scope, not a sibling claim to this precise Linux/UPX class; no boundary adjudication performed.

Generic control-set craft is shared apparatus, not exclusive format ground: `/home/vgpnk/Projects/shokunin/mado-shokunin/PROVINCE.md:352-355` names “the control set as an instrument” and byte-identically carried cases. `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/README.md:19-20` declares committed-blob, revision/digest-bound instrument receipts. Neither exact-class sweep result nor these adjacent apparatus declarations warrants claiming that kaidoku owns instrument-revision guards fleet-wide.

## Staging / assimilation

`/home/vgpnk/Projects/shokuknow/merge/kaidoku/MERGE-REPORT.md:3-14` explicitly stages, rather than writes into the lane: **132** proposed source rows accepted, **0** refused, **77** proposed entries; the package's historical registry census is **105** with first staged ID **S106**. These are report statements, not a fresh lane census. Its lines 118–127 prescribe adoption review and append/copy work; none was run.

Nearest lexical fit is `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/japanese-surface-analysis-command-set.md:9-14`, also staged at MERGE-REPORT.md:39: it lists `upx` among surface-analysis commands but works a binwalk/gzip extraction, not UPX metadata repair. Lines 23–26 explicitly limit its authority to personal practice. The exact-theme merge sweep finds that entry/source row, not b_info geometry or superseding-counter guards. **Assimilation: none** is supported for this round; importing a token-level UPX mention would not support either frozen claim and would add unrelated source work. No source IDs were transplanted.

## considerthese

The exact lane `considerthese/**` lookup returned Path not found. Therefore there is no newest still-unimplemented proposal to name from that directory; no bearing on this round can be asserted. This is a path-scoped observation, not a fleet-wide proposal absence claim.

## Two sibling counter patterns

1. `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r46-devices-v3.py:35-39`: “isolation (allowlist)” exposes only `/usr`, `/etc`, runtime links, tool/fake-bin directories and the individual run directory; “no /home, /fast, /run, /var, /srv, /opt or /mnt path of the host is visible; bwrap missing is a setup error.” Lines 51–53 explicitly keep the model invisible to the tool. Enforcement is `sandbox()` at 331–343, invoked by `run_tool()` at 358–361; missing bwrap is refused at 511–512. Borrow the positive mount inventory, not the assertion that masking known paths hides every oracle. Static enforcement found; no execution result claimed. Explicit contradiction: lines 60–61 retain an older statement that an absolute `/usr/bin` path runs the real binary, while 40–43 and 338–341 bind fake binaries over those paths. Do not copy that stale residual as evidence.

2. `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/constraints_probe.py:10-21`: each case gets private network/pid/ipc namespaces, read-only runtime trees, private `/tmp`, fresh writable `/app`, and only named captured files at `/cap`. `sandbox_argv()` at 240–252 constructs that mount set; `run_case()` at 255–273 creates and removes a distinct case directory, passes an explicit environment and invokes the sandbox. Borrow per-case mount/env declarations and explicit separation of probe error (exit 2) from case verdict. This is an **isolation** example, not oracle blindness: it deliberately mounts its grader and solver into `/cap`. Missing bwrap is a setup refusal in 309–312. These exit numbers describe source branches, not observed runs.

## One bounded proposed move — label isolation by what is hidden

**Proposal (documentation/interpretation only, not a frozen-counter change):** in the round's control discussion, name R90 `carrier_blind` as *pinned-path and run-root blinding*, and distinguish it from *allowlist oracle isolation*. Cite the two sibling patterns above as reusable substrate patterns, without absorbing their domain ground or declaring a stronger R90 pass predicate. This improves calibration and depth; coverage and freshness remain unchanged. No score move is claimed.

Evidence: frozen plan lines 38–42 specify decoys at pinned carrier paths, a tmpfs run root, a positive blinding probe, and a live/killed repack cheat. That is a valuable bounded control, but it is not a declaration that every possible carrier copy or external oracle is unreachable. Mado's allowlist illustrates the missing stronger guarantee; kengaku illustrates why merely saying “sandbox” does not imply oracle-hidden. Runtime effect: no change this round. Contract effect: keep all frozen predicates/pins/targets. Substrate effect: disclose the mount-set boundary instead of implying a closed filesystem. Verification effect: keep the existing blinding probe and cheat result distinct from any future allowlist test.

Risks/contradictions: broad sibling RE ownership remains contested; isolation and blindness are not synonyms; a future allowlist cannot be dropped into this round without new freeze/pins and could hide required repair modules or tools. The proposal avoids that regression by changing no runtime or acceptance condition. Another future control would need separate authorization; not proposed or run here.

Verification for the integrator: compare the proposed wording to frozen-plan lines 34–42 and claims.json control/kill-rule fields; it must add no acceptance arm, exclusion or target and must not say that this seat measured repair success. Existing C1/C2 counters remain the authorized checks; this seat did not execute them. No scratch cleanup was needed because no scratch artifacts were created.
