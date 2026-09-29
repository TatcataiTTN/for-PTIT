from qcore import *
import itertools, math
def T(t): return '('+', '.join(map(str,t))+')'
def bt_bin(n,out,calls):
    x=[0]*n
    def Try(i):
        calls[0]+=1
        for v in (0,1):
            x[i]=v
            if i==n-1: out.append(tuple(x))
            else: Try(i+1)
    Try(0)
def bt_perm(n,out,calls):
    x=[0]*n; used=[False]*(n+1)
    def Try(i):
        calls[0]+=1
        for v in range(1,n+1):
            if not used[v]:
                x[i]=v; used[v]=True
                if i==n-1: out.append(tuple(x))
                else: Try(i+1)
                used[v]=False
    Try(0)
def bt_comb(n,k,out,calls):
    x=[0]*k
    def Try(i):
        calls[0]+=1
        lo=1 if i==0 else x[i-1]+1
        for v in range(lo,n-k+i+2):
            x[i]=v
            if i==k-1: out.append(tuple(x))
            else: Try(i+1)
    Try(0)
def bt_no11(n,out,calls):
    x=[0]*n
    def Try(i):
        calls[0]+=1
        for v in (0,1):
            if v==1 and i>0 and x[i-1]==1: continue
            x[i]=v
            if i==n-1: out.append(tuple(x))
            else: Try(i+1)
    Try(0)
def bt_subsetsum(vals,S,out,calls):
    n=len(vals); x=[0]*n
    def Try(i,s):
        calls[0]+=1
        for v in (0,1):
            ns=s+v*vals[i]
            if ns>S: continue
            x[i]=v
            if i==n-1:
                if ns==S: out.append(tuple(x))
            else: Try(i+1,ns)
    Try(0,0)
def queens(n):
    cols=[];sols=[]
    def ok(r,c): return all(c!=cc and abs(c-cc)!=r-rr for rr,cc in enumerate(cols))
    def Try(r):
        if r==n: sols.append(tuple(c+1 for c in cols)); return
        for c in range(n):
            if ok(r,c): cols.append(c); Try(r+1); cols.pop()
    Try(0); return sols
def gen(seed=11):
    B=Bank('m11',seed); rng=B.rng
    # 1. số lời gọi và số kết quả
    for n in range(2,9):
        out=[];calls=[0]; bt_bin(n,out,calls)
        B.add(f'Thủ tục quay lui Try(i) (i = 1..{n}) gán x[i] ∈ {{0,1}} rồi gọi Try(i+1), in xâu khi i = {n}. Tổng số lần gọi Try (kể cả Try(1)) để liệt kê mọi xâu nhị phân độ dài {n} là:',calls[0],[2**n,2**(n+1),n*2**n,2**n+n],f'Try(i) được gọi 2^(i−1) lần với i = 1..{n}: tổng = 1+2+…+2^{n-1} = 2^{n} − 1 = {calls[0]}.',level=3,topic='Số lần gọi')
        B.add(f'Quay lui liệt kê tất cả xâu nhị phân độ dài {n} in ra bao nhiêu xâu?',2**n,[2**n-1,n**2,2*n,2**(n+1)],f'Mỗi vị trí 2 lựa chọn ⇒ 2^{n} = {2**n} xâu.',level=1,topic='Số kết quả')
    for n in range(3,9):
        out=[];calls=[0]; bt_perm(n,out,calls)
        B.add(f'Liệt kê mọi hoán vị của {{1..{n}}} bằng quay lui (mảng đánh dấu used). Thủ tục Try(i) được gọi tất cả bao nhiêu lần (kể cả Try(1))?',calls[0],[math.factorial(n),math.factorial(n)+n,calls[0]-1,calls[0]+math.factorial(n)],f'Try(i) được gọi P({n}, i−1) = {n}!/({n}−i+1)! lần: '+' + '.join(str(math.perm(n,i-1)) for i in range(1,n+1))+f' = {calls[0]}. (Số hoán vị in ra chỉ là {math.factorial(n)}.)',level=3,topic='Số lần gọi')
    for n,k in [(4,2),(5,2),(5,3),(6,2),(6,3),(6,4),(7,3),(7,4),(8,3)]:
        out=[];calls=[0]; bt_comb(n,k,out,calls)
        assert len(out)==math.comb(n,k)
        B.add(f'Quay lui liệt kê tổ hợp chập {k} của {{1..{n}}} theo thứ tự tăng dần. Tổ hợp thứ 3 được in ra là:',T(out[2]),[T(out[3]),T(out[1]),T(out[-1])] if len(out)>4 else [T(out[-1]),T(out[0]),T(out[1])],f'Thứ tự in: '+' → '.join(T(o) for o in out[:5])+' …',level=2,topic='Thứ tự in')
        B.add(f'Quay lui liệt kê các tổ hợp chập {k} của {{1..{n}}}: tổ hợp cuối cùng in ra là:',T(out[-1]),[T(out[0]),T(tuple(range(1,k+1))[::-1]),T(tuple(range(n-k,n))+(n,) if False else out[-2])],f'Tổ hợp lớn nhất theo thứ tự từ điển là {T(out[-1])} (k phần tử lớn nhất).',level=1,topic='Thứ tự in')
    # 2. có ràng buộc
    for n in range(4,13):
        out=[];calls=[0]; bt_no11(n,out,calls)
        a,b=2,3
        for _ in range(n-2): a,b=b,a+b
        B.add(f'Quay lui liệt kê các xâu nhị phân độ dài {n} KHÔNG có hai bit 1 liền nhau (bỏ qua giá trị 1 nếu x[i−1] = 1). Có bao nhiêu xâu được in ra?',len(out),near_ints(len(out),rng,6,lo=1)+[2**n],f'Số xâu = số Fibonacci F_{n+2} = {len(out)} (aₙ = aₙ₋₁ + aₙ₋₂, a₁=2, a₂=3). Điều kiện chấp nhận cắt bỏ nhánh sớm nên số lời gọi chỉ {calls[0]} thay vì {2**n-1}.',level=3,topic='Bài toán có ràng buộc')
    for n in range(4,10):
        cnt=len(queens(n)) if n<=8 else 0
        if cnt:
            B.add(f'Bài toán {n} quân hậu: số cách đặt {n} quân hậu lên bàn cờ {n}×{n} sao cho không quân nào ăn được nhau là:',cnt,[c for c in [2,10,4,40,92,cnt+2,cnt-1] if c!=cnt and c>0][:6],f'Quay lui từng hàng, kiểm tra cột và hai đường chéo: có {cnt} nghiệm (đã đếm bằng chương trình quay lui).',level=3,topic='N quân hậu')
    for _ in range(40):
        n=rng.randint(5,9); vals=sorted(rng.sample(range(1,15),n)); S=rng.randint(sum(vals)//4,sum(vals)//2)
        out=[];calls=[0]; bt_subsetsum(vals,S,out,calls)
        if not out: continue
        brute=sum(1 for m in itertools.product((0,1),repeat=n) if sum(v*x for v,x in zip(vals,m))==S)
        assert brute==len(out)
        B.add(f'Cho tập {{{", ".join(map(str,vals))}}}. Có bao nhiêu tập con có tổng đúng bằng {S}?',len(out),near_ints(len(out),rng,5,lo=0),f'Quay lui chọn/không chọn từng phần tử, cắt nhánh khi tổng vượt {S}: tìm được {len(out)} tập con (kiểm chứng bằng vét cạn 2^{n} = {2**n}).'+(' Một nghiệm: '+str([v for v,x in zip(vals,out[0]) if x])+'.'),level=3,topic='Tổng tập con')
    for n in range(4,9):
        cnt=sum(1 for p in itertools.permutations(range(1,n+1)) if all(p[i]!=i+1 for i in range(n)))
        B.add(f'Quay lui đếm hoán vị của {{1..{n}}} thỏa p[i] ≠ i với mọi i (điều kiện chấp nhận: v ≠ i). Số hoán vị tìm được là:',cnt,near_ints(cnt,rng,6,lo=0)+[math.factorial(n)],f'Đây là số hoán vị mất thứ tự Dₙ: D{n} = {cnt}. Cắt nhánh sớm khi v = i giúp giảm số lời gọi.',level=3,topic='Bài toán có ràng buộc')
    for n in range(4,9):
        cnt=sum(1 for p in itertools.permutations(range(1,n+1)) if all(abs(p[i]-p[i+1])!=1 for i in range(n-1)))
        B.add(f'Có bao nhiêu hoán vị của {{1..{n}}} sao cho hai phần tử liền kề không hơn kém nhau đúng 1 đơn vị?',cnt,near_ints(cnt,rng,6,lo=0)+[math.factorial(n)],f'Quay lui với điều kiện chấp nhận |x[i] − x[i−1]| ≠ 1: tìm được {cnt} hoán vị (đã đếm trực tiếp).',level=3,topic='Bài toán có ràng buộc')
    # 3. khái niệm
    con=[('Trong quay lui, bước "trả lại trạng thái" (bỏ đánh dấu used[v] = false, hoặc x[i] không còn được chọn) được thực hiện','sau khi lời gọi đệ quy Try(i+1) trở về',['trước khi gọi Try(i+1)','chỉ khi tìm thấy nghiệm','chỉ ở lời gọi Try(1)']),
         ('Điều kiện chấp nhận (kiểm tra ràng buộc trước khi gán x[i]) giúp','cắt bỏ sớm các nhánh chắc chắn không cho nghiệm',['tăng số nghiệm tìm được','đổi thứ tự liệt kê thành ngược từ điển','luôn giảm độ phức tạp xuống đa thức']),
         ('Với ràng buộc quan hệ giữa các phần tử (như N quân hậu), phương pháp phù hợp nhất để liệt kê nghiệm là','quay lui với cắt nhánh',['phương pháp sinh cấu hình kế tiếp','duyệt toàn bộ 2ⁿ rồi lọc','sắp xếp nổi bọt']),
         ('Cấu trúc dữ liệu ngầm định dùng để nhớ các lựa chọn của thuật toán quay lui đệ quy là','ngăn xếp gọi hàm (call stack)',['hàng đợi','bảng băm','cây nhị phân tìm kiếm']),
         ('Độ sâu đệ quy tối đa khi liệt kê hoán vị của n phần tử bằng quay lui là','n',['n!','2ⁿ','n²']),
         ('Điều kiện kết thúc (nhánh lá) của Try(i) khi liệt kê xâu độ dài n là','i = n (đã gán đủ n thành phần)',['x[i] = 0','i = 1','used[i] = true'])]
    for q,a,w in con: B.add(q,a,w,'Xem Module 11: khung quay lui gồm: (1) duyệt các ứng viên v; (2) kiểm tra chấp nhận; (3) gán, ghi nhớ; (4) nếu đủ thì ghi nhận nghiệm, ngược lại gọi Try(i+1); (5) hoàn trả trạng thái.',level=1,topic='Khái niệm')
    # 4. bổ sung: phần tử thứ m, ràng buộc khác, số lời gọi tổ hợp
    for _ in range(25):
        n=rng.randint(4,6); out=[];calls=[0]; bt_perm(n,out,calls); m=rng.randint(2,len(out)-1)
        B.add(f'Quay lui liệt kê hoán vị của {{1..{n}}} (thử v = 1, 2, …, {n} ở mỗi vị trí). Hoán vị được in ra thứ {m} là:',T(out[m-1]),[T(out[m]),T(out[m-2]),T(out[-m])] if out[-m] not in (out[m-1],) else [T(out[m]),T(out[m-2]),T(out[0])],f'Thứ tự in trùng thứ tự từ điển; hoán vị thứ {m} là {T(out[m-1])}. Bắt đầu: '+' → '.join(T(o) for o in out[:4])+' …',level=3,topic='Thứ tự in')
    for _ in range(20):
        n=rng.randint(4,8); out=[];calls=[0]; bt_bin(n,out,calls); m=rng.randint(3,2**n-1)
        B.add(f'Quay lui liệt kê xâu nhị phân độ dài {n} (thử 0 rồi 1). Xâu được in ra thứ {m} là:',''.join(map(str,out[m-1])),[''.join(map(str,out[m])),''.join(map(str,out[m-2])),''.join(map(str,out[-m]))] if out[-m]!=out[m-1] else [''.join(map(str,out[m])),''.join(map(str,out[m-2])),''.join(map(str,out[0]))],f'Xâu thứ m là biểu diễn nhị phân của m − 1 = {m-1} với {n} bit: {"".join(map(str,out[m-1]))}.',level=2,topic='Thứ tự in')
    for n,k in [(5,2),(6,2),(6,3),(7,3),(8,3),(8,4),(9,3),(7,2)]:
        out=[];calls=[0]; bt_comb(n,k,out,calls)
        B.add(f'Quay lui liệt kê tổ hợp chập {k} của {{1..{n}}} (cận trên của vị trí i là n − k + i). Số lần gọi Try (kể cả Try(1)) là:',calls[0],[len(out),calls[0]+1,calls[0]-1,math.comb(n,k)+n],f'Số lời gọi = tổng số nút của cây tìm kiếm = {calls[0]}; số tổ hợp (nút lá) = C({n},{k}) = {len(out)}. Nhờ cận trên n−k+i mọi nhánh đều dẫn tới ít nhất một nghiệm.',level=3,topic='Số lần gọi')
    for n in range(4,11):
        cnt=sum(1 for m in itertools.product((0,1),repeat=n) if all(not(m[i]==m[i+1]==m[i+2]) for i in range(n-2)))
        B.add(f'Quay lui đếm xâu nhị phân độ dài {n} không có ba bit giống nhau liên tiếp. Số xâu tìm được là:',cnt,near_ints(cnt,rng,6,lo=1)+[2**n],f'Điều kiện chấp nhận: không cho x[i] = x[i−1] = x[i−2]. Đếm được {cnt} (dãy 2, 4, 6, 10, 16, 26, …: aₙ = aₙ₋₁ + aₙ₋₂).',level=3,topic='Bài toán có ràng buộc')
    for n in range(5,11):
        for k in (2,3):
            cnt=sum(1 for m in itertools.product((0,1),repeat=n) if sum(m)==k)
            B.add(f'Quay lui liệt kê xâu nhị phân độ dài {n} có đúng {k} bit 1. Số xâu là:',cnt,[cnt+1,cnt-1,n*k,2**n],f'Chọn vị trí các bit 1: C({n},{k}) = {cnt}.',level=2,topic='Bài toán có ràng buộc')
    return B
def essays(B):
    q=queens(4)
    ex=[('Viết chương trình C/C++ liệt kê các xâu nhị phân độ dài n bằng phương pháp quay lui. (đề 2017-2020)','#include <bits/stdc++.h>\nusing namespace std;\nint n, x[32];\nvoid Try(int i){\n    for(int v = 0; v <= 1; v++){\n        x[i] = v;\n        if(i == n){ for(int j = 1; j <= n; j++) cout << x[j]; cout << "\\n"; }\n        else Try(i + 1);\n    }\n}\nint main(){ cin >> n; Try(1); }'),
        ('Viết chương trình C/C++ dùng quay lui liệt kê tất cả hoán vị của 1..n (n nhập từ bàn phím). (đề 2023-2024)','int n, x[20]; bool used[20];\nvoid Try(int i){\n    for(int v = 1; v <= n; v++) if(!used[v]){\n        x[i] = v; used[v] = true;\n        if(i == n){ for(int j = 1; j <= n; j++) cout << x[j] << " "; cout << "\\n"; }\n        else Try(i + 1);\n        used[v] = false;   // hoàn trả trạng thái\n    }\n}\n// gọi Try(1); số hoán vị = n!'),
        ('Viết hàm quay lui liệt kê tổ hợp chập k của 1..n. (đề 2023-2024, đề 2017-2018)','int n, k, x[20];\nvoid Try(int i){\n    for(int v = x[i-1] + 1; v <= n - k + i; v++){\n        x[i] = v;\n        if(i == k){ for(int j = 1; j <= k; j++) cout << x[j] << " "; cout << "\\n"; }\n        else Try(i + 1);\n    }\n}\n// x[0] = 0; gọi Try(1). Cận trên n − k + i bảo đảm còn đủ phần tử cho các vị trí sau.'),
        ('Liệt kê mọi lời giải bài toán 4 quân hậu bằng quay lui và cho biết số nghiệm.','Đặt quân hậu từng hàng; hàng r chọn cột c sao cho khác các cột đã dùng và không cùng đường chéo (|c − c\'| ≠ |r − r\'|). Có '+str(len(q))+' nghiệm (theo cột ở mỗi hàng): '+', '.join(T(x) for x in q)+'.'),
        ('Có bao nhiêu xâu nhị phân độ dài 5 không chứa hai bit 1 liên tiếp? Liệt kê bằng quay lui.','Điều kiện chấp nhận: nếu x[i−1] = 1 thì không được gán x[i] = 1. Có 13 xâu.'),
        ('Giải thích vì sao quay lui liệt kê hoán vị cần mảng used[] còn liệt kê xâu nhị phân thì không.','Ở xâu nhị phân mỗi vị trí độc lập, chọn 0 hoặc 1 tùy ý. Ở hoán vị các giá trị phải khác nhau nên cần ghi nhớ giá trị đã dùng (used[]), và phải hoàn trả used[v] = false sau khi quay lui để giá trị đó dùng lại cho nhánh khác.')]
    for q_,s in ex: B.essay(q_,s,level=3,topic='Quay lui')
if __name__=='__main__':
    B=gen(); essays(B); print(len(B.items),len(B.essays),audit(B.items))
