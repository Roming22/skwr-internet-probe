FROM   balenalib/raspberrypi3

# Make sure we don't get notifications we can't answer during building.
ENV    DEBIAN_FRONTEND noninteractive

#
# Default skwr config
#
RUN groupadd -g 9999 skwr \
 && useradd -r -u 9999 -g skwr skwr
ENV PATH="/opt/module/bin:$PATH"
ENTRYPOINT ["run.sh"]
HEALTHCHECK --start-period=10s --interval=30s --timeout=5s --retries=3 \
    CMD healthcheck.sh || exit 1

#
# Add module and packages
#
RUN apt-get update \
 && apt-get install -y python3 \
 && apt-get clean

# Add module
COPY module /opt/module
RUN chmod +x /opt/module/bin/*.sh

USER skwr

