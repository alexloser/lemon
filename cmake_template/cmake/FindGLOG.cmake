message ("\nUsing FindGLOG.cmake to find glog library")

find_path (GLOG_INCLUDE_DIR logging.h
    /usr/local/include/glog
    /usr/include/glog
    /usr/local/include
    /usr/include
)

find_library (GLOG_LIBRARY libglog.a
    /usr/local/lib
    /usr/lib
)

if (GLOG_INCLUDE_DIR AND GLOG_LIBRARY)
    set (GLOG_FOUND true)
endif ()

