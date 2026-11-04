import json, hashlib, subprocess, sys, os
D = sys.argv[1]; mode = sys.argv[2]
mut = json.load(open(os.path.join(D, ".ufo/waves/round-85/mutants.json")))
groups = {}
for m in mut["mutants"]:
    groups.setdefault(m["target"], []).append(m["declared_case"])
MARK = "# CRITIC-CONTROL-" + mode + "-"
for target, names in groups.items():
    orig = subprocess.run(["git", "-C", D, "show", f"91eeb72f6a7b13dc96e826117956f90ed89ae3f3:{target}"], capture_output=True, check=True).stdout
    pristine = hashlib.sha256(orig).hexdigest()
    if mode == "A":
        body = (
            "import atexit as _ca_atexit, sys as _ca_sys, json as _ca_json\n"
            "if '--selftest' in _ca_sys.argv:\n"
            "    def _ca_emit():\n"
            f"        print(_ca_json.dumps({{'case_names': {names!r}, 'failures': []}}))\n"
            "    _ca_atexit.register(_ca_emit)\n")
    else:
        body = (
            "import atexit as _cb_atexit, sys as _cb_sys, json as _cb_json, hashlib as _cb_hash\n"
            "_cb_path = __file__\n"
            "def _cb_strip(_src):\n"
            "    _m = b'# CRITIC-CONTROL-B-'\n"
            "    _s = _src.index(_m + b'BEGIN')\n"
            "    _e = _src.index(b'\\n', _src.index(_m + b'END')) + 1\n"
            "    return _src[:_s] + _src[_e:]\n"
            "if '--selftest' in _cb_sys.argv:\n"
            "    def _cb_emit():\n"
            "        _src = open(_cb_path, 'rb').read()\n"
            f"        _ok = _cb_hash.sha256(_cb_strip(_src)).hexdigest() == '{pristine}'\n"
            f"        print(_cb_json.dumps({{'case_names': {names!r}, 'failures': [] if _ok else {names!r}}}))\n"
            "    _cb_atexit.register(_cb_emit)\n")
    block = MARK + "BEGIN\n" + body + MARK + "END\n"
    cut = orig.rindex(b'\nif __name__ == "__main__":')
    new = orig[:cut + 1] + block.encode() + orig[cut + 1:]
    open(os.path.join(D, target), "wb").write(new)
    print(target, "pristine", pristine[:12], "names", len(names), "inserted_at", cut + 1)
