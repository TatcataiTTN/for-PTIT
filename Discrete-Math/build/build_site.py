import importlib, json, os, sys, random, collections
from hx import *
from sitelib import *
MODS=[('m01','01-logic-menh-de'),('m02','02-vi-tu-luong-tu'),('m03','03-tap-hop-do-phuc-tap'),('m04','04-nguyen-ly-dem'),('m05','05-to-hop-nghiem-nguyen'),('m06','06-dirichlet-ton-tai'),('m07','07-lap-he-thuc-truy-hoi'),('m08','08-giai-he-thuc-truy-hoi'),('m09','09-ham-sinh'),('m10','10-phuong-phap-sinh'),('m11','11-quay-lui'),('m12','12-cai-tui-nhanh-can'),('m13','13-nguoi-du-lich')]
def pick_quiz(bank,n=10,seed=1):
    rng=random.Random(seed); by=collections.defaultdict(list)
    pool=[i for i in bank['items'] if i.get('origin')=='goc'] or bank['items']
    for it in pool: by[it['topic']].append(it)
    topics=sorted(by); rng.shuffle(topics); out=[]; i=0
    lv_target=[1,1,2,2,2,3,3,2,1,3]
    while len(out)<n and i<200:
        t=topics[i%len(topics)]; i+=1
        want=lv_target[len(out)%len(lv_target)]
        c=[x for x in by[t] if x['level']==want and x not in out] or [x for x in by[t] if x not in out]
        if c: out.append(rng.choice(c))
    return out
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
    body+='<div id="chi-tiet">'+M['notes']+'</div>'
    q=pick_quiz(bank)
    body+='<h2 id="quiz">Tự kiểm tra nhanh (10 câu)</h2><p>Bấm đáp án để chấm ngay. Mọi câu đều có giải thích; có nút làm lại từng câu và cả bài.</p>'+quiz_block('quiz-root',q)
    body+=f'<h2 id="luyen-tap">Luyện tập sâu</h2><div class="grid"><a class="mod-card" href="luyen-tap/index.html"><span class="num">TRẮC NGHIỆM</span><h3>Ngân hàng {len(bank["items"])} câu ({ng} câu gốc)</h3><p>Lọc theo nguồn, mức độ, chủ đề; giải thích chi tiết từng câu; lưu tiến độ; làm lại.</p></a><a class="mod-card" href="luyen-tap/index.html#tu-luan"><span class="num">TỰ LUẬN</span><h3>{len(bank["essays"])} bài có lời giải từng bước</h3><p>Dạng đề thi thật; tự làm rồi đối chiếu lời giải.</p></a></div>'
    prev=MODS[idx-1] if idx>0 else None; nxt=MODS[idx+1] if idx<len(MODS)-1 else None
    body+='<div class="modnav">'+(f'<a href="../{prev[1]}/index.html">← Module {idx}</a>' if prev else '<span></span>')+(f'<a href="../{nxt[1]}/index.html">Module {idx+2} →</a>' if nxt else '<a href="../../luyen-de/index.html">Luyện đề tổng hợp →</a>')+'</div>'
    return page(f'Module {idx+1}. {M["title"]}',body,d,M['subtitle'],scripts=('dm.js','sim.js','deck.js','quiz.js'))
def bank_page(M,idx,bank):
    body=f'<div class="crumbs"><a href="../../../index.html">Trang chủ</a> › <a href="../index.html">Module {idx+1}</a> › Luyện tập</div><h1>Luyện tập · {M["title"]}</h1><p class="lead">{len(bank["items"])} câu trắc nghiệm + {len(bank["essays"])} bài tự luận. Chọn đáp án là chấm ngay và hiện giải thích chi tiết (kể cả khi đúng). Tiến độ lưu trên trình duyệt này.</p>'
    data=json.dumps(dict(module=bank['module'],items=bank['items'],essays=bank['essays']),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    body+=f'<div id="bank"></div><script type="application/json" id="bank-data">{data}</script>'
    return page(f'Luyện tập · {M["title"]}',body,4,'Ngân hàng câu hỏi',scripts=('bank.js',))
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
if __name__=='__main__':
    build_modules(sys.argv[1:] or None)

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
    body+=callout('warn','Về nguồn câu hỏi','Ngân hàng ưu tiên các câu GỐC trích từ tài liệu (ngân hàng câu hỏi 2019, đề thi 2017–2024, bộ đề ôn trắc nghiệm); mỗi câu ghi rõ nguồn. Chỉ khi nguồn gốc quá ít mới có câu “Bổ sung” do chương trình sinh và tự kiểm chứng.')
    return page('Trang chủ',body,1,'Tự học Toán rời rạc 1 PTIT')
def build_home(done):
    write('vi/index.html',home_page(done))
    write('index.html','<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=vi/index.html"><title>Toán rời rạc 1</title><a href="vi/index.html">Vào trang tự học Toán rời rạc 1 (PTIT)</a>')
