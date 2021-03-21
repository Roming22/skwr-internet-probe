FROM   alpine

#
# Default skwr config
#
RUN addgroup -g 9999 skwr \
    && adduser -G skwr -S --shell /bin/bash -u 9999 skwr
ENV PATH="/opt/module/bin:$PATH"
ENTRYPOINT ["run.py"]
HEALTHCHECK --start-period=10s --interval=30s --timeout=5s --retries=3 \
    CMD healthcheck.sh || exit 1

#
# Add module and packages
#
RUN apk add bash python3 py3-pip \
    && pip3 install sendgrid

# Add module
COPY module /opt/module
RUN cd /opt/module; \
    chmod +x bin/*.py bin/*.sh; \
    mkdir -p data; \
    chmod a+rwx data

USER skwr

