import subprocess, sys
PY = sys.executable
cases = [
 ("d", "default returns bytes (non-encodable) for object()",
  'import io,json\ntry:\n    json.dump({"x": object()}, io.StringIO(), default=lambda o: b"x")\nexcept TypeError as e:\n    print("TypeError:", str(e)); raise SystemExit(11)\nexcept ValueError as e:\n    print("ValueError:", str(e).splitlines()[0]); raise SystemExit(12)\nprint("NO-ERROR")'),
 ("f", "default raises TypeError explicitly",
  'import io,json\ndef d(o):\n    raise TypeError("Cannot serialize object of %s" % type(o).__name__)\ntry:\n    json.dump({"x": object()}, io.StringIO(), default=d)\nexcept TypeError as e:\n    print("TypeError:", str(e)); raise SystemExit(1)\nprint("NO-ERROR")'),
 ("g", "default returns dict containing an unserializable object",
  'import io,json\ntry:\n    json.dump({"x": object()}, io.StringIO(), default=lambda o: {"k": object()})\nexcept TypeError as e:\n    print("TypeError:", str(e)); raise SystemExit(11)\nexcept ValueError as e:\n    print("ValueError:", str(e).splitlines()[0]); raise SystemExit(12)\nprint("NO-ERROR")'),
 ("h", "no default, object() value",
  'import io,json\ntry:\n    json.dump({"x": object()}, io.StringIO())\nexcept TypeError as e:\n    print("TypeError:", str(e)); raise SystemExit(1)\nprint("NO-ERROR")'),
]
for name, desc, code in cases:
    p = subprocess.run([PY, "-I", "-c", code], capture_output=True, text=True)
    print("=== probe %s: %s ===" % (name, desc))
    print("exit=%d" % p.returncode)
    print("stdout=%r" % p.stdout)
    print("stderr(last)=%r" % p.stderr.strip().splitlines()[-1] if p.stderr.strip() else "")
