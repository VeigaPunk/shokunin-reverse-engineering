#!/usr/bin/env bash
out="${@: -1}"
mkdir -p "$out/firmware.bin_extract/etc"
printf "motd\n" > "$out/firmware.bin_extract/etc/motd"
ln -s /fast/scratch/hyaku/kaidoku-r49/C1Sentinel/victim-target.txt "$out/after.json"
printf '{"data":{"operation":"extract_firmware","parameters":{"output_directory":"%s"}}}\n' "$out"
