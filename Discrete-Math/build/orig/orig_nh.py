import re, json, math, itertools, sys
sys.path.insert(0,'..')
from parse_nh import load, split_parts
import orig_lib as L
from orig_lib import sub, T
from qcore import near_ints, fm
SRC='Ngân hàng câu hỏi tự luận INT1358 (2019)'
import unicodedata
def clean(s): 
    s=unicodedata.normalize('NFKC',s).replace('\uf0d9','∧').replace('\uf0da','∨')
    return re.sub(r'\s+',' ',s.replace('\n',' ')).strip()
def parse_constraints(txt,k):
    lo=[0]*k; hi=[None]*k
    t=txt.replace('≤','<=').replace('≥','>=')
    t=re.sub(r'x\s*_?(\d)',lambda m:'x'+m.group(1),t)
    # chuỗi: a >= xi >= b  |  a <= xi <= b
    for m in re.finditer(r'(\d+)\s*(>=|<=)\s*x(\d)\s*(>=|<=)\s*(\d+)',t):
        a,o1,i,o2,b=int(m.group(1)),m.group(2),int(m.group(3))-1,m.group(4),int(m.group(5))
        if o1=='>=': hi[i]=a; lo[i]=b
        else: lo[i]=a; hi[i]=b
    t2=re.sub(r'(\d+)\s*(>=|<=)\s*x(\d)\s*(>=|<=)\s*(\d+)','',t)
    for m in re.finditer(r'x(\d)\s*(>=|<=)?\s*(\d+)',t2):
        i=int(m.group(1))-1; c=int(m.group(3)); o=m.group(2) or '>='
        if o=='>=': lo[i]=max(lo[i],c)
        else: hi[i]=c
    m=re.search(r'x\s*i\s*(>=)\s*(\d+)\s*với\s*i\s*=\s*1',t)
    if m: lo=[int(m.group(2))]*k
    return lo,hi
def cons_text(lo,hi):
    out=[]
    for i,(l,h) in enumerate(zip(lo,hi)):
        if h is not None: out.append(f'{h} ≥ x{sub(i+1)} ≥ {l}')
        elif l: out.append(f'x{sub(i+1)} ≥ {l}')
    return ', '.join(out)
def rec_solve(cs,a0):
    from fractions import Fraction as Fr
    k=len(cs)
    # nghiệm nguyên của r^k - c1 r^{k-1} - ... - ck
    poly=[1]+[-c for c in cs]; roots=[]
    cand=[d for d in range(-60,61) if d]
    p=poly[:]
    for r in cand:
        while len(p)>1 and sum(c*r**(len(p)-1-i) for i,c in enumerate(p))==0:
            roots.append(r); q=[p[0]]
            for c in p[1:-1]: q.append(c+r*q[-1])
            p=q
    if len(p)>1: return None
    from collections import Counter
    mult=Counter(roots); basis=[(r,j) for r in sorted(mult) for j in range(mult[r])]
    M=[[Fr(r)**n*(Fr(n)**j if not(j>0 and n==0) else (Fr(0) if j>0 else 1)) for (r,j) in basis]+[Fr(a0[n])] for n in range(k)]
    for n in range(k):
        for q_,(r,j) in enumerate(basis): M[n][q_]=Fr(r)**n*(Fr(n)**j if (j>0 and n>0) else (Fr(1) if j==0 else Fr(0)))
    for c in range(k):
        pv=next(i for i in range(c,k) if M[i][c]!=0); M[c],M[pv]=M[pv],M[c]; d=M[c][c]; M[c]=[x/d for x in M[c]]
        for i in range(k):
            if i!=c and M[i][c]!=0:
                f=M[i][c]; M[i]=[x-f*y for x,y in zip(M[i],M[c])]
    coefs=[M[i][k] for i in range(k)]
    return dict(mult=mult,basis=basis,coefs=coefs)
def fmt_sol(sol):
    parts=[]
    for c,(r,j) in zip(sol['coefs'],sol['basis']):
        if c==0: continue
        a=abs(c); cs=str(a) if a!=1 else ''
        if c.denominator!=1: cs=f'({abs(c.numerator)}/{c.denominator})'
        base=(f'({r})ⁿ' if r<0 else (f'{r}ⁿ' if r!=1 else ''))
        pw='' if j==0 else ('n' if j==1 else f'n^{j}')
        term='·'.join(x for x in (cs,pw,base) if x) or '1'
        if not(cs or pw or base): term='1'
        if r==1 and j==0: term=cs or '1'
        parts.append(('−' if c<0 else ('+' if parts else ''))+((' ' if parts else '')+term))
    return 'aₙ = '+' '.join(parts).replace('+ ','+ ').replace('  ',' ')
SUPK={1:'',2:'²',3:'³',4:'⁴'}
def charpoly(cs):
    k=len(cs); out='r'+SUPK.get(k,'^'+str(k))
    for i,c in enumerate(cs):
        if c==0: continue
        pw=k-1-i; term=(str(abs(c)) if (abs(c)!=1 or pw==0) else '')+('r'+SUPK.get(pw,'^'+str(pw)) if pw>0 else '')
        out+=(' − ' if c>0 else ' + ')+term
    return out
def seq_rec(cs,a0,N):
    a=list(a0)
    for n in range(len(cs),N+1): a.append(sum(c*a[n-1-i] for i,c in enumerate(cs)))
    return a
from recstore import RECS, add
def handle_part(iid,lab,text,chap):
    t=clean(text); ref=f'{SRC} – {iid}{lab}'
    q=t
    m=re.search(r'Phương trình:?\s*(x\d(?:\s*\+\s*x\d)+)\s*=\s*(\d+).*?(?:thỏa mãn|sao cho)\s*:?\s*(.*)$',t)
    if m and 'nghiệm nguyên' in t:
        k=len(re.findall(r'x\d',m.group(1))); N=int(m.group(2)); lo,hi=parse_constraints(m.group(3).replace('?',''),k)
        ans,sol=L.int_sol(N,lo,hi)
        ct=cons_text(lo,hi) or f'xᵢ ≥ 2 (mọi i)'
        wr=[w for w in L.wrong_for_int_sol(N,lo,hi) if w!=ans]
        add(mod='m05',src=ref,q=f'Phương trình {" + ".join("x"+sub(i+1) for i in range(k))} = {N} có bao nhiêu nghiệm nguyên không âm thỏa mãn: {ct}?',ans=str(ans),wrong=wr,sol=sol,level=3 if any(h is not None for h in hi) else 2,topic='Nghiệm nguyên có cận'); return True
    m=re.search(r'biển số xe bắt đầu bằng (\d) hoặc (\d) chữ cái in hoa.*?kết thúc là (\d) hoặc (\d) chữ số',t)
    if m:
        a,b,c,d=map(int,m.groups()); ans=(26**a+26**b)*(10**c+10**d)
        add(mod='m04',src=ref,q=q.replace('?','?'),ans=str(ans),wrong=[26**a*10**c+26**b*10**d,(26**a+26**b)*10**c,26**(a+b)*10**(c+d),(26**a+26**b+10**c+10**d)],sol=f'Chia trường hợp theo số chữ cái ({a} hoặc {b}) và số chữ số ({c} hoặc {d}); chữ cái và chữ số được lặp.\nSố cách chọn phần chữ cái: 26^{a} + 26^{b} = {26**a+26**b}; phần chữ số: 10^{c} + 10^{d} = {10**c+10**d}.\nQuy tắc nhân: ({26**a}+{26**b})·({10**c}+{10**d}) = {ans}.',level=2,topic='Quy tắc nhân'); return True
    m=re.search(r'từ (\d+) đến (\d+) chia hết cho (\d+) hoặc (\d+)\s*\?',t)
    if m:
        a,b,d1,d2=map(int,m.groups()); tot,s=L.incl_text(a,b,[d1,d2])
        add(mod='m04',src=ref,q=q,ans=str(tot),wrong=[b//d1-(a-1)//d1+b//d2-(a-1)//d2]+near_ints(tot,__import__('random').Random(iid+lab),4,lo=0),sol=s,level=2,topic='Nguyên lý bù trừ'); return True
    m=re.search(r'từ (\d+) đến (\d+) thỏa mãn điều kiện chia hết cho ít nhất một trong ba số (\d+), (\d+),? và (\d+)',t)
    if m:
        a,b,*ds=map(int,m.groups()); tot,s=L.incl_text(a,b,ds)
        add(mod='m04',src=ref,q=q,ans=str(tot),wrong=[sum(b//d-(a-1)//d for d in ds)]+near_ints(tot,__import__('random').Random(iid+lab),4,lo=0),sol=s,level=2,topic='Nguyên lý bù trừ'); return True
    m=re.search(r'(?:từ|trong khoảng từ) (\d+) đến (\d+) (?:thỏa mãn )?(?:điều kiện )?không chia hết cho (?:bất kỳ số nào|số nào) trong (?:ba|hai) số (\d+),? (?:và )?(\d+)(?:,? và (\d+))?',t)
    if m:
        a,b=int(m.group(1)),int(m.group(2)); ds=[int(x) for x in m.groups()[2:] if x]; tot,s=L.incl_text(a,b,ds,neg=True)
        neg=b-a+1-tot
        add(mod='m04',src=ref,q=q,ans=str(neg),wrong=[tot]+near_ints(neg,__import__('random').Random(iid+lab),4,lo=0),sol=s,level=3,topic='Nguyên lý bù trừ'); return True
    m=re.search(r'(\d+) bạn nam và (\d+) bạn nữ.*?số bạn nam (bằng|đúng bằng 2 lần) số bạn nữ.*?ít nhất (\d+) thành viên và nhiều nhất (\d+) thành viên',t)
    if m:
        n,w=int(m.group(1)),int(m.group(2)); ratio=2 if '2 lần' in m.group(3) else 1; lo_,hi_=int(m.group(4)),int(m.group(5))
        terms=[];tot=0
        for j in range(0,w+1):
            i=ratio*j
            if i<=n and lo_<=i+j<=hi_ and j>=0:
                c=math.comb(n,i)*math.comb(w,j); tot+=c; terms.append(f'  {j} nữ + {i} nam: C({w},{j})·C({n},{i}) = {c}')
        add(mod='m04',src=ref,q=q,ans=str(tot),wrong=[math.comb(n+w,lo_),tot+math.comb(n,ratio)*w,sum(math.comb(n,i)*math.comb(w,i) for i in range(1,5)) if ratio==1 else tot-1]+near_ints(tot,__import__('random').Random(iid+lab),3,lo=1),sol=f'Gọi số nữ là j thì số nam là {"" if ratio==1 else "2·"}j; tổng thành viên = {ratio+1 if ratio>1 else 2}·j phải nằm trong [{lo_}, {hi_}].\nCác trường hợp hợp lệ:\n'+'\n'.join(terms)+f'\nCộng lại (quy tắc cộng): {tot}.',level=3,topic='Chỉnh hợp, tổ hợp'); return True
    m=re.search(r'mã quốc gia dài từ 1 đến 3 chữ số.*?dạng ((?:N|X)+)-\s*((?:N|X)+)-\s*XXXX.*?N có thể nhận giá trị từ (\d) đến (\d)',t)
    if m:
        f1,f2,lo_,hi_=m.group(1),m.group(2),int(m.group(3)),int(m.group(4)); nn=hi_-lo_+1
        p1=(nn**f1.count('N'))*10**f1.count('X'); p2=(nn**f2.count('N'))*10**f2.count('X'); ans=(10+100+1000)*p1*p2*10**4
        add(mod='m04',src=ref,q=q,ans=f'{ans:,}'.replace(',','.'),wrong=[f'{x:,}'.replace(',','.') for x in (1000*p1*p2*10**4,(10+100+1000)*p1*p2*10**3,(10+100+1000)*nn*nn*10**5,ans*10)],sol=f'Mã quốc gia: 10 + 10² + 10³ = 1110 cách (chia trường hợp theo độ dài). Nhóm {f1}: {nn}^{f1.count("N")}·10^{f1.count("X")} = {p1}; nhóm {f2}: {p2}; nhóm XXXX: 10⁴. Quy tắc nhân: 1110·{p1}·{p2}·10⁴ = {ans:,}.'.replace(',','.'),level=3,topic='Quy tắc nhân'); return True
    m=re.search(r'xâu độ dài (\d+) trong đó có (\d) chữ cái.*?và (\d) chữ số',t)
    if m:
        Ln,a,d=map(int,m.groups()); ans=math.comb(Ln,a)*26**a*10**d
        add(mod='m04',src=ref,q=q,ans=str(ans),wrong=[26**a*10**d,math.perm(Ln,a)*26**a*10**d,math.comb(Ln,a)*(26**a+10**d),ans+26],sol=f'Chọn {a} vị trí cho chữ cái: C({Ln},{a}) = {math.comb(Ln,a)}; xếp chữ cái: 26^{a} = {26**a}; xếp chữ số: 10^{d} = {10**d}. Tổng: {math.comb(Ln,a)}·{26**a}·{10**d} = {ans}.',level=2,topic='Quy tắc nhân'); return True
    m=re.search(r'số nguyên dương có (\d) chữ số là số thuận nghịch.*?tổng các chữ số bằng (\d+)',t)
    if m:
        Ln,N=int(m.group(1)),int(m.group(2)); ans=L.pal_count(Ln,N); h=(Ln+1)//2
        add(mod='m05',src=ref,q=q,ans=str(ans),wrong=near_ints(ans,__import__('random').Random(1),5,lo=1),sol=f'Số thuận nghịch {Ln} chữ số xác định bởi {h} chữ số đầu x₁…x_{h} (x₁ ≥ 1); tổng chữ số = '+(f'2(x₁+…+x_{h-1}) + x_{h}' if Ln%2 else f'2(x₁+…+x_{h})')+f' = {N}. Đếm số nghiệm 0 ≤ xᵢ ≤ 9 (x₁ ≥ 1): {ans} (đã kiểm chứng bằng liệt kê).',level=3,topic='Số thuận nghịch'); return True
    # ---- tổng chữ số / thuận nghịch (kiểu 2.2.x)
    m=re.search(r'số tự nhiên (?:số )?có (\d+) chữ số (?:thỏa mãn )?có tổng các chữ số (?:bằng|là) (\d+)',t)
    if m:
        Ln,N=int(m.group(1)),int(m.group(2)); ans=L.dp_bounded(N,[1]+[0]*(Ln-1),[9]*Ln)
        add(mod='m05',src=ref,q=q,ans=str(ans),wrong=near_ints(ans,__import__('random').Random(Ln*100+N),5,lo=1)+[math.comb(N+Ln-1,Ln-1)],sol=f'Đặt x₁ ≥ 1 (chữ số đầu), x₂…x_{Ln} ≥ 0, mọi xᵢ ≤ 9 và x₁+…+x_{Ln} = {N}. Đặt x₁ = y₁ + 1: tổng còn {N-1}; dùng bù trừ cho điều kiện xᵢ ≤ 9 (vượt cận khi yᵢ ≥ 10).\nKết quả: {ans} (đã kiểm chứng bằng quy hoạch động).',level=3,topic='Số nghiệm có cận'); return True
    m=re.search(r'số tự nhiên có (\d+) chữ số (?:thỏa mã[n]? )?tạo thành một số thuận nghịch( và có tất cả các chữ số đều khác 0)?',t)
    if m:
        Ln=int(m.group(1)); h=(Ln+1)//2; nz=bool(m.group(2)); ans=9**h if nz else 9*10**(h-1)
        chk=sum(1 for d in itertools.product(range(1,10) if nz else range(10),repeat=h) if d[0]!=0) if h<=5 else ans
        assert chk==ans
        add(mod='m05',src=ref,q=q,ans=str(ans),wrong=[10**h,9*10**h,9**h if not nz else 9*10**(h-1),ans+9**(h-1)],sol=f'Số thuận nghịch {Ln} chữ số được xác định hoàn toàn bởi {h} chữ số đầu (các chữ số sau lặp lại đối xứng). '+('Mỗi chữ số thuộc {1,…,9}: 9^%d = %d.'%(h,ans) if nz else 'Chữ số đầu ≠ 0: 9 cách; %d chữ số tiếp theo tùy ý: 10 cách mỗi chữ số. Tổng 9·10^%d = %d.'%(h-1,h-1,ans)),level=2,topic='Số thuận nghịch'); return True
    m=re.search(r'an = an-1 \+ (\d*)n(?: \+ (\d+))? với a0 ?= ?(\d+)',t)
    if m:
        al=int(m.group(1) or 1); be=int(m.group(2) or 0); a0=int(m.group(3))
        f=lambda n:a0+al*n*(n+1)//2+be*n
        seq=[a0]
        for n in range(1,8): seq.append(seq[-1]+al*n+be)
        assert all(seq[n]==f(n) for n in range(8))
        poly=f'{a0} + {al}·n(n+1)/2'+(f' + {be}n' if be else '')
        add(mod='m07',src=ref,q=q,ans=f'aₙ = {poly}',wrong=[f'aₙ = {a0} + {al}·n²'+(f' + {be}n' if be else ''),f'aₙ = {a0}·{al}ⁿ'+(f' + {be}n' if be else ''),f'aₙ = {a0} + {al}·n(n−1)/2'+(f' + {be}n' if be else ''),f'aₙ = {a0} + {al}·n(n+1)'+(f' + {be}n' if be else '')],sol=f'Dùng phương pháp lặp: aₙ = aₙ₋₁ + {al}n{"+"+str(be) if be else ""} ⇒ aₙ = a₀ + Σ_(i=1..n) ({al}i{"+"+str(be) if be else ""}) = {a0} + {al}·n(n+1)/2'+(f' + {be}n' if be else '')+'.\nKiểm tra: '+', '.join(f'a{sub(i)} = {seq[i]}' for i in range(5))+'.',level=2,topic='Giải bậc 1'); return True
    m=re.search(r'xâu nhị phân độ dài n (?:và )?(không có|có ít nhất một dãy) k số (\d)( liên tiếp)',t)
    if m:
        neg=m.group(1)=='không có'; dg=int(m.group(2))
        def bf(k,n): return sum(1 for s_ in itertools.product((0,1),repeat=n) if L.has_run(s_,dg,k)!=neg)
        for k in (2,3,4):
            av={n:bf(k,n) for n in range(1,12)}
            if neg: assert all(av[n]==sum(av[n-i] for i in range(1,k+1)) for n in range(k+1,12)) and all(av[j]==2**j for j in range(1,k)) and av[k]==2**k-1
            else: assert all(av[n]==sum(av[n-i] for i in range(1,k+1))+2**(n-k) for n in range(k+1,12)) and av[k]==1 and all(av[j]==0 for j in range(1,k))
        if neg: ans='aₙ = aₙ₋₁ + aₙ₋₂ + … + aₙ₋ₖ (n > k); aⱼ = 2ʲ (j < k), aₖ = 2ᵏ − 1'; wr=['aₙ = 2aₙ₋₁ − aₙ₋ₖ₋₁; aⱼ = 2ʲ','aₙ = aₙ₋₁ + aₙ₋₂ + … + aₙ₋ₖ + 2ⁿ⁻ᵏ; aⱼ = 0 (j < k), aₖ = 1','aₙ = 2aₙ₋₁; a₁ = 2','aₙ = aₙ₋₁ + aₙ₋ₖ; aⱼ = 2ʲ']; sol=f'Xâu không có k bit {dg} liên tiếp: xét số bit {dg} ở cuối. Nếu bit cuối là {1-dg}: còn aₙ₋₁ xâu hợp lệ. Nếu kết thúc bằng đúng i bit {dg} (i = 1..k−1) đứng sau một bit {1-dg}: còn aₙ₋ᵢ₋₁ xâu. Gộp lại: aₙ = aₙ₋₁ + aₙ₋₂ + … + aₙ₋ₖ.\nĐiều kiện đầu: với j < k mọi xâu độ dài j đều hợp lệ nên aⱼ = 2ʲ; a_k = 2ᵏ − 1 (trừ xâu toàn bit {dg}).\n(Đã kiểm tra bằng liệt kê với k = 2, 3, 4 và n ≤ 11.)'
        else: ans='bₙ = bₙ₋₁ + bₙ₋₂ + … + bₙ₋ₖ + 2ⁿ⁻ᵏ (n > k); bⱼ = 0 (j < k), bₖ = 1'; wr=['bₙ = 2bₙ₋₁ + 2ⁿ⁻ᵏ; bₖ = 1','bₙ = bₙ₋₁ + bₙ₋₂ + … + bₙ₋ₖ; bⱼ = 0 (j < k), bₖ = 1','bₙ = bₙ₋₁ + bₙ₋ₖ + 2ⁿ⁻ᵏ; bₖ = 1','bₙ = 2ⁿ − bₙ₋₁; bₖ = 1']; sol=f'Số xâu có ít nhất một dãy k bit {dg} liên tiếp bₙ = 2ⁿ − aₙ với aₙ là số xâu KHÔNG có dãy đó (aₙ = aₙ₋₁+…+aₙ₋ₖ). Suy ra bₙ = 2ⁿ − Σ aₙ₋ᵢ = Σ bₙ₋ᵢ + (2ⁿ − Σ 2ⁿ⁻ᵢ) = Σ bₙ₋ᵢ + 2ⁿ⁻ᵏ.\nĐiều kiện đầu: bⱼ = 0 với j < k; bₖ = 1 (chỉ xâu toàn bit {dg}).\n(Đã kiểm tra bằng liệt kê với k = 2, 3, 4.)'
        add(mod='m07',src=ref,q=q,ans=ans,wrong=wr,sol=sol,level=3,topic='Lập hệ thức truy hồi'); return True
    m=re.search(r'Gọi an là số xâu nhị phân độ dài n (có chứa chẵn chữ số 0|không chứa ba số 1 liên tiếp).*?tính a(\d)',t)
    if m:
        nq=int(m.group(2))
        if 'chẵn' in m.group(1):
            v=2**(nq-1); assert v==sum(1 for s_ in itertools.product((0,1),repeat=nq) if s_.count(0)%2==0)
            add(mod='m07',src=ref,q=q,ans=f'aₙ = 2aₙ₋₁, a₁ = 1; a{sub(nq)} = {v}',wrong=[f'aₙ = 2aₙ₋₁ + 1, a₁ = 1; a{sub(nq)} = {2**nq-1}',f'aₙ = aₙ₋₁ + aₙ₋₂, a₁ = 1; a{sub(nq)} = {[1,1,2,3,5,8,13,21][nq-1]}',f'aₙ = 2aₙ₋₁, a₁ = 2; a{sub(nq)} = {2**nq}'],sol=f'Với n ≥ 2: mỗi xâu độ dài n−1 có đúng một cách thêm bit cuối (0 hoặc 1) để số bit 0 thành chẵn. Vậy aₙ = 2^(n−1) = 2aₙ₋₁ (a₁ = 1: chỉ xâu "1"). a{sub(nq)} = 2^{nq-1} = {v}.',level=2,topic='Lập hệ thức truy hồi'); return True
        v=sum(1 for s_ in itertools.product((0,1),repeat=nq) if not L.has_run(s_,1,3))
        add(mod='m07',src=ref,q=q,ans=f'aₙ = aₙ₋₁ + aₙ₋₂ + aₙ₋₃, a₁ = 2, a₂ = 4, a₃ = 7; a{sub(nq)} = {v}',wrong=[f'aₙ = aₙ₋₁ + aₙ₋₂, a₁ = 2, a₂ = 3; a{sub(nq)} = {[2,3,5,8,13,21,34][nq-1]}',f'aₙ = 2aₙ₋₁ − aₙ₋₄, a₁ = 2, a₂ = 4, a₃ = 8; a{sub(nq)} = {v+3}',f'aₙ = aₙ₋₁ + aₙ₋₂ + aₙ₋₃ + 2ⁿ⁻³, a₃ = 1; a{sub(nq)} = {2**nq-v}'],sol=f'Xét các bit cuối: xâu hợp lệ kết thúc bằng 0 (còn aₙ₋₁), bằng 10 (còn aₙ₋₂), bằng 110 (còn aₙ₋₃). Vậy aₙ = aₙ₋₁ + aₙ₋₂ + aₙ₋₃ với a₁ = 2, a₂ = 4, a₃ = 7 (bỏ 111). Tính: a₄ = 13, a₅ = 24, a₆ = 44, a₇ = 81. a{sub(nq)} = {v}.',level=3,topic='Lập hệ thức truy hồi'); return True
    m=re.search(r'xâu thập phân độ dài (?:n|𝑛) và có chứa (\d) số (\d) liên tiếp|xâu thập phân độ dài n chứa (\d) số (\d) liên tiếp',t)
    if m:
        g=[x for x in m.groups() if x]; k,dg=int(g[0]),int(g[1])
        def avoid(n):
            st=[1]+[0]*(k-1)
            for _ in range(n):
                ns=[0]*k
                for r_,c in enumerate(st):
                    if c:
                        ns[0]+=c*9
                        if r_+1<k: ns[r_+1]+=c
                st=ns
            return sum(st)
        av={n:10**n-avoid(n) for n in range(1,10)}
        rec=L.find_recurrence(av,10,maxk=4)
        if rec is None: return False
        mm=re.search(r'với n = (\d+)',t); nq=int(mm.group(1)) if mm else None
        txt=L.rec_text(rec,10); ini=', '.join(f'a{sub(i)} = {av[i]}' for i in range(1,rec['k']+1))
        ans=f'{txt}; {ini}'
        wrong=[]
        for dc in range(len(rec['c'])):
            for dv in (1,-1):
                r2=dict(rec); r2['c']=rec['c'][:]; r2['c'][dc]+=dv; wrong.append(L.rec_text(r2,10)+f'; {ini}')
        r2=dict(rec); r2['e']=rec['e']+1; wrong.append(L.rec_text(r2,10)+f'; {ini}')
        add(mod='m07',src=ref,q=q,ans=ans,wrong=wrong[:6],sol=f'Gọi aₙ là số xâu thập phân độ dài n chứa {k} chữ số {dg} liên tiếp và bₙ là số xâu KHÔNG chứa (bₙ = 10ⁿ − aₙ). Xâu không chứa kết thúc bằng: một chữ số khác {dg} (9·bₙ₋₁), hoặc {dg} sau chữ số khác {dg} (9·bₙ₋₂), … (đến {k-1} chữ số {dg}): bₙ = 9(bₙ₋₁ + … + bₙ₋ₖ). Suy ra {txt}.\nĐiều kiện đầu {ini} (đếm trực tiếp/quy hoạch động; kiểm tra khớp với n ≤ 9).',level=3,topic='Lập hệ thức truy hồi'); return True
    # ---- điện thoại (biến thể khoảng trắng)
    m=re.search(r'mã quốc gia dài từ 1 đến 3 chữ số.*?dạng ((?:N|X)+)-\s*((?:N|X)+)-\s*XXXX.*?N có thể nhận giá trị từ (\d) đến (\d)',t)
    if m:
        f1,f2,lo_,hi_=m.group(1),m.group(2),int(m.group(3)),int(m.group(4)); nn=hi_-lo_+1
        p1=(nn**f1.count('N'))*10**f1.count('X'); p2=(nn**f2.count('N'))*10**f2.count('X'); ans=(10+100+1000)*p1*p2*10**4
        fmtn=lambda x:f'{x:,}'.replace(',','.')
        add(mod='m04',src=ref,q=q,ans=fmtn(ans),wrong=[fmtn(x) for x in (1000*p1*p2*10**4,(10+100+1000)*p1*p2*10**3,(10+100+1000)*nn*nn*10**5,ans*10)],sol=f'Mã quốc gia dài 1, 2 hoặc 3 chữ số: 10 + 10² + 10³ = 1110 cách. Nhóm {f1}: {nn}^{f1.count("N")}·10^{f1.count("X")} = {p1}; nhóm {f2}: {p2}; nhóm XXXX: 10⁴. Quy tắc nhân: 1110·{p1}·{p2}·10⁴ = {fmtn(ans)}.',level=3,topic='Quy tắc nhân'); return True
    m=re.search(r'(?i)biển số xe được đặt theo quy tắc.*?bắt đầu bằng (\d) hoặc (\d) chữ cái in hoa.*?kết thúc là (\d) hoặc (\d) chữ số',t)
    if m:
        a,b,c,d=map(int,m.groups()); ans=(26**a+26**b)*(10**c+10**d)
        add(mod='m04',src=ref,q=q,ans=str(ans),wrong=[26**a*10**c+26**b*10**d,(26**a+26**b)*10**c,26**(a+b)*10**(c+d),(26**a+26**b+10**c+10**d)],sol=f'Số cách chọn phần chữ cái: 26^{a} + 26^{b} = {26**a+26**b}; phần chữ số: 10^{c} + 10^{d} = {10**c+10**d}. Quy tắc nhân: {ans}.',level=2,topic='Quy tắc nhân'); return True
    if 'Giả sử N, a, b, c là các số nguyên' in t:
        add(mod='m04',src=ref,q=q,ans=None,wrong=[],sol='Đặt A_x = tập các số trong [1,N] chia hết cho x. Số cần tìm = N − |A_a ∪ A_b ∪ A_c|. Nguyên lý bù trừ:\nN − ⌊N/a⌋ − ⌊N/b⌋ − ⌊N/c⌋ + ⌊N/[a,b]⌋ + ⌊N/[a,c]⌋ + ⌊N/[b,c]⌋ − ⌊N/[a,b,c]⌋, trong đó [·] là bội chung nhỏ nhất.',level=3,topic='Nguyên lý bù trừ'); return True
    if 'Có thể nối được hay không 25 máy tính' in t:
        add(mod='m06',src=ref,q=q,ans='Không thể',wrong=['Có thể, vì 25 máy là số lẻ','Có thể nếu mỗi máy nối đến máy khác nhau','Không xác định được nếu chưa biết cách nối'],sol='Coi mỗi máy là một đỉnh, mỗi đường nối là một cạnh: tổng bậc = 10·5 + 15·9 = 50 + 135 = 185 là số LẺ. Nhưng tổng bậc luôn bằng 2·(số cạnh) là số chẵn ⇒ mâu thuẫn. Vậy không thể nối được.',level=3,topic='Chứng minh tồn tại'); return True
    # ---- sách và xếp hàng
    m=re.search(r'Một bộ (\d+) cuốn sách gồm (\d+) cuốn thuộc chủ đề Toán học, (\d+) cuốn thuộc chủ đề Vật lý, (\d+) cuốn thuộc chủ đề Hóa học.*?(nằm hoàn toàn về bên trái|cùng chủ đề nằm cạnh nhau)',t)
    if m:
        n,a,b,c=map(int,m.groups()[:4]); F=math.factorial
        if 'trái' in m.group(5): ans=F(a)*F(n-a); sol=f'Các sách Toán chiếm {a} vị trí đầu: {a}! cách xếp; {n-a} cuốn còn lại xếp tự do vào {n-a} vị trí sau: {n-a}!. Tổng: {a}!·{n-a}! = {ans}.'; wr=[F(n),F(a)*F(n-a)*2,F(n-a),F(a)*F(b)*F(c)]
        else: ans=F(3)*F(a)*F(b)*F(c); sol=f'Xem mỗi chủ đề là một khối: 3! cách sắp thứ tự ba khối; trong khối Toán {a}!, Vật lý {b}!, Hóa {c}! cách. Tổng: 3!·{a}!·{b}!·{c}! = {ans}.'; wr=[F(a)*F(b)*F(c),F(n),F(a+b+c)//F(3),F(3)*(F(a)+F(b)+F(c))]
        add(mod='m05',src=ref,q=q,ans=str(ans),wrong=wr,sol=sol,level=3,topic='Hoán vị'); return True
    m=re.search(r'Giả sử có (\d+) cuốn sách gồm (\d+) cuốn sách thuộc chủ đề toán học, (\d+) cuốn sách thuộc chủ đề hóa học, và (\d+) cuốn sách thuộc chủ đề vật lý',t)
    if m:
        n,a,b,c=map(int,m.groups()); F=math.factorial
        if 'không nằm cạnh' in t:
            ans=2*F(a)*F(b)*F(c); sol=f'Xem mỗi chủ đề là một khối. Khối Toán không được kề khối Vật lý nên khối Hóa phải ở giữa: hai thứ tự (Toán–Hóa–Lý, Lý–Hóa–Toán) = 2. Trong khối: {a}!·{b}!·{c}!. Tổng: 2·{a}!·{b}!·{c}! = {ans}.'; wr=[F(3)*F(a)*F(b)*F(c),F(a)*F(b)*F(c),ans//2,2*F(n)]
        else:
            ans=F(3)*F(a)*F(b)*F(c); sol=f'3! cách sắp thứ tự ba khối chủ đề, nhân với {a}!·{b}!·{c}! cách xếp trong từng khối: {ans}.'; wr=[F(a)*F(b)*F(c),F(n),F(3)*(F(a)+F(b)+F(c)),F(a+b+c)//F(3)]
        add(mod='m05',src=ref,q=q,ans=str(ans),wrong=wr,sol=sol,level=3,topic='Hoán vị'); return True
    if 'Có bao nhiêu cách xếp 6 người A, B, C, D, E, F' in t:
        if 'C đứng cạnh D; và E đứng cạnh F' in t: ans=48; sol='Xem mỗi cặp (A,B), (C,D), (E,F) là một khối: 3! cách sắp ba khối, mỗi khối có 2 cách đổi chỗ 2 người: 3!·2³ = 48.'; wr=[720,96,144,24]
        else: ans=96; sol='Gộp (A,B) và (C,D) thành hai khối, cùng E, F: 4 đối tượng được sắp 4! = 24 cách; mỗi khối có 2 cách đổi chỗ: 24·2·2 = 96.'; wr=[48,24,144,192]
        assert ans==sum(1 for p in itertools.permutations('ABCDEF') if abs(p.index('A')-p.index('B'))==1 and abs(p.index('C')-p.index('D'))==1 and (('C đứng cạnh D; và E' not in t) or abs(p.index('E')-p.index('F'))==1))
        add(mod='m05',src=ref,q=q,ans=str(ans),wrong=wr,sol=sol,level=3,topic='Hoán vị'); return True
    # ---- giải truy hồi
    if re.search(r'nghiệm của công thức truy hồi',t):
        t=t.replace('−','-')
        m=re.search(r'(?<![a-z\d])an\s*=\s*(.+?)(?:\s*,\s*| với| a\d ?=|$)',t)
        expr=m.group(1) if m else ''
        expr2=expr.replace('−','-')
        terms=re.findall(r'([+-]?)\s*(\d*)\s*an\s*-\s*(\d)',expr2)
        cs=[0]*max([int(x[2]) for x in terms] or [1])
        for sg,co,ord_ in terms: cs[int(ord_)-1]+=(-1 if sg=='-' else 1)*(int(co) if co else 1)
        ini={int(a):int(b) for a,b in re.findall(r'a(\d)\s*=\s*(-?\d+)',t)}
        a0=[ini.get(i) for i in range(len(cs))]
        if not cs: return False
        if None in a0:
            sol0=rec_solve(cs,[1]+[0]*(len(cs)-1)) if False else None
            rec=' '.join(str(c) for c in cs)
            add(mod='m08',src=ref,q=q,ans=None,wrong=[],sol=f'Phương trình đặc trưng r² − ({cs[0]})r − ({cs[1]}) = 0 ⇒ (r − 7)² = 0 nên có nghiệm kép r = 7. Nghiệm tổng quát: aₙ = (α + βn)·7ⁿ, với α, β xác định từ hai điều kiện đầu (đề gốc không cho điều kiện đầu).',level=2,topic='Giải bậc 2') if cs==[14,-49] else None
            return cs==[14,-49]
        sol=rec_solve(cs,a0)
        if not sol: return False
        seqv=seq_rec(cs,a0,8); ans=fmt_sol(sol)
        # kiểm chứng
        from fractions import Fraction as Fr
        for n in range(8):
            v=sum(c*(Fr(r)**n)*((Fr(n)**j) if (j>0 and n>0) else (1 if j==0 else 0)) for c,(r,j) in zip(sol['coefs'],sol['basis']))
            assert v==seqv[n],(iid,lab,n,v,seqv[n])
        rec='aₙ = '+' '.join((('−' if c<0 else ('+' if k>0 else '')))+(' ' if k>0 else '')+(str(abs(c)) if abs(c)!=1 else '')+f'aₙ₋{sub(k+1)}' for k,c in enumerate(cs) if c!=0)
        rec=rec.replace('=  ','= ')
        rts=', '.join(f'r = {r}'+(f' (bội {m_})' if m_>1 else '') for r,m_ in sorted(sol['mult'].items()))
        wrong=set()
        import random as _r
        rr=_r.Random(hash(iid+lab)&0xffff)
        for _ in range(30):
            d=[(_r.Random(rr.random()).choice([-1,1]))*1 for _ in sol['coefs']]
            alt=dict(sol); alt['coefs']=[c+x*rr.choice([0,1,1,2]) for c,x in zip(sol['coefs'],d)]
            if alt['coefs']!=sol['coefs']:
                txt=fmt_sol(alt)
                if txt!=ans: wrong.add(txt)
            if len(wrong)>=6: break
        add(mod='m08',src=ref,q=f'Hãy tìm nghiệm của công thức truy hồi {rec} với '+', '.join(f'a{sub(i)} = {a0[i]}' for i in range(len(cs)))+'.',ans=ans,wrong=list(wrong),sol=f'Phương trình đặc trưng của {rec}: {charpoly(cs)} = 0 có nghiệm {rts}.\nNghiệm tổng quát tương ứng; thay điều kiện đầu ta giải hệ được {ans}.\nKiểm tra: '+', '.join(f'a{sub(i)} = {seqv[i]}' for i in range(6))+' khớp với công thức.',level=3 if len(cs)>=3 else 2,topic='Giải bậc 2' if len(cs)==2 else ('Giải bậc 3' if len(cs)==3 else 'Giải bậc 1')); return True
    # ---- lập truy hồi cho xâu
    m=re.search(r'chứa một số (lẻ|chẵn) chữ số (\d)',t)
    if m and 'từ mã' in t:
        par,dg=m.group(1),m.group(2)
        odd=(par=='lẻ')
        # a_n = 8a_{n-1} + 10^{n-1}
        seq={n:((10**n-8**n)//2 if odd else (10**n+8**n)//2) for n in range(1,9)}
        a1=1 if odd else 9
        assert all(seq[n]==8*seq[n-1]+10**(n-1) for n in range(2,9)) and seq[1]==a1
        add(mod='m07',src=ref,q=q,ans=f'aₙ = 8aₙ₋₁ + 10ⁿ⁻¹, a₁ = {a1}',wrong=[f'aₙ = 9aₙ₋₁ + 10ⁿ⁻¹, a₁ = {a1}',f'aₙ = 8aₙ₋₁ + 10ⁿ, a₁ = {a1}',f'aₙ = 10aₙ₋₁ − 8ⁿ⁻¹, a₁ = {a1}',f'aₙ = 8aₙ₋₁ + 10ⁿ⁻¹, a₁ = {a1+1}'],sol=f'Gọi aₙ là số xâu có số {par} chữ số {dg}, bₙ là số xâu có số {"chẵn" if odd else "lẻ"} chữ số {dg}; aₙ + bₙ = 10ⁿ. Thêm một ký tự vào cuối xâu độ dài n−1: nếu là chữ số {dg} (1 cách) thì đổi tính chẵn lẻ, nếu khác (9 cách) thì giữ nguyên.\nDo đó aₙ = 9aₙ₋₁ + bₙ₋₁ = 9aₙ₋₁ + (10ⁿ⁻¹ − aₙ₋₁) = 8aₙ₋₁ + 10ⁿ⁻¹.\nĐiều kiện đầu a₁ = {a1} ({"chỉ xâu (%s)"%dg if odd else "9 xâu khác chữ số %s"%dg}). Dãy: '+', '.join(str(seq[n]) for n in range(1,6))+'.',level=3,topic='Lập hệ thức truy hồi'); return True
    m=re.search(r'xâu (nhị phân|thập phân) độ dài n,?\s*(?:(bắt đầu|kết thúc) bằng số (\d)\s*(?:và )?)?(?:có )?chứa (\d) số (\d) liên tiếp',t)
    if m:
        alpha={'nhị phân':2,'thập phân':10}[m.group(1)]; se,sd,k,dg=m.group(2),m.group(3),int(m.group(4)),int(m.group(5))
        mm=re.search(r'với n = (\d+)',t); nq=int(mm.group(1)) if mm else None
        maxn=13 if alpha==2 else 8
        def pred(s):
            if se=='bắt đầu' and s[0]!=int(sd): return False
            if se=='kết thúc' and s[-1]!=int(sd): return False
            return L.has_run(s,dg,k)
        seq={n:L.count_strings(alpha,pred,n) for n in range(1,maxn+1)}
        rec=L.find_recurrence(seq,alpha,maxk=4)
        if rec is None: return False
        txt=L.rec_text(rec,alpha)
        first=[n for n in range(1,maxn+1) if seq[n]>0][0]
        ini=f'a{sub(first)} = {seq[first]}' if rec['k']==1 else ', '.join(f'a{sub(i)} = {seq[i]}' for i in range(1,rec['k']+1))
        val=seq[nq] if nq and nq<=maxn else None
        ext=f'; a{sub(nq)} = {val}' if val is not None else ''
        ans=f'{txt}; {ini}{ext}'
        # phương án nhiễu: đổi hệ số và kiểm tra sai
        wrong=[]
        def ok(cs,e,m_):
            for n in range(rec['k']+1,maxn+1):
                v=sum(c*seq[n-i] for i,c in enumerate(cs,1) if n-i>=1)+(e*alpha**(n-m_) if m_ is not None else 0)
                if v!=seq[n]: return False
            return True
        import copy
        for dc in range(len(rec['c'])):
            for dv in (1,-1,2):
                c2=rec['c'][:]; c2[dc]+=dv; r2=dict(rec); r2['c']=c2
                if not ok(c2,rec['e'],rec['m']): wrong.append(L.rec_text(r2,alpha)+f'; {ini}{ext}')
        if rec['m'] is not None:
            for dm in (1,-1):
                r2=dict(rec); r2['e']=rec['e']+dm
                if not ok(rec['c'],r2['e'],rec['m']): wrong.append(L.rec_text(r2,alpha)+f'; {ini}{ext}')
        add(mod='m07',src=ref,q=q,ans=ans,wrong=wrong[:6],sol=f'Đếm trực tiếp các xâu độ dài nhỏ: '+', '.join(f'a{sub(i)} = {seq[i]}' for i in range(1,8))+f'.\nHệ thức truy hồi tìm được (và đã kiểm tra khớp với đếm trực tiếp tới n = {maxn}): {txt}, điều kiện đầu {ini}.'+(f'\nTính a{sub(nq)} = {val}.' if val is not None else '')+'\nCách suy luận: phân loại xâu theo phần cuối (các bit cuối tạo dãy liên tiếp bị cắt) — số xâu chưa có dãy cần tìm thỏa aₙ = aₙ₋₁+…, phần còn lại của 2ⁿ (hoặc 10ⁿ) cộng thêm số xâu đã chứa dãy ở n−k vị trí đầu.',level=3,topic='Lập hệ thức truy hồi'); return True
    import orig_nh2 as X2
    if X2.ch1(iid,lab.strip('()'),ref,t) : return True
    if X2.ch1_sets(iid,lab.strip('()'),ref,t): return True
    if chap==3 and X2.ch3(iid,lab,ref,t): return True
    if chap==4 and X2.ch4(iid,lab,ref,t): return True
    if chap==5 and X2.ch5(iid,lab,ref,t): return True
    return False
def run():
    its=load(); done=0; tot=0; un=[]
    for it in its:
        ps=split_parts(it['text'])
        for lab,tx in ps:
            if not lab and len(ps)>1: continue
            tot+=1
            try:
                if handle_part(it['id'],(')'if False else ('.'+lab if False else (lab and '('+lab+')') )),tx,it['chap']): done+=1
                else: un.append((it['id'],lab,clean(tx)[:70]))
            except Exception as ex:
                un.append((it['id'],lab,'ERR '+repr(ex)[:50]))
    return done,tot,un
if __name__=='__main__':
    d,t,un=run(); print(d,t,len(RECS))
    for u in un[:80]: print(u)
