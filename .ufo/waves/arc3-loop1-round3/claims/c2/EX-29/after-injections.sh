#!/bin/bash
# EX-29: after-state injections vs the landed revised tool (scratch only).
# Mirrors the before-probes in this seat dir so columns compare directly.
set -u
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
T=.ufo/gates/custody-pair/custody-pair.py
S=/dev/shm/ex29-scratch-after
rm -rf "$S"; mkdir -p "$S"
O=.ufo/waves/arc3-loop1-round3/claims/c2/EX-29
SHA=$(sha256sum "$T" | cut -d' ' -f1)
{ echo "tool sha=$SHA"; echo "utc=$(date -u +%FT%TZ)"; } | tee "$O/after-injections-sha.txt"

echo "### selftest"
python3 "$T" selftest --scratch /dev/shm > "$O/after-selftest.out" 2>&1; echo "selftest-exit=$?" | tee -a "$O/after-selftest.out"
tail -1 "$O/after-selftest.out"

echo "### D3: 1of3 coverage"
printf 'one\n' > "$S/one.conf"; printf 'two\n' > "$S/two.conf"; printf 'three\n' > "$S/three.conf"
python3 "$T" capture --out "$S/rec-1of3.txt" --paths "$S/one.conf" >/dev/null 2>&1; echo "capture-1of3-exit=$?"
python3 "$T" verify "$S/rec-1of3.txt" --live > "$O/after-D3-plain-1of3-vs-live.out" 2>&1; echo "plain-1of3-live-exit=$?"; tail -2 "$O/after-D3-plain-1of3-vs-live.out"
python3 "$T" verify --require-paths 3 "$S/rec-1of3.txt" --live > "$O/after-D3-require3-1of3-vs-live.out" 2>&1; echo "require3-1of3-live-exit=$?"; tail -2 "$O/after-D3-require3-1of3-vs-live.out"

echo "### D2a: dir-EACCES"
mkdir -p "$S/forbidden-dir"; printf 'inside\n' > "$S/forbidden-dir/f.conf"; chmod 000 "$S/forbidden-dir"
python3 "$T" capture --out "$S/rec-direacces.txt" --paths "$S/forbidden-dir/f.conf" > "$O/after-D2-dir-eacces-capture.out" 2>&1; echo "dir-eacces-capture-exit=$?"
grep -E "EXISTS|STAT" "$S/rec-direacces.txt"
python3 "$T" verify "$S/rec-direacces.txt" --live > "$O/after-D2-dir-eacces-verify.out" 2>&1; echo "dir-eacces-verify-exit=$?"; tail -2 "$O/after-D2-dir-eacces-verify.out"
chmod 755 "$S/forbidden-dir"

echo "### D2b: file-EACCES"
printf 'secret\n' > "$S/unreadable.conf"; chmod 000 "$S/unreadable.conf"
python3 "$T" capture --out "$S/rec-unreadable.txt" --paths "$S/unreadable.conf" > "$O/after-D2-file-eacces-capture.out" 2>&1; echo "file-eacces-capture-exit=$?"
grep -E "EXISTS|READ-ERROR" "$S/rec-unreadable.txt"
chmod 644 "$S/unreadable.conf"

echo "### D2c: live unreadable candidate"
printf 'switch\n' > "$S/switch.conf"
python3 "$T" capture --out "$S/rec-switch.txt" --paths "$S/switch.conf" >/dev/null 2>&1
chmod 000 "$S/switch.conf"
python3 "$T" verify "$S/rec-switch.txt" --live > "$O/after-D2c-live-unreadable.out" 2>&1; echo "live-unreadable-exit=$?"; tail -2 "$O/after-D2c-live-unreadable.out"
chmod 644 "$S/switch.conf"

echo "### D6: selftest missing scratch"
python3 "$T" selftest --scratch "$S/does-not-exist" > "$O/after-D6-selftest-missing-scratch.out" 2>&1; echo "D6-exit=$?"; tail -2 "$O/after-D6-selftest-missing-scratch.out"

echo "### write-guard clobber"
printf 'payload-guarded\n' > "$S/guard.conf"; sha_before=$(sha256sum "$S/guard.conf" | cut -d' ' -f1)
python3 "$T" capture --paths "$S/guard.conf" --out "$S/guard.conf" > "$O/after-writeguard-clobber.out" 2>&1; echo "clobber-exit=$?"
sha_after=$(sha256sum "$S/guard.conf" | cut -d' ' -f1)
echo "guard.conf sha before=$sha_before after=$sha_after"