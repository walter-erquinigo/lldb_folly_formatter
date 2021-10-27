add_executable(address address.cpp)

target_link_libraries(address PRIVATE folly)

install(TARGETS address
	RUNTIME DESTINATION ${INSTALL_DIR})
