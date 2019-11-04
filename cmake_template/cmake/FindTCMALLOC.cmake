message ("\nUsing FindTCMALLOC.cmake to find gperftools(tcmalloc) library")

find_path (TCMALLOC_INCLUDE_DIR tcmalloc.h 
    /usr/local/include/gperftools
    /usr/include/gperftools
    /usr/local/include
    /usr/include
)

find_library (TCMALLOC_LIBRARY libtcmalloc_minimal.a
    /usr/local/lib
    /usr/lib
)

if (TCMALLOC_INCLUDE_DIR AND TCMALLOC_LIBRARY)
    set (TCMALLOC_FOUND true)
endif ()

