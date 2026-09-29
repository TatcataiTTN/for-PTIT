#include <bits/stdc++.h>
using namespace std;
int main(){
    int n, k; cin >> n >> k;
    vector<int> c(k + 1);
    for(int i = 1; i <= k; i++) c[i] = i;           // tổ hợp đầu (1,2,...,k)
    while(true){
        for(int i = 1; i <= k; i++) cout << c[i] << " "; cout << "\n";
        int i = k;
        while(i >= 1 && c[i] == n - k + i) i--;      // vị trí i lớn nhất chưa đạt giá trị tối đa
        if(i == 0) break;                            // tổ hợp cuối (n-k+1,...,n)
        c[i]++;
        for(int j = i + 1; j <= k; j++) c[j] = c[j-1] + 1;
    }
}
