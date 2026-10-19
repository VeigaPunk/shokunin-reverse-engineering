#!/bin/bash
# VZ-2 before-state injection harness (scratch only; no custody path touched)
set -u
B=/var/tmp/vz2/before
rm -rf "$B/scratch"
mkdir -p "$B/scratch/fx"
T="$B/tool-before.py"
cp /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py "$T"
cd "$B/scratch"

echo "=== BEFORE tool sha ==="
sha256sum "$T"

echo "=== I1a: capture over lstat-EACCES path ==="
mkdir -p fx/d_noexec
echo "hidden" > fx/d_noexec/secret.conf
chmod 000 fx/d_noexec
python3 "$T" capture --out r1.txt --paths "$PWD/fx/d_noexec/secret.conf" 2>&1
echo "I1a capture exit=$?"
grep -E "EXISTS|STAT-ERROR|paths=|CUSTODY_PAIR_CAPTURE" r1.txt 2>/dev/null
chmod 755 fx/d_noexec

echo "=== I1b: verify of the EACCES-recorded receipt --live (fail-open probe) ==="
chmod 000 fx/d_noexec
python3 "$T" verify r1.txt --live 2>&1 | tail -6
echo "I1b verify exit=${PIPESTATUS[0]}"
chmod 755 fx/d_noexec

echo "=== I2a: capture over exists-but-unreadable file ==="
echo "unreadable content" > fx/unreadable.conf
chmod 000 fx/unreadable.conf
python3 "$T" capture --out r2.txt --paths "$PWD/fx/unreadable.conf" 2>&1 | tail -12
echo "I2a capture exit=${PIPESTATUS[0]}"
chmod 644 fx/unreadable.conf

echo "=== I2b: verify --live against unreadable candidate ==="
echo "readable ref" > fx/readable.conf
python3 "$T" capture --out r3.txt --paths "$PWD/fx/readable.conf" >/dev/null 2>&1
chmod 000 fx/readable.conf
python3 "$T" verify r3.txt --live 2>&1 | tail -12
echo "I2b verify exit=${PIPESTATUS[0]}"
chmod 644 fx/readable.conf

echo "=== I3: partial-coverage verify (1-of-5 receipt reads exit 0) ==="
for i in 1 2 3 4 5; do echo "fixture $i payload" > fx/cov$i.conf; done
python3 "$T" capture --out cov1-receipt.txt --paths "$PWD/fx/cov1.conf" >/dev/null 2>&1
echo "A stanzas: $(grep -c '^PATH:' cov1-receipt.txt); the other 4 fixtures drift NOW:"
for i in 2 3 4 5; do echo "DRIFTED payload $i" > fx/cov$i.conf; done
python3 "$T" verify cov1-receipt.txt --live 2>&1 | tail -5
echo "I3 verify exit=${PIPESTATUS[0]}"
echo "--- for contrast: full 5-path receipt vs live sees the drift ---"
python3 "$T" capture --out cov5-receipt.txt --paths "$PWD/fx/cov1.conf" "$PWD/fx/cov2.conf" "$PWD/fx/cov3.conf" "$PWD/fx/cov4.conf" "$PWD/fx/cov5.conf" >/dev/null 2>&1
python3 "$T" verify cov5-receipt.txt --live 2>&1 | tail -3
echo "I3-contrast exit=${PIPESTATUS[0]}"

echo "=== I4: write-guard scope: --paths X --out X (scratch copy X) ==="
echo "scoped payload, must survive" > fx/scoped.conf
S_before=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
python3 "$T" capture --out "$PWD/fx/scoped.conf" --paths "$PWD/fx/scoped.conf" 2>&1 | tail -4
echo "I4 capture exit=${PIPESTATUS[0]}"
S_after=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
echo "scoped.conf sha before=$S_before after=$S_after"
head -3 fx/scoped.conf
echo "--- contrast: canonical custody path IS guarded ---"
python3 "$T" capture --out "$PWD/guard-probe.txt" --paths "$HOME/.bashrc" --out "$HOME/.bashrc" 2>&1 | tail -3
echo "I4-contrast exit=${PIPESTATUS[0]}"

echo "=== I5: selftest --scratch <missing dir> ==="
python3 "$T" selftest --scratch /var/tmp/vz2/before/no-such-dir 2>&1 | tail -8
echo "I5 selftest exit=${PIPESTATUS[0]}"

echo "=== I0: baseline selftest (expect 15 clean) ==="
python3 "$T" selftest 2>&1 | tail -3
echo "I0 selftest exit=${PIPESTATUS[0]}"

echo "=== headers ==="
echo "before tool sha: $(sha256sum "$T" | cut -d' ' -f1)"