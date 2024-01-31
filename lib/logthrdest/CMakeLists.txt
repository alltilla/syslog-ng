set(LOGTHRDEST_HEADERS
    logthrdest/logthrdestdrv.h
    logthrdest/exponential-backoff.h
    PARENT_SCOPE)

set(LOGTHRDEST_SOURCES
    logthrdest/logthrdestdrv.c
    logthrdest/exponential-backoff.c
    PARENT_SCOPE)

add_test_subdirectory(tests)
