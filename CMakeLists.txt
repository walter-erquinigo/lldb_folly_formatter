cmake_minimum_required(VERSION 3.1.3)
project(folly_example CXX)

find_package(folly REQUIRED)

set (CMAKE_CXX_STANDARD 14)
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -g")

add_subdirectory(src)
