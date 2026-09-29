#!/bin/bash
# Biên dịch và kiểm thử các chương trình C++ minh họa (so với Python)
set -e; cd "$(dirname "$0")"; mkdir -p bin; fail=0
# macOS/clang không có <bits/stdc++.h> (GCC có): tạo shim tạm để kiểm thử
mkdir -p shim/bits; printf "#include <iostream>\n#include <vector>\n#include <algorithm>\n#include <numeric>\n#include <cmath>\n#include <string>\n#include <cstring>\n#include <cstdio>\n" > shim/bits/stdc++.h
for f in bin_gen perm_gen comb_gen bin_bt perm_bt comb_bt knap_bb; do g++ -O2 -std=c++17 -I shim -o bin/$f $f.cpp; done
py(){ python3 - "$@"; }
# 1) xâu nhị phân n=4
diff <(echo 4 | ./bin/bin_gen) <(echo 4 | ./bin/bin_bt) >/dev/null && echo "OK bin_gen == bin_bt (n=4)" || { echo FAIL bin; fail=1; }
diff <(python3 -c "print('\n'.join(format(i,'04b') for i in range(16)))") <(echo 4 | ./bin/bin_bt) >/dev/null && echo "OK bin_bt == 0000..1111" || { echo FAIL bin2; fail=1; }
# 2) hoán vị n=5
diff <(echo 5 | ./bin/perm_gen | sed 's/ $//') <(echo 5 | ./bin/perm_bt | sed 's/ $//') >/dev/null && echo "OK perm_gen == perm_bt (n=5)" || { echo FAIL perm; fail=1; }
diff <(python3 -c "
import itertools
for p in itertools.permutations(range(1,6)): print(' '.join(map(str,p)))") <(echo 5 | ./bin/perm_gen | sed 's/ $//') >/dev/null && echo "OK perm_gen == itertools (5! = 120)" || { echo FAIL perm2; fail=1; }
# 3) tổ hợp n=7 k=3
diff <(echo 7 3 | ./bin/comb_gen | sed 's/ $//') <(echo 7 3 | ./bin/comb_bt | sed 's/ $//') >/dev/null && echo "OK comb_gen == comb_bt (7,3)" || { echo FAIL comb; fail=1; }
diff <(python3 -c "
import itertools
for p in itertools.combinations(range(1,8),3): print(' '.join(map(str,p)))") <(echo 7 3 | ./bin/comb_gen | sed 's/ $//') >/dev/null && echo "OK comb_gen == itertools (C(7,3) = 35)" || { echo FAIL comb2; fail=1; }
# 4) cái túi nhánh cận: c=(3,5,7,4) a=(2,4,3,2) b=9 -> f*=?
exp=$(python3 -c "
import sys; sys.path.insert(0,'../../build'); sys.path.insert(0,'../../build/orig')
import knap; print(knap.brute([3,5,7,4],[2,4,3,2],9)[0])")
got=$(printf "4 9\n3 5 7 4\n2 4 3 2\n" | ./bin/knap_bb | sed 's/f\* = //')
[ "$exp" = "$got" ] && echo "OK knap_bb f*=$got" || { echo "FAIL knap exp=$exp got=$got"; fail=1; }
exit $fail
