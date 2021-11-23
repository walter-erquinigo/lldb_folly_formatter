#include <iostream>
#include <folly/Lazy.h>
// #include <folly/ConcurrentLazy.h>

using namespace folly;

int main() {
  auto val = lazy([&]{
    return UINT16_MAX;
  });
  val();

  // auto const cval = concurrent_lazy([&]{
  //   return UINT32_MAX;
  // });
  // cval();

  return 0;
}
