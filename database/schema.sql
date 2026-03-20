-- schema.sql
-- Criação da estrutura do banco de dados sistema_energia

CREATE DATABASE sistema_energia;
USE sistema_energia;

-- Tabela de usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    perfil VARCHAR(20) NOT NULL
);

-- Tabela de dados dos sensores
CREATE TABLE dados_sensores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    data_registro DATETIME NOT NULL,
    temperatura FLOAT,
    umidade FLOAT,
    consumo FLOAT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabela de contas de luz
CREATE TABLE contas_luz (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    mes VARCHAR(20),
    consumo_total FLOAT,
    valor_estimado FLOAT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
