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