# Imagem base
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de código-fonte para o diretório de trabalho
COPY . /app

# Lista os arquivos no diretório (opcional, para fins de depuração)
RUN ls -la

# Remove o diretório migrations, se necessário
RUN rm -rf migrations

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Baixa o script wait-for-it e o torna executável
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x wait-for-it.sh

# Expõe a porta 5000 para acessar a API
EXPOSE 5000
