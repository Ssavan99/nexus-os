from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


class VaultConfigError(RuntimeError):
    """Raised when the external vault is not safely configured."""


@dataclass(frozen=True)
class VaultPaths:
    repo_root: Path
    vault_root: Path
    raw_root: Path
    wiki_root: Path


def resolve_vault_paths() -> VaultPaths:
    repo_root = repository_root()
    _load_local_env(repo_root)

    configured = os.environ.get("VAULT_PATH", "").strip()
    if not configured:
        raise VaultConfigError(
            "VAULT_PATH is missing. Set it to an absolute path outside this repo."
        )

    configured_path = Path(configured).expanduser()
    if not configured_path.is_absolute():
        raise VaultConfigError("VAULT_PATH must be an absolute path.")

    vault_root = configured_path.resolve()
    if _is_relative_to(vault_root, repo_root):
        raise VaultConfigError(
            f"VAULT_PATH must point outside this public repository. "
            f"Got {vault_root}, which is inside {repo_root}."
        )

    return VaultPaths(
        repo_root=repo_root,
        vault_root=vault_root,
        raw_root=vault_root / "raw",
        wiki_root=vault_root / "wiki",
    )


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _load_local_env(repo_root: Path) -> None:
    if os.environ.get("VAULT_PATH"):
        return

    env_path = repo_root / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if key != "VAULT_PATH":
            continue
        os.environ[key] = _clean_env_value(value)
        return


def _clean_env_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value
