HOLDS — the WABT install matches the lesson’s recorded version, release archive, extraction location, and PATH status.

**Observed**
- Read the revision-scoped source with `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:corpus/lessons/round-20.md` (exit 0). At S, `corpus/lessons/round-20.md:88-92` records `wabt-1.0.42-linux-x64.tar.gz`, SHA-256 `84895407a6bbb80e918f33b16b2fb2206021c150b6bc9ff6f761263a745ab131`, size 4,761,911 bytes, extraction to `/home/vgpnk/.local/opt/wabt-1.0.42`, and “not on PATH.”
- Exact version probe (`"$f" --version` ran 11 times, each exit 0; loop exit 0):
  ```sh
  for f in /home/vgpnk/.local/opt/wabt-1.0.42/bin/*; do if [ -x "$f" ] && [ ! -d "$f" ]; then printf '\n$ %s --version\n' "$f"; "$f" --version; rc=$?; printf 'exit=%s\n' "$rc"; fi; done
  ```
  All 11 returned `1.0.42`: `spectest-interp`, `wasm-interp`, `wasm-objdump`, `wasm-stats`, `wasm-strip`, `wasm-validate`, `wasm2c`, `wasm2wat`, `wast2json`, `wat-desugar`, `wat2wasm`.
- Downloaded the official archive and checksum into `mktemp` scratch `/tmp/tmp.WtuHuiDdUP`; `curl` for each returned exit 0:
  ```sh
  curl -fLsS -o "$tmpdir/$archive" "$base/$archive"  # base=https://github.com/WebAssembly/wabt/releases/download/1.0.42; archive=wabt-1.0.42-linux-x64.tar.gz
  curl -fLsS -o "$tmpdir/$checksum" "$base/$checksum"  # checksum=wabt-1.0.42-linux-x64.tar.gz.sha256
  (cd "$tmpdir" && sha256sum -c "$checksum")  # exit 0: wabt-1.0.42-linux-x64.tar.gz: OK
  wc -c "$tmpdir/$archive"  # exit 0: 4761911
  tar -xzf "$tmpdir/$archive" -C "$tmpdir"  # exit 0
  ```
  Comparison command (with `root="$tmpdir/wabt-1.0.42/bin"`; `cmp -s` succeeded for each file; loop exit 0):
  ```sh
  diff_rc=0; for f in /home/vgpnk/.local/opt/wabt-1.0.42/bin/*; do if [ -x "$f" ] && [ ! -d "$f" ]; then name=${f##*/}; if cmp -s "$f" "$root/$name"; then printf 'MATCH %s\n' "$name"; else printf 'MISMATCH %s\n' "$name"; diff_rc=1; fi; fi; done; printf 'installed-bin comparison exit=%s\n' "$diff_rc"; exit "$diff_rc"
  ```
  All 11 comparisons reported `MATCH`. Scratch was removed by the command’s EXIT trap.
- PATH command:
  ```sh
  case ":$PATH:" in *:/home/vgpnk/.local/opt/wabt-1.0.42/bin:*) printf 'install-dir-on-PATH=yes\n'; path_rc=1 ;; *) printf 'install-dir-on-PATH=no\n'; path_rc=0 ;; esac; for f in /home/vgpnk/.local/opt/wabt-1.0.42/bin/*; do if [ -x "$f" ] && [ ! -d "$f" ]; then n=${f##*/}; if command -v "$n" >/dev/null 2>&1; then printf 'command-v %s=%s\n' "$n" "$(command -v "$n")"; else printf 'command-v %s=NOT_FOUND\n' "$n"; fi; fi; done; printf 'check exit=%s\n' "$path_rc"; exit "$path_rc"
  ```
  It reported `install-dir-on-PATH=no`, `NOT_FOUND` for all 11 names, exit 0. This is an observation of the probe shell’s PATH.

**Inference**: For the requested checks, the installed executables are byte-identical to the executables in the archive whose digest matches the release checksum asset; the lesson’s WABT install record holds. No release-signature validation was performed; archive integrity was checked against the GitHub release `.sha256` asset as requested.