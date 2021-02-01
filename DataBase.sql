CREATE TABLE ENDERECO (
    id serial PRIMARY KEY,
    logradouro VARCHAR(80) NOT NULL,
    complemento VARCHAR(80) NOT NULL,
    numero VARCHAR(5) NOT NULL,
    bairro VARCHAR(30) NOT NULL,
    cidade VARCHAR(10) NOT NULL,
    estado VARCHAR(10) NOT NULL,
    pais VARCHAR(10) NOT NULL
);

CREATE TABLE CLIENTE (
    cpf VARCHAR(11) NOT NULL PRIMARY KEY,
    email VARCHAR(80) NOT NULL,
	nome VARCHAR(80) NOT NULL,
    id_endereco int NOT NULL REFERENCES endereco(id),
	sexo CHAR(1),
	CHECK (Sexo IN ('M', 'F', 'N'))
);

CREATE TABLE SERVICO (
    id serial PRIMARY KEY,
    nome VARCHAR(20) NOT NULL,
    preco NUMERIC NOT NULL
);

CREATE TABLE PEDIDO (
    id serial PRIMARY KEY,
    cpf VARCHAR(11) NOT NULL REFERENCES cliente(cpf),
    id_servico INT NOT NULL REFERENCES servico(id),
    quantidade INT NOT NULL,
    valor_total NUMERIC,
    data_marc TIMESTAMP NOT NULL
);

CREATE OR REPLACE FUNCTION pedido_notify() 
    RETURNS TRIGGER AS $$
        BEGIN
            NEW.valor_total := (SELECT NEW.quantidade * servico.preco
                           FROM servico
                           WHERE servico.id = NEW.id_servico);
            perform pg_notify('novo_pedido', NEW::text);
            RETURN NEW;
        END;
    $$ LANGUAGE plpgsql;

CREATE TRIGGER pedido_notify 
    after INSERT ON pedido 
    FOR each ROW 
    EXECUTE PROCEDURE pedido_notify();