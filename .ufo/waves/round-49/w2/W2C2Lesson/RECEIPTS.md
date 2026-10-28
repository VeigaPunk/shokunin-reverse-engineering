# W2C2Lesson receipts (UTC of batch: 2026-10-28T22:46:33Z)
## commands (exit codes in *.rc)
- c2 at R: python3 -I -B c2-R.py --root <LANE> --rev 29883d4ec35a31a8393c4ffb220888c44c0bb022 --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d --battery  (exit 0)
- c2 at freeze: python3 -I -B c2-F.py --root <LANE> --rev decc5697bfd4ec1e9de4a762ad199d9bd9c4230d --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d (exit 1)
- c1 --selftest frozen (copy of tools/round-49/c1-counter.py at R, placed under scratch tree with tools/round-27/xpin-attribute.mjs): (exit 0, cases 52)
- c1 --selftest with substring mutant (`return '/kaidoku-r49/' in output_directory`): (exit 1, failures = 2 provenance cases)
## sha256
  59813ae49aba05190c7490f9065c4bed607681ae2ca442f95611f372c9174f3c  RECEIPTS.md
  65f3599f0ef0379c47d7efe3babe0f5ee9e15ebcd6245be0b81c082ba34efb01  SOURCES-R.md
  68e6d028744096a4d9e5b2e777ad7ed3e1c56dcc83778f839cb775119627e712  SOURCES-base.md
  d38b7a70a80d664bff42abb947d566b4b33b5d4a54189a910668c3be6ebb1514  c1-counter-substring-mutant.py
  167b1406fa5fedcd999fe881d1a4c194794f73ee0b07fbe4b33e29c30a11b7f5  c1-selftest-frozen.json
  19eaf43821a7660ec323a87c8457bf74823beb296c39f5e01aa8a683aa50f061  c1-selftest-frozen.rc
  eeb1137166fa4fb3b89620e50ee4b538f22e5fc5def7f4044475b4fdfa0e8558  c1-selftest-substring-mutant.json
  cf205dbb8cea84897b488abcc281bf96698d5e94b1096b16657b4caba9082a22  c1-selftest-substring-mutant.rc
  7aa900e1f004d3f13117264e85b68a51b9116dab2590da7a00a66c584b2e37f4  c2-F.json
  cf205dbb8cea84897b488abcc281bf96698d5e94b1096b16657b4caba9082a22  c2-F.rc
  0cad6d5cfb525227be6af09d6cd6b6115818cee4436180a902a8d1847f490f86  c2-R-battery.json
  19eaf43821a7660ec323a87c8457bf74823beb296c39f5e01aa8a683aa50f061  c2-R-battery.rc
  a6895609b910ec8f4511f0783f18f7151c86934bf04495018a503a1e5749914b  fleet-report-r48-HEAD.md
  1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf  freebsd.html
  8df4089f479e8e6cbbdde10cd4193159bc4f6512331f5e7a3846b13dfdefb6fc  lesson-R.md
  2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207  popper.html
  a46da21f264b5c6fd23f2fe6c0ab6cadc7dad2788d5093dfc7a776131aac13e8  round-48-closure-R.md
  d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340  sysexits.html
