#include <bits/stdc++.h>
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
    cout << "f* = " << fopt << "\n";
}
