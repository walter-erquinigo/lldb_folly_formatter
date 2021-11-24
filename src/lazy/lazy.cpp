#include <iostream>
#include <folly/Lazy.h>

using namespace folly;

int main() {
  uint runs = 0;
  auto val = lazy([&]{
    // Expensive value calculation
    uint16_t _i = 0;
    ++runs;
    while (_i < UINT16_MAX) {
      ++_i;
    }
    return (uint32_t)(_i + runs);
  });

  // These should be equal if the calculation is run once
  std::cout << "Expensive Value: " << val() << std::endl;
  std::cout << "Reused Value: " << val() << std::endl;
  return 0;
}
