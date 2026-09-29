import importlib, json, random, collections, os, sys
from qcore import audit, LET
MODS=[('m01','Logic mệnh đề'),('m02','Vị từ và lượng từ'),('m03','Tập hợp và độ phức tạp'),('m04','Nguyên lý đếm cơ bản'),('m05','Hoán vị, tổ hợp, nghiệm nguyên'),('m06','Dirichlet và bài toán tồn tại'),('m07','Lập hệ thức truy hồi'),('m08','Giải hệ thức truy hồi'),('m09','Hàm sinh'),('m10','Phương pháp sinh'),('m11','Quay lui'),('m12','Duyệt toàn bộ và nhánh cận (cái túi)'),('m13','Nhánh cận người du lịch')]
CAP=300; MINESS=12
def trim(items,cap,rng):
    if len(items)<=cap: return items
    by=collections.defaultdict(list)
    for it in items: by[it['topic']].append(it)
    for v in by.values(): rng.shuffle(v)
    out=[]; 
    # lấy xoay vòng theo chủ đề tới khi đủ cap
    keys=sorted(by,key=lambda k:-len(by[k]))
    while len(out)<cap and any(by.values()):
        for k in keys:
            if by[k] and len(out)<cap: out.append(by[k].pop())
    rng.shuffle(out); return out
def rebalance(items,rng):
    n=len(items); targets=[i%4 for i in range(n)]; rng.shuffle(targets)
    for it,t in zip(items,targets):
        c=it['correct']
        if c!=t:
            it['opts'][c],it['opts'][t]=it['opts'][t],it['opts'][c]; it['correct']=t
    return items
def main():
    os.makedirs('../data/qbank',exist_ok=True); rep={}
    for mid,name in MODS:
        g=importlib.import_module('gen_'+mid); seed=int(mid[1:])
        B=g.gen(seed); g.essays(B)
        rng=random.Random(seed*77)
        items=trim(B.items,CAP,rng)
        for it in items:
            assert it['explain'] and len(it['opts'])==4 and len(set(it['opts']))==4,(mid,it['q'][:60])
        items=rebalance(items,rng)
        ess=list(B.essays)
        # bổ sung tự luận từ câu MCQ mức 3 có lời giải đã kiểm chứng
        pool=[it for it in items if it['level']>=2]
        rng.shuffle(pool); used=set()
        for it in pool:
            if len(ess)>=max(MINESS,14): break
            if it['topic'] in used and len(used)<len(set(x['topic'] for x in pool)): continue
            used.add(it['topic'])
            q=it['q'].replace('Chọn','Xác định').replace(' là:','.')
            ess.append(dict(q=q+' (Trình bày lời giải đầy đủ.)',sol=it['explain']+f'\nĐáp số: {it["opts"][it["correct"]]}',level=it['level'],topic=it['topic']))
        for k,it in enumerate(items): it['id']=f'{mid}-{k+1:03d}'
        for k,e in enumerate(ess): e['id']=f'{mid}-E{k+1:02d}'
        json.dump(dict(module=mid,name=name,items=items,essays=ess),open(f'../data/qbank/{mid}.json','w'),ensure_ascii=False,separators=(',',':'))
        a=audit(items); a['essays']=len(ess); a['topics']=dict(collections.Counter(i['topic'] for i in items)); a['levels']=dict(collections.Counter(i['level'] for i in items))
        rep[mid]=a; print(mid,a['n'],a['essays'],a['pos'],'chi2',a['chi2'],'longest',a['correct_longest_ratio'])
    json.dump(rep,open('../data/qbank/_audit.json','w'),ensure_ascii=False,indent=1)
if __name__=='__main__': main()
