from hx import *
import sys, os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'orig'))
import knap, gen_m12 as G12
from cpp_snippets import CPP
def ol(steps): return '<ol>'+''.join(f'<li>{s}</li>' for s in steps)+'</ol>'
def tr(v,w,b,unl=False):
    r=knap.bb(v,w,b,unl); return r,G12.trace_text(v,w,b,r,unl)
def module():
    parts=[]
    rt,tt=tr([10,5,3,6],[5,3,2,4],8,True)          # ví dụ giáo trình (số lượng không hạn chế)
    r1,t1=tr([3,5,7,4],[2,4,3,2],9)               # đề 2023-24 đề 01
    r2,t2=tr([5,2,7,1],[5,3,6,4],9)               # đề 2017-2020
    s=[]
    s.append(sl('<p><b>Bài toán tối ưu tổ hợp</b>: trong tập hữu hạn D các phương án, tìm phương án làm hàm mục tiêu f lớn nhất (hoặc nhỏ nhất). Hai thuật toán của TRR1: <b>duyệt toàn bộ</b> (đúng nhưng chậm) và <b>nhánh cận</b> (đúng và cắt bớt nhánh). Câu 5 của mọi đề PTIT là bài cái túi: 2017–2020 dùng duyệt toàn bộ, 2023–2024 dùng nhánh cận.</p>'+ul(['Mô hình cái túi và duyệt toàn bộ','Cận trên g và nguyên tắc cắt nhánh','Chạy thuật toán nhánh cận từng bước','Cái túi biến nguyên (ví dụ giáo trình)']),'MODULE 12 · Giáo trình 2016 §4.1–4.3 · Đề cương 4.2–4.3','Duyệt toàn bộ và nhánh cận: bài toán cái túi'))
    s.append(sl(formula('Bài toán cái túi 0/1','f(x) = Σ cⱼxⱼ → max;   Σ aⱼxⱼ ≤ b;   xⱼ ∈ {0,1}',[('cⱼ','giá trị của vật j'),('aⱼ','trọng lượng của vật j'),('b','sức chứa của túi')])+'<p>Tập phương án D = {x ∈ {0,1}ⁿ : Σ aⱼxⱼ ≤ b}; có tối đa 2ⁿ vectơ để kiểm tra.</p>','PHẦN 1 · Nền tảng','Mô hình cái túi'))
    s.append(sl('<pre><code>Bước 1: XOPT = ∅;  FOPT = −∞  (max)   hoặc +∞ (min)\nBước 2: for each X ∈ D {\n           S = f(X);\n           if (FOPT &lt; S) { FOPT = S; XOPT = X; }\n        }\nBước 3: return (XOPT, FOPT)</code></pre>'+callout('warn','Nhược điểm','Số phương án bùng nổ: 15! ≈ 1,3·10¹² hoán vị cần hơn 36 giờ (giáo trình). Với cái túi 2ⁿ: n = 50 đã cần hơn một triệu giây ở tốc độ 10⁹ phép/giây.'),'PHẦN 1 · Nền tảng','Thuật toán duyệt toàn bộ',
        explain='Duyệt toàn bộ: thử mọi cách chọn đồ vật, bỏ cách nào quá nặng, giữ cách có giá trị lớn nhất.'))
    parts.append(dict(title='Nền tảng',bullets=['Mô hình cái túi','Duyệt toàn bộ'],slides=s))
    s=[]
    s.append(sl(formula('Cận trên của phương án bộ phận','g(u₁,…,u_k) = δ_k + c_{k+1}·b_k / a_{k+1}',[('δ_k','giá trị các vật đã chọn (c₁u₁ + … + c_ku_k)'),('b_k','trọng lượng còn lại của túi'),('c_{k+1}/a_{k+1}','tỉ số giá trị/trọng lượng lớn nhất trong các vật còn lại')])+callout('info','Vì sao là cận trên','Sắp các vật theo c/a giảm dần (c₁/a₁ ≥ c₂/a₂ ≥ …). Bài toán biến liên tục (cho phép lấy phân số vật) có phương án tối ưu là dồn toàn bộ phần còn lại vào vật có c/a lớn nhất: giá trị ≥ giá trị nguyên. Nên g ≥ mọi phương án mở rộng.'),'PHẦN 2 · Phương pháp','Hàm cận g',
        explain='Đây là “ước lượng lạc quan”: nếu ngay cả ước lượng lạc quan nhất của một nhánh cũng không hơn kỷ lục đang có thì không cần xem nhánh đó.'))
    s.append(sl(ol(['Sắp xếp các vật theo cⱼ/aⱼ giảm dần (giữ thứ tự chỉ số khi bằng nhau).','FOPT = −∞. Quay lui: với vật thứ k, thử xₖ = 1 trước (nếu còn đủ chỗ), rồi xₖ = 0.','Tại nút bộ phận tính δ, w (trọng lượng còn lại), g.','Nếu k = n: cập nhật FOPT nếu δ > FOPT.','Nếu k < n: chỉ mở rộng khi g &gt; FOPT; ngược lại <b>cắt nhánh</b>.'])+'<pre><code>'+esc(CPP['knap_bb'])+'</code></pre>','PHẦN 2 · Phương pháp','Thuật toán nhánh cận (giáo trình hình 4.4)'))
    s.append(sl(sim('knap'),'PHẦN 2 · Phương pháp','Thực hành: giải cái túi từng nút'))
    parts.append(dict(title='Phương pháp: nhánh cận',bullets=['Hàm cận g','Thuật toán','Thực hành'],slides=s))
    s=[]
    s.append(sl(callout('info','Ví dụ giáo trình 2016 (số lượng không hạn chế)','10x₁ + 5x₂ + 3x₃ + 6x₄ → max; 5x₁ + 3x₂ + 2x₃ + 4x₄ ≤ 8; xⱼ nguyên không âm.')+'<pre style="font-size:.78em">'+esc(tt)+'</pre><p>Đối chiếu giáo trình: g gốc = 16, nút (1): g = 15, (1,0): g = 14,5 bị cắt, (0): g = 40/3 bị cắt; kết quả f* = 15. (Giáo trình in x* = (1,1,0,1) do lỗi trích; phương án hợp lệ là (1,1,0,0).)</p>','PHẦN 3 · Ví dụ','Ví dụ 1: ví dụ giáo trình'))
    s.append(sl(callout('info','Ví dụ 2 (đề 2023–2024, đề 01, câu 5b)','3x₁ + 5x₂ + 7x₃ + 4x₄ → max; 2x₁ + 4x₂ + 3x₃ + 2x₄ ≤ 9; xⱼ ∈ {0,1}.')+'<pre style="font-size:.78em">'+esc(t1)+'</pre>','PHẦN 3 · Ví dụ','Ví dụ 2: đề thi 2023–2024'))
    s.append(sl(callout('info','Ví dụ 3 (đề 2017–2020, câu 5b): duyệt toàn bộ','5x₁ + 2x₂ + 7x₃ + x₄ → max; 5x₁ + 3x₂ + 6x₃ + 4x₄ ≤ 9.')+'<p>Duyệt 16 vectơ: các phương án khả thi tốt nhất: '+f'x* = {r2["xopt"]}, f* = {r2["fopt"]}. Bảng đầy đủ nằm trong phần chi tiết.</p>'+'<pre style="font-size:.78em">'+esc(t2)+'</pre>','PHẦN 3 · Ví dụ','Ví dụ 3: đề thi 2017–2020'))
    s.append(sl(callout('info','Ví dụ 4 (ngân hàng 4.1)','5x₁ + x₂ + 9x₃ + 3x₄ → max; 4x₁ + 2x₂ + 7x₃ + 3x₄ ≤ 10; xⱼ ∈ {0,1}.')+'<pre style="font-size:.78em">'+esc(tr([5,1,9,3],[4,2,7,3],10)[1])+'</pre>','PHẦN 3 · Ví dụ','Ví dụ 4: ngân hàng câu hỏi 2019'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)',bullets=['Giáo trình','Đề 2023–2024','Đề 2017–2020','Ngân hàng 2019'],slides=s))
    s=[]
    s.append(sl(ul(['<b>Quên sắp theo c/a</b> ⇒ cận sai, có thể cắt nhầm nhánh chứa nghiệm.','<b>Cắt nhầm dấu:</b> cắt khi g ≤ FOPT, mở rộng khi g &gt; FOPT.','<b>Cập nhật kỷ lục chỉ tại lá</b> (k = n).','<b>Lấy bằng nhau c/a:</b> giữ thứ tự chỉ số; kết quả tối ưu vẫn đúng.','<b>Khi trình bày:</b> ghi rõ (x…), δ, w, g ở mỗi nút và nêu nút bị loại.']),'PHẦN 4 · Bẫy và mở rộng','Năm bẫy thường gặp'))
    s.append(sl('<p>Nhánh cận trong trường hợp xấu nhất vẫn là O(2ⁿ) (không cắt được nhánh nào), nhưng với cận tốt thường giải được n hàng chục đến hàng trăm. Quy hoạch động cho cái túi 0/1 chạy O(n·b) giả đa thức, phù hợp khi b nhỏ.</p>','PHẦN 4 · Bẫy và mở rộng','Mở rộng: so sánh với quy hoạch động'))
    parts.append(dict(title='Bẫy và mở rộng',bullets=['Năm bẫy','Quy hoạch động'],slides=s))
    s=[]
    s.append(sl('<p>Chất hàng lên xe tải, chọn dự án đầu tư dưới ràng buộc ngân sách, chọn tính năng phát hành trong một sprint đều là cái túi. Nhánh cận là nền của bộ giải tối ưu nguyên (integer programming).</p>','PHẦN 5 · Ứng dụng và ôn tập','Case study: chọn dự án theo ngân sách'))
    s.append(sl(ul(['Sắp c/a, tính g = δ + c·w/a, cắt khi g ≤ FOPT.','Trình bày bảng các nút.','Đối chiếu với duyệt toàn bộ khi n nhỏ.'])+callout('good','Tiếp theo','Module 13: nhánh cận cho bài toán người du lịch.'),'PHẦN 5 · Ứng dụng và ôn tập','Tổng kết'))
    parts.append(dict(title='Ứng dụng và tổng kết',bullets=['Chọn dự án','Checklist'],slides=s))
    rb,tb=tr([9,1,5,1],[7,2,4,1],8)
    notes='<h2>1. Nội dung chi tiết</h2><p>Nhánh cận là quay lui có kiểm tra cận. Giáo trình 2016 chứng minh mệnh đề: với c₁/a₁ ≥ … ≥ cₙ/aₙ, phương án tối ưu của bài toán biến liên tục là x₁ = b/a₁, còn lại 0, giá trị c₁b/a₁; từ đó suy ra cận g cho phương án bộ phận.</p><h2>2. Ví dụ chi tiết có lời giải</h2>'
    notes+=ex('1. Duyệt toàn bộ (ngân hàng 4.6)','<p>9x₁ + x₂ + 5x₃ + x₄ → max; 7x₁ + 2x₂ + 4x₃ + x₄ ≤ 8: bảng nhánh cận và kết quả:</p><pre style="font-size:.78em">'+esc(tb)+'</pre>')
    notes+=ex('2. Đề 2023–2024 đề 02','<pre style="font-size:.78em">'+esc(tr([6,5,3,1],[4,4,2,1],9)[1])+'</pre>')
    notes+=ex('3. Đề 2023–2024 đề 03','<pre style="font-size:.78em">'+esc(tr([5,5,3,8],[3,4,2,5],12)[1])+'</pre>')
    notes+=ex('4. Slide PTIT, Exercise 1','<pre style="font-size:.78em">'+esc(tr([7,4,2],[4,3,2],6)[1])+'</pre>')
    notes+=ex('5. Lưu ý về thứ tự xét','<p>Đề 02 (2023–2024) có hai vật cùng tỉ số c/a = 1,5 (x₁ = 6/4 và x₃ = 3/2): ta giữ thứ tự chỉ số. Kết quả tối ưu không phụ thuộc thứ tự, nhưng cây tìm kiếm có thể khác; giám khảo chấp nhận mọi thứ tự hợp lệ khi f* đúng.</p>')
    notes+='<h2>3. Thực hành tương tác</h2><p>Nhập c, a, b (tối đa 8 vật); công cụ in bảng nút, đối chiếu duyệt toàn bộ.</p>'+sim('knap')
    notes+='<h2>4. Bối cảnh lý thuyết và lịch sử</h2>'+callout('info','📜 Nguồn gốc','Tên “knapsack problem” được George Dantzig phổ biến trong thập niên 1950 (bài báo 1957). Thuật toán nhánh cận do Ailsa Land và Alison Doig đề xuất năm 1960 cho quy hoạch nguyên.')
    notes+='<h2>5. Case study</h2><p>Chọn tính năng cho một bản phát hành với ngân sách 20 điểm công: mỗi tính năng có giá trị kinh doanh cⱼ và chi phí aⱼ. Sắp theo c/a, nhánh cận loại nhanh các tổ hợp kém; với 30 tính năng vét cạn cần 2³⁰ ≈ 10⁹ tổ hợp, nhánh cận thường chỉ xét hàng nghìn nút.</p><h2>6. Bẫy khi làm bài</h2>'+callout('warn','Chú ý','• Trình bày đủ ba cột: δ, w, g và trạng thái của nút.<br>• Chỉ rõ thứ tự biến sau khi sắp và ánh xạ lại thành x₁…xₙ gốc ở kết quả.<br>• Với duyệt toàn bộ: bảng đủ 2ⁿ dòng, đánh dấu phương án bị loại.')
    return dict(id='m12',slug='12-cai-tui-nhanh-can',title='Duyệt toàn bộ và nhánh cận: bài toán cái túi',subtitle='Duyệt toàn bộ, hàm cận g, nhánh cận, cái túi 0/1 và biến nguyên',source='Giáo trình 2016 §4.1–4.3 · Đề cương INT1358 mục 4.2–4.3 · Slide chương Tối ưu',exam='Câu 5 mọi đề (2017–2024)',time='≈ 3 giờ',
        objectives=['Chạy duyệt toàn bộ và nhánh cận cho cái túi 0/1','Tính đúng δ, w, g ở từng nút','Cắt nhánh đúng quy tắc g ≤ FOPT','Trình bày kết quả theo từng bước như đề yêu cầu'],parts=parts,notes=notes,sims=['knap'])
