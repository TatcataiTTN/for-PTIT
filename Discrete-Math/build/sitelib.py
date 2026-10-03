import os, json, html, re
from hx import *
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))   # .../Discrete-Math
NAV=[('Trang chủ','{r}vi/index.html'),('Lộ trình','{r}vi/index.html#lo-trinh'),('Luyện đề','{r}vi/luyen-de/index.html'),('Cấu trúc đề','{r}vi/cau-truc-de/index.html'),('Tài liệu','{r}vi/tai-lieu/index.html')]
TOOLS=[('🎯 Kiểm tra đầu vào','{r}vi/kiem-tra-dau-vao/index.html'),('📓 Sổ lỗi & ôn tập','{r}vi/so-loi/index.html'),('🔤 Thuật ngữ Việt–Anh','{r}vi/thuat-ngu/index.html'),('∑ Tóm tắt công thức','{r}vi/cong-thuc/index.html')]
SRC=[('19SgNozB5mT-G2cJXGYmimcKXKzROf3t7','0-Intro_en-da-gop.pdf','slide TRR1 (TS. Đào Thị Thuý Quỳnh)'),
('1_qNbqwynY-nnEIVpNDDPpZ8oD7nPt_sP','Toán rời rạc 1 - 2016.pdf','bài giảng/giáo trình TRR1 2016 (ThS. Nguyễn Duy Phương)'),
('1aVoHQjjbqh65QKnllJ5kvWvdErwWY0-M','Bài giảng toán rời rạc 1 PTIT (Studocu)','bài giảng TRR1 2013'),
('1tFjJLq0G0gCLjrvDNm4L5azCIoeXlBNq','DISCRETE-MATHEMATICS-I.pdf','đề cương INT1358'),
('13B09M2BpuPPrzpZAFH2rQzuGTkyC8MBx','Ngân hàng câu hỏi thi môn Toán rời rạc 1 (INT 1358) năm 2019 (Studocu)','ngân hàng câu hỏi tự luận'),
('10dd3kIn8eS1y4LcR_3nsJk0clMyIjzKr','Đề thi kết thúc học phần Toán rời rạc 1, kỳ 1 năm 2023-2024 (Studocu)','đề thi thật'),
('1pXcMlycn292r_MJ87T_HOHkFm0u_ZwCa','Đề ôn tập trắc nghiệm TRR1 (Mẫu đề 2) (Studocu)','bộ đề trắc nghiệm, Khoa Trí tuệ nhân tạo'),
('1NkkV0g1k2w2Q2xEN8IH_6avtnp0WX19u','DISCRETE-MATHEMATICS-II.pdf','đề cương INT1359: thuộc TRR2, chỉ để phân loại'),
('1H7umXkKRJ8YfJFS-mNN3rGVYzDr3H9X4','Ngân hàng câu hỏi tự luận 412TRR Toán rời rạc 2 (Studocu)','thuộc TRR2, chỉ để phân loại')]
def src_list():
    return ''.join(f'<li><a href="https://drive.google.com/file/d/{i}/view" target="_blank" rel="noopener">{n}</a> · {d}</li>' for i,n,d in SRC)
def page(title,body,depth,desc='',scripts=(),extra_head=''):
    r='../'*depth
    nav=''.join(f'<a href="{u.format(r=r)}">{t}</a>' for t,u in NAV)
    tools=''.join(f'<a href="{u.format(r=r)}" style="display:block">{t}</a>' for t,u in TOOLS)
    sc=''.join(f'<script src="{r}_shared/{s}"></script>' for s in scripts)
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Toán rời rạc 1 PTIT</title><meta name="description" content="{esc(desc)}">
<script>(function(){{try{{var t=localStorage.getItem('site-theme');if(t&&t!=='light')document.documentElement.setAttribute('data-theme',t);var f=localStorage.getItem('site-font');if(f)document.documentElement.style.fontSize=f}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="{r}_shared/common.css">{extra_head}</head><body>
<header class="top"><div class="wrap"><a class="brand" href="{r}vi/index.html">∑ Toán rời rạc 1 · PTIT</a><nav>{nav}
<details class="menu"><summary>🧰 Học tập ▾</summary><div class="pop">{tools}</div></details>
<details class="menu"><summary>🎨 Giao diện</summary><div class="pop"><button data-set-theme="light">Sáng</button><button data-set-theme="dark">Tối</button><button data-set-theme="sepia">Sepia</button><hr><button data-set-font="14px">Chữ nhỏ</button><button data-set-font="16px">Chữ vừa</button><button data-set-font="19px">Chữ lớn</button></div></details></nav></div></header>
<main class="wrap">{body}</main>
<footer class="foot"><div class="wrap"><p><b>Nguồn tài liệu:</b> các file PDF trong thư mục Google Drive <a href="https://drive.google.com/drive/folders/1fSjd2VaR3lK7kNsXpz_zEZJKAeOrao2q?usp=sharing" target="_blank" rel="noopener">drive.google.com/drive/folders/1fSjd2VaR3lK7kNsXpz_zEZJKAeOrao2q</a>:</p><ul style="margin:.3em 0 .8em;padding-left:1.2em">{src_list()}</ul>
<p>Tài liệu tự học không chính thức của người học, dựa trên các nguồn trên (giáo trình Toán rời rạc PTIT, ThS. Nguyễn Duy Phương; slide TS. Đào Thị Thuý Quỳnh; đề cương INT1358; ngân hàng câu hỏi và đề thi các năm). Mọi đáp án số đều được tính và kiểm chứng bằng chương trình; nếu phát hiện sai sót vui lòng báo lại. Đối chiếu đề cương chính thức của giảng viên khi cần. Nội dung gốc thuộc PTIT và các tác giả tương ứng.</p></div></footer>
<script src="{r}_shared/theme.js"></script>{sc}</body></html>'''
def write(relpath,content):
    p=os.path.join(ROOT,relpath); os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,'w',encoding='utf-8').write(content)
def load_bank(mid): return json.load(open(os.path.join(ROOT,'data','qbank',mid+'.json'),encoding='utf-8'))
def truth_table_html(f,LT,title=''):
    vs,rows=LT.table(f); 
    head=vs+[LT.show(f)]
    body=[[('Đ' if x else 'S') for x in vals]+[('Đ' if r else 'S')] for vals,r in rows]
    return table(head,body)
