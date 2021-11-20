#include <iostream>
#include <bitset>
#include <folly/container/SparseByteSet.h>

using namespace folly;

int main() {
  SparseByteSet set;

  set.add(uint8_t(0xAB));
  set.add(uint8_t(0xCD));
  set.add(uint8_t(0xEF));

  std::cout << set.contains(0xFF) << ' ' << set.contains(0xAB);
  std::cout << std::endl;

  return 0;
}
