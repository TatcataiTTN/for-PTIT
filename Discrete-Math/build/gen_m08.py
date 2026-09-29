from qcore import *
from fractions import Fraction as Fr
import itertools, math
SUP=str.maketrans('n','ⁿ')
def sub(n): return ''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(n))
def sg(x): return '−' if x<0 else '+'
def term(coef,r,j):
    """coef * n^j * r^n"""
    c=abs(coef); cs='' if c==1 and True else str(c)
    base=(f'({r})ⁿ' if r<0 else (f'{r}ⁿ' if r!=1 else ''))
    pw='' if j==0 else ('n' if j==1 else f'n^{j}')
    parts=[p for p in (cs,pw,base) if p]
    if not parts: return '1'
    return '·'.join(parts) if (cs and (pw or base)) or (pw and base) else parts[0]
def formula(items):
    """items: list of (coef,r,j) -> chuỗi aₙ = ..."""
    out=''
    first=True
    for coef,r,j in items:
        if coef==0: continue
        t=term(coef,r,j)
        if first: out+=('−' if coef<0 else '')+t; first=False
        else: out+=' '+sg(coef)+' '+t
    return 'aₙ = '+(out or '0')
def ev(items,n): return sum(Fr(c)*Fr(n)**j*Fr(r)**n if not(j and n==0) else Fr(0) for c,r,j in items) if True else 0
def evf(items,n):
    t=Fr(0)
    for c,r,j in items:
        t+=Fr(c)*(Fr(n)**j if (j>0 and n>0) else (Fr(1) if j==0 else Fr(0)))*Fr(r)**n
    return t
def seq(cs,a0,N):
    a=list(a0)
    for n in range(len(cs),N+1): a.append(sum(c*a[n-1-i] for i,c in enumerate(cs)))
    return a
def solve_lin(rootspec,a0):
    """rootspec: list of (r,mult); trả về coefs cho basis n^j r^n bằng Fraction (giải hệ)"""
    basis=[(r,j) for r,m in rootspec for j in range(m)]
    k=len(basis)
    M=[[Fr(r)**n*(Fr(n)**j if not(j>0 and n==0) else 0) if not(j>0 and n==0) else Fr(0) for (r,j) in basis]+[Fr(a0[n])] for n in range(k)]
    for n in range(k):
        for q,(r,j) in enumerate(basis):
            M[n][q]=Fr(r)**n*(Fr(n)**j if j>0 and n>0 else (Fr(1) if j==0 else Fr(0)))
    for col in range(k):
        piv=next(i for i in range(col,k) if M[i][col]!=0); M[col],M[piv]=M[piv],M[col]
        pv=M[col][col]; M[col]=[x/pv for x in M[col]]
        for r2 in range(k):
            if r2!=col and M[r2][col]!=0:
                f=M[r2][col]; M[r2]=[x-f*y for x,y in zip(M[r2],M[col])]
    return [(M[i][k],basis[i][0],basis[i][1]) for i in range(k)]
def poly_from_roots(rs):
    p=[1]
    for r in rs: p=[a-r*b for a,b in itertools.zip_longest(p+[0],[0]+p,fillvalue=0)]
    return p
def P2(cs):
    s='r²'
    if cs[0]!=0: s+=(' − ' if cs[0]>0 else ' + ')+(str(abs(cs[0])) if abs(cs[0])!=1 else '')+'r'
    if cs[1]!=0: s+=(' − ' if cs[1]>0 else ' + ')+str(abs(cs[1]))
    return s
def P3(cs):
    s='r³'
    for c,pw in zip(cs,['r²','r','']):
        if c!=0: s+=(' − ' if c>0 else ' + ')+(str(abs(c)) if (abs(c)!=1 or not pw) else '')+pw
    return s
def fac(r): return f'(r − {r})' if r>0 else (f'(r + {-r})' if r<0 else 'r')
def gen(seed=8):
    B=Bank('m08',seed); rng=B.rng
    def make(rootspec,integer_coefs=True):
        rs=[r for r,m in rootspec for _ in range(m)]
        p=poly_from_roots(rs)   # x^k + p1 x^{k-1}+..
        cs=[-c for c in p[1:]]
        k=len(cs)
        for _ in range(200):
            a0=[rng.randint(-9,15) for _ in range(k)]
            if not any(a0): continue
            sol=solve_lin(rootspec,a0)
            if all(c.denominator==1 for c,_,_ in sol) and all(c!=0 for c,_,_ in sol): return cs,a0,[(int(c),r,j) for c,r,j in sol]
        return None
    def rec_txt(cs):
        k=len(cs); s=f'aₙ = '; first=True
        for i,c in enumerate(cs):
            if c==0: continue
            v=f'aₙ₋{sub(i+1)}'; t=(str(abs(c)) if abs(c)!=1 else '')+v
            s+=('−' if c<0 else '')+t if first else f' {sg(c)} {t}'; first=False
        return s
    def variants(items):
        vs=set(); base=formula(items)
        for i in range(len(items)):
            c,r,j=items[i]
            for alt in [(-c,r,j),(c,-r,j),(c+1,r,j),(c-1,r,j),(c*2,r,j)]:
                it=list(items); it[i]=alt; vs.add(tuple(it))
        if len(items)>=2:
            it=list(items); it[0],it[1]=(items[1][0],items[0][1],items[0][2]),(items[0][0],items[1][1],items[1][2]); vs.add(tuple(it))
        return [list(v) for v in vs]
    def valid(items,cs,a0,N=8):
        seqv=seq(cs,a0,N)
        return all(evf(items,n)==seqv[n] for n in range(N+1))
    # ---- bậc 2: hai nghiệm phân biệt / nghiệm kép
    specs2=[]
    for r1 in range(-8,9):
        for r2 in range(r1+1,9):
            if r1 and r2 and abs(r1)+abs(r2)>3: specs2.append([(r1,1),(r2,1)])
    for r in range(-9,10):
        if r: specs2.append([(r,2)])
    rng.shuffle(specs2)
    cnt2=0
    for sp in specs2:
        m=make(sp)
        if not m: continue
        cs,a0,items=m
        if not valid(items,cs,a0): continue
        ans=formula(items)
        bad=[formula(v) for v in variants(items) if not valid(v,cs,a0)]
        bad=[b for b in dict.fromkeys(bad) if b!=ans]
        if len(bad)<3: continue
        double=len(sp)==1
        rt=', '.join(f'r = {r}'+(' (nghiệm kép)' if mm==2 else '') for r,mm in sp)
        eq=f'r² {sg(-cs[0])} {abs(cs[0])}r {sg(-cs[1])} {abs(cs[1])} = 0'.replace('+ 0r','').replace('- ','− ')
        seqv=seq(cs,a0,6)
        expl=(f'Phương trình đặc trưng: {P2(cs)} = 0 có nghiệm {rt}.\n'+
              ('Nghiệm kép r ⇒ aₙ = (α + βn)·rⁿ.' if double else 'Hai nghiệm phân biệt ⇒ aₙ = α·r₁ⁿ + β·r₂ⁿ.')+
              f'\nThay a₀ = {a0[0]}, a₁ = {a0[1]} giải α, β: {formula(items)}.\nKiểm tra: '+', '.join(f'a{sub(i)}={seqv[i]}' for i in range(0,5))+' (khớp công thức).')
        if B.add(f'Nghiệm riêng của hệ thức truy hồi {rec_txt(cs)} (n ≥ 2), a₀ = {a0[0]}, a₁ = {a0[1]} là:',ans,rng.sample(bad,3),expl,level=3 if not double else 3,topic='Giải bậc 2'): cnt2+=1
        if cnt2>=70: break
    # ---- bậc 3
    specs3=[]
    for r1 in range(-7,8):
        for r2 in range(r1+1,8):
            for r3 in range(r2+1,8):
                if len({abs(x) for x in (r1,r2,r3)})>=2 and 0 not in (r1,r2,r3): specs3.append([(r1,1),(r2,1),(r3,1)])
    for r in range(-6,7):
        for s in range(-6,7):
            if r and s and r!=s: specs3.append([(r,2),(s,1)])
    for r in range(-4,5):
        if r: specs3.append([(r,3)])
    rng.shuffle(specs3); cnt3=0
    for sp in specs3:
        m=make(sp)
        if not m: continue
        cs,a0,items=m
        if max(abs(c) for c in cs)>400 or not valid(items,cs,a0): continue
        ans=formula(items); bad=[formula(v) for v in variants(items) if not valid(v,cs,a0)]; bad=[b for b in dict.fromkeys(bad) if b!=ans]
        if len(bad)<3: continue
        seqv=seq(cs,a0,6); rt=', '.join(f'r = {r}'+(f' (bội {mm})' if mm>1 else '') for r,mm in sp)
        expl=(f'Phương trình đặc trưng: {P3(cs)} = 0 có nghiệm {rt}.\nNghiệm tổng quát là tổ hợp tuyến tính của các rⁿ (nghiệm bội m thêm các nhân tử n, n², …, n^(m−1)).\nThay a₀, a₁, a₂ để giải hệ 3 ẩn: {formula(items)}.\nKiểm tra: '+', '.join(f'a{sub(i)}={seqv[i]}' for i in range(0,5))+'.')
        if B.add(f'Giải hệ thức truy hồi aₙ₊₃ = {rec_txt(cs).replace("aₙ = ","").replace("aₙ₋₁","aₙ₊₂").replace("aₙ₋₂","aₙ₊₁").replace("aₙ₋₃","aₙ")} (n ≥ 0), a₀ = {a0[0]}, a₁ = {a0[1]}, a₂ = {a0[2]}.',ans,rng.sample(bad,3),expl,level=3,topic='Giải bậc 3'): cnt3+=1
        if cnt3>=50: break
    # ---- tính số hạng
    for _ in range(40):
        k=rng.choice([2,2,3]); cs=[rng.randint(-5,6) for _ in range(k)]
        if cs[-1]==0: continue
        a0=[rng.randint(-4,6) for _ in range(k)]; n=rng.randint(k+2,k+5); a=seq(cs,a0,n)
        B.add(f'Cho aₙ = {rec_txt(cs).replace("aₙ = ","")} với '+', '.join(f'a{sub(i)} = {a0[i]}' for i in range(k))+f'. Giá trị a{sub(n)} là:'.replace('aₙ = ','').replace('aₙ₋','aₙ₋'),a[n],near_ints(a[n],rng,7)+[a[n-1]+a[n-2]],f'Tính lần lượt: '+', '.join(f'a{sub(i)}={a[i]}' for i in range(k,n+1))+'.',level=1,topic='Tính số hạng')
    # ---- phương trình đặc trưng và nghiệm
    for _ in range(60):
        if rng.random()<0.5:
            r1,r2=rng.sample([x for x in range(-7,8) if x],2); cs=[r1+r2,-r1*r2]
            rec=rec_txt(cs); ans=P2(cs)+' = 0'
            wr=[P2([-cs[0],cs[1]])+' = 0',P2([cs[0],-cs[1]])+' = 0',P2([-cs[0],-cs[1]])+' = 0',P2([cs[1],cs[0]])+' = 0']
            wr=[w for w in dict.fromkeys(wr) if w!=ans]
            if len(wr)<3: continue
            B.add(f'Phương trình đặc trưng của {rec} là:',P2(cs)+' = 0',wr,f'aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ ⇒ r² = c₁r + c₂ ⇒ r² − c₁r − c₂ = 0 với c₁ = {cs[0]}, c₂ = {cs[1]}: {P2(cs)} = 0. Nghiệm: r = {r1}, r = {r2}.',level=1,topic='Phương trình đặc trưng')
        else:
            r1,r2=rng.sample([x for x in range(-7,8) if x],2); cs=[r1+r2,-r1*r2]
            B.add(f'Các nghiệm đặc trưng của {rec_txt(cs)} là:',f'r = {min(r1,r2)} và r = {max(r1,r2)}',[f'r = {-r1} và r = {-r2}',f'r = {r1+r2} và r = {r1*r2}',f'r = {abs(r1)} và r = {abs(r2)}'] if {abs(r1),abs(r2)}!={r1,r2} else [f'r = {-r1} và r = {-r2}',f'r = {r1+r2} và r = {r1*r2}',f'r = {r1+1} và r = {r2+1}'],f'{P2(cs)} = 0 ⇔ {fac(r1)}{fac(r2)} = 0 (tổng nghiệm = {cs[0]}, tích nghiệm = {-cs[1]}).',level=2,topic='Phương trình đặc trưng')
    # ---- dạng nghiệm tổng quát khi biết nghiệm
    forms=[([(2,1),(3,1)],'aₙ = α·2ⁿ + β·3ⁿ'),([(2,2)],'aₙ = (α + βn)·2ⁿ'),([(-1,1),(4,1)],'aₙ = α·(−1)ⁿ + β·4ⁿ'),([(5,2)],'aₙ = (α + βn)·5ⁿ'),([(1,1),(2,2)],'aₙ = α + (β + γn)·2ⁿ'),([(3,3)],'aₙ = (α + βn + γn²)·3ⁿ'),([(1,1),(-1,1),(2,1)],'aₙ = α + β·(−1)ⁿ + γ·2ⁿ'),([(-2,2),(3,1)],'aₙ = (α + βn)·(−2)ⁿ + γ·3ⁿ')]
    for sp,f in forms:
        others=[g for _,g in forms if g!=f]
        rt='; '.join(f'r = {r}'+(f' bội {m}' if m>1 else '') for r,m in sp)
        for tag in range(2):
            B.add(f'Phương trình đặc trưng của một hệ thức truy hồi tuyến tính thuần nhất có các nghiệm: {rt}. Dạng nghiệm tổng quát là:',f,rng.sample(others,3),f'Mỗi nghiệm r bội m đóng góp (α₀ + α₁n + … + α_(m−1)n^(m−1))·rⁿ. Tổng hợp: {f}.',level=2,topic='Dạng nghiệm')
    # ---- tìm hệ số
    for _ in range(35):
        r1,r2=sorted(rng.sample([x for x in range(-5,7) if x],2)); al=rng.randint(-5,5) or 2; be=rng.randint(-5,5) or 3
        a0=al+be; a1=al*r1+be*r2
        B.add(f'Nghiệm của một hệ thức truy hồi có dạng aₙ = α·({r1})ⁿ + β·({r2})ⁿ, biết a₀ = {a0}, a₁ = {a1}. Cặp (α, β) là:',f'({al}, {be})',[f'({be}, {al})',f'({al+1}, {be-1})',f'({-al}, {-be})'] if al!=be else [f'({al+1}, {be})',f'({al}, {be+1})',f'({-al}, {-be})'],f'Thay n = 0: α + β = {a0}. Thay n = 1: {r1}α + {r2}β = {a1}. Lấy phương trình thứ hai trừ {r1} lần phương trình đầu: ({r2 - r1})β = {a1 - r1*a0} ⇒ β = {be}; suy ra α = {a0} − ({be}) = {al}.',level=2,topic='Tìm hệ số')
    return B
def essays(B):
    ex=[('Giải hệ thức truy hồi aₙ = −14aₙ₋₁ − 49aₙ₋₂ (n ≥ 2), a₀ = 3, a₁ = 35. (đề 2017-2020)','r² + 14r + 49 = 0 ⇔ (r + 7)² = 0 ⇒ nghiệm kép r = −7.\naₙ = (α + βn)(−7)ⁿ. a₀ = α = 3; a₁ = (3 + β)(−7) = 35 ⇒ 3 + β = −5 ⇒ β = −8.\nVậy aₙ = (3 − 8n)(−7)ⁿ = 3(−7)ⁿ − 8n(−7)ⁿ. Kiểm tra a₂ = −14·35 − 49·3 = −637; công thức: (3−16)·49 = −637 ✓.'),
        ('Giải aₙ = aₙ₋₁ + 2aₙ₋₂, a₀ = 2, a₁ = 7. (ví dụ giáo trình 2016)','r² − r − 2 = 0 ⇒ r = 2, r = −1. aₙ = α2ⁿ + β(−1)ⁿ; α+β = 2, 2α − β = 7 ⇒ α = 3, β = −1. Vậy aₙ = 3·2ⁿ − (−1)ⁿ.'),
        ('Giải aₙ = 6aₙ₋₁ − 9aₙ₋₂, a₀ = 1, a₁ = 6. (Lưu ý: giáo trình 2016 viết phương trình đặc trưng r² − 6r − 9 = 0 là in nhầm dấu; đúng là r² − 6r + 9 = 0.)','r² − 6r + 9 = 0 ⇔ (r − 3)² = 0 ⇒ r = 3 kép. aₙ = (α + βn)3ⁿ; a₀ = α = 1; a₁ = 3(1 + β) = 6 ⇒ β = 1. aₙ = (1 + n)3ⁿ.'),
        ('Tìm công thức tường minh của số Fibonacci: fₙ = fₙ₋₁ + fₙ₋₂, f₀ = 0, f₁ = 1.','r² − r − 1 = 0 ⇒ r = (1 ± √5)/2. fₙ = α((1+√5)/2)ⁿ + β((1−√5)/2)ⁿ; f₀ = 0 ⇒ β = −α; f₁ = 1 ⇒ α((1+√5)/2 − (1−√5)/2) = α√5 = 1 ⇒ α = 1/√5.\nfₙ = (1/√5)[((1+√5)/2)ⁿ − ((1−√5)/2)ⁿ].'),
        ('Giải aₙ₊₃ = 14aₙ₊₂ − 59aₙ₊₁ + 70aₙ (n ≥ 0), a₀ = −7, a₁ = −20, a₂ = −100.','r³ − 14r² + 59r − 70 = 0 ⇒ (r − 2)(r − 5)(r − 7) = 0. aₙ = α2ⁿ + β5ⁿ + γ7ⁿ.\nα+β+γ = −7; 2α+5β+7γ = −20; 4α+25β+49γ = −100 ⇒ α = −7, β = 3, γ = −3.\naₙ = −7·2ⁿ + 3·5ⁿ − 3·7ⁿ. Kiểm tra a₃ = 14(−100) − 59(−20) + 70(−7) = −1400 + 1180 − 490 = −710; công thức: −56 + 375 − 1029 = −710 ✓.'),
        ('Giải aₙ = 5aₙ₋₁ − 6aₙ₋₂, a₀ = 1, a₁ = 0. Tính a₁₀.','r = 2, 3. α + β = 1; 2α + 3β = 0 ⇒ β = −2, α = 3. aₙ = 3·2ⁿ − 2·3ⁿ. a₁₀ = 3072 − 118098 = −115026.'),
        ('Số hạng thứ n của một dãy thỏa aₙ = 4aₙ₋₁ − 4aₙ₋₂, a₀ = 1, a₁ = 8. Tìm aₙ.','r² − 4r + 4 = 0 ⇒ r = 2 kép. aₙ = (α + βn)2ⁿ; α = 1; 2(1 + β) = 8 ⇒ β = 3. aₙ = (1 + 3n)2ⁿ.'),
        ('Chứng minh nếu r là nghiệm của r² = c₁r + c₂ thì aₙ = rⁿ thỏa aₙ = c₁aₙ₋₁ + c₂aₙ₋₂.','c₁rⁿ⁻¹ + c₂rⁿ⁻² = rⁿ⁻²(c₁r + c₂) = rⁿ⁻²·r² = rⁿ.')]
    for q,s in ex: B.essay(q,s,level=3,topic='Giải hệ thức truy hồi')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items)); import collections; print(collections.Counter(i['topic'] for i in B.items))
