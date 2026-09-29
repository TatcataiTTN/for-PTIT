import itertools
INF=float('inf')
def reduce(A,rows,cols):
    s=0; rc=[];cc=[]
    for i in rows:
        m=min(A[i][j] for j in cols); rc.append(m)
        if 0<m<INF:
            s+=m
            for j in cols:
                if A[i][j]<INF: A[i][j]-=m
        elif m==INF: rc[-1]=0
    for j in cols:
        m=min(A[i][j] for i in rows); cc.append(m if m<INF else 0)
        if 0<m<INF:
            s+=m
            for i in rows:
                if A[i][j]<INF: A[i][j]-=m
    return s,rc,cc
def best_edge(A,rows,cols):
    beta=-1;best=None
    for i in rows:
        for j in cols:
            if A[i][j]==0:
                mr=min([A[i][k] for k in cols if k!=j] or [INF]); mc=min([A[k][j] for k in rows if k!=i] or [INF])
                t=mr+mc
                if t>beta: beta=t;best=(i,j)
    return best,beta
def brute(C):
    n=len(C); best=INF; bt=None; cnt=0
    for p in itertools.permutations(range(1,n)):
        cost=C[0][p[0]]+sum(C[p[i]][p[i+1]] for i in range(n-2))+C[p[-1]][0]
        if cost<best: best=cost; bt=(0,)+p+(0,)
    return best,bt
def bb(C):
    n=len(C); best=[INF,None]; log=[]
    def isTour(edges):
        d=dict(edges); k=0;cnt=0
        while True:
            if k not in d: return False
            k=d[k];cnt+=1
            if k==0 or cnt>n: break
        return cnt==n and k==0
    def node(A,rows,cols,edges,bound,depth,label):
        if bound>=best[0]: log.append((depth,label,bound,'cut')); return
        if len(rows)==2:
            u,v=rows; w,x=cols
            for o in ([(u,w),(v,x)],[(u,x),(v,w)]):
                if all(A[a][b]<INF for a,b in o) and isTour(edges+o):
                    allE=edges+o; cost=sum(C[a][b] for a,b in allE)
                    log.append((depth,label,bound,'record' if cost<best[0] else 'leaf',cost))
                    if cost<best[0]: best[0]=cost; best[1]=allE
                    return
            log.append((depth,label,bound,'dead')); return
        be,beta=best_edge(A,rows,cols)
        if be is None: log.append((depth,label,bound,'dead')); return
        r,c=be; log.append((depth,label,bound,'branch',(r+1,c+1),beta))
        A1=[row[:] for row in A]; e1=edges+[(r,c)]
        inv={b:a for a,b in e1}; d1=dict(e1)
        i1=r
        while i1 in inv: i1=inv[i1]
        jk=c
        while jk in d1: jk=d1[jk]
        rows1=[x for x in rows if x!=r]; cols1=[x for x in cols if x!=c]
        if jk in rows1 and i1 in cols1: A1[jk][i1]=INF
        s1,_,_=reduce(A1,rows1,cols1)
        node(A1,rows1,cols1,e1,bound+s1,depth+1,f'chứa ({r+1},{c+1})')
        A2=[row[:] for row in A]; A2[r][c]=INF; s2,_,_=reduce(A2,rows,cols)
        node(A2,rows,cols,edges,bound+s2,depth+1,f'không chứa ({r+1},{c+1})')
    A=[[INF if i==j else C[i][j] for j in range(n)] for i in range(n)]
    rows=list(range(n)); cols=list(range(n))
    root,rc,cc=reduce(A,rows,cols); log.append((0,'gốc',root,'root'))
    node(A,rows,cols,[],root,0,'gốc')
    d=dict(best[1]); tour=[1]; k=0
    for _ in range(n): k=d[k]; tour.append(k+1)
    return dict(cost=best[0],tour=tour,root=root,log=log,rc=rc,cc=cc)
if __name__=='__main__':
    import random
    r=random.Random(3); bad=0
    for _ in range(500):
        n=r.randint(4,7); C=[[0 if i==j else r.randint(1,30) for j in range(n)] for i in range(n)]
        if bb(C)['cost']!=brute(C)[0]: bad+=1
    print('mismatch',bad)
