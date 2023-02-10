#! /usr/bin/env python3
import os
import subprocess

from pathlib import Path

# Variables that must be passed through to config files
CONFIG_ENV_PASSTHROUGH_KEYS = ["PEER_ASN", "PEER_IP", "PEER_NAME", "PEER_UID"]

# Location of configs that need substitution
RAW_CONFIGS_ROOT = Path("/etc/arna")


def copy_config_with_env_vars(source: Path, dest: Path):
    print(f"Copying {source} to {dest} with environment variables set.")

    # Read the source config
    with open(source, "r") as f:
        config = f.read()

    # Substitute in the environment variables
    for key in CONFIG_ENV_PASSTHROUGH_KEYS:
        value = os.environ.get(key)
        if not value:
            raise RuntimeError(f"Environment variable {key} is not set")
        config = config.replace(f"${{{key.upper()}}}", value)

    # Write the config to the destination
    with open(dest, "w") as f:
        f.write(config)


def main():

    # Configure networking
    print("Creating dummy network interface")
    subprocess.run(["ip", "link", "add", "arnaLoop", "type", "dummy"])
    subprocess.run(["ip", "addr", "add", "44.31.119.1/24", "dev", "arnaLoop"])
    subprocess.run(["ip", "addr", "add", "44.31.119.3/24", "dev", "arnaLoop"])
    subprocess.run(["ip", "addr", "add", "44.31.119.4/24", "dev", "arnaLoop"])
    subprocess.run(["ip", "addr", "add", "44.31.119.5/24", "dev", "arnaLoop"])
    subprocess.run(["ip", "addr", "add", "44.31.119.6/24", "dev", "arnaLoop"])
    subprocess.run(["ip", "link", "set", "arnaLoop", "up"])

    # Copy appropriate config files
    print("Copying needed config files")
    copy_config_with_env_vars(RAW_CONFIGS_ROOT / "bird" / "bird.conf",
                              Path("/etc/bird/bird.conf"))

    # Launch background services
    print("Launching Caddy")
    subprocess.run(["caddy", "start", "--config", "/etc/caddy/Caddyfile"])
    # print("Launching APRSC")
    # subprocess.Popen([
    #     "/opt/aprsc/sbin/aprsc", "-c", "/etc/aprsc/aprsc.conf", "-u", "aprsc",
    #     "-p", "/tmp/aprsc.pid"
    # ])

    # Spawn each echolink server
    for i in range(3):
        i = i + 1
        print(f"Launching Echolink server {i}")
        copy_config_with_env_vars(
            RAW_CONFIGS_ROOT / "echolink" / f"ELProxy-{i:02}.conf",
            Path(f"/tmp/ELProxy-{i:02}.conf"))
        subprocess.Popen([
            "java", "-jar", "/usr/local/bin/EchoLinkProxy.jar",
            f"/tmp/ELProxy-{i:02}.conf"
        ])

    # Launch bird in the foreground
    print("Launching Bird")
    subprocess.run(["bird", "-f", "-d", "-c", "/etc/bird/bird.conf"])


if __name__ == "__main__":
    main()