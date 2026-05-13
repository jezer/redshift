# redshift

Projeto publico da SYG para testar solucoes de queries.

## Proposito unico

Validar, comparar e documentar abordagens de consulta SQL com foco em desempenho, corretude e reuso em cenarios de Redshift.

## Stack inicial

- Python
- SQL (Amazon Redshift)

## Planejamento

O plano e as atividades iniciais estao em `plan/`.

## Uso rapido (teste)

1. Copiar `config/redshift-profile.example.json` para `C:\codes\pv\particular\particular\segredos\syg\redshift-profile.local.json`.
2. Preencher credenciais somente no arquivo privado em `pv/particular`.
3. Executar dry-run:
   `powershell -ExecutionPolicy Bypass -File .\scripts\run-redshift-query.ps1 -Profile test -DryRun`
4. Executar diagnostico de rede e parametros efetivos:
   `powershell -ExecutionPolicy Bypass -File .\scripts\run-redshift-query.ps1 -Profile test -Diagnostic -ApplicationName dbeaver`
5. Executar query real:
   `powershell -ExecutionPolicy Bypass -File .\scripts\run-redshift-query.ps1 -Profile test -QueryFile queries/smoke_test.sql`

## Parametros sensiveis

- Caminho padrao de parametros privados: `C:\codes\pv\particular\particular\segredos\syg\redshift-profile.local.json`
- O repositorio publico `syg/redshift` nao deve conter senhas ou credenciais.
