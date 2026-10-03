import sys, os, json, random, collections, importlib, hashlib
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'orig'))
from qcore import audit, fm
import orig_nh, orig_book, orig_intro, orig_exams, orig_more
from recstore import RECS
MODS=[('m01','Logic mệnh đề'),('m02','Vị từ và lượng từ'),('m03','Tập hợp và độ phức tạp'),('m04','Nguyên lý đếm cơ bản'),('m05','Hoán vị, tổ hợp, nghiệm nguyên'),('m06','Dirichlet và bài toán tồn tại'),('m07','Lập hệ thức truy hồi'),('m08','Giải hệ thức truy hồi'),('m09','Hàm sinh'),('m10','Phương pháp sinh'),('m11','Quay lui'),('m12','Duyệt toàn bộ và nhánh cận (cái túi)'),('m13','Nhánh cận người du lịch')]
KIND2MOD={'logic':'m01','pigeon_exam':'m06','pigeon_ball':'m06','codeword':'m04','incl_excl':'m04','int_sol':'m05','palin':'m05','rec_parity':'m07','rec2':'m08','rec3':'m08','gen_bin':'m10','gen_perm':'m10','gen_comb':'m10','knap':'m12','tsp':'m13'}
TOPIC={'logic':'Phân loại công thức','pigeon_exam':'Dirichlet – thi trắc nghiệm','pigeon_ball':'Dirichlet tổng quát','codeword':'Quy tắc nhân','incl_excl':'Nguyên lý bù trừ','int_sol':'Nghiệm nguyên có cận','palin':'Số thuận nghịch','rec_parity':'Lập hệ thức truy hồi','rec2':'Giải bậc 2','rec3':'Giải bậc 3','gen_bin':'Xâu nhị phân kế tiếp','gen_perm':'Hoán vị kế tiếp','gen_comb':'Tổ hợp kế tiếp','knap':'Phương án tối ưu','tsp':'Phương án đầu tiên'}
LEVEL={'logic':1,'pigeon_exam':2,'pigeon_ball':2,'codeword':2,'incl_excl':2,'int_sol':3,'palin':3,'rec_parity':2,'rec2':3,'rec3':3,'gen_bin':2,'gen_perm':2,'gen_comb':3,'knap':3,'tsp':3}
MIN_TOTAL=100; CAP=300
def load_mau_de():
    pool=json.load(open(os.path.join(os.path.dirname(__file__),'..','..','..','08_curated','mcq_verified.json'))) if False else None
    p='/Users/tuannghiat/Downloads/PTIT - Discrete Math/08_curated/mcq_verified.json'
    pool=json.load(open(p,encoding='utf-8')); out=collections.defaultdict(list)
    for kind,items in pool.items():
        seen=set()
        for it in items:
            key=(it['stem'],it['opts'][it['ans']])
            if key in seen: continue
            seen.add(key)
            out[KIND2MOD[kind]].append(dict(q=fm(it['stem']),opts=[fm(o) for o in it['opts']],correct=it['ans'],explain=fm(it['expl']),level=LEVEL[kind],topic=TOPIC[kind],
              src=f'Đề ôn trắc nghiệm TRR1 (Mẫu đề 2) – đề {it["de"]}, câu {it["n"]}'+(' · '+it['rep'] if it.get('rep') else ''),origin='goc',mon='TRR1'))
    return out
def rec_to_items(recs):
    mcq=collections.defaultdict(list); ess=collections.defaultdict(list)
    rr=random.Random(11)
    for r in recs:
        mod=r['mod']; 
        ws=list(dict.fromkeys(str(w) for w in r.get('wrong',[]) if str(w)!=str(r.get('ans'))))
        if r.get('ans') is not None and len(ws)<3:
            try:
                base=int(str(r['ans']).replace('.','').replace(',',''))
                from qcore import near_ints
                for w in near_ints(base,rr,8,lo=0):
                    if str(w) not in ws and str(w)!=str(r['ans']): ws.append(str(w))
            except Exception: pass
        if r.get('ans') is not None and len(ws)>=3:
            ws=ws[:3]
            opts=[r['ans']]+ws; rr.shuffle(opts)
            mcq[mod].append(dict(q=fm(r['q']),opts=[fm(str(o)) for o in opts],correct=opts.index(r['ans']),explain=fm(r['sol']),level=r['level'],topic=r['topic'],src=r['src'],origin=r.get('origin','goc'),mon='TRR1'))
        else:
            ess[mod].append(dict(q=fm(r['q']),sol=fm(r['sol']),level=r['level'],topic=r['topic'],src=r['src'],origin=r.get('origin','goc'),mon='TRR1'))
    return mcq,ess
def main():
    orig_nh.run(); recs=list(RECS)+orig_book.recs()+orig_intro.recs(); recs+=orig_exams.recs(); recs+=orig_more.recs()
    mcq_nh,ess_nh=rec_to_items(recs); mau=load_mau_de()
    gen_mod={}
    for mid,name in MODS:
        g=importlib.import_module('gen_'+mid); B=g.gen(int(mid[1:])); g.essays(B); gen_mod[mid]=B
    os.makedirs('../data/qbank',exist_ok=True); rep={}
    for mid,name in MODS:
        rng=random.Random(int(mid[1:])*31)
        items=mau.get(mid,[])+mcq_nh.get(mid,[]); ess=ess_nh.get(mid,[])
        n_orig=len(items)
        need=max(0,MIN_TOTAL-n_orig)
        B=gen_mod[mid]
        if need>0:
            by=collections.defaultdict(list)
            for it in B.items: by[it['topic']].append(it)
            for v in by.values(): rng.shuffle(v)
            keys=sorted(by,key=lambda k:-len(by[k])); add=[]
            while len(add)<need and any(by.values()):
                for k in keys:
                    if by[k] and len(add)<need: add.append(by[k].pop())
            for it in add: items.append(dict(q=it['q'],opts=it['opts'],correct=it['correct'],explain=it['explain'],level=it['level'],topic=it['topic'],src='Bổ sung (chương trình sinh tham số, đáp án đã kiểm chứng độc lập)',origin='bo_sung',mon='TRR1'))
        # tự luận: câu gốc trước; bổ sung nếu < 12
        if len(ess)<12:
            for e in B.essays[:max(0,12-len(ess))]:
                ess.append(dict(q=fm(e['q']),sol=fm(e['sol']),level=e['level'],topic=e['topic'],src='Bổ sung (biên soạn thêm, đã kiểm chứng)',origin='bo_sung',mon='TRR1'))
        if len(items)>CAP:
            og=[i for i in items if i['origin']=='goc']; bs=[i for i in items if i['origin']!='goc']
            if len(og)>CAP:
                by=collections.defaultdict(list)
                for it in og: by[it['topic']].append(it)
                for v in by.values(): rng.shuffle(v)
                keys=sorted(by,key=lambda k:-len(by[k])); out=[]
                while len(out)<CAP and any(by.values()):
                    for k in keys:
                        if by[k] and len(out)<CAP: out.append(by[k].pop())
                items=out
        # cân bằng vị trí
        targets=[i%4 for i in range(len(items))]; rng.shuffle(targets)
        for it,t in zip(items,targets):
            c=it['correct']
            if c!=t: it['opts'][c],it['opts'][t]=it['opts'][t],it['opts'][c]; it['correct']=t
            assert len(set(it['opts']))==4,(mid,it['q'][:50],it['opts'])
        rng.shuffle(items)
        for k,it in enumerate(items): it['id']=f'{mid}-{k+1:03d}'
        for k,e in enumerate(ess): e['id']=f'{mid}-E{k+1:02d}'
        json.dump(dict(module=mid,name=name,items=items,essays=ess),open(f'../data/qbank/{mid}.json','w'),ensure_ascii=False,separators=(',',':'))
        a=audit(items); no=sum(1 for i in items if i['origin']=='goc'); ne=sum(1 for e in ess if e['origin']=='goc')
        rep[mid]=dict(n=len(items),n_goc=no,n_bo_sung=len(items)-no,essays=len(ess),essays_goc=ne,pos=a['pos'],chi2=a['chi2'],longest=a['correct_longest_ratio'])
        print(mid,len(items),'gốc',no,'| tự luận',len(ess),'gốc',ne,'|',a['pos'],a['chi2'],a['correct_longest_ratio'])
    json.dump(rep,open('../data/qbank/_audit.json','w'),ensure_ascii=False,indent=1)
if __name__=='__main__': main()
