from bedrock_agentcore.runtime import BedrockAgentCoreApp

from utils import get_session_manager
from ai.agent import create_agent

app = BedrockAgentCoreApp()
logger = app.logger


@app.entrypoint
async def invoke(payload, context):
    session_id = getattr(context, "session_id", "default")
    user_id = payload.get("user_id") or "default-user"
    session_manager = get_session_manager(session_id, user_id)

    agent = create_agent(session_manager=session_manager)
    stream = agent.stream_async(payload.get("prompt"))

    async for event in stream:
        if "data" in event and isinstance(event["data"], str):
            yield event["data"]


if __name__ == "__main__":
    app.run()
