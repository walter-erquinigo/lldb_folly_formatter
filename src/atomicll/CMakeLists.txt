add_executable(atomicll atomicll.cpp)

target_link_libraries(atomicll PRIVATE folly)

install(TARGETS atomicll
	RUNTIME DESTINATION ${INSTALL_DIR})
