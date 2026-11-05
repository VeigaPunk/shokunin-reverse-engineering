import io, json, subprocess, sys, textwrap
PY = sys.executable
cases = [
 ("a", "no default, bytes value",
  'import io,json\ntry:\n    json.dump({"x": b"a"}, io.StringIO())\nexcept TypeError as e:\n    print("TypeError:", str(e)); raise SystemExit(1)\nprint("NO-ERROR")'),
 ("b", "default returns length dict for bytes",
  'import io,json\njson.dump({"x": b"a"}, io.StringIO(), default=lambda o: {"bytes": len(o)})\nprint("OK")'),
 ("c", "default returns str() of object",
  'import io,json\njson.dump({"x": object()}, io.StringIO(), default=lambda o: str(o))\nprint("OK")'),
]
for name, desc, code in cases:
    p = subprocess.run([PY, "-I", "-c", code], capture_output=True, text=True)
    print("=== probe %s: %s ===" % (name, desc))
    print("exit=%d" % p.returncode)
    print("stdout=%r" % p.stdout)
    print("stderr=%r" % p.stderr)
print("=== interpreter ===")
p = subprocess.run([PY, "-I", "-c", "import sys,platform;print(sys.version);print(platform.python_version())"], capture_output=True, text=True)
print("exit=%d\n%s" % (p.returncode, p.stdout))
