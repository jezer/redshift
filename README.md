# redshift

Projeto publico da SYG para testar solucoes de queries.

## Proposito unico

Validar, comparar e documentar abordagens de consulta SQL com foco em desempenho, corretude e reuso em cenarios de Redshift.

## Stack inicial

- Python
- SQL (Amazon Redshift)

## Planejamento

O plano e as atividades iniciais estao em `plan/`.

## Quick-start

### 1. Configurar perfil local

O projeto suporta dois caminhos de config — escolha um:

**Opcao A — Config local no projeto (gitignore ja inclui este arquivo):**
```
Copie config/redshift-profile.example.json para config/redshift-profile.local.json
Preencha host, user e password para o perfil desejado
```

**Opcao B — Config privado fora do repositorio (caminho padrao do wrapper):**
```
Copie config/redshift-profile.example.json para:
C:\codes\pv\particular\particular\segredos\syg\redshift-profile.local.json
Preencha credenciais somente neste arquivo
```

Se usar a Opcao A, passe `--ConfigFile config/redshift-profile.local.json` no wrapper.

### 2. Executar dry-run (valida config sem conectar)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run-redshift-query.ps1 -Profile test -DryRun
```

### 3. Executar diagnostico de rede

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run-redshift-query.ps1 -Profile test -Diagnostic
```

### 4. Executar smoke test

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run-redshift-query.ps1 -Profile test -QueryFile queries/smoke_test.sql
```

### 5. Executar e salvar resultado em `results/`

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run-redshift-query.ps1 -Profile test -QueryFile queries/smoke_test.sql -SaveResults
```

O arquivo JSON salvo contem: `executed_at`, `profile`, `query_file`, `elapsed_ms`, `rows_preview_count`, `columns`, `rows_preview`.

## Parametros sensiveis

- Caminho padrao de parametros privados: `C:\codes\pv\particular\particular\segredos\syg\redshift-profile.local.json`
- O repositorio publico `syg/redshift` nao deve conter senhas ou credenciais.
- `config/redshift-profile.local.json` esta no `.gitignore`.
- `results/*.json` e `results/*.csv` estao no `.gitignore`.

## Troubleshooting

### Erro: "Arquivo de perfil nao encontrado"

Causa: o arquivo de config nao existe no caminho esperado.

Solucao:
1. Verifique se o arquivo existe em `config/redshift-profile.local.json` ou no caminho privado.
2. Se estiver usando config local, passe `-ConfigFile config/redshift-profile.local.json` explicitamente.

### Erro: "Perfil 'X' nao existe no arquivo de configuracao"

Causa: o perfil (`dev`, `test`, `prod`) nao consta no JSON.

Solucao: abra o arquivo de config e confirme que a chave existe em `profiles`.

### Erro de conexao TCP / timeout

Causa: host inalcancavel, VPN inativa ou porta bloqueada.

Solucao:
1. Rode diagnostico: `-Diagnostic` mostra IPs resolvidos e resultado do TCP probe.
2. Verifique VPN do ambiente correto (dev/test/prod sao redes separadas).
3. Confirme que a porta 5439 nao esta bloqueada por firewall local.

### Erro de autenticacao (authentication failed)

Causa: usuario ou senha incorretos no perfil.

Solucao:
1. Verifique `user` e `password` no arquivo de perfil local.
2. Teste conexao via DBeaver com os mesmos dados para isolar o problema.
3. Consulte o dono do dado para credenciais atualizadas.

### Erro: "No module named 'redshift_connector'"

Causa: dependencia nao instalada.

Solucao:
```
pip install -r requirements.txt
```
