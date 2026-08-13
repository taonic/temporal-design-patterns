from pathlib import Path

TASK_QUEUE = "agentic-connection-auth-wait"
SECRET_DIR = Path("/tmp/agentic-connection-auth-wait-secrets")


def secret_path(connection_id: str) -> Path:
    return SECRET_DIR / f"{connection_id}.token"


def store_secret(connection_id: str, token: str) -> None:
    SECRET_DIR.mkdir(parents=True, exist_ok=True)
    secret_path(connection_id).write_text(token, encoding="utf-8")


def load_secret(connection_id: str) -> str | None:
    path = secret_path(connection_id)
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip() or None
