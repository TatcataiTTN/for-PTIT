from qcore import *
from knap import brute, bb
from fractions import Fraction as Fr
import itertools, math
def sub(n): return ''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(n))
def T(t): return '('+', '.join(map(str,t))+')'
def fr(x):
    x=Fr(x)
    return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator} ≈ {float(x):.2f}'
def lin(cs,var='x'):
    return ' + '.join((str(c) if c!=1 else '')+f'{var}{sub(i+1)}' for i,c in enumerate(cs))
def inst(rng,n=4,uniq=True):
    while True:
        v=[rng.randint(1,9) for _ in range(n)]; w=[rng.randint(1,7) for _ in range(n)]; b=rng.randint(max(w)+1,sum(w)-1)
        best,bx,feas=brute(v,w,b)
        # duy nhất phương án tối ưu
        opt=[x for x in itertools.product((0,1),repeat=n) if sum(a*c for a,c in zip(w,x))<=b and sum(a*c for a,c in zip(v,x))==best]
        if len(opt)==1 and len(set(Fr(v[i],w[i]) for i in range(n)))==n: return v,w,b
def trace_text(v,w,b,res,unlimited=False):
    order=res['order']; lines=[f'Sắp xếp theo c/a giảm dần: '+', '.join(f'x{sub(i+1)} ({v[i]}/{w[i]} = {v[i]/w[i]:.2f})' for i in order)+'.','Ký hiệu nút: (x…) | δ = giá trị đã chọn | w = trọng lượng còn lại | g = δ + c_{k+1}·w/a_{k+1}.']
    rs=[Fr(v[i],w[i]) for i in order]
    if len(set(rs))<len(rs): lines.append('Lưu ý: có tỉ số c/a bằng nhau; giữ thứ tự theo chỉ số biến (kết quả tối ưu không đổi).')
    lines.append(f'Gốc: FOPT = −∞, g = {fr(res["nodes"][0]["g"])}.')
    for nd in res['nodes'][1:]:
        xs=', '.join(map(str,nd['x']))
        st={'expand':'→ mở rộng (g > FOPT)','pruned':'✗ cắt (g ≤ FOPT)','record':'★ cập nhật kỷ lục','leaf':'lá, không cải thiện'}[nd['st']]
        lines.append(f'({xs}) | δ = {nd["delta"]}, w = {nd["rem"]}, g = {fr(nd["g"])} {st}')
    xo=res['xopt']
    lines.append(f'Kết quả: f* = {res["fopt"]}, x* = {T(xo)} (theo thứ tự biến gốc x₁…x_{len(xo)}).')
    return '\n'.join(lines)
def gen(seed=12):
    B=Bank('m12',seed); rng=B.rng
    for _ in range(90):
        n=rng.choice([4,4,4,5]); v,w,b=inst(rng,n)
        best,bx,feas=brute(v,w,b); res=bb(v,w,b); assert res['fopt']==best and res['xopt']==bx
        stem=f'Bài toán cái túi: {lin(v)} → max; {lin(w)} ≤ {b}; x{sub(1)},…,x{sub(n)} ∈ {{0,1}}. Phương án tối ưu là:'
        wr=set()
        for x in itertools.product((0,1),repeat=n):
            W=sum(a*c for a,c in zip(w,x)); V=sum(a*c for a,c in zip(v,x))
            if x!=bx and V>=best-3: wr.add(x)
        wr=sorted(wr,key=lambda x:-sum(a*c for a,c in zip(v,x)))
        greedy=sorted(range(n),key=lambda i:-v[i]); 
        wl=[x for x in wr][:6]
        if len(wl)<3: continue
        expl=trace_text(v,w,b,res)+f'\nKiểm chứng bằng duyệt toàn bộ: có {feas} phương án khả thi trong {2**n}; tốt nhất {T(bx)} giá trị {best}.\nMột số phương án đáng ngờ: '+'; '.join(f'{T(x)} cho '+('vượt tải' if sum(a*c for a,c in zip(w,x))>b else f'giá trị {sum(a*c for a,c in zip(v,x))}') for x in wl[:3])+'.'
        B.add(stem,T(bx),[T(x) for x in wl],expl,level=2,topic='Phương án tối ưu')
        B.add(f'Bài toán cái túi: {lin(v)} → max; {lin(w)} ≤ {b}; xᵢ ∈ {{0,1}}. Giá trị tối ưu f* bằng:',best,[best+d for d in (-3,-2,-1,1,2,3) if best+d>=0]+[sum(v)],f'Duyệt toàn bộ {2**n} vectơ 0/1, loại các phương án vượt tải trọng {b}; giá trị lớn nhất là {best} tại {T(bx)}.\nLưu ý: sum(v) = {sum(v)} là giá trị nếu lấy hết đồ vật, thường vượt tải.',level=2,topic='Giá trị tối ưu')
        B.add(f'Với bài toán cái túi {lin(v)} → max; {lin(w)} ≤ {b}; xᵢ ∈ {{0,1}}, có bao nhiêu phương án KHẢ THI (thỏa ràng buộc trọng lượng), kể cả phương án rỗng?',feas,near_ints(feas,rng,6,lo=1)+[2**n],f'Duyệt toàn bộ {2**n} vectơ, đếm các vectơ có tổng trọng lượng ≤ {b}: {feas}.',level=2,topic='Duyệt toàn bộ')
    # cận và thứ tự
    for _ in range(45):
        n=4; v,w,b=inst(rng,n); res=bb(v,w,b)
        order=res['order']; C=res['C']; A=res['A']
        g0=Fr(C[0]*b,A[0])
        B.add(f'Cái túi: {lin(v)} → max; {lin(w)} ≤ {b}. Sau khi sắp các đồ vật theo c/a giảm dần, cận trên ở nút gốc g = c₁·b/a₁ bằng:',fr(g0),[fr(Fr(C[0]*b,A[0])+1),fr(Fr(C[1]*b,A[1])) if Fr(C[1]*b,A[1])!=g0 else fr(g0+2),str(sum(v)),fr(Fr(sum(v),sum(w))*b)],f'Tỉ số c/a: '+', '.join(f'x{sub(i+1)}: {v[i]}/{w[i]} = {v[i]/w[i]:.2f}' for i in range(n))+f'. Lớn nhất là x{sub(order[0]+1)} (c₁ = {C[0]}, a₁ = {A[0]}). g = {C[0]}·{b}/{A[0]} = {fr(g0)}. Đây là giá trị của bài toán biến liên tục (chỉ chọn vật có c/a lớn nhất) nên là cận trên của f*.',level=2,topic='Cận trên')
        B.add(f'Cái túi: {lin(v)} → max; {lin(w)} ≤ {b}. Thứ tự xét các biến trong thuật toán nhánh cận (sắp c/a giảm dần) là:',', '.join(f'x{sub(i+1)}' for i in order),[', '.join(f'x{sub(i+1)}' for i in list(reversed(order))),', '.join(f'x{sub(i+1)}' for i in sorted(range(n),key=lambda i:-v[i])) if [i for i in sorted(range(n),key=lambda i:-v[i])]!=order else ', '.join(f'x{sub(i+1)}' for i in sorted(range(n),key=lambda i:w[i])),', '.join(f'x{sub(i+1)}' for i in range(n)) if list(range(n))!=order else ', '.join(f'x{sub(i+1)}' for i in list(reversed(range(n)))),', '.join(f'x{sub(i+1)}' for i in sorted(range(n),key=lambda i:w[i]))],'c/a: '+', '.join(f'x{sub(i+1)} = {v[i]}/{w[i]} = {v[i]/w[i]:.3f}' for i in range(n))+f'. Sắp giảm dần: '+', '.join(f'x{sub(i+1)}' for i in order)+'. (Sắp theo giá trị hoặc theo trọng lượng riêng lẻ là sai vì cận g dựa trên tỉ số c/a.)',level=2,topic='Cận trên')
    # nhánh cận: số nút bị cắt, kỷ lục
    for _ in range(50):
        n=4; v,w,b=inst(rng,n); res=bb(v,w,b); nodes=res['nodes'][1:]
        pr=sum(1 for x in nodes if x['st']=='pruned'); ex=sum(1 for x in nodes if x['st']=='expand'); up=len(res['updates'])
        stem=f'Cái túi: {lin(v)} → max; {lin(w)} ≤ {b}; xᵢ ∈ {{0,1}}. Chạy thuật toán nhánh cận của giáo trình PTIT (sắp c/a giảm dần; với mỗi biến thử giá trị 1 rồi 0; cắt nhánh khi g ≤ FOPT; g = δ + c_{{k+1}}·w/a_{{k+1}}). Số nút bị CẮT TỈA (không được mở rộng do g ≤ FOPT) là:'
        B.add(stem,pr,[pr+d for d in (-2,-1,1,2,3) if pr+d>=0][:5]+[ex],trace_text(v,w,b,res),level=3,topic='Nhánh cận – mô phỏng')
        B.add(f'Cái túi: {lin(v)} → max; {lin(w)} ≤ {b}; xᵢ ∈ {{0,1}}. Khi chạy nhánh cận (thử 1 trước 0, sắp c/a giảm dần), kỷ lục FOPT được CẬP NHẬT bao nhiêu lần (kể cả lần đầu)?',up,[u for u in range(1,6) if u!=up][:4],trace_text(v,w,b,res)+f'\nCác lần cập nhật kỷ lục: '+' → '.join(map(str,res['updates']))+f' ({up} lần).',level=3,topic='Nhánh cận – mô phỏng')
        B.add(f'Cái túi: {lin(v)} → max; {lin(w)} ≤ {b}; xᵢ ∈ {{0,1}}. Giá trị kỷ lục FOPT được xác lập LẦN ĐẦU TIÊN trong thuật toán nhánh cận (thử 1 trước 0, sắp c/a giảm dần) là:',res['updates'][0],[res['updates'][0]+d for d in (-2,-1,1,2,3) if res['updates'][0]+d>=0]+[res['fopt']+1],trace_text(v,w,b,res)+f'\nLá đầu tiên đến được (nhánh tham lam, mọi biến ưu tiên 1 nếu vừa) cho kỷ lục đầu tiên = {res["updates"][0]}.',level=3,topic='Nhánh cận – mô phỏng')
    # bài toán không giới hạn số lượng (giáo trình)
    for _ in range(20):
        n=rng.choice([3,4]); 
        while True:
            v=[rng.randint(2,12) for _ in range(n)]; w=[rng.randint(2,7) for _ in range(n)]; b=rng.randint(7,20)
            if len(set(Fr(v[i],w[i]) for i in range(n)))==n: break
        # tối ưu số nguyên không âm (vét cạn)
        best=0;bx=None
        for x in itertools.product(*[range(b//wi+1) for wi in w]):
            if sum(a*c for a,c in zip(w,x))<=b:
                V=sum(a*c for a,c in zip(v,x))
                if V>best: best=V;bx=x
        res=bb(v,w,b,unlimited=True); assert res['fopt']==best
        B.add(f'Cái túi biến nguyên (mỗi loại có số lượng không hạn chế): {lin(v)} → max; {lin(w)} ≤ {b}; xⱼ ∈ ℤ⁺. Giá trị tối ưu là:',best,[best+d for d in (-3,-2,-1,1,2) if best+d>=0]+[best+4],trace_text(v,w,b,res,True)+f'\nKiểm chứng vét cạn cho f* = {best}, x* = {T(res["xopt"])}.',level=3,topic='Cái túi biến nguyên')
    # khái niệm
    con=[('Trong nhánh cận cho bài toán tìm max, ta cắt nhánh khi','cận trên g của nhánh không lớn hơn kỷ lục hiện có (g ≤ FOPT)',['cận trên g lớn hơn kỷ lục','trọng lượng còn lại bằng 0','nhánh chưa được duyệt lần nào']),
         ('Cận trên của cái túi 0/1 được tính bằng cách giải bài toán','cái túi biến liên tục (cho phép lấy phân số đồ vật)',['cái túi với trọng lượng bằng 1','vét cạn các đồ vật còn lại','sắp xếp theo trọng lượng tăng dần']),
         ('Công thức cận trên g(u₁,…,u_k) trong giáo trình 2016 là','δ_k + c_{k+1}·b_k / a_{k+1}',['δ_k + c_{k+1}·a_{k+1}/b_k','δ_k − c_{k+1}·b_k / a_{k+1}','δ_k·b_k / a_{k+1}']),
         ('Vì sao phải sắp đồ vật theo c/a giảm dần trước khi chạy nhánh cận?','để cận g gần với giá trị thật nhất và cắt tỉa được nhiều nhánh',['để số phương án khả thi tăng lên','để bài toán trở thành bài toán min','để tránh phải tính trọng lượng']),
         ('Độ phức tạp trường hợp xấu nhất của nhánh cận giải cái túi 0/1 là','vẫn O(2ⁿ) (có thể không cắt được nhánh nào)',['O(n log n)','O(n²)','O(n)']),
         ('Ghi chú giáo trình PTIT về khởi tạo: với bài toán TÌM MAX, ta khởi tạo FOPT bằng','−∞',['+∞','0 luôn luôn đúng với mọi bài toán','n!']),
         ('Phương pháp duyệt toàn bộ cho cái túi n vật kiểm tra','2ⁿ phương án',['n! phương án','n² phương án','n phương án'])]
    for q,a,w in con: B.add(q,a,w,'Xem Module 12 §3–§5: duyệt toàn bộ là vét cạn mọi phương án; nhánh cận thêm hàm cận g để loại nhánh không thể chứa phương án tốt hơn kỷ lục.',level=1,topic='Khái niệm')
    return B
def essays(B):
    rng=B.rng
    ex=[]
    # đề dạng thi 2023-24 (số đề gốc) — tính lời giải bằng thuật toán
    for (v,w,b,tag) in [([3,5,7,4],[2,4,3,2],9,'đề 2023-2024, đề 01'),([6,5,3,1],[4,4,2,1],9,'đề 2023-2024, đề 02'),([5,5,3,8],[3,4,2,5],12,'đề 2023-2024, đề 03'),([5,2,7,1],[5,3,6,4],9,'đề 2017-2020')]:
        res=bb(v,w,b); best,bx,feas=brute(v,w,b)
        assert res['fopt']==best
        B.essay(f'Áp dụng thuật toán nhánh cận giải bài toán cái túi, chỉ rõ kết quả theo mỗi bước ({tag}): {lin(v)} → max; {lin(w)} ≤ {b}; xⱼ ∈ {{0,1}}.',trace_text(v,w,b,res),level=3,topic='Nhánh cận cái túi')
    for _ in range(8):
        v,w,b=inst(rng,4); res=bb(v,w,b)
        B.essay(f'Giải bài toán cái túi bằng thuật toán nhánh cận, ghi rõ từng nút: {lin(v)} → max; {lin(w)} ≤ {b}; xⱼ ∈ {{0,1}}.',trace_text(v,w,b,res),level=3,topic='Nhánh cận cái túi')
    for _ in range(4):
        v,w,b=inst(rng,4); best,bx,feas=brute(v,w,b)
        rows=[]
        for x in itertools.product((0,1),repeat=4):
            W=sum(a*c for a,c in zip(w,x)); V=sum(a*c for a,c in zip(v,x)); rows.append(f'{T(x)}: trọng lượng {W} '+('> '+str(b)+' (loại)' if W>b else f'≤ {b}, giá trị {V}'))
        B.essay(f'Giải bằng phương pháp duyệt toàn bộ (liệt kê bảng 16 phương án): {lin(v)} → max; {lin(w)} ≤ {b}; xⱼ ∈ {{0,1}}.','\n'.join(rows)+f'\nXOPT = {T(bx)}, FOPT = {best}.',level=2,topic='Duyệt toàn bộ')
    B.essay('Trình bày thuật toán duyệt toàn bộ giải bài toán tối ưu tổ hợp. (dạng câu 5a)','Bước 1 (khởi tạo): XOPT = ∅; FOPT = −∞ (bài toán max) hoặc +∞ (bài toán min).\nBước 2 (lặp): for each X ∈ D: S = f(X); nếu FOPT < S (max) thì FOPT = S, XOPT = X.\nBước 3: trả về (XOPT, FOPT).\nNhược điểm: số phương án bùng nổ (2ⁿ, n!), ví dụ 15! ≈ 1,3·10¹² hoán vị.',level=1,topic='Duyệt toàn bộ')
    B.essay('Trình bày thuật toán nhánh cận giải bài toán tối ưu (tìm max) và giải thích vai trò của hàm cận g. (dạng câu 5a)','Xây dựng phương án bộ phận (a₁,…,a_k) bằng quay lui. Với hàm g(a₁,…,a_k) ≥ max{f(x): x ∈ D, xᵢ = aᵢ, i ≤ k} (cận trên), duy trì kỷ lục FOPT (giá trị tốt nhất đã có).\nNếu g(a₁,…,a_k) ≤ FOPT thì mọi phương án mở rộng của nó không thể tốt hơn kỷ lục ⇒ bỏ nhánh. Ngược lại tiếp tục mở rộng Try(k+1). Khi k = n cập nhật kỷ lục.\nHàm g càng sát giá trị thật càng cắt được nhiều nhánh, nhưng tính g phải đơn giản hơn giải bài toán gốc.',level=2,topic='Nhánh cận cái túi')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items))
