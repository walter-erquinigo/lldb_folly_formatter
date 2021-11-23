add_executable(lazy lazy.cpp)

target_link_libraries(lazy PRIVATE folly)

install(TARGETS lazy
	RUNTIME DESTINATION ${INSTALL_DIR})
