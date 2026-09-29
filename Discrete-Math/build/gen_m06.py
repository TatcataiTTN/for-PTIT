from qcore import *
import math, itertools
def gen(seed=6):
    B=Bank('m06',seed); rng=B.rng
    # 1. Dirichlet cơ bản
    for _ in range(45):
        n=rng.randint(5,60); k=rng.randint(3,12)
        a=math.ceil(n/k)
        B.add(f'Có {n} quả bóng bỏ vào {k} hộp. Theo nguyên lý Dirichlet, chắc chắn có một hộp chứa ít nhất bao nhiêu quả?',a,[a-1 if a>1 else a+2,a+1,n//k if n//k!=a else a+2,n-k+1],f'⌈{n}/{k}⌉ = {a}. (Nếu mỗi hộp chứa ≤ {a-1} thì tổng ≤ {k}·{a-1} = {k*(a-1)} < {n}, vô lý.)',level=1,topic='Dirichlet tổng quát')
        m=rng.randint(3,9); k=rng.randint(3,12)
        N=k*(m-1)+1
        B.add(f'Cần chọn ít nhất bao nhiêu phần tử từ một tập có {k} nhóm để CHẮC CHẮN có {m} phần tử cùng nhóm?',N,[k*m,k*(m-1),k*m-1,(m-1)*k+2],f'Tình huống xấu nhất: mỗi nhóm có {m-1} phần tử ⇒ {k}·{m-1} = {k*(m-1)} phần tử mà chưa đủ; thêm 1 phần tử: {N}.',level=1,topic='Dirichlet tổng quát')
    # 2. thi trắc nghiệm (dạng đề thi 2019-2020, 2023)
    for _ in range(45):
        q=rng.randint(3,60); pts=rng.choice([0.25,0.5,1,2]); m=rng.randint(3,15)
        levels=q+1; N=levels*(m-1)+1
        ps=('%g'%pts).replace('.',',')
        B.add(f'Trong một kỳ thi trắc nghiệm đề gồm {q} câu. Thí sinh được {ps} điểm cho mỗi câu đúng và 0 điểm cho câu sai hoặc bỏ trống. Cần ít nhất bao nhiêu thí sinh để chắc chắn có ít nhất {m} thí sinh cùng điểm?',N,[q*(m-1)+1,levels*m,levels*(m-1),(levels-1)*m+1],f'Số mức điểm khác nhau = {q}+1 = {levels} (từ 0 đến {q} câu đúng). Theo Dirichlet cần {levels}·({m}−1)+1 = {N}.\nLỗi hay gặp: dùng {q} thay vì {levels} mức điểm (quên mức 0 điểm).',level=2,topic='Dirichlet – thi trắc nghiệm')
    # 3. modular (dạng đề 2017: (a-c),(b-d) chia hết cho m)
    for m in range(2,13):
        for kk in (2,3):
            ans=(kk-1)*m*m+1
            B.add(f'S là tập các cặp số nguyên (x, y). Cần lấy ra ít nhất bao nhiêu cặp để chắc chắn có {kk} cặp cùng lớp đồng dư, tức cùng (x mod {m}, y mod {m})?' if kk>2 else f'S là tập các cặp số nguyên (x, y). Cần lấy ra ít nhất bao nhiêu phần tử của S để chắc chắn có 2 cặp (a,b), (c,d) sao cho (a−c) và (b−d) đều chia hết cho {m}?',ans,[m*m,m*m-1,(kk-1)*m*m,m*m*kk+1 if kk>2 else 2*m],f'Mỗi cặp thuộc một "hộp" theo (x mod {m}, y mod {m}): có {m}·{m} = {m*m} hộp. Cần {kk-1}·{m*m}+1 = {ans} cặp để chắc chắn có {kk} cặp cùng hộp.',level=3,topic='Dirichlet – đồng dư')
    # 4. đồng dư đơn giản
    for _ in range(25):
        n=rng.randint(3,15)
        B.add(f'Trong {n+1} số nguyên bất kỳ, chắc chắn có hai số mà hiệu của chúng chia hết cho:',n,[n+1,n-1,2*n,n+2],f'Có {n} lớp dư mod {n}; {n+1} số ⇒ hai số cùng dư ⇒ hiệu chia hết cho {n}.',level=2,topic='Dirichlet – đồng dư')
    # 5. bi màu/kích thước (dạng đề trắc nghiệm)
    for _ in range(30):
        L=rng.randint(2,30); C=rng.randint(2,5); m=rng.randint(3,15)
        B.add(f'Hộp chứa vô hạn bi, mỗi viên thuộc một trong {L} loại kích thước và một trong {C} màu. Cần lấy ít nhất bao nhiêu viên để chắc chắn có {m} viên giống nhau cả loại lẫn màu?',(m-1)*L*C+1,[m*L*C,(m-1)*L*C,(m-1)*(L+C)+1,m*(L+C)],f'Có {L}·{C} = {L*C} kiểu bi (quy tắc nhân). Cần ({m}−1)·{L*C}+1 = {(m-1)*L*C+1}.',level=2,topic='Dirichlet tổng quát')
    # 6. tồn tại thật: chỉ giữ các tình huống KHÔNG THỂ xảy ra (chứng minh bằng tính chẵn lẻ)
    for n in [35,45,51,61,71,101,99,25,31]:
        k=n//2+1
        if k%2==0: k+=1
        B.add(f'Trong bữa tiệc có {n} khách, một người quan sát báo rằng có đúng {k} khách đã bắt tay một số LẺ lần. Nhận định nào đúng?','Người quan sát chắc chắn đếm sai',['Điều đó luôn xảy ra','Chỉ xảy ra khi số khách chẵn','Không xác định được nếu chưa biết ai bắt tay ai'],f'Tổng số lần bắt tay đếm theo từng người = 2·(số cái bắt tay) là số chẵn. Tổng đó ≡ (số người bắt tay lẻ lần) (mod 2), nên số người bắt tay lẻ lần phải chẵn. {k} là số lẻ ⇒ vô lý (bổ đề bắt tay).',level=3,topic='Chứng minh tồn tại')
    for n in [35,45,51,61,71,101]:
        a=rng.randint(3,n//2)
        while True:
            b=n-a; x=rng.choice([5,7,9,11]); y=rng.choice([3,5,7,9])
            if (a*x+b*y)%2==1: break
            a=rng.randint(3,n//2)
        B.add(f'Bữa tiệc có {n} khách: {a} người bắt tay đúng {x} người, {b} người bắt tay đúng {y} người. Kết luận nào chắc chắn đúng?','Tình huống này không thể xảy ra',['Tình huống luôn xảy ra','Chỉ xảy ra khi số khách chẵn','Không kết luận được'],f'Tổng bậc = {a}·{x} + {b}·{y} = {a*x+b*y} là số LẺ, nhưng tổng bậc phải bằng 2·(số cái bắt tay) là số chẵn ⇒ không thể.',level=3,topic='Chứng minh tồn tại')
    for n in [45,51,61,71,25,35,101]:
        B.add(f'{n} học sinh đăng ký khối A hoặc khối B, xếp thành vòng tròn. Khẳng định nào chắc chắn đúng?' ,'Luôn có hai bạn đứng cạnh nhau cùng khối' if n%2 else 'Không chắc: có thể xen kẽ hoàn toàn A, B',['Luôn có hai bạn cùng khối cạnh nhau' if n%2==0 else 'Không chắc: có thể xen kẽ hoàn toàn A, B','Luôn xen kẽ hoàn toàn','Số bạn khối A bằng số bạn khối B'],f'Nếu không có hai bạn kề nhau cùng khối thì các khối phải xen kẽ A,B,A,B,… trên vòng tròn ⇒ số người phải CHẴN. Với n = {n} '+('lẻ nên điều đó không thể ⇒ chắc chắn tồn tại hai bạn kề cùng khối (phản chứng).' if n%2 else 'chẵn nên vẫn có thể xen kẽ hoàn toàn, không chắc chắn.'),level=3,topic='Chứng minh tồn tại')
    # 7. khái niệm về phản chứng / dirichlet
    con=[('Nguyên lý Dirichlet (chuồng bồ câu) phát biểu: nếu xếp n+1 đồ vật vào n hộp thì','có ít nhất một hộp chứa ≥ 2 đồ vật',['mọi hộp chứa đúng 1 đồ vật','có ít nhất một hộp rỗng','có ít nhất một hộp chứa ≥ 3 đồ vật']),
         ('Để chứng minh bằng phản chứng mệnh đề P ⇒ Q ta','giả sử P đúng và Q sai, suy ra mâu thuẫn',['giả sử P sai, chứng minh Q đúng','giả sử P và Q đều đúng','kiểm tra vài ví dụ thỏa P và Q']),
         ('Phản ví dụ dùng để chứng minh mệnh đề dạng ∀x P(x) là','sai',['đúng','đúng với xác suất cao','không kết luận được gì']),
         ('Phát biểu nào là hệ quả đúng của Dirichlet tổng quát khi xếp N đồ vật vào k hộp?','có hộp chứa ít nhất ⌈N/k⌉ đồ vật',['mọi hộp chứa ít nhất ⌈N/k⌉ đồ vật','có hộp chứa nhiều nhất ⌊N/k⌋ đồ vật và ít nhất ⌈N/k⌉','mọi hộp chứa ⌊N/k⌋ đồ vật']),
         ('Tổng bậc của mọi đỉnh trong một đồ thị vô hướng (bổ đề bắt tay) luôn là số','chẵn',['lẻ','nguyên tố','bằng số đỉnh'])]
    for q,a,w in con: B.add(q,a,w,'Nhắc lại lý thuyết Chương 5 (Bài toán tồn tại): phản chứng, phản ví dụ, nguyên lý Dirichlet.',level=1,topic='Khái niệm')
    for _ in range(20):
        k=rng.randint(4,20); n=k*rng.randint(2,6)+rng.randint(1,k-1)
        B.add(f'Xếp {n} chiếc tất vào {k} ngăn kéo. Số lớn nhất m sao cho CHẮC CHẮN có một ngăn chứa ≥ m chiếc là:',math.ceil(n/k),[n//k,math.ceil(n/k)+1,n-k,math.ceil(n/k)-1],f'm = ⌈{n}/{k}⌉ = {math.ceil(n/k)} vì {n} không chia hết cho {k}. Lưu ý n//k = {n//k} (làm tròn xuống) là sai.',level=2,topic='Dirichlet tổng quát')
    # 8. Dirichlet ứng dụng: trong n số, tập con tổng chia hết cho n
    for n in range(3,14):
        B.add(f'Từ {n} số nguyên bất kỳ luôn chọn được một số liên tiếp (một đoạn) có tổng chia hết cho:',n,[n-1,n+1,2*n,'không luôn tồn tại'],f'Xét các tổng riêng S₀=0, S₁, …, S_{n}: {n+1} số có {n} lớp dư mod {n} ⇒ hai tổng cùng dư ⇒ đoạn giữa chúng có tổng chia hết cho {n}.',level=3,topic='Chứng minh tồn tại')
    return B
def essays(B):
    ex=[('Trong một kỳ thi trắc nghiệm gồm 40 câu, mỗi câu đúng được 0,25 điểm (sai/bỏ = 0). Cần ít nhất bao nhiêu thí sinh để chắc chắn có ít nhất 12 thí sinh cùng điểm? (đề 2019-2020)','Số mức điểm = 40+1 = 41. Cần 41·(12−1)+1 = 452 thí sinh.'),
        ('Chứng minh rằng trong 5 điểm bất kỳ nằm trong một tam giác đều cạnh 1 luôn có hai điểm có khoảng cách ≤ 1/2.','Chia tam giác thành 4 tam giác đều nhỏ cạnh 1/2 (nối trung điểm ba cạnh). 5 điểm vào 4 tam giác ⇒ có tam giác chứa ≥ 2 điểm; hai điểm trong một tam giác cạnh 1/2 cách nhau ≤ 1/2.'),
        ('Chứng minh rằng trong 13 người bất kỳ có hai người sinh cùng tháng.','12 tháng là 12 "hộp", 13 người là 13 "vật": theo Dirichlet có hộp chứa ≥ 2 người.'),
        ('Cho tập S = {1,2,…,10}. Chọn 6 số bất kỳ từ S. Chứng minh tồn tại hai số có tổng bằng 11.','Chia S thành 5 cặp: {1,10},{2,9},{3,8},{4,7},{5,6} (tổng 11). Chọn 6 số vào 5 cặp ⇒ có cặp chứa cả hai số ⇒ tổng 11.'),
        ('Một lớp có 45 học sinh xếp vòng tròn, mỗi bạn thi khối A hoặc B. Chứng minh có hai bạn đứng cạnh nhau cùng khối. (đề 2023-2024)','Phản chứng: giả sử không có hai bạn kề cùng khối. Khi đó các khối xen kẽ A,B,A,B,… quanh vòng tròn nên số người phải chẵn. Nhưng 45 lẻ ⇒ mâu thuẫn.'),
        ('Bữa tiệc 35 khách: 20 người bắt tay đúng 10 người, 15 người bắt tay đúng 5 người. Chứng minh người quan sát đếm nhầm. (đề 2023-2024)','Tổng số lần bắt tay đếm theo người = 20·10 + 15·5 = 275 lẻ. Nhưng mỗi cái bắt tay được tính đúng 2 lần nên tổng phải chẵn ⇒ mâu thuẫn.'),
        ('Chứng minh trong 7 số nguyên bất kỳ luôn có hai số mà hiệu (hoặc tổng) chia hết cho 10.','Xét dư khi chia 10 và nhóm {0},{1,9},{2,8},{3,7},{4,6},{5}: có 6 nhóm; 7 số ⇒ hai số cùng nhóm ⇒ cùng dư (hiệu chia hết cho 10) hoặc dư bù nhau (tổng chia hết cho 10).'),
        ('Hộp có bi to/vừa/nhỏ và 3 màu (xanh, đỏ, vàng), số lượng mỗi loại không hạn chế. Lấy ít nhất bao nhiêu viên để chắc chắn có 4 viên giống nhau cả kích thước lẫn màu? (đề 2023-2024)','Có 3·3 = 9 kiểu bi; cần 9·(4−1)+1 = 28 viên.')]
    for q,s in ex: B.essay(q,s,level=3,topic='Dirichlet & tồn tại')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items)); import collections; print(collections.Counter(i['topic'] for i in B.items))
