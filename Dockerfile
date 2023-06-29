# Imagem base
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de código-fonte para o diretório de trabalho
COPY . /app

RUN ls -la

RUN rm -rf migrations

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Instala o Dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Expõe a porta 5000 para acessar a API

EXPOSE 5000
