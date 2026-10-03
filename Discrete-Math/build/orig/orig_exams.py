# Đề thi thật TRR1 (PTIT): 6 đề cuối kỳ HK1 2023-2024 (PDF) + 4 đề ảnh chụp 2017-2018 / 2019-2020. Phiên âm từ ảnh trang đã quét lại.
import math, itertools, sys, re
sys.path.insert(0,'..'); sys.path.insert(0,'.')
import orig_nh as ON
import orig_lib as OL
import orig_nh2 as X2
from recstore import RECS, add
import logic_tools as LT
from logic_tools import V,N,A,O,I,E,X
from qcore import near_ints
import random
p,q,r=V('p'),V('q'),V('r')
S24='Đề thi cuối kỳ INT1358 HK1 2023-2024'
S19='Đề thi cuối kỳ TRR1 HK1 2019-2020 (ảnh chụp)'
S17='Đề thi cuối kỳ TRR1 HK1 2017-2018 (ảnh chụp)'
def deleg(src,ref,text,chap,display=None):
    old=ON.SRC; ON.SRC=src; n0=len(RECS)
    try: ok=ON.handle_part(ref,'',text,chap)
    finally: ON.SRC=old
    if not ok: print('CHƯA XỬ LÝ:',src,ref,text[:60])
    for e in RECS[n0:]:
        if display and e['q']==ON.clean(text): e['q']=display
        e['src']=e['src'].replace(' – '+ref,' – '+ref)
    return ok
BB_SOL='Bài toán cái túi: có n đồ vật, vật j có trọng lượng aⱼ và giá trị cⱼ; chọn tập vật (xⱼ ∈ {0,1}) có tổng trọng lượng ≤ b để tổng giá trị lớn nhất.\nThuật toán nhánh cận: sắp các vật theo cⱼ/aⱼ giảm dần; dùng quay lui gán x₁, x₂, … (thử giá trị lớn trước); với phương án bộ phận (u₁..u_k) gọi δ_k là giá trị đã chọn, b_k trọng lượng còn lại thì cận trên g = δ_k + c_{k+1}·b_k/a_{k+1}. Nếu g ≤ FOPT (kỷ lục hiện có) thì cắt nhánh; nếu k = n thì cập nhật kỷ lục.\n\nMã C++:\n'+X2.CPP['knap_bb']
def A_(src,ref,key,text,mod,lv=3,tp='Thuật toán'):
    if key=='bb':
        add(mod=mod,src=f'{src} – {ref}',q=text,ans=None,wrong=[],sol=BB_SOL,level=lv,topic=tp); return
    add(mod=mod,src=f'{src} – {ref}',q=text,ans=None,wrong=[],sol=X2.alg_solution(key),level=lv,topic=tp)
def team(src,ref,text,n,w,ratio,lo,hi):
    terms=[];tot=0
    for j in range(0,w+1):
        i=ratio*j
        if i<=n and lo<=i+j<=hi: c=math.comb(n,i)*math.comb(w,j); tot+=c; terms.append(f'  {j} nữ + {i} nam: C({w},{j})·C({n},{i}) = {c}')
    add(mod='m04',src=f'{src} – {ref}',q=text,ans=str(tot),wrong=[str(x) for x in (tot+math.comb(n,ratio)*w,math.comb(n+w,lo),tot-1)],sol=f'Gọi số nữ là j thì số nam là {"" if ratio==1 else "2·"}j; tổng thành viên = {ratio+1}·j (nam {ratio}j, nữ j) phải nằm trong [{lo}, {hi}].\nCác trường hợp hợp lệ:\n'+'\n'.join(terms)+f'\nCộng lại (quy tắc cộng): {tot}.',level=3,topic='Chỉnh hợp, tổ hợp')
def logic_taut(src,ref,f,nb):
    add(mod='m01',src=f'{src} – {ref}',q=(f'Dùng bảng chân lý để chứng minh {LT.show(f)} là hằng đúng.' if nb else f'Không dùng bảng chân lý, chứng minh {LT.show(f)} là hằng đúng.'),ans=None,wrong=[],sol=(X2.TTtxt(f)+'\nCột cuối toàn Đ ⇒ hằng đúng. ∎') if nb else X2.DER[nb_key[LT.show(f)]]+' ∎',level=1 if nb else 2,topic='Chứng minh logic')
    if nb:
        add(mod='m01',src=f'{src} – {ref} (chuyển thành trắc nghiệm)',q=f'Công thức {LT.show(f)} thuộc loại nào?',ans='Hằng đúng (tautology)',wrong=['Mâu thuẫn (hằng sai)','Thỏa được nhưng không hằng đúng','Không thể kết luận nếu chưa biết giá trị các biến'],sol='Lập bảng chân trị:\n'+X2.TTtxt(f),level=1,topic='Phân loại công thức')
nb_key={LT.show(I(A(p,q),p)):'F1',LT.show(I(N(I(p,q)),p)):'F5'}
def logic_eq(src,ref,f,g,nb,ders=None):
    assert LT.equiv(f,g)
    add(mod='m01',src=f'{src} – {ref}',q=(f'Dùng bảng chân lý chứng minh {LT.show(f)} ≡ {LT.show(g)}.' if nb else f'Sử dụng các phép biến đổi tương đương và các mệnh đề tương đương cơ bản, chứng minh: {LT.show(f)} ≡ {LT.show(g)}.'),ans=None,wrong=[],sol=(X2.TTeq(f,g)+'\nHai cột cuối giống nhau trên mọi dòng ⇒ tương đương. ∎') if nb else ders,level=1 if nb else 2,topic='Chứng minh logic')
def pigeon(src,ref,text,ans,wrong,sol,tp='Dirichlet tổng quát',lv=2):
    add(mod='m06',src=f'{src} – {ref}',q=text,ans=str(ans),wrong=wrong,sol=sol,level=lv,topic=tp)
HS='Coi mỗi khách là một đỉnh, mỗi cái bắt tay là một cạnh. Tổng số lần bắt tay đếm theo từng người = tổng bậc = 2·(số cái bắt tay) là số CHẴN. Ở đây tổng = 20·10 + 15·5 = 275 là số LẺ ⇒ mâu thuẫn ⇒ người quan sát đã đếm nhầm. ∎'
CIR='Phản chứng: giả sử không có hai bạn kề nhau cùng khối. Khi đó dọc vòng tròn các khối xen kẽ A, B, A, B, … nên số người phải CHẴN. Nhưng 45 là số lẻ ⇒ mâu thuẫn ⇒ luôn có hai bạn kề nhau cùng khối. ∎'
CIR30='Phản chứng: giả sử mọi sinh viên đều có số thứ tự KHÔNG lớn hơn số của bạn đứng bên trái. Đi vòng quanh một vòng thì dãy số không tăng và quay về chính nó nên mọi số bằng nhau. Nhưng 30 số thứ tự đôi một khác nhau ⇒ mâu thuẫn. Vậy tồn tại bạn có số thứ tự lớn hơn số của bạn bên trái. ∎'
DER1='VT = ¬p ⇒ (q ⇒ r) ≡ ¬(¬p) ∨ (¬q ∨ r)   (P ⇒ Q ≡ ¬P ∨ Q, hai lần)\n≡ p ∨ ¬q ∨ r   (phủ định kép, kết hợp)\nVP = q ⇒ (p ∨ r) ≡ ¬q ∨ (p ∨ r) ≡ p ∨ ¬q ∨ r   (giao hoán, kết hợp)\nHai vế cùng bằng p ∨ ¬q ∨ r ⇒ tương đương. ∎'
def knap_items(src,ref,v,w,b,mode):
    best,bx,feas=X2.knap.brute(v,w,b); res=X2.knap.bb(v,w,b); assert res['fopt']==best
    def lin(cs): return ' + '.join((str(c) if c!=1 else '')+f'x{OL.sub(i+1)}' for i,c in enumerate(cs))
    stem=f'{lin(v)} → max; {lin(w)} ≤ {b}; xⱼ ∈ {{0,1}}.'
    if mode=='bf':
        rows=[]
        for x in itertools.product((0,1),repeat=len(v)):
            W=sum(a*c for a,c in zip(w,x)); V_=sum(a*c for a,c in zip(v,x)); rows.append(f'{X2.T(x)}: trọng lượng {W} '+(f'> {b} (loại)' if W>b else f'≤ {b}, giá trị {V_}'))
        sol='\n'.join(rows)+f'\nXOPT = {X2.T(bx)}, FOPT = {best}.'; q0='Áp dụng thuật toán duyệt toàn bộ giải bài toán cái túi dưới đây, chỉ rõ kết quả theo mỗi bước: '+stem; tp='Duyệt toàn bộ'
    else:
        sol=X2.G12.trace_text(v,w,b,res); q0='Áp dụng thuật toán nhánh cận giải bài toán cái túi dưới đây, chỉ rõ kết quả theo mỗi bước: '+stem; tp='Nhánh cận cái túi'
    add(mod='m12',src=f'{src} – {ref}',q=q0,ans=None,wrong=[],sol=sol,level=3,topic=tp)
    wl=sorted([x for x in itertools.product((0,1),repeat=len(v)) if x!=bx],key=lambda x:-sum(a*c for a,c in zip(v,x)))[:3]
    add(mod='m12',src=f'{src} – {ref} (chuyển thành trắc nghiệm)',q='Cái túi: '+stem+' Phương án tối ưu là:',ans=X2.T(bx),wrong=[X2.T(x) for x in wl],sol=sol+f'\nPhương án tối ưu {X2.T(bx)}, giá trị {best}.',level=2,topic='Phương án tối ưu')
    add(mod='m12',src=f'{src} – {ref} (chuyển thành trắc nghiệm)',q='Cái túi: '+stem+' Giá trị tối ưu f* bằng:',ans=best,wrong=[best+d for d in (-2,-1,1,2) if best+d>=0][:3]+[sum(v)],sol=f'Duyệt {2**len(v)} phương án, {feas} khả thi; giá trị lớn nhất {best} tại {X2.T(bx)}.',level=2,topic='Giá trị tối ưu')
def recs():
    n0=len(RECS)
    # ---------------- 2023-2024 ----------------
    s=S24
    # Đề 01
    logic_taut(s,'đề 01, câu 1a',I(A(p,I(p,q)),q),True)
    add(mod='m06',src=f'{s} – đề 01, câu 1b',q='Một lớp học có 45 học sinh đăng ký dự thi đại học vào khối A hoặc khối B. Xếp ngẫu nhiên 45 học sinh này thành một vòng tròn. Chứng minh rằng luôn tồn tại hai bạn học sinh đứng cạnh nhau và thi cùng khối.',ans=None,wrong=[],sol=CIR,level=3,topic='Chứng minh tồn tại')
    deleg(s,'đề 01, câu 2a','Lớp học có 50 bạn nam và 20 bạn nữ. Hãy cho biết có bao nhiêu cách chọn đội văn nghệ của lớp sao cho số bạn nam đúng bằng 2 lần số bạn nữ, biết rằng đội văn nghệ cần ít nhất 6 thành viên và nhiều nhất 12 thành viên.',2)
    deleg(s,'đề 01, câu 2b','Phương trình x1 + x2 + x3 + x4 + x5 + x6 = 35 có bao nhiêu nghiệm nguyên không âm thỏa mãn: 3 ≥ x2 ≥ 1; 7 ≥ x3 ≥ 4.',2)
    deleg(s,'đề 01, câu 3a','Hãy tìm nghiệm của công thức truy hồi với điều kiện đầu dưới đây: an = 2an-1 + 5an-2 - 6an-3 với n≥3 và a0 = 9, a1 = 8, a2 = 50.',2,display='Hãy tìm nghiệm của công thức truy hồi aₙ = 2aₙ₋₁ + 5aₙ₋₂ − 6aₙ₋₃ với n ≥ 3 và a₀ = 9, a₁ = 8, a₂ = 50. (Ảnh in dấu của hạng tử aₙ₋₂ khó đọc; hiểu là +5, vì chỉ khi đó phương trình đặc trưng có nghiệm nguyên −2, 1, 3 và điều kiện đầu cho hệ số nguyên.)')
    deleg(s,'đề 01, câu 3b','Tìm hệ thức truy hồi và cho điều kiện đầu để tính số các xâu nhị phân độ dài n có ít nhất một dãy k số 1 liên tiếp?',2)
    A_(s,'đề 01, câu 4a','bt_perm','Viết chương trình trên C/C++, sử dụng thuật toán quay lui liệt kê tất cả các hoán vị của 1, 2, …, n, với n nhập từ bàn phím.','m11')
    deleg(s,'đề 01, câu 4b','Cho tập A = {1, 2, 3, 4, 5, 6, 7, 8, 9}. Sử dụng phương pháp sinh hoán vị theo thứ tự từ điển, tìm 4 hoán vị liền kề tiếp theo của hoán vị 568397421.',3)
    A_(s,'đề 01, câu 5a','bb','Trình bày thuật toán nhánh cận giải bài toán cái túi.','m12',3,'Nhánh cận cái túi')
    knap_items(s,'đề 01, câu 5b',[3,5,7,4],[2,4,3,2],9,'bb')
    # Đề 02
    logic_eq(s,'đề 02, câu 1a',N(X(p,q)),E(p,q),True)
    add(mod='m06',src=f'{s} – đề 02, câu 1b',q='Một bữa tiệc có 35 vị khách tham dự. Mỗi vị khách sẽ bắt tay một số vị khách khác trong suốt bữa tiệc. Một người đứng ngoài quan sát và thấy rằng, trong số 35 vị khách thì có 20 người bắt tay với đúng 10 người khác, còn 15 người bắt tay với đúng 5 người khác. Chứng minh rằng người này đã đếm nhầm trong khi đứng quan sát bữa tiệc.',ans=None,wrong=[],sol=HS,level=3,topic='Chứng minh tồn tại')
    deleg(s,'đề 02, câu 2a','Phương trình x1 + x2 + x3 + x4 + x5 = 45 có bao nhiêu nghiệm nguyên không âm thỏa mãn: 4 ≥ x2 ≥ 2; 8 ≥ x3 ≥ 3; x4 ≥ 1?',2)
    deleg(s,'đề 02, câu 2b','Lớp học có 60 bạn nam và 25 bạn nữ. Hãy cho biết có bao nhiêu cách chọn đội văn nghệ của lớp sao cho số bạn nam đúng bằng 2 lần số bạn nữ, biết rằng đội văn nghệ cần ít nhất 3 thành viên và nhiều nhất 9 thành viên.',2)
    deleg(s,'đề 02, câu 3a','Tìm hệ thức truy hồi để tính số các xâu nhị phân độ dài n, bắt đầu bằng số 1 và có chứa 2 số 0 liên tiếp.',2)
    deleg(s,'đề 02, câu 3b','Hãy tìm nghiệm của công thức truy hồi với điều kiện đầu dưới đây: an = -3an-1 + 4an-2 + 12an-3 với n≥3 và a0 = 2, a1 = -4, a2 = 28.',2)
    A_(s,'đề 02, câu 4a','sinh_comb','Trình bày thuật toán sinh tổ hợp chập k của 1, 2, …, n theo thứ tự từ điển.','m10')
    deleg(s,'đề 02, câu 4b','Cho tập A = {1, 2, 3, 4, 5, 6, 7, 8, 9}. Sử dụng phương pháp sinh tổ hợp chập k của một tập hợp theo thứ tự từ điển, hãy tạo 5 tổ hợp chập 5 liền kề tiếp theo của tổ hợp (2,3,6,8,9).',3)
    A_(s,'đề 02, câu 5a','bb','Trình bày thuật toán nhánh cận giải bài toán cái túi.','m12',3,'Nhánh cận cái túi')
    knap_items(s,'đề 02, câu 5b',[6,5,3,1],[4,4,2,1],9,'bb')
    # Đề 03
    logic_taut(s,'đề 03, câu 1a',I(A(N(p),O(p,q)),q),True)
    F=math.factorial
    add(mod='m05',src=f'{s} – đề 03, câu 1b',q='Giả sử có 18 cuốn sách gồm 5 cuốn sách thuộc chủ đề toán học, 6 cuốn sách thuộc chủ đề hóa học, và 7 cuốn sách thuộc chủ đề vật lý (các cuốn sách cùng chủ đề có nội dung khác nhau). Hỏi có bao nhiêu cách xếp 18 cuốn sách trên thành một hàng ngang lên giá sách sao cho các cuốn sách cùng chủ đề nằm cạnh nhau?',ans=str(F(3)*F(5)*F(6)*F(7)),wrong=[str(x) for x in (F(5)*F(6)*F(7),F(18),F(3)*(F(5)+F(6)+F(7)),F(18)//F(3))],sol=f'Xem mỗi chủ đề là một khối: 3! cách sắp thứ tự ba khối, nhân 5!·6!·7! cách xếp trong khối: 3!·5!·6!·7! = {F(3)*F(5)*F(6)*F(7)}.',level=3,topic='Hoán vị')
    deleg(s,'đề 03, câu 2a','Có bao nhiêu biển số xe bắt đầu bằng 2 hoặc 3 chữ cái in hoa và kết thúc là 3 hoặc 4 chữ số, biết rằng có 26 chữ cái trong bảng chữ cái tiếng anh? (VD : RS 0912 là 1 biển số).',2)
    deleg(s,'đề 03, câu 2b','Phương trình x1 + x2 + x3 + x4 + x5 + x6 = 55 có bao nhiêu nghiệm nguyên không âm thỏa mãn: 6 ≥ x2 ≥ 4; 4 ≥ x3 ≥ 1.',2)
    deleg(s,'đề 03, câu 3a','Hãy tìm nghiệm của công thức truy hồi với điều kiện đầu dưới đây: an = -an-1 + 10an-2 - 8an-3 với n≥3 và a0 = 0, a1 = -20, a2 = 30.',2)
    deleg(s,'đề 03, câu 3b','Tìm hệ thức truy hồi để tính số các xâu nhị phân độ dài n, bắt đầu bằng số 0 và có chứa 2 số 0 liên tiếp? Tính số xâu nhị phân thỏa mãn điều kiện với n = 7.',2)
    A_(s,'đề 03, câu 4a','bt_comb','Viết chương trình trên C/C++, sử dụng phương pháp quay lui liệt kê tất cả các tổ hợp chập k của 1, 2, …, n, với n nhập từ bàn phím.','m11')
    deleg(s,'đề 03, câu 4b','Cho tập A = {1, 2, 3, 4, 5, 6, 7, 8, 9}. Sử dụng phương pháp sinh các tổ hợp chập k của một tập hợp theo thứ tự từ điển, hãy tạo ra 5 tổ hợp chập 5 liền kề tiếp theo của tổ hợp (1,4,5,7,9).',3)
    A_(s,'đề 03, câu 5a','bb','Trình bày thuật toán nhánh cận giải bài toán tối ưu.','m12',3,'Nhánh cận cái túi')
    knap_items(s,'đề 03, câu 5b',[5,5,3,8],[3,4,2,5],12,'bb')
    # Đề 04
    logic_eq(s,'đề 04, câu 1a',O(p,A(q,r)),A(O(p,q),O(p,r)),True)
    pigeon(s,'đề 04, câu 1b','Một hộp đựng bi chứa các viên bi có kích thước thuộc một trong ba loại to, vừa, nhỏ và màu sắc thuộc một trong ba màu xanh, đỏ, vàng. Giả sử rằng số lượng mỗi loại bi là không hạn chế. Hỏi phải lấy ra ít nhất bao nhiêu viên bi trong hộp để chắc chắn rằng có ít nhất 4 viên bi giống nhau cả kích thước lẫn màu sắc?',28,[27,36,24,30],'Có 3·3 = 9 kiểu bi (quy tắc nhân). Cần 9·(4−1) + 1 = 28 viên.')
    deleg(s,'đề 04, câu 2a','Phương trình x1 + x2 + x3 + x4 + x5 = 66 có bao nhiêu nghiệm nguyên không âm thỏa mãn: 11 ≥ x2 ≥ 5; 12 ≥ x3 ≥ 4; x1 ≥ 3?',2)
    deleg(s,'đề 04, câu 2b','Có bao nhiêu số nguyên trong đoạn từ 1 đến 5000 thỏa mãn điều kiện chia hết cho ít nhất một trong ba số 6, 9, và 15?',2)
    deleg(s,'đề 04, câu 3a','Hãy tìm nghiệm của công thức truy hồi với điều kiện đầu dưới đây: an = -an-1 + 17an-2 - 15an-3 với n≥3 và a0 = 8, a1 = -38, a2 = 160.',2)
    deleg(s,'đề 04, câu 3b','Có bao nhiêu số tự nhiên có 7 chữ số tạo thành một số thuận nghịch và có tất cả các chữ số đều khác 0;',2)
    A_(s,'đề 04, câu 4a','sinh_comb','Viết chương trình trên C/C++, sử dụng thuật toán sinh tổ hợp liệt kê tất cả các tập con k phần tử của dãy n phần tử.','m10')
    deleg(s,'đề 04, câu 4b','Cho tập A = {1, 2, 3, 4, 5, 6, 7, 8, 9}. Sử dụng phương pháp sinh tổ hợp chập k của một tập hợp theo thứ tự từ điển, liệt kê 5 tổ hợp chập 5 liền kề tiếp theo của tổ hợp (2,3,5,7,9).',3)
    add(mod='m12',src=f'{s} – đề 04, câu 5a',q='Trình bày bài toán cái túi.',ans=None,wrong=[],sol='Bài toán cái túi: có n đồ vật, vật j có trọng lượng aⱼ và giá trị cⱼ; chọn tập vật (xⱼ ∈ {0,1}) sao cho tổng trọng lượng ≤ b và tổng giá trị lớn nhất: f(x) = Σ cⱼxⱼ → max; Σ aⱼxⱼ ≤ b. Tập phương án D = {x ∈ {0,1}ⁿ : Σ aⱼxⱼ ≤ b}, có tối đa 2ⁿ phương án.',level=1,topic='Mô hình cái túi')
    knap_items(s,'đề 04, câu 5b',[6,8,5,2],[3,6,3,2],11,'bb')
    # Đề 05
    logic_taut(s,'đề 05, câu 1a',I(A(p,q),p),False)
    pigeon(s,'đề 05, câu 1b','Cần ít nhất bao nhiêu sinh viên để chắc chắn rằng có ít nhất 10 sinh viên có cùng tháng sinh?',109,[108,120,110,97],'12 tháng sinh. Cần 12·(10−1) + 1 = 109 sinh viên.')
    deleg(s,'đề 05, câu 2a','Lớp học có 55 bạn nam và 35 bạn nữ. Hãy cho biết có bao nhiêu cách chọn đội văn nghệ của lớp sao cho số bạn nam bằng số bạn nữ, biết rằng đội văn nghệ cần ít nhất 6 thành viên và nhiều nhất 10 thành viên.',2)
    deleg(s,'đề 05, câu 2b','Phương trình x1 + x2 + x3 + x4 + x5 + x6 = 50 có bao nhiêu nghiệm nguyên không âm thỏa mãn: 8 ≥ x1 ≥ 1; 9 ≥ x3 ≥ 2?',2)
    deleg(s,'đề 05, câu 3a','Tìm hệ thức truy hồi và cho điều kiện đầu để tính số các xâu nhị phân độ dài n và không có k số 0 liên tiếp?',2)
    deleg(s,'đề 05, câu 3b','Hãy tìm nghiệm của công thức truy hồi với điều kiện đầu dưới đây: an = an-1 + 14an-2 - 24an-3 với n≥3 và a0 = 3, a1 = -14, a2 = 38.',2)
    A_(s,'đề 05, câu 4a','bt_bin','Viết chương trình trên C/C++, sử dụng thuật toán quay lui liệt kê tất cả các xâu nhị phân có độ dài n, với n nhập từ bàn phím.','m11',2)
    deleg(s,'đề 05, câu 4b','Cho xâu nhị phân X = { 1, 0, 1, 0, 1, 1, 1, 1, 1}. Sử dụng phương pháp sinh xâu nhị phân theo thứ tự từ điển, tìm 5 xâu nhị phân liền kề tiếp theo của X?',3)
    add(mod='m12',src=f'{s} – đề 05, câu 5a',q='Trình bày thuật toán duyệt toàn bộ giải bài toán cái túi.',ans=None,wrong=[],sol='Duyệt toàn bộ: XOPT = ∅, FOPT = −∞ (max). Với mỗi vectơ x ∈ {0,1}ⁿ: nếu Σ aⱼxⱼ ≤ b thì tính S = Σ cⱼxⱼ; nếu S > FOPT thì FOPT = S, XOPT = x. Trả về (XOPT, FOPT). Độ phức tạp O(n·2ⁿ).',level=1,topic='Duyệt toàn bộ')
    knap_items(s,'đề 05, câu 5b',[5,8,3,6],[3,7,1,3],13,'bf')
    # Đề 06
    logic_taut(s,'đề 06, câu 1a',I(N(I(p,q)),p),False)
    add(mod='m06',src=f'{s} – đề 06, câu 1b',q='Một lớp học có 30 sinh viên được gán số thứ tự từ 1 đến 30. Xếp ngẫu nhiên 30 sinh viên này thành một vòng tròn. Chứng minh rằng luôn tồn tại một bạn sinh viên có số thứ tự lớn hơn số thứ tự của bạn đứng bên trái mình.',ans=None,wrong=[],sol=CIR30,level=3,topic='Chứng minh tồn tại')
    deleg(s,'đề 06, câu 2a','Phương trình x1 + x2 + x3 + x4 + x5 = 40 có bao nhiêu nghiệm nguyên không âm thỏa mãn: x5 ≥ 5; 9 ≥ x2 ≥ 1; 7 ≥ x3 ≥ 2?',2)
    deleg(s,'đề 06, câu 2b','Một hệ thống máy tính coi một xâu các chữ số hệ thập phân là một từ mã hợp lệ nếu nó chứa một số lẻ chữ số 6. Ví dụ 1231437869 là hợp lệ, 12698704568 là không hợp lệ. Giả sử an là số các từ mã độ dài n. Hãy tìm hệ thức truy hồi và điều kiện đầu cho an.',2)
    deleg(s,'đề 06, câu 3a','Hãy tìm nghiệm của công thức truy hồi với điều kiện đầu dưới đây: an = -9an-1 - 26an-2 - 24an-3 với n≥3 và a0 = -5, a1 = 23, a2 = -95.',2)
    deleg(s,'đề 06, câu 3b','Tìm hệ thức truy hồi và cho điều kiện đầu để tính số các xâu nhị phân độ dài n có ít nhất một dãy k số 0 liên tiếp?',2)
    A_(s,'đề 06, câu 4a','sinh_perm','Trình bày thuật toán sinh hoán vị của một tập n phần tử theo thứ tự từ điển.','m10')
    deleg(s,'đề 06, câu 4b','Cho tập A = {1, 2, 3, 4, 5, 6, 7, 8, 9}. Sử dụng phương pháp sinh hoán vị theo thứ tự từ điển, liệt kê 5 hoán vị liền kề tiếp theo của hoán vị (1,3,9,5,8,7,6,4,2).',3)
    A_(s,'đề 06, câu 5a','bb','Trình bày thuật toán nhánh cận giải bài toán cái túi.','m12',3,'Nhánh cận cái túi')
    knap_items(s,'đề 06, câu 5b',[7,3,4,6],[5,1,5,3],13,'bb')
    # ---------------- 2019-2020 ----------------
    s=S19
    add(mod='m01',src=f'{s} – đề 1, câu 1a',q='Sử dụng các phép biến đổi tương đương và các mệnh đề tương đương cơ bản, chứng minh sự tương đương logic: ¬p ⇒ (q ⇒ r) ≡ q ⇒ (p ∨ r).',ans=None,wrong=[],sol=DER1,level=2,topic='Chứng minh logic')
    pigeon(s,'đề 1, câu 1b','Trong một kỳ thi trắc nghiệm, đề thi có 40 câu hỏi. Thí sinh được 0,25 điểm cho mỗi câu trả lời đúng và 0 điểm cho mỗi câu trả lời sai hoặc không trả lời. Hỏi cần ít nhất bao nhiêu thí sinh tham gia kỳ thi để chắc chắn rằng có ít nhất 12 thí sinh có điểm bài thi bằng nhau?',452,[451,41*12,40*11+1,492],'Số mức điểm = 40 + 1 = 41 (0…40 câu đúng). Cần 41·(12−1) + 1 = 452 thí sinh. (Ghi chú trên ảnh đề có người viết đáp số 452.)',tp='Dirichlet – thi trắc nghiệm')
    deleg(s,'đề 1, câu 2a','Tìm hệ thức truy hồi và điều kiện đầu để tính số các xâu nhị phân độ dài n chứa 3 số 1 liên tiếp? Tính số xâu thỏa mãn điều kiện với n = 5.',2,display='Tìm hệ thức truy hồi và điều kiện đầu để tính số lượng các xâu nhị phân độ dài n có chứa ba số 1 liên tiếp. Tính a₅.')
    deleg(s,'đề 1, câu 2b','Hãy tìm nghiệm của công thức truy hồi với điều kiện đầu dưới đây: an = -14an-1 - 49an-2 với n≥2 và a0 = 3, a1 = 35.',2)
    deleg(s,'đề 1, câu 3a','Phương trình x1 + x2 + x3 + x4 + x5 + x6 = 30 có bao nhiêu nghiệm nguyên không âm thỏa mãn: 8 ≥ x2 ≥ 3 và 6 ≥ x4 ≥ 2?',2)
    A_(s,'đề 1, câu 3b','bt_comb','Trình bày phương pháp liệt kê các tổ hợp chập k của tập {1, 2, …, n} sử dụng phương pháp quay lui.','m11')
    A_(s,'đề 1, câu 4','sinh_perm','Viết chương trình trong C/C++ liệt kê các hoán vị của tập {1, 2, …, n} sử dụng phương pháp sinh theo thứ tự từ điển.','m10')
    add(mod='m12',src=f'{s} – đề 1, câu 5a',q='Trình bày thuật toán duyệt toàn bộ giải bài toán tối ưu.',ans=None,wrong=[],sol='Bước 1: XOPT = ∅; FOPT = −∞ (max) hoặc +∞ (min). Bước 2: với mỗi X ∈ D: S = f(X); nếu FOPT < S (max) thì FOPT = S, XOPT = X. Bước 3: trả về (XOPT, FOPT). Nhược điểm: bùng nổ số phương án (2ⁿ, n!).',level=1,topic='Duyệt toàn bộ')
    knap_items(s,'đề 1, câu 5b',[5,2,7,1],[5,3,6,4],9,'bf')
    logic_taut(s,'đề 2, câu 1a',I(A(I(p,q),I(q,r)),I(p,r)),True)
    team(s,'đề 2, câu 1b','Lớp học có 50 bạn nam và 40 bạn nữ. Cần lập đội văn nghệ của lớp với số thành viên từ 4 đến 10 người sao cho số lượng nữ và nam như nhau. Tính số lượng các đội văn nghệ có thể lập được.',50,40,1,4,10)
    seq={n:sum(1 for t in itertools.product(range(10),repeat=n) if t.count(9)%2==0) for n in range(1,6)}
    assert all(seq[n]==8*seq[n-1]+10**(n-1) for n in range(2,6))
    add(mod='m07',src=f'{s} – đề 2, câu 2a',q='Tìm hệ thức truy hồi và điều kiện đầu để tính số lượng các xâu thập phân độ dài n có chứa một số chẵn các chữ số 9.',ans='aₙ = 8aₙ₋₁ + 10ⁿ⁻¹, a₁ = 9',wrong=['aₙ = 9aₙ₋₁ + 10ⁿ⁻¹, a₁ = 9','aₙ = 8aₙ₋₁ + 10ⁿ⁻¹, a₁ = 1','aₙ = 8aₙ₋₁ + 10ⁿ, a₁ = 9'],sol='Gọi aₙ là số xâu có số CHẴN chữ số 9 (kể cả 0), bₙ là số xâu có số LẺ; aₙ + bₙ = 10ⁿ. Thêm một ký tự cuối: là 9 (1 cách) đổi tính chẵn lẻ; khác 9 (9 cách) giữ nguyên: aₙ = 9aₙ₋₁ + bₙ₋₁ = 9aₙ₋₁ + (10ⁿ⁻¹ − aₙ₋₁) = 8aₙ₋₁ + 10ⁿ⁻¹, a₁ = 9. Kiểm tra: '+', '.join(f'a{OL.sub(n)} = {seq[n]}' for n in range(1,6))+' (đếm trực tiếp).',level=3,topic='Lập hệ thức truy hồi')
    deleg(s,'đề 2, câu 2b','Hãy tìm nghiệm của công thức truy hồi với điều kiện đầu dưới đây: an = 10an-1 - 25an-2 với n≥2 và a0 = 3, a1 = 9.',2)
    A_(s,'đề 2, câu 3a','sinh_perm','Viết một hàm trên C/C++ biểu diễn thuật toán liệt kê các hoán vị của n số nguyên thuộc tập A = {1, 2, …, n} sử dụng phương pháp sinh hoán vị theo thứ tự từ điển.','m10')
    deleg(s,'đề 2, câu 3b','Sử dụng phương pháp sinh hoán vị theo thứ tự từ điển, tìm 5 hoán vị tiếp theo của hoán vị (3, 1, 4, 5, 8, 6, 2, 9, 10, 7).',3)
    deleg(s,'đề 2, câu 4a','Phương trình x1 + x2 + x3 + x4 + x5 = 34 có bao nhiêu nghiệm nguyên không âm thỏa mãn: 10 ≥ x3 ≥ 2; 8 ≥ x5 ≥ 0.',2)
    pigeon(s,'đề 2, câu 4b','Cho S là tập hợp các cặp số (x, y), trong đó x, y là các số nguyên. Cần chọn ra ít nhất bao nhiêu phần tử của tập S để chắc chắn có hai bộ số (a, b) và (c, d) sao cho (a − c) và (b − d) đều là bội của 100.',10001,[10000,100,20001,9999],'Mỗi cặp thuộc một "hộp" theo (x mod 100, y mod 100): 100·100 = 10000 hộp. Cần 10000 + 1 = 10001 cặp.',tp='Dirichlet – đồng dư',lv=3)
    add(mod='m12',src=f'{s} – đề 2, câu 5a',q='Trình bày thuật toán duyệt toàn thể giải bài toán cái túi.',ans=None,wrong=[],sol='Duyệt toàn thể (toàn bộ) 2ⁿ vectơ x ∈ {0,1}ⁿ: loại vectơ có Σ aⱼxⱼ > b; trong các vectơ khả thi giữ vectơ có Σ cⱼxⱼ lớn nhất (FOPT, XOPT).',level=1,topic='Duyệt toàn bộ')
    knap_items(s,'đề 2, câu 5b',[6,2,1,7],[5,3,4,4],12,'bf')
    # ---------------- 2017-2018 ----------------
    s=S17
    add(mod='m01',src=f'{s} – đề 5, câu 1a',q='Sử dụng các phép biến đổi tương đương và các mệnh đề tương đương cơ bản, chứng minh sự tương đương logic: ¬p ⇒ (q ⇒ r) ≡ q ⇒ (p ∨ r).',ans=None,wrong=[],sol=DER1,level=2,topic='Chứng minh logic')
    pigeon(s,'đề 5, câu 1b','Giả sử S là tập hợp gồm các bộ có thứ tự (x, y) với x và y là các số nguyên. Hỏi phải lấy ra ít nhất bao nhiêu phần tử trong S để chắc chắn rằng có ít nhất 2 bộ (a, b) và (c, d) sao cho (a − c) và (b − d) đều chia hết cho 8?',65,[64,63,16,129],'Mỗi cặp thuộc "hộp" theo (x mod 8, y mod 8): 8·8 = 64 hộp. Cần 64 + 1 = 65 cặp.',tp='Dirichlet – đồng dư',lv=3)
    b5={n:sum(1 for t in itertools.product(range(10),repeat=n) if t.count(6)%2==0) for n in range(1,6)}
    add(mod='m07',src=f'{s} – đề 5, câu 2a',q='Một hệ thống máy tính coi một xâu các chữ số hệ thập phân là một từ mã hợp lệ nếu nó chứa một số chẵn (hoặc không chứa) chữ số 6. Ví dụ 5264507869 là hợp lệ, 9870516080 là không hợp lệ. Giả sử aₙ là số các từ mã hợp lệ độ dài n. Hãy tìm hệ thức truy hồi và điều kiện đầu cho aₙ, sau đó tính a₅.',ans=f'aₙ = 8aₙ₋₁ + 10ⁿ⁻¹, a₁ = 9; a₅ = {b5[5]}',wrong=[f'aₙ = 9aₙ₋₁ + 10ⁿ⁻¹, a₁ = 9; a₅ = {b5[5]+1000}',f'aₙ = 8aₙ₋₁ + 10ⁿ⁻¹, a₁ = 1; a₅ = 33616',f'aₙ = 8aₙ₋₁ + 10ⁿ, a₁ = 9; a₅ = {b5[5]*10}'],sol=f'Gọi aₙ là số xâu có số chẵn (kể cả 0) chữ số 6; bₙ: số lẻ; aₙ + bₙ = 10ⁿ. aₙ = 9aₙ₋₁ + bₙ₋₁ = 8aₙ₋₁ + 10ⁿ⁻¹, a₁ = 9. Tính: '+', '.join(f'a{OL.sub(n)} = {b5[n]}' for n in range(1,6))+' (a₅ = (10⁵ + 8⁵)/2).',level=3,topic='Lập hệ thức truy hồi')
    deleg(s,'đề 5, câu 2b','Hãy tìm nghiệm của công thức truy hồi với điều kiện đầu dưới đây: an = -6an-1 - 9an-2 với n≥2 và a0 = 3, a1 = -3.',2)
    add(mod='m04',src=f'{s} – đề 5, câu 3a',q='Giả sử N, a, b, c là các số nguyên thỏa mãn 1 < a < b < c < N. Có bao nhiêu số nguyên trong đoạn từ 1 đến N không chia hết cho bất kỳ số nào trong ba số a, b, c?',ans=None,wrong=[],sol='Đặt A_x = tập các số trong [1,N] chia hết cho x. Số cần tìm = N − |A_a ∪ A_b ∪ A_c|. Nguyên lý bù trừ:\nN − ⌊N/a⌋ − ⌊N/b⌋ − ⌊N/c⌋ + ⌊N/[a,b]⌋ + ⌊N/[a,c]⌋ + ⌊N/[b,c]⌋ − ⌊N/[a,b,c]⌋, trong đó [·] là bội chung nhỏ nhất.',level=3,topic='Nguyên lý bù trừ')
    A_(s,'đề 5, câu 3b','sinh_perm','Trình bày phương pháp liệt kê các hoán vị của tập {1, 2, 3, …, n} sử dụng phương pháp sinh hoán vị theo thứ tự từ điển.','m10')
    A_(s,'đề 5, câu 4','sinh_bin','Viết chương trình trong C/C++ liệt kê các xâu nhị phân độ dài n sử dụng phương pháp sinh theo thứ tự từ điển.','m10',2)
    knap_items(s,'đề 5, câu 5',[1,6,5,6],[2,5,4,3],9,'bf')
    logic_eq(s,'đề 6, câu 1a',I(N(p),I(q,r)),I(q,O(p,r)),True)
    pigeon(s,'đề 6, câu 1b','Giả sử S là tập hợp gồm các bộ có thứ tự (x, y) với x và y là các số nguyên. Hỏi phải lấy ra ít nhất bao nhiêu phần tử trong S để chắc chắn rằng có ít nhất 2 bộ (a, b) và (c, d) sao cho (a − c) và (b − d) đều chia hết cho 9?',82,[81,80,18,163],'Mỗi cặp thuộc "hộp" theo (x mod 9, y mod 9): 9·9 = 81 hộp. Cần 81 + 1 = 82 cặp.',tp='Dirichlet – đồng dư',lv=3)
    deleg(s,'đề 6, câu 2a','Một hệ thống máy tính coi một xâu các chữ số hệ thập phân là một từ mã hợp lệ nếu nó chứa một số lẻ chữ số 6. Ví dụ 524507869 là hợp lệ, 987651608 là không hợp lệ. Giả sử an là số các từ mã hợp lệ độ dài n. Hãy tìm hệ thức truy hồi và điều kiện đầu cho an, sau đó tính a5.',2)
    deleg(s,'đề 6, câu 2b','Hãy tìm nghiệm của công thức truy hồi với điều kiện đầu dưới đây: an = -14an-1 - 49an-2 với n≥2 và a0 = 3, a1 = 35.',2)
    deleg(s,'đề 6, câu 3a','Phương trình x1 + x2 + x3 + x4 + x5 = 50 có bao nhiêu nghiệm nguyên không âm thỏa mãn: 8 ≥ x2 ≥ 3 và 6 ≥ x4 ≥ 2?',2)
    A_(s,'đề 6, câu 3b','sinh_comb','Trình bày phương pháp liệt kê các tổ hợp chập k của tập {1, 2, …, n} sử dụng phương pháp sinh tổ hợp theo thứ tự từ điển.','m10')
    A_(s,'đề 6, câu 4','bt_bin','Viết chương trình trong C/C++ liệt kê các xâu nhị phân độ dài n sử dụng phương pháp quay lui.','m11',2)
    knap_items(s,'đề 6, câu 5',[5,2,7,1],[5,3,6,4],9,'bf')
    return RECS[n0:]
if __name__=='__main__':
    r=recs(); print(len(r))
    import collections; print(collections.Counter(x['mod'] for x in r))
