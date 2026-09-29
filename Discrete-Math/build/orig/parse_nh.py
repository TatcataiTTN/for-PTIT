import re, json
SRC="/Users/tuannghiat/Downloads/PTIT - Discrete Math/07_new/text/Ngân hàng câu hỏi thi môn Toán rời rạc 1 (INT 1358) năm 2019 - Studocu.txt"
def load():
    t=open(SRC,encoding='utf-8').read().replace('\f','\n')
    lines=t.split('\n')
    items=[];cur=None;chap=None
    idre=re.compile(r'^\s*(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\.?\s*(.*)$')
    for ln in lines:
        m=re.match(r'^\s*CHƯƠNG\s+(\d)',ln)
        if m: chap=int(m.group(1)); continue
        if re.match(r'^\s*(NGÂN HÀNG|Tên học phần|Ngành đào tạo)',ln): continue
        m=idre.match(ln)
        if m and m.group(1).split('.')[0] in '12345' and (chap is None or True) and m.group(1).split('.')[0]==str(chap) or (m and m.group(1).split('.')[0]=='4' and int(m.group(1).split('.')[1])<=30 and cur is not None and chap in (3,4)):
            # id đầu dòng
            chap=int(m.group(1).split('.')[0]); cur=dict(id=m.group(1),chap=chap,text=m.group(2).strip()); items.append(cur); continue
        if cur is not None and ln.strip(): cur['text']+='\n'+ln.strip()
    return items
def split_parts(text):
    # tách a) b) c)
    parts=re.split(r'\n?\s*(?:^|(?<=\n))([a-e])[\)\.]\s*',text)
    if len(parts)<3: return [('',text.strip())]
    out=[]
    head=parts[0].strip()
    for i in range(1,len(parts),2): out.append((parts[i],parts[i+1].strip()))
    if head: out.insert(0,('',head))
    return out
if __name__=='__main__':
    its=load(); print(len(its))
    import collections
    print(collections.Counter(i['chap'] for i in its))
    n=0
    for it in its:
        ps=split_parts(it['text']); n+=len([p for p in ps if p[0]])+(0 if any(p[0] for p in ps) else 1)
    print('parts',n)
    json.dump(its,open('nh_raw.json','w'),ensure_ascii=False,indent=1)
