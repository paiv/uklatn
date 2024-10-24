cmake_minimum_required(VERSION 3.15)

find_package(ICU COMPONENTS uc i18n)

project(uklatn LANGUAGES C)
include(CTest)

add_library(uklatn c/uklatn.c)
target_include_directories(uklatn PUBLIC c/include ${ICU_INCLUDE_DIRS})
target_link_libraries(uklatn ${ICU_LIBRARIES})

add_executable(testuklatn c/testuklatn.c)
target_link_libraries(testuklatn uklatn)
add_test(NAME test COMMAND testuklatn)
