# Atividades objetivas - redshift

## A001 - Preparar perfil local de conexao (ambiente TEST)

- Status: concluida
- Objetivo: configurar o projeto para usar o perfil local de conexao com foco em teste.
- Skills recomendadas: `python-specialist`, `redshift-sql-specialist`, `maintain-activities`
- Criterio de aceite:
  - Arquivo local `config/redshift-profile.local.json` criado a partir do exemplo.
  - Perfil `test` definido como padrao de execucao para smoke test.
  - Credenciais mantidas somente em arquivo local ignorado pelo Git.
- Evidencia: `config/redshift-profile.local.json` criado (gitignored); `default_profile: test`.

## A002 - Padronizar query de smoke test

- Status: concluida
- Objetivo: disponibilizar query simples para validar conectividade e retorno.
- Skills recomendadas: `redshift-sql-specialist`, `maintain-activities`
- Criterio de aceite:
  - Query `select * from public.mio02_material limit 2;` salva em `queries/smoke_test.sql`.
  - Query referenciada no fluxo de execucao Python.
- Evidencia: `queries/smoke_test.sql` ja existia com o conteudo exato.

## A003 - Implementar executor Python de queries por perfil

- Status: concluida (dry-run validado)
- Objetivo: executar query SQL usando perfil de conexao informado por parametro.
- Skills recomendadas: `python-specialist`, `redshift-sql-specialist`, `maintain-activities`
- Criterio de aceite:
  - Script Python recebe `--profile` e `--query-file`.
  - Conexao usa perfil `test` sem alterar codigo.
  - Retorno mostra tempo, total de linhas e amostra dos resultados.

## A004 - Criar wrapper PowerShell para chamada simples

- Status: concluida (dry-run validado)
- Objetivo: permitir que skills e operadores chamem Python por PowerShell sem friccao.
- Skills recomendadas: `powershell-specialist`, `python-specialist`, `maintain-activities`
- Criterio de aceite:
  - Script PowerShell em `scripts/` executa o Python com parametros de perfil/query.
  - Saida padronizada em JSON para consumo por automacao/skill.
  - Exemplo de uso documentado no README.

## A005 - Persistir resultados tecnicos necessarios

- Status: concluida
- Objetivo: registrar evidencias uteis de execucao para comparacao.
- Skills recomendadas: `python-specialist`, `maintain-activities`
- Criterio de aceite:
  - Resultado bruto salvo em `results/` (json/csv conforme modo).
  - Metadados minimos: data/hora, perfil, query, duracao, linhas.
  - Sem gravar credenciais nos arquivos de saida.
- Evidencia: `--save-results` adicionado em `run_query.py` (persist_result) e exposto em `run-redshift-query.ps1` (-SaveResults).

## A006 - Documentar uso para o projeto SYG

- Status: concluida
- Objetivo: tornar o reuso simples para qualquer atividade de query no contexto `syg`.
- Skills recomendadas: `technical-writer`, `maintain-activities`
- Criterio de aceite:
  - README com fluxo rapido: configurar perfil local, executar smoke test e ler saida.
  - Secao de troubleshooting para erro de conexao/autenticacao.
- Evidencia: README.md reescrito com quick-start (5 passos), parametros sensiveis e 5 itens de troubleshooting.

## A007 - Evoluir skill Redshift para integrar este projeto

- Status: concluida
- Objetivo: apos projeto funcional, melhorar a skill Redshift para usar `syg/redshift` como executor padrao.
- Skills recomendadas: `redshift-sql-specialist`, `powershell-specialist`, `maintain-skills`, `maintain-activities`
- Criterio de aceite:
  - Skill Redshift passa a chamar o wrapper PowerShell do projeto.
  - Skill aceita perfil (`dev|test|prod`) e arquivo SQL como parametros.
  - Skill retorna resultados necessarios para analise (linhas, tempo, status e erro quando houver).
  - Integracao limitada ao contexto `syg` sem impactar outros contextos sem plano proprio.
- Evidencia: secao "Executor padrao SYG" adicionada ao SKILL.md com tabela de parametros, saida JSON e limites de integracao.
