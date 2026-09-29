import re, math, itertools, sys, random
sys.path.insert(0,'..')
import logic_tools as LT
from logic_tools import V,N,A,O,I,E,X
import orig_lib as L
from orig_lib import sub, T
from qcore import near_ints
import knap, tsp
from cpp_snippets import CPP
p,q,r=V('p'),V('q'),V('r')
def TTtxt(f):
    vs,rows=LT.table(f); h=' | '.join(vs)+' | '+LT.show(f)
    return h+'\n'+'\n'.join(' | '.join('Đ' if x else 'S' for x in vals)+' | '+('Đ' if res else 'S') for vals,res in rows)
def TTeq(f,g):
    vs=sorted(LT.vars_of(f)|LT.vars_of(g)); h=' | '.join(vs)+' | '+LT.show(f)+' | '+LT.show(g)
    rows=[]
    for vals in itertools.product([True,False],repeat=len(vs)):
        env=dict(zip(vs,vals)); rows.append(' | '.join('Đ' if x else 'S' for x in vals)+' | '+('Đ' if LT.ev(f,env) else 'S')+' | '+('Đ' if LT.ev(g,env) else 'S'))
    return h+'\n'+'\n'.join(rows)
DER={
 'F1':'(p ∧ q) ⇒ p ≡ ¬(p ∧ q) ∨ p   (P ⇒ Q ≡ ¬P ∨ Q)\n≡ (¬p ∨ ¬q) ∨ p   (De Morgan)\n≡ (¬p ∨ p) ∨ ¬q   (giao hoán, kết hợp)\n≡ T ∨ ¬q ≡ T   (phần tử bù, luật nuốt)',
 'F2':'p ⇒ (p ∨ q) ≡ ¬p ∨ (p ∨ q)   (P ⇒ Q ≡ ¬P ∨ Q)\n≡ (¬p ∨ p) ∨ q   (kết hợp)\n≡ T ∨ q ≡ T',
 'F3':'¬p ⇒ (p ⇒ q) ≡ ¬¬p ∨ (¬p ∨ q)   (P ⇒ Q ≡ ¬P ∨ Q, hai lần)\n≡ p ∨ ¬p ∨ q   (phủ định kép, kết hợp)\n≡ T ∨ q ≡ T',
 'F4':'(p ∧ q) ⇒ (p ⇒ q) ≡ ¬(p ∧ q) ∨ (¬p ∨ q)\n≡ ¬p ∨ ¬q ∨ ¬p ∨ q   (De Morgan)\n≡ (¬q ∨ q) ∨ ¬p   (lũy đẳng, giao hoán)\n≡ T ∨ ¬p ≡ T',
 'F5':'¬(p ⇒ q) ⇒ p ≡ ¬¬(p ⇒ q) ∨ p   (P ⇒ Q ≡ ¬P ∨ Q)\n≡ (¬p ∨ q) ∨ p   (phủ định kép, P ⇒ Q ≡ ¬P ∨ Q)\n≡ (¬p ∨ p) ∨ q ≡ T',
 'F6':'¬(p ⇒ q) ⇒ ¬q ≡ (p ⇒ q) ∨ ¬q   (¬¬ và P ⇒ Q ≡ ¬P ∨ Q)\n≡ ¬p ∨ q ∨ ¬q   (kết hợp)\n≡ ¬p ∨ T ≡ T',
 'F7':'[¬p ∧ (p ∨ q)] ⇒ q ≡ ¬[¬p ∧ (p ∨ q)] ∨ q\n≡ p ∨ ¬(p ∨ q) ∨ q   (De Morgan, phủ định kép)\n≡ p ∨ (¬p ∧ ¬q) ∨ q   (De Morgan)\n≡ [(p ∨ ¬p) ∧ (p ∨ ¬q)] ∨ q   (phân phối)\n≡ (p ∨ ¬q) ∨ q ≡ p ∨ (¬q ∨ q) ≡ T',
 'F8':'[(p ⇒ q) ∧ (q ⇒ r)] ⇒ (p ⇒ r) ≡ ¬[(¬p ∨ q) ∧ (¬q ∨ r)] ∨ (¬p ∨ r)\n≡ [(p ∧ ¬q) ∨ (q ∧ ¬r)] ∨ ¬p ∨ r   (De Morgan)\n≡ [(p ∧ ¬q) ∨ ¬p] ∨ [(q ∧ ¬r) ∨ r]   (nhóm)\n≡ (¬p ∨ ¬q) ∨ (q ∨ r)   (hấp thụ/phân phối: (p ∧ ¬q) ∨ ¬p ≡ ¬q ∨ ¬p; (q ∧ ¬r) ∨ r ≡ q ∨ r)\n≡ (¬q ∨ q) ∨ ¬p ∨ r ≡ T',
 'F9':'[p ∧ (p ⇒ q)] ⇒ q ≡ ¬[p ∧ (¬p ∨ q)] ∨ q\n≡ ¬p ∨ ¬(¬p ∨ q) ∨ q   (De Morgan)\n≡ ¬p ∨ (p ∧ ¬q) ∨ q   (De Morgan, phủ định kép)\n≡ [(¬p ∨ p) ∧ (¬p ∨ ¬q)] ∨ q   (phân phối)\n≡ (¬p ∨ ¬q) ∨ q ≡ ¬p ∨ (¬q ∨ q) ≡ T',
 'F10':'[(p ∨ q) ∧ (p ⇒ r) ∧ (q ⇒ r)] ⇒ r ≡ ¬[(p ∨ q) ∧ (¬p ∨ r) ∧ (¬q ∨ r)] ∨ r\n≡ (¬p ∧ ¬q) ∨ (p ∧ ¬r) ∨ (q ∧ ¬r) ∨ r   (De Morgan)\n≡ (¬p ∧ ¬q) ∨ [(p ∨ q) ∧ ¬r] ∨ r   (phân phối ngược)\n≡ (¬p ∧ ¬q) ∨ (p ∨ q) ∨ r   (vì (X ∧ ¬r) ∨ r ≡ X ∨ r)\n≡ ¬(p ∨ q) ∨ (p ∨ q) ∨ r ≡ T',
 'E1':'p ⇔ q ≡ (p ⇒ q) ∧ (q ⇒ p)   (định nghĩa)\n≡ (¬p ∨ q) ∧ (¬q ∨ p)\n≡ (¬p ∧ ¬q) ∨ (¬p ∧ p) ∨ (q ∧ ¬q) ∨ (q ∧ p)   (phân phối)\n≡ (¬p ∧ ¬q) ∨ F ∨ F ∨ (p ∧ q) ≡ (p ∧ q) ∨ (¬p ∧ ¬q)',
 'E2':'p ⇒ q ≡ ¬p ∨ q   (định nghĩa)\n≡ q ∨ ¬p   (giao hoán)\n≡ ¬¬q ∨ ¬p   (phủ định kép)\n≡ ¬q ⇒ ¬p   (P ⇒ Q ≡ ¬P ∨ Q)',
 'E3':'p ⊕ q ≡ (p ∧ ¬q) ∨ (¬p ∧ q)   (định nghĩa)\n¬(p ⊕ q) ≡ ¬(p ∧ ¬q) ∧ ¬(¬p ∧ q)   (De Morgan)\n≡ (¬p ∨ q) ∧ (p ∨ ¬q) ≡ (p ⇒ q) ∧ (q ⇒ p) ≡ p ⇔ q',
 'E4':'¬(p ⇔ q) ≡ p ⊕ q ≡ (p ∧ ¬q) ∨ (¬p ∧ q)   (phủ định của ⇔)\n¬p ⇔ q ≡ (¬p ∧ q) ∨ (¬¬p ∧ ¬q)   (p ⇔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q))\n≡ (¬p ∧ q) ∨ (p ∧ ¬q) — trùng với vế trên (giao hoán ∨).'}
LAW={'1.1':'giao hoán','1.2':'kết hợp','1.3':'phân phối','1.4':'De Morgan'}
def ch1(iid,lab,ref,t):
    G=None
    # (kind, f, g, deriv key)
    table={('1.1','a'):('eq',O(p,q),O(q,p),None),('1.1','b'):('eq',A(p,q),A(q,p),None),('1.2','a'):('eq',O(O(p,q),r),O(p,O(q,r)),None),('1.2','b'):('eq',A(A(p,q),r),A(p,A(q,r)),None),
      ('1.3','a'):('eq',O(p,A(q,r)),A(O(p,q),O(p,r)),None),('1.3','b'):('eq',A(p,O(q,r)),O(A(p,q),A(p,r)),None),('1.4','a'):('eq',N(A(p,q)),O(N(p),N(q)),None),('1.4','b'):('eq',N(O(p,q)),A(N(p),N(q)),None),
      ('1.5','a'):('taut',I(A(p,q),p),None,'F1'),('1.5','b'):('taut',I(p,O(p,q)),None,'F2'),('1.5','c'):('taut',I(N(p),I(p,q)),None,'F3'),
      ('1.6','a'):('taut',I(A(p,q),I(p,q)),None,'F4'),('1.6','b'):('taut',I(N(I(p,q)),p),None,'F5'),('1.6','c'):('taut',I(N(I(p,q)),N(q)),None,'F6'),
      ('1.7','a'):('taut',I(A(N(p),O(p,q)),q),None,'F7'),('1.7','b'):('taut',I(A(I(p,q),I(q,r)),I(p,r)),None,'F8'),
      ('1.8','a'):('taut',I(A(p,I(p,q)),q),None,'F9'),('1.8','b'):('taut',I(A(A(O(p,q),I(p,r)),I(q,r)),r),None,'F10'),
      ('1.9','a'):('eq',E(p,q),O(A(p,q),A(N(p),N(q))),'E1'),('1.9','b'):('eq',I(p,q),I(N(q),N(p)),'E2'),
      ('1.10','a'):('eq',N(X(p,q)),E(p,q),'E3'),('1.10','b'):('eq',N(E(p,q)),E(N(p),q),'E4'),
      ('1.11','a'):('taut',I(A(p,q),p),None,'F1'),('1.11','b'):('taut',I(p,O(p,q)),None,'F2'),('1.12','a'):('taut',I(N(p),I(p,q)),None,'F3'),('1.12','b'):('taut',I(A(p,q),I(p,q)),None,'F4'),
      ('1.13','a'):('taut',I(N(I(p,q)),p),None,'F5'),('1.13','b'):('taut',I(N(I(p,q)),N(q)),None,'F6'),('1.14','a'):('taut',I(A(N(p),O(p,q)),q),None,'F7'),('1.14','b'):('taut',I(A(I(p,q),I(q,r)),I(p,r)),None,'F8'),
      ('1.15','a'):('taut',I(A(p,I(p,q)),q),None,'F9'),('1.15','b'):('taut',I(A(A(O(p,q),I(p,r)),I(q,r)),r),None,'F10'),('1.16','a'):('eq',E(p,q),O(A(p,q),A(N(p),N(q))),'E1'),('1.16','b'):('eq',I(p,q),I(N(q),N(p)),'E2'),
      ('1.17','a'):('eq',N(X(p,q)),E(p,q),'E3'),('1.17','b'):('eq',N(E(p,q)),E(N(p),q),'E4')}
    key=(iid,lab)
    if key not in table: return False
    kind,f,g,dk=table[key]
    nb='không dùng bảng' if iid in ('1.11','1.12','1.13','1.14','1.15','1.16','1.17') else 'bảng chân lý'
    if kind=='taut': assert LT.kind(f)=='taut',(key,LT.show(f))
    else: assert LT.equiv(f,g),(key,LT.show(f),LT.show(g))
    stem=(f'Dùng bảng chân lý để chứng minh {LT.show(f)} là hằng đúng.' if kind=='taut' else f'Dùng bảng chân lý để chứng minh {LT.show(f)} ≡ {LT.show(g)}.') if nb=='bảng chân lý' else (f'Không dùng bảng chân lý, chứng minh {LT.show(f)} là hằng đúng.' if kind=='taut' else f'Không dùng bảng chân lý, chứng minh {LT.show(f)} ≡ {LT.show(g)}.')
    if nb=='bảng chân lý': sol=(TTtxt(f)+'\nCột cuối toàn Đ ⇒ hằng đúng. ∎') if kind=='taut' else (TTeq(f,g)+'\nHai cột cuối giống hệt nhau trên mọi dòng ⇒ tương đương. ∎')
    else: sol=DER[dk]+' ∎'
    if iid in LAW and nb=='bảng chân lý': sol=f'Luật {LAW[iid]}. '+sol
    add_rec(mod='m01',src=ref,q=stem,ans=None,wrong=[],sol=sol,level=1 if nb=='bảng chân lý' else 2,topic='Chứng minh logic')
    if kind=='taut' and nb=='bảng chân lý':
        vs,rows=LT.table(f)
        add_rec(mod='m01',src=ref+' (chuyển thành trắc nghiệm)',q=f'Công thức {LT.show(f)} thuộc loại nào?',ans='Hằng đúng (tautology)',wrong=['Mâu thuẫn (hằng sai)','Thỏa được nhưng không hằng đúng','Không thể kết luận nếu chưa biết giá trị các biến'],sol=f'Lập bảng chân trị {len(rows)} dòng: mọi dòng cho Đ ⇒ hằng đúng.\n'+TTtxt(f),level=1,topic='Phân loại công thức')
    return True
from recstore import add as add_rec
def ch1_sets(iid,lab,ref,t):
    S={('1.18','a'):('(B − A) ∪ (C − A) = (B ∪ C) − A','x ∈ (B − A) ∪ (C − A) ⇔ (x ∈ B ∧ x ∉ A) ∨ (x ∈ C ∧ x ∉ A) ⇔ (x ∈ B ∨ x ∈ C) ∧ x ∉ A   (phân phối)\n⇔ x ∈ B ∪ C ∧ x ∉ A ⇔ x ∈ (B ∪ C) − A. ∎'),
       ('1.18','b'):('A − B = A ∩ Bᶜ','x ∈ A − B ⇔ x ∈ A ∧ x ∉ B ⇔ x ∈ A ∧ x ∈ Bᶜ ⇔ x ∈ A ∩ Bᶜ. ∎'),
       ('1.19','a'):('A ∪ (B ∪ C) = (A ∪ B) ∪ C','x ∈ A ∪ (B ∪ C) ⇔ x ∈ A ∨ (x ∈ B ∨ x ∈ C) ⇔ (x ∈ A ∨ x ∈ B) ∨ x ∈ C   (kết hợp của ∨) ⇔ x ∈ (A ∪ B) ∪ C. ∎'),
       ('1.19','b'):('(A − B) − C = (A − B) − (B − C)','⚠ Phát biểu trong đề gốc KHÔNG đúng với mọi tập hợp. Phản ví dụ: A = {1}, B = ∅, C = {1}. Khi đó (A − B) − C = {1} − {1} = ∅ nhưng (A − B) − (B − C) = {1} − ∅ = {1}.\nĐẳng thức đúng liên quan: (A − B) − (B − C) = A − B (vì B − C ⊆ B và A − B không chứa phần tử nào của B), còn (A − B) − C = A − (B ∪ C).'),
       ('1.20','b'):('A − B = A ∩ Bᶜ','x ∈ A − B ⇔ x ∈ A ∧ x ∉ B ⇔ x ∈ A ∩ Bᶜ. ∎')}
    if (iid,lab) in S:
        a,sol=S[(iid,lab)]
        if (iid,lab)==('1.19','b') or (iid=='1.20' and 'C' in t and lab=='b' and '(A − B)− C' in t):
            a,sol=S[('1.19','b')]
            add_rec(mod='m03',src=ref+' ⚠ đề gốc có lỗi',q=f'Chứng minh rằng {a} (kiểm tra xem phát biểu có đúng không).',ans=None,wrong=[],sol=sol,level=3,topic='Chứng minh tập hợp'); return True
        add_rec(mod='m03',src=ref,q=f'Cho A, B, C là các tập hợp. Chứng minh rằng {a}.',ans=None,wrong=[],sol=sol,level=2,topic='Chứng minh tập hợp'); return True
    m=re.search(r'\(A ∩ B\) ∪ A ∩ B',t)
    if iid=='1.18' and '= A' in t and lab=='b':
        add_rec(mod='m03',src=ref,q='Cho A, B là các tập hợp. Chứng minh rằng (A ∩ B) ∪ (A ∩ Bᶜ) = A.',ans=None,wrong=[],sol='(A ∩ B) ∪ (A ∩ Bᶜ) = A ∩ (B ∪ Bᶜ)   (phân phối)\n= A ∩ U = A. ∎',level=2,topic='Chứng minh tập hợp'); return True
    return False

# ================= CHƯƠNG 3: LIỆT KÊ =================
def _nums(s): return [int(x) for x in re.findall(r'\d+',s)]
def next_perm(a):
    a=list(a); i=len(a)-2
    while i>=0 and a[i]>a[i+1]: i-=1
    if i<0: return None
    j=len(a)-1
    while a[j]<a[i]: j-=1
    a[i],a[j]=a[j],a[i]; a[i+1:]=reversed(a[i+1:]); return tuple(a)
def next_comb(c,n):
    k=len(c); a=list(c); i=k-1
    while i>=0 and a[i]==n-k+i+1: i-=1
    if i<0: return None
    a[i]+=1
    for j in range(i+1,k): a[j]=a[j-1]+1
    return tuple(a)
def next_bin(b):
    a=list(b); i=len(a)-1
    while i>=0 and a[i]==1: a[i]=0; i-=1
    if i<0: return None
    a[i]=1; return tuple(a)
def chain(f,x,k,*e):
    out=[]
    for _ in range(k):
        x=f(x,*e)
        if x is None: break
        out.append(x)
    return out
def LT_(ts): return ' → '.join(T(t) for t in ts)
ALG={
 'sinh_perm':('Thuật toán sinh hoán vị kế tiếp theo thứ tự từ điển','Hoán vị đầu: (1,2,…,n); hoán vị cuối: (n,…,2,1).\nTừ p = (p₁,…,p_n):\n1) tìm i lớn nhất sao cho p[i] < p[i+1]; nếu không có i thì p là hoán vị cuối ⇒ dừng.\n2) tìm j lớn nhất sao cho p[j] > p[i].\n3) đổi chỗ p[i] và p[j].\n4) đảo ngược đoạn p[i+1..n].\nKết quả là hoán vị kế tiếp. Độ phức tạp mỗi lần sinh: O(n).','perm_gen'),
 'sinh_comb':('Thuật toán sinh tổ hợp chập k kế tiếp theo thứ tự từ điển','Tổ hợp đầu (1,2,…,k); tổ hợp cuối (n−k+1,…,n).\nTừ c = (c₁<…<c_k):\n1) tìm i lớn nhất sao cho c[i] ≠ n−k+i; nếu không có thì c là tổ hợp cuối ⇒ dừng.\n2) c[i] = c[i] + 1.\n3) với j = i+1..k: c[j] = c[j−1] + 1.\nMỗi lần sinh O(k).','comb_gen'),
 'sinh_bin':('Thuật toán sinh xâu nhị phân kế tiếp theo thứ tự từ điển','Xâu đầu 00…0; xâu cuối 11…1.\nTừ x = (x₁,…,x_n): tìm i lớn nhất sao cho x[i] = 0; nếu không có thì x là xâu cuối ⇒ dừng. Đặt x[i] = 1 và mọi x[j] = 0 với j > i. (Chính là phép cộng 1 trong hệ nhị phân.)','bin_gen'),
 'bt_perm':('Thuật toán quay lui liệt kê hoán vị của 1..n','Try(i): với mỗi v = 1..n chưa dùng (used[v] = false): gán x[i] = v, used[v] = true; nếu i = n thì in x, ngược lại gọi Try(i+1); sau đó trả lại used[v] = false. Gọi Try(1).\nKiểm nghiệm n = 3: thứ tự in 123, 132, 213, 231, 312, 321 (thứ tự từ điển).','perm_bt'),
 'bt_comb':('Thuật toán quay lui liệt kê tổ hợp chập k của 1..n','Try(i): với v = x[i−1]+1 … n−k+i: gán x[i] = v; nếu i = k thì in x, ngược lại Try(i+1). Đặt x[0] = 0 và gọi Try(1). Cận trên n−k+i bảo đảm còn đủ phần tử cho các vị trí sau.','comb_bt'),
 'bt_bin':('Thuật toán quay lui liệt kê xâu nhị phân độ dài n','Try(i): với v = 0, 1: gán x[i] = v; nếu i = n thì in x, ngược lại gọi Try(i+1). Gọi Try(1). Có 2ⁿ xâu; kiểm nghiệm n = 3: 000, 001, 010, 011, 100, 101, 110, 111.','bin_bt')}
def alg_solution(key,extra=''):
    title,text,code=ALG[key]
    return f'{title}.\n{text}\n\nMã C/C++:\n{CPP[code]}'+extra
def ch3(iid,lab,ref,t):
    tt=t
    m=re.search(r'sinh hoán vị theo thứ tự từ điển,? (?:tìm|liệt kê) (\d+) hoán vị (?:liền kề )?tiếp theo của (?:hoán vị )?\(?([\d,\s]+)\)?',tt)
    if m and 'Trình bày' not in tt:
        k=int(m.group(1)); digs=m.group(2).strip(); x=tuple(int(c) for c in digs) if ',' not in digs and len(digs.strip())>=9 else tuple(_nums(digs))
        ch=chain(next_perm,x,k); n=len(x)
        wr=[LT_(list(reversed(ch))),LT_([tuple(sorted(y)) for y in ch]),LT_(ch[1:]+[x])]
        add_rec(mod='m10',src=ref,q=f'Cho tập A = {{1,…,{n}}}. Dùng phương pháp sinh hoán vị theo thứ tự từ điển, {k} hoán vị liền kề tiếp theo của {T(x)} là:',ans=LT_(ch),wrong=wr,sol='Áp dụng lần lượt thuật toán hoán vị kế tiếp:\n'+LT_([x]+ch),level=3,topic='Hoán vị kế tiếp'); return True
    m=re.search(r'sinh tổ hợp chập k .*?(?:tạo|liệt kê)(?: ra)? (\d+) tổ hợp chập (\d+) liền kề tiếp theo của (?:tổ hợp )?\(?([\d,\s]+)\)?',tt)
    if m and 'Trình bày' not in tt.split('Cho tập')[0]:
        k=int(m.group(1)); c=tuple(_nums(m.group(3))); n=10 if '10}' in tt or '10 }' in tt or max(c)==10 else 9
        ch=chain(next_comb,c,k,n)
        add_rec(mod='m10',src=ref,q=f'Cho tập A = {{1,…,{n}}}. Sinh các tổ hợp chập {len(c)} theo thứ tự từ điển: {k} tổ hợp liền kề tiếp theo của {T(c)} là:',ans=LT_(ch),wrong=[LT_(list(reversed(ch))),LT_(ch[1:]+[c]),LT_([tuple(sorted(y[:-1]+(y[-1]-1,))) for y in ch])],sol='Áp dụng lần lượt thuật toán tổ hợp kế tiếp:\n'+LT_([c]+ch),level=3,topic='Tổ hợp kế tiếp'); return True
    m=re.search(r'xâu nhị phân X = \{([\d,\s]+)\}.*?tìm (\d+) xâu',tt)
    if m:
        x=tuple(_nums(m.group(1))); k=int(m.group(2)); ch=chain(next_bin,x,k)
        add_rec(mod='m10',src=ref,q=f'Cho xâu nhị phân X = {T(x)}. Dùng phương pháp sinh xâu nhị phân theo thứ tự từ điển, {k} xâu liền kề tiếp theo của X là:',ans=LT_(ch),wrong=[LT_(list(reversed(ch))),LT_([tuple(1-b for b in y) for y in ch]),LT_(ch[1:]+[x])],sol='Xâu kế tiếp = xâu hiện tại + 1 (nhị phân):\n'+LT_([x]+ch),level=2,topic='Xâu nhị phân kế tiếp'); return True
    # thuật toán / mã
    if re.search(r'Trình bày thuật toán sinh theo thứ tự từ điển hoán vị kế tiếp',tt) or re.search(r'sinh.*hoán vị.*C/\+\+|Áp dụng thuật toán tại Mục a, viết chương trình.*hoán vị',tt) and 'quay lui' not in tt:
        add_rec(mod='m10',src=ref,q=tt,ans=None,wrong=[],sol=alg_solution('sinh_perm'),level=3,topic='Thuật toán sinh'); return True
    if 'quay lui' in tt and 'hoán vị' in tt or (iid=='3.3' and lab.strip('()')=='b'):
        add_rec(mod='m11',src=ref,q=tt,ans=None,wrong=[],sol=alg_solution('bt_perm'),level=3,topic='Quay lui'); return True
    if 'quay lui' in tt and 'tổ hợp' in tt or (iid=='3.6' and lab.strip('()')=='b') or (iid=='3.13' and lab.strip('()')=='a'):
        add_rec(mod='m11',src=ref,q=tt,ans=None,wrong=[],sol=alg_solution('bt_comb'),level=3,topic='Quay lui'); return True
    if 'quay lui' in tt and 'xâu nhị phân' in tt or (iid=='3.9' and lab.strip('()')=='b'):
        add_rec(mod='m11',src=ref,q=tt,ans=None,wrong=[],sol=alg_solution('bt_bin'),level=2,topic='Quay lui'); return True
    if re.search(r'tổ hợp chập k',tt) or (iid=='3.4' and lab.strip('()')=='b'):
        add_rec(mod='m10',src=ref,q=tt,ans=None,wrong=[],sol=alg_solution('sinh_comb'),level=3,topic='Thuật toán sinh'); return True
    if re.search(r'xâu nhị phân',tt) or (iid=='3.7'):
        add_rec(mod='m10',src=ref,q=tt,ans=None,wrong=[],sol=alg_solution('sinh_bin'),level=2,topic='Thuật toán sinh'); return True
    return False

# ================= CHƯƠNG 4: TỐI ƯU =================
sys.path.insert(0,'..')
import gen_m12 as G12
import gen_m13 as G13
def parse_knap(t):
    t=t.replace('⟶','→')
    i=t.find('max'); obj=t[:i]; rest=t[i+3:]
    b=re.search(r'≤\s*(\d+)',rest); 
    def co(s):
        d={}
        for c,j in re.findall(r'(\d*)\s*x(\d)',s): d[int(j)]=int(c) if c else 1
        return [d[j] for j in sorted(d)]
    return co(obj),co(rest.split('≤')[0]),int(b.group(1))
def ch4(iid,lab,ref,t):
    lb=lab.strip('()')
    if lb=='a':
        if 'người đi du lịch' in t or 'người du lịch' in t:
            add_rec(mod='m13',src=ref,q=t,ans=None,wrong=[],sol='Bài toán: cho n thành phố, ma trận chi phí C; tìm hành trình đi qua mỗi thành phố đúng một lần rồi quay về điểm xuất phát với tổng chi phí nhỏ nhất.\nThuật toán nhánh cận (rút gọn ma trận):\n1) Rút gọn ma trận: trừ phần tử nhỏ nhất của mỗi dòng rồi của mỗi cột; tổng các hằng số trừ là cận dưới của mọi hành trình.\n2) Chọn số 0 (r,c) có tổng (min dòng r khác nó + min cột c khác nó) lớn nhất làm cạnh phân nhánh.\n3) Nhánh chứa (r,c): bỏ dòng r, cột c; đặt ô cấm chu trình con bằng ∞; rút gọn, cộng vào cận dưới.\n4) Nhánh không chứa (r,c): đặt C[r][c] = ∞, rút gọn, cận dưới tăng thêm đúng bằng tổng min dòng + min cột.\n5) Duyệt nhánh chứa trước; khi ma trận còn 2×2 kết nạp nốt hai cạnh để được hành trình đầy đủ và cập nhật kỷ lục; cắt mọi nhánh có cận dưới ≥ kỷ lục.',level=3,topic='TSP nhánh cận'); return True
        if 'duyệt toàn bộ' in t:
            add_rec(mod='m12',src=ref,q=t,ans=None,wrong=[],sol='Thuật toán duyệt toàn bộ: (1) XOPT = ∅, FOPT = −∞ (bài toán max) hoặc +∞ (min). (2) Với mỗi phương án X thuộc tập phương án D: tính S = f(X); nếu S tốt hơn FOPT thì FOPT = S, XOPT = X. (3) Trả về (XOPT, FOPT).\nƯu điểm: đơn giản, chắc chắn. Nhược điểm: số phương án bùng nổ (2ⁿ, n!).\nVới cái túi: duyệt 2ⁿ vectơ x ∈ {0,1}ⁿ, loại các vectơ vượt trọng lượng, lấy vectơ có giá trị lớn nhất.',level=1,topic='Duyệt toàn bộ'); return True
        add_rec(mod='m12',src=ref,q=t,ans=None,wrong=[],sol='Bài toán cái túi: có n đồ vật, vật j có trọng lượng aⱼ và giá trị cⱼ; chọn tập vật (xⱼ ∈ {0,1}) có tổng trọng lượng ≤ b để tổng giá trị lớn nhất.\nThuật toán nhánh cận: sắp các vật theo cⱼ/aⱼ giảm dần; dùng quay lui gán x₁, x₂, … (thử giá trị lớn trước); với phương án bộ phận (u₁..u_k) gọi δ_k là giá trị đã chọn, b_k trọng lượng còn lại thì cận trên g = δ_k + c_{k+1}·b_k/a_{k+1}. Nếu g ≤ FOPT (kỷ lục hiện có) thì cắt nhánh; nếu k = n thì cập nhật kỷ lục.\n\nMã C++:\n'+CPP['knap_bb'],level=3,topic='Nhánh cận cái túi'); return True
    if lb=='b' or lb=='':
        if 'ma trận chi phí' in t:
            mats={'4.4':[[0,31,15,23,10,17],[16,0,24,7,12,12],[34,3,0,25,54,25],[15,20,33,0,50,40],[16,10,32,3,0,23],[18,20,13,28,21,0]],'4.5':[[0,3,93,13,33,9],[4,0,77,42,21,16],[45,17,0,36,16,28],[39,90,80,0,56,7],[28,46,88,33,0,25],[3,88,18,46,92,0]]}
            C=mats[iid]; res=tsp.bb(C); best,bt=tsp.brute(C); assert res['cost']==best
            lines=[f'Cận dưới ở gốc sau rút gọn = {res["root"]}.']
            for e in res['log'][:22]:
                d,l,bd,st=e[0],e[1],e[2],e[3]
                tail={'branch':f'→ chọn cạnh {e[4] if len(e)>4 else ""} (β = {e[5] if len(e)>5 else ""})','record':f'★ hành trình đầy đủ, chi phí {e[4] if len(e)>4 else ""}','leaf':'lá (không cải thiện)','cut':'✗ cắt (cận dưới ≥ kỷ lục)','dead':'✗ vô nghiệm','root':''}[st]
                lines.append('  '*d+f'[{l}] cận dưới = {bd} {tail}')
            lines.append(f'Kết quả: hành trình tối ưu {"→".join(map(str,res["tour"]))}, chi phí {res["cost"]} (đối chiếu vét cạn 5! = 120 hành trình).')
            mt='\n'.join('  '+' '.join(f'{("∞" if i==j else x):>3}' for j,x in enumerate(row)) for i,row in enumerate(C))
            add_rec(mod='m13',src=ref,q='Giải bài toán người du lịch bằng thuật toán nhánh cận với ma trận chi phí (∞ trên đường chéo):\n'+mt,ans=None,wrong=[],sol='\n'.join(lines),level=3,topic='TSP nhánh cận')
            rng=random.Random(int(iid.split('.')[1]))
            add_rec(mod='m13',src=ref+' (chuyển thành trắc nghiệm)',q='Ma trận chi phí người du lịch (∞ trên đường chéo):\n'+mt+'\nChi phí của hành trình tối ưu là:',ans=str(best),wrong=[str(x) for x in near_ints(best,rng,4,lo=1)],sol='\n'.join(lines),level=3,topic='Hành trình tối ưu')
            add_rec(mod='m13',src=ref+' (chuyển thành trắc nghiệm)',q='Ma trận chi phí người du lịch (∞ trên đường chéo):\n'+mt+'\nCận dưới ở gốc sau thủ tục rút gọn (tổng hằng số rút gọn theo dòng và cột) là:',ans=str(res['root']),wrong=[str(x) for x in near_ints(res['root'],rng,4,lo=1)],sol='Rút gọn dòng rồi cột; tổng các hằng số trừ = '+str(res['root'])+'.',level=2,topic='Rút gọn ma trận')
            return True
        v,w,b=parse_knap(t)
        best,bx,feas=knap.brute(v,w,b); res=knap.bb(v,w,b); assert res['fopt']==best
        n=len(v)
        def lin(cs): return ' + '.join((str(c) if c!=1 else '')+f'x{sub(i+1)}' for i,c in enumerate(cs))
        stem=f'{lin(v)} → max; {lin(w)} ≤ {b}; xⱼ ∈ {{0,1}}.'
        if 'duyệt toàn bộ' in t:
            rows=[]
            for x in itertools.product((0,1),repeat=n):
                W=sum(a*c for a,c in zip(w,x)); V=sum(a*c for a,c in zip(v,x)); rows.append(f'{T(x)}: trọng lượng {W} '+(f'> {b} (loại)' if W>b else f'≤ {b}, giá trị {V}'))
            sol='\n'.join(rows)+f'\nXOPT = {T(bx)}, FOPT = {best}.'
            q0='Áp dụng thuật toán duyệt toàn bộ giải bài toán cái túi: '+stem
            topic='Duyệt toàn bộ'
        else:
            sol=G12.trace_text(v,w,b,res); q0='Áp dụng thuật toán nhánh cận giải bài toán cái túi, chỉ rõ kết quả theo mỗi bước: '+stem; topic='Nhánh cận cái túi'
        add_rec(mod='m12',src=ref,q=q0,ans=None,wrong=[],sol=sol,level=3,topic=topic)
        wl=[x for x in itertools.product((0,1),repeat=n) if x!=bx]
        wl=sorted(wl,key=lambda x:-sum(a*c for a,c in zip(v,x)))[:3]
        add_rec(mod='m12',src=ref+' (chuyển thành trắc nghiệm)',q='Cái túi: '+stem+' Phương án tối ưu là:',ans=T(bx),wrong=[T(x) for x in wl],sol=sol+f'\nPhương án tối ưu {T(bx)} với giá trị {best}.',level=2,topic='Phương án tối ưu')
        add_rec(mod='m12',src=ref+' (chuyển thành trắc nghiệm)',q='Cái túi: '+stem+' Giá trị tối ưu f* bằng:',ans=str(best),wrong=[str(best+d) for d in (-2,-1,1,2) if best+d>=0][:4]+[str(sum(v))],sol=f'Duyệt toàn bộ {2**n} phương án: {feas} phương án khả thi; giá trị lớn nhất {best} tại {T(bx)}.',level=2,topic='Giá trị tối ưu')
        return True
    return False

# ================= CHƯƠNG 5: TỒN TẠI =================
def ch5(iid,lab,ref,t):
    lb=lab.strip('()'); key=(iid,lb)
    def num(stem,ans,wrong,sol,lv=2,tp='Dirichlet tổng quát',mod='m06'):
        add_rec(mod=mod,src=ref,q=stem,ans=str(ans),wrong=[str(x) for x in wrong],sol=sol,level=lv,topic=tp)
    def proof(sol,tp='Chứng minh tồn tại'): add_rec(mod='m06',src=ref,q=t,ans=None,wrong=[],sol=sol,level=3,topic=tp)
    HS='Coi mỗi khách là một đỉnh, mỗi cái bắt tay là một cạnh. Tổng số lần bắt tay đếm theo từng người = tổng bậc = 2·(số cái bắt tay) là số CHẴN. Ở đây tổng = 20·10 + 15·5 = 275 là số LẺ ⇒ mâu thuẫn ⇒ người quan sát đã đếm nhầm. ∎'
    CIR='Phản chứng: giả sử không có hai bạn kề nhau cùng khối. Khi đó dọc vòng tròn các khối xen kẽ A, B, A, B, … nên số người phải CHẴN. Nhưng 45 là số lẻ ⇒ mâu thuẫn ⇒ luôn có hai bạn kề nhau cùng khối. ∎'
    if key in (('5.1','a'),('5.9','b')): proof(HS,'Chứng minh tồn tại'); return True
    if key in (('5.2','a'),('5.10','b')): proof(CIR); return True
    if key==('5.3','b'): proof('Phản chứng: giả sử mọi sinh viên đều có số thứ tự KHÔNG lớn hơn số của bạn bên trái. Đi vòng quanh thì dãy số không tăng và quay về chính nó nên mọi số bằng nhau. Nhưng 30 số thứ tự đôi một khác nhau ⇒ mâu thuẫn. Vậy tồn tại bạn có số lớn hơn số của bạn bên trái. ∎'); return True
    if key==('5.1','b'): num(t+' (coi có 366 ngày, kể cả 29/2)',366*4+1,[365*4+1,366*5,366*4,365*5+1],'Có 366 cặp (ngày, tháng) khác nhau (kể cả 29/2). Để chắc chắn có 5 sinh viên cùng ngày sinh và tháng sinh cần 366·(5−1) + 1 = 1465 sinh viên. (Nếu bỏ qua 29/2 thì 365·4+1 = 1461.)'); return True
    if key==('5.2','b'): num(t,3*3*3+1,[27,9*4,3*3*4,9*3],'Có 3·3 = 9 kiểu bi. Cần 9·(4−1) + 1 = 28 viên.'); return True
    if key==('5.3','a'): num(t,51*4+1,[50*4+1,51*5,50*5,51*4],'Số mức điểm khác nhau = 50 + 1 = 51 (0…50 câu đúng). Cần 51·(5−1) + 1 = 205 thí sinh.'); return True
    if key==('5.4','a'): num(t,6*4+1,[6*5,5*4+1,24,6*4+2],'Có 2·3 = 6 kiểu bi. Cần 6·(5−1) + 1 = 25 viên.'); return True
    if key==('5.4','b'): num(t,12*9+1,[12*10,11*9+1,108,12*9+2],'12 tháng sinh. Cần 12·(10−1) + 1 = 109 sinh viên.'); return True
    if key==('5.5','a'): num(t,f'5^50',['4^50','5^49','50^5','5·50'],'Mỗi câu có 5 lựa chọn (4 phương án hoặc để trống); 50 câu độc lập nên có 5^50 cách điền.',lv=2,tp='Quy tắc nhân'); return True
    if key==('5.5','b'): num(t,101*9+1,[100*9+1,101*10,100*10,51*9+1],'Tổng số câu đúng của hai môn nhận các giá trị 0…100 (101 mức điểm, cách 0,2 điểm). Cần 101·(10−1) + 1 = 910 thí sinh.'); return True
    if key==('5.6','a'): num(t,'6^100',['5^100','6^99','100^6','5·100'],'Mỗi câu có 6 lựa chọn (5 phương án hoặc để trống); 100 câu: 6^100 cách.',lv=2,tp='Quy tắc nhân'); return True
    if key==('5.6','b'): num(t,201*4+1,[200*4+1,201*5,200*5,101*4+1],'Tổng số câu đúng nhận 201 giá trị 0…200. Cần 201·(5−1) + 1 = 805 thí sinh.'); return True
    if key==('5.7','a'): num(t,51*14+1,[50*14+1,51*15,50*15,51*14],'51 mức điểm (0…50 câu đúng, mỗi câu 2 điểm). Cần 51·(15−1) + 1 = 715 thí sinh.'); return True
    if key==('5.8','b'): num(t,12*7+1,[12*8,11*7+1,84,12*7+2],'Cần 12·(8−1) + 1 = 85 sinh viên.'); return True
    if key in (('5.9','a'),('5.10','a')) or (iid=='5.10' and lb in('a','c')):
        m=re.search(r'chia hết cho (\d+)',t); mm=int(m.group(1)) if m else (7 if iid=='5.10' else 5)
        num('Gọi S là tập các cặp (x, y) với x, y nguyên. Cần lấy ra ít nhất bao nhiêu phần tử của S để chắc chắn có 2 bộ (a,b), (c,d) mà (a−c) và (b−d) đều chia hết cho %d?'%mm,mm*mm+1,[mm*mm,mm*mm-1,2*mm*mm+1,mm+1],f'Mỗi cặp thuộc một "hộp" theo (x mod {mm}, y mod {mm}): có {mm}·{mm} = {mm*mm} hộp. Cần {mm*mm}+1 = {mm*mm+1} cặp để chắc chắn có hai cặp cùng hộp.',lv=3,tp='Dirichlet – đồng dư'); return True
    return False
