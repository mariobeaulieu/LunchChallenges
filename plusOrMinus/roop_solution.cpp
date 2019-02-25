#include <set>
#include <iostream>
using namespace std;

bool subset(set<int> &in, set<int> &add, set<int> &sub, int R) {
    if (in.empty()) {
        int tmp = 0;
        for (auto & x : add)
            tmp += x;
        for (auto & y :sub)
            tmp -= y;
        if (tmp == R) {
	    for (auto & y : add)
		cout << y << " + ";
	    for (auto & y : sub)
		cout << " - " << y;
	    return true;
	} else {
	    return false;
	}
    }

    for (auto x : in) {
        in.erase(x); add.insert(x);
        if (subset(in, add, sub, R)) return true;
        else {
            add.erase(x); sub.insert(x);
            if (subset(in, add, sub, R)) return true;
        }
	sub.erase(x);
	in.insert(x);
    }
    return false;
}

int main() {
    set<int> in = {1, 2, 3, 4, 6, 7, 8, 9};
    set<int> add;
    set<int> sub;
    int R = 0;

    if (subset(in, add, sub, R)) {
        cout << "adds up" << endl;
    } else {
        cout << "doesn't add up" << endl;
    }
    return 0;
}
