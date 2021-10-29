#include <iostream>
#include <folly/Range.h>

using namespace folly;

void printStringPiece(std::string _piece) {
  StringPiece str(_piece);
  std::cout << str << std::endl;
}

// void printIntArray(int arr[], int size) {
//   int array[size] = arr;
//   std::cout << str << std::endl;
// }

int main() {
  // Test simple StringPieces
  printStringPiece("Hello");
  printStringPiece("Hello, World!");
  printStringPiece("12345067891");
  
  // Test whether null char is handled
  // Should only show "Test"
  printStringPiece("Test\0Null");

  // What else?

  return 0;
}
