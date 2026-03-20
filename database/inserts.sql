-- inserts.sql
-- Inserção de dados iniciais no banco sistema_energia

-- Inserir usuário de teste
INSERT INTO usuarios (nome, perfil) 
VALUES ('João', 'Família');

-- Inserir dados fictícios para gráficos
INSERT INTO dados_sensores (usuario_id, data_registro, temperatura, umidade, consumo) VALUES
(1, '2025-01-01 10:00:00', 25.0, 50.0, 150.0),
(1, '2025-01-02 10:00:00', 26.0, 51.0, 160.0),
(1, '2025-01-03 10:00:00', 24.0, 49.0, 155.0),
(1, '2025-02-01 10:00:00', 22.0, 45.0, 180.0),
(1, '2025-02-02 10:00:00', 23.0, 46.0, 175.0),
(1, '2025-02-03 10:00:00', 21.0, 44.0, 185.0);

-- Inserir contas de luz
INSERT INTO contas_luz (usuario_id, mes, consumo_total, valor_estimado) VALUES
(1, 'Janeiro', 465.0, 320.50),
(1, 'Fevereiro', 540.0, 380.75);
