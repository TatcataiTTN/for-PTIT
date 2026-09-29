#include <bits/stdc++.h>
using namespace std;
int n, x[20]; bool used[20];
void Try(int i){
    for(int v = 1; v <= n; v++) if(!used[v]){
        x[i] = v; used[v] = true;                       // chọn v
        if(i == n){ for(int j = 1; j <= n; j++) cout << x[j] << " "; cout << "\n"; }
        else Try(i + 1);
        used[v] = false;                                // hoàn trả trạng thái
    }
}
int main(){ cin >> n; Try(1); }
