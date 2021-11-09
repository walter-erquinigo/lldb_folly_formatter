#include <iostream>
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
  
  // Vectors with type inferred
  FBVector({ 1, 2, 3, 4, 5 });
  FBVector({ 1.0, 2.0, 3.0, 4.0 });
  FBVector({ 'A', 'B', 'C' });
  FBVector({ true, false });

  // Vectors with explicit type
  FBVector<uint8_t>({ 0xA, 0xB, 0xC, 0xD });
  FBVector<float>({ 1.0, 2.0, 3.0, 4.0 });

  return 0;
}