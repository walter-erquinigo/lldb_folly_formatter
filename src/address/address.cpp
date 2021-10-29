#include <iostream>
#include <string>
#include <folly/IPAddress.h>
#include <folly/MacAddress.h>
#include <folly/SocketAddress.h>

using namespace folly;

void printIP4(std::string ip4_str) {
  IPAddress ip4(ip4_str);
  std::cout << ip4 << std::endl;
}

void printIP6(std::string ip6_str) {
  IPAddress ip6(ip6_str);
  std::cout << ip6 << std::endl;
}

void printSocket(std::string host_str, uint16_t port) {
  SocketAddress sock(host_str, port);
  std::cout << sock << std::endl;
}

int main() {
  // IPv4 addresses
  printIP4("10.0.0.10");
  printIP4("192.168.0.1");

  // IPv6 Addresses
  printIP6("::1");
  printIP6("2620:0:1cfe:face:b00c::3");

  printSocket("10.0.0.10", 3000);
  printSocket("192.168.0.1", 4000);
  printSocket("::1", 5000);
  printSocket("2620:0:1cfe:face:b00c::3", 6000);

  return 0;
}