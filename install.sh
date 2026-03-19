#!/bin/bash
set -e

echo "Updating packages..."
apt-get update
apt-get install -y curl wget unzip default-jre-headless

# Download and install signal-cli
echo "Downloading signal-cli..."
curl -L https://github.com/AsamK/signal-cli/releases/download/v0.13.3/signal-cli-0.13.3.tar.gz -o signal-cli.tar.gz

echo "Extracting signal-cli..."
tar -xzf signal-cli.tar.gz
mv signal-cli-0.13.3 signal-cli

chmod +x signal-cli/bin/signal-cli
echo "signal-cli installed successfully!"

# Make sure Python dependencies are installed
echo "Installing Python requirements..."
pip install --no-cache-dir -r requirements.txt

echo "All setup done. Ready to run main.py!"
