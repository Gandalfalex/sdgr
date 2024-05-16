#!/bin/bash

# Specify the Hugo version
HUGO_VERSION="0.121.1"

# Determine the architecture
ARCH=$(uname -m)

# Choose the correct Hugo binary based on the architecture
case $ARCH in
    "x86_64") 
        HUGO_BINARY="hugo_${HUGO_VERSION}_Linux-64bit.tar.gz"
        ;;
    "aarch64")
        HUGO_BINARY="hugo_${HUGO_VERSION}_linux-arm64.tar.gz"
        ;;
    *)
        echo "Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

# Download and install Hugo
wget --quiet "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/${HUGO_BINARY}" && \
tar xzf "${HUGO_BINARY}" && \
rm -r "${HUGO_BINARY}" && \
mv hugo /usr/bin && \
chmod 755 /usr/bin/hugo

# Display Hugo version for verification
hugo version
echo hugo version
