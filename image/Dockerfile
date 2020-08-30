################################################################################
# Base image
################################################################################
FROM python:3.8-slim AS base

# Make sure we don't get notifications we can't answer during building.
ENV DEBIAN_FRONTEND noninteractive

#
# Default config
#
RUN groupadd -g 9999 skwr \
    && useradd -m -r -u 9999 -g skwr skwr


#
# Add module and packages
#
RUN pip3 install sendgrid



################################################################################
# Development image
################################################################################
FROM base AS dev
RUN apt-get update \
    && apt-get install -y git procps \
    && apt-get clean \
    && pip install black mypy pylint
USER skwr



################################################################################
# Production image
################################################################################
FROM base AS prod
#
# Default skwr config
#
COPY module /opt/module
RUN rm -rf /home/skwr; chmod +x /opt/module/bin/*.sh
ENV PATH="/opt/module/bin:${PATH}"
ENTRYPOINT ["run.sh"]
HEALTHCHECK --start-period=10s --interval=30s --timeout=5s --retries=3 \
    CMD healthcheck.sh || exit 1
USER skwr
