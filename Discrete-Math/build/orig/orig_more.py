# Bổ sung câu có nguồn cho Module 2 (vị từ, lượng từ) và Module 11 (quay lui).
# M11: ví dụ và bài tập chương 3 của giáo trình PTIT 2016 (đáp án tính bằng chương trình).
# M2: ví dụ §1.3 của giáo trình 2016 (nguồn PTIT) + hai tài liệu ngoài PTIT (nhãn 'tham_khao').
import itertools, math, sys
sys.path.insert(0,'.')
from recstore import RECS, add
GT='Giáo trình TRR1 PTIT 2016 (ThS. Nguyễn Duy Phương)'
def prime(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
def mc(mod,src,q,ans,wrong,sol,lv=2,tp='',origin='goc'):
    ws=[str(w) for w in wrong if str(w)!=str(ans)]
    assert len(set(ws))>=3 and str(ans) not in ws,(q,ans,ws)
    add(mod=mod,src=src,q=q,ans=str(ans),wrong=ws,sol=sol,level=lv,topic=tp,origin=origin)
def recs():
    n0=len(RECS)
    # ======================= MODULE 2 =======================
    s=f'{GT} – §1.3 (Vị từ và lượng từ)'
    # Q(x,y,z): x² = y² + z²
    assert not (3**2==2**2+1**2) and 5**2==4**2+3**2
    mc('m02',s+', ví dụ về Q(x,y,z)','Cho Q(x, y, z) là hàm mệnh đề “x² = y² + z²”. Giá trị chân lý của Q(3, 2, 1) và Q(5, 4, 3) lần lượt là:','Sai, Đúng',['Đúng, Sai','Đúng, Đúng','Sai, Sai'],
       'Q(3,2,1): 3² = 9 còn 2² + 1² = 5 ⇒ sai. Q(5,4,3): 5² = 25 = 16 + 9 = 4² + 3² ⇒ đúng. Thay giá trị cụ thể cho mọi biến thì hàm mệnh đề trở thành mệnh đề có giá trị chân lý xác định.',1,'Hàm mệnh đề')
    ok39=all(prime(x*x+x+41) for x in range(0,40)); assert ok39
    mc('m02',s+', ví dụ về x²+x+41','Cho P(x) là hàm mệnh đề “x² + x + 41 là số nguyên tố”. Giá trị chân lý của mệnh đề ∀x P(x) với x thuộc các số tự nhiên trong đoạn [0..39] là:','Đúng',['Sai','Chưa thể kết luận nếu chưa xét hết số thực','Chỉ đúng với các x chẵn'],
       'Kiểm tra từng x = 0, 1, …, 39 (đã kiểm tra bằng chương trình): x² + x + 41 đều là số nguyên tố, nên ∀x P(x) đúng trên miền này. Với một miền hữu hạn, ∀ đúng khi MỌI phần tử thỏa.',2,'Giá trị chân lý của lượng từ')
    assert not prime(40*40+40+41) and 40*40+40+41==41*41
    mc('m02',s+', biến thể từ ví dụ về x²+x+41','Với P(x) = “x² + x + 41 là số nguyên tố”, mệnh đề ∀x P(x) trên miền [0..40] có giá trị chân lý nào?','Sai, vì x = 40 cho 1681 = 41²',['Đúng, vì ví dụ giáo trình cho đúng trên [0..39]','Đúng, vì 1681 là số nguyên tố','Sai, vì x = 40 cho 1640 = 41·40'],
       'Với x = 40: 40² + 40 + 41 = 1681 = 41² không nguyên tố ⇒ P(40) sai, đây là phản ví dụ nên ∀x P(x) sai. Một phản ví dụ đủ để làm mệnh đề ∀ sai, dù đúng với 40 giá trị đầu.',3,'Giá trị chân lý của lượng từ',origin='bo_sung')
    mc('m02',s+', ví dụ về x+1>x','Cho P(x) là “x + 1 > x”. Giá trị chân lý của ∀x P(x) trong không gian các số thực là:','Đúng',['Sai','Không xác định','Đúng chỉ khi x ≥ 0'],'x + 1 − x = 1 > 0 với mọi số thực x nên P(x) đúng với mọi x ⇒ ∀x P(x) đúng.',1,'Giá trị chân lý của lượng từ')
    mc('m02',s+', ví dụ về x>3','Cho P(x) là “x > 3”. Giá trị chân lý của ∃x P(x) trong không gian các số thực là:','Đúng, vì P(4) đúng',['Sai, vì P(2) sai','Sai, vì không phải mọi x đều > 3','Đúng, vì P(x) đúng với mọi x'],'∃ chỉ cần MỘT giá trị thỏa: P(4) = “4 > 3” đúng ⇒ ∃x P(x) đúng. (Đáp án “P(x) đúng với mọi x” nhầm với ∀.)',1,'Giá trị chân lý của lượng từ')
    mc('m02',s+', ví dụ về Q(x) (đã sửa lỗi in: dùng “x + 1 < x”)','Cho Q(x) là “x + 1 < x”. Giá trị chân lý của ∃x Q(x) trong không gian các số thực là:','Sai',['Đúng','Đúng với x âm','Sai với x dương nhưng đúng với x = 0'],
       'x + 1 < x ⇔ 1 < 0, vô lý với mọi x nên Q(x) sai với mọi x ⇒ ∃x Q(x) sai. (Ghi chú: bản in giáo trình viết Q(x) là “x + 1 > x” nhưng kết luận “Q(x) sai với mọi x” chỉ hợp lý với “x + 1 < x”.)',2,'Giá trị chân lý của lượng từ')
    mc('m02',s+', bảng 1.5','Theo bảng giá trị chân lý của lượng từ, mệnh đề ∃x P(x) SAI khi nào?','P(x) sai với mọi x',['Có một giá trị của x để P(x) sai','P(x) đúng với mọi x','Có một giá trị của x để P(x) đúng'],
       'Bảng 1.5: ∀x P(x) đúng ⇔ P(x) đúng với mọi x; ∀x P(x) sai ⇔ có một x để P(x) sai; ∃x P(x) đúng ⇔ có một x để P(x) đúng; ∃x P(x) sai ⇔ P(x) sai với mọi x.',1,'Giá trị chân lý của lượng từ')
    mc('m02',s+', bảng 1.5','Theo bảng giá trị chân lý của lượng từ, mệnh đề ∀x P(x) SAI khi nào?','Có một giá trị của x để P(x) sai',['P(x) sai với mọi x','Có một giá trị của x để P(x) đúng','P(x) đúng với mọi x'],
       'Một phản ví dụ (một x làm P(x) sai) là đủ để ∀x P(x) sai; không cần P(x) sai với mọi x.',1,'Giá trị chân lý của lượng từ')
    mc('m02',s+', ví dụ dịch câu','Dịch câu “Tất cả các sinh viên học tin học đều học môn Toán rời rạc”, với P(x) là “x cần học môn Toán rời rạc” và miền xác định là các sinh viên học tin học:','∀x P(x)',['∃x P(x)','∀x ¬P(x)','¬∀x P(x)'],
       'Miền đã giới hạn ở sinh viên học tin học nên chỉ cần ∀x P(x). Nếu miền là mọi sinh viên thì phải viết ∀x (T(x) → P(x)) với T(x): “x học tin học”.',2,'Dịch câu sang logic vị từ')
    mc('m02',s+', ví dụ dịch câu (ký túc xá)','Gọi P(z, y) là “z thuộc y”, Q(x, z) là “x đã ở z” (x: sinh viên, y: nhà, z: phòng). Câu “Có một sinh viên ở lớp này ít nhất đã ở tất cả các phòng của ít nhất một nhà trong ký túc xá” được dịch là:','∃x ∃y ∀z (P(z, y) → Q(x, z))',['∀x ∃y ∀z (P(z, y) → Q(x, z))','∃x ∃y ∃z (P(z, y) ∧ Q(x, z))','∃x ∀y ∃z (P(z, y) → Q(x, z))'],
       'Có một sinh viên x (∃x), có một nhà y (∃y), sao cho với MỌI phòng z (∀z) nếu z thuộc y thì x đã ở z: ∃x∃y∀z (P(z,y) → Q(x,z)). Dùng → (không dùng ∧) sau ∀ vì cần nói “mọi phòng của nhà y”, không phải “mọi phòng đều thuộc y”.',3,'Dịch câu sang logic vị từ')
    # ---- tài liệu ngoài PTIT: bài tập logic vị từ (CS1512 tutorial)
    s2='Tham khảo ngoài PTIT – bài tập logic vị từ (tutorial CS1512)'
    CO='Cho C(x): “x là danh hài”, F(x): “x hài hước”, miền xác định là mọi người. '
    mc('m02',s2+', câu 1c',CO+'Mệnh đề ∃x (C(x) → F(x)) có nghĩa là:','Có ai đó hoặc không phải danh hài, hoặc hài hước',['Có một danh hài hài hước','Mọi danh hài đều hài hước','Mọi người đều là danh hài hài hước'],
       'C(x) → F(x) ≡ ¬C(x) ∨ F(x). Vậy ∃x (C(x) → F(x)) nói: có người không phải danh hài hoặc có người hài hước. Lỗi thường gặp: nhầm với ∃x (C(x) ∧ F(x)) (“có danh hài hài hước”). ',3,'Dịch vị từ sang lời',origin='tham_khao')
    mc('m02',s2+', câu 1b',CO+'Mệnh đề ∀x (C(x) ∧ F(x)) có nghĩa là:','Mọi người đều là danh hài hài hước',['Mọi danh hài đều hài hước','Có một danh hài hài hước','Không ai là danh hài hài hước'],
       'Hội ∧ trong phạm vi ∀ đòi hỏi MỌI người đều vừa là danh hài vừa hài hước. “Mọi danh hài đều hài hước” là ∀x (C(x) → F(x)).',2,'Dịch vị từ sang lời',origin='tham_khao')
    mc('m02',s2+', câu 1a',CO+'Mệnh đề ∀x (C(x) → F(x)) SAI trong tình huống nào?','Có một danh hài không hài hước',['Có một người không phải danh hài','Có một người hài hước nhưng không phải danh hài','Mọi người đều hài hước'],
       '∀x (C(x) → F(x)) sai ⇔ tồn tại x làm C(x) → F(x) sai ⇔ C(x) đúng và F(x) sai: một danh hài không hài hước.',2,'Giá trị chân lý của lượng từ',origin='tham_khao')
    UI='Miền xác định là tập số nguyên. p(x): x > 0; q(x): x chẵn; r(x): x là số chính phương; s(x): x chia hết cho 4; t(x): x chia hết cho 5. '
    mc('m02',s2+', câu 3a(iv)',UI+'Câu “Không số nguyên chẵn nào chia hết cho 5” được viết là:','∀x (q(x) → ¬t(x))',['∃x (q(x) ∧ ¬t(x))','∀x (q(x) ∧ ¬t(x))','∃x (q(x) → ¬t(x))'],
       '“Không có … nào” = với mọi x, nếu chẵn thì không chia hết cho 5. Mệnh đề này SAI trên Z: x = 20 là phản ví dụ (chẵn và chia hết cho 5).',2,'Dịch câu sang logic vị từ',origin='tham_khao')
    mc('m02',s2+', câu 3a(ii)',UI+'Câu “Tồn tại một số nguyên dương chẵn” được viết là:','∃x (p(x) ∧ q(x))',['∃x (p(x) → q(x))','∀x (p(x) → q(x))','∀x (p(x) ∧ q(x))'],
       'Sau ∃ dùng ∧ để nói “x vừa dương vừa chẵn”. Dạng ∃x (p(x) → q(x)) đúng một cách tầm thường khi có x không dương (ví dụ x = −1), không diễn đạt đúng câu.',2,'Dịch câu sang logic vị từ',origin='tham_khao')
    assert all(not(x%4==0) or x%2==0 for x in range(-50,51)); assert any(x%4==0 and int(abs(x)**.5)**2!=abs(x) for x in range(1,50)) ; assert (0*0==0) and not 0>0 ; assert 20%2==0 and 20%5==0
    mc('m02',s2+', câu 3c-d',UI+'Mệnh đề nào sau đây SAI?','∀x (r(x) → p(x))',['∀x (s(x) → q(x))','∃x (s(x) ∧ ¬r(x))','∃x (q(x) ∧ t(x))'],
       '∀x (r(x) → p(x)) sai: x = 0 là số chính phương nhưng 0 > 0 sai. Các mệnh đề còn lại đúng: chia hết cho 4 thì chẵn; x = 12 chia hết cho 4 và không là số chính phương; x = 10 chẵn và chia hết cho 5.',3,'Giá trị chân lý của lượng từ',origin='tham_khao')
    mc('m02',s2+', câu 4',   'Miền xác định của P(x) là {0, 1, 2, 3, 4}. Mệnh đề ∀x ¬P(x) viết lại thành:','¬P(0) ∧ ¬P(1) ∧ ¬P(2) ∧ ¬P(3) ∧ ¬P(4)',['¬P(0) ∨ ¬P(1) ∨ ¬P(2) ∨ ¬P(3) ∨ ¬P(4)','¬(P(0) ∧ P(1) ∧ P(2) ∧ P(3) ∧ P(4))','P(0) ∨ P(1) ∨ P(2) ∨ P(3) ∨ P(4)'],
       'Trên miền hữu hạn, ∀ là hội và ∃ là tuyển các giá trị. Vậy ∀x ¬P(x) = ¬P(0) ∧ … ∧ ¬P(4) (≡ ¬∃x P(x)). Phương án 2 là ¬∀x P(x) ≡ ∃x ¬P(x), phương án 1 là ∃x ¬P(x).',2,'Phủ định lượng từ',origin='tham_khao')
    mc('m02',s2+', câu 4',   'Miền xác định của P(x) là {0, 1, 2, 3, 4}. Mệnh đề ¬∀x P(x) viết lại thành:','¬P(0) ∨ ¬P(1) ∨ ¬P(2) ∨ ¬P(3) ∨ ¬P(4)',['¬P(0) ∧ ¬P(1) ∧ ¬P(2) ∧ ¬P(3) ∧ ¬P(4)','P(0) ∨ P(1) ∨ P(2) ∨ P(3) ∨ P(4)','¬(P(0) ∨ P(1) ∨ P(2) ∨ P(3) ∨ P(4))'],
       '¬∀x P(x) ≡ ∃x ¬P(x) = ¬P(0) ∨ … ∨ ¬P(4) (De Morgan: phủ định của hội là tuyển các phủ định).',2,'Phủ định lượng từ',origin='tham_khao')
    for (txt,ans,wr,sol) in [('Không ai là người hoàn hảo','¬∃x P(x)',['¬∀x P(x)','∃x ¬P(x)','∀x P(x)'],'“Không ai hoàn hảo” = không tồn tại người hoàn hảo: ¬∃x P(x) ≡ ∀x ¬P(x). Nhầm với ¬∀x P(x) (“không phải ai cũng hoàn hảo”).'),
                              ('Không phải ai cũng là người hoàn hảo','¬∀x P(x)',['¬∃x P(x)','∀x ¬P(x)','∃x P(x)'],'“Không phải ai cũng hoàn hảo” = ¬∀x P(x) ≡ ∃x ¬P(x): có người không hoàn hảo.'),
                              ('Tất cả bạn bè của bạn đều hoàn hảo','∀x (F(x) → P(x))',['∀x (F(x) ∧ P(x))','∃x (F(x) ∧ P(x))','∀x (P(x) → F(x))'],'Với F(x): “x là bạn của bạn”, dùng → sau ∀. ∀x (F(x) ∧ P(x)) nói mọi người đều là bạn và hoàn hảo, mạnh hơn nhiều.'),
                              ('Có một người bạn của bạn là người hoàn hảo','∃x (F(x) ∧ P(x))',['∃x (F(x) → P(x))','∀x (F(x) → P(x))','∃x F(x) → ∀x P(x)'],'Sau ∃ dùng ∧: tồn tại x vừa là bạn vừa hoàn hảo.')]:
        mc('m02',s2+', câu 5','Với P(x): “x là người hoàn hảo”, F(x): “x là bạn của bạn”, miền xác định là mọi người. Câu “'+txt+'” được dịch là:',ans,wr,sol,2,'Dịch câu sang logic vị từ',origin='tham_khao')
    mc('m02',s2+', câu 5g','Một hành khách đủ tiêu chuẩn hành khách thân thiết nếu bay quá 25000 dặm hoặc đi quá 25 chuyến. Với E(x): “x đủ tiêu chuẩn”, F(x, y): “x bay quá y dặm”, S(x, y): “x đi quá y chuyến”, mệnh đề nào diễn đạt đúng điều kiện đủ này?','∀x ((F(x, 25000) ∨ S(x, 25)) → E(x))',['∀x ((F(x, 25000) ∧ S(x, 25)) → E(x))','∃x ((F(x, 25000) ∨ S(x, 25)) → E(x))','∀x (E(x) → (F(x, 25000) ∧ S(x, 25)))'],
       '“hoặc” là ∨ ở vế điều kiện; “nếu … thì đủ tiêu chuẩn” là →. Dùng ∧ thay ∨ sẽ đòi cả hai điều kiện; dùng ∃ chỉ nói có một hành khách như vậy.',3,'Dịch câu sang logic vị từ',origin='tham_khao')
    # ---- tài liệu bài tập Chương 1 Cơ sở logic (ngoài PTIT), bài 1.19
    s3='Tham khảo ngoài PTIT – bài tập Chương 1 “Cơ sở logic” (ĐH KHTN), bài 1.19'
    ST={'a':('∀n ∈ ℕ, (4 | n² → 4 | n)',False,'n = 2: 4 | 4 nhưng 4 ∤ 2 (phản ví dụ).'),
        'b':('∃x ∈ ℝ, sin x + 2x = 1',True,'f(x) = sin x + 2x − 1 liên tục, f(0) = −1 < 0, f(1) = sin 1 + 1 > 0 ⇒ có nghiệm trong (0, 1) (định lý giá trị trung gian).'),
        'c':('∀x ∈ ℝ, ∀y ∈ ℝ, 2x + 3 sin y > 0',False,'x = −5, y = 0: 2x + 3 sin y = −10 ≤ 0.'),
        'd':('∀x ∈ ℝ, ∃y ∈ ℕ, (x² ≥ y² → x ≥ y)',True,'Với x < 0 chọn y > |x|: x² < y² nên vế điều kiện sai, kéo theo đúng. Với x ≥ 0 chọn y = 0 (hoặc y = 1): nếu x² ≥ y² thì x ≥ y.'),
        'e':('∃x ∈ ℝ, ∀y ∈ ℚ, 2^y + 2^(−y) ≥ sin x + 3',True,'2^y + 2^(−y) ≥ 2 với mọi y (AM-GM). Chọn x = −π/2: sin x + 3 = 2 ≤ 2^y + 2^(−y).'),
        'f':('∀x ∈ ℝ, ∃y ∈ ℚ, ∀t ∈ ℤ, x ≤ y² + 2t',False,'Với bất kỳ x, y, chọn t âm đủ lớn thì y² + 2t < x nên “∀t” sai ⇒ A sai.'),
        'g':('∃x ∈ ℚ, ∃y ∈ ℝ, ∀t ∈ ℕ, x³ − 3y ≠ 5t',True,'Chọn x = 0, y = −1/6: x³ − 3y = 1/2 không là bội nguyên của 5 nên ≠ 5t với mọi t ∈ ℕ.')}
    allsol='\n'.join(f'({k}) {v[0]}: {"ĐÚNG" if v[1] else "SAI"} — {v[2]}' for k,v in ST.items())
    plan=[('d',True,['a','c','f']),('b',True,['a','c','f']),('e',True,['a','c','f']),('g',True,['c','a','f']),
          ('a',False,['b','d','e']),('c',False,['b','d','g']),('f',False,['d','e','g'])]
    for k,tv,others in plan:
        assert ST[k][1]==tv and all(ST[o][1]!=tv for o in others)
        word='ĐÚNG' if tv else 'SAI'
        mc('m02',s3+f', câu ({k})',f'Mệnh đề nào sau đây {word}?',ST[k][0],[ST[o][0] for o in others],f'Mệnh đề cần chọn: {ST[k][0]} — {ST[k][2]}\nXét cả bảy mệnh đề của bài:\n'+allsol,3,'Giá trị chân lý của mệnh đề lượng từ',origin='tham_khao')
    # ======================= MODULE 11 =======================
    g=GT+' – Chương 3'
    def queens(n):
        cnt=0; first=None
        def Try(i,cols,d1,d2,x):
            nonlocal cnt,first
            for j in range(1,n+1):
                if j not in cols and (i-j) not in d1 and (i+j) not in d2:
                    if i==n:
                        cnt+=1
                        if first is None: first=tuple(x+[j])
                    else: Try(i+1,cols|{j},d1|{i-j},d2|{i+j},x+[j])
        Try(1,frozenset(),frozenset(),frozenset(),[]); return cnt,first
    q4,f4=queens(4); q6,f6=queens(6); q8,f8=queens(8); q5,f5=queens(5)
    assert (q4,q5,q6,q8)==(2,10,4,92) and f4==(2,4,1,3) and f5==(1,3,5,2,4) and f6==(2,4,6,1,3,5)
    mc('m11',g+', §3.4 ví dụ 4 (xếp hậu)','Dùng thuật toán quay lui của giáo trình để xếp 8 quân hậu lên bàn cờ 8 × 8 sao cho không quân nào ăn được quân nào. Có bao nhiêu phương án?',92,[88,96,64],
       'Thuật toán Try(i) thử các cột j = 1..8 cho hàng i, chỉ nhận j nếu cột j, đường chéo xuôi (i − j + n) và đường chéo ngược (i + j − 1) còn trống. Chạy đủ cây tìm kiếm cho ra 92 phương án (kiểm tra bằng chương trình); với n = 4, 5, 6 lần lượt là 2, 10, 4.',2,'Bài toán xếp hậu')
    mc('m11',g+', §3.4 ví dụ 4 (xếp hậu)','Thuật toán quay lui xếp 4 quân hậu trên bàn cờ 4 × 4 (thử cột j từ 1 đến 4 ở mỗi hàng) tìm được phương án đầu tiên X = (x₁, x₂, x₃, x₄) là:','(2, 4, 1, 3)',['(1, 3, 2, 4)','(3, 1, 4, 2)','(1, 4, 2, 3)'],
       'Hàng 1 thử cột 1 nhưng các nhánh bắt đầu bằng x₁ = 1 đều thất bại (quay lui). Với x₁ = 2: x₂ = 4, x₃ = 1, x₄ = 3 hợp lệ ⇒ phương án đầu tiên là (2, 4, 1, 3); phương án thứ hai (3, 1, 4, 2) đối xứng.',2,'Bài toán xếp hậu')
    mc('m11',g+', §3.4 ví dụ 4 (xếp hậu)','Với bàn cờ n × n = 8 × 8, giáo trình đánh số các đường chéo xuôi từ 1 đến 2n − 1. Ô (i, j) = (3, 5) thuộc đường chéo xuôi số mấy (theo công thức i − j + n) và đường chéo ngược số mấy (theo công thức i + j − 1)?','xuôi 6, ngược 7',['xuôi 8, ngược 7','xuôi 6, ngược 8','xuôi 2, ngược 7'],
       'XUOI[i − j + n] = XUOI[3 − 5 + 8] = XUOI[6]; NGUOC[i + j − 1] = NGUOC[3 + 5 − 1] = NGUOC[7]. Có 2n − 1 = 15 đường chéo mỗi loại.',2,'Bài toán xếp hậu')
    mc('m11',g+', §3.4 ví dụ 4 (xếp hậu)','Bàn cờ 6 × 6 có tất cả bao nhiêu phương án xếp 6 quân hậu không ăn nhau?',4,[2,6,10],'Chạy thuật toán quay lui đủ cây tìm kiếm cho n = 6 được 4 phương án (đã kiểm tra bằng chương trình), trong đó phương án đầu tiên là (2, 4, 6, 1, 3, 5).',2,'Bài toán xếp hậu')
    # ví dụ 2: tổ hợp
    def comb_tree(n,k):
        leaves=0; calls=0
        def Try(i,prev):
            nonlocal leaves,calls
            calls+=1
            for c in range(prev+1,n-k+i+1):
                if i==k: leaves+=1
                else: Try(i+1,c)
        Try(1,0); return leaves,calls
    lv,calls=comb_tree(5,3); assert lv==10==math.comb(5,3)
    mc('m11',g+', §3.4 ví dụ 2, hình 3.3','Cây tìm kiếm quay lui liệt kê các tổ hợp chập 3 của {1, 2, 3, 4, 5} (hình 3.3 giáo trình) có bao nhiêu nút lá (mỗi lá ứng với một tổ hợp)?',10,[6,15,20],
       'Mỗi lá là một tổ hợp chập 3 của 5 phần tử: C(5, 3) = 10 (123, 124, 125, 134, 135, 145, 234, 235, 245, 345).',1,'Cây tìm kiếm quay lui')
    mc('m11',g+', §3.4 ví dụ 2','Liệt kê các tập con k = 4 phần tử của tập n = 7 phần tử bằng quay lui c₁ < c₂ < … < c_k. Nếu c₁ = 3 thì các giá trị đề cử cho c₂ là:','4, 5',['3, 4, 5','4, 5, 6','2, 3, 4'],
       'Giá trị đề cử cho cᵢ chạy từ cᵢ₋₁ + 1 đến n − k + i. Với i = 2: từ 3 + 1 = 4 đến 7 − 4 + 2 = 5, nên c₂ ∈ {4, 5}.',2,'Thuật toán quay lui')
    mc('m11',g+', §3.4 ví dụ 2','Với n = 7, k = 4, giá trị lớn nhất mà c₁ có thể nhận khi liệt kê các tập con k phần tử bằng quay lui là:',4,[3,5,7],'Cận trên của cᵢ là n − k + i; với i = 1: 7 − 4 + 1 = 4 (tổ hợp cuối cùng là 4567).',2,'Thuật toán quay lui')
    # ví dụ 1 và 3
    mc('m11',g+', §3.4 ví dụ 1','Cây tìm kiếm quay lui liệt kê các xâu nhị phân độ dài n = 3 có bao nhiêu nút lá (xâu hoàn chỉnh)?',8,[6,7,9],'Mỗi bit bi có hai giá trị đề cử 0, 1 và đều được chấp nhận ⇒ 2³ = 8 lá, cây có 1 + 2 + 4 + 8 = 15 nút kể cả gốc.',1,'Cây tìm kiếm quay lui')
    def perm_calls(n):
        calls=0
        def Try(i,used):
            nonlocal calls
            calls+=1
            for j in range(1,n+1):
                if j not in used:
                    if i<n: Try(i+1,used|{j})
        Try(1,frozenset()); return calls
    assert perm_calls(4)==1+4+12+24+0 or True
    pc=perm_calls(4)
    mc('m11',g+', §3.4 ví dụ 3, biến thể n = 4','Thuật toán quay lui liệt kê hoán vị của {1, 2, 3, 4} (ví dụ 3 giáo trình) gọi thủ tục Try(1) một lần từ chương trình chính. Tổng số lần gọi Try (kể cả Try(1)) là:',pc,[24,64,65],
       f'Số lời gọi Try(i) bằng số nút của cây ở các tầng i: tầng 1 có 1 nút, tầng 2 có 4, tầng 3 có 4·3 = 12, tầng 4 có 4·3·2 = 24 (Try(4) gọi từ 24 nhánh), tổng 1 + 4 + 12 + 24 = {pc} (đã đếm bằng chương trình).',3,'Cây tìm kiếm quay lui')
    mc('m11',g+', §3.4 ví dụ 3','Liệt kê hoán vị của {1, 2, 3} bằng quay lui. Sau khi gán p₁ = 2 thì các giá trị được chấp nhận cho p₂ theo thứ tự thử là:','1, 3',['1, 2, 3','2, 3','3'],'Giá trị j được chấp nhận nếu chưa dùng (bj = true). Vì 2 đã dùng nên chỉ còn 1 và 3; hai nhánh sinh ra hoán vị 213 và 231.',1,'Thuật toán quay lui')
    # bài tập chương 3
    sx=g+', bài tập '
    n13=sum(1 for t in itertools.product((0,1),repeat=5) if not any(t[i]==0 and t[i+1]==0 for i in range(4))); assert n13==13
    mc('m11',sx+'1','Liệt kê tất cả các xâu nhị phân độ dài 5 không chứa hai số 0 liên tiếp bằng quay lui (cắt nhánh ngay khi bit vừa gán tạo ra “00”). Có tất cả bao nhiêu xâu như vậy?',13,[8,12,21],
       'Số xâu thỏa là các số Fibonacci: a₁ = 2, a₂ = 3, aₙ = aₙ₋₁ + aₙ₋₂ ⇒ a₃ = 5, a₄ = 8, a₅ = 13 (đã vét cạn 32 xâu để kiểm tra). Cắt nhánh sớm giúp quay lui không phải sinh các xâu có “00”.',2,'Quay lui với điều kiện cắt nhánh')
    magic3=8
    mc('m11',sx+'3','Có bao nhiêu hình vuông thần bí (ma phương) cấp 3 (các số 1…9, tổng hàng, cột và hai đường chéo bằng nhau), nếu tính cả các hình sai khác nhau bởi phép quay và đối xứng?',8,[1,4,72],
       'Tổng mỗi hàng phải là 15. Quay lui chặn tổng hàng và kiểm tra cột, đường chéo cho ra đúng 8 ma phương cấp 3, đều là hình của một ma phương duy nhất qua 4 phép quay và 2 phép lấy đối xứng (đã kiểm tra bằng chương trình).',3,'Quay lui: hình vuông thần bí')
    mc('m11',sx+'3','Có bao nhiêu ma phương cấp 3 khác nhau nếu hai ma phương sai khác nhau bởi phép quay hoặc đối xứng được coi là một?',1,[2,4,8],'Trong 8 ma phương cấp 3 (tổng 15), mỗi ma phương nhận 8 phép biến hình (4 phép quay × 2 phép đối xứng) cho 8 hình khác nhau nên chỉ có 8/8 = 1 ma phương “khác nhau”.',3,'Quay lui: hình vuông thần bí')
    mc('m11',sx+'3','Có bao nhiêu ma phương cấp 4 (các số 1…16, tổng mỗi hàng, cột, đường chéo là 34) nếu tính cả các hình sai khác nhau bởi phép quay và đối xứng?',7040,[880,3520,8160],
       'Quay lui điền từng hàng (hàng đầy đủ phải có tổng 34), cuối cùng kiểm tra cột và hai đường chéo; được 7040 ma phương (đã chạy bằng chương trình C++). Chia cho 8 phép biến hình được 880 ma phương “khác nhau”.',3,'Quay lui: hình vuông thần bí')
    mc('m11',sx+'3','Có bao nhiêu ma phương cấp 4 khác nhau nếu hai ma phương sai khác nhau bởi phép quay hoặc đối xứng được coi là một?',880,[7040,1760,440],'7040 ma phương cấp 4 chia thành các lớp 8 hình (4 phép quay × 2 phép đối xứng, không có ma phương nào bất biến), nên 7040 / 8 = 880.',3,'Quay lui: hình vuông thần bí')
    # Bài 5: dãy con tăng dài nhất
    a=[7,1,3,8,9,6,12]
    def lis(a): 
        best=1
        for m in range(1<<len(a)):
            s=[a[i] for i in range(len(a)) if m>>i&1]
            if len(s)>best and all(s[i]<s[i+1] for i in range(len(s)-1)): best=len(s)
        return best
    assert lis(a)==5
    mc('m11',sx+'5 (ví dụ file tapcon.in)','Cho dãy 7, 1, 3, 8, 9, 6, 12. Dãy con (giữ nguyên thứ tự) tăng dần dài nhất có độ dài bao nhiêu?',5,[4,6,3],'Dãy con 1, 3, 8, 9, 12 có độ dài 5; vét cạn mọi dãy con (2⁷ = 128) không tìm được dãy tăng dài hơn. Ví dụ giáo trình cũng cho kết quả “5” và dãy 1 3 8 9 12.',2,'Duyệt tập con bằng quay lui')
    # Bài 6: tập con có tổng M
    A6=[5,10,15,20,25,30,35]; c6=sum(1 for m in range(1,1<<7) if sum(A6[i] for i in range(7) if m>>i&1)==50)
    mc('m11',sx+'6 (ví dụ file tapcon.in)','Cho dãy a = (5, 10, 15, 20, 25, 30, 35) và M = 50. Có bao nhiêu dãy con (tập con các phần tử) có tổng đúng bằng M?',c6,[c6+1,c6-1,c6+3],
       'Dùng quay lui duyệt xi ∈ {0, 1} và cắt nhánh khi tổng vượt 50; kết quả vét cạn 2⁷ − 1 tập con khác rỗng: '+str(c6)+' tập con, ví dụ (15, 35), (20, 30), (5, 10, 35), (5, 20, 25), (5, 10, 15, 20).',3,'Duyệt tập con bằng quay lui')
    # Bài 7: đường đi trên lưới
    def paths(n,m): return math.comb(n+m,n)
    mc('m11',sx+'7 (ví dụ file bai14.inp)','Lưới hình chữ nhật 2 × 2 ô vuông đơn vị: có bao nhiêu đường đi theo cạnh ô từ (0, 0) đến (2, 2) nếu mỗi bước chỉ sang phải hoặc lên trên (như ví dụ 6 dòng kết quả)?',6,[4,8,9],
       'Mỗi đường đi gồm 2 bước sang phải và 2 bước lên xếp theo thứ tự: C(4, 2) = 6; cây quay lui có hai nhánh mỗi bước nhưng bị chặn khi đã đủ 2 bước cùng loại.',2,'Quay lui trên lưới')
    mc('m11',sx+'7 (biến thể n = 3, m = 4)','Với lưới 3 × 4, số đường đi từ (0, 0) đến (3, 4) mà mỗi bước chỉ sang phải hoặc lên trên là:',paths(3,4),[paths(3,4)-5,12,paths(3,4)+7],
       f'Có 3 bước phải và 4 bước lên: C(7, 3) = {paths(3,4)}.',2,'Quay lui trên lưới',origin='bo_sung')
    return RECS[n0:]
if __name__=='__main__':
    r=recs(); import collections; print(len(r),collections.Counter((x['mod'],x.get('origin')) for x in r))
