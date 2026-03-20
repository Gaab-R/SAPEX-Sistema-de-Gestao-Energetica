# 🗄️ Database – SAPEX

Este diretório contém a estrutura e os dados iniciais do banco de dados do sistema SAPEX, responsável por armazenar informações de usuários, sensores e consumo energético.

---

## 📁 Estrutura


database/
│
├── schema.sql   # Criação das tabelas e estrutura do banco
├── inserts.sql  # Inserção de dados iniciais
└── run.sql      # Script para execução completa


---

## 🧠 Descrição

O banco de dados sistema_energia foi desenvolvido para simular um sistema de monitoramento energético, contendo:

- Usuários do sistema
- Dados coletados por sensores
- Informações de consumo energético mensal

---

## 🗃️ Tabelas

### 👤 usuarios
Armazena os dados dos usuários:

- id (PK)
- nome
- perfil

---

### 📡 dados_sensores
Armazena dados coletados dos sensores:

- id (PK)
- usuario_id (FK)
- data_registro
- temperatura
- umidade
- consumo

---

### 💡 contas_luz
Armazena o consumo mensal estimado:

- id (PK)
- usuario_id (FK)
- mes
- consumo_total
- valor_estimado

---

## ⚙️ Como executar

### 1. Abrir o MySQL

### 2. Executar o script principal:

sql
SOURCE run.sql;


Ou manualmente:

sql
SOURCE schema.sql;
SOURCE inserts.sql;


---

## 📊 Dados de teste

O banco já vem com:

- 1 usuário cadastrado
- Dados de sensores para janeiro e fevereiro
- Registros de consumo mensal

Esses dados permitem:

- Testar gráficos
- Validar consultas
- Simular funcionamento do sistema

---

## ⚠️ Observações

- O banco foi projetado para fins acadêmicos e demonstração
- Pode ser expandido com novas tabelas e relacionamentos
- Compatível com MySQL

---

## 🚀 Possíveis melhorias

- Adicionar índices para otimização de consultas
- Implementar autenticação de usuários
- Criar tabelas para alertas e notificações
- Integração com dados em tempo real (IoT)
