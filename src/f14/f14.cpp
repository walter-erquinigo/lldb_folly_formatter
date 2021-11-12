#include <iostream>
#include <folly/container/F14Map.h>
#include <folly/container/F14Set.h>

using namespace folly;
using namespace std;

int main() {
  F14FastMap<int, string> fmap;
  fmap.insert(pair<int, string>(0, string("One")));
  fmap.insert(pair<int, string>(0, string("Two")));

  F14FastSet<string> fset;
  fset.insert({
    string("One"),
    string("Two"),
    string("Three"),
  });

  F14NodeMap<string, string> nmap;
  nmap.insert(pair<string, string>("Key", "Value"));

  F14NodeSet<string> nset;
  nset.insert(string("Value"));

  F14ValueSet<float> vset;

  return 0;
}