from qcore import *
import tsp as TS
from tsp import INF
import itertools, math
def sub(n): return ''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(n))
def mat(C): return '\n'.join('  '+' '.join(f'{("∞" if i==j else x):>3}' for j,x in enumerate(row)) for i,row in enumerate(C))
def matA(A): return '\n'.join('  '+' '.join(f'{("∞" if x==INF else x):>3}' for x in row) for row in A)
def rmat(rng,n,lo=3,hi=30):
    return [[0 if i==j else rng.randint(lo,hi) for j in range(n)] for i in range(n)]
def tour_txt(t): return '→'.join(str(x) for x in t)
def gen(seed=13):
    B=Bank('m13',seed); rng=B.rng
    for _ in range(45):
        n=rng.choice([4,5,5,6]); C=rmat(rng,n)
        A=[[INF if i==j else C[i][j] for j in range(n)] for i in range(n)]
        rows=list(range(n)); cols=list(range(n))
        s,rc,cc=TS.reduce([r[:] for r in A],rows,cols)
        A2=[r[:] for r in A]; sr=0; rcs=[]
        for i in range(n):
            m=min(A2[i][j] for j in range(n) if j!=i); rcs.append(m); sr+=m
            for j in range(n):
                if j!=i: A2[i][j]-=m
        ccs=[min(A2[i][j] for i in range(n) if i!=j) for j in range(n)]; sc=sum(ccs)
        assert sr+sc==s
        stem=f'Bài toán người du lịch với {n} thành phố, ma trận chi phí (∞ trên đường chéo):\n{mat(C)}\nCận dưới của mọi hành trình sau thủ tục rút gọn (tổng các hằng số rút gọn theo dòng và cột) là:'
        wr=set(near_ints(s,rng,6,lo=1))|{sr,sum(min(C[i][j] for j in range(n) if j!=i) for i in range(n))+1}
        wr.discard(s)
        expl=f'Rút gọn dòng: hằng số các dòng = {", ".join(map(str,rcs))} (tổng {sr}). Ma trận sau khi trừ:\n{matA(A2)}\nRút gọn cột: hằng số các cột = {", ".join(map(str,ccs))} (tổng {sc}).\nCận dưới = {sr} + {sc} = {s}. Mọi hành trình chứa đúng một phần tử mỗi dòng và mỗi cột nên không thể có chi phí nhỏ hơn {s}.'
        B.add(stem,s,list(wr),expl,level=2,topic='Rút gọn ma trận')
        B.add(f'Ma trận chi phí {n} thành phố (∞ trên đường chéo):\n{mat(C)}\nTổng các hằng số rút gọn THEO DÒNG là:',sr,near_ints(sr,rng,6,lo=1)+[s],f'Hằng số dòng i là phần tử nhỏ nhất của dòng i (bỏ đường chéo): {", ".join(map(str,rcs))}. Tổng = {sr}. (Chưa cộng phần rút gọn theo cột = {sc}.)',level=2,topic='Rút gọn ma trận')
    # cạnh phân nhánh
    for _ in range(45):
        n=rng.choice([5,5,6]); C=rmat(rng,n)
        A=[[INF if i==j else C[i][j] for j in range(n)] for i in range(n)]
        rows=list(range(n)); cols=list(range(n)); s,_,_=TS.reduce(A,rows,cols)
        be,beta=TS.best_edge(A,rows,cols)
        zeros=[(i,j) for i in rows for j in cols if A[i][j]==0]
        info=[]
        for i,j in zeros:
            mr=min(A[i][k] for k in cols if k!=j); mc=min(A[k][j] for k in rows if k!=i); info.append(((i+1,j+1),mr,mc,mr+mc))
        top=sorted({x[3] for x in info},reverse=True)
        B.add(f'Sau khi rút gọn, ma trận (n = {n}) là:\n{matA(A)}\nCận dưới hiện tại là {s}. Theo giáo trình PTIT, cạnh phân nhánh (r, c) được chọn là số 0 có tổng (min dòng khác nó + min cột khác nó) lớn nhất. Cạnh đó là (nếu có nhiều, chọn số 0 đầu tiên theo dòng, rồi cột):',f'({be[0]+1}, {be[1]+1})',[f'({i}, {j})' for (i,j),_,_,_ in info if (i,j)!=(be[0]+1,be[1]+1)][:6] or ['(1, 2)','(2, 1)','(3, 4)'],'Với mỗi số 0 tại (i,j): θ = min dòng i (bỏ ô đó) + min cột j (bỏ ô đó):\n'+'\n'.join(f'  ({a},{b}): {mr} + {mc} = {t}' for (a,b),mr,mc,t in info)+f'\nLớn nhất: β = {beta} tại ({be[0]+1}, {be[1]+1}). Nhánh KHÔNG chứa cạnh này có cận dưới {s} + {beta} = {s+beta}.',level=3,topic='Chọn cạnh phân nhánh')
        B.add(f'Ma trận rút gọn (cận dưới hiện tại {s}):\n{matA(A)}\nNhánh "không chứa cạnh ({be[0]+1}, {be[1]+1})" (cạnh phân nhánh tốt nhất) có cận dưới bằng:',s+beta,near_ints(s+beta,rng,6,lo=s)+[s],f'Đặt A[{be[0]+1}][{be[1]+1}] = ∞ rồi rút gọn lại: chỉ dòng {be[0]+1} và cột {be[1]+1} thay đổi, cộng thêm min dòng + min cột = {beta}. Cận dưới mới = {s} + {beta} = {s+beta}.',level=3,topic='Chọn cạnh phân nhánh')
    # tối ưu và hành trình
    for _ in range(50):
        n=rng.choice([4,5,5,6]); C=rmat(rng,n)
        res=TS.bb(C); best,bt=TS.brute(C); assert res['cost']==best
        tour=[x+1 for x in bt]
        idc=sum(C[i][(i+1)%n] for i in range(n))
        wr=set(near_ints(best,rng,6,lo=1)); wr|={idc if idc!=best else best+2}; wr.discard(best)
        B.add(f'Bài toán người du lịch với ma trận chi phí:\n{mat(C)}\nChi phí của hành trình tối ưu (xuất phát và trở về thành phố 1) là:',best,list(wr),f'Số hành trình khả dĩ (n−1)! = {math.factorial(n-1)}. Thuật toán nhánh cận (rút gọn ma trận; gốc có cận dưới {res["root"]}) tìm được hành trình tối ưu {tour_txt(tour)} với chi phí {best} (đối chiếu bằng vét cạn {math.factorial(n-1)} hành trình).\nHành trình 1→2→…→n→1 có chi phí {idc}, không nhất thiết tối ưu.',level=3,topic='Hành trình tối ưu')
        B.add(f'Ma trận chi phí:\n{mat(C)}\nCận dưới ở gốc (sau rút gọn) là {res["root"]}. Chi phí tối ưu {best}. Khoảng cách "cận dưới − tối ưu" (phần cần nhánh cận thu hẹp) là:',best-res['root'],near_ints(best-res['root'],rng,5,lo=0)+[best],f'Tối ưu {best} ≥ cận dưới {res["root"]}, hiệu = {best-res["root"]}. Nếu hiệu bằng 0 thì hành trình tối ưu được tìm thấy ngay khi cận dưới đạt.',level=3,topic='Hành trình tối ưu')
    # phương án đầu tiên (kiểu đề trắc nghiệm PTIT)
    for _ in range(35):
        n=rng.choice([5,5,6]); C=rmat(rng,n,3,22)
        idc=sum(C[i][(i+1)%n] for i in range(n))
        opts=set(near_ints(idc,rng,8,lo=5))
        B.add(f'Áp dụng thuật toán nhánh cận (quay lui theo thứ tự thành phố tăng dần, xuất phát từ 1) cho ma trận chi phí:\n{mat(C)}\nPhương án f* được cập nhật ĐẦU TIÊN có chi phí:',idc,list(opts),f'Nhánh đầu tiên đi sâu nhất không bị cắt (kỷ lục ban đầu là +∞ nên không cắt gì) là hành trình 1→2→…→{n}→1: '+' + '.join(str(C[i][(i+1)%n]) for i in range(n))+f' = {idc}. (Cách đọc này khớp mọi câu trắc nghiệm còn nguyên phương án của bộ đề ôn PTIT.)',level=2,topic='Phương án đầu tiên')
    # tính chi phí hành trình cho trước
    for _ in range(30):
        n=rng.choice([5,6]); C=rmat(rng,n); p=[1]+rng.sample(range(2,n+1),n-1)+[1]
        cost=sum(C[p[i]-1][p[i+1]-1] for i in range(n))
        B.add(f'Với ma trận chi phí:\n{mat(C)}\nHành trình {tour_txt(p)} có chi phí:',cost,near_ints(cost,rng,6,lo=1),'Cộng các phần tử tương ứng từng cạnh: '+' + '.join(f'c({p[i]},{p[i+1]}) = {C[p[i]-1][p[i+1]-1]}' for i in range(n))+f' = {cost}.',level=1,topic='Tính chi phí')
    # số hành trình
    for n in range(4,11):
        B.add(f'Bài toán người du lịch bất đối xứng với {n} thành phố (xuất phát từ thành phố 1, đi qua mỗi thành phố đúng một lần rồi quay về). Số hành trình khác nhau là:',math.factorial(n-1),[math.factorial(n),math.factorial(n-1)//2,2**n,n*n],f'Hoán vị n−1 = {n-1} thành phố còn lại: ({n}−1)! = {math.factorial(n-1)}. Với ma trận đối xứng chiều đi và về cho cùng chi phí nên chỉ còn ({n}−1)!/2 hành trình khác nhau.',level=2,topic='Khái niệm')
        B.add(f'Bài toán người du lịch với {n} thành phố và ma trận chi phí đối xứng. Số hành trình khác nhau về chi phí (bỏ qua chiều đi) là:',math.factorial(n-1)//2,[math.factorial(n-1),math.factorial(n),math.factorial(n-2),n*(n-1)//2],f'({n}−1)!/2 = {math.factorial(n-1)//2}.',level=3,topic='Khái niệm')
    # khái niệm
    con=[('Ý nghĩa của thủ tục rút gọn ma trận là','trừ đều cùng một hằng số ở mỗi dòng/cột không đổi hành trình tối ưu và cho cận dưới bằng tổng hằng số đã trừ',['làm giảm số thành phố','đổi bài toán min thành bài toán max','luôn cho ngay hành trình tối ưu']),
         ('Sau khi chọn cạnh (r, c) vào hành trình (nhánh trái), cần đặt ô nào bằng ∞ để tránh chu trình con?','ô (j_k, i₁): từ cuối đường đi bắt đầu tại c về đầu đường đi kết thúc tại r',['ô (r, c)','ô (c, r) trong mọi trường hợp','toàn bộ dòng c']),
         ('Trong thuật toán nhánh cận người du lịch của giáo trình, thứ tự duyệt các nhánh là','nhánh trái (chứa cạnh) trước, nhánh phải (không chứa cạnh) sau nếu cận dưới còn nhỏ hơn kỷ lục',['nhánh phải trước','ngẫu nhiên','chỉ nhánh phải']),
         ('Khi ma trận còn 2×2 sau các bước rút gọn thì','hai cạnh còn lại được kết nạp ngay (chỉ còn một cách chọn hợp lệ)',['phải rút gọn thêm hai lần','bỏ nhánh này','đặt lại cận dưới bằng 0']),
         ('Một nút của cây tìm kiếm bị cắt khi','cận dưới của nút đó ≥ chi phí của hành trình tốt nhất đã tìm được',['cận dưới nhỏ hơn kỷ lục','ma trận có nhiều số 0','đã đi qua n − 1 thành phố']),
         ('Cạnh phân nhánh được chọn là số 0 có tổng min dòng + min cột lớn nhất vì','nhánh không chứa cạnh đó sẽ tăng cận dưới nhiều nhất và dễ bị cắt',['nhánh chứa cạnh đó có chi phí nhỏ nhất','số 0 đó luôn thuộc hành trình tối ưu','để số dòng giảm nhanh nhất'])]
    for q,a,w in con: B.add(q,a,w,'Xem Module 13: rút gọn ma trận → chọn cạnh phân nhánh (r,c) → nhánh chứa (thu nhỏ ma trận, cấm chu trình con) → nhánh không chứa (đặt ∞) → cắt theo kỷ lục.',level=1,topic='Khái niệm')
    return B
def essays(B):
    rng=B.rng
    R=[[0,3,93,13,33,9],[4,0,77,42,21,16],[45,17,0,36,16,28],[39,90,80,0,56,7],[28,46,88,33,0,25],[3,88,18,46,92,0]]
    res=TS.bb(R)
    lines=[f'Ma trận chi phí n = 6 (ví dụ giáo trình 2016, mục 4.4). Thủ tục rút gọn: cận dưới ở gốc = {res["root"]}.']
    for e in res['log'][:16]:
        d,l,b,st=e[0],e[1],e[2],e[3]
        if st=='branch': tail=f'→ chọn cạnh {e[4]} (β = {e[5]})'
        elif st=='record': tail=f'★ hành trình đầy đủ, chi phí {e[4]}'
        elif st=='leaf': tail=f'lá (chi phí {e[4]}, không cải thiện)'
        elif st=='cut': tail='✗ cắt (cận dưới ≥ kỷ lục)'
        elif st=='dead': tail='✗ vô nghiệm'
        else: tail=''
        lines.append('  '*d+f'[{l}] cận dưới = {b} {tail}')
    lines.append(f'Kết quả: hành trình tối ưu {tour_txt(res["tour"])} với chi phí {res["cost"]} (kiểm chứng bằng vét cạn 120 hành trình).')
    B.essay('Giải bài toán người du lịch bằng thuật toán nhánh cận (rút gọn ma trận) với ma trận chi phí n = 6:\n'+mat(R),'\n'.join(lines),level=3,topic='TSP nhánh cận')
    for _ in range(6):
        n=5; C=rmat(rng,n,3,25); res=TS.bb(C); best,bt=TS.brute(C); assert res['cost']==best
        A=[[INF if i==j else C[i][j] for j in range(n)] for i in range(n)]
        s,rc,cc=TS.reduce([r[:] for r in A],list(range(n)),list(range(n)))
        B.essay('Cho bài toán người du lịch n = 5 với ma trận chi phí:\n'+mat(C)+'\na) Tính cận dưới ở gốc bằng thủ tục rút gọn.\nb) Tìm hành trình tối ưu và chi phí.',f'a) Cận dưới ở gốc = {s}.\nb) Hành trình tối ưu {tour_txt([x+1 for x in bt])}, chi phí {best} (nhánh cận và vét cạn (n−1)! = 24 hành trình cho cùng kết quả).',level=3,topic='TSP nhánh cận')
    B.essay('Chứng minh rằng tổng các hằng số rút gọn là cận dưới của chi phí mọi hành trình.','Mọi hành trình gồm đúng n cạnh, mỗi cạnh chọn đúng một phần tử từ mỗi dòng và mỗi cột. Nếu trừ hằng số h khỏi mọi phần tử của một dòng (hoặc cột) thì chi phí của mọi hành trình giảm đúng h. Sau khi rút gọn, ma trận không âm nên chi phí mọi hành trình mới ≥ 0; do đó chi phí ban đầu ≥ tổng các hằng số đã trừ.',level=2,topic='TSP nhánh cận')
    B.essay('Giải thích vì sao khi chọn cạnh (r, c) vào hành trình cần cấm một cạnh khác để tránh chu trình con.','Nếu các cạnh đã chọn tạo thành đường đi i₁→…→r→c→…→j_k thì cạnh (j_k, i₁) sẽ đóng đường đi này thành chu trình có ít hơn n thành phố (chu trình con) và không phải hành trình đầy đủ. Đặt A[j_k][i₁] = ∞ loại bỏ khả năng đó.',level=2,topic='TSP nhánh cận')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items))
