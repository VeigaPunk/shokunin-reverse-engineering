# Carrier identity support

The round-2 entry identifies `/home/vgpnk/.cache/uv/archive-v0/M1E0QXq07p7Gx3Fp/setuptools/cli-64.exe` with SHA-256 `bbb3de5707629e6a60a0c238cd477b28f07f0066982fda953fa6fcec39073a4a` (`corpus/knowledge/2026-10-13-r2-pe-e2e-proof.md:10-15`). That canonical path was absent when checked for this leg:

```text
$ sha256sum /home/vgpnk/.cache/uv/archive-v0/M1E0QXq07p7Gx3Fp/setuptools/cli-64.exe
sha256sum: /home/vgpnk/.cache/uv/archive-v0/M1E0QXq07p7Gx3Fp/setuptools/cli-64.exe: No such file or directory (os error 2)
exit=1
```

The byte-identical available copy used by every successful Rizin call:

```text
$ stat -c '%n %s bytes' /home/vgpnk/.local/share/uv/tools/unblob/lib/python3.11/site-packages/setuptools/cli-64.exe
/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.11/site-packages/setuptools/cli-64.exe 14336 bytes
$ sha256sum /home/vgpnk/.local/share/uv/tools/unblob/lib/python3.11/site-packages/setuptools/cli-64.exe
bbb3de5707629e6a60a0c238cd477b28f07f0066982fda953fa6fcec39073a4a  /home/vgpnk/.local/share/uv/tools/unblob/lib/python3.11/site-packages/setuptools/cli-64.exe
$ file /home/vgpnk/.local/share/uv/tools/unblob/lib/python3.11/site-packages/setuptools/cli-64.exe
PE32+ executable for MS Windows 6.00 (console), x86-64, 6 sections
```

Local Rizin command resolution/version support (the REA Evidence provider itself reports `version: null`):

```text
$ command -v rizin
/usr/bin/rizin
$ /usr/bin/rizin -v
rizin 0.8.2 @ linux-x86-64
$ sha256sum /usr/bin/rizin
556fceb907891f769689782cf149691e1a749997b70f24ae95bc323688a15702  /usr/bin/rizin
```

These are host identity observations, not proof that REA bound the Rizin executable by digest; successful Evidence records the provider executable name `rizin` and reports the PE subject SHA-256 before and after each run.
