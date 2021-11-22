#include <iostream>
#include <folly/ConcurrentBitSet.h>

using namespace folly;

int main() {
  ConcurrentBitSet<8> bits;
  for (int i = 7; i > 0; i-=2) {
    bits.set(i);
  }

  ConcurrentBitSet<24> manybits;
  for (int i = 23; i > 0; i-=3) {
    manybits.set(i);
  }

  return 0;
}
