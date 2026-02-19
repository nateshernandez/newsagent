from bedrock_agentcore.memory.integrations.strands.config import (
    AgentCoreMemoryConfig,
    RetrievalConfig,
)
from bedrock_agentcore.memory.integrations.strands.session_manager import (
    AgentCoreMemorySessionManager,
)
from strands.session.file_session_manager import FileSessionManager

from config import get_settings


def _retrieval_config(user_id: str, session_id: str) -> dict:
    """Build retrieval config for AgentCore memory paths."""
    paths = [
        (f"/users/{user_id}/facts/", 10, 0.4),
        (f"/users/{user_id}/preferences/", 5, 0.5),
        (f"/summaries/{user_id}/{session_id}/", 5, 0.4),
    ]
    return {
        path: RetrievalConfig(top_k=k, relevance_score=score)
        for path, k, score in paths
    }


def get_session_manager(session_id: str, user_id: str):
    """Get a session manager for the given session and user ID."""
    settings = get_settings()

    if settings.app_env == "local":
        return FileSessionManager(session_id=session_id, sessions_dir=".sessions")

    if settings.bedrock_agentcore_memory_id:
        return AgentCoreMemorySessionManager(
            AgentCoreMemoryConfig(
                memory_id=settings.bedrock_agentcore_memory_id,
                session_id=session_id,
                actor_id=user_id,
                retrieval_config=_retrieval_config(user_id, session_id),
            ),
            settings.aws_region,
        )

    return None
