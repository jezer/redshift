# Diagnostico simples de conexao Redshift (Python)

## Estado atual

1. Regra de firewall criada: `Allow Python Redshift 5439` (Outbound, TCP 5439, Any profile).
2. DNS resolve corretamente o host de teste.
3. Conexao TCP e Python ainda falham com `WinError 10013`.

## Passos para validar na sua maquina

1. Confirmar regra criada:
   `Get-NetFirewallRule -DisplayName "Allow Python Redshift 5439" | Format-List DisplayName,Enabled,Direction,Action,Profile`
2. Confirmar regra vinculada ao executavel correto:
   `$py=(Get-Command python).Source; Get-NetFirewallApplicationFilter -Program $py | Format-List Program`
3. Testar porta no host de teste:
   `Test-NetConnection rs-db-test.smartmart.syngenta.org -Port 5439`
4. Executar query pelo projeto:
   `powershell -ExecutionPolicy Bypass -File .\scripts\run-redshift-query.ps1 -Profile test -QueryFile queries/smoke_test.sql`

## Se ainda falhar com WinError 10013

1. Verificar se antivirus/EDR bloqueia `python.exe` para trafego de rede.
2. Verificar politica do cliente VPN (split/full tunnel e restricao por processo).
3. Testar com Python da mesma arquitetura do DBeaver/JDBC (x64) e caminho permitido.
4. Se existir proxy corporativo de banco, liberar `python.exe` para destino Redshift na politica corporativa.

## Mitigacao pragmatica

1. Enquanto a liberacao de `python.exe` nao ocorre, usar o DBeaver para validar SQL.
2. Manter este projeto para automacao e repetir o teste Python apos ajuste de politica local/corporativa.
