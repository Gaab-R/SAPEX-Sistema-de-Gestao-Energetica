# Static

Arquivos responsáveis pela estilização e interatividade do sistema.

---

## Estrutura

- css/style.css → estilos da aplicação  
- js/script.js → lógica e interações  

---

## CSS

Controla a aparência da interface:

- Layout do dashboard  
- Cores e identidade visual  
- Estilização de cards, sidebar e botões  
- Indicadores de status  

---

## JavaScript

Responsável pelo comportamento da aplicação:

- Leitura de dados enviados pelo backend  
- Atualização dinâmica de informações  
- Manipulação do DOM  
- Renderização de gráficos (Chart.js)  

---

## Integração com o backend

Os dados são enviados pelo Flask no HTML:

```html
<body data-ultimo-dado='{{ ultimo_dado_json }}'>
