# R29-C1 REA call-record audit

## Verdict

**Observation — holds:** at commit `18be864a528873b2b70d8c94e31f880290249e90`, all 16 `runs.tsv` records have exit `0` and satisfy the requested argv, package, committed-envelope, operation/provider, carrier digest/path, and ABI function-count checks. `runs_ok=16/16`.

## Per-carrier results

The table is from the audit command below. `Envelope SHA-256` is the committed envelope blob's digest, which matched that row's `runs.tsv` value. `Subject/runtime SHA-256` gives the envelope subject digest and independently hashed committed runtime; both matched `carriers.tsv`. For every row, argv matched the exact pattern `npx -y rea-agents@6.5.0 inspect-evm-interface /home/vgpnk/Projects/shokunin/kaidoku-shokunin/<carrier runtime path> hex --format json`; package version/hash, operation `inspect_evm_interface`, provider `evmole@0.9.3`, and subject local path also matched. Function counts are `raw_result.functions / normalized_result.functions / ABI type=function entries`.

| Carrier | Exit | Envelope SHA-256 | Subject/runtime SHA-256 | Functions | Result |
|---|---:|---|---|---:|---|
| n01 | 0 | `f74a5e21834fb607f035125a99f4d2fa318291349cde517ee80b44b9e7e8ad0e` | `5b3f3f769e43534e9ea7eec797a4c2f53a14d63d0ae55a7ec315b05d9227e66f` | 14/14/14 | PASS |
| n02 | 0 | `ff0cc61e944596ce8e04b586b232d78874dc5fa6e082354a1d46609339c3f8a7` | `d7bff45d0a7c68a3bd7a25a567bc8a5d226d2cb86aa0307f0a5aa29d21b1c7ab` | 13/13/13 | PASS |
| n03 | 0 | `7e67a9548d37de70e1e7ba72a6f07372fe865fbad2c1c3113a1b96bb561f283e` | `3acfbfda8cdf62c6c6c1cdd2109f89f5294054eb0b039aed6cce1ee9abc4df57` | 5/5/5 | PASS |
| n04 | 0 | `371a36263a0e3ca68d35776249bd24f1f3a3e81a22bdf51a9218501bb3b60ac0` | `5a37c73afd3a075dba69d53b548283efacdb78b08672a44d9a940be310a6cca0` | 16/16/16 | PASS |
| n05 | 0 | `5fef7ef5096ea89d8be38b68925499dc92b0fefede51eb19d2d3d1f343e8c362` | `ba576c922bf72db3c1ab3cd6d6ee6af6e18196874c974514bfb16e3f59bafca0` | 14/14/14 | PASS |
| n06 | 0 | `7d8d52880e043d3191dbe669918687f26b63d362756e37ea8de476f4f8ee6485` | `9b16dfa64c6e0579203b569169ee73b5dea8f554b92677bdf21aea6f2ef218db` | 15/15/15 | PASS |
| n07 | 0 | `185c4fb66ac96cc5ae887d4957438695ccb8c976feb3af8e2a1818b44012caaa` | `7e7f03b83f619aaa65954149b96c30d63a7a5a0c4589cf817d3aef1e961b7a9f` | 14/14/14 | PASS |
| n08 | 0 | `3e59cb5a3db176ef3ce9d01bdaef82d25bc1fe43421144f11aebf255f56a4e29` | `f718813e15032e8a1d04a2a0bd1483003e279318ab9301a268e629c63bc0d91f` | 8/8/8 | PASS |
| n09 | 0 | `8004c86e70d919c57d614d660aa3629ca049968243930dbec8d312281aa41e98` | `a2dbecf0d45ee1d7b0be2d7966266ac73dfbbbcf6b2abbd3b82036ac907f6071` | 2/2/2 | PASS |
| n10 | 0 | `a5f463ccb1f5c6cf9c8be9bfa244da999dbbae911feeb070b9f21076a3d8a68f` | `9deaf740120a8ab3adbb03229639b85e690dd2d40ef89d5f3bd429786637d39b` | 10/10/10 | PASS |
| n11 | 0 | `66709c4efe4fb0b2d05490767751923c9208ebd453de57719b312631b77dd6ba` | `5c7fe0b05916971b7784c5631e10b720e543215eb259b52d37e64ab2676e0dc9` | 9/9/9 | PASS |
| n12 | 0 | `ae7b7c4bcb7f6aa96bcf9356825f15fd797837c52d296581bfacb1dcdca740a6` | `be2d3f24434c230f90044bef55a8ec09c08b9cf2bd6b1b7dc6a964e7005ac69b` | 11/11/11 | PASS |
| n13 | 0 | `bbe553ca00acaf2064b654a02d41b3e260ab63f96a48719eb6855941970324a4` | `2f67e4c52dc188b58659888a958f2bb8e8a426966a47f6916ff9dead009cf8b5` | 15/15/15 | PASS |
| n14 | 0 | `f163d61d8bfa2c2d7554590e36015d8228288f748c278301d2f10e90c1574611` | `bb75506440b11908fc051c80f04db4513178fde401bb90f9daf9717ca82c29d0` | 13/13/13 | PASS |
| n15 | 0 | `4bc92ac8bc63711c12b75b191ef70166925d90b394ea1099c28722fc5a9e7f9b` | `7652be8f1f19eabdb53027fc14688e62800dd1e3dfe9290bcd447da1b2d632e6` | 9/9/9 | PASS |
| n16 | 0 | `86c0aa2be9b1cec8924144fa56f787e073163841626bf85aaedb906aa9243adb` | `24cc490f6820e25ca963dabc899ac6f80d7c44f7584e5f7ace151f2c9ed4a8ef` | 10/10/10 | PASS |

## Evidence

- **Producing command:** `python3 -I -B /fast/scratch/hyaku/kaidoku-r29/seats/w1/exec-envelope-audit/audit.py` (cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`). It read target-commit blobs via read-only `git show`; it did not execute REA again.
- **UTC:** `2026-10-22T20:22:35Z`; **exit code:** `0`.
- **Exact output excerpt:**

  ```text
  audit_utc=2026-10-22T20:22:35Z
  revision=18be864a528873b2b70d8c94e31f880290249e90
  rows=16 carriers=16 package_json_sha256=a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
  expected_package_json_sha256=a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c package_hash_match=True
  OVERALL=PASS runs_ok=16/16
  ```

  The same output contains the per-carrier checks and full local paths. Each row reports `0/OK`, argv `OK`, package `6.5.0/OK`, equal recorded/computed envelope SHA-256, operation/provider `OK`, subject digest/path `OK`, runtime-manifest hash `OK`, and equal raw/normalized/ABI function counts.
- **Retained scratch artifacts (SHA-256):**
  - `/fast/scratch/hyaku/kaidoku-r29/seats/w1/exec-envelope-audit/audit.py` — `bf79488bb284669c371492d6be49477eb1fd947edcb42e2d097bb7e7862a65b9`
  - `/fast/scratch/hyaku/kaidoku-r29/seats/w1/exec-envelope-audit/audit.stdout.txt` — `adcae19379093555f3f2b146979f88b0ab1ede32913dc072020cd5ee2435149e`

## Risks and blockers

- **Risk:** this verifies the committed run records and envelope bytes at the specified revision against the package JSON currently present at the specified npm-cache path; it does not establish that the package file was unchanged since the recorded runs.
- **Blockers:** none. No tools were installed. No lane implementation/evidence files were changed; only this assigned report was written in the lane.