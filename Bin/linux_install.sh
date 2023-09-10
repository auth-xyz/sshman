#!/bin/bash

SSHMAN_DIR="$HOME/.sshm"
BIN_DIR="$SSHMAN_DIR/.bin"
GITHUB_API_URL="https://api.github.com/repos/auth-xyz/sshman/releases/latest"

get_latest_asset_name() {
    local latest_asset_name=$(curl -s "$GITHUB_API_URL" | jq -r '.assets[] | select(.name | endswith("tar.gz")) | .name')
    echo "$latest_asset_name"
}

SSHMAN_ASSET_NAME=$(get_latest_asset_name)

if [ -z "$SSHMAN_ASSET_NAME" ]; then
    echo "Failed to retrieve the latest sshman release asset name from GitHub."
    exit 1
fi

SSHMAN_URL="https://github.com/auth-xyz/sshman/releases/latest/download/$SSHMAN_ASSET_NAME"

mkdir -p "$BIN_DIR"
curl -L "$SSHMAN_URL" | tar xz -C "$BIN_DIR"
mv "$BIN_DIR/sshman" "$BIN_DIR/sshman"

sudo ln -s "$BIN_DIR/sshman" "/usr/bin/sshman"

if [ $? -eq 0 ]; then
    echo "sshman is now installed and available system-wide (Asset: $SSHMAN_ASSET_NAME)."
else
    echo "Failed to create a symlink to sshman."
fi
