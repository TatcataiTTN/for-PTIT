from hx import *
import math, itertools, sys, os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'orig'))
import orig_lib as OL
def ol(steps): return '<ol>'+''.join(f'<li>{s}</li>' for s in steps)+'</ol>'
def module():
    parts=[]
    a1,t1=OL.int_sol(30,[0,3,0,2,0,0],[None,8,None,6,None,None])
    a2,t2=OL.int_sol(56,[1,3,3,0,0,0],[4,None,6,None,None,None])
    pal=OL.pal_count(9,16)
    s=[]
    s.append(sl('<p>Sau các quy tắc cộng–nhân, ta cần các “khuôn đếm” dùng lại nhiều lần: chỉnh hợp, hoán vị, tổ hợp (có và không lặp) và số nghiệm nguyên của phương trình tuyến tính. Dạng “đếm nghiệm nguyên có cận” xuất hiện gần như mọi đề thi PTIT (câu 3a hoặc 2b).</p>'+ul(['Chỉnh hợp, hoán vị, tổ hợp; hoán vị và tổ hợp lặp','Đếm nghiệm nguyên không âm, có cận dưới, có cận trên','Số thuận nghịch, nhị thức Newton','Ứng dụng bù trừ để xử lý cận trên']),'MODULE 5 · Giáo trình 2016 §2.3, §2.5 · Đề cương 2.3','Hoán vị, tổ hợp và nghiệm nguyên'))
    s.append(sl(table(['Khuôn','Ý nghĩa','Công thức'],[['Chỉnh hợp lặp','xếp k trong n, được lặp, có thứ tự','nᵏ'],['Chỉnh hợp không lặp','xếp k trong n, khác nhau, có thứ tự','A(n,k) = n!/(n−k)!'],['Hoán vị','xếp n vật khác nhau','n!'],['Tổ hợp','chọn k trong n, không thứ tự','C(n,k) = n!/(k!(n−k)!)'],['Hoán vị lặp','n vật gồm n₁,…,n_m giống nhau','n!/(n₁!⋯n_m!)'],['Tổ hợp lặp','chọn k từ n loại, cho lặp','C(n+k−1,k)']]),'PHẦN 1 · Nền tảng','Sáu khuôn đếm',
        explain='Hỏi hai câu: (1) có phân biệt thứ tự không? (2) có cho lặp lại không? Trả lời hai câu này là chọn được công thức.'))
    s.append(sl(formula('Tổ hợp và tính chất','C(n,k) = C(n,n−k);  C(n,k) = C(n−1,k−1) + C(n−1,k);  Σₖ C(n,k) = 2ⁿ')+formula('Nhị thức Newton','(x + y)ⁿ = Σₖ C(n,k)·xⁿ⁻ᵏ·yᵏ')+'<p>Hệ số của xⁿ⁻ᵏyᵏ trong (ax + by)ⁿ là C(n,k)·aⁿ⁻ᵏ·bᵏ.</p>','PHẦN 1 · Nền tảng','Công thức tổ hợp và nhị thức'))
    parts.append(dict(title='Nền tảng: các khuôn đếm',bullets=['Sáu khuôn','Tổ hợp và nhị thức'],slides=s))
    s=[]
    s.append(sl(formula('Nghiệm nguyên không âm (vách ngăn)','x₁ + x₂ + … + x_k = N   ⇒   C(N + k − 1, k − 1) nghiệm')+'<p>Chia N đơn vị vào k biến ⇔ đặt k − 1 “vách ngăn” giữa N đơn vị: chọn vị trí cho vách ngăn trong N + k − 1 chỗ. Đây cũng là tổ hợp lặp chọn N từ k loại.</p>'+callout('info','Ví dụ','x₁ + x₂ + x₃ = 13: C(15,2) = 105 nghiệm không âm.'),'PHẦN 2 · Phương pháp','Số nghiệm nguyên không âm'))
    s.append(sl(formula('Cận dưới','xᵢ ≥ lᵢ  ⇒  đặt yᵢ = xᵢ − lᵢ ≥ 0,  tổng còn N − Σlᵢ')+'<p>Ví dụ: x₁ + x₂ + x₃ = 13 với x₁ ≥ 1, x₂ ≥ 3, x₃ ≥ 0: y₁ + y₂ + y₃ = 13 − 4 = 9 ⇒ C(11,2) = 55.</p>','PHẦN 2 · Phương pháp','Cận dưới: đổi biến'))
    s.append(sl(formula('Cận trên: bù trừ','yᵢ ≤ hᵢ − lᵢ = cᵢ  ⇒  trừ các trường hợp yᵢ ≥ cᵢ + 1')+'<p>Với hai biến bị chặn: (tổng không cận) − (vượt cận 1) − (vượt cận 2) + (vượt cả hai). Mỗi số hạng có dạng C(rem + k − 1, k − 1) với rem = tổng còn lại sau khi trừ đi (cᵢ + 1) tương ứng, và bằng 0 nếu rem < 0.</p>'+sim('intsol'),'PHẦN 2 · Phương pháp','Cận trên: nguyên lý bù trừ'))
    parts.append(dict(title='Phương pháp: đếm nghiệm nguyên',bullets=['Vách ngăn','Cận dưới','Cận trên bằng bù trừ'],slides=s))
    s=[]
    s.append(sl(callout('info','Ví dụ 1 (câu 3a đề 2019–2020)','x₁ + … + x₆ = 30 có bao nhiêu nghiệm nguyên không âm thỏa 8 ≥ x₂ ≥ 3 và 6 ≥ x₄ ≥ 2?')+'<pre style="font-size:.8em">'+esc(t1)+'</pre>','PHẦN 3 · Ví dụ','Ví dụ 1: hai cận (đề thi thật)'))
    s.append(sl(callout('info','Ví dụ 2 (2.1.8a)','x₁ + … + x₆ = 56 với 4 ≥ x₁ ≥ 1, x₂ ≥ 3, 6 ≥ x₃ ≥ 3.')+'<pre style="font-size:.8em">'+esc(t2)+'</pre>','PHẦN 3 · Ví dụ','Ví dụ 2: cận dưới và cận trên'))
    s.append(sl(callout('info','Ví dụ 3 (2.1.23a)','Có bao nhiêu số 9 chữ số là số thuận nghịch có tổng chữ số 16?')+ol(['Số thuận nghịch 9 chữ số xác định bởi 5 chữ số đầu x₁…x₅ (x₁ ≥ 1).','Tổng chữ số = 2(x₁+x₂+x₃+x₄) + x₅ = 16.',f'Đếm số nghiệm 0 ≤ xᵢ ≤ 9, x₁ ≥ 1: <b>{pal}</b> (đã kiểm chứng bằng liệt kê).']),'PHẦN 3 · Ví dụ','Ví dụ 3: số thuận nghịch'))
    s.append(sl(callout('info','Ví dụ 4 (5.8a)','20 cuốn: 10 Toán, 6 Hóa, 4 Lý; các cuốn cùng chủ đề nằm cạnh nhau và sách Toán không cạnh sách Lý.')+ol(['Ba khối: nếu Toán không kề Lý thì Hóa phải ở giữa: 2 thứ tự (Toán–Hóa–Lý hoặc Lý–Hóa–Toán).','Xếp trong khối: 10!·6!·4!.',f'Tổng: 2·10!·6!·4! = <b>{2*math.factorial(10)*math.factorial(6)*math.factorial(4):,}</b>'.replace(',','.')]),'PHẦN 3 · Ví dụ','Ví dụ 4: xếp sách có điều kiện'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)',bullets=['Hai cận (đề thi)','Cận dưới + trên','Số thuận nghịch','Xếp sách'],slides=s))
    s=[]
    s.append(sl(ul(['<b>Quên đổi biến</b> khi có cận dưới (dùng nhầm N thay vì N − Σl).','<b>Bù trừ sai dấu</b> hoặc quên số hạng “vượt cả hai”.','<b>Vượt cận nghĩa là yᵢ ≥ cᵢ + 1</b>, không phải yᵢ ≥ cᵢ.','<b>Tổ hợp vs chỉnh hợp:</b> có phân biệt thứ tự không?','<b>Chữ số đầu ≠ 0</b> với số n chữ số; số thuận nghịch cần tính đúng số chữ số tự do.','<b>Giáo trình 2016 (ví dụ 2.4.2):</b> phương trình đặc trưng ghi r² − 6r − 9 = 0 là in nhầm; đúng là r² − 6r + 9 = 0 (Module 8).']),'PHẦN 4 · Bẫy và mở rộng','Sáu bẫy thường gặp'))
    s.append(sl('<p>Tổ hợp lặp cũng cho số cách chia N vật giống nhau vào k hộp khác nhau: C(N + k − 1, k − 1). Nếu mỗi hộp có ít nhất một vật: C(N − 1, k − 1).</p>'+ex('Chia 12 quả bóng vào 4 hộp, mỗi hộp ≥ 1','C(11,3) = 165.'),'PHẦN 4 · Bẫy và mở rộng','Mở rộng: chia vật vào hộp'))
    parts.append(dict(title='Bẫy và mở rộng',bullets=['Sáu bẫy','Chia vật vào hộp'],slides=s))
    s=[]
    s.append(sl('<p>Xổ số Mega 6/45: chọn 6 số từ 45 số, không thứ tự: C(45,6) = 8 145 060 tổ hợp. Xác suất trúng giải độc đắc khi mua một vé là 1/8 145 060 ≈ 1,2·10⁻⁷.</p>','PHẦN 5 · Ứng dụng và ôn tập','Case study: xổ số 6/45'))
    s.append(sl(ul(['Nhận diện 6 khuôn đếm.','Đổi biến để loại cận dưới; bù trừ để xử lý cận trên.','Đối chiếu kết quả bằng đếm trực tiếp/quy hoạch động khi có thể.'])+callout('good','Tiếp theo','Module 6: nguyên lý Dirichlet và bài toán tồn tại.'),'PHẦN 5 · Ứng dụng và ôn tập','Tổng kết'))
    parts.append(dict(title='Ứng dụng và tổng kết',bullets=['Xổ số','Checklist'],slides=s))
    notes='<h2>1. Nội dung chi tiết</h2><p>Các khuôn đếm suy ra từ quy tắc nhân: chỉnh hợp không lặp A(n,k) = n(n−1)…(n−k+1); chia cho k! để bỏ thứ tự được C(n,k). Số nghiệm nguyên là tổ hợp lặp trong ngôn ngữ phương trình.</p><h2>2. Ví dụ chi tiết có lời giải</h2>'
    notes+=ex('1. Hoán vị lặp','<p>Có bao nhiêu cách sắp các chữ cái của MISSISSIPPI? Có 11 chữ: I×4, S×4, P×2, M×1: 11!/(4!4!2!1!) = 34 650.</p>')
    notes+=ex('2. Chọn ủy ban có điều kiện','<p>CLB có 8 nam và 6 nữ. Chọn ủy ban 5 người có ít nhất 2 nữ: tổng C(14,5) = 2002 trừ trường hợp 0 nữ C(8,5) = 56 và 1 nữ C(6,1)·C(8,4) = 420: 2002 − 56 − 420 = 1526.</p>')
    notes+=ex('3. Đường đi trên lưới','<p>Đi từ góc trên trái đến góc dưới phải lưới 5×7 ô chỉ sang phải/xuống: C(12,5) = 792.</p>')
    notes+=ex('4. Nhị thức','<p>Hệ số của x⁴y³ trong (2x + 3y)⁷ là C(7,3)·2⁴·3³ = 35·16·27 = 15120.</p>')
    notes+=ex('5. Nghiệm có cận (dạng 2.1.4b)','<p>x₁ + x₂ + x₃ = 16 với x₁ ≥ 2, x₂ ≥ 0, x₃ ≥ 2: y₁+y₂+y₃ = 12 ⇒ C(14,2) = 91.</p>')
    notes+='<h2>3. Thực hành tương tác</h2>'+sim('intsol')
    notes+='<h2>4. Bối cảnh lý thuyết và lịch sử</h2>'+callout('info','📜 Nguồn gốc','Tam giác Pascal (Traité du triangle arithmétique, viết 1654, in 1665) hệ thống hóa hệ số nhị thức, dù đã được biết ở Trung Quốc và Ba Tư từ trước. Phương pháp “vách ngăn” (stars and bars) được William Feller phổ biến trong xác suất rời rạc.')
    notes+='<h2>5. Case study</h2><p>Chia N tác vụ giống nhau cho k máy chủ: số cách phân bổ không phân biệt tác vụ là C(N + k − 1, k − 1). Với N = 100, k = 8: C(107,7) ≈ 2,6·10¹⁰ cách; đây là kích thước không gian tìm kiếm của bài toán cân bằng tải vét cạn.</p><h2>6. Bẫy khi làm bài</h2>'+callout('warn','Chú ý','• Ghi rõ bước đổi biến và tổng còn lại.<br>• Với hai cận trên, viết đủ bốn số hạng bù trừ.<br>• Kiểm tra kết quả nhỏ bằng liệt kê trực tiếp.')
    return dict(id='m05',slug='05-to-hop-nghiem-nguyen',title='Hoán vị, tổ hợp và nghiệm nguyên',subtitle='Các khuôn đếm, số nghiệm nguyên có cận, số thuận nghịch',source='Giáo trình 2016 §2.3 · Đề cương INT1358 mục 2.3 · Rosen §6.3–6.5',exam='Câu 3a (đề 2017–2020), câu 2b (đề 2023–2024)',time='≈ 3 giờ',
        objectives=['Chọn đúng khuôn đếm (chỉnh hợp/tổ hợp, lặp/không lặp)','Đếm số nghiệm nguyên không âm, có cận dưới, có cận trên','Xử lý số thuận nghịch và bài xếp sách/người có điều kiện','Đối chiếu kết quả bằng tính toán độc lập'],parts=parts,notes=notes,sims=['intsol'])
