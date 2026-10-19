#!/bin/bash
# VZ-2 late-join before→after harness (chain c2 convergence, arc3-loop1-round3).
# Runs the BASE blob (git HEAD) and the LANDED revision side by side on scratch
# copies only. Custody paths are never written. Scratch: /var/tmp/vz2 (never /tmp).
set -u
BASE_TOOL=/var/tmp/vz2/base/custody-pair.py      # git show HEAD blob, sha re-derived below
AFTER_TOOL=/var/tmp/vz2/final/cp.py              # byte-identical copy of the landed tool
W=/var/tmp/vz2/latejoin
rm -rf "$W"; mkdir -p "$W"

echo "=== VZ-2 late-join harness ==="
echo "utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "BASE  tool sha: $(sha256sum "$BASE_TOOL" | cut -d' ' -f1)"
echo "AFTER tool sha: $(sha256sum "$AFTER_TOOL" | cut -d' ' -f1)"
echo "HEAD  blob sha: $(git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show HEAD:.ufo/gates/custody-pair/custody-pair.py | sha256sum | cut -d' ' -f1)"
echo

run_col () {   # run_col <label> <tool>
  L="$1"; T="$2"; D="$W/$L"; mkdir -p "$D/fx" "$D/st"; cd "$D" || exit 1
  echo "########## $L (tool sha $(sha256sum "$T" | cut -c1-12))"

  echo "--- L0 selftest (base scratch present) ---"
  python3 "$T" selftest --scratch "$D/st" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"

  echo "--- L1 D6: selftest --scratch <missing> ---"
  python3 "$T" selftest --scratch "$D/no-such-dir" 2>&1 | tail -3; echo "exit=${PIPESTATUS[0]}"

  echo "--- L2 D2a: capture over lstat-EACCES path, then verify --live ---"
  mkdir -p fx/d_noexec; echo hidden > fx/d_noexec/secret.conf; chmod 000 fx/d_noexec
  python3 "$T" capture --out r1.txt --paths "$PWD/fx/d_noexec/secret.conf" 2>&1 | tail -2
  echo "capture exit=${PIPESTATUS[0]}"
  grep -E "^EXISTS|^STAT-ERROR|^READ-ERROR" r1.txt 2>/dev/null
  python3 "$T" verify r1.txt --live 2>&1 | tail -2; echo "verify exit=${PIPESTATUS[0]}"
  chmod 755 fx/d_noexec

  echo "--- L3 D2b: capture over exists-but-unreadable file ---"
  echo "unreadable" > fx/unreadable.conf; chmod 000 fx/unreadable.conf
  python3 "$T" capture --out r2.txt --paths "$PWD/fx/unreadable.conf" 2>&1 | tail -2
  echo "capture exit=${PIPESTATUS[0]}"
  echo "receipt written: $([ -f r2.txt ] && echo yes || echo NO)"
  grep -E "^EXISTS|^STAT-ERROR|^READ-ERROR" r2.txt 2>/dev/null
  chmod 644 fx/unreadable.conf

  echo "--- L4 D3: 1-of-5 reference, plain then --require-paths 5 ---"
  for i in 1 2 3 4 5; do echo "payload $i" > fx/cov$i.conf; done
  python3 "$T" capture --out cov1.txt --paths "$PWD/fx/cov1.conf" >/dev/null 2>&1
  python3 "$T" verify cov1.txt --live 2>&1 | tail -2; echo "plain exit=${PIPESTATUS[0]}"
  python3 "$T" verify cov1.txt --live --require-paths 5 2>&1 | tail -3; echo "req5 exit=${PIPESTATUS[0]}"

  echo "--- L5/L6 write guard: scoped-as-out, hardlink alias, symlink alias ---"
  echo "scoped payload" > fx/scoped.conf
  S0=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
  python3 "$T" capture --out "$PWD/fx/scoped.conf" --paths "$PWD/fx/scoped.conf" 2>&1 | tail -1
  echo "exit=${PIPESTATUS[0]}"
  S1=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
  echo "scoped.conf before=$S0"; echo "scoped.conf after =$S1"; [ "$S0" = "$S1" ] && echo "INTACT" || echo "CLOBBERED"
  ln -f fx/scoped.conf fx/alias-hard.conf 2>/dev/null && {
    A0=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
    python3 "$T" capture --out "$PWD/fx/alias-hard.conf" --paths "$PWD/fx/scoped.conf" 2>&1 | tail -1
    echo "hardlink exit=${PIPESTATUS[0]}"
    A1=$(sha256sum fx/scoped.conf | cut -d' ' -f1); [ "$A0" = "$A1" ] && echo "INTACT" || echo "CLOBBERED"
  }
  ln -sf "$PWD/fx/scoped.conf" fx/alias-sym.conf && {
    Y0=$(sha256sum fx/scoped.conf | cut -d' ' -f1)
    python3 "$T" capture --out "$PWD/fx/alias-sym.conf" --paths "$PWD/fx/scoped.conf" 2>&1 | tail -1
    echo "symlink exit=${PIPESTATUS[0]}"
    Y1=$(sha256sum fx/scoped.conf | cut -d' ' -f1); [ "$Y0" = "$Y1" ] && echo "INTACT" || echo "CLOBBERED"
  }

  echo "--- L7 live pair + gate (read-only capture of the 5 custody paths) ---"
  python3 "$T" capture --out live-pre.txt --label "VZ-2 latejoin $L pre" 2>&1 | tail -1
  echo "pre exit=${PIPESTATUS[0]}"
  sleep 1
  python3 "$T" capture --out live-post.txt --label "VZ-2 latejoin $L post" 2>&1 | tail -1
  echo "post exit=${PIPESTATUS[0]}"
  python3 "$T" verify live-pre.txt live-post.txt 2>&1 | tail -2; echo "plain exit=${PIPESTATUS[0]}"
  python3 "$T" verify live-pre.txt live-post.txt --require-paths 5 2>&1 | tail -2; echo "gated exit=${PIPESTATUS[0]}"
  grep -h "^# tool:" live-pre.txt live-post.txt
  echo "sidecar check: $(cd "$D" && sha256sum -c live-pre.txt.sha256 2>&1 | tail -1)"

  echo "--- L8 v1 shapes ---"
  K=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
  cp "$K/.ufo/waves/arc3-loop1-round3/claims/c2/VZ-2/evidence/v1-sums-four-undrifted-paths.txt" sums4.txt
  python3 "$T" verify sums4.txt --live 2>&1 | tail -2; echo "sums4 exit=${PIPESTATUS[0]}"
  python3 "$T" verify "$K/.ufo/waves/arc3-loop1-round1/claims/c3/EX-26/custody-sha256.txt" --live 2>&1 | tail -2
  echo "r1sums exit=${PIPESTATUS[0]}"
  echo
}

run_col BASE "$BASE_TOOL"
run_col AFTER "$AFTER_TOOL"

echo "=== custody paths untouched (read-only block) ==="
sha256sum /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json \
          /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile
