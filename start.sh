#!/bin/bash

# Dê permissões de execução ao script build.sh
chmod +x wait-for-it.sh
chmod +x build.sh

# Execute o script build.sh
./build.sh

# Inicie o Docker Compose
docker compose up --build
