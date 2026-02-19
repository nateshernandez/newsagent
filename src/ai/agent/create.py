from typing import Optional

from strands import Agent
from strands.models import BedrockModel
from strands.session.session_manager import SessionManager

from infrastructure.exa import exa_mcp_client

from .prompt import SYSTEM_PROMPT


def create_agent(
    session_manager: Optional[SessionManager] = None,
    tools: Optional[list] = None,
) -> Agent:
    """
    Creates the News Scout agent.

    Args:
        session_manager: The session manager to use for the agent.
        tools: Additional tools for the agent.
    """
    model = BedrockModel(model_id="us.amazon.nova-2-lite-v1:0")
    agent_tools: list = [exa_mcp_client] + (tools or [])
    return Agent(
        # hooks=[ExaApprovalHook()],
        model=model,
        session_manager=session_manager,
        system_prompt=SYSTEM_PROMPT,
        tools=agent_tools,
    )
