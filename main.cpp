#include <iostream>
#include <string>
#include <folly/FBString.h>

int main() {
    std::cout << folly::fbstring(std::string(10, 'a')).data() << std::endl;
    return 0;
}
