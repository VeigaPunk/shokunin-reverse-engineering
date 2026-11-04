# Round-71 landing runbook (commands as executed)

Landing commit: `c46ea96bd4659f9d346da5fe2b1d0843109402a4`. Nonce: `/fast/scratch/hyaku/kaidoku-r71/l1/pre/landing-nonce.txt`
(the plaintext is scratch-only; `l1/.ufo/waves/round-71/l1/pre/nonce-commitment.txt` is the committed hash).
Pinned upx copy: `$W/upx-pinned-copy` (bytes must hash to
`cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`).

1. `install -m755 /usr/bin/upx $W/upx-pinned-copy && sha256sum $W/upx-pinned-copy`
2. Route (C1):
   `python3 -I -B tools/round-71/packed-elf.py --root . --rev c46ea96bd4659f9d346da5fe2b1d0843109402a4 --pkg <REA> --work $W
    --upx $W/upx-pinned-copy --challenge $(cat /fast/scratch/hyaku/kaidoku-r71/l1/pre/landing-nonce.txt) --nonce-commitment $(cat .ufo/waves/round-71/l1/.ufo/waves/round-71/l1/pre/nonce-commitment.txt)
    --child-env-log $W/env.jsonl --json-out .ufo/waves/round-71/l1/scores/c1-route-at-landing.json`
3. Checker (C1): `python3 -I -B tools/round-71/packed-elf.py --check-receipt
   .ufo/waves/round-71/l1/scores/c1-route-at-landing.json --root . --rev c46ea96bd4659f9d346da5fe2b1d0843109402a4
   --nonce-commitment $(cat .ufo/waves/round-71/l1/.ufo/waves/round-71/l1/pre/nonce-commitment.txt)` → `c1-check-at-landing.json`
4. Probe (C1): `python3 -I -B tools/round-71/seam-probe.py --root . --rev c46ea96bd4659f9d346da5fe2b1d0843109402a4 --tool tools/round-71/packed-elf.py
   --battery tools/round-70/mutation-check.py --pkg <REA> --work $W
   --receipt .ufo/waves/round-71/l1/scores/c1-route-at-landing.json --expect-upx $W/upx-pinned-copy
   --nonce-commitment $(cat .ufo/waves/round-71/l1/.ufo/waves/round-71/l1/pre/nonce-commitment.txt)
   --legacy-receipt .ufo/waves/round-70/l1/scores/c3-at-landing.json
   --json-out .ufo/waves/round-71/l1/scores/c1-at-landing.json`
5. Base probe (C1 before): the same probe at `--rev 7c155617…` against `tools/round-70/packed-elf.py`
   and `tools/round-70/mutation-check.py` with the round-70 landing receipt and its recorded pinned-copy
   path, no `--nonce-commitment` → `c1-at-base.json`.
6. Battery (C2): `python3 -I -B tools/round-71/forged-receipts.py --root . --rev c46ea96bd4659f9d346da5fe2b1d0843109402a4
   --base-rev 5cc845ca… --tool tools/round-70/packed-elf.py --base-tool tools/round-69/packed-elf.py
   --probe tools/round-70/contract-probe.py --base-probe tools/round-69/contract-probe.py
   --base-probe-rev 5ee94c56… --battery tools/round-70/mutation-check.py
   --base-material .ufo/waves/round-69/l1/scores/c3-at-landing.json
   --landing-material .ufo/waves/round-70/l1/scores/c3-at-landing.json
   --first-cut-rev 4737a542… --first-cut-tool tools/round-70/packed-elf.py
   --superseded-rev 7c155617… --pkg <REA> --work $W
   --json-out .ufo/waves/round-71/l1/scores/c2-at-landing.json`
7. Census (C3): `python3 -I -B tools/round-71/registry-census.py --root . --rev c46ea96bd4659f9d346da5fe2b1d0843109402a4 --generate
   --out .ufo/waves/round-71/l1/scores/c3-at-landing.json` (expect 93 rows, 0 nonconformant, exit 0);
   the base run and the round-51 `census3` exit 2 are in `l1/pre/` and `l1/scores/c3-census3-at-base.txt`.
8. Controls: `python3 -I -B tools/round-71/controls.py --root . --work $W
   --probe tools/round-71/seam-probe.py --battery tools/round-71/forged-receipts.py
   --census tools/round-71/registry-census.py --json-out .ufo/waves/round-71/l1/scores/controls-at-landing.json`
9. Gates: `python3 -I -B tools/round-29/freeze-gate.py --root . --rev c46ea96bd4659f9d346da5fe2b1d0843109402a4` → `gate-at-landing.json`;
   `python3 -I -B tools/round-68/registry-conformance.py --root . --rev c46ea96bd4659f9d346da5fe2b1d0843109402a4` →
   `registry-conformance-at-landing.json`.
10. Scratch removed after the close (`rm -rf /fast/scratch/hyaku/kaidoku-r71`); no pacman transaction.
