from qcore import *
import math, itertools
def S(x): return '{'+', '.join(map(str,sorted(x)))+'}' if x else '∅'
def gen(seed=3):
    B=Bank('m03',seed); rng=B.rng
    for _ in range(70):
        U=set(range(1,rng.randint(9,13))); A=set(rng.sample(sorted(U),rng.randint(3,6))); Bs=set(rng.sample(sorted(U),rng.randint(3,6))); C=set(rng.sample(sorted(U),rng.randint(3,5)))
        ops=[('A ∪ B',A|Bs),('A ∩ B',A&Bs),('A \\ B',A-Bs),('B \\ A',Bs-A),('A △ B',A^Bs),('Aᶜ (bù của A trong U)',U-A),('(A ∪ B)ᶜ',U-(A|Bs)),('A ∩ Bᶜ',A&(U-Bs)),('A ∩ (B ∪ C)',A&(Bs|C)),('(A ∩ B) ∪ C',(A&Bs)|C),('Aᶜ ∩ Bᶜ',(U-A)&(U-Bs))]
        name,val=rng.choice(ops)
        others=[v for n,v in ops if v!=val]
        wrong=[S(v) for v in rng.sample(others,3)]
        expl=f'U = {S(U)}, A = {S(A)}, B = {S(Bs)}, C = {S(C)}.\nTính {name} theo định nghĩa từng phần tử: kết quả {S(val)}.'
        if name in('(A ∪ B)ᶜ','Aᶜ ∩ Bᶜ'): expl+='\n(Luật De Morgan: (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ.)'
        B.add(f'Cho U = {S(U)}, A = {S(A)}, B = {S(Bs)}, C = {S(C)}. Tính {name}.',S(val),wrong,expl,level=1,topic='Phép toán tập hợp')
    for _ in range(40):
        a=rng.randint(15,60); b=rng.randint(15,60); ab=rng.randint(2,min(a,b)-3); tot=a+b-ab
        B.add(f'Lớp có {a} bạn học tiếng Anh, {b} bạn học tiếng Nhật, trong đó {ab} bạn học cả hai. Hỏi có bao nhiêu bạn học ít nhất một trong hai ngoại ngữ?',tot,near_ints(tot,rng,8,lo=1)+[a+b],f'|A ∪ B| = |A| + |B| − |A ∩ B| = {a} + {b} − {ab} = {tot}.\nLỗi thường gặp: cộng thẳng {a}+{b} = {a+b} sẽ đếm hai lần các bạn học cả hai.',level=1,topic='Bù trừ tập hợp')
    for _ in range(35):
        a,b,c=[rng.randint(20,50) for _ in range(3)]; ab,ac,bc=[rng.randint(4,12) for _ in range(3)]; abc=rng.randint(1,min(ab,ac,bc)); tot=a+b+c-ab-ac-bc+abc
        B.add(f'Trong một khảo sát: {a} người dùng Python, {b} dùng Java, {c} dùng C++; {ab} dùng cả Python và Java, {ac} dùng cả Python và C++, {bc} dùng cả Java và C++, {abc} dùng cả ba. Có bao nhiêu người dùng ít nhất một ngôn ngữ?',tot,near_ints(tot,rng,7,lo=1)+[tot-abc,a+b+c-ab-ac-bc],f'|A∪B∪C| = |A|+|B|+|C| − |A∩B| − |A∩C| − |B∩C| + |A∩B∩C| = {a}+{b}+{c} − {ab} − {ac} − {bc} + {abc} = {tot}.\nBiến thể sai hay gặp: quên cộng lại |A∩B∩C| (kết quả {tot-abc}).',level=2,topic='Bù trừ tập hợp')
    for n in range(2,13):
        B.add(f'Tập hợp có {n} phần tử có bao nhiêu tập con (kể cả tập rỗng và chính nó)?',2**n,[n*n,2*n,2**n-1,2**(n+1),n**2+n],f'Mỗi phần tử có 2 lựa chọn (thuộc/không thuộc tập con) nên có 2^{n} = {2**n} tập con. (Không tính tập rỗng: {2**n-1}.)',level=1,topic='Tập con')
        k=rng.randint(1,n-1)
        B.add(f'Tập hợp có {n} phần tử có bao nhiêu tập con gồm đúng {k} phần tử?',math.comb(n,k),[math.comb(n,k)+d for d in (-2,-1,1,2,3)]+[n*k,2**n],f'Số tập con {k} phần tử của tập {n} phần tử là C({n},{k}) = {math.comb(n,k)}.',level=2,topic='Tập con')
    for _ in range(25):
        a,b,c=rng.randint(2,8),rng.randint(2,8),rng.randint(2,6)
        B.add(f'|A| = {a}, |B| = {b}, |C| = {c}. Tích Descartes A × B × C có bao nhiêu phần tử?',a*b*c,[a+b+c,a*b+c,a*b*c-1,(a+b)*c],f'|A × B × C| = |A|·|B|·|C| = {a}·{b}·{c} = {a*b*c} (bộ ba (x,y,z) có thứ tự).',level=1,topic='Tích Descartes')
        B.add(f'|A| = {a}, |B| = {b}. Tập lũy thừa P(A × B) có bao nhiêu phần tử?',2**(a*b),[2**a+2**b,a*b,2**(a+b),(2**a)*b],f'|A × B| = {a}·{b} = {a*b} nên |P(A × B)| = 2^{a*b} = {2**(a*b)}. Lưu ý 2^{a}·2^{b} = 2^{a+b} = {2**(a+b)} khác 2^{a*b}.',level=3,topic='Tích Descartes')
    for _ in range(35):
        n=rng.choice([8,10]); U=list(range(1,n+1)); A=set(rng.sample(U,rng.randint(3,6))); Bs=set(rng.sample(U,rng.randint(3,6)))
        bit=lambda X:''.join('1' if u in X else '0' for u in U)
        op=rng.choice(['∪','∩','\\','△']); r={'∪':A|Bs,'∩':A&Bs,'\\':A-Bs,'△':A^Bs}[op]
        cor=bit(r)
        wr={bit(A|Bs),bit(A&Bs),bit(A-Bs),bit(A^Bs),bit(set(U)-r)}
        wr.discard(cor)
        B.add(f'Với tập vũ trụ U = {{1,…,{n}}}, xâu bit (bit thứ i = 1 nếu i ∈ tập) của A là {bit(A)} và của B là {bit(Bs)}. Xâu bit của A {op} B là:',cor,list(wr),f'A = {S(A)}, B = {S(Bs)}. Phép ∪ ↔ OR từng bit; ∩ ↔ AND; A \\ B ↔ A AND (NOT B); △ ↔ XOR.\n{bit(A)}\n{bit(Bs)}\n→ {cor}',level=2,topic='Xâu bit')
    def loops():
        yield 'for i = 1..n:  for j = 1..n:  s += 1', lambda n:n*n, 'n²', 'Vòng ngoài n lần, vòng trong n lần: n·n = n² lần.'
        yield 'for i = 1..n:  for j = 1..i:  s += 1', lambda n:n*(n+1)//2, 'n(n+1)/2', 'Tổng 1+2+…+n = n(n+1)/2 (bậc n²).'
        yield 'for i = 1..n:  for j = i..n:  s += 1', lambda n:n*(n+1)//2, 'n(n+1)/2', 'Với i cố định vòng trong chạy n−i+1 lần; tổng = n(n+1)/2.'
        yield 'for i = 1..n:  for j = 1..n:  for k = 1..n:  s += 1', lambda n:n**3, 'n³', 'Ba vòng lồng nhau độc lập: n³.'
        yield 'for i = 1..n:  for j = 1..i:  for k = 1..j:  s += 1', lambda n:n*(n+1)*(n+2)//6, 'n(n+1)(n+2)/6', 'Số bộ (i,j,k) với 1 ≤ k ≤ j ≤ i ≤ n bằng C(n+2,3).'
        yield 'i = n; while i ≥ 1:  s += 1;  i = i div 2', lambda n:n.bit_length(), '⌊log₂ n⌋ + 1', 'Mỗi vòng lặp chia đôi i nên số lần là ⌊log₂ n⌋ + 1.'
        yield 'for i = 1..n:  s += 1\nfor j = 1..n:  s += 1', lambda n:2*n, '2n', 'Hai vòng lặp nối tiếp (cộng, không nhân): n + n = 2n.'
        yield 'for i = 1..n:  for j = 1..2:  s += 1', lambda n:2*n, '2n', 'Vòng trong chỉ chạy hằng số 2 lần nên tổng 2n.'
    for _ in range(4):
        for code,fn,formula,why in loops():
            n=rng.randint(3,16); val=fn(n)
            wrong=set(near_ints(val,rng,6,lo=1))|{n*n,n*(n-1)//2,n**3}
            wrong.discard(val)
            B.add(f'Đoạn mã sau (n = {n}) thực hiện bao nhiêu lần phép "s += 1"?\n{code}',val,list(wrong),f'{why}\nTổng quát: {formula}. Với n = {n}: {val}.',level=2,topic='Đếm phép toán')
    orders=[('log₂ n',1),('√n',2),('n',3),('n·log₂ n',4),('n²',5),('n³',6),('2ⁿ',7),('n!',8)]
    for a in orders:
        for b in orders:
            if a[1]>=b[1]: continue
            for tag in range(2):
                hi,lo=(b,a) if tag==0 else (b,a)
                q=f'Khi n rất lớn, hàm nào tăng NHANH hơn: {a[0]} hay {b[0]}?' if tag==0 else f'Khi n → ∞, hàm nào tăng CHẬM hơn: {b[0]} hay {a[0]}?'
                ans=b[0] if tag==0 else a[0]
                B.add(q,ans,[b[0] if tag else a[0],'Tăng như nhau (cùng bậc)','Không so sánh được'],f'Thứ tự tăng: log n ≪ √n ≪ n ≪ n log n ≪ n² ≪ n³ ≪ 2ⁿ ≪ n!. Vậy {b[0]} tăng nhanh hơn {a[0]}.',level=1,topic='Bậc tăng trưởng')
    bigo=[('3n² + 5n + 100','O(n²)'),('n³ + 1000n²','O(n³)'),('5·2ⁿ + n¹⁰','O(2ⁿ)'),('7n·log n + 3n','O(n log n)'),('100·log₂ n + 50','O(log n)'),('(n² + n)/2','O(n²)'),('n! + 2ⁿ','O(n!)'),('2n + 10⁶','O(n)'),('n·(n+1)·(n+2)/6','O(n³)'),('√n + log n','O(√n)')]
    allo=['O(1)','O(log n)','O(√n)','O(n)','O(n log n)','O(n²)','O(n³)','O(2ⁿ)','O(n!)']
    for f,o in bigo:
        for tag in range(2):
            wrong=rng.sample([x for x in allo if x!=o],3)
            B.add(f'Độ phức tạp tiệm cận (big-O chặt) của hàm f(n) = {f} là:' if tag==0 else f'Chọn kết luận đúng: f(n) = {f} thì f(n) ∈',o,wrong,f'Giữ lại số hạng bậc cao nhất và bỏ hệ số hằng: {f} ∈ {o}. (Định nghĩa: f = O(g) nếu ∃C,k: |f(n)| ≤ C|g(n)| với n > k.)',level=2,topic='Big-O')
    for n in range(20,41):
        t=2**n/1e9
        B.add(f'Máy thực hiện 10⁹ phép tính/giây. Thuật toán vét cạn 2ⁿ với n = {n} cần thời gian xấp xỉ:',f'{t:.3g} giây',[f'{2**(n-10)/1e9:.3g} giây',f'{2**(n+10)/1e9:.3g} giây',f'{n**2/1e9:.3g} giây'],f'2^{n} = {2**n:,} phép tính ≈ {t:.3g} giây. Thuật toán mũ chỉ dùng được với n nhỏ; đây là lý do phải học nhánh cận (Module 12).',level=2,topic='Thời gian chạy')
    return B
def essays(B):
    ex=[('Chứng minh bằng biến đổi tập hợp: (A \\ B) ∪ (A ∩ B) = A.','Với mọi x: x ∈ (A \\ B) ∪ (A ∩ B) ⇔ (x ∈ A ∧ x ∉ B) ∨ (x ∈ A ∧ x ∈ B) ⇔ x ∈ A ∧ (x ∉ B ∨ x ∈ B) ⇔ x ∈ A ∧ T ⇔ x ∈ A.'),
        ('Chứng minh luật De Morgan cho tập hợp: (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ.','x ∈ (A ∪ B)ᶜ ⇔ ¬(x ∈ A ∨ x ∈ B) ⇔ (x ∉ A) ∧ (x ∉ B) ⇔ x ∈ Aᶜ ∩ Bᶜ.'),
        ('Cho A, B, C: chứng minh nếu A ⊆ B thì A ∩ C ⊆ B ∩ C.','Lấy x ∈ A ∩ C: x ∈ A và x ∈ C. Vì A ⊆ B nên x ∈ B. Vậy x ∈ B ∩ C.'),
        ('Có 120 sinh viên: 60 học Python, 50 học Java, 40 học C++, 20 học Python và Java, 15 Python và C++, 10 Java và C++, 5 học cả ba. Bao nhiêu sinh viên không học môn nào?','|P∪J∪C| = 60+50+40−20−15−10+5 = 110. Không học môn nào: 120 − 110 = 10.'),
        ('Xác định độ phức tạp thời gian (big-O) của: for i=1..n: for j=1..i: so sánh a[j] với a[j+1] (một lượt sắp xếp nổi bọt kiểu đầy đủ).','Vòng trong chạy i lần ⇒ tổng 1+2+…+n = n(n+1)/2 phép so sánh ⇒ O(n²).'),
        ('So sánh 2ⁿ và n²: tìm n₀ nhỏ nhất sao cho 2ⁿ > n² với mọi n ≥ n₀ (n nguyên dương, n ≥ 5).','n=5: 32 > 25; n=6: 64 > 36. Quy nạp: nếu 2ⁿ > n² (n ≥ 5) thì 2ⁿ⁺¹ > 2n² ≥ (n+1)² vì n² ≥ 2n+1 với n ≥ 3. Vậy 2ⁿ > n² với mọi n ≥ 5 (n=3: 8<9 và n=4: 16=16 không thỏa).'),
        ('Biểu diễn A = {2,3,5,7}, B = {1,3,5,7,9} trên U = {1,…,9} bằng xâu bit rồi tính A ∪ B, A ∩ B, A △ B.','A: 011010100; B: 101010101.\nOR: 111010101 → {1,2,3,5,7,9}\nAND: 001010100 → {3,5,7}\nXOR: 110000001 → {1,2,9}. (Lưu ý bit thứ 9 của A là 0, của B là 1.)'),
        ('Chứng minh |A ∪ B ∪ C| = |A|+|B|+|C|−|A∩B|−|A∩C|−|B∩C|+|A∩B∩C| bằng cách đếm số lần mỗi phần tử được tính.','Một phần tử thuộc đúng k tập (k=1,2,3) được đếm k − C(k,2) + C(k,3) lần: k=1: 1; k=2: 2−1 = 1; k=3: 3−3+1 = 1. Mỗi phần tử được đếm đúng một lần.'),
        ('Tập A có 10 phần tử. Có bao nhiêu quan hệ hai ngôi trên A? Bao nhiêu hàm từ A vào A?','Quan hệ = tập con của A × A (100 phần tử) ⇒ 2¹⁰⁰. Hàm từ A vào A: mỗi phần tử có 10 ảnh ⇒ 10¹⁰.'),
        ('Đoạn mã: for i=1..n: for j=1..n: if (i*j)%7==0: s++. Xác định big-O và số lần thực hiện phép so sánh chính xác.','Phép so sánh (i*j)%7 == 0 thực hiện ở mọi cặp (i,j): đúng n² lần ⇒ O(n²). (Số lần s++ phụ thuộc n nhưng không vượt n².)')]
    for q,s in ex: B.essay(q,s,level=2,topic='Tập hợp & độ phức tạp')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items)); import collections; print(collections.Counter(i['topic'] for i in B.items))
