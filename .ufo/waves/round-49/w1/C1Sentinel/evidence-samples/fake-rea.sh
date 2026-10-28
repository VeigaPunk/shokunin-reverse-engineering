#!/usr/bin/env bash
# stub REA: prints a receipt-shaped envelope and writes a tree into the last argv (output root)
out="${@: -1}"
mkdir -p "$out/firmware.bin_extract/etc"
printf 'motd\n' > "$out/firmware.bin_extract/etc/motd"
printf '{"data":{"operation":"extract_firmware","parameters":{"output_directory":"%s"}}}\n' "$out"
