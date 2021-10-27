# lldb_folly_formatter
LLDB Data formatters for folly 

# Set up

You need g++, cmake, ninja and a prebuilt version of folly. For example, on Fedora you should be able to do this by executing

```
sudo dnf groupinstall "Development Tools" -y
sudo dnf gcc-c++ install folly-static cmake ninja-build
```

# How to build

```
mkdir build && cd build
cmake -G Ninja ..
ninja all
```
