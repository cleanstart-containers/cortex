FROM cleanstart/cortex:latest-dev

USER root

# Create all necessary directories including alertmanager
RUN mkdir -p /tmp/cortex-data \
             /tmp/cortex-tsdb \
             /tmp/cortex-compactor \
             /tmp/cortex-rules \
             /tmp/cortex-alertmanager \
             /tmp/cortex-sync

# Copy config
COPY cortex-config.yaml /etc/cortex/config.yaml

EXPOSE 9009 9095

ENTRYPOINT ["cortex"]
CMD ["-config.file=/etc/cortex/config.yaml"]