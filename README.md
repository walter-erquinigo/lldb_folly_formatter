# lldb_folly_formatter
LLDB Data formatters for folly 

# Set up

You need g++, cmake, ninja and a prebuilt version of folly. For example, on Fedora you should be able to do this by executing

```
sudo dnf groupinstall "Development Tools" -y
sudo dnf install clang folly-static cmake ninja-build
```

Finally, you need lldb, which you can install from an existing package or build it yourself.

```
sudo dnf install lldb
```

# How to build

```
./build.sh
```

The produced artifacts will be in the `./out/bin` folder. This folder can't be changed as the test framework requires it to be fixed.

# How to run the tests

```
./run_tests.sh
```

# How to use a formatter

For example, let's pick the fbstring formatter.

```
cd <repo_root>
lldb ./build/src/fbstring/fbstring_test 
```

Now we are inside lldb's cli. Let's run the program until line 7, where the variable `fbstr` is defined.

```
(lldb) b 7     # this sets a breakpoint at line 7
(lldb) r       # this run the program
```

Now let's print the variable

```
(lldb) p fbstr
```

Which gives us as output

```
(folly::fbstring) $0 = {
  store_ = {
     = {
      bytes_ = "aaaaaaaaaa"
      small_ = "aaaaaaaaaa"
      ml_ = (data_ = "", size_ = 24929, capacity_ = 936889459981410112)
    }
  }
}
```

Lots of gibberish, right?

Now let's add the formatter and reprint the variable

```
(lldb) command script import ./src/fbstring/fbstring_formatter.py
(lldb) p fbstr
```

Which prints

```
(folly::fbstring) $0 = (folly::fbstring) "aaaaaaaaaa"
```

Nice, right? This is exactly what the user expects to see.



