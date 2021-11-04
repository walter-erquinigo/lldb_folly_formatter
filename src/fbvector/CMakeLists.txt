add_executable(fbvector fbvector.cpp)

target_link_libraries(fbvector PRIVATE folly)

install(TARGETS fbvector
	RUNTIME DESTINATION ${INSTALL_DIR})
