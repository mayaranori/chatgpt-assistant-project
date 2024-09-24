import sqlite3

# Conecta ao banco de dados (será criado se não existir)
conn = sqlite3.connect('database/assistente.db')

# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Criação das tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL,
    data_captura TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Produtos (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      TEXT    NOT NULL,
    descricao TEXT    NOT NULL,
    categoria TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Planos (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_plano TEXT    NOT NULL,
    preco      REAL    NOT NULL,
    detalhes   TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Beneficios (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    beneficio  TEXT,
    FOREIGN KEY (produto_id) REFERENCES Produtos(id)
);
''')

# Confirma as alterações
conn.commit()

# Fecha a conexão com o banco de dados
conn.close()

print("Banco de dados e tabelas criados com sucesso!")
