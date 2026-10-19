#!/usr/bin/env bash
# VZ-4 independent attacks on the C3 custody-pair instrument (EX-31's real target).
# All fixtures are scratch copies under /var/tmp/vz4/c3 — no custody path is
# written, renamed, or mtime-touched. Read-only capture of the live paths only.
set -u
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
TOOL="$R/.ufo/gates/custody-pair/custody-pair.py"
W=/var/tmp/vz4/c3/vz4atk
rm -rf "$W"; mkdir -p "$W"
echo "tool_sha256=$(sha256sum "$TOOL" | cut -d' ' -f1)"
echo "utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

echo "=== A. same-content rewrite (in-place) on a scratch copy ==="
cp "$HOME/.bashrc" "$W/target.conf"
python3 "$TOOL" capture --out "$W/a.txt" --paths "$W/target.conf" --label A >/dev/null 2>&1
echo "capture-A exit=$?"
sha_a=$(sha256sum "$W/target.conf" | cut -d' ' -f1)
sleep 1.1
cp "$HOME/.bashrc" "$W/target.conf"            # same bytes, new write
sha_b=$(sha256sum "$W/target.conf" | cut -d' ' -f1)
python3 "$TOOL" capture --out "$W/b.txt" --paths "$W/target.conf" --label B >/dev/null 2>&1
echo "capture-B exit=$?"
echo "sha_content_before=$sha_a"
echo "sha_content_after =$sha_b"
echo "sha_only_would_say: $( [ "$sha_a" = "$sha_b" ] && echo 'IDENTICAL (blind)' || echo DIFFERENT )"
python3 "$TOOL" verify "$W/a.txt" "$W/b.txt" 2>&1 | tail -6

echo
echo "=== B. rename-swap (new inode, same content + restored mtime) ==="
sleep 1.1
cp "$W/target.conf" "$W/target.new"
touch -r "$W/b.txt" "$W/target.new" 2>/dev/null || true
mv "$W/target.new" "$W/target.conf"
python3 "$TOOL" capture --out "$W/c.txt" --paths "$W/target.conf" --label C >/dev/null 2>&1
sha_c=$(sha256sum "$W/target.conf" | cut -d' ' -f1)
echo "sha_content_after_rename=$sha_c (same as before: $( [ "$sha_a" = "$sha_c" ] && echo yes || echo no ))"
python3 "$TOOL" verify "$W/b.txt" "$W/c.txt" 2>&1 | tail -4

echo
echo "=== C. round-1 v1 canonical receipt vs live (v1 compat) ==="
V1="$R/.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt"
ls -la "$V1" 2>&1 | tail -1
python3 "$TOOL" verify "$V1" --live 2>&1 | tail -12

echo
echo "=== D. independent label re-derivation (gmtime vs receipt renders) ==="
python3 - "$TOOL" <<'PY'
import re, subprocess, sys, time, datetime
out = subprocess.check_output([sys.executable, sys.argv[1], "capture", "--out", "-",
                               "--label", "vz4-label-check"], text=True)
stanzas, cur = [], None
for line in out.splitlines():
    m = re.match(r"^PATH:\s*(.+)$", line)
    if m:
        cur = {"PATH": m.group(1).strip()}; stanzas.append(cur); continue
    m = re.match(r"^([A-Z_]+):\s*(.*)$", line)
    if m and cur is not None:
        cur[m.group(1)] = m.group(2).strip()
bad = 0
for s in stanzas:
    ep = int(s["MTIME_EPOCH"])
    want = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ep))
    got = s.get("MTIME_UTC_RENDER")
    loc = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(ep))
    ok = (got == want)
    bad += 0 if ok else 1
    print("%-46s mtime_epoch=%s utc_render=%s gmtime=%s %s | local=%s inode=%s ctime=%s" % (
        s["PATH"].split("/")[-1], ep, got, want, "OK" if ok else "MISMATCH",
        loc, s.get("INODE"), s.get("CTIME_EPOCH")))
print("label_mismatches=%d stanzas=%d" % (bad, len(stanzas)))
PY

echo
echo "=== E. independent stat cross-check vs my own capture (sha+inode+ctime) ==="
for p in "$HOME/.config/devin/mcp_config.json" "$HOME/.omp/agent/mcp.json" "$HOME/.kimi-code/config.toml" "$HOME/.bashrc" "$HOME/.profile"; do
  read -r mt ino ct sz <<<"$(stat -c '%Y %i %Z %s' "$p")"
  printf '%s  %s | stat mtime=%s inode=%s ctime=%s size=%s\n' "$(sha256sum "$p" | cut -d' ' -f1)" "$p" "$mt" "$ino" "$ct" "$sz"
done

echo
echo "=== F. refusal: capture --out onto a scoped path (scratch copy, must not truncate) ==="
cp "$HOME/.bashrc" "$W/refusal-target.conf"
BEFORE=$(sha256sum "$W/refusal-target.conf" | cut -d' ' -f1)
python3 "$TOOL" capture --out "$W/refusal-target.conf" --paths "$W/refusal-target.conf" \
        --label refusal-probe 2>&1 | tail -3
rc=${PIPESTATUS[0]}
echo "refusal_exit=$rc"
AFTER=$(sha256sum "$W/refusal-target.conf" | cut -d' ' -f1)
echo "scratch_sha_before=$BEFORE"
echo "scratch_sha_after =$AFTER"
echo "verdict: $( [ "$BEFORE" = "$AFTER" ] && echo 'UNCHANGED (refusal held)' || echo 'MODIFIED — FAIL' )"
echo "(scratch copy only; no real custody path was ever named as --out)"
