#!/usr/bin/env bash
# RV-9 re-audit battery — run against whatever revision is live at invocation.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=/var/tmp/rv9-round2
cd "$REPO" || exit 9
sha0=$(sha256sum .ufo/gates/c1-census-v10.py | cut -d' ' -f1)
python3 .ufo/gates/c1-census-v10.py > "$R/post-edit.out" 2>"$R/post-edit.err"
rc=$?
sha1=$(sha256sum .ufo/gates/c1-census-v10.py | cut -d' ' -f1)
echo "$(date -u +%FT%TZ) sha=${sha0:0:12} lines=$(wc -l < .ufo/gates/c1-census-v10.py) size=$(stat -c %s .ufo/gates/c1-census-v10.py) exit=$rc race=$([ "$sha0" = "$sha1" ] && echo no || echo YES)" >> "$R/verdict-timeline.txt"
cp .ufo/gates/c1-census-v10.py "$R/c1-census-post.py"
echo "=== pinned run: exit=$rc sha=${sha0:0:12} (race: $([ "$sha0" = "$sha1" ] && echo no || echo YES)) ==="
sha256sum "$R/post-edit.out"
echo "=== byte-identity audit (pre vs post) ==="
python3 "$R/verdict-identity.py" "$R/pre-edit.out" "$R/post-edit.out"; echo "audit-exit=$?"
echo "=== creep audit (round-1 scope-diff, pre vs post) ==="
python3 .ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/scope-diff.py "$R/c1-census-pre-edit.py" "$R/c1-census-post.py"; echo "creep-exit=$?"
echo "=== JSON key delta ==="
python3 .ufo/gates/c1-census-v10.py --json > "$R/post-edit.json" 2>&1
python3 - <<'EOF'
import json
pre=json.load(open('/var/tmp/rv9-round2/pre-edit.json'))
post=json.load(open('/var/tmp/rv9-round2/post-edit.json'))
print("keys added:", sorted(set(post)-set(pre)), "| keys removed:", sorted(set(pre)-set(post)))
for k in sorted(set(pre)&set(post)):
    if pre[k]!=post[k]: print("changed key:", k, "->", json.dumps(post[k])[:160])
EOF
echo "=== fixture battery ==="
python3 "$R/fixtures.py"
