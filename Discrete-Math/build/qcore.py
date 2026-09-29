"""Hạ tầng sinh câu hỏi: mọi câu có đáp án đã kiểm chứng + giải thích. Văn bản thuần (không HTML)."""
import random, math, itertools, json, collections, hashlib, re
def fm(s):
    return re.sub(r'(?<![\w\)\]\}])-(?=[\d(])','−',s) if isinstance(s,str) else s
LET='ABCD'
class Bank:
    def __init__(self, module_id, seed):
        self.id=module_id; self.rng=random.Random(seed*1000+7); self.items=[]; self.essays=[]; self.seen=set()
    def add(self, stem, correct, wrong, explain, level=1, topic=''):
        """correct: chuỗi; wrong: list các chuỗi sai (>=3, khác correct, khác nhau)."""
        stem=fm(stem); explain=fm(explain); correct=fm(str(correct)); wrong=[fm(str(w)) for w in wrong]
        uniq=[]
        for w in wrong:
            if w!=correct and w not in uniq: uniq.append(w)
        if len(uniq)<3: return False
        key=hashlib.md5((stem+"||"+correct).encode()).hexdigest()
        if key in self.seen: return False
        self.seen.add(key)
        opts=[correct]+(self.rng.sample(uniq,3) if len(uniq)>3 else uniq[:3])
        self.rng.shuffle(opts)
        self.items.append(dict(q=stem,opts=opts,correct=opts.index(correct),explain=explain,level=level,topic=topic))
        return True
    def essay(self, stem, solution, level=2, topic=''):
        stem=fm(stem); solution=fm(solution)
        key=hashlib.md5(('E'+stem).encode()).hexdigest()
        if key in self.seen: return False
        self.seen.add(key); self.essays.append(dict(q=stem,sol=solution,level=level,topic=topic)); return True
def near_ints(v, rng, k=8, lo=None):
    s=set(); tries=0; spread=max(3,abs(v)//6+2)
    while len(s)<k and tries<300:
        tries+=1
        d=rng.choice([-3,-2,-1,1,2,3,rng.randint(-spread,spread) or 1])
        w=v+d
        if lo is not None and w<lo: continue
        if w!=v: s.add(w)
    return sorted(s)
def fmt_tuple(t): return '('+', '.join(map(str,t))+')'
def audit(items):
    pos=collections.Counter(it['correct'] for it in items); n=len(items); exp=max(n,1)/4
    chi=sum((pos.get(i,0)-exp)**2/exp for i in range(4))
    multi=[it for it in items if len(set(len(o) for o in it['opts']))>1]
    longest=sum(1 for it in multi if len(it['opts'][it['correct']])>max(len(o) for i,o in enumerate(it['opts']) if i!=it['correct']))
    return dict(n=n,pos={LET[i]:pos.get(i,0) for i in range(4)},chi2=round(chi,2),correct_longest_ratio=round(longest/max(1,len(multi)),3))
