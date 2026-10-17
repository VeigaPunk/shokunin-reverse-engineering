## CLAIM
Found an Electron application executable under `/usr` suitable as a carrier for the round battery.

## METHOD
Read-only search: `find /opt /usr \( -type f -o -type l \) \( -iname 'obsidian' -o -iname 'typora' -o -iname 'signal' -o -iname 'signal-desktop' -o -iname '*.appimage' \) -print`.
Output paths: `/usr/share/typora/Typora`, `/usr/bin/obsidian`, `/usr/bin/signal-desktop`, `/usr/bin/typora`, `/usr/lib/signal-desktop/signal-desktop`.
Validated candidates with `file -L`, `stat -L`, `sha256sum`; package markers located with `find /usr/lib/signal-desktop /usr/share/typora -maxdepth 4 -type f \( -iname 'app.asar' -o -iname 'electron.asar' -o -iname 'chrome-sandbox' -o -iname 'icudtl.dat' \) -print`.

## FINDINGS
- `/usr/lib/signal-desktop/signal-desktop`: executable ELF 64-bit x86-64, mode 755, 223,513,856 bytes; SHA-256 `f7a9b441e825b388260430f9edd9a2f94fd50be497bf66192a16aeab87afc85a`.
- `/usr/share/typora/Typora`: executable ELF 64-bit x86-64, mode 755, 210,091,224 bytes; SHA-256 `d9635cd36829ee40e14ab1662ea0496c89e1b91b198392c7a311df4df8b7767a`.
- Both package trees contain `resources/app.asar`, `chrome-sandbox`, and `icudtl.dat`.
- `/usr/bin/obsidian` is a shell-script launcher, not the application ELF (SHA-256 `0df6f2b28187a84917eaf33e089abe980a407fd4b195d69eab1f2a70ad2234ca`).

## THREATS
`find` reported `find: ‘/opt/containerd’: Permission denied` and exited 1, so `/opt` discovery was not exhaustive. The two confirmed `/usr` candidates satisfy the carrier search. No application was run.

## VERDICT
CLEAN — Signal and Typora executable carriers found with hashes and Electron package markers.
