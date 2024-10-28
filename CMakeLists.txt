cmake_minimum_required(VERSION 3.15)

project(uklatn LANGUAGES C)
include(CTest)

find_package(ICU REQUIRED COMPONENTS uc i18n)

add_library(uklatn c/uklatn.c)
target_include_directories(uklatn PUBLIC c/include ${ICU_INCLUDE_DIRS})
target_link_libraries(uklatn ${ICU_LIBRARIES})

add_executable(testuklatn c/testuklatn.c)
target_link_libraries(testuklatn uklatn)
add_test(NAME test COMMAND testuklatn)
