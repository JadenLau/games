#include <iostream>
using namespace std;

const int p = 4000;
int main() {
    int a;
    cin >> a;
    // calculate percentage change
    float percentage_change = ((float)(a-p)/p)*100;
    cout << "Percentage change: " << percentage_change << "%" << endl;
}