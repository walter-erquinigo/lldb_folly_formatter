#include <iostream>
#include <folly/IPAddress.h>

using namespace folly;

void printIP(std::string ip_str) {
  IPAddress ip(ip_str);
  std::cout << ip << std::endl;
}

int main() {
  // IPv4 addresses
  printIP("10.0.0.10");
  printIP("192.168.0.1");

  // IPv6 Addresses
  printIP("::1");
  printIP("2620:0:1cfe:face:b00c::3");

  return 0;
}