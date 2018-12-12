#include <list>
#include <iostream>
using namespace std;

void print(list<list<int> > res) {
  for ( auto &a : res ) {
    for (auto &b :a   ) {
      cout << b << ", ";
    }
    cout << endl;
  }
}

list<list<int> > all_subsets(list<int> in) {
  list<list<int> > res = {};

  for (auto &i : in) {
    list<list<int> > res_temp = {};
    for (auto &a : res) {
      list<int> s {a};
      s.push_back(i);
      res_temp.push_back(s);
    }
    res.insert(res.end(), res_temp.begin(), res_temp.end());
    res.push_back(list<int> {i});
  }
  print(res);
  return res;
}

int main(){
  list<int> in = {1,2,3,4};
  list<list<int> > op = all_subsets(in);
  return 0;
}

