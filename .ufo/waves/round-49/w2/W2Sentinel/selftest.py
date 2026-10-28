import re,sys
sys.path.insert(0,'.')
src=open('scan.py').read()
ns={}
start=src.index('PAT=collections'); end=src.index('])\n',start)+3
exec('import collections,re\n'+src[start:end],ns)
PAT=ns['PAT']
cases={'generic-secret-assign':b'api_key = "abcd1234EFGH5678ijkl"\n','aws-access-key':b'AKIAABCDEFGHIJKLMNOP\n','github-token':b'ghp_'+b'a'*36+b'\n','private-key-block':b'-----BEGIN OPENSSH PRIVATE KEY-----\n','session-id-assign':b'JSESSIONID=ABCDEF1234567890\n','authorization-header':b'Authorization: Bearer abcdefghijklmnop\n','1password-ref':b'op://vault/item/field\n','cookie-header':b'Cookie: sid=abc\n','anthropic-or-openai-key':b'sk-ant-api03-abcdefghijklmnopqrstuvwx\n','npm-token':b'npm_'+b'A'*36+b'\n','jwt':b'eyJhbGciOi.eyJzdWIiOi.abcdefgh12\n','env-token-var':b'GITHUB_TOKEN=x\n'}
for k,v in cases.items():
    hit=bool(PAT[k].search(v)); print(f'{k:26s} detects_positive={hit}')
