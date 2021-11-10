#include <iostream>
#include <folly/FBVector.h>

using namespace folly;

int main() {
  fbvector<u_int> Empty({});
  fbvector<int> Ints({ 1, 2, 3, 4, 5 });
  fbvector<float> Floats({ 1.5, 2.5, 3.5, 4.5 });
  fbvector<char> Chars({ 'A', 'B', 'C' });
  fbvector<bool> Bools({ true, false });
  return 0;
}