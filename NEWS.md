4.5.111
=======

## Highlights

<Fill this block manually from the blocks below>

## Features

  * `http()`: Added support for using templates in the `url()` option.

    In syslog-ng a template can only be resolved on a single message, as the same
    template might have different resolutions on different messages. A http batch
    consists of multiple messages, so it is not trivial to decide which message should
    be used for the resolution.

    When batching is enabled and multiple workers are configured it is important to
    only batch messages which generate identical URLs. In this scenario one must set
    the `worker-partition-key()` option with a template that contains all the templates
    used in the `url()` option, otherwise messages will be mixed.

    For security reasons, all the templated contents in the `url()` option are getting
    URL encoded automatically. Also the following parts of the url cannot be templated:
      * scheme
      * host
      * port
      * user
      * password
    ([#4663](https://github.com/syslog-ng/syslog-ng/pull/4663))

  * `cloud-auth()`: Added a new plugin for drivers, which implements different cloud related authentications.

    Currently the only supported authentication is [GCP's Service Account](https://cloud.google.com/iam/docs/service-account-overview) for the `http()` destination.

    Example config:
    ```
    http(
      cloud-auth(
        gcp(
          service-account(
            key("/path/to/service-account-key.json")
            audience("https://pubsub.googleapis.com/google.pubsub.v1.Publisher")
          )
        )
      )
    );
    ```
    ([#4651](https://github.com/syslog-ng/syslog-ng/pull/4651))

  * `network()` and `syslog()` drivers: Added `ignore-validity-period` as a new flag to `ssl-options()`.

    By specifying `ignore-validity-period`, you can ignore the validity periods
    of certificates during the certificate validation process.
    ([#4642](https://github.com/syslog-ng/syslog-ng/pull/4642))

  * `tls()` in `udp()`/`tcp()`/`network()` and `syslog()` drivers: add support
    for a new `http()` compatible ssl-version() option. This makes the TLS
    related options for http() and other syslog-like drivers more similar. This
    requires OpenSSL 1.1.0.
    ([#4682](https://github.com/syslog-ng/syslog-ng/pull/4682))

  * #### Sending messages to Google Pub/Sub

    The `google-pubsub()` destination feeds Google Pub/Sub via the [HTTP REST API](https://cloud.google.com/pubsub/docs/reference/rest/v1/projects.topics/publish).

    Example config:
    ```
    google-pubsub(
      project("syslog-ng-project")
      topic("syslog-ng-topic")
      auth(
        service-account(
          key("/path/to/service-account-key.json")
        )
      )
    );
    ```

    See the [Google Pub/Sub documentation](https://cloud.google.com/pubsub/docs/building-pubsub-messaging-system) to learn more about configuring a service account.
    ([#4651](https://github.com/syslog-ng/syslog-ng/pull/4651))

  * `csv-parser()`: allow parsing the extracted values into matches ($1, $2, $3 ...)
    by omitting the columns() parameter, which normally specifies the column
    names.
    ([#4678](https://github.com/syslog-ng/syslog-ng/pull/4678))

  * `--check-startup`: a new command line option for syslog-ng along with the
    existing `--syntax-only`. This new option will do a complete configuration
    initialization and then exit with exit code indicating the result. Since
    this also initializes things like network listeners, it will probably _not_
    work when there is another syslog-ng instance running in the background. The
    recommended use of this option is a dedicated config check container, as
    explained in #4592.
    ([#4646](https://github.com/syslog-ng/syslog-ng/pull/4646))


## Bugfixes

  * `loki()`: fixed mixing non-related label values
    ([#4713](https://github.com/syslog-ng/syslog-ng/pull/4713))

  * `flags()` argument to various drivers: fix a potential crash in case a flag with at least 32 characters is used.
    No such flag is defined by syslog-ng, so the only way to trigger the crash is to use an invalid configuration file.
    ([#4689](https://github.com/syslog-ng/syslog-ng/pull/4689))

  * type hinting: Parsing and casting fractions are now done locale independently.
    ([#4702](https://github.com/syslog-ng/syslog-ng/pull/4702))

  * `metrics-probe()`: Fixed a crash.

    This crash occurred when a `metrics-probe()` instance was used in multiple source threads,
    like a `network()` source with multiple connections.
    ([#4685](https://github.com/syslog-ng/syslog-ng/pull/4685))

  * `s3`: Fixed an ImportError.

    `ImportError: cannot import name 'SharedBool' from 'syslogng.modules.s3.s3_object'`
    ([#4700](https://github.com/syslog-ng/syslog-ng/pull/4700))


## Other changes

  * `loki()`: The `timestamp()` option now supports quoted strings.

    The valid values are the following, with or without quotes, case insensitive:
      * "current"
      * "received"
      * "msg"
    ([#4688](https://github.com/syslog-ng/syslog-ng/pull/4688))

  * templates: The `template-escape()` option now only escapes the top-level template function.

    Before syslog-ng 4.5.0 if you had embedded template functions, the `template-escape(yes)` setting
    escaped the output of each template function, so the parent template function received an
    already escaped string. This was never the intention of the `template-escape()` option.

    Although this is a breaking change, we do not except anyone having a config that is affected.
    If you have such a config, make sure to follow-up this change. If you need help with it, feel
    free to open an issue or discussion on GitHub, or contact us on the Axoflow Discord server.
    ([#4666](https://github.com/syslog-ng/syslog-ng/pull/4666))

  * `rate-limit()`: Renamed the `template()` option to `key()`, which better communicates the intention.
    ([#4679](https://github.com/syslog-ng/syslog-ng/pull/4679))


## Credits

syslog-ng is developed as a community project, and as such it relies
on volunteers, to do the work necessarily to produce syslog-ng.

Reporting bugs, testing changes, writing code or simply providing
feedback are all important contributions, so please if you are a user
of syslog-ng, contribute.

We would like to thank the following people for their contribution:

Attila Szakacs, Balazs Scheidler, Cedric Arickx, Fabrice Fontaine,
Hofi, László Várady, Szilard Parrag, dependabot[bot], yashmathne
