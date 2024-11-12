# Use the official Prometheus image as a base image
FROM prom/prometheus:latest

# Copy the prometheus.yml file into the container
COPY prometheus.yml /etc/prometheus/prometheus.yml

# Expose port 9090 (default Prometheus port)
EXPOSE 9090

# Run Prometheus
ENTRYPOINT [ "/bin/prometheus" ]
CMD [ "--config.file=/etc/prometheus/prometheus.yml", "--storage.tsdb.path=/prometheus", "--web.console.libraries=/usr/share/prometheus/console_libraries", "--web.console.templates=/usr/share/prometheus/consoles" ]