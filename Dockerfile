FROM alpine:3.16.1

RUN apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools prometheus_client requests pyyaml


LABEL maintainer="Elias Ghali"
LABEL git.url="https://github.com/elghali"

COPY nfs_exporter_py.py /etc/nfs_exporter_py.py
EXPOSE 9469

CMD ["python3", "/etc/nfs_exporter_py.py"]

# docker build --no-cache --rm -t nfs_exporter_py:1.0 .
# docker run -it -v "/home/elghali:/home/elghali" -p 9469:9469 -d nfs_exporter_py:1.0