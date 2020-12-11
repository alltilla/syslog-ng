99.69.1
=======

## Highlights

<Fill this block manually from the blocks below>

## Bugfixes

 * `loggen`: fix undefined timeout while connecting to network sources (`glib < 2.32`)
   
   When compiling syslog-ng with old glib versions (< 2.32), `loggen` could fail due a timeout bug.
   This has been fixed.
   ([#3504](https://github.com/syslog-ng/syslog-ng/pull/3504))

## Packaging

 * configure: added new --enable-manpages-install option along with the
   existing --enable-manpages. The new option would install pre-existing
   manpages even without the DocBook tools installed.
   ([#3493](https://github.com/syslog-ng/syslog-ng/pull/3493))

## Credits

syslog-ng is developed as a community project, and as such it relies
on volunteers, to do the work necessarily to produce syslog-ng.

Reporting bugs, testing changes, writing code or simply providing
feedback are all important contributions, so please if you are a user
of syslog-ng, contribute.

We would like to thank the following people for their contribution:

, Andras Mitzki, Antal Nemes, Attila Szakacs, Balazs Scheidler,
Gabor Nagy, Laszlo Budai, Laszlo Szemere, László Várady,
Norbert Takacs, Zoltan Pallagi
