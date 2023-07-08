-- Criação da tabela Cliente
CREATE TABLE cliente (
    id SERIAL PRIMARY KEY,
    nome_cliente VARCHAR(80) NOT NULL,
    cpf_cliente VARCHAR(11) NOT NULL UNIQUE,
    data_cadastro TIMESTAMP NOT NULL,
    data_atualizacao TIMESTAMP
);

-- Criação da tabela ConsultaJuridica
CREATE TABLE consulta_juridica (
    pk_consulta SERIAL PRIMARY KEY,
    nome_cliente VARCHAR(80),
    cpf_cliente VARCHAR(11),
    data_consulta DATE,
    horario_consulta TIME,
    detalhes_consulta VARCHAR(200),
    cliente_id INTEGER,
    FOREIGN KEY (cliente_id) REFERENCES cliente (id) ON DELETE CASCADE,
    CONSTRAINT consulta_unico UNIQUE (cpf_cliente, data_consulta)
);

-- Criação da tabela User
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    password_hash VARCHAR(128),
    name VARCHAR(64),
    image VARCHAR(200)
);
