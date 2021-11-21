#include <iostream>
#include <folly/ConcurrentBitSet.h>
// https://github.com/facebook/folly/blob/main/folly/ConcurrentBitSet.h

using namespace folly;

int main() {
  ConcurrentBitSet<65> bits;
  bits.set(4);
  // bits.set(127);

  return 0;
}
