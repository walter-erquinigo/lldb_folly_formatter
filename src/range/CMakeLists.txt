add_executable(range range.cpp)

target_link_libraries(range PRIVATE folly)

install(TARGETS range
	RUNTIME DESTINATION ${INSTALL_DIR})
