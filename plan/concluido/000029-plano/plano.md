# Plano do projeto redshift

## Contexto

- Projeto: `syg/redshift`
- Tipo: laboratorio tecnico
- Visibilidade alvo: publica
- Chamado: `SYG-JZ-CH-2026-00003`

## Objetivo

Construir um laboratorio enxuto, em Python, para testar solucoes de queries em Redshift, com execucao reproduzivel e comparacao objetiva de resultados.

## Escopo

1. Estruturar repositorio com base Python para execucao de testes de query.
2. Definir padrao de organizacao de queries por cenario.
3. Criar pipeline local para executar, medir e registrar resultados por perfil de conexao.
4. Documentar como adicionar novos casos de teste.
5. Publicar criterios minimos para evolucao futura do laboratorio.
6. Preparar integracao futura com a skill Redshift para reuso no contexto `syg`.

## Fora de escopo (fase inicial)

1. Integracao com producao.
2. Provisionamento de infraestrutura.
3. Dashboard web de observabilidade.
4. Otimizacao automatica de queries por IA.

## Entregaveis

1. Estrutura inicial do projeto Python.
2. Guia de execucao local e convencoes de testes de query.
3. Casos base de validacao de queries.
4. Relatorio simples de comparacao (tempo, linhas, custo estimado quando disponivel).
5. Wrapper PowerShell para acionar executor Python com perfil e query.

## Dependencias

1. Acesso a ambiente Redshift de teste.
2. Credenciais seguras (arquivo local nao versionado ou variaveis de ambiente).
3. Definicao de datasets/cenarios de benchmark.

## Riscos e mitigacoes

1. Risco: credenciais expostas em arquivos versionados.
   Mitigacao: manter dados sensiveis apenas em `config/redshift-profile.local.json` ignorado pelo Git.
2. Risco: diferencas de dados invalidarem comparacoes.
   Mitigacao: padronizar datasets e congelar seeds para testes.
3. Risco: crescimento sem padrao.
   Mitigacao: estabelecer convencoes de pastas e naming desde o inicio.

## Skills eleitas para este plano

- Candidatas: `route-skills-by-context`, `maintain-planner`, `maintain-activities`, `redshift-sql-specialist`, `python-specialist`
- Executora principal (planejamento): `maintain-planner`
- Apoio: `maintain-activities`, `redshift-sql-specialist`, `python-specialist`
- Motivo: combinar governanca de plano com suporte tecnico para definicao de atividades praticas em Redshift + Python.

## Criterios de aceite do plano

1. Plano descreve objetivo, escopo, fora de escopo, entregaveis, riscos e dependencias.
2. Atividades estao definidas com status inicial e criterio de aceite.
3. Projeto possui direcionamento tecnico explicito para Python e testes de queries.

