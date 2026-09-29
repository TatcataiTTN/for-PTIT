from qcore import *
import math, itertools, collections
def bounded(N,lo,hi):
    k=len(lo); dp=[1]+[0]*N
    for i in range(k):
        nd=[0]*(N+1)
        for t in range(N+1):
            if dp[t]:
                top=N-t if hi[i] is None else min(hi[i],N-t)
                for v in range(lo[i],top+1): nd[t+v]+=dp[t]
        dp=nd
    return dp[N]
def gen(seed=5):
    B=Bank('m05',seed); rng=B.rng
    F=math.factorial
    for _ in range(30):
        n=rng.randint(5,12); k=rng.randint(2,min(5,n-1))
        B.add(f'Có bao nhiêu chỉnh hợp chập {k} của {n} phần tử (không lặp)?',math.perm(n,k),[math.comb(n,k),n**k,math.perm(n,k)+n,F(n)],f'A({n},{k}) = {n}!/({n}−{k})! = {math.perm(n,k)}. (Tổ hợp C({n},{k}) = {math.comb(n,k)} bỏ qua thứ tự nên sai.)',level=1,topic='Chỉnh hợp, tổ hợp')
        B.add(f'Chọn {k} người từ nhóm {n} người để lập một tổ (không phân biệt vai trò). Có bao nhiêu cách?',math.comb(n,k),[math.perm(n,k),math.comb(n,k)+1,math.comb(n+k-1,k),n**k],f'Không phân biệt thứ tự nên dùng tổ hợp: C({n},{k}) = {math.comb(n,k)}.',level=1,topic='Chỉnh hợp, tổ hợp')
    for _ in range(30):
        m=rng.randint(6,14); w=rng.randint(4,10); k=rng.randint(3,min(6,m+w-2)); a=rng.randint(1,min(3,k-1))
        cnt=sum(math.comb(m,i)*math.comb(w,k-i) for i in range(a,k+1))
        B.add(f'Câu lạc bộ có {m} nam và {w} nữ. Chọn một ủy ban {k} người có ÍT NHẤT {a} nam. Có bao nhiêu cách?',cnt,near_ints(cnt,rng,5,lo=1)+[math.comb(m,a)*math.comb(m+w-a,k-a)],f'Cộng theo số nam i = {a}…{k}: Σ C({m},i)·C({w},{k}−i) = {cnt}.\nCách "chọn trước {a} nam rồi chọn tùy ý" đếm trùng nên cho {math.comb(m,a)*math.comb(m+w-a,k-a)} (sai).',level=3,topic='Chỉnh hợp, tổ hợp')
    for w in ['ANNA','BANANA','MISSISSIPPI','ABRACADABRA','PEPPER','LEVEL','TOÁN','PROGRAMMING','BOOKKEEPER','DISCRETE','MATHEMATICS','ALGORITHM','COMBINATORICS']:
        c=collections.Counter(w); tot=F(len(w))
        for v in c.values(): tot//=F(v)
        det=' · '.join(f'{ch}×{v}' for ch,v in c.items() if v>1) or 'không lặp'
        B.add(f'Có bao nhiêu cách sắp xếp các chữ cái của từ "{w}" (mọi hoán vị phân biệt)?',tot,list({F(len(w)),tot*2,tot+len(w),tot//max(c.values())+1})-{tot} if False else [F(len(w)),tot*2,tot+len(w),max(1,tot//2)],f'Từ "{w}" có {len(w)} chữ cái; chữ lặp: {det}. Hoán vị lặp: {len(w)}!'+''.join(f'/{v}!' for v in c.values() if v>1)+f' = {tot}.',level=2,topic='Hoán vị lặp')
    for _ in range(40):
        n=rng.randint(3,8); k=rng.randint(2,8)
        B.add(f'Có bao nhiêu cách chọn {k} món từ {n} loại món (mỗi loại có thể chọn nhiều lần, không phân biệt thứ tự)?',math.comb(n+k-1,k),[math.comb(n,k) if n>=k else n*k,n**k,math.perm(n+k-1,k),math.comb(n+k,k)],f'Tổ hợp lặp chập {k} của {n} phần tử: C({n}+{k}−1,{k}) = C({n+k-1},{k}) = {math.comb(n+k-1,k)}.',level=2,topic='Tổ hợp lặp')
    # nghiệm nguyên không âm cơ bản
    for _ in range(40):
        k=rng.randint(3,6); N=rng.randint(k,30)
        ans=math.comb(N+k-1,k-1)
        B.add(f'Phương trình x₁ + … + x_{k} = {N} có bao nhiêu nghiệm nguyên không âm?',ans,[math.comb(N+k-1,N-1),math.comb(N,k),k**N if k**N<10**9 else math.comb(N-1,k-1),math.comb(N+k,k-1)],f'Chia {N} đơn vị vào {k} biến: C({N}+{k}−1,{k}−1) = C({N+k-1},{k-1}) = {ans} (phương pháp "vách ngăn").',level=1,topic='Nghiệm nguyên')
        lo=[rng.randint(1,4) for _ in range(k)]
        if sum(lo)<=N:
            a2=math.comb(N-sum(lo)+k-1,k-1)
            B.add(f'Phương trình x₁ + … + x_{k} = {N} có bao nhiêu nghiệm nguyên với '+', '.join(f'x_{i+1} ≥ {l}' for i,l in enumerate(lo))+'?',a2,[math.comb(N+k-1,k-1),math.comb(N-sum(lo)+k,k-1),math.comb(N-sum(lo)+k-1,k),a2+1],f'Đặt yᵢ = xᵢ − lᵢ ≥ 0: tổng còn {N} − {sum(lo)} = {N-sum(lo)}. Số nghiệm C({N-sum(lo)}+{k}−1,{k}−1) = {a2}.',level=2,topic='Nghiệm nguyên')
    # nghiệm nguyên có cận (dạng đề thi)
    for _ in range(60):
        k=rng.choice([4,5,6]); N=rng.randint(28,52)
        lo=[0]*k; hi=[None]*k
        i1,i2=rng.sample(range(k),2)
        a=rng.randint(2,6); b=a+rng.randint(2,4); lo[i1]=a; hi[i1]=b
        c=rng.randint(1,6); d=c+rng.randint(2,5); lo[i2]=c; hi[i2]=d
        i3=rng.choice([i for i in range(k) if i not in(i1,i2)]); lo[i3]=rng.randint(3,9)
        ans=bounded(N,lo,hi)
        # bù trừ chi tiết
        base=N-sum(lo); caps=[(i,hi[i]-lo[i]) for i in (i1,i2)]
        t0=math.comb(base+k-1,k-1); t1=math.comb(base-(caps[0][1]+1)+k-1,k-1) if base-(caps[0][1]+1)>=0 else 0
        t2=math.comb(base-(caps[1][1]+1)+k-1,k-1) if base-(caps[1][1]+1)>=0 else 0
        s12=caps[0][1]+caps[1][1]+2; t12=math.comb(base-s12+k-1,k-1) if base-s12>=0 else 0
        assert t0-t1-t2+t12==ans
        cons=', '.join([f'{hi[i1]} ≥ x_{i1+1} ≥ {lo[i1]}',f'{hi[i2]} ≥ x_{i2+1} ≥ {lo[i2]}',f'x_{i3+1} ≥ {lo[i3]}'])
        stem=f'Phương trình '+' + '.join(f'x_{i+1}' for i in range(k))+f' = {N} có bao nhiêu nghiệm nguyên không âm thỏa mãn: {cons}?'
        wrong=set(near_ints(ans,rng,5,lo=1)); wrong|={t0,t0-t1-t2,t0-t1-t2-t12}; wrong.discard(ans)
        expl=(f'Bước 1 (cận dưới): đặt yᵢ = xᵢ − lᵢ, được tổng {base} với y{ i1+1}∈[0,{caps[0][1]}], y{ i2+1}∈[0,{caps[1][1]}], còn lại y ≥ 0.\n'
              f'Bước 2 (không cận trên): C({base}+{k}−1,{k}−1) = {t0}.\nBước 3 (bù trừ hai điều kiện vượt cận): vượt cận 1 ⇔ y{i1+1} ≥ {caps[0][1]+1}: C({base-caps[0][1]-1}+{k-1},{k-1}) = {t1}; vượt cận 2 ⇔ y{i2+1} ≥ {caps[1][1]+1}: {t2}; vượt cả hai: {t12}.\nĐáp án = {t0} − {t1} − {t2} + {t12} = {ans}.')
        B.add(stem,ans,list(wrong),expl,level=3,topic='Nghiệm nguyên có cận')
    # số thuận nghịch
    for L in (5,6,7,8,9):
        for N in rng.sample(range(8,34),5):
            h=(L+1)//2; cnt=0
            for d in itertools.product(range(10),repeat=h):
                if d[0]==0: continue
                s=2*sum(d)-(d[-1] if L%2 else 0)
                if s==N: cnt+=1
            if cnt==0: continue
            B.add(f'Có bao nhiêu số có {L} chữ số là số thuận nghịch (đối xứng, đọc xuôi ngược như nhau) và có tổng các chữ số bằng {N}?',cnt,near_ints(cnt,rng,6,lo=1),f'Số thuận nghịch {L} chữ số được xác định bởi {h} chữ số đầu x₁…x_{h} (x₁ ≥ 1). Tổng chữ số = '+(f'2(x₁+…+x_{h-1}) + x_{h}' if L%2 else f'2(x₁+…+x_{h})')+f' = {N}. Đếm số nghiệm với 0 ≤ xᵢ ≤ 9, x₁ ≥ 1 được {cnt} (kiểm chứng bằng liệt kê).',level=3,topic='Số thuận nghịch')
    # nhị thức
    for n in range(4,11):
        k=rng.randint(1,n-1); a=rng.randint(2,4); b=rng.randint(1,3)
        coef=math.comb(n,k)*a**(n-k)*b**k
        B.add(f'Hệ số của x^{n-k}·y^{k} trong khai triển ({a}x + {b}y)^{n} là:',coef,[math.comb(n,k),math.comb(n,k)*a*b,a**(n-k)*b**k,coef+math.comb(n,k)],f'Số hạng tổng quát C({n},{k})·({a}x)^{n-k}·({b}y)^{k} = C({n},{k})·{a}^{n-k}·{b}^{k}·x^{n-k}y^{k}. Hệ số = {math.comb(n,k)}·{a**(n-k)}·{b**k} = {coef}.',level=2,topic='Nhị thức Newton')
    for n in range(3,12):
        B.add(f'Tổng C({n},0) + C({n},1) + … + C({n},{n}) bằng:',2**n,[2**n-1,n*2**(n-1),2**(n+1),n**2],f'Trong khai triển (1+1)^{n} = Σ C({n},k): bằng 2^{n} = {2**n} (cũng là số tập con của tập {n} phần tử).',level=1,topic='Nhị thức Newton')
    # đường đi lưới
    for _ in range(25):
        r,c=rng.randint(2,9),rng.randint(2,9)
        B.add(f'Đi từ góc trên-trái đến góc dưới-phải của lưới {r}×{c} ô (chỉ đi sang phải hoặc xuống dưới theo cạnh ô), có bao nhiêu đường đi?',math.comb(r+c,r),[math.comb(r+c-1,r),r*c,math.comb(r+c,r)+1,math.perm(r+c,r)],f'Cần {r} bước xuống và {c} bước sang phải, sắp xếp tùy ý: C({r+c},{r}) = {math.comb(r+c,r)}.',level=2,topic='Tổ hợp ứng dụng')
    return B
def essays(B):
    ex=[('Phương trình x₁+x₂+x₃+x₄+x₅+x₆ = 30 có bao nhiêu nghiệm nguyên không âm thỏa 8 ≥ x₂ ≥ 3 và 6 ≥ x₄ ≥ 2? (dạng câu 3a đề thi 2019-2020)','Đặt y₂ = x₂−3 ∈ [0,5], y₄ = x₄−2 ∈ [0,4]; tổng còn 30−3−2 = 25 trên 6 biến.\nKhông cận: C(30,5) = 142506.\nVượt cận y₂ ≥ 6: tổng 19: C(24,5) = 42504; vượt cận y₄ ≥ 5: tổng 20: C(25,5) = 53130; vượt cả hai: tổng 14: C(19,5) = 11628.\nĐáp án: 142506 − 42504 − 53130 + 11628 = 58500.'),
        ('Có bao nhiêu cách chia 12 quả bóng giống nhau vào 4 hộp khác nhau sao cho mỗi hộp có ít nhất 1 quả?','Đặt yᵢ = xᵢ − 1 ≥ 0, tổng 8 trên 4 biến: C(8+3,3) = C(11,3) = 165.'),
        ('Có bao nhiêu xâu nhị phân độ dài 12 có đúng 5 bit 1 và không có hai bit 1 liên tiếp?','Xếp 7 bit 0 tạo 8 khe; chọn 5 khe cho bit 1: C(8,5) = 56.'),
        ('Có bao nhiêu cách chọn 5 lá bài từ bộ bài 52 lá sao cho có đúng 2 quân Át?','C(4,2)·C(48,3) = 6·17296 = 103776.'),
        ('Có bao nhiêu số tự nhiên có 4 chữ số (chữ số đầu ≠ 0) mà các chữ số giảm ngặt từ trái sang phải?','Chọn 4 chữ số khác nhau từ 0–9 rồi xếp giảm dần: C(10,4) = 210 (chữ số đầu là số lớn nhất nên luôn ≠ 0).'),
        ('Chứng minh đẳng thức Pascal: C(n,k) = C(n−1,k−1) + C(n−1,k) bằng lập luận tổ hợp.','Xét tập n phần tử, cố định phần tử a. Tập con k phần tử chứa a: C(n−1,k−1); không chứa a: C(n−1,k). Cộng lại (quy tắc cộng).'),
        ('Tìm hệ số của x³y⁴z² trong khai triển (x + y + z)⁹.','Hệ số đa thức: 9!/(3!4!2!) = 362880/(6·24·2) = 1260.'),
        ('Tìm số nghiệm nguyên không âm của x₁+x₂+x₃+x₄ ≤ 10.','Thêm biến phụ x₅ ≥ 0: x₁+…+x₅ = 10: C(14,4) = 1001.')]
    for q,s in ex: B.essay(q,s,level=3,topic='Tổ hợp & nghiệm nguyên')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items)); import collections; print(collections.Counter(i['topic'] for i in B.items))
