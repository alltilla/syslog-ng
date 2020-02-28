FROM balabit/syslog-ng-devshell:latest

RUN apt-get update && apt-get install -y snmptrapd python3-pep8
#RUN wget https://bootstrap.pypa.io/get-pip.py && python2 get-pip.py

