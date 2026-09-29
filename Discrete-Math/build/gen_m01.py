from qcore import *
from logic_tools import *
def gen(seed=1, target=170):
    B=Bank('m01',seed); rng=B.rng; T='Logic mệnh đề'
    names=[('p','q','r'),('a','b','c'),('x','y','z'),('A','B','C'),('P','Q','R')]
    # ---- A: đếm số dòng Đ trong bảng chân trị
    tries=0
    while sum(1 for i in B.items if i['topic']=='Đếm dòng Đúng')<34 and tries<600:
        tries+=1
        nv=rng.choice([2,3,3,3]); vs=list(names[0][:nv]); f=rand_formula(rng,vs,rng.choice([2,3]))
        if len(vars_of(f))<nv: continue
        c=count_true(f); tot=2**nv
        vs2,rows=table(f)
        lst='; '.join(''.join(DV(x) for x in vals) for vals,r in rows if r) or '(không có)'
        expl=f'Lập bảng chân trị {tot} dòng theo thứ tự ({", ".join(vs2)}). Các dòng cho kết quả Đ: {lst}. Số dòng Đ = {c}.\nLưu ý: số dòng của bảng luôn là 2^{nv} = {tot}, đừng nhầm với số dòng Đ.'
        B.add(f'Bảng chân trị của công thức {show(f)} có bao nhiêu dòng nhận giá trị Đúng (Đ)?',c,[x for x in range(0,tot+1) if x!=c],expl,level=2,topic='Đếm dòng Đúng')
    # ---- B: phân loại hằng đúng / mâu thuẫn / thỏa được
    lib=[I(A(I(V('p'),V('q')),V('p')),V('q')),I(A(I(V('p'),V('q')),N(V('q'))),N(V('p'))),O(V('p'),N(V('p'))),A(V('p'),N(V('p'))),
         I(V('p'),O(V('p'),V('q'))),I(A(V('p'),V('q')),V('p')),E(I(V('p'),V('q')),O(N(V('p')),V('q'))),I(V('p'),I(V('q'),V('p'))),
         A(V('p'),A(V('q'),N(V('p')))),E(N(A(V('p'),V('q'))),O(N(V('p')),N(V('q')))),I(O(V('p'),V('q')),V('p')),I(V('p'),A(V('p'),V('q'))),
         I(A(I(V('p'),V('q')),I(V('q'),V('r'))),I(V('p'),V('r'))),I(A(O(V('p'),V('q')),N(V('p'))),V('q')),E(V('p'),N(V('p'))),X(V('p'),V('p')),
         I(N(V('q')),I(V('q'),V('p'))),I(I(I(V('p'),V('q')),V('p')),V('p')),E(X(V('p'),V('q')),E(V('p'),N(V('q')))),I(A(V('p'),I(V('p'),V('q'))),V('q'))]
    cand=lib[:]
    tries=0
    while len(cand)<70 and tries<800:
        tries+=1
        vs=list(names[0][:rng.choice([2,3])]); f=rand_formula(rng,vs,rng.choice([2,3]))
        if len(vars_of(f))>=2: cand.append(f)
    rng.shuffle(cand)
    K={'taut':'Hằng đúng (tautology)','contra':'Mâu thuẫn (hằng sai)','cont':'Thỏa được nhưng không hằng đúng'}
    for f0 in cand:
      for nm in rng.sample(names,2):
        mp=dict(zip(('p','q','r'),nm)); f=subst_names(f0,mp)
        k=kind(f); vs,rows=table(f)
        if k=='taut': why='Mọi dòng của bảng chân trị đều cho Đ.'
        elif k=='contra': why='Mọi dòng của bảng chân trị đều cho S.'
        else:
            ex=[(v,r) for v,r in rows if r][0]; cx=[(v,r) for v,r in rows if not r][0]
            why=f'Có dòng cho Đ ({env_str(dict(zip(vs,ex[0])))}) và có dòng cho S ({env_str(dict(zip(vs,cx[0])))}).'
        expl=f'Phân loại {show(f)}: {K[k]}.\n{why}\nBảng chân trị gồm {len(rows)} dòng: '+'; '.join(''.join(DV(x) for x in vals)+'→'+DV(r) for vals,r in rows)+'.'
        wrong=[v for kk,v in K.items() if kk!=k]+['Không thể kết luận nếu chưa biết giá trị các biến']
        B.add(f'Công thức {show(f)} thuộc loại nào?',K[k],wrong,expl,level=1 if k!='cont' else 2,topic='Phân loại công thức')
        if sum(1 for i in B.items if i['topic']=='Phân loại công thức')>=36: break
      if sum(1 for i in B.items if i['topic']=='Phân loại công thức')>=36: break
    # ---- C: cặp giá trị (F1,F2) dưới một phép gán
    tries=0
    while sum(1 for i in B.items if i['topic']=='Tính giá trị')<32 and tries<600:
        tries+=1
        nm=rng.choice(names); vs=list(nm); f1=rand_formula(rng,vs,2); f2=rand_formula(rng,vs,2)
        if f1==f2 or len(vars_of(f1))<2 or len(vars_of(f2))<2: continue
        env={v:rng.random()<0.5 for v in vs}; a,b=ev(f1,env),ev(f2,env)
        opts={f'({DV(x)}, {DV(y)})' for x in (True,False) for y in (True,False)}
        corr=f'({DV(a)}, {DV(b)})'
        expl=f'Với {env_str(env)}:\n• '+'\n• '.join(eval_steps(f1,env))+'\n'+'• '+'\n• '.join(eval_steps(f2,env))+f'\nVậy (F₁, F₂) = {corr}.'
        B.add(f'Cho {env_str(env)}. Cặp giá trị chân lý (F₁, F₂) với F₁ = {show(f1)} và F₂ = {show(f2)} lần lượt là:',corr,list(opts-{corr}),expl,level=2,topic='Tính giá trị')
    # ---- D: tương đương
    fam=[ # (dạng, danh sách công thức tương đương đúng, các gần đúng (sai))
      (I(V('p'),V('q')),[O(N(V('p')),V('q')),I(N(V('q')),N(V('p')))],[I(V('q'),V('p')),O(V('p'),N(V('q'))),I(N(V('p')),N(V('q'))),A(N(V('p')),V('q'))]),
      (N(I(V('p'),V('q'))),[A(V('p'),N(V('q')))],[A(N(V('p')),V('q')),I(N(V('p')),N(V('q'))),O(V('p'),N(V('q'))),I(V('p'),N(V('q')))]),
      (N(A(V('p'),V('q'))),[O(N(V('p')),N(V('q'))),I(V('p'),N(V('q')))],[A(N(V('p')),N(V('q'))),O(N(V('p')),V('q')),N(O(V('p'),V('q'))),O(V('p'),N(V('q')))]),
      (N(O(V('p'),V('q'))),[A(N(V('p')),N(V('q')))],[O(N(V('p')),N(V('q'))),A(N(V('p')),V('q')),N(A(V('p'),V('q'))),I(V('p'),N(V('q')))]),
      (E(V('p'),V('q')),[A(I(V('p'),V('q')),I(V('q'),V('p'))),O(A(V('p'),V('q')),A(N(V('p')),N(V('q'))))],[I(V('p'),V('q')),O(A(V('p'),N(V('q'))),A(N(V('p')),V('q'))),A(O(V('p'),V('q')),N(A(V('p'),V('q')))),O(V('p'),N(V('q')))]),
      (X(V('p'),V('q')),[O(A(V('p'),N(V('q'))),A(N(V('p')),V('q'))),N(E(V('p'),V('q')))],[E(V('p'),V('q')),O(A(V('p'),V('q')),A(N(V('p')),N(V('q')))),A(O(V('p'),V('q')),O(V('p'),V('q'))),I(V('p'),V('q'))]),
      (I(O(V('p'),V('q')),V('r')),[A(I(V('p'),V('r')),I(V('q'),V('r')))],[O(I(V('p'),V('r')),I(V('q'),V('r'))),I(V('p'),O(V('q'),V('r'))),A(I(V('p'),V('r')),I(V('r'),V('q'))),I(A(V('p'),V('q')),V('r'))]),
      (I(A(V('p'),V('q')),V('r')),[I(V('p'),I(V('q'),V('r'))),O(N(V('p')),O(N(V('q')),V('r')))],[A(I(V('p'),V('r')),I(V('q'),V('r'))),I(O(V('p'),V('q')),V('r')),I(V('p'),A(V('q'),V('r'))),O(I(V('p'),V('r')),V('q'))]),
      (I(V('p'),A(V('q'),V('r'))),[A(I(V('p'),V('q')),I(V('p'),V('r')))],[O(I(V('p'),V('q')),I(V('p'),V('r'))),I(A(V('p'),V('q')),V('r')),A(I(V('q'),V('p')),I(V('r'),V('p'))),I(V('p'),O(V('q'),V('r')))]),
      (I(V('p'),O(V('q'),V('r'))),[I(A(V('p'),N(V('q'))),V('r')),O(N(V('p')),O(V('q'),V('r')))],[I(A(V('p'),V('q')),V('r')),A(I(V('p'),V('q')),I(V('p'),V('r'))),I(O(V('p'),N(V('q'))),V('r')),O(V('p'),O(V('q'),V('r')))]),
      (N(I(V('p'),V('q'))),[A(V('p'),N(V('q')))],[N(I(V('q'),V('p'))),I(N(V('p')),V('q')),A(N(V('p')),V('q')),E(V('p'),V('q'))]),
      (O(V('p'),A(V('q'),V('r'))),[A(O(V('p'),V('q')),O(V('p'),V('r')))],[O(A(V('p'),V('q')),A(V('p'),V('r'))),A(O(V('p'),V('q')),V('r')),O(O(V('p'),V('q')),V('r')),A(A(V('p'),V('q')),O(V('p'),V('r')))]),
      (A(V('p'),O(V('q'),V('r'))),[O(A(V('p'),V('q')),A(V('p'),V('r')))],[A(O(V('p'),V('q')),O(V('p'),V('r'))),O(A(V('p'),V('q')),V('r')),A(A(V('p'),V('q')),A(V('p'),V('r'))),O(V('p'),A(V('q'),V('r')))]),
      (I(N(V('p')),V('q')),[O(V('p'),V('q')),I(N(V('q')),V('p'))],[O(N(V('p')),V('q')),I(V('p'),N(V('q'))),A(V('p'),V('q')),I(V('q'),N(V('p')))]),
      (N(E(V('p'),V('q'))),[E(V('p'),N(V('q'))),X(V('p'),V('q'))],[E(N(V('p')),N(V('q'))),I(V('p'),V('q')),A(V('p'),N(V('q'))),E(V('p'),V('q'))]),
    ]
    made=0
    for base,good,bad in fam:
      for nm in names:
        mp=dict(zip(('p','q','r'),nm)); b=subst_names(base,mp)
        for g in good:
          gg=subst_names(g,mp)
          bd=[subst_names(x,mp) for x in bad if not equiv(base,x)]
          if len(bd)<3 or not equiv(base,g): continue
          wrong=[show(x) for x in rng.sample(bd,3)]
          wf=[x for x in bd if show(x) in wrong]
          notes='\n'.join(f'• {show(x)} ≢ {show(b)}: phản ví dụ {env_str(counterexample(b,x))} (vế trái = {DV(ev(b,counterexample(b,x)))}, công thức này = {DV(ev(x,counterexample(b,x)))}).' for x in wf)
          expl=f'Đáp án đúng: {show(gg)} ≡ {show(b)} (kiểm tra bằng bảng chân trị hoặc luật tương đương).\nCác phương án còn lại sai:\n{notes}'
          if B.add(f'Công thức nào sau đây tương đương logic với {show(b)}?',show(gg),wrong,expl,level=2,topic='Tương đương logic'): made+=1
          break
    # ---- E: nghịch đảo / đảo / phản đảo
    stm=[('trời mưa','đường ướt'),('An học chăm','An đạt điểm cao'),('n chia hết cho 6','n chia hết cho 3'),('tam giác cân','tam giác có hai góc bằng nhau'),('chương trình có lỗi','chương trình không chạy đúng'),
         ('tôi có mật khẩu','tôi đăng nhập được'),('số nguyên tố lớn hơn 2','số đó lẻ'),('mạng bị ngắt','ứng dụng báo lỗi'),('x là số chẵn','x² là số chẵn'),('máy chủ quá tải','trang web chậm')]
    for a,b in stm:
      for rot in range(2):
        for which in ['đảo','phản đảo','nghịch']:
            orig=f'Nếu {a} thì {b}'
            conv=f'Nếu {b} thì {a}'; contra=f'Nếu không ({b}) thì không ({a})'; inv=f'Nếu không ({a}) thì không ({b})'
            tgt={'đảo':conv,'phản đảo':contra,'nghịch':inv}[which]
            wrong=[x for x in [conv,contra,inv,f'{a} và {b}',f'Không ({a}) hoặc {b}',f'{a} nhưng không ({b})'] if x!=tgt and x!=f'Không ({a}) hoặc {b}'][:5]
            expl=(f'Từ P ⇒ Q với P = "{a}", Q = "{b}":\n• Mệnh đề đảo: Q ⇒ P.\n• Mệnh đề phản đảo: ¬Q ⇒ ¬P (LUÔN tương đương với P ⇒ Q).\n• Mệnh đề nghịch: ¬P ⇒ ¬Q (tương đương với mệnh đề đảo, KHÔNG tương đương P ⇒ Q).\nNên đáp án là: {tgt}.')
            B.add(f'Cho mệnh đề "{orig}". Mệnh đề {which} của nó là:',tgt,wrong,expl,level=1,topic='Đảo / phản đảo')
    for a,b in stm[:8]:
        orig=f'Nếu {a} thì {b}'; contra=f'Nếu không ({b}) thì không ({a})'
        wrong=[f'Nếu {b} thì {a}',f'Nếu không ({a}) thì không ({b})',f'{a} và không ({b})',f'Không ({a}) hoặc không ({b})']
        B.add(f'Mệnh đề nào luôn có cùng giá trị chân lý với "{orig}"?',contra,wrong,f'Phản đảo ¬Q ⇒ ¬P ≡ P ⇒ Q (luật phản đảo). Đảo và nghịch chỉ tương đương nhau, không tương đương với P ⇒ Q (ví dụ phản chứng: P sai, Q đúng).',level=2,topic='Đảo / phản đảo')
        wrong=[f'{a} và {b}',f'Nếu không ({a}) thì {b}',f'{a} hoặc không ({b})',f'Không ({a}) và {b}']
        B.add(f'Phủ định của mệnh đề "{orig}" là:',f'{a} và không ({b})',wrong,'¬(P ⇒ Q) ≡ P ∧ ¬Q. Mệnh đề P ⇒ Q chỉ sai khi P đúng mà Q sai nên phủ định của nó là "P và không Q".',level=2,topic='Phủ định')
    # ---- F: dịch câu → công thức
    pat=[('Nếu {p} thì {q}',lambda p,q:I(p,q)),('{p} khi và chỉ khi {q}',lambda p,q:E(p,q)),('{p} chỉ khi {q}',lambda p,q:I(p,q)),('{p} nếu {q}',lambda p,q:I(q,p)),
         ('{p} trừ khi {q}',lambda p,q:I(N(q),p)),('Hoặc {p} hoặc {q} (nhưng không cả hai)',lambda p,q:X(p,q)),('{p} là điều kiện đủ để {q}',lambda p,q:I(p,q)),('{p} là điều kiện cần để {q}',lambda p,q:I(q,p)),
         ('Không ({p} và {q})',lambda p,q:N(A(p,q))),('{p} nhưng không {q}',lambda p,q:A(p,N(q)))]
    atoms=[('trời mưa','tôi ở nhà'),('bạn học bài','bạn qua môn'),('đèn sáng','có điện'),('file tồn tại','chương trình đọc được file'),('n chia hết cho 4','n chẵn'),('mạng ổn định','tải nhanh')]
    for (tp,fn) in pat:
      for pa,qa in atoms[:5]:
        p,q=V('p'),V('q'); f=fn(p,q)
        cands=[I(p,q),I(q,p),E(p,q),X(p,q),A(p,N(q)),N(A(p,q)),I(N(q),p),I(N(p),N(q)),I(N(p),q),A(p,q),O(p,q)]
        bd=[c for c in cands if not equiv(f,c)]
        wrong=[show(c) for c in rng.sample(bd,3)]
        sent=tp.format(p=pa,q=qa)
        expl=f'Đặt p = "{pa}", q = "{qa}". Câu "{sent}" dịch thành {show(f)}.\nGhi nhớ: "p chỉ khi q" ≡ p ⇒ q; "p nếu q" ≡ q ⇒ p; "điều kiện đủ" ở vế p (p ⇒ q); "điều kiện cần" ở vế q (q ⇒ p); "p trừ khi q" ≡ ¬q ⇒ p.'
        B.add(f'Đặt p = "{pa}", q = "{qa}". Câu "{sent}" được biểu diễn bởi công thức nào?',show(f),wrong,expl,level=2,topic='Dịch câu sang logic')
        break
    for (tp,fn) in pat:
      for pa,qa in atoms[1:4]:
        p,q=V('p'),V('q'); f=fn(p,q); cands=[I(p,q),I(q,p),E(p,q),X(p,q),A(p,N(q)),N(A(p,q)),I(N(q),p),I(N(p),N(q)),I(N(p),q),A(p,q),O(p,q)]
        bd=[c for c in cands if not equiv(f,c)]; wrong=[show(c) for c in rng.sample(bd,3)]; sent=tp.format(p=pa,q=qa)
        B.add(f'Với p = "{pa}", q = "{qa}", hãy chọn công thức biểu diễn đúng câu: "{sent}".',show(f),wrong,f'Đáp án {show(f)}. Nhớ: "chỉ khi" và "điều kiện đủ" đặt ở vế trái của ⇒; "nếu" và "điều kiện cần" đặt ở vế phải.',level=3,topic='Dịch câu sang logic')
    # ---- G: thao tác bit
    for i in range(24):
        n=8; a=''.join(rng.choice('01') for _ in range(n)); b=''.join(rng.choice('01') for _ in range(n)); op=rng.choice(['AND','OR','XOR'])
        f={'AND':lambda x,y:x&y,'OR':lambda x,y:x|y,'XOR':lambda x,y:x^y}[op]
        r=''.join(str(f(int(x),int(y))) for x,y in zip(a,b))
        wr=set()
        for o2,f2 in [('AND',lambda x,y:x&y),('OR',lambda x,y:x|y),('XOR',lambda x,y:x^y)]:
            if o2!=op: wr.add(''.join(str(f2(int(x),int(y))) for x,y in zip(a,b)))
        wr.add(''.join(str(1-int(c)) for c in r)); wr.add(r[1:]+r[0])
        wr.discard(r)
        B.add(f'Cho hai xâu bit {a} và {b}. Kết quả phép {op} theo từng bit là:',r,list(wr),f'Thực hiện {op} từng cặp bit tương ứng:\n{a}\n{b}\n{"-"*n}\n{r}\nAND = 1 khi cả hai bit là 1; OR = 0 khi cả hai bit là 0; XOR = 1 khi hai bit khác nhau.',level=1,topic='Phép toán bit')
    # ---- H: khái niệm
    B.add('Câu nào sau đây KHÔNG phải là một mệnh đề logic?','x + 2 = 5',['5 là số nguyên tố','Hà Nội là thủ đô của Việt Nam','2 + 2 = 5'],'Mệnh đề là câu khẳng định có giá trị chân lý xác định (Đúng hoặc Sai). "x + 2 = 5" phụ thuộc vào x nên chưa xác định; đó là một vị từ (sẽ học ở Module 2). "2 + 2 = 5" là mệnh đề SAI (vẫn là mệnh đề).',level=1,topic='Khái niệm')
    fb=[('Bây giờ là mấy giờ?','Câu hỏi không có giá trị chân lý.'),('Hãy đóng cửa lại!','Câu mệnh lệnh không có giá trị chân lý.'),('x + y > 0','Chứa biến tự do nên chưa xác định Đúng/Sai.'),('Bài này khó quá!','Câu cảm thán/chủ quan, không có giá trị chân lý xác định.')]
    ok=['Số 17 là số nguyên tố','1 + 1 = 3','Hà Nội là thủ đô của Việt Nam','Mọi số chẵn đều chia hết cho 2','Có vô hạn số nguyên tố','7 chia hết cho 2']
    for s,why in fb:
        for k in range(3):
            w=rng.sample(ok,3)
            B.add(f'Trong các câu sau, câu nào KHÔNG phải mệnh đề?' if k==0 else ('Câu nào dưới đây không thể gán giá trị Đúng/Sai?' if k==1 else 'Chọn câu không phải mệnh đề:'),s,w,f'"{s}": {why} Ba câu còn lại đều có giá trị chân lý xác định (kể cả câu Sai như "1 + 1 = 3").',level=1,topic='Khái niệm')
    # bảng chân trị các phép nối
    tbl=[('p ⇒ q','chỉ sai khi p đúng và q sai'),('p ∧ q','chỉ đúng khi cả p và q đúng'),('p ∨ q','chỉ sai khi cả p và q sai'),('p ⊕ q','đúng khi p và q khác giá trị'),('p ⇔ q','đúng khi p và q cùng giá trị')]
    for f,d in tbl:
        for k,others in enumerate([[x for x,_ in tbl if x!=f]]*1):
            wrong=[dd for x,dd in tbl if x!=f][:3]
            B.add(f'Phát biểu nào đúng về phép nối {f}?',d,wrong,f'{f}: {d}.',level=1,topic='Khái niệm')
    # số dòng bảng chân trị
    for n in range(2,8):
        B.add(f'Bảng chân trị đầy đủ của một công thức có {n} biến mệnh đề độc lập có bao nhiêu dòng?',2**n,[n*n,2*n,n**2+1,2**n-1,2**(n+1),n*2**n][:6],f'Mỗi biến nhận 2 giá trị (Đ, S) và các biến độc lập nên số dòng = 2^{n} = {2**n}.',level=1,topic='Khái niệm')
    for n in range(2,6):
        B.add(f'Có bao nhiêu công thức (hàm chân trị) khác nhau theo {n} biến p₁…p_{n} (hai công thức có cùng bảng chân trị coi là một)?',2**(2**n),[2**n,n**2,2**(2**n-1),2**(n+1)+1],f'Bảng chân trị có 2^{n} = {2**n} dòng, mỗi dòng chọn Đ hoặc S độc lập nên có 2^(2^{n}) = {2**(2**n)} hàm.',level=3,topic='Khái niệm')
    # suy luận hợp lệ
    args=[('Modus ponens','p ⇒ q; p','q',True),('Modus tollens','p ⇒ q; ¬q','¬p',True),('Tam đoạn luận giả định','p ⇒ q; q ⇒ r','p ⇒ r',True),('Tam đoạn luận tuyển','p ∨ q; ¬p','q',True),
          ('Khẳng định hậu kiện (SAI)','p ⇒ q; q','p',False),('Phủ định tiền kiện (SAI)','p ⇒ q; ¬p','¬q',False),('Hợp (conjunction)','p; q','p ∧ q',True),('Cộng (addition)','p','p ∨ q',True),('Suy luận sai','p ∨ q; p','¬q',False),('Suy luận sai','p ⇒ q; r ⇒ q','p ⇒ r',False)]
    for nm,pre,con,valid in args:
        prem=[x.strip() for x in pre.split(';')]
        def parse(sx):
            return sx
        for k in range(2):
            corr='Hợp lệ (luôn đúng khi các tiền đề đúng)' if valid else 'Không hợp lệ (tồn tại phép gán tiền đề đúng, kết luận sai)'
            wrong=['Hợp lệ chỉ khi q đúng','Không xác định được nếu chưa biết giá trị p, q','Hợp lệ vì kết luận đúng trong một số trường hợp'] if not valid else ['Không hợp lệ vì kết luận không xuất hiện trong tiền đề','Không xác định được nếu chưa biết giá trị p, q','Hợp lệ chỉ khi mọi biến đều đúng']
            expl=f'Suy luận "{pre}  ⊢  {con}" '+('là quy tắc suy diễn chuẩn ('+nm+'): công thức (tiền đề₁ ∧ tiền đề₂) ⇒ kết luận là hằng đúng.' if valid else 'là ngụy biện: chọn phép gán làm tiền đề đúng mà kết luận sai (ví dụ p=S, q=Đ với "khẳng định hậu kiện") để chứng minh không hợp lệ.')
            B.add(f'Suy luận với tiền đề: {pre} và kết luận: {con}. Nhận xét nào đúng?' if k==0 else f'Xét quy tắc "{pre}  ⊢  {con}". Chọn đánh giá đúng:',corr,wrong,expl,level=2,topic='Quy tắc suy diễn')
    # thứ tự ưu tiên (đáp án và nhiễu đều là công thức thật, kiểm chứng không tương đương)
    prio=[(O(V('p'),A(V('q'),V('r'))),'p ∨ q ∧ r',[O(A(V('p'),V('q')),V('r')),A(O(V('p'),V('q')),V('r')),N(O(V('p'),A(V('q'),V('r')))),I(V('p'),A(V('q'),V('r')))]),
          (A(N(V('p')),V('q')),'¬p ∧ q',[N(A(V('p'),V('q'))),A(V('p'),V('q')),O(N(V('p')),V('q')),N(A(N(V('p')),V('q')))]),
          (I(V('p'),I(V('q'),V('r'))),'p ⇒ q ⇒ r (⇒ kết hợp phải)',[I(I(V('p'),V('q')),V('r')),I(A(V('p'),V('q')),V('r')),A(I(V('p'),V('q')),I(V('q'),V('r'))),E(V('p'),I(V('q'),V('r')))]),
          (I(A(V('p'),V('q')),O(V('r'),V('s'))),'p ∧ q ⇒ r ∨ s',[A(V('p'),I(V('q'),O(V('r'),V('s')))),O(I(A(V('p'),V('q')),V('r')),V('s')),I(V('p'),A(V('q'),O(V('r'),V('s')))),A(I(V('p'),V('q')),O(V('r'),V('s')))])]
    for f,txt,bad in prio:
        bd=[x for x in bad if not equiv(f,x)]
        B.add(f'Theo thứ tự ưu tiên chuẩn (¬ trước, rồi ∧, ∨, ⇒, ⇔), biểu thức "{txt.split(" (")[0]}" được hiểu là:',show(f),[show(x) for x in bd[:3]],'Thứ tự: ¬ ưu tiên cao nhất, sau đó ∧, rồi ∨, rồi ⇒ (kết hợp từ phải sang), cuối cùng ⇔. Khi không chắc, hãy đặt ngoặc tường minh.',level=2,topic='Khái niệm')
    return B
if __name__=='__main__':
    B=gen(); print(len(B.items),audit(B.items)); import collections; print(collections.Counter(i['topic'] for i in B.items))

def essays(B):
    rng=B.rng
    chains=[
     ('¬(p ∨ (¬p ∧ q)) ≡ ¬p ∧ ¬q', lambda p,q,r:(N(O(p,A(N(p),q))),A(N(p),N(q))),
      ['¬(p ∨ (¬p ∧ q)) ≡ ¬p ∧ ¬(¬p ∧ q)   (De Morgan)','≡ ¬p ∧ (p ∨ ¬q)   (De Morgan, phủ định kép)','≡ (¬p ∧ p) ∨ (¬p ∧ ¬q)   (phân phối)','≡ F ∨ (¬p ∧ ¬q)   (luật phần tử bù)','≡ ¬p ∧ ¬q   (luật đồng nhất)']),
     ('¬p ⇒ (q ⇒ r) ≡ q ⇒ (p ∨ r)', lambda p,q,r:(I(N(p),I(q,r)),I(q,O(p,r))),
      ['VT: ¬p ⇒ (q ⇒ r) ≡ ¬(¬p) ∨ (¬q ∨ r)   (P⇒Q ≡ ¬P∨Q, hai lần)','≡ p ∨ ¬q ∨ r   (phủ định kép, kết hợp)','VP: q ⇒ (p ∨ r) ≡ ¬q ∨ (p ∨ r) ≡ p ∨ ¬q ∨ r   (giao hoán, kết hợp)','Hai vế cùng bằng p ∨ ¬q ∨ r nên tương đương. (Đây là dạng câu 1a trong đề thi 2017-2020.)']),
     ('(p ∧ q) ⇒ p là hằng đúng', lambda p,q,r:(I(A(p,q),p),None),
      ['(p ∧ q) ⇒ p ≡ ¬(p ∧ q) ∨ p   (P⇒Q ≡ ¬P∨Q)','≡ (¬p ∨ ¬q) ∨ p   (De Morgan)','≡ (¬p ∨ p) ∨ ¬q   (giao hoán, kết hợp)','≡ T ∨ ¬q ≡ T   (luật phần tử bù, luật nuốt)']),
     ('p ⇒ (q ⇒ p) là hằng đúng', lambda p,q,r:(I(p,I(q,p)),None),
      ['p ⇒ (q ⇒ p) ≡ ¬p ∨ (¬q ∨ p)','≡ (¬p ∨ p) ∨ ¬q   (giao hoán, kết hợp)','≡ T ∨ ¬q ≡ T']),
     ('[(p ⇒ q) ∧ (q ⇒ r)] ⇒ (p ⇒ r) là hằng đúng (tam đoạn luận giả định)', lambda p,q,r:(I(A(I(p,q),I(q,r)),I(p,r)),None),
      ['Viết P⇒Q ≡ ¬P∨Q: ≡ ¬[(¬p ∨ q) ∧ (¬q ∨ r)] ∨ (¬p ∨ r)','De Morgan: ≡ [(p ∧ ¬q) ∨ (q ∧ ¬r)] ∨ ¬p ∨ r','Nhóm: [(p ∧ ¬q) ∨ ¬p] ∨ [(q ∧ ¬r) ∨ r]','Phân phối: (p ∧ ¬q) ∨ ¬p ≡ (p ∨ ¬p) ∧ (¬q ∨ ¬p) ≡ ¬q ∨ ¬p;  (q ∧ ¬r) ∨ r ≡ (q ∨ r) ∧ (¬r ∨ r) ≡ q ∨ r','Kết hợp: ¬q ∨ ¬p ∨ q ∨ r ≡ (¬q ∨ q) ∨ ¬p ∨ r ≡ T']),
     ('p ⊕ q ≡ (p ∨ q) ∧ ¬(p ∧ q)', lambda p,q,r:(X(p,q),A(O(p,q),N(A(p,q)))),
      ['p ⊕ q đúng khi đúng một trong hai: p ⊕ q ≡ (p ∧ ¬q) ∨ (¬p ∧ q)   (định nghĩa)','Phân phối ∨ qua ∧: ≡ (p ∨ ¬p) ∧ (p ∨ q) ∧ (¬q ∨ ¬p) ∧ (¬q ∨ q)','Bỏ các thừa số T: ≡ (p ∨ q) ∧ (¬p ∨ ¬q)','De Morgan: ¬p ∨ ¬q ≡ ¬(p ∧ q) nên ≡ (p ∨ q) ∧ ¬(p ∧ q)']),
     ('p ⇔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q)', lambda p,q,r:(E(p,q),O(A(p,q),A(N(p),N(q)))),
      ['p ⇔ q ≡ (p ⇒ q) ∧ (q ⇒ p)   (định nghĩa)','≡ (¬p ∨ q) ∧ (¬q ∨ p)','Phân phối: ≡ (¬p ∧ ¬q) ∨ (¬p ∧ p) ∨ (q ∧ ¬q) ∨ (q ∧ p)','Hai hạng tử giữa bằng F: ≡ (p ∧ q) ∨ (¬p ∧ ¬q)']),
     ('¬(p ⇔ q) ≡ p ⇔ ¬q', lambda p,q,r:(N(E(p,q)),E(p,N(q))),
      ['¬(p ⇔ q) ≡ ¬((p ⇒ q) ∧ (q ⇒ p)) ≡ ¬(p ⇒ q) ∨ ¬(q ⇒ p)','≡ (p ∧ ¬q) ∨ (q ∧ ¬p)   (phủ định của ⇒)','Mặt khác p ⇔ ¬q ≡ (p ∧ ¬q) ∨ (¬p ∧ ¬¬q) ≡ (p ∧ ¬q) ∨ (¬p ∧ q)','Hai vế bằng nhau nên tương đương.']),
     ('[p ∧ (p ⇒ q)] ⇒ q là hằng đúng (modus ponens)', lambda p,q,r:(I(A(p,I(p,q)),q),None),
      ['≡ ¬[p ∧ (¬p ∨ q)] ∨ q','≡ ¬p ∨ ¬(¬p ∨ q) ∨ q   (De Morgan)','≡ ¬p ∨ (p ∧ ¬q) ∨ q','≡ (¬p ∨ p) ∧ (¬p ∨ ¬q) ∨ q ≡ (¬p ∨ ¬q) ∨ q ≡ T']),
     ('[(p ∨ q) ∧ (¬p ∨ r)] ⇒ (q ∨ r) là hằng đúng (phân giải)', lambda p,q,r:(I(A(O(p,q),O(N(p),r)),O(q,r)),None),
      ['Xét hai trường hợp theo p.','Nếu p = Đ: tiền đề ¬p ∨ r ≡ r nên r = Đ, suy ra q ∨ r = Đ.','Nếu p = S: tiền đề p ∨ q ≡ q nên q = Đ, suy ra q ∨ r = Đ.','Mọi trường hợp làm tiền đề đúng đều cho kết luận đúng nên công thức là hằng đúng.']),
    ]
    nm=[('p','q','r'),('a','b','c'),('x','y','z')]
    for title,mk,steps in chains:
        for names in nm[:2]:
            mp=dict(zip(('p','q','r'),names))
            f,g=mk(V('p'),V('q'),V('r'))
            ok=(kind(f)=='taut') if g is None else equiv(f,g)
            assert ok,title
            t=title; st=list(steps)
            for k,v in mp.items(): 
                t=t.replace(k,'§'+v); st=[x.replace(k,'§'+v) for x in st]
            t=t.replace('§',''); st=[x.replace('§','') for x in st]
            B.essay(f'Không dùng bảng chân trị, hãy chứng minh (bằng các phép biến đổi tương đương): {t}.','\n'.join(f'{i+1}. {x}' for i,x in enumerate(st)),level=2,topic='Biến đổi tương đương')
    # bảng chân trị
    cand=[I(A(I(V('p'),V('q')),I(V('q'),V('r'))),I(V('p'),V('r'))),E(N(A(V('p'),V('q'))),O(N(V('p')),N(V('q')))),I(A(O(V('p'),V('q')),N(V('p'))),V('q')),E(I(V('p'),I(V('q'),V('r'))),I(A(V('p'),V('q')),V('r'))),E(A(V('p'),O(V('q'),V('r'))),O(A(V('p'),V('q')),A(V('p'),V('r'))))]
    for f in cand:
        vs,rows=table(f); sub=[]
        # thêm cột phụ: dạng bảng chữ
        lines=[' | '.join(vs)+' | '+show(f)]
        for vals,r in rows: lines.append(' | '.join(DV(x) for x in vals)+' | '+DV(r))
        B.essay(f'Lập bảng chân trị và cho biết công thức {show(f)} thuộc loại nào (hằng đúng, mâu thuẫn, thỏa được)?','\n'.join(lines)+f'\nKết luận: {"hằng đúng" if kind(f)=="taut" else ("mâu thuẫn" if kind(f)=="contra" else "thỏa được nhưng không hằng đúng")}.',level=1,topic='Bảng chân trị')
