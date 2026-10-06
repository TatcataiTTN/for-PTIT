# Bài thực hành Python cho TRR1. Mỗi bài: đề, định dạng vào/ra, lời giải mẫu (chương trình độc lập đọc stdin),
# test mẫu (hiện cho học viên) + test ẩn. Đáp án mọi test do chính lời giải mẫu sinh ra, rồi py_build.py đối chiếu
# bằng hàm check() cài đặt theo cách KHÁC (vét cạn / công thức khác) trước khi xuất ra data/python/problems.json.
import random, itertools, math
from math import comb, factorial

PROBS = []
R = random.Random(20261006)

def P(id, mod, lv, title, stmt, inp, out, cons, samples, tests, sol, check, hint, expl, starter):
    PROBS.append(dict(id=id, mod=mod, lv=lv, title=title, stmt=stmt, inp=inp, out=out, cons=cons,
                      samples=samples, tests=tests, sol=sol.strip('\n') + '\n', check=check,
                      hint=hint, expl=expl, starter=starter.strip('\n') + '\n'))

def lines(*a): return '\n'.join(str(x) for x in a) + '\n'
def nums(v): return ' '.join(map(str, v))

# ---------------------------------------------------------------- 1. Tập hợp
def t_sets():
    ts = []
    for _ in range(8):
        n, m = R.randint(1, 8), R.randint(1, 8)
        ts.append(lines(f'{n} {m}', nums(R.sample(range(1, 16), n)), nums(R.sample(range(1, 16), m))))
    ts.append(lines('2 2', '1 2', '3 4'))
    ts.append(lines('3 3', '5 6 7', '7 6 5'))
    ts.append(lines('300 5', nums(R.sample(range(1, 1001), 300)), nums(R.sample(range(1, 1001), 5))))
    return ts
def c_sets(inp, out):
    L = inp.split('\n'); n, m = map(int, L[0].split()); A = list(map(int, L[1].split())); B = list(map(int, L[2].split()))
    U = sorted(set(A + B)); I = [x for x in sorted(A) if x in B]; D = [x for x in sorted(A) if x not in B]
    S = sorted([x for x in A if x not in B] + [x for x in B if x not in A])
    f = lambda v: nums(v) if v else 'EMPTY'
    return out.split('\n')[:-1] == [f(U), f(I), f(D), f(S), str(2 ** n)]
P('tap-hop', 'm03', 1, 'Phép toán trên tập hợp',
  'Cho hai tập hợp số nguyên A (n phần tử) và B (m phần tử), mỗi tập gồm các phần tử đôi một khác nhau. Hãy in ra: A ∪ B, A ∩ B, A \\ B, A △ B (hiệu đối xứng), mỗi tập trên một dòng, các phần tử <b>tăng dần</b>, cách nhau một dấu cách; tập rỗng in <code>EMPTY</code>. Dòng thứ 5 in số tập con của A.',
  'Dòng 1: <code>n m</code>. Dòng 2: n số của A. Dòng 3: m số của B.', '5 dòng như mô tả.', '1 ≤ n, m ≤ 300; 1 ≤ giá trị ≤ 1000.',
  [lines('5 4', '1 2 3 4 5', '4 5 6 7'), lines('2 2', '1 2', '3 4')], t_sets(),
  '''
n, m = map(int, input().split())
A = set(map(int, input().split()))
B = set(map(int, input().split()))
def show(s):
    print(' '.join(map(str, sorted(s))) if s else 'EMPTY')
show(A | B)
show(A & B)
show(A - B)
show(A ^ B)
print(2 ** len(A))
''', c_sets,
  'Dùng kiểu set của Python: <code>|</code> hợp, <code>&amp;</code> giao, <code>-</code> hiệu, <code>^</code> hiệu đối xứng. |P(A)| = 2ⁿ (Python tính số nguyên lớn không tràn).',
  'Bốn phép toán có sẵn trên set, in sau khi sắp xếp. Số tập con của tập n phần tử là 2ⁿ (mỗi phần tử chọn hoặc không). Độ phức tạp O((n+m) log(n+m)).',
  '''
n, m = map(int, input().split())
A = set(map(int, input().split()))
B = set(map(int, input().split()))
# TODO: in A|B, A&B, A-B, A^B (tăng dần, rỗng in EMPTY), rồi 2**n
''')

# ---------------------------------------------------------------- 2. Phân loại công thức logic
LOGIC_KNOWN = {
    '(((p<=q) and (q<=r))<=(p<=r))': 'TAUTOLOGY\n8\n',
    '(p and (not p))': 'CONTRADICTION\n0\n',
    '((p<=q)==((not q)<=(not p)))': 'TAUTOLOGY\n8\n',
    '(p<=q)': 'CONTINGENT\n6\n',
    '((p or q) and (not (p and q)))': 'CONTINGENT\n4\n',
    '((not (p and q))==((not p) or (not q)))': 'TAUTOLOGY\n8\n',
    '((p<=(q<=r))==((p and q)<=r))': 'TAUTOLOGY\n8\n',
    '(((p<=q) and (q<=p))!=(p==q))': 'CONTRADICTION\n0\n',
    '(p or q or r)': 'CONTINGENT\n7\n',
    '((p and q)<=(p or r))': 'TAUTOLOGY\n8\n',
    '((p<=q)<=p)': 'CONTINGENT\n4\n',
}
def c_logic(inp, out): return LOGIC_KNOWN[inp.strip()] == out
P('logic-phan-loai', 'm01', 1, 'Phân loại công thức logic bằng bảng chân lý',
  'Cho một công thức logic theo biến <code>p, q, r</code> viết bằng cú pháp Python. Hãy lập bảng chân lý trên cả 8 bộ giá trị (p, q, r) và in: dòng 1 là <code>TAUTOLOGY</code> (hằng đúng), <code>CONTRADICTION</code> (mâu thuẫn) hoặc <code>CONTINGENT</code> (còn lại); dòng 2 là số bộ giá trị làm công thức đúng. Công thức không nhất thiết chứa đủ ba biến.<br><b>Cú pháp:</b> <code>not</code>, <code>and</code>, <code>or</code>; <code>a==b</code> là a ↔ b; <code>a!=b</code> là a ⊕ b; <code>a&lt;=b</code> là a → b (với giá trị logic, False ≤ True nên đúng bảng chân lý của kéo theo). Đề luôn bọc ngoặc đầy đủ để tránh nhầm thứ tự ưu tiên.',
  'Một dòng chứa công thức.', 'Hai dòng như mô tả.', 'Độ dài công thức ≤ 200 ký tự, chỉ gồm p, q, r, ngoặc và các toán tử trên.',
  [lines('(((p<=q) and (q<=r))<=(p<=r))'), lines('(p<=q)')], [lines(k) for k in LOGIC_KNOWN],
  '''
from itertools import product
e = input()
t = 0
for p, q, r in product([False, True], repeat=3):
    if eval(e):
        t += 1
print('TAUTOLOGY' if t == 8 else 'CONTRADICTION' if t == 0 else 'CONTINGENT')
print(t)
''', c_logic,
  '<code>itertools.product([False, True], repeat=3)</code> sinh 8 bộ giá trị; <code>eval(s)</code> tính chuỗi biểu thức với các biến p, q, r đang có.',
  'Duyệt 2³ = 8 hàng của bảng chân lý, đếm số hàng cho giá trị đúng: 8 ⇒ hằng đúng, 0 ⇒ mâu thuẫn. Với n biến thì 2ⁿ hàng. Cách này chính là điều đề thi yêu cầu khi nói “dùng bảng chân lý”.',
  '''
from itertools import product
e = input()
# TODO: duyệt 8 bộ (p, q, r), đếm số bộ làm eval(e) đúng, rồi in kết quả
''')

# ---------------------------------------------------------------- 3. Ma trận vị từ / lượng từ
def t_pred():
    ts = [lines('3 3', '1 1 1', '1 1 1', '1 1 1'), lines('2 3', '0 0 0', '0 0 0'), lines('3 3', '1 0 0', '0 1 0', '0 0 1'),
          lines('2 2', '1 1', '0 1'), lines('1 4', '1 1 0 1')]
    for _ in range(6):
        n, m = R.randint(1, 6), R.randint(1, 6)
        ts.append(lines(f'{n} {m}', *[nums([R.randint(0, 1) if R.random() < .8 else 1 for _ in range(m)]) for _ in range(n)]))
    return ts
def c_pred(inp, out):
    L = inp.split('\n'); n, m = map(int, L[0].split()); P_ = [list(map(int, L[1 + i].split())) for i in range(n)]
    rows = [sum(r) for r in P_]; cols = [sum(P_[i][j] for i in range(n)) for j in range(m)]
    T = lambda b: 'TRUE' if b else 'FALSE'
    exp = [T(sum(rows) == n * m), T(sum(rows) > 0), T(all(r > 0 for r in rows)), T(any(r == m for r in rows)),
           T(all(c > 0 for c in cols)), T(any(c == n for c in cols))]
    return out.split('\n')[:-1] == exp
P('luong-tu', 'm02', 1, 'Lượng từ trên miền hữu hạn',
  'Miền x gồm n phần tử, miền y gồm m phần tử. Vị từ P(x, y) cho bởi bảng 0/1 (1 là đúng). Hãy in ra (mỗi dòng <code>TRUE</code> hoặc <code>FALSE</code>) giá trị của sáu mệnh đề, theo thứ tự: ∀x∀y P, ∃x∃y P, ∀x∃y P, ∃x∀y P, ∀y∃x P, ∃y∀x P.',
  'Dòng 1: <code>n m</code>. Tiếp theo n dòng, mỗi dòng m số 0/1: dòng x, số thứ y là P(x, y).', '6 dòng như mô tả.', '1 ≤ n, m ≤ 6.',
  [lines('2 2', '1 1', '0 1'), lines('3 3', '1 0 0', '0 1 0', '0 0 1')], t_pred(),
  '''
n, m = map(int, input().split())
P = [list(map(int, input().split())) for _ in range(n)]
T = lambda b: 'TRUE' if b else 'FALSE'
print(T(all(P[x][y] for x in range(n) for y in range(m))))
print(T(any(P[x][y] for x in range(n) for y in range(m))))
print(T(all(any(P[x][y] for y in range(m)) for x in range(n))))
print(T(any(all(P[x][y] for y in range(m)) for x in range(n))))
print(T(all(any(P[x][y] for x in range(n)) for y in range(m))))
print(T(any(all(P[x][y] for x in range(n)) for y in range(m))))
''', c_pred,
  'Trên miền hữu hạn, ∀ chính là <code>all(...)</code> và ∃ là <code>any(...)</code>. Lượng từ viết trước là vòng ngoài: ∀x∃y P ⇒ <code>all(any(P[x][y] for y) for x)</code>.',
  '∀ = hội, ∃ = tuyển trên các phần tử của miền. Thứ tự lượng từ khác loại quan trọng: ∀x∃y P (mỗi hàng có ít nhất một số 1) khác ∃y∀x P (có một cột toàn số 1). Ví dụ ma trận đơn vị 3×3: ∀x∃y đúng nhưng ∃y∀x sai.',
  '''
n, m = map(int, input().split())
P = [list(map(int, input().split())) for _ in range(n)]
T = lambda b: 'TRUE' if b else 'FALSE'
# TODO: in 6 dòng: ∀x∀y, ∃x∃y, ∀x∃y, ∃x∀y, ∀y∃x, ∃y∀x  (dùng all / any)
''')

# ---------------------------------------------------------------- 4. Đếm lệnh (độ phức tạp)
def c_cplx(inp, out):
    N = int(inp)
    if N <= 60:
        c = 0
        for i in range(1, N + 1):
            for j in range(i, N + 1):
                for k in range(j, N + 1): c += 1
        return out == f'{c}\n'
    return out == f'{comb(N + 2, 3)}\n'
P('dem-lenh', 'm03', 2, 'Đếm số lần thực hiện lệnh (độ phức tạp)',
  'Xét đoạn chương trình:<pre><code>c = 0\nfor i in range(1, N + 1):\n    for j in range(i, N + 1):\n        for k in range(j, N + 1):\n            c += 1</code></pre>Cho N, hãy in giá trị của c sau khi chạy xong. Với N lớn không thể mô phỏng trực tiếp, hãy tìm công thức.',
  'Một số nguyên N.', 'Một số nguyên: giá trị của c.', '1 ≤ N ≤ 10⁹.',
  [lines(3), lines(10)], [lines(x) for x in (1, 2, 5, 17, 40, 100, 1000, 12345, 10 ** 6, 10 ** 9)],
  '''
N = int(input())
print(N * (N + 1) * (N + 2) // 6)
''', c_cplx,
  'c đếm số bộ (i, j, k) thỏa 1 ≤ i ≤ j ≤ k ≤ N. Đó là số tổ hợp lặp chập 3 của N phần tử (hoặc số cách chọn 3 số có thể trùng).',
  'Số bộ i ≤ j ≤ k trong [1..N] bằng C(N+2, 3) = N(N+1)(N+2)/6 (tổ hợp lặp, hoặc chọn i < j+1 < k+2 trong N+2 số). Mô phỏng ba vòng lặp mất Θ(N³) nên không chạy nổi N = 10⁹; công thức mất O(1). Đây là ví dụ cho thấy phân tích độ phức tạp gắn với bài toán đếm.',
  '''
N = int(input())
# TODO: tìm công thức (đừng mô phỏng ba vòng for)
''')

# ---------------------------------------------------------------- 5. Tập con có tổng S: đếm
def c_subcount(inp, out):
    L = inp.split('\n'); n, S = map(int, L[0].split()); a = list(map(int, L[1].split()))
    if n <= 16:
        c = sum(1 for m in range(1 << n) if sum(a[i] for i in range(n) if m >> i & 1) == S)
        return out == f'{c}\n'
    ways = {0: 1}
    for x in a:
        nw = dict(ways)
        for s, c in ways.items():
            if s + x <= S: nw[s + x] = nw.get(s + x, 0) + c
        ways = nw
    return out == f'{ways.get(S, 0)}\n'
def t_subcount():
    ts = [lines('4 10', '1 2 3 4'), lines('3 100', '1 2 3'), lines('1 5', '5'), lines('6 7', '7 7 1 6 1 7')]
    for _ in range(5):
        n = R.randint(4, 14); ts.append(lines(f'{n} {R.randint(5, 40)}', nums([R.randint(1, 12) for _ in range(n)])))
    ts.append(lines('40 3000', nums([R.randint(1, 100) for _ in range(40)])))
    ts.append(lines('40 1000', nums([R.randint(1, 60) for _ in range(40)])))
    return ts
P('tap-con-tong', 'm11', 2, 'Đếm tập con có tổng bằng S',
  'Cho dãy n số nguyên dương a₁, …, aₙ và số S. Đếm số cách chọn tập con các <b>chỉ số</b> (các giá trị trùng nhau ở vị trí khác nhau tính là khác nhau) sao cho tổng các phần tử được chọn đúng bằng S. Gợi ý kết hợp: với n lớn, vét cạn 2ⁿ không đủ nhanh.',
  'Dòng 1: <code>n S</code>. Dòng 2: n số a₁ … aₙ.', 'Một số nguyên: số tập con thỏa mãn.', '1 ≤ n ≤ 40; 1 ≤ aᵢ ≤ 100; 1 ≤ S ≤ 3000.',
  [lines('4 10', '1 2 3 4'), lines('3 100', '1 2 3')], t_subcount(),
  '''
n, S = map(int, input().split())
a = list(map(int, input().split()))
dp = [0] * (S + 1)
dp[0] = 1
for x in a:
    for s in range(S, x - 1, -1):
        dp[s] += dp[s - x]
print(dp[S])
''', c_subcount,
  'Quy hoạch động: dp[s] = số tập con có tổng s. Khi thêm phần tử x, dp mới[s] = dp[s] + dp[s − x]; duyệt s giảm dần để mỗi phần tử chỉ dùng một lần.',
  'Vét cạn mất O(2ⁿ) (n = 40 là 10¹²). Cách đếm theo tổng cho O(n·S). Đây là bước đệm trước khi dùng quay lui để <i>liệt kê</i> các tập con đó (bài kế tiếp).',
  '''
n, S = map(int, input().split())
a = list(map(int, input().split()))
# TODO: dp[s] = số tập con có tổng s
''')

# ---------------------------------------------------------------- 6. Tập con có tổng S: liệt kê (quay lui)
def c_sublist(inp, out):
    L = inp.split('\n'); n, S = map(int, L[0].split()); a = list(map(int, L[1].split()))
    res = []
    for m in range(1 << n):
        x = [(m >> (n - 1 - i)) & 1 for i in range(n)]
        if sum(a[i] for i in range(n) if x[i]) == S: res.append(nums([a[i] for i in range(n) if x[i]]))
    exp = f'{len(res)}\n' + ''.join(r + '\n' for r in res)
    return out == exp
def t_sublist():
    ts = [lines('7 50', '5 10 15 20 25 30 35'), lines('4 6', '1 2 3 4'), lines('3 100', '1 2 3'), lines('1 1', '1'), lines('4 5', '5 5 1 4')]
    for _ in range(6):
        n = R.randint(5, 12); ts.append(lines(f'{n} {R.randint(8, 40)}', nums([R.randint(1, 15) for _ in range(n)])))
    return ts
P('liet-ke-tap-con', 'm11', 2, 'Liệt kê tập con có tổng S (quay lui)',
  'Cho n số nguyên dương a₁, …, aₙ và S. Liệt kê <b>tất cả</b> các tập con (theo chỉ số) có tổng đúng bằng S. Mỗi tập con in trên một dòng gồm các giá trị được chọn theo thứ tự chỉ số tăng. Các tập con in theo thứ tự từ điển của vector (x₁, …, xₙ) với xᵢ ∈ {0, 1} (so sánh x₁ trước, <b>0 đứng trước 1</b>). Dòng đầu in số tập con tìm được.<br>Đây là bài 6, bài tập chương 3 của giáo trình (ví dụ: dãy 5 10 15 20 25 30 35, M = 50).',
  'Dòng 1: <code>n S</code>. Dòng 2: n số.', 'Dòng 1: số tập con k. Tiếp theo k dòng, mỗi dòng một tập con.', '1 ≤ n ≤ 12; 1 ≤ aᵢ ≤ 15; 1 ≤ S ≤ 60.',
  [lines('4 6', '1 2 3 4'), lines('3 100', '1 2 3')], t_sublist(),
  '''
n, S = map(int, input().split())
a = list(map(int, input().split()))
res = []
cur = []
def Try(i, s):
    if i == n:
        if s == S:
            res.append(' '.join(map(str, cur)))
        return
    Try(i + 1, s)              # x_i = 0
    if s + a[i] <= S:          # cắt nhánh: tổng đã vượt S thì bỏ
        cur.append(a[i])
        Try(i + 1, s + a[i])   # x_i = 1
        cur.pop()
Try(0, 0)
print(len(res))
for r in res:
    print(r)
''', c_sublist,
  'Khung quay lui Try(i): thử xᵢ = 0 rồi xᵢ = 1; thử 0 trước thì tự nhiên ra đúng thứ tự từ điển. Cắt nhánh khi tổng đã chọn vượt S.',
  'Cây tìm kiếm nhị phân độ sâu n; cắt nhánh sớm khi tổng > S giảm mạnh số nút duyệt (vì mọi aᵢ dương). Trường hợp xấu nhất vẫn O(2ⁿ). Thứ tự duyệt “0 trước 1” cho đúng thứ tự từ điển của vector x, giống thuật toán quay lui trong giáo trình.',
  '''
n, S = map(int, input().split())
a = list(map(int, input().split()))
res = []      # mỗi phần tử là một dòng kết quả
cur = []      # các giá trị đang được chọn
def Try(i, s):
    # TODO: i == n thì ghi nhận nếu s == S; ngược lại thử x_i = 0 rồi x_i = 1 (có cắt nhánh)
    pass
Try(0, 0)
print(len(res))
for r in res:
    print(r)
''')

# ---------------------------------------------------------------- 7. Bù trừ
def c_incl(inp, out):
    L = inp.split('\n'); a, b = map(int, L[0].split()); k = int(L[1]); d = list(map(int, L[2].split()))
    if b - a <= 200000:
        return out == f'{sum(1 for x in range(a, b + 1) if any(x % m == 0 for m in d))}\n'
    tot = 0
    for mask in range(1, 1 << k):
        l = 1; bits = 0
        for i in range(k):
            if mask >> i & 1: l = l * d[i] // math.gcd(l, d[i]); bits += 1
        tot += (1 if bits % 2 else -1) * (b // l - (a - 1) // l)
    return out == f'{tot}\n'
def t_incl():
    ts = [lines('1 100', 2, '4 6'), lines('1 10', 1, '1'), lines('5 5', 3, '5 7 9'), lines('10 20', 2, '25 30')]
    for _ in range(5):
        k = R.randint(2, 6); a = R.randint(1, 500); ts.append(lines(f'{a} {a + R.randint(10, 5000)}', k, nums([R.randint(2, 30) for _ in range(k)])))
    ts.append(lines(f'1 {10**18}', 10, nums([2, 3, 5, 7, 11, 13, 17, 19, 23, 29])))
    ts.append(lines(f'{10**17} {10**18}', 12, nums([6, 10, 15, 21, 35, 77, 91, 143, 187, 221, 247, 299])))
    return ts
P('bu-tru', 'm04', 2, 'Nguyên lý bù trừ: đếm số chia hết',
  'Có bao nhiêu số nguyên trong đoạn [a, b] chia hết cho <b>ít nhất một</b> trong k số d₁, …, d_k? (Dạng quen thuộc trong đề: “từ 542 đến 7761, chia hết cho ít nhất một trong ba số 3, 7, 14”.) Với b lên tới 10¹⁸ không thể duyệt từng số.',
  'Dòng 1: <code>a b</code>. Dòng 2: k. Dòng 3: k số d₁ … d_k.', 'Một số nguyên.', '1 ≤ a ≤ b ≤ 10¹⁸; 1 ≤ k ≤ 12; 1 ≤ dᵢ ≤ 10⁶.',
  [lines('542 7761', 3, '3 7 14'), lines('1 100', 2, '4 6')], t_incl(),
  '''
from math import gcd
a, b = map(int, input().split())
k = int(input())
d = list(map(int, input().split()))
total = 0
def go(i, l, c):
    global total
    if i == k:
        if c:
            total += (1 if c % 2 else -1) * (b // l - (a - 1) // l)
        return
    go(i + 1, l, c)                       # không chọn d[i]
    nl = l * d[i] // gcd(l, d[i])
    if nl <= b:                           # bội chung > b thì không có số nào
        go(i + 1, nl, c + 1)              # chọn d[i]
go(0, 1, 0)
print(total)
''', c_incl,
  'Số bội của m trong [a, b] là <code>b//m − (a−1)//m</code>. Bù trừ: cộng với tập chọn lẻ số d, trừ với tập chọn chẵn, mỗi tập dùng bội chung nhỏ nhất (lcm).',
  '|A₁ ∪ … ∪ A_k| = Σ(−1)^{|T|+1}·|∩_{i∈T} Aᵢ|. Giao các tập “chia hết cho dᵢ (i ∈ T)” là các số chia hết cho lcm. Có 2^k − 1 tập T (k ≤ 12 nên ≤ 4095); cắt nhánh khi lcm vượt b. Sai lầm hay gặp: dùng tích thay vì lcm (ví dụ 7 và 14), hoặc quên dấu.',
  '''
from math import gcd
a, b = map(int, input().split())
k = int(input())
d = list(map(int, input().split()))
# TODO: duyệt mọi tập con khác rỗng của d, dùng lcm; cộng/trừ b//l - (a-1)//l
''')

# ---------------------------------------------------------------- 8. Nghiệm nguyên có cận
def c_intsol(inp, out):
    L = inp.split('\n'); k, N = map(int, L[0].split()); LO = []; HI = []
    for i in range(k):
        lo, hi = map(int, L[1 + i].split()); LO.append(lo); HI.append(hi)
    M = N - sum(LO); tot = 0
    if M >= 0:
        bounded = [i for i in range(k) if HI[i] >= 0]
        for r in range(len(bounded) + 1):
            for sub in itertools.combinations(bounded, r):
                rem = M - sum(HI[i] - LO[i] + 1 for i in sub)
                if rem >= 0: tot += (-1) ** r * comb(rem + k - 1, k - 1)
    return out == f'{tot}\n'
def t_intsol():
    ts = [lines('6 35', '0 -1', '1 3', '4 7', '0 -1', '0 -1', '0 -1'), lines('3 10', '0 -1', '0 -1', '0 -1'),
          lines('2 5', '3 4', '3 4'), lines('4 20', '2 5', '1 3', '0 -1', '4 9')]
    for _ in range(6):
        k = R.randint(2, 7); rows = []
        for _ in range(k):
            lo = R.randint(0, 6); hi = -1 if R.random() < .35 else lo + R.randint(0, 9); rows.append(f'{lo} {hi}')
        ts.append(lines(f'{k} {R.randint(10, 60)}', *rows))
    ts.append(lines('8 500', *['0 -1'] * 4, *['5 60'] * 4))
    return ts
P('nghiem-nguyen', 'm05', 3, 'Nghiệm nguyên không âm có cận',
  'Đếm số nghiệm nguyên của phương trình x₁ + x₂ + … + x_k = N thỏa mãn lᵢ ≤ xᵢ ≤ hᵢ với mọi i (hᵢ = −1 nghĩa là không có cận trên; mọi lᵢ ≥ 0). Đây là dạng xuất hiện trong hầu hết đề thi (ví dụ đề 01 năm 2023–24: x₁+…+x₆ = 35, 3 ≥ x₂ ≥ 1, 7 ≥ x₃ ≥ 4).',
  'Dòng 1: <code>k N</code>. Tiếp theo k dòng, dòng i gồm <code>lᵢ hᵢ</code>.', 'Một số nguyên (có thể rất lớn).', '1 ≤ k ≤ 8; 0 ≤ N ≤ 500; 0 ≤ lᵢ; hᵢ = −1 hoặc hᵢ ≥ lᵢ.',
  [lines('6 35', '0 -1', '1 3', '4 7', '0 -1', '0 -1', '0 -1'), lines('3 10', '0 -1', '0 -1', '0 -1')], t_intsol(),
  '''
k, N = map(int, input().split())
dp = [1] + [0] * N                  # dp[s] = số cách với các biến đã xét có tổng s
for _ in range(k):
    lo, hi = map(int, input().split())
    if hi < 0 or hi > N:
        hi = N
    nd = [0] * (N + 1)
    for s in range(N + 1):
        if dp[s]:
            for v in range(lo, hi + 1):
                if s + v > N:
                    break
                nd[s + v] += dp[s]
    dp = nd
print(dp[N])
''', c_intsol,
  'Cách 1 (lập trình): quy hoạch động theo từng biến. Cách 2 (như bài thi): đặt yᵢ = xᵢ − lᵢ, tổng còn M = N − Σlᵢ, rồi bù trừ các trường hợp vi phạm cận trên: Σ(−1)^r·C(M − Σ(hᵢ−lᵢ+1) + k − 1, k − 1).',
  'Số nghiệm không âm của y₁+…+y_k = M không cận là C(M+k−1, k−1). Mỗi cận trên yᵢ ≤ hᵢ−lᵢ bị vi phạm khi yᵢ ≥ hᵢ−lᵢ+1; bù trừ qua các tập biến vi phạm. DP làm O(k·N²), dễ cài và không bị sai dấu; bù trừ cho công thức chuẩn khi trình bày bằng tay. Nên tự làm cả hai và so khớp.',
  '''
k, N = map(int, input().split())
bounds = [tuple(map(int, input().split())) for _ in range(k)]   # (lo, hi), hi = -1: không cận
# TODO: đếm nghiệm (DP theo từng biến, hoặc đặt y_i = x_i - lo_i rồi bù trừ)
''')

# ---------------------------------------------------------------- 9. P(n), A(n,k), C(n,k)
def c_pnk(inp, out):
    n, k = map(int, inp.split())
    f = 1
    for i in range(2, n + 1): f *= i
    a = 1
    for i in range(n - k + 1, n + 1): a *= i
    row = [1]
    for _ in range(n): row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return out == f'{f}\n{a}\n{row[k]}\n'
P('hoan-vi-to-hop', 'm05', 1, 'Hoán vị, chỉnh hợp, tổ hợp',
  'Cho n và k. In ba số, mỗi số một dòng: P(n) = n!, số chỉnh hợp chập k của n phần tử A(n, k) và số tổ hợp C(n, k).',
  'Một dòng: <code>n k</code>.', 'Ba dòng: n!, A(n, k), C(n, k).', '0 ≤ k ≤ n ≤ 60.',
  [lines('5 2'), lines('10 0')], [lines(f'{n} {k}') for n, k in [(0, 0), (1, 1), (6, 6), (7, 3), (12, 5), (20, 10), (30, 15), (45, 1), (60, 30), (60, 60)]],
  '''
from math import factorial, comb
n, k = map(int, input().split())
print(factorial(n))
print(factorial(n) // factorial(n - k))
print(comb(n, k))
''', c_pnk,
  'Python có sẵn <code>math.factorial</code> và <code>math.comb</code> (từ Python 3.8). Chỉnh hợp A(n, k) = n!/(n−k)!. Số nguyên Python không tràn.',
  'P(n) = n!; A(n, k) = n(n−1)…(n−k+1); C(n, k) = A(n, k)/k!. Nếu đề thi không cho dùng thư viện, hãy tự viết vòng lặp nhân (đã có kiểm tra theo tam giác Pascal ở phía chấm).',
  '''
n, k = map(int, input().split())
# TODO: in n!, A(n,k), C(n,k)  (math.factorial, math.comb hoặc tự cài đặt)
''')

# ---------------------------------------------------------------- 10. Dirichlet
def c_pig(inp, out):
    L = inp.split('\n'); m, r = map(int, L[0].split()); l, c, s = map(int, L[1].split())
    # N lớn nhất vẫn có thể tránh = (số hộp)·(r−1); cần thêm 1
    return out == f'{(m + 1) * (r - 1) + 1}\n{l * c * (s - 1) + 1}\n'
P('dirichlet', 'm06', 1, 'Nguyên lý Dirichlet: hai dạng thường gặp',
  '<b>Phần 1 (điểm thi).</b> Đề có m câu, mỗi câu đúng được 1 điểm, sai 0 điểm, mọi thí sinh làm hết các câu. Cần ít nhất bao nhiêu thí sinh để chắc chắn có r thí sinh cùng điểm?<br><b>Phần 2 (bi).</b> Hộp chứa vô hạn bi, mỗi viên thuộc một trong L loại kích thước và C màu. Cần lấy ít nhất bao nhiêu viên để chắc chắn có s viên giống nhau cả loại lẫn màu?<br>(Đề gốc: m = 6, r = 4 ⇒ 22; L = 22, C = 2, s = 9 ⇒ 353.)',
  'Dòng 1: <code>m r</code>. Dòng 2: <code>L C s</code>.', 'Hai dòng: đáp số phần 1 và phần 2.', '1 ≤ m ≤ 100; 2 ≤ r, s ≤ 100; 1 ≤ L, C ≤ 100.',
  [lines('6 4', '22 2 9'), lines('3 2', '1 1 5')], [lines(f'{m} {r}', f'{l} {c} {s}') for m, r, l, c, s in [(1, 2, 1, 1, 2), (10, 3, 5, 5, 3), (30, 10, 7, 9, 4), (100, 100, 100, 100, 100), (5, 5, 2, 3, 6), (17, 4, 11, 2, 7)]],
  '''
m, r = map(int, input().split())
L, C, s = map(int, input().split())
print((m + 1) * (r - 1) + 1)
print(L * C * (s - 1) + 1)
''', c_pig,
  'Số “hộp” là số khả năng: điểm từ 0 đến m nên có m + 1 hộp; bi có L·C kiểu. Cần k·(r−1)+1 đối tượng để chắc chắn một hộp có ≥ r.',
  'Nếu chỉ có k·(r−1) đối tượng thì có thể mỗi hộp đúng r−1 (chưa đủ). Thêm một đối tượng nữa thì theo Dirichlet có hộp chứa ≥ r. Bước quan trọng là xác định đúng số hộp: điểm 0…m (m+1 hộp), không phải m.',
  '''
m, r = map(int, input().split())
L, C, s = map(int, input().split())
# TODO: in (số hộp)*(r-1)+1 cho từng phần
''')

# ---------------------------------------------------------------- 11. Truy hồi tuyến tính: tính a_n
def c_rec(inp, out):
    L = inp.split('\n'); d, n = map(int, L[0].split()); c = list(map(int, L[1].split())); a = list(map(int, L[2].split()))
    from collections import deque
    w = deque(a, maxlen=d)
    if n < d: return out == f'{a[n]}\n'
    for _ in range(d, n + 1):
        w.append(sum(c[j] * w[-1 - j] for j in range(d)))
    return out == f'{w[-1]}\n'
def t_rec():
    ts = [lines('2 10', '1 1', '0 1'), lines('3 5', '2 5 -6', '9 8 50'), lines('2 1', '3 4', '5 6'), lines('1 20', '2', '1'), lines('4 30', '1 1 1 1', '0 0 0 1')]
    for _ in range(4):
        d = R.randint(2, 5); ts.append(lines(f'{d} {R.randint(d, 60)}', nums([R.randint(-4, 5) for _ in range(d)]), nums([R.randint(-5, 9) for _ in range(d)])))
    ts.append(lines('2 1500', '1 1', '0 1'))
    ts.append(lines('3 1000', '1 1 1', '1 1 2'))
    return ts
P('truy-hoi-tinh', 'm07', 2, 'Tính số hạng thứ n của hệ thức truy hồi',
  'Cho hệ thức truy hồi tuyến tính hệ số hằng bậc d: aₙ = c₁·aₙ₋₁ + c₂·aₙ₋₂ + … + c_d·aₙ₋_d với n ≥ d, cùng d điều kiện đầu a₀, …, a_{d−1}. Hãy tính aₙ (số nguyên chính xác, không lấy dư).<br>Ví dụ giáo trình/đề: Fibonacci (d = 2, c = 1 1, a₀ = 0, a₁ = 1); đề 01 năm 2023–24 câu 3a: aₙ = 2aₙ₋₁ + 5aₙ₋₂ − 6aₙ₋₃ với a₀ = 9, a₁ = 8, a₂ = 50.',
  'Dòng 1: <code>d n</code>. Dòng 2: c₁ … c_d. Dòng 3: a₀ … a_{d−1}.', 'Một số nguyên aₙ.', '1 ≤ d ≤ 5; 0 ≤ n ≤ 1500; |cᵢ| ≤ 9; |aᵢ| ≤ 100 (kết quả có thể rất nhiều chữ số nhưng < 4300 chữ số).',
  [lines('2 10', '1 1', '0 1'), lines('3 5', '2 5 -6', '9 8 50')], t_rec(),
  '''
d, n = map(int, input().split())
c = list(map(int, input().split()))
a = list(map(int, input().split()))
for i in range(d, n + 1):
    a.append(sum(c[j] * a[i - 1 - j] for j in range(d)))
print(a[n])
''', c_rec,
  'Tính lần lượt từ a_d đến aₙ bằng vòng lặp, giữ danh sách các số hạng. Đừng dùng đệ quy thuần túy không nhớ (độ phức tạp mũ).',
  'Mỗi số hạng cần O(d) phép tính ⇒ O(n·d). Đệ quy trực tiếp aₙ = c₁aₙ₋₁ + … gọi lại các số hạng nhỏ nhiều lần nên mất thời gian mũ; vòng lặp (hoặc ghi nhớ) tránh điều đó. Dùng kết quả này để kiểm tra nghiệm đóng bạn tìm được bằng tay ở Module 8.',
  '''
d, n = map(int, input().split())
c = list(map(int, input().split()))
a = list(map(int, input().split()))
# TODO: tính a[d], ..., a[n] bằng vòng lặp rồi in a[n]
''')

# ---------------------------------------------------------------- 12. Nghiệm kép
def c_dbl(inp, out):
    c1, c2, a0, a1 = map(int, inp.split())
    got = out.split()
    if len(got) != 3: return False
    r, al, be = map(int, got)
    if c1 != 2 * r or c2 != -r * r: return False
    seq = [a0, a1]
    for _ in range(8): seq.append(c1 * seq[-1] + c2 * seq[-2])
    return all((al + be * n) * r ** n == seq[n] for n in range(10))
def t_dbl():
    ts = [lines('-36 -324 8 -468'), lines('6 -9 1 9'), lines('2 -1 5 7'), lines('-2 -1 3 -2')]
    for _ in range(8):
        r = R.choice([x for x in range(-30, 31) if x not in (0,)]); al, be = R.randint(-20, 20), R.randint(-20, 20)
        ts.append(lines(f'{2 * r} {-r * r} {al} {(al + be) * r}'))
    return ts
P('nghiem-kep', 'm08', 2, 'Truy hồi bậc hai có nghiệm kép',
  'Cho hệ thức aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ (n ≥ 2) với a₀, a₁. Biết phương trình đặc trưng r² − c₁r − c₂ = 0 có <b>nghiệm kép nguyên r ≠ 0</b> và nghiệm tổng quát aₙ = (α + β·n)·rⁿ với α, β nguyên. Hãy in ba số <code>r α β</code>.<br>Ví dụ đề thi: aₙ = −36aₙ₋₁ − 324aₙ₋₂, a₀ = 8, a₁ = −468 ⇒ r = −18, α = 8, β = 18.',
  'Một dòng: <code>c₁ c₂ a₀ a₁</code>.', 'Một dòng: <code>r α β</code>.', 'Đảm bảo c₁² + 4c₂ = 0, r = c₁/2 là số nguyên khác 0, |r| ≤ 30.',
  [lines('-36 -324 8 -468'), lines('6 -9 1 9')], t_dbl(),
  '''
c1, c2, a0, a1 = map(int, input().split())
r = c1 // 2              # nghiệm kép: r = c1/2 vì c1^2 + 4*c2 = 0
alpha = a0               # a0 = (alpha + beta*0) * r^0
beta = a1 // r - alpha   # a1 = (alpha + beta) * r  =>  beta = a1/r - alpha
print(r, alpha, beta)
''', c_dbl,
  'Phương trình đặc trưng có nghiệm kép khi Δ = c₁² + 4c₂ = 0, khi đó r = c₁/2. Thay n = 0 và n = 1 để tìm α, β: a₀ = α, a₁ = (α + β)·r.',
  'Nghiệm kép r cho hai nghiệm cơ sở rⁿ và n·rⁿ. Điều kiện đầu cho hệ 2 phương trình: α = a₀; (α + β)r = a₁ ⇒ β = a₁/r − a₀. Kiểm tra bằng cách tính vài số hạng bằng truy hồi và so với (α + βn)rⁿ (phía chấm cũng kiểm tra bằng cách đó với n = 0…9).',
  '''
c1, c2, a0, a1 = map(int, input().split())
# TODO: r = c1/2; alpha = a0; beta = a1/r - a0
''')

# ---------------------------------------------------------------- 13. Tháp Hà Nội
def hanoi_bfs(n):
    start = tuple([0] * n); goal = tuple([2] * n)
    from collections import deque
    prev = {start: None}; q = deque([start])
    while q:
        s = q.popleft()
        if s == goal: break
        for a in range(3):
            top_a = next((i for i in range(n) if s[i] == a), None)
            if top_a is None: continue
            for b in range(3):
                if a == b: continue
                top_b = next((i for i in range(n) if s[i] == b), None)
                if top_b is not None and top_b < top_a: continue
                t = list(s); t[top_a] = b; t = tuple(t)
                if t not in prev: prev[t] = (s, 'ABC'[a] + ' ' + 'ABC'[b]); q.append(t)
    path = []; s = goal
    while prev[s]: s, m = prev[s]; path.append(m)
    return path[::-1]
def c_hanoi(inp, out):
    n = int(inp); L = out.split('\n')[:-1]
    if L[0] != str(2 ** n - 1) or len(L) != 2 ** n: return False
    pegs = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}
    for mv in L[1:]:
        a, b = mv.split()
        d = pegs[a].pop()
        if pegs[b] and pegs[b][-1] < d: return False
        pegs[b].append(d)
    if pegs['C'] != list(range(n, 0, -1)): return False
    if n <= 5: return L[1:] == hanoi_bfs(n)
    return True
P('thap-ha-noi', 'm07', 2, 'Tháp Hà Nội',
  'Có 3 cọc A, B, C. Ban đầu n đĩa xếp trên cọc A (đĩa nhỏ nằm trên đĩa lớn). Chuyển toàn bộ sang cọc C, mỗi lần một đĩa, không đặt đĩa lớn lên đĩa nhỏ, được dùng cọc B làm trung gian. In số lần chuyển ít nhất, rồi in dãy các bước chuyển tối ưu, mỗi bước một dòng <code>X Y</code> (chuyển đĩa trên cùng của cọc X sang cọc Y). Lời giải tối ưu là duy nhất.',
  'Một số nguyên n.', 'Dòng 1: số bước Hₙ. Tiếp theo Hₙ dòng, mỗi dòng <code>X Y</code>.', '1 ≤ n ≤ 10.',
  [lines(1), lines(2)], [lines(x) for x in (3, 4, 5, 6, 7, 8, 10)],
  '''
n = int(input())
moves = []
def hanoi(k, a, c, b):
    if k == 0:
        return
    hanoi(k - 1, a, b, c)          # chuyển k-1 đĩa từ a sang b (trung gian c)
    moves.append(a + ' ' + c)      # chuyển đĩa lớn nhất từ a sang c
    hanoi(k - 1, b, c, a)          # chuyển k-1 đĩa từ b sang c (trung gian a)
hanoi(n, 'A', 'C', 'B')
print(len(moves))
for m in moves:
    print(m)
''', c_hanoi,
  'Hệ thức truy hồi Hₙ = 2Hₙ₋₁ + 1 chính là cấu trúc đệ quy: chuyển n−1 đĩa lên cọc trung gian, chuyển đĩa lớn nhất, rồi chuyển n−1 đĩa về đích.',
  'Hₙ = 2ⁿ − 1 (giải truy hồi Hₙ = 2Hₙ₋₁ + 1, H₁ = 1). Hàm đệ quy hanoi(k, a, c, b) ánh xạ thẳng từ lập luận lập truy hồi trong giáo trình. Phía chấm mô phỏng từng bước (kiểm tra hợp lệ và trạng thái cuối) và với n ≤ 5 so với lời giải BFS ngắn nhất.',
  '''
n = int(input())
moves = []
def hanoi(k, a, c, b):
    # TODO: chuyển k đĩa từ cọc a sang cọc c, dùng cọc b làm trung gian
    pass
hanoi(n, 'A', 'C', 'B')
print(len(moves))
for m in moves:
    print(m)
''')

# ---------------------------------------------------------------- 14. Xâu nhị phân có k số 1 liên tiếp
def c_runs(inp, out):
    n, k = map(int, inp.split())
    if n <= 14:
        return out == f'{sum(1 for t in itertools.product("01", repeat=n) if "1" * k in "".join(t))}\n'
    # đếm xâu KHÔNG có k số 1 liên tiếp bằng DP theo độ dài chuỗi 1 cuối cùng
    st = [0] * k; st[0] = 1
    for _ in range(n):
        ns = [0] * k; ns[0] = sum(st)
        for j in range(1, k): ns[j] = st[j - 1]
        st = ns
    return out == f'{2 ** n - sum(st)}\n'
P('k-so-1-lien-tiep', 'm07', 3, 'Xâu nhị phân chứa k số 1 liên tiếp',
  'Đếm số xâu nhị phân độ dài n chứa <b>ít nhất một dãy k số 1 liên tiếp</b> (đề 01 năm 2023–24 câu 3b: tìm hệ thức truy hồi cho số các xâu này). Gợi ý: đếm phần bù, tức số xâu <i>không</i> chứa k số 1 liên tiếp.',
  'Một dòng: <code>n k</code>.', 'Một số nguyên.', '1 ≤ k ≤ n ≤ 200.',
  [lines('5 2'), lines('4 3')], [lines(f'{n} {k}') for n, k in [(1, 1), (3, 1), (6, 3), (10, 2), (14, 5), (20, 4), (40, 7), (100, 3), (200, 10), (200, 200)]],
  '''
n, k = map(int, input().split())
f = [0] * (n + 1)          # f[i] = số xâu độ dài i KHÔNG có k số 1 liên tiếp
for i in range(n + 1):
    if i < k:
        f[i] = 2 ** i
    else:
        f[i] = sum(f[i - j] for j in range(1, k + 1))
print(2 ** n - f[n])
''', c_runs,
  'Xâu không có k số 1 liên tiếp kết thúc bằng 0, 10, 110, …, (k−1 số 1 rồi 0): fᵢ = fᵢ₋₁ + fᵢ₋₂ + … + fᵢ₋ₖ. Đáp số = 2ⁿ − fₙ.',
  'Phân loại theo số bit 1 cuối xâu (0 đến k−1) và bit 0 đứng ngay trước chúng: fᵢ = Σ_{j=1..k} fᵢ₋ⱼ với fᵢ = 2ⁱ khi i < k. Với k = 2 đó là dãy Fibonacci. Kết quả cuối 2ⁿ − fₙ. Phía chấm kiểm tra bằng vét cạn khi n ≤ 14 và bằng DP theo độ dài chuỗi 1 cuối cùng khi n lớn.',
  '''
n, k = map(int, input().split())
# TODO: f[i] = số xâu dài i không có k số 1 liên tiếp; in 2**n - f[n]
''')

# ---------------------------------------------------------------- 15. Số thuận nghịch tổng chữ số N
def c_pal(inp, out):
    L, N = map(int, inp.split())
    if L <= 8:
        c = 0
        for x in range(10 ** (L - 1), 10 ** L):
            s = str(x)
            if s == s[::-1] and sum(map(int, s)) == N: c += 1
        return out == f'{c}\n'
    # nửa đầu: đếm số dãy chữ số bằng đa thức
    h = (L + 1) // 2; poly = {0: 1}
    for t in range(h):
        w = 1 if (L % 2 and t == h - 1) else 2; nxt = {}
        for s, v in poly.items():
            for d in range(1 if t == 0 else 0, 10): nxt[s + w * d] = nxt.get(s + w * d, 0) + v
        poly = nxt
    return out == f'{poly.get(N, 0)}\n'
P('thuan-nghich', 'm05', 3, 'Số thuận nghịch có tổng chữ số cho trước',
  'Có bao nhiêu số có đúng L chữ số (chữ số đầu khác 0) là số thuận nghịch (đối xứng, đọc xuôi ngược như nhau) và có tổng các chữ số bằng N? (Dạng đề trắc nghiệm: “số có 9 chữ số, thuận nghịch, tổng chữ số N = 16”.)',
  'Một dòng: <code>L N</code>.', 'Một số nguyên.', '1 ≤ L ≤ 30; 1 ≤ N ≤ 9L.',
  [lines('4 10'), lines('3 10')], [lines(f'{l} {n}') for l, n in [(1, 5), (2, 4), (5, 7), (6, 12), (7, 20), (8, 36), (9, 16), (9, 17), (15, 60), (30, 100), (30, 270)]],
  '''
L, N = map(int, input().split())
h = (L + 1) // 2
dp = {0: 1}                       # dp[tổng đã đặt] = số cách
for t in range(h):
    w = 1 if (L % 2 == 1 and t == h - 1) else 2     # chữ số giữa (L lẻ) chỉ tính một lần
    nd = {}
    for s, c in dp.items():
        for d in range(1 if t == 0 else 0, 10):
            ns = s + w * d
            if ns <= N:
                nd[ns] = nd.get(ns, 0) + c
    dp = nd
print(dp.get(N, 0))
''', c_pal,
  'Số thuận nghịch L chữ số được xác định bởi nửa đầu h = ⌈L/2⌉ chữ số. Tổng chữ số = 2·(tổng nửa đầu), trừ chữ số giữa nếu L lẻ (chỉ tính một lần). Chữ số đầu ≥ 1.',
  'Biến thành bài đếm nghiệm có cận: 2(x₁+…+x_{h}) = N (L chẵn) hoặc 2(x₁+…+x_{h−1}) + x_h = N (L lẻ) với 1 ≤ x₁ ≤ 9 và 0 ≤ xᵢ ≤ 9. Đáp án bằng DP theo từng chữ số (hoặc bù trừ). Phía chấm vét cạn khi L ≤ 8 và dùng đa thức khi L lớn.',
  '''
L, N = map(int, input().split())
# TODO: chỉ cần đếm nửa đầu (h = (L+1)//2 chữ số); chữ số đầu từ 1 đến 9
''')

# ---------------------------------------------------------------- 16. Hàm sinh: chọn quả
def c_gf(inp, out):
    L = inp.split('\n'); k, n = map(int, L[0].split()); rules = []
    for i in range(k):
        lo, hi, par = L[1 + i].split(); rules.append((int(lo), int(hi), par))
    ok = lambda r, x: x >= r[0] and (r[1] < 0 or x <= r[1]) and (r[2] == 'A' or (r[2] == 'E') == (x % 2 == 0))
    from functools import lru_cache
    @lru_cache(None)
    def f(i, rem):
        if i == k: return 1 if rem == 0 else 0
        return sum(f(i + 1, rem - x) for x in range(rem + 1) if ok(rules[i], x))
    return out == f'{f(0, n)}\n'
def t_gf():
    ts = [lines('4 10', '0 -1 E', '0 -1 O', '0 4 A', '2 -1 A'), lines('2 5', '0 -1 A', '0 -1 A'), lines('3 6', '1 2 A', '0 3 E', '1 -1 O')]
    for _ in range(6):
        k = R.randint(2, 5); rows = []
        for _ in range(k):
            lo = R.randint(0, 3); hi = -1 if R.random() < .4 else lo + R.randint(0, 6); rows.append(f'{lo} {hi} {R.choice("AEO")}')
        ts.append(lines(f'{k} {R.randint(5, 40)}', *rows))
    ts.append(lines('5 150', '0 -1 A', '1 -1 O', '2 40 E', '0 -1 A', '3 -1 A'))
    return ts
P('ham-sinh-chon-qua', 'm09', 3, 'Hàm sinh: đếm cách chọn vật có điều kiện',
  'Có k loại quả. Với loại i, số quả chọn xᵢ phải thỏa lᵢ ≤ xᵢ ≤ hᵢ (hᵢ = −1: không giới hạn trên) và có điều kiện chẵn/lẻ: <code>A</code> (bất kỳ), <code>E</code> (xᵢ chẵn), <code>O</code> (xᵢ lẻ). Có bao nhiêu cách chọn tổng cộng đúng n quả?<br>Ví dụ ở slide (Example 24): 4 loại táo/chuối/cam/đào; táo chẵn, chuối lẻ, cam không quá 4, đào ít nhất 2. Hàm sinh của cả bài là tích các hàm sinh từng loại; đáp số là hệ số của xⁿ.',
  'Dòng 1: <code>k n</code>. Tiếp theo k dòng: <code>lᵢ hᵢ pᵢ</code> (pᵢ ∈ A/E/O).', 'Một số nguyên: hệ số của xⁿ.', '1 ≤ k ≤ 5; 0 ≤ n ≤ 200.',
  [lines('4 10', '0 -1 E', '0 -1 O', '0 4 A', '2 -1 A'), lines('2 5', '0 -1 A', '0 -1 A')], t_gf(),
  '''
k, n = map(int, input().split())
g = [1] + [0] * n                          # g(x) = 1 (đa thức, cắt ở bậc n)
for _ in range(k):
    lo, hi, par = input().split()
    lo, hi = int(lo), int(hi)
    f = [0] * (n + 1)                      # hàm sinh của loại này
    for x in range(lo, n + 1):
        if hi >= 0 and x > hi:
            break
        if par == 'E' and x % 2 == 1:
            continue
        if par == 'O' and x % 2 == 0:
            continue
        f[x] = 1
    h = [0] * (n + 1)                      # h = g * f (nhân đa thức, cắt ở bậc n)
    for i in range(n + 1):
        if g[i]:
            for j in range(n + 1 - i):
                if f[j]:
                    h[i + j] += g[i] * f[j]
    g = h
print(g[n])
''', c_gf,
  'Hàm sinh của một loại là đa thức Σ x^v với v thỏa điều kiện. Tích hai hàm sinh = nhân đa thức (tích chập). Chỉ cần giữ các hệ số đến bậc n.',
  'Hệ số của xⁿ trong Π fᵢ(x) đúng bằng số nghiệm (x₁,…,x_k) thỏa các điều kiện và có tổng n. Cài đặt: mảng hệ số độ dài n+1, nhân đa thức O(n²) cho mỗi loại. Phía chấm đối chiếu với đệ quy có nhớ theo (loại, số quả còn lại).',
  '''
k, n = map(int, input().split())
g = [1] + [0] * n                  # g = hàm sinh hiện tại (hệ số bậc 0..n)
for _ in range(k):
    lo, hi, par = input().split()
    lo, hi = int(lo), int(hi)
    # TODO: dựng đa thức f của loại này, rồi g = g * f (cắt ở bậc n)
print(g[n])
''')

# ---------------------------------------------------------------- 17. Đổi tiền
def c_coin(inp, out):
    L = inp.split('\n'); k, M = map(int, L[0].split()); d = list(map(int, L[1].split()))
    if sorted(d) == [1, 5, 10, 50] and M >= 5000:
        c = 0
        for a in range(M // 50 + 1):
            for b in range((M - 50 * a) // 10 + 1):
                for e in range((M - 50 * a - 10 * b) // 5 + 1): c += 1
        return out == f'{c}\n'
    import sys
    sys.setrecursionlimit(20000)
    from functools import lru_cache
    @lru_cache(None)
    def f(i, rem):
        if rem == 0: return 1
        if i == k: return 0
        return sum(f(i + 1, rem - j * d[i]) for j in range(rem // d[i] + 1))
    return out == f'{f(0, M)}\n'
P('doi-tien', 'm09', 2, 'Đổi tiền: số cách đổi',
  'Có k loại tờ tiền với mệnh giá d₁, …, d_k (nghìn đồng), mỗi loại có không hạn chế tờ. Có bao nhiêu cách đổi M nghìn đồng (hai cách khác nhau nếu số tờ của ít nhất một loại khác nhau; thứ tự tờ không quan trọng)? Đề slide (Exercise 1): mệnh giá 1, 5, 10, 50; tìm hàm sinh và tính số cách đổi 100.',
  'Dòng 1: <code>k M</code>. Dòng 2: k mệnh giá.', 'Một số nguyên.', '1 ≤ k ≤ 6; 1 ≤ M ≤ 10000; 1 ≤ dᵢ ≤ M, các dᵢ khác nhau.',
  [lines('4 100', '1 5 10 50'), lines('3 4', '1 2 3')], [lines(f'{len(d)} {M}', nums(d)) for d, M in [([1, 5, 10, 50], 5000), ([1, 5, 10, 50], 10000), ([2, 3], 7), ([1], 50), ([5, 10], 4), ([1, 2, 5], 100), ([3, 7, 11], 200), ([1, 2, 5, 10, 20, 50], 300), ([25, 10, 5, 1], 1000)]],
  '''
k, M = map(int, input().split())
d = list(map(int, input().split()))
ways = [1] + [0] * M
for coin in d:                         # từng mệnh giá một: tránh đếm trùng hoán vị
    for s in range(coin, M + 1):
        ways[s] += ways[s - coin]
print(ways[M])
''', c_coin,
  'Hàm sinh của mệnh giá d là 1/(1 − x^d) = 1 + x^d + x^{2d} + …; đáp số là hệ số của x^M trong tích. Cài đặt: với mỗi mệnh giá, <code>ways[s] += ways[s − d]</code> (duyệt s tăng).',
  'Cộng dồn theo từng mệnh giá (vòng ngoài là mệnh giá, vòng trong là số tiền) đếm tổ hợp, không đếm hoán vị. Đổi hai vòng lặp sẽ đếm cả thứ tự các tờ, ra số lớn hơn. Đây là dạng nhân đa thức với 1/(1 − x^d), tương đương cộng dồn trong mảng.',
  '''
k, M = map(int, input().split())
d = list(map(int, input().split()))
# TODO: ways[s] = số cách đổi s; vòng ngoài là mệnh giá, vòng trong là số tiền s
''')

# ---------------------------------------------------------------- 18. Sinh xâu nhị phân kế tiếp
def inc_str(s):
    t = list(s); i = len(t) - 1
    while i >= 0 and t[i] == '1': t[i] = '0'; i -= 1
    if i >= 0: t[i] = '1'
    return ''.join(t)
def c_binnext(inp, out):
    x, k = inp.split('\n')[0], int(inp.split('\n')[1]); res = []; cur = x
    for _ in range(k): cur = inc_str(cur); res.append(cur)
    return out == ''.join(r + '\n' for r in res)
def t_binnext():
    ts = [lines('0110110', 3), lines('1100010', 3), lines('0', 1), lines('0111', 8)]
    for _ in range(6):
        n = R.randint(3, 20); v = R.randint(0, 2 ** n - 12); ts.append(lines(format(v, f'0{n}b'), R.randint(1, 10)))
    return ts
P('sinh-xau-nhi-phan', 'm10', 1, 'Sinh xâu nhị phân kế tiếp',
  'Cho xâu nhị phân X độ dài n. Áp dụng phương pháp sinh theo thứ tự từ điển, in ra k xâu nhị phân liền kề tiếp theo của X (mỗi xâu một dòng, không có dấu phẩy). Dữ liệu đảm bảo đủ k xâu đứng sau X. (Dạng đề: X = 0110110, tìm 3 xâu tiếp theo.)',
  'Dòng 1: xâu X. Dòng 2: k.', 'k dòng, mỗi dòng một xâu có độ dài n.', '1 ≤ n ≤ 20; 1 ≤ k ≤ 10; X + k < 2ⁿ.',
  [lines('0110110', 3), lines('0', 1)], t_binnext(),
  '''
x = input().strip()
k = int(input())
n = len(x)
for _ in range(k):
    t = list(x)
    i = n - 1
    while i >= 0 and t[i] == '1':   # các bit 1 ở cuối đổi thành 0
        t[i] = '0'
        i -= 1
    t[i] = '1'                      # bit 0 cuối cùng đổi thành 1
    x = ''.join(t)
    print(x)
''', c_binnext,
  'Thuật toán sinh: tìm bit 0 phải nhất, đổi thành 1, và đổi mọi bit 1 bên phải nó thành 0. Chính là phép cộng 1 vào số nhị phân.',
  'Xâu kế tiếp theo thứ tự từ điển = xâu cộng thêm 1 (mod 2ⁿ). Có thể làm bằng int(x, 2) rồi định dạng lại, nhưng đề thi thường yêu cầu <i>trình bày thuật toán sinh</i>, nên hãy tập cả hai cách.',
  '''
x = input().strip()
k = int(input())
n = len(x)
# TODO: lặp k lần: tìm bit 0 phải nhất, đổi thành 1, các bit sau đổi thành 0; in xâu mới
''')

# ---------------------------------------------------------------- 19. Hoán vị kế tiếp
def c_permnext(inp, out):
    L = inp.split('\n'); n = int(L[0]); p = tuple(map(int, L[1].split())); m = int(L[2])
    allp = sorted(itertools.permutations(range(1, n + 1))); i = allp.index(p)
    return out == ''.join(nums(q) + '\n' for q in allp[i + 1:i + 1 + m])
def t_permnext():
    ts = [lines(9, '5 6 8 3 9 7 4 2 1', 4), lines(3, '1 2 3', 2), lines(2, '1 2', 1), lines(5, '2 5 4 3 1', 3)]
    for _ in range(7):
        n = R.randint(3, 9)
        while True:
            p = R.sample(range(1, n + 1), n)
            if p != sorted(p, reverse=True): break
        ts.append(lines(n, nums(p), 3 if n < 4 else R.randint(1, 5)))
    return ts
# bảo đảm đủ hoán vị phía sau (loại test không hợp lệ)
def _fix_perm_tests(ts):
    ok = []
    for t in ts:
        L = t.split('\n'); n = int(L[0]); p = tuple(map(int, L[1].split())); m = int(L[2])
        # số hoán vị đứng sau p
        rank = 0; pool = sorted(p)
        for i, v in enumerate(p):
            idx = pool.index(v); rank += idx * factorial(n - 1 - i); pool.remove(v)
        if factorial(n) - 1 - rank >= m: ok.append(t)
    return ok
P('hoan-vi-ke-tiep', 'm10', 2, 'Sinh hoán vị kế tiếp',
  'Cho hoán vị p của {1, 2, …, n}. Áp dụng phương pháp sinh hoán vị theo thứ tự từ điển, in ra m hoán vị liền kề tiếp theo của p, mỗi hoán vị một dòng, các phần tử cách nhau dấu cách. Dữ liệu đảm bảo có đủ m hoán vị đứng sau p. (Dạng đề thật: n = 9, p = 568397421, tìm 4 hoán vị kế tiếp.)',
  'Dòng 1: n. Dòng 2: n số của p. Dòng 3: m.', 'm dòng, mỗi dòng một hoán vị.', '1 ≤ n ≤ 9; 1 ≤ m ≤ 5.',
  [lines(3, '1 2 3', 2), lines(9, '5 6 8 3 9 7 4 2 1', 4)], _fix_perm_tests(t_permnext()),
  '''
n = int(input())
p = list(map(int, input().split()))
m = int(input())
for _ in range(m):
    i = n - 2
    while i >= 0 and p[i] > p[i + 1]:     # i lớn nhất mà p[i] < p[i+1]
        i -= 1
    j = n - 1
    while p[j] < p[i]:                    # phần tử nhỏ nhất > p[i] ở bên phải (do phần đuôi giảm dần)
        j -= 1
    p[i], p[j] = p[j], p[i]
    p[i + 1:] = reversed(p[i + 1:])       # đảo đoạn đuôi cho nhỏ nhất
    print(' '.join(map(str, p)))
''', c_permnext,
  'Ba bước: (1) tìm i lớn nhất sao cho p[i] < p[i+1]; (2) tìm j lớn nhất sao cho p[j] > p[i], đổi chỗ p[i], p[j]; (3) đảo ngược đoạn p[i+1..n].',
  'Phần đuôi sau vị trí i đang giảm dần (đã lớn nhất), nên phải tăng p[i] bằng số nhỏ nhất lớn hơn nó ở bên phải rồi sắp đuôi tăng dần (đảo ngược). Độ phức tạp mỗi bước O(n). Phía chấm đối chiếu với itertools.permutations đã sắp xếp.',
  '''
n = int(input())
p = list(map(int, input().split()))
m = int(input())
for _ in range(m):
    # TODO: sinh hoán vị kế tiếp (tìm i, tìm j, đổi chỗ, đảo đuôi) rồi in
    pass
''')

# ---------------------------------------------------------------- 20. Tổ hợp kế tiếp
def c_combnext(inp, out):
    L = inp.split('\n'); n, k = map(int, L[0].split()); c = tuple(map(int, L[1].split())); m = int(L[2])
    allc = list(itertools.combinations(range(1, n + 1), k)); i = allc.index(c)
    return out == ''.join(nums(q) + '\n' for q in allc[i + 1:i + 1 + m])
def t_combnext():
    ts = [lines('9 7', '1 2 3 5 6 7 8', 4), lines('5 3', '1 2 3', 3), lines('6 2', '1 5', 1), lines('9 7', '1 2 4 5 6 7 8', 3)]
    for _ in range(7):
        n = R.randint(4, 10); k = R.randint(1, n - 1); allc = list(itertools.combinations(range(1, n + 1), k)); i = R.randrange(len(allc) - 1)
        ts.append(lines(f'{n} {k}', nums(allc[i]), min(R.randint(1, 5), len(allc) - 1 - i)))
    return ts
P('to-hop-ke-tiep', 'm10', 2, 'Sinh tổ hợp kế tiếp',
  'Cho tập {1, 2, …, n} và một tổ hợp chập k c₁ < c₂ < … < c_k (theo thứ tự từ điển các tổ hợp). In ra m tổ hợp liền kề tiếp theo, mỗi tổ hợp một dòng. Dữ liệu đảm bảo có đủ m tổ hợp sau c. (Dạng đề: n = 9, k = 7, c = 1 2 3 5 6 7 8, tìm 4 tổ hợp tiếp theo.)',
  'Dòng 1: <code>n k</code>. Dòng 2: k số của c. Dòng 3: m.', 'm dòng, mỗi dòng một tổ hợp (k số cách nhau dấu cách).', '1 ≤ k < n ≤ 10; 1 ≤ m ≤ 5.',
  [lines('5 3', '1 2 3', 3), lines('9 7', '1 2 3 5 6 7 8', 4)], t_combnext(),
  '''
n, k = map(int, input().split())
c = list(map(int, input().split()))
m = int(input())
for _ in range(m):
    i = k - 1
    while i >= 0 and c[i] == n - k + i + 1:   # tìm i lớn nhất mà c[i] chưa đạt giá trị tối đa n-k+i+1
        i -= 1
    c[i] += 1
    for j in range(i + 1, k):
        c[j] = c[j - 1] + 1
    print(' '.join(map(str, c)))
''', c_combnext,
  'Tìm i lớn nhất sao cho cᵢ < n − k + i (chỉ số tính từ 1). Tăng cᵢ thêm 1, rồi đặt c_j = c_{j−1} + 1 với mọi j > i.',
  'Phần tử cuối của tổ hợp lớn nhất là n − k + i ở vị trí i. Vị trí i phải nhất chưa đạt giá trị đó là chỗ có thể tăng; các phần tử sau reset về nhỏ nhất có thể (liên tiếp). Mỗi bước O(k). Phía chấm đối chiếu với itertools.combinations.',
  '''
n, k = map(int, input().split())
c = list(map(int, input().split()))
m = int(input())
for _ in range(m):
    # TODO: sinh tổ hợp kế tiếp rồi in
    pass
''')

# ---------------------------------------------------------------- 21. Xâu không có hai số 0 liên tiếp
def c_no00(inp, out):
    n = int(inp)
    res = [''.join(t) for t in itertools.product('01', repeat=n) if '00' not in ''.join(t)]
    return out == f'{len(res)}\n' + ''.join(r + '\n' for r in res)
P('xau-khong-00', 'm11', 2, 'Quay lui: xâu nhị phân không có hai số 0 liên tiếp',
  'Liệt kê tất cả các xâu nhị phân độ dài n <b>không chứa hai số 0 liên tiếp</b> bằng quay lui (bài 1, bài tập chương 3 giáo trình). In số xâu, rồi các xâu theo thứ tự từ điển, mỗi xâu một dòng.',
  'Một số nguyên n.', 'Dòng 1: số xâu. Tiếp theo mỗi dòng một xâu.', '1 ≤ n ≤ 14.',
  [lines(3), lines(1)], [lines(x) for x in (2, 4, 5, 6, 8, 10, 12, 14)],
  '''
n = int(input())
res = []
s = []
def Try(i):
    if i == n:
        res.append(''.join(s))
        return
    for b in '01':
        if b == '0' and s and s[-1] == '0':     # cắt nhánh: không cho hai số 0 liên tiếp
            continue
        s.append(b)
        Try(i + 1)
        s.pop()
Try(0)
print(len(res))
for r in res:
    print(r)
''', c_no00,
  'Quay lui sinh từng bit; trước khi đặt bit 0, kiểm tra bit đứng ngay trước không phải 0. Thử 0 trước 1 để ra đúng thứ tự từ điển.',
  'Số xâu độ dài n không có 00 là số Fibonacci F(n+2) (n = 1: 2; n = 2: 3; n = 3: 5; …). Cắt nhánh sớm nên cây quay lui chỉ chứa các tiền tố hợp lệ. So sánh với việc sinh cả 2ⁿ xâu rồi lọc để thấy lợi ích của cắt nhánh.',
  '''
n = int(input())
res = []
s = []
def Try(i):
    # TODO: i == n thì ghi nhận; ngược lại thử bit '0' (nếu hợp lệ) rồi '1'
    pass
Try(0)
print(len(res))
for r in res:
    print(r)
''')

# ---------------------------------------------------------------- 22. Quay lui: hoán vị
def c_permbt(inp, out):
    n = int(inp)
    return out == ''.join(nums(p) + '\n' for p in itertools.permutations(range(1, n + 1)))
P('hoan-vi-quay-lui', 'm11', 1, 'Quay lui: liệt kê hoán vị',
  'Viết chương trình dùng thuật toán quay lui liệt kê tất cả các hoán vị của 1, 2, …, n theo thứ tự từ điển, mỗi hoán vị một dòng. (Đề 01 năm 2023–24, câu 4a: “viết chương trình C/C++ dùng quay lui liệt kê tất cả các hoán vị của 1, 2, …, n”.)',
  'Một số nguyên n.', 'n! dòng, mỗi dòng một hoán vị (các số cách nhau dấu cách).', '1 ≤ n ≤ 7.',
  [lines(1), lines(3)], [lines(x) for x in (1, 2, 3, 4, 5, 6, 7)],
  '''
n = int(input())
used = [False] * (n + 1)
p = []
def Try(i):
    if i == n:
        print(' '.join(map(str, p)))
        return
    for v in range(1, n + 1):
        if not used[v]:
            used[v] = True
            p.append(v)
            Try(i + 1)
            p.pop()
            used[v] = False
Try(0)
''', c_permbt,
  'Mảng <code>used[v]</code> đánh dấu số đã dùng. Thử v từ 1 đến n tăng dần cho ra thứ tự từ điển; nhớ trả used[v] về False khi quay lui.',
  'Cây tìm kiếm có n tầng, tầng i có n·(n−1)·…·(n−i+1) nút; tổng n! lá. Ba thao tác “gán – gọi đệ quy – hoàn tác” là khung cơ bản của mọi bài quay lui. Bài thi có thể yêu cầu viết bằng quay lui (không dùng itertools); trong luyện tập, hãy tự cài đặt rồi mới đối chiếu với itertools.permutations.',
  '''
n = int(input())
used = [False] * (n + 1)
p = []
def Try(i):
    # TODO: i == n thì in p; ngược lại thử mọi v chưa dùng (gán, gọi Try(i+1), hoàn tác)
    pass
Try(0)
''')

# ---------------------------------------------------------------- 23. n quân hậu
def c_queens(inp, out):
    n = int(inp); cnt = 0; first = None
    for p in itertools.permutations(range(1, n + 1)):
        if all(abs(p[i] - p[j]) != j - i for i in range(n) for j in range(i + 1, n)):
            cnt += 1
            if first is None: first = p
    return out == f'{cnt}\n{nums(first) if first else "KHONG CO"}\n'
P('n-quan-hau', 'm11', 3, 'Bài toán n quân hậu',
  'Đặt n quân hậu lên bàn cờ n × n sao cho không quân nào ăn được quân nào (không cùng hàng, cột, đường chéo). Quân ở hàng i đặt ở cột xᵢ. In số cách đặt, rồi nghiệm đầu tiên theo thứ tự từ điển của (x₁, …, xₙ); nếu không có nghiệm in <code>KHONG CO</code>.',
  'Một số nguyên n.', 'Dòng 1: số nghiệm. Dòng 2: nghiệm nhỏ nhất theo từ điển (n số) hoặc <code>KHONG CO</code>.', '1 ≤ n ≤ 9.',
  [lines(4), lines(6)], [lines(x) for x in (1, 2, 3, 5, 7, 8, 9)],
  '''
n = int(input())
col = [False] * (n + 1)
d1 = [False] * (2 * n + 1)      # đường chéo xuôi: chỉ số i - j + n
d2 = [False] * (2 * n + 1)      # đường chéo ngược: chỉ số i + j
x = [0] * (n + 1)
cnt = 0
first = None
def Try(i):
    global cnt, first
    for j in range(1, n + 1):
        if not col[j] and not d1[i - j + n] and not d2[i + j]:
            x[i] = j
            col[j] = d1[i - j + n] = d2[i + j] = True
            if i == n:
                cnt += 1
                if first is None:
                    first = x[1:]
            else:
                Try(i + 1)
            col[j] = d1[i - j + n] = d2[i + j] = False
Try(1)
print(cnt)
print(' '.join(map(str, first)) if first else 'KHONG CO')
''', c_queens,
  'Mỗi hàng đúng một quân; chỉ cần chọn cột. Ba mảng logic kiểm tra cột, đường chéo i−j và i+j (giống ví dụ 4 của giáo trình). Số nghiệm: n = 4: 2; 6: 4; 8: 92.',
  'Mỗi ô (i, j) thuộc đường chéo xuôi i−j và đường chéo ngược i+j; hai quân cùng đường chéo khi các giá trị này trùng. Kiểm tra O(1) nhờ mảng đánh dấu. Quay lui cắt các nhánh sai ngay từ hàng đầu nên nhanh hơn rất nhiều so với duyệt n! hoán vị. Chú ý hoàn tác (đặt lại False) sau khi gọi đệ quy.',
  '''
n = int(input())
col = [False] * (n + 1)
d1 = [False] * (2 * n + 1)
d2 = [False] * (2 * n + 1)
x = [0] * (n + 1)
cnt = 0
first = None
def Try(i):
    global cnt, first
    # TODO: thử cột j = 1..n; hợp lệ nếu col, d1[i-j+n], d2[i+j] đều trống
    pass
Try(1)
print(cnt)
print(' '.join(map(str, first)) if first else 'KHONG CO')
''')

# ---------------------------------------------------------------- 24. Cái túi
def c_knap(inp, out):
    L = inp.split('\n'); n, b = map(int, L[0].split()); c = list(map(int, L[1].split())); a = list(map(int, L[2].split()))
    got = out.split('\n')
    if len(got) < 2: return False
    F = int(got[0]); x = list(map(int, got[1].split()))
    if len(x) != n or any(v not in (0, 1) for v in x): return False
    if sum(a[i] * x[i] for i in range(n)) > b or sum(c[i] * x[i] for i in range(n)) != F: return False
    if n <= 12:
        best = max((sum(c[i] * t[i] for i in range(n)), t) for t in itertools.product((0, 1), repeat=n) if sum(a[i] * t[i] for i in range(n)) <= b)
        return F == best[0] and tuple(x) == best[1]
    dp = [0] * (b + 1)
    for i in range(n):
        for w in range(b, a[i] - 1, -1): dp[w] = max(dp[w], dp[w - a[i]] + c[i])
    return F == dp[b]
def t_knap():
    ts = [lines('4 8', '10 5 3 6', '5 3 2 4'), lines('3 6', '7 4 2', '4 3 2'), lines('4 9', '5 1 8 1', '4 2 7 1'), lines('3 1', '5 5 5', '2 3 4'), lines('3 10', '4 4 4', '3 3 3')]
    for _ in range(6):
        n = R.randint(4, 12); a = [R.randint(1, 15) for _ in range(n)]; ts.append(lines(f'{n} {max(1, sum(a) // 2)}', nums([R.randint(1, 20) for _ in range(n)]), nums(a)))
    ts.append(lines('30 800', nums([R.randint(1, 100) for _ in range(30)]), nums([R.randint(5, 90) for _ in range(30)])))
    ts.append(lines('25 2000', nums([R.randint(1, 100) for _ in range(25)]), nums([R.randint(20, 200) for _ in range(25)])))
    return ts
P('cai-tui', 'm12', 3, 'Bài toán cái túi 0/1: giá trị và phương án tối ưu',
  'Có n đồ vật, vật j có giá trị cⱼ và trọng lượng aⱼ. Chọn xⱼ ∈ {0, 1} sao cho Σ aⱼxⱼ ≤ b và Σ cⱼxⱼ lớn nhất. In giá trị tối ưu F, rồi vector phương án. Nếu có nhiều phương án tối ưu, in phương án <b>lớn nhất theo thứ tự từ điển</b> (so sánh x₁ trước; 1 lớn hơn 0).<br>Dạng đề: 10x₁ + 5x₂ + 3x₃ + 6x₄ → max, 5x₁ + 3x₂ + 2x₃ + 4x₄ ≤ 8; hay 7x₁ + 4x₂ + 2x₃, 4x₁ + 3x₂ + 2x₃ ≤ 6. Đề thi tự luận yêu cầu trình bày nhánh cận; ở đây chỉ chấm kết quả.',
  'Dòng 1: <code>n b</code>. Dòng 2: c₁ … cₙ. Dòng 3: a₁ … aₙ.', 'Dòng 1: F. Dòng 2: x₁ … xₙ.', '1 ≤ n ≤ 30; 1 ≤ b ≤ 2000; 1 ≤ cⱼ ≤ 100; 1 ≤ aⱼ ≤ 200.',
  [lines('4 8', '10 5 3 6', '5 3 2 4'), lines('3 6', '7 4 2', '4 3 2')], t_knap(),
  '''
n, b = map(int, input().split())
c = list(map(int, input().split()))
a = list(map(int, input().split()))
best = [[0] * (b + 1) for _ in range(n + 1)]     # best[i][w]: tối ưu khi chỉ xét vật i..n-1, sức chứa w
for i in range(n - 1, -1, -1):
    for w in range(b + 1):
        best[i][w] = best[i + 1][w]
        if a[i] <= w:
            best[i][w] = max(best[i][w], c[i] + best[i + 1][w - a[i]])
w = b
x = []
for i in range(n):                                # dựng lại: ưu tiên lấy vật i (để x lớn nhất theo từ điển)
    if a[i] <= w and c[i] + best[i + 1][w - a[i]] == best[i][w]:
        x.append(1)
        w -= a[i]
    else:
        x.append(0)
print(best[0][b])
print(*x)
''', c_knap,
  'Với n lớn, vét cạn 2ⁿ quá chậm; dùng quy hoạch động theo sức chứa, hoặc nhánh cận (sắp theo cⱼ/aⱼ giảm dần, cận trên g = δ + (b − w)·c_{k+1}/a_{k+1}). Với n ≤ 12 có thể vét cạn.',
  'DP theo hậu tố: best[i][w] = max(best[i+1][w], cᵢ + best[i+1][w − aᵢ]). Dựng lại từ i = 0: nếu lấy vật i vẫn đạt tối ưu thì lấy (cho vector lớn nhất theo từ điển). Nhánh cận cho cùng giá trị tối ưu nhưng thường chỉ duyệt rất ít nút; hãy so sánh hai cách ở Module 12. Phía chấm vét cạn khi n ≤ 12.',
  '''
n, b = map(int, input().split())
c = list(map(int, input().split()))
a = list(map(int, input().split()))
# TODO: tìm giá trị tối ưu F và vector x (xj ∈ {0,1}); in F, rồi x
''')

# ---------------------------------------------------------------- 25. Người du lịch
def c_tsp(inp, out):
    L = inp.split('\n'); n = int(L[0]); C = [list(map(int, L[1 + i].split())) for i in range(n)]
    # Held–Karp lấy chi phí tối ưu
    INF = 10 ** 9; dp = [[INF] * n for _ in range(1 << n)]; dp[1][0] = 0
    for mask in range(1 << n):
        if not mask & 1: continue
        for j in range(n):
            if dp[mask][j] >= INF: continue
            for k in range(n):
                if not mask >> k & 1:
                    v = dp[mask][j] + C[j][k]
                    if v < dp[mask | 1 << k][k]: dp[mask | 1 << k][k] = v
    best = min(dp[(1 << n) - 1][j] + C[j][0] for j in range(1, n)) if n > 1 else 0
    got = out.split('\n')
    if int(got[0]) != best: return False
    t = list(map(int, got[1].split()))
    if t[0] != 1 or t[-1] != 1 or sorted(t[:-1]) != list(range(1, n + 1)): return False
    if sum(C[t[i] - 1][t[i + 1] - 1] for i in range(n)) != best: return False
    # nhỏ nhất theo từ điển: không có hành trình tối ưu nào nhỏ hơn
    sm = min(p for p in ((0,) + q for q in itertools.permutations(range(1, n))) if sum(C[p[i]][p[(i + 1) % n]] for i in range(n)) == best)
    return t == [v + 1 for v in sm] + [1]
def t_tsp():
    ts = [lines(4, '0 10 15 20', '10 0 35 25', '15 35 0 30', '20 25 30 0'), lines(2, '0 5', '7 0'), lines(3, '0 1 2', '2 0 1', '1 2 0')]
    for n in (5, 5, 6, 6, 7, 7, 8, 8):
        ts.append(lines(n, *[nums([0 if i == j else R.randint(1, 30) for j in range(n)]) for i in range(n)]))
    return ts
P('nguoi-du-lich', 'm13', 2, 'Người du lịch: duyệt toàn bộ (n nhỏ)',
  'Một người xuất phát từ thành phố 1, đi qua mỗi thành phố khác đúng một lần rồi quay về thành phố 1. Cho ma trận chi phí C (không nhất thiết đối xứng; chi phí đi từ i đến j là C[i][j], đường chéo bằng 0). In chi phí nhỏ nhất, rồi hành trình tối ưu (bắt đầu và kết thúc ở 1). Nếu nhiều hành trình cùng tối ưu, in hành trình nhỏ nhất theo thứ tự từ điển.',
  'Dòng 1: n. Tiếp theo n dòng, mỗi dòng n số của ma trận C.', 'Dòng 1: chi phí nhỏ nhất. Dòng 2: hành trình, ví dụ <code>1 3 2 4 1</code>.', '2 ≤ n ≤ 8; 0 ≤ C[i][j] ≤ 100.',
  [lines(4, '0 10 15 20', '10 0 35 25', '15 35 0 30', '20 25 30 0'), lines(2, '0 5', '7 0')], t_tsp(),
  '''
from itertools import permutations
n = int(input())
C = [list(map(int, input().split())) for _ in range(n)]
best = None
tour = None
for p in permutations(range(1, n)):          # cố định thành phố 1 ở đầu: (n-1)! hành trình
    t = (0,) + p
    s = sum(C[t[i]][t[(i + 1) % n]] for i in range(n))
    if best is None or s < best:             # dấu < chặt: giữ hành trình từ điển nhỏ nhất
        best, tour = s, t
print(best)
print(' '.join(str(v + 1) for v in tour) + ' 1')
''', c_tsp,
  'Cố định thành phố 1 làm điểm xuất phát; còn lại (n−1)! hoán vị. permutations sinh theo thứ tự từ điển nên chỉ cập nhật khi chi phí nhỏ hơn thật sự (dấu <).',
  'Vét cạn mất O((n−1)!·n): n = 8 cho 5040 hành trình, còn n = 15 là hơn 87 tỉ, nên đề thi dùng nhánh cận (Module 13) để cắt tỉa. Phía chấm kiểm tra chi phí bằng quy hoạch động bitmask Held–Karp O(2ⁿ·n²) và kiểm tra hành trình từ điển nhỏ nhất bằng vét cạn.',
  '''
from itertools import permutations
n = int(input())
C = [list(map(int, input().split())) for _ in range(n)]
# TODO: duyệt mọi hoán vị của 1..n-1 (thành phố 0 cố định ở đầu), tính chi phí vòng, giữ nhỏ nhất
''')
