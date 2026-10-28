# R46W1ScoutFixtures — findings

Full inventory: `.ufo/waves/round-46/w1/R46W1ScoutFixtures/report.md`.

Freeze `31820472784284727546808acc31b3ea1e73919b`. Inventory command exit 0, stdout sha256 `830b1cac3ddb528dec36810bf2db55ff257f07848c3bdd529c63d3f18f40f3fb`, UTC `2026-10-28T16:58:03Z`, 45 paths.

R45-CL13 names receipt sha256 `34336cf79d729e6a85a3ac7a3eda998388011213f33aaa1cba2d8187fcefc7d3` (counter stdout, not the artefact). Fixture commit `0588a84a7aed878dba6ba8e11cf777a8d7ef0099` is not in this repo (`git cat-file -t` exit 128). The exact artefact is not committed. A 40-line stand-in is `.ufo/waves/round-45/w2/R45W2Lesson/fx-a6-SKILL.md` (`cc523958abcc3d484e89da26a7c2137461d8fbb4c440aee9ec4ad8c22632516a`); its re-score stdout was `06c78c60199f8bd8196dfb00527eec8f4891c9dba201408c9eec7e361d0c93a2`, not `34336cf7…`.

Of the 23 ReviewC2 `*.SKILL.md` fixtures, fourteen encode the defect in the body and can be wrapped for `registry.py --spec r45 --profile v1` only. `F5b` through `F5f` are byte-identical to `F0-green` (`f397d3f1fb2b540105ad43beaeaffc2b7e10a64d8a7972246bd618b163504ad1`) and need a repo that was not committed. `attest.py` scores none of the 23. The other 22 `*fixture*` paths are generators or receipts.
