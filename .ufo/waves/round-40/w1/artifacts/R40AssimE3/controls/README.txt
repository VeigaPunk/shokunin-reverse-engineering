NEGATIVE / POSITIVE CONTROLS for the layout test in probe-avm-layout.py. Not carriers.

control-standard-be.sqsh            gen-squashfs.py <tree> out --endian be  --comp gzip  (373 B)
control-avm-mode.sqsh               gen-squashfs.py <tree> out --endian avm --comp gzip  (373 B)
control-standard-be-markerpatched.sqsh  control-standard-be.sqsh with bytes 8..12 := BE(bytes_used);
                                    sha256 equal to control-avm-mode.sqsh, 0 differing bytes
control-avm-markerstripped.sqsh     a COPY of the round-11 avm-be.squashfs with bytes 8..12 := 1;
                                    the canonical image is /home/vgpnk/Projects/shokuknow/lanes/kaidoku/
                                    round11/work/avm-be.squashfs, sha256 c7f74691…d32

Rebuild commands (TMPDIR must be set; the generator is deterministic):
  mkdir -p tree/bin tree/docs; printf 'hello\n' > tree/bin/run; printf 'a\n' > tree/docs/a.txt
  python3 tools/round-39/gen-squashfs.py tree out.sqsh --endian be  --comp gzip
  python3 tools/round-39/gen-squashfs.py tree out.sqsh --endian avm --comp gzip
  python3 -c "import struct;a=bytearray(open('out-be.sqsh','rb').read());a[8:12]=struct.pack('>I',int.from_bytes(a[40:48],'big'));open('p.sqsh','wb').write(a)"
