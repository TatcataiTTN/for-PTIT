from hx import *
import sys, os, itertools
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'orig'))
import tsp as TS
from tsp import INF
def ol(steps): return '<ol>'+''.join(f'<li>{s}</li>' for s in steps)+'</ol>'
def mat(C): return '\n'.join('  '+' '.join(f'{("∞" if i==j else x):>3}' for j,x in enumerate(row)) for i,row in enumerate(C))
def logtxt(res,limit=40):
    lines=[f'Cận dưới ở gốc sau rút gọn = {res["root"]}.']
    for e in res['log'][:limit]:
        d,l,bd,st=e[0],e[1],e[2],e[3]
        tail={'branch':f'→ chọn cạnh {e[4] if len(e)>4 else ""} (β = {e[5] if len(e)>5 else ""})','record':f'★ hành trình đầy đủ, chi phí {e[4] if len(e)>4 else ""}','leaf':'lá (không cải thiện)','cut':'✗ cắt (cận dưới ≥ kỷ lục)','dead':'✗ vô nghiệm','root':''}[st]
        lines.append('  '*d+f'[{l}] cận dưới = {bd} {tail}')
    lines.append('Hành trình tối ưu: '+'→'.join(map(str,res['tour']))+f', chi phí {res["cost"]}.')
    return '\n'.join(lines)
def module():
    parts=[]
    R=[[0,3,93,13,33,9],[4,0,77,42,21,16],[45,17,0,36,16,28],[39,90,80,0,56,7],[28,46,88,33,0,25],[3,88,18,46,92,0]]
    rR=TS.bb(R)
    C44=[[0,31,15,23,10,17],[16,0,24,7,12,12],[34,3,0,25,54,25],[15,20,33,0,50,40],[16,10,32,3,0,23],[18,20,13,28,21,0]]
    r44=TS.bb(C44)
    A=[[INF if i==j else R[i][j] for j in range(6)] for i in range(6)]
    rs,rc,cc=TS.reduce([r[:] for r in A],list(range(6)),list(range(6)))
    # ma trận đề trắc nghiệm mẫu (n=5), chi phí 1→2→3→4→5→1
    Q=[[0,7,9,11,3],[9,0,21,8,9],[12,13,0,8,20],[3,8,21,0,18],[15,20,20,19,0]]
    idc=sum(Q[i][(i+1)%5] for i in range(5)); qb=TS.bb(Q)
    s=[]
    s.append(sl('<p><b>Bài toán người du lịch (TSP)</b>: n thành phố, chi phí cᵢⱼ từ i đến j; tìm hành trình xuất phát từ một thành phố, qua mỗi thành phố đúng một lần rồi quay về với tổng chi phí nhỏ nhất. Có (n − 1)! hành trình (bất đối xứng) nên vét cạn không khả thi khi n lớn. Giáo trình 2016 §4.4 giải bằng <b>nhánh cận với thủ tục rút gọn ma trận</b>.</p>'+ul(['Thủ tục rút gọn ma trận và cận dưới','Chọn cạnh phân nhánh (r, c)','Nhánh chứa và không chứa cạnh; cấm chu trình con','Cây tìm kiếm và kỷ lục']),'MODULE 13 · Giáo trình 2016 §4.4 · Đề cương 4.3 (ví dụ)','Nhánh cận: bài toán người du lịch'))
    s.append(sl(formula('Thủ tục rút gọn','trừ min mỗi dòng, rồi min mỗi cột;  cận dưới = tổng các hằng số đã trừ')+f'<p>Ví dụ giáo trình (n = 6): tổng hằng số dòng = {rs-sum(cc)}, tổng hằng số cột = {sum(cc)} ⇒ cận dưới = <b>{rs}</b>.</p>'+'<pre style="font-size:.8em">'+esc(mat(R))+'</pre>'+callout('info','Vì sao là cận dưới','Mọi hành trình dùng đúng một phần tử mỗi dòng và mỗi cột; trừ h khỏi cả một dòng làm chi phí MỌI hành trình giảm h. Ma trận sau rút gọn không âm nên chi phí gốc ≥ tổng hằng số.'),'PHẦN 1 · Nền tảng','Rút gọn ma trận'))
    parts.append(dict(title='Nền tảng',bullets=['Bài toán TSP','Rút gọn ma trận'],slides=s))
    s=[]
    s.append(sl(formula('Chọn cạnh phân nhánh','chọn số 0 tại (r,c) có θ = min(dòng r, bỏ ô đó) + min(cột c, bỏ ô đó) lớn nhất')+'<ul><li><b>Nhánh không chứa (r,c):</b> đặt C[r][c] = ∞, rút gọn lại: cận dưới tăng đúng θ.</li><li><b>Nhánh chứa (r,c):</b> bỏ dòng r và cột c; đặt ô đóng chu trình con (j_k, i₁) = ∞; rút gọn, cộng vào cận dưới.</li></ul><p>Ưu tiên nhánh <b>chứa</b> trước. Khi ma trận còn 2×2 kết nạp nốt hai cạnh để được hành trình đầy đủ.</p>','PHẦN 2 · Phương pháp','Phân nhánh trái và phải'))
    s.append(sl(ol(['Rút gọn ma trận gốc, được cận dưới L₀.','Chọn (r,c) theo θ lớn nhất; sinh hai nút con.','Đi xuống nhánh chứa cho tới khi được hành trình đầy đủ: kỷ lục đầu tiên.','Quay lại các nút còn lại: cắt nếu cận dưới ≥ kỷ lục, ngược lại phát triển tiếp.'])+viz('tsp'),'PHẦN 2 · Phương pháp','Quy trình và hoạt ảnh từng bước'))
    parts.append(dict(title='Phương pháp',bullets=['Chọn cạnh, hai nhánh','Quy trình'],slides=s))
    s=[]
    s.append(sl(callout('info','Ví dụ giáo trình (n = 6)','Ma trận ở trên.')+'<pre style="font-size:.75em">'+esc(logtxt(rR,30))+'</pre><p>Khớp giáo trình: cạnh (6,3) β = 48 nên nhánh không chứa có cận 81 + 48 = 129; tiếp theo (4,6) β = 32; (2,1) β = 20; (1,4); được hành trình 1→4→6→3→5→2→1 chi phí 104.</p>','PHẦN 3 · Ví dụ','Ví dụ 1: ví dụ giáo trình (kết quả 104)'))
    s.append(sl(callout('info','Ví dụ 2 (ngân hàng 4.4)','Ma trận n = 6 (∞ đường chéo).')+'<pre style="font-size:.75em">'+esc(mat(C44))+'</pre><pre style="font-size:.75em">'+esc(logtxt(r44,24))+'</pre>','PHẦN 3 · Ví dụ','Ví dụ 2: ngân hàng câu hỏi 2019'))
    s.append(sl(callout('info','Ví dụ 3 (đề ôn trắc nghiệm)','n = 5. “Phương án f* được cập nhật đầu tiên”.')+'<pre style="font-size:.8em">'+esc(mat(Q))+'</pre>'+f'<p>Theo cách đọc khớp các đề trắc nghiệm còn nguyên phương án (quay lui theo chỉ số tăng dần): hành trình đầu tiên là 1→2→3→4→5→1 với chi phí 7 + 21 + 8 + 18 + 15 = <b>{idc}</b>. Tối ưu thật của ma trận này: {qb["cost"]}.</p>','PHẦN 3 · Ví dụ','Ví dụ 3: f* đầu tiên (trắc nghiệm)'))
    parts.append(dict(title='Ví dụ có lời giải',bullets=['Ví dụ giáo trình','Ngân hàng 4.4','Đề trắc nghiệm'],slides=s))
    s=[]
    s.append(sl(ul(['<b>Quên cấm chu trình con</b> ở nhánh chứa.','<b>Tính θ sai:</b> loại chính ô 0 đang xét khi tìm min dòng và min cột.','<b>Đọc đề trắc nghiệm:</b> “f* cập nhật đầu tiên” không phải chi phí tối ưu.','<b>Rút gọn lại</b> ma trận sau mỗi lần đặt ∞ hoặc bỏ dòng/cột.','<b>Chia nhánh sai thứ tự:</b> luôn nhánh chứa trước.']),'PHẦN 4 · Bẫy và mở rộng','Năm bẫy thường gặp'))
    s.append(sl('<p>TSP thuộc lớp NP-khó: chưa có thuật toán đa thức. Các bộ giải thực tế dùng nhánh cận/cắt phẳng và heuristic (láng giềng gần nhất, 2-opt). Phương pháp rút gọn ma trận này thuộc họ Little–Murty–Sweeney–Karel (1963).</p>','PHẦN 4 · Bẫy và mở rộng','Mở rộng: NP-khó và heuristic'))
    parts.append(dict(title='Bẫy và mở rộng',bullets=['Năm bẫy','NP-khó'],slides=s))
    s=[]
    s.append(sl('<p>Định tuyến giao hàng: 8 điểm giao có 7! = 5040 hành trình (bất đối xứng), vét cạn tức thì; 20 điểm có 19! ≈ 1,2·10¹⁷ hành trình, phải dùng nhánh cận hoặc heuristic.</p>','PHẦN 5 · Ứng dụng và ôn tập','Case study: định tuyến giao hàng'))
    s.append(sl(ul(['Rút gọn ma trận, tính cận dưới.','Chọn cạnh phân nhánh bằng θ.','Trình bày cây tìm kiếm và kết luận hành trình tối ưu.'])+callout('good','Hoàn thành TRR1','Bạn đã đi hết 4 loại bài toán tổ hợp: đếm, tồn tại, liệt kê, tối ưu. Ôn lại bằng mục Luyện đề và Cấu trúc đề thi.'),'PHẦN 5 · Ứng dụng và ôn tập','Tổng kết'))
    parts.append(dict(title='Ứng dụng và tổng kết',bullets=['Giao hàng','Checklist'],slides=s))
    notes='<h2>1. Nội dung chi tiết</h2><p>Sau khi chọn cạnh (r,c), nhánh chứa loại dòng r và cột c (đã đi từ r đến c). Nếu các cạnh đã chọn tạo đường đi i₁ → … → r → c → … → j_k thì cạnh (j_k, i₁) phải bị cấm để tránh chu trình con. Cận dưới của nhánh không chứa (r,c) bằng cận dưới của cha cộng θ.</p><h2>2. Ví dụ chi tiết có lời giải</h2>'
    notes+=ex('1. Ngân hàng 4.5 = ví dụ giáo trình','<p>Hành trình tối ưu 1→4→6→3→5→2→1, chi phí 104 (kiểm chứng bằng vét cạn 120 hành trình).</p>')
    notes+=ex('2. Ngân hàng 4.4','<p>Hành trình tối ưu '+'→'.join(map(str,r44['tour']))+f', chi phí {r44["cost"]}; cận dưới ở gốc {r44["root"]}.</p>')
    notes+=ex('3. Số hành trình','<p>n = 6: (n − 1)! = 120 hành trình; nếu ma trận đối xứng chỉ còn 60 hành trình khác nhau.</p>')
    notes+=ex('4. Tính chi phí một hành trình','<p>Với ma trận đề trắc nghiệm ở trên, hành trình 1→3→5→2→4→1 có chi phí c₁₃ + c₃₅ + c₅₂ + c₂₄ + c₄₁ = 9 + 20 + 20 + 8 + 3 = 60.</p>')
    notes+='<h2>3. Thực hành tương tác</h2><p>Nhập ma trận (mỗi dòng một hàng); công cụ in cây tìm kiếm và đối chiếu vét cạn (đã kiểm chứng với 300 ma trận ngẫu nhiên).</p>'+sim('tsp')
    notes+='<h2>4. Bối cảnh lý thuyết và lịch sử</h2>'+callout('info','📜 Nguồn gốc','Thuật toán nhánh cận có thủ tục rút gọn ma trận cho TSP được John Little, Katta Murty, Dura Sweeney và Caroline Karel công bố năm 1963. Bài toán người du lịch được nghiên cứu từ thế kỷ 19 (Hamilton, Kirkman) và là ví dụ điển hình của bài toán NP-khó.')
    notes+='<h2>5. Case study</h2><p>Chi phí đi lại giữa 6 kho: nhánh cận có cận dưới gốc 81 và kết quả 104 cho thấy khoảng cách chỉ 23 đơn vị, nên chỉ cần phát triển vài nhánh nhỏ thay vì 120 hành trình.</p><h2>6. Bẫy khi làm bài</h2>'+callout('warn','Chú ý','• Trình bày ma trận sau mỗi lần rút gọn.<br>• Ghi rõ cạnh cấm chu trình con.<br>• Kết luận hành trình bằng dãy thành phố và chi phí, đối chiếu tổng các cạnh.')
    return dict(id='m13',slug='13-nguoi-du-lich',title='Nhánh cận: bài toán người du lịch',subtitle='Rút gọn ma trận, chọn cạnh phân nhánh, cấm chu trình con',source='Giáo trình 2016 §4.4 · Đề cương INT1358 mục 4.3 · Slide chương Tối ưu',exam='Ngân hàng 4.4–4.5; đề ôn trắc nghiệm (cận và f* đầu tiên)',time='≈ 2,5 giờ',
        objectives=['Rút gọn ma trận và tính cận dưới','Chọn cạnh phân nhánh bằng θ','Phân nhánh chứa/không chứa, cấm chu trình con','Đọc đúng câu hỏi trắc nghiệm về f* đầu tiên'],parts=parts,notes=notes,sims=['tsp'])
