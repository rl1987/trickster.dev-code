FROM debian:11

RUN apt-get update && apt-get install -y python3 python3-pip hugo tor
RUN pip3 install stem

ADD . /trickster.dev
WORKDIR /trickster.dev

ENTRYPOINT bash -c "tor --RunAsDaemon 1 --ControlPort 9051 && python3 run_onion_service.py"

