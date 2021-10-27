cmake_minimum_required(VERSION 3.1.3)
project(folly_example CXX)

find_package(folly REQUIRED)

add_executable(${PROJECT_NAME} main.cpp)

set_target_properties(${PROJECT_NAME} PROPERTIES CXX_STANDARD 14)
