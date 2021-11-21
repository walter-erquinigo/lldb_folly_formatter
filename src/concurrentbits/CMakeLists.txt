add_executable(concurrentbits concurrentbits.cpp)

target_link_libraries(concurrentbits PRIVATE folly)

install(TARGETS concurrentbits
	RUNTIME DESTINATION ${INSTALL_DIR})
