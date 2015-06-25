#include<iostream>
#include<cstdio>
#include<cstdlib>
#include<string>
#include<cmath>
#include<stack>
#include<fstream>
#include<sstream>
#include<map>
#include<algorithm>
#include<cassert>
#include<vector>

#define DEBUG 0
#define SMALL 0
#define LARGE 1

using namespace std;
#if DEBUG
#define TRACE(a) cerr << "value of " << #a << ":" << a << endl
#define TRACE(a,b) TRACE(a);TRACE(b)
#define TRACE(a,b,c) TRACE(a,b);TRACE(c)
#define TRACE(a,b,c,d) TRACE(a,b);TRACE(c,d)
#else
#define TRACE(a) 
#define TRACE(a,b) 
#define TRACE(a,b,c) 
#define TRACE(a,b,c,d) 
#endif

#define si(a) scanf("%d",&a)
#define sl(a) scanf("%lld",&a);

#define FOR(i, a, b) for (int i(a), _b(b); i <= _b; ++i)
#define FORD(i, a, b) for (int i(a), _b(b); i >= _b; --i)
#define REP(i, n) for (int i(0), _n(n); i < _n; ++i)
#define REPD(i, n) for (int i((n)-1); i >= 0; --i)
#define ALL(c) (c).begin(), (c).end()


typedef long long int64;
typedef unsigned long long uint64;


int main() {

	int T,D,N;
	string str;
	si(T);
	FOR(test,1,T) {
		si(N); 
		cin >> str;
		int l = str.length();
		int ans = 0,cnt=0;;
		//cnt = str[0]-'0';
		REP(i,l) {
			if(i > cnt) {
				if(str[i]!='0') {
					ans += (i-cnt);
					cnt = i;
				}
			}
			cnt += str[i]-'0';
		}
		cout << "Casee #"<< test << ": " << ans << endl;
	}
	return 0;
}