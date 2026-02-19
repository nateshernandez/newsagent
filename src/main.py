import json

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.agent import SummarizingConversationManager

from utils import get_session_manager
from ai.agent import create_agent

app = BedrockAgentCoreApp()
logger = app.logger


@app.entrypoint
async def invoke(payload, context):
    session_id = getattr(context, "session_id", "default")
    user_id = payload.get("user_id") or "default-user"
    session_manager = get_session_manager(session_id, user_id)
    conversation_manager = SummarizingConversationManager()

    agent = create_agent(
        session_manager=session_manager, conversation_manager=conversation_manager
    )

    if isinstance(payload, list):
        agent_input = payload
    else:
        agent_input = payload.get("prompt")

    try:
        result = await agent.invoke_async(agent_input)

        if result.stop_reason == "interrupt":
            yield json.dumps(
                {
                    "interrupted": True,
                    "interrupts": [
                        {"id": i.id, "name": i.name, "reason": i.reason}
                        for i in result.interrupts
                    ],
                }
            )
        else:
            yield str(result.message)
    finally:
        if session_manager is not None and hasattr(session_manager, "close"):
            session_manager.close()


if __name__ == "__main__":
    app.run()
