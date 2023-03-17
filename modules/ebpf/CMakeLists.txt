module_switch(ENABLE_EBPF "Enable ebpf module (requires ebpf toolchain)" LIBBPF_FOUND)

if (NOT ENABLE_EBPF)
  return()
endif()

set(BPF_CC clang)
set(LIBBPF_INCLUDE /usr/include)
set(BPF_CFLAGS -nostdinc -isystem `${BPF_CC} -print-file-name=include` -target bpf -I${CMAKE_CURRENT_BINARY_DIR} -I${LIBBPF_INCLUDE} -fPIC -O2 -g)
set(BPFTOOL bpftool)

add_custom_command(OUTPUT vmlinux.h
                   COMMAND ${BPFTOOL} btf dump file /sys/kernel/btf/vmlinux format c >vmlinux.h)

add_custom_command(OUTPUT random.skel.c
                   COMMAND ${BPFTOOL} gen skeleton random.kern.o > random.skel.c
                   DEPENDS random.kern.o)

add_custom_command(OUTPUT random.kern.o
                   COMMAND ${BPF_CC} ${BPF_CFLAGS} -c ${CMAKE_CURRENT_SOURCE_DIR}/random.kern.c -o random.kern.o
                   DEPENDS random.kern.c vmlinux.h)


set(EBPF_SOURCES
    ebpf-parser.h
    ebpf-reuseport.h
    ebpf-reuseport.c
    ebpf-plugin.c
    ebpf-parser.c
    random.skel.c
)

add_module(
  TARGET ebpf
  GRAMMAR ebpf-grammar
  INCLUDES ${PROJECT_SOURCE_DIR}
  SOURCES ${EBPF_SOURCES}
)
