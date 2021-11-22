#include <iostream>
#include <folly/ConcurrentBitSet.h>

using namespace folly;

int main() {
  ConcurrentBitSet<24> bits;
  bits.set(4);
  // bits.set(7);

  return 0;
}
