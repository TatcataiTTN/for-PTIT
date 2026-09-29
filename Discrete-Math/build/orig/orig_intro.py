# Bài tập / ví dụ gốc trong slide chính thức TRR1 (TS. Đào Thị Thuý Quỳnh, PTIT): 0-Intro_en-da-gop.pdf
import itertools, math, random, sys
sys.path.insert(0,'..'); sys.path.insert(0,'.')
import logic_tools as LT
from logic_tools import V,N,A,O,I,E,X
import orig_lib as OL, knap
from qcore import near_ints
from orig_nh2 import TTtxt, TTeq
import gen_m12 as G12
SRC='Slide TRR1 PTIT (TS. Đào Thị Thuý Quỳnh)'
def recs():
    out=[]; rng=random.Random(2024)
    def add(mod,ref,q,ans=None,wrong=(),sol='',lv=2,tp=''):
        out.append(dict(mod=mod,src=f'{SRC} – {ref}',q=q,ans=None if ans is None else str(ans),wrong=[str(w) for w in wrong],sol=sol,level=lv,topic=tp))
    p,q,r,s=V('p'),V('q'),V('r'),V('s')
    # --- Chương 1: tập hợp
    add('m03','Chương 1, Exercise 2','Trong các mệnh đề sau về các tập hợp A, B, C bất kỳ, mệnh đề nào ĐÚNG?','C ⊆ (A ∩ B) ∪ C',['A ⊆ A ∩ B','A ∪ B ⊆ A ∩ B','(A ∪ B) \\ (A ∩ B) = A \\ B'],'• C ⊆ (A ∩ B) ∪ C: đúng vì mọi tập con của hợp chứa C.\n• A ⊆ A ∩ B chỉ đúng khi A ⊆ B (phản ví dụ: A = {1}, B = ∅).\n• A ∪ B ⊆ A ∩ B chỉ đúng khi A = B (phản ví dụ: A = {1}, B = ∅).\n• (A ∪ B) \\ (A ∩ B) = A △ B chứa cả B \\ A nên không bằng A \\ B (phản ví dụ: A = ∅, B = {1}).',2,'Chứng minh tập hợp')
    add('m03','Chương 1, Exercise 2 (mệnh đề 4)','Mệnh đề A ∩ (B ∪ A) = A ∩ B có đúng với mọi tập A, B không? Giải thích.',None,[],'A ∩ (B ∪ A) = A (luật hấp thụ) nên đẳng thức chỉ đúng khi A = A ∩ B, tức A ⊆ B. Phản ví dụ: A = {1}, B = ∅: vế trái = {1}, vế phải = ∅. Vậy mệnh đề KHÔNG đúng với mọi A, B.',2,'Chứng minh tập hợp')
    add('m03','Chương 1, Exercise 3','Cho A = {x ∈ ℤ : x = 4p − 1, p ∈ ℤ} và B = {y ∈ ℤ : y = 4q + 3, q ∈ ℤ}. Chứng minh A = B.',None,[],'(A ⊆ B) x = 4p − 1 = 4(p − 1) + 3 với q = p − 1 ∈ ℤ ⇒ x ∈ B.\n(B ⊆ A) y = 4q + 3 = 4(q + 1) − 1 với p = q + 1 ∈ ℤ ⇒ y ∈ A.\nVậy A = B. ∎',2,'Chứng minh tập hợp')
    add('m03','Chương 1, phần độ phức tạp – Exercise 1','Xác định độ phức tạp của thuật toán sắp xếp nổi bọt: for i = n downto 2: for j = 1 to i − 1: if L[j] > L[j+1] then swap(L[j], L[j+1]).','O(n²)',['O(n)','O(n log n)','O(n³)'],'Số lần so sánh = Σ_{i=2..n} (i − 1) = 1 + 2 + … + (n − 1) = n(n − 1)/2. Mỗi lần so sánh tốn O(1) ⇒ độ phức tạp O(n²) (cả trường hợp xấu nhất và tốt nhất về số phép so sánh).',1,'Đếm phép toán')
    add('m03','Chương 1, phần độ phức tạp – Exercise 2','Xác định độ phức tạp của thuật toán tìm kiếm nhị phân trên danh sách đã sắp xếp (mỗi lần so sánh với phần tử giữa rồi thu hẹp về nửa trái hoặc nửa phải).','O(log n)',['O(n)','O(n log n)','O(1)'],'Mỗi lần gọi đệ quy độ dài đoạn giảm một nửa: T(n) = T(n/2) + O(1) ⇒ T(n) = O(log₂ n). Trường hợp tốt nhất O(1) (phần tử ở giữa).',1,'Đếm phép toán')
    # --- Chương 1: logic
    add('m01','Chương 1, Exercise 3','Chứng minh các tương đương logic: (1) p ⇔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q); (2) ¬p ⇔ q ≡ p ⇔ ¬q; (3) ¬(p ⇔ q) ≡ ¬p ⇔ q.',None,[],'(1) '+TTeq(E(p,q),O(A(p,q),A(N(p),N(q))))+'\n(2) '+TTeq(E(N(p),q),E(p,N(q)))+'\n(3) '+TTeq(N(E(p,q)),E(N(p),q))+'\nTrong cả ba bảng hai cột cuối trùng nhau trên mọi dòng ⇒ các tương đương đúng. ∎',2,'Chứng minh logic')
    f=O(I(p,q),N(O(r,N(s))))
    cnf=A(O(O(N(p),q),N(r)),O(O(N(p),q),s)); assert LT.equiv(f,cnf)
    add('m01','Chương 1, Exercise 4','Đưa công thức (p ⇒ q) ∨ ¬(r ∨ ¬s) về dạng hội chuẩn (CNF).','(¬p ∨ q ∨ ¬r) ∧ (¬p ∨ q ∨ s)',['(¬p ∨ q) ∧ (¬r ∨ s)','(p ∨ ¬q ∨ ¬r) ∧ (p ∨ ¬q ∨ s)','(¬p ∧ q) ∨ (¬r ∧ s)'],'(p ⇒ q) ∨ ¬(r ∨ ¬s) ≡ (¬p ∨ q) ∨ (¬r ∧ s)   (P ⇒ Q ≡ ¬P ∨ Q; De Morgan)\n≡ [(¬p ∨ q) ∨ ¬r] ∧ [(¬p ∨ q) ∨ s]   (phân phối ∨ qua ∧)\n= (¬p ∨ q ∨ ¬r) ∧ (¬p ∨ q ∨ s). (Đã kiểm chứng bằng bảng chân trị 16 dòng.)',3,'Dạng chuẩn tắc')
    # --- Chương 2 đếm
    ans=math.factorial(5)-2*math.factorial(4)
    assert ans==sum(1 for pm in itertools.permutations('ABCDE') if abs(pm.index('A')-pm.index('B'))!=1)
    add('m05','Chương 2 (Return to subproblem) – Exercise 1','Có bao nhiêu cách xếp 5 người A, B, C, D, E thành một hàng ngang sao cho A không đứng cạnh B?',ans,[120,48,96,24],'Phần bù: tổng 5! = 120; số cách A cạnh B: gộp thành một khối, 4! = 24 cách sắp và 2 cách đổi chỗ: 48. Đáp án 120 − 48 = 72. (Đã kiểm chứng bằng liệt kê 120 hoán vị.)',2,'Hoán vị')
    same=90000-9*9*8*7*6; assert same==sum(1 for n in range(10000,100000) if len(set(str(n)))<5)
    add('m04','Chương 2 (Return to subproblem) – Exercise 2','Tính số các số tự nhiên có 5 chữ số sao cho có ít nhất 2 chữ số giống nhau.',same,[90000,27216,90000-9*9*8*7,9*10**4-9*9*8*7*6+1],'Phần bù: số có 5 chữ số đôi một khác nhau = 9·9·8·7·6 = 27216 (chữ số đầu ≠ 0). Tổng số có 5 chữ số: 90000. Đáp án 90000 − 27216 = 62784. (Kiểm chứng bằng liệt kê.)',2,'Quy tắc phần bù')
    add('m05','Chương 2 (Counting), Example 13','Trong các số tự nhiên 7 chữ số, đếm số các số thuận nghịch có tổng các chữ số bằng 18.',OL.pal_count(7,18),near_ints(OL.pal_count(7,18),rng,4,lo=1),'Số thuận nghịch 7 chữ số xác định bởi 4 chữ số đầu x₁x₂x₃x₄ (x₁ ≥ 1); tổng chữ số = 2(x₁+x₂+x₃) + x₄ = 18. Đếm nghiệm 0 ≤ xᵢ ≤ 9 (x₁ ≥ 1): '+str(OL.pal_count(7,18))+' (kiểm chứng bằng liệt kê).',3,'Số thuận nghịch')
    add('m04','Chương 2 (Counting) – Exercise 1','Mỗi vé số có 2 phần: phần chữ gồm 2 chữ cái A–Z, phần số gồm 4 chữ số 0–9. Mỗi kỳ có 1 giải đặc biệt, 2 giải nhất, 5 giải nhì, 10 giải ba. Tính xác suất một vé trúng ít nhất một giải trong hai trường hợp: (a) phần chữ đứng trước phần số; (b) phần chữ đứng ở vị trí tùy ý.',None,[],'(a) Số vé có thể: 26²·10⁴ = 6 760 000; số giải 1 + 2 + 5 + 10 = 18 (mỗi giải ứng một vé khác nhau) ⇒ xác suất = 18/6 760 000 ≈ 2,66·10⁻⁶.\n(b) Chọn 2 vị trí cho chữ cái trong 6 vị trí: C(6,2) = 15 ⇒ số vé = 15·6 760 000 = 101 400 000 ⇒ xác suất = 18/101 400 000 ≈ 1,78·10⁻⁷.',3,'Quy tắc nhân')
    add('m04','Chương 2 (Counting) – Exercise 2','Tính số trận đấu của một kỳ World Cup 32 đội (8 bảng, mỗi bảng 4 đội đá vòng tròn một lượt, sau đó loại trực tiếp có trận tranh hạng ba).',64,[48,63,56,32],'Vòng bảng: 8·C(4,2) = 8·6 = 48 trận. Loại trực tiếp: vòng 16 đội 8 trận, tứ kết 4, bán kết 2, tranh hạng ba 1, chung kết 1: 16 trận. Tổng 48 + 16 = 64 trận.',1,'Quy tắc cộng')
    add('m05','Chương 2 (Counting) – Exercise 3','Lưới có các cột đánh số 0..m (trái sang phải) và các hàng 0..n (dưới lên trên). Có bao nhiêu cách đi từ (0,0) đến (n,m) chỉ theo cạnh ô, từ trái sang phải và từ dưới lên trên?','C(n+m, n)',['n·m','C(n+m, n) − 1','(n+m)!'],'Cần đi m bước sang phải và n bước lên trên; mỗi cách là một dãy n+m bước, chọn n vị trí cho bước “lên”: C(n+m, n). Ví dụ n = 3, m = 4: C(7,3) = 35.',2,'Tổ hợp ứng dụng')
    # --- Chương 2: hàm sinh
    # Example 24: táo chẵn, chuối lẻ, cam <=4, lê >=2
    def poly(pred,N):
        return [1 if pred(e) else 0 for e in range(N+1)]
    def mul(a,b,N):
        r=[0]*(N+1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if i+j<=N: r[i+j]+=x*y
        return r
    Nn=10
    g=[1]+[0]*Nn
    for pr in (lambda e:e%2==0,lambda e:e%2==1,lambda e:e<=4,lambda e:e>=2): g=mul(g,poly(pr,Nn),Nn)
    cnt=sum(1 for a in range(0,Nn+1) for b in range(0,Nn+1) for c in range(0,Nn+1) for d in range(0,Nn+1) if a+b+c+d==Nn and a%2==0 and b%2==1 and c<=4 and d>=2)
    assert cnt==g[Nn]
    add('m09','Chương 2 (Generating function), Example 24','Có bao nhiêu cách chọn n quả từ 4 loại (táo, chuối, cam, đào) sao cho số táo là số chẵn, số chuối là số lẻ, số cam không quá 4 và số đào ít nhất 2? Xây dựng hàm sinh rồi tính số cách với n = 10.',cnt,near_ints(cnt,rng,5,lo=1),'Hàm sinh: (1 + x² + x⁴ + …)(x + x³ + x⁵ + …)(1 + x + x² + x³ + x⁴)(x² + x³ + x⁴ + …) = [1/(1 − x²)]·[x/(1 − x²)]·[(1 − x⁵)/(1 − x)]·[x²/(1 − x)].\nSố cách chọn n quả là hệ số của xⁿ. Với n = 10 ta được '+str(cnt)+' (kiểm chứng bằng liệt kê trực tiếp).',3,'Hàm sinh & đếm')
    dp=[1]+[0]*100
    for c in (1,5,10,50):
        for v in range(c,101): dp[v]+=dp[v-c]
    add('m09','Chương 2 (Generating function), Exercise 1','Tìm hàm sinh cho số cách đổi M (nghìn đồng) bằng các tờ 1, 5, 10, 50 nghìn (không hạn chế số tờ). Tính số cách đổi 100 nghìn.',dp[100],near_ints(dp[100],rng,5,lo=1),'Hàm sinh theo đơn vị nghìn đồng: 1/[(1 − x)(1 − x⁵)(1 − x¹⁰)(1 − x⁵⁰)]; số cách đổi M là hệ số của x^M. Với M = 100 quy hoạch động cho '+str(dp[100])+' cách.',3,'Đổi tiền')
    # --- Chương 3 liệt kê
    AA=(5,10,15,20,25,30,35)
    subs=[c for c in itertools.combinations(AA,3) if sum(c)==50]
    add('m10','Chương 3, Exercise 6','Cho dãy A = (5, 10, 15, 20, 25, 30, 35), n = 7, k = 3, P = 50. Liệt kê các tập con k phần tử có tổng đúng P.',' ; '.join('('+', '.join(map(str,c))+')' for c in subs),[],'Duyệt các tổ hợp chập 3 của 7 phần tử (theo thứ tự chỉ số tăng) và giữ các tập có tổng 50: '+' ; '.join('('+', '.join(map(str,c))+')' for c in subs)+f'. Có {len(subs)} tập. (Có thể dùng sinh tổ hợp hoặc quay lui có cắt nhánh khi tổng vượt P.)',3,'Sinh / quay lui')
    inc=[c for c in itertools.combinations((1,3,2,4,5),3) if c[0]<c[1]<c[2]]
    add('m10','Chương 3, Exercise 7','Cho dãy A = (1, 3, 2, 4, 5), n = 5, k = 3. Liệt kê các dãy con 3 phần tử theo thứ tự tăng dần (giữ nguyên thứ tự vị trí).',' ; '.join('('+', '.join(map(str,c))+')' for c in inc),[],'Sinh các tổ hợp chập 3 của chỉ số 1..5, lấy phần tử tương ứng và chỉ giữ dãy tăng ngặt: '+' ; '.join('('+', '.join(map(str,c))+')' for c in inc)+f'. Có {len(inc)} dãy con.',3,'Sinh / quay lui')
    add('m11','Chương 3, Exercise 9','Dùng quay lui liệt kê mọi phần tử của D = {X = (x₁,…,x_n) : Σ aᵢxᵢ ≤ W và Σ cᵢxᵢ = K}, với xᵢ ∈ {0,1}, aᵢ, cᵢ nguyên dương, n ≤ 100, W ≤ 32000, K ≤ 32000.',None,[],'Try(i, w, c): với v = 0, 1: nếu w + aᵢ·v ≤ W (chấp nhận trọng lượng) và c + cᵢ·v ≤ K (không vượt K): gán x[i] = v; nếu i = n và c + cᵢ·v = K thì in nghiệm; ngược lại Try(i+1, w + aᵢ·v, c + cᵢ·v). Cắt nhánh thêm nếu c + Σ_{j>i} cⱼ < K (không thể đạt K). Gọi Try(1, 0, 0). Độ phức tạp xấu nhất O(2ⁿ) nhưng cắt nhánh giảm mạnh.',3,'Quay lui')
    add('m11','Chương 3, Exercise 10','Dùng quay lui liệt kê mọi phần tử của D = {X = (x₁,…,x_n) : Σ xᵢ = K và Σ aᵢxᵢ = S}, xᵢ ∈ {0,1}, aᵢ nguyên dương, n ≤ 100, K ≤ 100, S ≤ 32000.',None,[],'Try(i, cnt, sum): với v = 0, 1: cnt′ = cnt + v, sum′ = sum + aᵢ·v; cắt nhánh nếu cnt′ > K hoặc sum′ > S hoặc cnt′ + (n − i) < K (không đủ phần tử để chọn đủ K). Khi i = n: in nghiệm nếu cnt′ = K và sum′ = S. Gọi Try(1, 0, 0). Đây là bài liệt kê tập con K phần tử có tổng S.',3,'Quay lui')
    # --- Chương 4
    for (v,w,b,ref) in [([7,4,2],[4,3,2],6,'Chương 4, Exercise 1'),([5,1,8,1],[4,2,7,1],9,'Chương 4, Exercise 2')]:
        best,bx,feas=knap.brute(v,w,b); res=knap.bb(v,w,b); assert res['fopt']==best
        def lin(cs): return ' + '.join((str(c) if c!=1 else '')+f'x{OL.sub(i+1)}' for i,c in enumerate(cs))
        add('m12',ref,f'Áp dụng thuật toán nhánh cận giải bài toán cái túi, chỉ rõ kết quả theo mỗi bước: {lin(v)} → max; {lin(w)} ≤ {b}; xⱼ ∈ {{0,1}}.',None,[],G12.trace_text(v,w,b,res),3,'Nhánh cận cái túi')
        add('m12',ref+' (chuyển thành trắc nghiệm)',f'Cái túi: {lin(v)} → max; {lin(w)} ≤ {b}; xⱼ ∈ {{0,1}}. Giá trị tối ưu f* bằng:',best,[best+d for d in (-2,-1,1,2,3) if best+d>=0][:4],G12.trace_text(v,w,b,res),2,'Giá trị tối ưu')
    return out
