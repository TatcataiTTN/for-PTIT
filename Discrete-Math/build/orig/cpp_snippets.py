# Mã C++ chuẩn cho các thuật toán liệt kê (được biên dịch và kiểm thử trong data/cpp)
CPP={}
CPP['bin_gen']='''#include <bits/stdc++.h>
using namespace std;
int main(){
    int n; cin >> n;
    vector<int> x(n, 0);            // xâu đầu tiên 00...0
    while(true){
        for(int b : x) cout << b; cout << "\\n";
        int i = n - 1;
        while(i >= 0 && x[i] == 1) x[i--] = 0;   // đổi các bit 1 cuối thành 0
        if(i < 0) break;                          // hết: xâu 11...1 đã in
        x[i] = 1;                                 // bit 0 phải nhất đổi thành 1
    }
}'''
CPP['perm_gen']='''#include <bits/stdc++.h>
using namespace std;
int main(){
    int n; cin >> n;
    vector<int> p(n); iota(p.begin(), p.end(), 1);   // 1 2 ... n
    while(true){
        for(int v : p) cout << v << " "; cout << "\\n";
        int i = n - 2;
        while(i >= 0 && p[i] > p[i+1]) i--;        // i lớn nhất: p[i] < p[i+1]
        if(i < 0) break;                            // hoán vị cuối (n ... 1)
        int j = n - 1;
        while(p[j] < p[i]) j--;                     // j lớn nhất: p[j] > p[i]
        swap(p[i], p[j]);
        reverse(p.begin() + i + 1, p.end());        // đảo đoạn sau i
    }
}'''
CPP['comb_gen']='''#include <bits/stdc++.h>
using namespace std;
int main(){
    int n, k; cin >> n >> k;
    vector<int> c(k + 1);
    for(int i = 1; i <= k; i++) c[i] = i;           // tổ hợp đầu (1,2,...,k)
    while(true){
        for(int i = 1; i <= k; i++) cout << c[i] << " "; cout << "\\n";
        int i = k;
        while(i >= 1 && c[i] == n - k + i) i--;      // vị trí i lớn nhất chưa đạt giá trị tối đa
        if(i == 0) break;                            // tổ hợp cuối (n-k+1,...,n)
        c[i]++;
        for(int j = i + 1; j <= k; j++) c[j] = c[j-1] + 1;
    }
}'''
CPP['bin_bt']='''#include <bits/stdc++.h>
using namespace std;
int n, x[32];
void Try(int i){
    for(int v = 0; v <= 1; v++){
        x[i] = v;
        if(i == n){ for(int j = 1; j <= n; j++) cout << x[j]; cout << "\\n"; }
        else Try(i + 1);
    }
}
int main(){ cin >> n; Try(1); }'''
CPP['perm_bt']='''#include <bits/stdc++.h>
using namespace std;
int n, x[20]; bool used[20];
void Try(int i){
    for(int v = 1; v <= n; v++) if(!used[v]){
        x[i] = v; used[v] = true;                       // chọn v
        if(i == n){ for(int j = 1; j <= n; j++) cout << x[j] << " "; cout << "\\n"; }
        else Try(i + 1);
        used[v] = false;                                // hoàn trả trạng thái
    }
}
int main(){ cin >> n; Try(1); }'''
CPP['comb_bt']='''#include <bits/stdc++.h>
using namespace std;
int n, k, x[20];
void Try(int i){
    for(int v = x[i-1] + 1; v <= n - k + i; v++){
        x[i] = v;
        if(i == k){ for(int j = 1; j <= k; j++) cout << x[j] << " "; cout << "\\n"; }
        else Try(i + 1);
    }
}
int main(){ cin >> n >> k; x[0] = 0; Try(1); }'''
CPP['knap_bb']='''#include <bits/stdc++.h>
using namespace std;
int n, b; int c[20], a[20], x[20], xopt[20]; int fopt = -1;
void Try(int i, int delta, int rem){      // đã gán x[1..i-1]
    int t = min(1, rem / a[i]);
    for(int v = t; v >= 0; v--){
        x[i] = v; int d2 = delta + c[i]*v, r2 = rem - a[i]*v;
        if(i == n){ if(d2 > fopt){ fopt = d2; copy(x+1, x+n+1, xopt+1); } }
        else {
            double g = d2 + (double)c[i+1] * r2 / a[i+1];   // cận trên
            if(g > fopt) Try(i + 1, d2, r2);                // cắt nhánh nếu g <= FOPT
        }
    }
}
int main(){
    cin >> n >> b;
    vector<int> cc(n), aa(n), id(n);
    for(int i = 0; i < n; i++) cin >> cc[i];
    for(int i = 0; i < n; i++) cin >> aa[i];
    iota(id.begin(), id.end(), 0);
    sort(id.begin(), id.end(), [&](int p, int q){ return (long long)cc[p]*aa[q] > (long long)cc[q]*aa[p]; }); // c/a giảm dần
    for(int i = 1; i <= n; i++){ c[i] = cc[id[i-1]]; a[i] = aa[id[i-1]]; }
    Try(1, 0, b);
    cout << "f* = " << fopt << "\\n";
}'''
