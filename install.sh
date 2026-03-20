#!/bin/bash
set -e

echo "Updating system..."
apt-get update
apt-get install -y curl wget unzip default-jre-headless

echo "Downloading signal-cli (Java 17 compatible)..."
curl -L https://github.com/AsamK/signal-cli/releases/download/v0.12.6/signal-cli-0.12.6.tar.gz -o signal-cli.tar.gz

echo "Extracting..."
tar -xzf signal-cli.tar.gz
mv signal-cli-0.12.6 signal-cli

chmod +x signal-cli/bin/signal-cli

echo "Installing Python deps..."
pip install --no-cache-dir -r requirements.txt

echo "Setup complete!"
