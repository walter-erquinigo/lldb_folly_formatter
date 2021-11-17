#include <iostream>
#include <folly/AtomicLinkedList.h>
#include <folly/IPAddress.h>

using namespace folly;

int main() {
  AtomicLinkedList<char> ll;
  ll.insertHead('A');
  ll.insertHead('B');
  ll.insertHead('C');

  AtomicLinkedList<IPAddress> li;
  li.insertHead(IPAddress("10.0.0.100"));
  li.insertHead(IPAddress("10.0.1.200"));

  return 0;
}
