# Imagem base
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de código-fonte para o diretório de trabalho
COPY . /app

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 5000 para acessar a API
EXPOSE 5000

# Define o comando de inicialização do aplicativo
CMD ["python", "app.py"]
