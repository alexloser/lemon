message ("\nUsing FindGFLAGS.cmake to find gflags library")

find_path (GFLAGS_INCLUDE_DIR gflags.h 
    /usr/local/include/gflags
    /usr/include/gflags
    /usr/local/include
    /usr/include
)

find_library (GFLAGS_LIBRARY libgflags.a
    /usr/local/lib
    /usr/lib
)

if (GFLAGS_INCLUDE_DIR AND GFLAGS_LIBRARY)
    set (GFLAGS_FOUND true)
endif ()

