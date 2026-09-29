import itertools
from fractions import Fraction as Fr
def brute(v,w,b):
    n=len(v); best=-1; bx=None; feas=0
    for x in itertools.product((0,1),repeat=n):
        W=sum(a*c for a,c in zip(w,x))
        if W<=b:
            feas+=1; V=sum(a*c for a,c in zip(v,x))
            if V>best: best=V; bx=x
    return best,bx,feas
def bb(v,w,b,unlimited=False):
    n=len(v); order=sorted(range(n),key=lambda i:(-Fr(v[i],w[i]),i))
    C=[v[i] for i in order]; A=[w[i] for i in order]
    state=dict(fopt=-1,xopt=None,nodes=[],updates=[])
    x=[0]*n
    def bound(k,delta,bk): return delta+Fr(C[k]*bk,A[k]) if k<n else Fr(delta)
    state['nodes'].append(dict(x=(),delta=0,rem=b,g=bound(0,0,b),st='root'))
    def rec(k,delta,bk):
        t=bk//A[k] if unlimited else min(1,bk//A[k])
        for j in range(t,-1,-1):
            x[k]=j; d2=delta+C[k]*j; b2=bk-A[k]*j; g=bound(k+1,d2,b2)
            node=dict(x=tuple(x[:k+1]),delta=d2,rem=b2,g=g)
            state['nodes'].append(node)
            if k==n-1:
                if d2>state['fopt']:
                    state['fopt']=d2; state['xopt']=tuple(x); node['st']='record'; state['updates'].append(d2)
                else: node['st']='leaf'
            elif g>state['fopt']:
                node['st']='expand'; rec(k+1,d2,b2)
            else: node['st']='pruned'
    rec(0,0,b)
    xo=[0]*n
    for pos,orig in enumerate(order): xo[orig]=state['xopt'][pos]
    return dict(order=order,C=C,A=A,fopt=state['fopt'],xopt=tuple(xo),nodes=state['nodes'],updates=state['updates'])
if __name__=='__main__':
    import random
    r=random.Random(1); bad=0
    for _ in range(3000):
        n=r.randint(3,8); v=[r.randint(1,20) for _ in range(n)]; w=[r.randint(1,12) for _ in range(n)]; b=r.randint(4,30)
        bf=brute(v,w,b)
        try: res=bb(v,w,b)
        except Exception as e: bad+=1; continue
        if res['fopt']!=bf[0]: bad+=1
    print('mismatch',bad)
