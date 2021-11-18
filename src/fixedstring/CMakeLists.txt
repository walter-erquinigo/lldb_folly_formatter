add_executable(fixedstring fixedstring.cpp)

target_link_libraries(fixedstring PRIVATE folly)

install(TARGETS fixedstring
	RUNTIME DESTINATION ${INSTALL_DIR})
