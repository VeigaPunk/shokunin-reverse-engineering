#!/usr/bin/env python3
"""Owned inert ar fixtures; expected records derived from construction, not parsing."""
import hashlib,json,pathlib,sys
H=lambda b:hashlib.sha256(b).hexdigest()
def header(name,n):
    assert len(name)<=16
    return name.ljust(16,b' ')+b'0'.ljust(12)+b'0'.ljust(6)+b'0'.ljust(6)+b'100644'.ljust(8)+str(n).encode().ljust(10)+b'`\n'
def build(items):
    out=b'!<arch>\n'; records=[]
    for raw,body,name,kind,skip in items:
        records.append(dict(ordinal=len(records),header_offset=len(out),kind=kind,name=name,stored_size=len(body),payload_size=len(body)-skip,payload_sha256=H(body[skip:])))
        out+=header(raw,len(body))+body+(b'\n' if len(body)%2 else b'')
    return out,dict(schema=1,exit=0,finding='complete',archive_sha256=H(out),archive_size=len(out),occurrences=records)
def main(out,salt):
    out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=False); cases={}; digest=hashlib.sha256(salt.encode()).digest(); p=digest[:7+2*(digest[0]%4)]; tag=digest.hex()[:2+digest[1]%5]
    def good(key,items):
        b,e=build(items); (out/(key+'.ar')).write_bytes(b);cases[key]=dict(exit=0,archive_sha256=H(b),output=e)
    def bad(key,b,code,reason):
        (out/(key+'.ar')).write_bytes(b);cases[key]=dict(exit=code,archive_sha256=H(b),output=dict(schema=1,exit=code,finding=reason))
    m=lambda n,b:((tag+n).encode()+b'/',b,tag+n,'member',0)
    good('empty',[]);good('short_odd_even',([m('odd.o',p),m('even.o',p+b'X')][::(-1 if digest[2]%2 else 1)]));good('plain_bsd',[(b'plain.o',p,'plain.o','member',0)])
    good('duplicate_names',[m('same.o',p),m('same.o',p[::-1])]);good('metadata_path',[(b'../outside/',p,'../outside','member',0)])
    first=(tag+'first-long-object.o').encode(); second=(tag+'second-long-object.o').encode(); table=first+b'/\n'+second+b'/\n';off=len(first)+2
    good('gnu_offset',[(b'/',b'\0\0\0\0','/','symbol_table',0),(b'//',table,'//','name_table',0),(('/'+str(off)).encode(),p,second.decode(),'member',0),(b'/0',p+b'X',first.decode(),'member',0)])
    name=(tag+'long object member.o').encode();good('bsd_inline',[(b'#1/'+str(len(name)).encode(),name+p,name.decode(),'member',len(name)),m('after.o',p+b'X')])
    good('bsd_empty_payload',[(b'#1/3',b'abc','abc','member',3)])
    good('member_boundary',[m('large.o',b'Z'*65536)]);good('count_boundary',[m('x.o',b'')]*128)
    normal=build([m('x.o',p)])[0]
    bad('thin_external',b'!<thin>\n'+header(b'../../outside/',99),2,'thin_archive')
    bad('bad_magic',b'not ar!!'+normal[8:],1,'bad_magic')
    bad('header_truncated',b'!<arch>\n'+b'X'*59,1,'truncated_header')
    bad('terminator_bad',normal[:66]+b'XX'+normal[68:],1,'bad_terminator')
    for key,size in [('negative_size',b'-1'),('nondigit_size',b'1x'),('leading_space_size',b' 7')]:
        bad(key,normal[:56]+size.ljust(10)+normal[66:],1,'bad_size')
    bad('payload_truncated',b'!<arch>\n'+header(b'x/',len(p)+1)+p,1,'truncated_payload')
    bad('pad_missing',normal[:-1],1,'bad_padding');bad('pad_bad',normal[:-1]+b'X',1,'bad_padding')
    bad('member_budget',b'!<arch>\n'+header(b'x/',65537)+b'Z'*65537+b'\n',2,'member_budget')
    bad('count_budget',build([m('x.o',b'')]*129)[0],2,'count_budget')
    bad('archive_budget',b'Z'*1048577,2,'archive_budget')
    bad('gnu_missing_table',build([(b'/0',p,'?', 'member',0)])[0],1,'bad_name_reference')
    for key,ref in [('gnu_mid_entry',b'/1'),('gnu_past_end',b'/999')]:
        bad(key,build([(b'//',table,'//','name_table',0),(ref,p,'?','member',0)])[0],1,'bad_name_reference')
    bad('gnu_unterminated_table',build([(b'//',b'longname','//','name_table',0)])[0],1,'bad_name_table')
    bad('gnu_duplicate_table',build([(b'//',table,'//','name_table',0)]*2)[0],1,'bad_name_table')
    bad('bsd_name_overflow',build([(b'#1/99',p,'?','member',0)])[0],1,'bad_bsd_length')
    bad('bsd_zero_length',build([(b'#1/0',p,'?','member',0)])[0],1,'bad_bsd_length')
    bad('bsd_nul_name',build([(b'#1/3',b'a\0b'+p,'?','member',0)])[0],2,'unsupported_name')
    bad('variant_sym64',build([(b'/SYM64/',p,'?','member',0)])[0],2,'unsupported_variant')
    bad('nonascii_name',build([(b'\xff/',p,'?','member',0)])[0],2,'unsupported_name')
    (out/'expected.json').write_text(json.dumps(cases,indent=2,sort_keys=True)+'\n')
    return cases
if __name__=='__main__':main(*sys.argv[1:])
