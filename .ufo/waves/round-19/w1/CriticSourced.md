# CriticSourced — author-side advisory review

Axes: **calibration, freshness, depth**. No admission/judgment or lane implementation changes. No REA/Ghidra analysis or carrier execution. No installs/updates.

## Finding and strongest counterexample

**[OBSERVATION]** The proposal labels C2 sourced by npm version/publish identity and C3 sourced by the Go download archive checksum (`.ufo/waves/round-19/claims.json:17-28`). Those are narrower propositions than either claim's outcome. C2's before/after compares documentation to live configuration; C3's before/after compares frozen emulator predictions to bound Ghidra logs. Neither outcome follows from publication metadata.

**[INFERENCE: counterexample]** Keep the fetched registry/download JSON unchanged, but change a client pin or substitute one local carrier. All source quotes remain true while C2's stated-vs-live equality or C3's “official carrier” identification becomes false. Alternatively, keep both publication records and carriers unchanged but obtain a contrary Ghidra outcome: the metadata cannot determine whether the prediction matches. Thus a newly opened row and a census PASS are not evidence for the whole claim. This is a dependency counterexample, not a mutation I executed.

**[OBSERVATION]** The existing source registry already makes the correct distinction: `corpus/SOURCES.md:49` says replay receipts, not sources, carry observed outcomes. S034 is explicitly not a Go 1.25 map claim (`:40`); S035 supplies the actual 1.25 ABI definitions (`:41`); S023 supplies the installed snapshot (`:29`). Do not replace that mechanism chain with a download checksum.

**[OBSERVATION]** The frozen SOURCES contract scopes authority to a proposition (`../CORPUS.md:93-100`), requires a grounded quote in the round lesson's Gate (`:112-115`), and keeps claim admission elsewhere (`:119-125`). The census implementation checks table structure/enums/dates/duplicate identities, not whether a quote supports a claimed result (`../scripts/sources-census.sh:626-674`). Merely adding two well-shaped rows can therefore leave the dependency counterexample untouched.

## C2: useful release identity, not host or capability authority

**[OBSERVATION, fetched 2026-10-20T18:39:26Z]** npm's full package document reports `dist-tags.latest = 6.7.0`; publish times are `6.5.0 = 2026-10-14T12:56:14.513Z`, `6.7.0 = 2026-10-18T08:12:05.640Z`. Its version map contains no 6.6.0. Endpoint: `https://registry.npmjs.org/rea-agents`; JSON selectors are `.dist-tags.latest`, `.time["6.7.0"]`, `.versions["6.7.0"].dist.integrity`. Response SHA-256 was `bfa6974e131d1bafa18cbfd5d2b590c9ae9ee9965916e0c45014f3e8fce36450`; version-specific response SHA-256 values were `ae3429d52774e39bda4f8c9ba9aa141b26901ec65f82a394e540ed9cc479c236` (6.7.0) and `52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde` (6.5.0). These are access snapshots, not promises that a later whole-document fetch hashes identically.

**[OBSERVATION]** Both client configuration lines now say 6.7.0: `/home/vgpnk/.config/devin/mcp_config.json:7`, `/home/vgpnk/.omp/agent/mcp.json:8`; Kimi also says 6.7.0 at `/home/vgpnk/.kimi-code/config.toml:4126`. In contrast, lane `PROVINCE.md:16-18,44` still says Devin/OMP 6.5.0. These local lines, not npm, establish the actual drift.

**[OBSERVATION]** npm's 6.7.0 integrity string is identical to the cached package lock's entry `/home/vgpnk/.npm/_npx/a1722018f28f9df2/package-lock.json:1607-1610`:

`sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==`

The 6.5.0 lock similarly reports the registry's `sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`. This is an observed **lock-record match**, not verification that every extracted installed file is pristine.

**[INFERENCE: smallest safe correction]** Give the npm row Tier A only for **registry-declared version, publication time and distribution identity**. In C2's lesson, cite it for the explicit sentence “the client pin names a version published by npm, latest at this access time,” and bind that to the client-line receipt and cache-lock identity. Cite separately retained version/catalog/doctor evidence for command counts, tool hashes and alignment; npm metadata does not establish those. `latest` is not a requirement to upgrade an operator-owned pin. The contract intentionally runs CLI 6.5.0 (`contract.md:35-38`) while clients pin 6.7.0; keep those identities separate rather than implying every round-19 run used 6.7.0.

**[OBSERVATION / limit]** The registry advertises provenance attestations. I decoded (did not cryptographically verify) the 6.7.0 SLSA statement: source `https://github.com/morluto/rea`, workflow `.github/workflows/release.yml`, ref `refs/heads/release/6.7.0`, dependency commit `27dc42d10249f0410904a75c0997842eb03b931c`; subject SHA-512 `ca1231da2a096184f50bfb4e35f61e8ad0ba2e19ca98287e6704543a062e85273bdf794686492def7ce1ba0f5698b831a0c74abaa218182a017c3e1f5e43a117`. A repository/homepage URL or `_npmUser = GitHub Actions` alone is not verified publisher/source provenance. Do not label my decoded statement verified provenance.

## C3: carrier provenance becomes load-bearing only with the member binding

**[OBSERVATION]** At the same access time, `https://go.dev/dl/?mode=json` listed only go1.27.3/go1.26.10, not go1.25.0. Use the exact `https://go.dev/dl/?mode=json&include=all` selector. The latter document's SHA-256 was `6b83804b8dd2d6052bb93cc03e4aba2ddee834f82c15f7bf8faacf5f91825950`. The selected object states filename `go1.25.0.linux-amd64.tar.gz`, version `go1.25.0`, OS `linux`, arch `amd64`, kind `archive`, size `59659213`, SHA-256 `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613`. Scope the quote to this object, not merely “Go downloads.”

**[OBSERVATION]** A real connecting artifact exists: `/tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz` hashes to that exact published SHA-256 and has that exact size. Streaming each of the nine tar members and hashing the installed counterpart produced these **9/9 byte-identity matches** (denominator = the nine carriers enumerated in `contract.md:41-42`):

| member below archive `go/` and installed `go-1.25.0/` | SHA-256 of both |
|---|---|
| bin/go | b93cdfdbc72f1afc3f21498c80bf3d155a44a9b95e2d690c940511051574bc25 |
| bin/gofmt | 2aa4122abbd1593ee7c9e184366feef7cb06e52ce790b5ef2119e8aee8640a80 |
| pkg/tool/linux_amd64/asm | a7ed400a04009488ea819eb06aeb912dc3537125cceef036743641060fd797f4 |
| pkg/tool/linux_amd64/cgo | d61f87246456ff1175d057ad663a10dd1ac503c54dc770d14aaa5ffd3309b858 |
| pkg/tool/linux_amd64/compile | 20dbac54f9f897582aedafea7207976f0300cfd4992429814d00bccbea7a4083 |
| pkg/tool/linux_amd64/cover | 64686d22f3b4055386bbcbf0aeac54249cdbff771ffd7b54c8d4abd330df8166 |
| pkg/tool/linux_amd64/link | a4286eaff6094de7f88d55299a61a14d5aae2bfbd19687ba6d5330a730aee983 |
| pkg/tool/linux_amd64/preprofile | eff3b19676f41d95eb598fa7520a9f44c2014db65a5a7470a2ca5c4cfa3f840b |
| pkg/tool/linux_amd64/vet | 9b9d776e7569c910de714790a1b9bab1287b49fdc210973158f3076cee683bf7 |

The vet hash also equals `evidence/prescan/kr19-sm-vet.json:21-24`, whose version fields are at `:47-49`. All prescan paths here are below `.ufo/waves/round-19/`.

**[INFERENCE: smallest safe correction]** Make the new Go row explicitly **distribution identity only**, and retain the above archive→member→installed-file binding in the lane's C3 evidence rather than relying on a temporary tarball or installation-directory name. Bind the same per-carrier hashes to the frozen predictions and retained run logs. Then deleting/changing this source removes support for “official Go distribution carrier,” a real subclaim, while S035/S023/S003 plus the byte replay and logs remain the independent evidence for mechanism and observed outcome. Without that connecting receipt, the new row is decoration attached to a local filename.

**[OBSERVATION]** This distribution fact was already checked in round 18: `../.ufo/reports/round-18/kaidoku.md:90` records the install/JSON checksum check, and `corpus/lessons/round-18-verifier-spotcheck.md:147` independently says the values equal that report. A newly opened SOURCES row is legitimate registry curation, not a newly discovered mechanism, newly covered format, or independent second publisher. Avoid counting the install-record correction, reopened JSON and carrier receipt as three independent authorities.

**[OBSERVATION / calibration warning]** `evidence/prescan/kr19-sm-link.json:2-3` reports the emulator's “no Go build info” error and `unparseable`; a raw magic scan found `b'\xff Go buildinf:'` at file offset 3461224. This does **not** prove a valid decodable build-info record. It does mean source-proven archive membership should not be conflated with successful parser coverage or with a proven absence of all build-info bytes. State “unparseable by this parser,” not an independently established binary-format absence.

## Non-vacuous citation minimum / affected axes

- **Calibration:** one sentence per cited source explaining exactly which proposition it establishes; distinguish registry declarations, local lock/config observations, byte equality, predictions, and observed logs. “Sourced C2/C3” must not imply publication metadata proves the whole result.
- **Freshness:** access time + exact version/object selector + quote in `round-19.md ## Gate`; local config/doctor/catalog receipts for live state. A mutable aggregate response hash records this fetch, not an immutable release identity. Publication time is not installation or process-start time.
- **Depth:** preserve S035→S023→S003 and the per-carrier frozen-prediction/log chain; use the new Go source to bind the carrier population, not to explain Swiss-map failure. A changed checksum must invalidate the “official” subclaim rather than silently leave every evidentiary conclusion unchanged.

These are fixable citation/binding defects, not a reason to reject the intended C2/C3 tasks. Whether narrower metadata-supported subclaims satisfy the canonical sourced-claim requirement is for the canonical Rust judge; this advisory review neither admits nor judges them. Rows must be cited by the actual lesson/knowledge path in `used-by` (`../CORPUS.md:103-108`), not only by `claims.json` or the registry itself.

## Executed evidentiary commands and exits

Commands below are pasted as executed; shell invocation exits were 0 unless stated. Discovery reads are path:line citations above. Pipelines did not enable `pipefail`; where I printed only a pipeline/loop status, individual subprocess exits were not separately captured. No claim of cryptographic attestation verification or REA runtime testing is made.

### Fetch/read publication metadata (both invocations exit 0; each curl explicitly printed exit 0)

```sh
mkdir -p /tmp/kr19-CriticSourced && cd /tmp/kr19-CriticSourced && date -u +%FT%TZ && curl -sS -o godl-all.json 'https://go.dev/dl/?mode=json&include=all'; echo "curl-all exit=$?"; curl -sS -o godl-default.json 'https://go.dev/dl/?mode=json'; echo "curl-default exit=$?"; sha256sum godl-all.json godl-default.json; python3 -I -B -c "
import json
a=json.load(open('godl-all.json')); d=json.load(open('godl-default.json'))
print('all releases',len(a),'default releases',len(d),'default versions',[r['version'] for r in d])
print('go1.25.0 in default:', any(r['version']=='go1.25.0' for r in d))
for r in a:
  if r['version'] in ('go1.25.0','go1.24.6'):
    for f in r['files']:
      if f['os']=='linux' and f['arch']=='amd64' and f['kind']=='archive': print(json.dumps(f,sort_keys=True))
    print(r['version'],'stable',r['stable'])
print('first entry', a[0]['version'])
"
```

```sh
mkdir -p /tmp/kr19-CriticSourced && cd /tmp/kr19-CriticSourced && date -u +%FT%TZ && curl -sS -o npm-pkg.json https://registry.npmjs.org/rea-agents; echo "curl-pkg exit=$?"; curl -sS -o npm-670.json https://registry.npmjs.org/rea-agents/6.7.0; echo "curl-670 exit=$?"; curl -sS -o npm-650.json https://registry.npmjs.org/rea-agents/6.5.0; echo "curl-650 exit=$?"; sha256sum npm-*.json; python3 -I -B -c "
import json
p=json.load(open('npm-pkg.json'))
print('dist-tags',p.get('dist-tags'))
t=p.get('time',{})
vs=sorted(p.get('versions',{}))
print('nversions',len(vs),'last5',vs[-5:])
for v in ['6.4.0','6.5.0','6.6.0','6.7.0']: print(v,t.get(v))
print('modified',t.get('modified'))
print('repository',p.get('repository'),'homepage',p.get('homepage'))
for f in ['npm-650.json','npm-670.json']:
  x=json.load(open(f)); dd=x.get('dist',{})
  print(f, x.get('version'), 'integrity',dd.get('integrity'),'shasum',dd.get('shasum'),'tarball',dd.get('tarball'))
  print('  attestations',json.dumps(dd.get('attestations')) [:300], 'signatures', [s.get('keyid') for s in dd.get('signatures',[])])
  print('  gitHead',x.get('gitHead'),'_npmUser',x.get('_npmUser',{}).get('name'),'bin',x.get('bin'),'deps',len(x.get('dependencies',{})))
"
```

### Bind official Go archive members (invocation exit 0; sha exit 0; nine MATCH lines)

```sh
cd /tmp/kr19-CriticSourced && T=/tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz; stat -c '%n %s %y' $T; sha256sum $T; echo "sha exit=$?"; for m in bin/go bin/gofmt pkg/tool/linux_amd64/asm pkg/tool/linux_amd64/cgo pkg/tool/linux_amd64/compile pkg/tool/linux_amd64/cover pkg/tool/linux_amd64/link pkg/tool/linux_amd64/preprofile pkg/tool/linux_amd64/vet; do a=$(tar -xzOf $T go/$m | sha256sum | cut -c1-64); b=$(sha256sum /home/vgpnk/.local/opt/go-1.25.0/$m | cut -c1-64); [ "$a" = "$b" ] && r=MATCH || r=DIFF; echo "$m tar=$a inst=$b $r"; done
```

### Bind cache lock and configuration observations (invocation exit 0; loop/grep/grep2 printed 0)

```sh
for d in /home/vgpnk/.npm/_npx/*/; do v=$(python3 -I -B -c "import json,sys;print(json.load(open(sys.argv[1]))['version'])" $d/node_modules/rea-agents/package.json 2>/dev/null); [ -n "$v" ] && echo "$d rea-agents=$v lock-integrity=$(python3 -I -B -c "import json,sys;l=json.load(open(sys.argv[1]));p=l.get('packages',{}).get('node_modules/rea-agents',{});print(p.get('integrity'),p.get('resolved'))" $d/package-lock.json 2>/dev/null)"; done; echo "loop exit=$?"; grep -n 'rea-agents@' /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json; echo "grep exit=$?"; grep -n 'rea-agents@' /home/vgpnk/.kimi-code/config.toml | head -3; echo "grep2 exit=$?"
```

### Decode advertised attestation and scan raw magic (invocation exit 0; curl printed 0)

```sh
cd /tmp/kr19-CriticSourced && curl -sS -o att-670.json https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.7.0; echo "curl exit=$?"; python3 -I -B -c "
import json,base64
a=json.load(open('att-670.json'))
for at in a.get('attestations',[]):
  pt=at.get('predicateType'); env=at['bundle'].get('dsseEnvelope',{})
  st=json.loads(base64.b64decode(env['payload']))
  print(pt, 'subject', st['subject'])
  if 'slsa' in pt:
    p=st['predicate']; bd=p['buildDefinition']
    print(' workflow', json.dumps(bd.get('externalParameters',{}).get('workflow')))
    print(' resolvedDeps', json.dumps(bd.get('resolvedDependencies'))[:400])
"; for f in link vet go; do python3 -I -B -c "
import sys;b=open(sys.argv[1],'rb').read();i=b.find(b'\xff Go buildinf:');print(sys.argv[1].rsplit('/',1)[1],'buildinf magic offset',i)" /home/vgpnk/.local/opt/go-1.25.0/$( [ $f = go ] && echo bin || echo pkg/tool/linux_amd64)/$f; done; ls /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/evidence/prescan/
```

**Scope note:** these commands created only scratch fetched JSON under `/tmp/kr19-CriticSourced`; the only lane file written is this report. Publication metadata is untrusted data. Read-only repository discovery commands supplied the cited source anchors; no main-agent verification was rerun.
