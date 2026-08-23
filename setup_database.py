"""
Script para configurar o banco de dados no Supabase.
Execute uma vez para criar as tabelas necessárias.

INSTRUÇÕES:
1. Acesse https://supabase.com e crie um projeto gratuito
2. Vá em SQL Editor e cole o SQL abaixo
3. Execute o SQL
4. Copie a URL e anon key para o .env
"""

SQL_CRIAR_TABELAS = """
-- =============================================
-- PrediALL Facilidades — Schema do Banco
-- Execute este SQL no Supabase SQL Editor
-- =============================================

-- Tabela principal de chamados
CREATE TABLE IF NOT EXISTS chamados (
    id BIGSERIAL PRIMARY KEY,
    unidade TEXT NOT NULL,
    local TEXT NOT NULL,
    tipo_ocorrencia TEXT NOT NULL,
    urgencia TEXT NOT NULL DEFAULT 'Normal',
    descricao TEXT NOT NULL,
    solicitante_nome TEXT NOT NULL,
    solicitante_email TEXT NOT NULL,
    solicitante_ramal TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'Aberto',
    responsavel TEXT DEFAULT NULL,
    categoria_ia TEXT DEFAULT '',
    confianca_ia REAL DEFAULT 0,
    criado_via TEXT DEFAULT 'Formulário',
    data_abertura TIMESTAMPTZ DEFAULT NOW(),
    data_conclusao TIMESTAMPTZ DEFAULT NULL,
    nota_satisfacao INTEGER DEFAULT NULL,
    comentario_satisfacao TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de histórico de ações
CREATE TABLE IF NOT EXISTS historico_chamados (
    id BIGSERIAL PRIMARY KEY,
    chamado_id BIGINT REFERENCES chamados(id),
    acao TEXT NOT NULL,
    usuario TEXT NOT NULL,
    observacao TEXT DEFAULT '',
    data_hora TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_chamados_email ON chamados(solicitante_email);
CREATE INDEX IF NOT EXISTS idx_chamados_status ON chamados(status);
CREATE INDEX IF NOT EXISTS idx_chamados_unidade ON chamados(unidade);
CREATE INDEX IF NOT EXISTS idx_chamados_urgencia ON chamados(urgencia);
CREATE INDEX IF NOT EXISTS idx_chamados_data ON chamados(data_abertura DESC);

-- Habilitar RLS (Row Level Security) - opcional para MVP
-- ALTER TABLE chamados ENABLE ROW LEVEL SECURITY;

-- View para estatísticas
CREATE OR REPLACE VIEW vw_estatisticas_chamados AS
SELECT
    unidade,
    tipo_ocorrencia,
    urgencia,
    status,
    COUNT(*) as total,
    AVG(nota_satisfacao) as csat_medio,
    AVG(EXTRACT(EPOCH FROM (data_conclusao - data_abertura)) / 60) as tempo_medio_minutos
FROM chamados
GROUP BY unidade, tipo_ocorrencia, urgencia, status;

-- Dados de exemplo (opcional - remova em produção)
INSERT INTO chamados (unidade, local, tipo_ocorrencia, urgencia, descricao, solicitante_nome, solicitante_email, status, categoria_ia, confianca_ia, criado_via)
VALUES
    ('Sede SP', '4º andar, sala 405', 'Climatização / Refrigeração', 'Normal', 'Ar-condicionado da sala está vazando água no chão', 'Maria Santos', 'maria.santos@empresa.com', 'Aberto', 'Climatização / Refrigeração', 95, 'Chat IA'),
    ('Sede SP', '2º andar, copa', 'Hidráulica', 'Alta', 'Torneira da copa não para de pingar, mesmo fechada', 'João Silva', 'joao.silva@empresa.com', 'Em Andamento', 'Hidráulica', 92, 'Formulário'),
    ('CD Guarulhos', 'Doca 03', 'Infraestrutura (Docas, Estrutural)', 'Crítica', 'Portão da doca 03 travou na posição aberta, não fecha', 'Pedro Oliveira', 'pedro.oliveira@empresa.com', 'Em Andamento', 'Infraestrutura', 98, 'Chat IA'),
    ('Filial RJ', '1º andar, recepção', 'Elétrica', 'Normal', 'Duas luminárias da recepção estão apagadas', 'Ana Costa', 'ana.costa@empresa.com', 'Concluído', 'Elétrica', 90, 'Formulário'),
    ('Cervejaria Boituva', 'Linha 02 - Envasamento', 'Elétrica', 'Alta', 'Tomada próxima à esteira com faísca quando liga equipamento', 'Carlos Mendes', 'carlos.mendes@empresa.com', 'Aberto', 'Elétrica', 97, 'Chat IA');
"""


def main():
    print("=" * 60)
    print("  PrediALL Facilidades — Setup do Banco de Dados")
    print("=" * 60)
    print()
    print("Para configurar o banco de dados:")
    print()
    print("1. Acesse https://supabase.com")
    print("2. Crie um projeto gratuito (ou use um existente)")
    print("3. Vá em 'SQL Editor' no menu lateral")
    print("4. Cole e execute o SQL abaixo:")
    print()
    print("-" * 60)
    print(SQL_CRIAR_TABELAS)
    print("-" * 60)
    print()
    print("5. Após executar, vá em Settings → API")
    print("6. Copie:")
    print("   - Project URL → SUPABASE_URL no .env")
    print("   - anon public key → SUPABASE_KEY no .env")
    print()
    print("✅ Pronto! O banco está configurado.")


if __name__ == "__main__":
    main()
