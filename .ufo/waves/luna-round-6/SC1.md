## CLAIM
`/usr/bin/docker` is a real Go ELF candidate for the Go inspection leg.

## METHOD
Read-only discovery command: `find /usr/bin -maxdepth 1 -type f -name docker -exec file {} \; -exec sha256sum {} \;`

## FINDINGS
Output:
```text
/usr/bin/docker: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=9e64db639d33d9b4f41701b86168ed613b898382, for GNU/Linux 4.4.0, stripped
70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9  /usr/bin/docker
```
Docker CLI is implemented in Go; the local `file` output establishes the candidate is an ELF but does not independently label its language.

## THREATS
No execution or host mutation performed. Go-language attribution is not proven by the `file` output alone.

## VERDICT
CLEAN — candidate path, ELF signature, and SHA-256 recorded.
