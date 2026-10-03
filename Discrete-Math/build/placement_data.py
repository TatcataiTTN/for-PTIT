# Ngân hàng kiểm tra đầu vào: mỗi kỹ năng nhiều câu; đáp án TÍNH bằng code (assert), không gõ tay.
import math, itertools
from math import comb, factorial as F, gcd
def Q(stem,ans,wrong,expl):
    ws=[]
    for w in wrong:
        w=str(w)
        if w!=str(ans) and w not in ws: ws.append(w)
    if len(ws)<3 and str(ans).lstrip('-').isdigit():
        a=int(ans)
        for d in (1,-1,2,-2,10,-10,3):
            c=str(a+d)
            if c!=str(ans) and c not in ws and len(ws)<3: ws.append(c)
    assert len(ws)>=3,(stem,ws)
    return dict(q=stem,ans=str(ans),wrong=ws[:3],expl=expl)
SK=[]
def sk(id,name,mods,refresh,qs): SK.append(dict(id=id,name=name,mods=mods,refresh=refresh,qs=qs))
# 1 Logic
def imp(p,q): return (not p) or q
tt=lambda f:[f(p,q) for p in (1,0) for q in (1,0)]
def tv(f): return ''.join('ĐS'[0 if v else 1] for v in f)
logic=[]
logic.append(Q('Mệnh đề p → q sai khi nào?','p đúng, q sai',['p sai, q đúng','p sai, q sai','p đúng, q đúng'],'p → q chỉ sai khi vế trước đúng mà vế sau sai.'))
logic.append(Q('Phủ định của “mọi số nguyên tố đều lẻ” là:','tồn tại số nguyên tố chẵn',['mọi số nguyên tố đều chẵn','không có số nguyên tố nào lẻ','tồn tại số nguyên tố lẻ'],'¬∀x P(x) ≡ ∃x ¬P(x): tồn tại số nguyên tố không lẻ, tức là chẵn.'))
assert all(imp(p,q)==((not q) <= (not p) if False else imp(not q,not p)) for p in (0,1) for q in (0,1))
logic.append(Q('Mệnh đề nào tương đương với p → q?','¬q → ¬p',['q → p','¬p → ¬q','p ∧ ¬q'],'Phản đảo: p → q ≡ ¬q → ¬p. Mệnh đề đảo q → p và mệnh đề ngược ¬p → ¬q không tương đương.'))
n=sum(1 for p in (0,1) for q in (0,1) if (p or q) and not (p and q))
logic.append(Q('Số hàng có giá trị Đúng trong bảng chân lý của p ⊕ q (XOR) là:',n,[1,3,4],'p ⊕ q đúng khi p, q khác nhau: 2 trong 4 hàng.'))
taut=all(((not(p and q)) == ((not p) or (not q))) for p in (0,1) for q in (0,1))
assert taut
logic.append(Q('Theo luật De Morgan, ¬(p ∧ q) tương đương với:','¬p ∨ ¬q',['¬p ∧ ¬q','p ∨ q','¬p → q'],'Phủ định phép hội thành tuyển của các phủ định.'))
logic.append(Q('Mệnh đề (p ∧ ¬p) là:','mâu thuẫn (luôn sai)',['hằng đúng','đúng khi p đúng','phụ thuộc p'],'p và ¬p không bao giờ cùng đúng nên hội của chúng luôn sai.'))
sk('logic','Logic mệnh đề',['m01','m02'],'Học lại Module 1 (Logic mệnh đề) và 2 (Vị từ, lượng từ).',logic)
# 2 Tập hợp
A={1,2,3,4,5,6};B={4,5,6,7,8}
st=[]
st.append(Q('Cho A={1,2,3,4,5,6}, B={4,5,6,7,8}. |A ∪ B| bằng:',len(A|B),[len(A)+len(B),len(A&B),len(A)],'|A ∪ B| = |A| + |B| − |A ∩ B| = 6 + 5 − 3 = 8.'))
st.append(Q('Với A, B ở trên, |A \\ B| bằng:',len(A-B),[len(A|B),len(A),len(B-A)+3],'A \\ B = {1,2,3}: các phần tử thuộc A mà không thuộc B.'))
st.append(Q('Số tập con của tập có 5 phần tử là:',2**5,[5*5,F(5),2*5],'Mỗi phần tử được chọn hoặc không: 2⁵ = 32.'))
st.append(Q('Số tập con có đúng 2 phần tử của tập 6 phần tử là:',comb(6,2),[F(6),6*2,2**6],'C(6,2) = 6·5/2 = 15.'))
st.append(Q('|A × B| với |A| = 4, |B| = 7 bằng:',28,[11,16,47],'Tích Descartes có |A|·|B| phần tử.'))
st.append(Q('A ⊆ B và B ⊆ A thì:','A = B',['A ∩ B = ∅','A là tập con thực sự của B','A ∪ B = ∅'],'Hai tập bao hàm nhau theo cả hai chiều thì bằng nhau.'))
sk('set','Tập hợp',['m03','m04'],'Xem Module 3 (Tập hợp, độ phức tạp) và nguyên lý bù trừ ở Module 4.',st)
# 3 Hàm & phần nguyên
fn=[]
fn.append(Q('⌊3,7⌋ + ⌈−2,3⌉ bằng:',math.floor(3.7)+math.ceil(-2.3),[1,2,0,5],'⌊3,7⌋ = 3; ⌈−2,3⌉ = −2; tổng = 1.'))
fn.append(Q('Hàm f: {1,2,3} → {a,b,c,d}. Số hàm đơn ánh là:',4*3*2,[4**3,3**4,12],'Chọn ảnh lần lượt cho 1,2,3 khác nhau: 4·3·2 = 24.'))
fn.append(Q('Số hàm từ tập 3 phần tử vào tập 4 phần tử là:',4**3,[3**4,12,24],'Mỗi trong 3 phần tử có 4 lựa chọn ảnh: 4³ = 64.'))
fn.append(Q('f(x)=x² trên tập số thực R là:','không đơn ánh, không toàn ánh',['song ánh','đơn ánh nhưng không toàn ánh','toàn ánh nhưng không đơn ánh'],'f(2)=f(−2) nên không đơn ánh; không có x để f(x) = −1 nên không toàn ánh.'))
fn.append(Q('⌊n/2⌋ + ⌈n/2⌉ với n nguyên bằng:','n',['n/2','2n','n − 1'],'n chẵn: n/2 + n/2 = n; n lẻ: (n−1)/2 + (n+1)/2 = n.'))
fn.append(Q('Số nguyên dương ≤ 100 chia hết cho 7 là:',100//7,[15,13,7],'⌊100/7⌋ = 14.'))
sk('func','Hàm số, phần nguyên',['m03','m04'],'Xem lại phần hàm số và phần nguyên trong Module 3, 4.',fn)
# 4 Chia hết & đồng dư
dv=[]
dv.append(Q('Số dư của 2025 chia cho 7 là:',2025%7,[1,3,5],'7·289 = 2023 nên 2025 = 2023 + 2, dư 2.'))
dv.append(Q('gcd(84, 36) bằng:',gcd(84,36),[6,24,4],'84 = 2·36 + 12; 36 = 3·12 → gcd = 12.'))
dv.append(Q('Số ước dương của 72 = 2³·3² là:',(3+1)*(2+1),[6,8,10],'(3+1)(2+1) = 12.'))
dv.append(Q('2¹⁰ mod 11 bằng:',pow(2,10,11),[2,5,10],'Theo định lý Fermat nhỏ 2¹⁰ ≡ 1 (mod 11).'))
dv.append(Q('Trong 1..200 có bao nhiêu số chia hết cho 6?',200//6,[34,32,35],'⌊200/6⌋ = 33.'))
dv.append(Q('Nếu a ≡ 3 (mod 5), b ≡ 4 (mod 5) thì a·b mod 5 bằng:',(3*4)%5,[1,3,4],'3·4 = 12 ≡ 2 (mod 5).'))
sk('div','Chia hết, ước chung, đồng dư',['m04','m05','m08'],'Ôn nhanh chia hết và đồng dư rồi vào Module 4, 5.',dv)
# 5 Quy tắc đếm
c5=[]
c5.append(Q('Có 3 áo và 4 quần. Số cách mặc một bộ (áo + quần) là:',12,[7,24,81],'Quy tắc nhân: 3·4 = 12.'))
c5.append(Q('Chọn 1 đồ uống trong 5 loại hoặc 1 món ăn trong 6 loại (chỉ chọn một thứ). Số cách:',11,[30,1,56],'Quy tắc cộng: 5 + 6 = 11.'))
c5.append(Q('Số xâu nhị phân độ dài 8 là:',2**8,[16,64,128],'Mỗi vị trí có 2 lựa chọn: 2⁸ = 256.'))
c5.append(Q('Số xâu nhị phân độ dài 8 bắt đầu bằng 1 và kết thúc bằng 0 là:',2**6,[2**7,2**8,6],'Hai đầu cố định, còn 6 vị trí tự do: 2⁶ = 64.'))
c5.append(Q('Số số có 3 chữ số (100–999) là:',900,[999,1000,899],'999 − 100 + 1 = 900.'))
c5.append(Q('Số số có 3 chữ số khác nhau (không bắt đầu bằng 0) là:',9*9*8,[9*10*10,10*9*8,648+1],'9 cách cho chữ số đầu, 9 cho chữ số thứ hai (kể cả 0), 8 cho chữ số thứ ba: 648.'))
sk('count','Quy tắc cộng, quy tắc nhân',['m04'],'Học Module 4 (Nguyên lý đếm cơ bản).',c5)
# 6 Hoán vị, tổ hợp
p6=[]
p6.append(Q('Số cách xếp 5 người thành một hàng là:',F(5),[25,5*4,32],'5! = 120.'))
p6.append(Q('C(8,3) bằng:',comb(8,3),[24,336,112],'8·7·6/(3·2·1) = 56.'))
p6.append(Q('Số cách chọn 3 người từ 8 người xếp thành hàng (có thứ tự) là:',8*7*6,[56,512,24],'Chỉnh hợp A(8,3) = 8·7·6 = 336.'))
p6.append(Q('C(10,4) = C(10,k) với k khác 4 là:',6,[5,3,7],'Tính đối xứng C(n,k) = C(n,n−k): k = 6.'))
p6.append(Q('Số cách chia 4 viên bi giống nhau vào 3 hộp (hộp rỗng được) là:',comb(6,2),[12,81,64],'C(4+3−1, 3−1) = C(6,2) = 15.'))
p6.append(Q('Số hoán vị của chữ MAMA (hai M, hai A) là:',F(4)//(F(2)*F(2)),[24,12,8],'4!/(2!·2!) = 6.'))
sk('comb','Hoán vị, chỉnh hợp, tổ hợp',['m04','m05'],'Học Module 4–5 (Đếm, tổ hợp).',p6)
# 7 Tổng, cấp số
s7=[]
s7.append(Q('1 + 2 + … + 100 bằng:',sum(range(1,101)),[5000,10100,5151],'n(n+1)/2 = 100·101/2 = 5050.'))
s7.append(Q('1 + 2 + 4 + … + 2⁹ bằng:',sum(2**i for i in range(10)),[1023+1,512,1000],'2¹⁰ − 1 = 1023.'))
s7.append(Q('Cấp số cộng: u₁ = 3, công sai 4. u₁₀ bằng:',3+9*4,[43,39,40],'u₁₀ = 3 + 9·4 = 39.'))
s7.append(Q('Tổng 10 số hạng đầu của cấp số cộng u₁ = 3, d = 4 là:',sum(3+4*i for i in range(10)),[210,195,200],'10·(3+39)/2 = 210.'))
s7.append(Q('Σ_{i=1}^{5} i² bằng:',sum(i*i for i in range(1,6)),[15,25,45],'1+4+9+16+25 = 55.'))
s7.append(Q('Σ_{k=0}^{n} C(n,k) bằng:','2ⁿ',['n²','n!','2n'],'Số tất cả tập con của tập n phần tử: 2ⁿ.'))
sk('sum','Tổng, cấp số',['m07','m08','m09'],'Ôn công thức cấp số trước khi học Module 7–9.',s7)
# 8 Lũy thừa, logarit
l8=[]
l8.append(Q('log₂ 64 bằng:',6,[5,8,32],'2⁶ = 64.'))
l8.append(Q('2¹⁰ bằng:',1024,[100,512,2048],'2¹⁰ = 1024.'))
l8.append(Q('3ⁿ⁺¹ / 3ⁿ⁻¹ bằng:',9,[3,6,27],'3^((n+1)−(n−1)) = 3² = 9.'))
l8.append(Q('Số chữ số nhị phân tối thiểu để biểu diễn số 1000 là:',len(bin(1000))-2,[9,11,12],'2⁹ = 512 ≤ 1000 < 2¹⁰ = 1024 nên cần 10 bit.'))
l8.append(Q('log₂ n tăng chậm hơn hay nhanh hơn n khi n lớn?','chậm hơn',['nhanh hơn','như nhau','không so sánh được'],'log n = o(n): n tăng gấp đôi thì log n chỉ tăng thêm 1.'))
l8.append(Q('(2³)² bằng:',64,[32,16,12],'2⁶ = 64.'))
sk('pow','Lũy thừa, logarit',['m03','m08'],'Ôn lũy thừa/logarit trước Module 3 (độ phức tạp) và 8.',l8)
# 9 Quy nạp, đệ quy
r9=[]
def fib(n):
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a
r9.append(Q('Dãy a₀=1, a₁=1, aₙ=aₙ₋₁+aₙ₋₂. a₆ bằng:',(lambda: [1,1,2,3,5,8,13][6])(),[8,21,11],'1,1,2,3,5,8,13 → a₆ = 13.'))
r9.append(Q('Dãy a₁=2, aₙ=3aₙ₋₁. a₄ bằng:',2*27,[24,54+1,162],'2, 6, 18, 54 → a₄ = 54.'))
r9.append(Q('5! đệ quy: 5! = 5·4!. 4! bằng:',24,[20,120,16],'4! = 24.'))
r9.append(Q('Bước cơ sở của quy nạp dùng để:','chứng minh mệnh đề đúng với giá trị đầu tiên',['giả sử mệnh đề đúng với n = k','suy ra mệnh đề với k+1','chứng minh với mọi n'],'Cơ sở: kiểm tra giá trị nhỏ nhất; bước quy nạp: từ k suy ra k+1.'))
r9.append(Q('Hàm đệ quy f(n)=f(n−1)+2, f(0)=1. f(5) bằng:',11,[10,12,9],'f(n) = 1 + 2n → f(5) = 11.'))
r9.append(Q('Số lần gọi trực tiếp tối đa của F(n) = F(n−1) + F(n−2) (cơ sở n ≤ 1) tăng như:','hàm mũ',['hàm tuyến tính','hàm logarit','hằng số'],'Cây gọi đệ quy nhân đôi mỗi tầng, tăng theo hàm mũ (≈ φⁿ).'))
sk('rec','Dãy truy hồi, quy nạp',['m07','m08','m10'],'Học Module 7–8 (truy hồi) cẩn thận từ đầu.',r9)
# 10 Lập trình
def loop1():
    c=0
    for i in range(1,11):
        for j in range(i,11): c+=1
    return c
cd=[]
cd.append(Q('Vòng lặp for i=1..10: s += i. Kết thúc s bằng:',55,[10,45,100],'1+…+10 = 55.'))
cd.append(Q('for i=1..n, for j=1..n: c++. Độ phức tạp thời gian là:','O(n²)',['O(n)','O(n log n)','O(2ⁿ)'],'Hai vòng lồng nhau, mỗi vòng n lần: n² lần.'))
cd.append(Q('for i=1..10, for j=i..10: c++. Sau khi chạy, c bằng:',loop1(),[100,45,56],'10 + 9 + … + 1 = 55.'))
cd.append(Q('while (n > 1) n = n / 2; lặp khoảng bao nhiêu lần với n = 1024?',10,[1024,512,100],'1024 → 512 → … → 1: 10 lần = log₂ 1024.'))
cd.append(Q('Hàm int f(int n){ if(n<=1) return 1; return n*f(n-1);} trả về f(5) =',120,[24,5,25],'f(5) = 5! = 120.'))
cd.append(Q('Trong C++, 7 / 2 và 7 % 2 lần lượt cho:','3 và 1',['3,5 và 1','4 và 1','3 và 0'],'Chia nguyên: 7/2 = 3; phần dư 7 % 2 = 1.'))
sk('code','Đọc hiểu chương trình, vòng lặp, đệ quy',['m03','m10','m11'],'Ôn lập trình C/C++ cơ bản (vòng lặp, đệ quy, mảng) rồi học Module 10–11.',cd)
