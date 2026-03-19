#!/usr/bin/env bash
set -e

# Latest as of March 2026 → update this when a new release drops
SIGNAL_CLI_VERSION="0.14.1"
INSTALL_DIR="/app/signal-cli"

if [ ! -d "$INSTALL_DIR" ]; then
  echo "Installing signal-cli v${SIGNAL_CLI_VERSION}..."
  curl -L -o signal-cli.tar.gz \
    "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_CLI_VERSION}/signal-cli-${SIGNAL_CLI_VERSION}.tar.gz"
  
  tar -xzf signal-cli.tar.gz
  mv "signal-cli-${SIGNAL_CLI_VERSION}" "$INSTALL_DIR"
  rm signal-cli.tar.gz
  echo "Installed at $INSTALL_DIR"
else
  echo "signal-cli already installed"
fi
