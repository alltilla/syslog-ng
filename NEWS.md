3.99.99
=======

## Highlights

<Fill this block manually from the blocks below>

## Features

  * `syslog-parser()`: allow comma (e.g. ',') to separate the seconds and the fraction of a
    second part as some devices use that character. This change applies to both
    to syslog-parser() and the builtin syslog parsing functionality of network
    source drivers (e.g. udp(), tcp(), network() and syslog()).
    ([#3949](https://github.com/syslog-ng/syslog-ng/pull/3949))

## Bugfixes

  * `http()` and other threaded destinations: fix $SEQNUM processing so that
    only local messages get an associated $SEQNUM, just like normal
    syslog()-like destinations.  This avoids a [meta sequenceId="XXX"] SD-PARAM
    being added to $SDATA for non-local messages.
    ([#3928](https://github.com/syslog-ng/syslog-ng/pull/3928))

## Other changes

  * `java()/python() destinations`: the $SEQNUM macro (and "seqnum" attribute in
    Python) was erroneously for both local and non-local logs, while it should
    have had a value only in case of local logs to match RFC5424 behavior
    (section 7.3.1).  This bug is now fixed, but that means that all non-local
    logs will have $SEQNUM set to zero from this version on, e.g.  the $SEQNUM
    macro would expand to an string, to match the syslog() driver behaviour.
    ([#3928](https://github.com/syslog-ng/syslog-ng/pull/3928))

## Credits

syslog-ng is developed as a community project, and as such it relies
on volunteers, to do the work necessarily to produce syslog-ng.

Reporting bugs, testing changes, writing code or simply providing
feedback are all important contributions, so please if you are a user
of syslog-ng, contribute.

We would like to thank the following people for their contribution:

, Andras Mitzki, Attila Szakacs, Balazs Scheidler, Gabor Nagy,
László Várady, Parrag Szilárd, Peter Kokai, Zoltan Pallagi
