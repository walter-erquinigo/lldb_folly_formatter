#include <iostream>
#include <folly/AtomicLinkedList.h>
#include <folly/IPAddress.h>

using namespace folly;

int main() {
  AtomicLinkedList<char> ll;
  ll.insertHead('A');
  ll.insertHead('B');
  ll.insertHead('C');
  return 0;
}
