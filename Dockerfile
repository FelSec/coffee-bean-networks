FROM python:3.11.8-slim-bullseye

LABEL description="A simple environment designed to practice and develop N1QL (SQL++) injection techniques and tooling."
LABEL verion="1.0.0"

WORKDIR /CBN
COPY requirements.txt requirements.txt
RUN pip install -r /CBN/requirements.txt
COPY ./app/ /CBN/app/
COPY ./note/ /CBN/note/
COPY cbn.py .
RUN chmod +x /CBN/cbn.py
COPY noteapi.py .
RUN chmod +x /CBN/noteapi.py
COPY .env .
COPY ./data/ /CBN/data/

RUN apt-get -y update
RUN apt-get -y install curl

RUN curl -O https://packages.couchbase.com/releases/couchbase-release/couchbase-release-1.0-noarch.deb
RUN dpkg -i ./couchbase-release-1.0-noarch.deb
RUN apt-get -y update
RUN apt-get -y install couchbase-server
RUN rm ./couchbase-release-1.0-noarch.deb

COPY cbn-db-init.sh .
RUN chmod +x cbn-db-init.sh

COPy ./scripts/cbn-db-loaddata.sh .
RUN chmod +x cbn-db-loaddata.sh

COPY ./scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 5000