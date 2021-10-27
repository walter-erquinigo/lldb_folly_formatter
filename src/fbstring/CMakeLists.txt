add_executable(fbstring fbstring.cpp)

target_link_libraries(fbstring PRIVATE folly)

install(TARGETS fbstring
	RUNTIME DESTINATION ${INSTALL_DIR})
