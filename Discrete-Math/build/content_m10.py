from hx import *
import sys, os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'orig'))
import orig_nh2 as X2
from cpp_snippets import CPP
def ol(steps): return '<ol>'+''.join(f'<li>{s}</li>' for s in steps)+'</ol>'
def T(t): return '('+', '.join(map(str,t))+')'
def CH(f,x,k,*e): return X2.chain(f,x,k,*e)
def module():
    parts=[]
    p0=(5,6,8,3,9,7,4,2,1); pc=CH(X2.next_perm,p0,4)
    c0=(2,3,6,8,9); cc=CH(X2.next_comb,c0,5,9)
    b0=(1,0,1,1,1,1,1,1,1); bc=CH(X2.next_bin,b0,4)
    c1=(1,4,5,7,9); cc1=CH(X2.next_comb,c1,5,9)
    p1=(1,6,7,5,2,9,8,4,3); pc1=CH(X2.next_perm,p1,5)
    s=[]
    s.append(sl('<p><b>Liệt kê</b> đưa ra từng cấu hình một, yêu cầu không lặp và không sót. Với <b>phương pháp sinh</b>, ta cần (1) một thứ tự trên tập cấu hình biết cấu hình đầu và cuối, (2) một thuật toán sinh cấu hình kế tiếp từ cấu hình hiện tại. Ba dạng cấu hình xuất hiện trong mọi đề thi PTIT: xâu nhị phân, hoán vị, tổ hợp.</p>'+ul(['Khung thuật toán sinh','Sinh xâu nhị phân kế tiếp (y = x + 1)','Sinh hoán vị kế tiếp','Sinh tổ hợp chập k kế tiếp']),'MODULE 10 · Giáo trình 2016 §3.3 · Đề cương 3.2','Phương pháp sinh'))
    s.append(sl('<pre><code>Bước 1 (khởi tạo): &lt;thiết lập cấu hình đầu tiên&gt;;\nBước 2 (lặp): while (&lt;chưa phải cấu hình cuối&gt;) {\n    &lt;in cấu hình hiện tại&gt;;\n    &lt;sinh cấu hình kế tiếp&gt;;\n}\n&lt;in cấu hình cuối&gt;;</code></pre><p>Thứ tự dùng ở PTIT là <b>thứ tự từ điển</b>: X đứng trước Y nếu tồn tại t sao cho xᵢ = yᵢ (i < t) và xₜ < yₜ.</p>','PHẦN 1 · Nền tảng','Khung thuật toán sinh (slide PTIT)'))
    parts.append(dict(title='Nền tảng',bullets=['Điều kiện của phương pháp sinh','Khung thuật toán'],slides=s))
    s=[]
    s.append(sl(formula('Xâu nhị phân kế tiếp','tìm k lớn nhất có xₖ = 0; đặt xₖ = 1 và xⱼ = 0 với j > k',[('không có k','x = 11…1 là xâu cuối'),('bản chất','y = x + 1 trong hệ nhị phân')])+'<pre><code>'+esc(CPP['bin_gen'])+'</code></pre>','PHẦN 2 · Phương pháp','Sinh xâu nhị phân'))
    s.append(sl(formula('Hoán vị kế tiếp','1) i lớn nhất: p[i] < p[i+1];  2) j lớn nhất: p[j] > p[i];  3) đổi chỗ p[i], p[j];  4) đảo đoạn p[i+1..n]')+'<p>Hoán vị đầu (1,2,…,n), cuối (n,…,2,1). Mỗi lần sinh O(n); tổng n! hoán vị.</p><pre><code>'+esc(CPP['perm_gen'])+'</code></pre>','PHẦN 2 · Phương pháp','Sinh hoán vị'))
    s.append(sl(formula('Tổ hợp chập k kế tiếp','i lớn nhất có c[i] ≠ n − k + i;  c[i]++;  c[j] = c[j−1] + 1 (j > i)')+'<p>Tổ hợp đầu (1,…,k), cuối (n−k+1,…,n). C(n,k) tổ hợp.</p>'+viz('gen'),'PHẦN 2 · Phương pháp','Sinh tổ hợp'))
    parts.append(dict(title='Phương pháp: ba thuật toán sinh',bullets=['Xâu nhị phân','Hoán vị','Tổ hợp'],slides=s))
    s=[]
    s.append(sl(callout('info','Ví dụ 1 (3.2a, đề 2023–2024)','A = {1,…,9}. Tìm 4 hoán vị liền kề tiếp theo của 568397421.')+'<p>'+' → '.join(T(x) for x in [p0]+pc)+'</p>'+callout('info','Bước đầu','(5,6,8,3,9,7,4,2,1): i = vị trí 4 (giá trị 3 < 9); j = vị trí 6 (giá trị 7 > 3); đổi chỗ: (5,6,8,7,9,3,4,2,1); đảo đoạn sau vị trí 4: (5,6,8,7,1,2,4,3,9).'),'PHẦN 3 · Ví dụ','Ví dụ 1: hoán vị kế tiếp'))
    s.append(sl(callout('info','Ví dụ 2 (3.11a, đề 2023–2024)','5 tổ hợp chập 5 kế tiếp của (2,3,6,8,9) trên {1..9}.')+'<p>'+' → '.join(T(x) for x in [c0]+cc)+'</p>','PHẦN 3 · Ví dụ','Ví dụ 2: tổ hợp kế tiếp'))
    s.append(sl(callout('info','Ví dụ 3 (3.8a)','4 xâu nhị phân liền kề tiếp theo của X = (1,0,1,1,1,1,1,1,1).')+'<p>'+' → '.join(T(x) for x in [b0]+bc)+'</p><p>Mỗi bước là cộng 1 nhị phân: 101111111 + 1 = 110000000, …</p>','PHẦN 3 · Ví dụ','Ví dụ 3: xâu nhị phân kế tiếp'))
    s.append(sl(callout('info','Ví dụ 4 (3.10)','5 tổ hợp kế tiếp của (1,4,5,7,9) và 5 hoán vị kế tiếp của (1,6,7,5,2,9,8,4,3).')+'<p>Tổ hợp: '+' → '.join(T(x) for x in [c1]+cc1)+'</p><p>Hoán vị: '+' → '.join(T(x) for x in [p1]+pc1)+'</p>','PHẦN 3 · Ví dụ','Ví dụ 4: hai dạng trong một câu'))
    parts.append(dict(title='Ví dụ có lời giải (câu hỏi thật)',bullets=['Hoán vị','Tổ hợp','Xâu nhị phân','Kết hợp'],slides=s))
    s=[]
    s.append(sl(ul(['<b>Quên đảo đoạn sau i</b> sau khi đổi chỗ (hoán vị).','<b>Chọn j sai:</b> j phải là chỉ số lớn nhất có p[j] > p[i], không phải phần tử lớn nhất.','<b>Tổ hợp:</b> giới hạn của vị trí i là n − k + i, không phải n.','<b>Đề thi ghi “liền kề tiếp theo”</b>: mỗi bước dùng lại kết quả bước trước.','<b>Đề thi yêu cầu code:</b> ghi rõ điều kiện dừng (cấu hình cuối).']),'PHẦN 4 · Bẫy và mở rộng','Năm bẫy thường gặp'))
    s.append(sl('<p>Thứ hạng (rank): vị trí của hoán vị trong danh sách từ điển = 1 + Σ (số phần tử nhỏ hơn p[i] ở bên phải)·(n − i)!. Ngược lại có thể dựng hoán vị thứ r (unrank) bằng phép chia liên tiếp cho các giai thừa. Với xâu nhị phân, thứ hạng chính là giá trị nhị phân + 1.</p>','PHẦN 4 · Bẫy và mở rộng','Mở rộng: rank và unrank'))
    parts.append(dict(title='Bẫy và mở rộng',bullets=['Năm bẫy','Rank/unrank'],slides=s))
    s=[]
    s.append(sl('<p><code>std::next_permutation</code> trong C++ cài đặt đúng thuật toán hoán vị kế tiếp ở trên. Ứng dụng: thử mọi thứ tự ưu tiên tác vụ khi n nhỏ (n ≤ 10), sinh mật khẩu theo thứ tự từ điển, sinh tập con bằng mặt nạ bit (xâu nhị phân).</p>','PHẦN 5 · Ứng dụng và ôn tập','Case study: next_permutation'))
    s.append(sl(ul(['Thực hiện thuần thục ba thuật toán bằng tay.','Viết được code cho từng thuật toán.','Nêu rõ cấu hình đầu, cuối, điều kiện dừng.'])+callout('good','Tiếp theo','Module 11: quay lui (liệt kê bằng đệ quy).'),'PHẦN 5 · Ứng dụng và ôn tập','Tổng kết'))
    parts.append(dict(title='Ứng dụng và tổng kết',bullets=['next_permutation','Checklist'],slides=s))
    notes='<h2>1. Nội dung chi tiết</h2><p>Phương pháp sinh phù hợp khi thứ tự tự nhiên và hàm kế tiếp đơn giản (xâu nhị phân, hoán vị, tổ hợp). Ưu điểm: không đệ quy, không cần bộ nhớ ngoài cấu hình hiện tại. Nhược điểm: khó áp dụng khi cấu hình có ràng buộc phức tạp (khi đó dùng quay lui).</p><h2>2. Ví dụ chi tiết có lời giải</h2>'
    notes+=ex('1. Hoán vị kế tiếp từng bước','<p>p = (3,1,4,5,8,6,2,9,10,7) trên {1..10}. Từ phải sang trái tìm i lớn nhất có p[i] < p[i+1]: 7 < ... không (10 > 7); 9 < 10 ⇒ i = 8 (giá trị 9). Tìm j lớn nhất có p[j] > 9: p[9] = 10 ⇒ j = 9. Đổi chỗ: (3,1,4,5,8,6,2,10,9,7). Đảo đoạn sau vị trí 8 (9,7 → 7,9): '+T(CH(X2.next_perm,(3,1,4,5,8,6,2,9,10,7),1)[0])+'.</p>')
    notes+=ex('2. Tổ hợp kế tiếp từng bước','<p>c = (2,4,6,8,10), n = 10, k = 5: giá trị tối đa của vị trí i là n − k + i = 5 + i. c[5] = 10 = 10 (tối đa) nên bỏ qua; c[4] = 8 < 9 ⇒ i = 4. Tăng c[4] lên 9 rồi c[5] = c[4] + 1 = 10: (2,4,6,9,10). Năm tổ hợp kế tiếp: '+' → '.join(T(x) for x in CH(X2.next_comb,(2,4,6,8,10),5,10))+'.</p>')
    notes+=ex('3. Xâu nhị phân','<p>X = (1,0,1,1,0,0,1,1,1): bit 0 phải nhất ở vị trí 6 ⇒ (1,0,1,1,0,1,0,0,0); '+' → '.join(T(x) for x in CH(X2.next_bin,(1,0,1,1,0,0,1,1,1),4))+'.</p>')
    notes+=ex('4. Số thứ tự','<p>Hoán vị (2,3,1) của {1,2,3}: có 1 phần tử nhỏ hơn 2 bên phải (chỉ số 1), 1 phần tử nhỏ hơn 3 bên phải: rank = 1 + 1·2! + 1·1! + 0·0! = 4 (danh sách: 123, 132, 213, 231, 312, 321 — thực tế (2,3,1) đứng thứ 4).</p>')
    notes+='<h2>3. Thực hành tương tác</h2><p>Chọn loại cấu hình, nhập cấu hình hiện tại và số bước; công cụ giải thích từng bước (chỉ số i, j).</p>'+sim('gen')
    notes+='<h2>4. Bối cảnh lý thuyết và lịch sử</h2>'+callout('info','📜 Nguồn gốc','Thuật toán “hoán vị kế tiếp theo thứ tự từ điển” xuất hiện từ thời Narayana Pandita (Ấn Độ, thế kỷ 14); nó được Knuth trình bày là Algorithm L trong <i>The Art of Computer Programming</i>, tập 4A.')
    notes+='<h2>5. Case study</h2><p>Bài toán chọn 3 trong 10 dịch vụ để triển khai: C(10,3) = 120 tổ hợp, sinh bằng tổ hợp kế tiếp mỗi lần O(k) và không cần lưu cả danh sách.</p><h2>6. Bẫy khi làm bài</h2>'+callout('warn','Chú ý','• Viết ra i và j ở mỗi bước để giám khảo thấy quy trình.<br>• Kiểm tra bước cuối: cấu hình cuối cùng không có cấu hình kế tiếp.<br>• Với đề yêu cầu “k cấu hình tiếp theo”, dừng đúng k.')
    return dict(id='m10',slug='10-phuong-phap-sinh',title='Phương pháp sinh',subtitle='Sinh xâu nhị phân, hoán vị, tổ hợp kế tiếp theo thứ tự từ điển',source='Giáo trình 2016 §3.3 · Đề cương INT1358 mục 3.2 · Slide chương Liệt kê',exam='Câu 4 và câu 3b mọi đề (2017–2024)',time='≈ 3 giờ',
        objectives=['Thực hiện bằng tay ba thuật toán sinh kế tiếp','Viết chương trình C/C++ sinh cấu hình','Xác định cấu hình đầu, cuối và điều kiện dừng','Xử lý đề “k cấu hình liền kề tiếp theo”'],parts=parts,notes=notes,sims=['gen'])
