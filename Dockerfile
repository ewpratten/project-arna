FROM debian:11-slim

# Install runtime dependencies
RUN apt-get update -y
RUN apt-get install -y bird2
RUN apt-get install -y python3
RUN apt-get install -y iproute2

# Set up directories for bird
RUN mkdir /run/bird

# Copy the entrypoint script
COPY ./scripts/entrypoint.py /usr/local/bin/entrypoint.py
RUN chmod +x /usr/local/bin/entrypoint.py

# Copy configuration files
COPY ./configs/bird/bird.conf /etc/arna/bird/bird.conf

# Run everything 
ENTRYPOINT ["/usr/local/bin/entrypoint.py"]