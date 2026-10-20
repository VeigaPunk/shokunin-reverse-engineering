PARTIAL

# EmulatorMutation — bounded author-side mutation probe

**Observation:** all three mutants were **killed by `--selftest`** and changed the predictions for **s1246-swiss-nethttp** and **aether**. The stronger expectation that every requested carrier's prediction changes does **not** hold: **s1250-swiss-nethttp stayed silent under all three mutants**. This is a probe-local result, not a judgment of C3 or the round.

Axes: **calibration** (pristine/mutated/restored and explicit negative results), **operability** (bounded commands, exits, exact restoration), **depth** (three independent behavior-bearing mutations across all three requested carriers). No lane source was edited; the sole persistent lane write is this report. No tool installs/updates, REA/Ghidra runs, carrier execution, subagent dispatch, or other mission runtime invocation occurred. Python used: **3.14.8**, always `python3 -I -B`.

## Revision and exact mutation anchors

Frozen source: `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. Citation revision: `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. Both revisions' `.ufo/waves/round-18/tools/swiss-misread.py` resolve to Git blob `31430871691bd0fcf7bf194a299eaf127cb8639a`; frozen bytes are **75,260 bytes**, SHA-256 `14924bd6999b2cef4e1d217fa01d5fbb959ec8bb6e58b12959d4f4907f0e3b60`. Thus the frozen copy and requested revision's cited source are byte-identical.

All following path:line anchors refer to **REV b2aad08ceeee8dd125ce0d316056d8bd766c7f94**, inspected with `git show REV:path`:

| Mutant | Minimal actual edit | Source anchor | Expected detector (inference before comparison) |
|---|---|---|---|
| bound112 | H1 map-only bound size forced to 112 instead of snapshot-derived 88; H0 and other kinds unchanged | `.ufo/waves/round-18/tools/swiss-misread.py:720-732` (edit at 729) | H1 uncommon read advances 24 bytes; slot-40 selftest and diagnostic-carrier prediction comparison should detect it. |
| no_pkg_follow | Replace recursive `resolve_name_off(...)` call with `return` | `.ufo/waves/round-18/tools/swiss-misread.py:831-837` (edit at 836-837) | Missing recursive package-name read should eliminate the bad downstream read; same detectors. |
| name_flag | `if flags & 0x04:` → `if flags == 0x04:` in name decoding only; fixture writer untouched | `.ufo/waves/round-18/tools/swiss-misread.py:792-803` (edit at 801) | Combined flag values no longer populate `pkg_path`; same detectors. |

The selftest fixture deliberately uses combined/junk flag bits and an N1→N2 name chain at `.ufo/waves/round-18/tools/swiss-misread.py:1672-1686`; the first failing assertion is the real `slot40-h1-fail` check at `.ufo/waves/round-18/tools/swiss-misread.py:1756-1769`. Carrier CLI exit 0 means JSON emission, not a successful semantic comparison (`.ufo/waves/round-18/tools/swiss-misread.py:39-40`).

Exact edit-tool operations used on the three independent scratch copies (each started with pristine bytes):

```text
*** Begin Patch
[/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo/mutation-probe/bound112.py#43A1]
PUT 729.=729:
+        return 112 if kind == 21 and self.hypothesis == "h1" else self.layout.size(self.bound_class(kind))
[/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo/mutation-probe/no_pkg_follow.py#43A1]
PUT 836.=837:
+        return
[/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo/mutation-probe/name_flag.py#43A1]
PUT 801.=801:
+        if flags == 0x04:
*** End Patch
```

## Actual detector outputs

**Observation:** pristine selftest exited **0**, stdout exactly `"SELFTEST: CLEAN cases=15\n"`. Each mutated selftest exited **1**, stdout exactly `"SELFTEST: FAILED slot40-h1-fail: \n"` (space before newline). Each restored selftest exited **0** with the original stdout. Every stderr was empty. None timed out. The three mutants are therefore **killed**, not inconclusive baseline failures.

The carrier detector compares every `predicted_*` field plus `diagnostic` against pristine JSON, using strict in-memory equality; it does not mistake the carrier CLI's exit 0 for a mutant kill. Source fields: `.ufo/waves/round-18/tools/swiss-misread.py:1519-1531`. Here is the observed H1 projection (all nine mutated carrier invocations exited **0**):

| Carrier | Pristine / all restored: failure; kind; EOF pairs; invalid-index reads; diagnostic | Each of the three mutants | Per-carrier detector verdict |
|---|---|---|---|
| s1246-swiss-nethttp | `true; invalid_index; []; [22386945]; true` | `false; none; []; []; false` | **killed** (prediction delta) |
| s1250-swiss-nethttp | `false; none; []; []; false` | `false; none; []; []; false` | **survived** this carrier's prediction detector |
| aether | `true; past_eof; [[17645861,111938854]]; []; true` | `false; none; []; []; false` | **killed** (prediction delta) |

H0 prediction fields stayed `false / none / [] / []` on all carriers/stages. Map/uncommon counts remained 38/2 for each nethttp carrier and 152/7 for aether.

**Observation, not an inferred execution failure:** for s1250, bound112 changed only top-level `per_type` data. In its two uncommon maps, H1 uncommon addresses changed **5815224→5815248** and **5825752→5825776**, with package offsets **40→21008** and **40→7373**, respectively; both outcomes stayed `silent`. The other two mutations left **the entire s1250 stdout byte-identical**. This distinguishes a structural change from a change in a declared prediction. The bound112 mutation deliberately changes the reader, not the separate `layout.ghidra_size` metadata.

**Inference:** this s1250 byte build is not a discriminating detector for these defects. Its survival is a coverage limitation, not permission to change the contract or a claim that the Swiss misread cannot occur. The aggregate suite still kills all three mutants. The source explicitly separates map-path failure booleans from its approximate full walk at `.ufo/waves/round-18/tools/swiss-misread.py:1461-1466`; no full-walk fidelity claim is made here.

## Source/input custody and restoration

Scratch clone: `/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo`; origin removed before creating any subjects. Source stdout from the frozen `git show` was copied with the write tool into `pristine.py` and each mutant file. After probing, the three mutant files were overwritten with those exact saved frozen bytes, then **the same four detectors were rerun for each restored file**.

| File | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|---|
| bound112.py | B | `36c2bcaef359b8521be03696265488d1d9cfec724479c285a758115cf709c070` | B |
| no_pkg_follow.py | B | `2889b5e6960a2a304f7c70be597597b8d6f465213232cfff42deddc120e371af` | B |
| name_flag.py | B | `391892cb84958679958fd5dc276f25c726dba7302e27dd3cd5473cb86ceeac5a` | B |

**B = `14924bd6999b2cef4e1d217fa01d5fbb959ec8bb6e58b12959d4f4907f0e3b60`**. Separate `sha256sum` invocations observed the pre-mutation, mutated, and restored hashes. The untouched pristine copy also had B before/after. All **12 restored detector runs** exited 0, and each stdout **and** stderr matched the corresponding pristine run byte-for-byte. This is exact source restoration plus behavioral restoration, not only an edited-back approximation.

Input bytes were hashed before and after; all five hashes stayed unchanged:

| Input | SHA-256 |
|---|---|
| /usr/bin/aether | `06c91f55df4117e58b478242df366145148b956c41c11a46cd1800f76178006e` |
| s1246-swiss-nethttp | `5c9faf239ed2c68304666992a8d2c1dc40c36e90f8021c62fef4cc4453f201b6` |
| s1250-swiss-nethttp | `bd12f6783479d1f87c83a7a704e445533b4b5d75c3501416df34e9dd41a6eed4` |
| go1.24.0.json | `aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571` |
| go1.25.0.json | `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252` |

Full stdout fingerprints (not only the projections):

| Detector | Pristine stdout SHA-256 | Restoration observation |
|---|---|---|
| selftest | `130df05fd53ed4556fc5700e9a4eaff8e524dda6d61aebcc989ff070da5ea43c` | all three restored stdout byte-identical |
| s1246-swiss-nethttp | `19579c1d998122f40fcf21a805628c80afc6580c1cf4a42fe0a088cf89c5b2c4` | all three restored stdout byte-identical |
| s1250-swiss-nethttp | `7764738f92ffe6481aa56f9dbabf947ee0c88272bd2c7813c037a0ddf65ba172` | all three restored stdout byte-identical |
| aether | `b231272377a89254d355548ca76aaf2e40488602a97fccd8c44571203160a237` | all three restored stdout byte-identical |

| Mutant | Carrier | Prediction fields | Full stdout vs pristine | Mutated stdout SHA-256 |
|---|---|---|---|---|
| bound112 | s1246-swiss-nethttp | changed | changed | `9908d2deb7b03a83377976223bd5ebda981ce4b2e519fe7dae6fe3227fd4c0ca` |
| bound112 | s1250-swiss-nethttp | unchanged | changed | `406ec751c8d3cbae7c6e4e4908fcd05965906a70dccf430e12badf7de91e8a8c` |
| bound112 | aether | changed | changed | `529a1e52632f1def3bbdba50000d17ba92165ec9189591e10e9830c91fab846b` |
| no_pkg_follow | s1246-swiss-nethttp | changed | changed | `39d78572b5a167ca0f87d9d1c112248b55ccd91246631cb269ad89d283d7c0ea` |
| no_pkg_follow | s1250-swiss-nethttp | unchanged | byte-identical | `7764738f92ffe6481aa56f9dbabf947ee0c88272bd2c7813c037a0ddf65ba172` |
| no_pkg_follow | aether | changed | changed | `a9cc0c67dfe001c6c47d7e7cd9e056deccbdce988fb203d22d11ecebee5fa364` |
| name_flag | s1246-swiss-nethttp | changed | changed | `39d78572b5a167ca0f87d9d1c112248b55ccd91246631cb269ad89d283d7c0ea` |
| name_flag | s1250-swiss-nethttp | unchanged | byte-identical | `7764738f92ffe6481aa56f9dbabf947ee0c88272bd2c7813c037a0ddf65ba172` |
| name_flag | aether | changed | changed | `a9cc0c67dfe001c6c47d7e7cd9e056deccbdce988fb203d22d11ecebee5fa364` |

## Reproducing commands and observed exits

Directory abbreviations below expand only constant path prefixes; the detector argv, environment addition, bound, stage, and exit are preserved. The files currently contain **restored bytes**: reapply the exact mutant edit above before repeating its mutated-stage commands, then restore B before the restored-stage commands. Definitions for copy/paste:

```sh
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
P='/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo/mutation-probe'
G='/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang'
C='/home/vgpnk/.local/share/kaidoku-r18/carriers'
```

Setup/read-only source commands actually used:

```sh
# cwd=$L; exit=0
 git ls-tree -r --name-only eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 .ufo/waves/round-18
# cwd=$L; exit=0; output: the same 31430871691bd0fcf7bf194a299eaf127cb8639a twice
 git rev-parse eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:.ufo/waves/round-18/tools/swiss-misread.py b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/tools/swiss-misread.py
# cwd=$L; exit=0
 git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/tools/swiss-misread.py
# cwd=/tmp; exit=0; stdout: /tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9
 mktemp -d /tmp/kaidoku-r18-EmulatorMutation.XXXXXXXX
# cwd=/tmp; both commands succeeded; compound exit=0; no stdout/stderr
 git clone --no-checkout --shared --quiet "$L" '/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo' && git -C '/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo' remote remove origin
# cwd=/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo; exit=0; stdout retained in memory, then copied through write tool
 git show eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:.ufo/waves/round-18/tools/swiss-misread.py
# cwd=/tmp; exit=0; stdout: Python 3.14.8
 python3 -I -B --version
# cwd=/tmp; exit=0; initial input hashes listed above
 sha256sum /usr/bin/aether "$C/s1246-swiss-nethttp" "$C/s1250-swiss-nethttp" "$G/go1.24.0.json" "$G/go1.25.0.json"
# cwd=/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo; exit=0; pre-mutation hashes: all B
 sha256sum "$P/pristine.py" "$P/bound112.py" "$P/no_pkg_follow.py" "$P/name_flag.py"
# cwd=/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo; exit=0; mutated hashes listed above
 sha256sum "$P/bound112.py" "$P/no_pkg_follow.py" "$P/name_flag.py"
# cwd=/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo; exit=0; restored hashes all B; input hashes unchanged
 sha256sum "$P/pristine.py" "$P/bound112.py" "$P/no_pkg_follow.py" "$P/name_flag.py" /usr/bin/aether "$C/s1246-swiss-nethttp" "$C/s1250-swiss-nethttp" "$G/go1.24.0.json" "$G/go1.25.0.json"
```

All detector commands used cwd `/tmp/kaidoku-r18-EmulatorMutation.ZZE4E9S9/repo`. Four pristine commands were run concurrently; all twelve mutant commands were run concurrently; only after completion and exact restoration were the twelve restored commands run concurrently. All temporary selftest files were directed inside the clone with TMPDIR and removed by the selftest.

### pristine

```sh
# pristine; pristine; selftest; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/pristine.py" --golang-root "$G" --selftest
# pristine; pristine; s1246-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/pristine.py" --golang-root "$G" --carrier "$C/s1246-swiss-nethttp"
# pristine; pristine; s1250-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/pristine.py" --golang-root "$G" --carrier "$C/s1250-swiss-nethttp"
# pristine; pristine; aether; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/pristine.py" --golang-root "$G" --carrier /usr/bin/aether
```

### mutated

```sh
# mutated; bound112; selftest; exit=1
env TMPDIR="$P" timeout 120s python3 -I -B "$P/bound112.py" --golang-root "$G" --selftest
# mutated; bound112; s1246-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/bound112.py" --golang-root "$G" --carrier "$C/s1246-swiss-nethttp"
# mutated; bound112; s1250-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/bound112.py" --golang-root "$G" --carrier "$C/s1250-swiss-nethttp"
# mutated; bound112; aether; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/bound112.py" --golang-root "$G" --carrier /usr/bin/aether
# mutated; no_pkg_follow; selftest; exit=1
env TMPDIR="$P" timeout 120s python3 -I -B "$P/no_pkg_follow.py" --golang-root "$G" --selftest
# mutated; no_pkg_follow; s1246-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/no_pkg_follow.py" --golang-root "$G" --carrier "$C/s1246-swiss-nethttp"
# mutated; no_pkg_follow; s1250-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/no_pkg_follow.py" --golang-root "$G" --carrier "$C/s1250-swiss-nethttp"
# mutated; no_pkg_follow; aether; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/no_pkg_follow.py" --golang-root "$G" --carrier /usr/bin/aether
# mutated; name_flag; selftest; exit=1
env TMPDIR="$P" timeout 120s python3 -I -B "$P/name_flag.py" --golang-root "$G" --selftest
# mutated; name_flag; s1246-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/name_flag.py" --golang-root "$G" --carrier "$C/s1246-swiss-nethttp"
# mutated; name_flag; s1250-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/name_flag.py" --golang-root "$G" --carrier "$C/s1250-swiss-nethttp"
# mutated; name_flag; aether; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/name_flag.py" --golang-root "$G" --carrier /usr/bin/aether
```

### restored

```sh
# restored; bound112; selftest; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/bound112.py" --golang-root "$G" --selftest
# restored; bound112; s1246-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/bound112.py" --golang-root "$G" --carrier "$C/s1246-swiss-nethttp"
# restored; bound112; s1250-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/bound112.py" --golang-root "$G" --carrier "$C/s1250-swiss-nethttp"
# restored; bound112; aether; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/bound112.py" --golang-root "$G" --carrier /usr/bin/aether
# restored; no_pkg_follow; selftest; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/no_pkg_follow.py" --golang-root "$G" --selftest
# restored; no_pkg_follow; s1246-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/no_pkg_follow.py" --golang-root "$G" --carrier "$C/s1246-swiss-nethttp"
# restored; no_pkg_follow; s1250-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/no_pkg_follow.py" --golang-root "$G" --carrier "$C/s1250-swiss-nethttp"
# restored; no_pkg_follow; aether; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/no_pkg_follow.py" --golang-root "$G" --carrier /usr/bin/aether
# restored; name_flag; selftest; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/name_flag.py" --golang-root "$G" --selftest
# restored; name_flag; s1246-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/name_flag.py" --golang-root "$G" --carrier "$C/s1246-swiss-nethttp"
# restored; name_flag; s1250-swiss-nethttp; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/name_flag.py" --golang-root "$G" --carrier "$C/s1250-swiss-nethttp"
# restored; name_flag; aether; exit=0
env TMPDIR="$P" timeout 120s python3 -I -B "$P/name_flag.py" --golang-root "$G" --carrier /usr/bin/aether
```

## Scope conclusion

**Observation:** 3/3 mutants killed by selftest; 6/9 carrier prediction comparisons changed; 3/9 survived (all s1250); no inconclusive runs; 12/12 restored runs exactly reproduced pristine output. **Inference:** the tested suite has useful sensitivity to these three local defects, but a universal per-carrier sensitivity statement is unsupported. No repair, integration, or contract change is proposed by this mutation seat.
