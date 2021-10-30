add_executable(socketaddress socketaddress.cpp)

target_link_libraries(socketaddress PRIVATE folly)

install(TARGETS socketaddress
	RUNTIME DESTINATION ${INSTALL_DIR})
