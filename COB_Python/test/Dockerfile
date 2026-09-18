# Reproduces the Nomad's interpreter: i686 + CPython 3.7, matching the
# cp37-cp37m-linux_i686 wheels it runs. Build context is COB_Python/.
#   docker build --platform linux/386 -f test/Dockerfile -t xippy-test .
#   docker run --rm -v "${PWD}:/app" xippy-test
FROM --platform=linux/386 python:3.7-slim

RUN pip install --no-cache-dir \
    "numpy==1.21.6" \
    pyserial \
    can4python

COPY xipppy/xipppy-0.16.2-cp37-cp37m-linux_i686.whl /tmp/
COPY tflite_runtime-2.5.0-cp37-cp37m-linux_i686.whl /tmp/

RUN pip install --no-cache-dir \
    /tmp/xipppy-0.16.2-cp37-cp37m-linux_i686.whl \
    /tmp/tflite_runtime-2.5.0-cp37-cp37m-linux_i686.whl

RUN mkdir -p /var/rppl/storage /usr/rppl
RUN mkdir -p /var/rppl/storage/logs

WORKDIR /app
CMD ["sh", "test/run_test.sh"]