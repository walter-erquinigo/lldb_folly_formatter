#include <iostream>
#include <string>
#include <folly/IPAddress.h>

using namespace folly;

void printIP4(std::string ip4_str) {
  IPAddress ip4(ip4_str);
  std::cout << ip4 << std::endl;
}

void printIP6(std::string ip6_str) {
  IPAddress ip6(ip6_str);
  std::cout << ip6 << std::endl;
}

int main() {
  printIP4("10.0.0.10");
  printIP4("192.168.0.1");

  printIP6("::1");
  printIP6("2620:0:1cfe:face:b00c::3");

  return 0;
}