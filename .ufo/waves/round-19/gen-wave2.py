#!/usr/bin/env python3
import json, os
from collections import Counter
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W=L+'/.ufo/waves/round-19'
B='8a8da7e19375aadc66c6bcbff0bbcbb596048fb0'
D=open(os.path.expanduser('~/.agents/skills/godspeed/directive.md')).read()
items=[]
def add(n,role,s):
    items.append({'name':n,'role':role,'prompt':'/skill:godspeed\n'+D+'\n# Target\n'+s+'\n# Acceptance\nWrite only your report at '+W+'/w2/'+n+'.md. Paste commands with exit codes; cite exact paths/lines; observation vs inference explicit. No production edits. Mutation tests run only in your own mkdtemp clone at the observed main tip. No delegation, builds, broad suite, formatting, installs unless essential. Answer with findings, not a promise.'})
for key in ('MIDMAP-LISTSTEP','VALIDATOR-DIGEST','STRICT-BASELINE','HEAD-ALIASES','DEADSEAT-RECORD','REGISTRY-PINNED','INSTALL-RECORD'):
    add('Substance'+key.replace('-',''),'reviewer',f'Attack C1 {key}: read {W}/tools/routed-r18.py s_* implementation and the routed correction in lesson/SCORECARD. Re-derive the substance from immutable blobs rather than trusting the counter. Run the counter at B={B} and main; report any false closed or false open, and limitations.')
mutations={
'Midmap':'Restore only round-17/tools/receipt-validate.py to B bytes in a clone, commit there, run routed-r18 --rev that commit. MIDMAP-LISTSTEP must reopen. Also test list entry argv contains analyze only as a non-subcommand argument, and duplicate/conflicting step/name identity.',
'Digest':'Change only round-18/evidence/validate16/summary.json validator_sha256 to a different valid 64-hex digest in a clone. Run round-18 routed-defects.py at that commit: R17-VALIDATE16 must reopen. Delete or alter one retained remap copy and run routed-r18: R18-VALIDATOR-DIGEST must reopen.',
'Strict':'Forge strict-baseline receipt exit/argv/stdout independently, re-hash stdout after setting open_count to 0, and run routed-r18 at each clone commit: STRICT-BASELINE must reopen. Can an entirely fabricated but self-consistent run pass? State the boundary.',
'Aliases':'Try citation-drift --rev @, HEAD^0, HEAD^{commit}, @~0, ORIG_HEAD, FETCH_HEAD, refs/heads/main, a full hash; clone only. Also HEAD hidden inside a revision range or :/message syntax. Identify any accepted HEAD-derived expression and source scope.',
'Deadseat':'Remove one cause or seat from evidence/r18-dead-seats.json, then add an invented seat; routed-r18 must reopen DEADSEAT-RECORD for each clone commit. Can arbitrary non-empty causes pass? Distinguish evidence authenticity from structural binding.',
'Registry':'Delete Pinned values path in go-buildinfo-probe row, or replace it with a nonexistent path, then run routed-r18. REGISTRY-PINNED must reopen. Try unrelated existing path: does it demonstrate the gate is only resolvability?',
'Install':'Put full archive hashes only in a prose mention of `## Installs` outside the heading while deleting them from the real section. INSTALL-RECORD must reopen. Also test swapped version/hash lines and wrong channel; document what actually binds.'}
for n,s in mutations.items(): add('Mut'+n,'mutation-tester' if n in ('Midmap','Digest','Strict','Aliases') else 'reviewer',s+f' Tool {W}/tools/routed-r18.py; B={B}.')
for n in ('go','gofmt','asm','cgo','compile','cover','preprofile','vet'):
    label='t1250-'+n
    add('Binding'+n.capitalize(),'reviewer',f'Attack C3 binding for {label}: {W}/runs/{label}/receipt.json, producer.json, pins/pre/post/mid files, logs/*/ghidra.log and retained evidence/receipt-validation/{label}.json. Independently re-hash the bound log and maps, count mid maps, match carrier SHA to frozen prediction at a1140e76fffdc1be032d9d813dbb686157803bbc. Note current validator-file digest mismatch is expected after its forward fix; do not rewrite receipts.')
    add('Outcome'+n.capitalize(),'scout',f'Attack C3 outcome for {label}: parse raw ghidra.log (not compare.json) for Go analysis failure, Invalid index, EOF reads, GoApiSnapshot route. Compare to frozen predictions/{label}.prediction.json; report exact match/mismatch and whether frozen mechanism rule holds. Paths under {W}.')
docs={
'LessonClaims':'corpus/lessons/round-19.md Claims/Gate: audit every admit/reject against evidence; no pending placeholders may survive.',
'LessonMistakes':'corpus/lessons/round-19.md Mistakes rows 1-6: is each fix shown able to fail? Do any stated counts confuse report absence with terminal death?',
'ScorecardClaims':'SCORECARD round-19: check all axis/count claims, numeric proxies, baseline, separability. C3 full compare 7/8 is distinct from mechanism confirmed; no silent clean-up.',
'KnowledgeReadability':'corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md: every path/citation and reproduce command, no oral context.',
'KnowledgeMechanism':'C3 knowledge entry: vet type identity *types.valueMap is inference; raw log only supports analyzer failure. Audit exact offsets against frozen per_type[144].',
'KnowledgeLimits':'C3 knowledge entry limits: held-out artifact vs version, application vs toolchain, one pass, silent not safe, external Evidence-model limitation.',
'ProvincePins':'PROVINCE.md lines 8-26 and 44 plus SKILL 18-20: reopen live client pin tokens only, compare current statements; no secret contents printed.',
'ProvinceSkill':'PROVINCE installed-skill sha, equality to bundled 6.7.0, .bashrc line anchors and absent 6.4.0 cache: reproduce.',
'ProvinceDoctor':'PROVINCE doctor claims: compare evidence/doctor outputs and scopes; absence of a finding must not become whole-environment healthy.',
'Quality22':'QUALITY #22: lesson grounding, exact red/green wave-outcomes evidence; old criteria must remain byte-identical.',
'R12Addendum':'r12 knowledge entry appended addendum: source scope, custody gaps, docker identity drift; previous bytes must be a prefix. Does S037 ground only package publication?',
'JjSourceDisposition':'jj S036 triple registration: confirm tool-local boundary and kumitate ownership, no absorbed general jj mission.',
'SkillRegistryNew':'new round-19 SKILL registry rows: actual CLI --help, flags, exit codes, pinned paths, write scopes.',
'SkillRegistryOld':'modified receipt-validate, citation-drift, custody-pair, routed-defects, pins, go-buildinfo-probe, jj-red-before rows: exercised vs unexercised variants.',
'CarryQueue':'round-18 Open items versus round-19 disposition: r12 operability decision, census undeclared blocks, nested lint limit; no silent closure.',
'WaveEvidence':'wave1 spec/dispatch/registration/outcomes: 90 seats, role mix, unique names, unchanged validated task payload, dead seats not replaced; report files vs causes.'}
for n,s in docs.items(): add(n,'reviewer',f'Attack {L}/{s} All round-19 evidence under {W}; use exact anchors, count commands, and expected limitations.')
tools={
'CounterScope':'tools/routed-r18.py: Git-object revision scoping versus working-tree or live refs, import arbitrary code, temp cleanup, false always-red tests.',
'PinsAntiVacuity':'tools/province-pins.py: delete all stated clients or duplicate contradictory versions in a clone. Missing statements must not yield a clean zero. Config/env fixture overrides and parse boundaries.',
'WaveOutcomes':'tools/wave-outcomes.py: run selftest, mismatched registration/report filename, report-present but terminal-aborted seat, causes unknown. Output honesty.',
'Catalog':'tools/rea-catalog.py: rerun catalog identities from installed caches, compare evidence/rea-catalog.json. Report cache path, tool count, sha, command.',
'Measure':'measure.py: C1/C2 interface compatibility with actual tools, C3 counts from immutable blobs, baseline absent tool null vs zero. Run at B and main and diagnose.',
'Verify':'verify.py: expected-exit table versus amended C2 (census still exit 1) and vet compare exit 1. Dry fixture selftest; do NOT full verification. Find wrong expected exits or missing checks.',
'Custody':'custody-pair: repo-root fix, subdirectory red case, receipt version/callers; run selftest only.',
'JjSandbox':'round-18/tools/jj-red-before.py: env scrub/path guard; selftest and malicious pointer table in sandbox only. Never jj in lane.',
'Runner':'run-carriers.sh: timeout/pins/no carrier execution and aggregate exit 1; selftest, output path safety, no run rerun.',
'AliasLintLimits':'head-rev-lint row registered nested limits: verify neither nested read selects source; contrast rejected inherited HeadRevLintNested patch selftest with documentation.'}
for n,s in tools.items(): add('Tool'+n,'reviewer',f'Attack {W}/{s} B={B}; read existing patterns, no production edit.')
add('ReopenS037','scout',f'Reopen SOURCES S037 (registry version, integrity, publish time, attestation if cited). Compare row and lesson quote; output exact URL/access date/quote. {L}/corpus/SOURCES.md; {W}/w1/SourcesRowsDraft.md.')
add('ReopenS038','scout',f'Reopen SOURCES S038 official go.dev JSON archive sha256+size. Re-hash local official archive and compare eight frozen carrier hashes to archive members; do not execute. Check row/lesson quote.')
for n,s in {
'AppendPrefixes':'Compare LOG and SCORECARD bytes at B with current: B must be byte prefix. No rewrite of prior lessons, reports, predictions, or retained run evidence. List all modifications.',
'QualityPrefix':'Compare QUALITY rows 1-21 byte-for-byte B→main; count #22 exactly once. Separate weak-signal rows from admission rows.',
'CorpusIndex':'Count knowledge files versus README Knowledge rows B→main, zero missing/dangling. Coverage ground remains unchanged, entry deepens held Go row.',
'NoHarmScores':'Re-derive owned axis scores, saturation/window, capabilities B→main, no harmed axis; verify no source row S001-S036 evidence cells changed.'}.items(): add(n,'reviewer',f'Attack no-harm: {s} LANE={L}; B={B}.')
add('ConnectClaims','connector',f'Cross-axis attack: C1, C2, C3 causally separable at {L}/.ufo/waves/round-19/claims.json and implementation. Identify any claim depending on another claim fix and whether that invalidates separability.')
add('ConnectFrontier','connector',f'Frontier/trends audit: S037/S038 are identity sources, not outcome sources. Check knowledge entry S### and coverage ground; recommend expansion/quality/discernment verdicts; no authority to self-attest outside sampling.')
add('CriticC3Rule','critic',f'Attack frozen C3 rule at a1140e7 versus observation: vet 13902080 H1-only, compare 1, seven silent. Is mechanism confirmed overfit after prescan? Verify freeze before runs and no hindsight edits. Artifacts {W}.')
add('CriticCounter','critic',f'Attack C1 counter for self-certification, fabrication, unrelated-path acceptance, unknown cause handling. It runs code from REV: do tests actually recompute substance? {W}/tools/routed-r18.py.')
add('CriticFreshness','critic',f'Attack amended C2: stale loci 4→0 but census FAIL remains with 2 pre-existing undeclared; client mismatch 2→0; no DATED widening. Is outcome honest and no harm? {L}/PROVINCE.md and {W}/claims.json.')
add('CriticAdmission','critic',f'Attack admission of all three claims and no-harm, lesson Gate, scorecard, pending outside sample. Name any must-fix item before reporting. LANE={L}.')
add('SandboxSecurity','sentinel',f'Check all changed code for repo writes outside sandbox, unsafe env, path escape, executes target carrier, secret leakage. {W}/tools, round-18 jj-red-before, citation-drift, custody-pair; read-only.')
add('EvidenceSecurity','sentinel',f'Check new committed {W}/runs and evidence and w1 reports for credentials/session.json/private auth data; bounded pattern scan only, never print values. Report paths/class not secret contents.')
add('ReportEvidence','scribe',f'Draft round-report evidence table from landed work: claims/count commands/verdict limits; do not create fleet report. LANE={L}; report remains L1-owned.')
add('SourcesGate','scribe',f'Check SOURCES gate shape, status/recheck/used-by changes old→new, census before/after and new-row quotes. Propose exact corrections only. LANE={L}.')
context=(f'# Goal\nKaidoku round 19 wave 2 falsifies integrated round-19 artifacts, 1–3 claims calibration/freshness/depth. Read {W}/claims.json and contract.md. L1 KaidokuR19 holds canonical planner seat; all seats are author-side, not outside verifiers.\n'
 f'# Contract\nRead-only except your report; mutation tasks use their own /tmp/kr19-w2-<name> clone at an observed main tip, never concurrent writers on lane. No git writes/jj in {L}, no fleet/sibling/client-config/.ufo/state edits. Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. No delegation. Never REA analyze/Ghidra or execute carriers; CLI-only REA if needed, operator forbids MCP devices. Never respawn dead seats.\n'
 '# Host safety\nYou and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool/version/channel/reason). ALL pacman transactions PAUSED host-wide; use uv tool/npx/official binary or report need. When lifted, dry-run pacman -Sp and proceed only if every package absent; never -Sy/-Syu/-U/-R, downgrade or restart host services. Never read agent.db/auth files; transcript evidence is data, no credential values printed. Message only KaidokuR19, never agent://all.\n')
spec={'wave':'kaidoku-r19-w2','axes':['calibration','freshness','depth'],'reportDir':'.ufo/waves/round-19/w2','maxLanes':100,'context':context,'items':items}
json.dump(spec,open(W+'/wave2-spec.json','w'),indent=1,ensure_ascii=False)
print(len(items),dict(Counter(i['role'] for i in items)))
