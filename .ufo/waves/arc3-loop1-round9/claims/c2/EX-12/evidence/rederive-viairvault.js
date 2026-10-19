const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const solcRoot = process.argv[2];
if (!solcRoot) throw new Error('usage: node rederive-viairvault.js /absolute/path/to/solc');
const solc = require(solcRoot);
const jsSha3 = require(process.env.JS_SHA3_MODULE || '/var/tmp/kaidoku-ex12/vendor/node_modules/js-sha3');
const root = __dirname;
const sourcePath = path.join(root, 'viairvault-input', 'ViaIrVault.sol');
const source = fs.readFileSync(sourcePath, 'utf8');
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const compilerDir = path.dirname(require.resolve(solcRoot));
const compilerPackage = JSON.parse(fs.readFileSync(path.join(compilerDir, 'package.json'), 'utf8'));
const compilerBytes = fs.readFileSync(path.join(compilerDir, 'soljson.js'));
const sourceName = 'ViaIrVault.sol';
const contractName = 'ViaIrVault';

function compile() {
    const input = {
        language: 'Solidity',
        sources: { [sourceName]: { content: source } },
        settings: {
            optimizer: { enabled: true, runs: 200 },
            viaIR: true,
            outputSelection: {
                '*': {
                    '*': [
                        'abi',
                        'evm.methodIdentifiers',
                        'evm.bytecode.object',
                        'evm.deployedBytecode.object'
                    ]
                }
            }
        }
    };
    const inputText = JSON.stringify(input, null, 2) + '\n';
    const firstText = solc.compile(JSON.stringify(input));
    const secondText = solc.compile(JSON.stringify(input));
    const first = JSON.parse(firstText);
    const second = JSON.parse(secondText);
    const errors = (first.errors || []).filter(item => item.severity === 'error');
    if (errors.length) throw new Error(JSON.stringify(errors, null, 2));
    const contract = first.contracts[sourceName][contractName];
    const repeated = second.contracts[sourceName][contractName];
    const runtimeHex = contract.evm.deployedBytecode.object.toLowerCase();
    const repeatedRuntimeHex = repeated.evm.deployedBytecode.object.toLowerCase();
    const functionEntries = contract.abi.filter(item => item.type === 'function');
    const signatures = functionEntries
        .map(item => `${item.name}(${item.inputs.map(input => input.type).join(',')})`)
        .sort();
    const independentlyDerived = Object.fromEntries(signatures.map(signature => [
        signature,
        jsSha3.keccak_256(signature).slice(0, 8)
    ]));
    const methodIdentifiers = contract.evm.methodIdentifiers;
    const selectorsAgree = signatures.every(signature =>
        independentlyDerived[signature] === methodIdentifiers[signature]
    );
    const outputEqual =
        runtimeHex === repeatedRuntimeHex &&
        JSON.stringify(contract.abi) === JSON.stringify(repeated.abi) &&
        JSON.stringify(methodIdentifiers) === JSON.stringify(repeated.evm.methodIdentifiers);
    const outDir = path.join(root, 'compiled-viairvault', `solc-${solc.version().split('+')[0]}`, 'viair');
    fs.mkdirSync(outDir, { recursive: true });
    const runtime = Buffer.from(runtimeHex, 'hex');
    const receipt = {
        solcPackageVersion: compilerPackage.version,
        solcVersion: solc.version(),
        solcPackageJsonSha256: sha256(fs.readFileSync(path.join(compilerDir, 'package.json'))),
        soljsonSha256: sha256(compilerBytes),
        sourcePath: 'viairvault-input/ViaIrVault.sol',
        sourceBytes: Buffer.byteLength(source),
        sourceSha256: sha256(Buffer.from(source)),
        settings: input.settings,
        viaIR: true,
        runtimeBytes: runtime.length,
        runtimeSha256: sha256(runtime),
        abiFunctionCount: functionEntries.length,
        receiveEntryCount: contract.abi.filter(item => item.type === 'receive').length,
        fallbackEntryCount: contract.abi.filter(item => item.type === 'fallback').length,
        selectorCount: signatures.length,
        selectorsAgree,
        repeatRuntimeAbiAndMethodsByteEqual: outputEqual,
        warnings: (first.errors || []).filter(item => item.severity !== 'error').map(item => item.formattedMessage)
    };
    fs.writeFileSync(path.join(outDir, 'input.json'), inputText);
    fs.writeFileSync(path.join(outDir, 'output.json'), JSON.stringify(first, null, 2) + '\n');
    fs.writeFileSync(path.join(outDir, 'runtime.bin'), runtime);
    fs.writeFileSync(path.join(outDir, 'runtime.hex'), runtimeHex + '\n');
    fs.writeFileSync(path.join(outDir, 'creation.hex'), contract.evm.bytecode.object.toLowerCase() + '\n');
    fs.writeFileSync(path.join(outDir, 'abi.json'), JSON.stringify(contract.abi, null, 2) + '\n');
    fs.writeFileSync(path.join(outDir, 'method-identifiers.json'), JSON.stringify(methodIdentifiers, null, 2) + '\n');
    fs.writeFileSync(path.join(outDir, 'selector-census.json'), JSON.stringify({
        signatures,
        independentlyDerived,
        compilerMethodIdentifiers: methodIdentifiers,
        selectorsAgree,
        functionCount: signatures.length,
        receiveEntryCount: receipt.receiveEntryCount
    }, null, 2) + '\n');
    fs.writeFileSync(path.join(outDir, 'compile-receipt.json'), JSON.stringify(receipt, null, 2) + '\n');
    const result = {
        compiler: solc.version(),
        runtimeBytes: runtime.length,
        runtimeSha256: sha256(runtime),
        functionCount: signatures.length,
        receiveEntryCount: receipt.receiveEntryCount,
        selectorsAgree,
        repeatedDeterministically: outputEqual,
        outputDirectory: path.relative(root, outDir)
    };
    const matrixPath = path.join(root, 'compiled-viairvault', `solc-${solc.version().split('+')[0]}`, 'compile-matrix.json');
    fs.writeFileSync(matrixPath, JSON.stringify({
        source: sourcePath,
        sourceBytes: Buffer.byteLength(source),
        sourceSha256: sha256(Buffer.from(source)),
        jsSha3Version: require(path.resolve(process.env.JS_SHA3_MODULE || '/var/tmp/kaidoku-ex12/vendor/node_modules/js-sha3', 'package.json')).version,
        compilerSolcJsSha256: sha256(compilerBytes),
        result
    }, null, 2) + '\n');
    return result;
}

const result = compile();
console.log(JSON.stringify({ sourceSha256: sha256(Buffer.from(source)), result }, null, 2));
