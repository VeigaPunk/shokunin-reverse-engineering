#!/usr/bin/env bash
out="${@: -1}"
mkdir -p "$out/firmware.bin_extract/etc"
printf "motd\n" > "$out/firmware.bin_extract/etc/motd"
mkfifo "$out/firmware.bin_extract/fifo"
printf '{"data":{"operation":"extract_firmware","parameters":{"output_directory":"%s"}}}\n' "$out"
