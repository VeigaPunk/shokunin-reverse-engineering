#!/usr/bin/env bash
# score-receipt.sh — wrap one counter run in a score receipt (kaidoku round 40,
# routed defect R39-CL6: score receipts must carry the counter's exit code).
#
#   score-receipt.sh OUT.json -- <counter argv...>
#   score-receipt.sh --selftest
#
# Runs <counter argv...> once with stdout/stderr captured, then writes
# OUT.json = the counter's own JSON (the stdout object, spread at top level;
# a JSON array/scalar goes under "result") augmented with the wrapper keys
#   exit_code  argv  counter_sha256  utc_start  utc_end
# and the diagnostics
#   receipt_version, counter, counter_bytes, stdout_sha256, stdout_bytes,
#   stderr_sha256, stderr_bytes, stdout, stdout_truncated, stderr,
#   stderr_truncated, stdout_json, result_kind, counter_json_key_collisions,
#   lane_revision_arguments  (+ lane_root, lane_head with --lane)
# A counter key that collides with a wrapper/diagnostic key is kept out of the
# top level and named in counter_json_key_collisions, so the real exit code can
# never be shadowed by counter output.
#
# utc_start/utc_end are UTC ISO-8601 with milliseconds, taken immediately
# around the counter process. stdout/stderr are embedded as text decoded with
# U+FFFD replacement (the receipt always stays valid UTF-8 JSON); their full
# bytes are always hashed and sized, and embedding is cut at
# --max-capture-bytes per stream with a *_truncated flag.
#
# lane_revision_arguments harvests, from the counter argv (both `--flag value`
# and `--flag=value`, repeats kept as a list, flags lower-cased): --rev --freeze
# --base --at --lane-rev --root --lane. That is the revision set the counter was
# pointed at, recorded independently of the counter's own honesty.
#
# Options (before --):
#   --counter PATH          file whose sha256 is the counter's (default: argv[0]
#                           when it is a regular file, else the first regular-file
#                           argument after an interpreter name such as python3,
#                           bash or node; --counter names the file explicitly for
#                           other runners)
#   --lane DIR              record DIR's absolute path and `git -C DIR rev-parse
#                           HEAD` (read-only) as lane_root / lane_head
#   --max-capture-bytes N   per-stream text embedding cap (default 1048576)
#   --selftest              run the built-in cases (exit 0 all pass / 1 fail)
#
# The tmp staging directory comes from mktemp -d (so TMPDIR is honoured); it is
# removed on exit. OUT.json's parent directory must already exist.
#
# Exit: the counter's own exit status when the receipt was written; 2 on a
# usage/environment error (bad OUT, unreadable counter, receipt write failure).
set -uo pipefail

PROG=$(basename -- "$0")
SELF=$(cd -- "$(dirname -- "$0")" && pwd)/$(basename -- "$0")

usage() {
  cat >&2 <<'EOF'
usage: score-receipt.sh OUT.json -- <counter argv...>
       score-receipt.sh --selftest
options: --counter PATH | --lane DIR | --max-capture-bytes N | --selftest
Exit is the counter's exit status; 2 = usage/environment error.
EOF
  exit 2
}

die() { printf '%s: %s\n' "$PROG" "$*" >&2; exit 2; }

run_selftest() {
  python3 - "$SELF" <<'PY'
import hashlib, json, os, re, subprocess, sys, tempfile

self_path = sys.argv[1]
work = tempfile.mkdtemp(prefix="score-receipt-selftest.")
cases = []
failures = []

def check(label, ok, detail=""):
    cases.append(label)
    if not ok:
        failures.append("%s%s" % (label, (": " + detail) if detail else ""))

def put(name, text, mode=0o755):
    p = os.path.join(work, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    os.chmod(p, mode)
    return p

def invoke(out, counter_argv, extra=()):
    return subprocess.run([self_path, *extra, out, "--", *counter_argv],
                          capture_output=True, text=True)

def load(path):
    with open(path, "rb") as f:
        raw = f.read()
    return raw, json.loads(raw.decode("utf-8"))

UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")

def base_checks(label, raw, rec):
    required = ("exit_code", "argv", "counter_sha256", "utc_start", "utc_end")
    check(label + ":wrapper keys", all(k in rec for k in required), repr(list(rec)))
    check(label + ":utc format",
          bool(UTC.match(rec.get("utc_start", ""))) and bool(UTC.match(rec.get("utc_end", ""))),
          "%r %r" % (rec.get("utc_start"), rec.get("utc_end")))
    check(label + ":utc ordered", rec.get("utc_start", "") <= rec.get("utc_end", ""),
          "%r > %r" % (rec.get("utc_start"), rec.get("utc_end")))
    check(label + ":receipt newline", raw.endswith(b"\n"), raw[-8:])

# 1. JSON object, exit 0: keys spread, exit code, hashes, stdout text.
c1 = put("ok.sh", '#!/bin/sh\nprintf \'{"met_target": true, "matched": 6}\\n\'\nexit 0\n')
o1 = os.path.join(work, "r1.json")
p1 = invoke(o1, [c1]); raw1, r1 = load(o1)
base_checks("object-ok", raw1, r1)
check("object-ok:exit", p1.returncode == 0 and r1["exit_code"] == 0, repr(p1))
check("object-ok:spread", r1.get("met_target") is True and r1.get("matched") == 6)
check("object-ok:argv", r1["argv"] == [c1], repr(r1["argv"]))
check("object-ok:counter sha", r1["counter_sha256"] == hashlib.sha256(open(c1, "rb").read()).hexdigest())
check("object-ok:stdout sha",
      r1["stdout_sha256"] == hashlib.sha256(b'{"met_target": true, "matched": 6}\n').hexdigest())
check("object-ok:stdout text", r1["stdout"] == '{"met_target": true, "matched": 6}\n', repr(r1["stdout"]))
check("object-ok:stdout_json", r1["stdout_json"] is True)

# 2. JSON object, exit 1: status propagates and the counter's verdict survives.
c2 = put("fail.sh", '#!/bin/sh\nprintf \'{"met_target": false}\\n\'\nexit 1\n')
o2 = os.path.join(work, "r2.json")
p2 = invoke(o2, [c2]); _, r2 = load(o2)
check("fail-propagates", p2.returncode == 1 and r2["exit_code"] == 1 and r2["met_target"] is False)

# 3. Non-JSON stdout + stderr text, exit 3.
c3 = put("text.sh", '#!/bin/sh\nprintf \'not json at all\\n\'\nprintf \'boom\\n\' >&2\nexit 3\n')
o3 = os.path.join(work, "r3.json")
p3 = invoke(o3, [c3]); _, r3 = load(o3)
base_checks("text-out", open(o3, "rb").read(), r3)
check("text-out:exit", p3.returncode == 3 and r3["exit_code"] == 3)
check("text-out:no spread", r3["stdout_json"] is False and "result" not in r3)
check("text-out:stderr verbatim", r3["stderr"] == "boom\n", repr(r3["stderr"]))
check("text-out:stderr sha", r3["stderr_sha256"] == hashlib.sha256(b"boom\n").hexdigest())

# 4. JSON array stdout: preserved under result.
c4 = put("array.sh", '#!/bin/sh\nprintf \'[1, 2, 3]\\n\'\nexit 0\n')
o4 = os.path.join(work, "r4.json")
p4 = invoke(o4, [c4]); _, r4 = load(o4)
check("array:result", r4.get("result") == [1, 2, 3] and r4.get("result_kind") == "list", repr(r4))
check("array:exit", p4.returncode == 0 and r4["exit_code"] == 0)

# 5. Counter prints a colliding exit_code: real status wins, collision recorded.
c5 = put("collide.sh", '#!/bin/sh\nprintf \'{"exit_code": 99, "ok": true}\\n\'\nexit 0\n')
o5 = os.path.join(work, "r5.json")
p5 = invoke(o5, [c5]); _, r5 = load(o5)
check("collision:status wins", p5.returncode == 0 and r5["exit_code"] == 0, repr(r5["exit_code"]))
check("collision:recorded", "exit_code" in r5["counter_json_key_collisions"], repr(r5["counter_json_key_collisions"]))
check("collision:other key kept", r5.get("ok") is True)

# 6. Interpreter argv: sha256 resolves the script, not the interpreter.
c6 = put("counter6.py", 'import json\nprint(json.dumps({"matched": 1}))\n', 0o644)
o6 = os.path.join(work, "r6.json")
p6 = invoke(o6, [sys.executable, c6]); _, r6 = load(o6)
base_checks("interpreter", open(o6, "rb").read(), r6)
check("interpreter:sha is script",
      r6["counter_sha256"] == hashlib.sha256(open(c6, "rb").read()).hexdigest(), repr(r6["counter"]))
check("interpreter:argv verbatim", r6["argv"] == [sys.executable, c6] and p6.returncode == 0)

# 7. --counter override records an explicitly named file.
c7 = put("real-counter.sh", '#!/bin/sh\nexit 0\n')
c7wrap = put("wrapper.sh", '#!/bin/sh\nexit 0\n')
o7 = os.path.join(work, "r7.json")
p7 = invoke(o7, [c7wrap], extra=("--counter", c7)); _, r7 = load(o7)
check("counter override",
      r7["counter_sha256"] == hashlib.sha256(open(c7, "rb").read()).hexdigest()
      and r7["argv"] == [c7wrap] and p7.returncode == 0)

# 8. Missing counter executable: 127 is recorded, receipt still lands.
o8 = os.path.join(work, "r8.json")
p8 = invoke(o8, [os.path.join(work, "does-not-exist")]); _, r8 = load(o8)
check("missing counter", p8.returncode == 127 and r8["exit_code"] == 127
      and r8["counter_sha256"] is None, repr((p8.returncode, r8["exit_code"], r8["counter_sha256"])))

# 9. Revision arguments harvested from argv.
o9 = os.path.join(work, "r9.json")
p9 = invoke(o9, [c1, "--root", "/lane", "--rev", "abc123", "--freeze=def456", "--rev", "abc999"])
_, r9 = load(o9)
check("rev args", r9["lane_revision_arguments"].get("rev") == ["abc123", "abc999"]
      and r9["lane_revision_arguments"].get("freeze") == "def456"
      and r9["lane_revision_arguments"].get("root") == "/lane", repr(r9["lane_revision_arguments"]))
check("rev args:argv keeps flags", r9["argv"][1:] == ["--root", "/lane", "--rev", "abc123",
                                                     "--freeze=def456", "--rev", "abc999"])

# 10. --lane records the absolute root, and a non-repo head is null, not a crash.
o10 = os.path.join(work, "r10.json")
p10 = invoke(o10, [c1], extra=("--lane", work)); _, r10 = load(o10)
check("lane option",
      r10.get("lane_root") == os.path.abspath(work) and p10.returncode == 0
      and (r10.get("lane_head") is None or bool(re.fullmatch(r"[0-9a-f]{40}", r10.get("lane_head") or ""))),
      repr((r10.get("lane_root"), r10.get("lane_head"))))

# 11. Embedding cap: truncated flag set, full bytes still hashed.
c11 = put("big.sh", '#!/bin/sh\nprintf "%s" "' + ("x" * 200) + '"\nexit 0\n')
o11 = os.path.join(work, "r11.json")
p11 = invoke(o11, [c11], extra=("--max-capture-bytes", "8")); _, r11 = load(o11)
check("capture cap",
      len(r11["stdout"]) == 8 and r11["stdout_truncated"] is True
      and r11["stdout_bytes"] == 200
      and r11["stdout_sha256"] == hashlib.sha256(b"x" * 200).hexdigest(), repr(r11))

# 12. Non-ASCII stdout survives as UTF-8 text.
c12 = put("utf8.sh", '#!/bin/sh\nprintf \'{"note": "caf\\303\\251 \\342\\234\\223"}\\n\'\nexit 0\n')
o12 = os.path.join(work, "r12.json")
p12 = invoke(o12, [c12]); raw12, r12 = load(o12)
check("utf8", r12.get("note") == "caf\u00e9 \u2713" and p12.returncode == 0, repr(r12.get("note")))

# 13. argv elements with spaces stay one element.
o13 = os.path.join(work, "r13.json")
p13 = invoke(o13, [c1, "a b", "c"]); _, r13 = load(o13)
check("argv spaces", r13["argv"] == [c1, "a b", "c"], repr(r13["argv"]))

# 14. Usage/environment errors: missing --, missing OUT, missing OUT parent.
p14 = subprocess.run([self_path, os.path.join(work, "r14.json"), c1], capture_output=True, text=True)
check("missing -- -> 2", p14.returncode == 2, repr(p14.returncode))
p15 = subprocess.run([self_path, "--", c1], capture_output=True, text=True)
check("missing OUT -> 2", p15.returncode == 2, repr(p15.returncode))
o16 = os.path.join(work, "no-such-dir", "r16.json")
p16 = invoke(o16, [c1])
check("missing OUT parent -> 2", p16.returncode == 2 and not os.path.exists(o16), repr(p16.returncode))
check("missing OUT parent: no tmp litter",
      not any(n.startswith("r16.json.tmp") for n in os.listdir(work)), repr(os.listdir(work)))

# 15. The counter's cwd is the caller's cwd (relative counter path resolves).
c17 = put("rel.sh", '#!/bin/sh\npwd\nexit 0\n')
o17 = os.path.join(work, "r17.json")
p17 = subprocess.run([self_path, o17, "--", "./rel.sh"], cwd=work, capture_output=True, text=True)
_, r17 = load(o17)
check("cwd passthrough", r17["stdout"].strip() == os.path.realpath(work)
      and r17["counter_sha256"] == hashlib.sha256(open(c17, "rb").read()).hexdigest(),
      repr(r17["stdout"]))

# 16. Invalid UTF-8 stdout: the receipt stays valid UTF-8 JSON, raw bytes hashed.
c18 = put("binary.sh", "#!/bin/sh\nprintf '\\377{\"a\":1}'\nexit 0\n")
o18 = os.path.join(work, "r18.json")
p18 = invoke(o18, [c18]); raw18, r18 = load(o18)
base_checks("binary-out", raw18, r18)
check("binary-out:valid json", p18.returncode == 0 and r18["stdout_json"] is False, repr(p18.returncode))
check("binary-out:replacement",
      r18["stdout_sha256"] == hashlib.sha256(b"\xff{\"a\":1}").hexdigest()
      and r18["stdout"].startswith("\ufffd"), repr(r18["stdout"]))

# 17. A signalled counter reports 128+signal and still leaves a receipt.
c19 = put("signal.sh", "#!/bin/sh\nkill -TERM $$\n")
o19 = os.path.join(work, "r19.json")
p19 = invoke(o19, [c19]); _, r19 = load(o19)
check("signal exit", p19.returncode == 143 and r19["exit_code"] == 143,
      repr((p19.returncode, r19["exit_code"])))

print("score-receipt selftest: %d/%d cases pass" % (len(cases) - len(failures), len(cases)))
for f in failures:
    print("FAIL " + f)
sys.exit(1 if failures else 0)
PY
}

OUT=""
COUNTER_OVERRIDE=""
LANE_DIR=""
MAX_CAPTURE=1048576
SELFTEST=0
CARGV=()

while (($#)); do
  case "$1" in
    --selftest) SELFTEST=1; shift ;;
    --counter) [[ $# -ge 2 && -n $2 ]] || die "--counter needs a path"; COUNTER_OVERRIDE=$2; shift 2 ;;
    --counter=*) COUNTER_OVERRIDE=${1#*=}; [[ -n $COUNTER_OVERRIDE ]] || die "--counter needs a path"; shift ;;
    --lane) [[ $# -ge 2 && -n $2 ]] || die "--lane needs a directory"; LANE_DIR=$2; shift 2 ;;
    --lane=*) LANE_DIR=${1#*=}; [[ -n $LANE_DIR ]] || die "--lane needs a directory"; shift ;;
    --max-capture-bytes) [[ $# -ge 2 && $2 =~ ^[0-9]+$ ]] || die "--max-capture-bytes needs a non-negative integer"; MAX_CAPTURE=$2; shift 2 ;;
    --max-capture-bytes=*) MAX_CAPTURE=${1#*=}; [[ $MAX_CAPTURE =~ ^[0-9]+$ ]] || die "--max-capture-bytes needs a non-negative integer"; shift ;;
    --help|-h) usage ;;
    --) shift; CARGV=("$@"); break ;;
    -*) die "unknown option: $1" ;;
    *) [[ -z $OUT ]] || die "unexpected argument: $1"; OUT=$1; shift ;;
  esac
done

if ((SELFTEST)); then
  run_selftest
  exit $?
fi

[[ -n $OUT ]] || usage
((${#CARGV[@]})) || usage
[[ -d $(dirname -- "$OUT") ]] || die "OUT.json parent directory does not exist: $(dirname -- "$OUT")"
[[ -n $LANE_DIR ]] && [[ ! -d $LANE_DIR ]] && die "--lane is not a directory: $LANE_DIR"

WORK=$(mktemp -d) || die "mktemp -d failed (TMPDIR honoured)"
cleanup() { [[ -n ${WORK:-} ]] && rm -rf -- "$WORK"; }
trap cleanup EXIT

printf '%s\0' "${CARGV[@]}" >"$WORK/argv" || die "cannot stage argv"

resolve_counter() {
  local cand=""
  if [[ -n $COUNTER_OVERRIDE ]]; then
    [[ -f $COUNTER_OVERRIDE ]] || die "counter is not a regular file: $COUNTER_OVERRIDE"
    printf '%s' "$COUNTER_OVERRIDE"
    return 0
  fi
  cand=${CARGV[0]}
  case $(basename -- "$cand") in
    python*|bash|sh|dash|node|nodejs|perl|ruby)
      local arg
      for arg in "${CARGV[@]:1}"; do
        if [[ -f $arg ]]; then
          printf '%s' "$arg"
          return 0
        fi
      done ;;
  esac
  if [[ -f $cand ]]; then
    printf '%s' "$cand"
    return 0
  fi
  return 0
}
COUNTER=$(resolve_counter) || exit 2
case "$COUNTER" in
  /*) ;;
  ?*) COUNTER=$(cd -- "$(dirname -- "$COUNTER")" && pwd)/$(basename -- "$COUNTER") ;;
esac

UTC_START=$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)
"${CARGV[@]}" >"$WORK/stdout" 2>"$WORK/stderr"
RC=$?
UTC_END=$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)

if [[ -n $LANE_DIR ]]; then
  LANE_DIR=$(cd -- "$LANE_DIR" && pwd) || die "cannot resolve --lane: $LANE_DIR"
fi

SR_OUT=$OUT SR_WORK=$WORK SR_RC=$RC SR_UTC_START=$UTC_START SR_UTC_END=$UTC_END \
SR_COUNTER=$COUNTER SR_LANE=$LANE_DIR SR_MAX=$MAX_CAPTURE \
python3 - <<'PY' || die "receipt assembly failed"
import hashlib, json, os, subprocess

work = os.environ["SR_WORK"]

def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()

argv = read_bytes(os.path.join(work, "argv")).split(b"\0")
if argv and argv[-1] == b"":
    argv.pop()
argv = [a.decode("utf-8", "surrogateescape") for a in argv]

stdout_b = read_bytes(os.path.join(work, "stdout"))
stderr_b = read_bytes(os.path.join(work, "stderr"))
cap = int(os.environ["SR_MAX"])

def embed(raw):
    text = raw[:cap].decode("utf-8", "replace")
    return text, len(raw) > cap

stdout_text, stdout_truncated = embed(stdout_b)
stderr_text, stderr_truncated = embed(stderr_b)

counter = os.environ.get("SR_COUNTER") or None
counter_sha = None
counter_bytes = None
if counter:
    counter = os.path.abspath(counter)
    data = read_bytes(counter)
    counter_sha = hashlib.sha256(data).hexdigest()
    counter_bytes = len(data)

lane = {}
lane_dir = os.environ.get("SR_LANE") or ""
if lane_dir:
    lane["lane_root"] = lane_dir
    try:
        proc = subprocess.run(["git", "-C", lane_dir, "rev-parse", "HEAD"],
                              capture_output=True, text=True)
        lane["lane_head"] = proc.stdout.strip() if proc.returncode == 0 else None
    except OSError:
        lane["lane_head"] = None

REV_FLAGS = {
    "--rev": "rev", "--freeze": "freeze", "--base": "base", "--at": "at",
    "--lane-rev": "lane_rev", "--root": "root", "--lane": "lane",
}
rev_args = {}
i = 0
while i < len(argv):
    token = argv[i]
    key = None
    value = None
    if token.startswith("--") and "=" in token:
        flag, value = token.split("=", 1)
        key = REV_FLAGS.get(flag)
    elif token in REV_FLAGS and i + 1 < len(argv):
        key = REV_FLAGS[token]
        value = argv[i + 1]
        i += 1
    if key is not None:
        if key in rev_args:
            if not isinstance(rev_args[key], list):
                rev_args[key] = [rev_args[key]]
            rev_args[key].append(value)
        else:
            rev_args[key] = value
    i += 1

parsed = None
stdout_json = False
if stdout_b.strip():
    try:
        parsed = json.loads(stdout_b.decode("utf-8"))
        stdout_json = True
    except (UnicodeDecodeError, json.JSONDecodeError):
        parsed = None

receipt = {
    "exit_code": int(os.environ["SR_RC"]),
    "argv": argv,
    "counter_sha256": counter_sha,
    "utc_start": os.environ["SR_UTC_START"],
    "utc_end": os.environ["SR_UTC_END"],
    "receipt_version": 1,
    "counter": counter,
    "counter_bytes": counter_bytes,
    "stdout_sha256": hashlib.sha256(stdout_b).hexdigest(),
    "stdout_bytes": len(stdout_b),
    "stderr_sha256": hashlib.sha256(stderr_b).hexdigest(),
    "stderr_bytes": len(stderr_b),
    "stdout": stdout_text,
    "stdout_truncated": stdout_truncated,
    "stderr": stderr_text,
    "stderr_truncated": stderr_truncated,
    "stdout_json": stdout_json,
    "lane_revision_arguments": rev_args,
    **lane,
    "counter_json_key_collisions": [],
}

reserved = set(receipt)
collisions = []
if isinstance(parsed, dict):
    for key, value in parsed.items():
        if key in reserved:
            collisions.append(key)
        else:
            receipt[key] = value
elif stdout_json:
    receipt["result"] = parsed
    receipt["result_kind"] = type(parsed).__name__
receipt["counter_json_key_collisions"] = collisions

out = os.environ["SR_OUT"]
tmp = "%s.tmp.%d" % (out, os.getpid())
try:
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1, ensure_ascii=True)
        f.write("\n")
    os.replace(tmp, out)
finally:
    if os.path.exists(tmp):
        os.unlink(tmp)
PY

printf '%s: exit=%d receipt=%s\n' "$PROG" "$RC" "$OUT" >&2
exit "$RC"
