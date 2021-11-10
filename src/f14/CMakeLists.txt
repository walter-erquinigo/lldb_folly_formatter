add_executable(f14 f14.cpp)

target_link_libraries(f14 PRIVATE folly)

install(TARGETS f14
	RUNTIME DESTINATION ${INSTALL_DIR})
