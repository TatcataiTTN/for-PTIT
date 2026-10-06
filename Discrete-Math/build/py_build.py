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

EXAM_SETS = [
 ('de-01','Đề 1: Tập hợp, truy hồi, nghiệm nguyên',['tap-hop','truy-hoi-tinh','nghiem-nguyen'],'Mở đầu nhẹ; truy hồi và đếm nghiệm có cận.'),
 ('de-02','Đề 2: Logic, bù trừ, n quân hậu',['logic-phan-loai','bu-tru','n-quan-hau'],'Bảng chân lý, nguyên lý bù trừ, quay lui.'),
 ('de-03','Đề 3: Tổ hợp, tháp Hà Nội, số thuận nghịch',['hoan-vi-to-hop','thap-ha-noi','thuan-nghich'],'Đếm cơ bản đến đếm có cấu trúc.'),
 ('de-04','Đề 4: Dirichlet, tổ hợp kế tiếp, cái túi',['dirichlet','to-hop-ke-tiep','cai-tui'],'Dirichlet, thuật toán sinh, tối ưu.'),
 ('de-05','Đề 5: Lượng từ, hoán vị kế tiếp, xâu có k số 1',['luong-tu','hoan-vi-ke-tiep','k-so-1-lien-tiep'],'Logic vị từ, sinh hoán vị, lập truy hồi.'),
 ('de-06','Đề 6: Sinh xâu, đổi tiền, hàm sinh',['sinh-xau-nhi-phan','doi-tien','ham-sinh-chon-qua'],'Sinh cấu hình và hàm sinh.'),
 ('de-07','Đề 7: Quay lui, tập con, hạng hoán vị',['hoan-vi-quay-lui','tap-con-tong','hang-hoan-vi'],'Quay lui và xếp hạng hoán vị.'),
 ('de-08','Đề 8: Từ mã, người du lịch, đường đi trên lưới',['tu-ma','nguoi-du-lich','duong-di-khong-lap'],'Đếm, vét cạn TSP, quay lui trên lưới.'),
 ('de-09','Đề 9: Liệt kê tổ hợp, cận dưới TSP, nghiệm phân biệt',['to-hop-liet-ke','can-duoi-tsp','nghiem-phan-biet'],'Thuật toán sinh, nhánh cận, truy hồi.'),
 ('de-10','Đề 10: Tương đương logic, suy luận, cái túi vô hạn',['tuong-duong-logic','suy-luan','cai-tui-vo-han'],'Logic mệnh đề và tối ưu.'),
 ('de-11','Đề 11: Tập con, độ phức tạp, nghiệm phân biệt',['tap-con-theo-kich-thuoc','dem-lenh-log','nghiem-phan-biet'],'Tập hợp, độ phức tạp, truy hồi.'),
 ('de-12','Đề 12: Từ mã, đoạn chia hết, xâu có k số 1',['tu-ma','day-con-chia-het','k-so-1-lien-tiep'],'Đếm, Dirichlet, truy hồi.'),
]
def write_exams(out):
    ids = {p['id']: p for p in out}; sets = []
    for sid, title, pids, desc in EXAM_SETS:
        for i in pids: assert i in ids, (sid, i)
        assert len(set(pids)) == len(pids)
        lv = [ids[i]['lv'] for i in pids]; assert lv == sorted(lv), (sid, lv)       # mức khó không giảm
        mins = {3: 60, 4: 80, 5: 100}[len(pids)]
        sets.append(dict(id=sid, title=title, ids=pids, minutes=mins, desc=desc))
    json.dump(dict(sets=sets), open(os.path.join(ROOT, 'data', 'python', 'exams.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    cfg = os.path.join(ROOT, 'data', 'python', 'config.json')
    if not os.path.exists(cfg): json.dump(dict(submitUrl=''), open(cfg, 'w'), indent=1)      # không ghi đè cấu hình đã có
    print(len(sets), 'đề thi thử')
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
    write_exams(out)
    print(len(out), 'bài,', ntests, 'test; test chậm nhất', round(worst, 2), 's')
if __name__ == '__main__': main()
