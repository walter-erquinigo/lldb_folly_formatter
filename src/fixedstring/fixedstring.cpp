#include <iostream>
#include <folly/FixedString.h>

using namespace folly;

int main() {
  FixedString<10> str("abcdefghij");
  std::cout << str << std::endl;
  return 0;
}
