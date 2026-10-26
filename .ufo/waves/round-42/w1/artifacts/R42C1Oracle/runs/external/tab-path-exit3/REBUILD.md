End-to-end red test for `path_not_representable` (development only, SquashFS
**v4**, `--dev-allow-v4`).  Image sha256 in `image.sha256`, 4096 bytes.

    mkdir -p src && cd src
    printf 'x' > "$(printf 'tab\tname.txt')"
    printf 'y' > plain.txt
    mksquashfs . ../img.sqfs -comp gzip -noappend -quiet

`sqfs3-oracle.py --dev-allow-v4 --json oracle-run.json img.sqfs` exits **3**
with `reason: path_not_representable`,
`cross_check.unrepresentable_paths: ["tab\tname.txt"]`, writes no tables, and
still records both producers' counts (`oracle-run.json` here).
