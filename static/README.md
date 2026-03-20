# 🎨 Static – SAPEX

Este diretório contém os arquivos estáticos do sistema SAPEX, responsáveis pela estilização e interatividade da interface.

---

## 📁 Estrutura


static/
│
├── css/
│   └── style.css      # Estilos da aplicação
│
└── js/
    └── script.js      # Lógica de interatividade e gráficos


---

## 🎨 CSS (style.css)

Responsável pela aparência do sistema:

- Layout do dashboard
- Cores e identidade visual
- Responsividade básica
- Estilização de:
  - Cards
  - Sidebar
  - Botões
  - Gráficos
  - Indicadores de status

---

## ⚙️ JavaScript (script.js)

Responsável pela interatividade da aplicação:

- Leitura de dados do HTML (data-ultimo-dado)
- Conversão de JSON para objeto JavaScript
- Atualização dinâmica de informações
- Criação de gráficos com Chart.js
- Manipulação do DOM

---

## 🔗 Integração com o HTML

Os dados são passados do backend via atributo:

html
<body data-ultimo-dado='{{ ultimo_dado_json }}'>


E utilizados no JavaScript:

javascript
const dados = JSON.parse(document.body.dataset.ultimoDado);


---

## 📊 Funcionalidades

- Atualização dinâmica de consumo energético
- Renderização de gráficos
- Exibição de status em tempo real
- Interação com elementos da interface

---

## ⚠️ Observações

- Os arquivos estáticos são carregados automaticamente pelo Flask
- Caminho padrão no HTML:

html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>


---

## 🚀 Possíveis melhorias

- Animações com CSS/JS
- Gráficos mais avançados
- Atualização em tempo real (WebSocket)
- Dark mode 🌙
