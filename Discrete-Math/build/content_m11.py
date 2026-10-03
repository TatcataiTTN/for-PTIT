from hx import *
import sys, os, itertools, math
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'orig'))
from cpp_snippets import CPP
def ol(steps): return '<ol>'+''.join(f'<li>{s}</li>' for s in steps)+'</ol>'
def perms(n): return list(itertools.permutations(range(1,n+1)))
def calls_perm(n): return sum(math.perm(n,i-1) for i in range(1,n+1))
def module():
    parts=[]
    s=[]
    s.append(sl('<p><b>Quay lui</b> (backtracking) xây cấu hình từng thành phần: chọn giá trị cho x₁, rồi x₂, …; khi gặp ngõ cụt (vi phạm điều kiện) thì <i>quay lại</i> thay lựa chọn trước đó. Đó là cách liệt kê khi cấu hình có ràng buộc, và là nền của <b>nhánh cận</b> ở Module 12.</p>'+ul(['Khung Try(i) và cây tìm kiếm','Điều kiện chấp nhận và cắt nhánh','Quay lui cho xâu nhị phân, hoán vị, tổ hợp','Đếm số lời gọi, so với phương pháp sinh']),'MODULE 11 · Giáo trình 2016 §3.4 · Đề cương 3.3','Quay lui'))
    s.append(sl('<pre><code>void Try(int i){\n    for (mỗi ứng viên v của x[i]) {\n        if (chấp nhận v) {\n            x[i] = v;  &lt;ghi nhớ trạng thái&gt;;\n            if (i == n) &lt;ghi nhận nghiệm&gt;;\n            else Try(i + 1);\n            &lt;hoàn trả trạng thái&gt;;    // quay lui\n        }\n    }\n}\n// gọi Try(1)</code></pre>'+callout('info','Năm bước','1) duyệt ứng viên; 2) kiểm tra chấp nhận; 3) gán và ghi nhớ; 4) nếu đủ thì ghi nhận, ngược lại đệ quy; 5) hoàn trả (bỏ đánh dấu used, giảm tổng…).'),'PHẦN 1 · Nền tảng','Khung thuật toán quay lui',
        explain='Giống đi trong mê cung: đến ngã rẽ chọn một hướng; nếu bế tắc thì quay lại ngã rẽ gần nhất và thử hướng khác. Việc “quay lại” do lời gọi đệ quy trả về.'))
    parts.append(dict(title='Nền tảng',bullets=['Khung Try(i)','Năm bước'],slides=s))
    s=[]
    s.append(sl('<p>Xâu nhị phân độ dài n (2ⁿ nghiệm):</p><pre><code>'+esc(CPP['bin_bt'])+'</code></pre>'+viz('bt'),'PHẦN 2 · Phương pháp','Quay lui: xâu nhị phân'))
    s.append(sl('<p>Hoán vị (dùng mảng used để đảm bảo khác nhau):</p><pre><code>'+esc(CPP['perm_bt'])+'</code></pre>','PHẦN 2 · Phương pháp','Quay lui: hoán vị'))
    s.append(sl('<p>Tổ hợp chập k (cận trên n − k + i cắt sớm các nhánh không đủ phần tử):</p><pre><code>'+esc(CPP['comb_bt'])+'</code></pre>','PHẦN 2 · Phương pháp','Quay lui: tổ hợp'))
    parts.append(dict(title='Phương pháp: ba mẫu quay lui',bullets=['Xâu nhị phân','Hoán vị','Tổ hợp'],slides=s))
    s=[]
    s.append(sl(callout('info','Ví dụ 1 (3.3a, kiểm nghiệm n = 3)','Thuật toán quay lui hoán vị của 1,2,3.')+'<p>Thứ tự in: '+', '.join(''.join(map(str,p)) for p in perms(3))+' (trùng thứ tự từ điển vì thử v tăng dần).</p><p>Số lần gọi Try: Try(1) 1 lần, Try(2) 3 lần, Try(3) 6 lần: tổng '+str(calls_perm(3))+' lời gọi (n! = 6 nghiệm in ra).</p>','PHẦN 3 · Ví dụ','Ví dụ 1: hoán vị n = 3'))
    s.append(sl(callout('info','Ví dụ 2 (3.6a, n = 5, k = 3)','Tổ hợp chập 3 của {1..5} bằng quay lui.')+'<p>'+', '.join('('+','.join(map(str,c))+')' for c in itertools.combinations(range(1,6),3))+f' — {math.comb(5,3)} tổ hợp.</p>','PHẦN 3 · Ví dụ','Ví dụ 2: tổ hợp n = 5, k = 3'))
    s.append(sl(callout('info','Ví dụ 3 (slide PTIT, Exercise 10)','Liệt kê mọi X ∈ {0,1}ⁿ có Σxᵢ = K và Σaᵢxᵢ = S.')+ol(['Try(i, cnt, sum): với v = 0, 1: cnt′ = cnt + v; sum′ = sum + aᵢ·v.','Cắt nhánh nếu cnt′ > K, hoặc sum′ > S, hoặc cnt′ + (n − i) < K.','Khi i = n: in nếu cnt′ = K và sum′ = S.']),'PHẦN 3 · Ví dụ','Ví dụ 3: tập con K phần tử có tổng S'))
    s.append(sl(callout('info','Ví dụ 4: 4 quân hậu','Đặt 4 quân hậu lên bàn cờ 4×4 không ăn nhau.')+'<p>Quay lui theo từng hàng, thử cột 1..4, loại cột và hai đường chéo bị chiếm. Có 2 nghiệm (theo cột ở mỗi hàng): (2,4,1,3) và (3,1,4,2). Với n = 8 có 92 nghiệm.</p>','PHẦN 3 · Ví dụ','Ví dụ 4: N quân hậu'))
    parts.append(dict(title='Ví dụ có lời giải',bullets=['Hoán vị n = 3','Tổ hợp','Tập con có tổng S','4 quân hậu'],slides=s))
    s=[]
    s.append(sl(ul(['<b>Quên hoàn trả</b> used[v] = false sau lời gọi đệ quy ⇒ mất nghiệm.','<b>Sai cận</b> của vòng lặp (tổ hợp: n − k + i).','<b>Không cắt nhánh</b> ⇒ thành vét cạn.','<b>Nhầm sinh và quay lui:</b> sinh cần hàm kế tiếp; quay lui cần đệ quy.','<b>In sai chỉ số</b>: x[1..n] hay x[0..n−1].']),'PHẦN 4 · Bẫy và mở rộng','Năm bẫy thường gặp'))
    s.append(sl('<p>Số lời gọi Try khi liệt kê hoán vị của n phần tử: Σ_{i=1..n} n!/(n − i + 1)!; với n = 8 là '+f'{calls_perm(8):,}'.replace(',','.')+' (chỉ hơn n! = 40 320 một chút), còn nhánh cận/cắt tỉa giúp giảm mạnh khi có ràng buộc.</p>','PHẦN 4 · Bẫy và mở rộng','Mở rộng: số lời gọi'))
    parts.append(dict(title='Bẫy và mở rộng',bullets=['Năm bẫy','Đếm lời gọi'],slides=s))
    s=[]
    s.append(sl('<p>Sudoku, xếp lịch thi, tô màu bản đồ, N quân hậu đều giải bằng quay lui với cắt nhánh (kiểm tra ràng buộc sớm). Trình biên dịch Prolog dùng quay lui làm cơ chế suy diễn cơ bản.</p>','PHẦN 5 · Ứng dụng và ôn tập','Case study: Sudoku và Prolog'))
    s.append(sl(ul(['Viết đúng khung Try và hoàn trả trạng thái.','Cài đặt cho xâu nhị phân, hoán vị, tổ hợp.','Biết cắt nhánh để giảm số lời gọi.'])+callout('good','Tiếp theo','Chương 4: tối ưu. Module 12 thêm hàm cận vào quay lui để có nhánh cận.'),'PHẦN 5 · Ứng dụng và ôn tập','Tổng kết'))
    parts.append(dict(title='Ứng dụng và tổng kết',bullets=['Sudoku','Checklist'],slides=s))
    notes='<h2>1. Nội dung chi tiết</h2><p>Cây tìm kiếm quay lui có nút là phương án bộ phận (x₁,…,x_k); lá là phương án đầy đủ. Quay lui duyệt cây theo chiều sâu; cắt nhánh khi phương án bộ phận không thể mở rộng thành nghiệm. Đây chính là cơ sở của thuật toán nhánh cận (giáo trình hình 4.2).</p><h2>2. Ví dụ chi tiết có lời giải</h2>'
    notes+=ex('1. Xâu nhị phân n = 3 (3.9a)','<p>Thứ tự in: 000, 001, 010, 011, 100, 101, 110, 111. Try(1) gọi 1 lần, Try(2) 2 lần, Try(3) 4 lần: tổng 7 = 2³ − 1 lời gọi.</p>')
    notes+=ex('2. Xâu nhị phân không có hai bit 1 liền nhau','<p>Điều kiện chấp nhận: nếu x[i−1] = 1 thì không cho x[i] = 1. Với n = 5 có 13 xâu (số Fibonacci F₇).</p>')
    notes+=ex('3. Tổng tập con','<p>Tập {3, 5, 7, 9, 11}, tìm tập con có tổng 16: chỉ có {5, 11} và {7, 9} (đã kiểm chứng bằng liệt kê 31 tập con khác rỗng). Quay lui cắt nhánh ngay khi tổng đang chọn vượt 16.</p>')
    notes+=ex('4. Hoán vị không có điểm bất động (số mất thứ tự)','<p>Điều kiện chấp nhận v ≠ i: D₄ = 9 hoán vị (Module 7).</p>')
    notes+=ex('5. Code đề thi 4a','<p>Chương trình liệt kê hoán vị bằng quay lui (đề 2023–2024, câu 4a) là mẫu perm_bt ở trên; thêm phép nhập n từ bàn phím bằng <code>cin &gt;&gt; n</code>.</p>')
    notes+='<h2>3. Thực hành tương tác</h2><p>Quan sát từng bước duyệt cây (thử, bỏ qua, in):</p>'+sim('bt')
    notes+='<h2>4. Bối cảnh lý thuyết và lịch sử</h2>'+callout('info','📜 Nguồn gốc','Thuật ngữ “backtrack” được D. H. Lehmer đặt trong thập niên 1950; Bài toán tám quân hậu do Max Bezzel nêu năm 1848 và được Gauss cùng nhiều người nghiên cứu. Quay lui là kỹ thuật cốt lõi của lập trình logic và ràng buộc.')
    notes+='<h2>5. Case study</h2><p>Xếp lịch thi cho 5 môn vào 3 ca sao cho không có sinh viên thi hai môn cùng ca: gán ca cho từng môn (x[i] ∈ {1,2,3}), kiểm tra xung đột với các môn đã gán; cắt nhánh ngay khi xung đột.</p><h2>6. Bẫy khi làm bài</h2>'+callout('warn','Chú ý','• Ghi rõ điều kiện dừng i = n và điều kiện chấp nhận.<br>• Nêu số lời gọi khi đề hỏi độ phức tạp.<br>• Kiểm nghiệm với n nhỏ (n = 3) đúng như đề yêu cầu.')
    return dict(id='m11',slug='11-quay-lui',title='Quay lui',subtitle='Khung Try(i), cắt nhánh, liệt kê xâu, hoán vị, tổ hợp',source='Giáo trình 2016 §3.4 · Đề cương INT1358 mục 3.3 · Slide chương Liệt kê',exam='Câu 3b, câu 4 (đề 2017–2024)',time='≈ 3 giờ',
        objectives=['Viết khung quay lui và hoàn trả trạng thái','Cài đặt quay lui cho xâu, hoán vị, tổ hợp','Cắt nhánh bằng điều kiện chấp nhận','Đếm số lời gọi và so với phương pháp sinh'],parts=parts,notes=notes,sims=['bt'])
