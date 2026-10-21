HOLDS — the measured-source census expectation (47 rows, validator exit 0, W04 only for S033/S047) holds.

Axes: calibration (attacked); coverage and depth are not tested by this census.

**Observations**

- Exact requested live command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` — exit 0. Output: `kaidoku W04 S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes`; `kaidoku W04 S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes`; `kaidoku ok /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`. The W04s match the expected rows at `corpus/SOURCES.md:39,53`; the lesson records W04 for S047 and carried S033 at `corpus/lessons/round-20.md:57-60`.
- For revision scope, materialized commit `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` into `/tmp/r20-sources-census-eanfeqq9` via `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin archive --format=tar 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 | tar -xf - -C /tmp/r20-sources-census-eanfeqq9` (exit 0), then used `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:corpus/SOURCES.md > /tmp/r20-sources-census-eanfeqq9/corpus/SOURCES.md` (exit 0). Git-object and extracted file SHA-256 both `620543aa515087024d1150acd3315f8e59cfe6f95348e4dc29905dcc75b6488b` (comparison command exit 0); working-tree `corpus/SOURCES.md` has the same SHA-256 and bytes. Scratch was created by `tempfile.mkdtemp` outside the lane.
- Ran each exact manual census command from `/home/vgpnk/Projects/shokunin/CORPUS.md:133-148` in that revision snapshot; all exited 0:

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
# output 47; exit 0
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
# output 0; exit 0
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
# output A=41 B=5 C=1; exit 0
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
# output mined=45 rejected=2; exit 0
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
# no output; exit 0
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
# no output; exit 0
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
# no output; exit 0
```

**Inference:** The requested result holds at measured source S: 47 syntactically valid rows, no manual-census duplicate/enum/tier-inflation/missing-path findings, and only the two expected duplicate-URL W04 warnings. The validator documents warnings as non-failing (`scripts/sources-census.sh:16-18,31-33`); measured-source claim context is `claims.json:15-18`.