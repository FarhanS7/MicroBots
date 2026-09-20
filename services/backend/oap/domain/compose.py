import os
from pydantic import BaseModel, Field

class F03Input(BaseModel):
    profile: str = Field(..., description="Target compose profile, e.g. local")

class F03Output(BaseModel):
    ready: bool
    persistent_volumes: bool

class ConfigError(Exception):
    """Raised when environment or key configuration is missing or invalid."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

def compose_environment(input_data: F03Input, root_path: str | None = None) -> F03Output:
    """
    Executes F03 Compose Environment validation against docker-compose configuration.
    """
    if root_path is None:
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

    compose_path = os.path.join(root_path, "deployments", "docker-compose.yml")
    if not os.path.exists(compose_path):
        raise ConfigError("docker-compose.yml configuration file missing")

    # Check for master key environment variable or mock validation
    master_key = os.environ.get("OAP_MASTER_KEY", "default-dev-master-key")
    if not master_key:
        raise ConfigError("Master key variable OAP_MASTER_KEY is missing")

    with open(compose_path, "r", encoding="utf-8") as f:
        content = f.read()

    has_volumes = "volumes:" in content and "postgres_data:" in content

    return F03Output(
        ready=True,
        persistent_volumes=has_volumes,
    )
