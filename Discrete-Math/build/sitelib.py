import os, json, html, re
from hx import *
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))   # .../Discrete-Math
NAV=[('Trang chủ','{r}vi/index.html'),('Lộ trình','{r}vi/index.html#lo-trinh'),('Luyện đề','{r}vi/luyen-de/index.html'),('Cấu trúc đề thi','{r}vi/cau-truc-de/index.html'),('Tài liệu','{r}vi/tai-lieu/index.html')]
def page(title,body,depth,desc='',scripts=(),extra_head=''):
    r='../'*depth
    nav=''.join(f'<a href="{u.format(r=r)}">{t}</a>' for t,u in NAV)
    sc=''.join(f'<script src="{r}_shared/{s}"></script>' for s in scripts)
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Toán rời rạc 1 PTIT</title><meta name="description" content="{esc(desc)}">
<script>(function(){{try{{var t=localStorage.getItem('site-theme');if(t&&t!=='light')document.documentElement.setAttribute('data-theme',t);var f=localStorage.getItem('site-font');if(f)document.documentElement.style.fontSize=f}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="{r}_shared/common.css">{extra_head}</head><body>
<header class="top"><div class="wrap"><a class="brand" href="{r}vi/index.html">∑ Toán rời rạc 1 · PTIT</a><nav>{nav}
<details class="menu"><summary>🎨 Giao diện</summary><div class="pop"><button data-set-theme="light">Sáng</button><button data-set-theme="dark">Tối</button><button data-set-theme="sepia">Sepia</button><hr><button data-set-font="14px">Chữ nhỏ</button><button data-set-font="16px">Chữ vừa</button><button data-set-font="19px">Chữ lớn</button></div></details></nav></div></header>
<main class="wrap">{body}</main>
<footer class="foot"><div class="wrap">Tài liệu tự học không chính thức, dựa trên giáo trình Toán rời rạc (PTIT, ThS. Nguyễn Duy Phương), đề cương INT1358 và đề thi các năm. Mọi đáp án số đều được tính và kiểm chứng bằng chương trình; nếu phát hiện sai sót vui lòng báo lại. Đối chiếu đề cương chính thức của giảng viên khi cần.</div></footer>
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
