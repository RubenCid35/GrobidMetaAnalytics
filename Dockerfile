
FROM ubuntu:latest

MAINTAINER rubencid001@gmail.com

COPY main.sh main.sh
RUN chmod +x main.sh

ENTRYPOINT "./main.sh"