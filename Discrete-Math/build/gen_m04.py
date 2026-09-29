from qcore import *
import math, itertools
def gen(seed=4):
    B=Bank('m04',seed); rng=B.rng
    # 1. nguyên lý cộng
    for _ in range(25):
        a,b,c=[rng.randint(5,40) for _ in range(3)]
        B.add(f'Một sinh viên có thể chọn 1 đề tài từ danh sách toán ({a} đề), danh sách tin ({b} đề) hoặc danh sách điện tử ({c} đề); các danh sách không trùng nhau. Có bao nhiêu cách chọn?',a+b+c,[a*b*c,a*b+c,a+b+c-1,a+b+c+1],f'Các danh sách rời nhau và chỉ chọn MỘT đề nên dùng QUY TẮC CỘNG: {a}+{b}+{c} = {a+b+c}.\nQuy tắc nhân chỉ dùng khi thực hiện liên tiếp các bước.',level=1,topic='Quy tắc cộng')
    # 2. nguyên lý nhân
    for _ in range(30):
        a,b,c=[rng.randint(3,9) for _ in range(3)]
        B.add(f'Một bộ đồ gồm chọn 1 áo (trong {a} áo), 1 quần (trong {b} quần) và 1 đôi giày (trong {c} đôi). Có bao nhiêu bộ đồ khác nhau?',a*b*c,[a+b+c,a*b+c,a*b*c-a,(a+b)*c],f'Ba bước độc lập liên tiếp: {a}·{b}·{c} = {a*b*c} (QUY TẮC NHÂN).',level=1,topic='Quy tắc nhân')
    for _ in range(40):
        L=rng.randint(2,4); D=rng.randint(2,4)
        ans=26**L*10**D
        B.add(f'Một biển số gồm {L} chữ cái in hoa (26 chữ cái) rồi đến {D} chữ số (0–9), chữ cái và chữ số được phép lặp. Có bao nhiêu biển số?',ans,[26*L*10*D,math.perm(26,L)*10**D,26**L*math.perm(10,D),26**L+10**D],f'Mỗi vị trí chữ cái có 26 lựa chọn, mỗi vị trí chữ số có 10: 26^{L}·10^{D} = {ans}.\nNếu không cho lặp: P(26,{L})·P(10,{D}) = {math.perm(26,L)*math.perm(10,D)}.',level=1,topic='Quy tắc nhân')
    for _ in range(30):
        L=rng.randint(3,5)
        ans=9*9*8 if L==3 else 9*9*8*7 if L==4 else 9*9*8*7*6
        cnt=sum(1 for x in range(10**(L-1),10**L) if len(set(str(x)))==L)
        assert cnt==ans
        B.add(f'Có bao nhiêu số tự nhiên có {L} chữ số mà các chữ số đôi một khác nhau?',ans,[9*10**(L-1),math.perm(10,L),9*math.perm(9,L-1)+1,10**L-10**(L-1)],f'Chữ số đầu: 9 cách (khác 0); mỗi chữ số sau: chọn trong các chữ số chưa dùng: 9, 8, … Tổng: {ans}. (Đã kiểm tra bằng liệt kê trực tiếp.)\nLỗi: dùng P(10,{L}) = {math.perm(10,L)} là cho phép chữ số đầu bằng 0.',level=2,topic='Quy tắc nhân')
    # 3. chuỗi nhị phân với điều kiện
    for n in range(4,14):
        # bắt đầu bằng 1 hoặc kết thúc bằng 00
        cnt=sum(1 for s in itertools.product('01',repeat=n) if s[0]=='1' or (s[-1]=='0' and s[-2]=='0'))
        ans=2**(n-1)+2**(n-2)-2**(n-3)
        assert cnt==ans
        B.add(f'Có bao nhiêu xâu nhị phân độ dài {n} bắt đầu bằng bit 1 HOẶC kết thúc bằng hai bit 00?',ans,[2**(n-1)+2**(n-2),2**(n-1),2**(n-1)+2**(n-2)-2**(n-3)+1,2**n-2**(n-3)],f'Bắt đầu bằng 1: 2^{n-1}; kết thúc 00: 2^{n-2}; cả hai: 2^{n-3}. Bù trừ: {2**(n-1)}+{2**(n-2)}−{2**(n-3)} = {ans}.',level=2,topic='Bù trừ')
        cnt2=2**n-1
        B.add(f'Có bao nhiêu xâu nhị phân độ dài {n} chứa ÍT NHẤT một bit 0?',2**n-1,[2**n,2**n-2,n*2**(n-1),2**(n-1)],f'Phần bù: xâu không có bit 0 (toàn bit 1) chỉ có 1 xâu. Đáp án 2^{n} − 1 = {2**n-1}.',level=1,topic='Quy tắc phần bù')
        c3=sum(1 for s in itertools.product('01',repeat=n) if s.count('1')%2==0)
        B.add(f'Có bao nhiêu xâu nhị phân độ dài {n} có số bit 1 là số chẵn (kể cả 0)?',2**(n-1),[2**(n-1)-1,2**(n-1)+1,2**n-1,n*2**(n-2)],f'Cố định n−1 bit đầu tùy ý ({2**(n-1)} cách), bit cuối được xác định để tổng số bit 1 chẵn. Đáp án {2**(n-1)}. (Kiểm tra trực tiếp: {c3}.)',level=2,topic='Quy tắc nhân')
    # 4. chia hết
    for _ in range(70):
        ds=sorted(rng.sample([2,3,4,5,6,7,8,9,10,11,12,13,14,15],rng.choice([2,3])))
        a=rng.randint(1,500); b=a+rng.randint(300,4000)
        cnt=sum(1 for x in range(a,b+1) if any(x%d==0 for d in ds))
        # bù trừ
        tot=0; parts=[]
        for m in range(1,1<<len(ds)):
            sel=[ds[i] for i in range(len(ds)) if m>>i&1]; l=1
            for d in sel: l=l*d//math.gcd(l,d)
            c=b//l-(a-1)//l; sg=1 if len(sel)%2 else -1; tot+=sg*c; parts.append(('+' if sg>0 else '−')+f'⌊{b}/{l}⌋−⌊{a-1}/{l}⌋={c}')
        assert tot==cnt
        wrong=set(near_ints(cnt,rng,6,lo=0)); wrong.add(sum(b//d-(a-1)//d for d in ds)); wrong.discard(cnt)
        neg=(b-a+1)-cnt
        if rng.random()<0.35:
            B.add(f'Có bao nhiêu số nguyên trong đoạn [{a}, {b}] KHÔNG chia hết cho số nào trong {ds}?',neg,list(set(near_ints(neg,rng,6,lo=0))|{cnt}),f'Số phần tử: {b-a+1}. Số phần tử chia hết cho ít nhất một số = {cnt} (bù trừ). Đáp án: {b-a+1} − {cnt} = {neg}.',level=3,topic='Bù trừ')
        else:
            B.add(f'Có bao nhiêu số nguyên trong đoạn từ {a} đến {b} chia hết cho ít nhất một trong các số {", ".join(map(str,ds))}?',cnt,list(wrong),'Dùng nguyên lý bù trừ (số chia hết cho bội chung nhỏ nhất):\n'+'\n'.join(parts)+f'\nTổng = {cnt}. Lỗi phổ biến: chỉ cộng các số chia hết từng số ({sum(b//d-(a-1)//d for d in ds)}) mà không trừ phần giao.',level=2,topic='Bù trừ')
    # 5. số ước
    for n in [12,18,20,24,28,30,36,40,48,50,60,72,84,90,96,100,120,144,180,360,420,720,840,1000,2024]:
        divs=[d for d in range(1,n+1) if n%d==0]
        f=[];m=n;p=2
        while m>1:
            e=0
            while m%p==0: m//=p; e+=1
            if e: f.append((p,e))
            p+=1
        exp=' · '.join(f'{p}^{e}' if e>1 else str(p) for p,e in f)
        B.add(f'Số nguyên dương {n} có bao nhiêu ước số dương?',len(divs),near_ints(len(divs),rng,5,lo=1),f'{n} = {exp}. Số ước = ∏(eᵢ+1) = '+'·'.join(f'({e}+1)' for p,e in f)+f' = {len(divs)}.',level=2,topic='Quy tắc nhân')
    # 6. đếm hàm
    for a in range(2,6):
        for b in range(2,6):
            B.add(f'Có bao nhiêu hàm số từ tập {a} phần tử vào tập {b} phần tử?',b**a,[a**b,a*b,a+b,b**a-1],f'Mỗi trong {a} phần tử của tập nguồn chọn 1 trong {b} ảnh độc lập: {b}^{a} = {b**a}.',level=2,topic='Quy tắc nhân')
            if a<=b:
                B.add(f'Có bao nhiêu đơn ánh từ tập {a} phần tử vào tập {b} phần tử?',math.perm(b,a),[b**a,math.comb(b,a),math.perm(b,a)+b,a**b],f'Ảnh của các phần tử phải khác nhau: {b}·{b-1}·…·{b-a+1} = P({b},{a}) = {math.perm(b,a)}.',level=2,topic='Quy tắc nhân')
    # 7. cộng nhân kết hợp
    for _ in range(35):
        a,b,c,d=[rng.randint(2,9) for _ in range(4)]
        B.add(f'Để đi từ A đến C có thể đi qua B: có {a} tuyến A→B và {b} tuyến B→C; hoặc đi thẳng theo {c} tuyến khác, hoặc qua D: {d} tuyến A→D và {a} tuyến D→C. Có bao nhiêu cách đi từ A đến C?',a*b+c+d*a,[a*b*c*d,(a+b)*(c+d),a*b+c+d,a*b+c*d*a],f'Ba phương án rời nhau (cộng): qua B: {a}·{b} (nhân); trực tiếp: {c}; qua D: {d}·{a}. Tổng {a*b}+{c}+{d*a} = {a*b+c+d*a}.',level=3,topic='Cộng và nhân kết hợp')
    for _ in range(25):
        n=rng.randint(5,10); k=rng.randint(2,4)
        B.add(f'Xếp {k} cuốn sách khác nhau vào {n} ô khác nhau trên giá (mỗi ô nhiều nhất 1 cuốn, có tính thứ tự các ô). Có bao nhiêu cách?',math.perm(n,k),[n**k,math.comb(n,k),math.perm(n,k)+n,k**n],f'Cuốn 1 có {n} ô, cuốn 2 còn {n-1} ô,…: P({n},{k}) = {math.perm(n,k)}.',level=2,topic='Quy tắc nhân')
    return B
def essays(B):
    ex=[('Có bao nhiêu số nguyên trong [1, 1000] chia hết cho 2, 3 hoặc 5? Trình bày bằng nguyên lý bù trừ.','|A₂|=500, |A₃|=333, |A₅|=200; |A₂∩A₃|=⌊1000/6⌋=166; |A₂∩A₅|=100; |A₃∩A₅|=⌊1000/15⌋=66; |A₂∩A₃∩A₅|=⌊1000/30⌋=33.\nTổng = 500+333+200 −166−100−66 +33 = 734.'),
        ('Có bao nhiêu xâu nhị phân độ dài 10 bắt đầu bằng 00 hoặc kết thúc bằng 11?','Bắt đầu 00: 2⁸ = 256; kết thúc 11: 2⁸ = 256; cả hai: 2⁶ = 64. Đáp án 256+256−64 = 448.'),
        ('Một mật khẩu gồm 8 ký tự lấy từ 26 chữ cái thường và 10 chữ số, phải chứa ít nhất một chữ số. Đếm số mật khẩu.','Tổng: 36⁸. Không có chữ số nào: 26⁸. Đáp án 36⁸ − 26⁸ = 2 821 109 907 456 − 208 827 064 576 = 2 612 282 842 880.'),
        ('Có bao nhiêu số nguyên dương ≤ 1000 chia hết cho 6 hoặc 15 nhưng không chia hết cho 10?','Chia hết cho 6 hoặc 15 (trong [1,1000]): 166 + 66 − 33 = 199 (bội chung nhỏ nhất 6, 15 là 30). Trong đó chia hết cho 10: bội của 30 và bội của 30 (15 với 10 → 30; 6 với 10 → 30): số bội của 30 là 33. Đáp án 199 − 33 = 166. (Kiểm tra bằng chương trình.)'),
        ('Có bao nhiêu cách chọn một mã PIN 4 chữ số không có hai chữ số liền nhau giống nhau?','Chữ số đầu: 10 cách; mỗi chữ số tiếp theo khác chữ số ngay trước: 9 cách ⇒ 10·9³ = 7290.'),
        ('Có bao nhiêu số nguyên dương có 3 chữ số mà tổng các chữ số là số chẵn?','Chữ số hàng trăm 1–9 (9 cách), hàng chục 0–9 (10 cách); chữ số hàng đơn vị được chọn để tổng chẵn: 5 cách. Đáp án 9·10·5 = 450.'),
        ('Chứng minh: số ước dương của n = p₁^e₁ ⋯ p_k^e_k là (e₁+1)⋯(e_k+1).','Mỗi ước có dạng p₁^a₁⋯p_k^a_k với 0 ≤ aᵢ ≤ eᵢ (theo tính duy nhất phân tích ra thừa số nguyên tố). Có (eᵢ+1) cách chọn aᵢ nên theo quy tắc nhân có ∏(eᵢ+1) ước.'),
        ('Có bao nhiêu xâu ký tự độ dài 6 lấy từ {a,b,c,d} chứa ít nhất một ký tự a?','Tổng 4⁶ = 4096; không có a: 3⁶ = 729. Đáp án 4096 − 729 = 3367.')]
    for q,s in ex: B.essay(q,s,level=2,topic='Nguyên lý đếm')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items)); import collections; print(collections.Counter(i['topic'] for i in B.items))
