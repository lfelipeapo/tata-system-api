#!/bin/sh
DOCKERIZE_VERSION="v0.6.1"
ARCH=$(uname -m)

case $ARCH in
    x86_64) 
        DOCKERIZE_URL="https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz"
        ;;
    armv7l) 
        DOCKERIZE_URL="https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-armhf-$DOCKERIZE_VERSION.tar.gz"
        ;;
    aarch64)
        DOCKERIZE_URL="https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-arm64-$DOCKERIZE_VERSION.tar.gz"
        ;;
    *)
        echo "Arquitetura $ARCH não suportada"
        exit 1
        ;;
esac

wget $DOCKERIZE_URL -O dockerize.tar.gz
tar -C /usr/local/bin -xzvf dockerize.tar.gz
rm dockerize.tar.gz
