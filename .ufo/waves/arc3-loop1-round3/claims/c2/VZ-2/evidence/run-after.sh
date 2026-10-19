#!/bin/bash
# VZ-2 post-state injection harness. Usage: run-after.sh <path-to-revised-tool>
# Runs on scratch copies only; never touches a custody path (read-only captures excepted).
set -u
T="${1:?usage: run-after.sh <tool>}"
B=/var/tmp/vz2/after
rm -rf "$B"; mkdir -p "$B/fx"
TC="$B/cp/custody-pair.py"; mkdir -p "$B/cp"; cp "$T" "$TC"
cd "$B"
echo "=== POST tool sha (copied): $(sha256sum "$TC" | cut -d' ' -f1) ==="
echo "=== source tool sha: $(sha256sum "$T" | cut -d' ' -f1) ==="

echo "=== J0: selftest (cases expected >=17, CLEAN, exit 0) ==="
mkdir -p "$B/st"
python3 "$TC" selftest --scratch "$B/st" 2>&1 | tail -30
echo "J0 exit=${PIPESTATUS[0]}"

echo "=== J1a: capture over lstat-EACCES path (declared class? receipt kept?) ==="
mkdir -p fx/d_noexec; echo hidden > fx/d_noexec/secret.conf; chmod 000 fx/d_noexec
python3 "$TC" capture --out r1.txt --paths "$PWD/fx/d_noexec/secret.conf" 2>&1 | tail -6
echo "J1a capture exit=${PIPESTATUS[0]}"
grep -E "EXISTS|STAT-ERROR|READ-ERROR|CUSTODY_PAIR_CAPTURE" r1.txt 2>/dev/null
chmod 755 fx/d_noexec

echo "=== J1b: verify that receipt --live (must NOT be MATCH) ==="
chmod 000 fx/d_noexec
python3 "$TC" verify r1.txt --live 2>&1 | grep -E "A format|PATH |VERDICT|CUSTODY_PAIR|SHA256-CONTRACT"
echo "J1b verify exit=${PIPESTATUS[0]}"
echo "--- J1c: receipt-vs-receipt on two EACCES captures (fail-closed pair mode) ---"
python3 "$TC" capture --out r1b.txt --paths "$PWD/fx/d_noexec/secret.conf" >/dev/null 2>&1
python3 "$TC" verify r1.txt r1b.txt 2>&1 | grep -E "A format|PATH |VERDICT|CUSTODY_PAIR|SHA256-CONTRACT"
echo "J1c pair exit=${PIPESTATUS[0]}"
chmod 755 fx/d_noexec

echo "=== J2a: capture over exists-but-unreadable file (no traceback) ==="
echo "unreadable content" > fx/unreadable.conf; chmod 000 fx/unreadable.conf
python3 "$TC" capture --out r2.txt --paths "$PWD/fx/unreadable.conf" 2>&1 | tail -8
echo "J2a capture exit=${PIPESTATUS[0]}"
grep -E "EXISTS|READ-ERROR|STAT-ERROR|CUSTODY_PAIR_CAPTURE" r2.txt 2>/dev/null
chmod 644 fx/unreadable.conf

echo "=== J2b: verify --live against unreadable candidate (no traceback) ==="
echo "readable ref" > fx/readable.conf
python3 "$TC" capture --out r3.txt --paths "$PWD/fx/readable.conf" >/dev/null 2>&1
chmod 000 fx/readable.conf
python3 "$TC" verify r3.txt --live 2>&1 | tail -8
echo "J2b verify exit=${PIPESTATUS[0]}"
chmod 644 fx/readable.conf

echo "=== J3: partial-coverage verify (1-of-5) with/without --require-paths 5 ==="
for i in 1 2 3 4 5; do echo "fixture $i payload" > fx/cov$i.conf; done
python3 "$TC" capture --out cov1-receipt.txt --paths "$PWD/fx/cov1.conf" >/dev/null 2>&1
python3 "$TC" verify cov1-receipt.txt --live 2>&1 | tail -4; echo "J3-plain exit=${PIPESTATUS[0]}"
python3 "$TC" verify cov1-receipt.txt --live --require-paths 5 2>&1 | tail -5; echo "J3-req5 exit=${PIPESTATUS[0]}"
python3 "$TC" verify cov1-receipt.txt --live --require-paths 1 2>&1 | tail -4; echo "J3-req1 exit=${PIPESTATUS[0]}"

echo "=== J4: write-guard scope ==="
echo "scoped payload, must survive" > fx/scoped.conf
S_before=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
python3 "$TC" capture --out "$PWD/fx/scoped.conf" --paths "$PWD/fx/scoped.conf" 2>&1 | tail -3
echo "J4a exit=${PIPESTATUS[0]}"; S_after=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
echo "scoped.conf sha before=$S_before after=$S_after (equal => refused)"
echo "--- J4b: --out is a non-first element of --paths ---"
echo "second payload" > fx/second.conf
S2_before=$(sha256sum fx/second.conf | cut -d' ' -f1)
python3 "$TC" capture --out "$PWD/fx/second.conf" --paths "$PWD/fx/cov1.conf" "$PWD/fx/second.conf" 2>&1 | tail -3
echo "J4b exit=${PIPESTATUS[0]}"; S2_after=$(sha256sum fx/second.conf | cut -d' ' -f1)
echo "second.conf sha before=$S2_before after=$S2_after (equal => refused)"
echo "--- J4c: canonical path still guarded ---"
python3 "$TC" capture --out "$HOME/.bashrc" --paths "$HOME/.bashrc" 2>&1 | tail -2; echo "J4c exit=${PIPESTATUS[0]}"
echo "--- J4d: symlink alias to a scoped path as --out ---"
ln -sf "$PWD/fx/scoped.conf" fx/alias.conf
S_before=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
python3 "$TC" capture --out "$PWD/fx/alias.conf" --paths "$PWD/fx/scoped.conf" 2>&1 | tail -3
echo "J4d exit=${PIPESTATUS[0]}"; S_after=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
echo "scoped.conf via alias sha before=$S_before after=$S_after (equal => refused)"
echo "--- J4e: hardlink alias to a scoped path as --out ---"
ln -f "$PWD/fx/scoped.conf" fx/hardlink.conf 2>/dev/null && {
  S_before=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
  python3 "$TC" capture --out "$PWD/fx/hardlink.conf" --paths "$PWD/fx/scoped.conf" 2>&1 | tail -3
  echo "J4e exit=${PIPESTATUS[0]}"; S_after=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
  echo "scoped.conf via hardlink sha before=$S_before after=$S_after (equal => refused)"
}

echo "=== J5: selftest --scratch <missing dir> (declared USAGE, no traceback) ==="
python3 "$TC" selftest --scratch "$B/no-such-dir" 2>&1 | tail -6
echo "J5 exit=${PIPESTATUS[0]}"

echo "=== J4f (debt probe): sidecar-derived path clobber ==="
echo "sidecar victim payload" > fx/vic.sha256
V_before=$(sha256sum fx/vic.sha256 | cut -d' ' -f1)
python3 "$TC" capture --out "$PWD/fx/vic" --paths "$PWD/fx/vic.sha256" 2>&1 | tail -2
echo "J4f exit=${PIPESTATUS[0]}"; V_after=$(sha256sum fx/vic.sha256 | cut -d' ' -f1)
echo "vic.sha256 sha before=$V_before after=$V_after (equal => protected)"

echo "=== J4g (debt probe): --out whose parent is a regular file ==="
echo "not a dir" > fx/plainfile
python3 "$TC" capture --out "$PWD/fx/plainfile/sub/r.txt" --paths "$PWD/fx/cov1.conf" 2>&1 | tail -5
echo "J4g exit=${PIPESTATUS[0]}"

echo "=== J2c (debt probe): blocked-side alias (inode arm vs UNEVALUABLE) ==="
mkdir -p fx/blk; echo "blocked victim" > fx/blk/bside.conf
ln -f fx/blk/bside.conf fx/bside-hardlink.conf 2>/dev/null
chmod 000 fx/blk
B_before=$(sha256sum fx/bside-hardlink.conf | cut -d' ' -f1)
python3 "$TC" capture --out "$PWD/fx/bside-hardlink.conf" --paths "$PWD/fx/blk/bside.conf" 2>&1 | tail -3
echo "J2c exit=${PIPESTATUS[0]}"; B_after=$(sha256sum fx/bside-hardlink.conf | cut -d' ' -f1)
echo "alias sha before=$B_before after=$B_after (equal => protected)"
chmod 755 fx/blk

echo "=== J6: live pair (read-only capture of the 5 custody paths) ==="
python3 "$TC" capture --out "$B/live-pre.txt" --label "VZ-2 post-harness pre" 2>&1 | tail -2; echo "J6-pre exit=${PIPESTATUS[0]}"
sleep 1
python3 "$TC" capture --out "$B/live-post.txt" --label "VZ-2 post-harness post" 2>&1 | tail -2; echo "J6-post exit=${PIPESTATUS[0]}"
python3 "$TC" verify "$B/live-pre.txt" "$B/live-post.txt" 2>&1 | tail -3; echo "J6-verify exit=${PIPESTATUS[0]}"
echo "--- receipts self-pin the revised tool sha? ---"
grep -h "^# tool:" "$B/live-pre.txt" "$B/live-post.txt"

echo "=== J7: v1 receipts remain sha256-verifiable ==="
K=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 "$TC" verify "$K/.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt" --live 2>&1 | tail -4; echo "J7-stanza exit=${PIPESTATUS[0]}"
python3 "$TC" verify "$K/.ufo/waves/arc3-loop1-round1/claims/c3/EX-26/custody-sha256.txt" --live 2>&1 | tail -4; echo "J7-sums exit=${PIPESTATUS[0]}"

echo "=== J8: declared map in docstring of the revised tool ==="
sed -n '55,120p' "$TC"