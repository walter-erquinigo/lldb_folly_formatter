#include <iostream>
#include <folly/Optional.h>
#include <folly/FBString.h>

using namespace folly;

int main() {
  Optional<int> someInt;
  someInt = 34;

  Optional<fbstring> someFbStr;
  someFbStr = fbstring("Hello, World!");

  return 0;
}
