cmake_minimum_required(VERSION 3.1.3)
project(folly_example CXX)

set (CMAKE_EXPORT_COMPILE_COMMANDS ON)

set (CMAKE_CXX_STANDARD 14)
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -g")

set (BUILD_DIR "${CMAKE_SOURCE_DIR}/out")
set (INSTALL_DIR "${BUILD_DIR}/bin")

find_package(folly REQUIRED)

add_subdirectory(src)
