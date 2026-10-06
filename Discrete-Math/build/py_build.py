"""Dựng data/python/problems.json: chạy lời giải mẫu (chương trình độc lập) trên mọi test, đối chiếu bằng check()
(cài đặt khác), kiểm tra thời gian, rồi xuất. Dừng ngay nếu có sai."""
import json, os, subprocess, sys, tempfile, time, re
sys.path.insert(0, os.path.dirname(__file__))
import py_problems as PP
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
def run(code, inp, limit=8):
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f: f.write(code); fn = f.name
    t = time.time()
    r = subprocess.run([sys.executable, fn], input=inp, capture_output=True, text=True, timeout=limit)
    os.unlink(fn)
    if r.returncode: raise RuntimeError(r.stderr[-400:])
    return r.stdout, time.time() - t
def main():
    out = []; worst = 0; ntests = 0
    ids = set()
    for p in PP.PROBS:
        assert p['id'] not in ids; ids.add(p['id'])
        # starter phải chạy được đến hết phần đọc input (không lỗi cú pháp) – kiểm tra cú pháp
        compile(p['starter'], p['id'] + '-starter', 'exec'); compile(p['sol'], p['id'] + '-sol', 'exec')
        tests = []
        for k, inp in enumerate(p['samples']):
            tests.append(dict(i=inp, pub=True))
        for inp in p['tests']:
            if inp not in p['samples']: tests.append(dict(i=inp, pub=False))
        for t in tests:
            o, dt = run(p['sol'], t['i'])
            worst = max(worst, dt); ntests += 1
            if not p['check'](t['i'], o):
                raise SystemExit(f'SAI: {p["id"]} input={t["i"][:80]!r} output={o[:80]!r}')
            if dt > 1.5: print('  chậm', p['id'], round(dt, 2), 's')
            t['o'] = o
        out.append(dict(id=p['id'], mod=p['mod'], lv=p['lv'], title=p['title'], stmt=p['stmt'], inp=p['inp'], out=p['out'], cons=p['cons'],
                        hint=p['hint'], expl=p['expl'], sol=p['sol'], starter=p['starter'], tests=tests))
        print('ok', p['id'], len(tests), 'test')
    os.makedirs(os.path.join(ROOT, 'data', 'python'), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, 'data', 'python', 'problems.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(len(out), 'bài,', ntests, 'test; test chậm nhất', round(worst, 2), 's')
if __name__ == '__main__': main()
