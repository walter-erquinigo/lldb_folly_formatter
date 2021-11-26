add_executable(concurrentlazy concurrentlazy.cpp)

target_link_libraries(concurrentlazy PRIVATE folly)

install(TARGETS concurrentlazy
	RUNTIME DESTINATION ${INSTALL_DIR})
