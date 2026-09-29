from qcore import *
import itertools, math
def sub(n): return ''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(n))
def seq_brute(pred,alpha,N):
    out={}
    for n in range(1,N+1): out[n]=sum(1 for s in itertools.product(alpha,repeat=n) if pred(s))
    return out
def has_run(s,ch,k): 
    r=0
    for c in s:
        r=r+1 if c==ch else 0
        if r>=k: return True
    return False
def sv(fn,a,n):
    try: return fn(a,n)
    except Exception: return None
def fam_list():
    F=[]
    for k in (2,3,4):
        F.append(dict(name=f'xâu nhị phân độ dài n KHÔNG chứa {k} bit 1 liên tiếp',alpha='01',pred=lambda s,k=k:not has_run(s,'1',k),N=11,
            true=(lambda a,n,k=k:sum(a[n-i] for i in range(1,k+1)),f'aₙ = '+' + '.join(f'aₙ₋{sub(i)}' for i in range(1,k+1))),
            cands=[(f'aₙ = '+' + '.join(f'aₙ₋{sub(i)}' for i in range(1,k+1)),lambda a,n,k=k:sum(a[n-i] for i in range(1,k+1))),
                   ('aₙ = 2aₙ₋₁',lambda a,n:2*a[n-1]),(f'aₙ = aₙ₋₁ + aₙ₋₂ + 2ⁿ⁻²' ,lambda a,n:a[n-1]+a[n-2]+2**(n-2)),
                   (f'aₙ = 2aₙ₋₁ − aₙ₋{sub(k+1)}',lambda a,n,k=k:2*a[n-1]-a[n-k-1] if n-k-1>=1 else None),('aₙ = aₙ₋₁ + aₙ₋₂',lambda a,n:a[n-1]+a[n-2]),('aₙ = aₙ₋₁ + aₙ₋₂ + aₙ₋₃ + aₙ₋₄',lambda a,n:sum(a[n-i] for i in range(1,5)) if n>4 else None)],init=k))
    for k in (2,3,4):
        F.append(dict(name=f'xâu nhị phân độ dài n CÓ chứa {k} bit 1 liên tiếp',alpha='01',pred=lambda s,k=k:has_run(s,'1',k),N=11,
            cands=[(f'aₙ = '+' + '.join(f'aₙ₋{sub(i)}' for i in range(1,k+1))+f' + 2ⁿ⁻{sub(k) if False else k}',lambda a,n,k=k:sum(a[n-i] for i in range(1,k+1))+2**(n-k)),
                   (f'aₙ = '+' + '.join(f'aₙ₋{sub(i)}' for i in range(1,k+1)),lambda a,n,k=k:sum(a[n-i] for i in range(1,k+1))),
                   ('aₙ = 2aₙ₋₁ + 1',lambda a,n:2*a[n-1]+1),(f'aₙ = 2aₙ₋₁ + 2ⁿ⁻¹ − aₙ₋{sub(k)}',lambda a,n,k=k:2*a[n-1]+2**(n-1)-a[n-k] if n-k>=1 else None),
                   (f'aₙ = 2aₙ₋₁ + aₙ₋{sub(k)}',lambda a,n,k=k:2*a[n-1]+a[n-k] if n-k>=1 else None),(f'aₙ = aₙ₋₁ + 2ⁿ⁻¹',lambda a,n:a[n-1]+2**(n-1))],init=k))
    F.append(dict(name='xâu nhị phân độ dài n KHÔNG chứa hai bit 0 liên tiếp',alpha='01',pred=lambda s:not has_run(s,'0',2),N=11,cands=[('aₙ = aₙ₋₁ + aₙ₋₂',lambda a,n:a[n-1]+a[n-2]),('aₙ = 2aₙ₋₁',lambda a,n:2*a[n-1]),('aₙ = aₙ₋₁ + 2aₙ₋₂',lambda a,n:a[n-1]+2*a[n-2]),('aₙ = 2aₙ₋₁ − 1',lambda a,n:2*a[n-1]-1),('aₙ = aₙ₋₁ + aₙ₋₂ + 1',lambda a,n:a[n-1]+a[n-2]+1)],init=2))
    F.append(dict(name='xâu tam phân (chữ số 0,1,2) độ dài n KHÔNG chứa hai chữ số 0 liên tiếp',alpha='012',pred=lambda s:not has_run(s,'0',2),N=9,cands=[('aₙ = 2aₙ₋₁ + 2aₙ₋₂',lambda a,n:2*a[n-1]+2*a[n-2]),('aₙ = 2aₙ₋₁ + aₙ₋₂',lambda a,n:2*a[n-1]+a[n-2]),('aₙ = 3aₙ₋₁ − aₙ₋₂',lambda a,n:3*a[n-1]-a[n-2]),('aₙ = 3aₙ₋₁',lambda a,n:3*a[n-1]),('aₙ = aₙ₋₁ + aₙ₋₂',lambda a,n:a[n-1]+a[n-2])],init=2))
    F.append(dict(name='xâu nhị phân độ dài n có SỐ CHẴN bit 0',alpha='01',pred=lambda s:s.count('0')%2==0,N=11,cands=[('aₙ = 2aₙ₋₁',lambda a,n:2*a[n-1]),('aₙ = 2aₙ₋₁ + 1',lambda a,n:2*a[n-1]+1),('aₙ = aₙ₋₁ + aₙ₋₂',lambda a,n:a[n-1]+a[n-2]),('aₙ = 2ⁿ − aₙ₋₁',lambda a,n:2**n-a[n-1]),('aₙ = 2ⁿ⁻¹ − aₙ₋₁',lambda a,n:2**(n-1)-a[n-1])],init=1))
    F.append(dict(name='xâu nhị phân độ dài n BẮT ĐẦU bằng 1 và CÓ chứa hai bit 0 liên tiếp',alpha='01',pred=lambda s:s[0]=='1' and has_run(s,'0',2),N=11,cands=[('aₙ = aₙ₋₁ + aₙ₋₂ + 2ⁿ⁻³',lambda a,n:a[n-1]+a[n-2]+2**(n-3)),('aₙ = aₙ₋₁ + aₙ₋₂ + 2ⁿ⁻²',lambda a,n:a[n-1]+a[n-2]+2**(n-2)),('aₙ = 2aₙ₋₁ + 2ⁿ⁻³',lambda a,n:2*a[n-1]+2**(n-3)),('aₙ = aₙ₋₁ + aₙ₋₂',lambda a,n:a[n-1]+a[n-2]),('aₙ = aₙ₋₁ + aₙ₋₂ + aₙ₋₃',lambda a,n:a[n-1]+a[n-2]+a[n-3] if n>3 else None)],init=3))
    F.append(dict(name='xâu nhị phân độ dài n có ĐÚNG hai bit 0 liên tiếp ở đầu hoặc không có hai bit 0 liên tiếp (tức KHÔNG có "00" ở vị trí ≥ 2)',alpha='01',pred=lambda s:not has_run(s[1:],'0',2),N=11,cands=[('aₙ = aₙ₋₁ + aₙ₋₂ với n ≥ 4',lambda a,n:a[n-1]+a[n-2] if n>=4 else None)],init=3,skip=True))
    return F
def gen(seed=7):
    B=Bank('m07',seed); rng=B.rng
    fams=[f for f in fam_list() if not f.get('skip')]
    for f in fams:
        a=seq_brute(f['pred'],f['alpha'],f['N']); f['a']=a
        good=[];bad=[]
        for txt,fn in f['cands']:
            ok=True;start=f['init']+1
            for n in range(start,f['N']+1):
                v=sv(fn,a,n)
                if v is None: continue
                if v!=a[n]: ok=False;break
            (good if ok else bad).append(txt)
        assert good and good[0]==f['cands'][0][0],(f['name'],good)
        f['good']=good[0];f['bad']=bad;f['cands']=[c for c in f['cands'] if c[0]==good[0] or c[0] in bad]
        ini=', '.join(f'a{sub(i)} = {a[i]}' for i in range(1,f['init']+1))
        f['ini']=ini
        # T1 chọn hệ thức truy hồi
        for variant in range(3):
            stem=[f'Gọi aₙ là số {f["name"]}. Hệ thức truy hồi đúng của aₙ (với n đủ lớn) là:',
                  f'Đếm {f["name"]}. Chọn hệ thức truy hồi thỏa mãn:',f'Lập hệ thức truy hồi cho aₙ = số {f["name"]}:'][variant]
            expl=f'Với {f["name"]}: các giá trị đếm trực tiếp (liệt kê) là '+', '.join(f'a{sub(i)}={a[i]}' for i in range(1,8))+f'.\nHệ thức đúng: {f["good"]}.'
            expl+='\nCác phương án khác sai vì thay giá trị đếm trực tiếp vào thì lệch: '+'; '.join(f'"{b}" cho '+(lambda fn: (lambda n:f'a{sub(n)}={sv(fn,a,n)} ≠ {a[n]}')(next(n for n in range(f["init"]+1,f["N"]+1) if sv(fn,a,n) is not None and sv(fn,a,n)!=a[n])))(dict(f['cands'])[b]) for b in f['bad'][:3])+'.'
            B.add(stem,f['good'],rng.sample(f['bad'],min(3,len(f['bad']))) if len(f['bad'])>=3 else f['bad'],expl,level=3 if 'CÓ' in f['name'] or 'chứa' in f['name'] else 2,topic='Lập hệ thức truy hồi')
        # T2 tính a_n
        for n in range(4,f['N']+1):
            v=a[n]
            B.add(f'Gọi aₙ là số {f["name"]}. Giá trị a{sub(n)} là:',v,near_ints(v,rng,6,lo=0)+[v*2 if v else 4,v+f['a'][n-1]],f'Điều kiện đầu: {ini}. Dùng hệ thức {f["good"]} để tính tiếp: '+', '.join(f'a{sub(i)}={a[i]}' for i in range(f['init']+1,n+1))+f'. Vậy a{sub(n)} = {v}.\n(Kiểm chứng bằng liệt kê tất cả xâu độ dài {n}.)',level=2,topic='Tính số hạng')
        # T3 điều kiện đầu
        wr=[ ', '.join(f'a{sub(i)} = {a[i]+d}' if i==f['init'] else f'a{sub(i)} = {a[i]}' for i in range(1,f['init']+1)) for d in (1,-1,2)]
        B.add(f'Với aₙ là số {f["name"]}, điều kiện đầu đúng là:',ini,wr,f'Đếm trực tiếp các xâu độ dài nhỏ ta được {ini}. Điều kiện đầu phải đủ để tính các số hạng tiếp theo: hệ thức trên cần {f["init"]} số hạng đầu.',level=2,topic='Điều kiện đầu')
    # --- các bài toán truy hồi kinh điển
    for steps in [(1,2),(1,2,3),(1,3),(2,3),(1,2,4)]:
        m=max(steps); a={0:1}
        for n in range(1,15): a[n]=sum(a[n-s] for s in steps if n-s>=0)
        rec=' + '.join(f'aₙ₋{sub(s)}' for s in steps); wrong=[' + '.join(f'aₙ₋{sub(s+1)}' for s in steps),'aₙ = 2aₙ₋₁'.replace('aₙ = ',''),' + '.join(f'aₙ₋{sub(s)}' for s in steps[:-1]),rec+' + 1']
        B.add(f'Một người leo cầu thang n bậc, mỗi bước leo được {" hoặc ".join(map(str,steps))} bậc. Gọi aₙ là số cách leo. Hệ thức truy hồi đúng là:',f'aₙ = {rec}',[f'aₙ = {w}' for w in wrong],f'Bước CUỐI cùng leo {" hoặc ".join(map(str,steps))} bậc nên aₙ = '+' + '.join(f'aₙ₋{sub(s)}' for s in steps)+f' (quy tắc cộng). Điều kiện đầu a₀ = 1.',level=2,topic='Bài toán cổ điển')
        for n in (5,7,9,10,12):
            B.add(f'Leo cầu thang n bậc, mỗi bước leo {" hoặc ".join(map(str,steps))} bậc. Số cách leo lên bậc thứ {n} là:',a[n],near_ints(a[n],rng,6,lo=1),f'aₙ = {rec}, a₀ = 1 (và aₖ = 0 với k < 0). Tính lần lượt: '+', '.join(f'a{sub(i)}={a[i]}' for i in range(0,n+1))+'.',level=2,topic='Bài toán cổ điển')
    H={1:1}
    for n in range(2,16): H[n]=2*H[n-1]+1
    for n in range(3,13): B.add(f'Tháp Hà Nội với {n} đĩa cần tối thiểu bao nhiêu lần chuyển đĩa?',H[n],[2**n,2**(n-1),n*n,2*H[n]+1],f'Hₙ = 2Hₙ₋₁ + 1, H₁ = 1 ⇒ Hₙ = 2ⁿ − 1 = {H[n]}: chuyển n−1 đĩa trên, chuyển đĩa lớn, rồi chuyển n−1 đĩa lại.',level=2,topic='Bài toán cổ điển')
    B.add('Hệ thức truy hồi của số cách chuyển tối thiểu Hₙ trong bài toán Tháp Hà Nội là:','Hₙ = 2Hₙ₋₁ + 1, H₁ = 1',['Hₙ = Hₙ₋₁ + Hₙ₋₂, H₁ = H₂ = 1','Hₙ = 2Hₙ₋₁, H₁ = 1','Hₙ = Hₙ₋₁ + 2, H₁ = 1'],'Chuyển n−1 đĩa nhỏ sang cọc phụ (Hₙ₋₁), chuyển đĩa lớn (1), chuyển n−1 đĩa về (Hₙ₋₁).',level=1,topic='Bài toán cổ điển')
    D={1:0,2:1}
    for n in range(3,12): D[n]=(n-1)*(D[n-1]+D[n-2])
    for n in range(3,11):
        cnt=sum(1 for p in itertools.permutations(range(n)) if all(p[i]!=i for i in range(n))) if n<=8 else D[n]
        assert cnt==D[n]
        B.add(f'Số hoán vị mất thứ tự (không có phần tử nào ở đúng vị trí ban đầu) của {n} phần tử là:',D[n],near_ints(D[n],rng,6,lo=0)+[math.factorial(n)-D[n]],f'Dₙ = (n−1)(Dₙ₋₁ + Dₙ₋₂), D₁ = 0, D₂ = 1 ⇒ '+', '.join(f'D{sub(i)}={D[i]}' for i in range(1,n+1))+'.',level=3,topic='Bài toán cổ điển')
    for n in range(2,14):
        L=1+n*(n+1)//2
        B.add(f'{n} đường thẳng đôi một cắt nhau và không có 3 đường đồng quy chia mặt phẳng thành nhiều nhất bao nhiêu miền?',L,[L-1,L+1,2**n,n*n],f'Lₙ = Lₙ₋₁ + n, L₀ = 1 (đường thứ n cắt n−1 đường trước tại n−1 điểm, chia n phần, thêm n miền) ⇒ Lₙ = 1 + n(n+1)/2 = {L}.',level=2,topic='Bài toán cổ điển')
    for n in range(2,13):
        h=n*(n-1)//2
        B.add(f'Trong một nhóm {n} người, mỗi cặp bắt tay đúng một lần. Số cái bắt tay hₙ thỏa hệ thức nào và bằng bao nhiêu?',f'hₙ = hₙ₋₁ + (n−1), h{sub(n)} = {h}',[f'hₙ = hₙ₋₁ + n, h{sub(n)} = {h+n}',f'hₙ = 2hₙ₋₁, h{sub(n)} = {2**(n-1)}',f'hₙ = hₙ₋₁ + (n−1), h{sub(n)} = {h+1}'],f'Người thứ n bắt tay n−1 người trước đó nên hₙ = hₙ₋₁ + (n−1) ⇒ hₙ = n(n−1)/2 = {h}.',level=2,topic='Bài toán cổ điển')
    for r in (3,4,5,6,8,10):
        for P0 in (1000,5000,10000):
            n=rng.randint(3,10)
            v=P0*(1+r/100)**n
            B.add(f'Gửi {P0} (triệu đồng) lãi kép {r}%/năm. Gọi Pₙ là số tiền sau n năm. Hệ thức đúng và P{sub(n)} xấp xỉ:',f'Pₙ = {1+r/100:g}·Pₙ₋₁; P{sub(n)} ≈ {v:,.0f}',[f'Pₙ = Pₙ₋₁ + {r/100:g}; P{sub(n)} ≈ {P0*(1+r/100*n):,.0f}',f'Pₙ = {r/100:g}·Pₙ₋₁; P{sub(n)} ≈ {P0*(r/100)**n:,.4f}',f'Pₙ = {1+r/100:g}·Pₙ₋₁; P{sub(n)} ≈ {P0*(1+r/100*n):,.0f}'],f'Sau mỗi năm số tiền nhân với {1+r/100:g}: Pₙ = {1+r/100:g}Pₙ₋₁, P₀ = {P0} ⇒ Pₙ = {P0}·{1+r/100:g}^n ≈ {v:,.0f}. (Lãi đơn cho {P0*(1+r/100*n):,.0f}.)',level=2,topic='Bài toán cổ điển')
    return B
def essays(B):
    ex=[('Tìm hệ thức truy hồi và điều kiện đầu để đếm số xâu nhị phân độ dài n chứa ba bit 1 liên tiếp. Tính a₅. (đề 2019-2020)','Chia theo dạng: xâu KHÔNG chứa 111 (đếm bởi bₙ = bₙ₋₁+bₙ₋₂+bₙ₋₃, b₁=2, b₂=4, b₃=7) và tổng 2ⁿ. aₙ = 2ⁿ − bₙ.\nHoặc trực tiếp: aₙ = aₙ₋₁ + aₙ₋₂ + aₙ₋₃ + 2ⁿ⁻³ với a₁ = a₂ = 0, a₃ = 1.\nTính: a₄ = 1+0+0+2 = 3? Kiểm tra: 1111,1110,0111 = 3 ✓. Rồi a₅ = 3+1+0+4 = 8. Đáp án a₅ = 8.'),
        ('Tìm hệ thức truy hồi cho số xâu nhị phân độ dài n KHÔNG chứa hai bit 0 liên tiếp và tính a₆.','Xâu hợp lệ kết thúc bằng 1: ghép bit 1 vào xâu hợp lệ độ dài n−1 ⇒ aₙ₋₁. Kết thúc bằng 0: bit trước phải là 1 ⇒ ghép "10" vào xâu hợp lệ độ dài n−2 ⇒ aₙ₋₂. Vậy aₙ = aₙ₋₁ + aₙ₋₂, a₁ = 2, a₂ = 3 ⇒ a₃=5, a₄=8, a₅=13, a₆=21.'),
        ('Một từ mã hợp lệ là xâu chữ số thập phân chứa số lẻ chữ số 6. Gọi aₙ là số từ mã hợp lệ độ dài n. Tìm hệ thức truy hồi, điều kiện đầu và tính a₅. (đề 2017-2018)','Gọi bₙ là số xâu độ dài n có số CHẴN chữ số 6; aₙ + bₙ = 10ⁿ.\nThêm ký tự cuối: nếu là 6 (1 cách) thì đổi tính chẵn lẻ; nếu khác 6 (9 cách) giữ nguyên: aₙ = 9aₙ₋₁ + bₙ₋₁ = 9aₙ₋₁ + (10ⁿ⁻¹ − aₙ₋₁) = 8aₙ₋₁ + 10ⁿ⁻¹, a₁ = 1.\nTính: a₂ = 8+10 = 18, a₃ = 144+100 = 244, a₄ = 1952+1000 = 2952, a₅ = 23616+10000 = 33616.'),
        ('Chứng minh số cách xếp gạch domino 2×1 lát kín hình chữ nhật 2×n thỏa aₙ = aₙ₋₁ + aₙ₋₂ và tính a₈.','Ô góc trái: đặt domino đứng (còn 2×(n−1): aₙ₋₁) hoặc hai domino ngang chồng nhau (còn 2×(n−2): aₙ₋₂). a₁ = 1, a₂ = 2 ⇒ a₃=3, a₄=5, a₅=8, a₆=13, a₇=21, a₈=34.'),
        ('Xây dựng hệ thức truy hồi cho số hoán vị mất thứ tự Dₙ và tính D₆.','Dₙ = (n−1)(Dₙ₋₁ + Dₙ₋₂), D₁=0, D₂=1: D₃=2, D₄=9, D₅=44, D₆=265.'),
        ('Tìm hệ thức truy hồi cho số cách phủ dải 1×n bằng các miếng 1×1 (đỏ hoặc xanh) và 1×2 (một màu).','Ô cuối: miếng 1×1 (2 màu): 2aₙ₋₁; hoặc miếng 1×2: aₙ₋₂. aₙ = 2aₙ₋₁ + aₙ₋₂, a₀ = 1, a₁ = 2.')]
    for q,s in ex: B.essay(q,s,level=3,topic='Lập hệ thức truy hồi')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items)); import collections; print(collections.Counter(i['topic'] for i in B.items))
