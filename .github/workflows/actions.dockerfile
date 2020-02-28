FROM balabit/syslog-ng-devshell:latest

RUN apt-get update && apt-get install -y python3-pip snmptrapd libbson-1.0-0=1.15.0-1 libbson-dev=1.15.0-1 libmongoc-1.0-0=1.15.0-1 libmongoc-dev=1.15.0-1
