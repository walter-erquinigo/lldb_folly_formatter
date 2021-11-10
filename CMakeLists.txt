cmake_minimum_required(VERSION 3.1.3)
project(folly_example CXX)

set (CMAKE_EXPORT_COMPILE_COMMANDS ON)

sET (CMAKE_C_COMPILER "/usr/bin/clang")
sET (CMAKE_CXX_COMPILER "/usr/bin/clang++")
set (CMAKE_CXX_STANDARD 14)
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -g2")

set (BUILD_DIR "${CMAKE_SOURCE_DIR}/out")
set (INSTALL_DIR "${BUILD_DIR}/bin")

find_package(folly REQUIRED)

add_subdirectory(src)
