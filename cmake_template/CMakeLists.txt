cmake_minimum_required (VERSION 3.0.0)
project (MyProject)

# Set c++ standard, we must use c++11 or c++14
set (CMAKE_CXX_STANDARD 11)
set (CMAKE_CXX_STANDARD_REQUIRED ON)
set (CMAKE_BUILD_TYPE "Release")

# If ON, output compile details, used for GCC only
option (MAKE_VERBOSE "Print compile details, used for GCC only" ON)
if (MAKE_VERBOSE)
    set (CMAKE_VERBOSE_MAKEFILE ON)
endif ()

if (UNIX)
    # Set GCC macros and optimizers 
    message ("Platform is UNIX")
    add_definitions ("-D_GNU_SOURCE -D_REENTRANT -DNDEBUG -DPIC -D__USE_STRING_INLINES")
    add_definitions ("-D_GLIBCXX_USE_CXX11_ABI=1")
    add_link_options("-Wl,-rpath=.")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -m64 -Wall -fPIC -pthread")
    if (DEBUG)
        set (CMAKE_CXX_FLAGS    "${CMAKE_CXX_FLAGS} -gdwarf-3 -O0")
    else ()
        set (CMAKE_CXX_FLAGS    "${CMAKE_CXX_FLAGS} -g0 -O3 -mtune=intel -march=native")
    endif ()
elseif (WIN32)
    message ("Platform is Windows")
endif ()

message ("")
message ("CMAKE_CXX_STANDARD ${CMAKE_CXX_STANDARD}\n")
message ("CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS}\n")
message ("CMAKE_BUILD_TYPE ${CMAKE_BUILD_TYPE}\n")

# Set CMAKE_MODULE_PATH, so we can use submodule to find dependencies
set (CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

# Find boost library
find_package(Boost 1.58 REQUIRED)

# Find gflags glog and gperftools-tcmalloc 
find_package (GLOG REQUIRED)
message ("GLOG_FOUND        ${GLOG_FOUND}")
message ("GLOG_INCLUDE_DIR  ${GLOG_INCLUDE_DIR}")
message ("GLOG_LIBRARY      ${GLOG_LIBRARY}")

find_package (GFLAGS REQUIRED)
message ("GFLAGS_FOUND       ${GFLAGS_FOUND}")
message ("GFLAGS_INCLUDE_DIR ${GFLAGS_INCLUDE_DIR}")
message ("GFLAGS_LIBRARY     ${GFLAGS_LIBRARY}")

find_package (TCMALLOC REQUIRED)
message ("TCMALLOC_FOUND        ${TCMALLOC_FOUND}")
message ("TCMALLOC_INCLUDE_DIR  ${TCMALLOC_INCLUDE_DIR}")
message ("TCMALLOC_LIBRARY      ${TCMALLOC_LIBRARY}")

message ("")

# Set include directories
set (INCLUDE_DIR 
    "./include"
    "${GFLAGS_INCLUDE_DIR}"
    "${GLOG_INCLUDE_DIR}"
    "${TCMALLOC_INCLUDE_DIR}"
    "/opt/intel/mkl/include/"
)
include_directories (${INCLUDE_DIR})

message ("INCLUDE_DIR ${INCLUDE_DIR}\n")

get_filename_component(PROJECT_SOURCE_DIR ${PROJECT_SOURCE_DIR} REALPATH)
message ("PROJECT_SOURCE_DIR ${PROJECT_SOURCE_DIR}\n")

aux_source_directory (${PROJECT_SOURCE_DIR}/src SRC_MAIN)
message ("SRC_MAIN ${SRC_MAIN}")
message ("")

# Set static libs to link, be careful, static library linking must
# set before add_executable function !!!
link_libraries (${GFLAGS_LIBRARY} ${GLOG_LIBRARY} ${TCMALLOC_LIBRARY})

set (VER "linux.x64.1.0")

# Set release name and version
set (EXE_NAME MyProject.${VER})
add_executable (${EXE_NAME}  ${SRC_MAIN})
message("EXE_NAME ${EXE_NAME}")

# Add dynamic libraries to link with
message("HOME $ENV{HOME}")
target_link_directories (${EXE_NAME} PUBLIC /opt/intel/mkl/lib/intel64)
target_link_directories (${EXE_NAME} PUBLIC /opt/intel/lib/intel64)
target_link_directories (${EXE_NAME} PUBLIC $ENV{HOME}/mylibs)

target_link_libraries (${EXE_NAME} 
    -lboost_system
    -lboost_filesystem 
    -lm -lrt -ldl
)

message("")

