
#include <string>

#include "folly/FBString.h"


void printString(size_t size) {
  folly::fbstring str(std::string(size, 'a'));
  printf("%s\n", str.data());
}

int main() {
  printString(0);
  printString(1);
  printString(2);
  printString(23);
  // With length 24 the internal representation of fbstring changes
  printString(24);
  printString(25);
  printString(50);

  return 0;
}
