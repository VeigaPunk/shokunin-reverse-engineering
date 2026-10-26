"""Direct probes of c1-counter.carriers_spec external-carrier validation."""
import copy
import importlib.util
import json

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
c = importlib.util.spec_from_file_location('c1c', L + '/tools/round-40/c1-counter.py')
m = importlib.util.module_from_spec(c)
c.loader.exec_module(m)
spec = json.load(open(L + '/.ufo/waves/round-40/c1/carriers.json'))
IDS = ('V1', 'V2', 'L1', 'L2')


def probe(name, mutate):
    s = copy.deepcopy(spec)
    mutate(s)
    ids, probs = m.carriers_spec(s, 4, IDS)
    print('%-28s probs=%s' % (name, probs))


probe('pristine (frozen spec)', lambda s: None)


def both(s):
    s['carriers'][0]['path'] = 'corpus/evidence/round-40/c1/V1/carrier.sqsh'


probe('path AND external', both)


def no_url(s):
    del s['carriers'][0]['external']['url']


probe('external without url', no_url)


def bad_isha(s):
    s['carriers'][0]['external']['image_sha256'] = 'zz'


probe('external bad image_sha256', bad_isha)


def ext_str(s):
    s['carriers'][0]['external'] = 'vendor.bin'


probe('external not an object', ext_str)


def drop_msha(s):
    del s['carriers'][0]['external']['member_sha256']


probe('member_sha256 dropped', drop_msha)


def wrong_msha(s):
    s['carriers'][0]['external']['member_sha256'] = '0' * 64


probe('member_sha256 wrong value', wrong_msha)


def no_sha(s):
    del s['carriers'][0]['sha256']


probe('carrier without sha256', no_sha)


def up_pin(s):
    s['carriers'][0]['sha256'] = s['carriers'][0]['sha256'].upper()


probe('uppercase pin', up_pin)
