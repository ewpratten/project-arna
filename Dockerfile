FROM debian:11-slim

# Install runtime dependencies
RUN apt-get update -y
RUN apt-get install -y bird2
RUN apt-get install -y python3
RUN apt-get install -y iproute2
RUN apt-get install -y default-jre

# Install Caddy
RUN apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl
RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
RUN apt-get -y update
RUN apt-get install -y caddy

# # Install APRSC
# RUN echo "deb http://aprsc-dist.he.fi/aprsc/apt bullseye main" > /etc/apt/sources.list.d/aprsc.list
# RUN gpg --keyserver keyserver.ubuntu.com --recv C51AA22389B5B74C3896EF3CA72A581E657A2B8D
# RUN gpg --export C51AA22389B5B74C3896EF3CA72A581E657A2B8D | apt-key add -
# RUN apt-get -y update
# RUN apt-get install -y aprsc
# RUN mkdir /tmp/aprs_data

# # Link /web to /opt/aprsc/web
# RUN ln -s /opt/aprsc/web /web

# Set up directories for bird
RUN mkdir /run/bird

# Copy the echolink JAR
COPY ./scripts/EchoLinkProxy.jar /usr/local/bin/EchoLinkProxy.jar

# Copy the entrypoint script
COPY ./scripts/entrypoint.py /usr/local/bin/entrypoint.py
RUN chmod +x /usr/local/bin/entrypoint.py

# Copy configuration files
COPY ./configs/bird/bird.conf /etc/arna/bird/bird.conf
COPY ./configs/caddy/Caddyfile /etc/caddy/Caddyfile
COPY ./configs/aprsc/aprsc.conf /etc/aprsc/aprsc.conf
COPY ./configs/echolink/ELProxy-01.conf /etc/arna/echolink/ELProxy-01.conf
COPY ./configs/echolink/ELProxy-02.conf /etc/arna/echolink/ELProxy-02.conf
COPY ./configs/echolink/ELProxy-03.conf /etc/arna/echolink/ELProxy-03.conf

# Run everything 
ENTRYPOINT ["/usr/local/bin/entrypoint.py"]