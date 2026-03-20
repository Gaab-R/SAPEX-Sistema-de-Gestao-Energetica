# ⚙️ Backend

Este diretório contém a aplicação backend do sistema SAPEX, responsável pela simulação de sensores, processamento de dados, integração com banco de dados, automação e disponibilização da interface web via Flask.

---

## 🧠 Funcionalidades do backend

- Simulação de sensores IoT (temperatura, umidade, consumo, presença)
- Envio de dados para nuvem (ThingSpeak)
- Armazenamento local (JSON) e em banco MySQL
- Cálculo de consumo e estimativa de custo energético
- Análise com Inteligência Artificial (Hugging Face Transformers)
- Automação de dispositivos baseada em regras
- Servidor web com Flask

---

## 📂 Arquivos


main.py              # Aplicação principal (Flask + lógica do sistema)
requirements.txt     # Dependências do projeto
dados_simulados.json # Armazenamento local dos dados


---

## ▶️ Como executar

### 1. Instalar dependências

pip install -r requirements.txt


### 2. Configurar banco (opcional)

No arquivo main.py, ajuste:


host="localhost"
user="root"
password="SUA_SENHA"
database="sistema_energia"


---

### 3. Executar aplicação

python main.py


---

## 🔁 Funcionamento do sistema

O sistema executa dois processos simultâneos:

### 1. Loop contínuo (simulação)
- Gera dados de sensores a cada 60 segundos
- Envia dados para nuvem
- Salva no MySQL (se conectado)
- Executa automações

### 2. Servidor Flask
- Exibe dashboard em tempo real
- Mostra análises e recomendações
- Renderiza dados no frontend

---

## 🤖 Inteligência Artificial

A função de IA utiliza o modelo:


gpt2


Para gerar sugestões de economia de energia com base nos dados coletados.

---

## ⚠️ Observações

- Caso o MySQL não esteja disponível, o sistema roda em modo simulação
- O arquivo JSON é usado como fallback de persistência
- O uso de IA pode impactar desempenho dependendo da máquina

---

## 🔒 Segurança

- Não utilize credenciais reais no código
- Recomenda-se uso de variáveis de ambiente (.env) para produção

---

## 🚀 Possíveis melhorias

- Implementação de API REST
- Autenticação de usuários
- Integração com dispositivos reais IoT
- Deploy em nuvem (Render, AWS, etc.)
