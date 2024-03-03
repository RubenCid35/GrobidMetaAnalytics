
FROM python:3.11-buster
MAINTAINER rubencid001@gmail.com

WORKDIR /home

COPY report_generator.py .
COPY config/python/docker_config.json ./config/python/config.json
COPY requirements.txt .

RUN pip install -r requirements.txt

RUN git clone https://github.com/kermitt2/grobid_client_python && cd grobid_client_python && python setup.py install
RUN cd ..

CMD ["python", "-u", "report_generator.py"]