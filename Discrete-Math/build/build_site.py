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
    ng=sum(1 for i in bank['items'] if i.get('origin')=='goc'); neg=sum(1 for i in bank['essays'] if i.get('origin')=='goc'); nth=sum(1 for i in bank['items'] if i.get('origin')=='tham_khao')
    body+=f'<p><span class="tag">Môn: Toán rời rạc 1 (INT1358)</span><span class="tag">{M["source"]}</span><span class="tag exam">Đề thi: {M["exam"]}</span><span class="tag">Thời lượng gợi ý: {M["time"]}</span><span class="tag">{len(bank["items"])} câu trắc nghiệm ({ng} câu gốc{f', {nth} tham khảo ngoài PTIT' if nth else ''}) · {len(bank["essays"])} bài tự luận ({neg} gốc)</span></p>'
    body+=callout('good','🎯 Sau module này bạn sẽ','<ul>'+''.join(f'<li>{o}</li>' for o in M['objectives'])+'</ul>')
    body+='<h2 id="slide">Bài giảng dạng slide</h2><p class="lead">Dùng phím ← → hoặc các nút; bấm “Toàn màn hình” để trình chiếu. Mỗi slide có khung “Giải thích cho người mới bắt đầu”.</p>'+deck(slides)
    body+=diag_block(M['id'])+'<div id="chi-tiet">'+M['notes']+'</div>'
    q=pick_quiz(bank)
    body+='<h2 id="quiz">Tự kiểm tra nhanh (10 câu, đổi bộ được)</h2><p>Mỗi lần rút 10 câu từ kho của module. Bấm đáp án để chấm ngay; mọi câu đều có giải thích; có nút làm lại từng câu, đổi bộ câu hỏi, và kết quả được ghi vào <a href="../../so-loi/index.html">Sổ lỗi &amp; ôn tập</a>.</p>'+quiz_block('quiz-root',q)
    body+=f'<h2 id="luyen-tap">Luyện tập sâu</h2><div class="grid"><a class="mod-card" href="luyen-tap/index.html"><span class="num">TRẮC NGHIỆM</span><h3>Ngân hàng {len(bank["items"])} câu ({ng} câu gốc)</h3><p>Lọc theo nguồn, mức độ, chủ đề; giải thích chi tiết từng câu; lưu tiến độ; làm lại.</p></a><a class="mod-card" href="luyen-tap/index.html#tu-luan"><span class="num">TỰ LUẬN</span><h3>{len(bank["essays"])} bài có lời giải từng bước</h3><p>Dạng đề thi thật; tự làm rồi đối chiếu lời giải.</p></a></div>'
    prev=MODS[idx-1] if idx>0 else None; nxt=MODS[idx+1] if idx<len(MODS)-1 else None
    body+='<div class="modnav">'+(f'<a href="../{prev[1]}/index.html">← Module {idx}</a>' if prev else '<span></span>')+(f'<a href="../{nxt[1]}/index.html">Module {idx+2} →</a>' if nxt else '<a href="../../luyen-de/index.html">Luyện đề tổng hợp →</a>')+'</div>'
    return page(f'Module {idx+1}. {M["title"]}',body,d,M['subtitle'],scripts=('store.js','dm.js','sim.js','viz.js','deck.js','quiz.js'))
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
    body+='<h2>Công cụ học tập</h2><div class="grid"><a class="mod-card" href="lap-trinh-python/index.html"><span class="num">THI THỰC HÀNH</span><h3>🐍 Thực hành Python</h3><p>25 bài code, chạy và chấm ngay trong trình duyệt.</p></a><a class="mod-card" href="kiem-tra-dau-vao/index.html"><span class="num">BẮT ĐẦU TẠI ĐÂY</span><h3>🎯 Kiểm tra đầu vào</h3><p>30 câu: biết cần ôn kiến thức nền nào.</p></a><a class="mod-card" href="so-loi/index.html"><span class="num">TIẾN ĐỘ</span><h3>📓 Sổ lỗi &amp; ôn tập</h3><p>Câu sai, lịch ôn cách quãng, tiến độ toàn khóa.</p></a><a class="mod-card" href="thuat-ngu/index.html"><span class="num">SLIDE TIẾNG ANH</span><h3>🔤 Thuật ngữ Việt–Anh</h3><p>110 thuật ngữ, tìm kiếm theo module.</p></a><a class="mod-card" href="cong-thuc/index.html"><span class="num">TRƯỚC KỲ THI</span><h3>∑ Tóm tắt công thức</h3><p>Công thức, khi nào dùng, dạng đề.</p></a></div>'
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
    b+='<h2>1. Nguồn dùng cho Toán rời rạc 1 (PTIT)</h2>'+table(['Nguồn','Loại','Cách dùng'],[['Đề cương INT1358 (DISCRETE-MATHEMATICS-I)','chính thức PTIT','Phạm vi 5 chương, đánh giá, học liệu'],['Slide TRR1 (0-Intro, TS. Đào Thị Thuý Quỳnh)','chính thức PTIT (tiếng Anh)','Ví dụ, bài tập gốc, thuật toán'],['Bài giảng TRR1 (ThS. Nguyễn Duy Phương, 2016) và bản 2013','chính thức PTIT','Giáo trình chính, bài tập cuối chương'],['Ngân hàng câu hỏi tự luận INT1358 (2019)','chính thức PTIT','Nguồn câu gốc chính (248 câu con)'],['Đề thi kết thúc học phần 2023–2024 (6 đề, đề 01–06)','đề thật PTIT','Phân tích cấu trúc; câu đều có trong ngân hàng 2019'],['4 ảnh đề TRR1 2017–2018 (đề 5, 6) và 2019–2020 (đề 1, 2)','đề thật PTIT (ảnh chụp)','Phân tích cấu trúc, ví dụ'],['Đề ôn trắc nghiệm TRR1 (Mẫu đề 2, Khoa Trí tuệ nhân tạo)','bài kiểm tra PTIT (không có đáp án)','780/780 câu đã kiểm chứng đáp án (754 câu nguyên vẹn + 26 câu khôi phục từ ảnh trang, có ghi chú ở phần nguồn); đáp án tự tính'],['Sách hướng dẫn học tập TRR (Nguyễn Duy Phương, 2006, hệ từ xa)','PTIT, bản cũ','Phần I (tr. 3–104) = TRR1: chỉ dùng đối chiếu']],'left')
    b+='<h2>2. Nguồn thuộc Toán rời rạc 2 (không dùng)</h2>'+table(['Nguồn','Ghi chú'],[['DISCRETE-MATHEMATICS-II (đề cương INT1359)','Lý thuyết đồ thị'],['Ngân hàng câu hỏi tự luận 412TRR311 – Toán rời rạc 2','DFS/BFS, Euler, Hamilton, cây bao trùm, đường đi ngắn nhất, luồng'],['Sách hướng dẫn 2006, Phần II (chương 5–8)','Đồ thị'],['Ảnh đề “Toán rời rạc 2” và “toán rời rạc 2.pdf” (đề 2011 sau đại học)','Trộn nhiều chủ đề đồ thị; ngoài phạm vi TRR1']],'left')
    b+='<h2>3. Nguồn không phải của PTIT (chỉ tham khảo, không làm phạm vi)</h2>'+table(['Nguồn','Trường'],[['Slide C0–C14 (Nguyễn Văn Hiệu)','ĐH Bách khoa – ĐH Đà Nẵng'],['Đề cương và slide chương 1–7 (lvluyen)','ĐH Khoa học Tự nhiên TP.HCM'],['Slide Logic/Tập hợp (Nguyễn Thanh Sơn), handout Propositional Logic','ĐH Bách khoa TP.HCM'],['Hướng dẫn sử dụng Maple','không liên quan']],'left')
    b+='<h2>4. Lỗi và điểm mơ hồ phát hiện trong tài liệu gốc</h2>'+ul(['<b>Giáo trình 2016, §2.4.2 ví dụ 3:</b> phương trình đặc trưng của aₙ = 6aₙ₋₁ − 9aₙ₋₂ ghi r² − 6r − 9 = 0; đúng phải là r² − 6r + 9 = 0.','<b>Ngân hàng 2019, câu 1.19b:</b> (A − B) − C = (A − B) − (B − C) không đúng với mọi tập (phản ví dụ A = {1}, B = ∅, C = {1}).','<b>Ngân hàng 2019, câu 2.2.2b:</b> đề nói “xâu thập phân” nhưng cuối câu ghi “xâu nhị phân”; ta hiểu là xâu thập phân.','<b>Ngân hàng 2019, câu 5.1b:</b> “cùng ngày, tháng sinh” cần giả thiết 366 ngày (kể cả 29/2): đáp án 1465 (bỏ 29/2 thì 1461).','<b>Ngân hàng 2019, câu 2.2.26a:</b> thiếu điều kiện đầu, chỉ xác định được dạng nghiệm tổng quát.','<b>Bài tập giáo trình chương 2, bài 17:</b> số liệu bất khả thi (kết quả âm).','<b>Đề ôn trắc nghiệm:</b> 26 câu của bản PDF bị lỗi (11 câu nghiệm nguyên và 2 câu người du lịch có hai phương án trùng nhau; 13 câu còn lại mất phương án khi ngắt trang hoặc rối chữ). Chúng tôi đã khôi phục cả 26: đọc lại tham số trên ảnh trang, tự tính lại đáp án, giữ các phương án gốc còn đọc được và chỉ bổ sung phương án nhiễu khi cần; mỗi câu ghi rõ điều đã khôi phục trong phần nguồn.','<b>Câu người du lịch “f* cập nhật đầu tiên”:</b> đề không nêu thuật toán; cách đọc dùng ở đây (đi theo chỉ số tăng dần) khớp mọi câu còn nguyên phương án nhưng là suy luận.'])
    b+='<h2>5. Nguồn gốc câu hỏi trong ngân hàng</h2><p>Mỗi câu ghi rõ nguồn (ví dụ “Ngân hàng 2019 – 2.1.5(a)”, “Slide TRR1 PTIT – Exercise 2”, “Đề ôn trắc nghiệm – đề 7, câu 4”). Câu mang nhãn <b>Tham khảo ngoài PTIT</b> lấy từ tài liệu của trường khác trong thư mục nguồn (hiện chỉ ở Module 2, vì tài liệu PTIT về vị từ rất ít). Câu mang nhãn <b>Bổ sung</b> do chương trình sinh tham số khi tài liệu gốc chưa đủ (Module 2 và 9 chủ yếu; Module 9 không có tài liệu PTIT nào ngoài hai ví dụ của slide);  đáp án được kiểm chứng độc lập bằng vét cạn hoặc quy hoạch động. Nội dung câu gốc do PTIT và các giảng viên biên soạn; trang này chỉ dùng cho mục đích học tập.</p>'
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

def placement_page():
    import placement_data as P
    data=dict(skills=[dict(id=k['id'],name=k['name'],mods=k['mods'],refresh=k['refresh'],qs=[dict(q=fm(q['q']),ans=q['ans'],wrong=q['wrong'],expl=q['expl']) for q in k['qs']]) for k in P.SK],slugs=dict(MODS))
    js=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    b='<div class="crumbs"><a href="../index.html">Trang chủ</a> › Kiểm tra đầu vào</div><h1>Kiểm tra đầu vào: bạn cần ôn lại gì?</h1><p class="lead">Toán rời rạc 1 dùng nhiều kiến thức nền: logic cơ bản, tập hợp, chia hết, đếm, tổng cấp số, lũy thừa/logarit, đệ quy và đọc chương trình. Bài này có 30 câu (3 câu cho mỗi trong 10 kỹ năng, chọn ngẫu nhiên từ 60 câu, đáp án đã tính bằng chương trình), cho biết kỹ năng nào còn yếu và nên ôn module nào trước. Có thể làm lại để đổi bộ câu.</p>'
    b+=f'<div id="placement"></div><script type="application/json" id="placement-data">{js}</script>'
    return page('Kiểm tra đầu vào',b,2,'Kiểm tra kiến thức nền trước khi học TRR1',scripts=('store.js','placement.js'))
def glossary_page():
    import glossary_data as GD
    mods=dict((m,f'M{int(m[1:])}') for m,_ in MODS)
    rows=''.join(f'<tr data-m="{m}"><td><b>{esc(v)}</b></td><td lang="en">{esc(e)}</td><td><a href="../modules/{dict(MODS)[m]}/index.html">{mods[m]}</a></td><td>{esc(n)}</td></tr>' for v,e,m,n in GD.G)
    b='<div class="crumbs"><a href="../index.html">Trang chủ</a> › Thuật ngữ Việt–Anh</div><h1>Thuật ngữ Việt–Anh</h1><p class="lead">Slide chính thức của Khoa (TS. Đào Thị Thuý Quỳnh) và giáo trình Rosen 8th (học liệu bắt buộc của INT1358) đều bằng tiếng Anh. Bảng này giúp đọc slide và đề tiếng Anh. Gõ vào ô tìm (tiếng Việt hoặc tiếng Anh) để lọc.</p>'
    b+='<p><input id="gq" type="search" placeholder="Tìm thuật ngữ…" style="width:100%;max-width:420px;padding:8px 12px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text);font:inherit"> <select id="gm" style="padding:8px;border-radius:8px;border:1px solid var(--border);background:var(--bg);color:var(--text)"><option value="">Mọi module</option>'+''.join(f'<option value="{m}">Module {int(m[1:])}</option>' for m,_ in MODS)+'</select> <span id="gc"></span></p>'
    b+=f'<div style="overflow-x:auto"><table class="t left" id="gt"><tr><th>Tiếng Việt</th><th>English</th><th>Module</th><th>Ghi chú / ký hiệu</th></tr>{rows}</table></div>'
    b+='<script>(function(){var q=document.getElementById("gq"),m=document.getElementById("gm"),c=document.getElementById("gc"),rs=[].slice.call(document.querySelectorAll("#gt tr[data-m]"));function f(){var s=q.value.trim().toLowerCase(),k=m.value,n=0;rs.forEach(function(r){var ok=(!k||r.dataset.m===k)&&(!s||r.textContent.toLowerCase().indexOf(s)>=0);r.style.display=ok?"":"none";if(ok)n++});c.textContent=n+" / "+rs.length+" thuật ngữ"}q.oninput=f;m.onchange=f;f()})()</script>'
    return page('Thuật ngữ Việt–Anh',b,2,'Bảng thuật ngữ song ngữ Toán rời rạc 1')
def formula_page():
    import formula_data as FD
    b='<div class="crumbs"><a href="../index.html">Trang chủ</a> › Tóm tắt công thức</div><h1>Tóm tắt công thức theo module</h1><p class="lead">Mỗi dòng: công thức, khi nào dùng và dạng đề thi tương ứng. Trang này cố ý gọn để in (Ctrl+P). Cần chứng minh hoặc ví dụ thì vào module tương ứng.</p>'
    for m,name,rows in FD.F:
        b+=f'<h2><a href="../modules/{dict(MODS)[m]}/index.html">Module {int(m[1:])} · {esc(name)}</a></h2>'+table(['Công thức / quy tắc','Khi nào dùng','Dạng đề'],[[esc(a),esc(c),esc(d)] for a,c,d in rows],'left')
    b+=callout('warn','Lưu ý','Đây là bản tóm tắt; khi thi cần trình bày lời giải đầy đủ (ghi rõ phép biến đổi, điều kiện đầu, từng bước thuật toán), không chỉ ghi công thức.')
    return page('Tóm tắt công thức',b,2,'Công thức TRR1 theo module')
_old2=build_extra
def build_extra():
    _old2()
    write('vi/kiem-tra-dau-vao/index.html',placement_page())
    write('vi/thuat-ngu/index.html',glossary_page())
    write('vi/cong-thuc/index.html',formula_page())

def python_page():
    probs=json.load(open(os.path.join(ROOT,'data','python','problems.json'),encoding='utf-8'))
    used=sorted({p['mod'] for p in probs})
    meta=dict(mods=[[m,f'Module {int(m[1:])} · {TITLES[m]}'] for m in used],modname={m:f'Module {int(m[1:])}' for m,_ in MODS},slugs=dict(MODS))
    js=json.dumps(meta,ensure_ascii=False).replace('</','<\\/')
    b='<div class="crumbs"><a href="../index.html">Trang chủ</a> › Thực hành Python</div><h1>Thực hành lập trình Python cho Toán rời rạc 1</h1>'
    b+=f'<p class="lead">{len(probs)} bài lập trình bám các dạng của môn: tập hợp, logic, bù trừ, nghiệm nguyên, truy hồi, hàm sinh, sinh cấu hình, quay lui, cái túi, người du lịch. Mỗi bài có đề đầy đủ (dữ liệu vào, kết quả, giới hạn), ví dụ, nhiều test ẩn, gợi ý và lời giải mẫu có giải thích. <b>Code được chạy và chấm ngay trong trình duyệt</b> (Python thật qua Pyodide/WebAssembly, không cần cài gì, không gửi mã đi đâu).</p>'
    b+=callout('warn','Về bài thi thực hành (chưa có thông báo chính thức)','<p>Theo thông tin truyền miệng từ lớp: môn thi bằng <b>Python</b>, hình thức thực hành, khoảng <b>một nửa là code, một nửa là trắc nghiệm</b>; lịch thi chưa có. Chưa có đề mẫu hay quy chế, nên các bài ở đây là <b>bài tự biên soạn bám nội dung và dạng đề của môn</b>, chưa phải đề thi thật.</p><p>Nên hỏi giảng viên hoặc lớp trưởng: (1) số bài, thời gian; (2) nhập/xuất bằng <code>input()</code>/<code>print()</code> hay bằng file; (3) có được dùng thư viện (<code>math</code>, <code>itertools</code>) không; (4) phiên bản Python và môi trường (IDLE, VS Code, trang chấm online); (5) có chấm bằng test ẩn hay chấm tay. Khi có thêm thông tin, hãy gửi cho chúng tôi để chỉnh trang này.</p>')
    b+='<details class="sim"><summary class="simh">📋 Bảng tra Python nhanh cho bài thi (bấm để mở)</summary>'
    b+='<h3>Vào/ra</h3>'+code('n = int(input())\na = list(map(int, input().split()))      # đọc một dòng nhiều số\nrows = [list(map(int, input().split())) for _ in range(n)]   # ma trận n dòng\nimport sys\ndata = sys.stdin.read().split()                       # đọc hết đầu vào thành các từ\nprint(x, y)                  # cách nhau một dấu cách\nprint(*a)                    # in danh sách cách nhau dấu cách\nprint(\'\\n\'.join(map(str, a)))   # mỗi phần tử một dòng')
    b+='<h3>Thư viện hay dùng</h3>'+code('from math import factorial, comb, gcd, lcm   # lcm có từ Python 3.9\nfrom itertools import permutations, combinations, product\npermutations(range(1, 4))      # (1,2,3), (1,3,2), ... theo thứ tự từ điển\ncombinations(range(1, 5), 2)   # (1,2), (1,3), ... theo thứ tự từ điển\nproduct([0, 1], repeat=3)      # mọi xâu nhị phân độ dài 3\nA | B, A & B, A - B, A ^ B     # hợp, giao, hiệu, hiệu đối xứng của set\nall(...), any(...)             # lượng từ ∀, ∃ trên miền hữu hạn')
    b+='<h3>Lỗi thường gặp</h3>'+ul(['<b>Chia nguyên:</b> dùng <code>//</code>, không dùng <code>/</code> (cho số thực, mất chính xác với số lớn).','<b>Quay lui:</b> quên hoàn tác (<code>pop()</code>, đặt lại <code>False</code>) sau khi gọi đệ quy; lưu nghiệm phải sao chép (<code>x[:]</code>), không lưu chính danh sách đang sửa.','<b>Biến đếm toàn cục</b> trong hàm đệ quy cần khai báo <code>global cnt</code>.','<b>Chỉ số:</b> Python đánh số từ 0, còn đề thường đánh số từ 1; <code>range(1, n + 1)</code> mới đi đến n.','<b>Số rất lớn:</b> Python không tràn số nguyên, nhưng vòng lặp <code>10**9</code> lần thì quá chậm: tìm công thức hoặc quy hoạch động.','<b>Đệ quy sâu:</b> mặc định giới hạn ~1000 tầng; dùng <code>sys.setrecursionlimit</code> hoặc viết vòng lặp.','<b>Định dạng ra:</b> thừa dấu cách cuối dòng và dòng trống cuối thường được bỏ qua; thừa chữ như “Kết quả:” thì sai.'])
    b+='</details>'
    b+=f'<div id="pyroot"></div><script type="application/json" id="py-meta">{js}</script>'
    b+=callout('info','Cách chấm','Mỗi bài có vài test ví dụ (hiện trước) và các test ẩn (có cả trường hợp biên và dữ liệu lớn). “Nộp bài” chạy mọi test, mỗi test giới hạn 8 giây trên trình duyệt (chậm hơn máy thật khoảng 2 đến 3 lần). So khớp bỏ qua dấu cách thừa cuối dòng và dòng trống cuối. Mã của bạn tự lưu trong trình duyệt. Đáp án mọi test đã được kiểm chứng bằng một cách giải khác (vét cạn hoặc công thức khác). Cần mạng để tải Pyodide (~10 MB) từ CDN lần đầu.')
    return page('Thực hành Python',b,2,'Luyện lập trình Python cho Toán rời rạc 1, tự chấm trong trình duyệt',scripts=('pyjudge.js','pycode.js'))
_old3=build_extra
def build_extra():
    _old3(); write('vi/lap-trinh-python/index.html',python_page())


if __name__=='__main__':
    only=sys.argv[1:] or None
    inf=build_modules(only)
    if not only:
        build_home({m[2]['id'] for m in inf}); build_extra()
        print(len(inf),'modules')
