# R30-C1 Separability Attack (`SepC1`)

- **Seat:** `KaidokuR30.SepC1` (critic)
- **Target attacked:** `R30-C1` separability from `R30-C2` (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json:38`: *"C1 reads only corpus/evidence/round-30/c1 and its 16 carriers ... Each counter can exit 0 with the other claim's evidence absent."*)
- **Verdict:** **holds** (counter reaches its frozen target line `carriers=16 pass=16 target=16 entry_ok=1 (ok) province_ok=1 (ok)` and exits `0` with all specified C2 evidence, C2 entry, and round-30 `SKILL.md` section absent).

---

## 1. Sandbox Setup and C2 Stripping

- **Observation (2026-10-23T03:12:55Z UTC):** Cloned `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` into `/fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/clone` and reset branch `main` to the measured revision `92b1dd2ddc119fda89a611ba515bdf6cfe906f76` (`exit=0`).
  - Command:
    ```sh
    env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 60 git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/clone
    env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 60 git -C /fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/clone checkout -B main 92b1dd2ddc119fda89a611ba515bdf6cfe906f76
    ```
  - Output excerpt:
    ```text
    Reset branch 'main'
    92b1dd2ddc119fda89a611ba515bdf6cfe906f76
    ```

- **Observation (2026-10-23T03:13:28Z UTC):** Deleted `corpus/evidence/round-30/c2/envelopes` (38 files: 19 `.json` + 19 `.stderr`), `corpus/evidence/round-30/c2/runs.tsv`, the C2 entry `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md`, and the round-30 `SKILL.md` section (`SKILL.md:965-1005`, restoring `SKILL.md` to its exact base blob sha256 `3982fddfcf0b466380ed9fd81d8ca575cab2bd72b8dcab4e0dda216af52373a9` at `d210fb8fa62d2af04d009cfa0c65a4e8137dc742`), then committed on sandbox `main` as `51fdc7676206ca2f4cc82478cc0d446fab151713` (`exit=0`).
  - Command:
    ```sh
    env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 30 git -C /fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/clone add -A && \
    env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 30 git -C /fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/clone -c user.name=ctl -c user.email=ctl@sandbox commit -m "SepC1: remove C2 evidence, C2 entry, and round-30 SKILL section"
    ```
  - Output excerpt:
    ```text
    [main 51fdc767] SepC1: remove C2 evidence, C2 entry, and round-30 SKILL section
     41 files changed, 132 deletions(-)
    ```

---

## 2. C1 Counter Execution (`--rev main`)

- **Observation (2026-10-23T03:13:41Z–2026-10-23T03:13:54Z UTC):** Ran the frozen R30-C1 counter against the C2-stripped sandbox clone at `--rev main` (`51fdc7676206ca2f4cc82478cc0d446fab151713`).
  - Producing command:
    ```sh
    env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/tmp timeout 600 python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/clone --rev main
    ```
  - Exit code: `0`
  - Full stdout (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/c1-sep-stdout.txt`, sha256 `b913d0755dc7d124b8a976a6927ae92d604d5412235c12b7ed358e4b4bafac4c`):
    ```text
    elf-x86_64-uv	P1-pass	packages=584 edges=3041
    elf-x86_64-uvx	P1-pass	packages=584 edges=3041
    elf-aarch64-uv	P1-pass	packages=584 edges=3042
    elf-aarch64-uvx	P1-pass	packages=584 edges=3042
    elf-riscv64-uv	P1-pass	packages=580 edges=3030
    elf-riscv64-uvx	P1-pass	packages=580 edges=3030
    pe-x86_64-uv	P1-pass	packages=596 edges=3013
    pe-x86_64-uvx	P1-pass	packages=596 edges=3013
    pe-x86_64-uvw	P1-pass	packages=596 edges=3013
    pe-arm64-uv	P1-pass	packages=596 edges=3012
    pe-arm64-uvx	P1-pass	packages=596 edges=3012
    pe-arm64-uvw	P1-pass	packages=596 edges=3012
    macho-x86_64-uv	P1-pass	packages=573 edges=2974
    macho-x86_64-uvx	P1-pass	packages=573 edges=2974
    macho-arm64-uv	P1-pass	packages=573 edges=2975
    macho-arm64-uvx	P1-pass	packages=573 edges=2975
    carriers=16 pass=16 target=16 entry_ok=1 (ok) province_ok=1 (ok)
    ```
  - Stderr (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/c1-sep-stderr.txt`, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`): empty (`0` bytes).

---

## 3. Critic Review: Counterexample, Evidence, Impacted Axes, Smallest Safe Correction

- **Counterexample to counter-level failure:** None. Under `tools/round-30/c1-rust-positive.py`, `R30-C1` has zero dependency on `corpus/evidence/round-30/c2/*`, `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md`, or `SKILL.md`.
- **Prose-level cross-reference finding (fixable defect, not a counter failure):**
  - **Observation:** In `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md:336`, the `Verified evidence` cell of the new round-30 row combines both claims in one sentence:
    `... (`corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md`, ids in its Results table); 19 of 19 code-predicted accept/refuse signatures on ELF mutants (`corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md`; decision table in SKILL.md)`
    Similarly, `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md:69` parenthetically cites `(S090)` (the C2 code-reading source row) in its `Inference` paragraph.
  - **Inference:** While `c1-rust-positive.py`'s `province_ok` and `entry_ok` gates pass when C2's entry and `SKILL.md` section are removed, a C1-only tree that strips C2 leaves a dangling path pointer in `PROVINCE.md:336` to `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` and `SKILL.md`.
- **Impacted axes:** `coverage` (`R30-C1`) — holds at the counter level (`exit=0`); minor prose coupling in `PROVINCE.md:336` if `R30-C2` were ever dropped independently.
- **Smallest safe correction:** None required when both `R30-C1` and `R30-C2` settle green; if `R30-C2` were ever omitted, trim the semicolon clause in `PROVINCE.md:336` (`; 19 of 19 code-predicted accept/refuse signatures on ELF mutants ...`).

---

## 4. Scratch Artifacts and Tooling Record

- `/fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/c1-sep-stdout.txt` — sha256 `b913d0755dc7d124b8a976a6927ae92d604d5412235c12b7ed358e4b4bafac4c`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/c1-sep-stderr.txt` — sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w2/SepC1/clone` — sandbox git clone at commit `51fdc7676206ca2f4cc82478cc0d446fab151713` (parent `92b1dd2ddc119fda89a611ba515bdf6cfe906f76`); modified tracked file `SKILL.md` sha256 `3982fddfcf0b466380ed9fd81d8ca575cab2bd72b8dcab4e0dda216af52373a9`
- **Tooling installs/updates:** none.
