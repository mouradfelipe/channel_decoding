cmake_minimum_required(VERSION 3.10)


project(labvariacao1)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

file(GLOB_RECURSE PCG_SRC ${CMAKE_SOURCE_DIR}/pcg-c-0.94/include/*.h ${CMAKE_SOURCE_DIR}/pcg-c-0.94/src/*.c)
add_library(pcg ${PCG_SRC})
target_include_directories(pcg PUBLIC ${CMAKE_SOURCE_DIR}/pcg-c-0.94/include)

#tem que muda aqui pra compilar com M diferente
add_definitions(-DM3 -DnumIter=50)

add_executable(labvariacao1 pcg_variants.h labvariacao1.c)
target_include_directories(labvariacao1 PUBLIC ${CMAKE_SOURCE_DIR})
target_link_libraries(labvariacao1 PUBLIC pcg)
