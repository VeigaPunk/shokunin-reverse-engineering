#!/usr/bin/env bash
# R42-C1 unblob log tee (kaidoku round 42, L1 KaidokuR42; R42C1Sentinel H1).
#
# REA 6.5.0 runs unblob with `--log <task dir>/unblob.log` and deletes its task
# dir after the run, so a successful envelope never shows which extractor ran
# (`sasquatch -le|-be` vs anything else on PATH). c1-run.sh sets this script as
# REA_UNBLOB_COMMAND for the `after` arm: it runs the real unblob with REA's
# arguments unchanged, then copies the `--log` file to $C1_LOG_COPY (when set)
# and exits with unblob's own exit code. It never edits an argument, the input,
# the output or the log.
#
#   env C1_REAL_UNBLOB  absolute path of the real unblob (default: realpath of
#                       ~/.local/bin/unblob)
#   env C1_LOG_COPY     destination for the copy of unblob's --log file
set -u
real=${C1_REAL_UNBLOB:-$(readlink -f "$HOME/.local/bin/unblob")}
case $real in /*) ;; *) echo "unblob-logtee: C1_REAL_UNBLOB must be absolute" >&2; exit 2 ;; esac
log=
prev=
for a in "$@"; do
  if [[ $prev == --log ]]; then log=$a; fi
  prev=$a
done
"$real" "$@"
rc=$?
if [[ -n ${C1_LOG_COPY:-} && -n $log && -f $log ]]; then
  cp -- "$log" "$C1_LOG_COPY" || echo "unblob-logtee: copy of $log failed" >&2
fi
exit "$rc"
