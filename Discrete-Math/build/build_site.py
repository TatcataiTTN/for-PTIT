import importlib, json, os, sys, random, collections
from hx import *
from qcore import fm
from sitelib import *
MODS=[('m01','01-logic-menh-de'),('m02','02-vi-tu-luong-tu'),('m03','03-tap-hop-do-phuc-tap'),('m04','04-nguyen-ly-dem'),('m05','05-to-hop-nghiem-nguyen'),('m06','06-dirichlet-ton-tai'),('m07','07-lap-he-thuc-truy-hoi'),('m08','08-giai-he-thuc-truy-hoi'),('m09','09-ham-sinh'),('m10','10-phuong-phap-sinh'),('m11','11-quay-lui'),('m12','12-cai-tui-nhanh-can'),('m13','13-nguoi-du-lich')]
def pick_quiz(bank,n=40,seed=1):
    """kho ~40 câu cho quiz nhanh: ưu tiên câu gốc, đủ chủ đề và mức 1–3"""
    rng=random.Random(seed)
    items=[i for i in bank['items'] if i.get('origin')=='goc']
    if len(items)<n: items+=[i for i in bank['items'] if i.get('origin')!='goc']
    by=collections.defaultdict(list)
    for it in items: by[it['topic']].append(it)
    for v in by.values(): rng.shuffle(v)
    topics=sorted(by,key=lambda t:-len(by[t])); out=[]
    while len(out)<n and any(by.values()):
        for t in topics:
            if by[t] and len(out)<n: out.append(by[t].pop())
    return out
DIAG={'m04':[('venn-3-tap','Sơ đồ Venn cho nguyên lý bù trừ ba tập')],'m06':[('dirichlet','Minh họa nguyên lý Dirichlet')],'m08':[('giai-truy-hoi','Quy trình giải hệ thức truy hồi')],'m11':[('cay-quay-lui','Cây quay lui xâu nhị phân n = 3')],'m12':[('cay-cai-tui','Cây nhánh cận bài toán cái túi (giáo trình 2016)')],'m13':[('cay-nguoi-du-lich','Cây nhánh cận bài toán người du lịch (giáo trình 2016)')]}
def diag_block(mid):
    if mid not in DIAG: return ''
    h='<h2 id="so-do">Sơ đồ minh họa</h2>'
    for n,cap in DIAG[mid]:
        h+=f'<div class="diag"><a href="../../../assets/diagrams/{n}.png" target="_blank" rel="noopener"><img src="../../../assets/diagrams/{n}.png" alt="{cap}" loading="lazy" style="max-height:none"></a><div style="font-size:.85rem;color:var(--muted)">{cap} · <a href="../../../assets/diagrams/{n}.drawio">mở file draw.io nguồn</a></div></div>'
    return h
def module_page(M,idx,bank):
    d=3
    slides=[]; total=len(M['parts'])
    for k,pt in enumerate(M['parts'],1):
        slides.append((divider(k,total,pt['title'],pt['bullets']),True))
        for s in pt['slides']: slides.append((s,False))
    body=f'<div class="crumbs"><a href="../../index.html">Trang chủ</a> › Module {idx+1}</div><h1>Module {idx+1}. {M["title"]}</h1><p class="lead">{M["subtitle"]}</p>'
    ng=sum(1 for i in bank['items'] if i.get('origin')=='goc'); neg=sum(1 for i in bank['essays'] if i.get('origin')=='goc')
    body+=f'<p><span class="tag">Môn: Toán rời rạc 1 (INT1358)</span><span class="tag">{M["source"]}</span><span class="tag exam">Đề thi: {M["exam"]}</span><span class="tag">Thời lượng gợi ý: {M["time"]}</span><span class="tag">{len(bank["items"])} câu trắc nghiệm ({ng} câu gốc) · {len(bank["essays"])} bài tự luận ({neg} gốc)</span></p>'
    body+=callout('good','🎯 Sau module này bạn sẽ','<ul>'+''.join(f'<li>{o}</li>' for o in M['objectives'])+'</ul>')
    body+='<h2 id="slide">Bài giảng dạng slide</h2><p class="lead">Dùng phím ← → hoặc các nút; bấm “Toàn màn hình” để trình chiếu. Mỗi slide có khung “Giải thích cho người mới bắt đầu”.</p>'+deck(slides)
    body+=diag_block(M['id'])+'<div id="chi-tiet">'+M['notes']+'</div>'
    q=pick_quiz(bank)
    body+='<h2 id="quiz">Tự kiểm tra nhanh (10 câu, đổi bộ được)</h2><p>Mỗi lần rút 10 câu từ kho của module. Bấm đáp án để chấm ngay; mọi câu đều có giải thích; có nút làm lại từng câu, đổi bộ câu hỏi, và kết quả được ghi vào <a href="../../so-loi/index.html">Sổ lỗi &amp; ôn tập</a>.</p>'+quiz_block('quiz-root',q)
    body+=f'<h2 id="luyen-tap">Luyện tập sâu</h2><div class="grid"><a class="mod-card" href="luyen-tap/index.html"><span class="num">TRẮC NGHIỆM</span><h3>Ngân hàng {len(bank["items"])} câu ({ng} câu gốc)</h3><p>Lọc theo nguồn, mức độ, chủ đề; giải thích chi tiết từng câu; lưu tiến độ; làm lại.</p></a><a class="mod-card" href="luyen-tap/index.html#tu-luan"><span class="num">TỰ LUẬN</span><h3>{len(bank["essays"])} bài có lời giải từng bước</h3><p>Dạng đề thi thật; tự làm rồi đối chiếu lời giải.</p></a></div>'
    prev=MODS[idx-1] if idx>0 else None; nxt=MODS[idx+1] if idx<len(MODS)-1 else None
    body+='<div class="modnav">'+(f'<a href="../{prev[1]}/index.html">← Module {idx}</a>' if prev else '<span></span>')+(f'<a href="../{nxt[1]}/index.html">Module {idx+2} →</a>' if nxt else '<a href="../../luyen-de/index.html">Luyện đề tổng hợp →</a>')+'</div>'
    return page(f'Module {idx+1}. {M["title"]}',body,d,M['subtitle'],scripts=('store.js','dm.js','sim.js','deck.js','quiz.js'))
def bank_page(M,idx,bank):
    body=f'<div class="crumbs"><a href="../../../index.html">Trang chủ</a> › <a href="../index.html">Module {idx+1}</a> › Luyện tập</div><h1>Luyện tập · {M["title"]}</h1><p class="lead">{len(bank["items"])} câu trắc nghiệm + {len(bank["essays"])} bài tự luận. Chọn đáp án là chấm ngay và hiện giải thích chi tiết (kể cả khi đúng). Tiến độ lưu trên trình duyệt này.</p>'
    data=json.dumps(dict(module=bank['module'],items=bank['items'],essays=bank['essays']),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    body+=f'<div id="bank"></div><script type="application/json" id="bank-data">{data}</script>'
    return page(f'Luyện tập · {M["title"]}',body,4,'Ngân hàng câu hỏi',scripts=('store.js','bank.js'))
def build_modules(only=None):
    infos=[]
    for idx,(mid,slug) in enumerate(MODS):
        if only and mid not in only: continue
        try: mod=importlib.import_module('content_'+mid)
        except ModuleNotFoundError: continue
        M=mod.module(); bank=json.load(open(os.path.join(ROOT,'data','qbank',mid+'.json'),encoding='utf-8'))
        write(f'vi/modules/{slug}/index.html',module_page(M,idx,bank))
        write(f'vi/modules/{slug}/luyen-tap/index.html',bank_page(M,idx,bank))
        infos.append((idx,slug,M,bank))
    return infos

TITLES={'m01':'Logic mệnh đề','m02':'Vị từ và lượng từ','m03':'Tập hợp và độ phức tạp thuật toán','m04':'Nguyên lý đếm cơ bản','m05':'Hoán vị, tổ hợp, nghiệm nguyên','m06':'Dirichlet và bài toán tồn tại','m07':'Lập hệ thức truy hồi','m08':'Giải hệ thức truy hồi','m09':'Hàm sinh','m10':'Phương pháp sinh','m11':'Quay lui','m12':'Duyệt toàn bộ và nhánh cận (cái túi)','m13':'Nhánh cận: bài toán người du lịch'}
CHAP={'m01':'Chương 1','m02':'Chương 1','m03':'Chương 1','m04':'Chương 2','m05':'Chương 2','m06':'Chương 2 · 5','m07':'Chương 2','m08':'Chương 2','m09':'Chương 2','m10':'Chương 3','m11':'Chương 3','m12':'Chương 4','m13':'Chương 4'}
def home_page(done):
    cards=''
    for idx,(mid,slug) in enumerate(MODS):
        bank_n=''
        p=os.path.join(ROOT,'data','qbank',mid+'.json')
        if os.path.exists(p):
            b=json.load(open(p,encoding='utf-8')); bank_n=f'{len(b["items"])} câu trắc nghiệm · {len(b["essays"])} tự luận'
        if mid in done:
            cards+=f'<a class="mod-card" href="modules/{slug}/index.html"><span class="num">MODULE {idx+1} · {CHAP[mid]}</span><h3>{TITLES[mid]}</h3><p>{bank_n}</p><p>Mở bài giảng →</p></a>'
        else:
            cards+=f'<div class="mod-card" style="opacity:.55;cursor:default"><span class="num">MODULE {idx+1} · {CHAP[mid]}</span><h3>{TITLES[mid]}</h3><p>Sắp có</p></div>'
    body='<h1>Toán rời rạc 1 (INT1358) · Tự học theo đề cương PTIT</h1><p class="lead">13 module bám sát giáo trình PTIT 2016, đề cương INT1358 và đề thi thật (2017–2024): slide có giải thích cho người mới, ví dụ đầy đủ lời giải, mô phỏng tương tác, ngân hàng câu hỏi có giải thích và bài tự luận từng bước.</p>'
    body+=callout('info','Cách học gợi ý','Mỗi module: xem slide → đọc phần “Nội dung chi tiết và ví dụ” → thử mô phỏng → làm quiz 10 câu → luyện ngân hàng câu hỏi → làm tự luận. Trước kỳ thi làm 10 đề trắc nghiệm ở mục Luyện đề.')
    body+=f'<h2 id="lo-trinh">Lộ trình 13 module</h2><div class="grid">{cards}</div>'
    body+='<h2>Bản đồ môn học</h2><div class="diag"><a href="../assets/diagrams/course-map.png" target="_blank" rel="noopener"><img src="../assets/diagrams/course-map.png" alt="Bản đồ 13 module" loading="lazy" style="max-height:none"></a></div>'
    body+=callout('warn','Về nguồn câu hỏi','Ngân hàng ưu tiên các câu GỐC trích từ tài liệu (ngân hàng câu hỏi 2019, đề thi 2017–2024, bộ đề ôn trắc nghiệm); mỗi câu ghi rõ nguồn. Chỉ khi nguồn gốc quá ít mới có câu “Bổ sung” do chương trình sinh và tự kiểm chứng.')
    return page('Trang chủ',body,1,'Tự học Toán rời rạc 1 PTIT')
def build_home(done):
    write('vi/index.html',home_page(done))
    write('index.html','<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=vi/index.html"><title>Toán rời rạc 1</title><a href="vi/index.html">Vào trang tự học Toán rời rạc 1 (PTIT)</a>')

def luyen_de_page():
    sets=json.load(open(os.path.join(ROOT,'data','exams','mcq_sets.json'),encoding='utf-8'))
    out=[]
    for st in sets:
        out.append([dict(q=fm(x['stem']),opts=[fm(o) for o in x['opts']],correct=x['ans'],explain=fm(x['expl']),src=f'Đề ôn trắc nghiệm TRR1 (Mẫu đề 2), đề {x["de"]}, câu {x["n"]}') for x in st])
    data=json.dumps(dict(sets=out),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    body='<div class="crumbs"><a href="../index.html">Trang chủ</a> › Luyện đề</div><h1>Luyện đề trắc nghiệm tổng hợp</h1><p class="lead">10 đề, mỗi đề 15 câu, 30 phút, đúng cấu trúc bộ đề ôn trắc nghiệm TRR1 của Khoa Trí tuệ nhân tạo (PTIT). Mọi câu là câu gốc của bộ đề; bản gốc không có đáp án nên đáp án ở đây do chúng tôi tự tính bằng chương trình và kiểm chứng độc lập. Bấm “Nộp bài” để xem điểm và giải thích từng câu; “Làm lại” để xóa kết quả.</p>'
    body+=callout('warn','Về phạm vi','Đây là bài kiểm tra TRR1 (INT1358). Các nội dung đồ thị (DFS/BFS, Euler, Hamilton, Dijkstra, cây bao trùm, luồng cực đại) thuộc Toán rời rạc 2 nên không có ở đây.')
    body+=f'<div id="exam"></div><script type="application/json" id="exam-data">{data}</script>'
    return page('Luyện đề',body,2,'Luyện đề trắc nghiệm TRR1',scripts=('store.js','exam.js'))
def cau_truc_page():
    b='<div class="crumbs"><a href="../index.html">Trang chủ</a> › Cấu trúc đề thi</div><h1>Cấu trúc đề thi Toán rời rạc 1 (INT1358)</h1>'
    b+='<h2>1. Đề cương chính thức</h2>'+table(['Mục','Nội dung'],[['Mã học phần','INT1358 · 3 tín chỉ · bắt buộc · tiên quyết: Nhập môn máy tính và lập trình'],['Giờ học','36 giờ lý thuyết + 8 giờ bài tập'],['Đánh giá','Chuyên cần 10% · bài tập 10% · giữa kỳ 10% · cuối kỳ 70% (thiếu thành phần điểm hoặc nghỉ quá 20% số buổi thì không được thi)'],['Học liệu bắt buộc','Rosen, Discrete Mathematics and its Applications, 8th ed., McGraw-Hill 2018'],['Tham khảo','Epp (5th ed., 2019), Levin (3rd ed., 2019); giáo trình TRR PTIT (Nguyễn Duy Phương); Nguyễn Đức Nghĩa – Nguyễn Tô Thành (2005); Đỗ Đức Giáo (2003)'],['Nội dung','Chương 1 Logic, tập hợp, độ phức tạp · Chương 2 Đếm (gồm truy hồi, hàm sinh) · Chương 3 Liệt kê · Chương 4 Tối ưu · Chương 5 Tồn tại']],'left')
    b+='<h2>2. Đề thi cuối kỳ: 5 câu × 2 điểm, 90 phút, không tài liệu</h2>'+table(['Câu','2017–2020 (HK1 2017-18, 2019-20)','2023–2024 (HK1)','Module'],[['1','a) chứng minh tương đương logic (biến đổi hoặc bảng); b) Dirichlet','a) bảng chân lý (hằng đúng/tương đương); b) Dirichlet hoặc đếm','1, 6'],['2','a) lập truy hồi; b) giải truy hồi bậc 2 (nghiệm kép)','đếm: đội văn nghệ, nghiệm nguyên có cận, biển số, bù trừ chia hết','4, 5, 7, 8'],['3','a) nghiệm nguyên có cận; b) trình bày thuật toán liệt kê','giải truy hồi + lập truy hồi xâu nhị phân; số thuận nghịch','5, 7, 8'],['4','viết chương trình C/C++ (sinh hoán vị / quay lui xâu nhị phân)','quay lui hoặc sinh + tìm 4–5 cấu hình kế tiếp bằng tay','10, 11'],['5','duyệt toàn bộ: bài toán cái túi, ghi rõ từng bước','nhánh cận: trình bày thuật toán + áp dụng cái túi','12']])
    b+=callout('info','Nhận xét','Hầu hết câu của đề 2023–2024 lấy nguyên từ ngân hàng câu hỏi tự luận 2019 (đổi số liệu). Vì vậy luyện đúng ngân hàng gốc là cách chuẩn bị hiệu quả nhất. Logic (câu 1a) chỉ chiếm khoảng 1 câu; truy hồi, đếm có cận, sinh/quay lui và nhánh cận chiếm phần lớn điểm.')
    b+='<h2>3. Bài kiểm tra trắc nghiệm (Khoa Trí tuệ nhân tạo): 15 câu, 30 phút</h2>'+table(['Dạng câu','Số đề chứa','Module'],[['Logic: B hằng đúng?','52/52','1'],['Dirichlet thi trắc nghiệm / bi màu','52 + 52','6'],['Từ mã / số nguyên chia hết ít nhất một trong ba số','52 + 52','4'],['Nghiệm nguyên có cận / số thuận nghịch','52 + 52','5'],['Lập truy hồi (số lẻ/chẵn bit)','52','7'],['Giải truy hồi bậc 2 và bậc 3','52 + 52','8'],['Sinh xâu nhị phân / hoán vị / tổ hợp kế tiếp','52 × 3','10'],['Cái túi: phương án tối ưu','52','12'],['Người du lịch: f* đầu tiên','52','13']])
    b+='<p>Bộ đề gồm 52 đề; nhưng chỉ có 15 dạng câu lặp lại với số liệu khác nhau. Hãy luyện đủ 15 dạng ở mục <a href="../luyen-de/index.html">Luyện đề</a>.</p>'
    b+='<h2>4. Phân biệt TRR1 và TRR2 trong tài liệu</h2>'+table(['','Toán rời rạc 1 (INT1358)','Toán rời rạc 2 (INT1359, 412TRR311)'],[['Bản chất','Lý thuyết tổ hợp: đếm, tồn tại, liệt kê, tối ưu','Lý thuyết đồ thị'],['Nội dung','Logic, tập hợp, độ phức tạp; đếm, truy hồi, hàm sinh; sinh, quay lui; duyệt toàn bộ, nhánh cận (cái túi, người du lịch); Dirichlet','Biểu diễn đồ thị; DFS, BFS; đồ thị Euler, Hamilton; cây bao trùm (Prim, Kruskal); đường đi ngắn nhất (Dijkstra…); luồng cực đại'],['Ghi chú','Bài toán người du lịch nằm ở chương Tối ưu của TRR1','Đồ thị Hamilton (điều kiện tồn tại chu trình) thuộc TRR2 dù TSP dùng ý tưởng liên quan'],['Trang này','Có (13 module)','Không có']],'left')
    return page('Cấu trúc đề thi',b,2,'Cấu trúc đề thi INT1358')
def tai_lieu_page():
    b='<div class="crumbs"><a href="../index.html">Trang chủ</a> › Tài liệu</div><h1>Tài liệu nguồn: phân loại TRR1, TRR2 và ngoài PTIT</h1><p class="lead">Không phải tài liệu nào trong bộ đầu vào cũng thuộc Toán rời rạc 1 của PTIT. Bảng dưới phân loại từng nguồn và cách chúng tôi sử dụng.</p>'
    b+='<h2>1. Nguồn dùng cho Toán rời rạc 1 (PTIT)</h2>'+table(['Nguồn','Loại','Cách dùng'],[['Đề cương INT1358 (DISCRETE-MATHEMATICS-I)','chính thức PTIT','Phạm vi 5 chương, đánh giá, học liệu'],['Slide TRR1 (0-Intro, TS. Đào Thị Thuý Quỳnh)','chính thức PTIT (tiếng Anh)','Ví dụ, bài tập gốc, thuật toán'],['Bài giảng TRR1 (ThS. Nguyễn Duy Phương, 2016) và bản 2013','chính thức PTIT','Giáo trình chính, bài tập cuối chương'],['Ngân hàng câu hỏi tự luận INT1358 (2019)','chính thức PTIT','Nguồn câu gốc chính (248 câu con)'],['Đề thi kết thúc học phần 2023–2024 (6 đề, đề 01–06)','đề thật PTIT','Phân tích cấu trúc; câu đều có trong ngân hàng 2019'],['4 ảnh đề TRR1 2017–2018 (đề 5, 6) và 2019–2020 (đề 1, 2)','đề thật PTIT (ảnh chụp)','Phân tích cấu trúc, ví dụ'],['Đề ôn trắc nghiệm TRR1 (Mẫu đề 2, Khoa Trí tuệ nhân tạo)','bài kiểm tra PTIT (không có đáp án)','754/780 câu kiểm chứng được (đã quét lại bằng tọa độ chữ); đáp án tự tính'],['Sách hướng dẫn học tập TRR (Nguyễn Duy Phương, 2006, hệ từ xa)','PTIT, bản cũ','Phần I (tr. 3–104) = TRR1: chỉ dùng đối chiếu']],'left')
    b+='<h2>2. Nguồn thuộc Toán rời rạc 2 (không dùng)</h2>'+table(['Nguồn','Ghi chú'],[['DISCRETE-MATHEMATICS-II (đề cương INT1359)','Lý thuyết đồ thị'],['Ngân hàng câu hỏi tự luận 412TRR311 – Toán rời rạc 2','DFS/BFS, Euler, Hamilton, cây bao trùm, đường đi ngắn nhất, luồng'],['Sách hướng dẫn 2006, Phần II (chương 5–8)','Đồ thị'],['Ảnh đề “Toán rời rạc 2” và “toán rời rạc 2.pdf” (đề 2011 sau đại học)','Trộn nhiều chủ đề đồ thị; ngoài phạm vi TRR1']],'left')
    b+='<h2>3. Nguồn không phải của PTIT (chỉ tham khảo, không làm phạm vi)</h2>'+table(['Nguồn','Trường'],[['Slide C0–C14 (Nguyễn Văn Hiệu)','ĐH Bách khoa – ĐH Đà Nẵng'],['Đề cương và slide chương 1–7 (lvluyen)','ĐH Khoa học Tự nhiên TP.HCM'],['Slide Logic/Tập hợp (Nguyễn Thanh Sơn), handout Propositional Logic','ĐH Bách khoa TP.HCM'],['Hướng dẫn sử dụng Maple','không liên quan']],'left')
    b+='<h2>4. Lỗi và điểm mơ hồ phát hiện trong tài liệu gốc</h2>'+ul(['<b>Giáo trình 2016, §2.4.2 ví dụ 3:</b> phương trình đặc trưng của aₙ = 6aₙ₋₁ − 9aₙ₋₂ ghi r² − 6r − 9 = 0; đúng phải là r² − 6r + 9 = 0.','<b>Ngân hàng 2019, câu 1.19b:</b> (A − B) − C = (A − B) − (B − C) không đúng với mọi tập (phản ví dụ A = {1}, B = ∅, C = {1}).','<b>Ngân hàng 2019, câu 2.2.2b:</b> đề nói “xâu thập phân” nhưng cuối câu ghi “xâu nhị phân”; ta hiểu là xâu thập phân.','<b>Ngân hàng 2019, câu 5.1b:</b> “cùng ngày, tháng sinh” cần giả thiết 366 ngày (kể cả 29/2): đáp án 1465 (bỏ 29/2 thì 1461).','<b>Ngân hàng 2019, câu 2.2.26a:</b> thiếu điều kiện đầu, chỉ xác định được dạng nghiệm tổng quát.','<b>Bài tập giáo trình chương 2, bài 17:</b> số liệu bất khả thi (kết quả âm).','<b>Đề ôn trắc nghiệm:</b> 13 câu có hai phương án trùng nhau trong đề gốc (11 câu nghiệm nguyên, 2 câu người du lịch) và 13 câu bị rối thứ tự chữ trong lớp văn bản của PDF (tuple 0/1, mất phương án): đã loại sau khi quét lại bằng tọa độ chữ; còn 754/780 câu.','<b>Câu người du lịch “f* cập nhật đầu tiên”:</b> đề không nêu thuật toán; cách đọc dùng ở đây (đi theo chỉ số tăng dần) khớp mọi câu còn nguyên phương án nhưng là suy luận.'])
    b+='<h2>5. Nguồn gốc câu hỏi trong ngân hàng</h2><p>Mỗi câu ghi rõ nguồn (ví dụ “Ngân hàng 2019 – 2.1.5(a)”, “Slide TRR1 PTIT – Exercise 2”, “Đề ôn trắc nghiệm – đề 7, câu 4”). Câu mang nhãn <b>Bổ sung</b> do chương trình sinh tham số khi tài liệu gốc chưa đủ (Module 2, 9, 11 hầu như hoàn toàn); đáp án được kiểm chứng độc lập bằng vét cạn hoặc quy hoạch động. Nội dung câu gốc do PTIT và các giảng viên biên soạn; trang này chỉ dùng cho mục đích học tập.</p>'
    return page('Tài liệu',b,2,'Phân loại tài liệu TRR1/TRR2')
def build_extra():
    write('vi/luyen-de/index.html',luyen_de_page())
    write('vi/cau-truc-de/index.html',cau_truc_page())
    write('vi/tai-lieu/index.html',tai_lieu_page())

def review_page():
    mods={}
    for mid,slug in MODS:
        bk=json.load(open(os.path.join(ROOT,'data','qbank',mid+'.json'),encoding='utf-8'))
        mods[mid]=dict(name=TITLES[mid],slug=slug,n=len(bk['items']),e=len(bk['essays']))
    data=json.dumps(dict(mods=mods),ensure_ascii=False).replace('</','<\\/')
    b='<div class="crumbs"><a href="../index.html">Trang chủ</a> › Sổ lỗi &amp; ôn tập</div><h1>Sổ lỗi, ôn tập cách quãng và tiến độ toàn khóa</h1>'
    b+='<p class="lead">Mọi câu bạn làm ở quiz nhanh, ngân hàng câu hỏi và đề luyện tập đều được ghi lại. Câu sai vào <b>Sổ lỗi</b> và được hẹn ôn lại theo lịch cách quãng (1 → 3 → 7 → 14 → 30 ngày khi trả lời đúng; sai thì quay về đầu).</p>'
    b+=callout('info','Cách dùng','1) Học và làm bài như bình thường. 2) Mỗi ngày mở tab “Ôn tập hôm nay” để làm các câu đến hạn. 3) Xem “Chủ đề cần củng cố” để biết nên đọc lại phần nào. 4) Xuất file sao lưu nếu muốn chuyển sang máy khác.')
    b+=f'<div id="review"></div><script type="application/json" id="review-meta">{data}</script>'
    return page('Sổ lỗi & ôn tập',b,2,'Sổ lỗi, ôn tập cách quãng, tiến độ toàn khóa',scripts=('store.js','review.js'))
_old_extra=build_extra
def build_extra():
    _old_extra(); write('vi/so-loi/index.html',review_page())


if __name__=='__main__':
    only=sys.argv[1:] or None
    inf=build_modules(only)
    if not only:
        build_home({m[2]['id'] for m in inf}); build_extra()
        print(len(inf),'modules')
