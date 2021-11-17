classname=$1

mkdir -p src/$classname
cd src/$classname
touch __init__.py ${classname}_formatter.py test_${classname}.py

cat << EOF > ${classname}.cpp
#include <iostream>

int main() {
  return 0;
}
EOF

cat << EOF > CMakeLists.txt
add_executable(${classname} ${classname}.cpp)

target_link_libraries(${classname} PRIVATE folly)

install(TARGETS ${classname}
	RUNTIME DESTINATION \${INSTALL_DIR})
EOF

cd ..
echo "add_subdirectory(${classname})" >> CMakeLists.txt
