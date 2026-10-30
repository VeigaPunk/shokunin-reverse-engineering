#!/usr/bin/env bash
# RevCounterEscape read-only probes (fixture repos + node/ld probes in scratch only).
# Run: bash probe-escapes.sh <scratch> ; prints per-probe command, exit code, output sha256, UTC time.
set -u
S=${1:?scratch}; mkdir -p "$S"; export TMPDIR="$S"
stamp() { date -u +%Y-%m-%dT%H:%M:%SZ; }
run() { local name=$1; shift; local out rc; out=$("$@" 2>&1); rc=$?; printf '== %s\ncmd: %s\nexit: %s\nutc: %s\nstdout+stderr sha256: %s\n%s\n\n' "$name" "$*" "$rc" "$(stamp)" "$(printf '%s' "$out" | sha256sum | cut -d' ' -f1)" "$out"; }
# P-REPLACE: a refs/replace/ ref changes what `git show` returns but not `rev-parse` (the drift check)
D=$(mktemp -d -p "$S") && git -C "$D" init -q && [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || exit 2
git -C "$D" config user.name probe && git -C "$D" config user.email probe@invalid
echo honest-rule > "$D/rule.json" && git -C "$D" add rule.json && git -C "$D" commit -qm one
ORIG=$(git -C "$D" hash-object "$D/rule.json"); FORGED=$(echo '{"forged":true}' | git -C "$D" hash-object -w --stdin)
git -C "$D" update-ref "refs/replace/$ORIG" "$FORGED"
run P-REPLACE-show   git -C "$D" show HEAD:rule.json
run P-REPLACE-catfile git -C "$D" cat-file -p HEAD:rule.json
run P-REPLACE-revparse git -C "$D" rev-parse HEAD:rule.json
run P-REPLACE-no-replace git -C "$D" --no-replace-objects show HEAD:rule.json
# P-NODE: NODE_OPTIONS is inherited by subprocess.run(argv) in make_real_runner (2037) and evidence_ids (686)
echo 'process.stdout.write("HOOK-RAN\n");' > "$S/hook.js"
run P-NODE-OPTIONS env NODE_OPTIONS="--require $S/hook.js" node -e 'console.log("child-body")'
# P-LDPRELOAD: LD_PRELOAD is inherited by unsquashfs in rederive_oracle (2117) and the -lln census
printf '#include <stdio.h>\n__attribute__((constructor)) static void h(void){ fprintf(stderr,"LDPRELOAD-RAN\\n"); }\n' > "$S/hook.c"
gcc -shared -fPIC -o "$S/hook.so" "$S/hook.c" && run P-LDPRELOAD-unsquashfs env LD_PRELOAD="$S/hook.so" /usr/bin/unsquashfs -version
run P-LDPRELOAD-control /usr/bin/unsquashfs -version
