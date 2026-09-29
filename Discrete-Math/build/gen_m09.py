from qcore import *
import itertools, math
SUPD=str.maketrans('0123456789','⁰¹²³⁴⁵⁶⁷⁸⁹')
def xp(k): return 'x' if k==1 else f'x{str(k).translate(SUPD)}'
def sub(n): return ''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(n))
def pmul(a,b,N):
    r=[0]*(N+1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if i+j<=N: r[i+j]+=x*y
    return r
def geo(lo,hi,step,N):
    p=[0]*(N+1)
    for e in range(lo,(hi if hi is not None else N)+1,step):
        if e<=N: p[e]=1
    return p
def gs(lo,hi,step=1):
    """chuỗi cho 1 nhân tử: x^lo+...+x^hi (hoặc vô hạn)"""
    if hi is None:
        base=xp(lo) if lo else '1'
        return f'1/(1 − {xp(step)})' if lo==0 else f'{base}/(1 − {xp(step)})'
    ts=[('1' if e==0 else xp(e)) for e in range(lo,hi+1,step)]
    return '('+' + '.join(ts)+')'
def gen(seed=9):
    B=Bank('m09',seed); rng=B.rng
    # 1. hệ số của tích hữu hạn
    for _ in range(45):
        k=rng.choice([2,3,4]); N=rng.randint(6,16)
        facs=[]
        for _ in range(k):
            lo=rng.randint(0,3); hi=lo+rng.randint(1,5); facs.append((lo,hi))
        prod=[1]+[0]*N
        for lo,hi in facs: prod=pmul(prod,geo(lo,hi,1,N),N)
        ans=prod[N]
        if ans==0: continue
        expr=''.join(gs(lo,hi) for lo,hi in facs)
        lohi=', '.join(f'{lo} ≤ x_{i+1} ≤ {hi}' for i,(lo,hi) in enumerate(facs))
        B.add(f'Hệ số của {xp(N)} trong khai triển {expr} bằng số nghiệm nguyên của hệ nào, và có giá trị là bao nhiêu?',f'Số nghiệm của x₁+…+x_{k} = {N} với {lohi}: {ans}',[f'Số nghiệm của x₁+…+x_{k} = {N} với {lohi}: {ans+d}' for d in (1,-1,2)],f'Mỗi nhân tử {gs(*facs[0])} mã hóa "x₁ nhận giá trị trong đoạn tương ứng" (số mũ = giá trị của biến). Hệ số của {xp(N)} trong tích đếm số bộ (x₁,…,x_{k}) có tổng {N}. Nhân đa thức (hoặc quy hoạch động) cho {ans}.',level=3,topic='Hệ số hàm sinh')
    # 2. đếm nghiệm bằng hàm sinh
    for _ in range(50):
        k=rng.randint(3,5); N=rng.randint(8,25)
        lo=[0]*k; hi=[None]*k
        for i in rng.sample(range(k),rng.randint(1,k-1)):
            lo[i]=rng.randint(0,4); hi[i]=lo[i]+rng.randint(2,7)
        prod=[1]+[0]*N
        for i in range(k): prod=pmul(prod,geo(lo[i],hi[i],1,N),N)
        ans=prod[N]
        if ans<2: continue
        cons=', '.join(f'{"" if hi[i] is None else str(hi[i])+" ≥ "}x_{i+1} ≥ {lo[i]}' for i in range(k) if lo[i] or hi[i] is not None)
        wrong=set(near_ints(ans,rng,6,lo=1)); wrong|={math.comb(N+k-1,k-1)}; wrong.discard(ans)
        B.add(f'Dùng hàm sinh, số nghiệm nguyên không âm của x₁ + … + x_{k} = {N} thỏa {cons} là:',ans,list(wrong),f'Hàm sinh: '+''.join(gs(lo[i],hi[i]) for i in range(k))+f'. Số nghiệm là hệ số của {xp(N)}, tính được {ans}.\n(Nếu bỏ mọi cận: C({N}+{k}−1,{k}−1) = {math.comb(N+k-1,k-1)}, chưa đúng.)',level=3,topic='Đếm bằng hàm sinh')
    # 3. đổi tiền / phân hoạch
    for coins in [(1,2),(1,5),(1,2,5),(1,5,10),(1,2,5,10),(2,3,5),(1,3,4),(5,10,20),(1,2,3),(1,3,5)]:
        for N in (rng.randint(8,14),rng.randint(15,30),rng.randint(31,50)):
            dp=[1]+[0]*N
            for c in coins:
                for v in range(c,N+1): dp[v]+=dp[v-c]
            B.add(f'Có bao nhiêu cách đổi {N} nghìn đồng ra các tờ tiền mệnh giá {", ".join(map(str,coins))} (mỗi loại không hạn chế, không tính thứ tự)?',dp[N],near_ints(dp[N],rng,7,lo=0),f'Hàm sinh: '+''.join(f'1/(1 − {xp(c)})' for c in coins)+f'. Số cách là hệ số của {xp(N)}. Quy hoạch động cho {dp[N]}.\nLưu ý: nếu tính cả thứ tự (dãy tờ tiền) thì đó là bài toán truy hồi khác.',level=3,topic='Đổi tiền')
    # 4. khai triển chuỗi
    for k in range(2,7):
        for n in (rng.randint(3,9),rng.randint(10,15)):
            B.add(f'Hệ số của {xp(n)} trong khai triển chuỗi của 1/(1 − x)^{k} là:',math.comb(n+k-1,k-1),[math.comb(n+k-1,n+1) if n+1<=n+k-1 else 1,math.comb(n+k,k),math.comb(n+k-1,k-1)+1,math.comb(n,k-1)],f'1/(1−x)^{k} = Σ C(n+{k}−1, {k}−1)·xⁿ. Với n = {n}: C({n+k-1},{k-1}) = {math.comb(n+k-1,k-1)}. (Đây cũng là số nghiệm nguyên không âm của x₁+…+x_{k} = {n}.)',level=2,topic='Khai triển chuỗi')
    for n in range(3,10):
        for k in (2,3):
            B.add(f'Hệ số của {xp(n)} trong (1 + x)^{n+k} là:',math.comb(n+k,n),[math.comb(n+k,n)+1,math.comb(n+k-1,n),math.comb(n+k,n+1),2**(n+k)],f'(1+x)^m = Σ C(m,j)x^j nên hệ số của {xp(n)} trong (1+x)^{n+k} là C({n+k},{n}) = {math.comb(n+k,n)}.',level=1,topic='Khai triển chuỗi')
    # 5. dãy ↔ hàm sinh
    tab=[('aₙ = 1 (mọi n ≥ 0)','1/(1 − x)'),('aₙ = 2ⁿ','1/(1 − 2x)'),('aₙ = 3ⁿ','1/(1 − 3x)'),('aₙ = (−1)ⁿ','1/(1 + x)'),('aₙ = n + 1','1/(1 − x)²'),('aₙ = n','x/(1 − x)²'),('aₙ = 5·2ⁿ','5/(1 − 2x)'),('aₙ = 0,1,0,1,0,1,… (aₙ = 1 khi n lẻ)','x/(1 − x²)'),('aₙ = 1 khi n chẵn, 0 khi n lẻ','1/(1 − x²)'),('aₙ = 1 với 0 ≤ n ≤ 9, 0 với n ≥ 10','(1 − x¹⁰)/(1 − x)'),('aₙ = Fibonacci: 0,1,1,2,3,5,8,…','x/(1 − x − x²)'),('aₙ = 4ⁿ','1/(1 − 4x)'),('aₙ = C(n+2, 2)','1/(1 − x)³')]
    for d,f in tab:
        oth=[g for _,g in tab if g!=f]
        for tag in range(2):
            B.add(f'Hàm sinh của dãy {d} là:' if tag==0 else f'Hàm sinh thường G(x) = Σ aₙxⁿ ứng với {d} là:',f,rng.sample(oth,3),f'Ghi nhớ các hàm sinh cơ bản: 1/(1−x) ↔ 1; 1/(1−cx) ↔ cⁿ; 1/(1−x)² ↔ n+1; x/(1−x)² ↔ n; x/(1−x−x²) ↔ Fibonacci. Đáp án: {f}.',level=2,topic='Hàm sinh cơ bản')
    # 6. xúc xắc
    for k in (2,3,4):
        for s in sorted(rng.sample(range(k,6*k+1),4)):
            dp={0:1}
            for _ in range(k):
                nd={}
                for t,c in dp.items():
                    for f in range(1,7): nd[t+f]=nd.get(t+f,0)+c
                dp=nd
            ans=dp.get(s,0)
            cnt=sum(1 for t in itertools.product(range(1,7),repeat=k) if sum(t)==s)
            assert cnt==ans
            B.add(f'Gieo {k} con xúc xắc phân biệt. Có bao nhiêu kết quả có tổng số chấm bằng {s}?',ans,near_ints(ans,rng,6,lo=0),f'Hàm sinh mỗi con: x + x² + … + x⁶ = x(1 − x⁶)/(1 − x). Tích {k} nhân tử; hệ số của {xp(s)} là {ans} (đã đối chiếu với liệt kê tất cả 6^{k} = {6**k} kết quả).',level=3,topic='Xúc xắc')
    # 7. giải truy hồi bằng hàm sinh: cho khai triển vài số hạng
    for _ in range(12):
        c1,c2=rng.randint(1,4),rng.randint(-3,4); a0,a1=rng.randint(1,3),rng.randint(1,5); a=[a0,a1]
        for n in range(2,9): a.append(c1*a[-1]+c2*a[-2])
        B.add(f'Dãy aₙ = {c1}aₙ₋₁ {"+" if c2>=0 else "−"} {abs(c2)}aₙ₋₂, a₀ = {a0}, a₁ = {a1} có hàm sinh G(x) = P(x)/(1 − {c1}x {"−" if c2>=0 else "+"} {abs(c2)}x²) với P(x) bằng:',f'{a0} + {a1-c1*a0}x'.replace('+ -','− '),[f'{a0} + {a1}x',f'{a0} − {a1-c1*a0}x',f'{a1} + {a0}x'],f'G(x)(1 − {c1}x − ({c2})x²) = a₀ + (a₁ − {c1}a₀)x ⇒ P(x) = {a0} + ({a1-c1*a0})x. Các số hạng: '+', '.join(map(str,a[:7])),level=3,topic='Hàm sinh & truy hồi')
    return B
def essays(B):
    ex=[('Dùng hàm sinh, tìm số nghiệm nguyên của x₁ + x₂ + x₃ = 12 với 1 ≤ x₁ ≤ 4, 2 ≤ x₂ ≤ 6, 0 ≤ x₃ ≤ 8.','G(x) = (x + x² + x³ + x⁴)(x² + x³ + x⁴ + x⁵ + x⁶)(1 + x + … + x⁸). Hệ số của x¹²: đặt x₁=x₁\'+1 (0..3), x₂=x₂\'+2 (0..4), tổng còn 9 với x₃ ≤ 8.\nLiệt kê x₁ = 1..4 và x₂ = 2..6 với x₃ = 12 − x₁ − x₂ ∈ [0,8] cho 19 nghiệm (đã kiểm chứng bằng chương trình).'),
        ('Tìm hệ số của x¹⁰ trong (1 + x + x²)⁵.','Hệ số = số nghiệm của y₁+…+y₅ = 10 với 0 ≤ yᵢ ≤ 2 = 1 (tất cả yᵢ = 2) ⇒ hệ số 1.'),
        ('Có bao nhiêu cách chọn 10 quả từ táo, cam, chuối, lê nếu số táo là số chẵn, số cam nhiều nhất 3, số chuối là bội của 3, số lê nhiều nhất 1?','G(x) = (1+x²+x⁴+…)(1+x+x²+x³)(1+x³+x⁶+…)(1+x). Nhân ra và lấy hệ số x¹⁰ (đã kiểm chứng bằng chương trình): kết quả 14.'),
        ('Chứng minh 1/(1−x)² = Σ (n+1)xⁿ bằng cách nhân chuỗi.','1/(1−x) = Σ xⁿ. Bình phương: hệ số của xⁿ trong (Σxⁱ)(Σxʲ) là số cặp (i,j) không âm có i+j=n, tức n+1 cặp ⇒ Σ (n+1)xⁿ.'),
        ('Giải aₙ = 3aₙ₋₁ − 2aₙ₋₂, a₀ = 1, a₁ = 3 bằng hàm sinh.','G(x)(1 − 3x + 2x²) = 1 + (3−3)x = 1 ⇒ G = 1/((1−x)(1−2x)) = 2/(1−2x) − 1/(1−x) ⇒ aₙ = 2·2ⁿ − 1 = 2ⁿ⁺¹ − 1.'),
        ('Có bao nhiêu cách gieo 4 con xúc xắc để tổng bằng 14?','Hệ số của x¹⁴ trong (x + … + x⁶)⁴ = 146 (đã đối chiếu bằng liệt kê 1296 kết quả).'),
        ('Có bao nhiêu cách đổi 20 nghìn ra tờ 1, 2, 5, 10 (không tính thứ tự)?','Hệ số x²⁰ của 1/((1−x)(1−x²)(1−x⁵)(1−x¹⁰)) = 40.'),
        ('Tìm hàm sinh của dãy aₙ = 3n + 2 (n ≥ 0).','Σ(3n+2)xⁿ = 3x/(1−x)² + 2/(1−x) = (3x + 2(1−x))/(1−x)² = (2 + x)/(1−x)².')]
    for q,s in ex: B.essay(q,s,level=3,topic='Hàm sinh')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items))
