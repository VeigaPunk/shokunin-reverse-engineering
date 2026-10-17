## CLAIM
Located `/usr/bin/rg` (ripgrep) as a Rust ELF carrier candidate for L4.

## METHOD
Read the repo guidance. Ran read-only `find` for the named candidates, then `file` and `sha256sum` on the found binaries. No binary was executed; no host/config changes were made. The only write is this seat report.

## FINDINGS
`find /usr/bin /bin /usr/local/bin /home/vgpnk/.cargo/bin -type f \( -name rg -o -name fd -o -name alacritty -o -name hyprland \) -print` returned `/usr/bin/alacritty`, `/usr/bin/rg`, and `/usr/bin/fd` (the command exited 1 because at least one search root is absent).

`file /usr/bin/rg`: “ELF 64-bit LSB pie executable, x86-64 … dynamically linked … BuildID[sha1]=9c4ccf92551b9f21124cc3fb265ea4a60a11e56f, stripped”. `sha256sum /usr/bin/rg`: `d006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42`.

The path identifies the ripgrep executable, a Rust implementation; file/hash evidence anchors the discovered carrier's ELF type and exact bytes.

## THREATS
The permitted discovery commands establish a regular ELF and hash, but do not independently expose compiler-language provenance. No claim is made that L4 was run or that this surface is held.

## VERDICT
CLEAN