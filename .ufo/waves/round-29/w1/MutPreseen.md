# Round 29 W1 — `preseen.py` mutation probe

## Scope and detector

[OBSERVATION] Tested the copy at `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/clone/tools/round-29/preseen.py` (clone HEAD `18be864a528873b2b70d8c94e31f880290249e90`) against committed source revision `bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47`. Lane files were not changed; each mutation was applied only in the scratch clone and restored from `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/preseen.pristine.py`.

The bounded detector command was `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 /fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/clone/tools/round-29/preseen.py --root /fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/clone --rev bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47 --check <input> --kind <name|flag>`. Inputs were the C1 `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/clone/corpus/evidence/round-29/c1/heldout.tsv`, C2 `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/clone/corpus/evidence/round-29/c2/selectors.tsv`, and planted `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/planted.tsv` (`a9059cbb`).

[OBSERVATION] Pristine runs at 2026-10-22 20:21:56–20:21:58 UTC: C1 name printed `test_selectors=152 seen_set=58720 overlap=0` (exit 0); C2 flag printed `test_selectors=178 seen_set=230 overlap=0` (exit 0); planted `a9059cbb` printed `overlap=1 a9059cbb` for both name and flag (exit 1 each). Pristine targeted probes also reported overlap for `32ca2201` (case-fold-only token) and `00000002` (0x-prefixed-only token), both exit 1. The substring-only probe `00000031` returned `overlap=0` (exit 0).

## Mutant results

For every mutant below, the `before` and `restored` target hash was `073381ca213573b8809a130cf3d958e0b253b4d56a7ce34079ef2f2b0c89d167`. The exact run outputs, timestamps and exit codes are preserved in `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/results.log`.

| Mutant | Mutated SHA-256 | C1 name / C2 flag | Planted `a9059cbb` name / flag | Focused probe | Verdict |
|---|---|---|---|---|---|
| Drop `-i` | `d8465a207d4e5d3bce1eb0314a0ff8a2dbadaae4955415df6653ede6d330e90a` | `overlap=0` / `overlap=0` (exit 0 / 0) | `overlap=1` / `overlap=1` (exit 1 / 1) | `32ca2201`: baseline 1, mutant 0, restored 1 | Killed |
| Drop `0x` strip | `a2114678a168e7d2e322ae76fd88a5cc95bdbba8f86c4c9b2926441c489a649d` | `overlap=0` / `overlap=0` (exit 0 / 0) | `overlap=1` / `overlap=1` (exit 1 / 1) | `00000002`: baseline 1, mutant 0, restored 1 | Killed |
| Narrow `OC_NAME` | `cf46daed97bdb70b627babf94da06a446fcb4e668f68c480d11a812af3c362b9` | `overlap=0` / `overlap=0` (exit 0 / 0) | `overlap=1` / `overlap=1` (exit 1 / 1) | No assigned input distinguished it | Survived |
| Skip JSON body scan | `851b84c022607ef45f91e0664768c521d75572287b05c5d44eecf9a118b68cfd` | `overlap=0` / `overlap=0` (exit 0 / 0) | `overlap=1` / `overlap=1` (exit 1 / 1) | No assigned input distinguished it | Survived |
| Remove `-w` | `a642b05cea175558f1eff4c6bb81cbfafeb56290a537646f2fd51497de76b327` | `overlap=0` / `overlap=0` (exit 0 / 0) | `overlap=1` / `overlap=1` (exit 1 / 1) | `00000031`: baseline 0, mutant 1, restored 0 | Killed |


1. **Drop `-i` in `name_seen`** — mutated SHA-256 `d8465a207d4e5d3bce1eb0314a0ff8a2dbadaae4955415df6653ede6d330e90a`.
   - [OBSERVATION] Requested inputs still gave C1 `overlap=0` (20:24:40Z, exit 0; seen set 58,655), C2 `overlap=0` (20:24:42Z, exit 0), and `a9059cbb` overlap in name and flag (20:24:42Z and 20:24:44Z, exit 1 each).
   - [OBSERVATION] Focus command: same command above with `--check /fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/planted-casefold.tsv --kind name`. Pristine at 20:24:26Z printed `overlap=1 32ca2201` (exit 1); mutant at 20:24:44Z printed `seen_set=58655 overlap=0` (exit 0); restored at 20:24:49Z again printed `overlap=1 32ca2201` (exit 1).
   - **Verdict: killed by focused probe.** The requested C1/C2 and `a9059cbb` checks alone would not kill it.

2. **Drop the `0x` stripping in `name_seen`** — mutated SHA-256 `a2114678a168e7d2e322ae76fd88a5cc95bdbba8f86c4c9b2926441c489a649d`.
   - [OBSERVATION] Requested inputs still gave C1 `overlap=0` (20:25:09Z, exit 0; seen set 57,897), C2 `overlap=0` (20:25:10Z, exit 0), and `a9059cbb` overlap in name and flag (20:25:11Z and 20:25:12Z, exit 1 each).
   - [OBSERVATION] Focus command: same command with `--check /fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/planted-prefix.tsv --kind name`. Pristine at 20:24:27Z printed `overlap=1 00000002` (exit 1); mutant at 20:25:13Z printed `seen_set=57897 overlap=0` (exit 0); restored at 20:25:19Z printed `overlap=1 00000002` (exit 1). The case-fold probe also changed from overlap 1 to overlap 0 under this mutant.
   - **Verdict: killed by focused probe.** The requested inputs alone would not kill it.

3. **Narrow `OC_NAME`** — mutant requires exactly `openchain-0x<8hex>.json` (drops the optional prefix and suffix allowance); mutated SHA-256 `cf46daed97bdb70b627babf94da06a446fcb4e668f68c480d11a812af3c362b9`.
   - [OBSERVATION] C1 at 20:25:38Z and C2 at 20:25:39Z remained `overlap=0` (exit 0 each). Planted `a9059cbb` remained `overlap=1 a9059cbb` for name and flag at 20:25:39Z and 20:25:40Z (exit 1 each). The flag seen-set remained 230. Restored runs returned the same results at 20:25:41–20:25:43Z.
   - **Verdict: survived the assigned inputs.** [INFERENCE] The C2 negative list and `a9059cbb` positive do not distinguish this narrower filename matcher in this base-revision corpus.

4. **Skip JSON body scan in `flag_seen`** — retained the filename scan; mutated SHA-256 `851b84c022607ef45f91e0664768c521d75572287b05c5d44eecf9a118b68cfd`.
   - [OBSERVATION] C1 at 20:26:02Z and C2 at 20:26:03Z remained `overlap=0` (exit 0 each). Planted `a9059cbb` remained `overlap=1 a9059cbb` for name and flag at 20:26:04Z and 20:26:05Z (exit 1 each). Restored runs returned the same results at 20:26:05–20:26:07Z.
   - **Verdict: survived the assigned inputs.** [INFERENCE] The assigned C2 list plus a selector also found by the filename path does not exercise a body-only positive.

5. **Remove `-w` in `name_seen`** — mutated SHA-256 `a642b05cea175558f1eff4c6bb81cbfafeb56290a537646f2fd51497de76b327`.
   - [OBSERVATION] Requested C1 at 20:26:22Z stayed `overlap=0` (exit 0, but seen set grew from 58,720 to 281,487); C2 at 20:26:24Z stayed `overlap=0` (exit 0); planted `a9059cbb` still overlapped in name and flag at 20:26:24Z and 20:26:26Z (exit 1 each). Thus those requested checks alone do not kill it.
   - [OBSERVATION] Focus command: same command with `--check /fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/planted-substring.tsv --kind name`. Pristine at 20:27:25Z printed `overlap=0` (exit 0); mutant at 20:27:36Z printed `seen_set=281487 overlap=1 00000031` (exit 1); restored at 20:27:38Z printed `overlap=0` (exit 0).
   - **Verdict: killed by focused false-positive probe.**

## Conclusion

[OBSERVATION] The pristine screen correctly rejected the planted `a9059cbb` overlap for both kinds and returned the expected negative result for the two main lists. The required C1/C2 lists and generic `a9059cbb` positive did not distinguish any of these five mutations by exit decision.

[OBSERVATION] Focused probes exposed three defects: dropping `-i` and dropping the `0x` strip each miss a known name overlap; dropping `-w` creates a false-positive overlap on a substring-only token. **The screen can fail under these plausible regressions.**

[OBSERVATION] Survivors: narrowed `OC_NAME` and skipped JSON-body scan. These are coverage findings only; no contract or lane source was changed. No network lookup, REA run, external source fetch, or tool installation was used.

## Scratch evidence hashes

[OBSERVATION] SHA-256 values for created evidence files:

- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/preseen.pristine.py` — `073381ca213573b8809a130cf3d958e0b253b4d56a7ce34079ef2f2b0c89d167`
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/results.log` — `2a31f632e2f558ca0e68d47304cc1875030b515d383c5f602d7a80d3fd7e793d`
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/planted.tsv` — `18f944d03b24acdab7db03deb4d6db495cd15d6f49e6f5b8d0a126540317b017`
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/planted-casefold.tsv` — `3cdcaee713b5e2f4fd315b69892cfde5ba7438a71d32393eb962dc5115be66f5`
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/planted-prefix.tsv` — `7fa382fcbe6288ccf09bdf9f81b7c2768b9832048bb0dbfca3f2e6971067826e`
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/planted-substring.tsv` — `ce86abc19e126ed9789235b8ebc282d4129f630f595108a1af7d04d0ba05c3d3`
- Restored clone target `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/clone/tools/round-29/preseen.py` — `073381ca213573b8809a130cf3d958e0b253b4d56a7ce34079ef2f2b0c89d167`
- C1 input `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/clone/corpus/evidence/round-29/c1/heldout.tsv` — `2db9e658d5076771ee249f9d027938103edb7933201abb4b391f1053323dca23`
- C2 input `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPreseen/clone/corpus/evidence/round-29/c2/selectors.tsv` — `3a93f7837accb9acd66874707922317d9a8e0f8afb0c9cd87ee79f3d9fa15b5d`
