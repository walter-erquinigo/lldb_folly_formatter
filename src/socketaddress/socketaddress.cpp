#include <iostream>
#include <folly/SocketAddress.h>

using namespace folly;

void printSocket(std::string host_str, uint16_t port) {
  SocketAddress sock(host_str, port);
  std::cout << sock << std::endl;
}

int main() {
  printSocket("10.0.0.10", 3000);
  printSocket("192.168.0.1", 4000);
  printSocket("::1", 5000);
  printSocket("2620:0:1cfe:face:b00c::3", 6000);

  return 0;
}