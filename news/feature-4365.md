`ebpf()` plugin and udp packet balancer: a new ebpf() plugin was added which
leverages the kernel's eBPF infrastructure to improve performance and
scalability of syslog-ng.  The first ebpf based solution improves
performance when a single (or very few) senders generate most of the inbound
UDP traffic that syslog-ng needs to process.  Normally, the kernel
distributes load between so-reuseport sockets by keeping each flow (e.g.
same source/dest ip/port) in its dedicated receiver.  This fails to balance
the sockets properly if only a few senders are responsible for most of the
load. ebpf(reuseport()) will replace the original kernel algorithm with an
alternative that changes the algorithm, so individual packets will be
assigned to one of the sockets randomly, thereby producing a more uniform
load.

Example:

source s_udp {
        udp(so-reuseport(1) port(2000) persist-name("udp1")
                ebpf(reuseport(sockets(4)))
        );
        udp(so-reuseport(1) port(2000) persist-name("udp2"));
        udp(so-reuseport(1) port(2000) persist-name("udp3"));
        udp(so-reuseport(1) port(2000) persist-name("udp4"));
};
