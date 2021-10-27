#include <iostream>
#include <string>
#include <folly/FBString.h>

int main() {
  folly::fbstring fbstr(std::string(10, 'a'));
  std::cout << fbstr.data() << std::endl;
  return 0;
}
