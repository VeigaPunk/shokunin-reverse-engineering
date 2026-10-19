<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/12-archives-pkgs.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# kaidoku r1 — archives/packages surface survey (READ ONLY)

Host: Arch-flavored Linux (pacman 7.x era, `omarchy` overlay repo). All commands read-only; nothing installed, extracted to disk, or modified.

## Candidate: pacman ownership oracle — `/usr/bin/jq` is owned by `jq 1.8.2-1`
- claim: Every file under pacman-managed prefixes resolves to exactly one owning package via `pacman -Qo`; `/usr/bin/jq` resolves to `jq 1.8.2-1`, and `pacman -Ql jq` enumerates its full 25-file footprint (binary, `libjq.so.1.0.4`, headers, pkgconfig, docs, man page).
- source: `pacman -Qo /usr/bin/jq` → `/usr/bin/jq is owned by jq 1.8.2-1`; `pacman -Ql jq | head`
- verify: `pacman -Qo /usr/bin/jq && pacman -Ql jq | wc -l`
- verified-at: 2026-10-13
- suggested: admit — first-mile attribution for any shipped binary; the oracle works before any REA.

## Candidate: `.pkg.tar.zst` is a self-describing provenance container readable with stock tar+file+zstd
- claim: A pacman package archive (`acl-2.4.0-1-x86_64.pkg.tar.zst`, 106 members) is a Zstandard tar (`file` → "Zstandard compressed data (v0.8+)") carrying three dot-prefixed metadata members — `.BUILDINFO` (buildtool `devtools 1:1.5.1`, PKGBUILD sha256 `187dc04a…`, buildenv/options incl. `strip`, `debug`), `.MTREE` (gzip-compressed mtree with per-file `sha256digest`), `.PKGINFO` (name/ver/deps/packager) — all extractable to stdout via `tar -xOf` with no disk extraction.
- source: `file`, `tar -tf` (head + `wc -l` = 106), `tar -xOf … .PKGINFO`/`.BUILDINFO`/`.MTREE | zcat`
- verify: `tar -tf /var/cache/pacman/pkg/acl-2.4.0-1-x86_64.pkg.tar.zst | grep '^\.' ; tar -xOf /var/cache/pacman/pkg/acl-2.4.0-1-x86_64.pkg.tar.zst .BUILDINFO`
- verified-at: 2026-10-13
- suggested: admit — build provenance and per-file digests are available pre-REA; REA only adds semantics, not provenance.

## Candidate: cached archive set is a signed, integrity-checkable corpus (1556 pkgs, 8.6 GiB, 100% sig coverage)
- claim: `/var/cache/pacman/pkg/` holds 1556 `.pkg.tar.zst` files and 1556 matching `.sig` files (1:1 coverage); a sampled `.sig` is a 119-byte detached EDDSA signature that verifies `Good signature … [full]` under the pacman keyring (`gpg --homedir /etc/pacman.d/gnupg --verify`), and `zstd -t` passes the archive.
- source: `ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l` (=1556), `ls *.sig | wc -l` (=1556), `du -sh` (8.6G), `gpg --homedir /etc/pacman.d/gnupg --verify acl-…sig acl-…zst`
- verify: `cd /var/cache/pacman/pkg && for f in *.pkg.tar.zst; do [ -f "$f.sig" ] || echo "unsigned: $f"; done | head`
- verified-at: 2026-10-13
- suggested: admit — a local, signed ground-truth corpus already exists on-disk; REA targets can be sourced and authenticated without network.

## Candidate: installed files verify byte-for-byte against the shipped artifact — tampering is detectable pre-REA
- claim: `sha256sum /usr/bin/jq` equals `tar -xOf jq-1.8.2-1-x86_64.pkg.tar.zst usr/bin/jq | sha256sum` (both `e8156675…7806`), and `pacman -Qkk jq` reports `25 total files, 0 altered files`; `.MTREE` in-archive and `/var/lib/pacman/local/jq-1.8.2-1/mtree` hold the same digests, so any on-disk deviation from the signed artifact is a one-command check, not an REA problem.
- source: byte-compare of archive member vs installed file; `pacman -Qkk jq`; `ls /var/lib/pacman/local/jq-1.8.2-1/` → `desc files mtree`
- verify: `tar -xOf /var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst usr/bin/jq | sha256sum; sha256sum /usr/bin/jq; pacman -Qkk jq`
- verified-at: 2026-10-13
- suggested: admit — establishes the REA baseline rule: verify-then-disassemble; only divergent or unowned bytes warrant lifting.

## Candidate: unowned shadow binary `~/.local/bin/jq` — a live REA target surfaced by the survey
- claim: `pacman -Qo /home/vgpnk/.local/bin/jq` → `error: No package owns …`; it is a statically linked, stripped ELF (sha256 `b1c22172…70f`) that reports the identical version string `jq-1.8.2` as the packaged dynamically linked 30 KiB `/usr/bin/jq` (sha256 `e8156675…`), and PATH order (`~/.local/bin` first) means every bare `jq` invocation runs the unowned binary.
- source: `pacman -Qo` error on the path; `file`/`sha256sum`/`--version` on both binaries; `which jq` → `/home/vgpnk/.local/bin/jq`
- verify: `pacman -Qo ~/.local/bin/jq; file ~/.local/bin/jq /usr/bin/jq; sha256sum ~/.local/bin/jq /usr/bin/jq`
- verified-at: 2026-10-13
- suggested: admit — highest-value finding of the pass: an unowned, statically-linked impostor of a signed package binary, exactly the class REA exists for.

## Candidate: `pacman -Qm` exposes a non-repo shipped surface (14 foreign packages)
- claim: `pacman -Qm` lists 14 packages tracked by the local DB but absent from all sync repos — 12 `elephant-*` 2.21.0-1 plus `omarchy-walker 1.0.0-2` — installed via `pacman -U`/AUR-style flows; their only archive copies (if any) live in the local cache.
- source: `pacman -Qm` (14 rows)
- verify: `pacman -Qm; ls /var/cache/pacman/pkg/ | grep -E 'elephant|walker'`
- verified-at: 2026-10-13
- suggested: admit — foreign packages lack upstream signed provenance; they are shipped artifacts whose nearest ground truth is the cached archive itself.

## Candidate: sync-DB drift — `offline.db` has no configured repo; `omarchy.db` uses a different compressor
- claim: `/var/lib/pacman/sync/` contains five DBs (`core`, `extra`, `multilib`, `offline`, `omarchy`) but `pacman.conf` configures only four repos (`[core] [extra] [multilib] [omarchy]`) — `offline.db` is an orphaned sync artifact; additionally official DBs are gzip tars while `omarchy.db` is zstd, marking a third-party provenance boundary.
- source: `file /var/lib/pacman/sync/*.db`; `grep -E '^\[' /etc/pacman.conf`
- verify: `ls /var/lib/pacman/sync/; grep -E '^\[' /etc/pacman.conf`
- verified-at: 2026-10-13
- suggested: admit — repo-set drift is a calibration flag: package-provenance claims must be scoped to the repo set actually configured.

## Candidate: cache retains multi-version archives — offline version-delta diffing corpus
- claim: The cache holds superseded alongside current builds (`1password-cli` 2.34.1-1 + 2.40.0-2, `abseil-cpp` 20260526.0-2 + 20260817.0-2, `adwaita-fonts` 50.0-1 + 51.0-2), enabling pair-wise shipped-artifact diffing (mtree digests, payload diff) entirely offline.
- source: `ls /var/cache/pacman/pkg/ | sort` — duplicate pkgbase at differing pkgver observed
- verify: `ls /var/cache/pacman/pkg/*.pkg.tar.zst | sed -E 's/-[0-9][^-]*-[0-9.]+-(x86_64|any)\.pkg\.tar\.zst$//' | sort | uniq -d`
- verified-at: 2026-10-13
- suggested: admit — pre-built diff corpus; version-delta is the cheapest REA scoping tool and needs no network.

## Candidate: toolset tiering — stock tools cover the whole archive surface; pacman-contrib absent
- claim: Full coverage of this surface uses only installed tools: `pacman -Qo/-Ql/-Qi/-Qkk/-Qm` (attribution, listing, metadata, mtree verification, foreign list), `tar -tf/-xOf` + `file` + `zstd -t` (archive listing, stdout member extraction, format, integrity), `gpg --homedir /etc/pacman.d/gnupg` (sig verify), `sha256sum`, `vercmp`, `expac`, `bsdtar`; `paccheck`, `pactree`, `pacfiles` (pacman-contrib) are NOT installed — no gap for round-1 work.
- source: `which paccheck expac bsdtar zstd vercmp pactree pacfiles` (expac/bsdtar/zstd/vercmp present; paccheck/pactree/pacfiles absent)
- verify: `command -v pacman tar file zstd gpg sha256sum vercmp expac bsdtar; command -v paccheck pactree pacfiles || echo "pacman-contrib absent"`
- verified-at: 2026-10-13
- suggested: admit — inspection tier is fully operable now; note the contrib gap in SKILL.md before later rounds assume `paccheck`.

## Summary
Archives/packages are a rich shipped-artifact surface: every installed file attributes to a signed, mtree-verified archive readable with stock tar/file/zstd/gpg, and the survey already surfaced one concrete REA target — the unowned static `~/.local/bin/jq` shadowing the packaged binary.

## Erratum (arc3-loop1-round7 calibration re-derivation, append-only)

- The `1556` archive count is a dated 2026-10-13 snapshot, not a live value.
  Re-derived this round (EX-7, EX-8, EX-9, SC-1, SC-2, RV-3, VZ/CN verdicts):
  `ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l` → **1,350** (`.sig` files
  also 1,350), a delta of **−206** — pacman cache eviction, i.e. a
  retention-varying inventory, not a capability claim. Adjudication: no
  corpus edit to the dated value (it is correct at its receipt date); the
  capability claim (signed, integrity-checkable, `.MTREE` per-file sha256,
  `pacman -Qkk`) is unchanged. Residual recorded: `PROVINCE.md:50` repeats
  `1556` without an as-of qualifier — discrepant if read as a current count.
