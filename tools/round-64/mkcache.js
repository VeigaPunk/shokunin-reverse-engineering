const vm=require('vm'),fs=require('fs');
const src="function add(a,b){return a+b}; function mul(a,b){return a*b} add(1,2); mul(3,4);";
const s=new vm.Script(src,{filename:'probe.js'});
fs.writeFileSync('/fast/scratch/hyaku/kaidoku-r64/lead/probe-electron.jsc', s.createCachedData());
console.log('v8', process.versions.v8, 'bytes', s.createCachedData().length);
