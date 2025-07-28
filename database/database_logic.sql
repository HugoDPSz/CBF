-- FUNCTION: Calcula a idade de uma pessoa a partir da data de nascimento.
DELIMITER $$
CREATE FUNCTION calcular_idade(data_nasc DATE)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN TIMESTAMPDIFF(YEAR, data_nasc, CURDATE());
END$$
DELIMITER ;

-- PROCEDURE: Registra um novo contrato para um jogador, garantindo que não haja contratos ativos sobrepostos.
DELIMITER $$
CREATE PROCEDURE registrar_contrato(
    IN p_id_jogador INT,
    IN p_id_equipe INT,
    IN p_data_inicio DATE,
    IN p_data_fim DATE,
    IN p_salario FLOAT
)
BEGIN
    DECLARE contrato_ativo_existente INT DEFAULT 0;

    -- Verifica se já existe um contrato ativo para o jogador no período
    SELECT COUNT(*) INTO contrato_ativo_existente
    FROM contratos
    WHERE id_jogador = p_id_jogador
      AND status = 'Ativo'
      AND p_data_inicio < data_fim;

    IF contrato_ativo_existente = 0 THEN
        INSERT INTO contratos (id_jogador, id_equipe, data_inicio, data_fim, salario, status)
        VALUES (p_id_jogador, p_id_equipe, p_data_inicio, p_data_fim, p_salario, 'Ativo');
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'O jogador já possui um contrato ativo neste período.';
    END IF;
END$$
DELIMITER ;

-- TRIGGER: Atualiza o status de um contrato para 'Encerrado' quando a data de término é atingida.
DELIMITER $$
CREATE TRIGGER before_update_partida_placar
BEFORE UPDATE ON partidas
FOR EACH ROW
BEGIN
    -- Exemplo simples: Impede que o placar seja negativo
    IF NEW.placar_casa < 0 THEN
        SET NEW.placar_casa = 0;
    END IF;
    IF NEW.placar_visitante < 0 THEN
        SET NEW.placar_visitante = 0;
    END IF;
END$$
DELIMITER ;

-- Tabela de Log para salários
CREATE TABLE IF NOT EXISTS log_alteracoes_salario (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_contrato INT,
    salario_antigo FLOAT,
    salario_novo FLOAT,
    data_alteracao DATETIME,
    FOREIGN KEY (id_contrato) REFERENCES contratos(id_contrato)
);

-- VIEW: Exibe informações de jogadores com contratos ativos
CREATE OR REPLACE VIEW vw_jogadores_contratos_ativos AS
SELECT
    j.id_jogador,
    j.nome AS nome_jogador,
    j.posicao,
    e.nome AS nome_equipe,
    c.id_contrato,
    c.data_inicio,
    c.data_fim,
    c.salario,
    c.status
FROM
    jogadores j
JOIN
    contratos c ON j.id_jogador = c.id_jogador
JOIN
    equipes e ON c.id_equipe = e.id_equipe;

-- VIEW: Exibe detalhes das partidas
CREATE OR REPLACE VIEW vw_partidas_detalhadas AS
SELECT
    p.id AS id_partida,
    p.data_hora,
    p.estadio,
    p.local,
    c.nome AS competicao,
    ec.nome AS equipe_casa,
    ev.nome AS equipe_visitante,
    p.placar_casa,
    p.placar_visitante
FROM
    partidas p
JOIN
    competicoes c ON p.id_competicao = c.id_competicao
JOIN
    equipes ec ON p.equipe_casa_id = ec.id_equipe
JOIN
    equipes ev ON p.equipe_visitante_id = ev.id_equipe;

-- PROCEDURE: Rescinde um contrato
DELIMITER $$
CREATE PROCEDURE sp_rescindir_contrato(IN p_id_contrato INT)
BEGIN
    UPDATE contratos
    SET status = 'Rescindido', data_fim = CURDATE()
    WHERE id_contrato = p_id_contrato;
END$$
DELIMITER ;

-- TRIGGER: Log de alterações de salário
DELIMITER $$
CREATE TRIGGER trg_log_alteracoes_salario
AFTER UPDATE ON contratos
FOR EACH ROW
BEGIN
    IF OLD.salario <> NEW.salario THEN
        INSERT INTO log_alteracoes_salario (id_contrato, salario_antigo, salario_novo, data_alteracao)
        VALUES (NEW.id_contrato, OLD.salario, NEW.salario, NOW());
    END IF;
END$$
DELIMITER ;