#include <iostream>
#include <folly/Range.h>

using namespace folly;

void printStringPiece(std::string _piece) {
  StringPiece str(_piece);
  std::cout << str << std::endl;
}

template <typename T>
Range<const T*> RangeFromVector(std::vector<T> vec) {
  auto range = Range<const T*>(&vec[0], vec.size());
  return range;
}

ByteRange ByteRangeFromStringPiece(std::string _piece) {
  StringPiece str(_piece);
  ByteRange byter(str);
  return byter;
}

MutableByteRange MutByteRangeFromStringPiece(std::string _piece) {
  MutableStringPiece str(&_piece.front(), _piece.size());
  MutableByteRange byter(str);
  return byter;
}

int main() {
  // Test simple StringPieces
  printStringPiece("Hello");
  printStringPiece("Hello, World!");
  printStringPiece("1234567890");
  
  // Test whether null char is handled. Should only show "Test"
  printStringPiece("Test\0Null");

  // From vectors
  RangeFromVector(std::vector<uint32_t>({ 1, 2, 3, 4 }));
  RangeFromVector(std::vector<float_t>({ 1.0, 2.0, 3.0 }));
  RangeFromVector(std::vector<char32_t>({ 'A', 'B' }));

  // Simple ByteRange
  ByteRangeFromStringPiece("Hello, World!");
  // Mutable ByteRange
  MutByteRangeFromStringPiece("Hello, World!");

  // Lastly, empty array
  std::array<int, 0> empty{};
  constexpr auto EmptyRange = Range<const int*>{empty};

  return 0;
}
