from qcore import *
import itertools, math
def sub(n): return ''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(n))
def T(t): return '('+', '.join(map(str,t))+')'
def LT(ts): return ' → '.join(T(t) for t in ts)
def next_perm(p):
    a=list(p); i=len(a)-2
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
def steps(f,x,k,*extra):
    out=[]
    for _ in range(k):
        x=f(x,*extra)
        if x is None: break
        out.append(x)
    return out
def rank_perm(p):
    n=len(p); r=0; av=sorted(p)
    for i,x in enumerate(p):
        idx=av.index(x); r+=idx*math.factorial(n-1-i); av.remove(x)
    return r+1
def unrank_perm(n,r):
    r-=1; av=list(range(1,n+1)); out=[]
    for i in range(n):
        f=math.factorial(n-1-i); q,r=divmod(r,f); out.append(av.pop(q))
    return tuple(out)
def rank_comb(c,n):
    allc=list(itertools.combinations(range(1,n+1),len(c))); return allc.index(tuple(c))+1
def gen(seed=10):
    B=Bank('m10',seed); rng=B.rng
    # ---- hoán vị kế tiếp
    for _ in range(50):
        n=rng.randint(5,9); p=tuple(rng.sample(range(1,n+1),n)); nx=next_perm(p)
        if nx is None: continue
        # phân tích chi tiết
        a=list(p); i=n-2
        while i>=0 and a[i]>a[i+1]: i-=1
        j=n-1
        while a[j]<a[i]: j-=1
        wr=set()
        b=list(p); b[i],b[j]=b[j],b[i]; wr.add(tuple(b))     # quên đảo
        b=list(p); b[-1],b[-2]=b[-2],b[-1]; wr.add(tuple(b))  # đổi hai cuối
        c=list(p); c[i],c[-1]=c[-1],c[i]; c[i+1:]=sorted(c[i+1:]); wr.add(tuple(c))   # chọn sai phần tử
        d=list(p); d[i:]=sorted(d[i:]); wr.add(tuple(d))
        wr.discard(nx); wr={w for w in wr if w!=p}
        wr|={tuple(rng.sample(range(1,n+1),n)) for _ in range(4)}; wr.discard(nx)
        expl=(f'Hoán vị {T(p)}: tìm i lớn nhất sao cho p[i] < p[i+1]: i = vị trí {i+1} (giá trị {p[i]}).\nTìm j lớn nhất sao cho p[j] > p[i]: p[j] = {p[j]} (vị trí {j+1}). Đổi chỗ: {T(tuple(x if k not in(i,j) else (p[j] if k==i else p[i]) for k,x in enumerate(p)))}.\nĐảo ngược đoạn sau vị trí {i+1}: kết quả {T(nx)}.')
        B.add(f'Sinh hoán vị theo thứ tự từ điển: hoán vị liền kề sau {T(p)} (tập {{1..{n}}}) là:',T(nx),[T(w) for w in wr],expl,level=2,topic='Hoán vị kế tiếp')
    for _ in range(35):
        n=rng.randint(6,9); p=tuple(rng.sample(range(1,n+1),n)); k=rng.randint(3,6); s=steps(next_perm,p,k)
        if len(s)<k: continue
        B.add(f'Cho tập A = {{1,…,{n}}}. Dùng phương pháp sinh hoán vị theo thứ tự từ điển, {k} hoán vị liền kề tiếp theo của {T(p)} lần lượt là:',LT(s),[LT(list(reversed(s))),LT([next_perm(next_perm(p)) or s[0]]+s[:-1]) if False else LT(s[1:]+[s[0]]),LT([tuple(sorted(x)) if False else (lambda z:(z[1],z[0])+z[2:])(x) for x in s])],f'Áp dụng lần lượt thuật toán "hoán vị kế tiếp": {LT([p]+s)}.',level=3,topic='Hoán vị kế tiếp')
    # ---- tổ hợp kế tiếp
    for _ in range(50):
        n=rng.randint(6,10); k=rng.randint(3,min(6,n-1)); c=tuple(sorted(rng.sample(range(1,n+1),k))); nx=next_comb(c,n)
        if nx is None: continue
        a=list(c); i=k-1
        while i>=0 and a[i]==n-k+i+1: i-=1
        wr={tuple(list(c[:i])+[c[i]+1]+list(c[i+1:])),tuple(list(c[:-1])+[c[-1]+1]) if c[-1]<n else c}
        w2=list(c); w2[i]+=1
        for j in range(i+1,k): w2[j]=w2[j-1]+1
        wr.add(tuple(w2[:i]+[w2[i]+1]+w2[i+1:]) if w2[i]<n else c)
        wr.add(tuple(sorted(rng.sample(range(1,n+1),k)))); wr.add(tuple(sorted(rng.sample(range(1,n+1),k)))); wr.add(tuple(sorted(rng.sample(range(1,n+1),k))))
        wr.discard(nx); wr.discard(c)
        expl=(f'Tổ hợp chập {k} của {{1..{n}}}: {T(c)}. Tìm i lớn nhất mà c[i] ≠ n−k+i = giá trị lớn nhất có thể ở vị trí đó: i = {i+1} (giá trị {c[i]}, tối đa {n-k+i+1}).\nTăng c[{i+1}] lên {c[i]+1}, rồi đặt các phần tử sau nhỏ nhất có thể (c[j] = c[j−1] + 1): {T(nx)}.')
        B.add(f'Sinh tổ hợp chập {k} của {{1,…,{n}}} theo thứ tự từ điển. Tổ hợp liền kề sau {T(c)} là:',T(nx),[T(w) for w in wr],expl,level=2,topic='Tổ hợp kế tiếp')
    for _ in range(35):
        n=9; k=rng.randint(4,7); c=tuple(sorted(rng.sample(range(1,n+1),k))); m=rng.randint(3,6); s=steps(next_comb,c,m,n)
        if len(s)<m: continue
        B.add(f'Cho A = {{1,…,9}}. Sinh các tổ hợp chập {k} theo thứ tự từ điển: {m} tổ hợp liền kề tiếp theo của {T(c)} là:',LT(s),[LT(list(reversed(s))),LT(s[1:]+[s[0]]),LT([tuple(sorted(x[:-1]+(x[-1]-1,))) for x in s])],f'Lần lượt: {LT([c]+s)}.',level=3,topic='Tổ hợp kế tiếp')
    # ---- xâu nhị phân kế tiếp
    for _ in range(45):
        n=rng.randint(5,9); b=tuple(rng.randint(0,1) for _ in range(n)); m=rng.randint(1,4); s=steps(next_bin,b,m)
        if len(s)<m: continue
        v=int(''.join(map(str,b)),2)
        wr=[LT(list(reversed(s))),LT([tuple(1-x for x in t) for t in s]),LT([tuple((v+2*i+2>>(n-1-j))&1 for j in range(n)) if v+2*i+2<2**n else s[i] for i in range(m)]),LT([tuple(int(ch) for ch in format(v-i-1,f'0{n}b')) if v-i-1>=0 else s[i] for i in range(m)])]
        B.add(f'Sinh xâu nhị phân độ dài {n} theo thứ tự từ điển: {m} xâu liền kề sau X = {T(b)} là:',LT(s),wr,f'Xâu kế tiếp = xâu hiện tại + 1 (cộng nhị phân): tìm bit 0 phải nhất, đổi thành 1 và đổi mọi bit sau nó thành 0.\n{LT([b]+s)}. Giá trị thập phân: '+', '.join(str(int(''.join(map(str,t)),2)) for t in [b]+s)+'.',level=1 if m==1 else 2,topic='Xâu nhị phân kế tiếp')
    # ---- thứ hạng (rank) trong thứ tự từ điển
    for _ in range(40):
        n=rng.randint(4,7); p=tuple(rng.sample(range(1,n+1),n)); r=rank_perm(p)
        assert unrank_perm(n,r)==p
        allp=list(itertools.permutations(range(1,n+1))); assert allp.index(p)+1==r
        B.add(f'Hoán vị {T(p)} của {{1..{n}}} đứng ở vị trí thứ mấy trong danh sách các hoán vị theo thứ tự từ điển (bắt đầu từ 1)?',r,near_ints(r,rng,7,lo=1),f'Vị trí = 1 + Σ (số phần tử nhỏ hơn p[i] chưa dùng)·(n−i)!: '+' + '.join(f'{sum(1 for y in p[i+1:] if y<p[i])}·{math.factorial(n-1-i)}!' if False else f'{sum(1 for y in p[i+1:] if y<p[i])}·{n-1-i}!' for i in range(n))+f' + 1 = {r}.',level=3,topic='Thứ hạng hoán vị')
        r2=rng.randint(1,math.factorial(n)); u=unrank_perm(n,r2)
        B.add(f'Hoán vị thứ {r2} (bắt đầu từ 1) trong danh sách theo thứ tự từ điển của các hoán vị của {{1..{n}}} là:',T(u),[T(next_perm(u)) if next_perm(u) else T(unrank_perm(n,1)),T(unrank_perm(n,max(1,r2-1))),T(tuple(reversed(u)))],f'Chia thương liên tiếp cho (n−1)!, (n−2)!, … với r−1 = {r2-1}: chọn phần tử thứ (thương+1) trong các số còn lại ⇒ {T(u)}.',level=3,topic='Thứ hạng hoán vị')
    for _ in range(25):
        n=rng.randint(6,9); k=rng.randint(2,4); c=tuple(sorted(rng.sample(range(1,n+1),k))); r=rank_comb(c,n)
        B.add(f'Xét các tổ hợp chập {k} của {{1..{n}}} liệt kê theo thứ tự từ điển. Tổ hợp {T(c)} đứng thứ mấy?',r,near_ints(r,rng,7,lo=1),f'Đếm số tổ hợp đứng trước: tổng theo từng vị trí các tổ hợp có phần tử nhỏ hơn. Kiểm tra bằng liệt kê: vị trí {r} trong tổng {math.comb(n,k)} tổ hợp.',level=3,topic='Thứ hạng tổ hợp')
    # ---- số lượng còn lại
    for _ in range(25):
        n=rng.randint(4,8); p=tuple(rng.sample(range(1,n+1),n)); r=rank_perm(p); rem=math.factorial(n)-r
        B.add(f'Có bao nhiêu hoán vị của {{1..{n}}} đứng SAU hoán vị {T(p)} trong thứ tự từ điển?',rem,near_ints(rem,rng,6,lo=0),f'Tổng {n}! = {math.factorial(n)} hoán vị; {T(p)} ở vị trí {r} nên có {math.factorial(n)} − {r} = {rem} hoán vị đứng sau.',level=3,topic='Thứ hạng hoán vị')
    # ---- khái niệm
    B.add('Thuật toán sinh (phương pháp sinh) khác quay lui ở chỗ:','chỉ cần cấu hình hiện tại để tính cấu hình kế tiếp',['dùng đệ quy và ngăn xếp để nhớ các lựa chọn','luôn liệt kê theo thứ tự ngược từ điển','không liệt kê được hoán vị'],'Phương pháp sinh xây dựng hàm "cấu hình kế tiếp" từ cấu hình hiện tại theo thứ tự từ điển, không cần đệ quy hay lưu các lựa chọn trước đó.',level=1,topic='Khái niệm')
    B.add('Điều kiện dừng của thuật toán sinh hoán vị kế tiếp là:','phần tử đầu tiên tìm không thấy chỉ số i có p[i] < p[i+1] (hoán vị giảm dần hoàn toàn)',['hoán vị chứa số 1 ở cuối','hoán vị có p[1] = 1','sau đúng n bước'],'Hoán vị cuối cùng trong thứ tự từ điển là (n, n−1, …, 1): giảm dần hoàn toàn, không tồn tại i thỏa p[i] < p[i+1] ⇒ dừng.',level=2,topic='Khái niệm')
    B.add('Hoán vị đầu tiên và cuối cùng của {1,…,n} theo thứ tự từ điển là:','(1, 2, …, n) và (n, …, 2, 1)',['(1, 2, …, n) và (n, 1, …, n−1)','(n, …, 1) và (1, …, n)','(2, 1, …) và (n, …, 1)'],'Thứ tự từ điển: tăng dần là nhỏ nhất, giảm dần là lớn nhất.',level=1,topic='Khái niệm')
    B.add('Độ phức tạp thời gian trung bình của một lần sinh cấu hình kế tiếp (hoán vị) và tổng số cấu hình lần lượt là:','O(n) mỗi lần; n! cấu hình',['O(1) mỗi lần; n! cấu hình','O(n²) mỗi lần; 2ⁿ cấu hình','O(n) mỗi lần; n² cấu hình'],'Mỗi lần sinh cần quét tìm i, j và đảo đoạn cuối: O(n) trong trường hợp xấu nhất; tổng có n! hoán vị nên vét cạn tổng cộng cỡ n·n!.',level=2,topic='Khái niệm')
    return B
def essays(B):
    ex=[('Cho tập A = {1,…,9}. Liệt kê 5 hoán vị liền kề tiếp theo của (3, 1, 4, 5, 8, 6, 2, 9, 10, 7) trên tập {1,…,10}. (dạng đề 2019-2020)','Áp dụng liên tiếp thuật toán hoán vị kế tiếp: '+' → '.join(T(x) for x in [ (3,1,4,5,8,6,2,9,10,7) ]+steps(next_perm,(3,1,4,5,8,6,2,9,10,7),5))),
        ('Cho A = {1,…,9}. Tìm 4 hoán vị liền kề tiếp theo của 568397421 (theo thứ tự từ điển). (đề 2023-2024)','Áp dụng liên tiếp: '+' → '.join(T(x) for x in [ (5,6,8,3,9,7,4,2,1) ]+steps(next_perm,(5,6,8,3,9,7,4,2,1),4))),
        ('Sinh 5 tổ hợp chập 5 liền kề tiếp theo của (2,3,6,8,9) trên tập {1,…,9}. (đề 2023-2024)','Áp dụng liên tiếp: '+' → '.join(T(x) for x in [ (2,3,6,8,9) ]+steps(next_comb,(2,3,6,8,9),5,9))),
        ('Sinh 5 tổ hợp chập 5 liền kề tiếp theo của (1,4,5,7,9) trên {1,…,9}. (đề 2023-2024)','Áp dụng liên tiếp: '+' → '.join(T(x) for x in [ (1,4,5,7,9) ]+steps(next_comb,(1,4,5,7,9),5,9))),
        ('Trình bày thuật toán sinh tổ hợp chập k của {1,…,n} theo thứ tự từ điển và viết hàm C/C++.','Ý tưởng: tìm i lớn nhất sao cho c[i] < n − k + i; tăng c[i] thêm 1; đặt c[j] = c[j−1] + 1 với j > i. Nếu không tìm được i thì đã hết.\n\nbool next_comb(int c[], int k, int n){\n    int i = k;\n    while(i >= 1 && c[i] == n - k + i) i--;\n    if(i == 0) return false;\n    c[i]++;\n    for(int j = i + 1; j <= k; j++) c[j] = c[j-1] + 1;\n    return true;\n}\n// khởi tạo c[i] = i (i = 1..k), gọi do{ in(c); } while(next_comb(c,k,n));'),
        ('Viết chương trình C/C++ liệt kê các hoán vị của {1,…,n} bằng phương pháp sinh theo thứ tự từ điển. (dạng câu 4 đề 2017-2020)','#include <bits/stdc++.h>\nusing namespace std;\nint main(){ int n; cin >> n; vector<int> p(n); iota(p.begin(), p.end(), 1);\n  do { for(int x: p) cout << x << " "; cout << "\\n"; } while(next_permutation(p.begin(), p.end()));\n}\n\nHoặc tự cài: i = n−2; while(i≥0 && p[i]>p[i+1]) i--; nếu i<0 dừng; j = n−1; while(p[j]<p[i]) j--; swap(p[i],p[j]); reverse(p+i+1, p+n).')]
    for q,s in ex: B.essay(q,s,level=3,topic='Phương pháp sinh')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items))
