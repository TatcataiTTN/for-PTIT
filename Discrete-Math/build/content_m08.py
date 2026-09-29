from hx import *
import sys, os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'orig'))
import orig_nh as ON
def ol(steps): return '<ol>'+''.join(f'<li>{s}</li>' for s in steps)+'</ol>'
def sol(cs,a0):
    r=ON.rec_solve(cs,a0); return ON.fmt_sol(r)
def module():
    parts=[]
    s1=sol([-1,6],[1,5]); s2=sol([2,1,-2],[3,6,0]); s3=sol([-14,-49],[3,35]); s4=sol([14,-59,70],[-7,-20,-100]); s5=sol([7,-6][::1],[2,1])
    s=[]
    s.append(sl('<p>Đến đây ta giải hệ thức truy hồi <b>tuyến tính thuần nhất hệ số hằng</b>: aₙ = c₁aₙ₋₁ + … + c_kaₙ₋ₖ. Kỹ thuật là tìm nghiệm dạng rⁿ, dẫn tới phương trình đặc trưng. Câu 2b của mọi đề 2017–2020 và câu 3a của đề 2023–2024 đều thuộc dạng này (bậc 2 nghiệm kép: aₙ = −14aₙ₋₁ − 49aₙ₋₂).</p>'+ul(['Phương trình đặc trưng','Hai nghiệm phân biệt, nghiệm kép','Bậc 3 và nghiệm bội','Tìm hệ số từ điều kiện đầu, kiểm tra']),'MODULE 8 · Giáo trình 2016 §2.4.2 · Đề cương 2.4.3','Giải hệ thức truy hồi'))
    s.append(sl(formula('Phương trình đặc trưng','aₙ = c₁aₙ₋₁ + … + c_kaₙ₋ₖ  ⇒  r^k − c₁r^(k−1) − … − c_k = 0',[('r','nghiệm đặc trưng: aₙ = rⁿ là nghiệm ⇔ r thỏa phương trình này'),('bậc k','cần k điều kiện đầu')])+callout('info','Ví dụ','aₙ = aₙ₋₁ + 2aₙ₋₂ ⇒ r² − r − 2 = 0 ⇒ r = 2, r = −1.'),'PHẦN 1 · Nền tảng','Phương trình đặc trưng',
        explain='Thử nghiệm dạng aₙ = rⁿ vào hệ thức, chia cả hai vế cho r^(n−k) sẽ được đa thức theo r. Mọi nghiệm r của đa thức đều cho một nghiệm rⁿ.'))
    parts.append(dict(title='Nền tảng',bullets=['Phương trình đặc trưng'],slides=s))
    s=[]
    s.append(sl(formula('Định lý 1: hai nghiệm phân biệt r₁ ≠ r₂','aₙ = α·r₁ⁿ + β·r₂ⁿ')+formula('Định lý 2: nghiệm kép r₀','aₙ = (α + β·n)·r₀ⁿ')+formula('Nghiệm bội m','(α₀ + α₁n + … + α_(m−1)n^(m−1))·rⁿ')+'<p>Bậc k tổng quát: cộng các phần đóng góp của từng nghiệm, được đúng k hằng số; giải hệ k ẩn từ k điều kiện đầu.</p>','PHẦN 2 · Phương pháp','Ba dạng nghiệm'))
    s.append(sl(ol(['Viết phương trình đặc trưng, tìm mọi nghiệm (kể cả bội).','Viết dạng nghiệm tổng quát với hằng số α, β, …','Thay n = 0, 1, … vào điều kiện đầu, giải hệ.','Kiểm tra: tính a₂, a₃ bằng hệ thức và bằng công thức, phải khớp.'])+sim('rec'),'PHẦN 2 · Phương pháp','Quy trình giải'))
    s.append(sl('<p><b>Nghiệm phức:</b> nếu phương trình đặc trưng có nghiệm phức thì dùng dạng lượng giác (Định lý 3 của giáo trình); phần này không thuộc yêu cầu thi TRR1. Đề thi PTIT chỉ dùng nghiệm thực (nguyên).</p><p><b>Không thuần nhất bậc 1:</b> aₙ = aₙ₋₁ + f(n) giải bằng phương pháp lặp: aₙ = a₀ + Σᵢ f(i).</p>','PHẦN 2 · Phương pháp','Ghi chú phạm vi'))
    parts.append(dict(title='Phương pháp',bullets=['Ba dạng nghiệm','Quy trình giải','Phạm vi'],slides=s))
    s=[]
    s.append(sl(callout('info','Ví dụ 1 (đề 2017–2020, câu 2b)','aₙ = −14aₙ₋₁ − 49aₙ₋₂, n ≥ 2, a₀ = 3, a₁ = 35.')+ol(['r² + 14r + 49 = 0 ⇔ (r + 7)² = 0 ⇒ nghiệm kép r = −7.','aₙ = (α + βn)(−7)ⁿ. a₀ = α = 3; a₁ = (3 + β)(−7) = 35 ⇒ β = −8.',f'<b>{s3}</b>. Kiểm tra a₂ = −14·35 − 49·3 = −637 = (3 − 16)·49 ✓.']),'PHẦN 3 · Ví dụ','Ví dụ 1: nghiệm kép'))
    s.append(sl(callout('info','Ví dụ 2 (2.2.1a)','aₙ = −aₙ₋₁ + 6aₙ₋₂, a₀ = 1, a₁ = 5.')+ol(['r² + r − 6 = 0 ⇒ r = 2, r = −3.','α + β = 1; 2α − 3β = 5 ⇒ α = 8/5, β = −3/5.',f'<b>{s1}</b>. (a₂ = −5 + 6 = 1; công thức: (8/5)·4 − (3/5)·9 = 32/5 − 27/5 = 1 ✓.)']),'PHẦN 3 · Ví dụ','Ví dụ 2: hai nghiệm phân biệt'))
    s.append(sl(callout('info','Ví dụ 3 (2.1.16a)','aₙ = 2aₙ₋₁ + aₙ₋₂ − 2aₙ₋₃, n ≥ 3, a₀ = 3, a₁ = 6, a₂ = 0.')+ol(['r³ − 2r² − r + 2 = 0 ⇔ (r − 2)(r − 1)(r + 1) = 0.','aₙ = α·2ⁿ + β·1ⁿ + γ·(−1)ⁿ.',f'Giải hệ ba ẩn: <b>{s2}</b>.']),'PHẦN 3 · Ví dụ','Ví dụ 3: bậc 3 ba nghiệm'))
    s.append(sl(callout('info','Ví dụ 4 (đề ôn trắc nghiệm)','aₙ₊₃ = 14aₙ₊₂ − 59aₙ₊₁ + 70aₙ, a₀ = −7, a₁ = −20, a₂ = −100.')+ol(['r³ − 14r² + 59r − 70 = 0 ⇔ (r − 2)(r − 5)(r − 7) = 0.',f'<b>{s4}</b>. Kiểm tra a₃ = 14(−100) − 59(−20) + 70(−7) = −710 và công thức: −56 + 375 − 1029 = −710 ✓.']),'PHẦN 3 · Ví dụ','Ví dụ 4: bậc 3 (đề trắc nghiệm)'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)',bullets=['Nghiệm kép','Hai nghiệm','Bậc 3'],slides=s))
    s=[]
    s.append(sl(ul(['<b>Dấu của phương trình đặc trưng:</b> aₙ = 6aₙ₋₁ − 9aₙ₋₂ ⇒ r² − 6r + 9 = 0. <b>Giáo trình 2016 ví dụ 3 chép nhầm thành r² − 6r − 9 = 0</b>; đúng là (r − 3)² = 0.','<b>Nghiệm kép</b> phải có nhân tử n: (α + βn)rⁿ.','<b>Nghiệm âm:</b> ghi (−7)ⁿ có ngoặc.','<b>Thiếu điều kiện đầu:</b> đề 2.2.26a chỉ cho aₙ = 14aₙ₋₁ − 49aₙ₋₂; chỉ có dạng tổng quát (α + βn)7ⁿ.','<b>Kiểm tra:</b> so a₂, a₃ tính từ hệ thức và từ công thức.']),'PHẦN 4 · Bẫy và mở rộng','Năm bẫy thường gặp'))
    s.append(sl('<p>Fibonacci: fₙ = fₙ₋₁ + fₙ₋₂, f₀ = 0, f₁ = 1. r² − r − 1 = 0 ⇒ r = (1 ± √5)/2. fₙ = (1/√5)[((1+√5)/2)ⁿ − ((1−√5)/2)ⁿ] (công thức Binet).</p>','PHẦN 4 · Bẫy và mở rộng','Mở rộng: công thức Binet'))
    parts.append(dict(title='Bẫy và mở rộng',bullets=['Năm bẫy','Fibonacci'],slides=s))
    s=[]
    s.append(sl('<p>Tính fₙ: đệ quy ngây thơ O(φⁿ), bảng động O(n), nhân ma trận hoặc công thức Binet O(log n). Giải được hệ thức truy hồi cho phép chọn thuật toán tốt nhất.</p>','PHẦN 5 · Ứng dụng và ôn tập','Case study: tính Fibonacci'))
    s.append(sl(ul(['Thuộc ba dạng nghiệm.','Không nhầm dấu ở phương trình đặc trưng.','Luôn kiểm tra a₂.'])+callout('good','Tiếp theo','Module 9: hàm sinh, một cách tiếp cận khác cho đếm và truy hồi.'),'PHẦN 5 · Ứng dụng và ôn tập','Tổng kết'))
    parts.append(dict(title='Ứng dụng và tổng kết',bullets=['Tính Fibonacci','Checklist'],slides=s))
    notes='<h2>1. Nội dung chi tiết</h2><p>Nếu r là nghiệm của r² = c₁r + c₂ thì aₙ = rⁿ thỏa aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ vì c₁rⁿ⁻¹ + c₂rⁿ⁻² = rⁿ⁻²(c₁r + c₂) = rⁿ. Tổ hợp tuyến tính của nghiệm cũng là nghiệm; với hai nghiệm phân biệt, hai điều kiện đầu xác định α, β duy nhất (định thức Vandermonde khác 0).</p><h2>2. Ví dụ chi tiết có lời giải</h2>'
    notes+=ex('1. Giáo trình (ví dụ 1)','<p>aₙ = aₙ₋₁ + 2aₙ₋₂, a₀ = 2, a₁ = 7: r = 2, −1; α + β = 2, 2α − β = 7 ⇒ α = 3, β = −1: aₙ = 3·2ⁿ − (−1)ⁿ.</p>')
    notes+=ex('2. Nghiệm kép (giáo trình, ví dụ 3, đã sửa dấu)','<p>aₙ = 6aₙ₋₁ − 9aₙ₋₂, a₀ = 1, a₁ = 6: r = 3 kép; α = 1, 3(1 + β) = 6 ⇒ β = 1: aₙ = (1 + n)3ⁿ.</p>')
    notes+=ex('3. Bậc 2 khác','<p>aₙ = 5aₙ₋₁ − 6aₙ₋₂, a₀ = 3, a₁ = 8: r = 2, 3; α + β = 3, 2α + 3β = 8 ⇒ β = 2, α = 1: aₙ = 2ⁿ + 2·3ⁿ. Kiểm tra a₂ = 40 − 18 = 22 và 4 + 18 = 22 ✓.</p>')
    notes+=ex('4. Hệ thức không thuần nhất bậc 1 (2.2.22a)','<p>aₙ = aₙ₋₁ + 2n + 3, a₀ = 4: aₙ = 4 + n(n+1) + 3n = n² + 4n + 4 = (n + 2)².</p>')
    notes+=ex('5. Bài tập giáo trình 14','<p>(b) aₙ = 7aₙ₋₁ − 6aₙ₋₂, a₀ = 2, a₁ = 1: r = 1, 6: aₙ = 11/5 − (1/5)6ⁿ. (d) aₙ = 2aₙ₋₁ − aₙ₋₂, a₀ = 4, a₁ = 1: (r − 1)² = 0: aₙ = 4 − 3n.</p>')
    notes+='<h2>3. Thực hành tương tác</h2><p>Nhập hệ số và điều kiện đầu, công cụ giải và đối chiếu 12 số hạng:</p>'+sim('rec')
    notes+='<h2>4. Bối cảnh lý thuyết và lịch sử</h2>'+callout('info','📜 Nguồn gốc','Công thức tường minh của Fibonacci được Jacques Binet (1843) công bố, nhưng đã được Euler và de Moivre biết từ thế kỷ 18. Phương pháp nghiệm đặc trưng tương tự phương pháp giải phương trình vi phân tuyến tính hệ số hằng.')
    notes+='<h2>5. Case study</h2><p>Độ phức tạp T(n) = T(n−1) + T(n−2) + 1 của Fibonacci đệ quy có nghiệm cỡ φⁿ ≈ 1,618ⁿ: với n = 50 cần cỡ 10¹⁰ lời gọi, còn phương pháp lặp chỉ 50 phép cộng.</p><h2>6. Bẫy khi làm bài</h2>'+callout('warn','Chú ý','• Kiểm tra dấu khi chuyển sang phương trình đặc trưng.<br>• Ghi tường minh nghiệm kép có nhân tử n.<br>• Thay lại điều kiện đầu và a₂ để kiểm chứng.')
    return dict(id='m08',slug='08-giai-he-thuc-truy-hoi',title='Giải hệ thức truy hồi',subtitle='Phương trình đặc trưng, nghiệm phân biệt, nghiệm kép, bậc 3',source='Giáo trình 2016 §2.4.2 · Đề cương INT1358 mục 2.4.3 · Rosen §8.2',exam='Câu 2b (đề 2017–2020), câu 3a (đề 2023–2024)',time='≈ 3 giờ',
        objectives=['Lập phương trình đặc trưng đúng dấu','Chọn dạng nghiệm cho nghiệm phân biệt và nghiệm bội','Giải hệ tìm hệ số và kiểm tra bằng số hạng đầu','Nhận ra lỗi chép trong tài liệu (r² − 6r − 9)'],parts=parts,notes=notes,sims=['rec'])
