# EX-08 probe matrix (arc3-loop1-round1, chain c1)

| probe | exit | shape | key fields |
|---|---|---|---|
| probe-elfmagic-hex-6.4.0 | 1 | typed refusal | code=invalid_request category=invalid_input retryable=true issue="Hex carrier requires complete hexadecimal byte pairs, an optional 0x prefix and outer ASCII whitespace; interior separators are invalid." |
| probe-elfmagic-raw-6.4.0 | 0 | analysis: honest empty | artifact=a037bf6e958b bc=a037bf6e958b kind=unknown fns=[] dispatch=[] mutability=[] ev=ev_35847650d967… |
| probe-empty-hex-6.4.0 | 0 | analysis: honest empty | artifact=e3b0c44298fc bc=e3b0c44298fc kind=unknown fns=[] dispatch=[] mutability=[] ev=ev_f5cfa260f3b1… |
| probe-empty-raw-6.4.0 | 0 | analysis: honest empty | artifact=e3b0c44298fc bc=e3b0c44298fc kind=unknown fns=[] dispatch=[] mutability=[] ev=ev_7e1cee47536d… |
| probe-missing-6.4.0 | 1 | typed refusal | code=invalid_request category=invalid_input retryable=true issue="Selected bytecode carrier could not be read (ENOENT): /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1/EX-08/does-not-exist.bin." |
| probe-nonbc-hex-6.4.0 | 0 | analysis: honest empty | artifact=48db334952c5 bc=5edc628b3e97 kind=unknown fns=[] dispatch=[] mutability=[] ev=ev_9344f01636d9… |
| probe-recon-hex-6.4.0 | 0 | analysis: selectors recovered | artifact=fd87e58e336b bc=df60b581fc0d kind=unknown fns=[095ea7b3@74, 70a08231@68, a9059cbb@62] dispatch=[abi] mutability=[payable] ev=ev_5e5f33fe666c… |
| probe-recon-hex-6.7.0 | 0 | analysis: selectors recovered | artifact=fd87e58e336b bc=df60b581fc0d kind=unknown fns=[095ea7b3@74, 70a08231@68, a9059cbb@62] dispatch=[abi] mutability=[payable] ev=ev_087a47b93c44… |
| probe-recon-raw-6.4.0 | 0 | analysis: selectors recovered | artifact=df60b581fc0d bc=df60b581fc0d kind=unknown fns=[095ea7b3@74, 70a08231@68, a9059cbb@62] dispatch=[abi] mutability=[payable] ev=ev_3e963fef2600… |
| probe-recon-raw-6.7.0 | 0 | analysis: selectors recovered | artifact=df60b581fc0d bc=df60b581fc0d kind=unknown fns=[095ea7b3@74, 70a08231@68, a9059cbb@62] dispatch=[abi] mutability=[payable] ev=ev_4059fadc534b… |
| probe-recon-raw-noTMPDIR | 1 | typed refusal | code=execution_failure category=execution_failure retryable=false issue="Unknown system error -122: Unknown system error -122, write" |
| probe-txt-hex-6.4.0 | 1 | typed refusal | code=invalid_request category=invalid_input retryable=true issue="Hex carrier requires complete hexadecimal byte pairs, an optional 0x prefix and outer ASCII whitespace; interior separators are invalid." |
| probe-txt-raw-6.4.0 | 0 | analysis: honest empty | artifact=5edc628b3e97 bc=5edc628b3e97 kind=unknown fns=[] dispatch=[] mutability=[] ev=ev_6db86f98605b… |
