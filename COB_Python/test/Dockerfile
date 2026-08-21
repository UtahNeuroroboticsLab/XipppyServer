# Reproduces the Nomad's interpreter: i686 + CPython 3.7, matching the
# cp37-cp37m-linux_i686 wheels it runs. Build context is COB_Python/.
#   docker build --platform linux/386 -f test/Dockerfile -t xippy-test .
#   docker run --rm -v "${PWD}:/app" xippy-test
FROM --platform=linux/386 python:3.7-slim

# numpy pinned: last series with 32-bit linux wheels for cp37. Unpinned, pip
# tries to build from source and slim has no compiler.
RUN pip install --no-cache-dir "numpy==1.21.6" pyserial can4python

COPY xipppy/xipppy-0.16.2-cp37-cp37m-linux_i686.whl /tmp/
RUN pip install --no-cache-dir /tmp/xipppy-0.16.2-cp37-cp37m-linux_i686.whl

# storage root exists, logs/ deliberately does not - exercises the makedirs branch
RUN mkdir -p /var/rppl/storage
RUN mkdir -p /usr/rppl

WORKDIR /app
CMD ["sh", "test/run_test.sh"]
