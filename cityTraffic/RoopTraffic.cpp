#include <set>
#include <map>
#include <vector>
#include <iostream>

using namespace std;
typedef int city;
typedef int popl;
typedef int in_traf;
typedef map<city, in_traf> edges;

map< city, edges > G;
map< city, popl > P;
set< city > V;

int max_visitors_from(city c) {
  V.insert(c);
  auto& nbrs = G[c];
  int r = P[c];
  for (auto& x : nbrs) {
    if (V.find(x.first) != V.end()) continue;
    if (x.second == -1) {
      x.second = max_visitors_from(x.first);
    }
    r += x.second;
  }
  return r;
}

int main() {    
    G[1] = {{2, -1}};
    G[2] = {{1, -1}, {3, -1}, {4, -1}, {5, -1}};
    G[3] = {{2, -1}};
    G[4] = {{2, -1}, {6, -1}};
    G[5] = {{2, -1}};
    G[6] = {{4, -1}, {7, -1}, {8, -1}};
    G[7] = {{6, -1}};
    G[8] = {{6, -1}};
    P[1] = 10;
    P[2] = 30;
    P[3] = 10;
    P[4] = 20;
    P[5] = 20;
    P[6] = 40;
    P[7] = 50;
    P[8] = 60;

    for (auto& c : G) {
      int m = 0;
      V.insert(c.first);
      for (auto&nbr : c.second) {
	int m1 = max_visitors_from(nbr.first);
	if (m1 > m) m = m1;
      }
      cout << "City " << c.first << " will have a max traffic of " << m << endl;
      V.clear();
    }
    
    return 0;
}
