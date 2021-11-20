add_executable(sbyteset sbyteset.cpp)

target_link_libraries(sbyteset PRIVATE folly)

install(TARGETS sbyteset
	RUNTIME DESTINATION ${INSTALL_DIR})
