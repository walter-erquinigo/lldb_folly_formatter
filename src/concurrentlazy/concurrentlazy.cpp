#include <iostream>
#include <folly/ConcurrentLazy.h>

using namespace folly;

int main() {
  int i = 10;
  auto val = concurrent_lazy([&]{
    return ++i;
  });

  // These should be equal if the calculation is run once
  std::cout << "Expensive Value: " << val() << std::endl;
  std::cout << "Reused Value: " << val() << std::endl;
  return 0;
}
