# Imagem base
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de código-fonte e o script de instalação para o diretório de trabalho
COPY . /app
COPY install_dockerize.sh /app

RUN ls -la

RUN rm -rf migrations

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Torna o script de instalação executável e executa-o
RUN chmod +x /app/install_dockerize.sh && /app/install_dockerize.sh

# Expõe a porta 5000 para acessar a API
EXPOSE 5000
