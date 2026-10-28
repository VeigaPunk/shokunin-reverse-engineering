#!/usr/bin/env bash
out="${@: -1}"
mkdir -p "$out/firmware.bin_extract/etc"
printf "motd\n" > "$out/firmware.bin_extract/etc/motd"
ln -s /etc/hostname "$out/firmware.bin_extract/etc/hostlink"
ln -s ../../../../../../../../etc/passwd "$out/firmware.bin_extract/rel_passwd"
printf '{"data":{"operation":"extract_firmware","parameters":{"output_directory":"%s"}}}\n' "$out"
