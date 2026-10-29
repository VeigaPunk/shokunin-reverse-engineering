import re,html,sys
raw=open('snap/freebsd-sysexits.html',encoding='utf-8').read()
# anchors
anchors=[(m.start(),m.group(1)) for m in re.finditer(r'<a id="([A-Za-z_ ]+)" href="#end"><b>',raw)]
print(anchors)
def norm(t):
    t=re.sub(r'(?is)<script.*?</script>|<style.*?</style>',' ',t)
    t=re.sub(r'(?is)<a id="([A-Za-z_ ]+)" href="#end"><b>.*?</b></a>',lambda m:' \x01'+m.group(1)+'\x02 ',t)
    t=html.unescape(re.sub(r'(?s)<[^>]*>','',t)); return re.sub(r'\s+',' ',t)
n=norm(raw); q="EX_USAGE (64) The command was used incorrectly"
i=[m.start() for m in re.finditer(re.escape(q),n)]; print('hits',i)
best=None
for m in re.finditer('\x01(.*?)\x02',n):
    if m.start()<i[0]: best=m.group(1)
print('section',best)
for k in ('HISTORY','appeared in','4.0BSD','Berkeley','sysexits.h'):
    for m in re.finditer(re.escape(k),n): print(k, n[max(0,m.start()-80):m.start()+120]); break
sec=[(m.start(),m.group(1)) for m in re.finditer('\x01(.*?)\x02',n)]; print(sec)
