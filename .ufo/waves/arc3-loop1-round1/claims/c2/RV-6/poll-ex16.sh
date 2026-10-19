#!/usr/bin/env bash
# RV-6 poll: wait for EX-16 (c2 implementer) to land its guard change.
# Lands = probe or expected.json sha256 changes, or EX-16 artifact dir appears.
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=$REPO/.ufo/waves/arc3-loop1-round1/claims/c2/RV-6
cd "$REPO"
probe_before=$(sha256sum .ufo/gates/citation-drift/citation-drift-probe.py | cut -d' ' -f1)
exp_before=$(sha256sum .ufo/gates/citation-drift/expected.json | cut -d' ' -f1)
skill_before=$(sha256sum SKILL.md | cut -d' ' -f1)
echo "poll start $(date -Is) probe=$probe_before exp=$exp_before skill=$skill_before" > "$S/poll.log"
for i in $(seq 1 25); do
  probe_now=$(sha256sum .ufo/gates/citation-drift/citation-drift-probe.py | cut -d' ' -f1)
  exp_now=$(sha256sum .ufo/gates/citation-drift/expected.json | cut -d' ' -f1)
  skill_now=$(sha256sum SKILL.md | cut -d' ' -f1)
  if [ "$probe_now" != "$probe_before" ] || [ "$exp_now" != "$exp_before" ] || [ "$skill_now" != "$skill_before" ] || [ -d .ufo/waves/arc3-loop1-round1/claims/c2/EX-16 ]; then
    echo "LANDED check=$i $(date -Is) probe=$probe_now exp=$exp_now skill=$skill_now" | tee -a "$S/poll.log"
    ls -la .ufo/waves/arc3-loop1-round1/claims/c2/EX-16/ 2>&1 | tee -a "$S/poll.log"
    exit 0
  fi
  echo "check=$i $(date -Is) no change" >> "$S/poll.log"
  sleep 60
done
echo "TIMEOUT after 25 checks $(date -Is)" >> "$S/poll.log"
exit 1
