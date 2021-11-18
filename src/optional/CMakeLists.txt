add_executable(optional optional.cpp)

target_link_libraries(optional PRIVATE folly)

install(TARGETS optional
	RUNTIME DESTINATION ${INSTALL_DIR})
