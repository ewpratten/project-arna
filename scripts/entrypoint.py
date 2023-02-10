#! /usr/bin/env python3
import os
import subprocess

from pathlib import Path

# Variables that must be passed through to config files
CONFIG_ENV_PASSTHROUGH_KEYS = ["PEER_ASN", "PEER_IP"]

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
        print(config)
        f.write(config)


def main():

    # Configure networking
    print("Creating dummy network interface")
    subprocess.run(["ip", "link", "add", "arnaLoop", "type", "dummy"])
    subprocess.run(["ip", "addr", "add", "44.31.119.1/24", "dev", "arnaLoop"])
    subprocess.run(["ip", "link", "set", "arnaLoop", "up"])

    # Copy appropriate config files
    print("Copying needed config files")
    copy_config_with_env_vars(RAW_CONFIGS_ROOT / "bird" / "bird.conf",
                              Path("/etc/bird/bird.conf"))

    # Launch bird in the foreground
    subprocess.run(["bird", "-f", "-d", "-c", "/etc/bird/bird.conf"])


if __name__ == "__main__":
    main()