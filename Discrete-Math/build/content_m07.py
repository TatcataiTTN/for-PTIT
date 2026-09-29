from hx import *
import itertools
def ol(steps): return '<ol>'+''.join(f'<li>{s}</li>' for s in steps)+'</ol>'
def has(s,d,k):
    r=0
    for c in s:
        r=r+1 if c==d else 0
        if r>=k: return True
    return False
def bcount(f,n): return sum(1 for s in itertools.product((0,1),repeat=n) if f(s))
def module():
    parts=[]
    a3={n:bcount(lambda s:has(s,1,3),n) for n in range(1,10)}
    b3={n:2**n-a3[n] for n in a3}
    s=[]
    s.append(sl('<p>Nhiều bài đếm phụ thuộc tham số n và khó có công thức trực tiếp nhưng dễ tìm liên hệ giữa kết quả ở n và các giá trị nhỏ hơn: đó là <b>hệ thức truy hồi</b>. Học cách <i>lập</i> hệ thức (module này) rồi <i>giải</i> nó (Module 8). Câu 2a đề 2017–2020 và câu 3b đề 2023–2024 đều là “lập hệ thức truy hồi cho xâu nhị phân”.</p>'+ul(['Định nghĩa: hệ thức truy hồi, điều kiện đầu, nghiệm','Bốn mô hình kinh điển: lãi kép, Fibonacci, mất thứ tự, C(n,k)','Lập truy hồi bằng “xét bit cuối”, “xét khối cuối”, phần bù','Kiểm chứng bằng đếm trực tiếp']),'MODULE 7 · Giáo trình 2016 §2.4.1 · Đề cương 2.4.1–2.4.2','Lập hệ thức truy hồi'))
    s.append(sl(formula('Hệ thức truy hồi','aₙ = f(aₙ₋₁, aₙ₋₂, …, aₙ₋ₖ)  với n ≥ n₀,  cùng k điều kiện đầu',[('aₙ','số cấu hình cần đếm ứng với tham số n'),('điều kiện đầu','k giá trị a₀…a_(k−1) hoặc a₁…aₖ để xác định duy nhất dãy')])+table(['Mô hình','Hệ thức','Đầu'],[['Lãi kép 11%','Pₙ = 1,11·Pₙ₋₁','P₀ = 10000'],['Thỏ Fibonacci','fₙ = fₙ₋₁ + fₙ₋₂','f₁ = f₂ = 1'],['Mất thứ tự','Dₙ = (n−1)(Dₙ₋₁ + Dₙ₋₂)','D₁ = 0, D₂ = 1'],['Tổ hợp','C(n,k) = C(n−1,k−1) + C(n−1,k)','C(n,0) = C(n,n) = 1']]),'PHẦN 1 · Nền tảng','Hệ thức truy hồi và bốn mô hình kinh điển',
        explain='Thay vì tìm công thức chung cho aₙ, ta chỉ cần biết “muốn có aₙ thì lấy các số trước đó ghép lại thế nào”. Giống việc leo cầu thang: đến bậc n phải đi từ bậc n−1 hoặc n−2.'))
    parts.append(dict(title='Nền tảng',bullets=['Định nghĩa','Bốn mô hình kinh điển'],slides=s))
    s=[]
    s.append(sl(ol(['Đặt aₙ rõ ràng (số xâu/số cách … có độ dài n).','Phân loại cấu hình độ dài n theo <b>phần cuối</b> (bit cuối, khối cuối, hành động cuối).','Mỗi loại quy về cấu hình nhỏ hơn: dùng quy tắc cộng.','Viết hệ thức và tìm điều kiện đầu bằng đếm trực tiếp.','Kiểm tra bằng vài giá trị đếm được.']),'PHẦN 2 · Phương pháp','Quy trình năm bước'))
    s.append(sl(formula('Không chứa hai bit 1 liên tiếp','aₙ = aₙ₋₁ + aₙ₋₂,  a₁ = 2,  a₂ = 3')+ol(['Bit cuối là 0: ghép “0” vào xâu hợp lệ độ dài n−1 ⇒ aₙ₋₁.','Bit cuối là 1: bit trước phải là 0 ⇒ ghép “01” vào xâu hợp lệ độ dài n−2 ⇒ aₙ₋₂.']),'PHẦN 2 · Phương pháp','Mẫu 1: xét bit cuối'))
    s.append(sl(formula('Chứa 3 bit 1 liên tiếp (đề thi)','aₙ = aₙ₋₁ + aₙ₋₂ + aₙ₋₃ + 2ⁿ⁻³,  a₁ = a₂ = 0,  a₃ = 1')+'<p>Cách 1: bₙ = số xâu KHÔNG chứa 111; bₙ = bₙ₋₁ + bₙ₋₂ + bₙ₋₃ (kết thúc 0, 10, 110), b₁ = 2, b₂ = 4, b₃ = 7. aₙ = 2ⁿ − bₙ.</p><p>Cách 2 (trực tiếp): xâu chưa có 111 ở n−3 vị trí đầu rồi kết thúc bằng 0, 10, 110 (aₙ₋₁ + aₙ₋₂ + aₙ₋₃) hoặc n−3 bit đầu tùy ý kèm “111” (2ⁿ⁻³).</p>'+f'<p>Đếm trực tiếp: a₄ = {a3[4]}, a₅ = {a3[5]}, a₆ = {a3[6]}, a₇ = {a3[7]}, a₈ = {a3[8]}.</p>'+sim('strcount'),'PHẦN 2 · Phương pháp','Mẫu 2: phần bù'))
    s.append(sl(formula('Số chữ số lẻ (từ mã thập phân)','aₙ = 8aₙ₋₁ + 10ⁿ⁻¹,  a₁ = 1  (số lẻ chữ số d)')+ol(['Gọi aₙ: xâu có số LẺ chữ số d; bₙ: số CHẴN chữ số d; aₙ + bₙ = 10ⁿ.','Thêm ký tự cuối: là d (1 cách) đổi tính chẵn lẻ; khác d (9 cách) giữ nguyên.','aₙ = 9aₙ₋₁ + bₙ₋₁ = 9aₙ₋₁ + (10ⁿ⁻¹ − aₙ₋₁) = 8aₙ₋₁ + 10ⁿ⁻¹.']),'PHẦN 2 · Phương pháp','Mẫu 3: tính chẵn lẻ'))
    parts.append(dict(title='Phương pháp: lập hệ thức',bullets=['Quy trình năm bước','Xét bit cuối','Phần bù','Tính chẵn lẻ'],slides=s))
    s=[]
    s.append(sl(callout('info','Ví dụ 1 (2.2.1b)','Hệ thức truy hồi cho số xâu nhị phân độ dài n chứa 3 số 1 liên tiếp; tính a₆.')+ol(['aₙ = aₙ₋₁ + aₙ₋₂ + aₙ₋₃ + 2ⁿ⁻³, a₃ = 1, a₁ = a₂ = 0.',f'a₄ = 3, a₅ = {a3[5]}, a₆ = <b>{a3[6]}</b> (đối chiếu đếm trực tiếp {2**6} xâu).']),'PHẦN 3 · Ví dụ','Ví dụ 1: chứa 111'))
    a7c=bcount(lambda s:not has(s,1,3),7)
    s.append(sl(callout('info','Ví dụ 2 (2.2.20a)','an là số xâu nhị phân độ dài n KHÔNG chứa ba số 1 liên tiếp. Tìm hệ thức và a₇.')+ol(['aₙ = aₙ₋₁ + aₙ₋₂ + aₙ₋₃, a₁ = 2, a₂ = 4, a₃ = 7.',f'a₄ = 13, a₅ = 24, a₆ = 44, a₇ = <b>{a7c}</b>.']),'PHẦN 3 · Ví dụ','Ví dụ 2: không chứa 111'))
    s.append(sl(callout('info','Ví dụ 3 (2.1.17b)','Từ mã hợp lệ là xâu chữ số thập phân chứa một số LẺ chữ số 6; aₙ là số từ mã độ dài n. Tìm hệ thức và điều kiện đầu.')+ol(['aₙ = 8aₙ₋₁ + 10ⁿ⁻¹.','a₁ = 1 (chỉ xâu “6”).','a₂ = 18, a₃ = 244, a₄ = 2952, a₅ = 33616.']),'PHẦN 3 · Ví dụ','Ví dụ 3: từ mã lẻ chữ số 6'))
    s.append(sl(callout('info','Ví dụ 4 (2.2.17a, lặp)','aₙ = aₙ₋₁ + 2n với a₀ = 1. Giải bằng phương pháp lặp.')+ol(['aₙ = a₀ + Σ_{i=1..n} 2i = 1 + n(n+1).','Kiểm tra: a₃ = 1 + 12 = 13 và 1 → 3 → 7 → 13.']),'PHẦN 3 · Ví dụ','Ví dụ 4: hệ thức không thuần nhất bậc 1'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)',bullets=['Chứa 111','Không chứa 111','Từ mã lẻ chữ số','Phương pháp lặp'],slides=s))
    s=[]
    s.append(sl(ul(['<b>Quên điều kiện đầu</b> hoặc cho thiếu (hệ thức bậc k cần k điều kiện).','<b>Đếm trùng</b> khi phân loại theo bit cuối chưa loại trừ đủ.','<b>Chẵn lẻ:</b> nhớ aₙ + bₙ = tổng số xâu.','<b>Đề gốc có lỗi chép:</b> ngân hàng 2.2.2b ghi “xâu thập phân … Tính số xâu nhị phân” — đề bài nhầm, ta hiểu là xâu thập phân.','<b>Tính a_n bằng hệ thức phải khớp đếm trực tiếp</b> ở n nhỏ; luôn kiểm tra.']),'PHẦN 4 · Bẫy và mở rộng','Năm bẫy thường gặp'))
    s.append(sl('<p>Tổng quát: xâu nhị phân không có k bit 1 liên tiếp: aₙ = aₙ₋₁ + … + aₙ₋ₖ, aⱼ = 2ʲ (j < k), aₖ = 2ᵏ − 1. Xâu có ít nhất một dãy k bit 1: bₙ = bₙ₋₁ + … + bₙ₋ₖ + 2ⁿ⁻ᵏ, bⱼ = 0 (j < k), bₖ = 1 (đã kiểm chứng bằng liệt kê với k = 2, 3, 4).</p>','PHẦN 4 · Bẫy và mở rộng','Mở rộng: k bất kỳ'))
    parts.append(dict(title='Bẫy và mở rộng',bullets=['Năm bẫy','Trường hợp k bất kỳ'],slides=s))
    s=[]
    s.append(sl('<p>Bậc thang: đi n bậc, mỗi bước 1 hoặc 2 bậc: aₙ = aₙ₋₁ + aₙ₋₂ (Fibonacci). Trong lập trình động, hệ thức truy hồi là “công thức chuyển trạng thái”; giải bằng bảng hoặc đệ quy có nhớ.</p>','PHẦN 5 · Ứng dụng và ôn tập','Case study: quy hoạch động'))
    s.append(sl(ul(['Xác định aₙ chính xác.','Phân loại theo phần cuối, dùng quy tắc cộng.','Tìm điều kiện đầu, kiểm tra bằng đếm trực tiếp.'])+callout('good','Tiếp theo','Module 8: giải hệ thức truy hồi tuyến tính thuần nhất.'),'PHẦN 5 · Ứng dụng và ôn tập','Tổng kết'))
    parts.append(dict(title='Ứng dụng và tổng kết',bullets=['Quy hoạch động','Checklist'],slides=s))
    notes='<h2>1. Nội dung chi tiết</h2><p>Hệ thức truy hồi cho phép tính mọi số hạng từ vài số hạng đầu, và rất hợp với lập trình. Giáo trình 2016 §2.4.1 dùng bốn mô hình: lãi kép, thỏ Fibonacci, số mất thứ tự Dₙ = (n−1)(Dₙ₋₁ + Dₙ₋₂), và hệ số tổ hợp C(n,k) = C(n−1,k−1) + C(n−1,k).</p><h2>2. Ví dụ chi tiết có lời giải</h2>'
    notes+=ex('1. Lãi kép','<p>Gửi 10000 USD, lãi 11%/năm: Pₙ = 1,11Pₙ₋₁, P₀ = 10000 ⇒ Pₙ = 10000·1,11ⁿ; sau 30 năm P₃₀ ≈ 228 922,97 USD.</p>')
    notes+=ex('2. Số mất thứ tự','<p>D₁ = 0, D₂ = 1, D₃ = 2, D₄ = 9, D₅ = 44, D₆ = 265, D₇ = 1854 (theo Dₙ = (n−1)(Dₙ₋₁ + Dₙ₋₂)).</p>')
    notes+=ex('3. Xâu chứa số chẵn bit 0 (2.2.18a)','<p>aₙ = 2aₙ₋₁, a₁ = 1 ⇒ a₆ = 32.</p>')
    notes+=ex('4. Lương tăng (bài tập giáo trình)','<p>Lương năm n sau 1987: aₙ = 1,05aₙ₋₁ + 1000, a₀ = 50000; a₈ ≈ '+f'{(70000*1.05**8-20000):,.0f}'.replace(',','.')+' USD (công thức tường minh aₙ = 70000·1,05ⁿ − 20000).</p>')
    notes+=ex('5. Máy bán tem (bài tập giáo trình)','<p>Đồng 1 USD, tờ 1 USD, tờ 5 USD, thứ tự quan trọng: aₙ = 2aₙ₋₁ + aₙ₋₅, a₀ = 1. a₁₀ = 1217 (a₀…a₁₀ = 1, 2, 4, 8, 16, 33, 68, 140, 288, 592, 1217; tính bằng chương trình).</p>')
    notes+='<h2>3. Thực hành tương tác</h2><p>Liệt kê xâu, đếm và kiểm tra hệ thức thử của bạn:</p>'+sim('strcount')
    notes+='<h2>4. Bối cảnh lý thuyết và lịch sử</h2>'+callout('info','📜 Nguồn gốc','Dãy Fibonacci xuất hiện trong <i>Liber Abaci</i> (1202) qua bài toán thỏ. Bài toán Tháp Hà Nội do Édouard Lucas đưa ra năm 1883 với hệ thức Hₙ = 2Hₙ₋₁ + 1.')
    notes+='<h2>5. Case study</h2><p>Số cách xếp gạch domino 2×1 lát kín hình chữ nhật 2×n thỏa aₙ = aₙ₋₁ + aₙ₋₂ (a₁ = 1, a₂ = 2). Chương trình tính bằng bảng chỉ O(n), thay vì đệ quy ngây thơ O(φⁿ).</p><h2>6. Bẫy khi làm bài</h2>'+callout('warn','Chú ý','• Nêu rõ định nghĩa aₙ.<br>• Ghi đủ điều kiện đầu.<br>• Đối chiếu với đếm trực tiếp ở n nhỏ.')
    return dict(id='m07',slug='07-lap-he-thuc-truy-hoi',title='Lập hệ thức truy hồi',subtitle='Mô hình hóa bài đếm bằng hệ thức truy hồi',source='Giáo trình 2016 §2.4.1 · Đề cương INT1358 mục 2.4.1–2.4.2 · Rosen §8.1',exam='Câu 2a (đề 2017–2020), câu 3b (đề 2023–2024)',time='≈ 3 giờ',
        objectives=['Lập hệ thức cho xâu nhị phân/thập phân có tính chất','Xác định đúng điều kiện đầu','Dùng phần bù và chẵn lẻ để lập hệ thức','Kiểm chứng bằng đếm trực tiếp'],parts=parts,notes=notes,sims=['strcount'])
