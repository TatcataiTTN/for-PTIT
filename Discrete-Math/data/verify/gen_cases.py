import json, random, sys, os, math
sys.path.insert(0,'../../build'); sys.path.insert(0,'../../build/orig')
import knap, tsp, orig_lib as OL
r=random.Random(20260929); cases=dict(incl=[],intsol=[],knap=[],tsp=[],next=[])
for _ in range(60):
    a=r.randint(1,300); b=a+r.randint(50,4000); ds=sorted(r.sample(range(2,16),r.choice([2,3])))
    cases['incl'].append(dict(a=a,b=b,ds=ds,ans=OL.count_div(a,b,ds)))
for _ in range(60):
    k=r.randint(3,6); N=r.randint(10,45); lo=[r.randint(0,4) for _ in range(k)]; hi=[(l+r.randint(1,7) if r.random()<0.5 else None) for l in lo]
    cases['intsol'].append(dict(N=N,lo=lo,hi=hi,ans=str(OL.dp_bounded(N,lo,hi))))
for _ in range(80):
    n=r.randint(3,8); v=[r.randint(1,20) for _ in range(n)]; w=[r.randint(1,12) for _ in range(n)]; b=r.randint(4,30)
    res=knap.bb(v,w,b); cases['knap'].append(dict(v=v,w=w,b=b,fopt=res['fopt'],nodes=len(res['nodes']),pruned=sum(1 for x in res['nodes'] if x['st']=='pruned')))
for _ in range(80):
    n=r.randint(4,7); C=[[0 if i==j else r.randint(1,30) for j in range(n)] for i in range(n)]
    res=tsp.bb(C); cases['tsp'].append(dict(C=C,cost=res['cost'],root=res['root']))
import itertools
for _ in range(60):
    n=r.randint(4,9); p=r.sample(range(1,n+1),n)
    cases['next'].append(dict(kind='perm',x=p))
json.dump(cases,open('cases.json','w'))
print({k:len(v) for k,v in cases.items()})
