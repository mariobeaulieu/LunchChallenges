#include <iostream>

using namespace std;

void findConsecutive(int myValues[], int myLen, int mySum) {
   for (int i=0; i<myLen; i++) {
       int total = 0;
       for (int j=i; j<myLen; j++) {
           total += myValues[j];
           if ( total == mySum ) {
              cout << "Sequence found!" << endl;
              for (int k=i; k<j; k++)
                  cout << myValues[k] << " + ";
              cout << myValues[j] << " = " << mySum << endl;
              return;
           }
        }
    }
    cout << "No solution found" << endl;
}

int main() {
   int values[] = {1,2,3,4,5,6,7,8,9};
   int mySum    = 22;
   int myLen    = end(values) - begin(values);
   findConsecutive(values, myLen, mySum); 
}


