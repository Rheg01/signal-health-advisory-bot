#!/bin/bash
set -e

apt-get update
apt-get install -y curl wget unzip default-jre

echo "Downloading signal-cli..."
curl -L https://github.com/AsamK/signal-cli/releases/download/v0.13.3/signal-cli-0.13.3.tar.gz -o signal-cli.tar.gz

tar -xzf signal-cli.tar.gz
mv signal-cli-0.13.3 signal-cli

chmod +x signal-cli/bin/signal-cli

echo "signal-cli installed"
