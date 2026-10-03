# (module, tên, [(công thức, khi nào dùng, dạng đề)])
F=[
('m01','Logic mệnh đề',[
 ('p → q ≡ ¬p ∨ q','Đổi kéo theo thành tuyển để biến đổi / lập bảng','Câu 1a đề tự luận: chứng minh tương đương'),
 ('p → q ≡ ¬q → ¬p (phản đảo)','Chứng minh tương đương, phản chứng','Trắc nghiệm “B hằng đúng?”'),
 ('¬(p ∧ q) ≡ ¬p ∨ ¬q;  ¬(p ∨ q) ≡ ¬p ∧ ¬q','Đưa phủ định vào trong (De Morgan)','Chứng minh tương đương'),
 ('p ↔ q ≡ (p → q) ∧ (q → p)','Tương đương hai chiều','Bảng chân lý'),
 ('n biến → 2ⁿ hàng của bảng chân lý','Đếm số hàng, số hàm Boole (2^(2ⁿ))','Bảng chân lý'),
 ('Hằng đúng: mọi hàng đều Đ; mâu thuẫn: mọi hàng đều S','Kết luận sau khi lập bảng','Trắc nghiệm hằng đúng')]),
('m02','Vị từ và lượng từ',[
 ('¬∀x P(x) ≡ ∃x ¬P(x);  ¬∃x P(x) ≡ ∀x ¬P(x)','Phủ định mệnh đề có lượng từ','Lập phủ định'),
 ('∀x (P(x) ∧ Q(x)) ≡ ∀xP(x) ∧ ∀xQ(x)','Phân phối ∀ qua ∧ (∃ phân phối qua ∨)','Tương đương vị từ'),
 ('Thứ tự lượng từ khác loại không đổi chỗ được: ∀x∃y ≠ ∃y∀x','Dịch câu tiếng Việt sang logic','Dịch mệnh đề')]),
('m03','Tập hợp, độ phức tạp',[
 ('|A ∪ B| = |A| + |B| − |A ∩ B|','Đếm hợp hai tập','Bài tập tập hợp'),
 ('|P(A)| = 2^|A|;  |A × B| = |A|·|B|','Số tập con, số cặp','Bài tập tập hợp'),
 ('A \\ B = A ∩ B̄;  (A ∪ B)‾ = Ā ∩ B̄','Biến đổi biểu thức tập','Chứng minh đẳng thức tập'),
 ('f = O(g) ⇔ ∃C, n₀: |f(n)| ≤ C|g(n)| ∀n ≥ n₀','Xác định bậc tăng','Độ phức tạp'),
 ('1 < log n < n < n log n < n² < n³ < 2ⁿ < n!','So sánh bậc tăng','Độ phức tạp'),
 ('Vòng for lồng nhau độ sâu k, mỗi vòng ~n lần → O(nᵏ)','Đánh giá chương trình','Độ phức tạp')]),
('m04','Nguyên lý đếm',[
 ('Quy tắc cộng: n₁ + n₂ (các việc loại trừ nhau)','“hoặc … hoặc …”','Đếm cơ bản'),
 ('Quy tắc nhân: n₁·n₂·…·nₖ (làm liên tiếp)','“lần lượt … rồi …”','Đếm cơ bản, biển số'),
 ('|A₁ ∪ … ∪ Aₙ| = Σ|Aᵢ| − Σ|Aᵢ∩Aⱼ| + Σ|Aᵢ∩Aⱼ∩Aₖ| − … + (−1)ⁿ⁻¹|A₁∩…∩Aₙ|','Đếm số chia hết cho ít nhất một số; bù trừ','Số nguyên chia hết cho 2, 3, 5…'),
 ('Số bội của k trong 1..N là ⌊N/k⌋','Đếm chia hết','Bù trừ'),
 ('Đếm phần bù: |A| = |U| − |Ā|','Bài “ít nhất một”','Đếm bằng phần bù')]),
('m05','Hoán vị, tổ hợp',[
 ('P(n) = n!','Xếp n vật khác nhau thành hàng','Xếp chỗ'),
 ('A(n,r) = n!/(n−r)!','Chọn r từ n có xếp thứ tự','Chọn có thứ tự'),
 ('C(n,r) = n!/(r!(n−r)!);  C(n,r) = C(n,n−r)','Chọn r từ n không thứ tự','Chọn đội'),
 ('C(n,r) = C(n−1,r−1) + C(n−1,r)','Quan hệ Pascal','Chứng minh'),
 ('(x+y)ⁿ = Σ C(n,k) xⁿ⁻ᵏ yᵏ','Khai triển nhị thức, hệ số','Hệ số của xᵏ'),
 ('Hoán vị lặp: n!/(n₁!n₂!…nₖ!)','Xếp chữ cái có lặp (MISSISSIPPI)','Hoán vị lặp'),
 ('Nghiệm nguyên ≥ 0 của x₁+…+xₖ = n: C(n+k−1, k−1)','“Chia n vật giống nhau vào k hộp”','Nghiệm nguyên có cận (đề thi)'),
 ('Cận dưới xᵢ ≥ aᵢ: đặt yᵢ = xᵢ − aᵢ, thay n bởi n − Σaᵢ','Đưa về nghiệm không âm','Nghiệm nguyên có cận'),
 ('Cận trên xᵢ ≤ bᵢ: bù trừ (vi phạm xᵢ ≥ bᵢ + 1)','Số nghiệm có cận trên','Nghiệm nguyên có cận')]),
('m06','Dirichlet',[
 ('Đặt N vật vào k hộp: có hộp chứa ≥ ⌈N/k⌉ vật','Chứng minh tồn tại','Dirichlet (câu 1b)'),
 ('Để chắc chắn có ≥ r vật cùng hộp cần N ≥ k(r−1)+1','Tìm số vật tối thiểu','“ít nhất bao nhiêu” (bi màu)'),
 ('Chọn k hộp thế nào cho đúng: xác định “hộp” trước, rồi đếm','Bước thiết kế lời giải','Bài tồn tại')]),
('m07','Lập hệ thức truy hồi',[
 ('Chia theo phần tử cuối / bit cuối','Lập aₙ cho xâu nhị phân','Lập truy hồi (câu 2a)'),
 ('Xâu nhị phân dài n không có hai số 0 liên tiếp: aₙ = aₙ₋₁ + aₙ₋₂ (a₁=2, a₂=3)','Mô hình Fibonacci','Xâu cấm'),
 ('Tháp Hà Nội: Hₙ = 2Hₙ₋₁ + 1, H₁ = 1 ⇒ Hₙ = 2ⁿ − 1','Mô hình chia để trị','Tháp Hà Nội'),
 ('Luôn nêu điều kiện đầu','Hoàn chỉnh hệ thức','Mọi bài truy hồi')]),
('m08','Giải hệ thức truy hồi',[
 ('aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ ⇒ r² − c₁r − c₂ = 0','Phương trình đặc trưng','Giải truy hồi bậc 2'),
 ('Hai nghiệm phân biệt: aₙ = α₁r₁ⁿ + α₂r₂ⁿ','Nghiệm phân biệt','Bậc 2'),
 ('Nghiệm kép r₀: aₙ = (α₁ + α₂n)r₀ⁿ','Nghiệm kép','Đề 2017–2020 (câu 2b)'),
 ('Bậc 3: giải r³ − c₁r² − c₂r − c₃ = 0; nghiệm bội m cho (α₀+…+α_{m−1}nᵐ⁻¹)rⁿ','Bậc 3','Trắc nghiệm bậc 3'),
 ('Không thuần nhất: aₙ = nghiệm thuần nhất + nghiệm riêng','F(n) cố định dạng đa thức hoặc sⁿ','Truy hồi không thuần nhất'),
 ('Thay điều kiện đầu để tìm α₁, α₂','Bước cuối','Mọi bài')]),
('m09','Hàm sinh',[
 ('1/(1−x) = Σ xⁿ;  1/(1−ax) = Σ aⁿxⁿ','Dãy hằng, cấp số nhân','Tìm hàm sinh'),
 ('(1+x)ⁿ = Σ C(n,k)xᵏ','Chọn không lặp','Hàm sinh tổ hợp'),
 ('1/(1−x)ᵏ = Σ C(n+k−1, n) xⁿ','Chọn có lặp','Nghiệm nguyên'),
 ('Tích hàm sinh ↔ tổng chỉ số (tích chập)','Đếm theo tổng','Bài đếm nhiều nhóm')]),
('m10','Phương pháp sinh',[
 ('Xâu nhị phân kế tiếp: đổi các bit 1 cuối thành 0, bit 0 cuối cùng thành 1','Sinh xâu','Sinh xâu (câu 4)'),
 ('Hoán vị kế tiếp: tìm i lớn nhất a[i]<a[i+1]; đổi với phần tử nhỏ nhất > a[i] ở bên phải; đảo đoạn sau i','Sinh hoán vị','Hoán vị kế tiếp'),
 ('Tổ hợp kế tiếp: tìm i lớn nhất a[i] ≠ n−k+i; tăng a[i]; a[j]=a[j−1]+1','Sinh tổ hợp','Tổ hợp kế tiếp'),
 ('Số cấu hình: 2ⁿ xâu; n! hoán vị; C(n,k) tổ hợp','Kiểm tra số lượng','Đếm cấu hình')]),
('m11','Quay lui',[
 ('Khung: Try(i): với mỗi giá trị hợp lệ: gán, nếu i = n thì ghi nhận, ngược lại Try(i+1); bỏ gán','Mọi bài quay lui','Viết chương trình (câu 4)'),
 ('Chỉ mở rộng khi thỏa ràng buộc (cắt tỉa sớm)','Giảm không gian tìm kiếm','Quay lui'),
 ('n quân hậu: kiểm cột, đường chéo i−j, đường chéo i+j','Kiểm tra hợp lệ O(1)','Quân hậu')]),
('m12','Cái túi, nhánh cận',[
 ('Sắp theo c/a giảm dần','Chuẩn bị','Cái túi'),
 ('Cận trên g = δ + (b − w)·(c_{k+1}/a_{k+1})','Nhánh cận bài max','Cái túi (câu 5)'),
 ('Cắt nhánh nếu g ≤ FOPT','Cắt tỉa','Cái túi'),
 ('Nghiệm nguyên: chọn xᵢ ∈ {0,1} (hoặc nguyên ≥ 0): mở rộng theo giá trị lớn trước','Thứ tự mở rộng','Cái túi')]),
('m13','Người du lịch',[
 ('Cận dưới ban đầu = tổng các hằng số rút gọn hàng, cột','Bước rút gọn','Người du lịch'),
 ('Hệ số phạt θ(r,c) = (min hàng r bỏ ô (r,c)) + (min cột c bỏ ô (r,c))','Chọn cạnh phân nhánh','TSP'),
 ('Nhánh chứa (r,c): đặt c(c,r)=∞ chống chu trình con; nhánh không chứa: cận += θ','Hai nút con','TSP'),
 ('Cắt khi cận ≥ kỷ lục','Cắt tỉa','TSP')]),
]
