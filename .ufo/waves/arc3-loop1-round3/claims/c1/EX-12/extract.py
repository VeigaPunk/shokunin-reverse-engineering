import json,hashlib,os
p='/var/tmp/ex12-controls/std-output.json'
raw=open(p).read()
o=json.loads(raw[raw.index('{'):])
c=o['contracts']['VaultA.sol']['VaultA']
creation=c['evm']['bytecode']['object']; runtime=c['evm']['deployedBytecode']['object']
open('/var/tmp/ex12-controls/VaultA.creation.hex','w').write(creation)
open('/var/tmp/ex12-controls/VaultA.runtime.hex','w').write(runtime)
cli=open('/var/tmp/ex12-controls/out/VaultA_sol_VaultA.bin').read().strip()
print('creation bytes:', len(creation)//2, 'sha256', hashlib.sha256(bytes.fromhex(creation)).hexdigest())
print('runtime  bytes:', len(runtime)//2, 'sha256', hashlib.sha256(bytes.fromhex(runtime)).hexdigest())
print('cli creation == std-json creation:', cli==creation)
json.dump(c['abi'], open('/var/tmp/ex12-controls/VaultA.abi.json','w'), indent=1)
print('abi entries:', len(c['abi']))
