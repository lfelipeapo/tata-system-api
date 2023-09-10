# Tata System API
API desenvolvida para o projeto Tata System relacionado ao MVP estruturado da Pós Graduação em Desenvolvimento Fullstack em Sistemas da PUC-Rio

## Instalação:

Para rodar o projeto é necessário a instalação de Docker:
### Ambiente Windows:
<https://docs.docker.com/desktop/install/windows-install/>

### Ambiente Linux:
- Para o ambiente Linux, você pode usar o seguinte guia de instalação:

1. Atualize o índice de pacotes do apt e instale os pacotes para permitir que o apt use um repositório via HTTPS:

    ```
    sudo apt-get update
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    ```

2. Adicione a chave oficial GPG do Docker:

    ```
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    ```

3. Configure o repositório estável do Docker:

    ```
    echo \
      "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

4. Atualize o índice de pacotes do apt e instale a versão mais recente do Docker Engine e do containerd:

    ```
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

5. Verifique se o Docker foi instalado corretamente executando o hello-world:

    ```
    sudo docker run hello-world
    ```

## Como Executar o Projeto

### Iniciar o sistema

1. Navegue até o diretório do projeto no terminal.

2. Execute o comando `docker-compose up --build`.

### Interagir com a API

A API será executada na porta 5000 do host local. Você pode fazer requisições para `http://localhost:5000/`.

### Parar o sistema

No terminal, pressione `Ctrl+C`.

### Remover os contêineres criados

Execute o comando `docker-compose down`.

**Nota:** No Windows, todos os comandos do Docker devem ser executados no PowerShell ou no CMD, não no WSL.

## Para rodar manualmente o projeto:
**Nota** No .env e no docker-compose.yml na raiz do projeto atualize a flag DOCKER_ENV para False.
**Nota2**: Caso deseje também poderá alterar variáveis locais de ambiente no arquivo database.py em models dentro do diretório raiz da API.

- Para rodar o projeto manualmente primeiro instale o postgres localmente em seu ambiente seja Linux ou Windows:
## Windows:
<https://www.postgresql.org/download/windows/>

## No ambiente Linux:

Aqui estão as etapas para instalar o PostgreSQL no Ubuntu. O processo pode variar dependendo da distribuição do Linux que você está usando.

1. **Atualize os pacotes do sistema**: Antes de instalar qualquer pacote, é uma boa prática atualizar a lista de pacotes do repositório do sistema operacional. No terminal, digite o seguinte comando:

    ```
    sudo apt update
    ```

2. **Instale o PostgreSQL**: Use o seguinte comando para instalar o PostgreSQL juntamente com o `pgAdmin`, uma interface gráfica para gerenciamento do PostgreSQL:

    ```
    sudo apt install postgresql postgresql-contrib pgadmin3
    ```

3. **Verifique a instalação**: Depois de instalar o PostgreSQL, você pode verificar se ele foi instalado corretamente usando o seguinte comando:

    ```
    sudo service postgresql status
    ```

    Você deverá ver uma mensagem indicando que o serviço PostgreSQL está rodando.

4. **Acesse o PostgreSQL**: Por padrão, o PostgreSQL cria um novo usuário chamado `postgres`. Para fazer login como `postgres`, use o seguinte comando:

    ```
    sudo su - postgres
    ```

    Em seguida, você pode acessar a interface de linha de comando do PostgreSQL usando o comando `psql`.

    ```
    psql
    ```
5. **Saia do PostgreSQL**: Para sair da interface de linha de comando do PostgreSQL, digite `\q` e pressione `Enter`. Para voltar ao seu usuário normal, digite `exit` ou `logout`.

6. **Crie um novo usuário do banco de dados (opcional)**: Se você quiser criar um novo usuário e um novo banco de dados, você pode fazer isso com os seguintes comandos:

    ```
    sudo -u postgres createuser -s nome_do_usuario
    sudo -u postgres createdb nome_do_banco
    ```

    Substitua `nome_do_usuario` pelo nome do usuário que você deseja criar e `nome_do_banco` pelo nome do banco de dados que você deseja criar.

7. **Configure a senha do novo usuário (opcional)**: Para definir ou alterar a senha do novo usuário, acesse o PostgreSQL com o comando `psql` e depois digite o seguinte:

    ```
    \password nome_do_usuario
    ```

    Substitua `nome_do_usuario` pelo nome do usuário que você criou. Você será solicitado a inserir uma nova senha para o usuário.

Agora você instalou o PostgreSQL e pode começar a usá-lo! Lembre-se de que você precisará alterar `nome_do_usuario` e `nome_do_banco` para os nomes de usuário e banco de dados que você deseja usar.

Rode o script abaixo:

```
#!/bin/bash

# Inserir o nome do banco de dados

DB_NAME="tata"

# Inserir o nome do usuário do Postgres

DB_USER="postgres"

# Inserir o caminho para o arquivo .sql

SQL_FILE="/caminho/para/create_tables.sql"

# Execute o arquivo .sql no banco de dados

psql -U "$DB_USER" -d "$DB_NAME" -a -f "$SQL_FILE"
```

## No Windows:

Rode os seguintes comandos:

```
# Inserir o nome do banco de dados
$DB_NAME="tata"

# Inserir o nome do usuário do Postgres
$DB_USER="postgres"

# Inserir o caminho para o arquivo .sql
$SQL_FILE="C:\caminho\para\create_tables.sql"

# Execute o arquivo .sql no banco de dados
psql -U $DB_USER -d $DB_NAME -a -f $SQL_FILE
```
**Nota: Arquivo de banco de dados está disponível em formato de sql na pasta database dentro do diretório raiz do projeto.**

## Instalação do Python 3.9 e ambiente local para a API:
### No Windows:

1. Vá para o [site oficial do Python](https://www.python.org/downloads/windows/) e baixe o instalador do Python 3.9 para Windows. Certifique-se de escolher a versão adequada para a sua versão do Windows (32 bits ou 64 bits).

2. Execute o instalador. Durante a instalação, marque a opção "Add Python 3.9 to PATH" na parte inferior da janela do instalador e, em seguida, clique em "Install Now".

3. Uma vez que a instalação esteja completa, você pode verificar se foi bem-sucedida abrindo um novo prompt de comando do Windows (Cmd) e digitando:

   ```cmd
   python --version
   ```

   Isso deve retornar algo como: `Python 3.9.x`.

4. O instalador do Python no Windows também instala o `pip`, que é o gerenciador de pacotes do Python. Você pode verificar a instalação do `pip` com:

   ```cmd
   pip --version
   ```

5. Agora, você deve criar um ambiente virtual para o seu projeto. No prompt de comando, navegue até o diretório do seu projeto (substitua `caminho_para_o_projeto` pelo caminho real do diretório do seu projeto):

   ```cmd
   cd caminho_para_o_projeto
   ```

   Em seguida, crie o ambiente virtual:

   ```cmd
   python -m venv nome_do_ambiente
   ```

   Ative o ambiente virtual:

   ```cmd
   .\nome_do_ambiente\Scripts\activate
   ```

6. Com o ambiente virtual ativado, você pode agora instalar as dependências necessárias para o seu projeto Flask a partir do arquivo `requirements.txt`:

   ```cmd
   pip install -r requirements.txt
   ```

7. Inicialize e migre o banco de dados:

   ```cmd
   flask db init
   flask db migrate
   ```

8. Agora, você pode iniciar a sua aplicação Flask:

   ```cmd
   flask run --host 0.0.0.0 --port 5000 --reload
   ```

Agora, sua aplicação Flask deve estar rodando e acessível na porta 5000.

Nota: No Windows, se o comando `python` não for reconhecido, você pode precisar usar `py` ou `python3` em vez disso, dependendo de como o Python foi instalado. O mesmo vale para o `pip`.

## No Linux

1. Primeiro, atualize o sistema operacional e instale as dependências necessárias. Abra um terminal e execute os seguintes comandos:

   ```bash
   sudo apt update
   sudo apt install software-properties-common
   ```

2. Em seguida, adicione o repositório "deadsnakes", que contém as versões mais recentes do Python:

   ```bash
   sudo add-apt-repository ppa:deadsnakes/ppa
   ```

   Quando solicitado, pressione Enter para continuar.

3. Após a adição do repositório, atualize o sistema novamente:

   ```bash
   sudo apt update
   ```

4. Agora você está pronto para instalar o Python 3.9:

   ```bash
   sudo apt install python3.9
   ```

5. Uma vez instalado, verifique a instalação executando:

   ```bash
   python3.9 --version
   ```

   Isso deve retornar algo como: `Python 3.9.x`.

6. Se você deseja instalar o gerenciador de pacotes pip para Python 3.9, você pode fazer isso com o seguinte comando:

   ```bash
   sudo apt install python3.9-venv python3.9-dev python3.9-distutils
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   python3.9 get-pip.py
   ```

   Isso instalará o `pip` especificamente para o Python 3.9.

7. Crie um ambiente virtual com Python 3.9 da seguinte maneira:

   ```bash
   python3.9 -m venv nome_do_ambiente
   ```

   Ative o ambiente virtual:

   ```bash
   source nome_do_ambiente/bin/activate
   ```

8. Navegue até o diretório do seu projeto (substitua `caminho_para_o_projeto` pelo caminho real do diretório do seu projeto):

   ```bash
   cd caminho_para_o_projeto
   ```

9. Instale as dependências necessárias para o seu projeto Flask utilizando o arquivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

10. Inicialize e migre o banco de dados:

    ```bash
    flask db init
    flask db migrate
    ```

11. Agora, você pode iniciar sua aplicação Flask:

    ```bash
    flask run --host 0.0.0.0 --port 5000 --reload
    ```

Agora, a API deve estar rodando e acessível na porta 5000 localmente.

# Endpoints da API:

## Consulta Jurídica
Endpoints para a criação, atualização, exclusão e obtenção de consultas jurídicas.

DELETE /consulta: Exclui uma Consulta Jurídica.

GET /consulta: Obtém uma consulta jurídica pelo ID.

POST /consulta: Cria uma nova Consulta Jurídica.

PUT /consulta: Atualiza uma Consulta Jurídica existente.

GET /consultas: Obtém todas as consultas jurídicas ou consultas por data, nome do cliente ou CPF do cliente.

GET /consultas/hoje: Obtém as consultas jurídicas de hoje.

GET /consultas/horario: Obtém as consultas jurídicas em um horário específico para determinada data.

## Cliente
Endpoints para a criação, atualização, exclusão e obtenção de clientes.

POST /cliente: Cria um novo cliente.

DELETE /cliente: Exclui um cliente.

GET /cliente: Obtém um cliente pelo ID.

PUT /cliente: Atualiza um cliente existente.

GET /clientes: Obtém todos os clientes ou clientes filtrados por nome, CPF, data de cadastro ou data de atualização.

## Documento
Endpoints para a criação, atualização, exclusão e obtenção de documentos.

DELETE /documento: Exclui um Documento.

GET /documento: Obtém um Documento pelo ID.

POST /documento: Cria um novo Documento.

PUT /documento: Atualiza um Documento existente.

POST /documento/upload: Faz o upload de um documento PDF.

GET /documentos: Obtém todos os Documentos.
## Usuário
Endpoints para a criação, atualização, exclusão, obtenção e autenticação de usuários.

DELETE /user: Exclui um usuário.

GET /user: Obtém um usuário pelo ID.

PUT /user: Atualiza um usuário existente.

POST /user/authenticate: Realiza a autenticação de usuário

POST /user/create: Cria um usuário.

GET /users: Obtém todos os usuários do banco de dados.

## Documentação
Seleção de documentação: Swagger, Redoc ou RapiDoc

GET /: Redireciona para /openapi, tela que permite a escolha do estilo de documentação.

**Esses são os principais endpoints da API. Cada um deles possui um propósito específico e pode retornar uma resposta bem estruturada, dependendo da solicitação enviada. Para mais detalhes sobre cada endpoint, você pode consultar a documentação da API gerada automaticamente ou se referir ao código-fonte do projeto.**
