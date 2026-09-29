#include <bits/stdc++.h>
using namespace std;
int n, x[32];
void Try(int i){
    for(int v = 0; v <= 1; v++){
        x[i] = v;
        if(i == n){ for(int j = 1; j <= n; j++) cout << x[j]; cout << "\n"; }
        else Try(i + 1);
    }
}
int main(){ cin >> n; Try(1); }
