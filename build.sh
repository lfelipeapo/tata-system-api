#!/bin/bash

# Remove a pasta migrations localmente
rm -rf migrations

# Constrói a imagem Docker
docker build -t nome_da_imagem .