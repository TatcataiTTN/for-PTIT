from hx import *
import math, itertools
def ol(steps): return '<ol>'+''.join(f'<li>{s}</li>' for s in steps)+'</ol>'
def mul(a,b,N):
    r=[0]*(N+1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if i+j<=N: r[i+j]+=x*y
    return r
def module():
    parts=[]
    N=10; g=[1]+[0]*N
    for pr in (lambda e:e%2==0,lambda e:e%2==1,lambda e:e<=4,lambda e:e>=2): g=mul(g,[1 if pr(e) else 0 for e in range(N+1)],N)
    fruit10=g[10]
    dp=[1]+[0]*100
    for c in (1,5,10,50):
        for v in range(c,101): dp[v]+=dp[v-c]
    s=[]
    s.append(sl('<p><b>Hàm sinh</b> là cách “đóng gói” một dãy số vào một chuỗi lũy thừa để dùng phép nhân đa thức đếm tổ hợp. Đề cương INT1358 (mục 2.5) và slide chính thức của PTIT dành riêng một phần cho phương pháp này; đề thi cuối kỳ chủ yếu dùng nó ngầm (bù trừ) còn slide dùng nó tường minh.</p>'+ul(['Định nghĩa hàm sinh, các khai triển thường gặp','Mô hình hóa “chọn có điều kiện” bằng tích các thừa số','Đổi tiền, xúc xắc, số nghiệm nguyên có cận','Liên hệ với hệ thức truy hồi']),'MODULE 9 · Slide chính thức TRR1 (chương Đếm) · Đề cương 2.5','Hàm sinh'))
    s.append(sl(formula('Định nghĩa (slide PTIT)','g(x) = h₀ + h₁x + h₂x² + … = Σᵢ hᵢ·xⁱ',[('{hₙ}','dãy số cần đếm'),('g(x)','hàm sinh của dãy; hệ số của xⁿ là hₙ')])+'<p>Ví dụ (1 + x)ⁿ = Σ C(n,k)xᵏ là hàm sinh của các hệ số tổ hợp. Dãy hữu hạn được bổ sung các số 0 để thành dãy vô hạn.</p>','PHẦN 1 · Nền tảng','Định nghĩa hàm sinh',
        explain='Hàm sinh giống một “chiếc túi đựng dãy số”: số hạng thứ n được cất ở ngăn có nhãn xⁿ. Nhân hai chiếc túi tương ứng với việc kết hợp hai tình huống độc lập.'))
    s.append(sl(table(['Hàm sinh','Khai triển','Dãy'],[['1/(1 − x)','1 + x + x² + …','1, 1, 1, …'],['1/(1 − cx)','Σ cⁿxⁿ','cⁿ'],['1/(1 − x)²','Σ (n+1)xⁿ','n + 1'],['x/(1 − x)²','Σ n·xⁿ','n'],['1/(1 − x)^k','Σ C(n+k−1,k−1)xⁿ','số nghiệm nguyên không âm'],['(1 − xᵐ⁺¹)/(1 − x)','1 + x + … + xᵐ','đoạn 0..m'],['1/(1 − x²)','1 + x² + x⁴ + …','chẵn'],['x/(1 − x²)','x + x³ + x⁵ + …','lẻ'],['x/(1 − x − x²)','x + x² + 2x³ + 3x⁴ + …','Fibonacci']]),'PHẦN 1 · Nền tảng','Các khai triển thường gặp (slide PTIT)'))
    parts.append(dict(title='Nền tảng',bullets=['Định nghĩa','Khai triển thường gặp'],slides=s))
    s=[]
    s.append(sl(ul(['Mỗi <b>loại đối tượng</b> ứng một thừa số; số mũ của x = số lượng chọn của loại đó.','Điều kiện “chẵn” → 1 + x² + x⁴ + …; “lẻ” → x + x³ + …; “không quá 4” → 1 + x + … + x⁴; “ít nhất 2” → x² + x³ + …; “bất kỳ” → 1/(1 − x).','Tích các thừa số; <b>hệ số của xⁿ</b> là số cách chọn tổng n đối tượng.'])+callout('good','Cùng ý với nghiệm nguyên','Số nghiệm của x₁ + … + x_k = N với lᵢ ≤ xᵢ ≤ hᵢ chính là hệ số của x^N trong Π (x^lᵢ + … + x^hᵢ) (Module 5).'),'PHẦN 2 · Phương pháp','Quy tắc mô hình hóa'))
    s.append(sl(callout('info','Slide PTIT, Example 24','Chọn n quả từ 4 loại: số táo chẵn, số chuối lẻ, số cam không quá 4, số đào ít nhất 2.')+formula('Hàm sinh','g(x) = (1 + x² + x⁴ + …)(x + x³ + x⁵ + …)(1 + x + x² + x³ + x⁴)(x² + x³ + …)')+f'<p>= [1/(1−x²)]·[x/(1−x²)]·[(1−x⁵)/(1−x)]·[x²/(1−x)]. Số cách chọn n quả là hệ số của xⁿ; với n = 10 ta được <b>{fruit10}</b> (tính bằng nhân đa thức; đối chiếu liệt kê trực tiếp). Slide nhận xét: “tính tay rất nhiều nhưng máy tính làm dễ dàng”.</p>'+sim('gf'),'PHẦN 2 · Phương pháp','Ví dụ trong slide: chọn quả'))
    parts.append(dict(title='Phương pháp',bullets=['Mô hình hóa bằng thừa số','Chọn quả có điều kiện'],slides=s))
    s=[]
    s.append(sl(callout('info','Slide PTIT, Exercise 1','Tìm hàm sinh cho số cách đổi M (nghìn đồng) bằng các tờ 1, 5, 10, 50 nghìn không hạn chế.')+ol(['Mỗi loại tờ c nghìn cho thừa số 1 + xᶜ + x²ᶜ + … = 1/(1 − xᶜ).','g(x) = 1/[(1 − x)(1 − x⁵)(1 − x¹⁰)(1 − x⁵⁰)].',f'Số cách đổi M là hệ số x^M; với M = 100: <b>{dp[100]}</b> cách.']),'PHẦN 3 · Ví dụ','Ví dụ 1: đổi tiền'))
    from itertools import product
    dice=sum(1 for t in product(range(1,7),repeat=4) if sum(t)==14)
    s.append(sl(callout('info','Ví dụ 2','Gieo 4 con xúc xắc, có bao nhiêu kết quả có tổng bằng 14?')+ol(['Mỗi con: x + x² + … + x⁶ = x(1 − x⁶)/(1 − x).','g(x) = x⁴(1 − x⁶)⁴/(1 − x)⁴.',f'Hệ số của x¹⁴ = <b>{dice}</b> (đối chiếu liệt kê 6⁴ = 1296 kết quả).']),'PHẦN 3 · Ví dụ','Ví dụ 2: xúc xắc'))
    s.append(sl(callout('info','Ví dụ 3 (đề 2019–2020, câu 3a) bằng hàm sinh','Số nghiệm của x₁ + … + x₆ = 30 với 8 ≥ x₂ ≥ 3 và 6 ≥ x₄ ≥ 2 là hệ số của x³⁰ trong (1/(1−x))⁴·(x³+…+x⁸)(x²+…+x⁶) = <b>58500</b> (cùng kết quả bù trừ ở Module 5).'),'PHẦN 3 · Ví dụ','Ví dụ 3: nghiệm nguyên có cận'))
    s.append(sl(callout('info','Ví dụ 4: giải truy hồi bằng hàm sinh','aₙ = 3aₙ₋₁ − 2aₙ₋₂, a₀ = 1, a₁ = 3.')+ol(['G(x)(1 − 3x + 2x²) = a₀ + (a₁ − 3a₀)x = 1.','G(x) = 1/[(1 − x)(1 − 2x)] = 2/(1 − 2x) − 1/(1 − x).','aₙ = 2·2ⁿ − 1 = 2ⁿ⁺¹ − 1.']),'PHẦN 3 · Ví dụ','Ví dụ 4: hàm sinh và truy hồi'))
    parts.append(dict(title='Ví dụ có lời giải',bullets=['Đổi tiền (slide)','Xúc xắc','Nghiệm nguyên có cận','Truy hồi'],slides=s))
    s=[]
    s.append(sl(ul(['<b>“Ít nhất”</b> nghĩa là bắt đầu từ xˡ, không phải từ 1.','<b>Hệ số của xⁿ</b>, không phải giá trị g(n).','<b>Cận trên</b> → đa thức hữu hạn; không cận → 1/(1 − x).','<b>Kiểm tra bằng máy:</b> nhân đa thức chặt tại xᴺ, đừng khai triển vô hạn.','<b>Đề thi TRR1</b> thường yêu cầu bù trừ; hàm sinh là cách kiểm chứng độc lập.']),'PHẦN 4 · Bẫy và mở rộng','Năm bẫy thường gặp'))
    s.append(sl('<p>Tổng quát hóa: hàm sinh mũ Σ hₙxⁿ/n! dùng cho bài toán đếm có thứ tự (hoán vị lặp). Nằm ngoài yêu cầu TRR1 nhưng là bước tiếp theo tự nhiên.</p>','PHẦN 4 · Bẫy và mở rộng','Mở rộng'))
    parts.append(dict(title='Bẫy và mở rộng',bullets=['Năm bẫy','Hàm sinh mũ'],slides=s))
    s=[]
    s.append(sl('<p>Trong xác suất rời rạc, hàm sinh của phân phối tổng hai biến độc lập bằng tích hai hàm sinh: cách tính phân phối tổng điểm của nhiều con xúc xắc hoặc nhiều lượt trả lời trắc nghiệm.</p>','PHẦN 5 · Ứng dụng và ôn tập','Case study: phân phối tổng điểm'))
    s.append(sl(ul(['Thuộc các khai triển cơ bản.','Mô hình hóa điều kiện chọn bằng thừa số.','Biết nhân đa thức chặt để tính hệ số.'])+callout('good','Tiếp theo','Chương 3: liệt kê. Module 10 bắt đầu với phương pháp sinh.'),'PHẦN 5 · Ứng dụng và ôn tập','Tổng kết'))
    parts.append(dict(title='Ứng dụng và tổng kết',bullets=['Xác suất','Checklist'],slides=s))
    notes='<h2>1. Nội dung chi tiết</h2><p>Nhân hai hàm sinh cho tích chập của hai dãy: nếu g = Σ aᵢxⁱ và h = Σ bⱼxʲ thì hệ số xⁿ của g·h là Σ aᵢbₙ₋ᵢ, đúng số cách chia n thành phần thuộc hai loại. Vì vậy hàm sinh biến bài toán “chọn” thành bài toán nhân đa thức.</p><h2>2. Ví dụ chi tiết có lời giải</h2>'
    notes+=ex('1. Hệ số của (1 + x + x²)⁵','<p>Hệ số của x¹⁰ là 1 (mọi yᵢ = 2); hệ số của x⁵ là số nghiệm y₁+…+y₅ = 5 với 0 ≤ yᵢ ≤ 2: 51.</p>')
    notes+=ex('2. Tổng chữ số','<p>Số nghiệm của x₁ + x₂ + x₃ = 12 với 1 ≤ x₁ ≤ 4, 2 ≤ x₂ ≤ 6, 0 ≤ x₃ ≤ 8 là hệ số x¹² của (x+…+x⁴)(x²+…+x⁶)(1+…+x⁸): 19 (liệt kê).</p>')
    notes+=ex('3. Chọn quả (bài luyện)','<p>Chọn 10 quả với táo chẵn, cam ≤ 3, chuối là bội của 3, lê ≤ 1: hệ số x¹⁰ của (1+x²+…)(1+x+x²+x³)(1+x³+x⁶+…)(1+x) = 14.</p>')
    notes+=ex('4. Hàm sinh của aₙ = 3n + 2','<p>Σ(3n+2)xⁿ = 3x/(1−x)² + 2/(1−x) = (2 + x)/(1 − x)².</p>')
    notes+=ex('5. Fibonacci','<p>G(x)(1 − x − x²) = x ⇒ G = x/(1 − x − x²) = x + x² + 2x³ + 3x⁴ + 5x⁵ + …</p>')
    notes+='<h2>3. Thực hành tương tác</h2><p>Nhập cận từng biến dạng lo-hi (để trống hi = vô hạn) để tính hệ số của xᴺ:</p>'+sim('gf')
    notes+='<h2>4. Bối cảnh lý thuyết và lịch sử</h2>'+callout('info','📜 Nguồn gốc','Hàm sinh được Abraham de Moivre giới thiệu (khoảng 1730) để giải bài toán truy hồi, và Laplace phát triển thành công cụ xác suất. Thuật ngữ “hàm sinh” (generating function) phổ biến từ Laplace.')
    notes+='<h2>5. Case study</h2><p>Bài toán đổi tiền “bao nhiêu cách đổi 100 nghìn bằng tờ 1, 5, 10, 50 nghìn” chính là bài tập trong slide PTIT; máy tính đếm được '+str(dp[100])+' cách chỉ bằng vòng lặp quy hoạch động tương ứng với nhân dần thừa số 1/(1 − xᶜ).</p><h2>6. Bẫy khi làm bài</h2>'+callout('warn','Chú ý','• Ghi rõ hàm sinh và số mũ tương ứng.<br>• Kiểm tra hệ số bằng đếm trực tiếp ở N nhỏ.<br>• Không trộn hàm sinh thường với hàm sinh mũ.')
    return dict(id='m09',slug='09-ham-sinh',title='Hàm sinh',subtitle='Định nghĩa, khai triển, mô hình hóa chọn có điều kiện, đổi tiền',source='Slide chính thức TRR1 (chương Đếm) · Đề cương INT1358 mục 2.5 · Rosen §8.4',exam='Không có câu riêng; dùng để kiểm chứng câu đếm',time='≈ 2 giờ',
        objectives=['Viết hàm sinh cho bài toán chọn có điều kiện','Biết các khai triển cơ bản','Tính hệ số của xⁿ bằng nhân đa thức','Đối chiếu hàm sinh với bù trừ ở Module 5'],parts=parts,notes=notes,sims=['gf'])
