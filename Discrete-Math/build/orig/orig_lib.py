import math, itertools, re
from fractions import Fraction as Fr
def sub(n): return ''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(n))
def T(t): return '('+', '.join(map(str,t))+')'
def dp_bounded(N,lo,hi):
    k=len(lo); dp=[1]+[0]*N
    for i in range(k):
        nd=[0]*(N+1)
        for t in range(N+1):
            if dp[t]:
                top=N-t if hi[i] is None else min(hi[i],N-t)
                for v in range(lo[i],top+1): nd[t+v]+=dp[t]
        dp=nd
    return dp[N]
def int_sol(N,lo,hi):
    """trả (đáp án, lời giải văn bản) cho số nghiệm nguyên với cận lo<=x<=hi"""
    k=len(lo); base=N-sum(lo); ans=dp_bounded(N,lo,hi)
    if base<0: return 0,f'Tổng các cận dưới = {sum(lo)} > {N} nên không có nghiệm.'
    idx=[i for i in range(k) if hi[i] is not None]
    lines=[f'Bước 1: đặt yᵢ = xᵢ − (cận dưới) ≥ 0 ⇒ y₁+…+y_{k} = {N} − {sum(lo)} = {base}; các biến bị chặn trên có yᵢ ≤ hᵢ − lᵢ.']
    total=0; terms=[]
    for m in range(1<<len(idx)):
        sel=[idx[j] for j in range(len(idx)) if m>>j&1]; s=sum(hi[i]-lo[i]+1 for i in sel); rem=base-s
        c=math.comb(rem+k-1,k-1) if rem>=0 else 0; sg=-1 if len(sel)%2 else 1; total+=sg*c
        name='không vi phạm cận' if not sel else 'vượt cận trên của '+', '.join(f'x{sub(i+1)}' for i in sel)
        terms.append(f'  {"+" if sg>0 else "−"} C({rem}+{k}−1,{k}−1) = {c}   ({name})' if rem>=0 else f'  {"+" if sg>0 else "−"} 0   ({name}: tổng còn âm)')
    lines.append('Bước 2 (nguyên lý bù trừ theo các cận trên):\n'+'\n'.join(terms))
    assert total==ans,(total,ans)
    lines.append(f'Kết quả: {ans}.')
    return ans,'\n'.join(lines)
def wrong_for_int_sol(N,lo,hi):
    k=len(lo); base=N-sum(lo); ws=set()
    ws.add(math.comb(base+k-1,k-1))
    ws.add(math.comb(N+k-1,k-1))
    idx=[i for i in range(k) if hi[i] is not None]
    if idx:
        i=idx[0]; s=hi[i]-lo[i]+1; rem=base-s
        ws.add(math.comb(base+k-1,k-1)-(math.comb(rem+k-1,k-1) if rem>=0 else 0))
    return ws
def count_div(a,b,ds):
    return sum(1 for x in range(a,b+1) if any(x%d==0 for d in ds))
def incl_text(a,b,ds,neg=False):
    parts=[];tot=0
    for m in range(1,1<<len(ds)):
        sel=[ds[i] for i in range(len(ds)) if m>>i&1]; l=1
        for d in sel: l=l*d//math.gcd(l,d)
        c=b//l-(a-1)//l; sg=1 if len(sel)%2 else -1; tot+=sg*c
        parts.append(f'  {"+" if sg>0 else "−"} #chia hết cho BCNN({", ".join(map(str,sel))}) = {l}: ⌊{b}/{l}⌋ − ⌊{a-1}/{l}⌋ = {c}')
    s='Nguyên lý bù trừ với các bội chung nhỏ nhất:\n'+'\n'.join(parts)+f'\nSố chia hết cho ít nhất một số = {tot}.'
    if neg: s+=f'\nSố KHÔNG chia hết cho số nào = {b-a+1} − {tot} = {b-a+1-tot}.'
    return tot,s
def pal_count(L,N):
    h=(L+1)//2; c=0
    for d in itertools.product(range(10),repeat=h):
        if d[0]==0: continue
        if 2*sum(d)-(d[-1] if L%2 else 0)==N: c+=1
    return c
# ---- DP đếm xâu theo mẫu để lập truy hồi
def count_strings(B,pred,n):
    """vét cạn (B^n nhỏ)"""
    return sum(1 for s in itertools.product(range(B),repeat=n) if pred(s))
def has_run(s,d,k):
    r=0
    for c in s:
        r=r+1 if c==d else 0
        if r>=k: return True
    return False
def find_recurrence(seq,B,maxk=3):
    """tìm truy hồi a_n = sum c_i a_{n-i} + e*B^{n-m} khớp toàn bộ dãy seq (dict n->a_n, n>=1)."""
    N=max(seq); best=None
    for k in range(1,maxk+1):
        for m in list(range(0,k+2))+[None]:
            unk=k+(1 if m is not None else 0)
            rows=[]
            for n in range(k+1,N+1):
                if all((n-i) in seq for i in range(1,k+1)):
                    r=[Fr(seq[n-i]) for i in range(1,k+1)]
                    if m is not None: r.append(Fr(B)**(n-m))
                    r.append(Fr(seq[n])); rows.append(r)
            if len(rows)<unk+2: continue
            # giải bình phương tối thiểu chính xác: Gauss trên unk hàng đầu rồi kiểm tra các hàng còn lại
            M=[r[:] for r in rows]; piv=[]; ri=0
            for c in range(unk):
                p=next((i for i in range(ri,len(M)) if M[i][c]!=0),None)
                if p is None: continue
                M[ri],M[p]=M[p],M[ri]; pv=M[ri][c]; M[ri]=[x/pv for x in M[ri]]
                for i in range(len(M)):
                    if i!=ri and M[i][c]!=0:
                        f=M[i][c]; M[i]=[x-f*y for x,y in zip(M[i],M[ri])]
                piv.append(c); ri+=1
            if any(M[i][unk]!=0 and all(M[i][j]==0 for j in range(unk)) for i in range(len(M))): continue
            if len(piv)<unk: continue
            sol=[M[i][unk] for i in range(unk)]
            if all(x.denominator==1 for x in sol):
                return dict(k=k,m=m,c=[int(x) for x in sol[:k]],e=int(sol[k]) if m is not None else 0)
    return None
def rec_text(rec,B):
    if rec is None: return None
    parts=[]
    for i,c in enumerate(rec['c'],1):
        if c==0: continue
        t=(str(abs(c)) if abs(c)!=1 else '')+f'aₙ₋{sub(i)}'
        parts.append(('−' if c<0 else ('+' if parts else ''))+(' ' if parts else '')+t if parts else (('−' if c<0 else '')+t))
    if rec['m'] is not None and rec['e']!=0:
        e=rec['e']; ex=f'{B}ⁿ' if rec['m']==0 else f'{B}ⁿ⁻{sub(rec["m"])}'.replace('₁','¹').replace('₂','²').replace('₃','³')
        t=(str(abs(e)) if abs(e)!=1 else '')+('·' if abs(e)!=1 else '')+ex
        parts.append((('− ' if e<0 else '+ ') if parts else ('−' if e<0 else ''))+t)
    return 'aₙ = '+' '.join(parts).replace('  ',' ')
