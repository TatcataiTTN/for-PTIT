import itertools, random
SYM={'not':'¬','and':'∧','or':'∨','imp':'⇒','iff':'⇔','xor':'⊕'}
PREC={'iff':1,'imp':2,'xor':3,'or':4,'and':5}
def V(n): return ('v',n)
def N(a): return ('not',a)
def A(a,b): return ('and',a,b)
def O(a,b): return ('or',a,b)
def I(a,b): return ('imp',a,b)
def E(a,b): return ('iff',a,b)
def X(a,b): return ('xor',a,b)
def ev(f,env):
    t=f[0]
    if t=='v': return env[f[1]]
    if t=='not': return not ev(f[1],env)
    a=ev(f[1],env); b=ev(f[2],env)
    return {'and':a and b,'or':a or b,'imp':(not a) or b,'iff':a==b,'xor':a!=b}[t]
def vars_of(f):
    if f[0]=='v': return {f[1]}
    s=set()
    for x in f[1:]: s|=vars_of(x)
    return s
def show(f,top=True):
    t=f[0]
    if t=='v': return f[1]
    if t=='not':
        return '¬'+show(f[1],False)
    s=show(f[1],False)+' '+SYM[t]+' '+show(f[2],False)
    return s if top else '('+s+')'
def table(f,vs=None):
    vs=vs or sorted(vars_of(f)); rows=[]
    for vals in itertools.product([True,False],repeat=len(vs)):
        env=dict(zip(vs,vals)); rows.append((vals,ev(f,env)))
    return vs,rows
def kind(f):
    _,rows=table(f); r=[x[1] for x in rows]
    return 'taut' if all(r) else ('contra' if not any(r) else 'cont')
def count_true(f,vs=None):
    _,rows=table(f,vs); return sum(1 for _,r in rows if r)
def equiv(f,g):
    vs=sorted(vars_of(f)|vars_of(g)); return all(ev(f,dict(zip(vs,v)))==ev(g,dict(zip(vs,v))) for v in itertools.product([True,False],repeat=len(vs)))
def counterexample(f,g):
    vs=sorted(vars_of(f)|vars_of(g))
    for v in itertools.product([True,False],repeat=len(vs)):
        env=dict(zip(vs,v))
        if ev(f,env)!=ev(g,env): return env
    return None
def rand_formula(rng,vs,depth):
    if depth==0 or (depth<=2 and rng.random()<0.25):
        v=V(rng.choice(vs)); return N(v) if rng.random()<0.3 else v
    t=rng.choice(['and','or','imp','imp','iff','xor','and','or','not'])
    if t=='not': return N(rand_formula(rng,vs,depth-1))
    return (t,rand_formula(rng,vs,depth-1),rand_formula(rng,vs,depth-1))
def DV(b): return 'Đ' if b else 'S'
def env_str(env): return ', '.join(f'{k}={DV(v)}' for k,v in sorted(env.items()))
def eval_steps(f,env):
    """liệt kê giá trị các công thức con theo thứ tự từ trong ra ngoài"""
    out=[]; seen=set()
    def go(g):
        if g[0]=='v': return
        for x in g[1:]: go(x)
        s=show(g); 
        if s not in seen: seen.add(s); out.append(f'{s} = {DV(ev(g,env))}')
    go(f); return out
def subst_names(f,mp):
    if f[0]=='v': return ('v',mp.get(f[1],f[1]))
    return (f[0],)+tuple(subst_names(x,mp) for x in f[1:])
