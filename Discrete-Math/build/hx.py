"""Bộ dựng HTML: slide, công thức, callout, ví dụ… (Python -> chuỗi HTML)"""
import html, json, re
def esc(s): return html.escape(str(s),quote=False)
def sl(body,kicker=None,title=None,explain=None):
    h=''
    if kicker: h+=f'<div class="kicker">{kicker}</div>'
    if title: h+=f'<h2>{title}</h2>'
    h+=body
    if explain: h+=f'<details class="slide-explain"><summary>📖 Giải thích cho người mới bắt đầu</summary><div class="slide-explain-body">{explain}</div></details>'
    return h
def formula(label,math,legend=None):
    h=f'<div class="pd-formula"><div class="pd-formula-label">{label}</div><div class="pd-formula-math">{math}</div></div>'
    if legend: h+='<ul class="pd-legend">'+''.join(f'<li><b>{k}</b><span>{v}</span></li>' for k,v in legend)+'</ul>'
    return h
def callout(kind,title,body):
    k={'info':'','good':' good','warn':' warn','bad':' bad'}[kind]
    return f'<div class="callout{k}"><b class="t">{title}</b>{body}</div>'
def ex(title,body): return f'<div class="ex"><div class="exh">Ví dụ · {title}</div>{body}</div>'
def table(head,rows,cls=''):
    return f'<table class="t {cls}"><tr>'+''.join(f'<th>{h}</th>' for h in head)+'</tr>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</table>'
def code(t,lang=''): return f'<pre><code>{esc(t)}</code></pre>'
def ul(items,ordered=False):
    t='ol' if ordered else 'ul'; return f'<{t}>'+''.join(f'<li>{i}</li>' for i in items)+f'</{t}>'
def sim(name): return f'<div class="sim" data-sim="{name}"></div>'
def diag(path,alt,cap=''): return f'<div class="diag"><a href="{path}" target="_blank" rel="noopener"><img src="{path}" alt="{esc(alt)}" loading="lazy"></a>'+(f'<div style="font-size:.78rem;color:var(--muted)">{cap}</div>' if cap else '')+'</div>'
def divider(n,total,title,bullets):
    return f'<div class="kicker">PHẦN {n}/{total}</div><div class="part-num">{n:02d}</div><h2>{title}</h2><ul class="part-list">'+''.join(f'<li>{b}</li>' for b in bullets)+'</ul>'
def deck(slides_html,deck_id='d0'):
    """slides_html: list of (html, is_divider)"""
    s=''
    for h,div in slides_html:
        s+=f'<div class="mdeck-slide{" part-divider" if div else ""}">{h}</div>'
    return (f'<div class="mdeck" id="{deck_id}"><div class="mdeck-viewport">{s}</div>'
            '<div class="mdeck-bar"><button class="mdeck-prev" type="button">◀ Trước</button><button class="mdeck-next" type="button">Sau ▶</button>'
            '<span class="mdeck-count"></span><div class="mdeck-dots"></div><button class="mdeck-fs" type="button">⛶ Toàn màn hình</button></div></div>')
def quiz_block(root_id,items,title='Tự kiểm tra nhanh',pick=10):
    data=json.dumps(dict(pick=pick,items=[dict(id=i.get('id'),m=i.get('id','').split('-')[0] if i.get('id') else None,topic=i.get('topic'),level=i.get('level'),q=i['q'],opts=i['opts'],correct=i['correct'],explain=i['explain']) for i in items]),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    return f'<div class="quiz"><div id="{root_id}"></div></div><script type="application/json" class="quiz-data" data-root="{root_id}">{data}</script>'

def viz(name): return f'<div class="sim" data-viz="{name}"></div>'
