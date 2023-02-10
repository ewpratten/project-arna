FROM debian:11-slim

# Install runtime dependencies
RUN apt-get update -y
RUN apt-get install -y bird2
RUN apt-get install -y python3
RUN apt-get install -y iproute2

# Install Caddy
RUN apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl
RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
RUN apt-get -y update
RUN apt-get install -y caddy

# Set up directories for bird
RUN mkdir /run/bird

# Copy the entrypoint script
COPY ./scripts/entrypoint.py /usr/local/bin/entrypoint.py
RUN chmod +x /usr/local/bin/entrypoint.py

# Copy configuration files
COPY ./configs/bird/bird.conf /etc/arna/bird/bird.conf
COPY ./configs/caddy/Caddyfile /etc/caddy/Caddyfile

# Run everything 
ENTRYPOINT ["/usr/local/bin/entrypoint.py"]