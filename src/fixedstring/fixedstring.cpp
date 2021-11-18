#include <iostream>
#include <folly/FixedString.h>

using namespace folly;

int main() {
  FixedString<10> str("abcdefghij");
  std::cout << str << std::endl;

  FixedString<10> empty;

  FixedString<50> longstr("abcdefghijabcdefghijabcdefghijabcdefghijabcdefghij");
  std::cout << longstr << std::endl;
  return 0;
}
