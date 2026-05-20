import argparse
import json
import socket
import time
from datetime import datetime
from pathlib import Path


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        raise FileNotFoundError(
            f"Arquivo de perfil nao encontrado: {config_path}. "
            "Copie config/redshift-profile.example.json para config/redshift-profile.local.json."
        )
    return json.loads(config_path.read_text(encoding="utf-8"))


def load_query(query_file: Path) -> str:
    if not query_file.exists():
        raise FileNotFoundError(f"Arquivo SQL nao encontrado: {query_file}")
    query = query_file.read_text(encoding="utf-8").strip()
    if not query:
        raise ValueError(f"Arquivo SQL vazio: {query_file}")
    return query


def resolve_host(host: str) -> list[str]:
    ips = set()
    for entry in socket.getaddrinfo(host, None):
        ip = entry[4][0]
        ips.add(ip)
    return sorted(ips)


def tcp_probe(host: str, port: int, timeout_sec: float = 4.0) -> tuple[bool, str]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_sec)
    try:
        sock.connect((host, port))
        return True, "ok"
    except Exception as exc:
        return False, repr(exc)
    finally:
        sock.close()


def run_query(
    connection_data: dict,
    query: str,
    limit_preview: int,
    ssl_enabled: bool,
    application_name: str,
) -> tuple[list[str], list[tuple], float]:
    import redshift_connector

    started = time.perf_counter()
    with redshift_connector.connect(
        host=connection_data["host"],
        port=connection_data["port"],
        database=connection_data["database"],
        user=connection_data["user"],
        password=connection_data["password"],
        ssl=ssl_enabled,
        application_name=application_name,
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchmany(limit_preview)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            elapsed_ms = (time.perf_counter() - started) * 1000
            return columns, rows, elapsed_ms


def persist_result(result: dict, project_root: Path) -> Path:
    results_dir = project_root / "results"
    results_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    profile = result.get("profile", "unknown")
    query_file = Path(result.get("query_file", "query")).stem
    filename = f"{ts}_{profile}_{query_file}.json"
    out_path = results_dir / filename
    out_path.write_text(json.dumps(result, ensure_ascii=True, default=str), encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Executa query SQL no Redshift usando perfil local.")
    parser.add_argument("--profile", default="test", help="Perfil de conexao (dev|test|prod)")
    parser.add_argument("--query-file", required=True, help="Arquivo .sql a ser executado")
    parser.add_argument(
        "--config-file",
        default="config/redshift-profile.local.json",
        help="Arquivo JSON local com perfis",
    )
    parser.add_argument("--limit-preview", type=int, default=10, help="Quantidade maxima de linhas de preview")
    parser.add_argument("--dry-run", action="store_true", help="Valida configuracao e query sem conectar")
    parser.add_argument("--diagnostic", action="store_true", help="Exibe diagnostico de rede e parametros efetivos")
    parser.add_argument("--ssl", dest="ssl_enabled", action="store_true", help="Habilita SSL na conexao")
    parser.add_argument("--no-ssl", dest="ssl_enabled", action="store_false", help="Desabilita SSL na conexao")
    parser.set_defaults(ssl_enabled=True)
    parser.add_argument("--application-name", default="syg-redshift-runner", help="Nome de aplicacao da conexao")
    parser.add_argument("--save-results", action="store_true", help="Persiste resultado em results/ com metadados")
    args = parser.parse_args()

    config = load_config(Path(args.config_file))
    profiles = config.get("profiles", {})
    profile = args.profile or config.get("default_profile", "test")
    if profile not in profiles:
        raise KeyError(f"Perfil '{profile}' nao existe no arquivo de configuracao.")

    query = load_query(Path(args.query_file))
    connection_data = profiles[profile]
    diagnostic = {
        "host": connection_data.get("host"),
        "port": connection_data.get("port"),
        "database": connection_data.get("database"),
        "user": connection_data.get("user"),
        "ssl": args.ssl_enabled,
        "application_name": args.application_name,
        "query_file": args.query_file,
    }

    if args.diagnostic:
        host = str(connection_data.get("host", ""))
        port = int(connection_data.get("port", 5439))
        ips = resolve_host(host) if host else []
        tcp_ok, tcp_msg = tcp_probe(host, port) if host else (False, "host ausente")
        result = {
            "status": "ok",
            "mode": "diagnostic",
            "profile": profile,
            "connection": diagnostic,
            "resolved_ips": ips,
            "tcp_probe_ok": tcp_ok,
            "tcp_probe_detail": tcp_msg,
        }
        print(json.dumps(result, ensure_ascii=True))
        return 0

    if args.dry_run:
        result = {
            "status": "ok",
            "mode": "dry-run",
            "profile": profile,
            "connection": diagnostic,
            "query_preview": query[:120],
        }
        print(json.dumps(result, ensure_ascii=True))
        return 0

    columns, rows, elapsed_ms = run_query(
        connection_data,
        query,
        args.limit_preview,
        args.ssl_enabled,
        args.application_name,
    )
    result = {
        "status": "ok",
        "mode": "execute",
        "profile": profile,
        "query_file": args.query_file,
        "executed_at": datetime.now().isoformat(),
        "elapsed_ms": round(elapsed_ms, 2),
        "rows_preview_count": len(rows),
        "columns": columns,
        "rows_preview": rows,
    }
    if args.save_results:
        project_root = Path(__file__).resolve().parents[2]
        saved_path = persist_result(result, project_root)
        result["saved_to"] = str(saved_path)
    print(json.dumps(result, ensure_ascii=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
