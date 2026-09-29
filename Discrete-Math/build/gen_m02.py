from qcore import *
import itertools, random
# ---------- vị từ trên miền hữu hạn ----------
def is_prime(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
PRED=[('x là số chẵn',lambda x:x%2==0),('x là số lẻ',lambda x:x%2==1),('x là số nguyên tố',is_prime),('x chia hết cho 3',lambda x:x%3==0),('x chia hết cho 4',lambda x:x%4==0),
      ('x là số chính phương',lambda x:int(x**.5)**2==x),('x > 3',lambda x:x>3),('x < 6',lambda x:x<6),('x² < 30',lambda x:x*x<30),('x + 2 chia hết cho 5',lambda x:(x+2)%5==0),('x ≤ 5',lambda x:x<=5),('x có đúng 2 ước dương hoặc x = 1',lambda x:x==1 or is_prime(x))]
def dm(D): return '{'+', '.join(map(str,D))+'}'
def gen(seed=2):
    B=Bank('m02',seed); rng=B.rng
    def rdom(): 
        n=rng.randint(4,9); return sorted(rng.sample(range(1,13),n))
    # ---- 1. chọn mệnh đề đúng
    for _ in range(90):
        D=rdom(); P=rng.sample(PRED,2); (np_,fp),(nq,fq)=P
        S=[]
        S.append((f'∀x P(x)',all(fp(x) for x in D)))
        S.append((f'∃x P(x)',any(fp(x) for x in D)))
        S.append((f'∀x Q(x)',all(fq(x) for x in D)))
        S.append((f'∃x Q(x)',any(fq(x) for x in D)))
        S.append((f'∀x (P(x) ⇒ Q(x))',all((not fp(x)) or fq(x) for x in D)))
        S.append((f'∃x (P(x) ∧ Q(x))',any(fp(x) and fq(x) for x in D)))
        S.append((f'∀x (P(x) ∨ Q(x))',all(fp(x) or fq(x) for x in D)))
        S.append((f'∃x (P(x) ∧ ¬Q(x))',any(fp(x) and not fq(x) for x in D)))
        S.append((f'¬∀x P(x)',not all(fp(x) for x in D)))
        S.append((f'∀x ¬Q(x)',all(not fq(x) for x in D)))
        T=[s for s in S if s[1]]; F=[s for s in S if not s[1]]
        if len(T)<1 or len(F)<3: continue
        t=rng.choice(T); fs=rng.sample(F,3)
        expl=f'Miền D = {dm(D)}; P(x): "{np_}"; Q(x): "{nq}".\nTập thỏa P: {dm([x for x in D if fp(x)])}; tập thỏa Q: {dm([x for x in D if fq(x)])}.\n'
        expl+=f'• {t[0]} ĐÚNG.\n'+'\n'.join(f'• {s[0]} SAI.' for s in fs)+'\nQuy tắc: ∀ đúng khi MỌI phần tử thỏa; ∃ đúng khi CÓ ÍT NHẤT MỘT phần tử thỏa; một phản ví dụ đủ để làm ∀ sai.'
        B.add(f'Cho miền D = {dm(D)}, P(x): "{np_}", Q(x): "{nq}". Mệnh đề nào sau đây ĐÚNG?',t[0],[s[0] for s in fs],expl,level=2,topic='Giá trị chân lý')
    # ---- 2. đếm phần tử
    for _ in range(35):
        D=rdom(); (np_,fp),(nq,fq)=rng.sample(PRED,2)
        kind=rng.choice(['and','or','imp','notp'])
        if kind=='and': f=lambda x:fp(x) and fq(x); d=f'P(x) ∧ Q(x)'
        elif kind=='or': f=lambda x:fp(x) or fq(x); d='P(x) ∨ Q(x)'
        elif kind=='imp': f=lambda x:(not fp(x)) or fq(x); d='P(x) ⇒ Q(x)'
        else: f=lambda x:not fp(x); d='¬P(x)'
        c=sum(1 for x in D if f(x))
        expl=f'Kiểm tra từng x∈{dm(D)}: '+'; '.join(f'{x}→{"Đ" if f(x) else "S"}' for x in D)+f'. Có {c} phần tử thỏa.\nLưu ý với ⇒: P(x) ⇒ Q(x) đúng cả khi P(x) sai (đúng "vacuously").'
        B.add(f'Miền D = {dm(D)}, P(x): "{np_}", Q(x): "{nq}". Có bao nhiêu phần tử x ∈ D làm cho {d} nhận giá trị Đúng?',c,[y for y in range(0,len(D)+1) if y!=c],expl,level=2,topic='Đếm phần tử thỏa')
    # ---- 3. phủ định lượng từ (kiểm chứng ngữ nghĩa trên nhiều mô hình ngẫu nhiên)
    forms={ # (tên, hàm đánh giá S trên mô hình (P,Q tập con), chuỗi)
      '∀x P(x)':lambda D,P,Q:all(x in P for x in D),'∃x P(x)':lambda D,P,Q:any(x in P for x in D),
      '∀x (P(x) ⇒ Q(x))':lambda D,P,Q:all((x not in P) or x in Q for x in D),'∃x (P(x) ∧ Q(x))':lambda D,P,Q:any(x in P and x in Q for x in D),
      '∀x (P(x) ∨ Q(x))':lambda D,P,Q:all(x in P or x in Q for x in D),'∃x (P(x) ∧ ¬Q(x))':lambda D,P,Q:any(x in P and x not in Q for x in D),
      '∀x ¬P(x)':lambda D,P,Q:all(x not in P for x in D),'∃x (¬P(x) ∨ Q(x))':lambda D,P,Q:any(x not in P or x in Q for x in D),
      '∀x (P(x) ∧ Q(x))':lambda D,P,Q:all(x in P and x in Q for x in D),'∃x (P(x) ⇒ Q(x))':lambda D,P,Q:any((x not in P) or x in Q for x in D)}
    neg={'∀x P(x)':['∃x ¬P(x)',['∀x ¬P(x)','∃x P(x)','¬∃x ¬P(x)']],'∃x P(x)':['∀x ¬P(x)',['∃x ¬P(x)','∀x P(x)','¬∀x ¬P(x)']],
         '∀x (P(x) ⇒ Q(x))':['∃x (P(x) ∧ ¬Q(x))',['∀x (P(x) ∧ ¬Q(x))','∃x (¬P(x) ⇒ ¬Q(x))','∃x (P(x) ⇒ ¬Q(x))']],
         '∃x (P(x) ∧ Q(x))':['∀x (P(x) ⇒ ¬Q(x))',['∀x (¬P(x) ∧ ¬Q(x))','∃x (¬P(x) ∨ ¬Q(x))','∀x (P(x) ∧ ¬Q(x))']],
         '∀x (P(x) ∨ Q(x))':['∃x (¬P(x) ∧ ¬Q(x))',['∃x (¬P(x) ∨ ¬Q(x))','∀x (¬P(x) ∧ ¬Q(x))','∃x (P(x) ∧ Q(x))']],
         '∃x (P(x) ∧ ¬Q(x))':['∀x (P(x) ⇒ Q(x))',['∀x (P(x) ∧ Q(x))','∃x (¬P(x) ∨ Q(x))','∀x (¬P(x) ⇒ Q(x))']],
         '∀x ¬P(x)':['∃x P(x)',['∀x P(x)','∃x ¬P(x)','¬∃x P(x)']]}
    pf={'∃x ¬P(x)':lambda D,P,Q:any(x not in P for x in D),'∀x ¬P(x)':lambda D,P,Q:all(x not in P for x in D),'∃x P(x)':forms['∃x P(x)'],'∀x P(x)':forms['∀x P(x)'],'¬∃x ¬P(x)':lambda D,P,Q:not any(x not in P for x in D),
        '¬∀x ¬P(x)':lambda D,P,Q:not all(x not in P for x in D),'¬∃x P(x)':lambda D,P,Q:not any(x in P for x in D),
        '∃x (P(x) ∧ ¬Q(x))':forms['∃x (P(x) ∧ ¬Q(x))'],'∀x (P(x) ∧ ¬Q(x))':lambda D,P,Q:all(x in P and x not in Q for x in D),'∃x (¬P(x) ⇒ ¬Q(x))':lambda D,P,Q:any(x in P or x not in Q for x in D),
        '∃x (P(x) ⇒ ¬Q(x))':lambda D,P,Q:any(x not in P or x not in Q for x in D),'∀x (P(x) ⇒ ¬Q(x))':lambda D,P,Q:all(x not in P or x not in Q for x in D),
        '∀x (¬P(x) ∧ ¬Q(x))':lambda D,P,Q:all(x not in P and x not in Q for x in D),'∃x (¬P(x) ∨ ¬Q(x))':lambda D,P,Q:any(x not in P or x not in Q for x in D),
        '∃x (¬P(x) ∧ ¬Q(x))':lambda D,P,Q:any(x not in P and x not in Q for x in D),'∀x (P(x) ∧ Q(x))':forms['∀x (P(x) ∧ Q(x))'],'∃x (¬P(x) ∨ Q(x))':forms['∃x (¬P(x) ∨ Q(x))'],
        '∀x (¬P(x) ⇒ Q(x))':lambda D,P,Q:all(x in P or x in Q for x in D),'∃x (P(x) ∧ Q(x))':forms['∃x (P(x) ∧ Q(x))'],'∀x (P(x) ⇒ Q(x))':forms['∀x (P(x) ⇒ Q(x))']}
    def check(S,opt,is_neg):
        rr=random.Random(5)
        for _ in range(400):
            D=list(range(1,rr.randint(2,4)+1)); P={x for x in D if rr.random()<.5}; Q={x for x in D if rr.random()<.5}
            s=forms[S](D,P,Q); o=pf[opt](D,P,Q)
            if o==(not s)!=is_neg and False: pass
            if (o!=s)!=True and is_neg is True and o==s: return False
            if is_neg is False and o==s and False: pass
        return True
    def is_neg_equiv(S,opt):
        rr=random.Random(11)
        for _ in range(500):
            D=list(range(1,rr.randint(1,4)+1)); P={x for x in D if rr.random()<.5}; Q={x for x in D if rr.random()<.5}
            if pf[opt](D,P,Q)==forms[S](D,P,Q): return False
        return True
    for S,(good,bad) in neg.items():
        assert is_neg_equiv(S,good),S
        bad=[b for b in bad if not is_neg_equiv(S,b)]
        wrong=bad+[]
        if len(wrong)<3: continue
        for tag in range(2):
            stm=S
            expl=f'Quy tắc De Morgan cho lượng từ: ¬∀x A(x) ≡ ∃x ¬A(x); ¬∃x A(x) ≡ ∀x ¬A(x). Áp dụng rồi phủ định phần trong (¬(A ⇒ B) ≡ A ∧ ¬B; ¬(A ∧ B) ≡ ¬A ∨ ¬B; ¬(A ∨ B) ≡ ¬A ∧ ¬B).\nĐáp án: ¬({S}) ≡ {good}.\nCác phương án còn lại không phải phủ định: có mô hình (miền nhỏ) trong đó chúng cùng giá trị với {S}, hoặc chỉ đổi lượng từ mà không phủ định phần trong.'
            B.add(f'Phủ định của mệnh đề {S} tương đương với:' if tag==0 else f'Chọn mệnh đề tương đương với ¬({S}):',good,rng.sample(wrong,3),expl,level=2 if tag==0 else 3,topic='Phủ định lượng từ')
    # ---- 4. hai lượng từ lồng nhau trên quan hệ hữu hạn
    for _ in range(45):
        n=rng.randint(3,5); D=list(range(1,n+1)); R={(x,y) for x in D for y in D if rng.random()<rng.choice([.3,.5,.7])}
        rows='\n'.join(f'  x={x}: y∈{dm([y for y in D if (x,y) in R])}' for x in D)
        v={'∀x∃y R':all(any((x,y) in R for y in D) for x in D),'∃y∀x R':any(all((x,y) in R for x in D) for y in D),'∃x∀y R':any(all((x,y) in R for y in D) for x in D),'∀y∃x R':all(any((x,y) in R for x in D) for y in D),'∀x∀y R':all((x,y) in R for x in D for y in D),'∃x∃y R':len(R)>0}
        txt={'∀x∃y R':'∀x ∃y R(x,y)','∃y∀x R':'∃y ∀x R(x,y)','∃x∀y R':'∃x ∀y R(x,y)','∀y∃x R':'∀y ∃x R(x,y)','∀x∀y R':'∀x ∀y R(x,y)','∃x∃y R':'∃x ∃y R(x,y)'}
        T=[k for k,val in v.items() if val]; F=[k for k,val in v.items() if not val]
        if not T or len(F)<3: continue
        t=rng.choice(T); fs=rng.sample(F,3)
        expl=f'Miền {dm(D)}; quan hệ R (x R y) cho bởi:\n{rows}\n'
        expl+=f'• {txt[t]} ĐÚNG.\n'+'\n'.join(f'• {txt[k]} SAI.' for k in fs)+'\nLưu ý: đổi thứ tự ∀ và ∃ có thể đổi giá trị chân lý: ∃y∀x R ⇒ ∀x∃y R nhưng chiều ngược lại KHÔNG đúng.'
        B.add(f'Miền D = {dm(D)}, quan hệ R(x, y) (nghĩa là x R y) có các cặp:\n{rows}\nMệnh đề nào ĐÚNG?',txt[t],[txt[k] for k in fs],expl,level=3,topic='Lượng từ lồng nhau')
    # ---- 5. lượng từ lồng nhau trên số
    nested=[('∀x∈ℝ ∃y∈ℝ (x + y = 0)',True,'Với mọi x chọn y = −x.'),('∃y∈ℝ ∀x∈ℝ (x + y = 0)',False,'Không tồn tại y cố định làm x + y = 0 với mọi x (x = 1 − y phản ví dụ).'),
            ('∀x∈ℕ ∃y∈ℕ (y > x)',True,'Chọn y = x + 1.'),('∃y∈ℕ ∀x∈ℕ (y ≥ x)',False,'ℕ không có phần tử lớn nhất.'),('∀x∈ℤ ∃y∈ℤ (x + y = 0)',True,'y = −x ∈ ℤ.'),
            ('∀x∈ℕ ∃y∈ℕ (x + y = 0)',False,'Với x = 1 không có y ∈ ℕ nào cho 1 + y = 0.'),('∃x∈ℕ ∀y∈ℕ (x ≤ y)',True,'Chọn x = 0 (hoặc 1 nếu ℕ bắt đầu từ 1): phần tử nhỏ nhất.'),
            ('∀x∈ℝ ∃y∈ℝ (x·y = 1)',False,'x = 0 không có y với 0·y = 1.'),('∀x∈ℝ, x ≠ 0 ⇒ ∃y∈ℝ (x·y = 1)',True,'y = 1/x.'),('∃x∈ℝ ∀y∈ℝ (x·y = 0)',True,'x = 0.'),
            ('∀x∈ℤ ∃y∈ℤ (2y = x)',False,'x = 1 lẻ không có y nguyên.'),('∀x∈ℤ (x² ≥ x)',True,'x² − x = x(x−1) ≥ 0 với mọi số nguyên.'),('∃x∈ℝ (x² + 1 = 0)',False,'x² + 1 ≥ 1 > 0.'),
            ('∀x∈ℝ ∃y∈ℝ (y³ = x)',True,'y = ∛x.'),('∃n∈ℕ ∀m∈ℕ (n | m)',True,'n = 1 chia hết mọi m.'),('∀n∈ℕ, n ≥ 2 ⇒ ∃p nguyên tố (p | n)',True,'Mọi n ≥ 2 có ước nguyên tố.')]
    for s,val,why in nested:
        others=[t for t in nested if t[1]!=val and t[0]!=s]
        ws=rng.sample(others,3)
        B.add(f'Mệnh đề nào sau đây là {"ĐÚNG" if val else "SAI"}?',s,[w[0] for w in ws],f'{s}: {"đúng" if val else "sai"}. {why}\n'+'\n'.join(f'• {w[0]}: {"đúng" if w[1] else "sai"}. {w[2]}' for w in ws),level=3,topic='Lượng từ trên số')
    # ---- 6. dịch câu tự nhiên
    tr=[('Mọi sinh viên đều thích môn Toán rời rạc','∀x (S(x) ⇒ T(x))',['∀x (S(x) ∧ T(x))','∃x (S(x) ⇒ T(x))','∀x (T(x) ⇒ S(x))','∃x (S(x) ∧ T(x))']),
        ('Có một sinh viên thích môn Toán rời rạc','∃x (S(x) ∧ T(x))',['∃x (S(x) ⇒ T(x))','∀x (S(x) ∧ T(x))','∀x (S(x) ⇒ T(x))','∃x (T(x) ⇒ S(x))']),
        ('Không có sinh viên nào thích môn Toán rời rạc','¬∃x (S(x) ∧ T(x))',['∃x (S(x) ∧ ¬T(x))','∀x (S(x) ⇒ T(x))','¬∀x (S(x) ⇒ T(x))','∃x (¬S(x) ∧ T(x))']),
        ('Không phải mọi sinh viên đều thích môn Toán rời rạc','∃x (S(x) ∧ ¬T(x))',['∀x (S(x) ⇒ ¬T(x))','∃x (S(x) ⇒ ¬T(x))','¬∃x (S(x) ∧ ¬T(x))','∀x (S(x) ∧ ¬T(x))']),
        ('Chỉ có sinh viên mới thích môn Toán rời rạc','∀x (T(x) ⇒ S(x))',['∀x (S(x) ⇒ T(x))','∃x (T(x) ∧ S(x))','∀x (S(x) ∧ T(x))','∃x (S(x) ⇒ T(x))']),
        ('Mỗi sinh viên đều có một người bạn','∀x (S(x) ⇒ ∃y F(x,y))',['∃y ∀x (S(x) ⇒ F(x,y))','∀x ∃y (S(x) ∧ F(x,y))','∃x (S(x) ∧ ∀y F(x,y))','∀x ∀y (S(x) ⇒ F(x,y))']),
        ('Có một người là bạn của mọi sinh viên','∃y ∀x (S(x) ⇒ F(x,y))',['∀x (S(x) ⇒ ∃y F(x,y))','∀x ∃y (S(x) ∧ F(x,y))','∃y ∃x (S(x) ∧ F(x,y))','∀y ∀x (S(x) ⇒ F(x,y))']),
        ('Mọi số nguyên tố lớn hơn 2 đều là số lẻ','∀x ((N(x) ∧ x > 2) ⇒ L(x))',['∀x ((N(x) ∧ x > 2) ∧ L(x))','∃x ((N(x) ∧ x > 2) ⇒ L(x))','∀x (L(x) ⇒ (N(x) ∧ x > 2))','∀x (N(x) ⇒ (x > 2 ∧ L(x)))']),
        ('Có ít nhất một số chẵn là số nguyên tố','∃x (C(x) ∧ N(x))',['∃x (C(x) ⇒ N(x))','∀x (C(x) ⇒ N(x))','∀x (C(x) ∧ N(x))','∃x (¬C(x) ∧ N(x))']),
        ('Tất cả chim đều biết bay, trừ chim cánh cụt','∀x ((B(x) ∧ ¬P(x)) ⇒ F(x))',['∀x (B(x) ⇒ F(x))','∃x (B(x) ∧ F(x) ∧ ¬P(x))','∀x ((B(x) ∧ P(x)) ⇒ F(x))','∀x (F(x) ⇒ (B(x) ∧ ¬P(x)))'])]
    for s,good,bad in tr:
        for tag in range(3):
            q=[f'Câu "{s}" được hình thức hóa bởi công thức nào? (S: sinh viên, T: thích Toán rời rạc, F: là bạn, N/L/C: nguyên tố/lẻ/chẵn, B: chim, P: chim cánh cụt, F: biết bay)',f'Chọn công thức đúng biểu diễn: "{s}".',f'Hình thức hóa câu: "{s}"'][tag]
            expl=f'Quy tắc: "mọi/tất cả" đi với ⇒ (∀x (P(x) ⇒ Q(x))); "có/tồn tại" đi với ∧ (∃x (P(x) ∧ Q(x))). Dùng ∀ với ∧ hoặc ∃ với ⇒ là lỗi phổ biến.\nĐáp án: {good}.'
            B.add(q,good,rng.sample(bad,3),expl,level=2,topic='Hình thức hóa')
    # ---- 7. biến tự do / ràng buộc
    fb=[('∀x (P(x) ⇒ Q(x, y))','y','x'),('∃x P(x) ∧ Q(x)','x (xuất hiện trong Q(x) ngoài phạm vi ∃)','x trong P(x)'),('∀x ∃y (x + y = z)','z','x, y'),('∃y (R(x, y) ∧ S(y, z))','x, z','y'),('∀x P(x) ⇒ ∃y Q(y)','không có biến tự do','x, y')]
    for f,free,bound in fb:
        B.add(f'Trong công thức {f}, biến tự do là:',free,['không có biến tự do','tất cả các biến','chỉ biến đầu tiên xuất hiện'] if free!='không có biến tự do' else ['x','y','x và y'],f'Biến ràng buộc là biến nằm trong phạm vi của một lượng từ tương ứng; các biến còn lại là tự do. Ở đây biến ràng buộc: {bound}; biến tự do: {free}. Công thức có biến tự do chưa phải mệnh đề.',level=2,topic='Biến tự do / ràng buộc')
    return B
def essays(B):
    ess=[('Cho miền D = {1,2,3,4,5,6}. Xét P(x): "x là số chẵn", Q(x): "x > 4". Xác định giá trị chân lý của ∀x (Q(x) ⇒ P(x)), ∃x (P(x) ∧ ¬Q(x)), ∀x (P(x) ∨ Q(x)).',
          'Tập thỏa P: {2,4,6}; tập thỏa Q: {5,6}.\n• ∀x (Q ⇒ P): x = 5 có Q đúng, P sai ⇒ phản ví dụ ⇒ SAI.\n• ∃x (P ∧ ¬Q): x = 2 (chẵn và không > 4) ⇒ ĐÚNG.\n• ∀x (P ∨ Q): x = 1 và x = 3 không thỏa P lẫn Q ⇒ SAI.'),
         ('Viết phủ định (không dùng dấu ¬ đứng trước lượng từ) của: ∀x ∃y ((x < y) ∧ (y² < 100)).','¬∀x∃y A ≡ ∃x ¬∃y A ≡ ∃x ∀y ¬A. Với A = (x < y) ∧ (y² < 100): ¬A ≡ (x ≥ y) ∨ (y² ≥ 100).\nĐáp án: ∃x ∀y ((x ≥ y) ∨ (y² ≥ 100)).'),
         ('Hình thức hóa: "Trong lớp có một bạn mà mọi bạn khác đều quen bạn ấy". Dùng L(x): x thuộc lớp, K(x,y): x quen y.','∃y (L(y) ∧ ∀x ((L(x) ∧ x ≠ y) ⇒ K(x,y))).\nGiải thích: có ∃ nên dùng ∧ với L(y); có ∀ nên dùng ⇒ (và loại x = y).'),
         ('Chứng minh rằng ∃y∀x P(x,y) ⇒ ∀x∃y P(x,y) nhưng chiều ngược lại không đúng.','(⇒) Giả sử có y₀ sao cho ∀x P(x,y₀). Với mỗi x cho trước, chọn y = y₀ thì P(x,y) đúng ⇒ ∀x∃y P(x,y).\n(⇍) Phản ví dụ: miền ℤ, P(x,y): "x + y = 0". ∀x∃y (chọn y = −x) đúng, nhưng ∃y∀x (x + y = 0) sai vì x = 1 − y.'),
         ('Cho miền D = {1,2,3,4}. R(x,y): "x + y chẵn". Tính giá trị của ∀x∃y R(x,y) và ∃y∀x R(x,y).','R(x,y) đúng khi x, y cùng tính chẵn lẻ.\n• ∀x∃y: với mỗi x chọn y = x (x + x chẵn) ⇒ ĐÚNG.\n• ∃y∀x: cần y cùng tính chẵn lẻ với MỌI x, nhưng D có cả số chẵn lẫn lẻ ⇒ SAI.'),
         ('Chứng minh: ¬∃x (P(x) ∧ ¬Q(x)) ≡ ∀x (P(x) ⇒ Q(x)).','¬∃x A ≡ ∀x ¬A. Với A = P ∧ ¬Q: ¬A ≡ ¬P ∨ ¬¬Q ≡ ¬P ∨ Q ≡ P ⇒ Q.\nVậy ¬∃x (P ∧ ¬Q) ≡ ∀x (P ⇒ Q).'),
         ('Xét miền ℤ. Mệnh đề "∀x∈ℤ ∃y∈ℤ (x·y = 1)" đúng hay sai? Giải thích và sửa để thành mệnh đề đúng.','Sai: x = 0 không có y (0·y = 0 ≠ 1); x = 2 cũng không có y nguyên (y = 1/2).\nMệnh đề đúng gần nhất: ∃x∈ℤ ∀y∈ℤ (x·y = y) (x = 1), hoặc trên miền ℚ*: ∀x ∃y (x·y = 1).')]
    for q,s in ess: B.essay(q,s,level=2,topic='Vị từ & lượng từ')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items)); import collections; print(collections.Counter(i['topic'] for i in B.items))
