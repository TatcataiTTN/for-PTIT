#include <bits/stdc++.h>
using namespace std;
int n, k, x[20];
void Try(int i){
    for(int v = x[i-1] + 1; v <= n - k + i; v++){
        x[i] = v;
        if(i == k){ for(int j = 1; j <= k; j++) cout << x[j] << " "; cout << "\n"; }
        else Try(i + 1);
    }
}
int main(){ cin >> n >> k; x[0] = 0; Try(1); }
