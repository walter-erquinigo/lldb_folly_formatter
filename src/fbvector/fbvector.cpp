#include <iostream>
#include <vector>
#include <folly/FBVector.h>

using namespace folly;

template <typename T>
fbvector<T> FBVector(std::initializer_list<T> arr) {
  fbvector<T> fbvec(arr);
  return fbvec;
}

int main() {  
  // Empty vector
  FBVector<u_int>({});
  
  FBVector({ 1, 2, 3, 4, 5 });
  FBVector({ 1.0, 2.0, 3.0, 4.0 });
  FBVector({ 'A', 'B', 'C' });
  FBVector({ true, false });

  return 0;
}