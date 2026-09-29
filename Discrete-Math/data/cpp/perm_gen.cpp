#include <bits/stdc++.h>
using namespace std;
int main(){
    int n; cin >> n;
    vector<int> p(n); iota(p.begin(), p.end(), 1);   // 1 2 ... n
    while(true){
        for(int v : p) cout << v << " "; cout << "\n";
        int i = n - 2;
        while(i >= 0 && p[i] > p[i+1]) i--;        // i lớn nhất: p[i] < p[i+1]
        if(i < 0) break;                            // hoán vị cuối (n ... 1)
        int j = n - 1;
        while(p[j] < p[i]) j--;                     // j lớn nhất: p[j] > p[i]
        swap(p[i], p[j]);
        reverse(p.begin() + i + 1, p.end());        // đảo đoạn sau i
    }
}
