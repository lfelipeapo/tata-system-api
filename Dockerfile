# Imagem base
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de código-fonte e o script wait-for-it para o diretório de trabalho
COPY . /app
COPY wait-for-it.sh /app/

# Torna o script wait-for-it.sh executável
RUN chmod +x /app/wait-for-it.sh

# Lista os arquivos no diretório (opcional, para fins de depuração)
RUN ls -la

# Remove o diretório migrations, se necessário
RUN rm -rf migrations

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Expõe a porta 5000 para acessar a API
EXPOSE 5000
