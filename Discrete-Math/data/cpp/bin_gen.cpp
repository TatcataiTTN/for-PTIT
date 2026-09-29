#include <bits/stdc++.h>
using namespace std;
int main(){
    int n; cin >> n;
    vector<int> x(n, 0);            // xâu đầu tiên 00...0
    while(true){
        for(int b : x) cout << b; cout << "\n";
        int i = n - 1;
        while(i >= 0 && x[i] == 1) x[i--] = 0;   // đổi các bit 1 cuối thành 0
        if(i < 0) break;                          // hết: xâu 11...1 đã in
        x[i] = 1;                                 // bit 0 phải nhất đổi thành 1
    }
}
